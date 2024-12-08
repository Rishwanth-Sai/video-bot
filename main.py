import asyncio
import os
from config import FLIC_TOKEN, VIDEOS_DIR
from utils import count_downloaded_videos, load_uploaded_videos, save_uploaded_video, delete_file, generate_upload_url, upload_video, create_post
from instagram_downloader import download_instagram_videos_from_profile
from instaloader import Instaloader

MAX_VIDEOS = 10       # Maximum videos to download
PROFILES = ["_motivation_reels", "motivation.reels____"]

def create_instagram_session():
    """
    Create and return an authenticated Instaloader session.
    Tries to load a session from a file or logs in using credentials.
    """
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        raise ValueError("Instagram username or password not set in environment variables.")

    loader = Instaloader()
    print("Logging in to Instagram...")
    try:
        loader.load_session_from_file(username)  # Try loading saved session
        print("Session loaded successfully.")
    except FileNotFoundError:
        print("No existing session found. Logging in with credentials.")
        loader.login(username, password)  # Login using credentials
        loader.save_session_to_file()  # Save session for future use
        print("New session saved.")

    return loader

async def search_and_download_videos(loader):
    """
    Periodically search Instagram for videos from specific profiles.
    Stops when the video count reaches MAX_VIDEOS.
    """
    while count_downloaded_videos() < MAX_VIDEOS:
        print(f"Searching for videos... Current count: {count_downloaded_videos()}")
        for profile in PROFILES:
            try:
                download_instagram_videos_from_profile(loader, profile, VIDEOS_DIR, 5)  # Download 5 videos per profile
            except Exception as e:
                print(f"Error downloading videos from {profile}: {e}")

        await asyncio.sleep(5)  # Avoid high-frequency polling, wait for 5 seconds

async def upload_video_from_directory():
    """Upload videos from the directory that have not been uploaded yet."""
    uploaded_videos = load_uploaded_videos()

    for video_filename in os.listdir(VIDEOS_DIR):  # Loop through files in the videos directory
        video_path = os.path.join(VIDEOS_DIR, video_filename)

        if video_filename.lower().endswith(".mp4") and video_filename not in uploaded_videos:  # Check for .mp4 videos
            print(f"Uploading video: {video_filename}")
            await process_video(video_path)  # Process and upload the video
            save_uploaded_video(video_filename)  # Log the video as uploaded
            delete_file(video_path)  # Delete the video after upload

async def process_video(video_path):
    """Process a single video for upload, including generating the upload URL and creating a post."""
    try:
        print("Generating upload URL...")
        response = await generate_upload_url(FLIC_TOKEN)  # Get pre-signed URL
        upload_url = response.get("url")
        hash_id = response.get("hash")

        print("Uploading video...")
        upload_status = await upload_video(video_path, upload_url)  # Upload the video

        if upload_status == 200:  # If upload is successful
            print("Video uploaded successfully. Creating post...")
            post_response = await create_post(FLIC_TOKEN, "motivational reels", hash_id, category_id=25)  # Create post after upload
            print("Post created:", post_response)
        else:
            print("Upload failed with status:", upload_status)
    except Exception as e:
        print(f"Error processing video: {e}")

def monitor_directory():
    """Monitor the video directory for new files and upload them."""
    print("Monitoring directory for new videos...")
    asyncio.run(upload_video_from_directory())

if __name__ == "__main__":
    if not os.path.exists(VIDEOS_DIR):
        os.makedirs(VIDEOS_DIR)  # Create directory if it doesn't exist
    
    try:
        # Create a single Instagram session
        instagram_loader = create_instagram_session()

        # Start the periodic search and download loop
        asyncio.run(search_and_download_videos(instagram_loader))
    except KeyboardInterrupt:
        print("Stopped video downloader.")
    except Exception as e:
        print(f"Error: {e}")

    # Monitor directory and upload new videos
    monitor_directory()
