"""Which 1Password mail item a login reads its mail codes from, and its To filter.

The login email (the account's ``login_email``, else its username when that is an
address) picks the item, in this order (:func:`resolve_mail_route`):

1. The mailbox of that exact address (``tom@bobwitmiester.com`` -> ``mail-tom``), or the
   account's own ``mail-{account}`` item when it holds that address.
2. A plus alias's base mailbox (``jim+x@plato.so`` -> ``mail-jim``).
3. The shared inbox of the address's domain (``collab-3@bobwitmiester.com`` -> ``mail-tom``).

No match is no route: an own item that holds another address is never read.

Steps 2 and 3 read a mailbox that gets the mail of many addresses, so they set
``to_contains`` to the login email. The code reader on the agent VM (``get_otp.py``)
has no SDK and keeps its own reader of ``to_contains``.
"""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator

_SLUG_RE = re.compile(r"[^a-z0-9]+")

# A plain address local part. The reader puts ``to_contains`` into the IMAP SEARCH
# command without quotes, so a space or a quote must never get there.
_PLAIN_LOCAL = re.compile(r"[a-z0-9._%+-]+")


def _slug(value: str | None) -> str:
    """Match the login world's ``slugify``: ``Jim Collab`` -> ``jim_collab``."""
    if not value:
        return ""
    return _SLUG_RE.sub("_", value.strip().lower()).strip("_")


class SharedInbox(BaseModel):
    """The mailbox of all addresses at a domain; ``item`` is used only when it holds ``address``."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    item: str
    address: str

    @field_validator("item")
    @classmethod
    def _mail_item(cls, item: str) -> str:
        # The fallback sends the item's password to the IMAP server: never a site
        # login item.
        if not item.strip().startswith("mail-"):
            raise ValueError(f"shared inbox item {item!r} is not a mail-* item")
        return item

    @field_validator("address")
    @classmethod
    def _full_address(cls, address: str) -> str:
        local, at, domain = address.strip().partition("@")
        if not (local and at and domain):
            raise ValueError(f"shared inbox address {address!r} is not an address")
        return address


# Google Workspace aliases: the mail of each alias goes to the base mailbox.
# Code only (no config overrides it): a new persona domain is a new entry.
DEFAULT_SHARED_INBOXES: dict[str, SharedInbox] = {
    "bobwitmiester.com": SharedInbox(item="mail-tom", address="tom@bobwitmiester.com"),
}


def mail_item_name(account: str | None) -> str:
    """The per-account mail item: ``Jim Collab`` -> ``mail-jim_collab``."""
    return f"mail-{_slug(account)}"


def _address(value: str | None) -> str | None:
    """``value`` trimmed and case-folded when it is one plain address, else None."""
    address = (value or "").strip().casefold()
    local, at, domain = address.partition("@")
    if not (local and at and "." in domain.strip(".")) or "@" in domain or any(c.isspace() for c in address):
        return None
    return address


def login_email_of(login_email: str | None, username: str | None) -> str | None:
    """``login_email``, else ``username`` when that is an address, else None."""
    return _address(login_email) or _address(username)


def exact_mail_item_name(address: str | None) -> str | None:
    """``tom@bobwitmiester.com`` -> ``mail-tom``; None when not an address."""
    plain = _address(address)
    return mail_item_name(plain.partition("@")[0]) if plain else None


def base_mail_item_name(username: str | None) -> str | None:
    """``jim+canva-free-1@plato.so`` -> ``mail-jim``; None when not a plus alias."""
    local, _, domain = (username or "").strip().casefold().partition("@")
    base, plus, _ = local.partition("+")
    return mail_item_name(base) if base and plus and domain else None


def own_inbox_recipient(username: str | None, imap_user: str | None) -> str | None:
    """``username`` when it is the inbox's own address or a plus alias of it, else None.
    That mailbox holds the mail of every alias: unfiltered, a reader takes ANY alias's newest code."""
    if not username or not imap_user:
        return None
    user, inbox = username.strip().casefold(), imap_user.strip().casefold()
    u_local, _, u_domain = user.partition("@")
    i_local, _, i_domain = inbox.partition("@")
    if not u_domain or not i_local or u_domain != i_domain:
        return None
    if u_local == i_local or u_local.startswith(f"{i_local}+"):
        return user
    return None


def shared_inbox_for(username: str | None, inboxes: Mapping[str, SharedInbox]) -> SharedInbox | None:
    """The entry for the domain of ``username`` (keys match without case); None when
    ``username`` is not a plain address or the entry's address is at another domain."""
    local, _, domain = (username or "").strip().casefold().partition("@")
    if not domain or not _PLAIN_LOCAL.fullmatch(local):
        return None
    for key, box in inboxes.items():
        if str(key).strip().casefold() == domain:
            box_domain = box.address.strip().casefold().partition("@")[2]
            return box if box_domain == domain else None
    return None


def shared_inbox_recipient(
    username: str | None,
    imap_user: str | None,
    inboxes: Mapping[str, SharedInbox] | None = None,
) -> str | None:
    """``username`` when it is at a shared-inbox domain and ``imap_user`` is that inbox, else None.
    This also covers an own item that holds the base address (``mail-tomdesmond``)."""
    shared = shared_inbox_for(username, DEFAULT_SHARED_INBOXES if inboxes is None else inboxes)
    inbox = (imap_user or "").strip().casefold()
    if not shared or inbox != shared.address.strip().casefold():
        return None
    return (username or "").strip().casefold()


class MailRoute(BaseModel):
    """The mail item an account reads its codes from; ``to_contains`` is set for a fallback inbox."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    item: str
    imap_user: str
    imap_password: str = Field(repr=False)
    to_contains: str | None = None


MailFieldReader = Callable[[str, str], Awaitable[str | None]]
"""An async ``read(item, field) -> value``. It returns None for a missing item or
field, and must not raise for one."""


async def resolve_mail_route(
    read: MailFieldReader,
    account: str | None,
    login_email: str | None,
    inboxes: Mapping[str, SharedInbox] | None = None,
) -> MailRoute | None:
    """The mail item of ``account`` that signs in as ``login_email``, in the module docstring's order.

    A fallback item must hold the base address of its mailbox. ``read`` gets each field
    once, and a password only after its username passed.
    """
    fields: dict[tuple[str, str], str | None] = {}

    async def read_once(item: str, field: str) -> str | None:
        # Steps share items (the own item can be step 1's and step 2's base).
        if (item, field) not in fields:
            fields[item, field] = await read(item, field)
        return fields[item, field]

    own_item = mail_item_name(account)
    address = _address(login_email)

    exact_items = (exact_mail_item_name(address), own_item) if address else ()
    for item in dict.fromkeys(name for name in exact_items if name):
        user = await read_once(item, "username")
        password = await read_once(item, "password") if (user or "").strip().casefold() == address else None
        if user and password:
            return MailRoute(item=item, imap_user=user, imap_password=password)

    base_item = base_mail_item_name(address)
    if base_item:
        base_user = await read_once(base_item, "username")
        to = own_inbox_recipient(address, base_user)
        base_password = await read_once(base_item, "password") if to else None
        if to and base_user and base_password:
            return MailRoute(item=base_item, imap_user=base_user, imap_password=base_password, to_contains=to)

    shared = shared_inbox_for(address, DEFAULT_SHARED_INBOXES if inboxes is None else inboxes)
    if shared:
        shared_user = await read_once(shared.item, "username")
        holds_base = (shared_user or "").strip().casefold() == shared.address.strip().casefold()
        shared_password = await read_once(shared.item, "password") if holds_base else None
        if shared_user and shared_password and address:
            return MailRoute(
                item=shared.item, imap_user=shared_user, imap_password=shared_password, to_contains=address
            )
    return None
