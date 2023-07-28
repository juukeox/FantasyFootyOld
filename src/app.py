#app.py
from flask import Flask, request, jsonify, send_file, json
from flask_cors import CORS
from merge import run_table1
from algorithm import handle_request1, download_file1
import pandas as pd
import os
import json
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "Hello, world!", {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods" : "GET, POST, PUT, DELETE, OPTIONS",
        "Content-Type": "application/json",
    }

@app.route('/run-table', methods=['GET'])
def run_table():
    return run_table1()

@app.route('/api/endpoint', methods=['POST'])
def handle_request():
    handle_request1()

@app.route('/send', methods=['GET', 'POST'])
def download_file():
    download_file1()

@app.route('/calculate', methods=['POST'])
def final_data1():
    payload = request.get_json()

    team = payload['team']
    points_per_million = float(payload['value'])
    points_per_game = float(payload['efficiency'])
    recent_form = float(payload['form'])
    differential = float(payload['differential'])
    position = payload['position']
    budget = float(payload['budget'])
    team_support = float(payload['teamSupport'])

    def min_max_normalize(value, min_val, max_val):
        if min_val == max_val:
            normalized_value = 0.0  # Handle division by zero when min_val equals max_val
        else:
            normalized_value = (value - min_val) / (max_val - min_val)
        return normalized_value
    
    def normalize_pick_pct(value):
        pick_pct_cap = 3
        if value < pick_pct_cap:
            return pick_pct_cap
        else:
            return value

    final_scores = []
    normalized_scores = []

    with open("merged_data.json", "r") as file:
        merged_data = json.load(file)

    if position != "ANY":
        merged_data = {k: v for k, v in merged_data.items() if v["Position"] == position}

    prices = []
    ppgs = []
    ppms = []
    forms = []
    pick_pcts = []
    point_values = []

    for player, data in merged_data.items():
        price = float(data['Price'])
        ppg = float(data['Points per Game'])
        ppm = float(data['Points per Million'])
        form = float(data['Last 6'])
        pick_pct = float(data['Pick %'])
        points = float(data['Points'])

        prices.append(price)
        ppgs.append(ppg)
        ppms.append(ppm)
        forms.append(form)
        pick_pcts.append(pick_pct)
        point_values.append(points)

    min_price = min(prices)
    max_price = max(prices)
    min_ppg = min(ppgs)
    max_ppg = max(ppgs)
    min_ppm = min(ppms)
    max_ppm = max(ppms)
    min_form = min(forms)
    max_form = max(forms)
    min_pick_pct = min(pick_pcts)
    max_pick_pct = max(pick_pcts)
    min_points = min(point_values)
    max_points = max(point_values)

    for player, data in merged_data.items():
        team = data['Team']
        price = float(data['Price'])
        ppg = float(data['Points per Game'])
        ppm = float(data['Points per Million'])
        form = float(data['Last 6'])
        pick_pct = float(data['Pick %'])
        points = float(data['Points'])

        pick_pct = normalize_pick_pct(pick_pct)

        normalized_ppg = min_max_normalize(ppg, min_ppg, max_ppg)
        normalized_ppm = min_max_normalize(ppm, min_ppm, max_ppm)
        normalized_form = min_max_normalize(form, min_form, max_form)
        normalized_pick_pct = min_max_normalize(pick_pct, min_pick_pct, max_pick_pct)
        normalized_points = min_max_normalize(points, min_points, max_points)

        weighted_ppg = normalized_ppg * points_per_game
        weighted_ppm = normalized_ppm * points_per_million
        weighted_form = normalized_form * recent_form
        weighted_differential = (1 - normalized_pick_pct) * differential

        team_support_boost = team_support
        final_score = 0

        if team != team:
            team_support_boost = 0

        if price <= budget:
            final_score = (
                weighted_ppg
                + (1.5 * weighted_ppm)
                + weighted_form
                + (0.6 * team_support_boost)
                + (0.5 * weighted_differential)
                + (0.7 * normalized_points)
            )
        else:
            final_score = 3

        final_scores.append(final_score)

        print(f"Player: {player}")
        print(f"Price: {price}")
        print(f"PPG: {ppg}")
        print(f"PPM: {ppm}")
        print(f"Form: {form}")
        print(f"Pick Pct: {pick_pct}")
        print(f"Points: {points}")
        print(f"Final Score: {final_score}")
        print("------------------------------")    

    for final_score in final_scores:
        normalized_final_score = 100 * min_max_normalize(final_score, min(final_scores), max(final_scores))
        normalized_final_score = round(normalized_final_score, 2)
        normalized_scores.append(normalized_final_score)

    for index, value in enumerate(final_scores):
        merged_data[list(merged_data.keys())[index]]["Score"] = normalized_scores[index]

    print("merged_data:", merged_data)  # Check the updated merged_data dictionary

    with open("final_scores.json", "w") as file:
        json.dump(merged_data, file)

    return send_file("final_scores.json", as_attachment=True)


if __name__ == "__main__":
    app.run()
    