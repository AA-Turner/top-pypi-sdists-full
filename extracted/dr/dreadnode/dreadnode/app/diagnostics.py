"""Credential redaction shared by runtime diagnostics and bug reports."""

import re

_REDACTED = "[REDACTED]"
_SECRET_ASSIGNMENT_RE = re.compile(
    r"""(?ix)
    (?P<prefix>
        (?:
            ["']?\b
            (?:[a-z0-9]+[_-])*
            (?:authorization|proxy-authorization|x-api-key|api[_-]?key|
               access[_-]?token|refresh[_-]?token|id[_-]?token|password|
               passwd|client[_-]?secret|secret|[a-z0-9]+[_-](?:token|key))
            \b["']?\s*[=:]\s*
            |
            # Bare key/token labels also occur in prose. Require assignment or quoting.
            (?:["']\b(?:token|key)["']\s*[=:]\s*|
               \b(?:token|key)\s*(?:=\s*|:\s*(?=["'])))
        )
    )
    (?:
        (?P<double_quote>") (?:\\.|[^"\\\r\n])* "
        |
        (?P<single_quote>') (?:\\.|[^'\\\r\n])* '
        |
        (?:Bearer\s+)?[^\s,;}\]"']+
    )
    """
)
_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_KNOWN_TOKEN_RE = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{12,}|dn_[A-Za-z0-9_-]{12,}|"
    r"ghp_[A-Za-z0-9]{12,}|github_pat_[A-Za-z0-9_]{12,}|"
    r"xox[baprs]-[A-Za-z0-9-]{12,})\b"
)
# Match through the last @ in the authority, without consuming the path/query/fragment.
_URL_CREDENTIAL_RE = re.compile(r"""(?i)(\b[a-z][a-z0-9+.-]*://[^\s/:@'"<>]*:)([^\s/?#'"<>]+)(@)""")


def redact_sensitive_text(value: str) -> str:
    """Redact common credentials without dumping or inspecting environment state."""

    def redact_assignment(match: re.Match[str]) -> str:
        quote = match.group("double_quote") or match.group("single_quote") or ""
        return f"{match.group('prefix')}{quote}{_REDACTED}{quote}"

    value = _SECRET_ASSIGNMENT_RE.sub(redact_assignment, value)
    value = _BEARER_RE.sub(f"Bearer {_REDACTED}", value)
    value = _KNOWN_TOKEN_RE.sub(_REDACTED, value)
    return _URL_CREDENTIAL_RE.sub(
        lambda match: f"{match.group(1)}{_REDACTED}{match.group(3)}", value
    )
