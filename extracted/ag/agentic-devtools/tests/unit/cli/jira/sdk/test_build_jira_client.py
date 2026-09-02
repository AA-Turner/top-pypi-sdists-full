"""Tests for agentic_devtools.cli.jira.sdk.build_jira_client."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

MODULE = "agentic_devtools.cli.jira.sdk"
DUMMY_BEARER_AUTH = "DUMMY_AUTH_HEADER"


class TestBuildJiraClientUrlAndSsl:
    """URL and verify_ssl wiring."""

    def test_passes_url_and_verify_ssl_true(self) -> None:
        """build_jira_client() forwards base URL and verify_ssl=True."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        mock_jira_cls.assert_called_once_with(url="https://jira.example.com", verify_ssl=True)

    def test_passes_url_and_verify_ssl_ca_path(self) -> None:
        """build_jira_client() forwards CA bundle path as verify_ssl."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.corp.local"),
            patch(f"{MODULE}._get_ssl_verify", return_value="/etc/ssl/ca-bundle.pem"),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        mock_jira_cls.assert_called_once_with(url="https://jira.corp.local", verify_ssl="/etc/ssl/ca-bundle.pem")

    def test_passes_verify_ssl_false(self) -> None:
        """build_jira_client() forwards verify_ssl=False."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.test"),
            patch(f"{MODULE}._get_ssl_verify", return_value=False),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        mock_jira_cls.assert_called_once_with(url="https://jira.test", verify_ssl=False)


class TestBuildJiraClientAuthInjection:
    """Authorization header injection."""

    def test_bearer_header_injected(self) -> None:
        """Dummy auth header is set on client._session.headers."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        assert mock_client._session.headers["Authorization"] == DUMMY_BEARER_AUTH

    def test_basic_header_injected(self) -> None:
        """Basic auth header is set on client._session.headers."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(
                f"{MODULE}.get_jira_auth_header",
                return_value="Basic dXNlcjpwYXNz",
            ),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        assert mock_client._session.headers["Authorization"] == "Basic dXNlcjpwYXNz"


class TestBuildJiraClientMissingCredentials:
    """OSError propagation on missing credentials."""

    def test_oserror_propagates(self) -> None:
        """OSError from get_jira_auth_header() propagates unchanged."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(
                f"{MODULE}.get_jira_auth_header",
                side_effect=OSError("Set JIRA_COPILOT_PAT"),
            ),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(OSError, match="JIRA_COPILOT_PAT"):
                build_jira_client()


class TestBuildJiraClientIncompatibleSdk:
    """RuntimeError on incompatible SDK versions."""

    def test_missing_session_raises_runtime_error(self) -> None:
        """RuntimeError when client has no _session attribute."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock(spec=[])  # no _session attribute
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(RuntimeError, match="incompatible"):
                build_jira_client()

    def test_headers_not_mutable_mapping_raises_runtime_error(self) -> None:
        """RuntimeError when _session.headers is not a MutableMapping."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = "not-a-mapping"  # string, not MutableMapping
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(RuntimeError, match="incompatible"):
                build_jira_client()


class TestBuildJiraClientLazyImport:
    """Lazy import behavior."""

    def test_import_module_without_atlassian(self) -> None:
        """Importing sdk.py succeeds without atlassian installed."""
        import importlib

        import agentic_devtools.cli.jira.sdk

        with patch.dict("sys.modules", {"atlassian": None}):
            importlib.reload(agentic_devtools.cli.jira.sdk)

    def test_missing_package_raises_import_error_with_hint(self) -> None:
        """ImportError with install hint when atlassian is not installed."""
        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
            patch.dict("sys.modules", {"atlassian": None}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(ImportError, match="atlassian-python-api") as exc_info:
                build_jira_client()

            assert "pip install" in str(exc_info.value)

    def test_unrelated_module_not_found_reraises(self) -> None:
        """ModuleNotFoundError for a non-atlassian module is re-raised as-is."""
        import builtins
        from typing import Any

        unrelated_err = ModuleNotFoundError("No module named 'foobar'")
        unrelated_err.name = "foobar"
        original_import = builtins.__import__

        def fake_import(name: str, *a: Any, **kw: Any) -> Any:
            if name == "atlassian":
                raise unrelated_err
            return original_import(name, *a, **kw)

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://j.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value=DUMMY_BEARER_AUTH),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with patch("builtins.__import__", side_effect=fake_import):
                with pytest.raises(ModuleNotFoundError, match="foobar"):
                    build_jira_client()


class TestBuildJiraClientVersionDetection:
    """_get_atlassian_version coverage."""

    def test_version_detection_failure_returns_unknown(self) -> None:
        """_get_atlassian_version returns 'unknown' on failure."""
        from agentic_devtools.cli.jira.sdk import _get_atlassian_version

        with patch("importlib.metadata.version", side_effect=Exception("boom")):
            result = _get_atlassian_version()

        assert result == "unknown"


class TestBuildJiraClientWithConfig:
    """Tests for build_jira_client() with optional JiraConfig parameter."""

    def test_uses_config_base_url(self) -> None:
        """When config is provided, uses config.base_url instead of helper."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="https://jira.custom.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client(config=config)

        mock_jira_cls.assert_called_once_with(url="https://jira.custom.com", verify_ssl=True)

    def test_uses_config_ssl_verify(self) -> None:
        """When config is provided, uses config.ssl_verify."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="https://jira.custom.com",
            headers={"Authorization": "******"},
            ssl_verify="/custom/ca-bundle.pem",
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client(config=config)

        mock_jira_cls.assert_called_once_with(url="https://jira.custom.com", verify_ssl="/custom/ca-bundle.pem")

    def test_uses_config_auth_header(self) -> None:
        """When config is provided, uses Authorization from config.headers."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="https://jira.custom.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client(config=config)

        assert mock_client._session.headers["Authorization"] == "******"

    def test_empty_config_auth_header_raises_oserror(self) -> None:
        """An empty Authorization header from config is rejected."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="https://jira.custom.com",
            headers={"Authorization": ""},
            ssl_verify=True,
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(OSError, match="Authorization"):
                build_jira_client(config=config)

    def test_empty_config_base_url_raises_valueerror(self) -> None:
        """An empty base_url from config raises ValueError before creating the client."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(ValueError, match="base_url"):
                build_jira_client(config=config)

        mock_jira_cls.assert_not_called()

    def test_whitespace_only_config_base_url_raises_valueerror(self) -> None:
        """A whitespace-only base_url from config raises ValueError."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="   ",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            with pytest.raises(ValueError, match="base_url"):
                build_jira_client(config=config)

        mock_jira_cls.assert_not_called()

    def test_does_not_call_helpers_when_config_provided(self) -> None:
        """When config is provided, repo helpers are not called."""
        from agentic_devtools.tools.jira import JiraConfig

        config = JiraConfig(
            base_url="https://jira.custom.com",
            headers={"Authorization": "******"},
            ssl_verify=True,
        )
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url") as mock_url,
            patch(f"{MODULE}._get_ssl_verify") as mock_ssl,
            patch(f"{MODULE}.get_jira_auth_header") as mock_auth,
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client(config=config)

        mock_url.assert_not_called()
        mock_ssl.assert_not_called()
        mock_auth.assert_not_called()

    def test_backward_compat_no_args(self) -> None:
        """Calling without arguments still works (backward compat)."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.legacy.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value="******"),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        mock_jira_cls.assert_called_once_with(url="https://jira.legacy.com", verify_ssl=True)

    def test_timeout_set_on_session(self) -> None:
        """Session timeout is set to 30 seconds."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value="******"),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        assert mock_client._session.timeout == 30

    def test_session_request_wrapped_to_inject_timeout(self) -> None:
        """session.request is wrapped so all HTTP calls include the timeout."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        # Capture the original child mock before build_jira_client wraps it.
        original_request_mock = mock_client._session.request

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value="******"),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        # session.request has been replaced by our wrapper.
        wrapped = mock_client._session.request
        assert wrapped is not original_request_mock

        # Calling the wrapper without an explicit timeout injects _SDK_TIMEOUT_SECONDS.
        wrapped("GET", "https://jira.example.com/api")
        original_request_mock.assert_called_once_with("GET", "https://jira.example.com/api", timeout=30)

    def test_session_request_does_not_override_explicit_timeout(self) -> None:
        """Explicit timeout= kwarg is preserved; the wrapper does not override it."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        original_request_mock = mock_client._session.request

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value="******"),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        wrapped = mock_client._session.request
        wrapped("POST", "https://jira.example.com/api", timeout=5)
        original_request_mock.assert_called_once_with("POST", "https://jira.example.com/api", timeout=5)

    def test_session_request_overrides_explicit_timeout_none(self) -> None:
        """Explicit timeout=None is treated as missing and overridden with the default."""
        mock_jira_cls = MagicMock()
        mock_client = MagicMock()
        mock_client._session.headers = {}
        mock_jira_cls.return_value = mock_client

        original_request_mock = mock_client._session.request

        with (
            patch(f"{MODULE}.get_jira_base_url", return_value="https://jira.example.com"),
            patch(f"{MODULE}._get_ssl_verify", return_value=True),
            patch(f"{MODULE}.get_jira_auth_header", return_value="******"),
            patch.dict("sys.modules", {"atlassian": MagicMock(Jira=mock_jira_cls)}),
        ):
            from agentic_devtools.cli.jira.sdk import build_jira_client

            build_jira_client()

        wrapped = mock_client._session.request
        wrapped("GET", "https://jira.example.com/api", timeout=None)
        original_request_mock.assert_called_once_with("GET", "https://jira.example.com/api", timeout=30)
