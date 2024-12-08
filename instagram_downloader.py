import instaloader
import os
from utils import count_downloaded_videos  # Ensure count_downloaded_videos is correctly implemented

# Constants
MAX_VIDEOS_PER_PROFILE = 5  # Maximum videos to download per profile
TOTAL_DOWNLOAD_LIMIT = 10    # Total download limit

def download_instagram_videos_from_profile(loader, profile, download_path, limit):
    """
    Download videos from a specific Instagram profile using an existing session.
    """
    print(f"Searching Instagram profile: {profile}...")
    try:
        # Use Instaloader's Profile class to get the profile by username
        profile_obj = instaloader.Profile.from_username(loader.context, profile)
        
        # Get the posts from the profile
        posts = profile_obj.get_posts()

        video_count = 0  # Track videos downloaded for this profile
        for post in posts:
            if count_downloaded_videos() >= TOTAL_DOWNLOAD_LIMIT:
                print("Download limit reached. Stopping all downloads.")
                break

            if video_count >= limit:
                print(f"Reached {limit} videos for profile {profile}. Moving to next profile.")
                break

            if post.is_video:
                video_url = post.video_url  # Get the direct URL for the video
                video_filename = f"{download_path}/{post.shortcode}.mp4"

                if not os.path.exists(video_filename):
                    print(f"Downloading Instagram video: {post.shortcode}")
                    # Use Instaloader's utility to download the video file
                    loader.context.get_and_write_raw(video_url, video_filename)
                    video_count += 1  # Increment the counter for each video downloaded
                else:
                    print(f"Video {post.shortcode} already exists. Skipping.")
    except Exception as e:
        print(f"Error fetching posts from {profile}: {e}")
