import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"Attempting to connect with: {database_url}")

try:
    conn = psycopg2.connect(database_url)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")