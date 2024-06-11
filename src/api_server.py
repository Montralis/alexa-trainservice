from flask import Flask, jsonify
import os
import json
import threading


app = Flask(__name__)

# Constants for file names and paths
FILENAME_JSON = "train_data.json"
DATA_DIR = "../data/"

def get_abs_path(relative_path):
    """Returns the absolute path for a given relative path."""
    my_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(my_path, relative_path)

@app.route('/api/train', methods=['GET'])
def get_data():
    json_path = get_abs_path(os.path.join(DATA_DIR, FILENAME_JSON))
    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract relevant data
        journeys = data.get("ResC", {}).get("SBRes", {}).get("JourneyList", {}).get("Journey", [])
        result = []

        for journey in journeys:
            main_stop = journey.get("MainStop", {}).get("BasicStop", {})
            departure_time = main_stop.get("Dep", {}).get("Time")
            delay = main_stop.get("Dep", {}).get("Delay")
            
            result.append({
                "departure_time": departure_time,
                "delay": delay
            })

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def start_api():
    app.run(host='0.0.0.0', port=5000)

def start_api_thread():
    api_thread = threading.Thread(target=start_api)
    api_thread.daemon = True
    api_thread.start()
