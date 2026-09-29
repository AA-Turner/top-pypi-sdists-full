"""Kind tools write the four CERTIFIED tables as the person — RLS decides.

Chair ruling (2026-09-27): content_ir.kind_definition, content_ir.kind_instance,
skill.definition and skill.render_definition are certified, so every kind-tool write
to them runs inside the caller's RLS session (``kind_shared.writing_as_the_person``;
the admin lane opened inside it on an admin surface). The five uncertified component
tables stay on the privileged connection until iam.apply_rls re-runs on them
(``KIND_TABLES_PENDING_CANONICAL_RLS``).

Two layers: a structural guard (no write to a certified table outside the person's
session, anywhere in the kind tool modules) and behaviour (a refused write answers
``no_access`` naming the row and changes nothing).

Scenario: a home-inspection company's "Roof inspection" kind; Omar edits its
instances, Lena (another company) must not.
"""

from __future__ import annotations

import ast
import contextlib
from contextvars import ContextVar
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.models import ToolContext

_IMPL = Path(__file__).resolve().parents[1] / "matrx_ai" / "tools" / "implementations"
_CERTIFIED_MODELS = {"KindDefinition", "KindInstance", "SklDefinition", "RenderDefinition"}
_WRITE_METHODS = {"create_item", "update_where", "delete_where", "create_items"}
_PERSON_WRITERS = {"writing_as_the_person", "update_as_the_person"}

_acting: ContextVar[str | None] = ContextVar("fake_acting_kind_writes", default=None)


def _writes_outside_the_person_session(path: Path) -> list[str]:
    tree = ast.parse(path.read_text())
    parents: dict[ast.AST, ast.AST] = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node

    def inside_person_session(node: ast.AST) -> bool:
        while node in parents:
            node = parents[node]
            if isinstance(node, ast.AsyncWith):
                for item in node.items:
                    call = item.context_expr
                    if isinstance(call, ast.Call) and getattr(call.func, "id", None) in _PERSON_WRITERS:
                        return True
        return False

    bad = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in _WRITE_METHODS
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in _CERTIFIED_MODELS
            and not inside_person_session(node)
        ):
            bad.append(f"{path.name}:{node.lineno} {node.func.value.id}.{node.func.attr}")
    return bad


@pytest.mark.parametrize("module", ["kind_authoring.py", "kind_instance.py", "kind_component.py"])
def test_no_certified_kind_table_is_written_outside_the_persons_session(module: str) -> None:
    assert _writes_outside_the_person_session(_IMPL / module) == []


def test_the_pending_tables_are_named_and_disjoint_from_the_certified_ones() -> None:
    from matrx_ai.tools.implementations import kind_shared

    assert set(kind_shared.KIND_TABLES_WRITTEN_AS_THE_PERSON) == {
        "content_ir.kind_definition", "content_ir.kind_instance",
        "skill.definition", "skill.render_definition",
    }
    assert not set(kind_shared.KIND_TABLES_PENDING_CANONICAL_RLS) & set(
        kind_shared.KIND_TABLES_WRITTEN_AS_THE_PERSON
    )


# --- behaviour ---------------------------------------------------------------

OMAR = "a0b1c2d3-0000-4000-8000-00000000a001"
LENA = "a0b1c2d3-0000-4000-8000-00000000b002"


class RlsInstances:
    def __init__(self, row: Any, *, readers: set[str], writers: set[str]) -> None:
        self.row, self.readers, self.writers = row, readers, writers
        self.writes: list[tuple[str | None, dict[str, Any]]] = []

    async def get_or_none(self, use_cache: bool = True, **pk: Any) -> Any:
        return self.row if _acting.get() in self.readers else None

    def filter(self, **_pk: Any) -> Any:
        model = self

        class _Q:
            def select_for_update(self) -> Any:
                return self

            async def values(self, *_f: str) -> list[dict[str, Any]]:
                return [{"id": str(model.row.id)}] if _acting.get() in model.writers else []

        return _Q()

    async def update_where(self, where: dict[str, Any], **values: Any) -> Any:
        who = _acting.get()
        self.writes.append((who, values))
        if who is None or who not in self.writers:
            return SimpleNamespace(rows_affected=0, updated_rows=[])
        return SimpleNamespace(rows_affected=1, updated_rows=[{**vars(self.row), **values}])


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai import _ext
    from matrx_ai.tools.implementations import kind_instance as ki

    current: dict[str, str] = {}

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        token = _acting.set(current.get("user"))
        try:
            yield
        finally:
            _acting.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)
    row = SimpleNamespace(
        id=uuid4(), kind_definition_id=uuid4(), title="12 Elm St — roof", kind_version=1,
        validation_status="passed", data={"shingles": "worn"}, created_by=OMAR,
        organization_id=uuid4(), deleted_at=None, updated_at=None,
    )
    table = RlsInstances(row, readers={OMAR}, writers={OMAR})
    kd = SimpleNamespace(id=row.kind_definition_id, kind="roof_inspection", version=1,
                         emitted_json_schema=None, metadata=None, deleted_at=None)

    class _Kinds:
        @staticmethod
        async def get_or_none(**_k: Any) -> Any:
            return kd

    monkeypatch.setattr(ki, "get_db_model", lambda name: _Kinds if name == "KindDefinition" else table)

    async def no_store_arm(_ctx: Any) -> None:
        return None

    monkeypatch.setattr(ki, "_store_arm", no_store_arm)
    return ki, table, current


def _ctx(monkeypatch: pytest.MonkeyPatch, ki: Any, user: str) -> ToolContext:
    monkeypatch.setattr(ki, "ctx_user_id", lambda _ctx: user)
    return ToolContext(call_id="call-roof", tool_name="instance_update")


@pytest.mark.asyncio
async def test_the_editor_updates_inside_his_session(world, monkeypatch):
    ki, table, current = world
    current["user"] = OMAR
    result = await ki.instance_update(
        {"instance_id": str(table.row.id), "title": "12 Elm St — roof (re-inspected)"},
        _ctx(monkeypatch, ki, OMAR),
    )
    assert result.success, result.error
    assert table.writes and all(who == OMAR for who, _ in table.writes)


@pytest.mark.asyncio
async def test_a_viewer_whose_write_rls_refuses_gets_no_access_naming_the_row(world, monkeypatch):
    ki, table, current = world
    current["user"] = LENA
    table.readers.add(LENA)
    table.writers.add(LENA)  # the edit probe says yes …

    async def refuse(where: dict[str, Any], **values: Any) -> Any:  # … the write itself is refused
        table.writes.append((_acting.get(), values))
        raise RuntimeError("42501: new row violates row-level security policy")

    monkeypatch.setattr(table, "update_where", refuse)
    result = await ki.instance_update(
        {"instance_id": str(table.row.id), "title": "hijacked"}, _ctx(monkeypatch, ki, LENA)
    )
    assert not result.success
    assert result.error.error_type == "no_access"
    assert str(table.row.id) in result.error.message
    assert all(who == LENA for who, _ in table.writes), "the write left the person's session"
