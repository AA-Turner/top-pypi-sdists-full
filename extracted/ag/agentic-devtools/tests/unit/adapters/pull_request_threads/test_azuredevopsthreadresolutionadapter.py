from __future__ import annotations

from typing import Any

import pytest
import requests

from agentic_devtools.adapters.pull_request_threads import (
    AzureDevOpsThreadResolutionAdapter,
    ThreadResolutionRequest,
)
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig


class _Response:
    def __init__(self, payload: Any, status_code: int = 200) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> Any:
        return self._payload


class _Requests:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def get(self, url: str, **kwargs: Any) -> _Response:
        self.calls.append(("GET", {"url": url, **kwargs}))
        if len(self.calls) == 1:
            return _Response({"status": "active"})
        return _Response({"status": "closed"})

    def patch(self, url: str, **kwargs: Any) -> _Response:
        self.calls.append(("PATCH", {"url": url, **kwargs}))
        return _Response({})


def test_resolves_numeric_thread_and_verifies_closed_status() -> None:
    transport = _Requests()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert [method for method, _ in transport.calls] == ["GET", "PATCH", "GET"]
    assert transport.calls[1][1]["json"] == {"status": "closed"}


def test_already_closed_thread_skips_patch() -> None:
    class _AlreadyClosed(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            return _Response({"status": "closed"})

    transport = _AlreadyClosed()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "already_resolved"
    assert result.verification_status == "verified"
    assert [method for method, _ in transport.calls] == ["GET"]


@pytest.mark.parametrize("status", ["wontFix", "byDesign"])
def test_already_terminal_thread_skips_patch(status: str) -> None:
    class _AlreadyTerminal(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            return _Response({"status": status})

    transport = _AlreadyTerminal()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "already_resolved"
    assert result.prior_state == status.lower()
    assert result.resulting_state == status.lower()
    assert result.verification_status == "verified"
    assert [method for method, _ in transport.calls] == ["GET"]


@pytest.mark.parametrize("status", ["closed ", " closed", " closed "])
def test_already_closed_thread_with_whitespace_in_status_is_recognized(status: str) -> None:
    """A pre-read status containing surrounding whitespace must still be treated as already resolved."""

    class _AlreadyClosedWhitespace(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            return _Response({"status": status})

    transport = _AlreadyClosedWhitespace()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "already_resolved"
    assert [method for method, _ in transport.calls] == ["GET"]


def test_dry_run_resolve_does_not_contact_azure_devops() -> None:
    """A dry-run resolve must return dry_run success without any network calls."""

    class _NoRequests:
        def get(self, *_args: Any, **_kwargs: Any) -> _Response:
            raise AssertionError("dry-run must not contact Azure DevOps")

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
        dry_run=True,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_NoRequests(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "dry_run"
    assert result.azure_devops_thread_id is None
    assert result.as_dict()["azure_devops_thread_id"] is None


def test_unexpected_exception_redacts_encoded_basic_pat() -> None:
    import base64

    encoded = base64.b64encode(b":adapter-secret").decode("ascii")

    class _ExplodingRequests:
        def get(self, url: str, **kwargs: Any) -> _Response:
            raise RuntimeError(f"transport failed with Authorization: Basic {encoded}")

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "adapter-secret",
        requests_module=_ExplodingRequests(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    diagnostic = result.diagnostics[0]
    assert encoded not in diagnostic
    assert "[REDACTED]" in diagnostic


def test_attribute_error_in_response_maps_to_malformed_response() -> None:
    class _BadPayloadRequests:
        def get(self, url: str, **kwargs: Any) -> Any:
            raise AttributeError("'NoneType' object has no attribute 'get'")

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_BadPayloadRequests(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_non_string_verification_status_maps_to_malformed_response() -> None:
    class _BadVerificationStatus(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            if len(self.calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": None})

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_BadVerificationStatus(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)


def test_non_dict_status_payload_maps_to_malformed_response() -> None:
    class _NonDictStatusPayload(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            return _Response(["not-a-dict"])

    transport = _NonDictStatusPayload()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("malformed_response",)
    assert [method for method, _ in transport.calls] == ["GET"]


def test_repository_lookup_failure_maps_to_normalized_diagnostic() -> None:
    def _failing_resolver(_config: Any) -> str:
        raise RuntimeError("REST API returned 401: Unauthorized")

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        repository_id_resolver=_failing_resolver,
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("unauthorized",)


def test_repository_lookup_failure_without_status_maps_to_provider_unavailable() -> None:
    def _failing_resolver(_config: Any) -> str:
        raise RuntimeError("Azure CLI not found")

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        repository_id_resolver=_failing_resolver,
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("provider_unavailable",)


def test_connection_error_maps_to_provider_unavailable() -> None:
    class _ConnectionFailure:
        def get(self, url: str, **kwargs: Any) -> _Response:
            raise requests.ConnectionError("connection reset by peer")

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_ConnectionFailure(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("provider_unavailable",)


def test_default_resolver_uses_adapter_pat_for_repo_lookup() -> None:
    """Adapter's own PAT must be used for repository lookup, not get_pat()."""
    captured_headers: list[dict[str, str]] = []

    class _CapturingRequests:
        def __init__(self) -> None:
            self._thread_calls = 0

        def get(self, url: str, **kwargs: Any) -> _Response:
            captured_headers.append(dict(kwargs.get("headers", {})))
            if "pullRequests" not in url:
                return _Response({"id": "resolved-repo-id"})
            self._thread_calls += 1
            if self._thread_calls == 1:
                return _Response({"status": "active"})
            return _Response({"status": "closed"})

        def patch(self, url: str, **kwargs: Any) -> _Response:
            return _Response({})

    import base64

    expected_auth = "Basic " + base64.b64encode(b":adapter-secret").decode()

    transport = _CapturingRequests()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "adapter-secret",
        requests_module=transport,
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert all(headers.get("Authorization") == expected_auth for headers in captured_headers)


def test_transient_patch_response_rechecks_and_reports_success_if_closed() -> None:
    calls: list[str] = []

    class _TransientPatch(_Requests):
        def patch(self, url: str, **kwargs: Any) -> _Response:
            calls.append("PATCH")
            return _Response({}, status_code=503)

        def get(self, url: str, **kwargs: Any) -> _Response:
            calls.append("GET")
            if len(calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": "closed"})

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_TransientPatch(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.resulting_state == "closed"
    assert result.verification_status == "verified"


def test_transient_patch_response_rechecks_and_reports_fixed_state() -> None:
    """When the provider transitions the thread to 'fixed' concurrently, resulting_state reflects the actual state."""
    calls: list[str] = []

    class _TransientPatch(_Requests):
        def patch(self, url: str, **kwargs: Any) -> _Response:
            calls.append("PATCH")
            return _Response({}, status_code=503)

        def get(self, url: str, **kwargs: Any) -> _Response:
            calls.append("GET")
            if len(calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": "fixed"})

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_TransientPatch(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.resulting_state == "fixed"
    assert result.verification_status == "verified"


def test_successful_patch_accepts_fixed_verification_state() -> None:
    """A concurrent transition to 'fixed' after a successful PATCH remains a verified success."""

    class _FixedAfterPatch(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            if len(self.calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": "fixed"})

    transport = _FixedAfterPatch()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.resulting_state == "fixed"
    assert result.verification_status == "verified"


@pytest.mark.parametrize("status", ["wontFix", "byDesign"])
def test_successful_patch_accepts_additional_terminal_verification_states(status: str) -> None:
    class _TerminalAfterPatch(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            if len(self.calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": status})

    transport = _TerminalAfterPatch()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.resulting_state == status.lower()
    assert result.verification_status == "verified"


@pytest.mark.parametrize("status", ["wontFix", "byDesign"])
def test_transient_patch_recheck_accepts_additional_terminal_states(status: str) -> None:
    calls: list[str] = []

    class _TransientPatch(_Requests):
        def patch(self, url: str, **kwargs: Any) -> _Response:
            calls.append("PATCH")
            return _Response({}, status_code=503)

        def get(self, url: str, **kwargs: Any) -> _Response:
            calls.append("GET")
            if len(calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": status})

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_TransientPatch(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.resulting_state == status.lower()
    assert result.verification_status == "verified"


def test_patch_timeout_rechecks_and_reports_success_if_closed() -> None:
    timeout_calls: list[str] = []

    class _TimeoutOnPatch(_Requests):
        def patch(self, url: str, **kwargs: Any) -> _Response:
            timeout_calls.append("PATCH")
            raise requests.Timeout("timed out")

        def get(self, url: str, **kwargs: Any) -> _Response:
            timeout_calls.append("GET")
            if len(timeout_calls) == 1:
                return _Response({"status": "active"})
            return _Response({"status": "closed"})

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_TimeoutOnPatch(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is True
    assert result.status == "resolved"
    assert result.verification_status == "verified"


def test_patch_timeout_preserves_diagnostic_when_reread_shows_not_closed() -> None:
    class _TimeoutOnPatch(_Requests):
        def patch(self, url: str, **kwargs: Any) -> _Response:
            raise requests.Timeout("timed out")

        def get(self, url: str, **kwargs: Any) -> _Response:
            return _Response({"status": "active"})

    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=_TimeoutOnPatch(),
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("timeout",)


def test_invalid_organization_url_returns_invalid_organization_diagnostic() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=1,
        azure_devops_thread_id=2,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://evil.example.com/org", "project", "repo"),
        "real-pat",
    )

    result = adapter.readiness(request)

    assert result.success is False
    assert result.diagnostics == ("invalid_organization",)


def test_invalid_organization_does_not_store_pat() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=1,
        azure_devops_thread_id=2,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://evil.example.com/org", "project", "repo"),
        "real-pat",
    )

    assert adapter._pat == ""
    assert adapter._org_invalid is True
    result = adapter.resolve(request)
    assert result.success is False
    assert result.diagnostics == ("invalid_organization",)


def test_valid_dev_azure_com_organization_accepts_pat() -> None:
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=1,
        azure_devops_thread_id=2,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/myorg", "project", "repo"),
        "real-pat",
    )

    assert adapter._pat == "real-pat"
    assert adapter._org_invalid is False
    result = adapter.readiness(request)
    assert result.success is True
    assert result.status == "ready"


@pytest.mark.parametrize(
    ("request_repo", "request_org", "request_project"),
    [
        ("other-repo", None, None),
        ("repo", "https://dev.azure.com/other-org", None),
        ("repo", None, "other-project"),
    ],
)
def test_readiness_fails_when_request_does_not_match_adapter_config(
    request_repo: str, request_org: str | None, request_project: str | None
) -> None:
    """readiness() must return configuration_mismatch when coordinates differ from adapter config."""
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository=request_repo,
        pull_request_id=1,
        azure_devops_thread_id=2,
        azure_devops_organization=request_org,
        azure_devops_project=request_project,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/myorg", "project", "repo"),
        "real-pat",
    )

    result = adapter.readiness(request)

    assert result.success is False
    assert result.diagnostics == ("configuration_mismatch",)


def test_patch_rate_limited_returns_directly_without_read_back() -> None:
    """A 429 PATCH response must return rate_limited immediately without a read-back GET."""

    class _RateLimitedPatch(_Requests):
        def get(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("GET", {"url": url, **kwargs}))
            return _Response({"status": "active"})

        def patch(self, url: str, **kwargs: Any) -> _Response:
            self.calls.append(("PATCH", {"url": url, **kwargs}))
            return _Response({}, status_code=429)

    transport = _RateLimitedPatch()
    request = ThreadResolutionRequest(
        provider="azure_devops",
        repository="repo",
        pull_request_id=12,
        azure_devops_thread_id=34,
    )
    adapter = AzureDevOpsThreadResolutionAdapter(
        AzureDevOpsConfig("https://dev.azure.com/org", "project", "repo"),
        "pat",
        requests_module=transport,
        repository_id_resolver=lambda _config: "repo-id",
    )

    result = adapter.resolve(request)

    assert result.success is False
    assert result.diagnostics == ("rate_limited",)
    assert [method for method, _ in transport.calls] == ["GET", "PATCH"]
