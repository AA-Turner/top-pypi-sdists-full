# sprigconfig/deepmerge.py
"""
Shared deep merge logic for SprigConfig.

This module implements the canonical deep-merge algorithm:

    - Nested dictionaries merged recursively.
    - Lists overwrite, never append.
    - Scalars overwrite.
    - Missing keys are added.
    - Existing keys are overridden.
    - Warnings emitted unless suppress=True.

This function is intentionally free of Config/ConfigLoader logic so it
can be reused or unit-tested in isolation.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def deep_merge(base: Dict[str, Any], override: Dict[str, Any], *, suppress=False, path=""):
    """
    Recursively deep-merge override → base, modifying base in-place.

    RULES:
    - If both values are dicts → recurse.
    - If both values are lists → override entirely.
    - If override is scalar → replace.
    - If key not present in base → add.
    - If override omits keys present in base → warn unless suppress=True.

    Returns:
        The modified base dict (for chaining).
    """
    for key, value in override.items():
        current_path = f"{path}{key}"

        # Both are dicts → recursive merge
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            # Warn for missing keys (partial override)
            if not suppress:
                missing = set(base[key].keys()) - set(value.keys())
                if missing:
                    logger.warning(
                        f"Config section '{current_path}' partially overridden; "
                        f"missing keys: {missing}"
                    )

            deep_merge(base[key], value, suppress=suppress, path=current_path + ".")

        else:
            # Value replaced or added
            if key in base and base[key] != value and not suppress:
                logger.info(f"Overriding config '{current_path}'")
            elif key not in base and not suppress:
                logger.info(f"Adding new config '{current_path}'")

            # Replace or add
            base[key] = value

    return base
