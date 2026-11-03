"""Unified review system for Plato worlds.

This package contains all review-related infrastructure:

- ``data``: Review model schema system (ReviewData, RenderHint, FeedbackField)
- ``spec``: Recursive ReviewSpec model
- ``world``: BaseReviewWorld base class
- ``identity``: Session identity helpers
- ``result``: ReviewSignal, ReviewFinding, ReviewResult
"""

from plato.worlds.review.data import (
    FeedbackField,
    RenderHint,
    ReviewData,
    ReviewModelMeta,
    StandardFeedback,
    collect_review_schemas,
    get_review_model_meta,
    review_model,
    review_model_to_json_schema,
)
from plato.worlds.review.result import (
    ReviewFinding,
    ReviewResult,
    ReviewSignal,
    SessionData,
)
from plato.worlds.review.spec import ReviewSpec

# Note: BaseReviewWorld, ReviewWorldConfig, and identity helpers are NOT
# re-exported here to avoid circular imports (world.py → config.py → spec.py → __init__.py).
# Import them directly:
#   from plato.worlds.review.world import BaseReviewWorld, ReviewWorldConfig
#   from plato.worlds.review.identity import is_review_session, ...

__all__ = [
    # Data / models
    "FeedbackField",
    "RenderHint",
    "ReviewData",
    "ReviewModelMeta",
    "collect_review_schemas",
    "get_review_model_meta",
    "review_model",
    "review_model_to_json_schema",
    "StandardFeedback",
    # Spec
    "ReviewSpec",
    # Result
    "ReviewFinding",
    "ReviewResult",
    "ReviewSignal",
    "SessionData",
]
