"""Tests for the hooks relay command.

The typer command is a thin wrapper over ``runlayer_cli.hook.relay`` — the
patches target that shared module rather than ``commands.hooks`` so the
test surface mirrors the production credential / POST contract used by
both the bash shim and the in-process ``aiwatch-hook`` paths.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest
from typer.testing import CliRunner

from runlayer_cli.commands.hooks import app
from runlayer_cli.config import Config, HostConfig

runner = CliRunner()


@pytest.fixture(autouse=True)
def _no_managed_config():
    """Neutralize MDM lookup for every test in this file.

    ``hook.relay._load_credentials`` calls ``read_managed_config`` on every
    invocation. On a dev Mac with a real AI Watch profile installed, the
    ``no_host`` test would resolve a host from there and the suite would
    fail. Pin to an empty mapping so config-only credentials drive the
    tests deterministically.
    """
    with patch("runlayer_cli.hook.relay.read_managed_config", return_value={}):
        yield


def _make_config(*, host: str = "https://app.example.com", secret: str = "test-key"):
    config = Config(
        default_host=host,
        hosts={
            "app.example.com": HostConfig(url=host),
        },
    )
    mock_store = MagicMock()
    mock_store.get_secret.return_value = secret
    return config, mock_store


def test_relay_enforce_success():
    """Relay enforce posts to /api/v1/hooks/cursor and returns response."""
    config, mock_store = _make_config()
    response_body = json.dumps({"permission": "allow"})

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = response_body
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce"], input='{"test": true}')
        assert result.exit_code == 0
        assert response_body in result.output

        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert "/api/v1/hooks/cursor" in call_args[0][0]
        assert call_args[1]["headers"]["x-runlayer-api-key"] == "test-key"


def test_relay_event_success():
    """Relay event posts to /api/v1/hooks/events."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "{}"
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["event"], input='{"test": true}')
        assert result.exit_code == 0

        call_args = mock_client.post.call_args
        assert "/api/v1/hooks/events" in call_args[0][0]


def test_relay_tool_lifecycle_targets():
    """Relay tool-pre/tool-post posts to local tool lifecycle endpoints."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "{}"
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["tool-pre"], input='{"test": true}')
        assert result.exit_code == 0
        assert "/api/v1/hooks/tool/pre" in mock_client.post.call_args[0][0]

        mock_client.post.reset_mock()

        result = runner.invoke(app, ["tool-post"], input='{"test": true}')
        assert result.exit_code == 0
        assert "/api/v1/hooks/tool/post" in mock_client.post.call_args[0][0]


def test_relay_unknown_target():
    """Unknown target exits with code 1."""
    result = runner.invoke(app, ["unknown"], input="{}")
    assert result.exit_code == 1


def test_relay_no_host_exits_1():
    """Missing host in config exits with code 1."""
    config = Config()

    with patch("runlayer_cli.hook.relay.load_config", return_value=config):
        result = runner.invoke(app, ["enforce"], input="{}")
        assert result.exit_code == 1


def test_relay_no_secret_exits_1():
    """Missing secret for host exits with code 1."""
    config = Config(
        default_host="https://app.example.com",
        hosts={"app.example.com": HostConfig(url="https://app.example.com")},
    )

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=None),
    ):
        result = runner.invoke(app, ["enforce"], input="{}")
        assert result.exit_code == 1


def test_relay_network_error_exits_2():
    """Network error exits with code 2."""
    config, mock_store = _make_config()

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.side_effect = httpx.ConnectError("connection refused")
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce"], input="{}")
        assert result.exit_code == 2


def test_relay_api_error_exits_2():
    """Non-success HTTP response exits with code 2."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = '{"error": "unauthorized"}'
    mock_response.status_code = 401
    mock_response.is_success = False

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce"], input="{}")
        assert result.exit_code == 2


def test_relay_timeout_override():
    """--timeout overrides the default for the target."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "{}"
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["event", "--timeout", "15"], input="{}")
        assert result.exit_code == 0
        assert mock_client.post.call_args[1]["timeout"] == 15


def test_relay_hidden_from_help():
    """The hooks app should be hidden."""
    assert app.info.hidden is True


def test_relay_debug_writes_file(tmp_path: Path):
    """--debug writes request/response JSON to temp dir."""
    config, mock_store = _make_config()
    response_body = '{"ok": true}'

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = response_body
    mock_response.status_code = 200
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
        patch("runlayer_cli.hook.relay._DEBUG_DIR", tmp_path),
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce", "--debug"], input='{"req": 1}')
        assert result.exit_code == 0
        assert response_body in result.output

    files = list(tmp_path.glob("runlayer-relay-enforce-*.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert data["url"] == "https://app.example.com/api/v1/hooks/cursor"
    # Bodies are deliberately not persisted — see `_write_debug` docstring.
    assert "request_body" not in data
    assert "response_body" not in data
    assert data["request_body_size"] == len('{"req": 1}')
    assert data["response_body_size"] == len(response_body)
    assert data["response_status"] == 200
    assert "timestamp" in data


def test_relay_debug_does_not_alter_exit_code(tmp_path: Path):
    """--debug doesn't change exit code on HTTP failure."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = '{"error": "bad"}'
    mock_response.status_code = 403
    mock_response.is_success = False

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
        patch("runlayer_cli.hook.relay._DEBUG_DIR", tmp_path),
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce", "--debug"], input="{}")
        assert result.exit_code == 2

    files = list(tmp_path.glob("runlayer-relay-enforce-*.json"))
    assert len(files) == 1
    assert json.loads(files[0].read_text())["response_status"] == 403


def test_relay_debug_io_failure_ignored(tmp_path: Path):
    """Debug file write failure doesn't affect relay behaviour."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = '{"ok": true}'
    mock_response.status_code = 200
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
        patch("runlayer_cli.hook.relay._write_debug", side_effect=OSError("boom")),
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce", "--debug"], input="{}")
        assert result.exit_code == 0


def test_relay_debug_on_network_error(tmp_path: Path):
    """--debug still writes a file on network error (response fields null)."""
    config, mock_store = _make_config()

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
        patch("runlayer_cli.hook.relay._DEBUG_DIR", tmp_path),
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.side_effect = httpx.ConnectError("refused")
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["enforce", "--debug"], input='{"x": 1}')
        assert result.exit_code == 2

    files = list(tmp_path.glob("runlayer-relay-enforce-*.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text())
    assert data["response_status"] is None
    assert data["response_body_size"] is None
    assert "response_body" not in data


def test_relay_org_key_mode_uses_org_key_and_attaches_device():
    """When MDM ships an OrgApiKey, hooks authenticate with it and attach a
    device block so the backend can resolve identity server-side."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "{}"
    mock_response.is_success = True

    managed = {"host": "https://app.example.com", "org_api_key": "org-key-123"}
    device = {"device_id": "dev-1", "username": "alice"}

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.hook.relay.read_managed_config", return_value=managed),
        patch("runlayer_cli.hook.relay._build_device_context", return_value=device),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["event"], input='{"event_name": "SessionStart"}')
        assert result.exit_code == 0

        call_args = mock_client.post.call_args
        assert call_args[1]["headers"]["x-runlayer-api-key"] == "org-key-123"
        body = json.loads(call_args[1]["content"])
        assert body["device"] == device


def test_build_device_context_logs_failure_to_stderr(capsys):
    """When scan helpers blow up (broken import, permission error), the device
    block is unavailable. Org-key mode degrades silently server-side, so the
    cause must surface on stderr (not stdout, which is the hook protocol
    channel) to help MDM rollouts spot the breakage — type/message only."""
    from runlayer_cli.hook import relay

    boom = PermissionError("denied: /Users/x/.runlayer/device_id")
    with patch(
        "runlayer_cli.scan.device.get_device_metadata",
        side_effect=boom,
    ):
        result = relay._build_device_context()

    assert result is None
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "device context unavailable" in captured.err
    assert "PermissionError" in captured.err
    assert "denied" in captured.err


def test_relay_legacy_user_key_attaches_no_device():
    """Without an OrgApiKey, the per-user path is unchanged: user key, no
    device block."""
    config, mock_store = _make_config()

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "{}"
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.hook.relay.read_managed_config", return_value={}),
        patch("runlayer_cli.config.get_keyring_store", return_value=mock_store),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["event"], input='{"event_name": "SessionStart"}')
        assert result.exit_code == 0

        call_args = mock_client.post.call_args
        assert call_args[1]["headers"]["x-runlayer-api-key"] == "test-key"
        body = json.loads(call_args[1]["content"])
        assert "device" not in body
