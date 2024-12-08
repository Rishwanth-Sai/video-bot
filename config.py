import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
FLIC_TOKEN = os.getenv("FLIC_TOKEN")
BASE_API_URL = "https://api.socialverseapp.com/posts"
VIDEOS_DIR = "videos" 
