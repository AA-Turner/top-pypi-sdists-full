"""A Collect Inputs field bound to table data is filled at run start (W1.1, 2026-10-02).

The binding is the SAME merge-field declaration an agent variable carries; the host injects
its one resolver through ``matrx_graph.input_bindings``. These pin the node's half: a bound
field is filled, never asked for on the run form, and a binding that finds nothing SAYS so —
in the value and in the run — never a silent empty.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_graph.input_bindings import BoundInput, InputBindingBlocked, configure_input_binding_resolver
from matrx_graph.nodes.io.user_input import UserInputConfig, UserInputExecutor, UserInputInput

BINDING = {
    "kind": "merge_field",
    "source": "record",
    "semantic_type": "collection",
    "table_id": "5b5d2f87-ced4-43ac-8c36-d426dcb96c47",
}


def _config() -> UserInputConfig:
    return UserInputConfig(
        fields=[
            {"key": "topic", "label": "Topic", "type": "text", "required": True},
            {"key": "supplies", "label": "Supplies", "type": "long_text", "required": True, "binding": BINDING},
        ]
    )


class _Ctx(SimpleNamespace):
    async def progress(self, message: str = "", **_: Any) -> None:
        self.said.append(message)


def _ctx() -> _Ctx:
    return _Ctx(user_id="87a6e699-3622-4869-8843-d0867456c0dd", organization_id="org-1", said=[])


@pytest.fixture(autouse=True)
def _clear_resolver():
    yield
    configure_input_binding_resolver(None)


async def _run(ctx: _Ctx, payload: dict[str, Any]):
    return await UserInputExecutor().execute(ctx, UserInputInput(**payload), _config())


async def test_a_bound_field_is_filled_through_the_injected_resolver() -> None:
    seen: dict[str, Any] = {}

    async def resolver(bindings, user_id, organization_id):
        seen.update(bindings=dict(bindings), user_id=user_id, organization_id=organization_id)
        return {"supplies": BoundInput(text="- Foam rollers: backordered", present=True)}

    configure_input_binding_resolver(resolver)
    ctx = _ctx()
    result = await _run(ctx, {"topic": "Weekly reorder"})
    out = result.result.model_dump()
    assert out["supplies"] == "- Foam rollers: backordered"
    assert seen["bindings"] == {"supplies": BINDING}
    assert seen["user_id"] == ctx.user_id and seen["organization_id"] == "org-1"
    assert ctx.said == []


async def test_a_binding_that_finds_nothing_says_so_in_the_value_and_the_run() -> None:
    async def resolver(bindings, user_id, organization_id):
        return {
            "supplies": BoundInput(
                text="[not available — Clinic Supplies Count has no rows you can read]",
                present=False,
                absent_sentence="Clinic Supplies Count has no rows you can read.",
            )
        }

    configure_input_binding_resolver(resolver)
    ctx = _ctx()
    out = (await _run(ctx, {"topic": "Weekly reorder"})).result.model_dump()
    assert out["supplies"].startswith("[not available")
    assert ctx.said == ["Supplies: Clinic Supplies Count has no rows you can read."]


async def test_a_blocking_binding_parks_the_run_with_its_sentence() -> None:
    async def resolver(bindings, user_id, organization_id):
        raise InputBindingBlocked("Supplies could not be read, so this run cannot start.", key="supplies")

    configure_input_binding_resolver(resolver)
    with pytest.raises(ValueError, match="Supplies could not be read"):
        await _run(_ctx(), {"topic": "Weekly reorder"})


async def test_no_resolver_refuses_by_name() -> None:
    with pytest.raises(ValueError, match="filled from your data"):
        await _run(_ctx(), {"topic": "Weekly reorder"})


def test_a_bound_field_is_never_asked_for_on_the_run_form() -> None:
    config = _config()
    schema = config.effective_output_json_schema()
    assert schema["properties"]["supplies"]["ui:hidden"] is True
    assert schema["required"] == ["topic"]
    bound = next(f for f in config.fields if f.key == "supplies")
    assert bound.effective_sourcing() == "optional"
