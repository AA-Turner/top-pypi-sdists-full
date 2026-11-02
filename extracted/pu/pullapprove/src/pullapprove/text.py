"""Small helpers for the text PullApprove prints."""

from __future__ import annotations


def plural(n: int, word: str) -> str:
    """`word`, spelled for a count of `n`."""
    return word if n == 1 else word + "s"
