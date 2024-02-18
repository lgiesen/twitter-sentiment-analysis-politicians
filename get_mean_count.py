"""
Get Mean Count
This script processes .db files containing tweet data and sentiment analysis results,
aggregates the data, and saves the output in JSON format for further analysis.
"""

import json
import os
import sqlite3

import pandas as pd

# Retrieve configuration data
from config import cities


def get_db_files(root_dir):
    """
    Recursively find all .db files in the given directory.
    Parameters:
        root_dir (str): Root directory to begin search for .db files.
    Returns:
        list of str: A list containing the paths to all the .db files found.
    """
    db_files = []
    for subdir, _, files in os.walk(root_dir):
        db_files.extend(
            os.path.join(subdir, file)
            for file in files
            if file.endswith('.db') and not file.startswith('.')
        )
    return db_files

def get_compound_stats(db_file):
    """
    Get the sum and count of the 'Compound' column from the SQLite database.
    Parameters:
        db_file (str): Path to the SQLite database file.
    Returns:
        dict: A dictionary with keys 'total_compound' and 'count'.
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
            return {"total_compound": 0, "count": 0} if df.empty else df.iloc[0].to_dict()
    except sqlite3.DatabaseError as e:
        print(f"Database error in file {db_file}: {e}")
        return None
    except Exception as e:
        print(f"An error occurred with file {db_file}: {e}")
        return None

def save_results(data, filename):
    """
    Save data to a JSON file.
    Parameters:
        data (dict): Data to be saved.
        filename (str): Path to the JSON file where the data will be saved.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Results saved to {filename}")

def load_json_data(file_path):
    """
    Load data from a JSON file.
    Parameters:
        file_path (str): Path to the JSON file to read.
    Returns:
        dict: The data loaded from the JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_weighted_mean(json_files):
    """
    Calculate the weighted mean from a list of JSON files containing 'overall_mean' and 'total_count'.
    Parameters:
        json_files (list): List of paths to JSON files.
    Returns:
        float: The weighted mean calculated from the files.
    """
    weighted_sum = 0
    total_weights = 0
    for file_path in json_files:
        data = load_json_data(f'results/{file_path}_mean_count.json')
        weighted_sum += data['overall_mean'] * data['total_count']
        total_weights += data['total_count']
    return weighted_sum / total_weights if total_weights > 0 else 0

if __name__ == "__main__":
    monthly_tweet_count = pd.DataFrame(index=cities)
    for city in cities:
        db_files = get_db_files(os.path.join(root, city))
        total_compound = 0
        total_count = 0
        for db_file in db_files:
            stats = get_compound_stats(db_file)
            if stats:
                month = os.path.basename(db_file)[-10:-3]  # Extract month from the filename
                monthly_tweet_count.at[city, month] = stats['count']
                total_compound += stats['total_compound']
                total_count += stats['count']

        overall_mean = total_compound / total_count if total_count > 0 else 0
        print(f"The overall mean of the 'Compound' column for {city} is: {overall_mean}")
        results = {
            "overall_mean": overall_mean,
            "total_count": total_count
        }
        save_results(results, f'results/{city}_mean_count.json')

    monthly_tweet_count.loc['Great Britain'] = monthly_tweet_count.loc['Birmingham'] + monthly_tweet_count.loc['London']
    monthly_tweet_count.loc['US'] = monthly_tweet_count.loc['LA'] + monthly_tweet_count.loc['NYC']
    monthly_tweet_count.loc['All'] = monthly_tweet_count.sum(axis=0)
    monthly_tweet_count.to_pickle('results/monthly_tweet_count.pkl')

    city_country_relation = {
        'Great Britain': [
            'Birmingham_mean_count',
            'London_mean_count'
        ],
        'US': [
            'LA_mean_count',
            'NYC_mean_count'
        ]
    }

    country_means = {
        country: calculate_weighted_mean(files)
        for country, files in city_country_relation.items()
    }
    save_results(country_means, filename='results/country_mean_count.json')

    overall_stats = {"total_compound": 0, "count": 0}
    for db_file in get_db_files(root):
        stats = get_compound_stats(db_file)
        if stats:
            overall_stats["total_compound"] += stats["total_compound"]
            overall_stats["count"] += stats["count"]

    if overall_stats["count"] > 0:
        overall_mean = overall_stats["total_compound"] / overall_stats["count"]
        print(f"The overall mean of the 'Compound' column is: {overall_mean}")
    else:
        print("No data to calculate the mean.")

    results = {
        "overall_mean": overall_mean,
        "total_count": overall_stats["count"]
    }
    save_results(results, filename='results/mean_count.json')
