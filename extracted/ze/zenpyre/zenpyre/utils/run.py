r"""Contain utility functions to generate run identifiers."""

from __future__ import annotations

__all__ = ["extract_run_id", "extract_run_ids", "generate_run_id"]

import uuid
from typing import TYPE_CHECKING, Any

from zenpyre.utils.hashing import hash_dict_uuid

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig


def extract_run_id(config: RunnableConfig | None) -> str | None:
    r"""Return the caller-supplied ``run_id`` from a config, if any.

    Args:
        config: The config to extract the run ID from. If ``None``,
            no run ID is returned.

    Returns:
        The run ID as a string, or ``None`` if ``config`` is ``None``
        or does not contain a ``run_id``.

    Example:
        ```pycon
        >>> from zenpyre.utils.run import extract_run_id
        >>> extract_run_id({"run_id": "abc-123"})
        'abc-123'
        >>> extract_run_id(None) is None
        True

        ```
    """
    if config is None:
        return None
    run_id = config.get("run_id")
    return str(run_id) if run_id is not None else None


def extract_run_ids(
    config: RunnableConfig | list[RunnableConfig] | None, n: int
) -> list[str | None]:
    r"""Return one ``run_id`` per item for a batch call.

    Handles both a single config shared by every item and a list of
    per-item configs.

    Args:
        config: The config(s) to extract run IDs from. Can be a
            single config shared by all ``n`` items, a list of ``n``
            per-item configs, or ``None``.
        n: The number of items in the batch. Must match ``len(config)``
            when ``config`` is a list.

    Returns:
        A list of ``n`` run IDs (or ``None`` for items without one).

    Raises:
        ValueError: if ``config`` is a list and its length does not
            match ``n``.

    Example:
        ```pycon
        >>> from zenpyre.utils.run import extract_run_ids
        >>> extract_run_ids({"run_id": "abc"}, n=3)
        ['abc', 'abc', 'abc']
        >>> extract_run_ids([{"run_id": "a"}, {"run_id": "b"}], n=2)
        ['a', 'b']
        >>> extract_run_ids(None, n=2)
        [None, None]

        ```
    """
    if config is None:
        return [None] * n
    if isinstance(config, list):
        if len(config) != n:
            msg = f"Expected {n} configs but received {len(config)}"
            raise ValueError(msg)
        return [extract_run_id(c) for c in config]
    return [extract_run_id(config)] * n


def generate_run_id(config: dict[str, Any] | None = None) -> str:
    r"""Generate a unique identifier for a run.

    If a configuration is given, the identifier is derived
    deterministically from its content, so the same configuration
    always produces the same run ID. Otherwise, a random identifier
    is generated.

    Args:
        config: The configuration used to derive a deterministic
            run ID. If ``None``, a random run ID is generated.

    Returns:
        The generated run ID.

    Example:
        ```pycon
        >>> from zenpyre.utils.run import generate_run_id
        >>> generate_run_id()  # doctest: +SKIP
        '3f2504e0-4f89-11d3-9a0c-0305e82c3301'
        >>> generate_run_id({"lr": 0.01, "batch_size": 32})  # doctest: +SKIP
        'a94a8fe5-ccb1-4bb2-8bb1-3e8b79d7de35'

        ```
    """
    if config is None:
        return str(uuid.uuid4())
    return hash_dict_uuid(config)
