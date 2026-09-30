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
from typing import Any, Callable

#: Matches the two template forms the resolver understands.
_TEMPLATE_RE = re.compile(r"\{\{[^{}]+\}\}|\$\{[^{}]+\}")


def fence_value(rendered: Any) -> str:
    """Wrap one substituted value in a triple-quoted block."""
    return f'\n"""\n{rendered}\n"""\n'


def fence_templates(description: Any, resolver: Callable[[str], Any]) -> Any:
    """Resolve every template in ``description``, fencing each substituted value.

    Each token is resolved in isolation through ``resolver`` (the package's own
    ``var``), so namespace dispatch, defaults and traversal behave exactly as
    they do everywhere else — only the rendering differs.

    A token the resolver cannot resolve is left as the literal ``{{name}}`` and
    is NOT fenced: an unresolved name must stay visible so the failure is
    legible rather than buried in quotes.

    Resolvers disagree on how they signal "unresolved" — some hand back the
    literal token, others an empty string — so both are treated as unresolved.
    The cost is that a variable holding a genuinely empty value also renders as
    its literal token, which is the better failure anyway: an empty fenced block
    tells the vision model nothing, while a visible ``{{name}}`` shows what was
    missing.

    Non-string input and text with no templates pass through untouched.
    """
    if not isinstance(description, str) or not _TEMPLATE_RE.search(description):
        return description

    def _sub(match: "re.Match[str]") -> str:
        token = match.group(0)
        resolved = resolver(token)
        # Unresolved: the literal token back, or an empty result (see docstring).
        if resolved is None or resolved == token or resolved == "":
            return token
        return fence_value(resolved)

    return _TEMPLATE_RE.sub(_sub, description)
