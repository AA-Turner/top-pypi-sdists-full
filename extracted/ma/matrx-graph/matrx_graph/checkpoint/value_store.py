"""The run's value store (``workflow.checkpoint_value``) for EVENTS — write, read, resolve (MKT-167).

Checkpoints already keep every value over their knob ONCE per run, sha256-addressed
(MKT-111, ``checkpoint/values.py``). Events now do the same: a ``node_started``
``inputs`` block, a ``node_completed`` ``output`` child, a ``run_completed``
``last_outputs`` entry over the ``workflow.event_payload.inline_value_max_bytes``
knob is stored here and the event carries ``{REF_KEY: <sha256>}``.

ONE store, ONE read path: :func:`load_run_values` is what the host's
``GET /runs/{id}/values`` serves to every screen that opens a value, and what any
server reader (a failed-step assist, a summary) calls through
:func:`resolve_run_values`. Old events carry no references and resolve to themselves.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_graph.checkpoint.values import (
    REF_KEY,
    RunOutputValueMissingError,
    event_payload_row,
    referenced_hashes,
    resolve_values,
)
from matrx_graph.db._registry import get_model

logger = logging.getLogger(__name__)

#: Most hashes one read resolves (a screen asks for a handful at a time).
MAX_HASHES_PER_READ = 200


async def store_run_values(
    run_id: str,
    values: dict[str, Any],
    *,
    organization_id: str | None = None,
    remember: bool = True,
) -> set[str]:
    """Persist ``values`` (hash → value) for ``run_id``; already-stored hashes are skipped.

    Returns the hashes this call wrote. ``remember=False`` is for a caller writing INSIDE a
    transaction: a hash is remembered as stored only once it is COMMITTED, so the caller
    calls :func:`remember_stored_values` after its commit. Remembered before the commit, a
    concurrent sibling with the same value writes only a reference — to a value that a
    rollback never stores (and its row becomes visible before the value does)."""
    if not values:
        return set()
    from matrx_graph.checkpoint.postgres import (
        _organization_for_run,
        _payload_bytes,
        _stored_value_hashes,
    )

    stored = _stored_value_hashes.get(run_id, set())
    fresh = {h: v for h, v in values.items() if h not in stored}
    if not fresh:
        return set()
    org = organization_id or await _organization_for_run(run_id)
    await get_model("WfCheckpointValue").bulk_insert_ignore(
        [
            {
                "run_id": run_id,
                "organization_id": org,
                "value_hash": digest,
                # A str is stored as a jsonb STRING by the ORM field (never parsed as JSON).
                "value": value,
                "size_bytes": _payload_bytes(value),
            }
            for digest, value in fresh.items()
        ],
        on_conflict=["run_id", "value_hash"],
    )
    if remember:
        remember_stored_values(run_id, fresh)
    return set(fresh)


def remember_stored_values(run_id: str, hashes: Any) -> None:
    """Remember ``hashes`` as COMMITTED to ``run_id``'s store (later writes skip them)."""
    from matrx_graph.checkpoint.postgres import _STORED_HASH_RUNS, _stored_value_hashes

    _stored_value_hashes.setdefault(run_id, set()).update(hashes)
    if len(_stored_value_hashes) > _STORED_HASH_RUNS:
        _stored_value_hashes.pop(next(iter(_stored_value_hashes)))


async def intern_event_payload(run_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """``payload`` with its large data values by reference, the values already stored.

    Stored BEFORE the event is returned, so no reader can ever see a reference whose
    value is not there yet. Never raises: if the store is absent or the write fails,
    the event goes out whole (loud) — a lost value is worse than a big event.
    """
    from matrx_graph.checkpoint.postgres import _value_store_available
    from matrx_graph.knobs import event_inline_value_max_bytes

    if not isinstance(payload, dict) or not _value_store_available():
        return payload
    try:
        limit = await event_inline_value_max_bytes()
        out, values = event_payload_row(payload, limit)
        if values:
            await store_run_values(run_id, values)
        return out
    except Exception:  # noqa: BLE001 — the event must still land
        logger.exception(
            "[wf:%s] event value store write FAILED (event=%s) — event stored INLINE",
            run_id[:8],
            payload.get("event"),
        )
        return payload


async def fetch_stored_values(run_id: str, hashes: set[str] | list[str]) -> dict[str, Any]:
    """hash → stored value (NOT following nested references) from ``run_id``'s OWN store.

    A run reads only its own store — never a run it called (a called workflow's answer is COPIED into the
    caller's store at the hand-off, :func:`carry_run_values`), so deleting a child run never takes a value
    its caller still references."""
    wanted = set(hashes)
    if not wanted:
        return {}
    out: dict[str, Any] = {}
    ordered = sorted(wanted)
    for i in range(0, len(ordered), MAX_HASHES_PER_READ):
        found = await get_model("WfCheckpointValue").filter(
            run_id=run_id, value_hash__in=ordered[i : i + MAX_HASHES_PER_READ]
        ).values("value_hash", "value")
        for item in found:
            # The jsonb codec already decoded it: a stored long STRING comes back as a str and
            # must never be json.loads-ed (it is the value, not its JSON text).
            out[str(item["value_hash"])] = item["value"]
    return out


async def load_run_values(run_id: str, hashes: list[str] | set[str]) -> dict[str, Any]:
    """hash → FULLY resolved value for ``run_id`` (nested references followed).

    A hash this run never stored is simply absent from the result.
    """
    wanted = sorted(set(hashes))[:MAX_HASHES_PER_READ]
    if not wanted:
        return {}
    store: dict[str, Any] = {}
    pending = set(wanted)
    while pending:
        found = await fetch_stored_values(run_id, pending)
        if not found:
            break
        fresh: set[str] = set()
        for digest, value in found.items():
            store[digest] = value
            fresh |= referenced_hashes(value)
        pending = fresh - set(store)
    out: dict[str, Any] = {}
    for digest in wanted:
        if digest in store:
            out[digest] = resolve_values(store[digest], store)
    return out


#: The key that marks a value a step HELD ON THE SERVER (MKT-167 part 2). Distinct from
#: ``REF_KEY`` on purpose: a held value is never resolved by a checkpoint load or for a
#: screen — only for the step that reads it (:func:`resolve_step_inputs`) and for an admin
#: in debug mode (``GET /runs/{id}/values``).
HELD_KEY = "__matrx_held_value__"


def held_hash(value: Any) -> str | None:
    """The reference a held-value marker names (opaque; older runs carry a value hash), else None."""
    if isinstance(value, dict) and len(value) == 1 and isinstance(value.get(HELD_KEY), str):
        return value[HELD_KEY]
    return None


def _store_available() -> bool:
    from matrx_graph.checkpoint.postgres import _value_store_available

    return _value_store_available()


def new_held_ref() -> str:
    """An opaque reference for one held value: 32 random bytes as hex — the same shape as a value hash, so every
    reader and the store's key column take it unchanged, but derived from NOTHING (review 46 leak class). A held
    value is a provision snapshot, often small; an unsalted sha256 of it in an event let anyone holding the event
    confirm a guessed snapshot. The reference resolves only server-side (:func:`resolve_step_inputs`, and
    ``GET /runs/{id}/values`` for an admin in debug mode)."""
    import secrets

    return secrets.token_hex(32)


async def hold_on_server(run_id: str, value: Any, *, organization_id: str | None = None) -> Any:
    """Store ``value`` once in the run's value store and return ``{HELD_KEY: <opaque ref>}``.

    For a step whose output is server-side state (a provision snapshot): the marker is what
    travels through channels, checkpoints and events; the scheduler resolves it for every
    downstream executor (:func:`resolve_step_inputs`), so the next step gets exactly the value.
    The marker is a random reference (:func:`new_held_ref`), never a digest of the value.
    Without a value store (a DB-less install) the value itself is returned — it travels inline.
    """
    if value is None or not _store_available():
        return value
    from matrx_graph.checkpoint.values import _force_ref

    values: dict[str, Any] = {}
    digest = _force_ref(value, values)[REF_KEY]
    ref = new_held_ref()
    values[ref] = values.pop(digest)  # the held value is keyed by its opaque reference only
    await store_run_values(run_id, values, organization_id=organization_id)
    return {HELD_KEY: ref}


async def resolve_step_inputs(run_id: str, held: dict[str, Any]) -> dict[str, Any]:
    """Each held argument (``name → {HELD_KEY: hash}``) as its full value — what the executor receives."""
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    hashes = {h for h in (held_hash(v) for v in held.values()) if h}
    store = await load_run_values(run_id, hashes)
    out: dict[str, Any] = {}
    for name, marker in held.items():
        digest = held_hash(marker)
        if digest not in store:
            raise MissingCheckpointValueError(f"held value {str(digest)[:12]}… for {name!r} is not stored for this run")
        out[name] = store[digest]
    return out


def _strip_held(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _strip_held(v) for k, v in value.items() if held_hash(v) is None}
    if isinstance(value, list):
        return [_strip_held(v) for v in value if held_hash(v) is None]
    return value


#: Keys of a step's output that only a debug view shows, at any depth outside a kind instance: request and search
#: ledgers, a raw page. (Arman, 2026-10-15: provisions, raw pages and ledgers stay on the server.)
DEBUG_ONLY_KEYS: frozenset[str] = frozenset({"requests", "searches", "html", "provision_values", "results_by_engine"})


def _raw_rank(hit: Any) -> float:
    rank = hit.get("rank") if isinstance(hit, dict) else None
    return float(rank) if isinstance(rank, (int, float)) else float("inf")


def screen_value(value: Any, cut: list[dict[str, Any]] | None = None, path: list[str | int] | None = None) -> Any:
    """``value`` as a viewer who is NOT an admin in debug mode receives it (pure).

    An agent transcript (``messages``) is an empty list at any depth (the envelope stays recognizable, its content
    never ships). A kind instance is otherwise rendered content and passes untouched. Elsewhere: the
    ``DEBUG_ONLY_KEYS`` are absent and an engine's ``raw_results`` keep only the best-ranked one — the one result the
    screen draws. Creativity Warehouse, 2026-10-16: one Identify run's debug-off events were 609 KB, 121 KB of it
    every engine object of every hit; ``GET /runs/{id}`` sent the whole 2.4 MB output.

    ``cut`` collects a ``WithheldValue`` description of everything left out (a debug-only field, a transcript, the
    engine rows past the first), ``path`` prefixing each — so a screen says what it is not showing (2026-10-29)."""
    return _screen(value, in_kind=False, path=path or [], cut=cut)


#: The fields of an engine's search row (``raw_results[].result``) the web-result renderer draws, and for the nested
#: objects the keys it reads (matrx-frontend ``features/search-review/webResult.ts`` ``toWebResultValue``). Everything
#: else an engine sends (cluster, deep links, FAQ, language, a thumbnail's original...) stays on the server.
SEARCH_ROW_FIELDS: dict[str, frozenset[str] | None] = {
    **dict.fromkeys((
        "__kind", "title", "url", "link", "description", "snippet", "extra_snippets", "age", "page_age", "date",
        "published_at", "age_text", "type", "site_name", "source", "displayed_url", "displayed_link", "favicon",
    )),
    "profile": frozenset({"name", "img"}),
    "meta_url": frozenset({"favicon"}),
    "thumbnail": frozenset({"src"}),
}


#: An agent's answer fields that repeat its ``content`` (prose is ``final_text`` re-detected, a bound answer IS
#: ``structured_output``; ``final_message`` wraps ``final_text``). When ``content`` is a non-empty list the screen
#: draws ``content`` (matrx-frontend agent-result.ts: content wins on screen), so these never ship twice.
#: ``final_text`` stays as ``""`` so every reader still recognizes the agent-run envelope.
ANSWER_REPEAT_KEYS: tuple[str, ...] = ("final_text", "final_message", "structured_output")


def _search_field(value: Any, keys: frozenset[str] | None) -> Any:
    if keys is None or not isinstance(value, dict):
        return value
    return {k: v for k, v in value.items() if k in keys}


def _search_row(hit: Any) -> Any:
    if isinstance(hit, dict) and isinstance(hit.get("result"), dict):
        result = {k: _search_field(v, SEARCH_ROW_FIELDS[k]) for k, v in hit["result"].items() if k in SEARCH_ROW_FIELDS}
        return {**hit, "result": result}
    return hit


def _note_cut(cut: list[dict[str, Any]] | None, value: Any, path: list[str | int]) -> None:
    if cut is None:
        return
    ref = value.get(REF_KEY) if isinstance(value, dict) and len(value) == 1 else None
    # A by-reference value is never read just to measure it: its size stays unknown, its ref still loads it.
    cut.append(describe_withheld(_DROP, path, ref) if isinstance(ref, str) else describe_withheld(value, path, None))


def _screen(value: Any, *, in_kind: bool, path: list[str | int], cut: list[dict[str, Any]] | None) -> Any:
    if isinstance(value, list):
        return [_screen(v, in_kind=in_kind, path=[*path, i], cut=cut) for i, v in enumerate(value)]
    if not isinstance(value, dict):
        return value
    in_kind = in_kind or "__kind" in value
    answered = isinstance(value.get("content"), list) and bool(value["content"])
    out: dict[str, Any] = {}
    for k, v in value.items():
        here = [*path, k]
        if k == "messages" and isinstance(v, list):
            # The transcript: never rendered, even by the agent_result kind (matrx-frontend agent-run-output.ts).
            if v:
                _note_cut(cut, v, here)
            out[k] = []
        elif answered and k in ANSWER_REPEAT_KEYS:
            # The answer is sent once, in ``content`` (agent_result kinds included) — a repeat, not a loss.
            if k == "final_text":
                out[k] = ""
        elif in_kind:
            out[k] = _screen(v, in_kind=True, path=here, cut=cut)
        elif k in DEBUG_ONLY_KEYS:
            _note_cut(cut, v, here)
            continue
        elif k == "raw_results" and isinstance(v, list) and v:
            best = min(v, key=_raw_rank)
            if len(v) > 1:
                # The rows past the best-ranked one: described as the list left out at this path.
                _note_cut(cut, [r for r in v if r is not best], here)
            out[k] = [_search_row(_screen(best, in_kind=False, path=[*here, 0], cut=None))]
        else:
            out[k] = _screen(v, in_kind=False, path=here, cut=cut)
    return out


def _screen_trim(payload: dict[str, Any]) -> dict[str, Any]:
    # channel_values is engine state; last_outputs repeats every terminal step's output the
    # viewer already received on its node_completed (the 13.4 MB of MKT-167's first run).
    out = _strip_held({k: v for k, v in payload.items() if k not in ("channel_values", "last_outputs")})
    # A step's arguments are screened exactly like its output (Arman, 2026-10-27: the step's In tab claimed "No
    # inputs received" for every step because they were blanked here; testing and diagnosis need them). Provisions,
    # ledgers and raw pages still stay on the server; a large non-kind argument becomes WITHHELD_VALUE, never absent.
    cut: list[dict[str, Any]] = []
    if out.get("event") == "node_started" and isinstance(out.get("inputs"), dict):
        # An argument NAMED like a debug-only key (an `html` page, a `searches` ledger, a transcript) is announced,
        # never dropped: the In tab must not say a step lacked an input it received.
        out["inputs"] = {
            k: WITHHELD_VALUE if k in DEBUG_ONLY_KEYS or k == "messages" else screen_value(v, cut, ["inputs", k])
            for k, v in out["inputs"].items()
        }
    for key in ("output", "payload"):
        if key in out:
            out[key] = screen_value(out[key], cut, [key])
    if cut:
        out["withheld"] = cut
    return out


_DROP = object()

#: What a screen viewer sees in place of a step argument too large to send inline that is not rendered content.
#: (An output value is described in the event's ``withheld`` list instead, so the output keeps its shape.)
WITHHELD_VALUE = "(large value kept on the server — open in AI Watch to see it)"


def _is_kind(value: Any) -> bool:
    """A kind instance, or a non-empty list of them — what a screen renders."""
    if isinstance(value, dict):
        return "__kind" in value
    return isinstance(value, list) and bool(value) and all(isinstance(i, dict) and "__kind" in i for i in value)


def describe_withheld(value: Any, path: list[str | int], ref: str | None) -> dict[str, Any]:
    """A value left out of a screen view, described so the screen can show a stub exactly where it was
    (``types.events.WithheldValue``): what it was, how big, and the stored copy that brings it back.
    ``value`` is ``_DROP`` when the store no longer holds it."""
    from matrx_graph.checkpoint.values import _leaf_bytes

    if value is _DROP:
        return {"path": path, "value_type": "unknown", "bytes": 0, "items": None, "chars": None, "ref": ref}
    if isinstance(value, dict):
        kind, items, chars = "object", len(value), None
    elif isinstance(value, list):
        kind, items, chars = "list", len(value), None
    elif isinstance(value, str):
        kind, items, chars = "text", None, len(value)
    elif isinstance(value, bool):
        kind, items, chars = "boolean", None, None
    elif isinstance(value, (int, float)):
        kind, items, chars = "number", None, None
    elif value is None:
        kind, items, chars = "null", None, None
    else:
        kind, items, chars = "unknown", None, None
    return {"path": path, "value_type": kind, "bytes": _leaf_bytes(value), "items": items, "chars": chars, "ref": ref}


def _fill(
    value: Any,
    store: dict[str, Any],
    withheld: Any = _DROP,
    path: list[str | int] | None = None,
    cut: list[dict[str, Any]] | None = None,
) -> Any:
    here = path or []
    if isinstance(value, dict):
        if len(value) == 1 and isinstance(value.get(REF_KEY), str):
            found = store.get(value[REF_KEY], _DROP)
            if found is not _DROP and _is_kind(found):
                return found
            if withheld is _DROP and cut is not None:
                cut.append(describe_withheld(found, here, value[REF_KEY]))
            return withheld
        out = {k: _fill(v, store, withheld, [*here, k], cut) for k, v in value.items()}
        return {k: v for k, v in out.items() if v is not _DROP}
    if isinstance(value, list):
        return [v for v in (_fill(v, store, withheld, [*here, i], cut) for i, v in enumerate(value)) if v is not _DROP]
    return value


def _fill_event(item: Any, store: dict[str, Any]) -> Any:
    """``_fill`` for one screened event. A withheld step argument reads ``WITHHELD_VALUE`` in place (the In tab,
    Arman 2026-10-27). A withheld OUTPUT value stays out of the value — its shape is unchanged for every reader —
    and is described in the event's ``withheld`` list (path, type, size, stored ref), so the screen can put a loud
    stub exactly where it was and load it back (2026-10-29: "The website, read" lost its five pages silently)."""
    if not isinstance(item, dict):
        return _fill(item, store)
    cut: list[dict[str, Any]] = []
    if item.get("event") == "node_started" and isinstance(item.get("inputs"), dict):
        out = {**_fill({k: v for k, v in item.items() if k not in ("inputs", "withheld")}, store, _DROP, [], cut),
               "inputs": _fill(item["inputs"], store, WITHHELD_VALUE)}
    else:
        out = _fill({k: v for k, v in item.items() if k != "withheld"}, store, _DROP, [], cut)
    earlier = item.get("withheld")
    every = [*(earlier if isinstance(earlier, list) else []), *cut]
    if every:
        out["withheld"] = every
    return out


#: The marker a step's output carries in place of a finding the same response already sent on the step's
#: ``node_emitted`` event (matrx-frontend ``parseEvidenceItem`` reads it as "not a finding" and keeps the emitted one).
EMITTED_KEY = "__matrx_emitted__"


def _digest(value: Any) -> str:
    import hashlib

    from matrx_graph.checkpoint.values import _dumps

    return hashlib.sha256(_dumps(value).encode()).hexdigest()


def mark_emitted(payload: Any, seen: dict[str, dict[str, str]]) -> Any:
    """``payload`` (a screened event payload) with its findings sent ONCE per response (pure but for ``seen``).

    A ``node_emitted`` event records the digest of each keyed list item it carries, by node. A later
    ``node_completed`` of that node carries ``{EMITTED_KEY: item.key}`` in place of an identical output list item.
    ``seen`` lives for ONE response or ONE stream: a client that never received the emitted event (a later page,
    a resumed stream) gets the full item."""
    if not isinstance(payload, dict):
        return payload
    node = payload.get("node_id")
    if not isinstance(node, str):
        return payload
    event = payload.get("event")
    if event == "node_emitted" and isinstance(payload.get("payload"), dict):
        bucket = seen.setdefault(node, {})
        for items in payload["payload"].values():
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and isinstance(item.get("key"), str):
                        bucket[_digest(item)] = item["key"]
        return payload
    if event == "node_completed" and isinstance(payload.get("output"), dict) and seen.get(node):
        bucket = seen[node]
        output: dict[str, Any] = {}
        for name, items in payload["output"].items():
            if isinstance(items, list) and any(isinstance(i, dict) and isinstance(i.get("key"), str) for i in items):
                items = [
                    {EMITTED_KEY: bucket[d]}
                    if isinstance(i, dict) and isinstance(i.get("key"), str) and (d := _digest(i)) in bucket
                    else i
                    for i in items
                ]
            output[name] = items
        return {**payload, "output": output}
    return payload


async def screen_views(
    run_id: str, payloads: list[dict[str, Any]], seen: dict[str, dict[str, str]] | None = None
) -> list[dict[str, Any]]:
    """What a viewer who is NOT an admin in debug mode receives for ``payloads`` (MKT-167 part 2).

    Arman, 2026-10-15: the client gets only what the screen renders. So: step arguments
    (``node_started.inputs``, which the step's In tab renders — Arman, 2026-10-27) screened like an output, a large
    non-kind one as :data:`WITHHELD_VALUE`; no channel state, no repeated ``last_outputs``, no held value (a provision — the key is
    simply absent), and a remaining large value INLINE (a screen
    shows it, and this viewer may not call ``GET /runs/{id}/values``) only when it is a kind
    instance (or a list of them): content the screen renders. A large value that is not a kind
    (a raw page, a request ledger, full search objects, an agent's message list) is withheld, and says so: an
    argument reads :data:`WITHHELD_VALUE` in place; an output value stays out of the value (its shape unchanged)
    and is described in the event's ``withheld`` list — path, type, size and the stored ref (2026-10-29).
    A finding already sent on the step's ``node_emitted`` in this response (``seen``; a stream passes one dict for
    its whole life) is a :data:`EMITTED_KEY` marker on its ``node_completed``.
    """
    seen = {} if seen is None else seen
    trimmed = [_screen_trim(p) if isinstance(p, dict) else p for p in payloads]
    hashes: set[str] = set()
    for item in trimmed:
        hashes |= referenced_hashes(item)
    if hashes:
        store: dict[str, Any] = {}
        ordered = sorted(hashes)
        for i in range(0, len(ordered), MAX_HASHES_PER_READ):
            store |= await load_run_values(run_id, ordered[i : i + MAX_HASHES_PER_READ])
        trimmed = [_fill_event(item, store) for item in trimmed]
    from matrx_graph.knobs import withheld_list_max

    cap = await withheld_list_max()
    trimmed = [_cap_withheld(item, cap) for item in trimmed]
    return [mark_emitted(item, seen) for item in trimmed]


def _cap_withheld(item: Any, limit: int) -> Any:
    """At most ``limit`` cuts listed (the ``workflow.event_payload.withheld_list_max`` knob), the rest counted in
    ``withheld_more``: a list of N pages that each lose their ``html`` would otherwise add N entries to the very
    event the screen view keeps small."""
    cuts = item.get("withheld") if isinstance(item, dict) else None
    if not isinstance(cuts, list) or len(cuts) <= limit:
        return item
    return {**item, "withheld": cuts[:limit], "withheld_more": len(cuts) - limit}


def screen_run_output(output: Any, limit: int, withheld: list[dict[str, Any]] | None = None) -> Any:
    """A run record's ``output`` (``{node_id: step output}``) as a viewer NOT in debug mode receives it (pure).

    The screen view (:func:`screen_value`), then the rule events follow: a step-output child that is not a kind and
    is over ``limit`` (the ``workflow.event_payload.inline_value_max_bytes`` knob) is withheld. Pass ``withheld`` to
    collect a description of each cut (``types.events.WithheldValue``, path from the output's root) — the record
    keeps its shape and the screen still says what it left out. Creativity
    Warehouse, 2026-10-16: the screened record was still 358 KB (web evidence, own-site results, page text)."""
    from matrx_graph.checkpoint.values import _leaf_bytes

    screened = screen_value(_strip_held(output), withheld)
    if not isinstance(screened, dict) or limit <= 0:
        return screened
    out: dict[str, Any] = {}
    for node, step in screened.items():
        if isinstance(step, dict):
            kept: dict[str, Any] = {}
            for k, v in step.items():
                if _is_kind(v) or _leaf_bytes(v) <= limit:
                    kept[k] = v
                elif withheld is not None:
                    withheld.append(describe_withheld(v, [node, k], None))
            step = kept
        elif not _is_kind(step) and _leaf_bytes(step) > limit:
            if withheld is not None:
                withheld.append(describe_withheld(step, [node], None))
            continue
        out[node] = step
    return out


async def resolve_run_values(run_id: str, value: Any) -> Any:
    """``value`` (an event payload or any part of one) with every reference resolved."""
    hashes = referenced_hashes(value)
    if not hashes:
        return value
    store = await load_run_values(run_id, hashes)
    return resolve_values(value, store)


def _held_hashes(value: Any) -> set[str]:
    found: set[str] = set()
    stack = [value]
    while stack:
        item = stack.pop()
        digest = held_hash(item)
        if digest is not None:
            found.add(digest)
        elif isinstance(item, dict):
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return found


async def carry_run_values(
    from_run_id: str, to_run_id: str, value: Any, *, organization_id: str | None = None
) -> Any:
    """``value`` produced in one run made valid in ANOTHER run (a called workflow's answer).

    Both kinds of marker are scoped to the run that wrote them: a reference
    (``REF_KEY``) is resolved from ``from_run_id``'s store, and every held value
    (``HELD_KEY``) is HELD AGAIN in ``to_run_id`` — so the receiving run's steps
    read it exactly as if they had produced it, and it stays off every screen.
    A marker the source run never stored raises :class:`MissingCheckpointValueError`.
    """
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    refs = referenced_hashes(value)
    if refs:
        value = resolve_values(value, await _load_all(from_run_id, refs))
    await _copy_child_values(from_run_id, to_run_id, organization_id=organization_id)
    held = _held_hashes(value)
    if not held:
        return value
    store = await _load_all(from_run_id, held)

    async def carry(item: Any) -> Any:
        digest = held_hash(item)
        if digest is not None:
            if digest not in store:
                raise MissingCheckpointValueError(
                    f"held value {digest[:12]}… is not stored for run {from_run_id}"
                )
            return await hold_on_server(to_run_id, store[digest], organization_id=organization_id)
        if isinstance(item, dict):
            return {k: await carry(v) for k, v in item.items()}
        if isinstance(item, list):
            return [await carry(v) for v in item]
        return item

    return await carry(value)


async def _copy_child_values(child_run_id: str, caller_run_id: str, *, organization_id: str | None = None) -> None:
    """Copy every value the CHILD stored into the CALLER's store — one INSERT … SELECT inside the database.

    The answer a called workflow hands back is whole in memory (callers read ``last_outputs.<step>``), and
    the caller's events, outcome and checkpoints intern it with the same rule the child already applied —
    the same sha256 for the same subtree. Re-writing them from Python cost ~28 s per hand-off (2026-10-28,
    Smart Add offerings: ~15.7 MB / ~500 values); the copy moves no value through Python, and the copied
    hashes are marked stored for the caller so its writes skip them. The caller then OWNS its values: a child
    run (or its definition) deleted later never takes one with it, and every read stays in one run's store.
    A failure here only costs the speed-up: nothing is marked, so the caller's own writes store every value."""
    from matrx_graph.checkpoint.postgres import _STORED_HASH_RUNS, _organization_for_run, _stored_value_hashes

    try:
        org = organization_id or await _organization_for_run(caller_run_id)
        landed = await get_model("WfCheckpointValue").copy_rows_ignore(
            where={"run_id": child_run_id},
            overrides={"run_id": caller_run_id, "organization_id": org},
            columns=["value_hash", "value", "size_bytes"],
            casts={"run_id": "uuid", "organization_id": "uuid"},
            on_conflict=["run_id", "value_hash"],
            returning="value_hash",
        )
    except Exception:  # noqa: BLE001 — the caller's own writes store every value instead (slower, never lost)
        logger.warning(
            "[wf:%s] copying the called run's values FAILED — the caller stores its own copies",
            caller_run_id[:8],
            exc_info=True,
        )
        return
    if not landed:
        return
    _stored_value_hashes.setdefault(caller_run_id, set()).update(str(h) for h in landed)
    if len(_stored_value_hashes) > _STORED_HASH_RUNS:
        _stored_value_hashes.pop(next(iter(_stored_value_hashes)))
    logger.info("[wf:%s] %d value(s) copied from called run %s", caller_run_id[:8], len(landed), child_run_id[:8])


async def _load_all(run_id: str, hashes: set[str]) -> dict[str, Any]:
    ordered = sorted(hashes)
    store: dict[str, Any] = {}
    for i in range(0, len(ordered), MAX_HASHES_PER_READ):
        store |= await load_run_values(run_id, ordered[i : i + MAX_HASHES_PER_READ])
    return store


#: Most bytes of values one ``store_run_values`` call writes while a run's result moves out of its row
#: (a 20 MB result is many statements, never one that times out like the row did).
RUN_OUTPUT_STORE_BATCH_BYTES = 2_097_152


def _step_by_reference(step: Any, store: dict[str, Any], piece: int, limit: int) -> Any:
    """One step's output with its large values by reference. An object keeps its keys (what a reader sees at a
    glance: ``__kind``, ``content``, ``count``) when that alone brings it under ``limit``; otherwise the
    whole output is one reference. Values are interned at ``piece`` bytes, the checkpoint's grain, so the
    same subtrees a checkpoint already stored for this run are the same rows."""
    from matrx_graph.checkpoint.values import _leaf_bytes, intern_values

    if isinstance(step, dict) and held_hash(step) is None and not _is_ref(step):
        kept = {k: intern_values(v, store, piece) for k, v in step.items()}
        if _leaf_bytes(kept) <= limit:
            return kept
    return intern_values(step, store, piece)


def _is_ref(value: Any) -> bool:
    from matrx_graph.checkpoint.values import _is_ref as is_ref

    return is_ref(value)


def run_output_row(output: Any, limit: int, piece: int) -> tuple[Any, dict[str, Any]]:
    """``workflow.run.output`` (``{step: output}``) as the row stores it, plus the values it references (pure).

    Every step output over ``limit`` goes by reference; while the whole row is still over ``limit``, the
    largest remaining steps follow. Step ids always stay readable. ``limit <= 0`` changes nothing."""
    from matrx_graph.checkpoint.values import _REF_BYTES, _leaf_bytes

    store: dict[str, Any] = {}
    if limit <= 0 or not isinstance(output, dict) or _leaf_bytes(output) <= limit:
        return output, store
    piece = piece if 0 < piece < limit else limit
    sized = sorted(((_leaf_bytes(v), k) for k, v in output.items()), reverse=True)
    out = dict(output)
    total = sum(size for size, _ in sized)
    for size, key in sized:
        if size <= limit and total <= limit:
            break
        if size <= _REF_BYTES * 2:
            break
        out[key] = _step_by_reference(output[key], store, piece, limit)
        total -= size - _leaf_bytes(out[key])
    return out, store


async def run_output_limit() -> int:
    """The run-output knob when by-reference storage is on (a value store exists and the knob is > 0), else 0.
    The run store reads the row's existing output only when this is on."""
    from matrx_graph.knobs import run_output_inline_value_max_bytes

    if not _store_available():
        return 0
    return max(0, await run_output_inline_value_max_bytes())


async def output_by_reference(
    run_id: str,
    output: Any,
    *,
    organization_id: str | None = None,
    existing: dict[str, Any] | None = None,
) -> Any:
    """The run row's ``output`` with its large step outputs stored in the run's value store and referenced.

    ``existing`` is what the row already holds. A write MERGES into the row (``JsonbMerge``: incoming keys
    replace, earlier keys stay), so the row is sized as existing + incoming: when the merged row would be over
    the knob, earlier legs' large steps move by reference too and are returned for the merge to rewrite.
    Without this a many-leg run (pause/interrupt/resume) rebuilt a > 1 MB row one under-limit leg at a time.

    Stored BEFORE the row is written, so no reader sees a reference whose value is missing. Raises when the
    store write fails: the caller's terminal write then ends the run ``final_write_failed`` (loud), never a
    row that silently lost a value. Without a value store (a DB-less install) the output stays inline."""
    from matrx_graph.knobs import checkpoint_write_policy

    if not isinstance(output, dict) or not output:
        return output
    limit = await run_output_limit()
    if limit <= 0:
        return output
    piece = (await checkpoint_write_policy()).inline_value_max_bytes
    earlier = existing if isinstance(existing, dict) else {}
    merged = {**earlier, **output}
    row, values = run_output_row(merged, limit, piece)
    if not values:
        return output
    from matrx_graph.checkpoint.values import _leaf_bytes

    batch: dict[str, Any] = {}
    size = 0
    for digest, value in values.items():
        batch[digest] = value
        size += _leaf_bytes(value)
        if size >= RUN_OUTPUT_STORE_BATCH_BYTES:
            await store_run_values(run_id, batch, organization_id=organization_id)
            batch, size = {}, 0
    if batch:
        await store_run_values(run_id, batch, organization_id=organization_id)
    # Every incoming key, plus each earlier key whose stored form changed (moved by reference now).
    moved = [k for k in earlier if k not in output and row[k] is not earlier[k]]
    logger.info(
        "[wf:%s] run output: %d value(s) stored by reference (%d earlier step(s) moved)",
        run_id[:8],
        len(values),
        len(moved),
    )
    return {**{k: row[k] for k in output}, **{k: row[k] for k in moved}}


def _missing_output(digest: str) -> dict[str, Any]:
    return {"output_elided": True, "where": "workflow.checkpoint_value", "missing": True, "reference": digest}


async def _load_tolerant(run_id: str, hashes: list[str]) -> dict[str, Any]:
    """``_load_all`` that survives a value whose NESTED value is gone: the batch is halved until the bad one is
    alone (dropped, so it reads as missing). A few reads per bad value, never one read per hash."""
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    if not hashes:
        return {}
    try:
        return await _load_all(run_id, set(hashes))
    except MissingCheckpointValueError:
        if len(hashes) == 1:
            return {}
        mid = len(hashes) // 2
        return await _load_tolerant(run_id, hashes[:mid]) | await _load_tolerant(run_id, hashes[mid:])


async def resolve_run_output(run_id: str, output: Any, *, missing: str = "raise") -> Any:
    """A run row's ``output`` with every reference resolved — what every server reader of the run receives.

    A reference this run never stored (a value deleted by retention) is logged as an ERROR and raises
    :class:`RunOutputValueMissingError` (``missing="raise"``, every reader that hands the answer on); the
    display read passes ``missing="mark"`` and gets an honest ``{"output_elided": true, "missing": true}``
    marker in its place. Never a raw reference. Values are read in batches, never one read per hash."""
    from matrx_graph.checkpoint.values import MissingCheckpointValueError

    if missing not in ("raise", "mark"):
        raise ValueError(f"missing must be 'raise' or 'mark', not {missing!r}")
    hashes = referenced_hashes(output)
    if not hashes:
        return output
    try:
        store = await _load_all(run_id, hashes)
    except MissingCheckpointValueError:
        store = await _load_tolerant(run_id, sorted(hashes))
    absent = sorted(hashes - set(store))
    if not absent:
        return resolve_values(output, store)
    logger.error(
        "[wf:%s] run output names %d stored value(s) that are missing (first %s)",
        run_id[:8],
        len(absent),
        absent[0][:12],
    )
    if missing == "raise":
        raise RunOutputValueMissingError(run_id, absent)

    def fill(value: Any) -> Any:
        if _is_ref(value):
            return store[value[REF_KEY]] if value[REF_KEY] in store else _missing_output(value[REF_KEY])
        if isinstance(value, dict):
            return {k: fill(v) for k, v in value.items()}
        if isinstance(value, list):
            return [fill(v) for v in value]
        return value

    return fill(output)


__all__ = [
    "MAX_HASHES_PER_READ",
    "RunOutputValueMissingError",
    "output_by_reference",
    "resolve_run_output",
    "run_output_limit",
    "run_output_row",
    "carry_run_values",
    "fetch_stored_values",
    "HELD_KEY",
    "held_hash",
    "hold_on_server",
    "new_held_ref",
    "resolve_step_inputs",
    "EMITTED_KEY",
    "mark_emitted",
    "describe_withheld",
    "screen_run_output",
    "screen_value",
    "screen_views",
    "intern_event_payload",
    "load_run_values",
    "resolve_run_values",
    "store_run_values",
]
