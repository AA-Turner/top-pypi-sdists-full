"""Integration tests for Agent workflows using VCR cassettes."""

import pytest
from mistralai.client import models as mistralai_models

from mistralai.workflows.plugins.mistralai import Agent
from mistralai.workflows.plugins.mistralai.connectors import connector
from mistralai.workflows.plugins.mistralai.runner import Runner
from mistralai.workflows.plugins.mistralai.session import LocalSession


class TestAgentIntegration:
    @pytest.mark.vcr()
    @pytest.mark.asyncio
    async def test_simple_agent_run(self):
        """Test a simple agent run with LocalSession."""
        session = LocalSession()

        agent = Agent(
            model="mistral-medium-latest",
            name="test-agent",
            instructions="You are a helpful assistant. Answer briefly.",
        )

        outputs = await Runner.run(
            agent=agent,
            inputs="What is 2+2? Answer with just the number.",
            session=session,
        )

        assert len(outputs) >= 1
        assert any(isinstance(output, mistralai_models.TextChunk) for output in outputs)

    @pytest.mark.vcr()
    @pytest.mark.asyncio
    async def test_agent_with_handoff(self):
        """Test agent with handoff to another agent."""
        session = LocalSession()

        math_agent = Agent(
            model="mistral-medium-latest",
            name="math-agent",
            instructions="You are a math expert. Answer math questions concisely.",
        )

        router_agent = Agent(
            model="mistral-medium-latest",
            name="router-agent",
            instructions="Route math questions to the math agent.",
            handoffs=[math_agent],
        )

        outputs = await Runner.run(
            agent=router_agent,
            inputs="What is 5 * 7?",
            session=session,
        )

        assert len(outputs) >= 1
        assert any(isinstance(output, mistralai_models.TextChunk) for output in outputs)

    @pytest.mark.vcr()
    @pytest.mark.asyncio
    async def test_agent_with_connector(self):
        """Test an agent with a connector tool via LocalSession."""
        session = LocalSession()

        agent = Agent(
            model="mistral-medium-latest",
            name="github-agent",
            instructions="You have access to GitHub. Be brief.",
            connectors=[connector("github_app")],
        )

        outputs = await Runner.run(
            agent=agent,
            inputs="List 1 recent PR on octocat/Hello-World. One sentence.",
            session=session,
        )

        assert len(outputs) >= 1
        assert any(isinstance(output, mistralai_models.TextChunk) for output in outputs)
