"""Network and credential policy shared by every sandbox type.

Each sandbox type translates this policy to its own mechanism, and refuses at construction a
part it cannot enforce: a sandbox never runs with a weaker policy than the one its author wrote.
"""

import ipaddress
import re
from collections.abc import Sequence
from typing import Annotated, Literal, Self
from urllib.parse import unquote, urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..sandbox.proxy_lifecycle import SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS
from .secrets import SecretOrigin, validate_secret_name

type NetworkMode = Literal["none", "all", "allow"]
NETWORK_MODES: tuple[NetworkMode, ...] = ("none", "all", "allow")

_HOST_LABEL = re.compile(r"(?!-)[a-z0-9-]{1,63}(?<!-)")
# RFC 9110 field-name token.
_HEADER_NAME = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
# Sandbox Proxy enforces the same header, affix and path rules on the rules it stores
# (sandbox-proxy/sandbox_proxy/secret_injection/domain.py): a binding it would refuse is refused here.
_FORBIDDEN_HEADERS = frozenset(
    {
        "connection",
        "content-length",
        "host",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "proxy-connection",
        "te",
        "trailer",
        "transfer-encoding",
        "upgrade",
    }
)


def _normalize_host(entry: str) -> str:
    """Return ``entry`` as a lowercase ``host[:port]``, or raise ``ValueError``."""

    host = entry.strip().lower()
    invalid = ValueError(f"Invalid host {entry!r}: expected a host name or IP address, with an optional :port")
    if not host or any(character in host for character in "/?#@*\\ "):
        raise invalid
    try:
        parts = urlsplit(f"//{host}")
        hostname, port = parts.hostname, parts.port
    except ValueError:
        raise invalid from None
    if hostname is None or port == 0 or host.endswith(":"):
        raise invalid
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        if len(hostname) > 253 or not all(_HOST_LABEL.fullmatch(label) for label in hostname.split(".")):
            raise invalid from None
    return host


class Network(BaseModel):
    """Outbound network of a sandbox. Build it with `none()`, `all()` or `allow(hosts=...)`."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    mode: NetworkMode = "none"
    """``"none"`` for no outbound connection, ``"all"`` for every one, ``"allow"`` for the listed hosts only."""
    hosts: tuple[str, ...] = ()
    """The ``host`` or ``host:port`` entries an ``"allow"`` network reaches over HTTPS; empty otherwise."""

    @classmethod
    def none(cls) -> Self:
        """No outbound connection."""

        return cls(mode="none")

    @classmethod
    def all(cls) -> Self:
        """Every outbound connection."""

        return cls(mode="all")

    @classmethod
    def allow(cls, *, hosts: Sequence[str]) -> Self:
        """Only HTTPS connections to the listed ``host`` or ``host:port`` entries. Wildcards are not accepted.

        Args:
            hosts: The ``host`` or ``host:port`` entries, at least one.
        """

        if isinstance(hosts, str):
            raise TypeError(f"Network.allow takes a sequence of hosts, not a string: write hosts=({hosts!r},)")
        return cls(mode="allow", hosts=tuple(hosts))

    def reaches(self, host: str) -> bool:
        """Whether this network opens connections to ``host``, a ``host[:port]`` entry.

        Args:
            host: The ``host`` or ``host:port`` entry to check.
        """

        return self.mode == "all" or (self.mode == "allow" and _normalize_host(host) in self.hosts)

    @field_validator("hosts")
    @classmethod
    def _validate_hosts(cls, hosts: tuple[str, ...]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(_normalize_host(host) for host in hosts))

    @model_validator(mode="after")
    def _validate_mode(self) -> Self:
        if self.mode == "allow" and not self.hosts:
            raise ValueError("Network.allow needs at least one host; use Network.none() instead")
        if self.mode != "allow" and self.hosts:
            raise ValueError(f"hosts is only valid with Network.allow, not Network.{self.mode}()")
        return self


class HeaderBinding(BaseModel):
    """Add a secret to the HTTPS requests that a sandbox sends to one host.

    ``secret_name`` picks a secret that ``Agent(secrets=...)`` declares. An ``experimental.CustomSandbox`` that lists
    ``HeaderBinding`` in ``supported_header_bindings`` takes it, and adds ``prefix + value + suffix`` as
    the ``header`` of each matching request. For a ``MistralSandbox``, a workspace admin stores such
    rules in Sandbox Proxy: pass ``WorkspaceHeaderBindings``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["header_binding"] = "header_binding"
    """Always ``"header_binding"``."""
    host: str
    """The ``host`` or ``host:port`` whose requests get the header."""
    header: str
    """The name of the header, such as ``"Authorization"``."""
    secret_name: str
    """The name of a secret that ``Agent(secrets=...)`` declares."""
    path_prefix: str = "/"
    """Only requests whose path starts with it get the header."""
    prefix: str = ""
    """The text before the secret's value, such as ``"Bearer "``."""
    suffix: str = ""
    """The text after the secret's value."""

    @field_validator("host")
    @classmethod
    def _validate_host(cls, host: str) -> str:
        return _normalize_host(host)

    @field_validator("header")
    @classmethod
    def _validate_header(cls, header: str) -> str:
        if _HEADER_NAME.fullmatch(header) is None:
            raise ValueError(f"Invalid header name {header!r}")
        if header.lower() in _FORBIDDEN_HEADERS:
            raise ValueError(f"Header {header!r} frames the request or is hop-by-hop; it cannot carry a secret")
        return header

    @field_validator("prefix", "suffix")
    @classmethod
    def _validate_affix(cls, affix: str) -> str:
        # A control character such as CRLF would end the header and start another.
        if any(ord(character) < 32 or ord(character) == 127 for character in affix):
            raise ValueError("prefix and suffix must not contain control characters")
        return affix

    @field_validator("secret_name")
    @classmethod
    def _validate_secret_name(cls, secret_name: str) -> str:
        return validate_secret_name(secret_name)

    @field_validator("path_prefix")
    @classmethod
    def _validate_path_prefix(cls, path_prefix: str) -> str:
        if not path_prefix.startswith("/") or any(character in path_prefix for character in "?#"):
            raise ValueError(f"Invalid path_prefix {path_prefix!r}: it must start with / and have no query")
        if _has_dot_segments(path_prefix):
            raise ValueError(f"Invalid path_prefix {path_prefix!r}: it must not contain . or .. segments")
        return path_prefix


def _has_dot_segments(path: str) -> bool:
    # Decode until stable, so a percent-encoded `..` cannot pass either.
    seen: set[str] = set()
    while path not in seen:
        if any(segment in {".", ".."} for segment in path.split("/")):
            return True
        seen.add(path)
        path = unquote(path)
    return False


# git reaches github.com, and gh reaches the GitHub API.
_GITHUB_HOSTS = ("github.com", "api.github.com")


class GitHubBinding(BaseModel):
    """Give a sandbox Git and GitHub API access as the session user.

    Sandbox Proxy gets a short-lived token for the user's GitHub access, and the sandbox's ``git``
    and ``gh`` use it without seeing it. It does more than a header binding: it also sets up ``git``
    and ``gh``, and checks each request against ``repos``. It takes no ``secret_name`` because the
    token never comes from ``Agent(secrets=...)``. ``repos`` lists the ``owner/repository`` names the
    sandbox can reach, or is ``"all"`` for every repository the user can reach. The token is renewed
    before ``ttl_seconds`` elapse.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["github"] = "github"
    """Always ``"github"``."""
    repos: tuple[str, ...] | Literal["all"]
    """The ``owner/repository`` names the sandbox can reach, or ``"all"`` for every repository the user
    can reach."""
    ttl_seconds: int = Field(default=3600, gt=SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS)
    """How long one token lives; it is renewed before it expires."""
    host: str = "github.com"
    """The GitHub host: ``"github.com"``."""

    @field_validator("repos", mode="before")
    @classmethod
    def _validate_repos(cls, repos: object) -> object:
        if isinstance(repos, str) and repos != "all":
            raise ValueError(f'repos takes a sequence of repositories or "all": write repos=({repos!r},)')
        if isinstance(repos, Sequence) and not isinstance(repos, str) and not repos:
            raise ValueError('repos needs at least one repository; pass repos="all" for every repository')
        return repos

    @field_validator("host")
    @classmethod
    def _validate_host(cls, host: str) -> str:
        if host.strip() != "github.com":
            raise ValueError(f"GitHubBinding supports only github.com, not {host!r}")
        return "github.com"


class MistralApiBinding(BaseModel):
    """Give a sandbox Mistral API access as the session user.

    Sandbox Proxy gives the sandbox a ``MISTRAL_API_KEY`` that only the proxy accepts, and the
    proxy URL as ``MISTRAL_API_HTTP_PROXY``. Clients that send their Mistral API requests through
    that proxy, such as the ``agents`` CLI, act as the session user without seeing a real
    credential. The credential is renewed before ``ttl_seconds`` elapse.

    ``run_as`` names that identity. ``"auto"``, the only value, is the session's user, or, in a
    local run, the user of ``MISTRAL_API_KEY``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["mistral_api"] = "mistral_api"
    """Always ``"mistral_api"``."""
    run_as: Literal["auto"] = "auto"
    """``"auto"``, the only value: the session's user, or, in a local run, the user of
    ``MISTRAL_API_KEY``."""
    ttl_seconds: int = Field(default=3600, gt=SANDBOX_PROXY_RENEWAL_MARGIN_SECONDS)
    """How long one credential lives; it is renewed before it expires."""

    @field_validator("run_as", mode="before")
    @classmethod
    def _validate_run_as(cls, run_as: object) -> object:
        if run_as == "deployment":
            raise ValueError(
                'MistralApiBinding(run_as="deployment") is not supported: Sandbox Proxy gives a service '
                'account no Mistral API access yet. Use run_as="auto", the session user.'
            )
        return run_as


class WorkspaceHeaderBindings(BaseModel):
    """Route a Mistral sandbox through Sandbox Proxy, and apply the rules a workspace admin stored there.

    Each rule adds a workspace secret to the HTTPS requests that match it. The rules and their
    secrets are not in the agent code, and the sandbox never sees the secrets.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    kind: Literal["workspace_header_bindings"] = "workspace_header_bindings"
    """Always ``"workspace_header_bindings"``."""


type SandboxHeaderBinding = Annotated[
    HeaderBinding | GitHubBinding | MistralApiBinding | WorkspaceHeaderBindings,
    Field(discriminator="kind"),
]


def network_blocks(network: Network, binding: SandboxHeaderBinding) -> str | None:
    """Say what ``binding`` needs that ``network`` blocks, or return None when the network reaches it."""

    if isinstance(binding, WorkspaceHeaderBindings):
        return None if network.mode != "none" else "applies rules to outbound connections"
    if isinstance(binding, MistralApiBinding):
        # The API host depends on the deployment, so only a closed network is known to block it.
        return None if network.mode != "none" else "needs network access to the Mistral API"
    hosts = _GITHUB_HOSTS if isinstance(binding, GitHubBinding) else (binding.host,)
    blocked = [host for host in hosts if not network.reaches(host)]
    return f"needs network access to {', '.join(blocked)}" if blocked else None


class SandboxPolicy(BaseModel):
    """The network and header binding of one sandbox, as they travel with its serialized state."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    network: Network = Network()
    header_bindings: tuple[SandboxHeaderBinding, ...] = ()
    # The origin of each secret that header_bindings names, bound by the Harness that holds the sandbox.
    secret_origins: dict[str, SecretOrigin] = Field(default_factory=dict)


__all__ = [
    "NETWORK_MODES",
    "GitHubBinding",
    "Network",
    "NetworkMode",
    "SandboxHeaderBinding",
    "SandboxPolicy",
    "HeaderBinding",
    "MistralApiBinding",
    "WorkspaceHeaderBindings",
    "network_blocks",
]
