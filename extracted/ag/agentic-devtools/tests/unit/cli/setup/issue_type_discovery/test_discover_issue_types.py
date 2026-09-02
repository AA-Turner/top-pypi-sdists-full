"""Tests for discover_issue_types in issue_type_discovery."""

from __future__ import annotations

import json
from collections.abc import Generator
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.adapters.base import IssueTypeInfo
from agentic_devtools.cli.setup.issue_type_discovery import discover_issue_types


@pytest.fixture(autouse=True)
def _mock_provider_connectivity() -> Generator[None, None, None]:
    """Default all discovery tests to a healthy provider unless they opt out."""
    with patch(
        "agentic_devtools.cli.setup.issue_type_discovery.check_provider_connectivity", return_value=(True, None)
    ):
        yield


def _write_platform_config(git_root: Path, config: dict) -> None:
    """Write .github/agdt-config.json with given platform config."""
    config_dir = git_root / ".github"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "agdt-config.json"
    config_file.write_text(json.dumps({"platform": config}), encoding="utf-8")


def _write_project_config(git_root: Path, config: dict) -> None:
    """Write .agdt/config/project.json."""
    config_dir = git_root / ".agdt" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "project.json"
    config_file.write_text(json.dumps(config, indent=2), encoding="utf-8")


def _read_project_config(git_root: Path) -> dict:
    """Read .agdt/config/project.json."""
    config_file = git_root / ".agdt" / "config" / "project.json"
    if not config_file.exists():
        return {}
    return json.loads(config_file.read_text(encoding="utf-8"))


class TestDiscoverIssueTypesHappyPath:
    """Tests for discover_issue_types happy-path scenarios."""

    def test_jira_adapter_discovers_types(self, tmp_path: Path) -> None:
        """Jira adapter returns types → persisted correctly with timestamps."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description="A defect"),
            IssueTypeInfo(name="Story", description="A user story"),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" in cfg
        entry = cfg["issue_types_metadata"]["PROJ"]
        assert entry["provider"] == "jira"
        assert entry["lastDiscovered"] == "2026-07-20T12:00:00+00:00"
        assert entry["lastRefreshed"] == "2026-07-20T12:00:00+00:00"
        assert len(entry["issue_types"]) == 2
        assert entry["issue_types"][0]["name"] == "Bug"
        assert entry["issue_types"][1]["name"] == "Story"

    def test_github_adapter_discovers_types(self, tmp_path: Path) -> None:
        """GitHub adapter returns types with correct project identifier."""
        _write_platform_config(
            tmp_path,
            {"issue_adapter": "github", "github": {"repo_owner": "org", "repo_name": "repo"}},
        )
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="bug", description="Bug report"),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "github", "github": {"repo_owner": "org", "repo_name": "repo"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        entry = cfg["issue_types_metadata"]["org/repo"]
        assert entry["provider"] == "github"
        assert len(entry["issue_types"]) == 1
        assert entry["issue_types"][0]["name"] == "bug"

    def test_empty_list_persisted_with_timestamp(self, tmp_path: Path) -> None:
        """Provider returns empty list → persisted as empty list with valid timestamp."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "EMPTY"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = []

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "EMPTY"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        entry = cfg["issue_types_metadata"]["EMPTY"]
        assert entry["issue_types"] == []
        assert entry["lastDiscovered"] == "2026-07-20T12:00:00+00:00"

    def test_blank_name_skipped_in_mapping(self, tmp_path: Path) -> None:
        """IssueTypeInfo with blank name is skipped."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="", description="blank"),
            IssueTypeInfo(name="Valid", description="ok"),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        entry = cfg["issue_types_metadata"]["PROJ"]
        assert len(entry["issue_types"]) == 1
        assert entry["issue_types"][0]["name"] == "Valid"


class TestDiscoverIssueTypesConnectivityGuard:
    """Tests for provider reachability gating before discovery."""

    def test_provider_unreachable_skips_discovery_and_keeps_cache(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An unreachable provider warns and leaves project.json untouched."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        existing_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2025-01-01T00:00:00+00:00",
                    "lastRefreshed": "2025-01-01T00:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [
                        {"id": "Legacy", "name": "Legacy", "description": "", "is_subtask": False, "properties": []}
                    ],
                }
            }
        }
        _write_project_config(tmp_path, existing_config)
        mock_adapter = MagicMock()

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.cli.setup.issue_type_discovery.check_provider_connectivity",
                return_value=(False, "offline"),
            ),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True)

        captured = capsys.readouterr()
        assert outcome.status == "failed"
        assert outcome.reason == "provider_unreachable"
        assert outcome.error is not None
        assert "offline" in outcome.error
        assert "Issue type discovery skipped" in captured.err
        mock_adapter.get_issue_types.assert_not_called()
        assert _read_project_config(tmp_path) == existing_config

    def test_reuses_preflight_connectivity_result_when_provided(self, tmp_path: Path) -> None:
        """A caller-provided preflight result skips a second connectivity probe."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="A defect")]

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.check_provider_connectivity") as mock_check,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(
                tmp_path,
                force_refresh=True,
                preflight_connectivity=(True, None),
            )

        assert outcome.status == "success"
        mock_check.assert_not_called()
        mock_adapter.get_issue_types.assert_called_once()

    def test_suppresses_duplicate_warning_when_preflight_already_warned(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """If setup already warned for unreachable provider, discovery does not warn again."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(
                tmp_path,
                force_refresh=True,
                preflight_connectivity=(False, "offline"),
                preflight_warning_emitted=True,
            )

        captured = capsys.readouterr()
        assert outcome.status == "failed"
        assert outcome.reason == "provider_unreachable"
        assert captured.err == ""
        mock_adapter.get_issue_types.assert_not_called()


class TestDiscoverIssueTypesCacheSkip:
    """Tests for cache-hit skip behavior."""

    def test_cache_exists_no_force_skips(self, tmp_path: Path) -> None:
        """Cache already exists and no force_refresh → skip discovery, no API call."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        existing_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2025-01-01T00:00:00+00:00",
                    "lastRefreshed": "2025-01-01T00:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [],
                }
            }
        }
        _write_project_config(tmp_path, existing_config)
        mock_adapter = MagicMock()

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        mock_adapter.get_issue_types.assert_not_called()

    def test_invalid_cached_entry_no_force_rediscovers(self, tmp_path: Path) -> None:
        """Invalid cache entry is treated as cache miss and re-discovered."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        existing_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2025-01-01T00:00:00+00:00",
                    # invalid: missing lastRefreshed/provider/issue_types
                }
            }
        }
        _write_project_config(tmp_path, existing_config)
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description=""),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        mock_adapter.get_issue_types.assert_called_once()
        cfg = _read_project_config(tmp_path)
        entry = cfg["issue_types_metadata"]["PROJ"]
        assert entry["provider"] == "jira"
        assert entry["lastDiscovered"] == "2026-07-20T12:00:00+00:00"
        assert entry["lastRefreshed"] == "2026-07-20T12:00:00+00:00"
        assert len(entry["issue_types"]) == 1

    def test_force_refresh_calls_adapter(self, tmp_path: Path) -> None:
        """force_refresh=True → calls get_issue_types(), overwrites cache."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        existing_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2025-01-01T00:00:00+00:00",
                    "lastRefreshed": "2025-01-01T00:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [],
                }
            }
        }
        _write_project_config(tmp_path, existing_config)
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="NewType", description="new"),
        ]

        frozen = datetime(2026, 7, 20, 14, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path, force_refresh=True)

        mock_adapter.get_issue_types.assert_called_once()
        cfg = _read_project_config(tmp_path)
        entry = cfg["issue_types_metadata"]["PROJ"]
        assert entry["lastDiscovered"] == "2025-01-01T00:00:00+00:00"
        assert entry["lastRefreshed"] == "2026-07-20T14:00:00+00:00"
        assert len(entry["issue_types"]) == 1
        assert entry["issue_types"][0]["name"] == "NewType"


class TestDiscoverIssueTypesGracefulDegradation:
    """Tests for graceful failure handling."""

    def test_connection_error_warns_stderr(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """ConnectionError → stderr warning, no cache written."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = ConnectionError("Connection refused")

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "ConnectionError" in captured.err
        assert "Connection refused" in captured.err
        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" not in cfg

    def test_http_403_mentions_permissions(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """HTTP 403 error → warning mentions permissions."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = RuntimeError("HTTP 403 Forbidden")

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "permissions or authorization" in captured.err

    def test_non_http_number_does_not_trigger_permissions_hint(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Non-HTTP numeric text does not trigger the permissions hint."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = RuntimeError("Record 1403 could not be loaded")

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "Record 1403 could not be loaded" in captured.err
        assert "permissions or authorization" not in captured.err

    def test_not_implemented_error_silent_skip(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """NotImplementedError → debug log only, no user warning."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = NotImplementedError("not supported")

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert captured.err == ""
        assert captured.out == ""

    def test_existing_cache_preserved_on_failure(self, tmp_path: Path) -> None:
        """Existing cache preserved unchanged when discovery fails."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        existing_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2025-01-01T00:00:00+00:00",
                    "lastRefreshed": "2025-01-01T00:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [
                        {"id": "Bug", "name": "Bug", "description": "", "is_subtask": False, "properties": []}
                    ],
                }
            }
        }
        _write_project_config(tmp_path, existing_config)
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = ConnectionError("timeout")

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path, force_refresh=True)

        cfg = _read_project_config(tmp_path)
        # Cache should be unchanged
        assert cfg == existing_config

    def test_validation_failure_skips_persist(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """validate_issue_types_metadata() failure → stderr warning, data not persisted."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description="ok"),
        ]

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch(
                "agentic_devtools.cli.setup.issue_type_discovery.validate_issue_types_metadata",
                side_effect=ValueError("invalid metadata"),
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "validation failed" in captured.err
        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" not in cfg


class TestDiscoverIssueTypesSkipPlatformDetection:
    """Tests for --skip-platform-detection behavior."""

    def test_skip_platform_detection_no_call(self, tmp_path: Path) -> None:
        """skip_platform_detection=True → no get_issue_types() call."""
        mock_adapter = MagicMock()

        with patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter):
            discover_issue_types(tmp_path, skip_platform_detection=True)

        mock_adapter.get_issue_types.assert_not_called()

    def test_skip_platform_detection_preserves_cache(self, tmp_path: Path) -> None:
        """Existing cache unchanged when --skip-platform-detection is active."""
        existing_config = {
            "issue_types_metadata": {
                "PROJ": {
                    "lastDiscovered": "2025-01-01T00:00:00+00:00",
                    "lastRefreshed": "2025-01-01T00:00:00+00:00",
                    "provider": "jira",
                    "issue_types": [],
                }
            }
        }
        _write_project_config(tmp_path, existing_config)

        discover_issue_types(tmp_path, skip_platform_detection=True)

        cfg = _read_project_config(tmp_path)
        assert cfg == existing_config

    def test_skip_platform_detection_with_force_refresh(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """skip_platform_detection + force_refresh → skip with no warning."""
        mock_adapter = MagicMock()

        with patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter):
            discover_issue_types(tmp_path, skip_platform_detection=True, force_refresh=True)

        mock_adapter.get_issue_types.assert_not_called()
        captured = capsys.readouterr()
        assert captured.err == ""


class TestDiscoverIssueTypesEdgeCases:
    """Tests for edge cases in discover_issue_types."""

    def test_unresolvable_project_identifier_skips(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Unresolvable project identifier → silent skip."""
        with patch(
            "agentic_devtools.config.load_platform_config",
            return_value={"issue_adapter": "unknown"},
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert captured.err == ""
        assert captured.out == ""

    def test_corrupted_project_json_overwritten(self, tmp_path: Path) -> None:
        """Corrupted project.json (invalid JSON) → overwritten on discovery."""
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "project.json").write_text("not json {{{", encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description="defect"),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" in cfg
        assert "PROJ" in cfg["issue_types_metadata"]

    def test_project_json_not_dict_overwritten(self, tmp_path: Path) -> None:
        """project.json with non-dict content → overwritten on discovery."""
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "project.json").write_text("[1, 2, 3]", encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Story", description=""),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" in cfg

    def test_issue_types_metadata_not_dict_overwritten(self, tmp_path: Path) -> None:
        """project.json with non-dict issue_types_metadata → key reset and discovery persisted."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        # Corrupt the issue_types_metadata key so it holds a non-dict value
        _write_project_config(tmp_path, {"issue_types_metadata": "corrupted-string"})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description=""),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        cfg = _read_project_config(tmp_path)
        assert isinstance(cfg["issue_types_metadata"], dict)
        assert "PROJ" in cfg["issue_types_metadata"]

    def test_file_lock_failure_warns_stderr(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """File lock failure → stderr warning, no crash."""
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description=""),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=OSError("Permission denied"),
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "failed to persist" in captured.err

    def test_cache_entry_not_dict_treated_as_no_existing(self, tmp_path: Path) -> None:
        """Cache entry that is not a dict → treated as first discovery (existing=None)."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        existing_config = {"issue_types_metadata": {"PROJ": "not-a-dict"}}
        _write_project_config(tmp_path, existing_config)
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [
            IssueTypeInfo(name="Bug", description=""),
        ]

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            discover_issue_types(tmp_path, force_refresh=True)

        cfg = _read_project_config(tmp_path)
        entry = cfg["issue_types_metadata"]["PROJ"]
        # Both timestamps should be set (no existing to preserve)
        assert entry["lastDiscovered"] == "2026-07-20T12:00:00+00:00"
        assert entry["lastRefreshed"] == "2026-07-20T12:00:00+00:00"

    def test_none_raw_types_warns_and_skips_persist(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Adapter returning None for get_issue_types() → TypeError caught, warning, no persist."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = None  # not iterable

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "failed to map results" in captured.err
        assert "TypeError" in captured.err
        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" not in cfg

    def test_non_iterable_raw_types_warns_and_skips_persist(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Adapter returning a non-iterable (int) → TypeError caught, warning, no persist."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = 42  # not iterable

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            discover_issue_types(tmp_path)

        captured = capsys.readouterr()
        assert "failed to map results" in captured.err
        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" not in cfg


class TestDiscoverIssueTypesRefreshOutcome:
    """Tests for the structured RefreshOutcome return contract."""

    def test_happy_path_returns_success(self, tmp_path: Path) -> None:
        """Successful discovery returns RefreshOutcome.success()."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path)

        assert outcome.status == "success"
        assert outcome.reason is None
        assert outcome.error is None

    def test_skip_platform_detection_returns_skipped(self, tmp_path: Path) -> None:
        """--skip-platform-detection short-circuit returns skipped taxonomy reason."""
        outcome = discover_issue_types(tmp_path, skip_platform_detection=True)
        assert outcome.status == "skipped"
        assert outcome.reason == "skip_platform_detection"
        assert outcome.error is None

    def test_unresolvable_identifier_returns_unsupported(self, tmp_path: Path) -> None:
        """Unresolvable project identifier returns issue_type_discovery_unsupported."""
        with patch(
            "agentic_devtools.config.load_platform_config",
            return_value={"issue_adapter": "unknown"},
        ):
            outcome = discover_issue_types(tmp_path)
        assert outcome.status == "skipped"
        assert outcome.reason == "issue_type_discovery_unsupported"

    def test_cache_valid_no_force_returns_success(self, tmp_path: Path) -> None:
        """Valid cache without force_refresh returns success (nothing to do)."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        _write_project_config(
            tmp_path,
            {
                "issue_types_metadata": {
                    "PROJ": {
                        "lastDiscovered": "2025-01-01T00:00:00+00:00",
                        "lastRefreshed": "2025-01-01T00:00:00+00:00",
                        "provider": "jira",
                        "issue_types": [],
                    }
                }
            },
        )
        mock_adapter = MagicMock()
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path)
        assert outcome.status == "success"

    def test_not_implemented_returns_unsupported(self, tmp_path: Path) -> None:
        """Adapter without get_issue_types() returns issue_type_discovery_unsupported."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = NotImplementedError("nope")
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path)
        assert outcome.status == "skipped"
        assert outcome.reason == "issue_type_discovery_unsupported"

    def test_provider_unreachable_returns_failed(self, tmp_path: Path) -> None:
        """get_issue_types() raising returns failed/provider_unreachable with error."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.side_effect = ConnectionError("timeout")
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True)
        assert outcome.status == "failed"
        assert outcome.reason == "provider_unreachable"
        assert outcome.error is not None
        assert "timeout" in outcome.error

    def test_mapping_error_returns_failed(self, tmp_path: Path) -> None:
        """Non-iterable get_issue_types() result returns failed/mapping_error."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = 42  # not iterable
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path)
        assert outcome.status == "failed"
        assert outcome.reason == "mapping_error"
        assert outcome.error is not None

    def test_validation_error_returns_failed(self, tmp_path: Path) -> None:
        """Metadata validation failure returns failed/validation_error."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch(
                "agentic_devtools.cli.setup.issue_type_discovery.validate_issue_types_metadata",
                side_effect=ValueError("bad"),
            ),
        ):
            outcome = discover_issue_types(tmp_path)
        assert outcome.status == "failed"
        assert outcome.reason == "validation_error"
        assert outcome.error is not None

    def test_persist_error_returns_failed(self, tmp_path: Path) -> None:
        """A locked_file failure returns failed/persist_error."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch(
                "agentic_devtools.file_locking.locked_file",
                side_effect=OSError("Permission denied"),
            ),
        ):
            outcome = discover_issue_types(tmp_path)
        assert outcome.status == "failed"
        assert outcome.reason == "persist_error"
        assert outcome.error is not None

    def test_standalone_all_property_fetches_fail_no_write(self, tmp_path: Path) -> None:
        """standalone=True with all property fetches failing → failed, no project.json write."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.side_effect = RuntimeError("Server down")
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)
        assert outcome.status == "failed"
        assert outcome.reason == "property_fetch_failed"
        assert outcome.error is not None
        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" not in cfg

    def test_standalone_empty_issue_type_list_no_write(self, tmp_path: Path) -> None:
        """standalone=True with zero types returned leaves project.json unchanged."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        original = json.dumps({"unrelated": "value"})
        (config_dir / "project.json").write_text(original, encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = []
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "failed"
        assert outcome.reason == "property_fetch_failed"
        assert (
            outcome.error == "Provider returned no issue types, so no property discovery call completed successfully; "
            "project.json left unchanged."
        )
        assert (config_dir / "project.json").read_text(encoding="utf-8") == original

    def test_standalone_not_implemented_property_discovery_no_write(self, tmp_path: Path) -> None:
        """standalone=True with zero successful property calls leaves project.json unchanged."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        original = json.dumps({"unrelated": "value"})
        (config_dir / "project.json").write_text(original, encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.side_effect = NotImplementedError("not supported")
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "failed"
        assert outcome.reason == "property_fetch_failed"
        assert outcome.error == "No property discovery call completed successfully; project.json left unchanged."
        assert (config_dir / "project.json").read_text(encoding="utf-8") == original

    def test_non_standalone_all_property_fetches_fail_still_writes(self, tmp_path: Path) -> None:
        """standalone=False keeps legacy behavior: writes preserved metadata on all-fail."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.side_effect = RuntimeError("Server down")
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True)
        assert outcome.status == "success"
        cfg = _read_project_config(tmp_path)
        assert "issue_types_metadata" in cfg

    def test_standalone_malformed_project_json_not_overwritten(self, tmp_path: Path) -> None:
        """standalone=True leaves a malformed project.json byte-for-byte unchanged."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        original = "not json {{{"
        (config_dir / "project.json").write_text(original, encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.return_value = []
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "failed"
        assert outcome.reason == "malformed_project_json"
        assert outcome.error is not None
        assert (config_dir / "project.json").read_text(encoding="utf-8") == original

    def test_standalone_initial_discovery_missing_metadata_key(self, tmp_path: Path) -> None:
        """standalone=True with no issue_types_metadata key → initial discovery, both timestamps set."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        _write_project_config(tmp_path, {"unrelated": "value"})
        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.return_value = []

        frozen = datetime(2026, 7, 20, 12, 0, 0, tzinfo=timezone.utc)
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch("agentic_devtools.cli.setup.issue_type_discovery.datetime") as mock_dt,
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            mock_dt.now.return_value = frozen
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "success"
        cfg = _read_project_config(tmp_path)
        assert cfg["unrelated"] == "value"  # unrelated config preserved
        entry = cfg["issue_types_metadata"]["PROJ"]
        assert entry["lastDiscovered"] == "2026-07-20T12:00:00+00:00"
        assert entry["lastRefreshed"] == "2026-07-20T12:00:00+00:00"

    def test_standalone_atomic_write_preserves_file_on_tmp_write_error(self, tmp_path: Path) -> None:
        """standalone=True: if mkstemp raises the original project.json is left unchanged."""
        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        original = json.dumps({"unrelated": "value"})
        (config_dir / "project.json").write_text(original, encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.return_value = []

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch(
                "agentic_devtools.cli.setup.issue_type_discovery.tempfile.mkstemp",
                side_effect=OSError("simulated disk full"),
            ),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "failed"
        assert outcome.reason == "persist_error"
        # Original file must be untouched
        assert (config_dir / "project.json").read_text(encoding="utf-8") == original

    def test_standalone_atomic_write_cleans_up_tmp_on_replace_failure(self, tmp_path: Path) -> None:
        """standalone=True: if os.replace fails the temp file is cleaned up and failed outcome returned."""
        import agentic_devtools.cli.setup.issue_type_discovery as _mod

        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        original = json.dumps({"unrelated": "value"})
        (config_dir / "project.json").write_text(original, encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.return_value = []

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch.object(_mod.os, "replace", side_effect=OSError("simulated replace failure")),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "failed"
        assert outcome.reason == "persist_error"
        # Original file must be untouched
        assert (config_dir / "project.json").read_text(encoding="utf-8") == original
        # No temp files left behind
        assert not any(config_dir.glob(".project_json_*.tmp"))

    def test_standalone_atomic_write_replace_and_unlink_both_fail(self, tmp_path: Path) -> None:
        """If both os.replace and os.unlink fail, persist_error is still returned (no crash)."""
        import agentic_devtools.cli.setup.issue_type_discovery as _mod

        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        config_dir = tmp_path / ".agdt" / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        original = json.dumps({"unrelated": "value"})
        (config_dir / "project.json").write_text(original, encoding="utf-8")

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.return_value = []

        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
            patch.object(_mod.os, "replace", side_effect=OSError("replace failed")),
            patch.object(_mod.os, "unlink", side_effect=OSError("unlink also failed")),
        ):
            outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)

        assert outcome.status == "failed"
        assert outcome.reason == "persist_error"
        assert (config_dir / "project.json").read_text(encoding="utf-8") == original


class TestDiscoverIssueTypesConcurrentRefresh:
    """Concurrent standalone-refresh contention (FR-005).

    The persistence path takes a stable sidecar lock (``project.json.lock``)
    around the read + atomic ``os.replace()`` so overlapping refreshes are
    serialized and cannot lose updates or corrupt the file.
    """

    def test_concurrent_refreshes_serialize_and_preserve_config(self, tmp_path: Path) -> None:
        """Two barrier-synced refreshes leave valid JSON with unrelated config intact."""
        import threading

        _write_platform_config(tmp_path, {"issue_adapter": "jira", "jira": {"project_key": "PROJ"}})
        # Pre-seed with unrelated config that must survive both writes.
        _write_project_config(tmp_path, {"unrelated": "keep-me"})

        mock_adapter = MagicMock()
        mock_adapter.get_issue_types.return_value = [IssueTypeInfo(name="Bug", description="")]
        mock_adapter.get_type_properties.return_value = []

        barrier = threading.Barrier(2)
        results_lock = threading.Lock()
        outcomes: list[object] = []
        errors: list[BaseException] = []

        def _refresh() -> None:
            try:
                barrier.wait()  # maximize contention: both enter persist near-simultaneously
                outcome = discover_issue_types(tmp_path, force_refresh=True, standalone=True)
                with results_lock:
                    outcomes.append(outcome)
            except BaseException as exc:  # noqa: BLE001 - surface thread failures to the test
                with results_lock:
                    errors.append(exc)

        # Apply patches once in the main thread so both workers observe a stable
        # module state (``patch`` mutates globals and is not thread-safe when
        # entered/exited concurrently from multiple threads).
        with (
            patch("agentic_devtools.adapters.get_adapter", return_value=mock_adapter),
            patch(
                "agentic_devtools.config.load_platform_config",
                return_value={"issue_adapter": "jira", "jira": {"project_key": "PROJ"}},
            ),
        ):
            threads = [threading.Thread(target=_refresh) for _ in range(2)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=30)

        assert not errors, f"refresh threads raised: {errors}"
        assert all(not t.is_alive() for t in threads)
        assert [getattr(o, "status", None) for o in outcomes] == ["success", "success"]

        # File is valid JSON, unrelated config preserved, and the metadata is intact.
        cfg = _read_project_config(tmp_path)
        assert cfg["unrelated"] == "keep-me"
        entry = cfg["issue_types_metadata"]["PROJ"]
        assert entry["provider"] == "jira"
        assert [t["name"] for t in entry["issue_types"]] == ["Bug"]
