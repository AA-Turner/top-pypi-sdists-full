"""What connecting a WhatsApp number carries in and out, with no infrastructure: the request, what Meta verified and the result.

They moved here unchanged from `services/whatsapp_accounts/connect_number.py` (ENG-458) so the application layer of api-chatty can import
them without loading the package `services/whatsapp_accounts`, whose `__init__` imports the Mongo repositories (motor, pymongo, redis).
`services/whatsapp_accounts/connect_number.py` re-exports every name, so the old import path keeps working.
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional

from pydantic import SecretStr

from ...models.utils.types.identifier import StrObjectId
from ...models.whatsapp import WhatsAppAccount

__all__ = ["ConnectMode", "VerifiedConnection", "ConnectRequest", "WabaChange", "ConnectionResult"]


class ConnectMode(StrEnum):
    NEW = "new"
    RECONNECT = "reconnect"


@dataclass(frozen=True)
class VerifiedConnection:
    """What Meta confirmed for an Embedded Signup, server side."""
    phone_number_id: str
    display_phone_number: str
    waba_id: str
    token: SecretStr
    verified_name: str = ""
    portfolio_id: Optional[str] = None
    portfolio_name: str = ""
    waba_name: str = ""
    is_coexistence: bool = False


@dataclass(frozen=True)
class ConnectRequest:
    company_id: StrObjectId
    mode: ConnectMode
    #: RECONNECT: the account that takes the number.
    account_id: Optional[StrObjectId] = None
    #: NEW: the name the user gave the account. Defaults to Meta's verified name.
    name: Optional[str] = None


@dataclass(frozen=True)
class WabaChange:
    previous_waba_id: str
    new_waba_id: str
    portfolio_changed: bool


@dataclass(frozen=True)
class ConnectionResult:
    account: WhatsAppAccount
    created: bool
    previous_phone_number_id: Optional[str]
    waba_change: Optional[WabaChange]
