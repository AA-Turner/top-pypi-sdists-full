"""
SAGE central SMS/message bridge — server-side.

SAGE owns a single bridge email address (configured via env vars).
Users message that address from iMessage or Gmail.
The backend receives the email, authenticates the sender against
their registered contacts, and routes the task to the right CLI
session via WebSocket.

Environment variables (set in Cloud Run):
  SAGE_BRIDGE_EMAIL          — e.g. message@sageworksai.com
  SAGE_BRIDGE_APP_PASSWORD   — Gmail/iCloud app password for that account
  SAGE_BRIDGE_IMAP_HOST      — default: imap.gmail.com
  SAGE_BRIDGE_SMTP_HOST      — default: smtp.gmail.com
  SAGE_BRIDGE_SMTP_PORT      — default: 587
  SAGE_BRIDGE_DISPLAY_EMAIL  — shown to users, defaults to SAGE_BRIDGE_EMAIL

The CLI never touches email.  It opens a WebSocket to /ws/sms,
authenticates with its SAGE token, and waits for tasks.
"""

from __future__ import annotations

import asyncio
import email as _email_mod
import email.utils
import imaplib
import logging
import os
import re
import smtplib
import time
from email.mime.text import MIMEText
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import WebSocket

logger = logging.getLogger("sage.sms_poller")

# ── Configuration from environment ────────────────────────────────────────────

BRIDGE_EMAIL       = os.environ.get("SAGE_BRIDGE_EMAIL",         "messages@sageworksai.com")
BRIDGE_PASSWORD    = os.environ.get("SAGE_BRIDGE_APP_PASSWORD",  "")
BRIDGE_IMAP_HOST   = os.environ.get("SAGE_BRIDGE_IMAP_HOST",     "imap.gmail.com")
BRIDGE_SMTP_HOST   = os.environ.get("SAGE_BRIDGE_SMTP_HOST",     "smtp.gmail.com")
BRIDGE_SMTP_PORT   = int(os.environ.get("SAGE_BRIDGE_SMTP_PORT", "587"))
# Address shown to users — defaults to the bridge email itself
DISPLAY_EMAIL      = os.environ.get("SAGE_BRIDGE_DISPLAY_EMAIL", BRIDGE_EMAIL)

# ── Active CLI WebSocket sessions ──────────────────────────────────────────────
# { uid: { computer_name: WebSocket } }
_cli_sessions: dict[str, dict[str, "WebSocket"]] = {}

# Pending task replies: { task_id: asyncio.Future }
_pending: dict[str, "asyncio.Future[str]"] = {}


def register_cli_session(uid: str, computer_name: str, ws: "WebSocket") -> None:
    _cli_sessions.setdefault(uid, {})[computer_name.lower()] = ws
    logger.info("CLI connected: uid=%s computer=%s", uid, computer_name)


def unregister_cli_session(uid: str, computer_name: str) -> None:
    user_sessions = _cli_sessions.get(uid, {})
    user_sessions.pop(computer_name.lower(), None)
    if not user_sessions:
        _cli_sessions.pop(uid, None)
    logger.info("CLI disconnected: uid=%s computer=%s", uid, computer_name)


def get_online_computers(uid: str) -> list[str]:
    return list(_cli_sessions.get(uid, {}).keys())


async def dispatch_to_cli(
    uid: str,
    computer_name: str | None,
    task_id: str,
    task: str,
    from_addr: str,
) -> str | None:
    """
    Send a task to a CLI session and await the result.
    Returns the output string, or None if no session is available.
    """
    user_sessions = _cli_sessions.get(uid, {})
    if not user_sessions:
        return None

    # Route: specific computer, @all, or first available
    if computer_name == "all":
        targets = list(user_sessions.values())
    elif computer_name and computer_name in user_sessions:
        targets = [user_sessions[computer_name]]
    elif computer_name and computer_name not in user_sessions:
        return f"❌ [{computer_name}] is not online. Online: {', '.join(user_sessions) or 'none'}"
    else:
        targets = [next(iter(user_sessions.values()))]  # first available

    loop = asyncio.get_event_loop()
    futures: list["asyncio.Future[str]"] = []
    for ws in targets:
        fut: asyncio.Future[str] = loop.create_future()
        _pending[task_id] = fut
        try:
            await ws.send_json({
                "type": "task",
                "task_id": task_id,
                "task": task,
                "from": from_addr,
            })
            futures.append(fut)
        except Exception as exc:
            logger.warning("Could not send task to CLI: %s", exc)
            _pending.pop(task_id, None)

    if not futures:
        return None

    try:
        # Wait up to 3 minutes for the CLI to respond
        results = await asyncio.wait_for(
            asyncio.gather(*futures, return_exceptions=True),
            timeout=180,
        )
        outputs = [r for r in results if isinstance(r, str)]
        return "\n\n".join(outputs) if outputs else "Task completed."
    except asyncio.TimeoutError:
        _pending.pop(task_id, None)
        return "⏱ Task timed out (>3 min). Check your terminal for progress."


def resolve_task_result(task_id: str, output: str) -> None:
    """Called when a CLI WebSocket sends back a result."""
    fut = _pending.pop(task_id, None)
    if fut and not fut.done():
        fut.set_result(output)


# ── Email utilities ────────────────────────────────────────────────────────────

def _clean_body(raw: str) -> str:
    lines = raw.splitlines()
    clean: list[str] = []
    for line in lines:
        lower = line.strip().lower()
        if re.match(r'^on .{5,80} wrote:$', lower):
            break
        if lower.startswith(("--\n", "-- \n", ">>>", "from:", "sent:", "subject:")):
            break
        clean.append(line)
    return "\n".join(clean).strip()


def _parse_routing(text: str) -> tuple[str | None, str]:
    m = re.match(r'^@([\w\-]+)\s*[:：]\s*', text.strip())
    if m:
        return m.group(1).lower(), text[m.end():].strip()
    return None, text.strip()


# Known SMS-to-email gateway domains — replies go back as SMS
_SMS_GATEWAY_DOMAINS = {
    "vtext.com", "vzwpix.com",           # Verizon
    "txt.att.net", "mms.att.net",        # AT&T
    "tmomail.net", "msg.fi.google.com",  # T-Mobile / Google Fi
    "messaging.sprintpcs.com",           # Sprint
    "mymetropcs.com",                    # Metro PCS
    "mypixmessages.com",                 # Pix messaging
    "mmst5.tracfone.com",               # TracFone
    "sms.myboostmobile.com",            # Boost Mobile
}

SMS_MAX_CHARS = 300  # keep SMS replies concise; carriers split at 160 chars


def _is_sms_gateway(addr: str) -> bool:
    domain = addr.split("@")[-1].lower() if "@" in addr else ""
    if domain in _SMS_GATEWAY_DOMAINS:
        return True
    # Heuristic: local-part is all digits (phone number)
    local = addr.split("@")[0] if "@" in addr else ""
    return bool(re.match(r"^\d{7,15}$", local))


def _truncate_for_sms(text: str) -> str:
    """Condense a long SAGE response to SMS-friendly length."""
    text = text.strip()
    if len(text) <= SMS_MAX_CHARS:
        return text
    # Take first meaningful sentences up to the limit
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = ""
    for s in sentences:
        candidate = (result + " " + s).strip() if result else s
        if len(candidate) <= SMS_MAX_CHARS - 4:
            result = candidate
        else:
            break
    if not result:
        result = text[: SMS_MAX_CHARS - 4]
    return result + " ..."


def _chunk_text(text: str, max_chars: int = 1500) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    paras = [p.strip() for p in re.split(r'\n{2,}', text) if p.strip()]
    current = ""
    for para in paras:
        candidate = (current + "\n\n" + para).strip() if current else para
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)
            if len(para) > max_chars:
                for i in range(0, len(para), max_chars - 20):
                    chunks.append(para[i:i + max_chars - 20])
                current = ""
            else:
                current = para
    if current:
        chunks.append(current)
    return chunks or [text[:max_chars]]


def _build_mime(to_addr: str, text: str, computer_name: str, part_info: str = "") -> MIMEText:
    msg = MIMEText(f"[{computer_name}]{part_info} {text}")
    msg["From"] = f"SAGE AI <{DISPLAY_EMAIL or BRIDGE_EMAIL}>"
    msg["To"] = to_addr
    msg["Subject"] = "SAGE"
    return msg


def _send_via_gmail_api(to_addr: str, raw_mime: bytes) -> bool:
    """Send one message via Gmail REST API using service account + Domain-Wide Delegation."""
    import base64
    try:
        import google.auth
        import google.auth.transport.requests as google_requests

        creds, _ = google.auth.default(scopes=["https://mail.google.com/"])
        # Domain-Wide Delegation: impersonate the bridge inbox
        if hasattr(creds, "with_subject"):
            creds = creds.with_subject(BRIDGE_EMAIL)
        else:
            logger.debug("Gmail API: credentials don't support DWD — falling back to SMTP")
            return False

        creds.refresh(google_requests.Request())
        raw_b64 = base64.urlsafe_b64encode(raw_mime).decode()

        import httpx
        r = httpx.post(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            json={"raw": raw_b64},
            headers={
                "Authorization": f"Bearer {creds.token}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        if r.status_code == 200:
            return True
        logger.debug("Gmail API returned %s: %s", r.status_code, r.text[:200])
        return False
    except Exception as exc:
        logger.debug("Gmail API unavailable: %s", exc)
        return False


def _send_via_smtp(mime_msgs: list[MIMEText]) -> bool:
    """Send via SMTP with app password."""
    try:
        srv = smtplib.SMTP(BRIDGE_SMTP_HOST, BRIDGE_SMTP_PORT)
        srv.ehlo(); srv.starttls(); srv.ehlo()
        srv.login(BRIDGE_EMAIL, BRIDGE_PASSWORD)
        for i, msg in enumerate(mime_msgs):
            srv.send_message(msg)
            if i < len(mime_msgs) - 1:
                time.sleep(0.4)
        srv.quit()
        return True
    except smtplib.SMTPAuthenticationError as exc:
        if exc.smtp_code == 534:
            logger.error(
                "SMTP blocked (534) — Google requires browser sign-in for new accounts. "
                "Fix: open mail.google.com, sign into %s, then retry. "
                "Permanent fix: enable Domain-Wide Delegation in Google Workspace Admin.",
                BRIDGE_EMAIL,
            )
        else:
            logger.error("SMTP auth error %s: %s", exc.smtp_code, exc.smtp_error)
        return False
    except Exception as exc:
        logger.error("SMTP failed: %s", exc)
        return False


def send_reply(to_addr: str, text: str, computer_name: str = "SAGE") -> None:
    """Send a reply — tries Gmail API first (requires DWD), falls back to SMTP.
    SMS gateway addresses receive a smart-truncated summary instead of the full output.
    """
    if not BRIDGE_EMAIL:
        logger.warning("SAGE_BRIDGE_EMAIL not configured — cannot send reply")
        return

    # For SMS gateways, condense the response to fit phone screen limits
    if _is_sms_gateway(to_addr):
        text = _truncate_for_sms(text)

    chunks = _chunk_text(text)
    total = len(chunks)
    sent = 0

    for i, chunk in enumerate(chunks):
        part_info = f" ({i+1}/{total})" if total > 1 else ""
        msg = _build_mime(to_addr, chunk, computer_name, part_info)
        raw = msg.as_bytes()

        if _send_via_gmail_api(to_addr, raw):
            sent += 1
        elif BRIDGE_PASSWORD and _send_via_smtp([msg]):
            sent += 1
        else:
            logger.error("Could not send reply to %s — all methods failed", to_addr)
            break

    if sent:
        logger.info("Replied to %s (%d/%d parts)", to_addr, sent, total)


# ── Inbound email handler ──────────────────────────────────────────────────────

async def handle_inbound_email(from_addr: str, body: str) -> None:
    """
    Process one inbound email: route task to CLI, reply.

    Authorization: first try the contact reverse-index (registered contacts).
    If the sender isn't registered, fall back to the owner of any online
    computer — this handles phone SMS-gateway addresses (e.g. 4085073140@vtext.com)
    that weren't explicitly registered but come from the bridge owner's phone.
    """
    from .sms_manager import find_user_by_contact_email

    from_addr = from_addr.lower().strip()
    body = _clean_body(body).strip()
    if not body:
        return

    # Primary: look up by registered contact
    uid = find_user_by_contact_email(from_addr)

    # Fallback: if unregistered, route to the owner of any currently online computer
    if uid is None:
        online_uids = list(_cli_sessions.keys())
        if len(online_uids) == 1:
            uid = online_uids[0]
            logger.info(
                "Unregistered sender %s → routing to single online user %s",
                from_addr, uid,
            )
        elif len(online_uids) > 1:
            logger.info(
                "Unregistered sender %s — multiple users online, cannot auto-route. "
                "Register this address: sage sms contacts add %s",
                from_addr, from_addr,
            )
            return
        else:
            logger.info("Unregistered sender %s — no computers online", from_addr)
            return

    target, task = _parse_routing(body)
    logger.info("Task from %s → [%s]: %s", from_addr, target or "any", task[:80])

    import uuid
    task_id = str(uuid.uuid4())
    online = get_online_computers(uid)

    if not online:
        send_reply(
            from_addr,
            "⚠️ No SAGE computers are currently online.\n"
            "Start the bridge on your computer with: sage sms start",
        )
        return

    output = await dispatch_to_cli(uid, target, task_id, task, from_addr)
    if output:
        # Determine which computer responded for the prefix
        computer_label = target if target and target != "all" else (online[0] if online else "SAGE")
        send_reply(from_addr, output, computer_name=computer_label)


# ── IMAP IDLE poller (runs as asyncio background task) ────────────────────────

async def run_imap_poller() -> None:
    """
    Persistent IMAP IDLE loop for the SAGE bridge inbox.
    Runs forever in the background; reconnects on failure.
    """
    if not BRIDGE_EMAIL or not BRIDGE_PASSWORD:
        logger.warning(
            "SAGE_BRIDGE_EMAIL / SAGE_BRIDGE_APP_PASSWORD not set — "
            "SMS bridge disabled. Set these in Cloud Run env vars."
        )
        return

    logger.info("SMS poller starting for %s", BRIDGE_EMAIL)
    reconnect_delay = 5

    while True:
        mail = None
        try:
            mail = await asyncio.to_thread(_imap_connect)
            reconnect_delay = 5
            logger.info("IMAP connected (%s)", BRIDGE_IMAP_HOST)

            # Drain any messages that arrived while disconnected
            await _drain_and_dispatch(mail)

            # IDLE loop
            while True:
                activity = await asyncio.to_thread(_imap_idle_wait, mail, 25)
                if activity:
                    await _drain_and_dispatch(mail)

        except asyncio.CancelledError:
            logger.info("SMS poller cancelled")
            return
        except Exception as exc:
            logger.warning("IMAP error: %s — reconnecting in %ds", exc, reconnect_delay)
            await asyncio.sleep(reconnect_delay)
            reconnect_delay = min(reconnect_delay * 2, 120)
        finally:
            if mail:
                try:
                    mail.logout()
                except Exception:
                    pass


def _imap_connect() -> imaplib.IMAP4_SSL:
    mail = imaplib.IMAP4_SSL(BRIDGE_IMAP_HOST)
    mail.login(BRIDGE_EMAIL, BRIDGE_PASSWORD)
    mail.select("INBOX")
    return mail


def _imap_idle_wait(mail: imaplib.IMAP4_SSL, timeout: int = 25) -> bool:
    """Send IMAP IDLE, block until notification or timeout. Returns True if activity."""
    try:
        tag = mail._new_tag().decode()
        mail.send(f"{tag} IDLE\r\n".encode())
        resp = mail.readline()
        if not resp.startswith(b"+"):
            mail.send(b"DONE\r\n")
            return False
        mail.sock.settimeout(timeout)
        try:
            line = mail.readline()
        except (OSError, TimeoutError):
            line = b""
        finally:
            mail.sock.settimeout(None)
        mail.send(b"DONE\r\n")
        mail.readline()  # consume tagged OK
        return bool(line and line.strip())
    except Exception:
        return False


async def _drain_and_dispatch(mail: imaplib.IMAP4_SSL) -> None:
    """Fetch all UNSEEN messages and dispatch each as a task."""
    messages = await asyncio.to_thread(_fetch_unseen, mail)
    for m in messages:
        asyncio.create_task(handle_inbound_email(m["from"], m["body"]))


def _extract_text(msg: _email_mod.message.Message) -> str:
    """Extract the best plain-text body from a (possibly multipart) email."""
    if msg.is_multipart():
        # Prefer text/plain; fall back to text/html stripped of tags
        plain = html = ""
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == "text/plain" and not plain:
                plain = part.get_payload(decode=True).decode(
                    part.get_content_charset("utf-8"), errors="replace"
                )
            elif ct == "text/html" and not html:
                raw = part.get_payload(decode=True).decode(
                    part.get_content_charset("utf-8"), errors="replace"
                )
                html = re.sub(r"<[^>]+>", " ", raw)
        return plain or html
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(msg.get_content_charset("utf-8") or "utf-8", errors="replace")
        return msg.get_payload() or ""


def _fetch_unseen(mail: imaplib.IMAP4_SSL) -> list[dict]:
    results = []
    _, data = mail.search(None, "UNSEEN")
    ids = data[0].split() if data[0] else []
    for mid in ids:
        try:
            # Fetch full RFC822 message — handles multipart/html/plain correctly
            _, raw_data = mail.fetch(mid, "(RFC822)")
            mail.store(mid, "+FLAGS", "\\Seen")
            raw = raw_data[0][1] if isinstance(raw_data[0], tuple) else b""
            msg = _email_mod.message_from_bytes(raw)
            from_addr = _email_mod.utils.parseaddr(msg.get("From", ""))[1].lower().strip()
            body_text = _extract_text(msg)
            if from_addr and body_text.strip():
                results.append({"from": from_addr, "body": body_text})
        except Exception as exc:
            logger.warning("Failed to fetch message %s: %s", mid, exc)
    return results
