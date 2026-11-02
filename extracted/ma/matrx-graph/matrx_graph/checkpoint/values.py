"""Large values in a checkpoint go BY REFERENCE, stored once per run (MKT-111).

THE FAILURE THIS CLOSES (2026-10-15). A Smart Add identify round fans one step's
output (a 311 KB social-lookup ledger, page text, search payloads) into nine
capture points. Every join target buffered its own copy in ``pending_bindings``,
every scheduled invocation carried its merged copy in ``next_invocations``, and
every super-step's checkpoint repeated all of it: one round wrote 9 checkpoint
rows totalling 37 MB (the largest 11 MB) for perhaps 2 MB of distinct data, and
the server held the Python form of each row (several times its JSON size) while
writing it. Three concurrent rounds took a 4 GB task out of memory.

The rule, for every workflow: a value whose serialized size is over the
``workflow.checkpoint_write.inline_value_max_bytes`` knob is replaced in the
checkpoint row by ``{REF_KEY: <sha256>}`` and stored ONCE per run in
``workflow.checkpoint_value`` (content-addressed, so the same value on nine edges
and in nine checkpoints is one row). Interning is bottom-up, so a large value
that differs from its sibling only in one small field still shares every large
part. Loading resolves the references back, so a loaded :class:`Checkpoint` is
exactly what was saved (modulo the JSON round trip the row always applied).

Pure functions — no I/O. The Postgres checkpointer persists the store; the
guard test (``aidream tests/test_workflow_checkpoint_stays_small.py``) measures a
real round's rows through the same :func:`checkpoint_row`.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

#: The key that marks a reference. Namespaced so a person's own data can never be
#: mistaken for one (a plain ``$ref`` is a real JSON-Schema key).
REF_KEY = "__matrx_checkpoint_value__"

#: Serialized size of a reference marker (``{"<REF_KEY>": "<64 hex>"}``).
_REF_BYTES = len(json.dumps({REF_KEY: "0" * 64}))


def _dumps(value: Any) -> str:
    return json.dumps(value, default=str, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _leaf_bytes(value: Any) -> int:
    if isinstance(value, str):
        return len(value.encode()) + 2
    if value is None or isinstance(value, bool):
        return 5
    if isinstance(value, (int, float)):
        return len(repr(value))
    return len(_dumps(value).encode())


def intern_values(value: Any, store: dict[str, Any], max_inline_bytes: int) -> Any:
    """``value`` with every subtree over ``max_inline_bytes`` replaced by a reference.

    The replaced subtrees are added to ``store`` (hash → value, itself interned).
    ``max_inline_bytes <= 0`` disables interning (returns ``value`` unchanged).
    """
    if max_inline_bytes <= 0:
        return value
    return _intern(value, store, max_inline_bytes)[0]


def _intern(value: Any, store: dict[str, Any], limit: int) -> tuple[Any, int]:
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        size = 2
        for key, child in value.items():
            new_child, child_size = _intern(child, store, limit)
            out[key] = new_child
            size += len(str(key).encode()) + 4 + child_size
    elif isinstance(value, (list, tuple)):
        out_list: list[Any] = []
        size = 2
        for child in value:
            new_child, child_size = _intern(child, store, limit)
            out_list.append(new_child)
            size += child_size + 1
        out = out_list  # type: ignore[assignment]
    else:
        size = _leaf_bytes(value)
        if size <= limit:
            return value, size
        out = value  # a long string goes by reference too
    if size <= limit:
        return out, size
    digest = hashlib.sha256(_dumps(out).encode()).hexdigest()
    store.setdefault(digest, out)
    return {REF_KEY: digest}, _REF_BYTES


def referenced_hashes(value: Any) -> set[str]:
    """Every reference hash ``value`` carries (not following the references)."""
    found: set[str] = set()
    stack = [value]
    while stack:
        item = stack.pop()
        if isinstance(item, dict):
            ref = item.get(REF_KEY) if len(item) == 1 else None
            if isinstance(ref, str):
                found.add(ref)
                continue
            stack.extend(item.values())
        elif isinstance(item, list):
            stack.extend(item)
    return found


class MissingCheckpointValueError(LookupError):
    """A checkpoint names a stored value that is not in the run's value store."""


class RunOutputValueMissingError(LookupError):
    """A run's ``output`` references a stored value that is gone (``workflow.checkpoint_value`` row deleted).

    Raised by :func:`resolve_run_output` (``RunStore.load``) so a missing value never flows on as data — a
    caller handing the run's answer onward (a ``subgraph.call`` reattach, a plan step, a mandate's answer, a
    chat wake) fails or says so in words. Only the display read (``GET /runs/{id}``) asks for the honest
    ``{"output_elided": true, "missing": true}`` marker instead (``missing="mark"``)."""

    def __init__(self, run_id: str, missing: list[str]) -> None:
        self.run_id = run_id
        self.missing = missing
        super().__init__(
            f"run {run_id}'s result names {len(missing)} stored value(s) that are missing "
            f"(cause run_output_value_missing; first {missing[0][:12]}…)"
        )


class RunInputValueMissingError(LookupError):
    """A run's stored input values (``metadata._settings.input_values``) reference a value that is gone.

    Raised by ``run_store.execution_input_values`` on a leg about to EXECUTE the run, so it fails naming the
    missing value — never starts with a reference marker where its input should be. ``RunStore.load`` never
    raises it: an owner check, cancel or delete of the run keeps working."""

    def __init__(self, run_id: str, detail: str) -> None:
        self.run_id = run_id
        super().__init__(
            f"run {run_id}'s stored input values are missing (cause run_input_value_missing; {detail})"
        )


def resolve_values(value: Any, store: dict[str, Any]) -> Any:
    """``value`` with every reference replaced by its stored value (recursively)."""
    if isinstance(value, dict):
        if len(value) == 1 and isinstance(value.get(REF_KEY), str):
            digest = value[REF_KEY]
            if digest not in store:
                raise MissingCheckpointValueError(
                    f"checkpoint value {digest[:12]}… is referenced but not stored for this run"
                )
            return resolve_values(store[digest], store)
        return {k: resolve_values(v, store) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve_values(v, store) for v in value]
    return value


def _intern_each(mapping: Any, store: dict[str, Any], limit: int) -> Any:
    if not isinstance(mapping, dict):
        return intern_values(mapping, store, limit)
    return {k: intern_values(v, store, limit) for k, v in mapping.items()}


def _force_ref(value: Any, store: dict[str, Any]) -> dict[str, str]:
    digest = hashlib.sha256(_dumps(value).encode()).hexdigest()
    store.setdefault(digest, value)
    return {REF_KEY: digest}


def _is_ref(value: Any) -> bool:
    return isinstance(value, dict) and len(value) == 1 and isinstance(value.get(REF_KEY), str)


def _fit_binding(binding: dict[str, Any], store: dict[str, Any], limit: int) -> dict[str, Any]:
    """MKT-130: a binding whose many mid-size values add up past the knob goes by reference, largest first.

    Each value under the knob stays inline on its own, but a join target that buffers dozens of
    them (a row measured 22-69 KB) is the same failure as one big value. Argument names stay
    readable; only the biggest remaining values are replaced until the binding is back under the knob.
    """
    if _leaf_bytes(binding) <= limit:
        return binding
    candidates: list[tuple[int, str, str]] = []
    for edge_id, edge in binding["edges"].items():
        payload = edge.get("payload") if isinstance(edge, dict) else None
        if isinstance(payload, dict):
            for arg, value in payload.items():
                if not _is_ref(value):
                    size = _leaf_bytes(value)
                    if size > _REF_BYTES:
                        candidates.append((size, edge_id, arg))
    candidates.sort(reverse=True)
    edges = {k: ({**v, "payload": dict(v["payload"])} if isinstance(v, dict) and isinstance(v.get("payload"), dict) else v)
             for k, v in binding["edges"].items()}
    total = _leaf_bytes(binding)
    for size, edge_id, arg in candidates:
        if total <= limit:
            break
        edges[edge_id]["payload"][arg] = _force_ref(edges[edge_id]["payload"][arg], store)
        total -= size - _REF_BYTES
    return {**binding, "edges": edges}


def _fit_column(bindings: dict[str, Any], store: dict[str, Any], limit: int) -> dict[str, Any]:
    """MKT-130: the WHOLE ``pending_bindings`` column is measured against the knob, not each binding alone.

    Six join targets that each buffer the same ~4 KB edge map are 24 KB together. While the column is
    over the knob, the largest inline ``edges`` map is replaced by a reference; the store is content
    addressed, so identical maps on every node (and in every checkpoint of the run) are one row.
    Node ids, firing counters and loop stacks stay readable.
    """
    while _leaf_bytes(bindings) > limit:
        pick: tuple[int, str] | None = None
        for node_id, binding in bindings.items():
            edges = binding.get("edges") if isinstance(binding, dict) else None
            if isinstance(edges, dict) and not _is_ref(edges):
                size = _leaf_bytes(edges)
                if size > _REF_BYTES and (pick is None or size > pick[0]):
                    pick = (size, node_id)
        if pick is None:
            break
        node_id = pick[1]
        bindings = {**bindings, node_id: {**bindings[node_id], "edges": _force_ref(bindings[node_id]["edges"], store)}}
    return bindings


def checkpoint_row(
    *,
    channel_values: Any,
    pending_bindings: Any,
    next_invocations: Any,
    interrupt_payload: Any,
    max_inline_bytes: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """The stored JSON columns of a checkpoint row, interned, plus the new values.

    Only DATA positions are interned — each channel's value, each delivered
    edge's payload argument, each scheduled invocation's input argument — so the
    row's skeleton (node ids, edge ids, correlation keys, argument names) stays
    readable by anything that inspects a row without loading it (run summaries,
    the sleep/wake marker). ``interrupt_payload`` stays inline: it is read raw.

    Returns ``(columns, store)``: ``store`` is hash → value for every referenced
    value, deduplicated across all columns. The caller persists ``store`` for
    the run (idempotently — a hash already stored for the run is the same value).
    """
    store: dict[str, Any] = {}
    limit = max_inline_bytes
    bindings = pending_bindings
    if limit > 0 and isinstance(pending_bindings, dict):
        bindings = {}
        for node_id, binding in pending_bindings.items():
            if isinstance(binding, dict) and isinstance(binding.get("edges"), dict):
                binding = {
                    **binding,
                    "edges": {
                        edge_id: {**edge, "payload": _intern_each(edge.get("payload"), store, limit)}
                        if isinstance(edge, dict) and "payload" in edge
                        else edge
                        for edge_id, edge in binding["edges"].items()
                    },
                }
                binding = _fit_binding(binding, store, limit)
            bindings[node_id] = binding
        bindings = _fit_column(bindings, store, limit)
    invocations = next_invocations
    if limit > 0 and isinstance(next_invocations, list):
        invocations = [
            {**inv, "inputs": _intern_each(inv.get("inputs"), store, limit)}
            if isinstance(inv, dict) and "inputs" in inv
            else inv
            for inv in next_invocations
        ]
    columns = {
        "channel_values": _intern_each(channel_values, store, limit) if limit > 0 else channel_values,
        "pending_bindings": bindings,
        "next_invocations": invocations,
        "interrupt_payload": interrupt_payload,
    }
    return columns, store


def checkpoint_columns(checkpoint: Any, max_inline_bytes: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """What the Postgres checkpointer stores for ``checkpoint``: its JSON columns, interned, and the values.

    One function so the guard test measures exactly the bytes production writes.
    """
    return checkpoint_row(
        channel_values=checkpoint.channel_values,
        pending_bindings={
            node_id: binding.model_dump(mode="json")
            for node_id, binding in checkpoint.pending_bindings.items()
        },
        next_invocations=[ni.model_dump(mode="json") for ni in checkpoint.next_invocations],
        interrupt_payload=checkpoint.interrupt_payload,
        max_inline_bytes=max_inline_bytes,
    )


#: The DATA fields of a workflow event (MKT-167). Everything else on an event — its
#: type, ids, timing, kind verdicts, the small ``wrapper`` / ``metadata`` — is the
#: skeleton every screen folds, and stays inline. ``payload`` (a ``node_emitted``
#: delivery the person watches arrive) and stream frames are never touched.
EVENT_VALUE_FIELDS: tuple[str, ...] = ("inputs", "output", "last_outputs", "channel_values")


def _fit_mapping(mapping: dict[str, Any], store: dict[str, Any], limit: int) -> dict[str, Any]:
    """``mapping`` (already interned child by child) with its largest inline children
    replaced by references until the whole mapping is back under ``limit``.

    Keys always stay readable — a reader still sees ``__kind``, ``iteration`` or a
    decision field — only the heaviest values move out.
    """
    if _leaf_bytes(mapping) <= limit:
        return mapping
    sized = sorted(
        ((_leaf_bytes(v), k) for k, v in mapping.items() if not _is_ref(v)),
        reverse=True,
    )
    out = dict(mapping)
    total = _leaf_bytes(mapping)
    for size, key in sized:
        if total <= limit or size <= _REF_BYTES:
            break
        out[key] = _force_ref(out[key], store)
        total -= size - _REF_BYTES
    return out


def event_payload_row(payload: dict[str, Any], max_inline_bytes: int) -> tuple[dict[str, Any], dict[str, Any]]:
    """A workflow event's payload with its large DATA values by reference (MKT-167).

    The same rule and the same store as a checkpoint: one Smart Add run wrote 49.7 MB
    of events because every ``node_started`` carried the full 1.4 MB provision block in
    its ``inputs`` and ``run_completed`` repeated every output (13.4 MB). Each field in
    :data:`EVENT_VALUE_FIELDS` keeps its keys; any child over ``max_inline_bytes`` (and,
    while the field is still over it, the largest remaining children) is replaced by
    ``{REF_KEY: <sha256>}``, its value returned in ``store`` for the run's
    ``workflow.checkpoint_value`` rows. A payload already interned is unchanged.
    ``max_inline_bytes <= 0`` returns the payload untouched.
    """
    store: dict[str, Any] = {}
    if max_inline_bytes <= 0 or not isinstance(payload, dict):
        return payload, store
    out = payload
    for field in EVENT_VALUE_FIELDS:
        value = payload.get(field)
        if value is None or _leaf_bytes(value) <= max_inline_bytes:
            continue
        if isinstance(value, dict) and not _is_ref(value):
            interned = _fit_mapping(_intern_each(value, store, max_inline_bytes), store, max_inline_bytes)
        else:
            interned = intern_values(value, store, max_inline_bytes)
        if out is payload:
            out = dict(payload)
        out[field] = interned
    return out, store


def outcome_input_row(inputs: Any, max_inline_bytes: int) -> tuple[Any, dict[str, Any]]:
    """A node outcome's ``input`` or ``output`` with its large values by reference (MKT-170/171).

    The same rule and the same store as an event's ``inputs``: each child over
    ``max_inline_bytes`` becomes ``{REF_KEY: <sha256>}`` (value returned in ``store``).
    """
    store: dict[str, Any] = {}
    if max_inline_bytes <= 0 or inputs is None or _leaf_bytes(inputs) <= max_inline_bytes:
        return inputs, store
    if isinstance(inputs, dict) and not _is_ref(inputs):
        return _fit_mapping(_intern_each(inputs, store, max_inline_bytes), store, max_inline_bytes), store
    return intern_values(inputs, store, max_inline_bytes), store


def row_bytes(columns: dict[str, Any]) -> int:
    """Serialized size of a checkpoint row's JSON columns — what the guard bounds."""
    return sum(len(_dumps(v).encode()) for v in columns.values() if v is not None)


__all__ = [
    "RunInputValueMissingError",
    "RunOutputValueMissingError",
    "EVENT_VALUE_FIELDS",
    "REF_KEY",
    "MissingCheckpointValueError",
    "checkpoint_columns",
    "checkpoint_row",
    "event_payload_row",
    "intern_values",
    "referenced_hashes",
    "resolve_values",
    "row_bytes",
]
