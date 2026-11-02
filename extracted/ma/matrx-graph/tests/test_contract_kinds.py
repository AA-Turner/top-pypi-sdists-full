from pydantic import BaseModel

from matrx_graph.contract_kinds import (
    ContractDirection,
    ContractFamily,
    check_schema,
    contract_from_model,
    contract_kind_slug,
    envelope,
    example_from_schema,
)
from matrx_graph.executor.registry import NodeRegistry
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import NodeCategory


class Inputs(BaseModel):
    value: int


class Outputs(BaseModel):
    text: str


class Executor:
    spec = NodeSpec(
        type="data.example",
        category=NodeCategory.DATA,
        display_name="Example",
        input_schema=Inputs,
        output_schema=Outputs,
        output_kind="json",
    )

    async def execute(self, ctx, inputs, config):  # pragma: no cover
        raise NotImplementedError


class DynamicExecutor:
    spec = NodeSpec(
        type="io.dynamic_example",
        category=NodeCategory.IO,
        display_name="Dynamic Example",
        input_schema=Inputs,
        output_schema=Outputs,
        dynamic_output=True,
    )

    async def execute(self, ctx, inputs, config):  # pragma: no cover
        raise NotImplementedError


def test_slug_is_stable_and_disambiguated() -> None:
    one = contract_kind_slug(ContractFamily.TOOL_IO, "server:read", "input")
    two = contract_kind_slug(ContractFamily.TOOL_IO, "server.read", "input")
    assert one == contract_kind_slug(ContractFamily.TOOL_IO, "server:read", "input")
    assert one != two


def test_envelope_preserves_business_value() -> None:
    definition = contract_from_model(
        family=ContractFamily.AGENT_IO,
        source_name="agent-1",
        direction=ContractDirection.OUTPUT,
        model=Outputs,
    )
    value = {"text": "done"}
    verdict = check_schema(value, definition.json_schema)
    wrapped = envelope(definition=definition, value=value, verdict=verdict)
    assert wrapped.value is value
    assert wrapped.checked is True
    assert wrapped.errors == []


def test_registry_never_rewrites_declarations() -> None:
    # AUTO-MINT IS DEAD (Arman 2026-08-20, plan §12): an undeclared spec stays
    # undeclared — the registry no longer stamps fingerprint slugs into
    # input_kind/output_kind, so a node can never READ as kind-compliant while
    # holding only a type signature. Settlement's runtime propagation is the
    # honest replacement for pass-throughs.
    registry = NodeRegistry()
    executor = Executor()
    registry.register(executor)
    assert executor.spec.input_kind is None
    # The fixture declares "json" and it STAYS "json" — the registry no longer
    # replaces the weak declaration with a fingerprint (the ledger's army
    # replaces "json" with real kinds, node by node).
    assert executor.spec.output_kind == "json"
    # The ABI capture is NOT lost: exact contracts still derive for the
    # drift-detection publisher — they just no longer masquerade as
    # declarations.
    contracts = registry.content_ir_contracts()
    assert all(item.source_id == "data.example" for item in contracts)
    assert {item.direction for item in contracts} == {
        ContractDirection.INPUT,
        ContractDirection.OUTPUT,
    }


def test_registry_leaves_dynamic_outputs_unbound_and_undeclared() -> None:
    registry = NodeRegistry()
    executor = DynamicExecutor()
    registry.register(executor)
    assert executor.spec.input_kind is None
    assert executor.spec.output_kind is None
    contracts = registry.content_ir_contracts()
    assert [item.direction for item in contracts] == [ContractDirection.INPUT]


def test_example_generator_resolves_pydantic_defs() -> None:
    class Nested(BaseModel):
        count: int

    class Container(BaseModel):
        nested: Nested
        names: list[str]

    schema = Container.model_json_schema()
    sample = example_from_schema(schema)
    assert sample == {"nested": {"count": 0}, "names": []}
    assert check_schema(sample, schema).errors == []
