"""Configuration loaded from environment variables."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field

from ghost_pc.config.schema import GHOST_HOME

logger = logging.getLogger(__name__)

# Model tier → concrete model name mapping
_MODEL_TIERS: dict[str, tuple[str, str]] = {
    # (main_model, computer_use_model)
    "flash": ("gemini-3-flash-preview", "gemini-3-flash-preview"),
    "pro": ("gemini-2.5-pro-preview-06-05", "gemini-2.5-pro-preview-06-05"),
}


def _resolve_model_tier(tier: str) -> tuple[str, str]:
    """Map a model tier name to (model, computer_use_model) strings."""
    return _MODEL_TIERS.get(tier, _MODEL_TIERS["flash"])


@dataclass(frozen=True)
class Settings:
    """Application settings — all from env vars, no config files."""

    gemini_api_key: str
    gemini_model: str = "gemini-3-flash-preview"
    # Gemini 3 Flash has native Computer Use — no separate CU model needed
    gemini_computer_use_model: str = "gemini-3-flash-preview"

    # Model tier — "flash" or "pro"
    model_tier: str = "flash"

    # Browser automation — "vision", "cdp", or "browser-use"
    browser_method: str = "vision"

    # Screen capture
    screen_fps: int = 10
    jpeg_quality: int = 70
    capture_width: int = 1280
    capture_height: int = 720

    # Streaming
    stream_port: int = 8443
    stream_mode: str = "mjpeg"  # "mjpeg" or "webrtc"

    # Security
    emergency_hotkey: str = "ctrl+alt+q"
    allowed_numbers: list[str] = field(default_factory=list)
    max_messages_per_minute: int = 30

    # Paths
    credentials_dir: str = "credentials"
    bridge_dir: str = "bridge"

    # Confirmation
    confirmation_enabled: bool = True
    confirmation_timeout: int = 120  # seconds

    # Notifications
    notifications_enabled: bool = True
    notification_watch_dirs: list[str] = field(default_factory=lambda: ["~/Downloads"])
    notification_rate_limit: int = 20  # max per day

    # Logging
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Validate settings after creation."""
        errors: list[str] = []

        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY is required")

        if self.screen_fps < 1 or self.screen_fps > 60:
            errors.append(f"screen_fps must be 1-60, got {self.screen_fps}")

        if self.jpeg_quality < 1 or self.jpeg_quality > 100:
            errors.append(f"jpeg_quality must be 1-100, got {self.jpeg_quality}")

        if self.stream_port < 1 or self.stream_port > 65535:
            errors.append(f"stream_port must be 1-65535, got {self.stream_port}")

        if self.capture_width < 320 or self.capture_height < 240:
            errors.append(
                f"capture resolution too small: {self.capture_width}x{self.capture_height}"
            )

        for num in self.allowed_numbers:
            if not num.startswith("+"):
                errors.append(f"allowed_numbers must start with '+': {num!r}")

        if errors:
            raise ValueError("Invalid settings:\n  " + "\n  ".join(errors))

    @classmethod
    def from_config(cls, **overrides: object) -> Settings:
        """Load from config file, override with env vars, then CLI kwargs.

        Priority: CLI overrides > env vars > config file > defaults.
        """
        from ghost_pc.config.schema import GhostConfig

        cfg = GhostConfig.load()

        # Start with config file values
        api_key = cfg.gemini_api_key
        tier = cfg.model_tier
        model = cfg.gemini_model
        cu_model = cfg.gemini_computer_use_model
        browser = cfg.browser_method
        fps = cfg.screen_fps
        quality = cfg.jpeg_quality
        width = cfg.capture_width
        height = cfg.capture_height
        port = cfg.stream_port
        mode = cfg.stream_mode
        hotkey = cfg.emergency_hotkey
        allowed = cfg.allowed_numbers
        max_msg = cfg.max_messages_per_minute
        creds = str(cfg.get_credentials_dir())
        bridge = str(cfg.get_bridge_dir())
        log_lvl = cfg.log_level
        conf_enabled = cfg.confirmation_enabled
        conf_timeout = cfg.confirmation_timeout
        notif_enabled = cfg.notifications_enabled
        notif_watch = cfg.notification_watch_dirs
        notif_rate = cfg.notification_rate_limit

        # Override with env vars if set
        if env_key := os.environ.get("GEMINI_API_KEY"):
            api_key = env_key
        if env_key := os.environ.get("GOOGLE_API_KEY"):
            api_key = api_key or env_key
        if v := os.environ.get("GHOST_GEMINI_MODEL"):
            model = v
        if v := os.environ.get("GHOST_SCREEN_FPS"):
            fps = int(v)
        if v := os.environ.get("GHOST_JPEG_QUALITY"):
            quality = int(v)
        if v := os.environ.get("GHOST_CAPTURE_RESOLUTION"):
            parts = v.split("x")
            if len(parts) == 2:
                width, height = int(parts[0]), int(parts[1])
        if v := os.environ.get("GHOST_STREAM_PORT"):
            port = int(v)
        if v := os.environ.get("GHOST_STREAM_MODE"):
            mode = v
        if v := os.environ.get("GHOST_EMERGENCY_HOTKEY"):
            hotkey = v
        if v := os.environ.get("GHOST_ALLOWED_NUMBERS"):
            allowed = [n.strip() for n in v.split(",") if n.strip()]
        if v := os.environ.get("GHOST_MAX_MESSAGES_PER_MINUTE"):
            max_msg = int(v)
        if v := os.environ.get("GHOST_CREDENTIALS_DIR"):
            creds = v
        if v := os.environ.get("GHOST_BRIDGE_DIR"):
            bridge = v
        if v := os.environ.get("GHOST_LOG_LEVEL"):
            log_lvl = v
        if v := os.environ.get("GHOST_MODEL_TIER"):
            tier = v
        if v := os.environ.get("GHOST_BROWSER_METHOD"):
            browser = v

        # New feature settings from env vars (override config file values)
        if v := os.environ.get("GHOST_CONFIRMATION_ENABLED"):
            conf_enabled = v.lower() not in ("false", "0", "no")
        if v := os.environ.get("GHOST_CONFIRMATION_TIMEOUT"):
            conf_timeout = int(v)
        if v := os.environ.get("GHOST_NOTIFICATIONS_ENABLED"):
            notif_enabled = v.lower() not in ("false", "0", "no")

        # Apply model tier mapping (only if model wasn't explicitly overridden)
        default_model = cfg.model_fields["gemini_model"].default
        if not os.environ.get("GHOST_GEMINI_MODEL") and cfg.gemini_model == default_model:
            model, cu_model = _resolve_model_tier(tier)

        # Override with CLI kwargs (only non-None values)
        if "gemini_api_key" in overrides and overrides["gemini_api_key"] is not None:
            api_key = str(overrides["gemini_api_key"])
        if "stream_port" in overrides and overrides["stream_port"] is not None:
            port = int(overrides["stream_port"])  # type: ignore[arg-type]
        if "screen_fps" in overrides and overrides["screen_fps"] is not None:
            fps = int(overrides["screen_fps"])  # type: ignore[arg-type]
        if "log_level" in overrides and overrides["log_level"] is not None:
            log_lvl = str(overrides["log_level"])

        settings = cls(
            gemini_api_key=api_key,
            gemini_model=model,
            gemini_computer_use_model=cu_model,
            model_tier=tier,
            browser_method=browser,
            screen_fps=fps,
            jpeg_quality=quality,
            capture_width=width,
            capture_height=height,
            stream_port=port,
            stream_mode=mode,
            emergency_hotkey=hotkey,
            allowed_numbers=allowed,
            max_messages_per_minute=max_msg,
            credentials_dir=creds,
            bridge_dir=bridge,
            confirmation_enabled=conf_enabled,
            confirmation_timeout=conf_timeout,
            notifications_enabled=notif_enabled,
            notification_watch_dirs=notif_watch,
            notification_rate_limit=notif_rate,
            log_level=log_lvl,
        )

        logger.info(
            "Settings loaded (config+env): model=%s, tier=%s, browser=%s, fps=%d, port=%d",
            settings.gemini_model,
            settings.model_tier,
            settings.browser_method,
            settings.screen_fps,
            settings.stream_port,
        )

        return settings

    @classmethod
    def from_env(cls) -> Settings:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        # Parse resolution
        resolution = os.environ.get("GHOST_CAPTURE_RESOLUTION", "1280x720")
        parts = resolution.split("x")
        width = int(parts[0]) if len(parts) == 2 else 1280
        height = int(parts[1]) if len(parts) == 2 else 720

        # Parse allowed numbers
        numbers_str = os.environ.get("GHOST_ALLOWED_NUMBERS", "")
        allowed = [n.strip() for n in numbers_str.split(",") if n.strip()]

        settings = cls(
            gemini_api_key=api_key,
            gemini_model=os.environ.get("GHOST_GEMINI_MODEL", "gemini-3-flash-preview"),
            screen_fps=int(os.environ.get("GHOST_SCREEN_FPS", "10")),
            jpeg_quality=int(os.environ.get("GHOST_JPEG_QUALITY", "70")),
            capture_width=width,
            capture_height=height,
            stream_port=int(os.environ.get("GHOST_STREAM_PORT", "8443")),
            stream_mode=os.environ.get("GHOST_STREAM_MODE", "mjpeg"),
            emergency_hotkey=os.environ.get("GHOST_EMERGENCY_HOTKEY", "ctrl+alt+q"),
            allowed_numbers=allowed,
            max_messages_per_minute=int(os.environ.get("GHOST_MAX_MESSAGES_PER_MINUTE", "30")),
            credentials_dir=os.environ.get(
                "GHOST_CREDENTIALS_DIR", str(GHOST_HOME / "credentials")
            ),
            bridge_dir=os.environ.get("GHOST_BRIDGE_DIR", str(GHOST_HOME / "bridge")),
            log_level=os.environ.get("GHOST_LOG_LEVEL", "INFO"),
        )

        logger.info(
            "Settings loaded: model=%s, fps=%d, quality=%d, port=%d",
            settings.gemini_model,
            settings.screen_fps,
            settings.jpeg_quality,
            settings.stream_port,
        )

        return settings
