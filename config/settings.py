"""
Configuration settings for the Travel Planning Agent
Works both locally (.env) and on Streamlit Cloud (secrets.toml)
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env (local) or Streamlit secrets (cloud)
load_dotenv()

def get_secret(key, default=None):
    """Get secret from Streamlit secrets or environment variables"""
    try:
        import streamlit as st
        # Try Streamlit secrets first (when deployed)
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    # Fall back to environment variables (local development)
    return os.getenv(key, default)

# LLM Configuration
GOOGLE_API_KEY = get_secret("GOOGLE_API_KEY")

# MCP Server API Keys
ACCUWEATHER_API_KEY = get_secret("ACCUWEATHER_API_KEY")

# Application Settings
USE_MOCK_DATA = get_secret("USE_MOCK_DATA", "False").lower() == "true"

# API Endpoints
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
OPENWEATHER_FORECAST_URL = f"{OPENWEATHER_BASE_URL}/forecast"
OPENWEATHER_CURRENT_URL = f"{OPENWEATHER_BASE_URL}/weather"

# LLM Model Configuration
# Using compatible Gemini model name for current API version
GEMINI_MODEL = "gemini-1.5-flash-latest"  # Latest stable version of Gemini 1.5 Flash
LLAMA_MODEL = "meta-llama/Llama-2-7b-chat-hf"

# Temperature for LLM generation
LLM_TEMPERATURE = 0.7

# Agent Configuration
MAX_ITERATIONS = 10
VERBOSE = True
