"""Tests for the hooks relay command.

The typer command is a thin wrapper over ``runlayer_cli.hook.relay`` — the
patches target that shared module rather than ``commands.hooks`` so the
test surface mirrors the production credential / POST contract used by
both the bash shim and the in-process ``aiwatch-hook`` paths.
"""

import json
import logging
import os
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest
import structlog
from typer.testing import CliRunner

from runlayer_cli.commands.hooks import app
from runlayer_cli.config import Config, HostConfig

runner = CliRunner()


@pytest.fixture(autouse=True)
def _reset_logging_state():
    """Undo ``silence_hook_logging``'s process-global mutation after each test.

    The hook entrypoints call ``silence_hook_logging`` (structlog reconfigure +
    ``logging.disable``). That state is process-global, so reset it in teardown
    to keep it from leaking into unrelated tests.
    """
    yield
    logging.disable(logging.NOTSET)
    structlog.reset_defaults()


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


def test_relay_event_stamps_client_timestamp_when_absent():
    """Tool events get a host send-time so the backend scanner can order them
    against transcript-derived reasoning events (which carry their own logical
    timestamps) instead of the scrambled server-receipt arrival order."""
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

        wrapper = (
            '{"client":"claude_code","event_name":"PostToolUse",'
            '"payload":{"tool_name":"Bash"}}'
        )
        result = runner.invoke(app, ["event"], input=wrapper)
        assert result.exit_code == 0

        body = json.loads(mock_client.post.call_args[1]["content"])
        parsed = datetime.fromisoformat(body["payload"]["timestamp"])
        assert parsed.tzinfo is not None


def test_relay_event_preserves_existing_timestamp():
    """A client-supplied timestamp is never overwritten by the send-time stamp."""
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

        wrapper = (
            '{"client":"claude_code","event_name":"PostToolUse",'
            '"payload":{"tool_name":"Bash","timestamp":"2020-01-01T00:00:00+00:00"}}'
        )
        result = runner.invoke(app, ["event"], input=wrapper)
        assert result.exit_code == 0

        body = json.loads(mock_client.post.call_args[1]["content"])
        assert body["payload"]["timestamp"] == "2020-01-01T00:00:00+00:00"


def test_maybe_stamp_client_time_only_stamps_event_target():
    """Enforcement targets (tool-pre/tool-post/enforce) are passed through
    untouched; only ``event`` posts feed the ordering-sensitive scanner."""
    from runlayer_cli.hook import relay

    wrapper = '{"client":"c","event_name":"PreToolUse","payload":{"tool_name":"Bash"}}'
    assert relay._maybe_stamp_client_time(wrapper, "tool-pre") == wrapper
    stamped = relay._maybe_stamp_client_time(wrapper, "event")
    assert "timestamp" in json.loads(stamped)["payload"]


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


def test_mcp_usage_metadata_payload_is_strictly_minimal():
    from runlayer_cli.hook import relay

    captured: list[tuple[str, str]] = []
    with (
        patch.object(
            relay,
            "_forward_post",
            side_effect=lambda target, body, **_kwargs: captured.append((target, body)),
        ),
        patch.object(
            relay,
            "_build_device_context",
            return_value={
                "device_id": "device-1",
                "username": "ada@example.com",
                "device_name": "must-not-leave-host",
                "platform": "must-not-leave-host",
            },
        ),
    ):
        relay.forward_mcp_usage_metadata(
            client_name="claude_code",
            tool_name="mcp__github__create_issue",
            mcp_server_name="github",
        )

    assert captured == [
        (
            "mcp-usage",
            json.dumps(
                {
                    "client": "claude_code",
                    "tool_name": "mcp__github__create_issue",
                    "mcp_server_name": "github",
                    "device": {
                        "device_id": "device-1",
                        "username": "ada@example.com",
                    },
                }
            ),
        )
    ]


def test_mcp_usage_metadata_truncates_oversized_names():
    """Server caps are 512/255 with extra=forbid; the send is best-effort with
    exceptions swallowed, so an oversized name must be truncated client-side
    rather than silently 422-dropped."""
    from runlayer_cli.hook import relay

    captured: list[tuple[str, str]] = []
    with (
        patch.object(
            relay,
            "_forward_post",
            side_effect=lambda target, body, **_kwargs: captured.append((target, body)),
        ),
        patch.object(relay, "_build_device_context", return_value=None),
    ):
        relay.forward_mcp_usage_metadata(
            client_name="claude_code",
            tool_name="t" * 600,
            mcp_server_name="s" * 300,
        )

    body = json.loads(captured[0][1])
    assert body["tool_name"] == "t" * 512
    assert body["mcp_server_name"] == "s" * 255


def test_mcp_usage_metadata_defers_network_send():
    from runlayer_cli.hook import relay

    scheduled: list[Callable[[], None]] = []
    post = MagicMock()

    def enqueue(send):
        scheduled.append(send)
        return True

    relay.set_deferred_event_sender(enqueue)
    try:
        with (
            patch.object(
                relay,
                "_forward_post",
                side_effect=AssertionError("metadata POST must not block the hook"),
            ),
            patch.object(
                relay,
                "_load_credentials",
                return_value=("https://app.example.com", "test-key"),
            ),
            patch.object(relay, "_post", post),
            patch.object(
                relay,
                "_build_device_context",
                return_value={"device_id": "device-1"},
            ),
        ):
            relay.forward_mcp_usage_metadata(
                client_name="claude_code",
                tool_name="mcp__github__create_issue",
                mcp_server_name="github",
            )

            post.assert_not_called()
            assert len(scheduled) == 1
            scheduled[0]()

        post.assert_called_once()
        assert post.call_args.kwargs["target"] == "mcp-usage"
        assert post.call_args.kwargs["prepared"] is True
    finally:
        relay.set_deferred_event_sender(None)


def test_finalize_never_attaches_device_context_to_mcp_usage():
    """The finalize pipeline must not inject the full device context (hostname,
    serial number, ...) into ``mcp-usage`` bodies — even for a payload that
    (hypothetically) lacks the closed ``device`` key ``forward_mcp_usage_metadata``
    always sets. The backend rejects extra device fields; a silent attach here
    would break the only-identity-leaves-the-host contract."""
    from runlayer_cli.hook import relay

    full_context = {
        "device_id": "device-1",
        "username": "ada@example.com",
        "hostname": "must-not-leave-host",
        "serial_number": "must-not-leave-host",
        "os": "must-not-leave-host",
    }
    body = json.dumps({"client": "claude_code", "tool_name": "mcp__github__x"})
    with (
        patch.object(
            relay,
            "read_managed_config",
            return_value={"org_api_key": "rl_org_test"},
        ),
        patch.object(relay, "_build_device_context", return_value=full_context),
    ):
        finalized = json.loads(relay._finalize_payload(body, "mcp-usage"))
        assert "device" not in finalized
        assert "hostname" not in json.dumps(finalized)

        # The gate is target-scoped: event bodies still get the device block.
        event_finalized = json.loads(relay._finalize_payload(body, "event"))
        assert event_finalized["device"] == full_context


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


def test_hook_relay_emits_no_log_output_in_org_key_mode():
    """Regression (ENG-3839): a hook fire must write no log output.

    With structlog at its unconfigured default (as in a fresh hook process that
    never calls ``setup_logging``) and a REAL device-id resolver that logs, an
    org-key hook fire routes through ``_build_device_context`` ->
    ``get_or_create_device_id`` (which logs a device-id line). Before the fix
    that line hit stderr (via the old ``redirect_stdout(sys.stderr)`` band-aid)
    and clients flagged the hook as errored. Now ``silence_hook_logging`` at the
    entrypoint + the os.devnull redirect keep both channels clean: stdout
    carries only the protocol response, stderr is empty.
    """
    structlog.reset_defaults()  # emulate the fresh, unconfigured hook process

    config, mock_store = _make_config()
    managed = {"host": "https://app.example.com", "org_api_key": "org-key-123"}

    mock_response = MagicMock(spec=httpx.Response)
    mock_response.text = "{}"
    mock_response.is_success = True

    with (
        patch("runlayer_cli.hook.relay.load_config", return_value=config),
        patch("runlayer_cli.hook.relay.read_managed_config", return_value=managed),
        # RUNLAYER_DEVICE_ID makes the real resolver take its first branch and
        # emit the ``Using device ID from environment`` structlog line — no
        # hardware probe, no file I/O — so the test deterministically exercises
        # the device-id logging path that regressed.
        patch.dict(os.environ, {"RUNLAYER_DEVICE_ID": "regression-device-id"}),
        patch("httpx.Client") as mock_client_cls,
    ):
        mock_client = MagicMock()
        mock_client.__enter__ = MagicMock(return_value=mock_client)
        mock_client.__exit__ = MagicMock(return_value=False)
        mock_client.post.return_value = mock_response
        mock_client_cls.return_value = mock_client

        result = runner.invoke(app, ["event"], input='{"event_name": "SessionStart"}')

    assert result.exit_code == 0
    # The real resolver ran (device block attached with the env device id),
    # i.e. the code path that logs the device-id line was exercised.
    body = json.loads(mock_client.post.call_args[1]["content"])
    assert body["device"]["device_id"] == "regression-device-id"
    # stdout carries only the protocol response; no structlog line leaked.
    assert result.stdout == "{}"
    assert result.stderr == ""
    combined = result.stdout + result.stderr
    assert "device ID" not in combined
    assert "device_id_prefix" not in combined


def test_build_device_context_failure_silent_without_debug(capsys):
    """When scan helpers blow up (broken import, permission error) the device
    block is unavailable, but org-key mode degrades silently server-side. That
    is not a hook error, so by default nothing goes to stdout (protocol channel)
    or stderr (clients treat any stderr as a failed hook)."""
    from runlayer_cli.hook import relay

    boom = PermissionError("denied: /Users/x/.runlayer/device_id")
    with (
        patch.dict(os.environ),
        patch("runlayer_cli.scan.device.get_device_metadata", side_effect=boom),
    ):
        os.environ.pop("RUNLAYER_HOOK_DEBUG", None)
        result = relay._build_device_context()

    assert result is None
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_build_device_context_logs_failure_to_stderr_when_debug(capsys):
    """With RUNLAYER_HOOK_DEBUG=1, the failure cause surfaces on stderr (not
    stdout, which is the hook protocol channel) to help MDM rollouts spot broken
    scan imports or permission issues — type/message only, no secrets."""
    from runlayer_cli.hook import relay

    boom = PermissionError("denied: /Users/x/.runlayer/device_id")
    with (
        patch.dict(os.environ, {"RUNLAYER_HOOK_DEBUG": "1"}),
        patch("runlayer_cli.scan.device.get_device_metadata", side_effect=boom),
    ):
        result = relay._build_device_context()

    assert result is None
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "device context unavailable" in captured.err
    assert "PermissionError" in captured.err
    assert "denied" in captured.err


def test_build_device_context_includes_serial_number():
    """The org-key hook device block carries the collected hardware serial."""
    from runlayer_cli.hook import relay

    metadata = {
        "hostname": "host-1",
        "os": "darwin",
        "os_version": "15.0",
        "username": "alice",
        "serial_number": "C02XYZ123ABC",
    }
    with (
        patch("runlayer_cli.scan.device.get_device_metadata", return_value=metadata),
        patch(
            "runlayer_cli.scan.device.get_or_create_device_id",
            return_value="device-uuid",
        ),
        patch("runlayer_cli.hook.relay.read_managed_config", return_value={}),
    ):
        result = relay._build_device_context()

    assert result is not None
    assert result["serial_number"] == "C02XYZ123ABC"
    assert result["device_id"] == "device-uuid"


class TestDeferredEventSending:
    """Daemon-installed deferred sender: the request body is fully built at
    schedule time on the hook thread (device context, client-time stamp,
    client_flows drain, credentials); only the network send is queued."""

    def _mock_wire(self, requests: list[httpx.Request]) -> httpx.Client:
        def respond(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, text="{}")

        return httpx.Client(transport=httpx.MockTransport(respond))

    def test_forward_event_enqueues_send_with_prepared_body(self, monkeypatch):
        from runlayer_cli.hook import relay

        queued: list = []
        requests: list[httpx.Request] = []
        monkeypatch.setattr(
            relay,
            "_deferred_event_sender",
            lambda send: queued.append(send) or True,
        )
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )
        client = self._mock_wire(requests)
        monkeypatch.setattr(relay, "_shared_http_client_provider", lambda: client)
        try:
            relay.forward_event("claude_code", "PostToolUse", {"tool_name": "Bash"})

            # Nothing hits the wire at schedule time; one send is queued.
            assert requests == []
            assert len(queued) == 1

            # The queued send must not re-run the payload mutators — the body
            # (including the ordering-key timestamp) was built at schedule
            # time.
            def _boom(payload: str, target: str) -> str:
                raise AssertionError("mutators must not re-run at send time")

            monkeypatch.setattr(relay, "_finalize_payload", _boom)
            queued[0]()
        finally:
            client.close()

        assert len(requests) == 1
        assert requests[0].url.path == "/api/v1/hooks/events"
        body = json.loads(requests[0].content)
        assert body["event_name"] == "PostToolUse"
        parsed = datetime.fromisoformat(body["payload"]["timestamp"])
        assert parsed.tzinfo is not None

    def test_client_flows_drained_at_schedule_time(self, monkeypatch):
        from runlayer_cli.hook import relay

        queued: list = []
        drains: list[str] = []
        monkeypatch.setattr(
            relay,
            "_deferred_event_sender",
            lambda send: queued.append(send) or True,
        )
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )

        def _record_drain(payload: str, target: str) -> str:
            drains.append(target)
            return payload

        monkeypatch.setattr(relay, "_maybe_attach_client_flows", _record_drain)

        relay.forward_event("claude_code", "PostToolUse", {"tool_name": "Bash"})

        # The spool drain happened while scheduling, not when the queued
        # send eventually runs (lag-one delivery semantics preserved).
        assert drains == ["event"]
        assert len(queued) == 1

    def test_sync_fallback_when_sender_declines(self, monkeypatch):
        from runlayer_cli.hook import relay

        requests: list[httpx.Request] = []
        monkeypatch.setattr(relay, "_deferred_event_sender", lambda send: False)
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )
        client = self._mock_wire(requests)
        monkeypatch.setattr(relay, "_shared_http_client_provider", lambda: client)
        try:
            relay.forward_event("claude_code", "PostToolUse", {"tool_name": "Bash"})
        finally:
            client.close()

        # Closed/declining queue falls back to the synchronous POST.
        assert len(requests) == 1
        assert requests[0].url.path == "/api/v1/hooks/events"

    def test_declined_sender_preserves_drained_client_flows(
        self, monkeypatch, tmp_path
    ):
        """Schedule-time finalization already drained the spool (destructive);
        the declined-sender fallback must send that finalized payload rather
        than re-finalize, which re-drains an empty spool and loses the
        client_flows envelope."""
        import time

        from runlayer_cli import flow_spool, flow_trace
        from runlayer_cli.hook import relay

        monkeypatch.setattr(flow_spool, "get_runlayer_dir", lambda: tmp_path)
        requests: list[httpx.Request] = []
        monkeypatch.setattr(relay, "_deferred_event_sender", lambda send: False)
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )
        client = self._mock_wire(requests)
        monkeypatch.setattr(relay, "_shared_http_client_provider", lambda: client)
        flow_trace.enable_flow_tracing(flow_spool.spool_append)
        try:
            flow_spool.spool_append(
                {"operation": "cli.hook_event", "status": "ok", "ts": int(time.time())}
            )
            relay.forward_event("claude_code", "PostToolUse", {"tool_name": "Bash"})
        finally:
            flow_trace.disable_flow_tracing()
            client.close()

        assert len(requests) == 1
        body = json.loads(requests[0].content)
        assert body.get("client_flows"), "drained flow envelope was lost"

    def test_defer_false_posts_inline_even_with_sender_installed(self, monkeypatch):
        from runlayer_cli.hook import relay

        queued: list = []
        requests: list[httpx.Request] = []
        monkeypatch.setattr(
            relay,
            "_deferred_event_sender",
            lambda send: queued.append(send) or True,
        )
        monkeypatch.setattr(
            relay,
            "_load_credentials",
            lambda: ("https://api.example.com", "rl_org_test"),
        )
        client = self._mock_wire(requests)
        monkeypatch.setattr(relay, "_shared_http_client_provider", lambda: client)
        try:
            relay.forward_event(
                "claude_code", "Stop", {"session_id": "s1"}, defer=False
            )
        finally:
            client.close()

        assert queued == []
        assert len(requests) == 1

    def test_schedule_time_failure_is_swallowed(self, monkeypatch):
        from runlayer_cli.hook import relay

        def _no_creds() -> tuple[str, str]:
            raise relay.RelayError(1, "no secret for host")

        monkeypatch.setattr(relay, "_deferred_event_sender", lambda send: True)
        monkeypatch.setattr(relay, "_load_credentials", _no_creds)

        # Best-effort like the sync path: no exception escapes the hook.
        relay.forward_event("claude_code", "PostToolUse", {"tool_name": "Bash"})


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
