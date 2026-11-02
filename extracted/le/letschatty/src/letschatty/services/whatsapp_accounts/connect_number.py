"""Connecting a WhatsApp number to a company, and administering its accounts.

The user who connects a number decides whether it is a NEW account or RECONNECTS an existing
one (decision 2); it is never inferred. The company's first connection needs no choice: it
creates the default account.

Meta is not called here. The caller verifies the Embedded Signup result with Meta (token
exchange, `debug_token`, the WABA's owner portfolio) and passes the confirmed ids as a
`VerifiedConnection`; nothing the browser sent is trusted.
"""
from dataclasses import dataclass
from enum import StrEnum
from typing import List, Optional

from bson import ObjectId
from pydantic import SecretStr

from ...models.utils.types.identifier import StrObjectId
from ...models.whatsapp import (
    AccountCannotBeDefault,
    CannotDisconnectDefaultAccount,
    WhatsAppAccount,
    WhatsAppAccountNotFound,
    WhatsAppAccountStatus,
    WhatsAppBusinessAccount,
    WhatsAppNumber,
    WhatsAppPortfolio,
)
from ...models.whatsapp.exceptions import CannotTakeDownDefaultNumber, NumberAlreadyClaimed
from ...models.whatsapp.whatsapp_number import known_number_digits
from ...models.whatsapp.time import utc_now
from .directory import AccountDirectory
from .repositories import (
    WhatsAppAccountRepository,
    WhatsAppBusinessAccountRepository,
    WhatsAppNumberRepository,
    WhatsAppPortfolioRepository,
)


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


class NumberAlreadyInAccount(NumberAlreadyClaimed):
    """The number is already the current number of one of the company's accounts."""


class ConnectNumber:
    def __init__(
        self,
        accounts: WhatsAppAccountRepository,
        numbers: WhatsAppNumberRepository,
        wabas: WhatsAppBusinessAccountRepository,
        portfolios: WhatsAppPortfolioRepository,
        directory: AccountDirectory,
    ):
        self.accounts = accounts
        self.numbers = numbers
        self.wabas = wabas
        self.portfolios = portfolios
        self.directory = directory

    async def plan(self, request: ConnectRequest, connection: VerifiedConnection) -> Optional[WabaChange]:
        """What a RECONNECT would change, to warn the user BEFORE they confirm (decision 3).
        Raises `NumberAlreadyClaimed` for a number of another company: the caller has not
        touched Meta yet, and must not (registering would re-register that company's number)."""
        reconnects = request.mode == ConnectMode.RECONNECT and request.account_id is not None
        await self._ensure_number_is_free(request.company_id, request.account_id if reconnects else None, connection)
        if not reconnects:
            return None
        account = await self._own_account(request.company_id, request.account_id)
        return _waba_change(account, connection)

    async def execute(self, request: ConnectRequest, connection: VerifiedConnection) -> ConnectionResult:
        existing = await self.accounts.list_by_company(request.company_id)
        mode = ConnectMode.NEW if not existing else request.mode
        await self._register_meta_assets(request.company_id, connection)
        if mode == ConnectMode.NEW:
            return await self._create(request, connection, is_first=not existing, existing=existing)
        if request.account_id is None:
            raise WhatsAppAccountNotFound("Reconnect needs the account to reconnect", company_id=str(request.company_id))
        account = await self._own_account(request.company_id, request.account_id)
        await self._ensure_number_is_free(request.company_id, account.id, connection)
        return await self._reconnect(account, connection)

    async def _create(
        self, request: ConnectRequest, connection: VerifiedConnection, is_first: bool, existing: List[WhatsAppAccount]
    ) -> ConnectionResult:
        holder = next((a for a in existing if a.phone_number_id == connection.phone_number_id), None)
        if holder is not None:
            raise NumberAlreadyInAccount(
                f"This number is already the account «{holder.name}». Reconnect it instead.", company_id=request.company_id
            )
        now = utc_now()
        account = WhatsAppAccount(
            _id=str(ObjectId()),
            company_id=request.company_id,
            name=(request.name or connection.verified_name or connection.display_phone_number).strip(),
            is_default=is_first,
            status=WhatsAppAccountStatus.CONNECTED,
            phone_number_id=connection.phone_number_id,
            display_phone_number=connection.display_phone_number,
            waba_id=connection.waba_id,
            portfolio_id=connection.portfolio_id,
            token=connection.token,
            is_coexistence=connection.is_coexistence,
            connected_at=now,
        )
        # A number already in Chatty (any company, any WABA) is rejected before anything is written.
        await self._ensure_number_is_free(request.company_id, None, connection)
        # Account first, number second: a failed insert (two requests creating the default at
        # once) must never leave the number routed to an account that does not exist.
        await self.accounts.insert(account)
        try:
            await self.numbers.claim(self._number(account))
        except NumberAlreadyClaimed:
            await self.accounts.delete(account.id)  # another company claimed it in between
            raise
        await self.directory.invalidate_number(connection.phone_number_id)
        return ConnectionResult(account=account, created=True, previous_phone_number_id=None, waba_change=None)

    async def _reconnect(self, account: WhatsAppAccount, connection: VerifiedConnection) -> ConnectionResult:
        waba_change = _waba_change(account, connection)
        previous = account.phone_number_id if account.phone_number_id != connection.phone_number_id else None
        updated = account.model_copy(
            update={
                "phone_number_id": connection.phone_number_id,
                "display_phone_number": connection.display_phone_number,
                "waba_id": connection.waba_id,
                "portfolio_id": connection.portfolio_id or account.portfolio_id,
                "token": connection.token,
                "is_coexistence": connection.is_coexistence,
                "status": WhatsAppAccountStatus.CONNECTED,
                "connected_at": utc_now(),
                "disconnected_at": None,
            }
        )
        await self.numbers.claim(self._number(updated))
        if previous:
            # The previous number stays, inactive: late statuses and messages still reach this account.
            await self.numbers.deactivate(previous)
            await self.directory.invalidate_number(previous)
        await self.accounts.update_fields(
            account.id,
            {
                "phone_number_id": updated.phone_number_id,
                "display_phone_number": updated.display_phone_number,
                "waba_id": updated.waba_id,
                "portfolio_id": updated.portfolio_id,
                "token": updated.token.get_secret_value(),
                "is_coexistence": updated.is_coexistence,
                "status": updated.status.value,
                "connected_at": updated.connected_at,
                "disconnected_at": None,
            },
        )
        await self.directory.invalidate_number(connection.phone_number_id)
        return ConnectionResult(account=updated, created=False, previous_phone_number_id=previous, waba_change=waba_change)

    async def _ensure_number_is_free(self, company_id: StrObjectId, account_id: Optional[StrObjectId], connection: VerifiedConnection) -> None:
        """A number goes into Chatty only if no account anywhere uses it or still receives from it
        (current or previous number), looked up by id AND by digits: a number moved to another
        WABA gets a new id. The one exception is going back to it from its own account. A number
        taken down in Meta is free."""
        holders = []
        by_id = await self.numbers.get(connection.phone_number_id)
        if by_id is not None and by_id.is_live:
            holders.append(by_id)
        digits = known_number_digits(connection.display_phone_number)
        if digits:
            holders += [n for n in await self.numbers.live_by_digits(digits) if n.phone_number_id != connection.phone_number_id]
        for holder in holders:
            if account_id is not None and holder.account_id == account_id:
                continue
            if holder.company_id != company_id:
                raise NumberAlreadyClaimed("This number is already connected to another company in Chatty", company_id=str(company_id))
            other = await self.accounts.get(holder.account_id)
            name = other.name if other else "otra cuenta"
            raise NumberAlreadyInAccount(
                f"This number is already the account «{name}» of this company. Reconnect that account instead.", company_id=str(company_id)
            )

    async def _register_meta_assets(self, company_id: StrObjectId, connection: VerifiedConnection) -> None:
        if connection.portfolio_id:
            await self.portfolios.upsert(WhatsAppPortfolio(company_id=company_id, portfolio_id=connection.portfolio_id, name=connection.portfolio_name))
        existing = await self.wabas.get(company_id, connection.waba_id)
        if existing is None:
            await self.wabas.upsert(
                WhatsAppBusinessAccount(company_id=company_id, waba_id=connection.waba_id, portfolio_id=connection.portfolio_id, name=connection.waba_name)
            )

    async def _own_account(self, company_id: StrObjectId, account_id: StrObjectId) -> WhatsAppAccount:
        account = await self.accounts.get(account_id)
        if account is None or account.company_id != company_id:
            raise WhatsAppAccountNotFound(f"Account {account_id} is not from company {company_id}", company_id=str(company_id))
        return account

    @staticmethod
    def _number(account: WhatsAppAccount) -> WhatsAppNumber:
        return WhatsAppNumber(
            _id=account.phone_number_id,
            company_id=account.company_id,
            account_id=account.id,
            display_phone_number=account.display_phone_number,
        )


class AccountAdministration:
    """Rename, pick the default, disconnect. Permission checks belong to the caller."""

    def __init__(self, accounts: WhatsAppAccountRepository, directory: AccountDirectory):
        self.accounts = accounts
        self.directory = directory

    async def rename(self, company_id: StrObjectId, account_id: StrObjectId, name: str) -> WhatsAppAccount:
        account = await self._own(company_id, account_id)
        clean = name.strip()
        if not clean:
            raise ValueError("An account needs a name")
        await self.accounts.update_fields(account.id, {"name": clean})
        return account.model_copy(update={"name": clean})

    async def make_default(self, company_id: StrObjectId, account_id: StrObjectId) -> WhatsAppAccount:
        """Only an account that can send: everything that does not pick a number goes out through
        the default one. The screen already hides it; this is the rule, for every caller."""
        account = await self._own(company_id, account_id)
        if not account.can_send:
            raise AccountCannotBeDefault(company_id=str(company_id))
        await self.accounts.set_default(company_id, account.id)
        return account.model_copy(update={"is_default": True})

    async def disconnect(self, company_id: StrObjectId, account_id: StrObjectId) -> WhatsAppAccount:
        """The account stops sending; its chats stay readable and its numbers keep routing. The
        default one only when it is the company's only account (decision 13-oct): with others,
        another one becomes the default first."""
        account = await self._own(company_id, account_id)
        if account.is_default and len(await self.accounts.list_by_company(company_id)) > 1:
            raise CannotDisconnectDefaultAccount(company_id=str(company_id))
        now = utc_now()
        await self.accounts.update_fields(account.id, {"status": WhatsAppAccountStatus.DISCONNECTED.value, "disconnected_at": now})
        return account.model_copy(update={"status": WhatsAppAccountStatus.DISCONNECTED, "disconnected_at": now})

    async def follow_waba_migration(self, account_id: StrObjectId, waba_id: str) -> Optional[WhatsAppAccount]:
        """Meta moved the account's number to another WABA (webhooks for it now come with that
        WABA as `entry.id`). The account follows: its templates and continuous-conversation
        template live in the new WABA from now on. Conditional, so among the concurrent webhooks
        that notice it exactly one moves the account; the others get None. None too when there
        is nothing to move."""
        account = await self.accounts.get(account_id)
        if account is None or not waba_id or account.waba_id == waba_id:
            return None
        if not await self.accounts.move_waba(account.id, account.waba_id, waba_id):
            return None
        # Only when the company does not have that WABA yet: an upsert would blank its template
        # and dataset settings.
        if await self.directory.wabas.get(account.company_id, waba_id) is None:
            await self.directory.wabas.upsert(
                WhatsAppBusinessAccount(company_id=account.company_id, waba_id=waba_id, portfolio_id=account.portfolio_id)
            )
        return account.model_copy(update={"waba_id": waba_id})

    async def check_take_down(self, company_id: StrObjectId, account_id: StrObjectId, phone_number_id: str) -> WhatsAppAccount:
        """Whether the number can be taken down; raises if not. Called BEFORE Meta is touched."""
        account = await self._own(company_id, account_id)
        number = await self.directory.numbers.get(phone_number_id)
        if number is None or number.account_id != account.id or not number.is_live:
            raise WhatsAppAccountNotFound(f"Number {phone_number_id} is not a live number of account {account_id}", company_id=str(company_id))
        if phone_number_id == account.phone_number_id and account.is_default and len(await self.accounts.list_by_company(company_id)) > 1:
            raise CannotTakeDownDefaultNumber(company_id=str(company_id))
        return account

    async def take_down(self, company_id: StrObjectId, account_id: StrObjectId, phone_number_id: str) -> WhatsAppAccount:
        """The number was taken down in Meta: Chatty stops routing it and anyone may connect it
        again. If it was the account's current number the account stays, disconnected, with its
        chats and history, ready to be reconnected (same or another number: same chats)."""
        account = await self.check_take_down(company_id, account_id, phone_number_id)
        await self.directory.numbers.take_down(phone_number_id)
        await self.directory.invalidate_number(phone_number_id)
        if phone_number_id != account.phone_number_id:
            return account
        now = utc_now()
        await self.accounts.update_fields(account.id, {"status": WhatsAppAccountStatus.DISCONNECTED.value, "disconnected_at": now})
        return account.model_copy(update={"status": WhatsAppAccountStatus.DISCONNECTED, "disconnected_at": now})

    async def _own(self, company_id: StrObjectId, account_id: StrObjectId) -> WhatsAppAccount:
        account = await self.accounts.get(account_id)
        if account is None or account.company_id != company_id:
            raise WhatsAppAccountNotFound(f"Account {account_id} is not from company {company_id}", company_id=str(company_id))
        return account


def _waba_change(account: WhatsAppAccount, connection: VerifiedConnection) -> Optional[WabaChange]:
    if account.waba_id == connection.waba_id:
        return None
    return WabaChange(
        previous_waba_id=account.waba_id,
        new_waba_id=connection.waba_id,
        portfolio_changed=bool(connection.portfolio_id) and connection.portfolio_id != account.portfolio_id,
    )
