"""Integration test for CodeWorld with a real agent."""

import os
import shutil
import tempfile

import pytest


@pytest.fixture
def git_token():
    """Git token for hub.plato.so."""
    token = os.environ.get("GIT_TOKEN")
    if not token:
        pytest.skip("GIT_TOKEN not set")
    return token


@pytest.fixture
def gemini_api_key():
    """Gemini API key."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        pytest.skip("GEMINI_API_KEY not set")
    return key


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory."""
    tmpdir = tempfile.mkdtemp(prefix="code_world_test_")
    yield tmpdir
    # Cleanup
    shutil.rmtree(tmpdir, ignore_errors=True)


class TestCodeWorldIntegration:
    """Full integration test for CodeWorld."""

    @pytest.mark.asyncio
    async def test_code_world_creates_pr(
        self,
        git_token: str,
        gemini_api_key: str,
        temp_workspace: str,
    ):
        """Test that CodeWorld can clone a repo and create a PR."""
        from code_world import CodeWorld, CodeWorldConfig

        config = CodeWorldConfig(
            repository_url="https://hub.plato.so/plato/localstack",
            prompt="Create a new pull request called 'hello from integration test'. Just add a simple README change.",
            checkout="main",
            workspace_dir=temp_workspace,
            coder={
                "image": "openhands:local",
                "config": {
                    "model_name": "gemini/gemini-2.5-flash-preview-05-20",
                    "gemini_api_key": gemini_api_key,
                },
            },
            git_token=git_token,
        )

        world = CodeWorld()
        await world.run(config)
