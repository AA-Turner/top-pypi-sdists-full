"""``data.read_record`` — the reader of ONE platform Record, proved.

The fake gateway here stands in for the HOST (aidream's entity registry +
``iam.has_access_for`` + the ORM read), which is the only way this package can
be tested at all: matrx-graph never imports the host. What is under test is the
part that IS this package's: the refusals, the shaping, and the fact that
identity comes from the carried context and from nowhere else.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from matrx_graph.nodes.data.read_record import (
    PlatformRecord,
    ReadRecordExecutor,
    ReadRecordInput,
)
from matrx_graph.records import (
    RecordEntity,
    RecordReadRefused,
    configure_record_gateway,
    is_record_gateway_configured,
)
from matrx_graph.types.result import Failure, Success
from matrx_graph.types import EmptyConfig

DOC = RecordEntity(
    entity_type="google_document",
    schema_name="workbench",
    table_name="google_document",
    label="Google Document",
    title_column="title",
    excluded_columns=("raw_oauth_payload",),
)

ROW: dict[str, Any] = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Q3 Plan",
    "organization_id": "00000000-0000-4000-8000-0000000fffa1",
    "raw_oauth_payload": "SECRET-NOT-FOR-CLIENTS",
}


@dataclass
class FakeGateway:
    entities: dict[str, RecordEntity] = field(default_factory=lambda: {"google_document": DOC})
    rows: dict[tuple[str, str], dict[str, Any]] = field(
        default_factory=lambda: {("google_document", ROW["id"]): dict(ROW)}
    )
    allowed: set[tuple[str, str, str]] = field(default_factory=set)
    access_questions: list[tuple[str, str, str]] = field(default_factory=list)

    async def describe_entity(self, entity_type: str) -> RecordEntity | None:
        return self.entities.get(entity_type)

    async def known_entity_types(self) -> list[str]:
        return sorted(self.entities)

    async def may_read(self, *, actor_id: str, entity_type: str, record_id: str) -> bool:
        self.access_questions.append((actor_id, entity_type, record_id))
        return (actor_id, entity_type, record_id) in self.allowed

    async def read_row(self, *, entity: RecordEntity, record_id: str):
        return self.rows.get((entity.entity_type, record_id))


class FakeApp:
    """Only what the node reads off the carried context: the actor + the org."""

    user_id = "11111111-1111-1111-1111-111111111111"
    organization_id = "00000000-0000-4000-8000-0000000fffa1"


class FakeCtx:
    def __init__(self, user_id: str | None = FakeApp.user_id) -> None:
        self.app = FakeApp()
        self._user_id = user_id

    @property
    def user_id(self) -> str:
        return self._user_id or ""

    @property
    def organization_id(self) -> str | None:
        return self.app.organization_id


@pytest.fixture
def gateway():
    gw = FakeGateway()
    configure_record_gateway(gw)
    yield gw
    configure_record_gateway(None)


async def _run(inputs: ReadRecordInput, ctx: FakeCtx | None = None):
    return await ReadRecordExecutor().execute(
        ctx or FakeCtx(), inputs, EmptyConfig()  # type: ignore[arg-type]
    )


def _allow(gw: FakeGateway, entity_type: str, record_id: str) -> None:
    gw.allowed.add((FakeApp.user_id, entity_type, record_id))


# ---------------------------------------------------------------------------
# 1. known type + accessible row -> the shaped record, carrying __kind
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_accessible_record_comes_back_shaped_and_kind_marked(gateway):
    _allow(gateway, "google_document", ROW["id"])

    out = await _run(ReadRecordInput(entity_type="google_document", record_id=ROW["id"]))

    assert isinstance(out, Success), out
    record = out.result
    assert isinstance(record, PlatformRecord)
    dumped = record.model_dump(by_alias=True)
    # __kind is part of the DATA, not a side channel.
    assert dumped["__kind"] == "platform_record"
    assert dumped["entity_type"] == "google_document"
    assert dumped["record_id"] == ROW["id"]
    assert dumped["table"] == "workbench.google_document"
    assert dumped["entity_label"] == "Google Document"
    # The label comes from the REGISTRY's title_column, not a guess.
    assert dumped["record_label"] == "Q3 Plan"
    assert dumped["organization_id"] == ROW["organization_id"]
    assert dumped["fields"]["title"] == "Q3 Plan"
    # A registry-excluded column is withheld AND named — never silently dropped.
    assert "raw_oauth_payload" not in dumped["fields"]
    assert dumped["hidden_fields"] == ["raw_oauth_payload"]

    # Identity was the CARRIED actor; the node asked about that actor and no other.
    assert gateway.access_questions == [
        (FakeApp.user_id, "google_document", ROW["id"])
    ]


@pytest.mark.asyncio
async def test_the_node_takes_no_identity_arguments():
    """A workflow author cannot choose whose eyes this reads with."""
    fields = set(ReadRecordInput.model_fields)
    assert fields == {"entity_type", "record_id"}


# ---------------------------------------------------------------------------
# 2. denied -> the refusal sentence, and NO row data
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_denied_refuses_by_name_and_leaks_nothing(gateway):
    # The row exists and is in the same organization as the actor — and the
    # access answer is still the only thing that matters.
    out = await _run(ReadRecordInput(entity_type="google_document", record_id=ROW["id"]))

    assert isinstance(out, Failure), out
    assert out.error.code == "access_denied"
    message = out.error.message
    assert "do not have access" in message
    assert "share it with you at view level" in message  # the remedy
    blob = f"{message} {out.error.details}"
    for secret in ("Q3 Plan", ROW["organization_id"], "SECRET-NOT-FOR-CLIENTS"):
        assert secret not in blob, f"a denied read leaked {secret!r}"


# ---------------------------------------------------------------------------
# 3. unknown type -> refusal NAMING the type
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_unknown_entity_type_is_named(gateway):
    out = await _run(ReadRecordInput(entity_type="gogle_doc", record_id=ROW["id"]))

    assert isinstance(out, Failure), out
    assert out.error.code == "unknown_entity_type"
    assert "gogle_doc" in out.error.message
    # And it says what IS available, so the refusal is actionable.
    assert "google_document" in out.error.message
    # Access was never asked — an unknown type has no token to ask about.
    assert gateway.access_questions == []


# ---------------------------------------------------------------------------
# 4. missing row -> refusal, never an empty success
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_absent_row_refuses_instead_of_succeeding_empty(gateway):
    missing = "00000000-0000-0000-0000-0000000000ff"
    _allow(gateway, "google_document", missing)

    out = await _run(ReadRecordInput(entity_type="google_document", record_id=missing))

    assert isinstance(out, Failure), out
    assert out.error.code == "record_not_found"
    assert missing in out.error.message
    assert "workbench.google_document" in out.error.message


# ---------------------------------------------------------------------------
# The rest of the refusal ladder
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_no_actor_in_context_refuses(gateway):
    _allow(gateway, "google_document", ROW["id"])

    out = await _run(
        ReadRecordInput(entity_type="google_document", record_id=ROW["id"]),
        ctx=FakeCtx(user_id=None),
    )

    assert isinstance(out, Failure), out
    assert out.error.code == "no_actor_in_context"
    # It never fell back to a default identity to get an answer.
    assert gateway.access_questions == []


@pytest.mark.asyncio
async def test_unwired_gateway_refuses_with_the_wiring_remedy():
    configure_record_gateway(None)
    assert not is_record_gateway_configured()

    out = await _run(ReadRecordInput(entity_type="google_document", record_id=ROW["id"]))

    assert isinstance(out, Failure), out
    assert out.error.code == "record_gateway_unavailable"
    assert "configure_record_gateway" in out.error.message


@pytest.mark.asyncio
async def test_blank_reference_refuses(gateway):
    out = await _run(ReadRecordInput(entity_type="google_document", record_id="   "))

    assert isinstance(out, Failure), out
    assert out.error.code == "incomplete_reference"


# ---------------------------------------------------------------------------
# The spec itself — what the palette (and the kind gate) will read
# ---------------------------------------------------------------------------


def test_spec_declares_the_platform_record_kind_not_the_fallback():
    spec = ReadRecordExecutor.spec
    assert spec.node_type == "data.read_record"
    assert spec.display_name == "Read a Record"
    assert spec.output_kind == "platform_record"
    # generic_structured is the can-never-fail fallback; it is never a declaration.
    assert spec.output_kind != "generic_structured"
    assert not spec.dynamic_output
    schema = spec.output_json_schema()
    assert "__kind" in schema["properties"], "the kind marker must be IN the schema"


def test_the_node_is_a_builtin_and_appears_in_the_palette():
    from matrx_graph.executor.registry import NodeRegistry
    from matrx_graph.nodes import register_builtin_nodes

    registry = register_builtin_nodes(NodeRegistry())
    entry = next(
        p for p in registry.palette() if p["type"] == "data.read_record"
    )
    assert entry["display_name"] == "Read a Record"


@pytest.mark.asyncio
async def test_a_type_with_no_door_is_refused_by_name_never_not_found(gateway):
    """The gateway's named refusal reaches the person as itself — not "record_not_found"."""
    sentence = "context_value_refs lives in the record store; read it through the custom.context_* doors."
    gateway.entities["context_value_refs"] = RecordEntity(
        entity_type="context_value_refs", schema_name="custom", table_name="x",
        label="", title_column="", excluded_columns=(),
    )
    _allow(gateway, "context_value_refs", "r1")

    async def refuse(*, entity, record_id):
        raise RecordReadRefused(sentence)

    gateway.read_row = refuse  # type: ignore[method-assign]
    out = await _run(ReadRecordInput(entity_type="context_value_refs", record_id="r1"))
    assert isinstance(out, Failure), out
    assert out.error.code == "record_type_not_readable"
    assert sentence in out.error.message
    assert "No " not in out.error.message.split(sentence)[0]
