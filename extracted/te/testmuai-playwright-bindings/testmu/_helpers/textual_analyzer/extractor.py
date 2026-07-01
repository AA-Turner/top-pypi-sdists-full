"""Pure helpers for executing a recorded textual extraction expression.

The extraction code may reference snapshot nodes via ``el(i)``. We parse those
indices, resolve each to a stable Playwright element handle, and wrap the code so
``el(i)`` returns the matching handle. The wrap format and index alignment are
kept stable so a recorded extraction runs identically at record, replay, and
export time across the Python and TypeScript bindings.
"""
from __future__ import annotations

import re

_EL_REFERENCE = re.compile(r"\bel\(\s*(\d+)\s*\)")


def parse_el_references(code: str) -> list[int]:
    """Return the el(i) indices referenced in ``code``, unique, first-seen order."""
    seen: list[int] = []
    for match in _EL_REFERENCE.finditer(code):
        index = int(match.group(1))
        if index not in seen:
            seen.append(index)
    return seen


def wrap_extractor_code(code: str, indices: list[int]) -> str:
    """Wrap ``code`` for ``page.evaluate(fn, els)``.

    ``els`` is the array of resolved element handles in ``indices`` order;
    ``el(i)`` maps each referenced snapshot index to its handle's position. A
    boolean result is coerced to a lowercase ``'true'``/``'false'`` STRING so the
    value matches the analyzer node's runtime normalization; ``null`` and every
    other type pass through unchanged.
    """
    pos_map = ", ".join(
        f"{index}: {position}" for position, index in enumerate(indices)
    )
    return (
        "(els) => {\n"
        f"  const __m = {{{pos_map}}};\n"
        "  const el = (i) => els[__m[i]];\n"
        f"  const __v = ({code});\n"
        "  return (typeof __v === 'boolean' ? String(__v) : __v);\n"
        "}"
    )
