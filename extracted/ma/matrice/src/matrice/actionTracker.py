"""Backward-compat shim: re-export symbols from action_tracker.

This module preserves the old camelCase path `matrice.actionTracker` by
re-exporting the canonical implementations from `matrice.action_tracker`.
"""

from matrice.action_tracker import ActionTracker, LocalActionTracker, _dotdict

__all__ = [
    "ActionTracker",
    "LocalActionTracker",
    "_dotdict",
]
