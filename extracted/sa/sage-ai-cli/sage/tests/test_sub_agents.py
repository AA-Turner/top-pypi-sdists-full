"""Tests for sub-agent (specialist) abstraction (D12).

Mirrors Claude Code's Agent tool: the main agent can DELEGATE a focused
subtask to a specialist whose system prompt is tailored for that domain
(frontend, backend, devops, data). The specialist runs in its own
context — its findings come back as a summary, not as raw tool output —
so the main agent's context window doesn't bloat.
"""

from __future__ import annotations

import pytest


class TestDefaultSpecialists:

    def test_includes_core_four_domains(self):
        from sage.core.specialists import default_specialists
        names = {s.domain for s in default_specialists()}
        assert {"frontend", "backend", "devops", "data"} <= names

    def test_each_specialist_has_focused_system_prompt(self):
        from sage.core.specialists import default_specialists
        for s in default_specialists():
            # Reasonable prompt — not empty, not just a name
            assert len(s.system_prompt) > 100
            # Domain name should appear in the prompt body
            assert s.domain.lower() in s.system_prompt.lower()

    def test_frontend_prompt_mentions_dom_and_ui(self):
        from sage.core.specialists import default_specialists
        fe = next(s for s in default_specialists() if s.domain == "frontend")
        prompt = fe.system_prompt.lower()
        assert any(kw in prompt for kw in ("ui", "react", "component", "dom", "css"))

    def test_backend_prompt_mentions_api_and_data(self):
        from sage.core.specialists import default_specialists
        be = next(s for s in default_specialists() if s.domain == "backend")
        prompt = be.system_prompt.lower()
        assert any(kw in prompt for kw in ("api", "endpoint", "database", "service"))


class TestDelegate:

    def test_delegate_calls_router_with_specialist_prompt(self):
        from sage.core.router import ProviderRouter
        from sage.core.specialists import Specialist, delegate_to
        from sage.providers.base import ModelInfo, ProviderBase

        captured = {}

        class _Provider(ProviderBase):
            name = "mock"
            def is_available(self): return True
            def list_models(self):
                return [ModelInfo(id="m", provider="mock", name="m", local=True)]
            def generate(self, messages, model_name, *a, **kw):
                captured["messages"] = list(messages)
                captured["model"] = model_name
                return "DONE"
            def stream(self, *a, **kw):
                yield "DONE"

        router = ProviderRouter([_Provider()])
        spec = Specialist(
            name="TestSpec",
            domain="frontend",
            system_prompt="You are a frontend specialist.",
        )
        result = delegate_to(spec, "fix the dashboard layout", router)
        assert result == "DONE"
        # Specialist prompt was sent as a system message
        assert any(
            m.role == "system" and "frontend specialist" in m.content.lower()
            for m in captured["messages"]
        )
        # User task came through verbatim
        assert any(
            m.role == "user" and m.content == "fix the dashboard layout"
            for m in captured["messages"]
        )


class TestSpecialistAsTool:
    """Specialists are emitted to capable providers as structured tools
    so the main agent can DELEGATE: <domain> "task" exactly like any
    other tool call."""

    def test_specialist_to_tool_spec(self):
        from sage.core.specialists import Specialist, specialist_to_tool_spec
        spec = Specialist(
            name="DBSpec",
            domain="data",
            system_prompt="...",
        )
        tool = specialist_to_tool_spec(spec)
        # Tool name follows DELEGATE_<domain> convention
        assert tool.name.startswith("DELEGATE")
        assert "data" in tool.name.lower()
        # Has a task parameter
        assert "task" in tool.parameters


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
