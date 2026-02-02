"""Configuration for Datafold MCP client."""

import os
from dataclasses import dataclass


@dataclass
class Config:
    """Datafold MCP configuration."""

    api_key: str
    host: str = "https://app.datafold.com"
    timeout: int = 300  # 5 minutes default timeout
    log_file: str | None = None
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        api_key = os.environ.get("DATAFOLD_API_KEY")
        if not api_key:
            raise ValueError(
                "DATAFOLD_API_KEY environment variable is required. "
                "Generate one at Datafold → Settings → Account."
            )

        return cls(
            api_key=api_key,
            host=os.environ.get("DATAFOLD_HOST", "https://app.datafold.com"),
            timeout=int(os.environ.get("DATAFOLD_TIMEOUT", "300")),
            log_file=os.environ.get("DATAFOLD_LOG_FILE"),
            log_level=os.environ.get("DATAFOLD_LOG_LEVEL", "INFO"),
        )
