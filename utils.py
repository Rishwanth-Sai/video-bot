import os
import aiohttp
import json
from config import BASE_API_URL,VIDEOS_DIR

async def generate_upload_url(token):
    """Fetch a pre-signed upload URL from the API."""
    headers = {"Flic-Token": token, "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_API_URL}/generate-upload-url", headers=headers) as resp:
            return await resp.json()

async def upload_video(video_path, upload_url):
    """Upload a video to the pre-signed URL."""
    async with aiohttp.ClientSession() as session:
        with open(video_path, 'rb') as file:
            async with session.put(upload_url, data=file) as resp:
                return resp.status

async def create_post(token, title, hash_id, category_id):
    """Create a new post in the system."""
    headers = {"Flic-Token": token, "Content-Type": "application/json"}
    payload = {
        "title": title,
        "hash": hash_id,
        "is_available_in_public_feed": True,
        "category_id": category_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_API_URL, headers=headers, json=payload) as resp:
            return await resp.json()

def count_downloaded_videos():
    """Count the number of .mp4 files in the videos directory."""
    if not os.path.exists(VIDEOS_DIR):
        return 0  # Return 0 if the directory doesn't exist
    
    return len([file for file in os.listdir(VIDEOS_DIR) if file.lower().endswith(".mp4")])

def load_uploaded_videos():
    """Load the list of uploaded videos from a file."""
    if os.path.exists("uploaded_videos.json"):
        with open("uploaded_videos.json", "r") as file:
            return json.load(file)
    return []

def save_uploaded_video(video_filename):
    """Log an uploaded video to the uploaded videos log."""
    uploaded_videos = load_uploaded_videos()
    uploaded_videos.append(video_filename)
    with open("uploaded_videos.json", "w") as file:
        json.dump(uploaded_videos, file)

def delete_file(file_path):
    """Delete a file from the system."""
    if os.path.exists(file_path):
        os.remove(file_path)
