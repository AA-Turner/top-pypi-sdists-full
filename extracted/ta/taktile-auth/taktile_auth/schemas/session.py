import typing as t

from pydantic import UUID4, BaseModel, root_validator


class SessionState(BaseModel):
    """Authenticated session state used by ``AuthClient``.

    Holds a credential (``api_key`` or ``jwt``) plus a PEP-295
    ``session_prefix`` used to thread session identity through nested
    service calls (``flow → agent → flow → …``).

    Inbound: the ``jwt`` field accepts either a bare token or the
    wire-format ``<prefix>+<token>``. A root validator splits the
    prefix off and populates ``session_prefix``.

    Hand the raw header value straight in:

        # Authorization header (after stripping ``Bearer ``)
        state = SessionState(jwt=raw_auth_header)
        # Or pre-split — also fine
        state = SessionState(api_key=uuid_obj, session_prefix="abc")

    Outbound: ``to_auth_headers()`` re-emits the wire format on
    ``Authorization`` when ``session_prefix`` is set.
    """

    api_key: t.Optional[UUID4]
    jwt: t.Optional[str]
    # PEP-295 session id stamped onto the auth header. Carried separately
    # from the credential so consumers can read it without re-parsing.
    session_prefix: t.Optional[str] = None

    @root_validator(pre=True)
    @classmethod
    def _peel_wire_format_prefix(cls, data: t.Any) -> t.Any:
        """Strip the PEP-295 wire-format prefix off a string-typed
        ``jwt`` input before field validation runs.

        ``root_validator(pre=True)`` rather than the pydantic-v2-only
        ``model_validator(mode="before")`` so this module stays
        importable for pydantic v1 consumers. Runs before field
        validation, so the cleaned value flows into pydantic's normal
        type coercion. Caller-supplied ``session_prefix`` is preserved
        if set; otherwise it's populated from the prefix embedded in
        the JWT.
        """
        if not isinstance(data, dict):
            return data
        session_prefix = data.get("session_prefix")
        raw_jwt = data.get("jwt")
        if isinstance(raw_jwt, str):
            parsed_prefix, inner = parse_session_prefix(raw_jwt)
            if parsed_prefix is not None:
                data["jwt"] = inner
            if not session_prefix:  # keep if explicitly specified
                session_prefix = parsed_prefix
        if session_prefix:
            data["session_prefix"] = session_prefix
        return data

    @property
    def prefixed_jwt(self) -> t.Optional[str]:
        """The JWT in PEP-295 wire format: ``<session_prefix>+<jwt>`` when a
        session prefix is set, the bare ``jwt`` otherwise, ``None`` when there
        is no JWT.
        """
        if not self.jwt:
            return None
        if not self.session_prefix:
            return self.jwt
        return f"{self.session_prefix}{SESSION_PREFIX_SEPARATOR}{self.jwt}"

    def to_auth_headers(self) -> t.Dict[str, str]:
        headers: t.Dict[str, str] = {}
        if self.api_key:
            headers["X-Api-Key"] = str(self.api_key)
        if self.prefixed_jwt:
            headers["Authorization"] = f"Bearer {self.prefixed_jwt}"
        return headers


# Separator between the PEP-295 session prefix and the underlying credential
# in the wire-format header. JWTs use base64url (no '+') and API keys are
# UUID4s, so '+' is collision-safe with both credential alphabets.
SESSION_PREFIX_SEPARATOR = "+"


def parse_session_prefix(
    value: str,
) -> t.Tuple[t.Optional[str], str]:
    """Split a wire-format credential into ``(session_prefix, credential)``.

    Returns ``(None, value)`` when no prefix is present. Splits on the
    first ``+`` only — the prefix is a UUID (no '+' in its alphabet)
    and JWTs use base64url (also no '+'), so the first '+' is
    unambiguously the separator.

    Public utility for direct callers (e.g. ``AuthClient.decode_id_token``
    accepts raw token strings that may or may not be wire-format
    prefixed). The common path (``SessionState`` construction) auto-peels
    via the model validator.
    """
    sep_idx = value.find(SESSION_PREFIX_SEPARATOR)
    if sep_idx <= 0:
        return None, value
    return value[:sep_idx], value[sep_idx + 1 :]  # noqa: E203
