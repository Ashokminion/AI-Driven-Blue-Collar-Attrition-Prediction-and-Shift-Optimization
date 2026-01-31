import sqlite3
import pandas as pd
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="data/shiftsync_v2.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        
        # 2. Employees Table (Dataset)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                Employee_ID TEXT PRIMARY KEY,
                Age INTEGER,
                Gender TEXT,
                Department TEXT,
                Shift_Type TEXT,
                Daily_Wages INTEGER,
                Overtime_Hours INTEGER,
                Distance_km INTEGER,
                Years_of_Service INTEGER,
                Last_Month_Leave INTEGER,
                Satisfaction INTEGER,
                Fatigue_Score REAL,
                OT_Trend TEXT,
                Leave_Trend TEXT,
                last_updated TIMESTAMP
            )
        ''')
        
        # 3. Predictions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                Employee_ID TEXT PRIMARY KEY,
                Attrition_Risk TEXT,
                Probability REAL,
                Classification TEXT,
                FOREIGN KEY(Employee_ID) REFERENCES employees(Employee_ID)
            )
        ''')

        # Insert default manager
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           ('admin', 'admin123', 'Senior HR Manager'))
        
        conn.commit()
        conn.close()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def save_employees(self, df):
        conn = self.get_connection()
        df['last_updated'] = datetime.now()
        # Use append instead of replace to allow multiple uploads
        # We try to append, if there's a PK collision we could catch it, 
        # but for simplicity we'll assume new data is being added.
        # To truly upsert, we would need a more complex SQL command.
        df.to_sql('employees', conn, if_exists='append', index=False, method='multi')
        conn.close()

    def clear_employees(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees")
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()

    def get_employees(self):
        conn = self.get_connection()
        df = pd.read_sql("SELECT * FROM employees", conn)
        conn.close()
        return df

    def save_predictions(self, pred_df):
        conn = self.get_connection()
        pred_df.to_sql('predictions', conn, if_exists='replace', index=False)
        conn.close()

    def verify_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
