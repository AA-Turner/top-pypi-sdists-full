import typing as t

from loguru import logger

if t.TYPE_CHECKING:
    from dreadnode.generators.message import Message

CacheMode = t.Literal["latest"]
"""
How to handle cache_control entries on messages.

- latest: Mark the final system message (if present) and the last 2 non-assistant,
  non-system messages with ``cache_control: ephemeral``. This spends up to 3 of
  Anthropic's 4 breakpoints — one pinning the tools+system prefix, two forming a
  rolling window over the most recent user/tool turns — which matches the
  rolling-window pattern recommended for multi-turn agents.
"""


def apply_cache_mode_to_messages(
    mode: CacheMode | None,
    messages: "list[list[Message]]",
) -> "list[list[Message]]":
    if mode is None:
        return messages

    if mode != "latest":
        logger.warning(
            f"Unknown caching mode '{mode}', defaulting to 'latest'",
        )
        mode = "latest"

    # Clone + clear any prior cache_control so each call is self-contained.
    updated: list[list[Message]] = [
        [m.clone().cache(cache_control=False) for m in _messages] for _messages in messages
    ]

    for _messages in updated:
        # Pin the tools+system prefix via the final system message.
        # Anthropic caches the prefix up to and including the marked block,
        # so marking system implicitly caches tool definitions too.
        system_messages = [m for m in _messages if m.role == "system"]
        if system_messages:
            system_messages[-1].cache(cache_control=True)

        # Rolling window on the last 2 user/tool turns so cache_read hits
        # extend to the current generation step.
        rolling = [m for m in _messages if m.role not in ("assistant", "system")][-2:]
        for message in rolling:
            message.cache(cache_control=True)

    return updated
