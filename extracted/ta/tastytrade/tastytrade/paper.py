import math
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from decimal import Decimal
from typing import Any, Literal
from uuid import uuid4

from httpx2 import AsyncClient
from typing_extensions import deprecated

from tastytrade import PAPER_URL
from tastytrade.account import Account
from tastytrade.session import Session
from tastytrade.streamer import AlertStreamer
from tastytrade.utils import validate_response


class PaperSession(Session):
    """
    Contains a session which can be used to interact with the paper trading API.
    Note these sessions are only valid for endpoints in the `Account` class.

    :param api_key:
        tastyware paper API key, buy one at https://tastyware.dev/login
        defaults to the $TW_API_KEY environment variable
    """

    def __init__(self, api_key: str | None, **client_kwargs: Any):
        super().__init__("kyrie", "eleison", is_test=True)
        self.api_key = api_key or os.environ["TW_API_KEY"]
        self.session_expiration = math.inf
        # The headers to use for API requests
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key,
        }
        # httpx client for async requests
        self._client = AsyncClient(base_url=PAPER_URL, headers=headers, **client_kwargs)
        client_kwargs["headers"] = headers
        self.client_kwargs = client_kwargs

    async def create_account(
        self,
        name: str,
        margin_or_cash: Literal["Cash", "Margin"] = "Margin",
        initial_deposit: int = 100_000,
    ) -> Account:
        """
        Create a new paper trading account with the given configuration.

        :param name: name for the account
        :param margin_or_cash: whether the account should be margin or cash
        :param initial_deposit: the initial balance for the new account
        """
        json = {
            "account_name": name,
            "margin_or_cash": margin_or_cash,
            "initial_deposit": initial_deposit,
        }
        data = await self._post("/accounts", json=json)
        return Account(**data)

    async def delete_account(self, account: Account) -> None:
        """
        Delete the given paper trading account along with its orders, transactions, etc.

        :param account: account to delete
        """
        params = {"account_number": account.account_number}
        await self._delete("/accounts", params=params)

    async def deposit(self, account: Account, amount: Decimal) -> None:
        """
        Deposit the given quantity of fake dollars into the paper trading account. Use
        with a negative number for withdrawals.

        :param account: account to deposit into
        :param amount: amount of money to deposit/withdraw
        """
        params = {"account_number": account.account_number, "amount": f"{amount:.2f}"}
        response = await self._client.post("/accounts/deposit", params=params)
        validate_response(response)

    @asynccontextmanager
    async def temporary_account(
        self, margin_or_cash: Literal["Cash", "Margin"] = "Margin"
    ) -> AsyncGenerator[Account, None]:
        """
        Create an account for temporary use that will be cleaned up when exiting the
        context manager. Useful for unit testing.

        :param margin_or_cash: whether the account should be margin or cash
        """
        acc = await self.create_account(uuid4().hex, margin_or_cash=margin_or_cash)
        try:
            yield acc
        finally:
            await self.delete_account(acc)


@deprecated(
    "`PaperAlertStreamer` is deprecated and may be removed in a future version. Use "
    "`AlertStreamer` with a `PaperSession` instead."
)
class PaperAlertStreamer(AlertStreamer):
    """
    Currently only supports listening to orders.
    """

    pass
