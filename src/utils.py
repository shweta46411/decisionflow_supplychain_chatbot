import json
import os
import pandas as pd

# === JSON I/O ===
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# === Data File Paths ===
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")

file_paths = {
    "demands.csv": os.path.join(BASE_DIR, "demands.csv"),
    "processing.csv": os.path.join(BASE_DIR, "processing.csv"),
    "transportation.csv": os.path.join(BASE_DIR, "transportation.csv")
}

# === Optional: Load All Datasets at Once ===
def load_all_data():
    """Returns (demands_df, processing_df, transportation_df)"""
    return (
        pd.read_csv(file_paths["demands.csv"]),
        pd.read_csv(file_paths["processing.csv"]),
        pd.read_csv(file_paths["transportation.csv"])
    )
