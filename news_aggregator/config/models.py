import os

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Model Selection
# We will iterate through these if one is unavailable or rate-limited
SLM_MODELS = [
    "google/gemma-3-27b-it:free",
    "openai/gpt-oss-120b:free", 
    "nvidia/nemotron-nano-9b-v2:free"
]

DEFAULT_MODEL = SLM_MODELS[0]
