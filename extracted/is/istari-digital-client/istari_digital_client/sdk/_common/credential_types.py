"""Rich type for stored credentials (Linked Accounts)."""

from __future__ import annotations

from istari_digital_client.sdk._base import ClientHaving
from istari_digital_client.sdk._generated.v2.models.stored_credential import (
    StoredCredential as _GenStoredCredential,
)


class Credential(_GenStoredCredential, ClientHaving):
    """A stored credential — a Linked Account or shared service account a job can run with.

    Aliases: linked_account linked-account account connection login
    """
