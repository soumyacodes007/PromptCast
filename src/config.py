# src/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
ALCHEMYST_API_KEY = os.getenv("ALCHEMYST_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
FIRE_CRAWL_API_KEY = os.getenv("FIRE_CRAWL_API_KEY")

# ElevenLabs Voice IDs (Hard-coded as you mentioned)
# You can get these from your ElevenLabs Voice Lab
VOICE_ID_HOST = "21m00Tcm4TlvDq8ikWAM"  # Example: Rachel
VOICE_ID_GUEST = "AZnzlk1XvdvUeBnXmlld" # Example: Adam

# File Paths
ASSETS_DIR = "assets"
OUTPUT_DIR = "output"
VIDEO_TEMPLATE_PATH = os.path.join(ASSETS_DIR, "pre_recorded_video.mp4")

# Other settings
SILENCE_BETWEEN_SPEAKERS_MS = 800 # Milliseconds of silence between speakers