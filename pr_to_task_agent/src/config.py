import os
from pathlib import Path
from dotenv import load_dotenv # <-- NEW
from pydantic_settings import BaseSettings
from typing import Optional

# --- NEW LINES START ---
# Build the path to the .env file (one level up from this 'src' folder)
env_path = Path('.') / '../.env'
load_dotenv(dotenv_path=env_path)
# --- NEW LINES END ---


class Settings(BaseSettings):
    # App config
    PROJECT_NAME: str = "PR-to-Task Agent"

    # --- LLM Settings ---
    LLM_PROVIDER: str = "gemini"  # 'gemini' or 'claude'
    GOOGLE_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # --- Tool API Keys ---
    GITHUB_TOKEN: str
    CLICKUP_TOKEN: str
    
    # ClickUp
    CLICKUP_LIST_ID: str
    CLICKUP_ASSIGNEE_ID: str

    class Config:
        # We no longer need this, 'load_dotenv' is handling it
        env_file = ".env" 
        env_file_encoding = 'utf-8'
        pass # Keep the Config class

# Create a single, importable instance of the settings
settings = Settings()