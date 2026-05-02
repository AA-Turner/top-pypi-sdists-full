# sprigconfig/__init__.py
"""
Public API for the SprigConfig package.

This file intentionally exposes ONLY the supported, stable API surface:

    - Config              (mapping wrapper with dotted-key access)
    - ConfigLoader        (primary config loader)
    - ConfigSingleton     (thread-safe global config cache)
    - deep_merge          (standalone merge utility, backward compatible)
    - ConfigLoadError     (all loader errors)
    - load_config()       (legacy API, now calls ConfigLoader)

    Dependency Injection (NEW):
    - ConfigValue                (field-level descriptor for lazy config binding)
    - ConfigurationProperties    (class decorator for section binding)
    - config_inject              (function parameter injection decorator)
    - instantiate                (dynamic class instantiation from config via _target_)

Backward compatibility:
    Existing projects importing:
        from sprigconfig import load_config, deep_merge
    will continue to work exactly as before.
"""

from pathlib import Path

# Core classes
from .config import Config
from .config_loader import ConfigLoader
from .config_singleton import ConfigSingleton
from .deepmerge import deep_merge
from .exceptions import ConfigLoadError

# Dependency Injection
from .injection import (
    ConfigValue,
    ConfigurationProperties,
    config_inject,
)
from .instantiate import instantiate

# ---------------------------------------------------------------------------
# Backward-compatible load_config()
# ---------------------------------------------------------------------------

def load_config(*, profile: str, config_dir: Path = None):
    """
    Legacy-compatible convenience function.

    Existing ETL-service-web code uses:
        cfg = load_config(profile="dev", config_dir=...)
    and expects a dict-like object.

    NEW behavior:
        Returns a Config object instead of a raw dict,
        but Config behaves like a Mapping and supports dotted-key access.

    This function delegates entirely to ConfigLoader.
    """
    loader = ConfigLoader(config_dir=config_dir, profile=profile)
    cfg = loader.load()

    if not isinstance(cfg, Config):
        # Should never happen, but defensive for backward compatibility
        raise ConfigLoadError("ConfigLoader.load() must return a Config object")

    return cfg


__all__ = [
    "Config",
    "ConfigLoader",
    "ConfigSingleton",
    "deep_merge",
    "ConfigLoadError",
    "load_config",
    # Dependency Injection
    "ConfigValue",
    "ConfigurationProperties",
    "config_inject",
    "instantiate",
]
