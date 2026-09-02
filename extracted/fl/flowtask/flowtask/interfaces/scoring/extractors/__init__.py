"""flowtask.interfaces.scoring.extractors — concrete feature extractors.

Importing this package self-registers all v1 extractors
(``count_within_radius``, ``nearest_distance``, ``gravity``) with
``flowtask.interfaces.scoring.abstract.extractor_registry`` via the
``@register_extractor`` decorator (TASK-124).

Each extractor module lazily imports its heavy dependency (``sklearn``)
inside ``compute()`` — importing this package does NOT pull in scipy/sklearn
at import time.
"""
from . import count  # noqa: F401
from . import nearest  # noqa: F401
from . import gravity  # noqa: F401

__all__ = ("count", "nearest", "gravity")
