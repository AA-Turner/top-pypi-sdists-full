"""The three use-case clients: :class:`Istari`, :class:`IstariIntegrations`,
:class:`IstariAdmin`.

Each takes a :class:`~istari_digital_client._configuration.Configuration`, builds the
shared :class:`~istari_digital_client._engine._Engine` (the generated API handles), and exposes its
managers as lazy ``cached_property`` accessors bound to that engine (no version
namespace — the backing API version is internal). See SDK_REDESIGN.md §1/§5.
"""

from __future__ import annotations

from functools import cached_property

from istari_digital_client.sdk._configuration import Configuration

from istari_digital_client.sdk._engine import _Engine
from istari_digital_client.sdk._admin import (
    Infosec,
    Keys,
    Scs,
    Tenants,
    Tokens,
    Usage,
    Users,
)
from istari_digital_client.sdk._common import Jobs, Resources, Systems
from istari_digital_client.sdk._integrations import (
    AgentPools,
    Agents,
    FunctionAuthSecrets,
    Functions,
    Modules,
    OperatingSystems,
    Tools,
)


class _ClosableClient:
    """Mixin giving the clients an explicit lifecycle for their HTTP pool.

    Each client owns a shared connection pool (via its ``_Engine``). Long-running
    processes that build many short-lived clients must be able to release those
    sockets deterministically instead of waiting for GC — call :meth:`close`, or
    use the client as a context manager.
    """

    _engine: _Engine

    def close(self) -> None:
        """Release the client's HTTP connection pool. Safe to call more than once."""
        self._engine.close()

    def __enter__(self):
        """Return the client for use in a ``with`` block."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Release the connection pool on context exit."""
        self.close()


class Istari(_ClosableClient):
    """Common-user entry point: resources, systems (git-like), and jobs.

    .. warning::
       **Beta — API subject to change.** This facade is under active development
       and its surface may change without a deprecation cycle. For production
       code today, prefer the stable legacy client
       (:class:`istari_digital_client.Client` / ``V3Client``); adopt this facade
       when you can absorb breaking changes between releases.
    """

    def __init__(self, config: Configuration, *, list_cache: bool = False) -> None:
        """Create the client from a :class:`Configuration`.

        ``list_cache`` (default off) opts this client into a process-local,
        commit-keyed cache of branch resource listings, so repeated
        ``branch.resources()`` calls within a turn hit the API once instead of
        re-listing every time. Off by default — a no-op for other consumers.
        The cache auto-invalidates when a branch advances and is cleared on any
        mutating call.
        """
        self._engine = _Engine(config, list_cache=list_cache)

    @cached_property
    def resources(self) -> Resources:
        """Resources (models / artifacts / files unified) + revisions/comments/relationships."""
        return Resources(self._engine)

    @cached_property
    def systems(self) -> Systems:
        """Systems — git-like: branches, commits, change requests, workflows."""
        return Systems(self._engine)

    @cached_property
    def jobs(self) -> Jobs:
        """Jobs — submit, monitor, and execute."""
        return Jobs(self._engine)


class IstariIntegrations(_ClosableClient):
    """Integrations entry point: agents, modules, tools, functions, operating systems.

    The surface the Integrations SDK and ``stari`` CLI use to talk to the registry.

    .. warning::
       **Beta — API subject to change.** This facade is under active development
       and its surface may change without a deprecation cycle. For production
       code today, prefer the stable legacy client
       (:class:`istari_digital_client.Client` / ``V3Client``); adopt this facade
       when you can absorb breaking changes between releases.
    """

    def __init__(self, config: Configuration) -> None:
        """Create the client from a :class:`Configuration`."""
        self._engine = _Engine(config)

    @cached_property
    def agents(self) -> Agents:
        """Agents — register and manage."""
        return Agents(self._engine)

    @cached_property
    def agent_pools(self) -> AgentPools:
        """Agent pools."""
        return AgentPools(self._engine)

    @cached_property
    def modules(self) -> Modules:
        """Modules (and module versions)."""
        return Modules(self._engine)

    @cached_property
    def tools(self) -> Tools:
        """Tools (and tool versions)."""
        return Tools(self._engine)

    @cached_property
    def functions(self) -> Functions:
        """Functions (and function versions)."""
        return Functions(self._engine)

    @cached_property
    def function_auth_secrets(self) -> FunctionAuthSecrets:
        """Function auth secrets (execution credentials)."""
        return FunctionAuthSecrets(self._engine)

    @cached_property
    def operating_systems(self) -> OperatingSystems:
        """Operating-system reference data."""
        return OperatingSystems(self._engine)


class IstariAdmin(_ClosableClient):
    """Tenant / platform entry point: sync infra, infosec config, users, tokens, keys.

    .. warning::
       **Beta — API subject to change.** This facade is under active development
       and its surface may change without a deprecation cycle. For production
       code today, prefer the stable legacy client
       (:class:`istari_digital_client.Client` / ``V3Client``); adopt this facade
       when you can absorb breaking changes between releases.
    """

    def __init__(self, config: Configuration) -> None:
        """Create the client from a :class:`Configuration`."""
        self._engine = _Engine(config)

    @cached_property
    def scs(self) -> Scs:
        """Secure Connection Service: connections, received resources, object stores."""
        return Scs(self._engine)

    @cached_property
    def infosec(self) -> Infosec:
        """Configure the available infosec levels."""
        return Infosec(self._engine)

    @cached_property
    def users(self) -> Users:
        """User administration."""
        return Users(self._engine)

    @cached_property
    def tokens(self) -> Tokens:
        """Personal access tokens."""
        return Tokens(self._engine)

    @cached_property
    def keys(self) -> Keys:
        """Principal keypair registration with the Identity Service."""
        return Keys(self._engine)

    @cached_property
    def tenants(self) -> Tenants:
        """Tenant configuration."""
        return Tenants(self._engine)

    @cached_property
    def usage(self) -> Usage:
        """Customer usage metrics."""
        return Usage(self._engine)
