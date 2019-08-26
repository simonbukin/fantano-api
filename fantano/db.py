"""
fantano/db.py
Handles all database operations except for lookup.
"""

import sqlite3

from fantano import get_all_yt_videos, update_batch


def open_db_connection(db_name):
    """Open a SQLite3 database connection and return it."""
    try:
        c = sqlite3.connect(db_name)
        return c
    except Exception as e:
        print('SQLite3 Database Connection Exception: {}'.format(e))


def create_table(db, create_sql):
    """Create a table with the given types and names."""
    try:
        cursor = db.cursor()
        cursor.execute(create_sql)
    except Exception as e:
        print('SQLite3 Database Creation Exception: {}'.format(e))


def insert_row(db, row):
    """Insert a row into a given db."""
    c = db.cursor()
    add = '''
        INSERT INTO fantano (videoid, rating, artist, album, description)
        VALUES (?, ?, ?, ?, ?)
    '''
    c.execute(add, row)


def create_fantano_db():
    """Create the Fantano review database."""
    db = open_db_connection('fantano.db')
    table_sql = '''
        CREATE TABLE IF NOT EXISTS fantano (
            id integer PRIMARY KEY,
            videoid TEXT,
            rating INTEGER,
            artist TEXT,
            album TEXT,
            description TEXT
        );
    '''
    create_table(db, table_sql)
    return db


def populate_fantano_db(db):
    """Fill Fantano DB with review information."""
    for videos in get_all_yt_videos():
        batch = update_batch(videos)
        for video in batch:
            insert_row(db, (video['resourceId']['videoId'],
                            video['rating'],
                            video['artist'],
                            video['album'],
                            video['description']))
            print('{} - {} - {} - {}'.format(video['resourceId']['videoId'],
                                             video['rating'],
                                             video['artist'],
                                             video['album'],
                                             ))


def create_and_populate():
    """Initialize and fill the Fantano DB"""
    db = create_fantano_db()
    populate_fantano_db(db)
    db.commit()
