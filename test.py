from db_connection import get_connection

conn = get_connection()
if conn:
    print("✅ Connected to local PostgreSQL!")
    conn.close()
