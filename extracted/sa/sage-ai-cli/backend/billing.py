"""SAGE billing — tier enforcement, usage tracking, PayPal subscription management."""

from __future__ import annotations

import os
import time
import logging
from datetime import datetime, timezone
from typing import Literal

import httpx

logger = logging.getLogger("ai-platform.billing")

# ── Admin bypass ─────────────────────────────────────────────────────────────

ADMIN_EMAILS: frozenset[str] = frozenset({"laynefaler@gmail.com"})

# ── Tier definitions ──────────────────────────────────────────────────────────

TierName = Literal["free", "starter", "pro", "premium", "admin"]

# Token-based billing. Limits are OUTPUT TOKENS per month (input is free).
# Overage rate is USD per 1,000 tokens above the monthly limit.
# 1 token ≈ 4 characters; average response ≈ 500–1,000 tokens.
TIERS: dict[str, dict] = {
    "free":    {"token_limit": 0,           "price_usd": 0,   "overage_per_1k": 0.000},
    "starter": {"token_limit": 300_000,     "price_usd": 19,  "overage_per_1k": 0.001},
    "pro":     {"token_limit": 2_000_000,   "price_usd": 49,  "overage_per_1k": 0.0008},
    "premium": {"token_limit": 10_000_000,  "price_usd": 99,  "overage_per_1k": 0.0005},
    "admin":   {"token_limit": -1,          "price_usd": 0,   "overage_per_1k": 0.000},
}

TIER_ALIASES = {"legacy_plan": "premium", "unlimited": "premium"}

def tokens_from_text(text: str) -> int:
    """Estimate output tokens from response text (1 token ≈ 4 chars)."""
    return max(1, len(text) // 4)

# ── PayPal env vars ───────────────────────────────────────────────────────────

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET    = os.environ.get("PAYPAL_SECRET", "")
PAYPAL_ENV       = os.environ.get("PAYPAL_ENV", "production")

PAYPAL_BASE = (
    "https://api-m.paypal.com"
    if PAYPAL_ENV == "production"
    else "https://api-m.sandbox.paypal.com"
)

PAYPAL_PLAN_IDS = {
    "starter":   os.environ.get("PAYPAL_STARTER_PLAN_ID", ""),
    "pro":       os.environ.get("PAYPAL_PRO_PLAN_ID", ""),
    "premium": os.environ.get("PAYPAL_PREMIUM_PLAN_ID", ""),
}

# ── Firestore client (lazy) ───────────────────────────────────────────────────

_db = None


def _get_db():
    global _db
    if _db is not None:
        return _db
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore as fs
        if not firebase_admin._apps:
            firebase_admin.initialize_app()
        _db = fs.client()
        logger.info("Firestore client initialised")
    except Exception as exc:
        logger.warning("Firestore unavailable (%s) — billing checks will use in-memory fallback", exc)
        _db = None
    return _db


# ── Usage key ─────────────────────────────────────────────────────────────────

def _month_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


# ── Core billing functions ─────────────────────────────────────────────────────

def get_user_record(uid: str) -> dict:
    """Return user billing record from Firestore, default free tier if missing."""
    db = _get_db()
    if db is None:
        return {"tier": "free", "subscription_status": None}
    try:
        doc = db.collection("users").document(uid).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as exc:
        logger.warning("Firestore read error for uid %s: %s", uid, exc)
    return {"tier": "free", "subscription_status": None}


def ensure_user_record(uid: str, email: str) -> None:
    """Create user record on first login if it doesn't exist."""
    db = _get_db()
    if db is None:
        return
    try:
        ref = db.collection("users").document(uid)
        doc = ref.get()
        if not doc.exists:
            tier = "admin" if email in ADMIN_EMAILS else "free"
            ref.set({
                "uid": uid,
                "email": email,
                "tier": tier,
                "paypal_subscription_id": None,
                "subscription_status": None,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
    except Exception as exc:
        logger.warning("Could not create user record for %s: %s", uid, exc)


def get_usage(uid: str) -> dict:
    """Return usage for the current billing month."""
    db = _get_db()
    zero = {"tokens_used": 0, "server_messages": 0, "cli_messages": 0, "browser_messages": 0}
    if db is None:
        return zero
    try:
        doc = db.collection("usage").document(uid).collection("months").document(_month_key()).get()
        if doc.exists:
            data = doc.to_dict()
            # Backfill tokens_used from message counts for legacy records
            if "tokens_used" not in data:
                msgs = data.get("server_messages", 0) + data.get("cli_messages", 0)
                data["tokens_used"] = msgs * 500  # assume 500 tokens/msg for old records
            return data
    except Exception as exc:
        logger.warning("Usage read error for uid %s: %s", uid, exc)
    return zero


def increment_usage(uid: str, message_type: Literal["server", "cli", "browser"],
                    tokens: int = 500) -> None:
    """Atomically increment token + message counters for the current month."""
    db = _get_db()
    if db is None:
        return
    try:
        from google.cloud.firestore_v1 import Increment
        ref = db.collection("usage").document(uid).collection("months").document(_month_key())
        ref.set({
            "tokens_used": Increment(tokens),
            f"{message_type}_messages": Increment(1),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }, merge=True)
    except Exception as exc:
        logger.warning("Usage increment error for uid %s: %s", uid, exc)


def check_access(uid: str, email: str,
                 message_type: Literal["server", "cli", "browser"]) -> tuple[bool, str]:
    """Returns (allowed, reason_or_tier).
    - Admin email: always allowed.
    - Browser messages: always allowed (must be logged in).
    - Server/CLI: requires paid tier and remaining token quota.
    """
    if email in ADMIN_EMAILS:
        return True, "admin"

    if message_type == "browser":
        return True, "free_browser"

    record = get_user_record(uid)
    raw_tier = record.get("tier", "free")
    tier = TIER_ALIASES.get(raw_tier, raw_tier)
    if tier not in TIERS:
        tier = "free"

    tier_info = TIERS[tier]
    token_limit = tier_info["token_limit"]

    if token_limit == 0:
        return False, (
            "UPGRADE_REQUIRED: Server models and CLI require a paid plan. "
            "Visit the Billing page to subscribe — Browser AI is always free."
        )

    if token_limit == -1:
        return True, tier  # admin unlimited

    usage = get_usage(uid)
    used_tokens = usage.get("tokens_used", 0)

    if used_tokens < token_limit:
        return True, tier

    # Over limit — all paid plans allow overage (billed at end of period)
    overage = tier_info.get("overage_per_1k", 0)
    if tier in ("starter", "pro", "premium") and overage > 0:
        return True, f"{tier}_overage"

    remaining_fmt = f"{(token_limit - used_tokens):,}" if used_tokens < token_limit else "0"
    return False, (
        f"LIMIT_REACHED: Monthly token limit of {token_limit:,} reached for {tier} plan "
        f"(used {used_tokens:,}). "
        f"Upgrade to Pro ($49/mo) or Premium ($99/mo) for more tokens."
    )


# ── PayPal helpers ─────────────────────────────────────────────────────────────

def _paypal_token() -> str:
    r = httpx.post(
        f"{PAYPAL_BASE}/v1/oauth2/token",
        auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET),
        data={"grant_type": "client_credentials"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def get_paypal_subscription(subscription_id: str) -> dict:
    token = _paypal_token()
    r = httpx.get(
        f"{PAYPAL_BASE}/v1/billing/subscriptions/{subscription_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def activate_subscription(uid: str, subscription_id: str) -> str:
    """Verify subscription with PayPal and update Firestore tier. Returns tier name."""
    db = _get_db()
    sub = get_paypal_subscription(subscription_id)
    plan_id = sub.get("plan_id", "")
    status = sub.get("status", "")

    tier = "free"
    for tier_name, pid in PAYPAL_PLAN_IDS.items():
        if pid and pid == plan_id:
            tier = tier_name
            break

    if status != "ACTIVE":
        raise ValueError(f"Subscription {subscription_id} status is {status}, not ACTIVE")

    if db:
        try:
            db.collection("users").document(uid).set({
                "tier": tier,
                "paypal_subscription_id": subscription_id,
                "subscription_status": "active",
                "subscription_activated": datetime.now(timezone.utc).isoformat(),
            }, merge=True)
        except Exception as exc:
            logger.warning("Firestore write error activating subscription: %s", exc)

    return tier


def cancel_subscription(uid: str) -> None:
    """Cancel the user's active PayPal subscription and downgrade to free."""
    db = _get_db()
    record = get_user_record(uid)
    sub_id = record.get("paypal_subscription_id")

    if sub_id:
        try:
            token = _paypal_token()
            httpx.post(
                f"{PAYPAL_BASE}/v1/billing/subscriptions/{sub_id}/cancel",
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                json={"reason": "User requested cancellation"},
                timeout=15,
            )
        except Exception as exc:
            logger.warning("PayPal cancel failed for %s: %s", sub_id, exc)

    if db:
        try:
            db.collection("users").document(uid).set({
                "tier": "free",
                "subscription_status": "cancelled",
                "subscription_cancelled": datetime.now(timezone.utc).isoformat(),
            }, merge=True)
        except Exception as exc:
            logger.warning("Firestore write error cancelling subscription: %s", exc)


def delete_account(uid: str) -> None:
    """Cancel subscription and delete all Firestore data for this user."""
    cancel_subscription(uid)
    db = _get_db()
    if db:
        try:
            # Delete monthly usage docs
            for doc in db.collection("usage").document(uid).collection("months").stream():
                doc.reference.delete()
            db.collection("usage").document(uid).delete()
            db.collection("users").document(uid).delete()
        except Exception as exc:
            logger.warning("Error deleting account data for %s: %s", uid, exc)


# ── PayPal webhook handler ─────────────────────────────────────────────────────

def handle_webhook(event_type: str, resource: dict) -> None:
    """Process a verified PayPal webhook event."""
    db = _get_db()
    if db is None:
        return

    sub_id = resource.get("id") or resource.get("subscription_id", "")
    if not sub_id:
        return

    # Find user by subscription ID
    try:
        users = db.collection("users").where("paypal_subscription_id", "==", sub_id).limit(1).stream()
        user_doc = next(users, None)
    except Exception:
        return

    if user_doc is None:
        return

    uid = user_doc.id

    if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
        try:
            sub = get_paypal_subscription(sub_id)
            plan_id = sub.get("plan_id", "")
            tier = next((t for t, pid in PAYPAL_PLAN_IDS.items() if pid == plan_id), "free")
            db.collection("users").document(uid).set(
                {"tier": tier, "subscription_status": "active"}, merge=True
            )
        except Exception as exc:
            logger.warning("Webhook activation error: %s", exc)

    elif event_type in ("BILLING.SUBSCRIPTION.CANCELLED", "BILLING.SUBSCRIPTION.EXPIRED"):
        try:
            db.collection("users").document(uid).set(
                {"tier": "free", "subscription_status": "cancelled"}, merge=True
            )
        except Exception as exc:
            logger.warning("Webhook cancel/expire error: %s", exc)

    elif event_type == "BILLING.SUBSCRIPTION.PAYMENT.FAILED":
        try:
            db.collection("users").document(uid).set(
                {"subscription_status": "payment_failed"}, merge=True
            )
        except Exception as exc:
            logger.warning("Webhook payment failed error: %s", exc)


# ── PayPal plan creation (run once at setup) ───────────────────────────────────

def _ensure_paypal_product(token: str) -> str:
    """Create or retrieve the SAGE AI product in PayPal Catalog."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    # Try creating the product; if it already exists, PayPal returns the existing one
    r = httpx.post(
        f"{PAYPAL_BASE}/v1/catalogs/products",
        headers=headers,
        json={
            "name": "SAGE AI",
            "description": "SAGE AI — local-first AI coding assistant",
            "type": "SERVICE",
            "category": "SOFTWARE",
        },
        timeout=30,
    )
    if r.status_code in (200, 201):
        product_id = r.json().get("id", "")
        logger.info("PayPal product created/exists: %s", product_id)
        return product_id
    # If conflict (already exists), list products and find it
    if r.status_code == 409:
        lr = httpx.get(f"{PAYPAL_BASE}/v1/catalogs/products?page_size=20", headers=headers, timeout=15)
        if lr.is_success:
            for p in lr.json().get("products", []):
                if p.get("name") == "SAGE AI":
                    return p["id"]
    raise RuntimeError(f"Could not create PayPal product: {r.text}")


def create_paypal_plans() -> dict[str, str]:
    """Create PayPal subscription plans for all paid tiers. Returns {tier: plan_id}."""
    token = _paypal_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    product_id = _ensure_paypal_product(token)
    logger.info("Using PayPal product ID: %s", product_id)

    plan_ids = {}
    for tier_name, price, label in [
        ("starter",           "19.00", "Starter — 300 msgs/mo + $0.10 overage"),
        ("pro",               "49.00", "Pro — 2,000 msgs/mo + $0.08 overage"),
        ("premium", "99.00", "Premium — 10,000 msgs/mo + $0.05 overage"),
    ]:
        payload = {
            "product_id": product_id,
            "name": f"SAGE AI {tier_name.replace('_', ' ').title()}",
            "description": label,
            "status": "ACTIVE",
            "billing_cycles": [{
                "frequency": {"interval_unit": "MONTH", "interval_count": 1},
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": 0,
                "pricing_scheme": {"fixed_price": {"value": price, "currency_code": "USD"}},
            }],
            "payment_preferences": {
                "auto_bill_outstanding": True,
                "setup_fee_failure_action": "CANCEL",
                "payment_failure_threshold": 1,
            },
        }
        r = httpx.post(f"{PAYPAL_BASE}/v1/billing/plans", headers=headers, json=payload, timeout=30)
        if r.status_code in (200, 201):
            plan_ids[tier_name] = r.json().get("id", "")
            logger.info("Created PayPal plan for %s: %s", tier_name, plan_ids[tier_name])
        else:
            logger.error("Failed to create PayPal plan for %s: %s", tier_name, r.text)
            print(f"Failed to create PayPal plan for {tier_name}: {r.text}")

    return plan_ids
