"""opaque cursors: pack and unpack, per search channel, per view offset, and the delivery stand-in."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
from typing import Any
from ....sdk import errors
from ....foundation.token_budget.token_budget import count_tokens
from ....shared.reads.search_contract import Channel
from ...delivery.delivery import encode as _encode_delivery_cursor
from ...delivery.context import current_delivery


def _pack_cursor(payload: dict) -> str:
    """Pack a cursor payload into an opaque token that is deliberately NOT JSON.

    A raw ``json.dumps({...})`` cursor cannot survive the MCP tool layer. FastMCP's
    `pre_parse_json` runs json.loads on every string argument and, when the result
    is not a scalar, REPLACES the argument with the parsed object — so a JSON-object
    cursor reaches the tool as a dict and is rejected against ``cursor: str | None``.
    Pagination then works perfectly in-process and 422s over the wire, which is
    exactly how it shipped: no test calls the tool layer, they all call the service
    directly.

    Base64 keeps the token a string through that pre-parse, and makes it genuinely
    opaque, so nobody hand-builds one and depends on the shape."""
    raw = json.dumps(payload, sort_keys=True).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _unpack_cursor(cursor: str, *, hint: str) -> dict:
    """Opaque token -> its payload, or a ValidationError naming how to get a real one.

    Raw-JSON cursors are still accepted: tokens minted before cursors were packed
    are already in agent transcripts, and refusing them would turn a stale cursor
    into an error instead of a page."""
    for decode in (
        lambda: json.loads(
            base64.urlsafe_b64decode((cursor + "=" * (-len(cursor) % 4)).encode()).decode()
        ),
        lambda: json.loads(cursor),  # legacy: pre-pack raw-JSON cursor
    ):
        try:
            parsed = decode()
        except (json.JSONDecodeError, ValueError, TypeError, binascii.Error, UnicodeDecodeError):
            continue
        if isinstance(parsed, dict):
            return parsed
    raise errors.ValidationError(
        f"malformed cursor: pass the next_cursor value from a previous {hint} call",
        status=422,
    )


def _split_cursor(cursor: str | None) -> tuple[str | None, str | None]:
    """The tool's opaque cursor carries the per-channel backend cursors."""
    if not cursor:
        return None, None
    parsed = _unpack_cursor(cursor, hint="research_search")
    return parsed.get(Channel.EXACT), parsed.get(Channel.SEMANTIC)


def _join_cursor(exact: str | None, semantic: str | None) -> str | None:
    cursors = {
        key: value
        for key, value in ((Channel.EXACT.value, exact), (Channel.SEMANTIC.value, semantic))
        if value
    }
    return _pack_cursor(cursors) if cursors else None

#: The state of a delivery cursor of representative size. A read that fits its
#: own rows to the budget must leave room for the continuation token delivery
#: puts in `next_cursor` -- a bound, compressed state roughly this long, not the
#: short native cursor the service writes there.
_DELIVERY_CURSOR_STAND_IN_STATE = {
    "native": "9999",
    # A page cursor carries the read's identity snapshot (a 64-hex hash,
    # which does not compress) -- see `_check_series_identity`.
    "source_snapshot": {
        "source": "series",
        "end": 0,
        "sha256": hashlib.sha256(b"series-identity-stand-in").hexdigest(),
    },
}


def _stand_in_request(fallback: str) -> Any:
    """What a stand-in cursor is encoded for: the request delivery will bind
    the real one to, when this read runs under delivery. A cursor also carries
    the call's optional arguments (`continuation.Request`), and a stand-in
    without them undercounts the real one by exactly those tokens -- the page
    then overflows and goes out as fragments. Outside delivery, `fallback`."""
    context = current_delivery()
    request = context.request if context is not None else None
    return fallback if request is None else request


#: Identity hashes a stand-in cursor is tried with. A delivery cursor is
#: base64 of compressed bytes that hold the read's identity hash, and how many
#: tokens base64 of RANDOM bytes takes varies with the bytes: one cursor shape,
#: 120 to 146 tokens over 60,000 hashes. A stand-in measured with one fixed
#: hash sat near the middle (130), so a real cursor outweighed it about half
#: the time, and a page that fit by fewer tokens than that went out as JSON
#: fragments (`test_a_series_page_is_sized_for_the_cursor_delivery_puts_on_it`,
#: red on main 4af98a780 and flaky before it). The heaviest of these, plus
#: `_CURSOR_TOKEN_SLACK`, held every one of those 60,000.
_STAND_IN_IDENTITIES = tuple(
    hashlib.sha256(f"series-identity-stand-in-{i}".encode()).hexdigest() for i in range(64)
)


def _delivery_cursor_stand_in() -> str:
    """The HEAVIEST stand-in cursor for this read's request (by tokens): a
    fit that reserves it, plus `_CURSOR_TOKEN_SLACK`, leaves room for the real
    cursor delivery puts on the page whatever its identity hash."""
    request = _stand_in_request(hashlib.sha256(b"delivery-cursor-stand-in").hexdigest()[:32])
    cursors = (
        _encode_delivery_cursor(
            {**_DELIVERY_CURSOR_STAND_IN_STATE,
             "source_snapshot": {**_DELIVERY_CURSOR_STAND_IN_STATE["source_snapshot"], "sha256": identity}},
            request,
        )
        for identity in _STAND_IN_IDENTITIES
    )
    return max(cursors, key=lambda cursor: (count_tokens(cursor), len(cursor)))


def _split_get_cursor(cursor: str | None, view: str) -> tuple[int, str | None]:
    """research_get's opaque cursor, carrying ``{"view": v, "offset": n}`` and,
    for a view that resumes on its route's own cursor, ``"after"``: the key of
    the last row sent (see `_ViewData.resume_key`).

    The view is carried so a cursor can never be silently re-based onto another
    view — offset 40 of a trajectory means nothing in an events list, and quietly
    reinterpreting it would skip 40 events with no signal at all."""
    if not cursor:
        return 0, None
    parsed = _unpack_cursor(cursor, hint="research_get")
    try:
        offset, cursor_view = parsed["offset"], parsed["view"]
        after = parsed.get("after")
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            raise ValueError
        if after is not None and not isinstance(after, str):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        raise errors.ValidationError(
            "malformed cursor: pass the next_cursor value from a previous research_get call",
            status=422,
        ) from None
    if cursor_view != view:
        raise errors.ValidationError(
            f"cursor was issued for view={cursor_view!r} but this call asked for "
            f"view={view!r}: pass a cursor back with the view that produced it",
            status=422,
        )
    return offset, after


def _join_get_cursor(view: str, offset: int, *, after: str | None = None) -> str:
    payload: dict[str, Any] = {"offset": offset, "view": str(view)}
    if after is not None:
        payload["after"] = after
    return _pack_cursor(payload)
