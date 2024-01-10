import os
import sqlite3
from sqlite3 import Error

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

def export_data(data, path_without_filetype, pickle=True, csv=True):
    """
    export data in a pickle and csv format
    :param data: DataFrame
    :param path_without_filetype: String filepath without the extension
    :param pickle: Bool if it should be exported as pickle
    :param csv: Bool if it should be exported as csv 
    :return: None
    """
    if pickle:
        data.to_pickle(f'{path_without_filetype}.pkl')
    if csv:
        data.to_csv(f'{path_without_filetype}.csv')

def get_data():
    root = '/Volumes/Festplatte/data-UA/'
    data_path = root + 'data/'
    presidents = ['trump', 'johnson']
    cities = ['Birmingham', 'LA', 'London', 'NYC']
    countries = ['Great Britain', 'US']
    years = [str(year) for year in range(2018, 2023)] # ['2018', '2019', '2020', '2021', '2022']
    colors = ['#910830', '#BFBFBF', '#6D0624', '#5E5E5D']
    return (root, data_path, presidents, cities, countries, years, colors)
