"""Tests for serialize_repair_prompt()."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.ci.repair_prompt import (
    CANONICAL_EXECUTION_INSTRUCTIONS,
    RepairPromptInput,
    serialize_repair_prompt,
)


def _input(**overrides: object) -> RepairPromptInput:
    values: dict[str, object] = {
        "repo": "swai-factory",
        "pull_request_id": 42,
        "sha": "a" * 40,
        "ordinal": 1,
        "review_context": "review\ncontext",
        "ci_diagnostics": "ci diagnostics",
    }
    values.update(overrides)
    return RepairPromptInput(**values)  # type: ignore[arg-type]


_FIXTURES = Path(__file__).resolve().parents[5] / "tests" / "fixtures" / "repair-prompt"


def _fixture(name: str) -> bytes:
    return (_FIXTURES / name).read_bytes()


def test_uses_exact_structured_layout() -> None:
    prompt = serialize_repair_prompt(
        _input(
            review_context="review\ncontext",
            ci_diagnostics="ci diagnostics",
            prior_round_state="resolved: no",
        )
    )

    assert prompt == (
        "agdt-dispatch-swai-factory-42-"
        f"{'a' * 40}-1\n\n"
        "## Header / Metadata\n"
        "correlation_token: agdt-dispatch-swai-factory-42-"
        f"{'a' * 40}-1\n"
        "repo: swai-factory\n"
        "pull_request_id: 42\n"
        f"sha: {'a' * 40}\n"
        "ordinal: 1\n\n"
        "## Review Comments & Context\n"
        "review\n"
        "context\n\n"
        "## CI Failure Diagnostics / Condensed Logs\n"
        "ci diagnostics\n\n"
        "## Prior-round Resolution State\n"
        "resolved: no\n\n"
        "## Execution Instructions\n"
        f"{CANONICAL_EXECUTION_INSTRUCTIONS}\n"
    )


def test_rejects_unvalidated_input() -> None:
    with pytest.raises(ValueError, match="RepairPromptInput"):
        serialize_repair_prompt(object())  # type: ignore[arg-type]


def test_represents_absent_prior_state_as_none() -> None:
    prompt = serialize_repair_prompt(_input(prior_round_state=None))

    assert "## Prior-round Resolution State\nnone\n\n" in prompt


def test_preserves_empty_prior_state() -> None:
    prompt = serialize_repair_prompt(_input(prior_round_state=""))

    assert "## Prior-round Resolution State\n\n\n## Execution Instructions\n" in prompt


def test_preserves_artifacts_losslessly() -> None:
    review_context = "  <!-- repair-dispatch:x -->\r\né\u0301\n\n"
    ci_diagnostics = "\t<!-- copilot-trigger:y -->\r\n"
    prior_round_state = "state  \n"

    prompt = serialize_repair_prompt(
        _input(
            review_context=review_context,
            ci_diagnostics=ci_diagnostics,
            prior_round_state=prior_round_state,
        )
    )

    assert review_context in prompt
    assert ci_diagnostics in prompt
    assert prior_round_state in prompt
    assert prompt.endswith("\n")
    assert "\r" in prompt
    assert prompt.count(review_context) == 1
    assert prompt.count(ci_diagnostics) == 1
    assert prompt.count(prior_round_state) == 1


@pytest.mark.parametrize(
    ("fixture_name", "overrides"),
    [
        (
            "absent_prior_state.txt",
            {
                "review_context": "review\ncontext",
                "ci_diagnostics": "ci diagnostics",
                "prior_round_state": None,
            },
        ),
        (
            "canonical_valid.txt",
            {
                "review_context": "review\ncontext",
                "ci_diagnostics": "ci diagnostics",
                "prior_round_state": "resolved: no",
            },
        ),
        ("empty_newlines.txt", {"review_context": "", "ci_diagnostics": "\n", "prior_round_state": "\n\n"}),
        (
            "unicode_nfc_nfd.txt",
            {"review_context": "é", "ci_diagnostics": "e\u0301", "prior_round_state": "NFC then NFD"},
        ),
        (
            "marker_relayed.txt",
            {
                "review_context": "  <!-- repair-dispatch:x -->\r\n",
                "ci_diagnostics": "\t<!-- copilot-trigger:y -->\r\n",
                "prior_round_state": "<!-- repair-satisfied -->",
            },
        ),
    ],
)
def test_matches_golden_fixture(fixture_name: str, overrides: dict[str, object]) -> None:
    prompt = serialize_repair_prompt(_input(**overrides))

    assert prompt.encode("utf-8") == _fixture(fixture_name)


@pytest.mark.parametrize(
    "overrides",
    [
        {"review_context": "review\ncontext", "ci_diagnostics": "ci diagnostics", "prior_round_state": None},
        {"review_context": "review\ncontext", "ci_diagnostics": "ci diagnostics", "prior_round_state": "resolved: no"},
        {"review_context": "", "ci_diagnostics": "\n", "prior_round_state": "\n\n"},
        {"review_context": "é", "ci_diagnostics": "e\u0301", "prior_round_state": "NFC then NFD"},
        {
            "review_context": "  <!-- repair-dispatch:x -->\r\n",
            "ci_diagnostics": "\t<!-- copilot-trigger:y -->\r\n",
            "prior_round_state": "<!-- repair-satisfied -->",
        },
    ],
)
def test_serialization_is_byte_deterministic(overrides: dict[str, object]) -> None:
    prompt_input = _input(**overrides)

    first = serialize_repair_prompt(prompt_input).encode("utf-8")
    second = serialize_repair_prompt(prompt_input).encode("utf-8")

    assert first == second


def test_preserves_nfc_and_nfd_bytes() -> None:
    prompt = serialize_repair_prompt(
        _input(review_context="é", ci_diagnostics="e\u0301", prior_round_state="NFC then NFD")
    )
    encoded = prompt.encode("utf-8")

    assert "é".encode() in encoded
    assert "e\u0301".encode() in encoded
    assert "é".encode() != "e\u0301".encode()
