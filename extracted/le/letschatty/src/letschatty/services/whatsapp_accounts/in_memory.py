"""In-memory implementations of the WhatsApp account ports.

For tests of any consumer (api-chatty, lambdas): wire an `AccountDirectory` without a database.
Same contracts as the Mongo adapters, including `claim` rejecting another company's number."""
from typing import Any, Dict, List, Optional

from ...models.whatsapp.time import utc_now
from ...models.whatsapp import (
    DefaultAccountExists,
    NumberAlreadyClaimed,
    WhatsAppAccount,
    WhatsAppAccountStatus,
    WhatsAppBusinessAccount,
    WhatsAppNumber,
)


class InMemoryWhatsAppAccountRepository:
    def __init__(self, *accounts: WhatsAppAccount):
        self.by_id: Dict[str, WhatsAppAccount] = {a.id: a for a in accounts}
        self.reads = 0

    async def get(self, account_id: str) -> Optional[WhatsAppAccount]:
        self.reads += 1
        return self.by_id.get(account_id)

    async def get_default(self, company_id: str) -> Optional[WhatsAppAccount]:
        return next((a for a in self.by_id.values() if a.company_id == company_id and a.is_default), None)

    async def list_by_company(self, company_id: str) -> List[WhatsAppAccount]:
        return [a for a in self.by_id.values() if a.company_id == company_id]

    async def list_by_waba(self, waba_id: str) -> List[WhatsAppAccount]:
        return [a for a in self.by_id.values() if a.waba_id == waba_id]

    async def insert(self, account: WhatsAppAccount) -> None:
        if account.is_default and any(a.is_default and a.company_id == account.company_id for a in self.by_id.values()):
            raise DefaultAccountExists(company_id=str(account.company_id))
        self.by_id[account.id] = account

    async def delete(self, account_id: str) -> None:
        self.by_id.pop(account_id, None)

    async def update_fields(self, account_id: str, fields: Dict[str, Any]) -> None:
        # Validated like a Mongo round trip: callers pass stored values (a token as str).
        current = self.by_id[account_id]
        self.by_id[account_id] = WhatsAppAccount.model_validate({**current.model_dump(by_alias=True), **fields})

    async def list_additional_connected(self) -> List[WhatsAppAccount]:
        return [a for a in self.by_id.values() if not a.is_default and a.status == WhatsAppAccountStatus.CONNECTED]

    async def move_waba(self, account_id: str, from_waba_id: str, to_waba_id: str) -> bool:
        account = self.by_id.get(account_id)
        if account is None or account.waba_id != from_waba_id:
            return False
        self.by_id[account_id] = account.model_copy(update={"waba_id": to_waba_id})
        return True

    async def set_default(self, company_id: str, account_id: str) -> None:
        for a in list(self.by_id.values()):
            if a.company_id == company_id:
                self.by_id[a.id] = a.model_copy(update={"is_default": a.id == account_id})


class InMemoryWhatsAppNumberRepository:
    def __init__(self, *numbers: WhatsAppNumber):
        self.by_id: Dict[str, WhatsAppNumber] = {n.phone_number_id: n for n in numbers}
        self.reads = 0

    async def get(self, phone_number_id: str) -> Optional[WhatsAppNumber]:
        self.reads += 1
        return self.by_id.get(phone_number_id)

    async def claim(self, number: WhatsAppNumber) -> WhatsAppNumber:
        holder = self.by_id.get(number.phone_number_id)
        if holder is not None and holder.company_id != number.company_id and holder.is_live:
            raise NumberAlreadyClaimed("taken")
        self.by_id[number.phone_number_id] = number.model_copy(update={"active": True, "until": None, "taken_down_at": None})
        return self.by_id[number.phone_number_id]

    async def live_by_digits(self, digits: str) -> List[WhatsAppNumber]:
        return [n for n in self.by_id.values() if n.digits == digits and n.is_live]

    async def take_down(self, phone_number_id: str) -> None:
        self.by_id[phone_number_id] = self.by_id[phone_number_id].model_copy(update={"taken_down_at": utc_now(), "active": False})

    async def deactivate(self, phone_number_id: str) -> None:
        self.by_id[phone_number_id] = self.by_id[phone_number_id].model_copy(update={"active": False})

    async def list_by_account(self, account_id: str) -> List[WhatsAppNumber]:
        return [n for n in self.by_id.values() if n.account_id == account_id]


class InMemoryWhatsAppBusinessAccountRepository:
    def __init__(self, *wabas: WhatsAppBusinessAccount):
        self.items: Dict[tuple, WhatsAppBusinessAccount] = {(w.company_id, w.waba_id): w for w in wabas}

    async def get(self, company_id: str, waba_id: str) -> Optional[WhatsAppBusinessAccount]:
        return self.items.get((company_id, waba_id))

    async def upsert(self, waba: WhatsAppBusinessAccount) -> WhatsAppBusinessAccount:
        self.items[(waba.company_id, waba.waba_id)] = waba
        return waba

    async def list_by_company(self, company_id: str) -> List[WhatsAppBusinessAccount]:
        return [w for (c, _), w in self.items.items() if c == company_id]


class InMemoryCache:
    def __init__(self):
        self.values: Dict[str, str] = {}

    async def get(self, key: str) -> Optional[str]:
        return self.values.get(key)

    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        self.values[key] = value

    async def delete(self, key: str) -> None:
        self.values.pop(key, None)

    async def delete_many(self, keys: List[str]) -> None:
        for key in keys:
            self.values.pop(key, None)

    async def get_many(self, keys: List[str]) -> List[Optional[str]]:
        return [self.values.get(k) for k in keys]


class InMemoryWhatsAppPortfolioRepository:
    def __init__(self):
        self.items: Dict[tuple, Any] = {}

    async def get(self, company_id: str, portfolio_id: str):
        return self.items.get((company_id, portfolio_id))

    async def upsert(self, portfolio):
        self.items[(portfolio.company_id, portfolio.portfolio_id)] = portfolio
        return portfolio

    async def list_by_company(self, company_id: str):
        return [p for (c, _), p in self.items.items() if c == company_id]


def in_memory_directory() -> "AccountDirectory":
    """An empty directory: every company behaves as one without accounts (legacy single number)."""
    from .directory import AccountDirectory
    return AccountDirectory(
        InMemoryWhatsAppAccountRepository(),
        InMemoryWhatsAppNumberRepository(),
        InMemoryWhatsAppBusinessAccountRepository(),
        InMemoryCache(),
    )
