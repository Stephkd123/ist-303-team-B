from flask import Flask, render_template, request, redirect, url_for, session
import os
import requests
import pandas as pd
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'your-secret-key' #secure key in production
load_dotenv()

# API Key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

# Hardcoded user for demo purposes
USER_CREDENTIALS = {"userA": "password123"}

def get_google_travel_data(origin, destination, mode="driving"):
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(GOOGLE_MAPS_API_URL, params=params).json()
    
    if "routes" in response and response["routes"]:
        leg = response["routes"][0]["legs"][0]
        return {
            "mode": mode.capitalize(),
            "time": leg["duration"]["text"],
            "distance": leg["distance"]["text"],
            "cost": "Varies"
        }
    return None

def get_uber_estimate():
    return {"mode": "Uber", "time": "Varies", "distance": "Varies", "cost": "$10 - $25"}

def get_la_metro_data():
    return {"mode": "Public Transit", "time": "35 mins", "distance": "10 miles", "cost": "$2.50"}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if USER_CREDENTIALS.get(username) == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    results = []
    sort_option = None

    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        sort_option = request.form.get('sort_option')

        if origin and destination:
            modes = ["driving", "walking", "bicycling", "transit"]
            for mode in modes:
                data = get_google_travel_data(origin, destination, mode)
                if data:
                    results.append(data)
            results.append(get_uber_estimate())
            results.append(get_la_metro_data())

            df = pd.DataFrame(results)

            if sort_option == "Cheapest":
                results = df.sort_values(by="cost").to_dict('records')
            elif sort_option == "Fastest":
                results = df.sort_values(by="time").to_dict('records')
            elif sort_option == "Eco-Friendly":
                df = df[df["mode"].isin(["Public Transit", "Walking", "Bicycling"])]
                results = df.to_dict('records')

    return render_template("index.html", results=results, sort_option=sort_option)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
