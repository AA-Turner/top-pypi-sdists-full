"""A skill's allowed_tools may name a tool; the provider must resolve it, never drop it."""

from types import SimpleNamespace
from uuid import UUID, uuid4

from matrx_ai.skills import providers


def _row(allowed):
    return SimpleNamespace(
        id=uuid4(), skill_id="shape-authoring", label="Shape authoring", description="d",
        skill_type="reference", body="b", allowed_tools=allowed, trigger_patterns=[],
        disable_auto_invocation=False, config={}, version=1, category_id=None,
    )


def test_tool_name_resolves_to_its_uuid(monkeypatch):
    tool_id = uuid4()
    monkeypatch.setattr(providers, "_tool_uuid_for_name", lambda n: tool_id if n == "kindcomp_preview" else None)
    body = providers._row_to_body(_row(["kindcomp_preview"]), [])
    assert body.allowed_tools == [tool_id]


def test_uuid_entries_still_pass_and_unknown_names_drop(monkeypatch):
    known = uuid4()
    monkeypatch.setattr(providers, "_tool_uuid_for_name", lambda n: None)
    body = providers._row_to_body(_row([str(known), "no_such_tool"]), [])
    assert body.allowed_tools == [UUID(str(known))]
