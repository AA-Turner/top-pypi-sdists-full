"""Integration tests for plato.agents.AgentRunner.

Tests the AgentRunner utility that runs agents in Docker containers.
Each agent has its own entrypoint that handles execution internally.

These tests require:
- Docker installed and running
- GCR authentication for the agent images

Run with:
    RUN_HARBOR_TESTS=1 GEMINI_API_KEY=... pytest tests/integration/test_harbor_agent_runner.py -v -s
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile

import pytest


def _cleanup_docker_dir(path: str) -> None:
    """Clean up directory that may contain root-owned files from Docker."""
    try:
        shutil.rmtree(path)
    except PermissionError:
        # Docker creates files as root, use subprocess to clean up
        subprocess.run(["sudo", "rm", "-rf", path], check=False)


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory."""
    tmpdir = tempfile.mkdtemp()
    # Create a simple file to work with
    test_file = os.path.join(tmpdir, "test.py")
    with open(test_file, "w") as f:
        f.write("# Test file\nprint('hello')\n")
    yield tmpdir
    _cleanup_docker_dir(tmpdir)


@pytest.fixture
def temp_logs_dir():
    """Create a temporary logs directory."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    _cleanup_docker_dir(tmpdir)


@pytest.fixture
def openhands_image():
    """OpenHands ECR image."""
    return "383806609161.dkr.ecr.us-west-1.amazonaws.com/agents/plato/openhands:1.0.7"


@pytest.fixture
def openhands_config():
    """OpenHands agent config matching the schema."""
    # Use Gemini model for testing
    return {
        "model_name": "gemini/gemini-3-flash-preview",
    }


@pytest.fixture
def secrets():
    """Secrets from environment."""
    # Try Gemini first, then Anthropic
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        return {"gemini_api_key": gemini_key}

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_key:
        return {"anthropic_api_key": anthropic_key}

    pytest.skip("GEMINI_API_KEY or ANTHROPIC_API_KEY not set")
    return {}


class TestAgentRunner:
    """Test AgentRunner with real OpenHands agent."""

    @pytest.mark.skipif(
        os.environ.get("RUN_HARBOR_TESTS") != "1",
        reason="Set RUN_HARBOR_TESTS=1 to run harbor integration tests",
    )
    @pytest.mark.asyncio
    async def test_openhands_agent_runner(
        self,
        temp_workspace: str,
        temp_logs_dir: str,
        openhands_image: str,
        openhands_config: dict,
        secrets: dict,
    ):
        """Test running OpenHands agent via AgentRunner."""
        from plato.agents import AgentRunner

        # Ask agent to create a file so we can verify it actually works
        instruction = "Create a file called hello.txt with the content 'hello world' in the current directory."

        output_lines = []
        result = AgentRunner.run(
            image=openhands_image,
            config=openhands_config,
            secrets=secrets,
            instruction=instruction,
            workspace=temp_workspace,
            logs_dir=temp_logs_dir,
            pull=True,
        )

        async for line in result:
            print(line)
            output_lines.append(line)

        # Verify we got some output
        assert len(output_lines) > 0, "Expected some output from agent"

        # Check for expected patterns in output
        full_output = "\n".join(output_lines)
        # OpenHands should at least start up
        assert any(pattern in full_output.lower() for pattern in ["openhands", "agent", "running", "sandbox"]), (
            f"Expected OpenHands startup output, got: {full_output[:500]}"
        )

        # Check logs were written (use sudo since Docker creates files as root)
        logs_agent_dir = os.path.join(temp_logs_dir, "agent")
        check_result = subprocess.run(["sudo", "test", "-d", logs_agent_dir], capture_output=True)
        assert check_result.returncode == 0, "Expected agent logs directory"

        # Debug: list files in workspace (use sudo since Docker creates files as root)
        ls_result = subprocess.run(["sudo", "ls", "-la", temp_workspace], capture_output=True, text=True)
        print(f"\nWorkspace contents after agent run:\n{ls_result.stdout}")

        # Verify the agent actually created the file (use sudo to read root-owned file)
        hello_file = os.path.join(temp_workspace, "hello.txt")
        cat_result = subprocess.run(["sudo", "cat", hello_file], capture_output=True, text=True)
        assert cat_result.returncode == 0, (
            f"Expected agent to create hello.txt in {temp_workspace}. Error: {cat_result.stderr}"
        )
        content = cat_result.stdout
        assert "hello" in content.lower(), f"Expected hello.txt to contain 'hello', got: {content}"
        print(f"\nhello.txt content: {content}")

        # Print logs location (use sudo since Docker creates files as root)
        print(f"\nLogs saved to: {result.logs_dir}")
        logs_ls = subprocess.run(["sudo", "ls", "-la", logs_agent_dir], capture_output=True, text=True)
        print(f"Agent logs dir contents:\n{logs_ls.stdout}")

    @pytest.mark.skipif(
        os.environ.get("RUN_HARBOR_TESTS") != "1",
        reason="Set RUN_HARBOR_TESTS=1 to run harbor integration tests",
    )
    @pytest.mark.asyncio
    async def test_agent_runner_no_pull(
        self,
        temp_workspace: str,
        temp_logs_dir: str,
        openhands_image: str,
        openhands_config: dict,
        secrets: dict,
    ):
        """Test running agent without pulling (assumes image exists)."""
        from plato.agents import AgentRunner

        instruction = "Print 'hello world'"

        output_lines = []
        result = AgentRunner.run(
            image=openhands_image,
            config=openhands_config,
            secrets=secrets,
            instruction=instruction,
            workspace=temp_workspace,
            logs_dir=temp_logs_dir,
            pull=False,  # Skip pull
        )

        async for line in result:
            print(line)
            output_lines.append(line)

        # Should not have any [pull] prefixed lines
        pull_lines = [line for line in output_lines if line.startswith("[pull]")]
        assert len(pull_lines) == 0, "Should not have pull output when pull=False"

    def test_agent_schemas(self):
        """Test that agent schemas are available."""
        from plato.agents import AGENT_SCHEMAS, get_agent_schema

        # Check some agents exist
        assert "openhands" in AGENT_SCHEMAS
        assert "claude-code" in AGENT_SCHEMAS
        assert "aider" in AGENT_SCHEMAS

        # Check schema structure
        oh_schema = get_agent_schema("openhands")
        assert oh_schema is not None
        assert "properties" in oh_schema
        assert "model_name" in oh_schema["properties"]

        # Check unknown agent returns None
        assert get_agent_schema("nonexistent") is None
