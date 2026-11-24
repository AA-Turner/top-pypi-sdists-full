"""Description-text drift: the gate compares the words the model reads, not only the contract.

Agents read the live ``tool.definition`` row. Wording improved in the code model only (ask_person,
2026-11-10) never reached them, and ``validate_tools.py`` stayed green because it compared
parameters and ignored text. These tests plant a difference and prove the gate fails on it.
"""
from __future__ import annotations

from typing import Annotated, ClassVar, Literal

from matrx_ai.tools.declared import DeclaredTool, ToolArgs
from matrx_ai.tools.validation.engine import FindingKind, Severity, validate
from pydantic import Field, RootModel


class _Args(ToolArgs):
    """Developer docs, never compared."""

    message: str = Field(description="To the person. Only the lead-in; the ask goes in payload.")


class _ToolLevelArgs(ToolArgs):
    tool_description: ClassVar[str] = "Ask the person one thing."
    message: str = Field(description="To the person.")


class _A(ToolArgs):
    action: Literal["go"]
    target: str = Field(description="go: where to.")


class _Dispatch(RootModel[Annotated[_A, Field(discriminator="action")]]):
    pass


def _decl(name: str, model: type) -> DeclaredTool:
    def _f(args, ctx):  # pragma: no cover
        return None

    return DeclaredTool(
        name=name, source_kind="native", args_model=model, func=_f, module="tests.fake",
        qualname=name, executor=None, validate=True, deprecated=False,
    )


def _row(name: str, params: dict, description: str = "") -> dict:
    return {
        "name": name, "source_kind": "native", "description": description, "is_active": True,
        "validation_exempt": False, "executors": [], "parameters": params,
    }


def _kinds(code: dict, rows: list[dict]) -> list[tuple[FindingKind, Severity]]:
    report = validate(code, rows, owner_executors=set())
    return [(f.kind, f.severity) for f in report.findings]


def _msg_row(text: str) -> dict:
    return _row("t", {"message": {"type": "string", "required": True, "description": text}})


def test_matching_text_is_clean_even_across_whitespace():
    row = _msg_row("To the person.  Only the lead-in;\nthe ask goes in payload.")
    assert _kinds({"t": _decl("t", _Args)}, [row]) == []


def test_planted_param_difference_fails():
    row = _msg_row("To the person, in their words.")
    assert _kinds({"t": _decl("t", _Args)}, [row]) == [(FindingKind.DESCRIPTION_DRIFT, Severity.ERROR)]


def test_text_in_code_only_on_one_param_names_the_param():
    row = _msg_row("older wording")
    (finding,) = validate({"t": _decl("t", _Args)}, [row], owner_executors=set()).findings
    assert finding.detail["param"] == "message"
    assert finding.detail["db"] == "older wording"
    assert finding.detail["code"].startswith("To the person.")


def test_row_without_text_at_that_location_is_a_gap_not_drift():
    assert _kinds({"t": _decl("t", _Args)}, [_msg_row("")]) == []


def test_code_without_text_is_not_compared():
    class _Bare(ToolArgs):
        message: str

    assert _kinds({"t": _decl("t", _Bare)}, [_msg_row("anything")]) == []


def test_brief_first_sentence_form_of_the_code_text_is_not_drift():
    row = _msg_row("To the person.")
    assert _kinds({"t": _decl("t", _Args)}, [row]) == []


def test_brief_form_does_not_excuse_a_different_first_sentence():
    row = _msg_row("To someone.")
    assert _kinds({"t": _decl("t", _Args)}, [row]) == [(FindingKind.DESCRIPTION_DRIFT, Severity.ERROR)]


def test_tool_level_text_is_compared_when_the_model_declares_it():
    params = {"message": {"type": "string", "required": True, "description": "To the person."}}
    same = _row("t", params, "Ask the person one thing.")
    assert _kinds({"t": _decl("t", _ToolLevelArgs)}, [same]) == []
    stale = _row("t", params, "Ask the person something.")
    assert _kinds({"t": _decl("t", _ToolLevelArgs)}, [stale]) == [
        (FindingKind.DESCRIPTION_DRIFT, Severity.ERROR)
    ]


def test_dispatcher_variant_text_is_compared_per_action():
    def row(text: str) -> dict:
        return _row(
            "t",
            {
                "action": {"type": "string", "enum": ["go"], "required": True},
                "$variants": {"go": {"target": {"type": "string", "required": True, "description": text}}},
            },
        )

    assert _kinds({"t": _decl("t", _Dispatch)}, [row("go: where to.")]) == []
    assert _kinds({"t": _decl("t", _Dispatch)}, [row("go: the place.")]) == [
        (FindingKind.DESCRIPTION_DRIFT, Severity.ERROR)
    ]
