import asyncio

# config
from navconfig.logging import logging

# Notify:
from notify import Notify
from notify.models import Actor, Chat
from notify.providers.email import Email

from ..conf import (
    DEFAULT_RECIPIENT,
    EMAIL_HOST,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_USERNAME,
    EVENT_CHAT_BOT,
    EVENT_CHAT_ID,
)


def getNotify(notify, **kwargs):
    args = {}
    if notify == "telegram":
        # defining the Default chat object:
        recipient = Chat(**{"chat_id": EVENT_CHAT_ID, "chat_name": "Navigator"})
        # send notifications to Telegram bot
        args = {"bot_token": EVENT_CHAT_BOT, **kwargs}
        ntf = Notify("telegram", **args)
    elif notify == "email":
        account = {
            "host": EMAIL_HOST,
            "port": EMAIL_PORT,
            "username": EMAIL_USERNAME,
            "password": EMAIL_PASSWORD,
        }
        recipient = Actor(**DEFAULT_RECIPIENT)
        ntf = Email(debug=True, **account)
    else:
        recipient = Actor(**DEFAULT_RECIPIENT)
        ntf = Notify(notify, **args)
    return [ntf, recipient]


async def _send_(ntf, **kwargs):
    async with ntf as conn:
        await conn.send(**kwargs)


def send_notification(event_loop, message, provider):
    asyncio.set_event_loop(event_loop)
    ntf, recipients = getNotify(provider)
    args = {
        "recipient": [recipients],
        "message": message,
    }
    if ntf.provider_type == "email":
        args["subject"] = message
    if ntf.provider == "telegram":
        args["disable_notification"] = False
    try:
        result = event_loop.run_until_complete(_send_(ntf, **args))
        logging.debug(f"NOTIFY result: {result}")
    except Exception as err:
        logging.exception(err)
