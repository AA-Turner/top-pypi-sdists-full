"""A typed health payload must survive the real encoder and committed replay."""

import json

import pytest
from pydantic import ValidationError

from matrx_connect.context.data_types import (
    DATA_TYPE_REGISTRY,
    VaultPasswordHealthProgressData,
    VaultPasswordHealthScanReferenceData,
)
from matrx_connect.emitters.stream_emitter import StreamEmitter


class Journal:
    stream_id = "22222222-2222-4222-8222-222222222222"

    def __init__(self):
        self.wires = []

    async def enqueue(self, *, sequence, wire, publish):
        self.wires.append(wire)
        await publish(wire)

    async def close(self, **kwargs):
        pass


def reference():
    return VaultPasswordHealthScanReferenceData(
        request_id="request",
        execution_id="execution",
        status_path="/status",
        events_path="/events",
        rejoin_path="/rejoin",
        result_path="/result",
        resume_path="/resume",
    )


@pytest.mark.asyncio
async def test_real_typed_wire_and_committed_replay_keep_type_and_never_take_legacy_path(
    monkeypatch,
):
    emitter = StreamEmitter(heartbeat_interval=3600)
    journal = Journal()
    emitter.attach_journal_sink(journal)
    monkeypatch.setattr(emitter, "_serialize", lambda *_: pytest.fail("legacy payload path"))
    await emitter.send_data(reference())
    await emitter.send_data(
        VaultPasswordHealthProgressData(
            request_id="request",
            execution_id="execution",
            checked=3,
            skipped=2,
        )
    )
    await emitter.send_end()
    replay = [wire async for wire in emitter.generate_replay()]
    assert replay == journal.wires
    payloads = [json.loads(wire)["data"] for wire in replay[:-1]]
    assert "__kind" not in payloads[0]  # `type` discriminates it; it is not a kind (Content IR rule 28)
    assert payloads[0]["type"] == "vault_password_health_scan_reference"
    assert payloads[1] == {
        "type": "vault_password_health_progress",
        "request_id": "request",
        "execution_id": "execution",
        "checked": 3,
        "skipped": 2,
    }
    assert set(payloads[0]) == {
        "type",
        "request_id",
        "execution_id",
        "resumed_from_execution_id",
        "status_path",
        "events_path",
        "rejoin_path",
        "result_path",
        "resume_path",
    }


@pytest.mark.parametrize(
    "model", [VaultPasswordHealthProgressData, VaultPasswordHealthScanReferenceData]
)
def test_registry_schema_is_closed_and_exposes_only_its_type_discriminator(model):
    assert DATA_TYPE_REGISTRY[model.model_fields["type"].default] is model
    schema = model.model_json_schema()
    assert schema["additionalProperties"] is False
    assert "__kind" not in schema["properties"]
    assert "marker" not in schema["properties"]
    payload = (
        reference().model_dump()
        if model is VaultPasswordHealthScanReferenceData
        else {
            "request_id": "request",
            "execution_id": "execution",
            "checked": 0,
            "skipped": 0,
        }
    )
    for forbidden in ("snapshot", "findings", "item_id", "password", "grant", "jwt"):
        with pytest.raises(ValidationError):
            model.model_validate({**payload, forbidden: "private"})


@pytest.mark.parametrize("count", [-1, True, "2"])
def test_progress_refuses_invalid_counts(count):
    with pytest.raises(ValidationError):
        VaultPasswordHealthProgressData(
            request_id="request", execution_id="execution", checked=count, skipped=0
        )


def test_an_older_journal_rows_kind_marker_still_parses_and_is_never_written_back():
    """Rows journaled before 2026-10-27 carry `__kind: password_health_progress` (Content IR rule 28)."""
    old = {
        "type": "vault_password_health_progress",
        "__kind": "password_health_progress",
        "request_id": "request",
        "execution_id": "execution",
        "checked": 1,
        "skipped": 0,
    }
    parsed = VaultPasswordHealthProgressData.model_validate(old)
    assert "__kind" not in parsed.model_dump(by_alias=True)
    assert "__kind" not in json.loads(parsed.model_dump_json(by_alias=True))
