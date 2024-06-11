import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import xmltodict
import json
import time
import threading

# Constants for file names and paths
FILENAME_XML = "train_data.xml"
FILENAME_JSON = "train_data.json"
DATA_DIR = "../data/"

def get_abs_path(relative_path):
    """Returns the absolute path for a given relative path."""
    my_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(my_path, relative_path)

def load_data(url, path):
    """Downloads data from a URL and saves it to a file."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    with open(path, "w", encoding="utf-8") as file:
        file.write(response.text)

    now = datetime.now()
    print(f"Loaded training data into file {os.path.basename(path)} at: {now.strftime('%d/%m/%Y %H:%M:%S')}")

def xml_to_json(xml_path, json_path):
    """Converts an XML file to a JSON file."""
    with open(xml_path, "r", encoding="utf-8") as file:
        xml_data = file.read()

    data_dict = xmltodict.parse(xml_data)
    json_data = json.dumps(data_dict, indent=4)

    with open(json_path, "w", encoding="utf-8") as file:
        file.write(json_data)

def fetch_and_convert_data():
    load_dotenv()
    url = os.getenv('URL')

    if not url:
        raise Exception("No URL given")

    xml_path = get_abs_path(os.path.join(DATA_DIR, FILENAME_XML))
    json_path = get_abs_path(os.path.join(DATA_DIR, FILENAME_JSON))

    while True:
        load_data(url, xml_path)
        xml_to_json(xml_path, json_path)
        time.sleep(15 * 60)  # Wait for 15 minutes

def start_data_thread():
    data_thread = threading.Thread(target=fetch_and_convert_data)
    data_thread.daemon = True
    data_thread.start()
