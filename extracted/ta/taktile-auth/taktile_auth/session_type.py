from enum import Enum

SEPARATOR = ":"


class SessionType(str, Enum):
    AUTHORIZATION_CODE = "AC"
    API_KEY = "AK"
    NATIVE_APP = "NA"
    CLIENT_CREDENTIALS = "CC"
    MCP = "MCP"


def session_type_from_jti(jti: str | None) -> SessionType | None:
    """Parse the session type out of a jti (``<TYPE>:<uuid>:<nonce>``).

    Fail-safe: runs in the auth path of every request and never raises.
    Returns ``None`` for anything that is not a well-formed jti with a
    known session-type prefix.
    """
    if not isinstance(jti, str):
        return None
    parts = jti.split(SEPARATOR)
    if len(parts) != 3:
        return None
    try:
        return SessionType(parts[0])
    except ValueError:
        return None
