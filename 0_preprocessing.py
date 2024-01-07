# TODO: filter by date?; check data quality (if really from city)
# TODO: filter out retweets and potential spam
# in the London data set until April 2019 are tweets from Rotterdam and Amsterdam, so you can use country_code = 'GB' to filter the tweets.
# TODO: check data quality (same column names and tables)
# TODO: Birmingham does not have data before August 2018; the others do
# TODO: not only filter by name of president, but also by keywords; take out the %, because it might include irrelevant results

import os
import sqlite3
import time
from sqlite3 import Error

import pandas as pd


def get_files(dir):
    """ get all files from a directory 
    that do not start with a '.'
    :param dir: String
    :return: List of Strings
    """
    return sorted([s for s in os.listdir(dir) if not s.startswith('.')])

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def db_select(conn, table, limit, select = '*', where = 'True'):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f'SELECT {select} FROM {table} WHERE {where} LIMIT {limit}')

    rows = cur.fetchall()

    for row in rows:
        print(row)

def create_dataset(conn, leader_hashtags, president):
    """ create a dataset based on a database connection to the SQLite database
    :param conn: database connection
    :param leader_hashtags: Tuple of Strings
    :param president: String (either 'trump' or 'johnson')
    :return: DataFrame
    """
    # join sentiment and tweet table
    # only select english tweets
    data_en_keywords = pd.read_sql_query(
        f"""
        SELECT * 
        FROM tweets 
        INNER JOIN sentiment 
        USING (item_number) 
        WHERE (
            lang == 'en'
            AND
            text LIKE '%{president}%'
        );
        """, 
        conn)
    # alternatively: # cur.execute('SQL STATEMENT')
    # now the compounded sentiment value should be a column as well in the cursor
    assert 'Compound' in data_en_keywords.columns
    
    hashtags = pd.read_sql_query(f'SELECT DISTINCT item_number FROM hashtags WHERE text IN {leader_hashtags}', conn)
    # posts that are not present in the current data_en_keywords that has a relevant hashtag is now added to the data
    newly_relevant_hashtags = list(set(hashtags['item_number']) - set(data_en_keywords['item_number']))
    print(f'{len(newly_relevant_hashtags)} posts are relevant because of hashtags, which were not present in the dataset before.')

    tweets_by_hashtags = pd.read_sql_query(f"""
                                        SELECT * 
                                        FROM tweets INNER JOIN sentiment 
                                        USING (item_number) 
                                        WHERE (
                                            lang == 'en' 
                                            AND 
                                            item_number IN {str(tuple(newly_relevant_hashtags)).replace(',)',')')}
                                        )""", conn)
    # .replace(',)',')') because the tuple creates a comma at the end, which disrupts the SQL statement
    print(f'There are {tweets_by_hashtags.shape[0]} tweets which are in english and are relevant by using the hashtag')
    # concat the tweets from before with the relevant hashtag-tweets
    data_en_keywords_hashtags = pd.concat([data_en_keywords, tweets_by_hashtags], axis=0)
    return data_en_keywords_hashtags



def preprocessing():
    # The files `LA/2018/month_2018_04.db` and `NYC/2020/month_2020_01_RADIUS.db` were deleted because they were empty or did not conform the data format of the other tables
    root = '/Volumes/Festplatte/data-UA/'
    data_path = root + 'data/'
    president = 'trump'
    cities = ['Birmingham', 'LA', 'London', 'NYC']
    years = [str(year) for year in range(2018, 2023)] # ['2018', '2019', '2020', '2021', '2022']
    boris_johnson_hashtags = ('BorisJohnson', 'UKPrimeMinister', 'ToryLeader', 'Boris')
    donald_trump_hashtags = ('DonaldTrump', 'Trump2024', 'MakeAmericaGreatAgain', 'Trump')
    president_hashtags = donald_trump_hashtags if president == 'trump' else boris_johnson_hashtags

    # make directory for relevant data
    if not os.path.exists(data_path):
        os.mkdir(data_path)
    
    # check how long the loop will take
    total_iterations = len(cities) * len(years) * 12  # assuming 12 months per year
    completed_iterations = 0
    start_time = time.time()

    for city in cities:
        for year in years:
            for month in get_files(f'{root}{city}/{year}/'):
                iteration_start_time = time.time()
                month_only = month[-5:-3]
                print(f'{city} - {year} - {month_only}')
                # check if file exists
                month_path = f'{root}{city}/{year}/{month}'
                assert os.path.exists(month_path)
                # create connection
                conn = create_connection(month_path)
                month_dataset = create_dataset(conn=conn, leader_hashtags=president_hashtags, president=president)
                print(f'The shape of the preprocessed data is: {month_dataset.shape}')
                # save dataset
                month_dataset_path = f'{data_path}{city}-{year}-{month_only}.pkl'
                month_dataset.to_pickle(month_dataset_path)
                # close the connection
                conn.close()

                # estimate time left of the loop
                completed_iterations += 1
                average_time_per_iteration = (time.time() - start_time) / completed_iterations
                estimated_total_time = average_time_per_iteration * total_iterations
                estimated_time_remaining = estimated_total_time - (time.time() - start_time)
                print(f'Estimated time remaining: {estimated_time_remaining // 60} minutes, {estimated_time_remaining % 60:.2f} seconds')
                print('\n')    


if __name__ == '__main__':
    preprocessing()