"""Kind-filtered edges and fan-out modes — routing by what the payload IS.

Plan of record §7.3 / §7.4, ratified 2026-08-20:

    "An edge declares 'carry `website` instances'; the engine fans matching
    instances from a `content` list (or any list payload) down that edge; an
    edge whose kind never appears doesn't fire — conditional downstream paths
    with zero custom code."

    Fan-out default (Arman, build authorization): an edge carrying ``list[K]``
    delivers the WHOLE list (``all``) unless the author opts the edge into
    ``each``. **Fan-out is always a visible, deliberate authoring choice, never
    implicit parallelism.**

That default is the load-bearing half. Implicit per-item parallelism is how a
canvas silently turns one step into fifty paid invocations, so ``all`` is what
you get unless you asked otherwise, and ``each`` is a mode the author sets on
the edge and can see on the canvas.

AUTHORING SHAPE (on ``EdgeDef.data``)
-------------------------------------
    "kind_filter": "website"     # carry only website instances
    "fan_out": "each"            # one target invocation per instance ("all")
    "item_key": "value"          # key the target receives the item(s) under

Every key is optional; an edge with none of them behaves exactly as it always
has. That matters: this feature must be invisible to the thousands of edges
that predate it.

WHERE THE INSTANCES COME FROM
-----------------------------
The deep scan in ``occurrences`` — the SAME one kind-triggered nodes use, on
purpose (see that module). So an edge filter finds a ``website`` in a plain
list, inside an ``agent_result``'s ``content``, or nested three levels down in
a structure the author never thought about, and it finds exactly what a trigger
on the same kind would find.

Matches are ``top_level_only``: an edge asking for ``website`` instances that
found a website does NOT also deliver the websites nested inside it. This is
the one place the outermost rule is right — the author is selecting a payload
to send somewhere, not taking an inventory — and it keeps a self-nesting kind
from multiplying an edge's fan-out.

EMPTY IS A PRUNE, NEVER AN ERROR
--------------------------------
"An edge whose kind never appears doesn't fire" is the feature, not a failure:
that IS the zero-code conditional path. The scheduler prunes the edge, so the
target's join set releases instead of blocking forever, and a downstream branch
that depended solely on it resolves dead — the same semantics as a false
CONDITIONAL predicate.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.occurrences import find_occurrences

__all__ = [
    "FanOutMode",
    "EdgeKindRouting",
    "parse_edge_routing",
    "select_instances",
    "DEFAULT_ITEM_KEY",
]

FanOutMode = Literal["all", "each"]

#: The key a fanned/filtered payload arrives under when the author names none.
#: ``value`` matches ``control.branch``'s input and ``control.map``'s default
#: ``payload_key`` — one word for "the thing that flowed", everywhere.
DEFAULT_ITEM_KEY = "value"


class EdgeKindRouting(BaseModel):
    """One edge's kind-routing declaration, normalized."""

    model_config = ConfigDict(frozen=True)

    kind_filter: str | None = None
    fan_out: FanOutMode = "all"
    item_key: str = DEFAULT_ITEM_KEY

    @property
    def is_active(self) -> bool:
        """Whether this edge does anything beyond classic routing."""
        return self.kind_filter is not None or self.fan_out == "each"

    @property
    def fans_out(self) -> bool:
        return self.fan_out == "each"


class EdgeRoutingDeclarationError(ValueError):
    """A malformed kind-routing declaration on an edge.

    Raised at COMPILE time (never at run time): a bad ``fan_out`` value is an
    authoring mistake the studio must show while editing, not a surprise
    halfway through a paid run.
    """


def parse_edge_routing(data: dict[str, Any] | None) -> EdgeKindRouting:
    """Read the kind-routing keys off an ``EdgeDef.data`` payload.

    Loud on malformed values, silent on absent ones. There is no "close enough"
    reading of ``fan_out: "eachh"`` — guessing would fan out a paid step fifty
    times because of a typo.
    """
    data = data or {}

    raw_filter = data.get("kind_filter")
    if raw_filter is not None and (not isinstance(raw_filter, str) or not raw_filter.strip()):
        raise EdgeRoutingDeclarationError(
            f"kind_filter must be a non-empty kind slug string, got {raw_filter!r}."
        )

    raw_mode = data.get("fan_out")
    if raw_mode is None:
        mode: FanOutMode = "all"
    elif raw_mode in ("all", "each"):
        mode = raw_mode
    else:
        raise EdgeRoutingDeclarationError(
            f"fan_out must be 'all' (the whole list to one invocation, the "
            f"default) or 'each' (one invocation per instance), got {raw_mode!r}."
        )

    raw_key = data.get("item_key")
    if raw_key is not None and (not isinstance(raw_key, str) or not raw_key.strip()):
        raise EdgeRoutingDeclarationError(
            f"item_key must be a non-empty target-argument name, got {raw_key!r}."
        )

    return EdgeKindRouting(
        kind_filter=raw_filter.strip() if isinstance(raw_filter, str) else None,
        fan_out=mode,
        item_key=raw_key.strip() if isinstance(raw_key, str) else DEFAULT_ITEM_KEY,
    )


class InstanceSelection(BaseModel):
    """What a kind filter drew out of one source payload."""

    model_config = ConfigDict(frozen=True)

    kind: str
    instances: list[Any] = Field(default_factory=list)
    #: Where each instance was found, index-for-index with ``instances`` — the
    #: provenance a run page shows ("3 websites, from results[0..2]") and what
    #: a per-item invocation records so a failure names the item.
    paths: list[str] = Field(default_factory=list)

    def __len__(self) -> int:
        return len(self.instances)


def select_instances(payload: Any, kind_filter: str) -> InstanceSelection:
    """Every ``kind_filter`` instance in ``payload``, in document order."""
    occurrences = find_occurrences(payload, kind_filter, top_level_only=True)
    return InstanceSelection(
        kind=kind_filter,
        instances=[o.value for o in occurrences],
        paths=[o.path for o in occurrences],
    )


def fan_out_items(payload: Any, routing: EdgeKindRouting) -> list[Any] | None:
    """The items an ``each`` edge should dispatch, or ``None`` when it can't.

    Two sources, in order:

    * a kind filter — the instances it selected;
    * no filter — the payload's own list. An ``each`` edge with no kind filter
      is the plain "``list[K]`` fan-out" of §7.4, and it needs a list: a lone
      dict is ONE thing and fanning it would be a lie about what happened.
      ``None`` says "this edge cannot fan out", which the scheduler reports
      against the edge instead of quietly delivering something else.
    """
    if routing.kind_filter is not None:
        return list(select_instances(payload, routing.kind_filter).instances)
    if isinstance(payload, list | tuple):
        return list(payload)
    if isinstance(payload, dict):
        # An edge with no source handle broadcasts the node's whole output
        # dump. When that dump has exactly ONE list field, it is unambiguous
        # what "each" means; more than one and the author must say which, via a
        # kind filter or a source handle. Ambiguity is never resolved by
        # picking the first — it is refused.
        lists = [v for v in payload.values() if isinstance(v, list | tuple)]
        if len(lists) == 1:
            return list(lists[0])
    return None
