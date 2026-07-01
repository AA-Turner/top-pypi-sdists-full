"""
cvc.core.curator — background skill-maintenance pass (Phase 1B stub).

CVC v4.0's curator is a memory-pruning + skill-refresh sweep that runs
periodically (CLI startup, idle thresholds, etc.) to keep the agent's
sidecar state in good shape. Phase 4 will implement the actual
algorithm; for Phase 1B this is a no-op so callers can wire imports
without behaviour changes.

The Phase 1B stub honours the vendor's call signature so callers can
swap the import path with no edits.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def maybe_run_curator(
    idle_for_seconds: float = 0.0,
    *,
    force: bool = False,
    config: Optional[Dict[str, Any]] = None,
) -> None:
    """Phase 1B stub — does nothing.

    Parameters mirror the vendored signature so swapping the import
    path is a one-line change. ``idle_for_seconds=float('inf')`` (the
    CLI startup call) is a no-op by definition; we'll wire a real
    schedule in Phase 4.
    """
    return None


__all__ = ["maybe_run_curator"]
