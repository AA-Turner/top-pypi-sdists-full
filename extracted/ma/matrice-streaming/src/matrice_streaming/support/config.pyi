"""Auto-generated stub for module: config."""
from typing import Any, Optional

from __future__ import annotations
from dataclasses import dataclass, field
import os

# Functions
def get_settings() -> Any: ...
    """
    Return the process-wide Settings singleton.
    """

# Classes
class Settings:
    """
    All gateway tunables in one place. Instantiate once at process startup.
    """

    def from_env(cls: Any) -> Any: ...
        """
        Create Settings by reading current environment.
        """

