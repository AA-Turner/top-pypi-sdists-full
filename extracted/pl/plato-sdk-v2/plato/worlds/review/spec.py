"""Recursive review specification for Plato worlds.

A ``ReviewSpec`` describes how a session should be reviewed, forming a
recursive chain where each reviewer can itself be reviewed.

Example::

    ReviewSpec(
        world="webclone-cua-review",
        config={"scoring_llm": {"model": "gemini/gemini-3.1-pro-preview"}},
        review=ReviewSpec(
            world="feedback-comparison",
            config={"ground_truth_fields": ["verdict", "comment"]},
            review=None,  # human feedback is the terminal ground truth
        ),
    )
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ReviewSpec(BaseModel):
    """Recursive specification for how a session should be reviewed.

    Attributes:
        world: Registered review world name (e.g. ``"webclone-cua-review"``).
        config: World-specific config overrides merged into the review world's config.
        review: How to review the reviewer itself. ``None`` means human
            feedback is the ground truth (recursion terminal).
    """

    world: str = Field(description="Registered review world name")
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Config overrides for the review world",
    )
    review: ReviewSpec | None = Field(
        default=None,
        description="How to review the reviewer. None = human feedback is terminal.",
    )
