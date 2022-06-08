import sqlite3
from sqlite3 import Error
import csv
import glob
from datetime import datetime
import os

# Current path of file
cwd = os.path.dirname(os.path.abspath(__file__))

def main():
    """Main function"""
    conn = create_connection()
    with conn:
        create_table(conn)
        insert_data(conn)

def create_connection():
    """Connect to or create our SQLite Database"""
    conn = None
    try:
        conn = sqlite3.connect(f'{cwd}/database/starling.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        return conn
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create table if not exists"""

    sql_create_table = """CREATE TABLE IF NOT EXISTS transactions (
                              transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              date TIMESTAMP,
                              counter_party TEXT,
                              reference TEXT,
                              type TEXT,
                              amount REAL,
                              balance REAL,
                              category TEXT,
                              notes TEXT,
                              UNIQUE(date, counter_party, reference, type, amount, balance, category, notes)
                              );
                                """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
        c.close()
    except Error as e:
        print(e)

def insert_data(conn):
    """extract csv data and insert into sqlite database"""
    to_db = []
    for fname in glob.glob(f'{cwd}/statements/CSV/*csv'):
        with open(fname, 'r') as f:
            dr = csv.DictReader(f)
            for i in dr:
                date = datetime.strptime(i['Date'], '%d/%m/%Y')
                date = date.strftime('%Y-%m-%d')
                to_db.append((date, i['Counter Party'], i['Reference'], i['Type'], i['Amount (GBP)'], i['Balance (GBP)'], i['Spending Category'], i['Notes']))
    
    try:
        c = conn.cursor()
        c.executemany("INSERT OR IGNORE INTO transactions (date, counter_party, reference, type, amount, balance, category, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        c.close()
    except Error as e:
        print(e)

if __name__ == '__main__':
    main()