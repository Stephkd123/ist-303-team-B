import os
import requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys (Set in .env file)
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
LA_METRO_API_KEY = os.getenv("LA_METRO_API_KEY")

# Base URLs
GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"
LA_METRO_API_URL = "https://api.metro.net/openapi.json"

# Function to fetch travel time & cost from Google Maps API
def get_google_travel_data(origin, destination, mode="driving"):
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(GOOGLE_MAPS_API_URL, params=params).json()
    
    if "routes" in response and response["routes"]:
        route = response["routes"][0]["legs"][0]
        travel_time = route["duration"]["text"]
        distance = route["distance"]["text"]
        return {"mode": mode, "time": travel_time, "distance": distance, "cost": "Varies"}
    return None

# Function to fetch Uber cost estimates (Placeholder, needs OAuth setup)
def get_uber_estimate():
    return {"mode": "Uber", "time": "Varies", "distance": "Varies", "cost": "$10 - $25"}

# Function to fetch LA Metro transit details (Placeholder, update with API call)
def get_la_metro_data():
    return {"mode": "Public Transit", "time": "35 mins", "distance": "10 miles", "cost": "$2.50"}

# Streamlit UI Setup
st.title("🚗 Travel Time & Cost Comparison App")

# User Input
origin = st.text_input("Enter starting location:")
destination = st.text_input("Enter destination:")
transport_modes = ["driving", "walking", "bicycling", "transit"]

if st.button("Compare Options"):
    if origin and destination:
        travel_data = []
        for mode in transport_modes:
            data = get_google_travel_data(origin, destination, mode)
            if data:
                travel_data.append(data)
        
        # Add Uber and LA Metro estimates
        travel_data.append(get_uber_estimate())
        travel_data.append(get_la_metro_data())
        
        df = pd.DataFrame(travel_data)
        
        # Sorting & Filtering
        sort_option = st.radio("Sort by:", ["Cheapest", "Fastest", "Eco-Friendly"], horizontal=True)
        if sort_option == "Cheapest":
            df = df.sort_values(by=["cost"])
        elif sort_option == "Fastest":
            df = df.sort_values(by=["time"])
        elif sort_option == "Eco-Friendly":
            df = df[df["mode"].isin(["Public Transit", "Walking", "Bicycling"])]
        
        # Display Data
        st.subheader("Travel Options")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Please enter both starting location and destination!")