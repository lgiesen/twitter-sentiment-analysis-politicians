import os
import sqlite3
import time

import pandas as pd

from data_collection import export_data, get_data, get_files


def create_dataset(conn, leader_hashtags, query, president):
    """
    Create a dataset from tweets related to a specific president, using specified hashtags.
    
    Parameters:
    - conn: Connection to the SQLite database.
    - leader_hashtags: A tuple of hashtags associated with the president.
    - query: The query string for filtering tweets.
    - president: The name of the president to filter tweets for.
    
    Returns:
    - A pandas DataFrame with the relevant tweets and their analysis.
    """
    try:
        query = """
        SELECT * 
        FROM tweets 
        INNER JOIN sentiment USING (item_number) 
        INNER JOIN LIWC USING (item_number) 
        LEFT JOIN place USING (place_id)
        WHERE text LIKE ? AND (country_code = 'GB' OR country_code = 'US' OR country_code IS NULL OR country_code = '')
        """
        data_en_keywords = pd.read_sql_query(query, conn, params=(f'%{president}%',))

        assert 'Compound' in data_en_keywords.columns

        placeholder = ', '.join('?' for _ in leader_hashtags)
        query = f'SELECT DISTINCT item_number FROM hashtags WHERE text IN ({placeholder})'
        hashtags = pd.read_sql_query(query, conn, params=leader_hashtags)

        newly_relevant_hashtags = set(hashtags['item_number']) - set(data_en_keywords['item_number'])

        if newly_relevant_hashtags:
            placeholders = ', '.join('?' for _ in newly_relevant_hashtags)
            query = f"""
            SELECT * 
            FROM tweets 
            INNER JOIN sentiment USING (item_number) 
            INNER JOIN LIWC USING (item_number) 
            WHERE item_number IN ({placeholders})
            """
            tweets_by_hashtags = pd.read_sql_query(query, conn, params=tuple(newly_relevant_hashtags))
            data_en_keywords_hashtags = pd.concat([data_en_keywords, tweets_by_hashtags], ignore_index=True)
        else:
            data_en_keywords_hashtags = data_en_keywords
    except Exception as e:
        print(f"Error creating dataset for {president}: {e}")
        data_en_keywords_hashtags = pd.DataFrame()
    
    return data_en_keywords_hashtags

def process_month(root, city, year, month, president_hashtags, president, query, data_path):
    """
    Process tweets data for a specified month and city, filtering by president and hashtags.
    
    Parameters:
    - root: The root directory where data is stored.
    - city: The city for which data is being processed.
    - year: The year of the data.
    - month: The month of the data.
    - president_hashtags: Hashtags associated with the president.
    - president: The name of the president.
    - query: The query string for filtering tweets.
    - data_path: The path where processed data should be saved.
    
    Returns:
    - A DataFrame with processed data for the month, or an empty DataFrame in case of errors.
    """
    try:
        month_path = os.path.join(root, city, str(year), month)
        if not os.path.exists(month_path):
            print(f"File not found: {month_path}")
            return pd.DataFrame()

        with sqlite3.connect(month_path) as conn:
            month_dataset = create_dataset(conn, president_hashtags, query, president)
            filename = f'{city}-{year}-{month}.pkl'
            month_dataset.to_pickle(os.path.join(data_path, president, filename))
            return month_dataset
    except Exception as e:
        print(f"Error processing data for {president} in {city}, {month}/{year}: {e}")
        return pd.DataFrame()

def preprocessing(president, query):
    """
    Preprocess data for a given president and query, creating datasets for analysis.
    
    Parameters:
    - president: The name of the president.
    - query: The SQL query string used to filter tweets.
    """
    try:
        (root, data_path, _, cities, _, years, _) = get_data()
        president_hashtags = {
            'trump': ('DonaldTrump', 'Trump2024', 'MakeAmericaGreatAgain', 'Trump'),
            'johnson': ('BorisJohnson', 'UKPrimeMinister', 'ToryLeader', 'Boris')
        }.get(president, ())

        os.makedirs(os.path.join(data_path, president), exist_ok=True)

        total_iterations = len(cities) * len(years) * 12  # Assuming 12 months per year
        completed_iterations = 0
        start_time = time.time()
        all_data = []

        for city in cities:
            city_data = []
            for year in years:
                for month in get_files(os.path.join(root, city, str(year))):
                    try:
                        month_dataset = process_month(root, city, year, month, president_hashtags, president, query, data_path)
                        all_data.append(month_dataset)
                        city_data.append(month_dataset)

                        completed_iterations += 1
                        print_progress(completed_iterations, total_iterations, start_time)
                    except Exception as e:
                        print(f"Error in preprocessing loop for {president}: {e}")

            if city_data:
                city_dataset = pd.concat(city_data, ignore_index=True)
                export_data(city_dataset, os.path.join(data_path, f'{president}-{city}'))

        if all_data:
            full_dataset = pd.concat(all_data, ignore_index=True)
            export_data(full_dataset, os.path.join(data_path, f'{president}'))
    except Exception as general_e:
        print(f"General error in preprocessing for {president}: {general_e}")

def print_progress(completed_iterations, total_iterations, start_time):
    """
    Print the progress of the preprocessing step, estimating remaining time.
    
    Parameters:
    - completed_iterations: The number of iterations completed so far.
    - total_iterations: The total number of iterations expected.
    - start_time: The start time of the process.
    """
    try:
        average_time_per_iteration = (time.time() - start_time) / completed_iterations
        estimated_total_time = average_time_per_iteration * total_iterations
        estimated_time_remaining = estimated_total_time - (time.time() - start_time)
        print(f'Estimated time remaining: {estimated_time_remaining // 60} minutes, {estimated_time_remaining % 60:.2f} seconds')
    except Exception as e:
        print(f"Error printing progress: {e}")

def create_country_overview():
    """
    Generate a country overview of the sentiment analysis for each president.
    """
    try:
        for president in presidents:
            try:
                birmingham = pd.read_pickle(f'{data_path}{president}-Birmingham.pkl')
                london = pd.read_pickle(f'{data_path}{president}-London.pkl')
                la = pd.read_pickle(f'{data_path}{president}-LA.pkl')
                nyc = pd.read_pickle(f'{data_path}{president}-NYC.pkl')
            except FileNotFoundError as e:
                print(f"File not found during country overview creation for {president}: {e}")
                continue  # Skip this president if any file is missing.
            
            great_britain = pd.concat([birmingham, london], axis=0)
            us = pd.concat([la, nyc], axis=0)

            export_data(great_britain, os.path.join(data_path, f'{president}-Great Britain'))
            export_data(us, os.path.join(data_path, f'{president}-US'))
    except Exception as e:
        print(f"Error creating country overview: {e}")

if __name__ == '__main__':
    try:
        (root, data_path, presidents, cities, countries, years, colors) = get_data()
        for president in presidents:
            preprocessing(query='%trump%' if president == 'trump' else '%boris% OR text LIKE %johnson%', president=president)
        create_country_overview()
        # Caution: Using exec to run a script is risky and not recommended. Yet here I created the file myself, so I know it is safe
        exec(open('get_average_sentiment.py').read())
    except Exception as e:
        print(f"General error in main execution: {e}")
