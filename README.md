# YouTube Channel Videos and Metadata Collection

## Overview

This project allows users to collect video titles, URLs, and metadata from a specified YouTube channel. The collected information is stored in an SQLite database.


## Setting Up API Keys
1. Get API KEy from
2. Create a file named .env in the project root directory.
3. Add Your API Key: Open the .env file and add your YouTube API key in the following format:
    ```bash
    YOUTUBE_API_KEY=your_api_key_here
    ```

## Setting Up the Environment

### Using Conda (Recommended)

1. **Create a Conda Environment**:
   ```bash
   conda env create -f environment.yml
   conda activate youtube_scraper_env
   ```
   
## Running the Scripts
1. Collect Video Titles and Links: Use the following command to collect video titles and URLs from a specified YouTube channel:
    ```bash
    python collect_titles.py --channel_name 'ChannelName' --db_name 'path_to_database.db' --max_videos 5
    ```
    - `--channel_name`: The name of the YouTube channel (e.g., "StevenWilsonHQ").
    - `--db_name`: The name of the SQLite database file (default: youtube_videos.db). Ensure the path leads to a writable location.
    - `--max_videos`: The maximum number of videos to retrieve (default: fetch all videos).

2. Collect Metadata for Videos: After collecting video titles and links, run the metadata collection script:
    ```bash
    python collect_metadata.py --db_name 'path_to_database.db'

    ```
    This script will collect metadata for all videos in the database that do not already have metadata.











