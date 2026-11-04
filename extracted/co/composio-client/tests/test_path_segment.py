"""Path-parameter encoding, unit-level.

`tests/test_wire_parity.py` pins the encoding differentially against the
Stainless 1.43.0 oracle for the values the corpus happens to carry; this module
states the rules directly so a regression names itself.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from composio_client import Composio
from composio_client.resources._base import path_segment

from .conftest import BASE_URL

#: RFC 3986 §3.3 `pchar`, minus `%` (an escape introducer) — the exact set that
#: must survive unescaped inside a path segment.
_SUB_DELIMS = "!$&'()*+,;="
_UNRESERVED_PUNCTUATION = "-._~"


def test_empty_value_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-empty value for `session_id`"):
        path_segment("", "session_id")


@pytest.mark.parametrize("char", list(_SUB_DELIMS + ":@" + _UNRESERVED_PUNCTUATION))
def test_pchar_characters_are_left_unescaped(char: str) -> None:
    """Stainless Python keeps the sub-delims plus `:` and `@` safe; encoding
    them is legal but produces different bytes from the oracle."""
    assert path_segment(f"a{char}b", "session_id") == f"a{char}b"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("trs déjà+vu,x", "trs%20d%C3%A9j%C3%A0+vu,x"),
        ("a b/c", "a%20b%2Fc"),
        ("100%", "100%25"),
        ("a?b#c", "a%3Fb%23c"),
        ("a[b]c", "a%5Bb%5Dc"),
    ],
)
def test_encoding_matches_the_oracle(value: str, expected: str) -> None:
    assert path_segment(value, "session_id") == expected


def test_slash_is_never_safe() -> None:
    """The invariant that makes a per-parameter guard equivalent to a
    per-segment one: an encoded parameter cannot introduce a path boundary."""
    assert "/" not in path_segment("a/b/../c", "session_id")


# ---- dot-segment guard ----
#
# A path parameter of `..` would rewrite the request target: with no guard,
# `/api/v3.1/tool_router/session/../attach` resolves at the server to
# `/api/v3.1/tool_router/attach`. Both other implementations reject it — our
# TypeScript client (`src/compat/request.ts`) with `ComposioError`, Stainless
# Python (`_utils/_path.py`) with `ValueError`.

DOT_SEGMENTS = [".", "..", "%2e", "%2E", "%2e%2e", "%2E%2E", ".%2e", "%2e.", "%2E%2e"]


@pytest.mark.parametrize("value", DOT_SEGMENTS)
def test_dot_segments_are_rejected(value: str) -> None:
    with pytest.raises(ValueError, match="invalid segments") as excinfo:
        path_segment(value, "session_id")
    # the message names the offending argument
    assert "session_id" in str(excinfo.value)


@pytest.mark.parametrize(
    "value",
    [
        "v1.2.3",
        "a.b",
        ".hidden",
        "trailing.",
        "...",
        "..a",
        "a..",
        "%2ea",
        "sess_1",
        "....",
        "。",  # a non-ASCII lookalike must not be conflated with a dot
    ],
)
def test_values_that_merely_contain_dots_are_accepted(value: str) -> None:
    """Over-rejecting here would break legitimate identifiers; only a segment
    that *is* a dot-segment is refused."""
    assert path_segment(value, "session_id")


@respx.mock
@pytest.mark.parametrize("value", ["..", "."])
def test_session_path_param_dot_segment_never_dispatches(client: Composio, value: str) -> None:
    route = respx.route(host="api.test").mock(return_value=httpx.Response(200, json={}))
    with pytest.raises(ValueError, match="`session_id`"):
        client.tool_router.session.attach(value)
    assert route.call_count == 0


@respx.mock
@pytest.mark.parametrize("value", ["..", "."])
def test_mount_path_param_dot_segment_never_dispatches(client: Composio, value: str) -> None:
    """`files` interpolates two path parameters; both are guarded."""
    route = respx.route(host="api.test").mock(return_value=httpx.Response(200, json={}))
    with pytest.raises(ValueError, match="`mount_id`"):
        client.tool_router.session.files.list("sess_1", value)
    with pytest.raises(ValueError, match="`session_id`"):
        client.tool_router.session.files.list(value, "mount_1")
    assert route.call_count == 0


@respx.mock
def test_a_dot_free_path_still_dispatches(client: Composio) -> None:
    """The guard must not be load-bearing for ordinary ids — the negative tests
    above would pass vacuously if nothing ever reached the transport."""
    route = respx.get(f"{BASE_URL}/api/v3.1/tool_router/session/v1.2.3/tools").mock(
        return_value=httpx.Response(
            200, json={"items": [], "total_pages": 1, "current_page": 1, "total_items": 0}
        )
    )
    client.tool_router.session.tools("v1.2.3")
    assert route.call_count == 1
