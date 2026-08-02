"""Think/analyze reasoning tools are disabled for inline-app and email agent-gateway children.

The gateway dispatches downstream children; the new-UI inline ones (is_app + sync,
i.e. should_update_parent False) and email-triggered ones (source == "email") must run
without agno's ReasoningTools for latency. Async gateway children, non-app/non-email
runs, and non-gateway runs keep the toolkit.
"""

from __future__ import annotations

from types import SimpleNamespace

from xpander_sdk.modules.agents.models.agent import SourceNodeType
from xpander_sdk.modules.backend.frameworks.agno import _should_use_reasoning_tools


def _agent(enabled=True):
    return SimpleNamespace(agno_settings=SimpleNamespace(reasoning_tools_enabled=enabled))


def _task(*, gateway=True, is_app=False, should_update_parent=False, source=None):
    headers = {"x-is-from-agent-gateway": "true"} if gateway else {}
    return SimpleNamespace(
        payload_extension={"headers": headers},
        is_app=is_app,
        should_update_parent=should_update_parent,
        source=source,
    )


def test_disabled_for_inline_app_gateway_child():
    task = _task(is_app=True, should_update_parent=False)
    assert _should_use_reasoning_tools(_agent(), task) is False


def test_enabled_for_async_app_gateway_child():
    task = _task(is_app=True, should_update_parent=True)
    assert _should_use_reasoning_tools(_agent(), task) is True


def test_disabled_for_email_gateway_child_even_when_async():
    task = _task(is_app=False, should_update_parent=True, source=SourceNodeType.EMAIL.value)
    assert _should_use_reasoning_tools(_agent(), task) is False


def test_enabled_for_non_app_non_email_gateway_child():
    task = _task(is_app=False, should_update_parent=True)
    assert _should_use_reasoning_tools(_agent(), task) is True


def test_enabled_for_app_non_gateway_task():
    # direct new-UI chat (no gateway header) keeps reasoning
    task = _task(gateway=False, is_app=True, should_update_parent=False)
    assert _should_use_reasoning_tools(_agent(), task) is True


def test_enabled_for_email_non_gateway_task():
    task = _task(gateway=False, source=SourceNodeType.EMAIL.value)
    assert _should_use_reasoning_tools(_agent(), task) is True


def test_disabled_when_reasoning_setting_off():
    task = _task(is_app=False, should_update_parent=True)
    assert _should_use_reasoning_tools(_agent(enabled=False), task) is False


def test_handles_missing_task():
    assert _should_use_reasoning_tools(_agent(), None) is True
