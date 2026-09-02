import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.agents.source_tracking import (
    MISSING_SOURCE_TRACKING_KIND,
    ChildSourceContextError,
    capture_missing_source_tracking,
    resolve_child_source,
    warn_missing_source_tracking,
)


def test_resolve_child_source_requires_feature() -> None:
    with pytest.raises(ChildSourceContextError):
        resolve_child_source(
            source_app="aidream",
            source_feature="",
            caller="test",
        )


def test_resolve_child_source_uses_explicit_values() -> None:
    app, feature = resolve_child_source(
        source_app="aidream",
        source_feature="agent_call",
        caller="test",
    )
    assert app == "aidream"
    assert feature == "agent_call"


def test_resolve_child_source_defaults_app_when_omitted() -> None:
    app, feature = resolve_child_source(
        source_app=None,
        source_feature="agent_call",
        caller="test",
    )
    assert app in ("matrx-ai", "aidream")
    assert feature == "agent_call"


@pytest.mark.asyncio
async def test_missing_source_warning_creates_structured_system_error(monkeypatch) -> None:
    captured: list[dict[str, object]] = []
    completed = asyncio.Event()

    async def record_error(_error: BaseException, **kwargs: object) -> None:
        captured.append(kwargs)
        completed.set()

    monkeypatch.setattr(
        "matrx_ai._ext.get_ext",
        lambda name: record_error if name == "record_error" else None,
    )

    warn_missing_source_tracking(
        SimpleNamespace(source_app="", source_feature=""),
        handler="test.keyword_research",
        label="research",
    )
    await asyncio.wait_for(completed.wait(), timeout=1)

    assert captured == [
        {
            "kind": MISSING_SOURCE_TRACKING_KIND,
            "error_type": MISSING_SOURCE_TRACKING_KIND,
            "error_text": (
                "agent source tracking missing source_app, source_feature at test.keyword_research"
            ),
            "route": "test.keyword_research",
            "payload": {
                "handler": "test.keyword_research",
                "label": "research",
                "missing": ["source_app", "source_feature"],
            },
        }
    ]


@pytest.mark.asyncio
async def test_missing_source_capture_is_awaited_with_system_error_kind(monkeypatch) -> None:
    captured: list[dict[str, object]] = []

    async def record_error(_error: BaseException, **kwargs: object) -> None:
        await asyncio.sleep(0)
        captured.append(kwargs)

    monkeypatch.setattr(
        "matrx_ai._ext.get_ext",
        lambda name: record_error if name == "record_error" else None,
    )

    missing = await capture_missing_source_tracking(
        SimpleNamespace(source_app="", source_feature=""),
        handler="test.mandate_start",
        label="goal-writer",
    )

    assert missing is True
    assert captured[0]["kind"] == MISSING_SOURCE_TRACKING_KIND
    assert captured[0]["route"] == "test.mandate_start"
