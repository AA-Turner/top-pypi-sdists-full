"""
Pushover Notifications via lunchable
"""

from __future__ import annotations

import logging
from base64 import b64decode
from os import getenv

from httpx import QueryParams
from lunchable.models import (
    TransactionObject,
)

from lunchable_pushlunch.base import HttpRequest, Notifier

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)


class PushLunchError(Exception):
    """
    PushLunch Exception
    """


class PushLunch(Notifier):
    """
    Lunch Money Pushover Notifications via Lunchable
    """

    notification_endpoint: str = "https://api.pushover.net/1"
    auth_params: dict[str, str]

    def get_notifier_auth(self, key: str | None) -> None:
        """
        Get httpx Auth for the Notifier
        """
        _courtesy_token = b"YXpwMzZ6MjExcWV5OGFvOXNicWF0cmdraXc4aGVz"
        app_token = getenv("PUSHOVER_APP_TOKEN") or b64decode(_courtesy_token).decode(
            "utf-8"
        )
        user_key = key or getenv("PUSHOVER_USER_KEY")
        if not user_key:
            raise PushLunchError(
                "You must provide a Pushover User Key or define it with "
                "a `PUSHOVER_USER_KEY` environment variable"
            )
        self.auth_params = {"token": app_token, "user": user_key}

    def format_transaction(self, transaction: TransactionObject) -> HttpRequest:
        message = self.format_pushover_message(transaction)
        params_dict = {
            "message": message,
            "title": "Lunch Money Transaction",
            "html": 1,
        }
        default_params: QueryParams = QueryParams(**params_dict)
        params = default_params.merge(self.auth_params)
        return HttpRequest(
            url="messages.json",
            params=params,
        )

    def format_pushover_message(self, transaction: TransactionObject) -> str:
        """
        Format the Pushover message
        """
        transaction_lines = [
            f"<b>{key.title()}:</b> <i>{value}</i>"
            for key, value in self.get_notification_map(transaction=transaction).items()
        ]
        transaction_formatted = "\n".join(transaction_lines)
        if transaction.status == "uncleared":
            url = (
                f'<a href="{self.get_period_url(transaction=transaction)}">'
                "<b>Uncleared Transactions from this Period</b></a>"
            )
            transaction_formatted += f"\n\n{url}"
        return transaction_formatted
