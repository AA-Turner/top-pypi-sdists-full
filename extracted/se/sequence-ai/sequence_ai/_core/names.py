"""A name or id the user gives, checked before it goes into a request's path.

Every name a command or call takes - a policy's (or its id), a benchmark's, an adapter's, a secret's, a robot's, a
template's, a key's id, an eval's id, an episode's id - becomes one segment of a URL path, and a value that is not a
name rewrites the request instead: httpx folds a `..` segment (a volume named `../deployments/x` sent
DELETE /v1/deployments/x), a `?` or `#` ends the path (`x?force=true` would delete `x` past its refusal), and the gateway
decodes `%2F` back into `/` before it routes, so a quoted `x/files` still reaches another route. The platform's names and
ids are letters, digits, '.', '_' and '-' (':' in a recording's `eval:<id>`),
starting with a letter or digit; anything else is refused here as the request's mistake (exit 2) and nothing is
sent. The gateway refuses the same on its side.
"""
from __future__ import annotations

import re
from urllib.parse import quote

from sequence_ai.errors import InvalidRequest

_SEGMENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
_UNSAFE = re.compile(r"[/\\%?#\x00-\x1f\x7f]")


def segment(value: object, what: str = "name") -> str:
    """`value` as one path segment, or InvalidRequest before any request is made."""
    if isinstance(value, str) and _SEGMENT.fullmatch(value):
        return value
    raise InvalidRequest(f"{value!r} is not a {what}: a {what} is letters, digits, '.', '_' or '-', starting with a "
                         "letter or digit")


def label(value: object, what: str = "robot") -> str:
    """A name the user writes freely (a robot's, 'arm 7'), quoted into one segment: refused only for what would leave
    or re-route the segment - '/', '\\', '%', '?', '#', a control character, or '.' / '..' alone."""
    if isinstance(value, str) and value not in ("", ".", "..") and not _UNSAFE.search(value):
        return quote(value, safe="")
    raise InvalidRequest(f"{value!r} is not a {what}'s name: it cannot hold '/', '\\', '%', '?' or '#'")


def file_path(value: object) -> str:
    """A file of a listing (`seq policy data export`): segments as above, joined by '/'."""
    if isinstance(value, str) and all(_SEGMENT.fullmatch(p) for p in value.split("/")):
        return value
    raise InvalidRequest(f"{value!r} is not a file of this listing")
