"""The channel-drain gather reports item_indexes too, so a pairing step never
meets a silently empty index list (the engine path always filled it)."""

from types import SimpleNamespace

from matrx_graph.nodes.control.gather import GatherConfig, GatherExecutor, GatherInput


async def test_channel_gather_names_each_kept_values_position() -> None:
    ctx = SimpleNamespace(channels=SimpleNamespace(get=lambda _n, _d: [{"t": "a"}, {"error": "x"}, {"t": "c"}]))
    res = await GatherExecutor().execute(ctx, GatherInput(), GatherConfig(channel="pages"))  # type: ignore[arg-type]
    assert res.result.values == [{"t": "a"}, {"t": "c"}]
    assert res.result.item_indexes == [0, 2]
