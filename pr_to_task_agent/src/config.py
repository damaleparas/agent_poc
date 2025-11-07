from pydantic_settings import BaseSettings
from typing import Optional

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
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create a single, importable instance of the settings
settings = Settings()