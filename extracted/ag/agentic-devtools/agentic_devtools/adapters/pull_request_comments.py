"""Provider-neutral pull-request issue-comment contracts and transports."""

from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from inspect import Signature, signature
from typing import Any, Protocol
from urllib.parse import quote, urlsplit

import requests

from agentic_devtools.cli.azure_devops.auth import get_auth_headers
from agentic_devtools.cli.azure_devops.config import AzureDevOpsConfig

GITHUB_PR_COMMENT_TOKEN = "SPECKIT_PR_TOKEN"  # nosec B105 - environment variable name, not a credential
GITHUB_PR_COMMENT_TOKEN_FALLBACKS = ("GITHUB_TOKEN", "GH_TOKEN")
_GITHUB_API = "https://api.github.com"
_GITHUB_WRITE_SCOPES: frozenset[str] = frozenset({"repo", "public_repo"})


@dataclass(frozen=True)
class PullRequestCommentRequest:
    """Validated provider-neutral request for a pull-request comment."""

    provider: str
    repository: str
    pull_request_id: int
    content: str
    path: str | None = None
    line: int | None = None
    end_line: int | None = None
    resolve_after_posting: bool = True
    dry_run: bool = False
    idempotency_marker: str | None = None
    organization: str | None = None
    project: str | None = None

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
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("content is required")
        if self.path is not None and (not isinstance(self.path, str) or not self.path.strip()):
            raise ValueError("path must be a non-empty string")
        if self.line is not None and (not isinstance(self.line, int) or isinstance(self.line, bool) or self.line <= 0):
            raise ValueError("line must be a positive integer")
        if self.end_line is not None and (
            not isinstance(self.end_line, int) or isinstance(self.end_line, bool) or self.end_line <= 0
        ):
            raise ValueError("end_line must be a positive integer")
        if self.path is None and (self.line is not None or self.end_line is not None):
            raise ValueError("line and end_line require path")
        if self.end_line is not None and self.line is None:
            raise ValueError("end_line requires line")
        if self.end_line is not None and self.line is not None and self.end_line < self.line:
            raise ValueError("end_line must not be less than line")
        if not isinstance(self.resolve_after_posting, bool):
            raise ValueError("resolve_after_posting must be a boolean")
        if not isinstance(self.dry_run, bool):
            raise ValueError("dry_run must be a boolean")
        if self.idempotency_marker is not None and not isinstance(self.idempotency_marker, str):
            raise ValueError("idempotency_marker must be a string")
        if self.organization is not None and (not isinstance(self.organization, str) or not self.organization.strip()):
            raise ValueError("organization must be a non-empty string")
        if self.project is not None and (not isinstance(self.project, str) or not self.project.strip()):
            raise ValueError("project must be a non-empty string")


@dataclass(frozen=True)
class PullRequestCommentResult:
    """Equivalent success or failure result for either provider."""

    success: bool
    provider: str
    status: str
    comment_id: str = ""
    thread_id: str = ""
    url: str = ""
    error: str = ""

    def as_dict(self) -> dict[str, object]:
        """Return a JSON-serializable result."""
        return {
            "success": self.success,
            "provider": self.provider,
            "status": self.status,
            "comment_id": self.comment_id,
            "thread_id": self.thread_id,
            "url": self.url,
            "error": self.error,
        }


@dataclass(frozen=True)
class PullRequestCommentCapability:
    """Describe the anchoring and resolution features of a provider."""

    provider: str
    general_comments: bool = True
    file_anchoring: bool = False
    resolution: bool = False
    idempotency: bool = False


class PullRequestCommentAdapter(Protocol):
    """Transport protocol implemented by pull-request comment providers."""

    capability: PullRequestCommentCapability

    def readiness(self, request: PullRequestCommentRequest) -> PullRequestCommentResult:
        """Validate credentials and provider access without posting."""

    def add_comment(self, request: PullRequestCommentRequest) -> PullRequestCommentResult:
        """Post or reconcile a pull-request comment."""


def discover_github_token(environ: dict[str, str] | None = None) -> str:
    """Discover the cloud-agent GitHub token without interactive authentication."""
    values = os.environ if environ is None else environ
    for name in (GITHUB_PR_COMMENT_TOKEN, *GITHUB_PR_COMMENT_TOKEN_FALLBACKS):
        token = values.get(name, "").strip()
        if token:
            return token
    return ""


def _sanitize_error(error: object, token: str = "") -> str:  # nosec B107 - empty sentinel, not a credential
    """Return provider diagnostics with credentials removed."""
    message = str(error)
    if token:
        message = message.replace(token, "[REDACTED]")
    for secret_name in (GITHUB_PR_COMMENT_TOKEN, *GITHUB_PR_COMMENT_TOKEN_FALLBACKS):
        value = os.environ.get(secret_name, "").strip()
        if value:
            message = message.replace(value, "[REDACTED]")
    message = re.sub(r"(?i)(Authorization:\s*\S+\s+)\S+", r"\1[REDACTED]", message)
    message = re.sub(r"(?i)(['\"]authorization['\"]\s*:\s*['\"]\S+\s+)\S+(['\"])", r"\1[REDACTED]\2", message)
    return message[:1000]


class AzureDevOpsPullRequestCommentAdapter:
    """Adapter for Azure DevOps pull-request threads."""

    capability = PullRequestCommentCapability(
        provider="azure_devops",
        file_anchoring=True,
        resolution=True,
    )

    def __init__(
        self,
        config: AzureDevOpsConfig,
        pat: str,
        post_fn: Any | None = None,
        readiness_fn: Any | None = None,
    ) -> None:
        self._config = config
        self._pat = pat.strip()
        self._post_fn = post_fn
        self._readiness_fn = readiness_fn

    def readiness(self, request: PullRequestCommentRequest) -> PullRequestCommentResult:
        """Validate the ADO request and credential before mutation."""
        if request.provider != self.capability.provider:
            return PullRequestCommentResult(False, request.provider, "not_ready", error="provider mismatch")
        if not self._config.repository.strip():
            return PullRequestCommentResult(
                False, request.provider, "not_ready", error="Azure DevOps repository is required"
            )
        if not self._pat:
            return PullRequestCommentResult(
                False,
                request.provider,
                "not_ready",
                error="Azure DevOps credentials are required",
            )
        try:
            if self._readiness_fn is None:
                repository_url = (
                    f"{self._config.organization.rstrip('/')}/"
                    f"{quote(self._config.project, safe='')}/_apis/git/repositories/"
                    f"{quote(self._config.repository, safe='')}"
                )
                pull_request_url = f"{repository_url}/pullRequests/{request.pull_request_id}?api-version=7.0"
                repository_response = requests.get(
                    f"{repository_url}?api-version=7.0",
                    headers=get_auth_headers(self._pat),
                    timeout=30,
                )
                pull_request_response = requests.get(pull_request_url, headers=get_auth_headers(self._pat), timeout=30)
            else:
                readiness_signature: Signature | None
                try:
                    readiness_signature = signature(self._readiness_fn)
                except (TypeError, ValueError):
                    readiness_signature = None
                parameters = () if readiness_signature is None else tuple(readiness_signature.parameters.values())
                supports_pull_request_argument = readiness_signature is not None and (
                    any(parameter.kind == parameter.VAR_POSITIONAL for parameter in parameters) or len(parameters) >= 3
                )
                if supports_pull_request_argument:
                    pull_request_response = self._readiness_fn(self._config, self._pat, request.pull_request_id)
                    repository_response = pull_request_response
                else:
                    repository_response = self._readiness_fn(self._config, self._pat)
                    pull_request_response = repository_response
            if repository_response.status_code != 200:
                return PullRequestCommentResult(
                    False,
                    request.provider,
                    "not_ready",
                    error=f"Azure DevOps readiness check failed ({repository_response.status_code})",
                )
            if pull_request_response.status_code != 200:
                return PullRequestCommentResult(
                    False,
                    request.provider,
                    "not_ready",
                    error=f"Azure DevOps pull-request readiness check failed ({pull_request_response.status_code})",
                )
        except Exception as exc:
            return PullRequestCommentResult(False, request.provider, "not_ready", error=_sanitize_error(exc, self._pat))
        return PullRequestCommentResult(
            True,
            request.provider,
            "ready_unverified",
        )

    def add_comment(self, request: PullRequestCommentRequest) -> PullRequestCommentResult:
        """Post a new ADO thread and preserve its IDs."""
        if request.dry_run:
            return PullRequestCommentResult(True, request.provider, "dry_run")
        ready = self.readiness(request)
        if not ready.success:
            return ready
        try:
            if self._post_fn is None:
                from agentic_devtools.tools.azure_devops import add_pull_request_comment

                self._post_fn = add_pull_request_comment
            result = self._post_fn(
                config=self._config,
                pat=self._pat,
                pull_request_id=request.pull_request_id,
                content=request.content,
                path=request.path,
                line=request.line,
                end_line=request.end_line,
                resolve_after_posting=request.resolve_after_posting,
            )
            raw_comment_id = result.get("comment_id")
            raw_thread_id = result.get("thread_id")
            if not (isinstance(raw_thread_id, int) and not isinstance(raw_thread_id, bool) and raw_thread_id > 0):
                return PullRequestCommentResult(
                    False, request.provider, "failed", error="Azure DevOps response did not contain a thread ID"
                )
            valid_comment_id = (
                isinstance(raw_comment_id, int) and not isinstance(raw_comment_id, bool) and raw_comment_id > 0
            )
            return PullRequestCommentResult(
                True,
                request.provider,
                "created",
                comment_id=str(raw_comment_id) if valid_comment_id else "",
                thread_id=str(raw_thread_id),
            )
        except Exception as exc:
            return PullRequestCommentResult(False, request.provider, "failed", error=_sanitize_error(exc, self._pat))


class GitHubPullRequestCommentAdapter:
    """Adapter for GitHub pull-request issue comments."""

    capability = PullRequestCommentCapability(
        provider="github",
        idempotency=True,
    )

    def __init__(
        self,
        token: str | None = None,
        request_fn: Any | None = None,
    ) -> None:
        self._token = (token if token is not None else discover_github_token()).strip()
        self._request = request_fn or requests.request

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + self._token,
            "Content-Type": "application/json",
        }

    def _request_with_retry(self, method: str, url: str, **kwargs: Any) -> Any:
        """Retry transient GitHub responses and transport failures."""
        for attempt in range(3):
            try:
                response = self._request(method, url, **kwargs)
            except requests.exceptions.RequestException:
                if attempt == 2:
                    raise
                time.sleep(2**attempt)
                continue
            if not self._is_retryable_response(response):
                return response
            if attempt < 2:
                time.sleep(self._retry_delay(response, attempt))
        return response

    @staticmethod
    def _retry_delay(response: Any, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        try:
            return max(0.0, min(float(retry_after), 30.0)) if retry_after is not None else float(2**attempt)
        except (TypeError, ValueError):
            return float(2**attempt)

    @staticmethod
    def _is_retryable_response(response: Any) -> bool:
        if response.status_code in {429, 500, 502, 503, 504}:
            return True
        if response.status_code == 403:
            headers = response.headers
            return "Retry-After" in headers or headers.get("X-RateLimit-Remaining") == "0"
        return False

    def _find_marker(self, request: PullRequestCommentRequest, marker: str) -> PullRequestCommentResult | None:
        page_url: str | None = self._comments_url(request)
        while page_url:
            comments = self._request_with_retry(
                "GET",
                page_url,
                headers=self._headers(),
                params={"per_page": 100} if page_url == self._comments_url(request) else None,
                timeout=30,
            )
            if comments.status_code != 200:
                raise RuntimeError(f"GitHub idempotency check failed ({comments.status_code}): {comments.text}")
            payload = comments.json()
            if not isinstance(payload, list):
                raise RuntimeError(
                    f"GitHub idempotency check failed: expected a list of comments, got {type(payload).__name__}"
                )
            for comment in payload:
                if not isinstance(comment, dict):
                    continue
                body = comment.get("body")
                if not isinstance(body, str) or marker not in body:
                    continue
                raw_comment_id = comment.get("id")
                if isinstance(raw_comment_id, bool):
                    continue
                if isinstance(raw_comment_id, int):
                    comment_id = str(raw_comment_id)
                elif isinstance(raw_comment_id, str):
                    comment_id = raw_comment_id.strip()
                else:
                    continue
                if not comment_id:
                    continue
                comment_url = comment.get("html_url")
                if not isinstance(comment_url, str):
                    comment_url = ""
                return PullRequestCommentResult(
                    True,
                    request.provider,
                    "already_exists",
                    comment_id=comment_id,
                    url=comment_url,
                )
            links = getattr(comments, "links", {})
            page_url = links.get("next", {}).get("url") if isinstance(links, dict) else None
            if page_url is None:
                link_header = comments.headers.get("Link", "")
                match = re.search(r'<([^>]+)>;\s*rel="next"', link_header) if isinstance(link_header, str) else None
                page_url = match.group(1) if match else None
            if page_url is not None and not self._is_expected_github_api_url(page_url):
                raise RuntimeError("GitHub idempotency check failed: unexpected pagination host")
        return None

    @staticmethod
    def _is_expected_github_api_url(url: str) -> bool:
        expected = urlsplit(_GITHUB_API)
        candidate = urlsplit(url)
        return candidate.scheme == expected.scheme and candidate.netloc.lower() == expected.netloc.lower()

    @staticmethod
    def _comments_url(request: PullRequestCommentRequest) -> str:
        return f"{_GITHUB_API}/repos/{quote(request.repository, safe='/')}/issues/{request.pull_request_id}/comments"

    def readiness(self, request: PullRequestCommentRequest) -> PullRequestCommentResult:
        """Check token availability and read access before a write."""
        if request.provider != self.capability.provider:
            return PullRequestCommentResult(False, request.provider, "not_ready", error="provider mismatch")
        if "/" not in request.repository or any(part.strip() == "" for part in request.repository.split("/", 1)):
            return PullRequestCommentResult(False, request.provider, "not_ready", error="repository must be owner/repo")
        if not self._token:
            return PullRequestCommentResult(
                False,
                request.provider,
                "not_ready",
                error=f"{GITHUB_PR_COMMENT_TOKEN} is required with pull-request comment write permission",
            )
        try:
            url = f"{_GITHUB_API}/repos/{quote(request.repository, safe='/')}/pulls/{request.pull_request_id}"
            response = self._request_with_retry("GET", url, headers=self._headers(), timeout=30)
            if response.status_code != 200:
                return PullRequestCommentResult(
                    False,
                    request.provider,
                    "not_ready",
                    error=_sanitize_error(
                        f"GitHub readiness check failed ({response.status_code}): {response.text}", self._token
                    ),
                )
            scopes_header = response.headers.get("X-OAuth-Scopes", "")
            if scopes_header:
                granted = {s.strip() for s in scopes_header.split(",")}
                if not granted & _GITHUB_WRITE_SCOPES:
                    return PullRequestCommentResult(
                        False,
                        request.provider,
                        "not_ready",
                        error="GitHub token lacks write scope (repo or public_repo required to post comments)",
                    )
            comments = self._request_with_retry(
                "GET",
                self._comments_url(request),
                headers=self._headers(),
                params={"per_page": 1},
                timeout=30,
            )
            if comments.status_code not in (200, 204):
                return PullRequestCommentResult(
                    False,
                    request.provider,
                    "not_ready",
                    error=_sanitize_error(
                        f"GitHub comment readability check failed ({comments.status_code}): {comments.text}",
                        self._token,
                    ),
                )
            return PullRequestCommentResult(
                True,
                request.provider,
                "ready_unverified",
            )
        except Exception as exc:
            return PullRequestCommentResult(
                False, request.provider, "not_ready", error=_sanitize_error(exc, self._token)
            )

    def add_comment(self, request: PullRequestCommentRequest) -> PullRequestCommentResult:
        """Post a general issue comment on the pull request."""
        if any(value is not None for value in (request.path, request.line, request.end_line)):
            return PullRequestCommentResult(
                False,
                request.provider,
                "unsupported",
                error="GitHub pull-request issue comments do not support file anchoring",
            )
        if request.dry_run:
            return PullRequestCommentResult(True, request.provider, "dry_run")
        ready = self.readiness(request)
        if not ready.success:
            return ready

        marker = request.idempotency_marker
        try:
            url = self._comments_url(request)
            body = request.content
            if marker:
                existing = self._find_marker(request, marker)
                if existing is not None:
                    return existing
                body = f"{body}\n\n{marker}"
                for attempt in range(3):  # pragma: no branch
                    try:
                        response = self._request("POST", url, headers=self._headers(), json={"body": body}, timeout=30)
                    except requests.exceptions.RequestException:
                        existing = self._find_marker(request, marker)
                        if existing is not None:
                            return existing
                        if attempt == 2:
                            raise
                        time.sleep(2**attempt)
                        continue
                    if not self._is_retryable_response(response):
                        break
                    existing = self._find_marker(request, marker)
                    if existing is not None:
                        return existing
                    if attempt == 2:
                        break
                    time.sleep(self._retry_delay(response, attempt))
            else:
                response = self._request(
                    "POST",
                    url,
                    headers=self._headers(),
                    json={"body": body},
                    timeout=30,
                )
            if response.status_code not in (200, 201):
                return PullRequestCommentResult(
                    False,
                    request.provider,
                    "failed",
                    error=_sanitize_error(
                        f"GitHub comment failed ({response.status_code}): {response.text}", self._token
                    ),
                )
            payload = response.json()
            comment_id = payload.get("id") if isinstance(payload, dict) else None
            if not isinstance(payload, dict) or not (
                (isinstance(comment_id, int) and not isinstance(comment_id, bool) and comment_id > 0)
                or (isinstance(comment_id, str) and comment_id.strip())
            ):
                return PullRequestCommentResult(
                    False, request.provider, "failed", error="GitHub response did not contain a comment ID"
                )
            comment_url = payload.get("html_url")
            return PullRequestCommentResult(
                True,
                request.provider,
                "created",
                comment_id=str(comment_id),
                url=comment_url if isinstance(comment_url, str) else "",
            )
        except Exception as exc:
            return PullRequestCommentResult(False, request.provider, "failed", error=_sanitize_error(exc, self._token))
