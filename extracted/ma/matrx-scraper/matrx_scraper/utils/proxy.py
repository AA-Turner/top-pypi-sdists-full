"""Translate the configured proxy URL into Playwright's proxy contract."""
import re
from urllib.parse import unquote, urlsplit

# Query parameters whose VALUE is a credential. Matched by exact name,
# case-insensitively; the name stays in the output so a reader sees what was cut.
SECRET_QUERY_PARAMS = (
    "access_token",
    "api_key",
    "apikey",
    "auth",
    "authorization",
    "client_secret",
    "id_token",
    "key",
    "passwd",
    "password",
    "pwd",
    "refresh_token",
    "secret",
    "session_token",
    "sig",
    "signature",
    "token",
    "x-amz-credential",
    "x-amz-security-token",
    "x-amz-signature",
    "x-goog-credential",
    "x-goog-signature",
)

REDACTED = "***"

# `user:password@` right after a URL's `//` — greedy to the LAST `@` before the
# path, so a raw `@` inside a password cannot leave its tail behind.
_URL_USERINFO = re.compile(r"(?<=//)[^/\s?#'\"]*@")
_SECRET_QUERY_VALUE = re.compile(
    r"(?i)([?&;](?:" + "|".join(re.escape(name) for name in SECRET_QUERY_PARAMS) + r")=)[^&#\s'\"]*"
)


def redact_url_secrets(value: object) -> str:
    """The ONE redaction for URLs headed to OUTPUT — logs, vcprint, exception text.

    Strips every URL's ``user:password@`` and every ``SECRET_QUERY_PARAMS``
    value from ``str(value)``, keeping scheme, host, port, path, and every other
    parameter, and marking each cut with ``***``. Accepts any object (a URL, an
    exception whose message echoes one) because both reach the same log line.

    Output only: never route a URL used for identity, dedupe, cache keys, or a
    fetch through this — redaction is lossy by design.
    """
    text = str(value)
    text = _URL_USERINFO.sub(f"{REDACTED}@", text)
    return _SECRET_QUERY_VALUE.sub(rf"\1{REDACTED}", text)


def playwright_proxy(proxy: str) -> dict[str, str]:
    # Playwright strips URL userinfo from server without transferring it to
    # username/password. Preserve authentication explicitly at this boundary.
    parsed = urlsplit(proxy if "://" in proxy else f"http://{proxy}")
    options = {"server": f"{parsed.scheme}://{parsed.netloc.rsplit('@', 1)[-1]}"}
    if parsed.username is not None:
        options["username"] = unquote(parsed.username)
    if parsed.password is not None:
        options["password"] = unquote(parsed.password)
    return options
