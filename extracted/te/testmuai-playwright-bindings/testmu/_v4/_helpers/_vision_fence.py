"""Fence captured values spliced into a VQE vision query.

automind's vision model reads the query as prose. A multi-line or list value
substituted inline runs together with the surrounding words, and the model binds
the predicate to the LAST line instead of the whole captured block — a
confident, wrong verdict.

Fencing wraps each substituted value in triple quotes so the whole block reads
as one reference.

Vision-query text ONLY. This deliberately lives beside the vision helper rather
than inside the shared variable resolver: fencing an ordinary variable read
would put quote characters into typed values, assertion operands and fill text.

Port of V2 (_fence_vision_query_value).
"""
from __future__ import annotations

import re
from typing import Any

#: Matches the two template forms the resolver understands.
_TEMPLATE_RE = re.compile(r"\{\{[^{}]+\}\}|\$\{[^{}]+\}")


def fence_value(rendered: Any) -> str:
    """Wrap one substituted value in a triple-quoted block."""
    return f'\n"""\n{rendered}\n"""\n'


