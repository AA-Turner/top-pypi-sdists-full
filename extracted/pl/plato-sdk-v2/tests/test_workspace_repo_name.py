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
    async def test_resume_forwards_dvc_files_to_input_ref(self):
        """When resuming from another session, dvc_files from the restored ref must be forwarded."""
        world = self._make_world_with_workspaces(
            "stripe",
            {"webclone/stripe/recordings": "source-session:step.1.stage.ingest_recordings"},
        )
        world._download_state = AsyncMock(return_value=None)

        fake_dvc_files = {"recordings": "outs:\n- md5: abc123\n  path: recordings\n"}

        ws = world._workspaces["recordings"]

        # Simulate restore setting _last_restored_dvc_files (as the real Workspace does)
        async def fake_restore(step_name):
            ws._last_restored_dvc_files = fake_dvc_files
            ws._last_restored_source_ref_public_id = ""
            return True

        ws.restore = AsyncMock(side_effect=fake_restore)
        ws._record_workspace_ref = AsyncMock()

        result = await world.load_state()
        assert result is True

        # The input ref must carry the dvc_files, not an empty dict
        ws._record_workspace_ref.assert_called_once()
        call_args = ws._record_workspace_ref.call_args
        recorded_dvc_files = call_args[0][2]  # 3rd positional arg
        assert recorded_dvc_files == fake_dvc_files, f"Expected dvc_files to be forwarded but got: {recorded_dvc_files}"

    @pytest.mark.asyncio
    async def test_short_field_name_keys_are_accepted_as_legacy_aliases(self):
        """Legacy short field names should still restore tracked workspaces."""
        world = self._make_world_with_workspaces(
            "stripe",
            {
                "code": "abc123:step.1.stage.build",
            },
        )

        world._download_state = AsyncMock(return_value=None)
        world._workspaces["code"].restore = AsyncMock(return_value=True)
        world._workspaces["code"]._record_workspace_ref = AsyncMock()

        result = await world.load_state()

        assert result is True
        world._workspaces["code"].restore.assert_called_once_with("step.1.stage.build")
        world.logger.warning.assert_not_called()

    @pytest.mark.asyncio
    async def test_unmatched_full_name_warns_and_is_ignored(self):
        """A key that doesn't match any repo name should warn and be ignored."""
        world = self._make_world_with_workspaces(
            "stripe",
            {
                "webclone/hubspot/code": "abc123:step.1.stage.build",  # wrong clone
            },
        )

        world._download_state = AsyncMock(return_value=None)

        result = await world.load_state()

        assert result is False
        world.logger.warning.assert_called_once_with(
            "Ignoring unknown workspace key '%s' in state.workspaces. Expected one of: %s",
            "webclone/hubspot/code",
            ["webclone/stripe/code", "webclone/stripe/recordings", "code", "recordings"],
        )

    @pytest.mark.asyncio
    async def test_unknown_workspace_specs_do_not_block_valid_ones(self):
        """Unknown repo names should not prevent matched workspace restores."""
        world = self._make_world_with_workspaces(
            "stripe",
            {
                "webclone/stripe/code": "abc123:step.1.stage.build",
                "webclone/hubspot/code": "def456:step.9.stage.build",
            },
        )

        world._download_state = AsyncMock(return_value=None)

        world._workspaces["code"].restore = AsyncMock(return_value=True)
        world._workspaces["code"]._record_workspace_ref = AsyncMock()
        world._workspaces["recordings"].restore = AsyncMock(return_value=True)
        world._workspaces["recordings"]._record_workspace_ref = AsyncMock()

        result = await world.load_state()

        assert result is True
        world._workspaces["code"].restore.assert_called_once_with("step.1.stage.build")
        world._workspaces["recordings"].restore.assert_not_called()
        world.logger.warning.assert_called_once_with(
            "Ignoring unknown workspace key '%s' in state.workspaces. Expected one of: %s",
            "webclone/hubspot/code",
            ["webclone/stripe/code", "webclone/stripe/recordings", "code", "recordings"],
        )

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
