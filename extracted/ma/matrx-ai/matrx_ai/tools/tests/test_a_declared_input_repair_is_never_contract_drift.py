"""A call the tool's own declared input repair settles is never Content IR input drift.

Live 2026-11-14: ask_person got ``message: ''``; its input model's ``mode="before"`` repair
(``repair_ask``) filled the message from the first question and the tool ran the repaired
call, yet the executor judged the RAW arguments and filed ``tool_input_contract_drift`` four
times. The shadow check now judges what the tool ran (``arguments_as_meant``). A model that
merely IGNORES a key the contract forbids declares no repair, so that stays drift.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.contract_kinds import check_schema
from pydantic import BaseModel, ConfigDict, model_validator

from matrx_ai.tools.executor import arguments_as_meant

CONTRACT = {
    "type": "object",
    "properties": {
        "message": {"type": "string", "minLength": 1},
        "question": {"type": "string"},
    },
    "required": ["message"],
    "additionalProperties": False,
}


class RepairingArgs(BaseModel):
    message: str
    question: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _as_meant(cls, data: Any) -> Any:
        if isinstance(data, dict) and not (data.get("message") or "").strip() and data.get("question"):
            return {**data, "message": data["question"]}
        return data


class IgnoringArgs(BaseModel):
    model_config = ConfigDict(extra="ignore")
    message: str


def test_the_raw_call_fails_the_contract_but_the_repaired_call_passes() -> None:
    raw = {"message": "", "question": "Which plan should I pick?"}
    assert check_schema(raw, CONTRACT).errors, "the raw call must fail the contract (else this test proves nothing)"
    meant = arguments_as_meant(raw, RepairingArgs)
    assert meant == {"message": "Which plan should I pick?", "question": "Which plan should I pick?"}
    assert not check_schema(meant, CONTRACT).errors


def test_a_model_that_only_ignores_a_forbidden_key_declares_no_repair() -> None:
    raw = {"message": "hi", "confirm_opens": True}
    assert check_schema(raw, CONTRACT).errors
    assert arguments_as_meant(raw, IgnoringArgs) is None


def test_a_call_the_model_refuses_keeps_the_raw_verdict() -> None:
    assert arguments_as_meant({"question": None}, RepairingArgs) is None
    assert arguments_as_meant({"message": ""}, None) is None

