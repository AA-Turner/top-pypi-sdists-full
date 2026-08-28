"""DeepOCSORT adapter.

DeepOCSORT = OC-SORT motion core + appearance (ReID) association + optional
camera-motion compensation. This adapter previously preferred the ``boxmot``
package's ``boxmot.DeepOcSort`` implementation when installed.

**The ``boxmot`` backend has been removed.** ``boxmot`` is AGPL-3.0 (a strong
copyleft license); even as a lazily-imported, not-bundled-by-default optional
dependency, an "auto"-mode adapter that silently activates AGPL-licensed code
whenever it happens to find `boxmot` importable is not a safe posture for a
commercially-distributed/hosted product to carry, and this substrate was
already documented as "F10 v1.0 (superseded) benchmark/dev-only ... never a
runtime dependency of the shipped tracker path" before this removal -- so
nothing that was ever meant to ship depended on it. See
`matrice-hub/features/2026-07-MLOps-F10-tracker-reid/design-doc.md` Sec 12
Option A for the original tradeoff writeup this removal supersedes.

This adapter now always uses the in-repo pure-python ``AdvancedTracker`` (a
BYTE-style motion tracker, no ReID/appearance association) via
``AdvancedTrackerAdapter``. ``deep_oc_sort_backend="boxmot"`` in an existing
deployment config is accepted (not a hard failure -- avoids breaking a
deployment JSON in the wild) but only ever resolves to the fallback, with a
warning logged once.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from ..advanced_tracker import AdvancedTrackerAdapter
from ..base import BaseObjectTracker, DetectionDict
from ..config import MatriceTrackerConfig

logger = logging.getLogger(__name__)


class DeepOCSortAdapter(BaseObjectTracker):
    """Matrice wrapper for DeepOCSORT. Motion-only: always the in-repo
    ``AdvancedTracker`` (the historical ``boxmot`` ReID backend was removed
    for AGPL-3.0 licensing reasons -- see module docstring)."""

    #: kept only as an accepted-and-ignored config field so an existing
    #: deployment JSON specifying deep_oc_sort_backend doesn't hard-fail.
    backend: str = "fallback"

    def __init__(self, config: MatriceTrackerConfig, namespace: Optional[str] = None):
        self._config = config
        self._namespace = namespace

        requested = (config.deep_oc_sort_backend or "auto").lower().strip()
        if requested not in {"auto", "boxmot", "fallback"}:
            raise ValueError(
                f"Unknown deep_oc_sort_backend '{config.deep_oc_sort_backend}'. "
                "Use 'auto', 'boxmot', or 'fallback'."
            )
        if requested == "boxmot":
            logger.warning(
                "DeepOCSORT 'boxmot' backend has been removed (AGPL-3.0 licensing, "
                "incompatible with commercial distribution) -- using the in-repo "
                "'advanced' motion tracker fallback instead."
            )

        self._fallback = AdvancedTrackerAdapter(config, namespace=namespace)

    # ---- update -----------------------------------------------------------

    def update(
        self,
        detections: List[DetectionDict],
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[DetectionDict]:
        dets = [d for d in (detections or []) if isinstance(d, dict)]
        return self._fallback.update(dets, stream_info=stream_info)

    # ---- lifecycle --------------------------------------------------------

    def reset(self) -> None:
        self._fallback.reset()

    def restore_state(self) -> None:
        self._fallback.restore_state()

    def save_state(self) -> None:
        self._fallback.save_state()
