import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print("❌ Failed to connect to database:", e)
        return None

def fetch_all(query, params=None):
    conn = get_connection()
    if not conn:
        return []

    try:
        cur = conn.cursor()
        cur.execute(query, params or ())
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as e:
        print("❌ Query failed:", e)
        return []
    finally:
        conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print("❌ Query execution failed:", e)
        return False
    finally:
        conn.close()
