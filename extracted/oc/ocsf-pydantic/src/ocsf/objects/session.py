from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Session(BaseModel):
    """
    The Session object describes details about an authenticated session. e.g.
    Session Creation Time, Session Issuer
    Defined by D3FEND (https://d3fend.mitre.org/dao/artifact/d3f:Session/)
    """

    # Recommended:
    created_time: datetime | None = None # The time when the session was created.
    is_remote: bool | None = None
    issuer: str | None = None # The identifier of the session issuer.
    uid: str | None = None # The unique identifier of the session.

    # Optional:
    count: int | None = None # The number of identical sessions spawned from the same source IP,
                             # destination IP, application, and content/threat type seen over a period
                             # of time.
    credential_uid: str | None = None
    expiration_time: datetime | None = None # The session expiration time.
    expiration_reason: str | None = None # The reason which triggered the session expiration.
    is_mfa: bool | None = None
    is_vpn: bool | None = None
    terminal: str | None = None # The Pseudo Terminal associated with the session. Ex: the tty or pts
                                # value.
    uid_alt: str | None = None # The alternate unique identifier of the session. e.g. AWS ARN -
                               # `arn:aws:sts::123344444444:assumed-role/Admin/example-
                               # session`.
    uuid: UUID | None = None # The universally unique identifier of the session.
