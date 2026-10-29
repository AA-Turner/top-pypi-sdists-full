"""The code a vendor emailed to a vault account's login email, read by code from that inbox.

`plato vault mint token`'s ``fill_sign_in`` with ``email_code`` types it (:mod:`app_mint`). The
inbox is the one the login world reads (:func:`plato.vault.mail_route.resolve_mail_route`): a
``mail-*`` item in the 1Password ``login`` vault, which Chronos does not serve, so this machine reads
it with ``OP_SERVICE_ACCOUNT_TOKEN``. The code is never printed or shown to the agent.

The extractor follows the login world's ``get_otp._extract_code`` (the agent VM's reader has no SDK
and keeps its own copy), plus the dashed codes some vendors send (Slack: ``ABC-123``).
"""

from __future__ import annotations

import asyncio
import email
import email.header
import email.utils
import imaplib
import os
import re
import ssl
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from email.message import Message
from html import unescape
from typing import Any

from pydantic import SecretStr

from plato.cli.vault import mail
from plato.vault.mail_route import (
    MailFieldReader,
    MailRoute,
    own_inbox_recipient,
    resolve_mail_route,
    shared_inbox_recipient,
)

OP_TOKEN_ENV = "OP_SERVICE_ACCOUNT_TOKEN"
OP_VAULT = "login"
OP_INTEGRATION_NAME = "plato-vault-mint"
OP_INTEGRATION_VERSION = "0.1.0"
# How long code waits for the mail, and how often it looks. Under the page job's 120 s.
WAIT_S = 90.0
POLL_S = 5.0
# A mail this much older than the mint's start still counts (a code the agent asked for at once).
EARLY_S = 60.0
# 1Password answers that mean "this item or field is not there": no route through it. Any other
# error (access, the service) is raised, never read as absence.
OP_ABSENT = frozenset({"itemNotFound", "fieldNotFound", "noMatchingSections"})

_URL_RE = re.compile(r"https?://\S+")
_CODE_ANCHOR_RE = re.compile(
    r"\b(?:verification|security|login|sign[-\s]?in|auth(?:entication)?|"
    r"one[-\s]?time|passcode|pass[-\s]?code|otp|code|pin|confirm)"
    r"\D{0,15}(\d{4,8})",
    re.IGNORECASE,
)
# A dashed code (Slack's ``ABC-123``): two upper-case or digit halves, typed without the dash.
_DASHED_RE = re.compile(r"(?<![\w-])([A-Z0-9]{3,4})-([A-Z0-9]{3,4})(?![\w-])")
_TOKEN_RE = re.compile(r"\b[A-Za-z0-9]{5,8}\b")
_CODE_RE = re.compile(r"\b(\d{4,8})\b")
_YEARISH_RE = re.compile(r"(?:19|20)\d\d$")
_LENGTH_RE = re.compile(r"\b([4-8]|four|five|six|seven|eight)[-\s]?digits?\b", re.IGNORECASE)
_LENGTH_WORDS = {"four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8}
_NOT_CODE_BEFORE_RE = re.compile(
    r"(?:\b[A-Z]{2},?[ \t]+|#[ \t]?|\b(?i:suite|apt|ste|unit)\.?[ \t]*#?[ \t]*|[+($]|\d[.-])\Z"
)
_NOT_CODE_AFTER_RE = re.compile(r"[.-]\d")
_TAG_RE = re.compile(r"<(script|style)\b.*?</\1>|<[^>]+>", re.IGNORECASE | re.DOTALL)


class MailCodeError(Exception):
    """Code cannot read the inbox (no token, no mailbox for the login email, IMAP refused). No value in the text."""


def _announced_length(text: str) -> int | None:
    m = _LENGTH_RE.search(text)
    if not m:
        return None
    word = m.group(1).lower()
    return _LENGTH_WORDS.get(word) or int(word)


def _plausible(text: str, m: re.Match[str], length: int | None) -> bool:
    token = m.group(1)
    if (len(token) == 4 and _YEARISH_RE.match(token)) or (length is not None and len(token) != length):
        return False
    return not (_NOT_CODE_BEFORE_RE.search(text[: m.start(1)]) or _NOT_CODE_AFTER_RE.match(text[m.end(1) :]))


def _alone_on_line(text: str, start: int, end: int) -> bool:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    line_end = len(text) if line_end < 0 else line_end
    return not (text[line_start:start].strip() or text[end:line_end].strip())


def extract_code(text: str) -> str | None:
    """The most code-like token in a mail's subject and body, or None."""
    text = _URL_RE.sub(" ", text or "")
    for m in _DASHED_RE.finditer(text):
        joined = m.group(1) + m.group(2)
        near_code = "code" in text[max(0, m.start() - 60) : m.start()].lower()
        # A phone number or a date is digits only: a dashed code has a letter, or is named a code.
        if any(c.isalpha() for c in joined) and (near_code or _alone_on_line(text, m.start(), m.end())):
            return joined
    length = _announced_length(text)
    for m in _CODE_ANCHOR_RE.finditer(text):
        if _plausible(text, m, length):
            return m.group(1)
    if length is None:
        for token in _TOKEN_RE.findall(text):
            if any(c.isdigit() for c in token) and any(c.isalpha() for c in token):
                return token
    runs = [m for m in _CODE_RE.finditer(text) if _plausible(text, m, length)]
    alone = [m for m in runs if _alone_on_line(text, m.start(1), m.end(1))]
    if alone:
        return alone[0].group(1)
    near = [m for m in runs if "code" in text[max(0, m.start(1) - 40) : m.start(1)].lower()]
    return (near or runs)[-1].group(1) if runs else None


def _body(msg: Message) -> str:
    plain: list[str] = []
    html: list[str] = []
    for part in msg.walk() if msg.is_multipart() else [msg]:
        kind = part.get_content_type()
        if kind not in ("text/plain", "text/html") or part.get_filename():
            continue
        raw = part.get_payload(decode=True)
        if not isinstance(raw, bytes):
            continue
        text = raw.decode(part.get_content_charset() or "utf-8", "replace")
        (plain if kind == "text/plain" else html).append(text)
    if plain:
        return "\n".join(plain)
    return unescape(_TAG_RE.sub(" ", "\n".join(html)))


def _header(msg: Message, name: str) -> str:
    value = msg.get(name)
    return str(email.header.make_header(email.header.decode_header(value))) if value else ""


def recipient(msg: Message) -> str:
    """Who the mail was delivered to: Delivered-To, else To (as the login world reads it)."""
    return (_header(msg, "Delivered-To") or _header(msg, "To")).casefold()


def _received(msg: Message) -> float | None:
    date = msg.get("Date")
    parsed = email.utils.parsedate_to_datetime(date) if date else None
    return parsed.timestamp() if parsed and parsed.tzinfo else None


def sender_domains(hosts: set[str]) -> set[str]:
    """The vendor's mail domains: each host's last two labels (``app.slack.com`` -> ``slack.com``).
    A vendor mails from its own domain, often another subdomain than its sign-in page."""
    return {".".join(h.split(".")[-2:]) for h in hosts if h.count(".") >= 1}


def from_vendor(msg: Message, senders: set[str]) -> bool:
    """The mail's From address is at one of ``senders`` or a subdomain of one."""
    _, address = email.utils.parseaddr(_header(msg, "From"))
    domain = address.rpartition("@")[2].casefold().strip(".")
    return any(domain == d or domain.endswith("." + d) for d in senders)


def to_filter(route: MailRoute, login_email: str | None) -> str | None:
    """The recipient a mail must name: set whenever the inbox holds more than this login's mail."""
    return (
        route.to_contains
        or own_inbox_recipient(login_email, route.imap_user)
        or shared_inbox_recipient(login_email, route.imap_user)
    )


def newest_code(
    route: MailRoute, to: str | None, senders: set[str], since: float, used: frozenset[str] = frozenset()
) -> tuple[str, SecretStr] | None:
    """One look at the inbox: the newest mail since ``since`` (epoch) to ``to``, from the vendor
    (``senders``), that has a code and is not in ``used`` (Message-IDs), as (its Message-ID, the
    code); or None. A login's inbox can be a person's own: any other sender's mail is skipped."""
    imap: Any = None
    try:
        imap = mail.IMAP_SSL(
            mail.IMAP_HOST, mail.IMAP_PORT, ssl_context=ssl.create_default_context(), timeout=mail.IMAP_TIMEOUT_S
        )
        imap.login(route.imap_user, route.imap_password)
        imap.select("INBOX", readonly=True)
        day = datetime.fromtimestamp(since - 86400, UTC).strftime("%d-%b-%Y")
        # Only the vendor's mail since yesterday, all of it: a busy inbox cannot push a code out.
        # FROM matches a substring; from_vendor below checks the domain exactly.
        nums: set[bytes] = set()
        for domain in sorted(senders):
            status, data = imap.search(None, "SINCE", day, "FROM", f'"{domain}"')
            if status != "OK":
                raise MailCodeError(f"the inbox {route.item} refused the search ({status})")
            nums.update((data[0] or b"").split() if data else [])
        for num in sorted(nums, key=int, reverse=True):
            status, parts = imap.fetch(num, "(BODY.PEEK[])")
            raw = next((p[1] for p in parts or [] if isinstance(p, tuple) and len(p) > 1), None)
            if status != "OK" or not isinstance(raw, bytes):
                raise MailCodeError(f"the inbox {route.item} refused a fetch ({status})")
            msg = email.message_from_bytes(raw)
            received = _received(msg)
            if received is None or received < since:
                continue
            if (to and to.casefold() not in recipient(msg)) or not from_vendor(msg, senders):
                continue
            mail_id = msg.get("Message-ID") or f"{route.item}:{num.decode()}"
            if mail_id in used:
                continue
            code = extract_code(f"{_header(msg, 'Subject')}\n{_body(msg)}")
            if code:
                return mail_id, SecretStr(code)
        return None
    except (imaplib.IMAP4.error, OSError) as e:
        raise MailCodeError(f"the inbox {route.item} could not be read ({type(e).__name__})") from None
    finally:
        if imap is not None:
            try:
                imap.logout()
            except (imaplib.IMAP4.error, OSError):
                pass


def op_reader(token: str) -> MailFieldReader:
    """An async ``read(item, field)`` over the 1Password ``login`` vault; None for a missing item or field."""
    box: dict[str, Any] = {}

    async def read(item: str, field: str) -> str | None:
        try:
            from onepassword.client import Client  # the pi extra
        except ImportError:
            raise MailCodeError("reading the inbox needs the onepassword-sdk package (the pi extra)") from None
        if "client" not in box:
            box["client"] = await Client.authenticate(
                auth=token, integration_name=OP_INTEGRATION_NAME, integration_version=OP_INTEGRATION_VERSION
            )
        ref = f"op://{OP_VAULT}/{item}/{field}"
        try:
            got = await box["client"].secrets.resolve_all([ref])
        except Exception as e:  # noqa: BLE001 - its text can quote the reference, not a value
            raise MailCodeError(f"1Password could not be read ({type(e).__name__})") from None
        return op_value(got, ref, item)

    return read


def op_value(got: Any, ref: str, item: str) -> str | None:
    """The secret of ``ref`` in a ``resolve_all`` answer; None when the item or field is not there."""
    one = got.individual_responses.get(ref)
    error = getattr(one, "error", None)
    if error is not None:
        kind = str(getattr(getattr(error, "type", None), "value", getattr(error, "type", "")))
        if kind in OP_ABSENT:
            return None
        raise MailCodeError(f"1Password could not read {item} ({kind or 'unknown error'})")
    content = getattr(one, "content", None)
    return content.secret if content is not None else None


class EmailCodeReader:
    """The emailed code of one vault account, for one mint. The mailbox is found on first use."""

    def __init__(
        self,
        account: str,
        login_email: Callable[[], str | None],
        senders: set[str],
        reader: Callable[[], MailFieldReader] | None = None,
        clock: Callable[[], float] = time.time,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.account = account
        self.login_email = login_email
        self.senders = senders
        self.reader = reader or self._op_reader
        self.clock = clock
        self.sleep = sleep
        self.started = clock()
        self._route: tuple[MailRoute, str | None] | None = None
        # The mails whose code was typed: a second fill waits for a new mail (a resent code).
        self.used: set[str] = set()
        self._last: str | None = None

    @staticmethod
    def _op_reader() -> MailFieldReader:
        token = os.environ.get(OP_TOKEN_ENV)
        if not token:
            raise MailCodeError(f"code reads the inbox from 1Password: set {OP_TOKEN_ENV}")
        return op_reader(token)

    def route(self) -> tuple[MailRoute, str | None]:
        if self._route is None:
            address = self.login_email()
            if not address:
                raise MailCodeError("the vault item has no login email, so code knows no inbox")
            # The fill runs on the page thread, where playwright's event loop is running: the
            # 1Password reads get a loop of their own on a thread of their own.
            read = self.reader()

            def resolve() -> MailRoute | None:
                return asyncio.run(resolve_mail_route(read, self.account, address))

            with ThreadPoolExecutor(max_workers=1) as pool:
                found = pool.submit(resolve).result()
            if found is None:
                raise MailCodeError(f"no mail-* item in the login vault reads the mail of {address}")
            self._route = (found, to_filter(found, address))
        return self._route

    def wait(self, wait_s: float = WAIT_S) -> SecretStr | None:
        """The newest code mailed since the mint started and not typed yet, waiting up to ``wait_s``."""
        route, to = self.route()
        since = self.started - EARLY_S
        end = self.clock() + wait_s
        while True:
            found = newest_code(route, to, self.senders, since, frozenset(self.used))
            if found is not None:
                self._last = found[0]
                return found[1]
            if self.clock() >= end:
                return None
            self.sleep(min(POLL_S, max(0.0, end - self.clock())))

    def typed(self) -> None:
        """The last code from :meth:`wait` was typed: never hand it out again."""
        if self._last is not None:
            self.used.add(self._last)
            self._last = None
