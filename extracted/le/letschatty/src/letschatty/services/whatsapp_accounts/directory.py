"""Read side of the account model: which account a webhook, a chat or a request belongs to.

This is the single place that answers "with which number and token do I talk to Meta?".
Senders receive the `AccountContext` it builds; they never read the company.

Rules (see the technical design, «Cuentas por Empresa · Diseño técnico» §1):
- R2: a chat sends through ITS account. If that account cannot send, `AccountUnavailable`
  is raised; there is no fallback to another account.
- R3: the default account is picked only by `for_request(company_id, None)`, the entry point
  of an endpoint that did not say which account to use.
"""
import json
import logging
from dataclasses import dataclass
from typing import Optional

from ...models.cache.cache_protocol import CacheProtocol
from ...models.cache.no_cache import NoCache
from ...models.utils.types.identifier import StrObjectId
from ...models.whatsapp import (
    AccountContext,
    AccountUnavailable,
    NumberNotConnected,
    WhatsAppAccount,
    WhatsAppAccountNotFound,
    WhatsAppAccountStatus,
    WhatsAppNumber,
)
from .repositories import WhatsAppAccountRepository, WhatsAppBusinessAccountRepository, WhatsAppNumberRepository

logger = logging.getLogger(__name__)

ROUTE_TTL_SECONDS = 600


def unavailable_reason(account) -> str:
    """Why a message was not sent through `account`, for the agent (Spanish)."""
    if account.status == WhatsAppAccountStatus.PENDING:
        return f"No se envió: la cuenta de WhatsApp «{account.name}» todavía no terminó de conectarse."
    return f"No se envió: la cuenta de WhatsApp «{account.name}» está desconectada. Reconectala en Mi cuenta › WhatsApp y Meta para volver a enviar."


def number_route_key(phone_number_id: str) -> str:
    return f"whatsapp_numbers:route:{phone_number_id}"


@dataclass(frozen=True)
class NumberRoute:
    """Where a webhook for `phone_number_id` goes."""
    phone_number_id: str
    company_id: StrObjectId
    account_id: StrObjectId
    #: False when the account stopped using this number (a message to it is the 5A case).
    is_current_number: bool


class AccountDirectory:
    def __init__(
        self,
        accounts: WhatsAppAccountRepository,
        numbers: WhatsAppNumberRepository,
        wabas: WhatsAppBusinessAccountRepository,
        cache: Optional[CacheProtocol] = None,
    ):
        self.accounts = accounts
        self.numbers = numbers
        self.wabas = wabas
        self.cache: CacheProtocol = cache or NoCache()

    # ── webhooks ──

    async def route(self, phone_number_id: str) -> NumberRoute:
        """The account a webhook belongs to. Raises `NumberNotConnected` for an unknown number:
        the caller logs it and never creates a chat for it."""
        cached = await self._cached_route(phone_number_id)
        if cached:
            return NumberRoute(**json.loads(cached))
        number = await self.numbers.get(phone_number_id)
        if number is None or not number.is_live:
            raise NumberNotConnected(f"Phone number {phone_number_id} is not connected to any account")
        route = NumberRoute(
            phone_number_id=phone_number_id,
            company_id=number.company_id,
            account_id=number.account_id,
            is_current_number=await self._is_current_number(number),
        )
        try:
            await self.cache.set(number_route_key(phone_number_id), json.dumps(route.__dict__), ttl=ROUTE_TTL_SECONDS)
        except Exception as e:  # noqa: BLE001
            logger.error("Route cache unavailable writing number %s: routed from MongoDB anyway (%s)", phone_number_id, e)
        return route

    async def invalidate_number(self, phone_number_id: str) -> None:
        """Best effort: if the cache is down, the stale route expires with its TTL."""
        try:
            await self.cache.delete(number_route_key(phone_number_id))
        except Exception as e:  # noqa: BLE001
            logger.error("Route cache unavailable invalidating number %s: it expires in %ss (%s)", phone_number_id, ROUTE_TTL_SECONDS, e)

    async def _cached_route(self, phone_number_id: str) -> Optional[str]:
        """The cache only saves reads. Every webhook of every company is routed here first, so a
        cache outage must fall back to MongoDB, never fail the webhook: backup-chatty parks a 500
        in S3 without retrying it (the legacy routing already fell back the same way)."""
        try:
            return await self.cache.get(number_route_key(phone_number_id))
        except Exception as e:  # noqa: BLE001
            logger.error("Route cache unavailable reading number %s: routing from MongoDB (%s)", phone_number_id, e)
            return None

    # ── sending ──

    async def for_account(self, account_id: StrObjectId) -> AccountContext:
        """The context to send as this account. Raises if it cannot send."""
        account = await self.get_account(account_id)
        if not account.can_send:
            raise AccountUnavailable(f"Account «{account.name}» is {account.status}", reason=unavailable_reason(account), company_id=str(account.company_id))
        return await self._context(account)

    async def context_of(self, account_id: StrObjectId) -> AccountContext:
        """The account's context whatever its status: inbound webhooks of a disconnected account
        are still recorded. Use `for_account` to send."""
        return await self._context(await self.get_account(account_id))

    async def for_webhook(self, phone_number_id: str) -> AccountContext:
        """The account a webhook belongs to, flagged when it arrived on a previous number."""
        route = await self.route(phone_number_id)
        context = await self.context_of(route.account_id)
        return context if route.is_current_number else context.model_copy(update={"via_current_number": False})

    async def for_chat(self, account_id: Optional[StrObjectId], company_id: StrObjectId) -> AccountContext:
        """The context to send in a chat. A chat created before the migration has no account:
        until the backfill (M2) finishes it is served by its company's default account, the
        only account such a company can have. This branch is logged so it can be removed."""
        if account_id:
            return await self.for_account(account_id)
        logger.warning("Chat without account_id in company %s: using the default account (pre-migration chat)", company_id)
        return await self.for_request(company_id, None)

    async def for_request(self, company_id: StrObjectId, account_id: Optional[StrObjectId]) -> AccountContext:
        """R3: the only place that picks the default account."""
        if account_id:
            account = await self.get_account(account_id)
            if account.company_id != company_id:
                raise WhatsAppAccountNotFound(f"Account {account_id} is not from company {company_id}", company_id=str(company_id))
            return await self.for_account(account.id)
        account = await self.accounts.get_default(company_id)
        if account is None:
            raise WhatsAppAccountNotFound("The company has no default WhatsApp account", company_id=str(company_id))
        return await self.for_account(account.id)

    async def context_for_request(self, company_id: StrObjectId, account_id: Optional[StrObjectId]) -> AccountContext:
        """R3 for READS (looking up a chat, listing templates): the same account `for_request`
        picks, whatever its status. A disconnected account cannot send, but its chats and
        templates can still be looked at."""
        if account_id:
            account = await self.get_account(account_id)
            if account.company_id != company_id:
                raise WhatsAppAccountNotFound(f"Account {account_id} is not from company {company_id}", company_id=str(company_id))
            return await self._context(account)
        account = await self.accounts.get_default(company_id)
        if account is None:
            raise WhatsAppAccountNotFound("The company has no default WhatsApp account", company_id=str(company_id))
        return await self._context(account)

    # ── reads ──

    async def get_account(self, account_id: StrObjectId) -> WhatsAppAccount:
        account = await self.accounts.get(account_id)
        if account is None:
            raise WhatsAppAccountNotFound(f"WhatsApp account {account_id} not found")
        return account

    async def _context(self, account: WhatsAppAccount) -> AccountContext:
        waba = await self.wabas.get(account.company_id, account.waba_id)
        return AccountContext(
            account_id=account.id,
            company_id=account.company_id,
            account_name=account.name,
            phone_number_id=account.phone_number_id,
            display_phone_number=account.display_phone_number,
            waba_id=account.waba_id,
            portfolio_id=account.portfolio_id,
            dataset_id=waba.dataset_id if waba else None,
            is_default=account.is_default,
            token=account.token,
        )

    async def _is_current_number(self, number: WhatsAppNumber) -> bool:
        if not number.active:
            return False
        account = await self.accounts.get(number.account_id)
        return account is not None and account.phone_number_id == number.phone_number_id
