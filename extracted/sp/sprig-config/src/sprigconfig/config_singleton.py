# sprigconfig/config_singleton.py

from __future__ import annotations
from pathlib import Path
import threading

from .config_loader import ConfigLoader
from .config import Config
from .exceptions import ConfigLoadError


class ConfigSingleton:
    """
    Java-style singleton for SprigConfig.

    Rules:
      • initialize(profile, config_dir) MUST be called exactly once at app startup.
      • get() returns the single global Config instance.
      • Subsequent calls to initialize() with ANY arguments raise errors.
      • No component may call initialize() implicitly.
    """

    _instance: Config | None = None
    _profile: str | None = None
    _config_dir: Path | None = None

    _lock = threading.Lock()

    # ----------------------------------------------------------------------
    # PUBLIC API
    # ----------------------------------------------------------------------

    @classmethod
    def initialize(cls, *, profile: str, config_dir: str | Path) -> Config:
        # Strict input validation (NEW in RC8)
        if profile is None or str(profile).strip() == "":
            raise ConfigLoadError("Profile must be provided")

        config_dir = Path(config_dir).resolve()

        with cls._lock:
            if cls._instance is not None:
                raise ConfigLoadError(
                    "ConfigSingleton already initialized. "
                    "Calling initialize() twice is not allowed."
                )

            loader = ConfigLoader(config_dir=config_dir, profile=profile)
            cfg = loader.load()

            if not isinstance(cfg, Config):
                raise ConfigLoadError("ConfigLoader.load() did not return Config instance")

            cls._instance = cfg
            cls._profile = profile
            cls._config_dir = config_dir
            return cfg

    @classmethod
    def get(cls) -> Config:
        """
        Return the global config.

        If not initialized, this is a programming error — the application
        MUST initialize configuration during startup (e.g., create_app()).
        """
        if cls._instance is None:
            raise ConfigLoadError(
                "ConfigSingleton.get() called before initialize(). "
                "You must call ConfigSingleton.initialize(profile, config_dir) first."
            )
        return cls._instance

    @classmethod
    def _clear_all(cls):
        """
        Test fixture helper — completely reset singleton state.
        """
        with cls._lock:
            cls._instance = None
            cls._profile = None
            cls._config_dir = None
