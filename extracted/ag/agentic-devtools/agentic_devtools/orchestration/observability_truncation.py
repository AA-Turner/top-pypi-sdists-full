"""Deterministic truncation utility for observability summaries."""

from __future__ import annotations

import json
from typing import Any


def truncate_summary(data: Any, max_chars: int = 2000) -> Any:
    """Truncate data to a maximum character budget.

    The serialised form of *data* is used to measure size: strings are
    measured directly; dicts and lists are JSON-serialised first; other
    types are converted via ``str()``.

    **Return type is input-dependent:** when the serialised form of a
    ``str`` fits within *max_chars* the original string is returned
    unchanged. When a JSON-serialisable ``dict`` or ``list`` fits
    within *max_chars*, the original object is returned (preserving
    the type for downstream JSON encoding). If a ``dict`` or ``list``
    falls back to ``repr()`` because JSON serialisation fails, the
    repr string is returned even when it fits within budget. For all
    other types (``int``, ``set``, custom classes, …), the ``str()``
    representation is always returned — never the original object —
    to guarantee log-safe output. When truncation is required, a
    ``str`` is always returned regardless of the input type.

    Args:
        data: Input data (string, dict, list, or other).
        max_chars: Maximum character length for the output.

    Returns:
        - ``None`` when *data* is ``None``.
        - The original ``str`` or JSON-serialisable ``dict``/``list``
          when its serialised form fits within *max_chars*.
        - A ``str`` representation for non-str/dict/list types even
          when within budget (guarantees downstream JSON safety).
        - A truncated ``str`` with ``… [N chars omitted]``
          suffix when over budget. When the suffix itself cannot fit,
          a shorter ellipsis (``…``) form is used instead.
    """
    if data is None:
        return None

    return_original = True

    if isinstance(data, str):
        text = data
    elif isinstance(data, (dict, list)):
        try:
            text = json.dumps(data, default=str)
        except (TypeError, ValueError):
            text = repr(data)
            return_original = False
    else:
        text = str(data)
        return_original = False

    if len(text) <= max_chars:
        return data if return_original else text

    if max_chars <= 0:
        return ""

    omitted = len(text) - max_chars
    suffix = f"… [{omitted} chars omitted]"
    if len(suffix) >= max_chars:
        if max_chars == 1:
            return "…"
        return text[: max_chars - 1] + "…"

    # Iterate until cut_at stabilises.  Each step recomputes omitted as
    # len(text) - cut_at so the suffix accurately reflects chars actually
    # dropped.  Digit-count growth in omitted can shift cut_at by 1,
    # requiring at most one extra iteration; the loop always converges in
    # O(log10(len(text))) steps (≤ 3 for any realistic input).
    cut_at = max_chars - len(suffix)
    while True:
        omitted = len(text) - cut_at
        suffix = f"… [{omitted} chars omitted]"
        new_cut_at = max_chars - len(suffix)
        if new_cut_at == cut_at:
            break
        cut_at = new_cut_at
    return text[:cut_at] + suffix
