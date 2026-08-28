"""
Utilities package for Matrice Deploy.

This package contains utility modules for the Matrice deployment system.

Import cost (PY-20)
-------------------
Every public name below is resolved **lazily**, via the PEP 562 module-level
``__getattr__``.  Importing :mod:`matrice_analytics` -- or, more importantly,
importing a subpackage such as :mod:`matrice_analytics.engine` -- therefore no
longer executes ``matrice_analytics.post_processing``, which eagerly imports
~180 modules (pulling in ``torch`` and ``cv2``) and instantiates and registers
the whole legacy use-case catalogue.

Nothing about the legacy surface changes: ``matrice_analytics.PostProcessor``,
``from matrice_analytics import PostProcessor`` and ``from matrice_analytics
import *`` all still work, and the first such access performs exactly the
import that used to happen at package-import time.  Only the *timing* moves.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

# Subpackages that used to be bound as attributes of this package as a side
# effect of the eager import block this module ran at import time, and so must
# stay reachable as attributes even before anyone imports them explicitly.
_LAZY_SUBMODULES = frozenset(
    {
        "post_processing",
        "runtime",
    }
)

# Public name -> subpackage that provides it.  Mirrors the eager
# ``from .post_processing import ...`` / ``from .runtime import ...`` blocks
# this module used to run at import time.
_LAZY_EXPORTS = {
    # Re-exported from post_processing for convenience.
    "PostProcessor": "post_processing",
    "create_config_from_template": "post_processing",
    "create_people_counting_config": "post_processing",
    "list_available_usecases": "post_processing",
    "process_simple": "post_processing",
    "validate_config": "post_processing",
    # Runtime seam: single per-frame post-processing entrypoint for inference
    # workers (owns PostProcessor construction, event loop, stream_info,
    # result shape).  See matrice_analytics.runtime.
    "PostProcRunner": "runtime",
    "build_stream_info": "runtime",
    "normalize_detections": "runtime",
}

# Static re-exports so type checkers, IDEs and the generated stubs still see
# the full surface. Never executed at runtime -- __getattr__ below does the
# real work. ``runtime`` is deliberately absent from __all__ (it never was in
# it); it is re-exported here only so `matrice_analytics.runtime` type-checks.
if TYPE_CHECKING:  # pragma: no cover
    from . import post_processing, runtime  # noqa: F401
    from .post_processing import (
        PostProcessor,
        create_config_from_template,
        create_people_counting_config,
        list_available_usecases,
        process_simple,
        validate_config,
    )
    from .runtime import PostProcRunner, build_stream_info, normalize_detections


def __getattr__(name: str) -> Any:
    """Resolve a public name on first access (PEP 562).

    Keeps the whole legacy surface importable from :mod:`matrice_analytics`
    while making ``import matrice_analytics.engine...`` cheap.
    """
    if name in _LAZY_SUBMODULES:
        value: Any = importlib.import_module(f"{__name__}.{name}")
    else:
        submodule = _LAZY_EXPORTS.get(name)
        if submodule is None:
            raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
        value = getattr(importlib.import_module(f"{__name__}.{submodule}"), name)

    # Cache so subsequent lookups skip __getattr__ entirely.
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__) | _LAZY_SUBMODULES | set(_LAZY_EXPORTS))


__all__ = [
    "post_processing",
    "PostProcessor",
    "create_config_from_template",
    "create_people_counting_config",
    "process_simple",
    "list_available_usecases",
    "validate_config",
    "PostProcRunner",
    "build_stream_info",
    "normalize_detections",
]
