"""
Ntfy Notifications
"""

from __future__ import annotations

import os
from typing import Any

from lunchable.models import TransactionObject

from lunchable_pushlunch.base import HttpRequest, Notifier


class Ntfy(Notifier):
    """
    Lunch Money NTFY Notifications via Lunchable
    """

    notification_endpoint: str = "https://ntfy.sh"
    topic: str

    def get_notifier_auth(self, key: str | None) -> None:
        """
        Set the NTFY Topic
        """
        topic = key or os.getenv("NTFY_TOPIC")
        if not topic:
            raise ValueError(
                "You must provide an NTFY Topic or define it with "
                "a `NTFY_TOPIC` environment variable"
            )
        self.topic = topic

    def format_transaction(self, transaction: TransactionObject) -> HttpRequest:
        """
        Prepare the HTTP Request for the Notification
        """
        transaction_lines = [
            f"**{key.title()}:** _{value}_"
            for key, value in self.get_notification_map(transaction=transaction).items()
        ]
        payload: dict[str, Any] = {
            "topic": self.topic,
            "message": "\n".join(transaction_lines),
            "markdown": True,
            "title": "Lunch Money Transaction",
            "icon": "https://lunchmoney.app/assets/images/logos/mascot.png",
            "actions": [
                {
                    "action": "view",
                    "label": "More Transactions from this Period",
                    "url": self.get_period_url(transaction=transaction),
                }
            ],
        }
        return HttpRequest(data=payload)
