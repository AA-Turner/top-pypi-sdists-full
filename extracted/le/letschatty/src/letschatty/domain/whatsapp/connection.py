"""The WhatsApp connection state of a number, the signal that changes it and the connection log entry (api-chatty
`docs/whatsapp-connection-state.md` and `docs/whatsapp/conexion-reglas.md`, ADR-014).

Pure models and constants: they moved here unchanged from api-chatty `company/whatsapp_connection/model.py` (C1) so
the repositories of the state and of the log (C2) can read them; the rules that use them live in api-chatty
`application/whatsapp/connection/rules/`.
"""
from __future__ import annotations

from dataclasses import dataclass, field as dataclass_field
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any, Mapping, Optional

from pydantic import BaseModel, Field, field_validator
from zoneinfo import ZoneInfo


class ConnectionStatus(StrEnum):
    """What the company can do. The exact reason goes in `IssueCode`."""

    CONNECTED = "connected"
    AT_RISK = "at_risk"              # works, but Meta warned (spam, scheduled disable)
    RESTRICTED = "restricted"        # works partly until a date
    RECONNECTING = "reconnecting"    # Meta is reconnecting it on its own (phone change)
    DISCONNECTED = "disconnected"    # neither receives nor sends; fixed by reconnecting
    BLOCKED = "blocked"              # a Meta sanction; reconnecting does not fix it


# A milder signal never overrides a more serious one (a spam warning does not erase a «disabled»).
SEVERITY: dict[ConnectionStatus, int] = {
    ConnectionStatus.CONNECTED: 0,
    ConnectionStatus.AT_RISK: 1,
    ConnectionStatus.RESTRICTED: 2,
    ConnectionStatus.RECONNECTING: 3,
    ConnectionStatus.DISCONNECTED: 4,
    ConnectionStatus.BLOCKED: 5,
}

# The states in which the number neither receives nor sends: they turn off the «connected» of the lists. Restricted
# and at risk keep working; «reconnecting» is the phone change Meta solves on its own in minutes (if not, it becomes
# disconnected).
OFFLINE_STATUSES: frozenset[ConnectionStatus] = frozenset({ConnectionStatus.DISCONNECTED, ConnectionStatus.BLOCKED})


class IssueCode(StrEnum):
    """Our reason, stable. The texts for the person come from it (api-chatty `rules/copy.py`)."""

    # PARTNER_REMOVED + disconnection_info.reason
    PRIMARY_DEVICE_INACTIVE = "primary_device_inactive"
    COMPANION_DEVICE_INACTIVE = "companion_device_inactive"
    ACCOUNT_DISCONNECTED = "account_disconnected"     # PARTNER_REMOVED · ACCOUNT_DISCONNECTED (USER or SYSTEM)
    NUMBER_ON_CONSUMER_APP = "number_on_consumer_app"
    NUMBER_CHANGED = "number_changed"
    REREGISTERED_ON_NEW_DEVICE = "reregistered_on_new_device"
    ACCESS_REMOVED = "access_removed"               # PARTNER_REMOVED without a reason / PARTNER_APP_UNINSTALLED
    # Coexistence: phone change
    DEVICE_CHANGE_IN_PROGRESS = "device_change_in_progress"
    RECONNECT_TIMED_OUT = "reconnect_timed_out"
    # Sanctions and account
    ACCOUNT_DISABLED = "account_disabled"
    DISABLE_SCHEDULED = "disable_scheduled"
    ACCOUNT_RESTRICTED = "account_restricted"
    POLICY_VIOLATION = "policy_violation"
    ACCOUNT_DELETED = "account_deleted"
    NUMBER_REMOVED = "number_removed"
    ACCOUNT_UNDER_REVIEW = "account_under_review"
    ACCOUNT_REVIEW_REJECTED = "account_review_rejected"
    # Deduced from a failed send and confirmed with Meta (the safety net when the webhook was lost). Only a broken
    # connection; see api-chatty `rules/send_errors.py`.
    NUMBER_NOT_REGISTERED = "number_not_registered"
    PERMISSIONS_LOST = "permissions_lost"
    # 131037: Meta has not approved the number's display name yet, and until then EVERY outgoing send fails. It is not
    # a broken connection (reconnecting does not fix it): it is a block that lifts on its own.
    DISPLAY_NAME_NOT_APPROVED = "display_name_not_approved"


class SignalSource(StrEnum):
    WEBHOOK = "webhook"
    SEND_ERROR = "send_error"
    VERIFICATION = "verification"  # the `meta-status` probe: Meta rejected our token when reading the number
    TRAFFIC = "traffic"          # an inbound message or an accepted send: the connection works
    SIGNUP = "signup"            # the signup (Embedded Signup) finished well
    SWEEP = "sweep"              # the periodic sweep: expirations and escalations
    BACKFILL = "backfill"


_UTC = ZoneInfo("UTC")


def as_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Mongo returns dates without a time zone (see api-chatty docs/funnels-chat-funnel-integrity.md): every date that
    enters the model ends up in UTC, so comparisons never blow up."""
    if value is None or value.tzinfo is not None:
        return value
    return value.replace(tzinfo=_UTC)


# How long «at risk» lasts without new warnings, and how long to wait for Meta to reconnect on its own.
AT_RISK_TTL = timedelta(days=30)
RECONNECT_GRACE = timedelta(minutes=30)

# The TTL index of `whatsapp_connection_events` (api-chatty Database/indexes/whatsapp_connection_events_indexes.py)
# deletes each entry this many days after it happened; the Connection card shows it so it does not say «no warnings»
# when they were deleted for being old.
EVENTS_RETENTION_DAYS = 180


@dataclass(frozen=True)
class AccountSignal:
    """Something Meta (or a send) said about an account, already normalized.

    `event` is Meta's raw value (`PARTNER_REMOVED`, `DISABLED_UPDATE`, a send error code…) and `reason` the raw
    reason, if any. The interpretation lives in the policy, not here."""

    source: SignalSource
    occurred_at: datetime
    event: str
    field: Optional[str] = None
    reason: Optional[str] = None
    initiated_by: Optional[str] = None
    waba_id: Optional[str] = None
    phone_number_id: Optional[str] = None
    display_phone: Optional[str] = None
    details: Mapping[str, Any] = dataclass_field(default_factory=dict)
    raw: Optional[Mapping[str, Any]] = None
    idempotency_key: Optional[str] = None

    def meta_summary(self) -> dict[str, Any]:
        """What is stored and shown to look the case up in Meta."""
        summary: dict[str, Any] = {"event": self.event}
        for key in ("field", "reason", "initiated_by", "waba_id", "phone_number_id", "display_phone"):
            value = getattr(self, key)
            if value:
                summary[key] = value
        if self.details:
            summary["details"] = dict(self.details)
        return summary


class ConnectionIssue(BaseModel):
    code: IssueCode
    since: datetime
    until: Optional[datetime] = None
    source: SignalSource
    meta: dict[str, Any] = Field(default_factory=dict)

    @field_validator("since", "until", mode="after")
    @classmethod
    def _to_utc(cls, value: Optional[datetime]) -> Optional[datetime]:
        return as_utc(value)


def state_id_of(company_id: str, account_id: Optional[str] = None) -> str:
    """The `_id` of the state: the company for its default number (the usual document, which the lists and the
    Connection card read) and `company:account` for each additional number."""
    return company_id if account_id is None else f"{company_id}:{account_id}"


class ConnectionState(BaseModel):
    """One document per number in `whatsapp_connection_state`: `_id = company_id` for the company's default number
    and `company_id:account_id` for the others (see `state_id_of`)."""

    company_id: str
    #: None = the company's default number. Otherwise the account (an additional number).
    account_id: Optional[str] = None
    status: ConnectionStatus = ConnectionStatus.CONNECTED
    issue: Optional[ConnectionIssue] = None
    last_signal_at: Optional[datetime] = None
    banner_notification_id: Optional[str] = None
    updated_at: Optional[datetime] = None

    @field_validator("last_signal_at", "updated_at", mode="after")
    @classmethod
    def _to_utc(cls, value: Optional[datetime]) -> Optional[datetime]:
        return as_utc(value)

    @property
    def signature(self) -> str:
        """What defines «the state changed»: a warning goes out only when this changes."""
        code = self.issue.code.value if self.issue else ""
        until = self.issue.until.isoformat() if self.issue and self.issue.until else ""
        return f"{self.status.value}|{code}|{until}"

    @property
    def state_id(self) -> str:
        return state_id_of(self.company_id, self.account_id)

    @classmethod
    def connected(cls, company_id: str, account_id: Optional[str] = None) -> "ConnectionState":
        return cls(company_id=company_id, account_id=account_id)

    @classmethod
    def connected_for(cls, state_id: str) -> "ConnectionState":
        company_id, _, account_id = state_id.partition(":")
        return cls.connected(company_id, account_id or None)

    def effective(self, now: datetime) -> "ConnectionState":
        """The state as it has to be shown now: applies the expirations the sweep has not persisted yet. Never
        writes."""
        if self.issue is None:
            return self
        if self.status == ConnectionStatus.RESTRICTED and self.issue.until and self.issue.until <= now:
            return self.model_copy(update={"status": ConnectionStatus.CONNECTED, "issue": None})
        if self.status == ConnectionStatus.AT_RISK and self.issue.code == IssueCode.POLICY_VIOLATION and self.issue.since + AT_RISK_TTL <= now:
            return self.model_copy(update={"status": ConnectionStatus.CONNECTED, "issue": None})
        return self


class ConnectionEvent(BaseModel):
    """One entry of the connection log (`whatsapp_connection_events`, api-chatty `docs/refactor/conexion-de-whatsapp-diseno.md`
    §5.6). `id` is the idempotency key (the stored `_id`, which the Connection card shows as `id`), built by the rule
    `event_key_for`. `source` is free text: besides the `SignalSource` values, the signup marks write `signup_error`
    and `signup_finished`. The other fields are the ones `main` stores; one that was not given stays out of the
    stored document (the log adapter dumps with `exclude_unset`)."""

    # In the order `main` stores them (a document keeps the order its keys were given in).
    id: str
    company_id: str
    account_id: Optional[str] = None
    waba_id: Optional[str] = None
    occurred_at: datetime
    received_at: Optional[datetime] = None
    source: str
    field: Optional[str] = None
    event: Optional[str] = None
    reason: Optional[str] = None
    initiated_by: Optional[str] = None
    details: Optional[dict[str, Any]] = None
    raw: Optional[dict[str, Any]] = None
    status_before: Optional[str] = None
    status_after: Optional[str] = None
    issue_code: Optional[str] = None
    notified: Optional[bool] = None
    backfill: Optional[bool] = None


class ConnectionTarget:
    """Which number a signal is about, with the face of a company (Adapter).

    The module was born with one connection per company and reads `empresa.phone_number_id`, `display_phone_number`,
    `meta_token`… With several accounts, a signal is about ONE number: the default one (the company's fields, which
    mirror it) or an additional account. This object exposes those same attributes with the right number's data, so
    the policy, the banner, Slack and the card do not change. `id` is still the company: the banner and Slack belong
    to the company.
    """

    def __init__(self, empresa: Any, account: Any = None) -> None:
        self.empresa = empresa
        # The default account IS the company (its fields mirror it): one single state for it.
        self.account = None if account is None or getattr(account, "is_default", False) else account

    @property
    def id(self) -> Any:
        return self.empresa.id

    @property
    def account_id(self) -> Optional[str]:
        return str(self.account.account_id) if self.account is not None else None

    @property
    def state_id(self) -> str:
        return state_id_of(str(self.empresa.id), self.account_id)

    @property
    def name(self) -> str:
        if self.account is None:
            return self.empresa.name
        return f"{self.empresa.name} («{self.account.account_name}»)"

    @property
    def phone_number_id(self) -> Optional[str]:
        return self.account.phone_number_id if self.account is not None else self.empresa.phone_number_id

    @property
    def display_phone_number(self) -> Optional[str]:
        return self.account.display_phone_number if self.account is not None else self.empresa.display_phone_number

    @property
    def business_account_id(self) -> Optional[str]:
        return self.account.waba_id if self.account is not None else self.empresa.business_account_id

    @property
    def meta_token(self) -> Optional[str]:
        return self.account.token.get_secret_value() if self.account is not None else self.empresa.meta_token

    @property
    def messaging_settings(self) -> Any:
        return self.empresa.messaging_settings

    @property
    def deleted_at(self) -> Any:
        return getattr(self.empresa, "deleted_at", None)
