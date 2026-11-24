"""A button on a business's own kind runs that business's own job or workflow.

PF-L4 (2026-11-02): Company Setup bound a kind's "Generate image" button to the
platform-only ``run_shortcut`` handler with a pinned platform shortcut id — no
company workflow was built, and the business could neither see nor change what
its button ran. The write gate on every component write path now refuses that
source for any kind not owned by the platform, and names the right shape.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai.tools.models import ToolContext

PLATFORM_ORG = "39c38960-d30c-4840-b0c1-c9960de95582"

PINNED_SHORTCUT_BUTTON = """
import { KindActionButton } from "@/components/kind-kit/KindActionButton";
const IMAGE_SHORTCUT = "a415f9f8-aa62-45f9-a532-5987da03ee59";
export default function PostIdea({ data, runAction }) {
  return <KindActionButton label="Generate image" runAction={runAction}
    action="run_shortcut" input={{ shortcutId: IMAGE_SHORTCUT, scope: { idea: data.title } }} />;
}
"""

OWN_WORKFLOW_BUTTON = """
import { KindActionButton } from "@/components/kind-kit/KindActionButton";
export default function PostIdea({ data, runAction }) {
  return <KindActionButton label="Generate image" runAction={runAction} action="run"
    input={{ action: "workflow.id_0123456789abcdef0123456789abcdef", input: { idea: data.title },
             into: { state: "image_run" } }} />;
}
"""


def _harness(monkeypatch, organization_id: str) -> list[dict[str, Any]]:
    from matrx_ai.tools.implementations import kind_component

    created: list[dict[str, Any]] = []
    kind = SimpleNamespace(id=uuid4(), kind="post_idea", organization_id=organization_id)

    async def fake_resolve(_ref: str, _ctx: ToolContext):
        return kind, None

    async def fake_allow(_kind: Any, _ctx: ToolContext):
        return None

    async def fake_source(_source: str):
        return None, True

    class Query:
        async def all(self):
            return []

    class FakeKindComponent:
        @classmethod
        def filter(cls, **_filters):
            return Query()

        @classmethod
        async def update_where(cls, _filters, **_values):
            return []

        @classmethod
        async def create_item(cls, **payload):
            created.append(payload)
            return SimpleNamespace(id=uuid4(), semver="1.0.0")

    monkeypatch.setattr(kind_component, "resolve_kind", fake_resolve)
    monkeypatch.setattr(kind_component, "ensure_can_edit_kind", fake_allow)
    monkeypatch.setattr(kind_component, "_refuse_broken_source", fake_source)
    monkeypatch.setattr(kind_component, "get_db_model", lambda _name: FakeKindComponent)
    monkeypatch.setattr(kind_component, "ctx_user_id", lambda _ctx: "user-1")
    return created


async def _create(source: str):
    from matrx_ai.tools.implementations import kind_component

    return await kind_component.kindcomp_create_component(
        {"kind": "post_idea", "component_key": "post_idea_card", "component_source": source},
        ToolContext(call_id=str(uuid4()), tool_name="test"),
    )


@pytest.mark.asyncio
async def test_a_business_kind_refuses_a_pinned_platform_shortcut_button(monkeypatch) -> None:
    created = _harness(monkeypatch, str(uuid4()))
    result = await _create(PINNED_SHORTCUT_BUTTON)
    assert result.success is False, "a business kind's button was bound to a platform shortcut"
    assert created == []
    message = result.error.message
    assert "run_shortcut" in message and "a415f9f8" in message
    assert 'mandate: "<feature>.<name>"' in message and "workflow.id_<hex>" in message


@pytest.mark.asyncio
async def test_a_business_kind_accepts_a_button_running_its_own_workflow(monkeypatch) -> None:
    created = _harness(monkeypatch, str(uuid4()))
    result = await _create(OWN_WORKFLOW_BUTTON)
    assert result.success is True
    assert len(created) == 1


@pytest.mark.asyncio
async def test_a_platform_kind_may_still_use_platform_shortcuts(monkeypatch) -> None:
    created = _harness(monkeypatch, PLATFORM_ORG)
    result = await _create(PINNED_SHORTCUT_BUTTON)
    assert result.success is True
    assert len(created) == 1


def test_the_lint_names_every_platform_binding() -> None:
    from matrx_ai.tools.implementations.kind_shared import component_binding_lint

    org = str(uuid4())
    assert component_binding_lint(OWN_WORKFLOW_BUTTON, organization_id=org) is None
    assert component_binding_lint(PINNED_SHORTCUT_BUTTON, organization_id=None) is None
    agent = 'runAction("run", { action: "agent.id_0123456789abcdef0123456789abcdef" })'
    assert "agent Action" in (component_binding_lint(agent, organization_id=org) or "")
    trig = 'runAction("trigger_agent", { agentId: x })'
    assert "trigger_agent" in (component_binding_lint(trig, organization_id=org) or "")


@pytest.mark.asyncio
async def test_a_plain_word_lookup_finds_the_business_own_kinds(monkeypatch) -> None:
    """Company Setup asked kind_get for "idea", heard "no kind", and told the owner the
    business had no idea cards — while post_idea and post_idea_set were its own kinds."""
    from matrx_ai.tools.implementations import kind_authoring

    org = str(uuid4())

    async def not_found(_ref: str, _ctx: ToolContext):
        from matrx_ai.tools.implementations.kind_shared import err

        return None, err("not_found", "no such kind")

    class Query:
        async def all(self):
            return [
                SimpleNamespace(kind="post_idea", deleted_at=None),
                SimpleNamespace(kind="post_idea_set", deleted_at=None),
                SimpleNamespace(kind="post_analysis", deleted_at=None),
                SimpleNamespace(kind="old_idea", deleted_at="2026-01-01"),
            ]

    class FakeKindDefinition:
        @classmethod
        def filter(cls, **filters):
            assert filters == {"organization_id": org}
            return Query()

    monkeypatch.setattr(kind_authoring, "resolve_kind", not_found)
    monkeypatch.setattr(kind_authoring, "ctx_org_id", lambda _ctx: org)
    monkeypatch.setattr(kind_authoring, "get_db_model", lambda _name: FakeKindDefinition)

    result = await kind_authoring.kind_get({"kind": "idea"}, ToolContext(call_id="c", tool_name="kind_get"))
    note = result.output.note
    assert "post_idea" in note and "post_idea_set" in note, note
    assert "post_analysis" not in note and "old_idea" not in note
