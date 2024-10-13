import sqlite3
from tqdm import tqdm  # Make sure to import tqdm


# Create the videos table if it doesn't already exist.
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create video titles table if it doesn't already exist
    create_video_table(cursor)
    
    # Create the video_meta table if it doesn't already exist
    create_meta_table(cursor)
    
    conn.commit()
    return conn, cursor

# Function to save video information to the database
def save_videos_to_db(video_info_list, cursor):
    for video in tqdm(video_info_list, desc="Saving videos to database", unit="video"):
        cursor.execute('''
            INSERT OR IGNORE INTO videos (title, url)
            VALUES (?, ?)
        ''', (video['title'], video['url']))
        cursor.connection.commit()  # Commit after each insert for progress tracking


# Create titles table 
def create_video_table(cursor):
    # Create the videos table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        title TEXT NOT NULL,
        url TEXT NOT NULL UNIQUE
    )
    ''')
    cursor.connection.commit() # Commit the changes to the database

# Create the video_meta table if it doesn't already exist.
def create_meta_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_meta (
            id TEXT PRIMARY KEY,
            publishedAt TEXT,
            channelId TEXT,
            description TEXT,
            likes INTEGER,
            dislikes INTEGER,
            views INTEGER,
            favorites INTEGER,
            comments INTEGER,
            duration TEXT,
            thumbnail TEXT
        )
    ''')
    cursor.connection.commit()  # Commit the changes to the database


# Function to insert metadata into the database
def save_meta_to_db(meta, cursor):
    cursor.execute('''
        INSERT INTO video_meta 
        (id, publishedAt, channelId, description, likes, dislikes, views, favorites, comments, duration, thumbnail)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        meta['id'],
        meta['publishedAt'],
        meta['channelId'],
        meta['description'],
        meta['likes'],
        meta['dislikes'],
        meta['views'],
        meta['favorites'],
        meta['comments'],
        meta['duration'],
        meta.get('thumbnail', 'Not available')  # Ensure thumbnail is included
    ))
    cursor.connection.commit()


