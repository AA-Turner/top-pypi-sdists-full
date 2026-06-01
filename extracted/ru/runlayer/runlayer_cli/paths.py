"""Path utilities for Runlayer CLI."""

from pathlib import Path


def get_runlayer_dir() -> Path:
    """
    Get the base Runlayer configuration directory.

    Returns:
        Path to ~/.runlayer directory
    """
    return Path.home() / ".runlayer"
