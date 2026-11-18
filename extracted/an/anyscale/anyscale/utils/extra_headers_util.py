"""Custom HTTP headers for the Anyscale API clients.

Three sources merge per header name, ignoring letter case, and a later source
wins: the ANYSCALE_EXTRA_HEADERS env var (a JSON object), then the repeatable
root `anyscale --header 'Name: Value'` option, then `Anyscale(headers=...)`.

Only the generated clients bound to the Anyscale API host apply them
(authenticate.py, commands/login_commands.py, sdk/anyscale_client/sdk.py), and
a redirect to another host drops them. They are read when a client is built,
and the CLI and module-level SDK reuse one cached client per process. No
message here includes a header value, since one may be a credential.
"""

import functools
import json
import os
import re
from typing import Any, Dict, Iterable, List, Mapping, Optional

import click
from urllib3.util.retry import Retry

from anyscale.shared_anyscale_utils.headers import RequestHeaders


EXTRA_HEADERS_ENV_VAR = "ANYSCALE_EXTRA_HEADERS"
HEADER_OPTION = "--header"
REDACTED_HEADER_VALUE = "<redacted>"

# The client sets these itself. Default headers override per-call ones, so a
# custom Accept/Content-Type/traceparent would replace them (and rest.py picks
# the body encoding from Content-Type). Cookie carries cli_token, Host and the
# length headers frame the request, and the backend reads X-Anyscale-Client*.
RESERVED_HEADER_NAMES = frozenset(
    name.lower()
    for name in (
        "Accept",
        "Content-Length",
        "Content-Type",
        "Cookie",
        "Host",
        "Transfer-Encoding",
        RequestHeaders.CLIENT.value,
        RequestHeaders.CLIENT_VERSION.value,
        RequestHeaders.TRACEPARENT.value,
    )
)

# RFC 9110 token, and field-value characters limited to printable ASCII.
_TOKEN_RE = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]+")
_VALUE_RE = re.compile(r"[\t\x20-\x7e]*")


def _validate_header(name: Any, value: Any) -> None:
    """Raise ValueError when a header is not valid.

    The name must be an HTTP token that is not reserved. The value must not be
    blank. It must contain only printable ASCII characters and tabs.
    """
    # Echo the name only once it is a valid token: a misplaced secret can land
    # in either slot.
    if not isinstance(name, str) or not _TOKEN_RE.fullmatch(name):
        raise ValueError(
            "header names must be non-empty and use only letters, digits and !#$%&'*+-.^_`|~"
        )
    if name.lower() in RESERVED_HEADER_NAMES:
        raise ValueError(
            f"the {name} header is set by the Anyscale client and cannot be overridden"
        )
    if not isinstance(value, str) or not value.strip() or not _VALUE_RE.fullmatch(value):
        raise ValueError(f"the {name} header needs a non-blank, printable ASCII value")


def _merge_headers(target: Dict[str, str], headers: Mapping[str, str]) -> None:
    """Copy `headers` into `target`. Each name replaces the same name in any letter case."""
    for name, value in headers.items():
        for existing in [k for k in target if k.lower() == name.lower()]:
            del target[existing]
        target[name] = value


def parse_header_args(raw_values: Iterable[str]) -> Dict[str, str]:
    """Parse `Name: Value` strings, raising ValueError on an invalid one."""
    headers: Dict[str, str] = {}
    for raw in raw_values:
        name, sep, value = raw.partition(":")
        if not sep:
            raise ValueError("expected 'Name: Value'")
        name, value = name.strip(), value.strip()
        _validate_header(name, value)
        _merge_headers(headers, {name: value})
    return headers


# Mutated rather than rebound, so updating it needs no `global` (ruff PLW0603).
_cli_headers: Dict[str, str] = {}


def set_cli_headers(raw_values: Iterable[str]) -> None:
    """Replace this process's `--header` values, raising ValueError on an invalid one."""
    parsed = parse_header_args(raw_values)
    _cli_headers.clear()
    _cli_headers.update(parsed)


def redact_header_args(args: Iterable[str]) -> List[str]:
    """Return command-line `args` with each `--header` value replaced, for code that records them."""
    redacted: List[str] = []
    tokens = iter(args)
    for token in tokens:
        if token.startswith(HEADER_OPTION + "="):
            redacted.extend([HEADER_OPTION, REDACTED_HEADER_VALUE])
        elif token == HEADER_OPTION:
            # Click takes the next token as the value even if it starts with "-".
            next(tokens, None)
            redacted.extend([HEADER_OPTION, REDACTED_HEADER_VALUE])
        else:
            redacted.append(token)
    return redacted


def _load_env_headers() -> Dict[str, str]:
    """Return the headers in ANYSCALE_EXTRA_HEADERS. Raise ValueError for an invalid value."""
    raw = os.environ.get(EXTRA_HEADERS_ENV_VAR, "")
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except ValueError as e:
        # JSONDecodeError's message carries only a position, never the input.
        raise ValueError(f"expected a JSON object ({e})") from e
    if not isinstance(parsed, dict):
        raise ValueError("expected a JSON object mapping header names to string values")
    headers: Dict[str, str] = {}
    for name, value in parsed.items():
        _validate_header(name, value)
        _merge_headers(headers, {name: value})
    return headers


def get_extra_headers(overrides: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
    """Merge ANYSCALE_EXTRA_HEADERS, `--header` and `overrides`, later sources winning."""
    try:
        headers = _load_env_headers()
    except ValueError as e:
        raise click.ClickException(f"Invalid {EXTRA_HEADERS_ENV_VAR}: {e}.") from e
    _merge_headers(headers, _cli_headers)
    if overrides:
        try:
            for name, value in overrides.items():
                _validate_header(name, value)
        except ValueError as e:
            raise click.ClickException(f"Invalid headers: {e}.") from e
        _merge_headers(headers, overrides)
    return headers


def apply_extra_headers(api_client: Any, headers: Mapping[str, str]) -> None:
    """Send `headers` on every request from a generated ApiClient to its own host."""
    if not headers:
        return
    _merge_headers(api_client.default_headers, headers)

    base = api_client.configuration.retries
    if not isinstance(base, Retry):
        # urllib3 assigns DEFAULT after the class body, so the stubs omit it.
        base = Retry.DEFAULT  # type: ignore[attr-defined]
    remove_on_redirect = base.remove_headers_on_redirect | {name.lower() for name in headers}
    policy = base.new(remove_headers_on_redirect=remove_on_redirect)
    # urllib3 strips Cookie/Authorization on a cross-host redirect, and these
    # need the same. urllib3 1.26 (allowed by requirements.in, pinned by Bazel)
    # reads that list only from a per-request `retries`, never the pool's, and
    # generated rest.py passes none, so bind one here instead of editing it.
    pool_manager = api_client.rest_client.pool_manager
    pool_manager.request = functools.partial(pool_manager.request, retries=policy)
