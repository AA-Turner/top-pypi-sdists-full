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

from collections.abc import Iterable
from typing import Any

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


def dotted_target_message(
    target_key: str,
    source_key: str,
    *,
    edge_id: str,
    node_id: str | None = None,
    takes: Iterable[str] | None = None,
) -> str:
    """The ONE sentence for a dotted TARGET key (``provision_values.policies``), at save and at run time.

    A mapping's dot-paths read the SOURCE side only; a dotted target would become a literal input key named
    ``"provision_values.policies"`` that no step takes (live 2026-11-17: Company Setup's first runs). The
    sentence names the step, the key and what the step takes."""
    head = str(target_key).split(".", 1)[0]
    leaf = str(target_key).rsplit(".", 1)[-1]
    step = f"step '{node_id}'" if node_id else "the step it feeds"
    names = sorted(str(n) for n in (takes or ()))
    takes_text = f" It takes: {', '.join(names)}." if names else ""
    use = (
        f"Hand the value to {head!r} as a whole (one object holding {leaf!r}), not into a place inside it."
        if names and head in names
        else f"Use e.g. {leaf!r} as the target key instead."
    )
    return (
        f"edge '{edge_id}' mapping has a dotted TARGET key {target_key!r} (mapped from {source_key!r}) "
        f"into {step}. Target keys must be plain top-level input field names — a dotted target creates a "
        f"literal input key named {target_key!r}, not a nested field, so the run stops at this connection. "
        f"Dot-notation is only supported on the SOURCE side of a mapping.{takes_text} {use}"
    )


def output_reads(edges: Iterable[Any]) -> tuple[str, ...] | None:
    """The source paths a step's outgoing connections read out of its OUTPUT, or None
    when the whole output is read.

    Ruled 2026-11-02 (Arman): a called workflow hands back only what the caller's
    connections read. ``edges`` are the step's outgoing compiled edges. None — the whole
    output — when there are none (the step's output is the run's answer), or any
    connection carries the whole payload (no mappings, ``$FULL_PAYLOAD``), tests the output
    (a condition) or draws from anywhere in it (a kind filter). A CONTROL connection
    carries nothing, an ERROR connection carries the failure record and a connection on a
    named handle carries that emission: none of them read the output.
    """
    from matrx_graph.paths import source_paths
    from matrx_graph.types.primitives import EdgeKind

    reads: list[str] = []
    seen_any = False
    for edge in edges:
        seen_any = True
        if edge.kind in (EdgeKind.CONTROL, EdgeKind.ERROR) or edge.source_handle is not None:
            continue
        if edge.mappings is None or edge.condition or edge.kind_filter:
            return None
        for source in edge.mappings.values():
            if not isinstance(source, str) or source == WHOLE_PAYLOAD:
                return None
            paths = source_paths(source)
            if any(not p.strip() or p.strip() == CURRENT_ELEMENT for p in paths):
                return None
            reads.extend(paths)
    if not seen_any:
        return None
    return tuple(dict.fromkeys(reads))


#: ``@`` alone is the element itself — as a mapping source, the whole output.
CURRENT_ELEMENT = "@"


__all__ = [
    "MAPPING_SOURCE_SIGILS",
    "WHOLE_PAYLOAD",
    "output_reads",
    "unknown_sigil",
    "unknown_sigil_message",
]
