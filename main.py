import sqlite3
from flask import Flask , render_template, redirect, url_for, flash, request, jsonify

app = Flask(__name__)

TRANSPORT_OPTIONS = [
    {"mode": "bus", "time": 30, "cost": 2.5, "eco_friendly": True},
    {"mode": "metro", "time": 20, "cost": 3.0, "eco_friendly": True},
    {"mode": "ride_share", "time": 15, "cost": 10.0, "eco_friendly": False},
    {"mode": "bike", "time": 25, "cost": 1.0, "eco_friendly": True}
]

@app.route('/recommend', methods=['GET'])
def recommend_transport():
    preference = request.args.get('preference', 'eco_friendly')
    
    if preference == 'fastest':
        best_option = min(TRANSPORT_OPTIONS, key=lambda x: x['time'])
    elif preference == 'cheapest':
        best_option = min(TRANSPORT_OPTIONS, key=lambda x: x['cost'])
    else:  # Default to eco-friendly
        best_option = next((x for x in TRANSPORT_OPTIONS if x['eco_friendly']), TRANSPORT_OPTIONS[0])
    
    return jsonify(best_option)

if __name__ == '__main__':
    app.run(debug=True)