import asyncio
import datetime as dt
import logging
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

import aiosmtplib

from project.core.settings import get_cached_settings
from project.core.setup_logging import setup_logging

_logger = logging.getLogger(__name__)


def _build_email_message(
        *,
        from_email: str,
        to_email: str,
        subject: str,
        html_content: str,
        from_name: str | None = None,
) -> EmailMessage:
    msg = EmailMessage()
    if from_name:
        msg["From"] = formataddr((from_name, from_email))
    else:
        msg["From"] = from_email  # без имени
    msg["To"] = to_email.strip()
    msg["Subject"] = subject
    msg.add_alternative(html_content, subtype="html")
    return msg


def sync_send_email(
        *,
        from_name: str | None = get_cached_settings().common_project_title,
        to_email: str,
        subject: str = get_cached_settings().common_project_title,
        html_content: str,
        emulate: bool = False,
):
    if emulate:
        _logger.info(f"emulate email sending, to_email={to_email!r}, subject={subject!r}")
        return

    message = _build_email_message(
        from_email=get_cached_settings().email_smtp_user,
        from_name=from_name,
        to_email=to_email, subject=subject, html_content=html_content
    )

    if get_cached_settings().email_smtp_port == 465:
        _logger.info("using port 465 (SSL)")
        with smtplib.SMTP_SSL(
                host=get_cached_settings().email_smtp_hostname,
                port=465,
                timeout=dt.timedelta(seconds=15).total_seconds(),
                context=ssl.create_default_context(),
        ) as server:
            server.login(
                get_cached_settings().email_smtp_user,
                get_cached_settings().email_smtp_password,
            )
            server.send_message(message)

    elif get_cached_settings().email_smtp_port == 587:
        _logger.info("using port 587 (STARTTLS)")
        with smtplib.SMTP(
                host=get_cached_settings().email_smtp_hostname,
                port=587,
                timeout=dt.timedelta(seconds=15).total_seconds(),
        ) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(
                get_cached_settings().email_smtp_user,
                get_cached_settings().email_smtp_password,
            )
            server.send_message(message)
    else:
        raise ValueError("Unsupported SMTP port")

    _logger.info(f"email was sent, to_email={to_email!r}")


async def async_send_email(
        *,
        from_name: str | None = get_cached_settings().common_project_title,
        to_email: str,
        subject: str = get_cached_settings().common_project_title,
        html_content: str,
        emulate: bool = False,
):
    if emulate:
        _logger.info(f"emulate email sending, to_email={to_email!r}, subject={subject!r}")
        return

    message = _build_email_message(
        from_email=get_cached_settings().email_smtp_user,
        from_name=from_name,
        to_email=to_email, subject=subject, html_content=html_content
    )

    if get_cached_settings().email_smtp_port == 465:
        _logger.info("using port 465 (SSL)")
        await aiosmtplib.send(
            message,
            hostname=get_cached_settings().email_smtp_hostname,
            port=465,
            username=get_cached_settings().email_smtp_user,
            password=get_cached_settings().email_smtp_password,
            use_tls=True,
            start_tls=False,
            timeout=dt.timedelta(seconds=15).total_seconds(),
            tls_context=ssl.create_default_context(),
        )

    elif get_cached_settings().email_smtp_port == 587:
        _logger.info("using port 587 (STARTTLS)")
        await aiosmtplib.send(
            message,
            hostname=get_cached_settings().email_smtp_hostname,
            port=587,
            username=get_cached_settings().email_smtp_user,
            password=get_cached_settings().email_smtp_password,
            use_tls=False,
            start_tls=True,
            timeout=dt.timedelta(seconds=15).total_seconds(),
            tls_context=ssl.create_default_context(),
        )
    else:
        raise ValueError("Unsupported SMTP port")

    _logger.info(f"email was sent, to_email={to_email!r}")


async def __async_example():
    setup_logging()
    await async_send_email(
        to_email="arpakit@gmail.com",
        html_content="Hello world 2",
        from_name="Gamer Market"
    )


if __name__ == "__main__":
    asyncio.run(__async_example())
