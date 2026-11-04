"""ClientMessage: what the server tells a client and its coding agent (a refusal or a staff notice),
one vocabulary for the server, the SDK/CLI, the tap, the hooks and the dashboard."""

from __future__ import annotations

from pydantic import BaseModel, Field

from ..compat import StrEnum
from ..records import Record

#: The longest sentence a message carries; a staff override is held to it too.
MAX_TEXT_LENGTH = 500


class Severity(StrEnum):
    """How hard the message stops the client: every refusal is `blocking`."""

    BLOCKING = "blocking"
    WARNING = "warning"
    INFO = "info"


class Action(StrEnum):
    """What the person should do next; each client words its own line for it."""

    UPDATE = "update"
    REINSTALL = "reinstall"
    CONTACT_SUPPORT = "contact_support"
    NONE = "none"


class Audience(StrEnum):
    """Who the sentence is written for."""

    PERSON = "person"
    AGENT = "agent"
    BOTH = "both"


class MessageCode(StrEnum):
    """The wire `code`s a client may key on. OPEN on the wire: an unknown code still shows its text."""

    CLIENT_TOO_OLD = "client_too_old"
    WORKSPACE_REQUIRED = "workspace_required"
    # A batch the server accepted (202) and refused once it applied it: listed on the run (I15d).
    DATA_REFUSED = "data_refused"
    # A tenant's queued data is over its share of the ingest queue: resend after Retry-After (I16).
    INGEST_BACKLOG = "ingest_backlog"
    # A staff notice's codes (non-blocking).
    UPDATE_RECOMMENDED = "update_recommended"
    MAINTENANCE = "maintenance"
    INCIDENT = "incident"
    ANNOUNCEMENT = "announcement"


class ClientMessage(Record):
    """One message from the server: a stable id, the code clients key on, and the sentence to show.

    `message_id` names the message (several share a `code`: every floor answers `client_too_old`);
    `text` is the server's current sentence, a staff override or the default.
    """

    message_id: str
    # A MessageCode value, typed `str` so a client parses a code it does not know yet.
    code: str
    severity: Severity
    action: Action
    audience: Audience
    text: str = Field(max_length=MAX_TEXT_LENGTH)
    # The release that has the replacement; None when no update lifts it.
    min_version: str | None = None
    # Bumped when a notice's content changes; always 0 for a refusal.
    revision: int = 0
    # Only on our own docs domain (the server refuses any other link).
    docs_url: str | None = None


class ClientRefusalBody(BaseModel):
    """The FLAT body of a refusal: `detail` stays the plain sentence, so a client older than the
    other keys still prints it. `min_version` and `docs_url` are absent when unset."""

    detail: str
    code: str
    min_version: str | None = None
    message_id: str
    action: Action
    severity: Severity
    docs_url: str | None = None


class ClientMessageList(BaseModel):
    """`GET /v1/client/messages`: the notices that apply to the caller now. `set_revision` is the
    `X-Probe-Notices` value for this set (None when it is empty); refetch when the header differs."""

    set_revision: str | None = None
    messages: list[ClientMessage]
