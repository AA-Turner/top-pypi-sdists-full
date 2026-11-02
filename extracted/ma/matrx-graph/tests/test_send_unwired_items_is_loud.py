"""``control.send`` must not fan out ZERO items in silence.

Dispatching nothing is legal — an empty list is a real result. Dispatching
nothing because nothing REACHED ``items`` is an authoring mistake that looks
identical: the node succeeds, ``dispatched`` is 0 either way, and the target
node simply never runs.

The common shape of that mistake, found by running a real scheduler graph
during the kind-distillation pass (chip task_34291ebc, 2026-08-20): an upstream
``data.transform`` hands over ``{"result": [...]}``, ``SendInput`` is
``extra="allow"``, and the list is swallowed under the wrong key. The node was
holding the author's list and reported success having sent none of it.

The node still does NOT auto-map — guessing which key was meant is a decision it
does not get to make — but it says what arrived.
"""

from __future__ import annotations

import logging

from matrx_graph.nodes.control.send import SendConfig, SendExecutor, SendInput


class _CollectingCtx:
    def __init__(self) -> None:
        self.sent: list[tuple[str, dict]] = []

    def send(self, target: str, payload: dict) -> None:
        self.sent.append((target, payload))


async def test_list_arriving_under_the_wrong_key_names_that_key(caplog):
    caplog.set_level(logging.WARNING)
    ctx = _CollectingCtx()

    # Exactly what the scheduler passes when data.transform feeds control.send.
    result = await SendExecutor().execute(
        ctx, SendInput(result=[{"n": 1}, {"n": 2}]), SendConfig(target_node_id="worker")
    )

    assert result.result.dispatched == 0
    assert ctx.sent == []
    warning = caplog.text
    assert "nothing reached" in warning
    assert "'result'" in warning, warning
    assert "worker" in warning


async def test_deliberately_empty_list_is_not_flagged(caplog):
    """``items=[]`` explicitly is a legitimate result and must stay quiet."""
    caplog.set_level(logging.WARNING)

    result = await SendExecutor().execute(
        _CollectingCtx(), SendInput(items=[]), SendConfig(target_node_id="worker")
    )

    assert result.result.dispatched == 0
    assert "nothing reached" not in caplog.text


async def test_wired_items_still_dispatch_one_send_each():
    ctx = _CollectingCtx()

    result = await SendExecutor().execute(
        ctx,
        SendInput(items=[{"n": 1}, {"n": 2}, {"n": 3}]),
        SendConfig(target_node_id="worker", payload_key="row"),
    )

    assert result.result.dispatched == 3
    assert ctx.sent == [("worker", {"row": {"n": i}}) for i in (1, 2, 3)]
