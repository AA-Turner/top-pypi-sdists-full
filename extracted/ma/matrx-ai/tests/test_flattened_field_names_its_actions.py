"""A flattened dispatcher field that only some actions take says which ones.

Live evidence, 2026-11-06 (conversation a2d03e88): the model was shown ``wait_after_ms`` on
``cloud_browser`` with no hint that only ``click`` takes it, sent it with
``action="navigate"``, and the call was refused (``navigate.wait_after_ms: Extra inputs are
not permitted``). The refusal then said "re-read the schema" — the schema that offered it.

Two layers: the advertised field names its owning actions on every provider dialect, and
the refusal names which action a stray field belongs to.
"""

from __future__ import annotations

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import other_action_fields_sentence
from matrx_ai.tools.arg_models.browser_args import CloudBrowserArgs
from matrx_ai.tools.models import ToolDefinition
from matrx_ai.tools.validation.params_from_model import build_parameters


def _cloud_browser() -> ToolDefinition:
    return ToolDefinition(
        name="cloud_browser",
        description="Drive the cloud browser.",
        parameters=build_parameters(CloudBrowserArgs, action_description="The operation."),
    )


def test_click_only_field_says_click_on_every_provider() -> None:
    td = _cloud_browser()
    anthropic = td.to_anthropic_format()["input_schema"]["properties"]
    google = td.to_google_format()["parameters"]["properties"]
    openai = td.to_openai_responses_format()["parameters"]["properties"]
    for props in (anthropic, google, openai):
        desc = props["wait_after_ms"].get("description", "")
        assert "click" in desc and "Only for action" in desc, desc
        assert "navigate" not in desc
        assert "Only for action wait_for" in props["timeout_ms"].get("description", "")


def test_a_field_every_action_takes_is_not_labelled() -> None:
    props = _cloud_browser().to_anthropic_format()["input_schema"]["properties"]
    assert "Only for action" not in (props["profile_id"].get("description") or "")
    assert "Not for action" not in (props["profile_id"].get("description") or "")


def test_a_hand_written_owner_prefix_is_kept_as_written() -> None:
    td = ToolDefinition(
        name="t",
        description="d",
        parameters={
            "action": {"type": "string", "enum": ["a", "b"], "required": True},
            "drop": {"type": "array", "items": {"type": "string"}, "description": "b: junk to drop."},
            "$variants": {
                "a": {"type": "object", "properties": {"action": {"const": "a"}}},
                "b": {
                    "type": "object",
                    "properties": {"action": {"const": "b"}, "drop": {"type": "array", "items": {"type": "string"}}},
                },
            },
        },
    )
    desc = td.to_anthropic_format()["input_schema"]["properties"]["drop"]["description"]
    assert desc == "b: junk to drop."


def test_the_refusal_names_the_action_that_owns_the_stray_field() -> None:
    args = {"action": "navigate", "url": "https://qz.com/x", "wait_after_ms": 3000}
    try:
        CloudBrowserArgs.model_validate(args)
    except ValidationError as exc:
        sentence = other_action_fields_sentence(args, CloudBrowserArgs, exc)
    else:  # pragma: no cover - the model must refuse this call
        raise AssertionError("navigate accepted click's wait_after_ms")
    assert sentence is not None
    assert "`wait_after_ms` belongs to click, not navigate" in sentence
    assert "`navigate` takes:" in sentence and "wait_for" in sentence
