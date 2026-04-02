"""
Base Notification Provider
"""

from __future__ import annotations

import asyncio
import calendar
import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any, Mapping

import httpx
from lunchable.models import (
    AssetsObject,
    CategoriesObject,
    PlaidAccountObject,
    TransactionObject,
)
from lunchable.plugins import LunchableApp
from pydantic_core import to_jsonable_python

logger = logging.getLogger(__name__)


@dataclass
class HttpRequest:
    """
    HTTP Request TypedDict
    """

    method: str = "POST"
    url: str = ""
    params: httpx.QueryParams | None = None
    data: Mapping[str, Any] | None = None


class _BaseNotifier(LunchableApp, ABC):
    """
    Base Notifier Class
    """

    headers: dict[str, Any] | None = None
    notification_endpoint: str | None = None

    @abstractmethod
    def format_transaction(self, transaction: TransactionObject) -> HttpRequest:
        """
        Format the Payload for the Notification

        Parameters
        ----------
        transaction: TransactionObject
            LunchMoney Transaction Object

        Returns
        -------
        HttpRequest
            Prepared HTTP Request
        """

    def __init__(
        self,
        url: httpx.URL | None = None,
        auth: httpx.Auth | None = None,
        lunchmoney_access_token: str | None = None,
    ) -> None:
        """
        Initialize

        Parameters
        ----------
        url: httpx.URL | None
            URL to send the notification to.
        auth: httpx.Auth | None
            httpx Auth instance. Defaults to None.
        lunchmoney_access_token: Optional[str]
            LunchMoney Access Token. Will be inherited from `LUNCHMONEY_ACCESS_TOKEN`
            environment variable.
        """
        super().__init__(access_token=lunchmoney_access_token)
        endpoint = url or self.notification_endpoint
        if not endpoint:
            raise NotImplementedError("You must provide a URL in your Notifier")
        base_url = url or self.notification_endpoint
        if not base_url:
            raise ValueError("You must provide a Notification Endpoint URL")
        self.notification_client = httpx.AsyncClient(
            headers=self.headers, auth=auth, base_url=base_url
        )
        self.refresh_data(models=[AssetsObject, PlaidAccountObject, CategoriesObject])
        self.notified_transactions: set[int] = set()

    async def send_notification(self, transaction: TransactionObject) -> httpx.Response:
        """
        Prepare the Notification Request

        Parameters
        ----------
        transaction: TransactionObject
            LunchMoney Transaction Object

        Returns
        -------
        httpx.Request
            Prepared HTTP Request
        """
        request = self.format_transaction(transaction=transaction)
        self.notified_transactions.add(transaction.id)
        response = await self.notification_client.request(
            url=request.url,
            method=request.method,
            json=to_jsonable_python(request.data),
            params=request.params,
        )
        response.raise_for_status()
        return response

    @classmethod
    def format_float(cls, amount: float) -> str:
        """
        Format Floats to be pleasant and human readable

        Parameters
        ----------
        amount: float
            Float Amount to be converted into a string

        Returns
        -------
        str
        """
        if amount < 0:
            float_string = f"$ ({float(amount):,.2f})".replace("-", "")
        else:
            float_string = f"$ {float(amount):,.2f}"
        return float_string

    async def notify_uncleared_transactions(
        self, continuous: bool = False, interval: int | None = None
    ) -> list[TransactionObject]:
        """
        Get the Current Period's Uncleared Transactions and Send a Notification for each

        Parameters
        ----------
        continuous : bool
            Whether to continuously check for more uncleared transactions,
            waiting a fixed amount in between checks.
        interval: Optional[int]
            Sleep Interval in Between Tries - only applies if `continuous` is set.
            Defaults to 60 (minutes). Cannot be less than 5 (minutes)

        Returns
        -------
        list[TransactionObject]
        """
        default_interval = 60
        min_interval = 5
        if interval is None:
            interval = default_interval
        if continuous is True and interval < min_interval:
            logger.warning(
                "Check interval cannot be less than 5 minutes. Defaulting to 5."
            )
            interval = min_interval
        if continuous is True:
            logger.info("Continuous Notifications Enabled. Beginning PushLunch.")

        uncleared_transactions = []
        continuous_search = True

        while continuous_search is True:
            found_transactions = len(self.notified_transactions)
            start_date, end_date = self._get_time_period()
            uncleared_transactions += self.lunch.get_transactions(
                status="uncleared",
                start_date=start_date,
                end_date=end_date,
            )
            for transaction in uncleared_transactions:
                if transaction.id not in self.notified_transactions:
                    await self.send_notification(transaction=transaction)
            if continuous is True:
                notified = len(self.notified_transactions)
                new_transactions = notified - found_transactions
                logger.info(
                    "%s new transactions pushed. %s total.", new_transactions, notified
                )
                await asyncio.sleep(interval * 60)
            else:
                continuous_search = False

        return uncleared_transactions

    @classmethod
    def _get_time_period(cls) -> tuple[date, date]:
        """
        Get the Start and End Dates to fetch transactions
        """
        today = datetime.now(tz=timezone.utc).astimezone().date()
        start_of_this_month = today.replace(day=1)
        end_of_last_month = start_of_this_month - timedelta(days=1)
        start_of_last_month = end_of_last_month.replace(day=1)
        last_day_of_this_month = calendar.monthrange(today.year, today.month)[1]
        end_of_this_month = today.replace(day=last_day_of_this_month)
        return start_of_last_month, end_of_this_month

    def get_notification_map(self, transaction: TransactionObject) -> dict[str, str]:
        """
        Parse a Transaction into a Dictionary for the Notification
        """
        if transaction.category_id is None:
            category = "N/A"
        else:
            category = self.data.categories[transaction.category_id].name
        account_id = transaction.plaid_account_id or transaction.asset_id
        account = self.data.asset_map[account_id]  # type: ignore[index]
        if isinstance(account, AssetsObject):
            account_name = account.display_name or account.name
        else:
            account_name = account.name
        transaction_map: dict[str, Any] = OrderedDict(
            payee=transaction.payee,
            amount=self.format_float(transaction.amount),
            date=transaction.date.strftime("%A %B %-d, %Y"),
            category=category,
            account=account_name,
        )
        if transaction.currency is not None:
            transaction_map["currency"] = transaction.currency.upper()
        if transaction.status is not None:
            transaction_map["status"] = transaction.status.title()
        if transaction.notes is not None:
            transaction_map["notes"] = transaction.notes
        return transaction_map

    def get_period_url(self, transaction: TransactionObject) -> str:
        start_date, end_date = self._get_time_period()
        more_transactions_url = (
            "https://my.lunchmoney.app/transactions/"
            f"{transaction.date.year}/{transaction.date.strftime('%m')}?"
            f"status=unreviewed&start_date={start_date}&end_date={end_date}&"
            f"match=all&time=custom"
        )
        return more_transactions_url


class Notifier(_BaseNotifier, ABC):
    """
    Base Notifier Class
    """

    @abstractmethod
    def get_notifier_auth(self, key: str | None) -> httpx.Auth | None:
        """
        Get the Auth instance for the Notifier
        """

    def __init__(
        self,
        key: str | None = None,
        url: httpx.URL | None = None,
        lunchmoney_access_token: str | None = None,
    ) -> None:
        """
        Notifier Base Class

        Parameters
        ----------
        url: httpx.URL
            URL to send the notification to.
        key: str | None
            Key to use for the notification service.
        lunchmoney_access_token: Optional[str]
            LunchMoney Access Token. Will be inherited from `LUNCHMONEY_ACCESS_TOKEN`
            environment variable.
        """
        super().__init__(
            url=url,
            auth=self.get_notifier_auth(key=key),
            lunchmoney_access_token=lunchmoney_access_token,
        )
