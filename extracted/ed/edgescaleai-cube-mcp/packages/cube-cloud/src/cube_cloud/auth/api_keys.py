"""DynamoDB-backed API key storage and validation."""

from __future__ import annotations

import hashlib
import secrets
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError

from cube_cloud.config import settings


def _get_table():
    dynamodb = boto3.resource("dynamodb", region_name=settings.aws_region)
    return dynamodb.Table(settings.dynamodb_table)


def hash_key(raw_key: str) -> str:
    """SHA-256 hash of an API key for storage."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def hash_email(email: str) -> str:
    """SHA-256 hash of a normalized (lowercased, trimmed) email address.

    Non-reversible identity for tool-call analytics — lets distinct-user counts
    and controlled person lookups without storing cleartext email.
    """
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()


def derive_email_identity(user_email: str | None) -> tuple[str | None, str | None]:
    """Return (domain, email_hash) for a user email, or (None, None) if absent
    or malformed (no `@`, or nothing after it).

    Public (not `_`-prefixed) because `scripts/manage-keys.py` also calls it —
    keep this the single source of truth so browser-login and CLI-issued keys
    hash the same email identically.
    """
    if not user_email or "@" not in user_email:
        return None, None
    domain = user_email.strip().lower().rsplit("@", 1)[1]
    if not domain:
        return None, None
    return domain, hash_email(user_email)


_BROWSER_LOGIN_PREFIX = "Browser login: "


ACTOR_USER = "user"
ACTOR_BOT = "bot"
ACTOR_TEST = "test"


def _test_account_domains() -> frozenset[str]:
    return frozenset(
        d.strip().lower()
        for d in (settings.telemetry_test_account_domains or "").split(",")
        if d.strip()
    )


def is_test_account_email(email: str | None) -> bool:
    """True for a plus-addressed login on a configured home domain.

    `wyatt.tyree+demo@edgescaleai.com` is a test account; `wyatt.tyree@edgescaleai.com`
    is the person, and `someone+x@customer.com` is a customer — plus-addressing is
    only OUR convention, so the rule is scoped to `telemetry_test_account_domains`.
    The check is on the local part alone, so a `+` anywhere else in the string
    (there is nowhere valid for one) does not match by accident.
    """
    if not email or "@" not in email:
        return False
    local, _, domain = email.strip().lower().rpartition("@")
    return "+" in local and domain in _test_account_domains()


def classify_actor(item: dict[str, Any]) -> tuple[str, str | None]:
    """Return ``(actor_type, bot_name)`` for an API-key item.

    ``actor_type`` is ``"user"`` when the key belongs to a person — it has a
    stored ``user_domain`` (browser login, or a CLI key created with a known
    email) or a ``"Browser login: <email>"`` description (a pre-#231 browser key
    not yet backfilled). It is ``"test"`` when that browser-login address is a
    plus-addressed alias on a home domain (`is_test_account_email`): a test
    account is not a person, and distinct-user counts must not count it as one,
    while its rows stay recorded so a feature can still be validated with it.
    Otherwise it is ``"bot"`` — a service / long-running agent key — and
    ``bot_name`` is its ``description`` label (e.g. ``"disco long-running
    agent"``); ``bot_name`` is ``None`` for users and test accounts.

    Derived from data already on every key item, so the analytics event can
    carry actor type + bot name WITHOUT storing them per-key — which is also why
    the test rule needs no backfill: it reads the description on every request,
    so an existing test key classifies as ``test`` from the next call on. A CLI
    key created with `--user-email` stores only domain + hash and cannot be
    recognised as a test account; none are created that way today. Deliberately
    only the bot's label is surfaced — a user key's description holds its
    cleartext email, which must not reach the logs (identity there stays domain
    + hash), and the test rule reads it here without ever returning it.
    """
    description = item.get("description", "") or ""
    if item.get("user_domain") or description.startswith(_BROWSER_LOGIN_PREFIX):
        if is_test_account_email(email_from_description(description)):
            return ACTOR_TEST, None
        return ACTOR_USER, None
    return ACTOR_BOT, description or None


def email_from_description(description: str) -> str | None:
    """Return the cleartext address a browser-login key's description carries.

    The only place cube-cloud holds a user's cleartext email (`create_key` stores
    domain + hash, never the address). `classify_actor` deliberately never
    surfaces it into logs; this returns it for the narrow case of writing it into
    a destination the user asked us to write it into — today, the reporter field
    on a Jira feedback ticket (`tools/feedback.py`).

    Keep this the single reader of `_BROWSER_LOGIN_PREFIX` alongside
    `classify_actor`, so a change to the description format updates both.
    """
    if not description.startswith(_BROWSER_LOGIN_PREFIX):
        return None
    email = description[len(_BROWSER_LOGIN_PREFIX):].strip()
    return email or None


def generate_key() -> str:
    """Generate a new API key (prefix + random token)."""
    return f"cmcp_{secrets.token_urlsafe(32)}"


async def validate_key(raw_key: str) -> dict[str, Any] | None:
    """Validate an API key. Returns the item dict if valid, None otherwise.

    Item schema: {key_hash, profile, description, created_at, enabled,
    user_domain?, user_email_hash?} — the user_* fields are only present when
    the key was created with a known user email (e.g. browser login).
    """
    key_hash = hash_key(raw_key)
    table = _get_table()
    try:
        resp = table.get_item(Key={"key_hash": key_hash})
    except ClientError:
        return None

    item = resp.get("Item")
    if not item:
        return None

    if not item.get("enabled", True):
        return None

    if _is_expired(item):
        return None

    return item


def _is_expired(item: dict[str, Any]) -> bool:
    """True iff the key carries an ``expires_at`` that has passed.

    **Absent ``expires_at`` means never expires.** Every key issued before this
    field existed, and every CLI/bot key issued without one, must keep working —
    only the browser/console flow sets it (see :func:`create_key`).

    This check, not the DynamoDB TTL on the table, is the security boundary: TTL
    deletion is lazy (AWS documents up to 48h after expiry), so an expired row
    can still be readable long after its time. A malformed value is treated as
    expired — fail closed.
    """
    raw = item.get("expires_at")
    if raw is None:
        return False
    try:
        return int(raw) <= int(time.time())
    except (TypeError, ValueError):
        return True


def create_key(
    profile: str,
    description: str = "",
    user_email: str | None = None,
    ttl_seconds: int | None = None,
) -> tuple[str, str]:
    """Create a new API key. Returns (raw_key, key_hash).

    `user_email`, when known (e.g. browser login via Cognito), is never stored
    in cleartext — only its domain and a SHA-256 hash are, for tool-call
    analytics identity (see docs/tool-call-logging-spec.md).

    `ttl_seconds`, when given, stamps an `expires_at` epoch that
    :func:`validate_key` enforces (and the table's DynamoDB TTL later reaps).
    **Only the browser/console cookie flow passes it** — see
    docs/console-spec.md §4.7. The agent `session_id` flow deliberately does
    not: that key becomes the developer's long-lived CLI credential. Omitted
    means the key never expires, which is the historical behavior for every
    existing key.
    """
    from datetime import datetime, timezone

    raw_key = generate_key()
    key_hash_val = hash_key(raw_key)
    user_domain, user_email_hash = derive_email_identity(user_email)
    item: dict[str, Any] = {
        "key_hash": key_hash_val,
        "profile": profile,
        "description": description,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "enabled": True,
    }
    if user_domain is not None:
        item["user_domain"] = user_domain
        item["user_email_hash"] = user_email_hash
    if ttl_seconds is not None:
        item["expires_at"] = int(time.time()) + int(ttl_seconds)
    _get_table().put_item(Item=item)
    return raw_key, key_hash_val


def revoke_key(key_hash_val: str) -> bool:
    """Disable an API key. Returns False if no such key exists.

    The ``attribute_exists`` condition is a security control, not an
    optimization. DynamoDB ``UpdateItem`` is an **upsert**, and ``/auth/logout``
    is unauthenticated (it is in ``APIKeyMiddleware.EXEMPT_PATHS``) and calls this
    with whatever ``cmcp_session`` cookie the caller presents. Without the
    condition, anyone could write unbounded rows into the table that holds every
    live API key — unauthenticated, unrate-limited (the app-proxy limiter keys on
    ``request.state.session_key``, which is never set on an exempt path), and
    billable on a PAY_PER_REQUEST table.

    It also prevents a benign-but-permanent leak: once a browser key has been
    reaped by the DynamoDB TTL while its 12h cookie is still live in the browser,
    a sign-out would otherwise resurrect a tombstone row carrying no
    ``expires_at`` — which the TTL can then never reap.
    """
    table = _get_table()
    try:
        table.update_item(
            Key={"key_hash": key_hash_val},
            UpdateExpression="SET enabled = :v",
            ExpressionAttributeValues={":v": False},
            ConditionExpression="attribute_exists(key_hash)",
        )
        return True
    except ClientError:
        # Includes ConditionalCheckFailedException (no such key) — a no-op, not an
        # error worth surfacing: the caller either never had a key or it is gone.
        return False
