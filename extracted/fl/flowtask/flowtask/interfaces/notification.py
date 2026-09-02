"""
Interface for sending messages using Notify.
"""
import os
import asyncio
from pathlib import Path, PurePath
from navconfig.logging import logging
from notify import Notify
from notify.providers.email import Email
from notify.models import (
    Actor,
    Chat,
    Channel,
    TeamsChannel,
    TeamsCard
)
from notify.conf import MS_TEAMS_DEFAULT_TEAMS_ID
from flowtask.conf import (
    EVENT_CHAT_ID,
    EVENT_CHAT_BOT,
    DEFAULT_RECIPIENT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_HOST,
    SLACK_DEFAULT_CHANNEL,
    SLACK_DEFAULT_CHANNEL_NAME,
    MS_TEAMS_NAVIGATOR_CHANNEL,
    MS_TEAMS_NAVIGATOR_CHANNEL_ID,
)
from .mask import MaskSupport


class Notification(MaskSupport):
    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)
        self.provider: str = kwargs.pop("type", "dummy")
        self.list_attachment: list = []
        self.account: str = self.set_account(
            kwargs.pop("account", {})
        )
        # recipient:
        self._recipients = kwargs.pop("recipients", [])
        self._channel = kwargs.pop("channel", "Navigator")
        self._channel_id = kwargs.pop("channel_id", None)
        self._chat_id = kwargs.pop('chat_id', EVENT_CHAT_ID)
        self._bot_token = kwargs.pop('bot_token', EVENT_CHAT_BOT)
        self._kwargs = kwargs
        self.message = kwargs.pop("message", {})
        template = self.message.pop("template", None)
        self._template = kwargs.pop("template", template)
        self._loop = kwargs.pop(
            "event_loop",
            asyncio.get_event_loop()
        )

    def set_account(self, account: dict):
        for key, default in account.items():
            val = self.get_env_value(account[key], default=default)
            account[key] = val
        return account

    def get_env_value(self, key, default: str = None):
        if key is None:
            return None
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key

    def get_notify(self, **kwargs):
        recipient = Actor(**DEFAULT_RECIPIENT)
        if self.provider == "telegram":
            recipient = Chat(**{"chat_id": self._chat_id, "chat_name": self._channel})
            # send notifications to Telegram bot
            args = {
                "bot_token": self._bot_token,
                "loop": asyncio.get_event_loop(),
                **kwargs,
            }
            provider = Notify("telegram", **args)
        elif self.provider == "outlook":
            args = {"use_credentials": True, "loop": asyncio.get_event_loop(), **kwargs}
            provider = Notify("outlook", **args)
        elif self.provider == "slack":
            _id = self._channel_id if self._channel_id else SLACK_DEFAULT_CHANNEL
            name = self._channel if self._channel else SLACK_DEFAULT_CHANNEL_NAME
            recipient = Channel(channel_id=_id, channel_name=name)
            provider = Notify("slack", **kwargs)
        elif self.provider == "email":
            if not self.account:
                account = {
                    "host": EMAIL_HOST,
                    "port": EMAIL_PORT,
                    "username": EMAIL_USERNAME,
                    "password": EMAIL_PASSWORD,
                }
            else:
                account = self.account
            account = {**account, **kwargs}
            if not self._recipients:
                recipient = Actor(**DEFAULT_RECIPIENT)
            else:
                recipient = [Actor(**user) for user in self._recipients]
            provider = Email(debug=True, **account)
        elif self.provider == "teams":
            _id = (
                self._channel_id if self._channel_id else MS_TEAMS_NAVIGATOR_CHANNEL_ID
            )
            name = self._channel if self._channel else MS_TEAMS_NAVIGATOR_CHANNEL
            args = {"as_user": True, "loop": asyncio.get_event_loop(), **kwargs}
            recipient = TeamsChannel(
                name=name, team_id=MS_TEAMS_DEFAULT_TEAMS_ID, channel_id=_id
            )
            provider = Notify("teams", **args)
        else:
            # Any other Notify Provider:
            if not self._recipient:
                recipient = Actor(**DEFAULT_RECIPIENT)
            else:
                recipient = [Actor(**user) for user in self._recipients]
            provider = Notify(self.provider, **kwargs)
        logging.debug(f"Created Notify Component {provider}")
        return [provider, recipient]

    def get_attachment_files(self, result: list) -> list:
        if result is None:
            return []
        elif isinstance(result, str):
            result = [result]
        files = []
        for part in result:
            if isinstance(part, str):
                file = Path(part.strip("'"))
                if file.exists():
                    files.append(file)
            elif isinstance(part, PurePath):
                if file.exists():
                    files.append(file)
        return files

    def get_message(self, message: str):
        if self.provider in ("email", "gmail", "outlook"):
            args = {"subject": message, **self.message}
        elif self.provider == "teams":
            msg = TeamsCard(text=message, summary="Task Summary")
            args = {"message": msg, **self.message}
        elif self.provider in ("slack", "telegram"):
            args = {"message": message, **self.message}
        else:
            args = {"message": message, **self.message}
        return args
