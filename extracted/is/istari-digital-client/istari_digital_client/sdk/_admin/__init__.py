"""Managers for the :class:`~istari.IstariAdmin` client.

Tenant / platform configuration: the Secure Connection Service (``scs`` →
connections, object stores), infosec level configuration, users, tokens,
keys, tenants, and usage.
"""

from __future__ import annotations

# Implemented managers
from istari_digital_client.sdk._admin.tokens import Tokens
from istari_digital_client.sdk._admin.users import Users
from istari_digital_client.sdk._admin.usage import Usage
from istari_digital_client.sdk._admin.infosec import Infosec
from istari_digital_client.sdk._admin.scs import Scs
from istari_digital_client.sdk._admin.keys import Keys
from istari_digital_client.sdk._admin.tenants import Tenants

# Rich types
from istari_digital_client.sdk._admin.admin_types import PersonalAccessToken, User


__all__ = [
    "Infosec",
    "Keys",
    "PersonalAccessToken",
    "Scs",
    "Tenants",
    "Tokens",
    "Usage",
    "User",
    "Users",
]
