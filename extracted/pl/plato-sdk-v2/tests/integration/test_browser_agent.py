"""Integration tests for browser agents.

These tests:
- Build the browser agent Docker image locally
- Run the test agent to navigate to google.com and take a screenshot
- Verify events are captured correctly

Run with:
    pytest tests/integration/test_browser_agent.py -v -s

Requirements:
- Docker running
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

# Get the browser agent directory path (Dockerfile is now in browser/ not docker/)
BROWSER_DIR = Path(__file__).parent.parent.parent / "plato" / "agent" / "browser"
TEST_IMAGE_NAME = "plato-browser-agent-test:latest"


def is_docker_available() -> bool:
    """Check if Docker is available."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


HAS_DOCKER = is_docker_available()


@pytest.fixture(scope="module")
def browser_agent_image() -> str:
    """Build the browser agent Docker image for testing."""
    if not HAS_DOCKER:
        pytest.skip("Docker not available")

    print(f"\nBuilding browser agent image from {BROWSER_DIR}...")

    # Build the image
    result = subprocess.run(
        [
            "docker",
            "build",
            "-t",
            TEST_IMAGE_NAME,
            "-f",
            str(BROWSER_DIR / "Dockerfile"),
            str(BROWSER_DIR),
        ],
        capture_output=True,
        text=True,
        timeout=600,  # 10 minutes for build
    )

    if result.returncode != 0:
        print(f"Build stdout: {result.stdout}")
        print(f"Build stderr: {result.stderr}")
        pytest.fail(f"Failed to build Docker image: {result.stderr}")

    print(f"Successfully built image: {TEST_IMAGE_NAME}")
    return TEST_IMAGE_NAME


@pytest.mark.skipif(not HAS_DOCKER, reason="Docker not available")
class TestBrowserAgentDocker:
    """Tests for browser agent Docker image."""

    def test_docker_image_builds(self, browser_agent_image: str):
        """Test that the Docker image builds successfully."""
        # Just verify the fixture ran
        assert browser_agent_image == TEST_IMAGE_NAME

        # Verify image exists
        result = subprocess.run(
            ["docker", "images", "-q", TEST_IMAGE_NAME],
            capture_output=True,
            text=True,
        )
        assert result.stdout.strip(), f"Image {TEST_IMAGE_NAME} not found"

    def test_test_agent_runs(self, browser_agent_image: str):
        """Test that the test agent can run and navigate to a URL."""
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                browser_agent_image,
                "--model",
                "test",
                "--task",
                "navigate only",
                "--start-url",
                "https://example.com",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        print(f"\nOutput:\n{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")

        assert result.returncode == 0, f"Agent failed: {result.stderr}"
        assert "RESULT:" in result.stdout, "No result in output"
        assert "example.com" in result.stdout.lower(), "Should have navigated to example.com"

    def test_test_agent_screenshot(self, browser_agent_image: str):
        """Test that the test agent can take a screenshot."""
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                browser_agent_image,
                "--model",
                "test",
                "--task",
                "take a screenshot",
                "--start-url",
                "https://example.com",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        print(f"\nOutput:\n{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")

        assert result.returncode == 0, f"Agent failed: {result.stderr}"
        assert "Screenshot captured" in result.stdout, "Screenshot not captured"

    def test_test_agent_google(self, browser_agent_image: str):
        """Test that the test agent can navigate to google.com and screenshot."""
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                browser_agent_image,
                "--model",
                "test",
                "--task",
                "take a screenshot",
                "--start-url",
                "https://www.google.com",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        print(f"\nOutput:\n{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")

        assert result.returncode == 0, f"Agent failed: {result.stderr}"
        assert "RESULT:" in result.stdout, "No result in output"
        assert "Screenshot captured" in result.stdout, "Screenshot not captured"
        # Google's title varies by region but should contain "Google"
        assert "google" in result.stdout.lower(), "Should have Google in output"

    def test_events_are_emitted(self, browser_agent_image: str):
        """Test that events are properly emitted as JSON."""
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                browser_agent_image,
                "--model",
                "test",
                "--task",
                "take a screenshot",
                "--start-url",
                "https://example.com",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, f"Agent failed: {result.stderr}"

        # Parse events from output
        events = []
        for line in result.stdout.split("\n"):
            if line.startswith("EVENT:"):
                try:
                    event = json.loads(line[6:])
                    events.append(event)
                except json.JSONDecodeError:
                    pass

        print(f"\nCaptured {len(events)} events:")
        for event in events:
            print(f"  - {event.get('type', 'unknown')}")

        # Verify expected events
        event_types = [e.get("type") for e in events]

        assert "start" in event_types, "Missing start event"
        assert "tool_use" in event_types, "Missing tool_use event"
        assert "tool_result" in event_types, "Missing tool_result event"
        assert "complete" in event_types, "Missing complete event"

        # Verify event structure
        start_event = next(e for e in events if e.get("type") == "start")
        assert start_event.get("agent") == "TestAgent"
        assert start_event.get("provider") == "test"
        assert "timestamp" in start_event

        complete_event = next(e for e in events if e.get("type") == "complete")
        assert complete_event.get("success") is True
        assert "output" in complete_event


class TestBrowserAgentConfig:
    """Tests for browser agent configuration."""

    def test_browser_agent_config_defaults(self):
        """Test default configuration values."""
        from plato.agent.browser import BrowserAgentConfig

        config = BrowserAgentConfig(model="test")

        assert config.model == "test"
        assert config.runtime == "docker"  # Default is docker
        assert config.browser_type == "local"
        assert config.headless is True
        assert config.viewport_width == 1280
        assert config.viewport_height == 800
        assert config.start_url is None

    def test_browser_agent_config_local_runtime(self):
        """Test local runtime configuration."""
        from plato.agent.browser import BrowserAgentConfig

        config = BrowserAgentConfig(
            model="test",
            runtime="local",
            headless=False,
        )

        assert config.model == "test"
        assert config.runtime == "local"
        assert config.headless is False

    def test_browser_agent_config_custom(self):
        """Test custom configuration values."""
        from plato.agent.browser import BrowserAgentConfig

        config = BrowserAgentConfig(
            model="claude-sonnet-4-5-20250929",
            browser_type="browserbase",
            headless=False,
            viewport_width=1920,
            viewport_height=1080,
            start_url="https://example.com",
        )

        assert config.model == "claude-sonnet-4-5-20250929"
        assert config.browser_type == "browserbase"
        assert config.headless is False
        assert config.viewport_width == 1920
        assert config.viewport_height == 1080
        assert config.start_url == "https://example.com"

    def test_browser_agent_properties(self):
        """Test BrowserAgent properties."""
        from plato.agent.browser import BrowserAgent, BrowserAgentConfig

        agent = BrowserAgent(BrowserAgentConfig(model="test"))

        assert agent.name == "BrowserAgent[test]"
        assert agent.provider == "test"
        assert "test" in agent.models()
        assert "plato-browser-agent" in agent.image

    def test_browser_agent_claude_model(self):
        """Test BrowserAgent with Claude model."""
        from plato.agent.browser import BrowserAgent, BrowserAgentConfig

        agent = BrowserAgent(BrowserAgentConfig(model="claude-sonnet-4-5-20250929"))

        assert agent.name == "BrowserAgent[claude-sonnet-4-5-20250929]"
        assert agent.provider == "anthropic"
        assert "claude-sonnet-4-5-20250929" in agent.models()

    def test_browser_agent_unsupported_model(self):
        """Test BrowserAgent with unsupported model raises error."""
        from plato.agent.browser import BrowserAgent, BrowserAgentConfig

        with pytest.raises(ValueError, match="Unsupported model"):
            BrowserAgent(BrowserAgentConfig(model="invalid-model-xyz"))

    def test_build_command(self):
        """Test command building for browser agents."""
        from plato.agent.browser import BrowserAgent, BrowserAgentConfig

        agent = BrowserAgent(
            BrowserAgentConfig(
                model="test",
                start_url="https://example.com",
            )
        )

        cmd = agent.build_command("take a screenshot")

        assert "--model" in cmd
        assert "test" in cmd
        assert "--task" in cmd
        assert "--start-url" in cmd
        assert "https://example.com" in cmd


class TestBrowserAgentImports:
    """Tests for browser agent imports."""

    def test_browser_agent_importable(self):
        """Test that BrowserAgent can be imported."""
        from plato.agent.browser import (
            SUPPORTED_MODELS,
            BrowserAgent,
            BrowserAgentConfig,
            StorageTraceAdapter,
        )

        # Verify imports work
        assert BrowserAgent is not None
        assert BrowserAgentConfig is not None
        assert StorageTraceAdapter is not None
        assert isinstance(SUPPORTED_MODELS, dict)

    def test_supported_models(self):
        """Test that supported models are available."""
        from plato.agent.browser import SUPPORTED_MODELS

        # Verify all expected providers are supported
        providers = set(SUPPORTED_MODELS.values())
        assert "anthropic" in providers
        assert "openai" in providers
        assert "google" in providers
        assert "amazon" in providers
        assert "test" in providers

        # Verify some specific models
        assert "claude-sonnet-4-5-20250929" in SUPPORTED_MODELS
        assert "gpt-4o" in SUPPORTED_MODELS
        assert "gemini-2.0-flash" in SUPPORTED_MODELS
        assert "test" in SUPPORTED_MODELS

    def test_agent_from_main_module(self):
        """Test that BrowserAgent can be imported from main plato.agent module."""
        from plato.agent import BrowserAgent, BrowserAgentConfig

        # Verify they have expected attributes
        assert hasattr(BrowserAgent, "models")
        # model is a field, not class attribute - check model_fields instead
        assert "model" in BrowserAgentConfig.model_fields
