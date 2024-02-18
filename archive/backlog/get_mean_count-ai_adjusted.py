"""
Get Mean Count
This script processes .db files containing tweet data and sentiment analysis results,
aggregates the data, and saves the output in JSON format for further analysis.
"""

import os
import sqlite3
import pandas as pd
import json
import logging
from typing import List, Dict, Optional
from main import get_data

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve configuration data
CONFIG = get_data()
root, data_path, presidents, cities, countries, years, colors = CONFIG

# Constants
DB_EXTENSION = '.db'
JSON_EXTENSION = '.json'
RESULTS_DIR = 'results'

def get_db_files(root_dir: str) -> List[str]:
    """
    Find all .db files in the directory.

    Args:
    root_dir: The directory to search for .db files.

    Returns:
    A list of file paths.
    """
    db_files = []
    for subdir, _, files in os.walk(root_dir):
        db_files += [os.path.join(subdir, file) for file in files if file.endswith(DB_EXTENSION) and not file.startswith('.')]
    return db_files

def get_compound_stats(db_file: str) -> Dict[str, float]:
    """
    Calculate the total and average compound sentiment from a database.

    Args:
    db_file: The path to the SQLite database file.

    Returns:
    A dictionary with the total and average compound sentiment.
    """
    query = """
        SELECT SUM(Compound) AS total_compound, COUNT(*) AS count 
        FROM tweets 
        INNER JOIN sentiment USING (item_number) 
        INNER JOIN LIWC USING (item_number) 
        LEFT JOIN place USING (place_id)
        WHERE country_code IN ('GB', 'US', '') OR country_code IS NULL
    """
    try:
        with sqlite3.connect(db_file) as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0].to_dict() if not df.empty else {"total_compound": 0.0, "count": 0}
    except sqlite3.DatabaseError as e:
        logging.error(f"Database error in file {db_file}: {e}")
        return {"total_compound": 0.0, "count": 0}
    except Exception as e:
        logging.error(f"An error occurred with file {db_file}: {e}")
        return {"total_compound": 0.0, "count": 0}

def save_results(data: Dict, filename: str) -> None:
    """
    Save data to a JSON file.

    Args:
    data: The data to be saved.
    filename: The name of the file to save the data to.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)
        logging.info(f"Results saved to {filename}")
    except IOError as e:
        logging.error(f"Failed to save data to {filename}: {e}")

def calculate_weighted_mean(json_files: List[str]) -> Optional[float]:
    """
    Calculate the weighted mean from JSON files.

    Args:
    json_files: A list of JSON file paths.

    Returns:
    The weighted mean or None if no data is found.
    """
    weighted_sum = 0.0
    total_weights = 0
    for file_name in json_files:
        file_path = os.path.join(RESULTS_DIR, f'{file_name}_mean_count{JSON_EXTENSION}')
        data = load_json_data(file_path)
        weighted_sum += data['overall_mean'] * data['total_count']
        total_weights += data['total_count']

    return weighted_sum / total_weights if total_weights > 0 else None

def load_json_data(file_path: str) -> Dict:
    """
    Load data from a JSON file.

    Args:
    file_path: The path to the JSON file.

    Returns:
    The data from the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except IOError as e:
        logging.error(f"Failed to load data from {file_path}: {e}")
        return {}

def process_city_files(db_files):
    total_compound, total_count = 0, 0
    for db_file in db_files:
        stats = get_compound_stats(db_file)
        total_compound += stats['total_compound']
        total_count += stats['count']
    overall_mean = total_compound / total_count if total_count else None
    return {"overall_mean": overall_mean, "total_count": total_count}

def process_countries(city_country_relation):
    country_means = {}
    for country, city_files in city_country_relation.items():
        country_files = [f'{city}_mean_count' for city in city_files]
        country_means[country] = calculate_weighted_mean(country_files)
    return country_means

def process_all_tweets(root_dir):
    db_files = get_db_files(root_dir)
    return process_city_files(db_files)

if __name__ == "__main__":
    # Process each city and calculate the mean compound sentiment
    for city in cities:
        logging.info(f'Processing city: {city}')
        city_db_files = get_db_files(f'{root}{city}/')
        city_stats = process_city_files(city_db_files)
        save_results(city_stats, f'{RESULTS_DIR}/{city}_mean_count{JSON_EXTENSION}')

    # Calculate the weighted mean compound sentiment for each country
    city_country_relation = {
        'Great Britain': [
            'Birmingham',
            'London'
        ],
        'US': [
            'LA',
            'NYC'
        ]
    }
    country_means = process_countries(city_country_relation)
    save_results(country_means, f'{RESULTS_DIR}/country_mean_count{JSON_EXTENSION}')

    # Calculate the overall mean sentiment across all tweets
    overall_stats = process_all_tweets(root)
    save_results(overall_stats, f'{RESULTS_DIR}/overall_mean_count{JSON_EXTENSION}')