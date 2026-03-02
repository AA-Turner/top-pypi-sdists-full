"""Plugin discovery utilities."""

from __future__ import annotations

import importlib.metadata
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


def discover_plugins(group: str, logger: logging.Logger | None = None) -> None:
    """Discover and load plugins from entry points.

    Args:
        group: Entry point group name (e.g., "plato.agents", "plato.worlds")
        logger: Optional logger for debug/warning messages
    """
    try:
        eps = importlib.metadata.entry_points(group=group)
    except TypeError:
        # Python < 3.10 compatibility
        eps = importlib.metadata.entry_points().get(group, [])

    for ep in eps:
        try:
            ep.load()
            if logger:
                logger.debug(f"Loaded plugin: {ep.name}")
        except Exception as e:
            if logger:
                logger.warning(f"Failed to load plugin '{ep.name}': {e}")
