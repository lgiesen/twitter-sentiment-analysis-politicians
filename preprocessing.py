import os
import sqlite3
import time
import pandas as pd
from main import get_files, export_data, get_data

def create_dataset(conn, leader_hashtags, president):
    """Create a dataset based on a database connection to the SQLite database."""
    query = f"""
    SELECT * 
    FROM tweets 
    INNER JOIN sentiment USING (item_number) 
    INNER JOIN LIWC USING (item_number) 
    LEFT JOIN place USING (place_id)
    WHERE text LIKE ? AND (country_code = 'GB' OR country_code = 'US' OR country_code IS NULL OR country_code = '')
    """
    data_en_keywords = pd.read_sql_query(query, conn, params=(f'%{president}%',))

    assert 'Compound' in data_en_keywords.columns

    placeholder = '?' * len(leader_hashtags)
    query = f'SELECT DISTINCT item_number FROM hashtags WHERE text IN ({", ".join(placeholder)})'
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

    return data_en_keywords_hashtags

def process_month(root, city, year, month, president_hashtags, president, data_path):
    """Process data for a single month."""
    month_path = os.path.join(root, city, str(year), month)
    if not os.path.exists(month_path):
        print(f"File not found: {month_path}")
        return pd.DataFrame()

    with sqlite3.connect(month_path) as conn:
        month_dataset = create_dataset(conn, leader_hashtags=president_hashtags, president=president)
        filename = f'{city}-{year}-{month[-5:-3]}.pkl'
        month_dataset.to_pickle(os.path.join(data_path, president, filename))
        return month_dataset

def preprocessing(president):
    """Preprocess the whole data and create a dataset."""
    (root, data_path, _, cities, years) = get_data()
    president_hashtags = {
        'trump': ('DonaldTrump', 'Trump2024', 'MakeAmericaGreatAgain', 'Trump'),
        'johnson': ('BorisJohnson', 'UKPrimeMinister', 'ToryLeader', 'Boris')
    }.get(president, ())

    os.makedirs(os.path.join(data_path, president), exist_ok=True)

    total_iterations = len(cities) * len(years) * 12  # assuming 12 months per year
    completed_iterations = 0
    start_time = time.time()
    all_data = []

    for city in cities:
        city_data = []
        for year in years:
            for month in get_files(os.path.join(root, city, str(year))):
                month_dataset = process_month(root, city, year, month, president_hashtags, president, data_path)
                all_data.append(month_dataset)
                city_data.append(month_dataset)

                completed_iterations += 1
                print_progress(completed_iterations, total_iterations, start_time)

        export_data(pd.concat(city_data, ignore_index=True), os.path.join(data_path, f'{president}-{city}'))

    full_dataset = pd.concat(all_data, ignore_index=True)
    export_data(full_dataset, os.path.join(data_path, f'{president}'))
    

def print_progress(completed_iterations, total_iterations, start_time):
    """Print the progress of the preprocessing."""
    average_time_per_iteration = (time.time() - start_time) / completed_iterations
    estimated_total_time = average_time_per_iteration * total_iterations
    estimated_time_remaining = estimated_total_time - (time.time() - start_time)
    print(f'Estimated time remaining: {estimated_time_remaining // 60} minutes, {estimated_time_remaining % 60:.2f} seconds')

def create_country_overview():
    # president sentiment by country
    for president in presidents:
        birmingham = pd.read_pickle(f'{data_path}{president}-Birmingham.pkl')
        london = pd.read_pickle(f'{data_path}{president}-London.pkl')
        la = pd.read_pickle(f'{data_path}{president}-LA.pkl')
        nyc = pd.read_pickle(f'{data_path}{president}-NYC.pkl')
        
        great_britain = pd.concat([birmingham, london], axis=0)
        us = pd.concat([la, nyc], axis=0)
        
        export_data(great_britain, os.path.join(data_path, f'{president}-Great Britain'))
        export_data(us, os.path.join(data_path, f'{president}-US'))

if __name__ == '__main__':
    (root, data_path, presidents, cities, countries, years, colors) = get_data()
    preprocessing(president='trump')
    preprocessing(president='johnson')
    create_country_overview()
    exec(open('get_average_sentiment.py').read())