"""Tests for prompt_library — specialized per-file-type prompts."""

from __future__ import annotations

from sage.core.principal_engineer import FileSpec
from sage.core.prompt_library import _classify_path, build_specialized_prompt


class TestClassify:
    def test_model(self) -> None:
        assert _classify_path("backend/app/models/campaign.py") == "model"

    def test_schema(self) -> None:
        assert _classify_path("backend/app/schemas/campaign.py") == "schema"

    def test_repository(self) -> None:
        assert _classify_path("backend/app/repositories/campaign.py") == "repository"

    def test_service(self) -> None:
        assert _classify_path("backend/app/services/campaign.py") == "service"

    def test_api(self) -> None:
        assert _classify_path("backend/app/api/v1/campaigns.py") == "api"

    def test_celery_task(self) -> None:
        assert _classify_path("backend/app/tasks/campaign.py") == "celery_task"
        assert _classify_path("backend/app/tasks/celery_app.py") == "celery_app"

    def test_rn_screen(self) -> None:
        assert _classify_path("frontend/app/(tabs)/dashboard.tsx") == "rn_screen"

    def test_rn_hook(self) -> None:
        assert _classify_path("frontend/src/hooks/useCampaign.ts") == "rn_hook"

    def test_rn_store(self) -> None:
        assert _classify_path("frontend/src/stores/campaign.store.ts") == "rn_store"

    def test_rn_component(self) -> None:
        assert _classify_path("frontend/src/components/campaign/Card.tsx") == "rn_component"

    def test_unknown_falls_back_to_generic(self) -> None:
        assert _classify_path("random/path.xyz") == "generic"


class TestBuildSpecializedPrompt:
    def test_model_prompt_includes_sqlmodel_patterns(self) -> None:
        spec = FileSpec(
            path="backend/app/models/campaign.py",
            role="domain entity",
            language="python",
        )
        prompt = build_specialized_prompt(
            "build a campaign feature", spec, ["backend/app/models/campaign.py"],
            "fastapi"
        )
        assert "SQLModel" in prompt
        assert "tenant_id" in prompt
        assert "soft-delete" in prompt
        assert "Relationship" in prompt

    def test_api_prompt_includes_fastapi_patterns(self) -> None:
        spec = FileSpec(
            path="backend/app/api/v1/campaigns.py",
            role="router",
            language="python",
        )
        prompt = build_specialized_prompt("x", spec, [], "fastapi")
        assert "Depends(get_current_user)" in prompt
        assert "response_model" in prompt
        assert "global handler" in prompt

    def test_rn_screen_prompt_forbids_html(self) -> None:
        spec = FileSpec(
            path="frontend/app/(tabs)/dashboard.tsx",
            role="screen",
            language="typescript",
        )
        prompt = build_specialized_prompt("x", spec, [], "react-native-web")
        assert "NO HTML elements" in prompt
        assert "Pressable" in prompt

    def test_includes_sibling_excerpts(self) -> None:
        spec = FileSpec(
            path="backend/app/schemas/campaign.py",
            role="schema",
            language="python",
        )
        prompt = build_specialized_prompt(
            "x", spec, [], "fastapi",
            sibling_excerpts={"backend/app/models/campaign.py": "class Campaign(SQLModel):\n    id: int"},
        )
        assert "class Campaign(SQLModel)" in prompt
        assert "backend/app/models/campaign.py" in prompt

    def test_reminder_about_no_thinking_tags(self) -> None:
        spec = FileSpec(path="x.py", role="x", language="python")
        prompt = build_specialized_prompt("x", spec, [], "fastapi")
        assert "no `<thinking>` tags" in prompt or "<thinking>" in prompt
        assert "Output ONLY the file contents" in prompt
