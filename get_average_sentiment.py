import json
import os

import pandas as pd

from config import cities, countries, presidents

data_path = os.environ['DATAPATH']

def get_mean(filepath, col='Compound'):
    """
    Calculate the mean of a specified column from a pickled DataFrame.

    Parameters:
    - filepath: The path to the pickle file.
    - col: The column from which to calculate the mean.

    Returns:
    - The mean value as a float.
    """
    try:
        data = pd.read_pickle(filepath)
        mean = data[col].mean()
        return mean
    except FileNotFoundError as e:
        print(f"File not found {filepath}: {e}")
        return None
    except pd.errors.EmptyDataError as e:
        print(f"No data in file {filepath}: {e}")
        return None

def load_mean_count(json_filename, col=None):
    """
    Load mean and count values from a JSON file.

    Parameters:
    - json_filename: The filename of the JSON file without extension.
    - col: Specific key to retrieve from the JSON data.

    Returns:
    - The requested data if found; otherwise, None.
    """
    try:
        with open(f'results/{json_filename}.json', 'r') as file:
            data = json.load(file)
        return data.get(col) if col else data
    except json.JSONDecodeError as e:
        print(f"Error reading {json_filename}: {e}")
        return None
    except FileNotFoundError as e:
        print(f"File not found {json_filename}: {e}")
        return None

if __name__ == '__main__':
    # Initialize the DataFrame to store mean sentiment values
    means = pd.DataFrame(index=presidents + ['All'], columns=cities + countries + ['Total'])

    # Calculate and fill the DataFrame with mean sentiment values for each president and city/country
    for president in presidents:
        for city in cities:
            filepath = f'{data_path}/{president}-{city}.pkl'
            mean_city = get_mean(filepath)
            means.at[president, city] = mean_city

        for country in countries:
            filepath = f'{data_path}/{president}-{country}.pkl'
            mean_country = get_mean(filepath)
            means.at[president, country] = mean_country

        # Calculate the total mean for each president
        filepath = f'{data_path}/{president}.pkl'
        means.at[president, 'Total'] = get_mean(filepath)

    # Calculate and fill the DataFrame with overall mean values
    means.at['All', 'Total'] = load_mean_count('mean_count', 'overall_mean')
    for city in cities:
        means.at['All', city] = load_mean_count(f'{city}_mean_count', 'overall_mean')
    for country in countries:
        overall_mean = load_mean_count('country_mean_count')
        means.at['All', country] = overall_mean.get(country) if overall_mean else None

    # Export the DataFrame to both Pickle and CSV for further analysis
    filepath = f'{data_path}/results/mean_compound'
    means.to_pickle(f'{filepath}.pkl')
    means.to_csv(f'{filepath}.csv')

    print("Average sentiment analysis results successfully saved.")
