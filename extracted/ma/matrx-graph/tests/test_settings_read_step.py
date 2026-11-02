"""``settings.read`` hands a run its organization's CURRENT setting value, and
fails by name when it cannot — a workflow limit is a setting, not a number in a
definition (coordinator ruling 2026-10-09; gap: Deep Research workflow limits)."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_graph import settings
from matrx_graph.nodes.settings.read import SettingReadConfig, SettingReadExecutor, SettingReadInput


@pytest.fixture(autouse=True)
def _reset() -> Any:
    yield
    settings.set_setting_reader(None)


@pytest.mark.asyncio
async def test_reads_the_value_for_the_runs_organization() -> None:
    seen: list[tuple[str, str, str | None]] = []

    async def _reader(feature: str, key: str, org: str | None, user: str | None = None) -> Any:
        seen.append((feature, key, org))
        return 5

    settings.set_setting_reader(_reader)
    res = await SettingReadExecutor().execute(
        SimpleNamespace(organization_id="org-1"),  # type: ignore[arg-type]
        SettingReadInput(feature="research.deep_research_workflow", key="search_result_pages"),
        SettingReadConfig(),
    )
    assert res.result.value == 5
    assert seen == [("research.deep_research_workflow", "search_result_pages", "org-1")]


@pytest.mark.asyncio
async def test_no_reader_is_a_named_failure() -> None:
    res = await SettingReadExecutor().execute(
        SimpleNamespace(organization_id="org-1"),  # type: ignore[arg-type]
        SettingReadInput(feature="f", key="k"),
        SettingReadConfig(),
    )
    assert res.status == "error" and res.error.code == "setting_reader_missing"


@pytest.mark.asyncio
async def test_a_missing_setting_fails_naming_it() -> None:
    async def _reader(feature: str, key: str, org: str | None, user: str | None = None) -> Any:
        raise LookupError("no such knob")

    settings.set_setting_reader(_reader)
    res = await SettingReadExecutor().execute(
        SimpleNamespace(organization_id=None),  # type: ignore[arg-type]
        SettingReadInput(feature="f", key="k"),
        SettingReadConfig(),
    )
    assert res.error.code == "setting_unreadable" and "f/k" in res.error.message


def test_registered_as_a_builtin() -> None:
    from matrx_graph.nodes import BUILTIN_VALUES_ARE

    assert "settings.read" in BUILTIN_VALUES_ARE


@pytest.mark.asyncio
async def test_no_key_reads_every_setting_of_the_feature_for_org_and_person() -> None:
    seen: list[tuple[str, str | None, str | None]] = []

    async def _feature_reader(feature: str, org: str | None, user: str | None) -> Any:
        seen.append((feature, org, user))
        return {"a": (1, "platform"), "b": (True, "user")}

    settings.set_feature_settings_reader(_feature_reader)
    try:
        res = await SettingReadExecutor().execute(
            SimpleNamespace(organization_id="org-1", user_id="user-1"),  # type: ignore[arg-type]
            SettingReadInput(feature="news"),
            SettingReadConfig(),
        )
    finally:
        settings.set_feature_settings_reader(None)
    assert res.result.value == {"a": {"value": 1, "source": "platform"}, "b": {"value": True, "source": "user"}}
    assert seen == [("news", "org-1", "user-1")]


@pytest.mark.asyncio
async def test_reading_a_whole_feature_with_no_reader_is_a_named_failure() -> None:
    res = await SettingReadExecutor().execute(
        SimpleNamespace(organization_id="org-1", user_id="u"),  # type: ignore[arg-type]
        SettingReadInput(feature="news"),
        SettingReadConfig(),
    )
    assert res.status == "error" and res.error.code == "setting_reader_missing"


@pytest.mark.asyncio
async def test_one_key_and_whole_feature_answer_the_same_with_a_user_override() -> None:
    """Same run, same person: the one-key read and the whole-feature read must agree (user rung included)."""
    truth = {"limit": (7, "user")}

    async def _one(feature: str, key: str, org: str | None, user: str | None = None) -> Any:
        return truth[key][0] if user == "user-1" else 3

    async def _all(feature: str, org: str | None, user: str | None) -> Any:
        return truth if user == "user-1" else {"limit": (3, "platform")}

    settings.set_setting_reader(_one)
    settings.set_feature_settings_reader(_all)
    try:
        ctx = SimpleNamespace(organization_id="org-1", user_id="user-1")
        one = await SettingReadExecutor().execute(ctx, SettingReadInput(feature="f", key="limit"), SettingReadConfig())  # type: ignore[arg-type]
        whole = await SettingReadExecutor().execute(ctx, SettingReadInput(feature="f"), SettingReadConfig())  # type: ignore[arg-type]
    finally:
        settings.set_feature_settings_reader(None)
    assert one.result.value == whole.result.value["limit"]["value"] == 7
