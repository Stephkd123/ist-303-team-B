import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import timedelta
from math import radians, cos, sin, sqrt, atan2

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Function to load GTFS data efficiently
def load_gtfs_data(gtfs_path):
    gtfs_data = {}
    if not os.path.exists(gtfs_path):
        raise FileNotFoundError(f"GTFS directory not found: {gtfs_path}")
    
    for filename in os.listdir(gtfs_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(gtfs_path, filename)
            try:
                gtfs_data[filename[:-4]] = pd.read_csv(file_path, encoding='utf-8')
                print(f"Loaded {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return gtfs_data

# Path to GTFS data
gtfs_directory = "/Users/stephenkeyen/Documents/ist-303-team-B/la_county"
gtfs_data = load_gtfs_data(gtfs_directory)

# Ensure required tables exist
required_dataframes = {"stops", "stop_times", "trips", "routes", "calendar"}
missing_dfs = required_dataframes - gtfs_data.keys()
if missing_dfs:
    raise ValueError(f"Missing GTFS data files: {missing_dfs}")

# Assign dataframes
stops_df, stop_times_df, trips_df, routes_df, calendar_df = (
    gtfs_data["stops"], gtfs_data["stop_times"], gtfs_data["trips"], gtfs_data["routes"], gtfs_data["calendar"]
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_transit_options", methods=["GET"])
def get_transit_options():
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)
    destination = request.args.get("destination")

    if user_lat is None or user_lng is None or not destination:
        return jsonify({"error": "Missing parameters"}), 400

    # Find the closest stop to the user
    user_stop = find_closest_stop(user_lat, user_lng, stops_df)
    if user_stop is None:
        return jsonify({"error": "No nearby stops found"}), 404

    # Get transit routes
    transit_options = find_transit_routes(user_stop, destination, gtfs_data)
    if not transit_options:
        return jsonify({"error": "No transit routes found"}), 404

    return jsonify({"transit_routes": transit_options})

# distance calculation using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in km

def find_closest_stop(user_lat, user_lng, stops_df):
    if stops_df.empty:
        return None
    
    stops_df["distance"] = stops_df.apply(
        lambda row: haversine(user_lat, user_lng, row["stop_lat"], row["stop_lon"]), axis=1
    )
    closest_stop = stops_df.nsmallest(1, "distance").iloc[0]
    return closest_stop.to_dict()

def find_transit_routes(start_stop, destination, gtfs_data):
    stop_times_df, trips_df, routes_df = gtfs_data["stop_times"], gtfs_data["trips"], gtfs_data["routes"]
    
    trips_from_stop = stop_times_df[stop_times_df['stop_id'] == start_stop["stop_id"]]['trip_id'].unique()
    transit_routes = []
    
    for trip_id in trips_from_stop:
        trip_stops = stop_times_df[stop_times_df['trip_id'] == trip_id].sort_values(by='stop_sequence')
        if trip_stops.empty:
            continue
        
        last_stop_info = trip_stops.iloc[-1]
        last_stop_name = stops_df.loc[stops_df['stop_id'] == last_stop_info["stop_id"], "stop_name"].values[0]
        arrival_time_at_last_stop = get_arrival_time_at_stop(trip_id, last_stop_info["stop_id"], stop_times_df)
        
        if arrival_time_at_last_stop == "Not Available":
            continue
        
        trip_info = trips_df.loc[trips_df['trip_id'] == trip_id].iloc[0]
        route_info = routes_df.loc[routes_df['route_id'] == trip_info["route_id"]].iloc[0]
        duration = calculate_duration(trip_stops.iloc[0]["departure_time"], arrival_time_at_last_stop)
        
        transit_routes.append({
            "line": route_info[" route_short_name"],
            "departure_stop": start_stop["stop_name"],
            "arrival_stop": last_stop_name,
            "departure_time": trip_stops.iloc[0]["departure_time"],
            "arrival_time": arrival_time_at_last_stop,
            "fare": "To Be Implemented",  # Placeholder
            "duration": duration,
        })
    return transit_routes

def get_arrival_time_at_stop(trip_id, stop_id, stop_times_df):
    stop_time_info = stop_times_df[(stop_times_df["trip_id"] == trip_id) & (stop_times_df["stop_id"] == stop_id)]
    return stop_time_info.iloc[0]["arrival_time"] if not stop_time_info.empty else "Not Available"

def calculate_duration(departure_time, arrival_time):
    def time_str_to_timedelta(time_str):
        hours, minutes, seconds = map(int, time_str.split(':'))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    duration = time_str_to_timedelta(arrival_time) - time_str_to_timedelta(departure_time)
    if duration.total_seconds() < 0:
        duration += timedelta(days=1)
    hours, minutes = divmod(duration.seconds, 3600)[0], divmod(duration.seconds, 60)[0] % 60
    return f"{hours:02}:{minutes:02}"

if __name__ == "__main__":
    app.run(debug=True)
