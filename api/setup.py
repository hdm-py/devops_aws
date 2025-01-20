# setup.py
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_NAME = os.getenv("DATABASE")
PASSWORD = os.getenv("PASSWORD")


def get_connection():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user="postgres",  # change if needed
        password=PASSWORD,
        host=os.getenv("DB_HOST", "localhost"),  # Use the DB_HOST variable
        port=os.getenv("DB_PORT", "5432"),  # Use the DB_PORT variable
    )


def create_tables():
    con = get_connection()
    create_user_table_query = """ CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE
    )
    """

    create_genre_table_query = """
    CREATE TABLE IF NOT EXISTS genres(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE
    )
    """

    create_movies_table_query = """
    CREATE TABLE IF NOT EXISTS movies(
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) UNIQUE,
        release_date DATE,
        genre_id INT REFERENCES genres(id)
    )
    """

    watchlist = """
    CREATE TABLE IF NOT EXISTS watchlist(
        user_id INT REFERENCES users(id),
        movie_id INT REFERENCES movies(id),
        added_date DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY(user_id, movie_id)
    )
    """

    reviews = """
    CREATE TABLE IF NOT EXISTS reviews(
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        movie_id INT REFERENCES movies(id),
        rating INT,
        review_text TEXT,
        review_date DATE DEFAULT CURRENT_DATE
    )
    """

    with con:
        with con.cursor() as cursor:
            cursor.execute(create_user_table_query)
            cursor.execute(create_genre_table_query)
            cursor.execute(create_movies_table_query)
            cursor.execute(reviews)
            cursor.execute(watchlist)


if __name__ == "__main__":
    # Only reason to execute this file would be to create new tables, meaning it serves a migration file
    create_tables()
    print("Tables created successfully.")
