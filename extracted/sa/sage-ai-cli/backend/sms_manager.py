"""
Firestore operations for the SAGE SMS/message bridge.

Schema
------
users/{uid}/sms_computers/{computer_id}
    computer_id   : str   (slugified hostname + short uuid)
    computer_name : str   (human-readable, used for @name: routing)
    bridge_email  : str   (the Gmail/iCloud inbox SAGE polls)
    last_seen     : str   (ISO datetime, updated every heartbeat)
    registered_at : str   (ISO datetime)

users/{uid}/sms_contacts/{contact_id}
    email         : str   (sender email SAGE will accept — iCloud, Gmail, etc.)
    label         : str   (e.g. "iPhone", "Android")
    added_at      : str   (ISO datetime)

Security model
--------------
- Contacts are fetched by the CLI at startup and cached in memory.
- Only emails in the contact list can trigger tasks on any of the user's computers.
- Computer registration is tied to the SAGE login — no anonymous registration.
"""

from __future__ import annotations

import uuid
import re
from datetime import datetime, timezone
from typing import Any

import logging

logger = logging.getLogger(__name__)


def _get_db():
    """Return a Firestore client pinned to the Firebase project (sage-ai-d1c22).

    Cloud Run's `GOOGLE_CLOUD_PROJECT` is the *deployment* project, which is
    NOT necessarily the same as the Firebase project. We must pass the explicit
    `projectId` so that no matter which module initializes firebase_admin first
    on a given instance, every Firestore client points at the right database.
    """
    try:
        import os
        import firebase_admin
        from firebase_admin import firestore as fs
        # Hard-coded fallback to "sage-ai-d1c22" — that's the Firebase project,
        # baked in to avoid a misconfigured deployment silently writing to a
        # different Firestore. GOOGLE_CLOUD_PROJECT is intentionally NOT in the
        # fallback chain — it points at love-in-da-house on this Cloud Run.
        project_id = (
            os.environ.get("FIREBASE_PROJECT_ID")
            or os.environ.get("VITE_FIREBASE_PROJECT_ID")
            or "sage-ai-d1c22"
        )
        if not firebase_admin._apps:
            firebase_admin.initialize_app(options={"projectId": project_id})
        return fs.client()
    except Exception as exc:
        logger.warning("Firestore unavailable: %s", exc)
        return None


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(name: str) -> str:
    """Normalize a name to a safe document ID segment."""
    return re.sub(r"[^a-z0-9\-]", "-", name.lower())[:40]


# ── Computers ──────────────────────────────────────────────────────────────────

def register_computer(uid: str, computer_name: str, bridge_email: str) -> dict:
    """
    Register or update a computer for a user.

    If a computer with the same name already exists for this user,
    update it in place (idempotent — safe to call on every `sage sms start`).
    Returns the computer document dict.
    """
    db = _get_db()
    if db is None:
        return _mock_computer(uid, computer_name, bridge_email)

    slug = _slug(computer_name)
    col = db.collection("users").document(uid).collection("sms_computers")

    # Check for existing record with same name
    existing = col.where("computer_name", "==", computer_name).limit(1).stream()
    for doc in existing:
        data = {**doc.to_dict(), "last_seen": _now(), "bridge_email": bridge_email}
        doc.reference.update({"last_seen": _now(), "bridge_email": bridge_email})
        return data

    # New registration
    computer_id = f"{slug}-{uuid.uuid4().hex[:8]}"
    data = {
        "computer_id":   computer_id,
        "computer_name": computer_name,
        "bridge_email":  bridge_email,
        "last_seen":     _now(),
        "registered_at": _now(),
    }
    col.document(computer_id).set(data)
    return data


def heartbeat_computer(uid: str, computer_name: str) -> None:
    """Update last_seen timestamp for a computer. Called every poll cycle."""
    db = _get_db()
    if db is None:
        return
    try:
        col = db.collection("users").document(uid).collection("sms_computers")
        for doc in col.where("computer_name", "==", computer_name).limit(1).stream():
            doc.reference.update({"last_seen": _now()})
    except Exception as exc:
        logger.debug("Heartbeat failed: %s", exc)


def list_computers(uid: str) -> list[dict]:
    db = _get_db()
    if db is None:
        return []
    try:
        return [
            doc.to_dict()
            for doc in db.collection("users").document(uid)
                          .collection("sms_computers").stream()
        ]
    except Exception as exc:
        logger.warning("list_computers failed: %s", exc)
        return []


def remove_computer(uid: str, computer_id: str) -> bool:
    db = _get_db()
    if db is None:
        return False
    try:
        db.collection("users").document(uid) \
          .collection("sms_computers").document(computer_id).delete()
        return True
    except Exception:
        return False


# ── Contacts ───────────────────────────────────────────────────────────────────

def _normalize_phone(value: str) -> str | None:
    """Return a 10-digit phone string if value looks like a phone number, else None."""
    digits = re.sub(r"\D", "", value)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return digits
    return None


def _phone_contact_key(phone: str) -> str:
    """Canonical storage key for a phone-number contact."""
    return f"phone:{phone}"


def _contact_doc_id(email: str) -> str:
    return email.lower().strip().replace("@", "_at_").replace(".", "_")


def add_contact(uid: str, email: str, label: str = "", provider: str = "", device_type: str = "") -> dict:
    """
    Add an authorized sender contact. Accepts either an email address or a
    plain phone number (e.g. "4085073140" or "+14085073140").

    `provider` (optional): a tag like "google.com" / "apple.com" that
    distinguishes contacts that share the same email address. When set, the
    document ID gets a provider prefix so Google + Apple with the same email
    show up as two separate rows in `sage sms contacts list`.

    Phone-number contacts match any inbound SMS gateway email whose local
    part equals that number (e.g. 4085073140@vtext.com, 4085073140@tmomail.net).

    Writes to two Firestore paths:
      users/{uid}/sms_contacts/{doc_id}   — user's contact list
      sms_contact_index/{doc_id}          — reverse lookup (O(1))
    """
    db = _get_db()
    raw = email.strip()

    # Detect phone number input and normalise
    phone = _normalize_phone(raw)
    if phone:
        stored_email = _phone_contact_key(phone)
        display      = f"+1{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        default_label = label or display
    else:
        stored_email  = raw.lower()
        display       = stored_email
        default_label = label or stored_email

    base_doc_id = _contact_doc_id(stored_email)
    # Per-provider doc_id keeps Google and Apple as separate rows even when
    # they share the same email. The bare doc_id remains a reverse-index
    # entry so any inbound message from that email still routes correctly.
    provider_short = provider.replace(".com", "") if provider else ""
    doc_id = f"{provider_short}_{base_doc_id}" if provider_short else base_doc_id

    data = {
        "email":    stored_email,
        "label":    default_label,
        "added_at": _now(),
        "display":  display,
    }
    if provider:
        data["provider"] = provider
    if device_type:
        data["device_type"] = device_type
    if db is None:
        return data
    try:
        db.collection("users").document(uid) \
          .collection("sms_contacts").document(doc_id).set(data, merge=True)
        # Reverse-index: always keep the bare-email entry too so inbound
        # email matching is O(1) regardless of which provider added the contact.
        db.collection("sms_contact_index").document(base_doc_id).set(
            {"uid": uid, "email": stored_email, "updated_at": _now()}, merge=True
        )
    except Exception as exc:
        logger.warning("add_contact failed: %s", exc)
    return data


def list_contacts(uid: str) -> list[dict]:
    db = _get_db()
    if db is None:
        return []
    try:
        return [
            doc.to_dict()
            for doc in db.collection("users").document(uid)
                          .collection("sms_contacts").stream()
        ]
    except Exception as exc:
        logger.warning("list_contacts failed: %s", exc)
        return []


def remove_contact(uid: str, email_or_doc: str) -> bool:
    """Remove a contact by phone number, email address, or raw doc_id.

    Accepts loosely-formatted input:
      • Phone:  "4085073140", "408-507-3140", "(408) 507-3140", "+14085073140"
      • Email:  "alice@example.com" (case-insensitive) — removes ALL provider
                variants (google_*, apple_*) plus the reverse-index entry.
      • Doc id: "phone:4085073140", "google_alice_at_example_com" — exact delete.

    Returns True when at least one document was deleted.
    """
    db = _get_db()
    if db is None:
        return False
    raw = email_or_doc.strip()
    if not raw:
        return False
    raw_lower = raw.lower()
    contacts_ref = db.collection("users").document(uid).collection("sms_contacts")

    # ── Path 1: looks like a phone number ─────────────────────────────────────
    phone = _normalize_phone(raw)
    if phone:
        target_doc_id = _phone_contact_key(phone)  # "phone:4085073140"
        try:
            snap = contacts_ref.document(target_doc_id).get()
            if snap.exists:
                snap.reference.delete()
                # Best-effort: clear any matching reverse-index entry
                try:
                    db.collection("sms_contact_index").document(target_doc_id).delete()
                except Exception:
                    pass
                return True
            # Fallback: scan stored "email" field == "phone:<digits>" — handles
            # legacy contacts whose doc_id may have been migrated
            for doc in contacts_ref.stream():
                data = doc.to_dict() or {}
                if data.get("email") == target_doc_id:
                    doc.reference.delete()
                    return True
            return False
        except Exception as exc:
            logger.warning("remove_contact (phone path) failed: %s", exc)
            return False

    # ── Path 2: caller passed a provider-prefixed doc_id directly ─────────────
    if ("_at_" in raw_lower) and ("_" in raw_lower) and ("@" not in raw_lower):
        try:
            doc_ref = contacts_ref.document(raw_lower)
            snap = doc_ref.get()
            if snap.exists:
                doc_ref.delete()
                return True
            return False
        except Exception as exc:
            logger.warning("remove_contact (doc_id path) failed: %s", exc)
            return False

    # ── Path 3: plain email — bulk-delete all provider variants ───────────────
    base_doc_id = _contact_doc_id(raw_lower)
    try:
        deleted_any = False
        for doc in contacts_ref.stream():
            if doc.id == base_doc_id or doc.id.endswith("_" + base_doc_id):
                doc.reference.delete()
                deleted_any = True
        try:
            db.collection("sms_contact_index").document(base_doc_id).delete()
        except Exception:
            pass
        return deleted_any
    except Exception as exc:
        logger.warning("remove_contact (email path) failed: %s", exc)
        return False


def get_contact_emails(uid: str) -> list[str]:
    """Return just the email strings for authorization checks."""
    return [c["email"] for c in list_contacts(uid) if c.get("email")]


def find_user_by_contact_email(email: str) -> str | None:
    """
    Look up which SAGE user registered this email / phone as a contact.

    Two-pass O(1) lookup:
      1. Direct match on the full email address (e.g. laynefaler@gmail.com)
      2. Phone-number match on the local part (e.g. 4085073140@vtext.com
         → checks index key phone:4085073140, works for any carrier gateway)
    """
    db = _get_db()
    if db is None:
        return None
    idx = db.collection("sms_contact_index")
    try:
        # Pass 1: exact email match
        doc = idx.document(_contact_doc_id(email)).get()
        if doc.exists:
            return doc.to_dict().get("uid")

        # Pass 2: phone-number gateway match
        local = email.split("@")[0] if "@" in email else email
        phone = _normalize_phone(local)
        if phone:
            phone_doc = idx.document(_contact_doc_id(_phone_contact_key(phone))).get()
            if phone_doc.exists:
                return phone_doc.to_dict().get("uid")
    except Exception as exc:
        logger.warning("find_user_by_contact_email failed: %s", exc)
    return None


# ── Helpers ────────────────────────────────────────────────────────────────────

def _mock_computer(uid: str, name: str, bridge_email: str) -> dict:
    """Fallback when Firestore is unavailable."""
    return {
        "computer_id":   f"local-{_slug(name)}",
        "computer_name": name,
        "bridge_email":  bridge_email,
        "last_seen":     _now(),
        "registered_at": _now(),
    }
