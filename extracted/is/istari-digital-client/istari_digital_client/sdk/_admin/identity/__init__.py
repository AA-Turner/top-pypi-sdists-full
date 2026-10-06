"""``admin.identity``: the identity-service v2 management surface, one manager per tag."""

from __future__ import annotations

from functools import cached_property

from istari_digital_client.sdk._admin.identity.keys import IdentityKeys
from istari_digital_client.sdk._admin.identity.memberships import IdentityMemberships
from istari_digital_client.sdk._admin.identity.oauth import IdentityOAuth
from istari_digital_client.sdk._admin.identity.principals import IdentityPrincipals
from istari_digital_client.sdk._admin.identity.roles import IdentityRoles
from istari_digital_client.sdk._admin.identity.tenants import IdentityTenants
from istari_digital_client.sdk._base import _Manager


class Identity(_Manager):
    """Identity-service tenants, memberships, principals, keys, roles and OAuth over the v2 API.

    Reached via ``admin.identity``. Requires identity-service's v2 API in force
    (``identity_api_version`` ``"v2"``, or the default ``"auto"`` against a server
    that serves ``/api/v2``) and identity-service auth (``identity_service_enabled``
    with credentials, plus a gateway or ``identity_url``). With v1 in force, or
    without that auth, the first operation on any manager below raises
    :class:`ConfigurationError` before an identity request. With v1 in force the only
    key surface is the deprecated ``admin.keys``.

    Managers:

    * ``tenants``: create, read, update, activate, deactivate and default tenants.
    * ``memberships``: grant, revoke and page through tenant memberships.
    * ``principals``: humans, agents and platform services, plus ``me`` and batch resolve.
    * ``keys``: register, list, read and revoke a principal's public keys.
    * ``roles``: the role catalog and grants at tenant and principal scope.
    * ``oauth``: issue and introspect v2 tokens.
    """

    @cached_property
    def tenants(self) -> IdentityTenants:
        """Tenant lifecycle: create, list, get, update, activate, deactivate, set default."""
        return IdentityTenants(self._engine)

    @cached_property
    def memberships(self) -> IdentityMemberships:
        """Tenant memberships: grant, revoke, and page through members by kind."""
        return IdentityMemberships(self._engine)

    @cached_property
    def principals(self) -> IdentityPrincipals:
        """Principals of every kind: ``list``, ``get``, ``me``, ``resolve``, ``activate``, ``deactivate``,
        and the per-kind managers ``humans`` and ``agents``."""
        return IdentityPrincipals(self._engine)

    @cached_property
    def keys(self) -> IdentityKeys:
        """Principal public keys: register, generate_and_register, list, get, revoke."""
        return IdentityKeys(self._engine)

    @cached_property
    def roles(self) -> IdentityRoles:
        """Role catalog, holders, and grants at tenant and principal scope."""
        return IdentityRoles(self._engine)

    @cached_property
    def oauth(self) -> IdentityOAuth:
        """v2 OAuth: issue a token from a client assertion and introspect one as a platform service."""
        return IdentityOAuth(self._engine)


__all__ = ["Identity", "IdentityKeys", "IdentityMemberships", "IdentityOAuth",
           "IdentityPrincipals", "IdentityRoles", "IdentityTenants"]
