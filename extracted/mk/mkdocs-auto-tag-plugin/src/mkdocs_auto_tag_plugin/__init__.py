import logging

# Set up a logger for my code to use
LOGGER = logging.getLogger("mkdocs.plugins.autotags")

def warning(message: str) -> None:
    LOGGER.warning(f"[auto-tags] {message}")


def debug(message: str, *args) -> None:
    LOGGER.debug(f"[auto-tags] {message}", *args)

# Import local files in the correct order
# from .utils import replace_regex_matches
# from .normal_badge import replace_normal_badges
from .plugin import Plugin

__all__ = ["Plugin"]
