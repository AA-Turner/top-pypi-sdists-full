"""The `toolcomp_*` tools read and write tool components AS THE PERSON.

Defect (2026-09-27): every toolcomp action loaded ``tool.ui`` / ``tool.definition`` /
``tool.test_sample`` / ``tool.ui_incident`` rows by id on the privileged connection with
no access decision, so ANY person's agent could overwrite the render code of ANY
tool's component — code every user's browser then runs. Chair ruling: RLS owns
access. Live RLS (2026-09-27): the catalog of public tools is readable by everyone; a
component is readable when its tool is, and writable only by an editor of its tool.
Every action now runs inside the caller's RLS session; a component RLS hides is
``not_found`` naming its id, and one the caller may read but not change is
``no_access`` — never a silent no-op reported as success.

Scenario: the platform's "Weather card" component renders the public ``get_weather``
tool. Riley, an ordinary member, may read it; only the tool's editor may change it.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from typing import Any

import pytest

EDITOR = "f0e1d2c3-0000-4000-8000-00000000e001"
READER = "f0e1d2c3-0000-4000-8000-00000000f002"
STRANGER = "f0e1d2c3-0000-4000-8000-00000000a003"
COMP_ID = "c0de0000-0000-4000-8000-000000000001"
HIDDEN_COMP = "c0de0000-0000-4000-8000-000000000002"
CODE = "export default function WeatherCard({ data }) { return <div>{data.temp}°</div>; }"

_acting: ContextVar[str | None] = ContextVar("fake_acting_user_toolcomp", default=None)


class _Inst:
    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data
        self._fields = dict.fromkeys(data)

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)


class RlsToolUi:
    """tool.ui as RLS shows it: readers see a row, writers may change it."""

    def __init__(self) -> None:
        self.rows = {
            COMP_ID: {
                "id": COMP_ID, "tool_id": "7001", "tool_name": "get_weather", "display_name": "Weather card",
                "semver": "1.0.0", "version": 3, "language": "tsx", "allowed_imports": [],
                "inline_code": CODE, "overlay_code": None, "notes": None,
            },
            HIDDEN_COMP: {
                "id": HIDDEN_COMP, "tool_id": None, "tool_name": "payroll_panel", "display_name": "Payroll",
                "semver": "1.0.0", "version": 1, "language": "tsx", "allowed_imports": [],
                "inline_code": "secret()", "overlay_code": None, "notes": None,
            },
        }
        self.readers = {COMP_ID: {EDITOR, READER}, HIDDEN_COMP: {EDITOR}}
        self.writers = {COMP_ID: {EDITOR}, HIDDEN_COMP: {EDITOR}}
        self.violations: list[str] = []
        self.db_calls = 0

    def _who(self, seam: str) -> str | None:
        self.db_calls += 1
        who = _acting.get()
        if who is None:
            self.violations.append(f"{seam}: ran on the privileged connection")
        return who

    async def get_or_none(self, use_cache: bool = True, **pk: Any) -> _Inst | None:
        who = self._who("get_or_none")
        rid = pk.get("id")
        return _Inst(dict(self.rows[rid])) if who in self.readers.get(rid, set()) else None

    async def update_where(self, where: dict[str, Any], **updates: Any) -> int:
        who = self._who("update_where")
        rid = where["id"]
        if who not in self.writers.get(rid, set()):
            return 0  # RLS: the UPDATE matched no row this person may change
        self.rows[rid].update(updates)
        self.rows[rid]["version"] += 1
        return 1


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai import _ext
    from matrx_ai.tools.implementations import tool_component

    ui = RlsToolUi()
    monkeypatch.setattr(tool_component, "get_db_model", lambda name: ui)

    current: dict[str, str] = {}

    @contextlib.asynccontextmanager
    async def acting_as_caller():
        token = _acting.set(current["user"])
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)
    return ui, current


def _ctx():
    from matrx_ai.tools.models import ToolContext

    return ToolContext(call_id="call-weather", tool_name="toolcomp")


@pytest.mark.asyncio
async def test_the_tools_editor_reads_and_changes_the_component(world):
    from matrx_ai.tools.implementations.tool_component import (
        toolcomp_get_code,
        toolcomp_update_code,
    )

    ui, current = world
    current["user"] = EDITOR
    got = await toolcomp_get_code({"component_id": COMP_ID}, _ctx())
    assert got.success, got.error
    changed = await toolcomp_update_code(
        {"component_id": COMP_ID, "updates": {"inline_code": CODE.replace("°", "°F")}}, _ctx()
    )
    assert changed.success, changed.error
    assert "°F" in ui.rows[COMP_ID]["inline_code"]
    assert ui.violations == [], ui.violations


@pytest.mark.asyncio
async def test_a_reader_may_read_but_every_change_is_no_access(world):
    from matrx_ai.tools.implementations.tool_component import (
        toolcomp_get_code,
        toolcomp_patch_code,
        toolcomp_update_code,
        toolcomp_update_settings,
    )

    ui, current = world
    current["user"] = READER
    got = await toolcomp_get_code({"component_id": COMP_ID}, _ctx())
    assert got.success, got.error

    for fn, args in (
        (toolcomp_update_code, {"component_id": COMP_ID, "updates": {"inline_code": "alert(document.cookie)"}}),
        (toolcomp_update_settings, {"component_id": COMP_ID, "settings": {"display_name": "Pwned"}}),
        (
            toolcomp_patch_code,
            {"component_id": COMP_ID, "patches": [{"old_string": "{data.temp}", "new_string": "{fetch('//x')}"}]},
        ),
    ):
        result = await fn(args, _ctx())
        assert not result.success, fn.__name__
        assert result.error.error_type == "no_access", (fn.__name__, result.error)
        assert COMP_ID in result.error.message
    assert ui.rows[COMP_ID]["inline_code"] == CODE, "a reader changed the component's code"
    assert ui.rows[COMP_ID]["display_name"] == "Weather card"
    assert ui.violations == [], ui.violations


@pytest.mark.asyncio
async def test_a_component_rls_hides_is_not_found_naming_its_id(world):
    from matrx_ai.tools.implementations.tool_component import (
        toolcomp_get_code,
        toolcomp_update_code,
    )

    ui, current = world
    current["user"] = STRANGER
    got = await toolcomp_get_code({"component_id": HIDDEN_COMP}, _ctx())
    assert not got.success and got.error.error_type == "not_found"
    assert HIDDEN_COMP in got.error.message and "secret" not in got.error.message

    upd = await toolcomp_update_code(
        {"component_id": HIDDEN_COMP, "updates": {"inline_code": "x()"}}, _ctx()
    )
    assert not upd.success and upd.error.error_type == "not_found"
    assert HIDDEN_COMP in upd.error.message
    assert ui.rows[HIDDEN_COMP]["inline_code"] == "secret()"
    assert ui.violations == [], ui.violations


@pytest.mark.asyncio
async def test_without_a_person_session_nothing_reaches_the_database(world, monkeypatch):
    from matrx_ai import _ext
    from matrx_ai.tools.implementations.tool_component import (
        toolcomp_get_code,
        toolcomp_update_code,
    )

    ui, current = world
    current["user"] = EDITOR
    monkeypatch.delitem(_ext._registry, "acting_as_caller", raising=False)
    for fn, args in (
        (toolcomp_get_code, {"component_id": COMP_ID}),
        (toolcomp_update_code, {"component_id": COMP_ID, "updates": {"inline_code": "x()"}}),
    ):
        result = await fn(args, _ctx())
        assert not result.success and result.error.error_type == "unavailable", result.error
    assert ui.db_calls == 0
