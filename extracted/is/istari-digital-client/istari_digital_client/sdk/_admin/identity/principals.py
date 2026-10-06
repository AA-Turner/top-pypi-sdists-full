"""Identity-service principals (admin.identity.principals)."""

from __future__ import annotations

from functools import cached_property
from typing import Any, List

from pydantic import BaseModel

from istari_digital_client.identity.v2.models.batch_resolve_request import BatchResolveRequest
from istari_digital_client.identity.v2.models.create_agent_request import CreateAgentRequest
from istari_digital_client.identity.v2.models.create_human_request import CreateHumanRequest
from istari_digital_client.identity.v2.models.update_agent_request import UpdateAgentRequest
from istari_digital_client.identity.v2.models.update_human_request import UpdateHumanRequest
from istari_digital_client.sdk._admin.identity._paging import paginate_cursor
from istari_digital_client.sdk._admin.identity._requests import build_request
from istari_digital_client.sdk._base import Page, _Manager


class _KindPrincipals(_Manager):
    """One principal kind: list, create, get, update, deactivate on its own subpath."""

    _list = _create = _get = _update = _deactivate = ""
    _request: type[BaseModel]
    _update_request: type[BaseModel]

    def list(self, *, tenant_id: str | None = None, limit: int | None = None, **filters: Any) -> Page[Any]:
        """Page through principals of this kind, optionally within one tenant.

        Extra keyword arguments are the kind's generated list filters, passed through
        unchanged: ``upstream_provider`` / ``upstream_user_id`` / ``email`` for humans,
        ``client_id`` and ``username`` for agents, ``active`` and ``role`` for every kind.
        """
        api = self._engine.identity_v2_api
        tenant_ids = [tenant_id] if tenant_id else None
        return paginate_cursor(lambda c: self._call(
            getattr(api, self._list), tenant_id=tenant_ids, cursor=c, limit=limit, **filters))

    def create(self, **fields: Any) -> Any:
        """Create a principal of this kind.

        Mutates: true
        """
        req = build_request(self._request, fields, verb="create")
        return self._call(getattr(self._engine.identity_v2_api, self._create), req)

    def get(self, principal_id: str) -> Any:
        """Read one principal of this kind."""
        return self._call(getattr(self._engine.identity_v2_api, self._get), principal_id)

    def update(self, principal_id: str, **fields: Any) -> Any:
        """Patch a principal of this kind.

        Mutates: true
        """
        req = build_request(self._update_request, fields, verb="update")
        return self._call(getattr(self._engine.identity_v2_api, self._update), principal_id, req)

    def deactivate(self, principal_id: str) -> Any:
        """Deactivate a principal of this kind; returns the deactivated record.

        Mutates: true
        """
        return self._call(getattr(self._engine.identity_v2_api, self._deactivate), principal_id)


class IdentityHumans(_KindPrincipals):
    """Human principals."""

    _list, _create, _get, _update, _deactivate = "list_humans", "create_human", "get_human", "update_human", "deactivate_human"
    _request, _update_request = CreateHumanRequest, UpdateHumanRequest


class IdentityAgents(_KindPrincipals):
    """Agent principals."""

    _list, _create, _get, _update, _deactivate = "list_agents", "create_agent", "get_agent", "update_agent", "deactivate_agent"
    _request, _update_request = CreateAgentRequest, UpdateAgentRequest


class IdentityPrincipals(_Manager):
    """Principals across kinds, with per-kind sub-managers."""

    @cached_property
    def humans(self) -> IdentityHumans:
        """Human principals."""
        return IdentityHumans(self._engine)

    @cached_property
    def agents(self) -> IdentityAgents:
        """Agent principals."""
        return IdentityAgents(self._engine)

    def list(self, *, tenant_id: str | None = None, kind: str | None = None, limit: int | None = None) -> Page[Any]:
        """Page through every principal kind as the ``Principal`` union."""
        tenant_ids = [tenant_id] if tenant_id else None
        return paginate_cursor(lambda c: self._call(
            self._engine.identity_v2_api.list_principals, tenant_id=tenant_ids, kind=kind, cursor=c, limit=limit))

    def get(self, principal_id: str) -> Any:
        """Read one principal of any kind."""
        return self._call(self._engine.identity_v2_api.get_principal, principal_id)

    def me(self) -> Any:
        """The authenticated principal."""
        return self._call(self._engine.identity_v2_api.get_current_principal)

    def resolve(self, ids: List[str]) -> Any:
        """Resolve many principal ids in one call."""
        return self._call(self._engine.identity_v2_api.batch_resolve_principals, BatchResolveRequest(ids=ids))

    def activate(self, principal_id: str) -> Any:
        """Return a deactivated principal to service.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.activate_principal, principal_id)

    def deactivate(self, principal_id: str) -> Any:
        """Deactivate a principal of any kind.

        Mutates: true
        """
        return self._call(self._engine.identity_v2_api.deactivate_principal, principal_id)
