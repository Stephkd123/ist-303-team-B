from flask import Flask, render_template, request, redirect, session, url_for
import pandas as pd
import os
import googlemaps
from polyline import decode as decode_polyline

app = Flask(__name__)
app.secret_key = "supersecret"

gmaps = googlemaps.Client(key="AIzaSyBqrXhBRKtjniEN453TybIXB0lnuawgk20")
df = pd.read_excel("LA Olympics Locations.xlsx")
locations = df.to_dict(orient="records")

@app.route("/")
def start():
    return render_template("start.html")

@app.route("/from_venue", methods=["GET", "POST"])
def from_venue():
    if request.method == "POST":
        session["start"] = request.form["venue"]
        session["destination"] = request.form["destination"]
        session["mode"] = request.form.getlist("mode")
        return redirect("/map")
    return render_template("from_venue.html", locations=locations)

@app.route("/to_venue", methods=["GET", "POST"])
def to_venue():
    if request.method == "POST":
        session["start"] = request.form["start"]
        session["destination"] = request.form["venue"]
        session["mode"] = request.form.getlist("mode")
        return redirect("/map")
    return render_template("to_venue.html", locations=locations)

@app.route("/between_venues", methods=["GET", "POST"])
def between_venues():
    if request.method == "POST":
        session["start"] = request.form["start_venue"]
        session["destination"] = request.form["end_venue"]
        session["mode"] = request.form.getlist("mode")
        return redirect("/map")
    return render_template("between_venues.html", locations=locations)

@app.route("/map")
def map():
    start = session.get("start")
    destination = session.get("destination")
    modes = session.get("mode")
    directions_found = False
    duration_seconds = {}
    message = ""

    if not start or not destination or not modes:
        return redirect("/")

    try:
        origin = gmaps.geocode(start)[0]
        dest = gmaps.geocode(destination)[0]
        origin_coords = origin["geometry"]["location"]
        dest_coords = dest["geometry"]["location"]
        origin_address = origin["formatted_address"]
        dest_address = dest["formatted_address"]

        import folium
        map_obj = folium.Map(location=[origin_coords["lat"], origin_coords["lng"]], zoom_start=12)
        folium.Marker([origin_coords["lat"], origin_coords["lng"]],
                      tooltip="Start", popup=f"Start: {origin_address}",
                      icon=folium.Icon(color="blue", icon="play")).add_to(map_obj)
        folium.Marker([dest_coords["lat"], dest_coords["lng"]],
                      tooltip="Destination", popup=f"Destination: {dest_address}",
                      icon=folium.Icon(color="red", icon="flag")).add_to(map_obj)

        colors = {"walking": "blue", "transit": "green"}

        for mode in modes:
            directions = gmaps.directions(origin_address, dest_address, mode=mode,
                                          transit_mode="bus", departure_time="now")
            if directions:
                polyline = directions[0]["overview_polyline"]["points"]
                decoded = decode_polyline(polyline)
                duration_val = directions[0]["legs"][0]["duration"]["value"]
                duration_seconds[mode] = duration_val
                folium.PolyLine(locations=decoded,
                                tooltip=f"{mode.title()} - {directions[0]['legs'][0]['duration']['text']}" + (" | $1.75" if mode == "transit" else ""),
                                color=colors[mode], weight=5).add_to(map_obj)

                # Save steps only
                steps = []
                for step in directions[0]["legs"][0]["steps"]:
                    if step["travel_mode"] == "WALKING":
                        steps.append(f"Walk: {step['html_instructions']}")
                    elif step["travel_mode"] == "TRANSIT":
                        transit = step["transit_details"]
                        line = transit["line"].get("short_name", transit["line"]["name"])
                        steps.append(
                            f"Bus: Take {line} from {transit['departure_stop']['name']} to {transit['arrival_stop']['name']}")
                session[mode + "_steps"] = steps
                directions_found = True

        if directions_found:
            os.makedirs("static", exist_ok=True)
            map_obj.save("static/map.html")

            if "walking" in duration_seconds and "transit" in duration_seconds:
                w = duration_seconds["walking"]
                t = duration_seconds["transit"]
                diff = abs(w - t) // 60
                if w < t:
                    message = f"Walking is faster by {diff} minutes."
                elif w > t:
                    message = f"Public transit is faster by {diff} minutes."
                else:
                    message = f"Walking and public transit take the same amount of time" 
        else:
            return "No directions available."

    except Exception as e:
        return f"Error generating map: {str(e)}"

    return render_template("map.html", start=start, destination=destination, mode=modes, message=message)

@app.route("/steps", methods=["GET", "POST"])
def steps():
    mode = request.form.get("show_steps")
    steps = session.get(mode + "_steps", [])
    route_name = None

    if request.method == "POST" and "save_name" in request.form:
        route_name = request.form.get("save_name")
        saved = session.get("saved_routes", [])
        saved.append({
            "name": route_name,
            "start": session.get("start"),
            "destination": session.get("destination"),
            "mode": mode,
            "steps": steps
        })
        session["saved_routes"] = saved
        return render_template("steps.html", steps=steps, mode=mode.title(), route_name=route_name)

    return render_template("steps.html", steps=steps, mode=mode.title())

@app.route("/my_routes")
def my_routes():
    saved_routes = session.get("saved_routes", [])
    return render_template("my_routes.html", routes=saved_routes)

@app.route("/delete_route/<int:index>", methods=["POST"])
def delete_route(index):
    saved = session.get("saved_routes", [])
    if 0 <= index < len(saved):
        saved.pop(index)
        session["saved_routes"] = saved
    return redirect("/my_routes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")  

if __name__ == "__main__":
    app.run(debug=True)
