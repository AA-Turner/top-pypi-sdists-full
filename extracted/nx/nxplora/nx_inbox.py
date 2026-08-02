"""nx_inbox.py — inbound email for NX agents (the receive half of /supply email).

Poll an agent's mailbox over IMAP; hand each NEW human message to the agent so it can reply
over SMTP (the caller does the reply, reusing the stored app-password). stdlib imaplib →
macOS / Windows / Linux, no new dependency. The same app-password /supply saved for SMTP
also authenticates IMAP (Gmail/Workspace: imap.gmail.com, etc.).

LOOP-SAFETY (critical): an operator often supplies their OWN address as the agent's address
(victor@nexplora.ai sends AS the agent AND the operator replies FROM it), so "skip mail from
myself" would wrongly skip the operator's replies. Instead every agent-sent email carries an
`X-NX-Agent` header; fetch_new SKIPS any message carrying it (our own sends + our replies
echoing back), plus bounces/auto-replies. A human's hand-typed message has no such header, so
it is the only thing the agent answers — no infinite loop, even when from == to.
"""
import email
import email.utils
import imaplib
import re
from email.header import decode_header

# SMTP host -> IMAP host for the providers /supply auto-detects; generic smtp.X -> imap.X.
_IMAP_HOSTS = {
    "smtp.gmail.com":        "imap.gmail.com",
    "smtp-mail.outlook.com": "outlook.office365.com",
    "smtp.mail.yahoo.com":   "imap.mail.yahoo.com",
    "smtp.mail.me.com":      "imap.mail.me.com",
}


def imap_host_for(smtp_host: str) -> str:
    h = (smtp_host or "").strip().lower()
    if h in _IMAP_HOSTS:
        return _IMAP_HOSTS[h]
    if h.startswith("smtp."):
        return "imap." + h[len("smtp."):]
    return h  # last resort: try the same host


def _decode(s: str) -> str:
    if not s:
        return ""
    parts = []
    for chunk, enc in decode_header(s):
        if isinstance(chunk, bytes):
            try:
                parts.append(chunk.decode(enc or "utf-8", "replace"))
            except Exception:
                parts.append(chunk.decode("utf-8", "replace"))
        else:
            parts.append(chunk)
    return "".join(parts)


def strip_quotes(body: str) -> str:
    """Trim quoted reply history so the agent answers the NEW text, not the whole thread."""
    lines = []
    for ln in (body or "").splitlines():
        s = ln.strip()
        if s.startswith(">"):
            continue
        if re.match(r"^On .*wrote:$", s):
            break
        if s.startswith("-----Original Message-----") or s.startswith("________________________________"):
            break
        lines.append(ln)
    trimmed = "\n".join(lines).strip()
    return trimmed or (body or "").strip()


def _plain_body(msg) -> str:
    """Best-effort plain-text body."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition") or ""):
                try:
                    return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                except Exception:
                    continue
        return ""
    try:
        return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", "replace")
    except Exception:
        return str(msg.get_payload() or "")


def is_own_or_auto(msg) -> bool:
    """True if this message is one WE sent (carries X-NX-Agent) or a bounce/auto-reply — never answer these."""
    if (msg.get("X-NX-Agent") or "").strip():
        return True
    auto = (msg.get("Auto-Submitted", "") or "").lower()
    if "auto-replied" in auto or "auto-generated" in auto:
        return True
    if (msg.get("X-Autoreply") or msg.get("X-Autorespond")):
        return True
    frm = email.utils.parseaddr(msg.get("From", ""))[1].strip().lower()
    local = frm.split("@", 1)[0] if "@" in frm else frm
    if local in ("mailer-daemon", "postmaster") or local.startswith("no-reply") or local.startswith("noreply"):
        return True
    return False


# A machine sender's local-part, VENDOR-AGNOSTIC. GitHub is only one example — this matches the
# shape any system uses (CI, monitoring, ticketing, billing, shipping, SaaS product alerts):
# no-reply@, notifications@, alerts@, jenkins@, build-bot@, alerts+xyz@, team.notifications@, …
_MACHINE_LOCAL = re.compile(
    r"^(?:.*[._+-])?(?:"
    r"no-?reply|do-?not-?reply|donotreply|reply-?to-?this|"
    r"notification[s]?|notify|alert[s]?|warning[s]?|"
    r"ci|cd|build[s]?|pipeline[s]?|deploy|jenkins|"
    r"auto|automated|automation|bot|robot|daemon|system|sysadmin|"
    r"monitor|monitoring|status|uptime|oncall|pager|"
    r"mailer|mail|mailman|bounce[s]?|postmaster|maildaemon|"
    r"support-?bot|helpdesk|ticket[s]?|jira|"
    r"digest|newsletter|updates?|announce|announcements?|marketing|billing|invoices?|receipts?"
    r")(?:[._+-].*)?$"
)


def fetch_telegram_new(token, offset=None, limit=20):
    """New HUMAN messages sent to the agent's bot, for the /takeoff loop.

    Returns (messages, next_offset) where each message is
    {text, who, chat_id, message_id}. Telegram's getUpdates is offset-based: passing
    `offset = last_update_id + 1` both fetches the next batch AND confirms the previous one, so
    each message is handed over exactly once (the same at-most-once contract as the IMAP side).
    Messages from bots — including our own agent's replies — are skipped, so the bot can never
    talk to itself. Best-effort: returns ([], offset) on any failure."""
    import requests
    out = []
    next_off = offset
    try:
        params = {"timeout": 0, "limit": int(limit)}
        if offset is not None:
            params["offset"] = int(offset)
        r = requests.get(f"https://api.telegram.org/bot{token}/getUpdates", params=params, timeout=20).json()
        if not r.get("ok"):
            return out, next_off
        for u in (r.get("result") or []):
            uid = u.get("update_id")
            if uid is not None:
                next_off = int(uid) + 1
            m = (u.get("message") or u.get("channel_post") or {})
            frm = m.get("from") or {}
            if frm.get("is_bot"):
                continue                      # loop-safety: never answer a bot (incl. ourselves)
            text = (m.get("text") or "").strip()
            chat = m.get("chat") or {}
            if not text or not chat.get("id"):
                continue                      # ignore stickers/photos/service messages
            out.append({
                "text":       text,
                "who":        frm.get("first_name") or frm.get("username") or "someone",
                "chat_id":    str(chat["id"]),
                "message_id": m.get("message_id"),
            })
    except Exception:
        pass
    return out, next_off


def looks_like_notification(msg) -> bool:
    """True if this is an automated NOTIFICATION/alert from ANY system — CI, monitoring, ticketing,
    billing, a SaaS product, a mailing list — not a person writing to the agent. (GitHub is just one
    example; nothing here is vendor-specific.) The agent must NOT reply to these: it briefs the
    OPERATOR with the diagnosis + next action instead.

    Signals, strongest first:
      1. list/bulk headers any notifier sets — List-Id, List-Unsubscribe, Precedence: bulk|list,
         Auto-Submitted, Feedback-ID, X-*-Notification/-Reason/-Alert/-Campaign/-Mailer style keys;
      2. a no-reply Reply-To (they don't want an answer, by construction);
      3. a machine local-part (_MACHINE_LOCAL) — no-reply@, alerts@, ci@, jenkins@, billing@, …
    A real person on a normal address matches none of these and still gets a reply."""
    if msg.get("List-Id") or msg.get("List-Unsubscribe") or msg.get("List-Post") or msg.get("Feedback-ID"):
        return True
    if (msg.get("Precedence", "") or "").lower() in ("bulk", "list", "auto_reply", "junk"):
        return True
    if (msg.get("Auto-Submitted", "") or "").lower().startswith("auto") or msg.get("X-Auto-Response-Suppress"):
        return True
    # vendor-neutral header shapes: X-GitHub-Reason, X-Jira-..., X-SES-..., X-Campaign-Id, X-Mailgun-...
    for k in (msg.keys() if hasattr(msg, "keys") else []):
        kl = str(k).lower()
        if kl.startswith("x-") and any(t in kl for t in ("notification", "-reason", "alert", "campaign",
                                                         "mailer", "bulk", "autoreply", "auto-reply")):
            return True
    rt = email.utils.parseaddr(msg.get("Reply-To", ""))[1].strip().lower()
    if rt and _MACHINE_LOCAL.match(rt.split("@", 1)[0]):
        return True
    frm = email.utils.parseaddr(msg.get("From", ""))[1].strip().lower()
    local = frm.split("@", 1)[0] if "@" in frm else frm
    return bool(local and _MACHINE_LOCAL.match(local))


def fetch_new(smtp_host, imap_port, user, password, limit=10):
    """Return NEW messages as dicts {uid, from_addr, subject, body, message_id, references,
    is_notification}. Skips our own agent-sent mail (X-NX-Agent) + bounces/auto-replies. Marks
    an automated notification with is_notification=True so the caller alerts the operator instead
    of replying to the bot. Fetching marks messages \\Seen (handed over once). [] on failure."""
    host = imap_host_for(smtp_host)
    out = []
    M = None
    try:
        M = imaplib.IMAP4_SSL(host, int(imap_port or 993), timeout=20)
        M.login(user, password)
        M.select("INBOX")
        typ, data = M.search(None, "UNSEEN")
        if typ != "OK":
            return out
        ids = (data[0].split() if (data and data[0]) else [])[-int(limit or 10):]
        for i in ids:
            try:
                typ, md = M.fetch(i, "(RFC822)")
                if typ != "OK" or not md or not md[0]:
                    continue
                msg = email.message_from_bytes(md[0][1])
                if is_own_or_auto(msg):
                    continue  # loop-safety (already marked \Seen by the fetch)
                out.append({
                    "uid":             i.decode() if isinstance(i, bytes) else str(i),
                    "from_addr":       email.utils.parseaddr(msg.get("From", ""))[1].strip(),
                    "subject":         _decode(msg.get("Subject", "")),
                    "body":            strip_quotes(_plain_body(msg)),
                    "message_id":      (msg.get("Message-ID", "") or "").strip(),
                    "references":      (msg.get("References", "") or msg.get("Message-ID", "") or "").strip(),
                    "is_notification": looks_like_notification(msg),
                })
            except Exception:
                continue
    except Exception:
        pass
    finally:
        try:
            if M is not None:
                M.logout()
        except Exception:
            pass
    return out
