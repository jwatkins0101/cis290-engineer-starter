"""
Configuration and Settings

Centralized configuration for the Lead Qualification Agent.
Students extend this as they add features.
"""

import os
from typing import Optional


class Settings:
    """Application settings loaded from environment variables."""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/agents"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Memory TTL (seconds)
    MEMORY_TTL_SECONDS: int = int(os.getenv("MEMORY_TTL_SECONDS", 90 * 24 * 60 * 60))  # 90 days

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # LLM Settings
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.0-flash")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", 0.0))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", 1000))


# Scoring thresholds
SCORE_THRESHOLDS = {
    "reject": (0, 39),
    "nurture": (40, 69),
    "qualified": (70, 100),
}

# Company size thresholds
SEGMENT_THRESHOLDS = {
    "smb": (1, 200),
    "enterprise": (201, float("inf")),
}

# Actions requiring approval
APPROVAL_REQUIRED_ACTIONS = {
    "reject_decision": True,
    "enterprise_scheduling": True,
    "send_email": True,
    "mark_spam": True,
}

# Required lead fields
REQUIRED_FIELDS = ["email", "company", "need", "timeline"]

# Scoring criteria weights (must sum to 100)
SCORING_WEIGHTS = {
    "industry_fit": 20,
    "budget": 20,
    "authority": 15,
    "need": 20,
    "timeline": 15,
    "company_size": 10,
}


# Singleton settings instance
settings = Settings()
