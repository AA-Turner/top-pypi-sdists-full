"""Kind subscriptions — the one mechanism under triggers AND directives.

Plan of record §7.7c (ratified 2026-08-20):

    A node sits off to the side, connected to nothing, declaring: *run when
    this kind is generated.* "All of a particular kind, wherever they're
    generated from, doesn't matter what node, where, and doesn't matter how
    deeply nested they are, they trigger something to happen."

    His motivating case: complex streams whose kinds must be persisted — the
    trigger node saves them, wherever they surfaced, with no wiring.

    "**This is the same subscription mechanism the directive kinds (§7.5)
    need**, so it is built once and both consume it: a directive kind is
    simply a kind whose registered trigger mutates the graph under the
    apply-policy."

So this module is deliberately PURPOSE-BLIND. It decides WHAT fired and WITH
WHICH instances; it never decides what firing means. A node trigger turns a
firing into an invocation (the scheduler); a directive kind will turn the same
firing into a graph mutation under its apply-policy — and that half is NOT
built here (see THE DIRECTIVE SEAM below).

THE CLOCK IS THE SUPER-STEP, NOT THE WALL
-----------------------------------------
``debounce_steps`` coalesces occurrences over N super-steps. Wall-clock
debounce was rejected: a run is crash-safe and replayable, and a millisecond
window makes the SAME run fire a different number of times on replay than it
did live — which would make a triggered persistence node write a different
number of rows the second time. The super-step is the engine's own clock, it is
recorded in the checkpoint, and it replays identically. ``0`` (the default)
means "fire in the next super-step", the responsive case.

MULTIPLICITY OBEYS THE SAME LAW AS EDGES
----------------------------------------
``each`` (one firing per instance) vs ``all`` (one firing carrying every
instance) is the §7.4 ruling applied to triggers, with the same default: ``all``
unless the author opted in. A subscription is an authoring choice on the trigger
node, visible on the canvas, never inferred.

DEDUPE IS BY OCCURRENCE IDENTITY
--------------------------------
The same value flows through many steps of a run. Without dedupe, a trigger on
``website`` would fire again every time that website was passed along — and
Arman's motivating case (persist it) would write the row N times. Identity is
``<scope>#<kind>@<indexed path>`` where scope is the producing invocation, so a
genuinely NEW production of an identical value is a genuinely new firing, while
a pass-through of one already seen is not.

THE DIRECTIVE SEAM (§7.5 — deliberately not built here)
-------------------------------------------------------
A directive kind subscribes exactly like a trigger node, with
``purpose="directive"``. Everything above already serves it: content-based
matching at any depth, ``each``/``all``, dedupe, the replayable clock. What is
NOT here, on purpose, is what a directive DOES — graph mutation under the
apply-policy cascade (``auto``/``ask``/``off``), the additive-only rule Arman
set for auto-apply, and the both-halves display ruling (inline activity AND
a persistent canvas marker). A consumer builds that on top by draining firings
with ``purpose="directive"``; it must never be bolted into the matcher, or the
apply-policy would end up living in the routing layer where nobody can audit it.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.occurrences import KindOccurrence, find_occurrences

__all__ = [
    "SubscriptionPurpose",
    "KindSubscription",
    "SubscriptionFiring",
    "SubscriptionMatcher",
]

SubscriptionPurpose = Literal["node_trigger", "directive"]


class KindSubscription(BaseModel):
    """One declared interest in a kind appearing anywhere in a run."""

    model_config = ConfigDict(frozen=True)

    #: Who is subscribing. For a trigger node, its node id.
    subscriber_id: str
    #: The kind slug that fires it.
    kind: str
    #: ``all`` (default) = one firing carrying every instance seen in the
    #: window; ``each`` = one firing per instance.
    mode: Literal["all", "each"] = "all"
    #: Fire at most once for the whole run.
    fire_once: bool = False
    #: Coalesce over this many super-steps (see the module docstring).
    debounce_steps: int = Field(default=0, ge=0)
    purpose: SubscriptionPurpose = "node_trigger"


class SubscriptionFiring(BaseModel):
    """One thing that should happen because a kind appeared."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    subscription: KindSubscription
    occurrences: list[KindOccurrence] = Field(default_factory=list)
    #: The super-step at which this firing was drained.
    step: int = 0
    #: Which node produced each occurrence, index-for-index with
    #: ``occurrences`` — the provenance a run page shows ("fired on a website
    #: from step 3") and the answer to "where did this come from" for a node
    #: that is wired to nothing.
    source_node_ids: list[str] = Field(default_factory=list)

    @property
    def values(self) -> list[Any]:
        return [o.value for o in self.occurrences]


class _Pending(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    occurrences: list[KindOccurrence] = Field(default_factory=list)
    source_node_ids: list[str] = Field(default_factory=list)
    #: Super-step at which the FIRST occurrence in this window landed — the
    #: debounce clock starts there, not at the last one, so a steady stream
    #: cannot postpone a firing forever.
    opened_at_step: int = 0


class SubscriptionMatcher:
    """Stateful, per-run matcher: observe payloads, drain firings.

    Lives for one run. Its whole state (seen identities, pending windows, spent
    fire-once subscriptions) is derived from what it observed, so a replay that
    re-observes the same outcomes in the same order reproduces the same
    firings — which is the property that makes a triggered persistence node
    safe to replay at all.
    """

    def __init__(self, subscriptions: list[KindSubscription]) -> None:
        self._subscriptions = list(subscriptions)
        self._seen: set[str] = set()
        self._pending: dict[str, _Pending] = {}
        self._spent: set[str] = set()

    @property
    def subscriptions(self) -> list[KindSubscription]:
        return list(self._subscriptions)

    @property
    def subscribed_kinds(self) -> set[str]:
        return {s.kind for s in self._subscriptions}

    def observe(
        self,
        payload: Any,
        *,
        source_node_id: str,
        step: int,
        scope: str = "",
    ) -> int:
        """Record every subscribed kind found in ``payload``. Returns the count
        of NEW occurrences (already-seen ones are silently, correctly ignored).

        ``scope`` distinguishes fan-out siblings: pass the invocation's
        dispatch/item identity so two items producing structurally identical
        values are two events, not one.
        """
        if not self._subscriptions:
            return 0
        identity_scope = scope or source_node_id
        new = 0
        # ONE scan for every subscribed kind, then bucket by slug — a scan per
        # subscription would walk the same payload N times for no new answers.
        wanted = self.subscribed_kinds
        occurrences = [
            occurrence
            for occurrence in find_occurrences(payload, None)
            if occurrence.kind in wanted
        ]
        for occurrence in occurrences:
            identity = occurrence.identity(identity_scope)
            if identity in self._seen:
                continue
            self._seen.add(identity)
            new += 1
            for subscription in self._subscriptions:
                if subscription.kind != occurrence.kind:
                    continue
                if subscription.subscriber_id in self._spent:
                    continue
                # A trigger node never fires on its OWN output: a node that
                # emits the kind it listens for would re-trigger itself every
                # step until max_steps killed the run.
                if subscription.subscriber_id == source_node_id:
                    continue
                key = _key(subscription)
                window = self._pending.get(key)
                if window is None:
                    window = _Pending(opened_at_step=step)
                    self._pending[key] = window
                window.occurrences.append(occurrence)
                window.source_node_ids.append(source_node_id)
        return new

    def drain(self, step: int) -> list[SubscriptionFiring]:
        """Every firing whose debounce window has closed by ``step``.

        Deterministic order: declaration order of the subscriptions, then
        document order of the occurrences within each — so a replay produces
        the same invocations in the same sequence.
        """
        firings: list[SubscriptionFiring] = []
        for subscription in self._subscriptions:
            key = _key(subscription)
            window = self._pending.get(key)
            if window is None or not window.occurrences:
                continue
            if step - window.opened_at_step < subscription.debounce_steps:
                continue
            del self._pending[key]
            if subscription.fire_once:
                self._spent.add(subscription.subscriber_id)
            if subscription.mode == "each":
                for occurrence, source in zip(
                    window.occurrences, window.source_node_ids, strict=True
                ):
                    firings.append(
                        SubscriptionFiring(
                            subscription=subscription,
                            occurrences=[occurrence],
                            step=step,
                            source_node_ids=[source],
                        )
                    )
                    if subscription.fire_once:
                        # fire_once + each is "fire on the FIRST instance",
                        # not "fire once per instance" — the alternative would
                        # make fire_once mean nothing under `each`.
                        break
            else:
                firings.append(
                    SubscriptionFiring(
                        subscription=subscription,
                        occurrences=list(window.occurrences),
                        step=step,
                        source_node_ids=list(window.source_node_ids),
                    )
                )
        return firings

    def pending_count(self) -> int:
        """Occurrences waiting on a debounce window — surfaced so a run page
        can say "2 waiting" instead of looking idle."""
        return sum(len(w.occurrences) for w in self._pending.values())


def _key(subscription: KindSubscription) -> str:
    return f"{subscription.subscriber_id}::{subscription.kind}::{subscription.purpose}"
