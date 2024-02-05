"""
Get Mean Count
This script processes .db files containing tweet data and sentiment analysis results,
aggregates the data, and saves the output in JSON format for further analysis.
"""

import json
import os
import sqlite3

import pandas as pd

from main import get_data

# Retrieve configuration data
(root, data_path, presidents, cities, countries, years, colors) = get_data()

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
        for file in files:
            if file.endswith('.db') and not file.startswith('.'):
                db_files.append(os.path.join(subdir, file))
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
    except Exception as e:
        print(f"An error occurred with file {db_file}: {e}")
    return {"total_compound": 0, "count": 0}

def save_results(dict, filename):
    import json

    # Write the dictionary to a JSON file
    with open(filename, 'w') as f:
        json.dump(dict, f)
        
    print(f"Results saved to {filename}")

# combine overall_mean compound data of US cities with the weighted mean using the total_count
def load_json_data(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_weighted_mean(json_files):
    weighted_sum = 0
    total_weights = 0

    for file_path in json_files:
        data = load_json_data(f'results/{file_path}_mean_count.json')
        weighted_sum += data['overall_mean'] * data['total_count']
        total_weights += data['total_count']

    return weighted_sum / total_weights if total_weights > 0 else None

if __name__ == "__main__":
    monthly_tweet_count = pd.DataFrame(index=cities)
    for city in cities:
        db_files = get_db_files(f'{root}{city}/')
        # Aggregate the stats
        total_compound = 0
        total_count = 0
        for db_file in db_files:
            stats = get_compound_stats(db_file)
            
            month = db_file[-10:-3] # e.g., 2018_09
            monthly_tweet_count.at[city, month] = stats['count']
            
            total_compound += stats['total_compound']
            total_count += stats['count']

        # Calculate the overall weighted mean
        if total_count > 0:
            overall_mean = total_compound / total_count
            print(f"The overall mean of the 'Compound' column is: {overall_mean}")
        else:
            print("No data to calculate the mean.")
        results = {
            "overall_mean": overall_mean,
            "total_count": total_count
        }
        save_results(results, f'results/{city}_mean_count.json')
    
    monthly_tweet_count.loc['Great Britain'] = monthly_tweet_count.loc['Birmingham'] + monthly_tweet_count.loc['London']
    monthly_tweet_count.loc['US'] = monthly_tweet_count.loc['LA'] + monthly_tweet_count.loc['NYC']
    monthly_tweet_count.loc['All'] = monthly_tweet_count.loc['Great Britain'] + monthly_tweet_count.loc['US']
    monthly_tweet_count.to_pickle('results/monthly_tweet_count.pkl')

    # Paths to the JSON files
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

    # Calculate the weighted mean compound sentiment per country
    country_means = {}
    for country, files in city_country_relation.items():
        country_means[country] = calculate_weighted_mean(files)

    save_results(country_means, filename='results/country_mean_count.json')

    # calculate the overall mean for every tweet
    db_files = get_db_files(root)

    # Aggregate the stats
    total_compound = 0
    total_count = 0
    for db_file in db_files:
        stats = get_compound_stats(db_file)
        total_compound += stats['total_compound']
        total_count += stats['count']

    # Calculate the overall weighted mean
    if total_count > 0:
        overall_mean = total_compound / total_count
        print(f"The overall mean of the 'Compound' column is: {overall_mean}")
    else:
        print("No data to calculate the mean.")

    results = {
        "overall_mean": overall_mean,
        "total_count": total_count
    }
    save_results(results, filename='results/mean_count.json')