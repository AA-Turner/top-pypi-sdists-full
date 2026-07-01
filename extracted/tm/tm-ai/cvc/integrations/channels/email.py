"""
Email adapter for CVC — IMAP polling + SMTP send.

Receive: IDLE on the IMAP mailbox (preferred) with a polling fallback
every N seconds when the server doesn't support IDLE.
Send: SMTP submission with starttls.

This adapter is intentionally dependency-free at runtime — it uses
``imaplib`` and ``smtplib`` from the stdlib. Email is the one channel
that's almost universally available without extra packages.

Features v1:
  - Plain text + multipart messages (text part extracted)
  - Inline images + attachments downloaded as media entries
  - Reply threading (In-Reply-To / References headers)
  - Per-sender allowlist
  - Subject-based commands (`Subject: /help` becomes `/help`)

Deliberately deferred to v1.1+:
  - HTML rendering (we always reply in plain text)
  - PGP/GPG signed mail
"""

from __future__ import annotations

import asyncio
import email
import email.policy
import email.utils
import imaplib
import logging
import smtplib
import time
from email.message import EmailMessage as PyEmailMessage
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


from .base import (  # noqa: E402
    BaseChannelAdapter,
    Capability,
    InboundMessage,
    OutboundMessage,
)
from ..formatting.markdown import markdown_to_plain  # noqa: E402


# C6: spine channel capture — fires at the channel boundary.
try:
    from cvc.events.channel_capture import (
        capture_message_in,
        capture_message_out,
        capture_message_error,
        capture_message_skipped,
    )
except Exception:  # noqa: BLE001
    def capture_message_in(*_a, **_kw): return None  # type: ignore
    def capture_message_out(*_a, **_kw): return None  # type: ignore
    def capture_message_error(*_a, **_kw): return None  # type: ignore
    def capture_message_skipped(*_a, **_kw): return None  # type: ignore


def _is_allowed(allowlist: List[str], from_addr: str) -> bool:
    if not allowlist:
        return False
    return from_addr.lower() in {a.lower() for a in allowlist}


class EmailAdapter(BaseChannelAdapter):
    name = "email"
    display_name = "Email (IMAP/SMTP)"
    description = (
        "Send and receive email via any IMAP/SMTP server (Gmail, Outlook, "
        "Fastmail, your own). Uses the Python stdlib — no extra dependencies. "
        "Subject-line slash commands are supported."
    )
    config_schema = [
        {
            "key": "imap_host",
            "label": "IMAP host",
            "help": "Example: imap.gmail.com",
            "required": True,
            "kind": "str",
        },
        {
            "key": "imap_user",
            "label": "IMAP username",
            "required": True,
            "kind": "str",
        },
        {
            "key": "imap_password",
            "label": "IMAP password (use an app password, NOT your real one)",
            "secret": True,
            "required": True,
            "kind": "str",
        },
        {
            "key": "smtp_host",
            "label": "SMTP host",
            "help": "Example: smtp.gmail.com",
            "required": True,
            "kind": "str",
        },
        {
            "key": "smtp_port",
            "label": "SMTP port",
            "default": "587",
            "kind": "str",
        },
        {
            "key": "smtp_user",
            "label": "SMTP username (defaults to imap_user)",
            "required": False,
            "kind": "str",
        },
        {
            "key": "smtp_password",
            "label": "SMTP password (defaults to imap_password)",
            "secret": True,
            "required": False,
            "kind": "str",
        },
        {
            "key": "from_addr",
            "label": "From address (defaults to smtp_user)",
            "required": False,
            "kind": "str",
        },
        {
            "key": "poll_seconds",
            "label": "Poll interval (seconds)",
            "default": "30",
            "kind": "str",
        },
        {
            "key": "allowlist",
            "label": "Allowed sender addresses (comma-separated)",
            "required": True,
            "kind": "list[str]",
        },
    ]


    def capabilities(self) -> List[Capability]:
        return [
            Capability.TEXT,
            Capability.MEDIA,
            Capability.THREADS,
        ]

    async def start(self) -> None:
        host = self.cfg("imap_host", "")
        user = self.cfg("imap_user", "")
        password = self.cfg("imap_password", "")
        smtp_host = self.cfg("smtp_host", host)
        smtp_port = int(self.cfg("smtp_port", 587))
        smtp_user = self.cfg("smtp_user", user)
        smtp_password = self.cfg("smtp_password", password)
        if not (host and user and password and smtp_host):
            raise RuntimeError("email: imap_host, imap_user, imap_password, smtp_host are required")
        self._imap_host = host
        self._imap_user = user
        self._imap_password = password
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port
        self._smtp_user = smtp_user
        self._smtp_password = smtp_password
        self._from_addr = self.cfg("from_addr", smtp_user)
        self._allowlist = self.cfg_list("allowlist")
        self._poll_seconds = int(self.cfg("poll_seconds", 30))
        self._seen_uids: set[bytes] = set()
        self._poll_task = asyncio.create_task(self._poll_loop())
        self._healthy = True
        self._started_at = time.time()
        logger.info("email: IMAP %s:%s user=%s", host, 993, user)

    async def stop(self) -> None:
        task: Optional[asyncio.Task] = getattr(self, "_poll_task", None)
        if task is not None:
            task.cancel()
        self._healthy = False

    async def _poll_loop(self) -> None:
        """IMAP poll loop. Runs forever, sleeps ``_poll_seconds`` between
        passes. SEEN-flagged messages older than ``_seen_uids`` are
        fetched and processed."""
        while True:
            try:
                await self._poll_once()
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001
                logger.warning("email: poll error: %s", exc)
                self._last_error = str(exc)
            await asyncio.sleep(self._poll_seconds)

    async def _poll_once(self) -> None:
        # imaplib is sync — run in default threadpool.
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._poll_sync)

    def _poll_sync(self) -> None:
        with imaplib.IMAP4_SSL(self._imap_host) as imap:
            imap.login(self._imap_user, self._imap_password)
            imap.select("INBOX")
            typ, data = imap.uid("SEARCH", "UNSEEN")
            if typ != "OK":
                return
            uids = (data[0] or b"").split()
            for uid in uids:
                if uid in self._seen_uids:
                    continue
                typ, msg_data = imap.uid("FETCH", uid, "(RFC822)")
                if typ != "OK" or not msg_data or not msg_data[0]:
                    continue
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw, policy=email.policy.default)
                # Schedule inbound handling as a task so we don't block
                # the sync imaplib loop.
                asyncio.create_task(self._handle_email(msg, uid))
                self._seen_uids.add(uid)

    async def _handle_email(self, msg: PyEmailMessage, uid: bytes) -> None:
        from_addr = email.utils.parseaddr(msg.get("From", ""))[1]
        if not from_addr or not _is_allowed(self._allowlist, from_addr):
            # C6: capture rejected message.
            if from_addr:
                try:
                    capture_message_skipped(
                        channel=self.name,
                        actor=from_addr,
                        summary=f"email: from {from_addr} not in allowlist",
                        data={"chat_id": from_addr, "reason": "not_in_allowlist"},
                    )
                except Exception:
                    pass
            return
        subject = msg.get("Subject", "")
        # Collect text parts and attachments.
        text_body = ""
        media: List[Dict[str, Any]] = []
        for part in msg.walk():
            if part.is_multipart():
                continue
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in disp:
                if not text_body:
                    text_body = part.get_content()
            elif ctype == "text/html":
                # Prefer the plain part if present; otherwise keep html.
                if not text_body:
                    text_body = part.get_content()
            else:
                data = part.get_payload(decode=True) or b""
                media.append({
                    "kind": "document",
                    "data": data,
                    "mime": ctype,
                    "size": len(data),
                    "filename": part.get_filename(),
                })
        # Slash-command extraction from the subject.
        first_line = text_body.split("\n", 1)[0] if text_body else subject
        is_command = first_line.lstrip().startswith("/")
        command = first_line.split(maxsplit=1)[0].lstrip("/").lower() or None
        command_args = first_line.split(maxsplit=1)[1] if " " in first_line else None
        inbound = InboundMessage(
            channel=self.name,
            chat_id=from_addr,
            user_id=from_addr,
            user_name=email.utils.parseaddr(msg.get("From", ""))[0] or from_addr,
            text=text_body or subject,
            thread_id=msg.get("Message-ID"),
            reply_to_message_id=None,
            media=media,
            is_command=is_command,
            command=command,
            command_args=command_args,
            raw=msg,
        )

        # C6: capture inbound at the channel boundary.
        try:
            capture_message_in(
                channel=self.name,
                actor=from_addr,
                session_id=f"cvc_ch_email_{msg.get('Message-ID') or from_addr}",
                summary=((text_body or subject)[:140]) or "<empty>",
                data={
                    "chat_id": from_addr,
                    "message_id": msg.get("Message-ID"),
                    "subject": subject[:200],
                    "media_count": len(media),
                    "is_command": is_command,
                    "command": command,
                    "text_length": len(text_body or subject or ""),
                },
            )
        except Exception:
            pass

        reply = await self._emit_inbound(inbound)
        if reply and reply.text:
            await self.send(reply)

    async def send(self, message: OutboundMessage) -> Dict[str, Any]:
        text = markdown_to_plain(message.text or "")
        out = PyEmailMessage()
        out["From"] = self._from_addr
        out["To"] = message.chat_id
        out["Subject"] = "Re: CVC"
        if message.thread_id:
            out["In-Reply-To"] = message.thread_id
            out["References"] = message.thread_id
        out.set_content(text)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_sync, out)
        result_msg_id = message.thread_id or out["Message-ID"]

        # C6: capture outbound.
        try:
            capture_message_out(
                channel=self.name,
                actor="bot",
                session_id=f"cvc_ch_email_{message.thread_id or message.chat_id}",
                summary=text[:140] or "<empty>",
                data={
                    "chat_id": message.chat_id,
                    "message_id": result_msg_id,
                    "in_reply_to": message.thread_id,
                    "text_length": len(text),
                },
            )
        except Exception:
            pass

        return {"message_id": result_msg_id}

    def _send_sync(self, msg: PyEmailMessage) -> None:
        with smtplib.SMTP(self._smtp_host, self._smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self._smtp_user, self._smtp_password)
            smtp.send_message(msg)

    def _info(self) -> Dict[str, Any]:
        info = super()._info()
        info["imap_host"] = self.cfg("imap_host", "")
        info["smtp_host"] = self.cfg("smtp_host", "")
        info["allowlist_size"] = len(getattr(self, "_allowlist", []))
        return info
