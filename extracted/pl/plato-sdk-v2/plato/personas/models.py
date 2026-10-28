"""Persona record models. Fixture card, bank and government id fields are placeholders only: never a real one.

The login console (expd) imports these models, so the API contract and the card and SSN check have one copy."""

from __future__ import annotations

import datetime
import re
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from plato.chronos.models import PersonaMismatch

# The fields the walker fills from a persona-values file (exploration_world steps_core.PERSONA_FIELDS).
WALKER_FIELDS = ("name", "first_name", "last_name", "email", "phone", "display_name")

FIXTURE_EMAIL_RE = re.compile(r"^[a-z]+\.[a-z]+[0-9]*@example\.(com|org|net)$")
FIXTURE_PHONE_RE = re.compile(r"^\+1-\d{3}-555-01\d{2}$")


# Cards: 15-19 digits (15 only for 34/37) that pass the Luhn check, so phone numbers (at most 15 digits under
# E.164) do not match. SSN: 3-2-4 groups.
_CARD_RE = re.compile(r"(?<!\d)\d(?:[ -]?\d){14,18}(?!\d)")
_SSN_RE = re.compile(r"(?<!\d)\d{3}[- ]\d{2}[- ]\d{4}(?!\d)")


def _luhn_ok(digits: str) -> bool:
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch) * (2 if i % 2 else 1)
        total += d - 9 if d > 9 else d
    return total % 10 == 0


def reject_secret_like(text: str | None) -> str | None:
    """Raise when the text holds a card number or SSN. The message never repeats the value."""
    if text is None:
        return text
    for match in _CARD_RE.finditer(text):
        digits = re.sub(r"\D", "", match.group())
        if (len(digits) > 15 or digits[:2] in ("34", "37")) and _luhn_ok(digits):
            raise ValueError("looks like a payment card number; use {PAYMENT_CARD}")
    if _SSN_RE.search(text):
        raise ValueError("looks like a government id; use {GOV_ID}")
    return text


# The record classes read console responses, so they ignore keys a newer console adds. The *Patch classes
# are the PUT body and stay extra="forbid", which keeps card, bank and ssn keys out of a write.
class PersonaView(StrEnum):
    live = "live"
    fixture = "fixture"


class SourcedValue(BaseModel):
    model_config = ConfigDict(extra="ignore")
    value: str | None = None
    source: str | None = None
    note: str | None = None

    @field_validator("value", "source", "note")
    @classmethod
    def _no_secrets(cls, v: str | None) -> str | None:
        return reject_secret_like(v)

    @model_validator(mode="after")
    def _null_needs_note(self):
        if self.value is None and not self.note:
            raise ValueError("a null live value needs a note")
        if self.value is not None and not self.source:
            raise ValueError("a filled live value needs its source")
        return self


class SourcedValuePatch(SourcedValue):
    model_config = ConfigDict(extra="forbid")


class LiveIdentity(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: SourcedValue | None = None
    display_name: SourcedValue | None = None
    first_name: SourcedValue | None = None
    last_name: SourcedValue | None = None
    email: SourcedValue | None = None
    phone: SourcedValue | None = None
    locale: SourcedValue | None = None
    timezone: SourcedValue | None = None
    job_title: SourcedValue | None = None
    company: SourcedValue | None = None
    avatar_asset: SourcedValue | None = None


class FixtureIdentity(BaseModel):
    model_config = ConfigDict(extra="ignore")
    dob: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    region: str | None = None
    postal_code: str | None = None
    country: str | None = None
    occupation: str | None = None
    bio: str | None = None
    payment_card: Literal["{PAYMENT_CARD}"] | None = None
    bank_account: Literal["{BANK_ACCOUNT}"] | None = None
    bank_routing: Literal["{BANK_ROUTING}"] | None = None
    gov_id: Literal["{GOV_ID}"] | None = None

    @field_validator("dob")
    @classmethod
    def _dob(cls, v: str | None) -> str | None:
        if v is not None:
            datetime.date.fromisoformat(v)
        return v

    @field_validator("address_line1", "address_line2", "city", "region", "postal_code", "country", "occupation", "bio")
    @classmethod
    def _no_secrets(cls, v: str | None) -> str | None:
        return reject_secret_like(v)


class LiveIdentityPatch(LiveIdentity):
    """PUT body view: each key that is set replaces that key; an explicit null removes it."""

    model_config = ConfigDict(extra="forbid")
    name: SourcedValuePatch | None = None
    display_name: SourcedValuePatch | None = None
    first_name: SourcedValuePatch | None = None
    last_name: SourcedValuePatch | None = None
    email: SourcedValuePatch | None = None
    phone: SourcedValuePatch | None = None
    locale: SourcedValuePatch | None = None
    timezone: SourcedValuePatch | None = None
    job_title: SourcedValuePatch | None = None
    company: SourcedValuePatch | None = None
    avatar_asset: SourcedValuePatch | None = None


class FixtureIdentityPatch(FixtureIdentity):
    """PUT body view: each key that is set replaces that key; an explicit null removes it."""

    model_config = ConfigDict(extra="forbid")


class PersonaUpdate(BaseModel):
    """PUT /api/logins/{login_key}/{account}/persona. Send with exclude_unset=True: an omitted key is kept."""

    model_config = ConfigDict(extra="forbid")
    person_key: str | None = Field(default=None, max_length=255)
    live: LiveIdentityPatch | None = None
    fixture: FixtureIdentityPatch | None = None

    @field_validator("person_key")
    @classmethod
    def _no_secrets(cls, v: str | None) -> str | None:
        return reject_secret_like(v)


class PersonaRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    login_key: str
    account: str
    person_key: str | None = None
    live: LiveIdentity = Field(default_factory=LiveIdentity)
    fixture: FixtureIdentity = Field(default_factory=FixtureIdentity)
    # Chronos: which sign-in facts (email, phone) of the account differ from its persona's. The link stands;
    # the mismatch is only flagged, and `plato vault persona check` lists it.
    mismatch: list[PersonaMismatch] = Field(default_factory=list)
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class CheckProblem(StrEnum):
    no_persona = "no_persona"
    no_name = "no_name"
    no_email = "no_email"
    # The account signs in with an email (its username) that is not its persona's.
    email_mismatch = "email_mismatch"
    # The account's phone is not its persona's (`--fix` only reports it: the number is the persona's).
    phone_mismatch = "phone_mismatch"


class PersonaFixAction(StrEnum):
    # Linked to the persona that has the account's sign-in email.
    relinked = "relinked"
    # No persona had that email: one was made from it (key <login_key>_<account>) and linked.
    created = "created"


class PersonaFixRow(BaseModel):
    login_key: str
    account: str
    action: PersonaFixAction
    persona: str
    # What Chronos still flags after the fix (a phone that differs: reported, not changed).
    mismatch: list[PersonaMismatch] = Field(default_factory=list)


class PersonaCheckRow(BaseModel):
    login_key: str
    account: str
    problem: CheckProblem


class PersonaCheckReport(BaseModel):
    ok: bool
    checked: int
    problems: list[PersonaCheckRow]
    # What `check --fix` changed; those accounts are not in `problems`.
    fixed: list[PersonaFixRow] = Field(default_factory=list)
    # True when the console could not list 1Password: accounts made by hand there may be missing from the check.
    incomplete: bool = False
    vault_error: str | None = None


class PersonaMode(StrEnum):
    live = "live"
    sim = "sim"


# slot -> field -> value (None: the bound card lacks the field)
SlotValues = dict[str, dict[str, str | None]]


class PersonaRound(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cards: dict[str, dict[str, str]] = Field(
        default_factory=dict, description="story id -> slot -> bound card id (for the record)"
    )
    values: dict[str, SlotValues] = Field(default_factory=dict, description="story id -> slot values")


class PersonaValues(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["persona-values"]
    mode: PersonaMode
    pack_sha256: str = ""
    rounds: dict[str, PersonaRound] = Field(min_length=1)

    def round_values(self, seed: str) -> dict[str, SlotValues]:
        if seed not in self.rounds:
            raise ValueError(f"persona file has no round {seed!r} (has {sorted(self.rounds)})")
        return self.rounds[seed].values


class SlotKind(StrEnum):
    acting = "acting"
    account = "account"
    fixture = "fixture"


class PersonaSlot(BaseModel):
    model_config = ConfigDict(extra="ignore")
    slot: str
    kind: SlotKind
    role: str = ""
    fields: list[str] = Field(default_factory=list)


class PersonaPack(BaseModel):
    model_config = ConfigDict(extra="ignore")
    # Required and non-empty: a pack without slots (a plain pack, a misspelled key) has nothing to bind.
    persona_slots: dict[str, list[PersonaSlot]] = Field(min_length=1)


class PersonaGap(BaseModel):
    story_id: str
    slot: str
    field: str


class BindResult(BaseModel):
    values: PersonaValues
    gaps: list[PersonaGap] = Field(default_factory=list)


class BindReport(BaseModel):
    """What `plato vault persona bind --json` prints."""

    out: str
    mode: PersonaMode
    rounds: list[str]
    stories: int
    gaps: list[PersonaGap]


class FixturePerson(BaseModel):
    model_config = ConfigDict(extra="forbid")
    card_id: str
    kind: Literal["fixture"]
    name: str
    first_name: str
    last_name: str
    display_name: str
    email: str
    phone: str

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        if not FIXTURE_EMAIL_RE.match(v):
            raise ValueError("fixture email must be first.last@example.(com|org|net)")
        return v

    @field_validator("phone")
    @classmethod
    def _phone(cls, v: str) -> str:
        if not FIXTURE_PHONE_RE.match(v):
            raise ValueError("fixture phone must be in the 555-01xx range")
        return v


class FixturePool(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["fixture-people"]
    version: int
    source: str
    people: list[FixturePerson] = Field(min_length=1)
