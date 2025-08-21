import asyncio
import logging
import smtplib
from email.message import EmailMessage

import aiosmtplib

from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging

_logger = logging.getLogger(__name__)


def send_email(
        *, to_email: str, subject: str = "Hello world", html_content: str,
        emulate: bool = False
):
    to_email = to_email.strip()

    if emulate:
        _logger.info(f"emulate email sending, {to_email=}, {subject=}, {html_content=}")
        return

    message = EmailMessage()
    message["From"] = get_cached_settings().email_smtp_user
    message["To"] = to_email
    message["Subject"] = subject
    message.add_alternative(html_content, subtype="html")

    with smtplib.SMTP_SSL(
            get_cached_settings().email_smtp_hostname,
            get_cached_settings().email_smtp_port
    ) as server:
        server.login(
            get_cached_settings().email_smtp_user,
            get_cached_settings().email_smtp_password
        )
        server.send_message(message)

    _logger.info(f"email was send, {to_email=}")


async def async_send_email(
        *,
        to_email: str, subject: str = "Hello world", html_content: str,
        emulate: bool = False
):
    to_email = to_email.strip()

    if emulate:
        _logger.info(f"emulate email sending, {to_email=}, {subject=}, {html_content=}")
        return

    message = EmailMessage()
    message["From"] = get_cached_settings().email_smtp_user
    message["To"] = to_email
    message["Subject"] = subject
    message.add_alternative(html_content, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=get_cached_settings().email_smtp_hostname,
        port=get_cached_settings().email_smtp_port,
        username=get_cached_settings().email_smtp_user,
        password=get_cached_settings().email_smtp_password,
        use_tls=True
    )

    _logger.info(f"email was send, {to_email=}")


async def __async_example():
    setup_logging()
    send_email(
        to_email="arpakit@gmail.com",
        html_content="Hello world 2"
    )


if __name__ == '__main__':
    asyncio.run(__async_example())
