"""Tests for per-subtask multi-model routing in /autofleet and /autoorg.

The current orchestrator binds to a single model at construction. For
/autofleet (parallel subtasks) and /autoorg (orchestrated steps), each
subtask should pick the best model for its complexity:

  - Trivial subtasks ("rename foo") → small fast local model
  - Architecture subtasks ("design auth flow") → big model with reasoning
  - Code-write subtasks ("implement endpoint") → coding-tuned model

This module adds `MultiModelOrchestrator` that wraps a router and
routes each call through the picker.
"""

from __future__ import annotations

import pytest


class TestSubtaskModelPicker:
    """Verify each subtask gets a model appropriate to its description."""

    def test_trivial_task_picks_small_model(self):
        from sage.core.multi_model_orchestration import pick_model_for_subtask
        from sage.providers.base import ModelInfo

        catalog = [
            ModelInfo(id="llama3.2", provider="ollama", name="small", local=True),
            ModelInfo(id="qwen3-coder-next", provider="ollama", name="big", local=True),
        ]
        picked = pick_model_for_subtask(
            description="rename utility function `foo` to `bar`",
            available=catalog,
        )
        assert picked == "llama3.2"

    def test_architecture_task_picks_big_model(self):
        from sage.core.multi_model_orchestration import pick_model_for_subtask
        from sage.providers.base import ModelInfo

        catalog = [
            ModelInfo(id="llama3.2", provider="ollama", name="small", local=True),
            ModelInfo(id="qwen3-coder-next", provider="ollama", name="big", local=True),
        ]
        picked = pick_model_for_subtask(
            description=(
                "Design the authentication subsystem architecture spanning the "
                "frontend SDK, the backend session service, and the multi-tenant "
                "permission model. Account for SSO, MFA, and audit trail."
            ),
            available=catalog,
        )
        assert picked == "qwen3-coder-next"

    def test_falls_back_to_first_model_when_no_match(self):
        from sage.core.multi_model_orchestration import pick_model_for_subtask
        from sage.providers.base import ModelInfo

        catalog = [
            ModelInfo(id="some-medium-model", provider="x", name="m", local=False),
        ]
        picked = pick_model_for_subtask(
            description="rename foo to bar",
            available=catalog,
        )
        assert picked == "some-medium-model"


class TestMultiModelOrchestratorRouting:
    """End-to-end: orchestrator routes each subtask through the picked model."""

    def test_each_subtask_uses_its_picked_model(self):
        from sage.core.multi_model_orchestration import MultiModelOrchestrator
        from sage.core.router import ProviderRouter
        from sage.providers.base import Message, ModelInfo, ProviderBase

        captured: list[tuple[str, str]] = []

        class _Provider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [
                    ModelInfo(id="llama3.2", provider="mock", name="s", local=True),
                    ModelInfo(id="qwen3-coder-next", provider="mock", name="b", local=True),
                ]
            def generate(self, messages, model_name, *a, **kw):
                captured.append((model_name, messages[-1].content[:50]))
                return "done"
            def stream(self, *a, **kw):
                yield "done"

        router = ProviderRouter([_Provider()])
        mmo = MultiModelOrchestrator(router=router)

        subtasks = [
            "rename foo to bar",
            "refactor the entire authentication architecture",
            "fix typo on line 5",
        ]
        results = [mmo.run_subtask(desc=t) for t in subtasks]
        assert len(results) == 3
        # Trivial → small, complex → big, trivial → small
        models_used = [m for m, _ in captured]
        assert models_used[0] == "llama3.2"
        assert models_used[1] == "qwen3-coder-next"
        assert models_used[2] == "llama3.2"

    def test_run_returns_per_subtask_metadata(self):
        from sage.core.multi_model_orchestration import MultiModelOrchestrator, SubtaskResult
        from sage.core.router import ProviderRouter
        from sage.providers.base import ModelInfo, ProviderBase

        class _Provider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [ModelInfo(id="m", provider="mock", name="m", local=True)]
            def generate(self, *a, **kw): return "answer"
            def stream(self, *a, **kw): yield "answer"

        router = ProviderRouter([_Provider()])
        mmo = MultiModelOrchestrator(router=router)

        result = mmo.run_subtask(desc="anything")
        assert isinstance(result, SubtaskResult)
        assert result.output == "answer"
        assert result.model_used == "m"
        assert result.subtask == "anything"


class TestRunFleetParallel:
    """A list of subtasks runs in parallel; each picks its own model;
    aggregate result preserves order."""

    def test_parallel_run_preserves_order(self):
        from sage.core.multi_model_orchestration import MultiModelOrchestrator
        from sage.core.router import ProviderRouter
        from sage.providers.base import ModelInfo, ProviderBase

        class _Provider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [ModelInfo(id="m", provider="mock", name="m", local=True)]
            def generate(self, messages, model_name, *a, **kw):
                # Echo the input back so we can verify order
                return f"echo:{messages[-1].content}"
            def stream(self, *a, **kw): yield "x"

        router = ProviderRouter([_Provider()])
        mmo = MultiModelOrchestrator(router=router)
        descs = ["one", "two", "three"]
        results = mmo.run_fleet(descs, parallel=True)
        assert [r.output for r in results] == ["echo:one", "echo:two", "echo:three"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
