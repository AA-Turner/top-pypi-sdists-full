"""Read-only approver evidence; repository role is not a token permission grant."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal

from agentic_devtools.cli.ci.credential_roles import AGDT_PR_APPROVER_PAT
from agentic_devtools.cli.ci.github_api_error import GitHubApiError
from agentic_devtools.cli.ci.retry import _provider_rate_limit_error_from_retryable
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

Capability = Literal["identity", "repository_visibility", "repository_role", "review_eligibility"]


class EvidenceStatus(Enum):
    """Whether a read-only capability has been established."""

    VERIFIED = "verified"
    MISSING = "missing"
    DENIED = "denied"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CapabilityEvidence:
    """Safe evidence; values are validated login or fixed repository-role names."""

    status: EvidenceStatus = EvidenceStatus.UNKNOWN
    value: str | None = None
    http_status: int | None = None


@dataclass(frozen=True)
class ApproverPreflightResult:
    """Independent evidence, with no inferred fine-grained review-write grant."""

    identity: CapabilityEvidence = field(default_factory=CapabilityEvidence)
    repository_visibility: CapabilityEvidence = field(default_factory=CapabilityEvidence)
    repository_role: CapabilityEvidence = field(default_factory=CapabilityEvidence)
    review_eligibility: CapabilityEvidence = field(default_factory=CapabilityEvidence)

    @property
    def authenticated_login(self) -> str | None:
        """Return only an authenticated identity, irrespective of review eligibility."""
        return self.identity.value if self.identity.status is EvidenceStatus.VERIFIED else None

    @property
    def blocking_capability(self) -> Capability | None:
        """Return the first missing, denied, unavailable, or unknown requirement."""
        if not self.identity.value:
            return "identity"
        capabilities: tuple[Capability, ...] = (
            "identity",
            "repository_visibility",
            "repository_role",
            "review_eligibility",
        )
        return next(
            (name for name in capabilities if getattr(self, name).status is not EvidenceStatus.VERIFIED),
            None,
        )


def _read_evidence(
    request: Callable[..., str],
    endpoint: str,
    token: str,
) -> tuple[dict[str, Any], CapabilityEvidence]:
    """Read once, converting capability failures but preserving real cooldowns."""
    try:
        response = request(
            endpoint,
            method="GET",
            token=token,
            credential_identity=AGDT_PR_APPROVER_PAT,
            read_pool=False,
        )
        data = json.loads(response)
        if not isinstance(data, dict):
            return {}, CapabilityEvidence()
        return data, CapabilityEvidence(EvidenceStatus.VERIFIED, http_status=200)
    except RetryableError as exc:
        if exc.is_rate_limit:
            raise _provider_rate_limit_error_from_retryable(exc) from exc
        raise
    except ProviderRateLimitError:
        raise
    except GitHubApiError as exc:
        status = EvidenceStatus.DENIED if exc.http_status in {401, 403} else EvidenceStatus.UNAVAILABLE
        return {}, CapabilityEvidence(status, http_status=exc.http_status)
    except Exception:
        # No raw response/exception text is a safe diagnostic at this boundary.
        return {}, CapabilityEvidence()


def _repository_role(data: dict[str, Any]) -> CapabilityEvidence:
    """Read repository permissions without mistaking role for PAT write grants."""
    permissions = data.get("permissions")
    if not isinstance(permissions, dict):
        return CapabilityEvidence()
    for permission, role in (
        ("admin", "admin"),
        ("maintain", "maintain"),
        ("push", "write"),
        ("triage", "triage"),
        ("pull", "read"),
    ):
        if permissions.get(permission) is True:
            status = EvidenceStatus.VERIFIED if role in {"admin", "maintain", "write"} else EvidenceStatus.DENIED
            return CapabilityEvidence(status, role, 200)
    if all(permissions.get(key) is False for key in ("admin", "maintain", "push", "triage", "pull")):
        return CapabilityEvidence(EvidenceStatus.DENIED, http_status=200)
    return CapabilityEvidence()


def collect_approver_preflight(
    request: Callable[..., str],
    base_repo_full_name: str,
    token: str,
) -> ApproverPreflightResult:
    """Collect GET-only evidence for the actual base repository, without retries."""
    if not token.strip():
        return ApproverPreflightResult(identity=CapabilityEvidence(EvidenceStatus.MISSING))
    data, identity = _read_evidence(request, "/user", token)
    if identity.status is EvidenceStatus.VERIFIED:
        login = data.get("login")
        identity = (
            CapabilityEvidence(EvidenceStatus.VERIFIED, login, 200)
            if isinstance(login, str) and re.fullmatch(r"[A-Za-z0-9_-]+(?:\[bot\])?", login)
            else CapabilityEvidence()
        )
    if identity.status is not EvidenceStatus.VERIFIED:
        return ApproverPreflightResult(identity=identity)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/(?!\.\.?$)[A-Za-z0-9_.-]+", base_repo_full_name):
        return ApproverPreflightResult(identity=identity)
    repository, visibility = _read_evidence(request, f"/repos/{base_repo_full_name}", token)
    role = _repository_role(repository) if visibility.status is EvidenceStatus.VERIFIED else CapabilityEvidence()
    # No authoritative read-only source for effective review eligibility is established.
    return ApproverPreflightResult(identity, visibility, role)
