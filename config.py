# config.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# --- API Keys & Credentials (Loaded securely from environment) ---
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = "deepseek/deepseek-chat-v3-0324:free"
OPENROUTER_SITE_URL = os.getenv("OPENROUTER_SITE_URL", "https://nextgensignals.ai")
OPENROUTER_SITE_NAME = os.getenv("OPENROUTER_SITE_NAME", "NextGen Signals")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID", "735d6963")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

# --- Content Strategy ---
CONTENT_SOURCES = {
    'Artificial Intelligence': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
    'Startups': 'https://techcrunch.com/category/startups/feed/',
    'Venture Capital': 'https://a16z.com/feed/',
    'Future Tech': 'https://hbr.org/topic/technology/feed',
    'Deep Dives': 'https://waitbutwhy.com/feed',
    'Google AI Research': 'https://ai.googleblog.com/feeds/posts/default?alt=rss',
    'OpenAI Updates': 'https://openai.com/blog/rss.xml',
    'In-Depth Tech': 'http://feeds.arstechnica.com/arstechnica/index',
    'AI News': 'https://venturebeat.com/category/ai/feed/',
    'Tech & Business': 'https://www.wired.com/category/business/feed',
    'Tech Innovation': 'https://www.fastcompany.com/technology/rss',
    'Startup Accelerator': 'https://blog.ycombinator.com/feed/',
    'VC Insights': 'https://www.sequoiacap.com/feed/',
    'Entrepreneurship': 'https://www.inc.com/rss/',
    'Societal Impact': 'https://www.exponentialview.co/feed'
}

STORYTELLING_STYLES = {
    "what_if": "Generate a 'What if...?' hook and a revelation that explores a future possibility based on the text.",
    "mind_blowing_fact": "Extract the single most mind-blowing fact or statistic and present it as a surprising revelation.",
    "problem_solution": "Frame the content as a major problem and how the technology described is the solution.",
    "historical_leap": "Present the technology as a monumental leap forward, comparing it to a major historical invention."
}

# --- Dynamic Editing Styles for A/B Testing ---
EDITING_STYLES = {
    "glassmorphism_center": {
        "description": "A calm, semi-transparent card in the center of the screen.",
        "function": "create_glassmorphism_reel",
        "font_hook": "fonts/Poppins-Bold.ttf",
        "font_revelation": "fonts/Poppins-Regular.ttf",
        "font_size_hook": 85,
        "font_size_revelation": 65,
        "text_color": "#FFFFFF",
        "card_color": "#000000",
        "card_opacity": 0.3
    },
    "kinetic_reveal": {
        "description": "Fast-paced, word-by-word animated typography.",
        "function": "create_kinetic_reel",
        "font_hook": "fonts/Poppins-Black.ttf",
        "font_revelation": "fonts/Poppins-Bold.ttf",
        "font_size_hook": 120,
        "font_size_revelation": 90,
        "text_color": "#FFFFFF",
        "highlight_color": "#00F5D4", # Electric Cyan
        "background_opacity": 0.4
    }
}

# --- Video & Asset Configuration ---
REEL_WIDTH = 1080
REEL_HEIGHT = 1920
REEL_DURATION_SECONDS = 12
LOGO_PATH = "assets/NextGen_Signals_Logo.png"
LOGO_WIDTH = 280

# --- Output & State Management ---
OUTPUT_DIR_VIDEO = "output/videos"
OUTPUT_DIR_DATA = "output/data"
ALL_POSTS_EXCEL_FILE = os.path.join(OUTPUT_DIR_DATA, "all_posts.xlsx")
STATE_FILE = os.path.join(OUTPUT_DIR_DATA, "state.json")
ANALYSIS_REPORT_FILE = os.path.join(OUTPUT_DIR_DATA, "weekly_analysis.json")
ANALYSIS_INTERVAL_DAYS = 7
