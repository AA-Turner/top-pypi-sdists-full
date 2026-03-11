"""Tests for workspace repo name mapping and state.workspaces key normalization."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar
from unittest.mock import AsyncMock, MagicMock

import pytest

from plato.markers import WorkspaceMarker
from plato.worlds import BaseWorld, Observation, RunConfig, StepResult

# ---------------------------------------------------------------------------
# Test fixtures: a world with a custom workspace_repo_name override
# ---------------------------------------------------------------------------


class CloneConfig(RunConfig):
    clone_name: str = "stripe"
    code: Annotated[Path, WorkspaceMarker(description="Code", tracked=True)] = Path("/workspace/code")
    recordings: Annotated[Path, WorkspaceMarker(description="Recordings", tracked=True)] = Path("/workspace/recordings")


class CloneWorld(BaseWorld[CloneConfig]):
    name: ClassVar[str] = "webclone"
    description: ClassVar[str] = "Test clone world"

    def workspace_repo_name(self, field_name: str) -> str:
        return f"{self.name}/{self.config.clone_name}/{field_name}"

    async def reset(self) -> Observation:
        return Observation()

    async def step(self) -> StepResult:
        return StepResult(observation=Observation(), done=True)


class SimpleConfig(RunConfig):
    output: Annotated[Path, WorkspaceMarker(description="Output", tracked=True)] = Path("/workspace/output")


class SimpleWorld(BaseWorld[SimpleConfig]):
    name: ClassVar[str] = "simple"
    description: ClassVar[str] = "Simple world with default repo naming"

    async def reset(self) -> Observation:
        return Observation()

    async def step(self) -> StepResult:
        return StepResult(observation=Observation(), done=True)


# ---------------------------------------------------------------------------
# Tests for workspace_repo_name
# ---------------------------------------------------------------------------


class TestWorkspaceRepoName:
    """Test workspace_repo_name method."""

    def test_default_repo_name(self):
        """Default implementation returns {world.name}/{field_name}."""
        world = SimpleWorld.__new__(SimpleWorld)
        world.config = SimpleConfig()
        assert world.workspace_repo_name("output") == "simple/output"

    def test_custom_repo_name_override(self):
        """Subclass override includes clone_name."""
        world = CloneWorld.__new__(CloneWorld)
        world.config = CloneConfig(clone_name="stripe")
        assert world.workspace_repo_name("code") == "webclone/stripe/code"
        assert world.workspace_repo_name("recordings") == "webclone/stripe/recordings"

    def test_custom_repo_name_different_clone(self):
        """Override works with different clone_name values."""
        world = CloneWorld.__new__(CloneWorld)
        world.config = CloneConfig(clone_name="hubspot")
        assert world.workspace_repo_name("code") == "webclone/hubspot/code"


# ---------------------------------------------------------------------------
# Tests for state.workspaces key normalization in load_state
# ---------------------------------------------------------------------------


class TestWorkspaceSpecsNormalization:
    """Test that load_state normalizes full repo names in state.workspaces to field names."""

    def _make_world_with_workspaces(self, clone_name: str, workspace_specs: dict[str, str]) -> CloneWorld:
        """Create a CloneWorld with pre-initialized workspaces and state config."""
        config = CloneConfig(clone_name=clone_name)
        config.state.workspaces = workspace_specs

        world = CloneWorld.__new__(CloneWorld)
        world.config = config
        world.logger = MagicMock()
        world._state = None

        # Pre-populate _workspaces as if _init_workspaces ran
        world._workspaces = {}
        for field_name in ("code", "recordings"):
            ws = MagicMock()
            ws.tracked = True
            ws.session_id = "current-session"
            ws.repo_name = world.workspace_repo_name(field_name)
            ws.repo_id = "repo-id"
            ws.s3_bucket = "bucket"
            ws.s3_prefix = "prefix"
            ws._sts_credentials = {}
            ws._sts_expires_at = 0
            world._workspaces[field_name] = ws

        # Mock session
        world.session = MagicMock()
        world.session.session_id = "current-session-id"

        return world

    @pytest.mark.asyncio
    async def test_full_repo_name_keys_are_normalized(self):
        """Config with full repo names (webclone/stripe/code) should work."""
        world = self._make_world_with_workspaces(
            "stripe",
            {
                "webclone/stripe/code": "abc123:step.1.stage.build",
                "webclone/stripe/recordings": "def456:step.1.stage.annotate",
            },
        )

        # Mock _download_state to return None (no DB state)
        world._download_state = AsyncMock(return_value=None)

        # Mock workspace.restore to return True
        for ws in world._workspaces.values():
            ws.restore = AsyncMock(return_value=True)
            ws._record_workspace_ref = AsyncMock()

        result = await world.load_state()
        assert result is True

        # Both workspaces should have had restore called
        world._workspaces["code"].restore.assert_called_once_with("step.1.stage.build")
        world._workspaces["recordings"].restore.assert_called_once_with("step.1.stage.annotate")

    @pytest.mark.asyncio
    async def test_short_field_name_keys_raise_error(self):
        """Config with short field names (code) should raise an error."""
        world = self._make_world_with_workspaces(
            "stripe",
            {
                "code": "abc123:step.1.stage.build",
            },
        )

        world._download_state = AsyncMock(return_value=None)

        with pytest.raises(RuntimeError, match="Unknown workspace repo name 'code'"):
            await world.load_state()

    @pytest.mark.asyncio
    async def test_unmatched_full_name_raises_error(self):
        """A key that doesn't match any repo name should raise an error."""
        world = self._make_world_with_workspaces(
            "stripe",
            {
                "webclone/hubspot/code": "abc123:step.1.stage.build",  # wrong clone
            },
        )

        world._download_state = AsyncMock(return_value=None)

        with pytest.raises(RuntimeError, match="Unknown workspace repo name 'webclone/hubspot/code'"):
            await world.load_state()

    @pytest.mark.asyncio
    async def test_default_world_with_full_repo_name(self):
        """SimpleWorld (no override) should also accept full repo names."""
        config = SimpleConfig()
        config.state.workspaces = {"simple/output": "abc123:step.1"}

        world = SimpleWorld.__new__(SimpleWorld)
        world.config = config
        world.logger = MagicMock()
        world._state = None
        world.session = MagicMock()
        world.session.session_id = "current"

        ws = MagicMock()
        ws.tracked = True
        ws.session_id = "current"
        ws.repo_name = "simple/output"
        ws.repo_id = "repo-id"
        ws.s3_bucket = "bucket"
        ws.s3_prefix = "prefix"
        ws._sts_credentials = {}
        ws._sts_expires_at = 0
        ws.restore = AsyncMock(return_value=True)
        ws._record_workspace_ref = AsyncMock()
        world._workspaces = {"output": ws}

        world._download_state = AsyncMock(return_value=None)

        result = await world.load_state()
        assert result is True
        ws.restore.assert_called_once_with("step.1")
