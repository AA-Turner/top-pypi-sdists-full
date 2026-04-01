"""Tests for plato pm core helpers and CLI commands."""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from typer.testing import CliRunner

from plato.cli.pm import (
    _get_last_chronos_session,
    _launch_datagen_world,
    _launch_env_world,
    _launch_on_chronos,
    pm_app,
)

runner = CliRunner()

# ---------------------------------------------------------------------------
# Shared fixtures / helpers
# ---------------------------------------------------------------------------

MOCK_ENV_BASE_CONFIG = {
    "world": {
        "package": "plato-world-structured-execution",
        "config": {
            "sim_name": "",
            "github_url": "",
            "plato_api_key": "",
            "anthropic_api_key": "",
            "skill_runner": {
                "package": "claude-code",
                "config": {
                    "plato_api_key": "",
                    "anthropic_api_key": "",
                },
            },
            "steps": [{"name": "research"}],
            "state": {"enabled": True, "resume_from": ""},
        },
    },
    "tags": ["simcreator"],
}

MOCK_ENV_RESUME_CONFIG = {
    "world": {
        "package": "plato-world-structured-execution",
        "config": {
            "sim_name": "",
            "artifact_id": "",
            "feedback": "",
            "plato_api_key": "",
            "anthropic_api_key": "",
            "skill_runner": {
                "package": "claude-code",
                "config": {
                    "plato_api_key": "",
                    "anthropic_api_key": "",
                },
            },
            "steps": [{"name": "fix"}],
            "state": {"enabled": True, "resume_from": ""},
        },
    },
    "tags": ["simcreator"],
}

MOCK_DATAGEN_CONFIG = {
    "world": {
        "package": "plato-world-interactive",
        "config": {
            "anthropic_api_key": "",
            "plato_api_key": "",
            "anchor_api_key": "",
            "mcps": [],
            "envs": [],
            "initial_messages": [
                {
                    "message": "base datagen prompt",
                    "iterations": 2,
                    "continuation_prompt": "continue",
                }
            ],
        },
    },
    "tags": ["datagen"],
}


def _make_httpx_client_mock(post_return=None, get_return=None):
    """Build a mock httpx.Client context manager."""
    mock_client = MagicMock()
    if post_return is not None:
        mock_client.post.return_value = post_return
    if get_return is not None:
        mock_client.get.return_value = get_return

    mock_cls = MagicMock()
    mock_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
    mock_cls.return_value.__exit__ = MagicMock(return_value=False)
    return mock_cls, mock_client


def _make_sim_mock(name="aureus", sim_id=42, config=None):
    """Build a mock simulator object."""
    sim = MagicMock()
    sim.id = sim_id
    sim.name = name
    sim.config = config or {
        "status": "not_started",
        "source_code_url": "https://github.com/example/aureus",
        "base_artifact_id": "artifact-abc-123",
        "data_artifact_id": "",
    }
    return sim


# ===========================================================================
# _launch_on_chronos
# ===========================================================================


class TestLaunchOnChronos:
    @patch("plato.cli.pm.httpx.Client")
    def test_posts_to_chronos_and_returns_session_id(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"session_id": "sess-xyz"}

        mock_client = MagicMock()
        mock_client.post.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = _launch_on_chronos({"key": "value"}, "my-api-key")

        assert result == "sess-xyz"
        call = mock_client.post.call_args
        assert "/api/jobs/launch" in call.args[0]
        assert b'"key": "value"' in call.kwargs["content"]
        assert call.kwargs["headers"]["X-API-Key"] == "my-api-key"
        assert call.kwargs["headers"]["Content-Type"] == "application/json"

    @patch("plato.cli.pm.httpx.Client")
    def test_raises_on_non_200_status(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 500
        resp.text = "Internal Server Error"

        mock_client = MagicMock()
        mock_client.post.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(Exception, match="500"):
            _launch_on_chronos({}, "key")

    @patch("plato.cli.pm.httpx.Client")
    def test_raises_on_401_status(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 401
        resp.text = "Unauthorized"

        mock_client = MagicMock()
        mock_client.post.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        with pytest.raises(Exception, match="401"):
            _launch_on_chronos({"config": "x"}, "bad-key")

    @patch("plato.cli.pm.httpx.Client")
    def test_sends_json_encoded_body(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"session_id": "s1"}

        mock_client = MagicMock()
        mock_client.post.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        config = {"world": {"package": "test-pkg"}, "tags": ["t1"]}
        _launch_on_chronos(config, "k")

        raw_body = mock_client.post.call_args.kwargs["content"]
        decoded = json.loads(raw_body)
        assert decoded["world"]["package"] == "test-pkg"
        assert "t1" in decoded["tags"]


# ===========================================================================
# _get_last_chronos_session
# ===========================================================================


class TestGetLastChronosSession:
    @patch("plato.cli.pm.httpx.Client")
    def test_returns_first_session(self, mock_client_cls):
        session = {"public_id": "session-001", "status": "done"}
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"sessions": [session]}

        mock_client = MagicMock()
        mock_client.get.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = _get_last_chronos_session(["simcreator", "aureus"], "api-key")

        assert result == session
        call = mock_client.get.call_args
        assert "/api/sessions" in call.args[0]
        assert call.kwargs["headers"]["X-API-Key"] == "api-key"

    @patch("plato.cli.pm.httpx.Client")
    def test_passes_tag_params_and_limit(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"sessions": []}

        mock_client = MagicMock()
        mock_client.get.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        _get_last_chronos_session(["simcreator", "aureus"], "key")

        params = mock_client.get.call_args.kwargs["params"]
        # params is list of (key, value) tuples
        tag_values = [v for k, v in params if k == "tag"]
        assert "simcreator" in tag_values
        assert "aureus" in tag_values
        limit_values = [v for k, v in params if k == "limit"]
        assert "1" in limit_values

    @patch("plato.cli.pm.httpx.Client")
    def test_returns_none_when_empty_sessions(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"sessions": []}

        mock_client = MagicMock()
        mock_client.get.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = _get_last_chronos_session(["simcreator"], "key")
        assert result is None

    @patch("plato.cli.pm.httpx.Client")
    def test_returns_none_on_http_error(self, mock_client_cls):
        resp = MagicMock()
        resp.status_code = 403
        resp.json.return_value = {}

        mock_client = MagicMock()
        mock_client.get.return_value = resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = _get_last_chronos_session(["simcreator"], "bad-key")
        assert result is None

    @patch("plato.cli.pm.httpx.Client")
    def test_returns_none_on_exception(self, mock_client_cls):
        mock_client_cls.side_effect = Exception("network error")

        result = _get_last_chronos_session(["t1"], "key")
        assert result is None


# ===========================================================================
# _launch_env_world
# ===========================================================================


class TestLaunchEnvWorld:
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fresh_sets_sim_name_and_github_url(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "session-fresh-001"

        result = asyncio.run(
            _launch_env_world(
                action="fresh",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={},
                action_inputs={"github_url": "https://github.com/example/aureus"},
            )
        )

        assert result == "session-fresh-001"
        # Verify the template was mutated before launch
        called_template = mock_launch.call_args.args[0]
        assert called_template["world"]["config"]["sim_name"] == "aureus"
        assert called_template["world"]["config"]["github_url"] == "https://github.com/example/aureus"
        assert "aureus" in called_template["tags"]

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fresh_fetches_env_base_experiment(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "sess-1"

        asyncio.run(
            _launch_env_world(
                action="fresh",
                simulator_name="memos",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={},
                action_inputs={"github_url": "https://github.com/example/memos"},
            )
        )

        mock_fetch.assert_called_once_with("env", "base", "key")

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fresh_returns_none_when_no_github_url(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")

        result = asyncio.run(
            _launch_env_world(
                action="fresh",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={},
                action_inputs={},  # no github_url
            )
        )

        assert result is None
        mock_launch.assert_not_called()

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_resume_uses_base_template_with_resume_from(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "session-resume-001"

        result = asyncio.run(
            _launch_env_world(
                action="resume",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={"source_code_url": "https://github.com/example/aureus"},
                action_inputs={"resume_from": "prev-session-id"},
            )
        )

        assert result == "session-resume-001"
        mock_fetch.assert_called_once_with("env", "base", "key")
        called_template = mock_launch.call_args.args[0]
        cfg = called_template["world"]["config"]
        assert cfg["sim_name"] == "aureus"
        assert cfg["github_url"] == "https://github.com/example/aureus"
        assert cfg["state"]["resume_from"] == "prev-session-id"

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fix_sets_artifact_id_and_feedback(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_RESUME_CONFIG), "ver-mock-1")
        mock_launch.return_value = "session-fix-001"

        result = asyncio.run(
            _launch_env_world(
                action="fix",
                simulator_name="aureus",
                artifact_id="",
                feedback="Please fix the login page",
                api_key="key",
                current_config={"base_artifact_id": "base-art-uuid"},
                action_inputs={"resume_from": "prev-session-id"},
            )
        )

        assert result == "session-fix-001"
        called_template = mock_launch.call_args.args[0]
        cfg = called_template["world"]["config"]
        assert cfg["sim_name"] == "aureus"
        assert cfg["artifact_id"] == "base-art-uuid"
        assert cfg["feedback"] == "Please fix the login page"
        assert cfg["state"]["resume_from"] == "prev-session-id"

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fix_fetches_env_fix_experiment(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_RESUME_CONFIG), "ver-mock-1")
        mock_launch.return_value = "sess-1"

        asyncio.run(
            _launch_env_world(
                action="fix",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={"base_artifact_id": "base-art-uuid"},
                action_inputs={},
            )
        )

        mock_fetch.assert_called_once_with("env", "fix", "key")

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fix_returns_none_when_no_base_artifact_id(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_RESUME_CONFIG), "ver-mock-1")

        result = asyncio.run(
            _launch_env_world(
                action="fix",
                simulator_name="aureus",
                artifact_id="",
                feedback="fix it",
                api_key="key",
                current_config={},  # no base_artifact_id
                action_inputs={},
            )
        )

        assert result is None
        mock_launch.assert_not_called()

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm._get_claude_credentials", return_value=("claude_oauth_credentials", '{"oauth":"creds"}'))
    def test_sets_api_keys_on_skill_runner(self, mock_creds, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        import plato.cli.pm as pm_module

        pm_module.DEFAULT_DATAGEN_API_KEY = "datagen-key"

        asyncio.run(
            _launch_env_world(
                action="fresh",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={},
                action_inputs={"github_url": "https://github.com/x"},
            )
        )

        called_template = mock_launch.call_args.args[0]
        cfg = called_template["world"]["config"]
        assert cfg["skill_runner"]["config"]["plato_api_key"] == "datagen-key"
        assert cfg["skill_runner"]["config"]["claude_oauth_credentials"] == '{"oauth":"creds"}'
        # Stale placeholder should be removed
        assert "anthropic_api_key" not in cfg["skill_runner"]["config"]
        assert "anthropic_api_key" not in cfg

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fresh_attaches_session_to_experiment(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-env-1")
        mock_launch.return_value = "sess-fresh-001"

        asyncio.run(
            _launch_env_world(
                action="fresh",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={},
                action_inputs={"github_url": "https://github.com/example/aureus"},
            )
        )

        mock_attach.assert_called_once_with("ver-env-1", "sess-fresh-001", "key")

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_resume_attaches_session_to_experiment(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-env-resume-1")
        mock_launch.return_value = "sess-resume-001"

        asyncio.run(
            _launch_env_world(
                action="resume",
                simulator_name="aureus",
                artifact_id="",
                feedback="",
                api_key="key",
                current_config={"source_code_url": "https://github.com/example/aureus"},
                action_inputs={"resume_from": "prev-session-id"},
            )
        )

        mock_attach.assert_called_once_with("ver-env-resume-1", "sess-resume-001", "key")

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    def test_fix_attaches_session_to_experiment(self, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_RESUME_CONFIG), "ver-env-fix-1")
        mock_launch.return_value = "sess-fix-001"

        asyncio.run(
            _launch_env_world(
                action="fix",
                simulator_name="aureus",
                artifact_id="",
                feedback="fix it",
                api_key="key",
                current_config={"base_artifact_id": "base-art-uuid"},
                action_inputs={"resume_from": "prev-session-id"},
            )
        )

        mock_attach.assert_called_once_with("ver-env-fix-1", "sess-fix-001", "key")


# ===========================================================================
# _launch_datagen_world
# ===========================================================================


class TestLaunchDatagenWorld:
    @pytest.fixture(autouse=True)
    def _auto_confirm_missing_anchor_key(self, monkeypatch):
        monkeypatch.setattr("plato.cli.pm.typer.confirm", lambda *args, **kwargs: True)

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_returns_session_id_on_success(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-mock-1")
        mock_launch.return_value = "datagen-session-001"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        result = asyncio.run(
            _launch_datagen_world(
                simulator_name="aureus",
                artifact_id="art-uuid",
                api_key="key",
                iterations=3,
            )
        )

        assert result == "datagen-session-001"

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_fetches_db_config_for_artifact(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(
            _launch_datagen_world(
                simulator_name="aureus",
                artifact_id="art-uuid",
                api_key="key",
            )
        )

        call_url = mock_client.get.call_args.args[0]
        assert "art-uuid" in call_url
        assert "db_config" in call_url

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_builds_mcps_with_db_vm_browser_functions(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        db_entry = {
            "db_type": "postgres",
            "db_port": 5432,
            "db_user": "admin",
            "db_password": "secret",
            "db_database": "mydb",
        }
        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = [db_entry]

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(
            _launch_datagen_world(
                simulator_name="aureus",
                artifact_id="art-uuid",
                api_key="key",
            )
        )

        called_template = mock_launch.call_args.args[0]
        mcps = called_template["world"]["config"]["mcps"]
        types = [m["type"] for m in mcps]
        assert "db" in types
        assert "vm" in types
        assert "browser" in types
        assert "functions" in types

        db_mcp = next(m for m in mcps if m["type"] == "db")
        assert db_mcp["db_type"] == "postgres"
        assert db_mcp["service"] == "aureus"

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_sets_iterations_on_initial_message(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(
            _launch_datagen_world(
                simulator_name="aureus",
                artifact_id="art-uuid",
                api_key="key",
                iterations=5,
            )
        )

        called_template = mock_launch.call_args.args[0]
        msg = called_template["world"]["config"]["initial_messages"][0]
        assert msg["iterations"] == 5

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_wraps_message_with_review_prompt_when_comments_given(
        self, mock_client_cls, mock_fetch, mock_launch, mock_attach
    ):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(
            _launch_datagen_world(
                simulator_name="aureus",
                artifact_id="art-uuid",
                api_key="key",
                review_comments=["Fix missing data", "Add more users"],
            )
        )

        called_template = mock_launch.call_args.args[0]
        msg = called_template["world"]["config"]["initial_messages"][0]["message"]
        assert "REVIEW FOLLOW-UP" in msg
        assert "Fix missing data" in msg
        assert "Add more users" in msg

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_appends_sim_name_to_tags(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(
            _launch_datagen_world(
                simulator_name="aureus",
                artifact_id="art-uuid",
                api_key="key",
            )
        )

        called_template = mock_launch.call_args.args[0]
        assert "aureus" in called_template["tags"]

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_does_not_set_world_package_in_template(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        """World package comes from the experiment config, not from the function."""
        import copy

        cfg = copy.deepcopy(MOCK_DATAGEN_CONFIG)
        # Simulate the experiment having a specific package already set
        cfg["world"]["package"] = "plato-world-interactive"
        mock_fetch.return_value = (cfg, "ver-mock-1")
        mock_launch.return_value = "s1"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(_launch_datagen_world("aureus", "art-uuid", "key"))

        called_template = mock_launch.call_args.args[0]
        # Package should remain as-is from experiment (not overwritten)
        assert called_template["world"]["package"] == "plato-world-interactive"

    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.httpx.Client")
    def test_attaches_session_to_experiment(self, mock_client_cls, mock_fetch, mock_launch, mock_attach):
        import copy

        mock_fetch.return_value = (copy.deepcopy(MOCK_DATAGEN_CONFIG), "ver-data-1")
        mock_launch.return_value = "datagen-sess-001"

        db_resp = MagicMock()
        db_resp.status_code = 200
        db_resp.json.return_value = []

        mock_client = MagicMock()
        mock_client.get.return_value = db_resp
        mock_client_cls.return_value.__enter__ = MagicMock(return_value=mock_client)
        mock_client_cls.return_value.__exit__ = MagicMock(return_value=False)

        asyncio.run(_launch_datagen_world("aureus", "art-uuid", "key"))

        mock_attach.assert_called_once_with("ver-data-1", "datagen-sess-001", "key")


# ===========================================================================
# CLI: plato pm list not-started
# ===========================================================================


class TestListNotStartedCommand:
    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.get_organization_members")
    @patch("plato.cli.pm.get_simulators")
    def test_shows_table_for_matching_simulators(self, mock_get_sims, mock_get_members):
        sim = {
            "name": "aureus",
            "id": 1,
            "config": {
                "status": "not_started",
                "type": "docker_app",
                "source_code_url": "https://github.com/x/aureus",
                "license": "MIT",
                "notes": "some notes",
            },
        }
        mock_get_sims.asyncio = AsyncMock(return_value=[sim])
        mock_get_members.asyncio = AsyncMock(return_value=[])

        result = runner.invoke(pm_app, ["list", "not-started"])

        assert result.exit_code == 0, result.output
        assert "aureus" in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.get_organization_members")
    @patch("plato.cli.pm.get_simulators")
    def test_skips_non_docker_app_simulators(self, mock_get_sims, mock_get_members):
        sims = [
            {
                "name": "aureus",
                "id": 1,
                "config": {
                    "status": "not_started",
                    "type": "docker_app",
                    "source_code_url": "",
                    "license": "",
                    "notes": "",
                },
            },
            {
                "name": "other-sim",
                "id": 2,
                "config": {
                    "status": "not_started",
                    "type": "some_other_type",
                    "source_code_url": "",
                    "license": "",
                    "notes": "",
                },
            },
        ]
        mock_get_sims.asyncio = AsyncMock(return_value=sims)
        mock_get_members.asyncio = AsyncMock(return_value=[])

        result = runner.invoke(pm_app, ["list", "not-started"])

        assert result.exit_code == 0, result.output
        assert "aureus" in result.output
        assert "other-sim" not in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.get_organization_members")
    @patch("plato.cli.pm.get_simulators")
    def test_shows_no_simulators_message_when_empty(self, mock_get_sims, mock_get_members):
        mock_get_sims.asyncio = AsyncMock(return_value=[])
        mock_get_members.asyncio = AsyncMock(return_value=[])

        result = runner.invoke(pm_app, ["list", "not-started"])

        assert result.exit_code == 0, result.output
        assert "not_started" in result.output


# ===========================================================================
# CLI: plato pm start env
# ===========================================================================


class TestStartEnvCommand:
    def _make_env_mocks(self, sim_config=None):
        """Create a set of mocks for start env. Returns (mock_get_by_name, mock_update_status, mock_fetch, mock_launch)."""
        sim = _make_sim_mock(
            config=sim_config
            or {
                "status": "not_started",
                "source_code_url": "https://github.com/example/aureus",
                "base_artifact_id": "base-art-uuid",
                "data_artifact_id": "",
            }
        )
        mock_get_by_name = MagicMock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        return sim, mock_get_by_name

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.update_simulator_status")
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_succeeds_with_github_url(
        self, mock_get_by_name, mock_update_status, mock_fetch, mock_launch, mock_attach
    ):
        import copy

        sim = _make_sim_mock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        mock_update_status.asyncio = AsyncMock(return_value=None)
        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "sess-start-001"

        result = runner.invoke(pm_app, ["start", "env", "aureus"], input="y\n")

        assert result.exit_code == 0, result.output
        assert "sess-start-001" in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.update_simulator_status")
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_skips_sim_without_github_url(
        self, mock_get_by_name, mock_update_status, mock_fetch, mock_launch, mock_attach
    ):
        sim = _make_sim_mock(config={"status": "not_started", "source_code_url": ""})
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        mock_update_status.asyncio = AsyncMock(return_value=None)

        result = runner.invoke(pm_app, ["start", "env", "aureus"], input="y\n")

        # Should print "Nothing to launch" since sim has no github URL
        assert "Nothing to launch" in result.output
        mock_launch.assert_not_called()

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.update_simulator_status")
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_sets_sim_name_in_config(
        self, mock_get_by_name, mock_update_status, mock_fetch, mock_launch, mock_attach
    ):
        import copy

        sim = _make_sim_mock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        mock_update_status.asyncio = AsyncMock(return_value=None)
        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        runner.invoke(pm_app, ["start", "env", "aureus"], input="y\n")

        called_template = mock_launch.call_args.args[0]
        assert called_template["world"]["config"]["sim_name"] == "aureus"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.update_simulator_status")
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_updates_status_before_launch(
        self, mock_get_by_name, mock_update_status, mock_fetch, mock_launch, mock_attach
    ):
        import copy

        sim = _make_sim_mock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        mock_update_status.asyncio = AsyncMock(return_value=None)
        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        runner.invoke(pm_app, ["start", "env", "aureus"], input="y\n")

        mock_update_status.asyncio.assert_called_once()
        update_kwargs = mock_update_status.asyncio.call_args.kwargs
        assert update_kwargs["body"].status == "env_in_progress"

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_cancels_when_user_declines(self, mock_get_by_name):
        sim = _make_sim_mock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)

        result = runner.invoke(pm_app, ["start", "env", "aureus"], input="n\n")

        assert "Cancelled" in result.output

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.update_simulator_status")
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_appends_sim_name_to_tags(
        self, mock_get_by_name, mock_update_status, mock_fetch, mock_launch, mock_attach
    ):
        import copy

        sim = _make_sim_mock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        mock_update_status.asyncio = AsyncMock(return_value=None)
        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-mock-1")
        mock_launch.return_value = "s1"

        runner.invoke(pm_app, ["start", "env", "aureus"], input="y\n")

        called_template = mock_launch.call_args.args[0]
        assert "aureus" in called_template["tags"]

    @patch.dict("os.environ", {"PLATO_API_KEY": "test-key"})
    @patch("plato.cli.pm._attach_session_to_experiment")
    @patch("plato.cli.pm._launch_on_chronos")
    @patch("plato.cli.pm._fetch_experiment_config")
    @patch("plato.cli.pm.update_simulator_status")
    @patch("plato.cli.pm.get_simulator_by_name")
    def test_start_env_attaches_session_to_experiment(
        self, mock_get_by_name, mock_update_status, mock_fetch, mock_launch, mock_attach
    ):
        import copy

        sim = _make_sim_mock()
        mock_get_by_name.asyncio = AsyncMock(return_value=sim)
        mock_update_status.asyncio = AsyncMock(return_value=None)
        mock_fetch.return_value = (copy.deepcopy(MOCK_ENV_BASE_CONFIG), "ver-start-1")
        mock_launch.return_value = "sess-start-001"

        runner.invoke(pm_app, ["start", "env", "aureus"], input="y\n")

        mock_attach.assert_called_once_with("ver-start-1", "sess-start-001", "test-key")
