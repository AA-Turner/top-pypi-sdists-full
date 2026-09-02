"""S6 §3.3 layer 2 — the committed test that survives someone relaxing
``extra="forbid"``. Walks every ``Browser*Args`` model and fails the build if any
principal-identifier field appears, if ``profile_id`` is missing/typed wrong, or
if a model drops ``extra="forbid"``.
"""

from __future__ import annotations

from typing import get_args

import pytest
from pydantic import ValidationError

from matrx_ai.tools.arg_models import browser_args

_MODELS = [
    browser_args.BrowserNavigateArgs,
    browser_args.BrowserClickArgs,
    browser_args.BrowserTypeArgs,
    browser_args.BrowserScreenshotArgs,
    browser_args.BrowserSelectOptionArgs,
    browser_args.BrowserWaitForArgs,
    browser_args.BrowserGetElementArgs,
    browser_args.BrowserScrollArgs,
    browser_args.BrowserCloseArgs,
]

FORBIDDEN = {
    "user_id",
    "organization_id",
    "owner_user_id",
    "acting_user_id",
    "org_id",
    "organisation_id",
    "principal_id",
    "tenant_id",
}


def test_there_are_exactly_nine_browser_arg_models():
    # The compatibility promise (S6 §1): every original arg shape survives.
    # Since the 2026-08-21 consolidation the nine are variants of the ONE
    # action-dispatched `cloud_browser` tool.
    assert len(_MODELS) == 9


def test_cloud_browser_union_carries_all_nine_actions():
    parsed = browser_args.CloudBrowserArgs.model_validate(
        {"action": "close", "session_id": "run-1"}
    )
    assert isinstance(parsed.root, browser_args.BrowserCloseArgs)
    actions = set()
    for model in _MODELS:
        (literal,) = get_args(model.model_fields["action"].annotation)
        actions.add(literal)
    assert actions == {
        "navigate", "click", "type_text", "select_option", "wait_for",
        "get_element", "scroll", "screenshot", "close",
    }


@pytest.mark.parametrize("model", _MODELS)
def test_no_principal_id_field(model):
    fields = set(model.model_fields)
    leaked = fields & FORBIDDEN
    assert not leaked, f"{model.__name__} exposes forbidden principal field(s): {leaked}"


@pytest.mark.parametrize("model", _MODELS)
def test_profile_id_is_optional_opaque_string(model):
    field = model.model_fields.get("profile_id")
    assert field is not None, f"{model.__name__} is missing the additive profile_id argument"
    assert field.annotation is str
    assert field.default == ""  # "" means resolve personal default (S6 §3.2)


@pytest.mark.parametrize("model", _MODELS)
def test_extra_forbid_rejects_a_principal_id(model):
    # A model that invents user_id fails at PARSE time, before any network call.
    base_kwargs = {
        name: (get_args(f.annotation)[0] if get_args(f.annotation) else "x")
        for name, f in model.model_fields.items()
        if f.is_required()
    }
    with pytest.raises(ValidationError):
        model(**base_kwargs, user_id="sneaky")
