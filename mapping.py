from flask import Flask, request, render_template, jsonify
import requests
import folium

app = Flask(__name__)

# Use Transit.land API for public transport
TRANSIT_API_URL = "https://transit.land/api/v2/rest/stops"
# Nominatim Geocoding API
# GEOCODE_API_URL = "https://nominatim.openstreetmap.org/search"

# google maps api
GOOGLE_MAPS_API_KEY = "AIzaSyBqrXhBRKtjniEN453TybIXB0lnuawgk20"

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/get_lat_lng_from_address', methods=['GET'])
def get_lat_lng_from_address():
    address = request.args.get('address')
    
    print(f"Received geocode request for: {address}")  # Debugging print
    
    GEOCODE_API_URL = f"https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(GEOCODE_API_URL, params=params)

        # Print the raw API response to debug
        print("Geocode API Response Status:", response.status_code)
        print("Geocode API Raw Response:", response.text[:500])  # Print first 500 chars

        data = response.json()

        if "results" in data and data["results"]:
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lng = data["results"][0]["geometry"]["location"]["lng"]
            print(f" Found coordinates: {lat}, {lng}")  # Debugging print
            return jsonify({"lat": lat, "lng": lng})

        print(" No results found for address.")
        return jsonify({"error": "No results found"}), 404

    except Exception as e:
        print(" Error making geocode request:", e)
        return jsonify({"error": "Failed to retrieve location"}), 500


@app.route('/get_nearby_transport', methods=['GET'])
def get_nearby_transport():
    # Get lat/lng for pickup and dropoff locations from the query parameters
    pickup_lat = float(request.args.get('pickup_lat'))
    pickup_lng = float(request.args.get('pickup_lng'))
    dropoff_lat = float(request.args.get('dropoff_lat'))
    dropoff_lng = float(request.args.get('dropoff_lng'))
    
    # Fetch nearby public transport stops for pickup location
    pickup_params = {
        "lat": pickup_lat,
        "lon": pickup_lng,
        "radius": 1000  # 1 km radius
    }
    pickup_response = requests.get(TRANSIT_API_URL, params=pickup_params)
    pickup_data = pickup_response.json()
    pickup_stops = pickup_data.get("stops", [])

    # Fetch nearby public transport stops for dropoff location
    dropoff_params = {
        "lat": dropoff_lat,
        "lon": dropoff_lng,
        "radius": 1000  # 1 km radius
    }
    dropoff_response = requests.get(TRANSIT_API_URL, params=dropoff_params)
    dropoff_data = dropoff_response.json()
    dropoff_stops = dropoff_data.get("stops", [])

    # Create an interactive map centered at the pickup location
    m = folium.Map(location=[pickup_lat, pickup_lng], zoom_start=15)
    
    # Marker for the pickup location
    folium.Marker([pickup_lat, pickup_lng], tooltip="Pickup Location", icon=folium.Icon(color='blue')).add_to(m)
    
    # Marker for the dropoff location
    folium.Marker([dropoff_lat, dropoff_lng], tooltip="Dropoff Location", icon=folium.Icon(color='red')).add_to(m)

    # Add markers for nearby public transport stations at the pickup location
    for stop in pickup_stops:
        stop_lat = stop['geometry']['coordinates'][1]
        stop_lng = stop['geometry']['coordinates'][0]
        folium.Marker(
            [stop_lat, stop_lng],
            tooltip=stop['name'],
            icon=folium.Icon(color='green')
        ).add_to(m)

    # Add markers for nearby public transport stations at the dropoff location
    for stop in dropoff_stops:
        stop_lat = stop['geometry']['coordinates'][1]
        stop_lng = stop['geometry']['coordinates'][0]
        folium.Marker(
            [stop_lat, stop_lng],
            tooltip=stop['name'],
            icon=folium.Icon(color='orange')
        ).add_to(m)

    # Return the map as HTML representation for frontend
    map_html = m._repr_html_()

    return jsonify({"map": map_html, "pickup_stops": pickup_stops, "dropoff_stops": dropoff_stops})

if __name__ == '__main__':
    app.run(debug=True)
