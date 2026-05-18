"""
Central configuration module for Execra.
Modules should import settings from here instead of os.getenv().
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List

from dotenv import load_dotenv
from core.utils.env_validator import assert_env

# Load .env file
load_dotenv()

# Validate environment at startup
assert_env()


def parse_cors_origins(raw_origins: str) -> List[str]:
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


@dataclass
class Settings:
    # LLM Configuration
    LLM_BACKEND: str = "openai"
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    # Screen Capture & Detection
    SCREEN_CAPTURE_FPS: int = 2
    DETECTION_THRESHOLD: float = 0.5
    DELTA_THRESHOLD: float = 0.05

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    )

    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_AUTH: Optional[str] = None

    # Privacy Configuration
    PRIVACY_MASKING_ENABLED: bool = True
    MASKED_REGIONS: List = field(default_factory=list)
    SENSITIVE_PATTERNS: List = field(
        default_factory=lambda: [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            r"\b\d{4}-\d{4}-\d{4}-\d{4}\b",
            r"\b\d{3}-\d{2}-\d{4}\b",
            r"(?i)api_key[:=]\s*[A-Za-z0-9_\-]+",
        ]
    )

    def __post_init__(self):
        # LLM
        if val := os.getenv("LLM_BACKEND"):
            self.LLM_BACKEND = val
        if val := os.getenv("OPENAI_API_KEY"):
            self.OPENAI_API_KEY = val
        if val := os.getenv("GEMINI_API_KEY"):
            self.GEMINI_API_KEY = val

        # Screen
        if val := os.getenv("SCREEN_CAPTURE_FPS"):
            self.SCREEN_CAPTURE_FPS = int(val)
        if val := os.getenv("DETECTION_THRESHOLD"):
            self.DETECTION_THRESHOLD = float(val)
        if val := os.getenv("DELTA_THRESHOLD"):
            self.DELTA_THRESHOLD = float(val)

        # API
        if val := os.getenv("API_HOST"):
            self.API_HOST = val
        if val := os.getenv("API_PORT"):
            self.API_PORT = int(val)
        if val := os.getenv("LOG_LEVEL"):
            self.LOG_LEVEL = val
        if val := os.getenv("CORS_ORIGINS"):
            self.CORS_ORIGINS = parse_cors_origins(val)

        # Redis
        if val := os.getenv("REDIS_URL"):
            self.REDIS_URL = val
        if val := os.getenv("REDIS_PASSWORD"):
            self.REDIS_AUTH = val

        # Privacy
        if val := os.getenv("PRIVACY_MASKING_ENABLED"):
            self.PRIVACY_MASKING_ENABLED = val.lower() == "true"


# Global settings instance
settings = Settings()