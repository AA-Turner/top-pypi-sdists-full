"""Tests for WorkspaceSourceSpec and backward-compatible state.workspaces parsing."""

from plato.worlds.config import StateConfig, WorkspaceSourceSpec


class TestWorkspaceSourceSpec:
    """Test the WorkspaceSourceSpec model."""

    def test_create_from_kwargs(self):
        spec = WorkspaceSourceSpec(repo="webclone/stripe/code", ref="abc123:step.1")
        assert spec.repo == "webclone/stripe/code"
        assert spec.ref == "abc123:step.1"

    def test_create_from_dict(self):
        spec = WorkspaceSourceSpec(**{"repo": "webclone/stripe/code", "ref": "abc123:step.1"})
        assert spec.repo == "webclone/stripe/code"
        assert spec.ref == "abc123:step.1"


class TestStateConfigWorkspacesBackwardCompat:
    """Ensure state.workspaces accepts both old string and new object formats."""

    def test_string_values_still_work(self):
        """Legacy format: {repo_or_field: 'session:step'} as plain strings."""
        cfg = StateConfig(
            workspaces={
                "code": "dabae6b6-1234:step.1.stage.builder",
                "recordings": "dabae6b6-1234:step.1.stage.builder",
            }
        )
        assert isinstance(cfg.workspaces["code"], str)
        assert cfg.workspaces["code"] == "dabae6b6-1234:step.1.stage.builder"

    def test_object_values_work(self):
        """New format: {field: WorkspaceSourceSpec}."""
        cfg = StateConfig(
            workspaces={
                "code": WorkspaceSourceSpec(
                    repo="webclone/stripe/code",
                    ref="dabae6b6-1234:step.1.stage.builder",
                ),
            }
        )
        spec = cfg.workspaces["code"]
        assert isinstance(spec, WorkspaceSourceSpec)
        assert spec.repo == "webclone/stripe/code"

    def test_mixed_string_and_object(self):
        """Mix of legacy strings and new objects in the same config."""
        cfg = StateConfig(
            workspaces={
                "code": WorkspaceSourceSpec(
                    repo="webclone/stripe/code",
                    ref="dabae6b6-1234:step.1",
                ),
                "recordings": "dabae6b6-1234:step.1",
            }
        )
        assert isinstance(cfg.workspaces["code"], WorkspaceSourceSpec)
        assert isinstance(cfg.workspaces["recordings"], str)

    def test_json_round_trip_string(self):
        """String values survive JSON serialization/deserialization."""
        cfg = StateConfig(workspaces={"code": "sess:step"})
        data = cfg.model_dump()
        restored = StateConfig.model_validate(data)
        assert restored.workspaces["code"] == "sess:step"

    def test_json_round_trip_object(self):
        """Object values survive JSON serialization/deserialization."""
        cfg = StateConfig(
            workspaces={
                "code": WorkspaceSourceSpec(repo="a/b/c", ref="sess:step"),
            }
        )
        data = cfg.model_dump()
        restored = StateConfig.model_validate(data)
        spec = restored.workspaces["code"]
        assert isinstance(spec, WorkspaceSourceSpec)
        assert spec.repo == "a/b/c"
        assert spec.ref == "sess:step"

    def test_from_raw_dict_json(self):
        """Parsing from raw JSON (as Chronos would send) produces correct types."""
        raw = {
            "workspaces": {
                "code": {"repo": "webclone/stripe/code", "ref": "abc:step.1"},
                "recordings": "abc:step.1",
            }
        }
        cfg = StateConfig.model_validate(raw)
        assert isinstance(cfg.workspaces["code"], WorkspaceSourceSpec)
        assert isinstance(cfg.workspaces["recordings"], str)

    def test_empty_workspaces_default(self):
        """Default is empty dict."""
        cfg = StateConfig()
        assert cfg.workspaces == {}
