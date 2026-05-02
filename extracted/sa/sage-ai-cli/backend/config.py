import json
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE = Path(__file__).resolve().parent.parent


class RuntimeConfig(BaseModel):
    default_runtime: str = "llama_cpp"
    default_threads: int = 0
    default_temperature: float = 0.3
    default_max_tokens: int = 512
    default_top_p: float = 0.95


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AI_PLATFORM_",
        extra="ignore",
        env_file=(".env", ".env.local", str(Path.home() / ".sage" / ".env")),
        env_file_encoding="utf-8",
    )
    host: str = "0.0.0.0"
    port: int = 8090
    models_dir: Path = _BASE / "models"
    config_dir: Path = _BASE / "config"
    data_dir: Path = _BASE / "data"
    log_level: str = "INFO"
    admin_token: str = ""
    # P0-6: Add dev_mode flag - when False, admin_token is required
    dev_mode: bool = True

    def validate_admin_token(self) -> bool:
        """
        P0-6: Validate admin token is set in production mode.

        Returns True if token is valid or we're in dev mode.
        """
        if self.dev_mode:
            return True
        # In production, require non-empty token of at least 16 chars
        return len(self.admin_token) >= 16

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.dev_mode
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, value):
        if value is None or value == "":
            return []
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            if text.startswith("["):
                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    pass  # Fall through to comma-separated parsing
            return [item.strip() for item in text.split(",") if item.strip()]
        return value

    def ensure_dirs(self) -> None:
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)


settings = AppSettings()
runtime_defaults = RuntimeConfig()
