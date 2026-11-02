"""The mapping-source vocabulary — what may stand on the SOURCE side of an edge.

An edge's ``data.mappings`` is ``{target_input_name: source_output_expression}``.
A source expression is either a dot-path into the upstream node's output
(``"result.canon"``, ``"items.0.id"``) or one of the SIGILS below — reserved
tokens the engine interprets instead of looking up a key.

There is exactly ONE sigil today: ``$FULL_PAYLOAD``, "the entire upstream
output". It is needed constantly (a ``text.template`` whose ``variables`` is
the whole upstream payload), so authors reach for it — and, before this
module existed, reached for it by INVENTING a name for it.

**The defect this module closes** (workflow ``129a4ec1``, run ``12c153a9``,
2026-09-12): the Masterwork Conductor wrote ``{"variables": "$payload"}`` on
the edge ``intake -> canon``. ``workflow_plan check`` reported "no breaks" and
the user's first real run died at step 0 with ``EdgeRoutingError: ... KeyError:
'$payload'``. Nothing anywhere knew that ``$``-prefixed source tokens are a
CLOSED vocabulary — every layer treated ``$payload`` as an ordinary output key
that the source node might plausibly emit, so a schema-shaped check (does the
upstream declare this key?) went quiet on a dynamic-output upstream where no
key can be ruled out. No node emits a ``$``-prefixed key; an unknown sigil is
therefore ALWAYS a run-killer, provably, with no schema knowledge at all.

So the check lives here, schema-free, and every layer that reads a mapping
source calls it: definition validation (refuse the save), the dry-run /
author-time handshake (refuse the plan), and the scheduler (the run-time
message names the alias the author meant).
"""

from __future__ import annotations

#: "The entire upstream output", as one value bound to one target input.
WHOLE_PAYLOAD = "$FULL_PAYLOAD"

#: Every reserved source-side token. A ``$``-prefixed source that is not in
#: here can never resolve — no node emits ``$``-prefixed output keys.
MAPPING_SOURCE_SIGILS = frozenset({WHOLE_PAYLOAD})

#: Names authors (and agents copying stale examples) have actually reached for
#: when they meant WHOLE_PAYLOAD. Purely for a better message — the refusal
#: does not depend on the token being listed here.
_KNOWN_MISTAKES = frozenset(
    {"$payload", "$output", "$all", "$whole", "$input", "$source", "$upstream", "$result"}
)


def unknown_sigil(source_key: object) -> str | None:
    """The offending token when ``source_key`` is an unsupported sigil, else None.

    ``$FULL_PAYLOAD`` passes. A plain key or dot-path passes. A bare ``"$"``
    or anything else starting with ``$`` is refused: it reads as a reserved
    token the engine does not have, and at run time it becomes a literal key
    lookup that no node output can satisfy.
    """
    if not isinstance(source_key, str) or not source_key.startswith("$"):
        return None
    if source_key in MAPPING_SOURCE_SIGILS:
        return None
    return source_key


def unknown_sigil_message(target_key: str, source_key: str, *, edge_id: str) -> str:
    """One sentence the author can act on, identical at every layer."""
    meant = (
        f" You almost certainly meant {WHOLE_PAYLOAD!r}."
        if source_key in _KNOWN_MISTAKES
        else ""
    )
    return (
        f"edge '{edge_id}' mapping '{target_key}' <- '{source_key}': "
        f"'{source_key}' is not a supported mapping source. A source starting "
        f"with '$' is a reserved token, and the only one the engine has is "
        f"{WHOLE_PAYLOAD!r} (the entire upstream output as one value)."
        f"{meant} Otherwise name a real output field of the upstream step "
        f"(dot-paths allowed, e.g. 'result.canon'), or drop 'mappings' "
        f"entirely to broadcast the whole payload."
    )


__all__ = [
    "MAPPING_SOURCE_SIGILS",
    "WHOLE_PAYLOAD",
    "unknown_sigil",
    "unknown_sigil_message",
]
