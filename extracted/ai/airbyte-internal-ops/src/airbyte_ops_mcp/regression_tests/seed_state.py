# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""A caller-chosen state for a regression read: its shape, and how it reaches the job.

A seed is the per-stream list `get_connection_state` returns: STREAM state
messages, one per stream. `seed_state_error` checks that outer shape, at the
MCP tool before a dispatch and in the workflow before a build; the connector
is the authority on what each message means.

Run as a script by the workflow's `Resolve READ inputs` step, this module also
carries the seed from the dispatch payload to a file for the READ step, and
registers its cursor values and its one-line form as masks first. The runner
prints a step's `env:` and `with:` in the step's log header before the step
runs, so a seed passed either way would be in the job log, which outlives the
run's artifacts, before any script could mask it; the payload at
`$GITHUB_EVENT_PATH` is never printed. The script imports nothing outside the
standard library, so the step runs it with the runner's `python3` straight
from the checkout.
"""

from __future__ import annotations

import json
import sys
from typing import Any

SEED_STATE_NEEDS_CONNECTION = (
    "state_json needs connection_id: without a connection the configured "
    "catalog is generated from DISCOVER with every stream on full_refresh, so "
    "the read would ignore the seed and still report it as used"
)

SEED_STATE_NEEDS_DISPATCH = (
    "state_json reaches the job through the dispatch payload, which the runner "
    "never prints; a calling workflow has no payload for it, so seed a read by "
    "dispatching this workflow"
)

STREAM_STATE_MESSAGE = (
    '{"type": "STREAM", "stream": {"stream_descriptor": {"name": ...}, '
    '"stream_state": {...}}}'
)

MASK_MIN_LENGTH = 8
"""Values shorter than this are not masked.

A cursor does not fit in them, and a mask redacts its value everywhere in the
job log, so a short one would eat unrelated output.
"""


def seed_state_error(state_json: str) -> str | None:
    """Why `state_json` cannot seed a read, or `None` when it can.

    Only the outer shape is checked: a non-empty list of STREAM state
    messages, each naming its stream. No message echoes the seed.
    """
    try:
        state = json.loads(state_json)
    except ValueError as exc:
        return f"state_json is not valid JSON: {exc}"
    if isinstance(state, dict):
        kind = state.get("type")
        if kind == "STREAM":
            return (
                "state_json holds a single STREAM state message; wrap it in a "
                "list, one message per stream"
            )
        if kind in ("GLOBAL", "LEGACY"):
            return (
                f"state_json holds a {kind} state message, which cannot seed a "
                "read; give the per-stream list `get_connection_state` returns, "
                f"one {STREAM_STATE_MESSAGE} per stream"
            )
        return (
            "state_json must be a JSON list of STREAM state messages, got a bare "
            f"object (the legacy state shape); give one {STREAM_STATE_MESSAGE} "
            "per stream"
        )
    if not isinstance(state, list):
        return (
            "state_json must be a JSON list of STREAM state messages, got "
            f"{_json_name(state)}"
        )
    if not state:
        return (
            "state_json is an empty list, which seeds nothing; leave it unset "
            "for a cold read"
        )
    for index, message in enumerate(state):
        error = _message_error(message)
        if error:
            return f"state_json[{index}] {error}"
    return None


def _json_name(value: Any) -> str:
    names = {
        bool: "a boolean",
        int: "a number",
        float: "a number",
        str: "a string",
        type(None): "null",
    }
    return names.get(type(value), type(value).__name__)


def _message_error(message: Any) -> str | None:
    if not isinstance(message, dict):
        return (
            f"is {_json_name(message)}, not a state message; expected "
            f"{STREAM_STATE_MESSAGE}"
        )
    kind = message.get("type")
    if kind is None:
        return f"has no type; expected {STREAM_STATE_MESSAGE}"
    if kind != "STREAM":
        # The seed's own text, so quoted, escaped and cut rather than echoed.
        shown = repr(kind)[:40] if isinstance(kind, str) else _json_name(kind)
        return (
            f"is a {shown} state message; only STREAM messages seed a read, one "
            "per stream"
        )
    stream = message.get("stream")
    descriptor = stream.get("stream_descriptor") if isinstance(stream, dict) else None
    name = descriptor.get("name") if isinstance(descriptor, dict) else None
    if not isinstance(name, str) or not name:
        return f"names no stream; expected {STREAM_STATE_MESSAGE}"
    return None


def seeded_streams(state_json: str) -> list[tuple[str | None, str]]:
    """The streams a seed that passed `seed_state_error` names, in its order.

    Each is `(namespace, name)`, as Airbyte identifies a stream, with a
    missing or empty namespace as `None`: `users` in two namespaces is two
    streams, and a connector applies a state only to the one it names.
    """
    descriptors = [
        message["stream"]["stream_descriptor"] for message in json.loads(state_json)
    ]
    return [
        (descriptor.get("namespace") or None, descriptor["name"])
        for descriptor in descriptors
    ]


def mask_values(state_json: str) -> list[str]:
    """What to register with `::add-mask::` so the seed does not show in the job log.

    The seed itself when it is one line, which is what a step that printed it
    would show, and its cursor values -- every scalar under a message's
    `stream_state` -- since a connector may log the state it was given. Each
    cursor is masked as written and as `json.dumps` writes it inside a JSON
    string, the form a connector that logs its state as JSON prints: the
    runner masks a value with its quotes and backslashes escaped on its own,
    but not with its non-ASCII written as `\\uXXXX`. A pretty-printed seed
    is not masked line by line: its structural lines (`{`, `},`,
    `"stream": {`) would redact the same text everywhere in the log. Values
    shorter than `MASK_MIN_LENGTH` are left out for the same reason, a short
    cursor in both forms. A seed that is not JSON has no values to find, so
    its lines are masked instead. `%`, CR and LF are escaped, since the
    runner unescapes them when it reads a command's value, and a mask is one
    line.
    """
    try:
        state = json.loads(state_json)
    except ValueError:
        candidates = [line.strip() for line in state_json.splitlines()]
    else:
        whole = state_json.strip()
        candidates = [whole] if "\n" not in whole else []
        candidates.extend(
            form
            for value in _cursor_values(state)
            if len(value) >= MASK_MIN_LENGTH
            for form in (value, json.dumps(value)[1:-1])
        )
    values: dict[str, None] = {}
    for candidate in candidates:
        if len(candidate) >= MASK_MIN_LENGTH:
            values.setdefault(_escape(candidate), None)
    return list(values)


def _escape(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def _cursor_values(state: Any) -> list[str]:
    """Every scalar under a `stream_state`, as text, wherever it sits in `state`."""
    found: list[str] = []

    def walk(node: Any, inside_state: bool) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, inside_state or key == "stream_state")
        elif isinstance(node, list):
            for value in node:
                walk(value, inside_state)
        elif (
            inside_state
            and isinstance(node, (str, int, float))
            and not isinstance(node, bool)
        ):
            found.append(str(node))

    walk(state, False)
    return found


def main(argv: list[str]) -> int:
    """Carry the seed from the dispatch payload to a file, masked and checked.

    `argv` is the event payload's path, the file to write and the run's
    `connection_id` (empty when none). The masks go out first, before the
    seed is judged, so a malformed seed is not shown either; then the error,
    or the streams the seed names. Workflow commands go to stdout, where the
    runner reads them. Returns the exit status.
    """
    event_path, seed_path, connection_id = argv
    with open(event_path, encoding="utf-8") as handle:
        inputs = json.load(handle).get("inputs") or {}
    state_json = inputs.get("state_json") or ""
    if not state_json:
        print(f"::error::{SEED_STATE_NEEDS_DISPATCH}")
        return 1
    for value in mask_values(state_json):
        print(f"::add-mask::{value}")
    sys.stdout.flush()
    error = (
        SEED_STATE_NEEDS_CONNECTION
        if not connection_id
        else seed_state_error(state_json)
    )
    if error:
        print(f"::error::{error}")
        return 1
    with open(seed_path, "w", encoding="utf-8") as handle:
        handle.write(state_json)
    names = [
        f"{namespace}.{name}" if namespace else name
        for namespace, name in seeded_streams(state_json)
    ]
    print(f"Seeding the READ with state for {len(names)} stream(s): {', '.join(names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
