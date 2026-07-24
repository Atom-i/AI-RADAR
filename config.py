import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')

ARXIV_KEYWORDS = [
    "inference-time compute",
    "test-time scaling",
    "chain-of-thought",
    "reasoning models",
    "multimodal AI",
    "efficient transformers",
    "speculative decoding"
]

GITHUB_QUERIES = [
    "inference-time-compute",
    "test-time-scaling",
    "reasoning",
    "chain-of-thought",
    "o1-model",
    "llm-optimization"
]

HACKERNEWS_KEYWORDS = [
    "AI", "inference", "compute", "reasoning",
    "LLM", "neural", "model", "transformer",
    "optimization", "scaling"
]

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ai_radar.db')
API_HOST = "0.0.0.0"
API_PORT = 8000
UPDATE_FREQUENCY = 6