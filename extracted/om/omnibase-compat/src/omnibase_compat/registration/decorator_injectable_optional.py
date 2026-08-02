# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: permanent cross-repo DI enforcement primitive

"""@injectable_optional decorator — declarative DI metadata marker.

Attaches ``__injectable_optional__`` to a class to document which constructor
parameters may be omitted by DI containers (e.g. Kafka publishers, loggers).
Purely declarative — no runtime injection logic.

Usage::

    @injectable_optional("event_bus", reason="optional Kafka publisher")
    class MyNode:
        def __init__(self, event_bus: EventBus | None = None) -> None:
            ...
"""

from __future__ import annotations

from typing import Any


def injectable_optional(param_name: str, *, reason: str) -> Any:
    """Class decorator marking ``param_name`` as an optional DI parameter.

    When applied multiple times the metadata is merged into a list so that
    all annotated parameters are visible via ``cls.__injectable_optional__``.
    """

    def decorator(cls: type) -> type:
        entry: dict[str, str] = {"param_name": param_name, "reason": reason}
        existing = getattr(cls, "__injectable_optional__", None)

        if existing is None:
            cls.__injectable_optional__ = entry  # type: ignore[attr-defined]
        elif isinstance(existing, list):
            existing.append(entry)
        else:
            cls.__injectable_optional__ = [existing, entry]  # type: ignore[attr-defined]

        return cls

    return decorator
