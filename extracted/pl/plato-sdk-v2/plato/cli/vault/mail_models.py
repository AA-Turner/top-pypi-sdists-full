"""Pydantic models for `plato vault mail`: what goes to the login console and what comes back."""

from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

# The console's item name: ``mail-{slugify(account)}`` (expd op_client.mail_item_name and
# login_snapshots.slugify). The CLI makes the same name, so a dry run names the real item.
_SLUG_RE = re.compile(r"[^a-z0-9]+")
MAIL_PREFIX = "mail-"


def slugify(value: str) -> str:
    """Lowercase, non-alnum -> ``_``, trimmed. A copy of expd ``login_snapshots.slugify``."""
    return _SLUG_RE.sub("_", (value or "").lower()).strip("_")


def mail_item_name(account: str) -> str:
    return f"{MAIL_PREFIX}{slugify(account)}"


def normalize_app_password(raw: str) -> str:
    """Gmail shows an app password as four groups of four letters. All whitespace goes."""
    return "".join(raw.split())


class MailCheckStatus(StrEnum):
    """The result of one IMAP sign-in. Each value has its own exit code (``CHECK_EXIT``)."""

    ok = "ok"
    auth_failed = "auth_failed"
    unreachable = "unreachable"
    tls_error = "tls_error"


# 0 = signed in. 1 = the server refused the address or the password. 2 = no answer (as ConsoleUnreachable).
# 6 = the TLS handshake failed, which is a network or proxy fault, not a bad password.
CHECK_EXIT: dict[MailCheckStatus, int] = {
    MailCheckStatus.ok: 0,
    MailCheckStatus.auth_failed: 1,
    MailCheckStatus.unreachable: 2,
    MailCheckStatus.tls_error: 6,
}


class WriteOutcome(StrEnum):
    created = "created"
    updated = "updated"
    dry_run = "dry_run"


def _check_address(value: str) -> str:
    value = value.strip()
    local, at, domain = value.partition("@")
    # ASCII only: the readers sign in with imaplib, which sends LOGIN in ASCII.
    if not (value.isascii() and local and at and domain and "@" not in domain and "." in domain and " " not in value):
        raise ValueError("must be one mailbox address, like jim@plato.so")
    return value


class MailboxCreate(BaseModel):
    """The body of the console's ``POST /api/logins/mailboxes`` (expd ``MailboxCreate``).
    The password stays a ``SecretStr`` until the client sends it."""

    model_config = ConfigDict(extra="forbid")

    account: str = Field(min_length=1)
    email: str
    password: SecretStr

    @field_validator("account")
    @classmethod
    def _account_has_a_slug(cls, value: str) -> str:
        if not slugify(value):
            raise ValueError("needs at least one letter or digit")
        return value.strip().lower()

    @field_validator("email")
    @classmethod
    def _email_is_an_address(cls, value: str) -> str:
        return _check_address(value)

    @field_validator("password")
    @classmethod
    def _password_not_empty(cls, value: SecretStr) -> SecretStr:
        secret = value.get_secret_value()
        if not secret.strip():
            raise ValueError("is empty")
        if not secret.isascii():
            raise ValueError("has a non-ASCII character: an IMAP login cannot send it")
        return value

    def wire(self) -> dict[str, str]:
        """The JSON body. The only place that reveals the password."""
        return {"account": self.account, "email": self.email, "password": self.password.get_secret_value()}


class MailboxSetResult(BaseModel):
    """The console's answer to the write: ``{ok, item, written, cleared, created}``."""

    model_config = ConfigDict(extra="ignore")

    ok: bool
    item: str
    written: list[str] = Field(default_factory=list)
    cleared: list[str] = Field(default_factory=list)
    created: bool = False


class MailboxView(BaseModel):
    """One registered inbox. Address only: the console never lists a password."""

    account: str
    item: str
    address: str


class MailboxList(BaseModel):
    """The console's ``GET /api/logins/mailboxes`` answer: ``{mailboxes: {slug: address}}``."""

    model_config = ConfigDict(extra="ignore")

    mailboxes: dict[str, str] = Field(default_factory=dict)

    def views(self) -> list[MailboxView]:
        return [
            MailboxView(account=slug, item=f"{MAIL_PREFIX}{slug}", address=addr)
            for slug, addr in sorted(self.mailboxes.items())
        ]


class MailCheckResult(BaseModel):
    account: str
    address: str
    status: MailCheckStatus
    # The server's reply on a refusal, with the password removed. Never the password itself.
    detail: str | None = None


class MailSetReport(BaseModel):
    """What `mail set` prints: one write, or the plan of one with ``--dry-run``."""

    account: str
    item: str
    address: str
    outcome: WriteOutcome
    replaced_address: str | None = None
    check: MailCheckStatus | None = None
