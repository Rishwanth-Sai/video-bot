# Video Search and Upload Bot

This Python-based bot is designed to download videos from Instagram and upload them to a server via provided APIs. It performs the following key tasks:

- Searches for videos from specified Instagram profiles.
- Downloads videos from Instagram profiles.
- Uploads videos to a server via a pre-signed URL.
- Deletes local files after successful upload.
- Monitors the videos directory for new `.mp4` files and uploads them as they appear.

## Prerequisites

Before running the bot, you need the following:

- Python 3.7 or higher.
- Instagram account credentials.
- Flic-Token from the Empowerverse app.
- API base URL for uploading videos.

## Setup Instructions

1. Clone the repository or download the files to your local machine.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file and add the following environment variables:
   ```bash
   INSTAGRAM_USERNAME=<your_instagram_username>
   INSTAGRAM_PASSWORD=<your_instagram_password>
   FLIC_TOKEN=<your_flic_token>
   ```

4. Create a folder named videos in the root directory to store downloaded videos.


## Running the Bot

To run the bot, simply execute the main.py script:
   ```bash
   python main.py
   ```

The bot will:
- Log in to Instagram.
- Start downloading videos from the specified Instagram profiles (listed in the PROFILES list).
- Upload the downloaded videos to the server.
- Monitor the videos directory and upload new files as they appear.

## Files

- **main.py** : The main script that runs the bot, handles Instagram video downloads, and uploads videos to the server.

- **instagram_downloader.py** : Contains the function to download videos from Instagram profiles.

- **utils.py** : Utility functions for video handling, API requests, and file management.

- **config.py** : Configuration for environment variables and constants.

- **requirements.txt** : List of dependencies required to run the bot.

## Usage

- **PROFILES** : List of Instagram profiles to download videos from. You can modify this list as needed.

- **MAX_VIDEOS** : Maximum number of videos to download. Default is set to 10.

- **VIDEOS_DIR** : Directory where the videos are stored. Ensure the videos directory exists or is created automatically.


## Error Handling

The bot includes basic error handling for API requests and video downloads. If an error occurs during any step, an exception will be raised with a descriptive message.