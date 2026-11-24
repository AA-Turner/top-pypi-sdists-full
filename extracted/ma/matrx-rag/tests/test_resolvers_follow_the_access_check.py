"""Indexing a source follows ``iam.has_access_for`` (platform_access_check), never ``created_by == user``.

A collaborator who may read a shared note / document / task / project / repository / canvas item /
workbook / research topic must be able to index it; a stranger gets None. Run:
uv run pytest packages/matrx-rag/tests/test_resolvers_follow_the_access_check.py
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_rag import sources


class _Row(dict):
    def __missing__(self, key: str) -> Any:
        return None


class _Q:
    def __init__(self, seen: dict[str, Any]) -> None:
        self.seen = seen

    def filter(self, *a: Any, **kw: Any) -> _Q:
        self.seen.update(kw)
        return self

    def order_by(self, *a: Any) -> _Q:
        return self

    def limit(self, *a: Any) -> _Q:
        return self

    async def values(self, *_f: str) -> list[dict[str, Any]]:
        return [_Row(id="x1", created_by="the-creator", topic_id="tp1", name="n", title="t", label="l",
                     content="body text", description="d", slug="s")]


class _Model:
    seen: dict[str, Any] = {}

    @classmethod
    def filter(cls, *a: Any, **kw: Any) -> _Q:
        cls.seen.update(kw)
        return _Q(cls.seen)


CASES = [
    ("_resolve_note", ("x1",), "note"),
    ("_resolve_document", ("x1",), "document"),
    ("_resolve_task", ("x1",), "task"),
    ("_resolve_project", ("x1",), "project"),
    ("_resolve_repository", ("x1",), "code_repository"),
    ("_resolve_canvas_item", ("x1",), "canvas_item"),
    ("_resolve_research", ("x1",), "research_topic"),
    ("_resolve_udt", ("workbook", "x1"), "workbook"),
    ("_resolve_udt", ("udt_document", "x1"), "udt_document"),
]


@pytest.fixture
def wired(monkeypatch):
    _Model.seen = {}
    monkeypatch.setattr(sources, "get_db_model", lambda *a, **k: _Model)
    return _Model.seen


@pytest.mark.parametrize("fn,args,token", CASES)
async def test_a_reader_who_did_not_create_it_is_let_in(fn, args, token, wired, monkeypatch):
    import matrx_orm

    asked: list[tuple] = []

    async def allowed(actor, tok, entity_id, level="viewer"):
        asked.append((actor, tok, level))
        return True

    monkeypatch.setattr(matrx_orm, "platform_access_check", allowed)
    try:
        await getattr(sources, fn)(*args, user_id="reader-1")
    except Exception:  # noqa: BLE001 - the fake row is thin; only the gate and the filter matter here
        pass
    assert asked and asked[0] == ("reader-1", token, "viewer")
    assert "created_by" not in wired


@pytest.mark.parametrize("fn,args,token", CASES)
async def test_a_stranger_gets_nothing(fn, args, token, wired, monkeypatch):
    import matrx_orm

    async def refused(*_a, **_k):
        return False

    monkeypatch.setattr(matrx_orm, "platform_access_check", refused)
    assert await getattr(sources, fn)(*args, user_id="stranger") is None


async def test_an_org_file_keeps_indexing_after_its_creator_left(monkeypatch):
    """Auto-ingest runs as the organization's system context: the departed creator no longer reaches the
    file, but the organization's own run still indexes it - and only for the file's own organization."""
    import matrx_orm

    class _CF:
        @staticmethod
        def filter(*a: Any, **kw: Any) -> _Q:
            return _Q({})

    async def refused(*_a, **_k):
        return False

    monkeypatch.setattr(matrx_orm, "platform_access_check", refused)
    monkeypatch.setattr(sources, "get_db_model", lambda *a, **k: _CF)

    class _R(_Q):
        async def values(self, *_f: str) -> list[dict[str, Any]]:
            return [_Row(id="f1", created_by="gone", organization_id="org-1", path="a.py", name="a.py",
                         content="x = 1", language="python", tags=[], metadata={})]

    _CF.filter = staticmethod(lambda *a, **kw: _R({}))
    assert await sources._resolve_code_file("f1", user_id="gone") is None
    assert await sources._resolve_code_file("f1", user_id="gone", system_organization_id="org-2") is None
    out = await sources._resolve_code_file("f1", user_id="gone", system_organization_id="org-1")
    assert out is not None and out.organization_id == "org-1"


# ── The narrow organization escape, the SAME for every source kind that carries an organization ──────────────────
# (fn, args, token). Off a person's request only: system_organization_id is set by an automatic ingest alone, and
# the row's own organization_id must equal it.
ESCAPE_CASES = [
    ("_resolve_note", ("x1",), "note"),
    ("_resolve_document", ("x1",), "document"),
    ("_resolve_task", ("x1",), "task"),
    ("_resolve_project", ("x1",), "project"),
    ("_resolve_repository", ("x1",), "code_repository"),
    ("_resolve_canvas_item", ("x1",), "canvas_item"),
    ("_resolve_transcript", ("x1",), "transcript"),
    ("_resolve_udt", ("workbook", "x1"), "workbook"),
    ("_resolve_udt", ("udt_document", "x1"), "udt_document"),
    ("_resolve_code_file", ("x1",), "code_file"),
]


@pytest.fixture
def org_row(monkeypatch):
    import matrx_orm

    class _OrgQ(_Q):
        async def values(self, *_f: str) -> list[dict[str, Any]]:
            return [_Row(id="x1", created_by="gone", organization_id="org-1", topic_id="tp1", name="n", title="t",
                         label="l", content="body", description="d", slug="s", path="a.py", language="python",
                         tags=[], metadata={})]

    class _OrgModel:
        @staticmethod
        def filter(*a: Any, **kw: Any) -> _OrgQ:
            return _OrgQ({})

    async def refused(*_a, **_k):
        return False

    monkeypatch.setattr(matrx_orm, "platform_access_check", refused)
    monkeypatch.setattr(sources, "get_db_model", lambda *a, **k: _OrgModel)
    gate: list[bool] = []
    real = sources._may_read

    async def spy(*a, **k):
        out = await real(*a, **k)
        gate.append(out)
        return out

    monkeypatch.setattr(sources, "_may_read", spy)
    return gate


async def _run(fn, args, **kw):
    try:
        return await getattr(sources, fn)(*args, user_id="gone", **kw)
    except Exception:  # noqa: BLE001 - the fake row is thin; only the gate's answer matters
        return "past-the-gate"


@pytest.mark.parametrize("fn,args,token", ESCAPE_CASES)
async def test_the_organizations_own_run_is_let_in_for_its_own_row(fn, args, token, org_row):
    await _run(fn, args, system_organization_id="org-1")
    assert org_row == [True]


@pytest.mark.parametrize("fn,args,token", ESCAPE_CASES)
async def test_the_escape_is_refused_for_another_organization(fn, args, token, org_row):
    assert await _run(fn, args, system_organization_id="org-2") is None
    assert org_row == [False]


@pytest.mark.parametrize("fn,args,token", ESCAPE_CASES)
async def test_a_persons_request_never_gets_the_escape(fn, args, token, org_row):
    assert await _run(fn, args) is None  # no system_organization_id: the access check alone decides
    assert org_row == [False]


async def test_resolve_passes_the_organization_to_every_kind_it_dispatches(monkeypatch):
    seen: dict[str, Any] = {}

    def fake(name):
        async def _f(*a: Any, **kw: Any):
            seen[name] = kw.get("system_organization_id")

        return _f

    for kind, fn in [("note", "_resolve_note"), ("document", "_resolve_document"), ("task", "_resolve_task"),
                     ("project", "_resolve_project"), ("repository", "_resolve_repository"),
                     ("canvas_item", "_resolve_canvas_item"), ("transcript", "_resolve_transcript"),
                     ("workbook", "_resolve_udt"), ("code_file", "_resolve_code_file")]:
        monkeypatch.setattr(sources, fn, fake(kind))
        await sources._resolve_dispatch(kind, "x1", None, user_id="u", system_organization_id="org-1")
    assert seen == dict.fromkeys(["note", "document", "task", "project", "repository", "canvas_item",
                                  "transcript", "workbook", "code_file"], "org-1")
