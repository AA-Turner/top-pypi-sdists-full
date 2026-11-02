"""Adversarial review of the kinds runtime (availability / accessor / edges /
triggers) — 2026-08-21.

Every test here either PINS a behavior that held under attack, or is an
``xfail(strict=True)`` documenting a REAL, reproducible hole with the intended
behavior in the assertion. When a hole is fixed, its xfail turns into an
XPASS failure and the marker must be deleted — the test then guards the fix.

Holes documented here (details in each test):

* H1 — accessor: a path segment applied to a SCALAR resolves through
  ``hasattr``/``getattr`` and leaks bound methods / classes (``n.text.strip``,
  ``n.text.__class__``) as "values". Downstream, the picker API's
  ``ReferenceResolution.values: list[JsonValue]`` cannot validate a bound
  method, so a typo'd reference 500s ``GET /runs/{id}/kind-reference``.
* H2 — subscriptions: occurrence identity ignores the FIRING. A node that
  fires twice in one run (loop / join_policy='any') and produces an identical
  payload both times fires a kind trigger ONCE — the second real production is
  swallowed as a "pass-through", contradicting the module's own contract
  ("a genuinely NEW production of an identical value is a genuinely new
  firing").
* H3 — triggers: a debounce window still open when the frontier drains is
  silently dropped — the run COMPLETES and the trigger never fires, even
  though its kind appeared. No deadlock-guard, no note, no park.
* H4 — subscriptions: matcher state (``_seen`` / ``_pending`` / ``_spent``)
  lives only in memory and is not checkpointed; the scheduler builds a fresh
  ``SubscriptionMatcher`` in ``__init__`` and never reconstructs it on
  ``resume()``. ``trigger_fire_once`` therefore re-fires after a crash/resume,
  and pending debounce occurrences observed before the checkpoint are lost.
"""

from __future__ import annotations

import pytest
from matrx_graph import RunStatus
from matrx_graph.content_ir.accessor import resolve_path
from matrx_graph.content_ir.subscriptions import KindSubscription, SubscriptionMatcher

from tests.test_kind_routing import (
    _definition,
    _registry,
    _run,
    _trigger_definition,
)

# ---------------------------------------------------------------------------
# H1 — accessor traversal into scalars leaks Python attributes
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason=(
        "HOLE H1: _child() falls through to hasattr/getattr for non-Mapping, "
        "non-BaseModel containers, so a path into a str resolves builtin "
        "methods. 'n.text.strip' yields a bound method with NO note; the API "
        "layer's list[JsonValue] then blows up (500). A path into a scalar "
        "should be an absence recorded in notes, never an attribute lookup."
    ),
)
def test_a_path_into_a_scalar_is_an_absence_not_an_attribute_lookup() -> None:
    resolution = resolve_path({"text": "hello"}, "text.strip", unwrap_root=False)
    assert resolution.values == []  # currently: [<built-in method strip>]
    assert resolution.notes  # and currently silent — no note at all


@pytest.mark.xfail(
    strict=True,
    reason=(
        "HOLE H1 (dunder variant): 'n.text.__class__' resolves to <class "
        "'str'> — type objects offered as data values."
    ),
)
def test_dunder_segments_do_not_resolve_to_type_objects() -> None:
    resolution = resolve_path({"text": "hello"}, "text.__class__", unwrap_root=False)
    assert resolution.values == []


# ---------------------------------------------------------------------------
# H2 — a second REAL production of an identical value is swallowed
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason=(
        "HOLE H2: occurrence identity is scope#kind@path where the scheduler "
        "passes scope=node_id (no firing number) for non-fanned invocations. "
        "A node re-fired in one run (loop, join_policy='any') that produces "
        "an identical payload both times triggers subscribers ONCE — the "
        "second real production is deduped as a pass-through. Contradicts the "
        "subscriptions module's own dedupe contract. Fix: fold the firing "
        "number into the observe() scope."
    ),
)
def test_a_second_real_production_of_an_identical_value_fires_again() -> None:
    matcher = SubscriptionMatcher(
        [KindSubscription(subscriber_id="saver", kind="website", mode="all")]
    )
    payload = {"__kind": "website", "url": "https://example.com"}
    # firing 1 of node "fetch"
    assert matcher.observe(payload, source_node_id="fetch", step=1) == 1
    assert len(matcher.drain(1)) == 1
    # firing 2 of node "fetch", two super-steps later — a NEW production event
    new = matcher.observe(payload, source_node_id="fetch", step=3)
    assert new == 1  # currently 0: swallowed
    assert len(matcher.drain(3)) == 1  # currently 0: the trigger never fires


# ---------------------------------------------------------------------------
# H3 — an open debounce window is dropped when the run drains
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason=(
        "HOLE H3: the drive loop exits when the frontier drains; pending "
        "debounce windows are never force-drained (and never parked, and "
        "never noted). A trigger with debounce_steps longer than the run's "
        "remaining super-steps NEVER fires even though its kind appeared — "
        "the motivating persistence case silently writes zero rows. The "
        "end-of-run path must flush (or at minimum loudly report) "
        "SubscriptionMatcher.pending_count() before completing."
    ),
)
async def test_an_open_debounce_window_still_fires_before_the_run_completes():
    registry, _source, sink = _registry(web=2)
    result = await _run(
        _trigger_definition({"trigger_kind": "web_result", "trigger_debounce_steps": 10}),
        registry,
        "adv-debounce-drop",
    )
    assert result.status is RunStatus.COMPLETED
    assert len(sink.calls) == 1  # currently 0: the firing is silently lost


# ---------------------------------------------------------------------------
# H4 — matcher state is not durable across a scheduler rebuild (resume)
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason=(
        "HOLE H4: SubscriptionMatcher state is neither checkpointed nor "
        "reconstructed on resume (scheduler.py uses _subscriptions only in "
        "__init__/observe/drain). A fresh matcher — which is exactly what a "
        "crash/park + resume in a new process builds — has an empty _spent "
        "set, so trigger_fire_once fires AGAIN post-resume. This test models "
        "the resume by rebuilding the matcher; durable fire-once must "
        "survive it."
    ),
)
def test_fire_once_survives_a_matcher_rebuild_as_on_resume() -> None:
    subscription = KindSubscription(subscriber_id="once", kind="website", fire_once=True)
    live = SubscriptionMatcher([subscription])
    live.observe(
        {"__kind": "website", "url": "https://a.com"}, source_node_id="a", step=1
    )
    assert len(live.drain(1)) == 1  # fired, spent

    resumed = SubscriptionMatcher([subscription])  # what resume() builds today
    resumed.observe(
        {"__kind": "website", "url": "https://b.com"}, source_node_id="b", step=5
    )
    assert len(resumed.drain(5)) == 0  # currently 1: fire_once fires twice


# ---------------------------------------------------------------------------
# Attacked and HELD — behaviors that survived the assault, pinned
# ---------------------------------------------------------------------------


async def test_held_empty_each_selection_prunes_and_does_not_deadlock_a_join():
    # source emits ZERO web_result instances; the `each` edge must not fire the
    # sink AND must not wedge the run.
    registry, _source, sink = _registry(web=0, news=1)
    result = await _run(
        _definition({"kind_filter": "web_result", "fan_out": "each"}),
        registry,
        "adv-empty-each",
    )
    assert result.status is RunStatus.COMPLETED
    assert sink.calls == []


async def test_held_empty_each_beside_an_ordinary_edge_still_fires_the_join():
    # sink has an ordinary DATA edge (joins) plus an empty `each` edge
    # (dispatcher, excluded from the join set). The join must fire exactly
    # once; the empty fan-out must contribute nothing and block nothing.
    from matrx_graph.types.definition import Definition

    registry, _source, sink = _registry(web=0, news=1)
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "source",
                    "type": "test.kind_source",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "sink",
                    "type": "test.kind_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {"id": "plain", "source": "source", "target": "sink", "data": {}},
                {
                    "id": "fan",
                    "source": "source",
                    "target": "sink",
                    "data": {"kind_filter": "web_result", "fan_out": "each"},
                },
            ],
        }
    )
    result = await _run(definition, registry, "adv-each-beside-join")
    assert result.status is RunStatus.COMPLETED
    assert len(sink.calls) == 1  # the join fired; no deadlock, no double-fire


async def test_held_sibling_each_edges_do_not_collide_in_the_dispatch_keyspace():
    # Two `each` edges from one source to one sink: dispatch identity is
    # derived per EDGE (edge:{edge_id}:...), so the siblings must both fan out
    # fully instead of the second colliding with the first.
    from matrx_graph.types.definition import Definition

    registry, _source, sink = _registry(web=2, news=2)
    definition = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "source",
                    "type": "test.kind_source",
                    "position": {"x": 0, "y": 0},
                    "data": {"config": {}},
                },
                {
                    "id": "sink",
                    "type": "test.kind_sink",
                    "position": {"x": 200, "y": 0},
                    "data": {"config": {}},
                },
            ],
            "edges": [
                {
                    "id": "each-web",
                    "source": "source",
                    "target": "sink",
                    "data": {"kind_filter": "web_result", "fan_out": "each"},
                },
                {
                    "id": "each-news",
                    "source": "source",
                    "target": "sink",
                    "data": {"kind_filter": "news_result", "fan_out": "each"},
                },
            ],
        }
    )
    result = await _run(definition, registry, "adv-sibling-each")
    assert result.status is RunStatus.COMPLETED
    kinds = sorted(c["value"]["__kind"] for c in sink.calls)
    assert kinds == ["news_result", "news_result", "web_result", "web_result"]


async def test_held_each_trigger_over_many_instances_is_unbounded_by_design():
    # 40 instances -> 40 invocations of the triggered node. There is NO cap and
    # debounce does not bound `each` (it only widens the window). Pinned so a
    # future cap is a deliberate change; flagged in the review as a cost
    # footgun for paid nodes.
    registry, _source, sink = _registry(web=40)
    result = await _run(
        _trigger_definition({"trigger_kind": "web_result", "trigger_mode": "each"}),
        registry,
        "adv-trigger-40",
    )
    assert result.status is RunStatus.COMPLETED
    assert len(sink.calls) == 40


def test_held_debounce_in_one_super_step_coalesces_all_mode_to_one_firing() -> None:
    # 500 instances landing in ONE super-step: `all` mode fires ONCE with all
    # 500 — debounce never multiplies firings within a window.
    matcher = SubscriptionMatcher(
        [KindSubscription(subscriber_id="s", kind="item", mode="all", debounce_steps=5)]
    )
    payload = {"items": [{"__kind": "item", "i": i} for i in range(500)]}
    matcher.observe(payload, source_node_id="gen", step=1)
    assert matcher.drain(3) == []  # window still open
    firings = matcher.drain(6)
    assert len(firings) == 1
    assert len(firings[0].occurrences) == 500


def test_held_a_steady_stream_cannot_postpone_a_debounced_firing_forever() -> None:
    # The window clock starts at the FIRST occurrence; later arrivals join the
    # window instead of resetting it.
    matcher = SubscriptionMatcher(
        [KindSubscription(subscriber_id="s", kind="item", mode="all", debounce_steps=3)]
    )
    for step in range(1, 4):
        matcher.observe(
            {"items": [{"__kind": "item", "i": step}]}, source_node_id=f"n{step}", step=step
        )
    firings = matcher.drain(4)
    assert len(firings) == 1
    assert len(firings[0].occurrences) == 3
