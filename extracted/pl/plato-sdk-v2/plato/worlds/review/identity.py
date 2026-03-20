"""Review session identity helpers.

Structural identification of review sessions — no tags, no markers.
A session is a review session if its world is a :class:`BaseReviewWorld`
subclass.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from plato.worlds.review.spec import ReviewSpec

if TYPE_CHECKING:
    from plato.chronos.models import SessionResponse
    from plato.chronos.sdk import AsyncChronos


def is_review_world(world_name: str) -> bool:
    """Check if a world name corresponds to a registered BaseReviewWorld.

    Args:
        world_name: The registered world name to check.

    Returns:
        True if the world is a BaseReviewWorld subclass.
    """
    from plato.worlds.base import _WORLD_REGISTRY
    from plato.worlds.review.world import BaseReviewWorld

    world_cls = _WORLD_REGISTRY.get(world_name)
    return world_cls is not None and issubclass(world_cls, BaseReviewWorld)


def is_review_session(session: SessionResponse) -> bool:
    """Check if a session is a review by checking its world type.

    Args:
        session: A Chronos session response.

    Returns:
        True if the session's world is a BaseReviewWorld subclass.
    """
    if session.world is None:
        return False
    if not session.world.name:
        return False
    return is_review_world(session.world.name)


def get_review_target(session: SessionResponse) -> str | None:
    """Get the target session ID from a review session's config.

    Args:
        session: A Chronos session response.

    Returns:
        The target session ID, or None if not a review session or not set.
    """
    wc = session.world_config or {}
    return wc.get("target_session_id")


def get_review_spec(session: SessionResponse) -> ReviewSpec | None:
    """Extract the ReviewSpec from a session's world_config.

    Args:
        session: A Chronos session response.

    Returns:
        The ReviewSpec, or None if not set.
    """
    wc = session.world_config or {}
    raw = wc.get("review")
    if raw and isinstance(raw, dict):
        return ReviewSpec.model_validate(raw)
    return None


async def get_review_chain(
    session_id: str,
    chronos: AsyncChronos,
) -> list[Any]:
    """Walk the review chain for a session.

    Returns a list of child sessions that are review sessions,
    recursively including their own review children.

    Args:
        session_id: The session to find reviewers for.
        chronos: Async Chronos client.

    Returns:
        Flat list of review sessions in the chain (depth-first order).
    """
    session = await chronos.get_session(session_id)
    chain: list[Any] = []
    for child in session.child_sessions or []:
        child_session = await chronos.get_session(child.public_id)
        if is_review_session(child_session):
            chain.append(child_session)
            chain.extend(await get_review_chain(child.public_id, chronos))
    return chain
