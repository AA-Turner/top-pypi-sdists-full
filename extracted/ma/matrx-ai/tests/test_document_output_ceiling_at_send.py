"""THE DOCUMENT-CEILING FLOOR AT THE WIRE — proven on the run that died of it.

Live failure (2026-09-12 19:29Z): workflow run
``d44f53b6-2e8e-49fc-a660-d43b835bbc49``, definition ``9c12787a…`` "Newsroom
Desk", node ``n_cross`` ("What only the whole bundle shows"), an
``ai.agent.start`` step. The node declared NO ceiling of its own. Its agent —
``9182bc0d…`` "Ledger Merge", minted by the meta-builder at 18:33Z — carried
``settings.max_output_tokens = 32000`` while its model (``claude-sonnet-5``,
offering ``9f4b2bb1…``) declares ``ai.model_definition.max_tokens = 128000``.
Its output schema is five arrays of free-text objects.

``chat.request 0a1d1528…`` recorded the result: ``output_tokens = 32000``,
``finish_reason = max_tokens``. The JSON never closed, the step failed
``output_truncated``, and $1.10 of run spend was lost.

The ruling (``matrx_ai.config.output_ceiling``) already existed. It was enforced
only where a ceiling is AUTHORED — agent birth, the agent update surface, and an
authored workflow step's own config — so a STORED row that predates the ruling
(this one predated its deployment by minutes; thousands of older rows predate it
by months) walked straight to the provider. Locked here: the send boundary,
which every provider call in the platform passes through, re-judges the ceiling
against the same ONE predicate.

Why it is a forcing test: every case runs the REAL ``prepare_for_send`` with the
REAL predicate over the run's real schema; only the two things that need a
database (the model catalog and the context-window lookup) are replaced.
``test_the_assertion_fails_when_the_floor_is_neutered`` removes the fix and
proves the wire goes back to 32,000 — an assertion that cannot fail is not a
guard.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config import context_preflight, output_ceiling
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state

CONVERSATION_ID = "conv-ledger-merge"
REQUEST_ID = "0a1d1528-8905-4331-95bf-51dea27f0bef"

#: What the agent row carried, and what the provider therefore permitted.
STORED_CEILING = 32_000
#: ``ai.model_definition.max_tokens`` for claude-sonnet-5.
SONNET_5_MAX = 128_000

#: The "Ledger Merge" output schema, reduced to the shape that decides the
#: question: arrays whose item count the INPUT decides, and free-form strings.
LEDGER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["pairs_examined", "conflicts", "how_to_read_this_ledger"],
    "additionalProperties": False,
    "properties": {
        "pairs_examined": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "document_a": {"type": "string"},
                    "document_b": {"type": "string"},
                    "verdict": {
                        "type": "string",
                        "enum": ["no_shared_facts", "corroborating", "conflicting"],
                    },
                },
            },
        },
        "conflicts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "subject": {"type": "string"},
                    "account_a": {"type": "string"},
                    "account_b": {"type": "string"},
                },
            },
        },
        "how_to_read_this_ledger": {"type": "string"},
    },
}

#: A schema that bounds its own answer: a menu and a capped string.
BOUNDED_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "fail"]},
        "note": {"type": "string", "maxLength": 200},
        "score": {"type": "number"},
    },
}


def _config(
    *,
    ceiling: int | None = STORED_CEILING,
    schema: dict[str, Any] | None = None,
    model: str = "claude-sonnet-5",
) -> SimpleNamespace:
    """The node's request as the executor holds it at the send boundary: the
    agent row's ceiling, and the response_format the structured contract built."""
    response_format: dict[str, Any] | None = None
    if schema is not None:
        response_format = {
            "type": "json_schema",
            "json_schema": {"name": "ledger_merge_output", "schema": schema, "strict": True},
        }
    return SimpleNamespace(
        model=model,
        matrx_model_name=model,
        messages=[{"role": "user", "content": "Merge the four per-document ledgers."}],
        system_instruction=None,
        tools=[],
        prompt_cache_key=None,
        max_output_tokens=ceiling,
        response_format=response_format,
    )


async def _send(config: SimpleNamespace) -> Any:
    return await prepare_for_send(
        config,
        stage=STAGE_LOOP,
        conversation_id=CONVERSATION_ID,
        request_id=REQUEST_ID,
        iteration=1,
    )


@pytest.fixture(autouse=True)
def _no_database(monkeypatch):
    """Replace ONLY the two catalog reads. Everything else is the real thing."""
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)
    # The context-window pre-flight is a different guard; unmeasurable = pass through.
    monkeypatch.setattr(context_preflight, "_declared_window", lambda _ref: None)

    async def _model_max(model_id_or_name: Any) -> int | None:
        return SONNET_5_MAX if str(model_id_or_name) == "claude-sonnet-5" else None

    monkeypatch.setattr(output_ceiling, "model_output_maximum", _model_max)
    yield
    reset_loop_state(CONVERSATION_ID, REQUEST_ID)


@pytest.mark.asyncio
async def test_the_incident_reaches_the_provider_at_the_model_maximum() -> None:
    """n_cross, exactly as it ran: a stored 32,000 under a 128,000 model with a
    document schema. The wire must carry 128,000."""
    config = _config(schema=LEDGER_SCHEMA)

    prep = await _send(config)

    assert config.max_output_tokens == SONNET_5_MAX
    assert "document_output_ceiling" in prep.steps
    # The declaration itself is untouched — only the ceiling moved.
    assert config.response_format["json_schema"]["schema"] is LEDGER_SCHEMA


@pytest.mark.asyncio
async def test_the_assertion_fails_when_the_floor_is_neutered(monkeypatch) -> None:
    """Neuter the fix (the predicate reconciles nothing) and the same call goes
    out at 32,000 again — which is the failure this guard exists to catch."""
    monkeypatch.setattr(
        output_ceiling, "enforce_document_ceiling", lambda *a, **k: [], raising=True
    )
    config = _config(schema=LEDGER_SCHEMA)

    prep = await _send(config)

    assert config.max_output_tokens == STORED_CEILING
    assert "document_output_ceiling" not in prep.steps


@pytest.mark.asyncio
async def test_a_second_iteration_does_not_re_announce() -> None:
    """One repair quiets itself: the canonical config now holds the maximum, so
    a tool loop's later rounds find nothing to fix."""
    config = _config(schema=LEDGER_SCHEMA)

    first = await _send(config)
    second = await _send(config)

    assert "document_output_ceiling" in first.steps
    assert "document_output_ceiling" not in second.steps
    assert config.max_output_tokens == SONNET_5_MAX


@pytest.mark.asyncio
async def test_a_bounded_schema_keeps_its_cost_knob() -> None:
    """Not a blanket raise: every leaf bounds itself, so the smaller number is a
    knowable fact and the organization's knob stands."""
    config = _config(schema=BOUNDED_SCHEMA)

    prep = await _send(config)

    assert config.max_output_tokens == STORED_CEILING
    assert "document_output_ceiling" not in prep.steps


@pytest.mark.asyncio
async def test_free_prose_is_left_to_the_author_time_layers() -> None:
    """A conversation's small prose ceiling is a legitimate cost knob (law 6);
    prose with nowhere to continue is judged where it is authored, not here."""
    config = _config(schema=None)

    prep = await _send(config)

    assert config.max_output_tokens == STORED_CEILING
    assert "document_output_ceiling" not in prep.steps


@pytest.mark.asyncio
async def test_an_absent_ceiling_is_not_invented() -> None:
    """Nothing declared = the offering default applies. Inventing a number here
    would be the silent default the platform forbids."""
    config = _config(ceiling=None, schema=LEDGER_SCHEMA)

    prep = await _send(config)

    assert config.max_output_tokens is None
    assert "document_output_ceiling" not in prep.steps


@pytest.mark.asyncio
async def test_an_unknown_model_maximum_stays_quiet() -> None:
    """The catalog could not say, so the floor says nothing rather than guessing
    a maximum — the release-health sweep still catches the row."""
    config = _config(schema=LEDGER_SCHEMA, model="some-unlisted-model")

    prep = await _send(config)

    assert config.max_output_tokens == STORED_CEILING
    assert "document_output_ceiling" not in prep.steps
