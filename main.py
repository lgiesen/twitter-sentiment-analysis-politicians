import os
import sqlite3
from sqlite3 import Error

"""
This script orchestrates the database connection and data selection/collection.
"""

def get_files(dir):
    """Get all files from a directory that do not start with a '.' (hidden files).
    
    Parameters:
    - dir: Directory path as a string.
    
    Returns:
    - List of file names in the directory (excluding hidden files).
    """
    return sorted([s for s in os.listdir(dir) if not s.startswith('.')])

def create_connection(db_file):
    """Create a database connection to an SQLite database specified by db_file.
    
    Parameters:
    - db_file: Path to the database file as a string.
    
    Returns:
    - Connection object on success, None on failure.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def db_select(conn, table, limit, select='*', where='True'):
    """Query all rows in the specified table with optional conditions and limit.
    
    Parameters:
    - conn: Connection object to the database.
    - table: Table name to query.
    - limit: Maximum number of rows to return.
    - select: Columns to include in the result, defaults to '*' (all columns).
    - where: Conditional clause for filtering, defaults to 'True' (no filter).
    
    Prints the rows fetched by the query.
    """
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT {select} FROM {table} WHERE {where} LIMIT {limit}")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Error as e:
        print(f"Error executing select query: {e}")

def export_data(data, path_without_filetype, pickle=True, csv=True):
    """Export data in pickle and/or csv format.
    
    Parameters:
    - data: DataFrame to export.
    - path_without_filetype: File path without the extension.
    - pickle: Boolean, if True export as a pickle file.
    - csv: Boolean, if True export as a CSV file.
    """
    if pickle:
        data.to_pickle(f"{path_without_filetype}.pkl")
    if csv:
        data.to_csv(f"{path_without_filetype}.csv")