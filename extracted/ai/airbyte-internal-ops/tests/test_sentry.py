# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the Sentry integration module."""

from unittest.mock import MagicMock, patch

import pytest
from sentry_sdk.integrations.starlette import StarletteIntegration

from airbyte_ops_mcp._sentry import (
    DEFAULT_TRACES_SAMPLE_RATE,
    SENTRY_ENVIRONMENT_ENV_VAR,
    TRACES_SAMPLE_RATE_ENV_VAR,
    _get_package_version,
    _get_traces_sample_rate,
    _webapp_traces_sampler,
    capture_exception,
    capture_message,
    get_sentry_environment,
    init_sentry_tracking,
)

_INITIALIZED_FLAG = "airbyte_ops_mcp._sentry._sentry_initialized"


@pytest.fixture(autouse=True)
def reset_sentry_state(monkeypatch: pytest.MonkeyPatch):
    """Reset the global sentry state before each test."""

    monkeypatch.setattr(_INITIALIZED_FLAG, False)
    yield


@pytest.fixture
def sentry_env(monkeypatch: pytest.MonkeyPatch):
    """Sentry only initializes when `SENTRY_ENVIRONMENT` is set."""
    monkeypatch.setenv(SENTRY_ENVIRONMENT_ENV_VAR, "test")


@pytest.mark.parametrize(
    "version_result,expected",
    [
        pytest.param("1.2.3", "1.2.3", id="valid_version"),
        pytest.param(None, "unknown", id="version_not_found"),
    ],
)
def test_get_package_version(version_result: str | None, expected: str) -> None:
    """Test _get_package_version returns correct version or 'unknown'."""
    if version_result is None:
        with patch(
            "importlib.metadata.version",
            side_effect=Exception("Package not found"),
        ):
            assert _get_package_version() == expected
    else:
        with patch("importlib.metadata.version", return_value=version_result):
            assert _get_package_version() == expected


def test_init_sentry_already_initialized(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test init_sentry returns True if already initialized."""

    monkeypatch.setattr(_INITIALIZED_FLAG, True)
    assert init_sentry_tracking() is True


def test_capture_exception_calls_sentry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test capture_exception calls sentry_sdk.capture_exception when initialized."""

    mock_capture = MagicMock()
    monkeypatch.setattr("sentry_sdk.capture_exception", mock_capture)
    monkeypatch.setattr(_INITIALIZED_FLAG, True)

    test_exception = ValueError("test error")
    capture_exception(test_exception)

    mock_capture.assert_called_once_with(test_exception)


def test_capture_message_calls_sentry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test capture_message calls sentry_sdk.capture_message when initialized."""

    mock_capture = MagicMock()
    monkeypatch.setattr("sentry_sdk.capture_message", mock_capture)
    monkeypatch.setattr(_INITIALIZED_FLAG, True)

    capture_message("test message", level="warning")

    mock_capture.assert_called_once_with("test message", level="warning")


def test_capture_exception_skips_when_not_initialized(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test capture_exception does nothing when Sentry is not initialized."""
    monkeypatch.setattr(
        "sentry_sdk.init", MagicMock(side_effect=Exception("no transport"))
    )

    with patch("sentry_sdk.capture_exception") as mock_capture:
        capture_exception(ValueError("test"))
        mock_capture.assert_not_called()


def test_capture_message_skips_when_not_initialized(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test capture_message does nothing when Sentry is not initialized."""
    monkeypatch.setattr(
        "sentry_sdk.init", MagicMock(side_effect=Exception("no transport"))
    )

    with patch("sentry_sdk.capture_message") as mock_capture:
        capture_message("test")
        mock_capture.assert_not_called()


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        pytest.param(None, DEFAULT_TRACES_SAMPLE_RATE, id="unset"),
        pytest.param("", DEFAULT_TRACES_SAMPLE_RATE, id="blank"),
        pytest.param("0.25", 0.25, id="override"),
        pytest.param("0", 0.0, id="tracing_off"),
        pytest.param("5", 1.0, id="clamped_high"),
        pytest.param("-1", 0.0, id="clamped_low"),
        pytest.param("abc", DEFAULT_TRACES_SAMPLE_RATE, id="invalid_falls_back"),
    ],
)
def test_get_traces_sample_rate(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str | None,
    expected: float,
) -> None:
    """Resolve and clamp the trace sample rate from env."""
    monkeypatch.delenv(TRACES_SAMPLE_RATE_ENV_VAR, raising=False)
    if env_value is not None:
        monkeypatch.setenv(TRACES_SAMPLE_RATE_ENV_VAR, env_value)

    assert _get_traces_sample_rate() == expected


def test_init_sentry_enables_tracing(
    monkeypatch: pytest.MonkeyPatch,
    sentry_env,
) -> None:
    """Tracing must be on, otherwise DB spans are never recorded."""
    monkeypatch.delenv(TRACES_SAMPLE_RATE_ENV_VAR, raising=False)
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)

    assert init_sentry_tracking() is True

    kwargs = init_mock.call_args.kwargs
    assert kwargs["traces_sample_rate"] == DEFAULT_TRACES_SAMPLE_RATE
    assert "traces_sampler" not in kwargs
    assert "disabled_integrations" not in kwargs
    assert kwargs["send_default_pii"] is False
    # Bind values stay out of Sentry; queries.py attaches selected params.
    assert "record_sql_params" not in kwargs.get("_experiments", {})


def test_init_sentry_mcp_mode_disables_starlette_integration(
    monkeypatch: pytest.MonkeyPatch,
    sentry_env,
) -> None:
    """`mcp` mode lets `mcp.server` spans become the trace roots."""
    monkeypatch.delenv(TRACES_SAMPLE_RATE_ENV_VAR, raising=False)
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)

    assert init_sentry_tracking(mode="mcp") is True

    kwargs = init_mock.call_args.kwargs
    disabled = kwargs["disabled_integrations"]
    assert any(isinstance(i, StarletteIntegration) for i in disabled)
    assert kwargs["traces_sample_rate"] == DEFAULT_TRACES_SAMPLE_RATE


def test_init_sentry_webapp_mode_uses_sampler(
    monkeypatch: pytest.MonkeyPatch,
    sentry_env,
) -> None:
    """`webapp` mode installs the sampler instead of a flat rate."""
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)

    assert init_sentry_tracking(mode="webapp") is True

    kwargs = init_mock.call_args.kwargs
    assert kwargs["traces_sampler"] is _webapp_traces_sampler
    assert "traces_sample_rate" not in kwargs


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        pytest.param(None, None, id="unset"),
        pytest.param("", None, id="blank"),
        pytest.param("   ", None, id="whitespace_only"),
        pytest.param(" preview ", "preview", id="stripped"),
    ],
)
def test_get_sentry_environment(
    monkeypatch: pytest.MonkeyPatch,
    env_value: str | None,
    expected: str | None,
) -> None:
    """Unset/blank means undeployed; values are stripped."""
    monkeypatch.delenv(SENTRY_ENVIRONMENT_ENV_VAR, raising=False)
    if env_value is not None:
        monkeypatch.setenv(SENTRY_ENVIRONMENT_ENV_VAR, env_value)

    assert get_sentry_environment() == expected


def test_init_skipped_when_environment_unset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Laptops and CI test runs have no env set; no client is created."""

    monkeypatch.delenv(SENTRY_ENVIRONMENT_ENV_VAR, raising=False)
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)

    assert init_sentry_tracking() is False
    init_mock.assert_not_called()


def test_init_skipped_when_environment_blank(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A whitespace-only env value counts as unset."""

    monkeypatch.setenv(SENTRY_ENVIRONMENT_ENV_VAR, "   ")
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)

    assert init_sentry_tracking() is False
    init_mock.assert_not_called()


def test_init_passes_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The env value flows through to `sentry_sdk.init`."""
    monkeypatch.setenv(SENTRY_ENVIRONMENT_ENV_VAR, "preview")
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)

    assert init_sentry_tracking() is True

    assert init_mock.call_args.kwargs["environment"] == "preview"


@pytest.mark.parametrize(
    "asgi_scope",
    [
        pytest.param(
            {"type": "http", "method": "GET", "path": "/mcp"}, id="listen_stream"
        ),
        pytest.param(
            {"type": "http", "method": "POST", "path": "/mcp"}, id="tool_call_hop"
        ),
        pytest.param(
            {"type": "http", "method": "DELETE", "path": "/mcp"},
            id="session_teardown",
        ),
        pytest.param(
            {
                "type": "http",
                "method": "GET",
                "root_path": "/x",
                "path": "/mcp/",
            },
            id="mounted_with_trailing_slash",
        ),
    ],
)
def test_webapp_traces_sampler_drops_mcp_proxy_route(asgi_scope: dict) -> None:
    """The browser→backend `/mcp` proxy route is transport; never sample it."""
    context = {"asgi_scope": asgi_scope, "parent_sampled": True}

    assert _webapp_traces_sampler(context) == 0.0


def test_webapp_traces_sampler_keeps_page_routes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Page routes fall back to the configured rate."""
    monkeypatch.setenv(TRACES_SAMPLE_RATE_ENV_VAR, "0.25")

    scope = {"type": "http", "method": "GET", "path": "/connector_versions"}
    assert _webapp_traces_sampler({"asgi_scope": scope}) == 0.25


@pytest.mark.parametrize(
    ("parent_sampled", "expected"),
    [
        pytest.param(True, 1.0, id="sampled"),
        pytest.param(False, 0.0, id="dropped"),
    ],
)
def test_webapp_traces_sampler_inherits_parent_decision(
    parent_sampled: bool,
    expected: float,
) -> None:
    """A distributed trace's upstream decision takes precedence."""
    assert _webapp_traces_sampler({"parent_sampled": parent_sampled}) == expected


def test_webapp_traces_sampler_defaults_to_configured_rate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No scope and no parent decision means the env-configured rate applies."""
    monkeypatch.delenv(TRACES_SAMPLE_RATE_ENV_VAR, raising=False)

    assert _webapp_traces_sampler({}) == DEFAULT_TRACES_SAMPLE_RATE


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        pytest.param([], "airbyte-ops", id="no_command"),
        # cyclopts registers the meta-commands in the tree, so they are kept.
        pytest.param(["--version"], "airbyte-ops --version", id="version_meta"),
        pytest.param(["cloud", "--help"], "airbyte-ops cloud --help", id="help_meta"),
        pytest.param(
            ["cloud", "connector", "rollout", "autopilot", "auto-advance"],
            "airbyte-ops cloud connector rollout autopilot auto-advance",
            id="full_depth_autopilot_cron_command",
        ),
        pytest.param(
            ["cloud", "connector", "rollout", "autopilot", "auto-advance", "--dry-run"],
            "airbyte-ops cloud connector rollout autopilot auto-advance",
            id="trailing_option_excluded",
        ),
        pytest.param(
            ["cloud", "organization", "search", "--name-contains", "Acme Corp"],
            "airbyte-ops cloud organization search",
            id="option_key_and_value_excluded",
        ),
        pytest.param(
            ["cloud", "organization", "search", "Acme Corporation"],
            "airbyte-ops cloud organization search",
            id="positional_value_excluded",
        ),
        pytest.param(
            ["cloud", "workspace", "info", "9f2c1a44-0e7b-4f11-bd3e-1a2b3c4d5e6f"],
            "airbyte-ops cloud workspace info",
            id="positional_uuid_excluded",
        ),
        pytest.param(
            ["cloud", "workspace", "info", "-5"],
            "airbyte-ops cloud workspace info",
            id="dash_prefixed_value_excluded",
        ),
        pytest.param(
            ["not-a-command", "at-all"],
            "airbyte-ops",
            id="unknown_command_truncates",
        ),
    ],
)
def test_command_path_excludes_argument_values(argv: list[str], expected: str) -> None:
    """Only registered subcommand names reach the transaction name."""
    from airbyte_ops_mcp.cli.app import _command_path

    assert _command_path(argv) == expected


def test_command_path_never_leaks_a_positional_value() -> None:
    """A positional is where an org name or search string actually arrives."""
    from airbyte_ops_mcp.cli.app import _command_path

    name = _command_path(["cloud", "organization", "search", "Acme Corporation"])

    assert "Acme" not in name
    assert "Corporation" not in name


def test_entrypoint_transaction_is_a_noop_when_sentry_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Callers need no branching when nothing has initialized Sentry."""
    from airbyte_ops_mcp._sentry import entrypoint_transaction

    monkeypatch.setattr("sentry_sdk.is_initialized", lambda: False)
    start_transaction = MagicMock()
    monkeypatch.setattr("sentry_sdk.start_transaction", start_transaction)

    with entrypoint_transaction("airbyte-ops probe", op="cli.command"):
        pass

    start_transaction.assert_not_called()


def test_entrypoint_transaction_does_not_initialize_sentry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`fastmcp_extensions` owns the CLI's client; a second init would fight it."""
    from airbyte_ops_mcp._sentry import entrypoint_transaction

    monkeypatch.setattr("sentry_sdk.is_initialized", lambda: True)
    init_mock = MagicMock()
    monkeypatch.setattr("sentry_sdk.init", init_mock)
    monkeypatch.setattr("sentry_sdk.start_transaction", MagicMock())

    with entrypoint_transaction("airbyte-ops probe", op="cli.command"):
        pass

    init_mock.assert_not_called()


def test_entrypoint_transaction_opens_a_root_transaction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """DB spans need a root, and it must be sampled despite a 0.0 sample rate.

    `fastmcp_extensions` initializes with `traces_sample_rate=0.0`, so without
    an explicit decision every span under this root would be dropped.
    """
    from airbyte_ops_mcp._sentry import entrypoint_transaction

    monkeypatch.setattr("sentry_sdk.is_initialized", lambda: True)
    start_transaction = MagicMock()
    monkeypatch.setattr("sentry_sdk.start_transaction", start_transaction)

    with entrypoint_transaction("airbyte-ops probe", op="cli.command"):
        pass

    start_transaction.assert_called_once_with(
        op="cli.command", name="airbyte-ops probe", sampled=True
    )
