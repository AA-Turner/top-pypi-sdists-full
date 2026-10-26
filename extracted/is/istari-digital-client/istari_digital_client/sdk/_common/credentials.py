"""Credentials manager (Istari common-user surface).

Stored credentials are the Linked Accounts a user connects under *Linked
Accounts* in the web app, plus any organization service accounts shared with
them. A job binds one to a function's ``auth_info`` input; see
``Jobs.create(auth_bindings=...)``. Distinct from
``IstariIntegrations.function_auth_secrets`` (the older per-function secrets).
"""

from __future__ import annotations

from istari_digital_client.sdk._base import Page, _Manager
from istari_digital_client.sdk._common.credential_types import Credential


class Credentials(_Manager):
    """Manager for stored credentials (Linked Accounts): list.

    Aliases: linked_accounts linked-account account connection login oauth
    """

    def list(self, *, auth_integration_id: str | None = None) -> Page[Credential]:
        """List the stored credentials the caller can bind to a job.

        Aliases: linked_accounts accounts logins

        ``auth_integration_id`` narrows the list to one app integration (one
        third-party application, as configured by an administrator).

        Returns Credential objects with fields: id, name (the label shown under
        Linked Accounts), status ("active" | "revoked" | "expired" — only an
        active one can run a job), auth_type, auth_integration_id,
        account_identity (the account at the provider, when known),
        owner_user_id (None for a shared service account), tenant_id, created.

        The underlying API returns a plain list; it is wrapped in a single Page.
        """
        items = self._call(
            self._engine.v2_api.list_credentials,
            auth_integration_id=auth_integration_id,
        )
        bound = [Credential._bind(dto, mgr=self) for dto in items]
        return Page(bound, fetch_next=None, total=len(bound))
