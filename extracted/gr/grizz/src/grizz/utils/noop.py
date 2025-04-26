r"""Contain no-op functions."""

from __future__ import annotations

__all__ = ["tqdm"]

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable


def tqdm(iterable: Iterable, *args: Any, **kwargs: Any) -> Iterable:  # noqa: ARG001
    r"""Implement a no-op tqdm progressbar that is used when tqdm is not
    installed.

    Args:
        iterable: Iterable to decorate with a progressbar.
        *args: Positional arbitrary arguments.
        **kwargs: Keyword arbitrary arguments.

    Returns:
        The input iterable.
    """
    return iterable
