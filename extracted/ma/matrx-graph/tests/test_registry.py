from __future__ import annotations

import pytest
from matrx_graph import NodeRegistry, NodeRegistryError
from matrx_graph.nodes.control.branch import BranchExecutor
from matrx_graph.nodes.data.transform import TransformExecutor
from matrx_graph.types.result import success
from pydantic import BaseModel


def test_register_and_get():
    reg = NodeRegistry()
    reg.register(BranchExecutor())
    assert reg.has("control.branch")
    assert reg.get("control.branch").spec.node_type == "control.branch"


def test_register_duplicate_raises():
    reg = NodeRegistry()
    reg.register(BranchExecutor())
    with pytest.raises(NodeRegistryError):
        reg.register(BranchExecutor())


def test_register_duplicate_overwrite_allowed():
    reg = NodeRegistry()
    reg.register(BranchExecutor())
    reg.register(BranchExecutor(), overwrite=True)  # should not raise


def test_get_unknown_raises_with_known_list():
    reg = NodeRegistry()
    reg.register(TransformExecutor())
    try:
        reg.get("nope.nope")
    except NodeRegistryError as e:
        assert "data.transform" in str(e)
    else:
        pytest.fail("expected NodeRegistryError")


def test_all_specs_returns_all_registered():
    reg = NodeRegistry()
    reg.register(BranchExecutor())
    reg.register(TransformExecutor())
    types = {s.node_type for s in reg.all_specs()}
    assert types == {"control.branch", "data.transform"}


def test_palette_produces_serializable_descriptors():
    reg = NodeRegistry()
    reg.register(BranchExecutor())
    palette = reg.palette()
    assert isinstance(palette, list)
    assert palette[0]["type"] == "control.branch"
    assert "config_schema" in palette[0]
    assert palette[0]["config_schema"]["properties"]["predicate"]["ui:widget"] == "code"


def test_executor_protocol_runtime_check():
    class NotAnExecutor:  # No `spec`, no `execute`
        pass

    reg = NodeRegistry()

    # Registry does not require Protocol conformance at register-time; errors
    # surface when the scheduler tries to call .execute(). Confirming the
    # registry is permissive keeps plugin authors unblocked.
    class LooksLikeOne:
        def __init__(self) -> None:
            from matrx_graph.types.node_spec import NodeSpec
            from matrx_graph.types.primitives import NodeCategory

            class _In(BaseModel):
                pass

            self.spec = NodeSpec(
                type="fake.one",
                category=NodeCategory.CUSTOM,
                display_name="Fake",
                input_schema=_In,
            )

        async def execute(self, ctx, inputs, config):  # type: ignore[no-untyped-def]
            return success(inputs)

    reg.register(LooksLikeOne())
    assert reg.has("fake.one")
