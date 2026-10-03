"""Bounded, stateless delivery of one requested MCP result.

The source owns collection ordering. This module owns delivery of a source page:
request -> authenticated read -> useful page or exact fragment -> final text cap.
Cursors carry positions and fingerprints, never source contents or credentials.
"""

from __future__ import annotations

import base64
import hashlib
import json
import zlib
from collections.abc import Callable

from .budget import Budget, serialize
from .contract import EntityType, EnvelopeState, MissingMarker
from .delivery_context import delivery_context

PREFIX = "prb2_"
_MAX_CURSOR = 4096
_MAX_STATE = 8192


class ContinuationError(ValueError):
    """A bounded, actionable error safe to expose to the caller."""


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def binding(tool: str, arguments: dict, scope: str) -> str:
    args = {k: v for k, v in arguments.items() if k not in {"cursor", "token_budget"}}
    return _digest(serialize([tool, args, scope]))[:32]


def encode(state: dict, request_id: str) -> str:
    packed = serialize({"b": request_id, "s": state}).encode()
    if len(packed) > _MAX_STATE:
        raise ContinuationError("Continuation request is too large; narrow the request.")
    value = PREFIX + base64.urlsafe_b64encode(zlib.compress(packed)).decode().rstrip("=")
    if len(value) > _MAX_CURSOR:
        raise ContinuationError("Continuation request is too large; narrow the request.")
    return value


def decode(cursor: str | None, request_id: str) -> dict:
    if not cursor or not isinstance(cursor, str) or not cursor.startswith(PREFIX):
        return {"native": cursor}
    if len(cursor) > _MAX_CURSOR:
        raise ContinuationError("Invalid continuation; restart the read.")
    try:
        raw = cursor[len(PREFIX) :]
        compressed = base64.b64decode(raw + "=" * (-len(raw) % 4), altchars=b"-_", validate=True)
        inflater = zlib.decompressobj()
        unpacked = inflater.decompress(compressed, _MAX_STATE + 1)
        if len(unpacked) > _MAX_STATE or not inflater.eof or inflater.unused_data:
            raise ValueError
        value = json.loads(unpacked)
        if value["b"] != request_id or not isinstance(value["s"], dict):
            raise ValueError
        state = value["s"]
        for key in ("offset", "length", "index"):
            if key in state and (type(state[key]) is not int or state[key] < 0):
                raise ValueError
        if state.get("native") is not None and not isinstance(state["native"], str):
            raise ValueError
        if state.get("after") is not None and not isinstance(state["after"], str):
            raise ValueError
        if "source_budget" in state:
            Budget(state["source_budget"])
        return state
    except (ValueError, KeyError, TypeError, zlib.error):
        raise ContinuationError(
            "Invalid continuation or changed request/scope; repeat the original read without cursor."
        ) from None


def _next(payload: dict) -> str | None:
    value = payload.get("next_cursor")
    return value if isinstance(value, str) and value else None


def omit_defaults(envelope: dict) -> dict:
    """Drop envelope keys that only restate the default answer.

    The reader is a model, and every key it sees is something to weigh. A
    `completeness` of complete-with-nothing-missing, a null `next_cursor` and an
    empty batch `missing` say "this is all of it" in ~30 tokens per envelope --
    per ROW in an `entity` batch -- ahead of the content that was asked for.
    ABSENCE IS THE CONTRACT (the server instructions say so): no `completeness`
    means complete, no `next_cursor` means nothing more to fetch, no `missing`
    means every ref resolved; an empty `evidence` says nothing either. Anything
    else -- partial, no_match, a marker, a cursor -- is kept exactly as built.

    Envelope level only, never inside `data`: a payload's own `completeness`
    (reproduce) or `next_cursor` is content, not bookkeeping.
    """
    out = dict(envelope)
    completeness = out.get("completeness")
    if (
        isinstance(completeness, dict)
        and set(completeness) <= {"state", "missing"}
        and completeness.get("state", EnvelopeState.COMPLETE) == EnvelopeState.COMPLETE
        and not completeness.get("missing")
    ):
        del out["completeness"]
    for key in ("next_cursor", "missing", "evidence"):
        if key in out and not out[key]:
            del out[key]
    return out


def batch_row(ref: str, envelope: dict) -> dict:
    """One `entity` batch row: the ref BESIDE its answer, not wrapped around it.

    A row used to be `{"ref", "data": <that ref's whole envelope>}`, so the
    answer sat at `rows[i].data.data` -- a box inside a box, and a reader had to
    guess which `data` held it. The envelope's keys now sit on the row. This is
    the RAW row, used as-is by a direct multi-ref call, which has no top-level
    cursor; what `_batch` sends is `_batch_row_on_the_wire`.
    """
    return {**envelope, "ref": ref}


def _batch_row_on_the_wire(ref: str, envelope: dict) -> dict:
    """A `_batch` row: `{ref, data}`, plus `completeness` when that row is partial
    and `next_cursor` when that entity has more -- except a row CUT FOR SIZE.

    Only a page's last row can hold a cursor (`_batch` returns right after it),
    and it is always the batch's top-level one. A row keeps that copy when it is
    the row's only sign of more: a view that ended at its fetch window reports
    `complete` plus a cursor, the complete block is omitted, and the top-level
    cursor alone also means "more refs to come". A row marked
    `truncated_by_token_budget` already says the cursor continues THIS row, so
    the copy only costs room: ~200 o200k tokens, which at `token_budget=512`
    left a two-ref notes read no room for a character of the note ("Request
    metadata exceeds this budget"). Verbose rows follow the same rule: the copy
    is delivery's duplicate, not bookkeeping the source built. Only `_batch`
    applies this -- it is the one place a top-level cursor is guaranteed.
    """
    row = batch_row(ref, envelope)
    missing = (row.get("completeness") or {}).get("missing") or []
    if MissingMarker.TRUNCATED_BY_TOKEN_BUDGET in missing:
        row.pop("next_cursor", None)
    return row


def _compact_unless_verbose(envelope: dict, args: dict) -> dict:
    """`verbose=True` is the debugging shape: it keeps every key the source built."""
    return envelope if args.get("verbose") else omit_defaults(envelope)


def _advance_state(state: dict, native: str) -> dict:
    advanced = {
        k: v
        for k, v in state.items()
        if k not in {"offset", "length", "hash", "format", "path", "after", "source_budget"}
    }
    advanced["native"] = native
    return advanced


def _read(call: Callable[[dict], dict], arguments: dict, state: dict) -> dict:
    with delivery_context(state.get("source_snapshot")) as delivery:
        payload = call(arguments)
    if delivery.snapshot is not None:
        state["source_snapshot"] = delivery.snapshot
    return payload


def _source_state(payload: dict) -> dict:
    source = payload.get("completeness")
    if not isinstance(source, dict):
        return {"state": "complete", "missing": []}
    # The old service flags an atomic payload as overflowing its approximate
    # row budget. Delivery now pages that payload exactly; it is not a source gap.
    missing = [m for m in source.get("missing", []) if m != "token_budget_exceeded"]
    if missing == source.get("missing", []):
        return source
    return {
        **source,
        "missing": missing,
        "state": "complete"
        if not missing and source.get("state") == "partial"
        else source.get("state", "complete"),
    }


def _stable_payload(payload: dict) -> dict:
    # Only transport bookkeeping is excluded. Scientific values and source
    # completeness remain part of the fingerprint.
    return {k: v for k, v in payload.items() if k not in {"as_of", "scope"}}


def _text_document(tool: str, args: dict, payload: dict) -> tuple[list, str] | None:
    """Locate a requested authored document, not an arbitrary long field."""
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        return None
    prefix = ["data"] if "data" in payload else []
    if tool != "entity":
        return None
    view = args.get("view", "card")
    # Sub-note excerpts carry authored caveats alongside the main document.
    # Reconstruct the full JSON page so completing a text fragment cannot hide them.
    if data.get("sub_notes"):
        return None
    if view == "summary":
        for key in ("project_summary", "experiment_summary"):
            doc = data.get(key)
            if isinstance(doc, dict) and isinstance(doc.get("document"), str):
                return prefix + [key, "document"], doc["document"]
    if view == "readme":
        doc = data.get("readme")
        if isinstance(doc, dict) and isinstance(doc.get("markdown"), str):
            return prefix + ["readme", "markdown"], doc["markdown"]
    if view == "notes":
        for key in ("project_notes", "experiment_notes", "run_notes", "group_notes", "notes"):
            doc = data.get(key)
            if isinstance(doc, str):
                return prefix + [key], doc
            if isinstance(doc, dict):
                for field in ("body", "text", "notes"):
                    if isinstance(doc.get(field), str):
                        return prefix + [key, field], doc[field]
    refs = args.get("refs") or []
    if (
        view != "record"
        and len(refs) == 1
        and (
            refs[0] == "team-note"
            # A sub-note's card IS its document, as the team note's is.
            or refs[0].startswith(
                ("team_note:", "team-note:", f"{EntityType.SUB_NOTE.value}:")
            )
        )
    ):
        entity = data.get("entity")
        if isinstance(entity, dict) and isinstance(entity.get("body"), str):
            return prefix + ["entity", "body"], entity["body"]
    return None


def page(
    payload: dict,
    tool: str,
    args: dict,
    state: dict,
    request_id: str,
    budget: Budget,
    *,
    finish: Callable[[dict], dict] | None = None,
) -> dict:
    """Fit a whole source page or emit exact, resumable fragments of it.

    `finish` wraps a page (for example, a batch item) BEFORE every size check.
    Cursor state includes the original native page cursor: advancing a fragment
    never accidentally advances the underlying collection too.
    """
    wrap = finish or (lambda value: value)
    next_native = state.get("after") if "after" in state else _next(payload)
    if next_native:
        next_cursor = encode(_advance_state(state, next_native), request_id)
    else:
        next_cursor = None
    whole = dict(payload)
    if "completeness" in whole:
        whole["completeness"] = _source_state(payload)
    if "next_cursor" in whole or next_cursor:
        whole["next_cursor"] = next_cursor
    # _source_state can turn the service's partial into complete (the atomic
    # overflow marker is not a gap here), so defaults are dropped AFTER it.
    whole = _compact_unless_verbose(whole, args)
    if "offset" not in state and budget.fits(wrap(whole)):
        return wrap(whole)

    stable = _stable_payload(payload)
    if "completeness" in stable:
        stable["completeness"] = _source_state(payload)
    # The rejoined JSON is the same answer the whole-fit path would have sent.
    stable = _compact_unless_verbose(stable, args)
    document = _text_document(tool, args, stable)
    path = None
    if document is not None:
        path, text = document
        length = state.get("length", len(text))
        if length > len(text):
            raise ContinuationError("source_changed: content was deleted; restart the read.")
        # A document view returns that document in text fragments. Hash only
        # the original prefix, not live identity/version bookkeeping. A full
        # raw result remains available through entity(view="record").
        content = text[:length]
    else:
        length = 0
        content = serialize(stable)
    fingerprint = _digest(content)
    if state.get("hash", fingerprint) != fingerprint:
        raise ContinuationError("source_changed: requested content changed; restart the read.")
    offset = state.get("offset", 0)
    if offset >= len(content) and (offset or content):
        raise ContinuationError("Invalid continuation position; restart the read.")

    context = None
    if offset == 0 and tool == "entity" and args.get("view") in {"notes", "summary", "readme"}:
        data = stable.get("data", {})
        context = {key: data[key] for key in ("entity_type", "entity", "view") if key in data}
        if args.get("view") == "summary" and isinstance(data.get("notes"), dict):
            context["notes"] = data["notes"]
        if args.get("view") == "readme" and isinstance(data.get("readme"), dict):
            # Which repo and commit the text is from: everything but the text.
            context["readme"] = {k: v for k, v in data["readme"].items() if k != "markdown"}
    elif offset == 0 and path == ["data", "entity", "body"]:
        # A sub-note's TITLE says what the caveat is about; a body fragment
        # without it is text with no subject. (The team note has no title.)
        data = stable.get("data", {})
        entity = data.get("entity")
        if data.get("entity_type") == EntityType.SUB_NOTE and isinstance(entity, dict):
            context = {
                "entity_type": data["entity_type"],
                "entity": {k: v for k, v in entity.items() if k != "body"},
            }

    def candidate(end: int) -> dict:
        more = end < len(content)
        fragment_state = {
            **state,
            "offset": end,
            "length": length,
            "hash": fingerprint,
            "after": next_native,
        }
        cursor = encode(fragment_state, request_id) if more else next_cursor
        result = {
            "data": {
                "format": "text_fragment" if path else "json_fragment",
                "offset": offset,
                "text": content[offset:end],
                "total_chars": len(content),
                "sha256": fingerprint,
                "complete": not more,
            },
            "completeness": (
                {
                    **_source_state(payload),
                    "state": "partial",
                    "missing": list(
                        dict.fromkeys(
                            [
                                *_source_state(payload).get("missing", []),
                                "truncated_by_token_budget",
                            ]
                        )
                    ),
                }
                if more
                else _source_state(payload)
            ),
            "next_cursor": cursor,
        }
        if path:
            result["data"]["path"] = path
        if context is not None:
            result["data"]["context"] = context
        return wrap(_compact_unless_verbose(result, args))

    # Optional first-page orientation must not strand the requested document.
    # Reserve its exact wrapped cost once before sizing the text. A giant
    # identity/caveat gets an explicit card door, never a silently partial copy.
    if context is not None and not budget.fits(candidate(offset + 1)):
        context = {"omitted": True, "read_more": 'view="card"'}

    # Token count is not monotonic in characters. Binary sizing only selects a
    # candidate; a final exact check is mandatory, and one character is a finite
    # progress fallback. There is no repeated growing-prefix quadratic scan.
    low, high = offset + 1, min(len(content), offset + budget.byte_limit)
    best = None
    while low <= high:
        end = (low + high) // 2
        result = candidate(end)
        if budget.fits(result):
            best, low = result, end + 1
        else:
            high = end - 1
    if best is None:
        best = candidate(offset + 1)
        if not budget.fits(best):
            raise ContinuationError(
                "Request metadata exceeds this budget; use a larger token_budget."
            )
    return best


def _sql_page(arguments: dict, call: Callable[[dict], dict]) -> dict:
    """ONE page for `query_sql`, never a cursor.

    Every other tool pages by calling its source again. For SQL that would
    RE-RUN the query, and any query over live data (a running run, `now()`)
    returns a different page two -- which this module then rejects as
    `source_changed`. So a result that does not fit is cut instead:

        fits the budget ──────────────────────────> returned as-is
        has rows ── keep the longest prefix that fits, truncated=True,
                    truncated_reason="byte_limit", row_count = rows kept
        discovery ── keep whole tables in order, name the rest in
                     `omitted_tables` so the agent can ask for them
    """
    budget = Budget(arguments.get("token_budget", 2000))
    payload = call(dict(arguments))
    if budget.fits(payload):
        return payload
    rows = payload.get("rows")
    if isinstance(rows, list):

        def cut(n: int) -> dict:
            return {
                **payload,
                "rows": rows[:n],
                "row_count": n,
                "truncated": True,
                "truncated_reason": "byte_limit",
            }

        lo, hi = 0, len(rows)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if budget.fits(cut(mid)):
                lo = mid
            else:
                hi = mid - 1
        if budget.fits(cut(lo)):
            return cut(lo)
    tables = payload.get("tables")
    if isinstance(tables, list):
        kept: list = []
        for i, table in enumerate(tables):
            trial = {
                **payload,
                "tables": [*kept, table],
                "omitted_tables": [t.get("name") for t in tables[i + 1 :]],
            }
            if not budget.fits(trial):
                break
            kept.append(table)
        omitted = [t.get("name") for t in tables[len(kept) :]]
        result = {**payload, "tables": kept, "omitted_tables": omitted}
        if kept and budget.fits(result):
            return result
    raise ContinuationError(
        "The SQL result does not fit token_budget even when cut; select fewer columns, "
        "aggregate, or raise token_budget."
    )


def invoke(tool: str, arguments: dict, call: Callable[[dict], dict], scope: str) -> dict:
    """Run an authenticated tool read and budget the complete emitted result."""
    if tool == "browse":
        from .browse_delivery import invoke as browse_invoke

        return browse_invoke(arguments, call, scope)
    if tool == "query_sql":
        return _sql_page(arguments, call)
    budget = Budget(arguments.get("token_budget", 2000))
    request_id = binding(tool, arguments, scope)
    state = decode(arguments.get("cursor"), request_id)
    native_args = dict(arguments)
    native_args["cursor"] = state.get("native")
    # A fragment resumes the same source page even if the caller changes the
    # delivery budget. Otherwise the service's row window changes under it.
    native_args["token_budget"] = state.get("source_budget", budget.token_limit)
    state["source_budget"] = native_args["token_budget"]
    if tool == "entity" and len(arguments.get("refs", [])) > 1:
        return _batch(arguments, native_args, call, state, request_id, budget)
    payload = _read(call, native_args, state)
    return page(payload, tool, arguments, state, request_id, budget)


def _batch(
    args: dict,
    native_args: dict,
    call: Callable[[dict], dict],
    state: dict,
    request_id: str,
    budget: Budget,
) -> dict:
    refs = args["refs"]
    index = state.get("index", 0)
    if index >= len(refs):
        raise ContinuationError("Invalid batch position; restart the read.")
    rows: list[dict] = []
    missing: list[dict] = []
    fitted: dict | None = None
    while index < len(refs):
        one = refs[index]
        one_args = {**native_args, "refs": [one]}
        result = _read(call, one_args, state)
        is_missing = isinstance(result.get("missing"), list) and not result.get("rows")
        item_state = {**state, "index": index}

        def wrap(item: dict) -> dict:
            item_cursor = item.get("next_cursor")
            if item_cursor:
                cursor = item_cursor
            elif index + 1 < len(refs):
                cursor = encode({"index": index + 1, "native": None}, request_id)
            else:
                cursor = None
            if is_missing and not isinstance(item.get("data"), dict):
                return _compact_unless_verbose(
                    {
                        "rows": rows,
                        "missing": missing + item.get("missing", []),
                        "next_cursor": cursor,
                    },
                    args,
                )
            return _compact_unless_verbose(
                {
                    "rows": rows + [_batch_row_on_the_wire(one, item)],
                    "missing": missing,
                    "next_cursor": cursor,
                },
                args,
            )

        # Do not hide a source page's own continuation inside a completed batch.
        whole = dict(result)
        if "completeness" in whole:
            whole["completeness"] = _source_state(result)
        if _next(result):
            whole["next_cursor"] = encode(_advance_state(item_state, _next(result)), request_id)
        combined = wrap(_compact_unless_verbose(whole, args))
        if budget.fits(combined) and "offset" not in item_state:
            rows, missing = combined["rows"], combined.get("missing", [])
            fitted = combined
            if _next(result):
                return combined
            index += 1
            state = {"native": None, "source_budget": budget.token_limit}
            native_args = {**native_args, "cursor": None, "token_budget": budget.token_limit}
            if index == len(refs):
                return combined
            continue
        if fitted is not None:
            # This ref does not fit beside the rows already taken. Send the page
            # the previous pass MEASURED: its cursor already starts this ref
            # afresh. Re-encoding `item_state` here carried this ref's source
            # snapshot and budget pin (~160 tokens vs ~40) into a page nobody had
            # measured, so a short note then a long one at 512 went out over
            # budget, was refused at the boundary, and retried into the same
            # page. Nothing of this ref was sent, so it owes no pinned snapshot.
            return fitted
        return page(result, "entity", one_args, item_state, request_id, budget, finish=wrap)
    raise AssertionError("batch must return or advance")
