"""Tests for plato pm experiment commands and helpers."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from plato.cli.pm import (
    _EXPERIMENT_NAMES,
    _fetch_experiment_config,
    _find_templates_dir,
    _load_template,
    pm_app,
)

runner = CliRunner()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_experiment_file(name: str, config_json: dict, version: int = 1) -> dict:
    return {
        "public_id": f"file-{name}",
        "name": name,
        "description": f"desc for {name}",
        "latest_version": {
            "public_id": f"ver-{name}-{version}",
            "version_number": version,
            "config_json": config_json,
        },
        "versions": [],
    }


def _mock_experiments_response(*names_and_configs: tuple[str, dict]) -> dict:
    return {"files": [_make_experiment_file(name, cfg) for name, cfg in names_and_configs]}


# ---------------------------------------------------------------------------
# _find_templates_dir
# ---------------------------------------------------------------------------


class TestFindTemplatesDir:
    def test_points_to_cli_templates(self):
        d = _find_templates_dir()
        assert d.name == "templates"
        assert d.parent.name == "cli"

    def test_directory_exists(self):
        assert _find_templates_dir().is_dir()


# ---------------------------------------------------------------------------
# _load_template
# ---------------------------------------------------------------------------


class TestLoadTemplate:
    def test_loads_env_create(self):
        t = _load_template("env-create-launch.json")
        assert "world" in t
        assert t["world"]["package"] == "plato-world-structured-execution"

    def test_loads_env_fix(self):
        t = _load_template("env-fix-launch.json")
        assert t["world"]["package"] == "plato-world-structured-execution"
        steps = t["world"]["config"]["steps"]
        assert [s["name"] for s in steps] == ["fix", "audit_verify", "snapshot", "submit"]

    def test_loads_datagen(self):
        t = _load_template("datagen-launch.json")
        assert t["world"]["package"] == "plato-world-interactive"

    def test_raises_for_missing_template(self):
        with pytest.raises(FileNotFoundError):
            _load_template("nonexistent.json")

    def test_no_world_package_placeholder(self):
        """Templates must not contain the old {world_package} placeholder."""
        for name in ("env-create-launch.json", "env-fix-launch.json", "datagen-launch.json"):
            t = _load_template(name)
            assert t["world"]["package"] != "{world_package}"

    def test_env_create_has_10_steps(self):
        t = _load_template("env-create-launch.json")
        steps = t["world"]["config"]["steps"]
        assert len(steps) == 10
        assert steps[0]["name"] == "research"
        assert steps[-1]["name"] == "submit"


# ---------------------------------------------------------------------------
# _fetch_experiment_config
# ---------------------------------------------------------------------------


MOCK_ENV_CREATE_CONFIG = {
    "world": {"package": "plato-world-structured-execution", "config": {"steps": [{"name": "research"}]}},
    "tags": ["simcreator"],
}

MOCK_DATAGEN_CONFIG = {
    "world": {"package": "plato-world-interactive", "config": {"initial_messages": []}},
    "tags": ["datagen"],
}


class TestFetchExperimentConfig:
    @patch("plato.cli.pm.httpx.Client")
    def test_returns_config_for_matching_experiment(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = _mock_experiments_response(
            ("some-other-experiment", {"world": {}}),
            ("env-create-launch", MOCK_ENV_CREATE_CONFIG),
        )
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=MagicMock(get=MagicMock(return_value=resp)))
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        config, version_id = _fetch_experiment_config("env", "base", "test-key")
        assert config == MOCK_ENV_CREATE_CONFIG
        assert version_id == "ver-env-create-launch-1"

    @patch("plato.cli.pm.httpx.Client")
    def test_raises_on_api_error(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 401
        resp.text = "Unauthorized"
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=MagicMock(get=MagicMock(return_value=resp)))
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(Exception, match="401"):
            _fetch_experiment_config("env", "base", "bad-key")

    @patch("plato.cli.pm.httpx.Client")
    def test_raises_when_experiment_not_found(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = _mock_experiments_response(
            ("some-other-experiment", {}),
        )
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=MagicMock(get=MagicMock(return_value=resp)))
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(Exception, match="env-create-launch"):
            _fetch_experiment_config("env", "base", "test-key")

    @patch("plato.cli.pm.httpx.Client")
    def test_raises_for_unknown_pipeline_mode(self, mock_client_cls):
        with pytest.raises(ValueError, match="Unknown experiment"):
            _fetch_experiment_config("env", "unknown-mode", "test-key")

    @patch("plato.cli.pm.httpx.Client")
    def test_raises_when_config_json_missing(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "files": [
                {
                    "public_id": "file-1",
                    "name": "env-create-launch",
                    "description": "",
                    "latest_version": {
                        "public_id": "ver-1",
                        "version_number": 1,
                        "config_json": None,
                    },
                }
            ]
        }
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=MagicMock(get=MagicMock(return_value=resp)))
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(Exception, match="no config_json"):
            _fetch_experiment_config("env", "base", "test-key")

    @patch("plato.cli.pm.httpx.Client")
    def test_empty_config_json_is_valid(self, mock_client_cls):
        """An empty dict config_json should NOT raise — only None should raise."""
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = _mock_experiments_response(
            ("env-create-launch", {}),
        )
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=MagicMock(get=MagicMock(return_value=resp)))
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        config, version_id = _fetch_experiment_config("env", "base", "test-key")
        assert config == {}
        assert version_id == "ver-env-create-launch-1"

    @patch("plato.cli.pm.httpx.Client")
    def test_filters_by_name_not_first_result(self, mock_client_cls):
        """Should return the named experiment even if it's not first in the list."""
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = _mock_experiments_response(
            ("datagen-launch", MOCK_DATAGEN_CONFIG),
            ("env-create-launch", MOCK_ENV_CREATE_CONFIG),
        )
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=MagicMock(get=MagicMock(return_value=resp)))
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        config, version_id = _fetch_experiment_config("env", "base", "test-key")
        assert config["world"]["package"] == "plato-world-structured-execution"


# ---------------------------------------------------------------------------
# _EXPERIMENT_NAMES mapping
# ---------------------------------------------------------------------------


class TestExperimentNames:
    def test_all_three_mappings_exist(self):
        assert ("env", "base") in _EXPERIMENT_NAMES
        assert ("env", "resume") in _EXPERIMENT_NAMES
        assert ("data", "base") in _EXPERIMENT_NAMES

    def test_correct_names(self):
        assert _EXPERIMENT_NAMES[("env", "base")] == "env-create-launch"
        assert _EXPERIMENT_NAMES[("env", "resume")] == "env-fix-launch"
        assert _EXPERIMENT_NAMES[("data", "base")] == "datagen-launch"


# ---------------------------------------------------------------------------
# plato pm experiment ... push commands
# ---------------------------------------------------------------------------


def _make_http_mock(list_files: list[dict], create_resp: dict | None = None, version_resp: dict | None = None):
    """Build a mock httpx.Client that returns canned responses."""
    list_response = MagicMock()
    list_response.raise_for_status = MagicMock()
    list_response.json.return_value = {"files": list_files}

    patch_response = MagicMock()
    patch_response.raise_for_status = MagicMock()

    create_response = MagicMock()
    create_response.raise_for_status = MagicMock()
    create_response.json.return_value = create_resp or {"latest_version": {"version_number": 1}}

    version_response = MagicMock()
    version_response.raise_for_status = MagicMock()
    version_response.json.return_value = version_resp or {"latest_version": {"version_number": 2}}

    mock_client = MagicMock()
    mock_client.get.return_value = list_response
    mock_client.post.return_value = version_response
    mock_client.patch.return_value = patch_response

    # When no existing file, post returns create_response for file creation
    def _post_side_effect(url, **kwargs):
        if "/versions" in url:
            return version_response
        return create_response

    mock_client.post.side_effect = _post_side_effect
    return mock_client


class TestExperimentPushCommands:
    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_env_base_push_creates_when_not_exists(self, mock_client_cls):
        mock_client = _make_http_mock(list_files=[])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = runner.invoke(pm_app, ["experiment", "env", "base", "push"])

        assert result.exit_code == 0, result.output
        assert "Created" in result.output
        assert "env-create-launch" in result.output

        # Verify POST to /files (create) was called with correct name
        create_call = mock_client.post.call_args
        body = create_call.kwargs.get("json", {})
        assert body.get("name") == "env-create-launch"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_env_base_push_creates_new_version_when_exists(self, mock_client_cls):
        existing = _make_experiment_file("env-create-launch", {}, version=5)
        mock_client = _make_http_mock(
            list_files=[existing],
            version_resp={"latest_version": {"version_number": 6}},
        )
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = runner.invoke(pm_app, ["experiment", "env", "base", "push"])

        assert result.exit_code == 0, result.output
        assert "v6" in result.output

        # Verify POST to /files/{id}/versions was called
        version_call = mock_client.post.call_args
        assert "file-env-create-launch" in version_call.args[0]
        assert "versions" in version_call.args[0]

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_env_fix_push(self, mock_client_cls):
        mock_client = _make_http_mock(list_files=[])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = runner.invoke(pm_app, ["experiment", "env", "fix", "push"])

        assert result.exit_code == 0, result.output
        assert "env-fix-launch" in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_data_base_push(self, mock_client_cls):
        mock_client = _make_http_mock(list_files=[])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = runner.invoke(pm_app, ["experiment", "data", "base", "push"])

        assert result.exit_code == 0, result.output
        assert "datagen-launch" in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_push_patches_description_on_existing(self, mock_client_cls):
        existing = _make_experiment_file("env-create-launch", {}, version=3)
        mock_client = _make_http_mock(list_files=[existing])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        runner.invoke(pm_app, ["experiment", "env", "base", "push"])

        # PATCH should have been called on the file to update description
        mock_client.patch.assert_called_once()
        patch_url = mock_client.patch.call_args.args[0]
        assert "file-env-create-launch" in patch_url

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_pushed_config_has_correct_world_package_env(self, mock_client_cls):
        mock_client = _make_http_mock(list_files=[])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        runner.invoke(pm_app, ["experiment", "env", "base", "push"])

        create_call = mock_client.post.call_args
        body = create_call.kwargs.get("json", {})
        pkg = body.get("config_json", {}).get("world", {}).get("package")
        assert pkg == "plato-world-structured-execution"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_pushed_config_has_correct_world_package_data(self, mock_client_cls):
        mock_client = _make_http_mock(list_files=[])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        runner.invoke(pm_app, ["experiment", "data", "base", "push"])

        create_call = mock_client.post.call_args
        body = create_call.kwargs.get("json", {})
        pkg = body.get("config_json", {}).get("world", {}).get("package")
        assert pkg == "plato-world-interactive"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.httpx.Client")
    def test_push_uses_correct_world_key_per_pipeline(self, mock_client_cls):
        """world_key must vary: structured-execution for env, interactive for data."""
        mock_client = _make_http_mock(list_files=[])
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        # env base → structured-execution
        runner.invoke(pm_app, ["experiment", "env", "base", "push"])
        body = mock_client.post.call_args.kwargs.get("json", {})
        assert body.get("world_key") == "structured-execution"

        # data base → interactive
        runner.invoke(pm_app, ["experiment", "data", "base", "push"])
        body = mock_client.post.call_args.kwargs.get("json", {})
        assert body.get("world_key") == "interactive"
