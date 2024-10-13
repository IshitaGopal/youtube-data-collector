import time
import sqlite3
from tqdm import tqdm
from googleapiclient.errors import HttpError
from youtube_infoParser import get_video_metadata, get_youtube_service
from savetoDb import save_meta_to_db
import argparse

# Main script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch metadata for all video urls in the videos table in the database")
    parser.add_argument('--db_name', type=str, help='The name of the SQLite database that has youtube urls for which metadata has to be colected.')
    
    args = parser.parse_args()
    
    # Connect to the database
    conn = sqlite3.connect(args.db_name)
    cursor = conn.cursor()

    # SQL query to fetch URLs that need metadata collection
    cursor.execute('''
        SELECT url
        FROM videos
        WHERE url NOT IN (
            SELECT 'https://www.youtube.com/watch?v=' || id
            FROM video_meta
        )
    ''')

    # Get all the URLs that need metadata collection
    urls_to_collect = [row[0] for row in cursor.fetchall()]
    num_links = len(urls_to_collect)
    api_key = 'AIzaSyDY-PgI9IdtzJmyHGH-VCi0pr676MpkuTQ'
    youtube = get_youtube_service(api_key)

    # Main loop to collect metadata for videos that haven't been processed
    for url in tqdm(urls_to_collect, desc="Collecting metadata", total=num_links):
        video_id = url.split('=')[1]  # Extract the video ID from the URL
        success = False  # Flag to indicate success
        
        while not success:  # Continue until metadata is successfully fetched
            try:
                # Fetch video metadata
                meta = get_video_metadata(video_id, youtube)
                
                if meta:  # If metadata is found, save it to the database
                    save_meta_to_db(meta, cursor)
                    success = True  # Mark as successful
                else:
                    print(f"No metadata found for video {video_id}. Skipping this video.")
                    success = True  # Skip if no metadata found

            except HttpError as e:
                if e.resp.status == 403 and "quota" in str(e):
                    print(f"Quota exceeded at video {video_id}. Sleeping for 24 hours...")
                    time.sleep(24 * 60 * 60)  # Sleep for 24 hours and try again

    # Close the database connection
    conn.close()
