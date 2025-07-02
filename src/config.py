# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ALCHEMYST_API_KEY = os.getenv("ALCHEMYST_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
FIRE_CRAWL_API_KEY = os.getenv("FIRE_CRAWL_API_KEY")

# ElevenLabs Voice IDs
VOICE_ID_HOST = "21m00Tcm4TlvDq8ikWAM"  # Example: Rachel
VOICE_ID_GUEST = "AZnzlk1XvdvUeBnXmlld" # Example: Adam

# File Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
VIDEO_TEMPLATE_PATH = os.path.join(ASSETS_DIR, "pre_recorded_video.mp4")

# Other settings
SILENCE_BETWEEN_SPEAKERS_MS = 800

# --- NEW: Podcast Personality Prompts ---
PROMPT_FLIRTY_COUPLE = """
You are a scriptwriter for a viral podcast. Your task is to write a script for a flirty Indian couple explaining a topic.
The tone should be flirty , technical and with cheesy real life examples . you should use real life flirty examples to explain the topic in a fun way. 
include all the details of that topic in 2 hours


The dialogue should alternate strictly between '[Host]:' and '[Guest]:'.
Use a SINGLE colon only. Do not include any other text, explanations, or introductions. Just the script.
The final script should be entertaining, funny, and educational in a very roundabout way.
"""

PROMPT_HUMOROUS_BROS = """
You are a scriptwriter for a hit comedy podcast. Your task is to write a script for two "bro" friends promoting a topic.
The tone should be humorous, laid-back, and full of casual banter. They should hype up the topic while playfully disrespecting and mocking competitor concepts or ideas in a satirical way.
The dialogue must alternate strictly between '[Host]:' and '[Guest]:'.
Use a SINGLE colon only. Do not include any other text or explanations. Just the script.
The final script should feel like an over-the-top, funny ad read by two best friends.
"""

PROMPT_PROFESSIONAL = """
You are a podcast scriptwriter. Your task is to create an engaging, professional interview script between a 'Host' and a 'Guest'.
The script should be based on the provided text.
Format the output clearly, with each line prefixed by either '[Host]:' or '[Guest]:'.
Use a SINGLE colon only. Do not include any other text.
"""