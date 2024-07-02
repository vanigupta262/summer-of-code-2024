import psycopg2
from psycopg2 import sql

DB_NAME = "POS"
DB_USER = "postgres"
DB_PASSWORD = "tiger"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connection to PostgreSQL DB successful")
        return connection
    except Exception as error:
        print(f"Error: Could not connect to the PostgreSQL DB")
        print(error)
        return None
