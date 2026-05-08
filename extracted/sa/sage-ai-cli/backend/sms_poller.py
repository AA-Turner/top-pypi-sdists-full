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
    device_type: str = "",
    deliver_natively: bool = False,
) -> str | None:
    """
    Send a task to a CLI session and await the result.

    When `deliver_natively` is True, the CLI is responsible for delivering the
    reply itself (via iMessage / KDE Connect). The backend skips its own SMTP
    send for that recipient. This is the primary path for carrier-gateway
    senders, since carrier email-to-SMS bridges silently drop most outbound
    replies even when they don't issue a bounce.

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
                "device_type": device_type,
                "deliver_natively": deliver_natively,
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


async def dispatch_native_message(
    uid: str,
    phone: str,
    text: str,
    device_type: str,
    computer_name: str | None = None,
) -> bool:
    """Tell the user's connected CLI to deliver a message via iMessage / KDE Connect.

    Used for outbound announcements / notifications where there's no
    corresponding inbound message — the CLI doesn't need to wait for a result,
    it just delivers the text to the phone. Returns True if at least one CLI
    accepted the dispatch.
    """
    user_sessions = _cli_sessions.get(uid, {})
    if not user_sessions:
        logger.info("Cannot send native message — no online CLI for uid=%s", uid)
        return False

    # Pick the requested computer or the first available
    if computer_name and computer_name.lower() in user_sessions:
        targets = [user_sessions[computer_name.lower()]]
    else:
        targets = [next(iter(user_sessions.values()))]

    payload = {
        "type":          "native_message",
        "phone":         phone,
        "text":          text,
        "device_type":   device_type,
        "computer_name": computer_name or "SAGE",
    }
    sent = 0
    for ws in targets:
        try:
            await ws.send_json(payload)
            sent += 1
        except Exception as exc:
            logger.warning("Failed to send native_message to CLI: %s", exc)
    return sent > 0


def resolve_task_result(task_id: str, output: str, delivered_locally: bool = False) -> None:
    """Called when a CLI WebSocket sends back a result.

    When `delivered_locally` is True, the CLI handled native delivery itself
    (iMessage / KDE Connect). The poller's caller (handle_inbound_email) checks
    its `deliver_natively` flag and skips SMTP regardless, but we record this
    for visibility on the future result.
    """
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
    """Extract `@target: …` prefix.

    Allows multi-word / apostrophe-bearing computer names — e.g.
    `@Layne's Macbook Pro: git status` resolves to target="layne's macbook pro",
    task="git status". Limit target to 40 non-colon chars to avoid slurping
    URLs (`@https://…`) into the target.
    """
    text = (text or "").strip()
    m = re.match(r'^@([^:：\n]{1,40})\s*[:：]\s*', text)
    if m:
        return m.group(1).strip().lower(), text[m.end():].strip()
    return None, text


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
    # Subject includes the computer name so Gmail threads split per device.
    # Replies preserve the subject (Re: SAGE — <name>) and stay in their own
    # thread, while a different computer's emails get their own thread.
    msg["Subject"] = f"SAGE — {computer_name}"
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


# Recent SMTP sends to phone-gateway recipients — used to replay via iMessage
# when carriers bounce the message asynchronously.
# Key: recipient email; Value: dict with text, computer_name, uid, sent_at.
_recent_phone_sends: dict[str, dict] = {}
_RECENT_SEND_TTL = 600  # seconds — bounces typically arrive within ~2 min


# ── Poller state — exposed via /sms/poller-status for debugging ────────────────
_poller_state: dict = {
    "started_at":          None,
    "imap_connected":      False,
    "imap_connected_at":   None,
    "last_idle_activity":  None,
    "last_message_at":     None,
    "last_message_from":   None,
    "messages_processed":  0,
    "tasks_dispatched":    0,
    "last_error":          None,
    "last_error_at":       None,
}


def get_poller_state() -> dict:
    """Snapshot of poller health for the diagnose endpoint."""
    return dict(_poller_state)


def _record_error(exc: Exception) -> None:
    _poller_state["last_error"] = f"{type(exc).__name__}: {exc}"
    _poller_state["last_error_at"] = time.time()


def _record_recent_send(to_addr: str, text: str, computer_name: str, uid: str | None) -> None:
    """Track a phone-gateway send so we can replay via iMessage if it bounces."""
    if not uid or not _is_sms_gateway(to_addr):
        return
    _recent_phone_sends[to_addr.lower()] = {
        "text":          text,
        "computer_name": computer_name,
        "uid":           uid,
        "sent_at":       time.time(),
    }
    # Garbage collect expired entries
    cutoff = time.time() - _RECENT_SEND_TTL
    expired = [k for k, v in _recent_phone_sends.items() if v["sent_at"] < cutoff]
    for k in expired:
        _recent_phone_sends.pop(k, None)


def send_reply(to_addr: str, text: str, computer_name: str = "SAGE", uid: str | None = None) -> None:
    """Send a reply — tries Gmail API first (requires DWD), falls back to SMTP.
    SMS gateway addresses receive a smart-truncated summary instead of the full output.
    """
    if not BRIDGE_EMAIL:
        logger.warning("SAGE_BRIDGE_EMAIL not configured — cannot send reply")
        return

    # Phone-number storage keys (e.g. "phone:6696498725") are not valid email
    # addresses. We can't send announcements/replies to them — the carrier
    # gateway domain only exists in the inbound message's From header.
    if not to_addr or "@" not in to_addr or to_addr.startswith("phone:"):
        logger.info("Skipping reply to non-email contact: %s", to_addr)
        return

    # Track this send before attempting — bounces may arrive after we return
    _record_recent_send(to_addr, text, computer_name, uid)

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


def _lookup_device_type(uid: str, gateway_email: str) -> str:
    """Look up the device_type ('apple'/'android') for the phone behind a
    carrier-gateway address like 4085551234@vtext.com.
    """
    try:
        from .sms_manager import _get_db, _normalize_phone, _phone_contact_key, _contact_doc_id
        local = gateway_email.split("@", 1)[0]
        phone = _normalize_phone(local)
        if not phone:
            return ""
        db = _get_db()
        if db is None:
            return ""
        doc_id = _contact_doc_id(_phone_contact_key(phone))
        doc = db.collection("users").document(uid) \
                 .collection("sms_contacts").document(doc_id).get()
        if doc.exists:
            return (doc.to_dict() or {}).get("device_type", "")
    except Exception as exc:
        logger.debug("Device type lookup failed: %s", exc)
    return ""


async def _handle_bounce(raw_body: str) -> None:
    """Parse a mailer-daemon bounce, find the original phone-gateway recipient,
    and signal the CLI to deliver the message via iMessage / KDE Connect.
    """
    m = re.search(
        r'(?:message to|original recipient|final-recipient[^:]*:|to)\s+<?([\w._%+-]+@[\w.-]+\.\w+)',
        raw_body, re.IGNORECASE,
    )
    if not m:
        logger.debug("Bounce received but couldn't extract recipient")
        return
    failed_addr = m.group(1).lower()
    entry = _recent_phone_sends.get(failed_addr)
    if not entry:
        logger.info("Bounce for %s — no recent send tracked, dropping", failed_addr)
        return
    if (time.time() - entry["sent_at"]) > _RECENT_SEND_TTL:
        logger.info("Bounce for %s — tracked send is too old, dropping", failed_addr)
        _recent_phone_sends.pop(failed_addr, None)
        return

    # Find an online CLI session and signal it with the device_type so the
    # CLI picks the correct delivery path (iMessage vs KDE Connect).
    user_sessions = _cli_sessions.get(entry["uid"], {})
    if not user_sessions:
        logger.warning("Bounce for %s — owner has no online CLI, can't send fallback", failed_addr)
        return
    device_type = _lookup_device_type(entry["uid"], failed_addr)
    ws = next(iter(user_sessions.values()))
    try:
        await ws.send_json({
            "type":          "imessage_fallback",
            "recipient":     failed_addr,
            "text":          entry["text"],
            "computer_name": entry["computer_name"],
            "device_type":   device_type,  # "apple" / "android" / ""
        })
        logger.info("Bounce for %s (device=%s) — signaled CLI fallback", failed_addr, device_type or "auto")
        _recent_phone_sends.pop(failed_addr, None)
    except Exception as exc:
        logger.warning("Failed to signal CLI for fallback: %s", exc)


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

    # Detect bounce notifications BEFORE cleaning the body — a mailer-daemon
    # bounce indicates a previous SMTP reply was rejected by the recipient
    # carrier. If the bounced recipient was a phone-gateway address that we
    # tracked recently, signal the CLI to replay the message via iMessage.
    if "mailer-daemon" in from_addr or "postmaster" in from_addr:
        await _handle_bounce(body)
        return

    cleaned = _clean_body(body).strip()
    if not cleaned:
        logger.info("Inbound from %s: body empty after cleaning — dropping", from_addr)
        return
    body = cleaned

    # Primary: look up by registered contact
    uid = find_user_by_contact_email(from_addr)
    if uid:
        logger.info("Inbound from %s matched contact → uid=%s", from_addr, uid)

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
    _poller_state["tasks_dispatched"] += 1
    logger.info("Task from %s → [%s]: %s", from_addr, target or "any", task[:80])

    import uuid
    task_id = str(uuid.uuid4())
    online = get_online_computers(uid)

    if not online:
        send_reply(
            from_addr,
            "⚠️ No SAGE computers are currently online.\n"
            "Start the bridge on your computer with: sage sms start",
            uid=uid,
        )
        return

    # Decide reply path:
    #   - Apple from SMS gateway: native iMessage (CLI). Apple's thread model
    #     unifies Apple ID + phone, so native delivery lands the reply in the
    #     same iMessage thread the user originally messaged from.
    #   - Android from SMS gateway: SMTP back through the email bridge. KDE
    #     Connect SMS to the user's own phone number files Android's reply in
    #     a SEPARATE self-SMS thread (4085073140-to-4085073140), splitting the
    #     conversation away from the email-bridge thread
    #     (4085073140-to-messages@sageworksai.com). SMTP from
    #     messages@sageworksai.com lands in the email-bridge thread, so the
    #     conversation stays unified.
    #   - Anything else (gmail, regular email): SMTP, same as before.
    device_type = ""
    deliver_natively = False
    if _is_sms_gateway(from_addr):
        device_type = _lookup_device_type(uid, from_addr)
        deliver_natively = device_type == "apple"

    output = await dispatch_to_cli(
        uid, target, task_id, task, from_addr,
        device_type=device_type, deliver_natively=deliver_natively,
    )
    if output:
        # Determine which computer responded for the prefix
        computer_label = target if target and target != "all" else (online[0] if online else "SAGE")
        if deliver_natively:
            # CLI handled delivery itself — skip SMTP. Log only.
            logger.info("Native delivery handled by CLI for %s", from_addr)
        else:
            send_reply(from_addr, output, computer_name=computer_label, uid=uid)


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
    _poller_state["started_at"] = time.time()
    reconnect_delay = 5

    while True:
        mail = None
        try:
            mail = await asyncio.to_thread(_imap_connect)
            reconnect_delay = 5
            _poller_state["imap_connected"] = True
            _poller_state["imap_connected_at"] = time.time()
            logger.info("IMAP connected (%s)", BRIDGE_IMAP_HOST)

            # Drain any messages that arrived while disconnected
            drained = await _drain_and_dispatch(mail)
            if drained:
                logger.info("Initial drain: processed %d unseen message(s)", drained)

            # IDLE loop with safety-net drain.
            #
            # Gmail's IMAP IDLE is unreliable — it sometimes silently stops
            # delivering notifications even though the TCP socket stays alive.
            # If we trusted IDLE alone, inbound mail would queue forever. So
            # we always drain on every loop iteration regardless of whether
            # IDLE fired. The IDLE wait gives us low latency (sub-second)
            # when it works; the unconditional drain caps worst-case latency
            # at 25s when it doesn't.
            #
            # We also NOOP after each IDLE return — if the connection silently
            # died, NOOP raises and we fall through to the outer reconnect
            # loop instead of looping forever against a zombie socket.
            while True:
                activity = await asyncio.to_thread(_imap_idle_wait, mail, 25)
                if activity:
                    _poller_state["last_idle_activity"] = time.time()
                # Health check — raises if connection is dead, triggering reconnect
                await asyncio.to_thread(_imap_noop, mail)
                drained = await _drain_and_dispatch(mail)
                if drained:
                    logger.info(
                        "Drained %d message(s)  (idle_fired=%s)", drained, activity,
                    )

        except asyncio.CancelledError:
            logger.info("SMS poller cancelled")
            _poller_state["imap_connected"] = False
            return
        except Exception as exc:
            _poller_state["imap_connected"] = False
            _record_error(exc)
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


def _imap_noop(mail: imaplib.IMAP4_SSL) -> None:
    """Send NOOP — raises if the connection is dead so the outer loop reconnects.

    Gmail kills IMAP connections after periods of inactivity without sending
    any FIN/RST that imaplib notices. Without an active probe, the poller can
    sit looping against a zombie socket forever. NOOP forces a server response.
    """
    typ, _ = mail.noop()
    if typ != "OK":
        raise RuntimeError(f"IMAP NOOP returned {typ!r} — connection unhealthy")


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


async def _drain_and_dispatch(mail: imaplib.IMAP4_SSL) -> int:
    """Fetch all UNSEEN messages and dispatch each as a task. Returns count."""
    messages = await asyncio.to_thread(_fetch_unseen, mail)
    if messages:
        logger.info(
            "IMAP drain: %d new message(s) — senders: %s",
            len(messages),
            [m.get("from", "?") for m in messages],
        )
    for m in messages:
        _poller_state["messages_processed"] += 1
        _poller_state["last_message_at"] = time.time()
        _poller_state["last_message_from"] = m.get("from")
        asyncio.create_task(handle_inbound_email(m["from"], m["body"]))
    return len(messages)


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
