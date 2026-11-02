"""The content of a user message: the one type that ``agent.run`` and the handles' sends take."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import TypeAdapter

from mistralai.vibe.harness.app_server import session as harness_session
from mistralai.vibe.sdk.execution_record import state as legacy_state
from mistralai.vibe_agents.sdk.authoring.errors import UnsupportedAgentFeatureError

__all__ = ["UserContentLike", "to_session_content"]

type UserContentLike = (
    str | Sequence[harness_session.TextContentBlock | harness_session.ImageContentBlock | Mapping[str, Any]]
)
"""A user message: text, or text and image blocks, as models or as dicts such as
``{"type": "text", "text": "..."}``."""

_BLOCK_ADAPTERS: dict[object, TypeAdapter[Any]] = {
    "text": TypeAdapter(harness_session.TextContentBlock),
    "image": TypeAdapter(harness_session.ImageContentBlock),
}


def to_session_content(content: UserContentLike) -> list[harness_session.ContentBlock]:
    """Return the Session content blocks of a user message, refusing a block kind no host takes yet."""
    if isinstance(content, str):
        return [harness_session.TextContentBlock(text=content)]

    converted: list[harness_session.ContentBlock] = []
    for item in content:
        block: object = item
        if isinstance(item, Mapping):
            adapter = _BLOCK_ADAPTERS.get(item.get("type"))
            if adapter is None:
                raise UnsupportedAgentFeatureError(
                    "user_content",
                    f"the first Unified Harness backend cannot accept {item.get('type')!r} user content",
                )
            block = adapter.validate_python(item)
        if isinstance(block, (harness_session.TextContentBlock, legacy_state.TextContentBlock)):
            converted.append(harness_session.TextContentBlock(text=block.text))
            continue
        if isinstance(block, harness_session.ImageContentBlock):
            converted.append(
                harness_session.ImageContentBlock(uri=block.uri, media_type=block.media_type, alt_text=block.alt_text)
            )
            continue
        raise UnsupportedAgentFeatureError(
            "user_content",
            f"the first Unified Harness backend cannot accept {type(block).__name__} user content",
        )
    return converted
