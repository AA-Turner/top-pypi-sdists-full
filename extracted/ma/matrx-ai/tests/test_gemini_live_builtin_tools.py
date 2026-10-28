"""Google's hosted Live tools ride the setup beside our own function tools.

The voice agent page declares google_search (and code_execution / url_context
when the catalog says the model has them) for a Gemini Live session; the setup
must carry each as Google's own tool AND keep every function declaration, or
search is either missing (slow answers) or our tools vanish (no hand-off).
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from matrx_ai.providers.google.specialized import (
    GoogleLiveFunction,
    GoogleLiveOptions,
    build_live_config,
)
from matrx_ai.testing.profile_factory import make_profile


def _live_profile():
    from matrx_ai.catalog.models import ControlRule

    return make_profile(
        model_name="gemini-3.8-live",
        wire_format="google_live",
        capabilities={"input": ["audio"], "output": ["audio"], "features": ["live_api"], "interaction": "realtime"},
        rules={
            "turn_coverage": ControlRule.model_validate({}),
            "response_modalities": ControlRule.model_validate({}),
        },
    )


def test_builtins_and_functions_share_one_setup():
    options = GoogleLiveOptions(
        tools=[GoogleLiveFunction(name="lookup_order", description="Find an order")],
        builtin_tools=["google_search", "code_execution", "url_context"],
    )
    tools = build_live_config(_live_profile(), options).tools or []
    names = [fd.name for t in tools for fd in (t.function_declarations or [])]
    assert names == ["lookup_order"]
    assert sum(1 for t in tools if t.google_search is not None) == 1
    assert sum(1 for t in tools if t.code_execution is not None) == 1
    assert sum(1 for t in tools if t.url_context is not None) == 1


def test_search_alone_is_a_tool_session():
    tools = build_live_config(_live_profile(), GoogleLiveOptions(builtin_tools=["google_search"])).tools
    assert tools is not None and len(tools) == 1 and tools[0].google_search is not None


def test_a_builtin_google_does_not_have_is_refused():
    with pytest.raises(ValidationError):
        GoogleLiveOptions(builtin_tools=["x_search"])  # type: ignore[list-item]
