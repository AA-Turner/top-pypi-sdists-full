"""How a client authenticates (``auth``), and which organization and project it addresses (``scope``)."""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import ClassVar, Literal, TypeAlias

__all__ = [
    "Auth",
    "AuthMode",
    "AutoAuth",
    "Credential",
    "AsyncCredential",
    "NoAuth",
    "OrganizationAuth",
    "ProjectAuth",
    "Scope",
    "UserAuth",
    "auth_from_credentials",
]

#: A key, or a function returning one, called once per logical call.
Credential: TypeAlias = str | Callable[[], str]

#: What ``AsyncComposio`` additionally accepts: a provider that is awaited.
AsyncCredential: TypeAlias = str | Callable[[], str] | Callable[[], Awaitable[str]]

AuthMode = Literal["none", "project", "user", "organization", "auto"]

#: Every character ``httpx`` sends unchanged: Latin-1, with no CR, LF or NUL.
_UNSENDABLE = re.compile(r"[\r\n\x00]|[^\x00-\xff]")


def is_sendable_key(value: object) -> bool:
    return isinstance(value, str) and value.strip() != "" and _UNSENDABLE.search(value) is None


def _check_credential(credential: object, owner: str) -> None:
    if callable(credential):
        return
    if not isinstance(credential, str):
        raise TypeError(f"`{owner}` must be a string or a function returning one.")
    if not is_sendable_key(credential):
        raise ValueError(
            f"`{owner}` must contain a non-whitespace character and no line break, NUL or "
            "character outside Latin-1."
        )


@dataclass(frozen=True, slots=True)
class NoAuth:
    """No Composio credential. ``x-api-key`` and friends are ordinary headers."""

    mode: ClassVar[AuthMode] = "none"


@dataclass(frozen=True, slots=True)
class ProjectAuth:
    """A project API key (``ApiKeyAuth``, ``x-api-key``) on every request."""

    credential: AsyncCredential = field(repr=False)
    mode: ClassVar[AuthMode] = "project"

    def __post_init__(self) -> None:
        _check_credential(self.credential, "ProjectAuth.credential")


@dataclass(frozen=True, slots=True)
class UserAuth:
    """A user API key (``UserApiKeyAuth``, ``x-user-api-key``) on every request."""

    credential: AsyncCredential = field(repr=False)
    mode: ClassVar[AuthMode] = "user"

    def __post_init__(self) -> None:
        _check_credential(self.credential, "UserAuth.credential")


@dataclass(frozen=True, slots=True)
class OrganizationAuth:
    """An organization API key (``OrgApiKeyAuth``, ``x-org-api-key``) on every request."""

    credential: AsyncCredential = field(repr=False)
    mode: ClassVar[AuthMode] = "organization"

    def __post_init__(self) -> None:
        _check_credential(self.credential, "OrganizationAuth.credential")


@dataclass(frozen=True, slots=True)
class AutoAuth:
    """One of the configured credentials per request, chosen from the
    operation's declared security schemes, falling back to the project key.
    At least one is required."""

    project: AsyncCredential | None = field(default=None, repr=False)
    user: AsyncCredential | None = field(default=None, repr=False)
    organization: AsyncCredential | None = field(default=None, repr=False)
    mode: ClassVar[AuthMode] = "auto"

    def __post_init__(self) -> None:
        if self.project is None and self.user is None and self.organization is None:
            raise ValueError("`AutoAuth` needs at least one of `project`, `user` and `organization`.")
        for name in ("project", "user", "organization"):
            value = getattr(self, name)
            if value is not None:
                _check_credential(value, f"AutoAuth.{name}")


#: Every way a client authenticates.
Auth: TypeAlias = NoAuth | ProjectAuth | UserAuth | OrganizationAuth | AutoAuth

AUTH_TYPES = (NoAuth, ProjectAuth, UserAuth, OrganizationAuth, AutoAuth)


def _check_id(value: object, name: str) -> None:
    if not isinstance(value, str) or value == "" or value != value.strip() or _UNSENDABLE.search(value):
        raise ValueError(
            f"`Scope.{name}` must be a non-empty string with no surrounding whitespace, line break or NUL."
        )


@dataclass(frozen=True, slots=True)
class Scope:
    """The organization and project requests are routed to, sent as
    ``x-org-id`` and ``x-project-id``. A project without its organization is
    valid: the API derives the organization from the project."""

    organization_id: str | None = None
    project_id: str | None = None

    def __post_init__(self) -> None:
        if self.organization_id is None and self.project_id is None:
            raise ValueError("`Scope` needs an `organization_id`, a `project_id`, or both.")
        if self.organization_id is not None:
            _check_id(self.organization_id, "organization_id")
        if self.project_id is not None:
            _check_id(self.project_id, "project_id")


def auth_from_credentials(
    *,
    project: AsyncCredential | None = None,
    user: AsyncCredential | None = None,
    organization: AsyncCredential | None = None,
) -> Auth:
    """One credential is that fixed mode, several are ``AutoAuth``, none is ``NoAuth``."""
    present = [value for value in (project, user, organization) if value is not None]
    if len(present) == 0:
        return NoAuth()
    if len(present) > 1:
        return AutoAuth(project=project, user=user, organization=organization)
    if project is not None:
        return ProjectAuth(project)
    if user is not None:
        return UserAuth(user)
    assert organization is not None
    return OrganizationAuth(organization)
