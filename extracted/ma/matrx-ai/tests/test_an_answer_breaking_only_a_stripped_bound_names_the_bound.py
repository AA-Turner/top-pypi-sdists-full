"""An answer that breaks only a bound the provider never received names that bound, not a divergence.

`extend.formula_author` (claude-sonnet-5-5, 2026-11-19 06:13Z) answered a `notes` string longer
than its declared `maxLength`. The request boundary strips `maxLength` for Anthropic
(`unsupported_structured_output_keywords`), so the provider enforced the shape but could never hold
the bound — and the finding still said "the translated wire schema and the declared schema have
diverged; the divergence is the bug", sending the reader after a translator bug that did not exist.

The check itself is unchanged: the answer is still off contract and still recorded. Only the
remedy is now the true one, and the stripped bound is named in `unenforced_bounds`.
"""

from __future__ import annotations

from matrx_ai.schema.answer_contract import bounds_the_provider_cannot_carry, verify_answer

SCHEMA = {
    "type": "object",
    "properties": {
        "mode": {"type": "string", "enum": ["list_pattern", "manual_css"]},
        "notes": {"type": "string", "maxLength": 40},
        "pattern": {"type": "string"},
    },
    "required": ["mode", "notes"],
    "additionalProperties": False,
}

TOO_LONG = "Kept the working title, link and company reads; added a region column."


def test_an_answer_breaking_only_a_stripped_bound_names_it() -> None:
    answer = {"mode": "list_pattern", "notes": TOO_LONG}
    assert verify_answer(answer, SCHEMA), "the declared bound is still judged"
    assert bounds_the_provider_cannot_carry(answer, SCHEMA, "anthropic") == ["maxLength"]


def test_a_shape_failure_is_still_a_divergence() -> None:
    # Off on the enforced shape too (bad enum): not explained by a stripped bound.
    answer = {"mode": "table", "notes": TOO_LONG}
    assert bounds_the_provider_cannot_carry(answer, SCHEMA, "anthropic") == []


def test_a_provider_that_keeps_every_bound_has_none_to_blame() -> None:
    answer = {"mode": "list_pattern", "notes": TOO_LONG}
    assert bounds_the_provider_cannot_carry(answer, SCHEMA, "google") == []


def test_a_property_named_like_a_keyword_is_not_a_bound() -> None:
    # `pattern` above is a PROPERTY name, not the keyword; only `maxLength` is present.
    answer = {"mode": "list_pattern", "notes": TOO_LONG, "pattern": "x"}
    assert bounds_the_provider_cannot_carry(answer, SCHEMA, "anthropic") == ["maxLength"]


async def test_the_recorded_remedy_names_the_bound(monkeypatch) -> None:
    from types import SimpleNamespace

    import matrx_ai.providers.structured_output_findings as findings
    from matrx_ai.schema import answer_contract

    recorded: list[dict] = []

    async def fake_record(key, *, provider, model, detail, was_recovered):
        recorded.append(detail)

    monkeypatch.setattr(findings, "record_structured_output_finding", fake_record)
    monkeypatch.setattr(
        answer_contract, "declared_output_contract", lambda: {"schema": SCHEMA, "enforced": True}
    )
    monkeypatch.setattr(answer_contract, "_turn_is_final", lambda response: True)
    monkeypatch.setattr(
        answer_contract,
        "_answer_text",
        lambda response: '{"mode": "list_pattern", "notes": "%s"}' % TOO_LONG,
    )
    monkeypatch.setattr(answer_contract, "answer_cut_short_by", lambda response: None)

    problems = await answer_contract.verify_answer_and_record(
        SimpleNamespace(), provider="anthropic", model="claude-sonnet-5-5"
    )
    assert problems
    assert recorded and recorded[0]["unenforced_bounds"] == ["maxLength"]
    assert "cannot enforce (maxLength)" in recorded[0]["remedy"]
    assert "divergence is the bug" not in recorded[0]["remedy"]
