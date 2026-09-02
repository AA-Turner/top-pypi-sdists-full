"""Provider-neutral pull-request discussion resolution contracts and adapters."""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

import requests

from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig
from agentic_devtools.cli.azure_devops.helpers import require_requests

_GITHUB_API = "https://api.github.com"
_GITHUB_TOKEN_NAMES = ("SPECKIT_PR_TOKEN", "COPILOT_GITHUB_TOKEN", "GITHUB_TOKEN", "GH_TOKEN")
_GITHUB_THREAD_ID = re.compile(r"^PRRT_[A-Za-z0-9_-]+$")
_TRANSIENT_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
_ADO_TERMINAL_STATUSES = frozenset({"closed", "fixed", "wontfix", "bydesign"})
_ADO_ORG_URL = re.compile(
    r"^https://(?:dev\.azure\.com/[A-Za-z0-9][A-Za-z0-9._-]*|[A-Za-z0-9][A-Za-z0-9._-]*\.visualstudio\.com)/?$"
)


def discover_github_token(environ: dict[str, str] | None = None) -> str:
    """Return the first non-empty ambient GitHub token."""
    values = os.environ if environ is None else environ
    for name in _GITHUB_TOKEN_NAMES:
        token = values.get(name, "").strip()
        if token:
            return token
    return ""


def sanitize_diagnostic(value: object, secrets: tuple[str, ...] = ()) -> str:
    """Redact credentials and cap provider diagnostics."""
    message = str(value)
    candidates = (*secrets, *(os.environ.get(name, "").strip() for name in _GITHUB_TOKEN_NAMES))
    for secret in candidates:
        if secret:
            message = message.replace(secret, "[REDACTED]")
    return message[:1000]


@dataclass(frozen=True)
class ThreadResolutionRequest:
    """Validated immutable request for resolving one pull-request discussion."""

    provider: str
    repository: str
    pull_request_id: int
    discussion_kind: str = "review_thread"
    thread_id: str | int | None = None
    azure_devops_thread_id: int | None = None
    azure_devops_organization: str | None = None
    azure_devops_project: str | None = None
    github_thread_node_id: str | None = None
    github_comment_id: int | None = None
    requested_operation: str = "resolve"
    dry_run: bool = False

    def __post_init__(self) -> None:
        if self.provider not in {"azure_devops", "github"}:
            raise ValueError("provider must be 'azure_devops' or 'github'")
        if not isinstance(self.repository, str) or not self.repository.strip():
            raise ValueError("repository is required")
        if self.provider == "github" and (
            self.repository.count("/") != 1
            or any(not part.strip() or any(char.isspace() for char in part) for part in self.repository.split("/"))
        ):
            raise ValueError("GitHub repository must be in owner/repo form")
        if not isinstance(self.pull_request_id, int) or isinstance(self.pull_request_id, bool):
            raise ValueError("pull_request_id must be a positive integer")
        if self.pull_request_id <= 0:
            raise ValueError("pull_request_id must be a positive integer")
        if self.discussion_kind != "review_thread":
            raise ValueError("discussion_kind must be 'review_thread'")
        if self.requested_operation != "resolve":
            raise ValueError("requested_operation must be 'resolve'")
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be a boolean")

        if self.thread_id is not None:
            if isinstance(self.thread_id, bool):
                raise ValueError("thread_id must not be a boolean")
            if (
                self.azure_devops_thread_id is not None
                or self.github_thread_node_id is not None
                or self.github_comment_id is not None
            ):
                raise ValueError("thread_id cannot be combined with a provider-native thread identifier")
            if self.provider == "azure_devops":
                native: int | str | bool = self.thread_id
                if isinstance(self.thread_id, str):
                    try:
                        native = int(self.thread_id)
                    except ValueError:
                        pass
                object.__setattr__(self, "azure_devops_thread_id", native)
            elif isinstance(self.thread_id, int) or (isinstance(self.thread_id, str) and self.thread_id.isdigit()):
                object.__setattr__(self, "github_comment_id", int(self.thread_id))
            else:
                object.__setattr__(self, "github_thread_node_id", self.thread_id)

        if self.provider == "azure_devops":
            if self.github_thread_node_id is not None or self.github_comment_id is not None:
                raise ValueError("GitHub identifiers are not valid for Azure DevOps")
            if (
                not isinstance(self.azure_devops_thread_id, int)
                or isinstance(self.azure_devops_thread_id, bool)
                or self.azure_devops_thread_id <= 0
            ):
                raise ValueError("azure_devops_thread_id must be a positive integer")
        else:
            if self.azure_devops_thread_id is not None:
                raise ValueError("Azure DevOps identifiers are not valid for GitHub")
            if self.github_thread_node_id is None and self.github_comment_id is None:
                raise ValueError("github_thread_node_id or github_comment_id is required")
            if self.github_thread_node_id is not None and (
                not isinstance(self.github_thread_node_id, str)
                or not _GITHUB_THREAD_ID.fullmatch(self.github_thread_node_id)
            ):
                raise ValueError("github_thread_node_id must be an opaque PRRT_ review-thread node ID")
            if self.github_comment_id is not None and (
                not isinstance(self.github_comment_id, int)
                or isinstance(self.github_comment_id, bool)
                or self.github_comment_id <= 0
            ):
                raise ValueError("github_comment_id must be a positive integer")
            if self.github_thread_node_id is not None and self.github_comment_id is not None:
                raise ValueError("provide either github_thread_node_id or github_comment_id, not both")

    def as_dict(self) -> dict[str, object]:
        """Return a credential-free JSON-serializable snapshot."""
        return {
            "provider": self.provider,
            "repository": self.repository,
            "pull_request_id": self.pull_request_id,
            "discussion_kind": self.discussion_kind,
            "azure_devops_thread_id": self.azure_devops_thread_id,
            "azure_devops_organization": self.azure_devops_organization,
            "azure_devops_project": self.azure_devops_project,
            "github_thread_node_id": self.github_thread_node_id,
            "github_comment_id": self.github_comment_id,
            "requested_operation": self.requested_operation,
            "dry_run": self.dry_run,
        }


@dataclass(frozen=True)
class ThreadResolutionResult:
    """Normalized result for a provider-native discussion resolution."""

    success: bool
    provider: str
    repository: str
    pull_request_id: int
    discussion_kind: str = "review_thread"
    requested_operation: str = "resolve"
    status: str = "failed"
    prior_state: str = "unknown"
    resulting_state: str = "unknown"
    verification_status: str = "not_checked"
    azure_devops_thread_id: int | None = None
    github_thread_node_id: str | None = None
    github_comment_id: int | None = None
    diagnostics: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, object]:
        """Return a stable, credential-free result envelope."""
        return {
            "success": self.success,
            "provider": self.provider,
            "repository": self.repository,
            "pull_request_id": self.pull_request_id,
            "discussion_kind": self.discussion_kind,
            "requested_operation": self.requested_operation,
            "status": self.status,
            "prior_state": self.prior_state,
            "resulting_state": self.resulting_state,
            "verification_status": self.verification_status,
            "azure_devops_thread_id": self.azure_devops_thread_id,
            "github_thread_node_id": self.github_thread_node_id,
            "github_comment_id": self.github_comment_id,
            "diagnostics": list(self.diagnostics),
        }


@dataclass(frozen=True)
class ThreadResolutionCapability:
    """Describe provider support for discussion resolution."""

    provider: str
    supported: bool = True
    verify: bool = True
    comment_lookup: bool = False


class ThreadResolutionAdapter(Protocol):
    """Adapter protocol implemented by supported code-hosting providers."""

    capability: ThreadResolutionCapability

    def readiness(self, request: ThreadResolutionRequest) -> ThreadResolutionResult:
        """Validate credentials and provider capability before mutation."""

    def resolve(self, request: ThreadResolutionRequest) -> ThreadResolutionResult:
        """Resolve a discussion and verify the resulting provider state."""


def _status_diagnostic(status_code: int) -> str:
    labels = {
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
        422: "invalid_request",
        429: "rate_limited",
    }
    return labels.get(status_code, "provider_error" if status_code < 500 else "provider_unavailable")


_REST_API_STATUS_RE = re.compile(r"\bREST API returned (?P<status>\d{3}):")


def _repo_lookup_diagnostic(exc: RuntimeError) -> str:
    """Map a repository-lookup RuntimeError to a stable diagnostic code.

    Searches for ``REST API returned NNN:`` status fragments in the error
    message produced by ``get_repository_id``.
    """
    for match in _REST_API_STATUS_RE.finditer(str(exc)):
        code = int(match.group("status"))
        if 400 <= code <= 599:
            return _status_diagnostic(code)
    return "provider_unavailable"


def _extract_ado_thread_status(payload: Any) -> str:
    """Return a normalized ADO thread status from a provider response payload."""
    if not isinstance(payload, dict):
        raise _ProviderResponseError("malformed_response")
    status = payload.get("status")
    if not isinstance(status, str) or not status.strip():
        raise _ProviderResponseError("malformed_response")
    return status.strip().lower()


def _extract_github_resolved_flag(payload: Any) -> bool:
    """Return a validated GitHub resolved flag from provider response data."""
    if not isinstance(payload, dict):
        raise _ProviderResponseError("malformed_response")
    is_resolved = payload.get("isResolved")
    if not isinstance(is_resolved, bool):
        raise _ProviderResponseError("malformed_response")
    return is_resolved


class AzureDevOpsThreadResolutionAdapter:  # pragma: no cover
    """Resolve Azure DevOps pull-request threads through the REST API."""

    capability = ThreadResolutionCapability(provider="azure_devops")

    def __init__(
        self,
        config: AzureDevOpsConfig,
        pat: str,
        requests_module: Any | None = None,
        repository_id_resolver: Any | None = None,
    ) -> None:
        self._config = config
        self._requests = requests_module
        self._repository_id_resolver = repository_id_resolver
        org = config.organization.strip()
        if not _ADO_ORG_URL.match(org):
            self._pat = ""
            self._org_invalid = True
        else:
            self._pat = pat.strip()
            self._org_invalid = False

    def readiness(self, request: ThreadResolutionRequest) -> ThreadResolutionResult:
        """Validate the ADO request and PAT without contacting the service."""
        if request.provider != "azure_devops":
            return self._failure(request, "provider_mismatch")
        if self._org_invalid:
            return self._failure(request, "invalid_organization")
        if not self._config.repository.strip():
            return self._failure(request, "repository_required")
        if not self._pat:
            return self._failure(request, "credentials_required")
        if request.repository.strip().lower() != self._config.repository.strip().lower():
            return self._failure(request, "configuration_mismatch")
        if (
            request.azure_devops_organization is not None
            and request.azure_devops_organization.rstrip("/").lower() != self._config.organization.rstrip("/").lower()
        ):
            return self._failure(request, "configuration_mismatch")
        if (
            request.azure_devops_project is not None
            and request.azure_devops_project.strip().lower() != self._config.project.strip().lower()
        ):
            return self._failure(request, "configuration_mismatch")
        return self._result(request, True, "ready")

    def resolve(self, request: ThreadResolutionRequest) -> ThreadResolutionResult:
        """Resolve one numeric ADO thread, avoiding a mutation when already closed."""
        if request.provider != "azure_devops":
            return self.readiness(request)
        if request.dry_run:
            return self._result(request, True, "dry_run", azure_devops_thread_id=None)
        ready = self.readiness(request)
        if not ready.success:
            return ready
        thread_id = request.azure_devops_thread_id
        try:
            requests_module = self._requests or require_requests()
            headers = {
                "Authorization": "Basic " + _basic_auth(self._pat),
                "Content-Type": "application/json",
            }
            try:
                repo_id = (
                    self._repository_id_resolver(self._config)
                    if self._repository_id_resolver is not None
                    else self._lookup_repo_id(requests_module, headers)
                )
            except RuntimeError as exc:
                raise _ProviderResponseError(_repo_lookup_diagnostic(exc)) from exc
            url = self._config.build_api_url(repo_id, "pullRequests", request.pull_request_id, "threads", thread_id)
            before = requests_module.get(url, headers=headers, timeout=30)
            if before.status_code != 200:
                return self._http_failure(request, before.status_code, thread_id=thread_id)
            before_payload = before.json()
            prior = _extract_ado_thread_status(before_payload)
            if prior in _ADO_TERMINAL_STATUSES:
                return self._result(
                    request,
                    True,
                    "already_resolved",
                    prior_state=prior,
                    resulting_state=prior,
                    verification_status="verified",
                )
            patch_diagnostic: str | None = None
            patch_succeeded = False
            try:
                response = requests_module.patch(url, headers=headers, json={"status": "closed"}, timeout=30)
                if response.status_code in {200, 204}:
                    patch_succeeded = True
                elif response.status_code == 429:
                    return self._failure(request, "rate_limited", prior_state=prior)
                elif response.status_code in _TRANSIENT_STATUS_CODES:
                    patch_diagnostic = _status_diagnostic(response.status_code)
                else:
                    return self._http_failure(request, response.status_code, thread_id=thread_id, prior_state=prior)
            except (requests.Timeout, TimeoutError):
                patch_diagnostic = "timeout"
            except (requests.ConnectionError, ConnectionError):
                patch_diagnostic = "provider_unavailable"
            if not patch_succeeded:
                verified_state = (
                    self._verify_ado_thread_closed(requests_module, url, headers)
                    if patch_diagnostic is not None
                    else None
                )
                if verified_state is not None:
                    return self._result(
                        request,
                        True,
                        "resolved",
                        prior_state=prior,
                        resulting_state=verified_state,
                        verification_status="verified",
                    )
                if patch_diagnostic == "timeout":
                    return self._failure(request, "timeout", prior_state=prior)
                return self._failure(request, patch_diagnostic or "provider_error", prior_state=prior)
            after = requests_module.get(url, headers=headers, timeout=30)
            if after.status_code != 200:
                return self._http_failure(request, after.status_code, thread_id=thread_id, prior_state=prior)
            after_payload = after.json()
            resulting = _extract_ado_thread_status(after_payload)
            if resulting not in _ADO_TERMINAL_STATUSES:
                return self._failure(
                    request,
                    "verification_failed",
                    prior_state=prior,
                    resulting_state=resulting or "unknown",
                    verification_status="failed",
                )
            return self._result(
                request,
                True,
                "resolved",
                prior_state=prior,
                resulting_state=resulting,
                verification_status="verified",
            )
        except _ProviderResponseError as exc:
            return self._failure(request, exc.diagnostic)
        except (requests.Timeout, TimeoutError):
            return self._failure(request, "timeout")
        except (requests.ConnectionError, ConnectionError):
            return self._failure(request, "provider_unavailable")
        except (ValueError, TypeError, KeyError, AttributeError):
            return self._failure(request, "malformed_response")
        except Exception as exc:
            encoded_pat = _basic_auth(self._pat) if self._pat else ""
            return self._failure(request, sanitize_diagnostic(exc, (self._pat, encoded_pat)))

    def _lookup_repo_id(self, requests_module: Any, headers: dict[str, str]) -> str:
        """Resolve the ADO repository ID using the adapter's own PAT and transport."""
        from urllib.parse import quote, unquote

        from agentic_devtools.cli.azure_devops.config import API_VERSION

        config = self._config
        project_encoded = quote(unquote(config.project), safe="")
        repository_encoded = quote(unquote(config.repository), safe="")
        url = (
            f"{config.organization.rstrip('/')}/{project_encoded}/_apis/git/repositories/"
            f"{repository_encoded}?api-version={API_VERSION}"
        )
        response = requests_module.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            raise RuntimeError(
                f"REST API returned {response.status_code}: {response.text.strip() or 'No response body'}"
            )
        data = response.json()
        repo_id = (data.get("id") or "").strip()
        if not repo_id:
            raise RuntimeError("REST API response did not include a repository id")
        return repo_id

    def _verify_ado_thread_closed(self, requests_module: Any, url: str, headers: dict[str, str]) -> str | None:
        """Re-read the ADO thread to confirm it was closed despite an ambiguous PATCH response.

        Returns the verified provider status string when the thread is confirmed resolved
        (``"closed"``, ``"fixed"``, ``"wontfix"``, or ``"bydesign"``), or ``None`` if the
        read fails or the state is not resolved.
        """
        try:
            after = requests_module.get(url, headers=headers, timeout=30)
            if after.status_code != 200:
                return None
            status = _extract_ado_thread_status(after.json())
            return status if status in _ADO_TERMINAL_STATUSES else None
        except Exception:
            return None

    def _result(
        self, request: ThreadResolutionRequest, success: bool, status: str, **kwargs: Any
    ) -> ThreadResolutionResult:
        thread_id = kwargs.pop("azure_devops_thread_id", request.azure_devops_thread_id)
        return ThreadResolutionResult(
            success,
            request.provider,
            request.repository,
            request.pull_request_id,
            status=status,
            azure_devops_thread_id=thread_id,
            **kwargs,
        )

    def _failure(self, request: ThreadResolutionRequest, diagnostic: str, **kwargs: Any) -> ThreadResolutionResult:
        return self._result(request, False, "failed", diagnostics=(diagnostic,), **kwargs)

    def _http_failure(
        self, request: ThreadResolutionRequest, status_code: int, **kwargs: Any
    ) -> ThreadResolutionResult:
        return self._failure(request, _status_diagnostic(status_code), **kwargs)


def _basic_auth(pat: str) -> str:
    import base64

    return base64.b64encode(f":{pat}".encode("ascii")).decode("ascii")


class GitHubThreadResolutionAdapter:  # pragma: no cover
    """Resolve GitHub review threads with GraphQL and verify their identity."""

    capability = ThreadResolutionCapability(provider="github", comment_lookup=True)

    def __init__(self, token: str | None = None, request_fn: Any | None = None) -> None:
        self._token = (token if token is not None else discover_github_token()).strip()
        self._request = request_fn or requests.request

    def readiness(self, request: ThreadResolutionRequest) -> ThreadResolutionResult:
        """Validate the GitHub request and ambient token without network access."""
        if request.provider != "github":
            return self._failure(request, "provider_mismatch")
        if not self._token:
            return self._failure(request, "credentials_required")
        return self._result(request, True, "ready")

    def resolve(self, request: ThreadResolutionRequest) -> ThreadResolutionResult:
        """Look up, resolve, and verify one review thread."""
        if request.provider != "github":
            return self.readiness(request)
        if request.dry_run:
            return self._result(request, True, "dry_run", github_thread_node_id=None, github_comment_id=None)
        ready = self.readiness(request)
        if not ready.success:
            return ready
        try:
            thread = self._find_thread(request)
            if thread is None:
                status = "missing_thread_identity" if request.github_comment_id is not None else "not_found"
                return self._failure(request, status)
            node_id = str(thread["id"])
            if not _GITHUB_THREAD_ID.fullmatch(node_id):
                return self._failure(request, "malformed_response")
            prior = _extract_github_resolved_flag(thread)
            if prior:
                return self._result(
                    request,
                    True,
                    "already_resolved",
                    prior_state="resolved",
                    resulting_state="resolved",
                    verification_status="verified",
                    github_thread_node_id=node_id,
                )
            try:
                mutation = self._graphql(_RESOLVE_MUTATION, {"threadId": node_id}, retry_transient=False)
            except _ProviderResponseError as exc:
                if exc.diagnostic in {"provider_unavailable", "rate_limited"} and self._verify_thread_state(
                    request, node_id
                ):
                    return self._result(
                        request,
                        True,
                        "resolved",
                        prior_state="unresolved",
                        resulting_state="resolved",
                        verification_status="verified",
                        github_thread_node_id=node_id,
                    )
                mutation = self._graphql(_RESOLVE_MUTATION, {"threadId": node_id})
            except (requests.Timeout, TimeoutError, requests.ConnectionError, ConnectionError):
                if self._verify_thread_state(request, node_id):
                    return self._result(
                        request,
                        True,
                        "resolved",
                        prior_state="unresolved",
                        resulting_state="resolved",
                        verification_status="verified",
                        github_thread_node_id=node_id,
                    )
                mutation = self._graphql(_RESOLVE_MUTATION, {"threadId": node_id})
            resolved = _extract_github_mutation_thread(mutation)
            if resolved["id"] != node_id:
                return self._failure(
                    request,
                    "verification_failed",
                    prior_state="unresolved",
                    verification_status="failed",
                    github_thread_node_id=node_id,
                )
            if _extract_github_resolved_flag(resolved) is not True:
                return self._failure(
                    request,
                    "verification_failed",
                    prior_state="unresolved",
                    verification_status="failed",
                    github_thread_node_id=node_id,
                )
            verified = self._find_thread(
                ThreadResolutionRequest(
                    provider="github",
                    repository=request.repository,
                    pull_request_id=request.pull_request_id,
                    github_thread_node_id=node_id,
                )
            )
            if verified is None or verified.get("id") != node_id or _extract_github_resolved_flag(verified) is not True:
                return self._failure(
                    request,
                    "verification_failed",
                    prior_state="unresolved",
                    verification_status="failed",
                    github_thread_node_id=node_id,
                )
            return self._result(
                request,
                True,
                "resolved",
                prior_state="unresolved",
                resulting_state="resolved",
                verification_status="verified",
                github_thread_node_id=node_id,
            )
        except _ProviderResponseError as exc:
            return self._failure(request, exc.diagnostic)
        except (requests.Timeout, TimeoutError):
            return self._failure(request, "timeout")
        except (requests.ConnectionError, ConnectionError):
            return self._failure(request, "provider_unavailable")
        except (ValueError, TypeError, KeyError, AttributeError):
            return self._failure(request, "malformed_response")
        except Exception as exc:
            return self._failure(request, sanitize_diagnostic(exc, (self._token,)))

    def _find_thread(self, request: ThreadResolutionRequest) -> dict[str, Any] | None:
        owner, repo_name = request.repository.split("/")
        cursor: str | None = None
        while True:
            variables: dict[str, Any] = {
                "owner": owner,
                "repoName": repo_name,
                "prNumber": request.pull_request_id,
                "threadsCursor": cursor,
            }
            payload = self._graphql(_THREADS_QUERY, variables)
            data = payload.get("data") or {}
            repository = data.get("repository")
            if repository is None:
                raise _ProviderResponseError("not_found")
            pull_request = repository.get("pullRequest")
            if pull_request is None:
                raise _ProviderResponseError("not_found")
            connection = pull_request["reviewThreads"]
            nodes = connection["nodes"]
            for node in nodes:
                if request.github_thread_node_id is not None and node.get("id") == request.github_thread_node_id:
                    return node
                if request.github_comment_id is not None:
                    comments = node.get("comments", {})
                    for comment in comments.get("nodes", []):
                        if comment.get("databaseId") == request.github_comment_id:
                            return node
                    comments_page_info = comments.get("pageInfo", {})
                    if comments_page_info.get("hasNextPage"):
                        comment_cursor = comments_page_info.get("endCursor")
                        if not comment_cursor:
                            raise ValueError("missing comment pagination cursor")
                        if self._find_comment_in_thread(request, node.get("id"), comment_cursor):
                            return node
            page_info = connection["pageInfo"]
            if not page_info["hasNextPage"]:
                return None
            cursor = page_info.get("endCursor")
            if not cursor:
                raise ValueError("missing pagination cursor")

    def _find_comment_in_thread(self, request: ThreadResolutionRequest, thread_id: object, cursor: str) -> bool:
        """Search all comment pages for a numeric review-comment identifier."""
        while True:
            payload = self._graphql(
                _THREAD_COMMENTS_QUERY,
                {"threadId": thread_id, "commentsCursor": cursor},
            )
            comments = payload["data"]["node"]["comments"]
            if any(comment.get("databaseId") == request.github_comment_id for comment in comments["nodes"]):
                return True
            page_info = comments["pageInfo"]
            if not page_info["hasNextPage"]:
                return False
            cursor = page_info.get("endCursor")
            if not cursor:
                raise ValueError("missing comment pagination cursor")

    def _verify_thread_state(self, request: ThreadResolutionRequest, node_id: str) -> bool:
        """Re-read one thread after a transient mutation response."""
        try:
            verified = self._find_thread(
                ThreadResolutionRequest(
                    provider="github",
                    repository=request.repository,
                    pull_request_id=request.pull_request_id,
                    github_thread_node_id=node_id,
                )
            )
            if verified is None or verified.get("id") != node_id:
                return False
            return _extract_github_resolved_flag(verified) is True
        except (
            _ProviderResponseError,
            requests.Timeout,
            TimeoutError,
            requests.ConnectionError,
            ConnectionError,
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
        ):
            return False

    def _graphql(self, query: str, variables: dict[str, Any], *, retry_transient: bool = True) -> dict[str, Any]:
        delay = 1.0
        total_wait = 0.0
        for attempt in range(4):
            response = self._request(
                "POST",
                f"{_GITHUB_API}/graphql",
                headers={
                    "Accept": "application/vnd.github+json",
                    "Authorization": "Bearer " + self._token,
                    "Content-Type": "application/json",
                },
                json={"query": query, "variables": variables},
                timeout=30,
            )
            diagnostic = _status_diagnostic(response.status_code) if response.status_code != 200 else None
            payload = response.json() if response.status_code == 200 else None
            if response.status_code == 200:
                if not isinstance(payload, dict):
                    raise _ProviderResponseError("graphql_error")
                errors = payload.get("errors")
                if not errors:
                    return payload
                diagnostic = _graphql_error_diagnostic(errors)
            if not retry_transient or diagnostic not in {"rate_limited", "provider_unavailable"} or attempt == 3:
                raise _ProviderResponseError(diagnostic or "graphql_error")
            retry_after = getattr(response, "headers", {}).get("Retry-After")
            try:
                wait = max(0.0, float(retry_after)) if retry_after is not None else delay
            except (TypeError, ValueError):
                wait = delay
            wait = min(wait, 15.0 - total_wait)
            if wait <= 0:
                raise _ProviderResponseError(diagnostic)
            time.sleep(wait)
            total_wait += wait
            delay *= 2
        raise AssertionError("unreachable")

    def _result(
        self, request: ThreadResolutionRequest, success: bool, status: str, **kwargs: Any
    ) -> ThreadResolutionResult:
        node_id = kwargs.pop("github_thread_node_id", request.github_thread_node_id)
        comment_id = kwargs.pop("github_comment_id", request.github_comment_id)
        return ThreadResolutionResult(
            success,
            request.provider,
            request.repository,
            request.pull_request_id,
            status=status,
            github_thread_node_id=node_id,
            github_comment_id=comment_id,
            **kwargs,
        )

    def _failure(self, request: ThreadResolutionRequest, diagnostic: str, **kwargs: Any) -> ThreadResolutionResult:
        return self._result(request, False, "failed", diagnostics=(diagnostic,), **kwargs)


class _ProviderResponseError(RuntimeError):  # pragma: no cover
    """Internal sanitized provider failure."""

    def __init__(self, diagnostic: str) -> None:
        super().__init__(diagnostic)
        self.diagnostic = diagnostic


def _extract_github_mutation_thread(mutation: dict[str, Any]) -> dict[str, Any]:
    """Validate and return the GraphQL mutation thread payload."""
    data = mutation.get("data")
    if not isinstance(data, dict):
        raise _ProviderResponseError("malformed_response")
    resolved = data.get("resolveReviewThread")
    if not isinstance(resolved, dict):
        raise _ProviderResponseError("malformed_response")
    thread = resolved.get("thread")
    if not isinstance(thread, dict):
        raise _ProviderResponseError("malformed_response")
    thread_id = thread.get("id")
    if not isinstance(thread_id, str) or not thread_id:
        raise _ProviderResponseError("malformed_response")
    return thread


def _graphql_error_diagnostic(errors: object) -> str:
    """Map recognized GraphQL provider errors to the stable HTTP diagnostics."""
    if isinstance(errors, list):
        for error in errors:
            if not isinstance(error, dict):
                continue
            extensions = error.get("extensions")
            if isinstance(extensions, dict):
                status: object = extensions.get("status")
                if isinstance(status, str) and status.isdigit():
                    status = int(status)
                if isinstance(status, int) and not isinstance(status, bool):
                    diagnostic = _status_diagnostic(status)
                    if diagnostic != "provider_error":
                        return diagnostic
            error_type: object = error.get("type") or (extensions.get("code") if isinstance(extensions, dict) else None)
            if isinstance(error_type, str):
                mapped = {
                    "UNAUTHORIZED": "unauthorized",
                    "FORBIDDEN": "forbidden",
                    "NOT_FOUND": "not_found",
                    "CONFLICT": "conflict",
                    "RATE_LIMITED": "rate_limited",
                    "VALIDATION": "invalid_request",
                    "VALIDATION_FAILED": "invalid_request",
                    "UNPROCESSABLE_ENTITY": "invalid_request",
                    "BAD_USER_INPUT": "invalid_request",
                }.get(error_type.upper())
                if mapped is not None:
                    return mapped
    return "graphql_error"


_THREADS_QUERY = """
query($owner: String!, $repoName: String!, $prNumber: Int!, $threadsCursor: String) {
  repository(owner: $owner, name: $repoName) {
    pullRequest(number: $prNumber) {
      reviewThreads(first: 100, after: $threadsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes { databaseId }
          }
        }
      }
    }
  }
}
"""

_RESOLVE_MUTATION = """
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}
"""

_THREAD_COMMENTS_QUERY = """
query($threadId: ID!, $commentsCursor: String) {
  node(id: $threadId) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes { databaseId }
      }
    }
  }
}
"""

__all__ = [
    "AzureDevOpsThreadResolutionAdapter",
    "GitHubThreadResolutionAdapter",
    "ThreadResolutionAdapter",
    "ThreadResolutionCapability",
    "ThreadResolutionRequest",
    "ThreadResolutionResult",
    "discover_github_token",
    "sanitize_diagnostic",
]
