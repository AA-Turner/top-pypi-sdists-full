"""Sample parts as `POST /v1/runs/{id}/samples/batch` takes them (twin: app/runs/samples): the body's
lists checked against the contract (`probe.generated.samples`), turns fitted to it and scrubbed, the 4 KiB log tail
and 1 MiB log cap, and the send-time gate on the turn capture fields (D7)."""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel

from ....foundation.compat.compat import StrEnum
from ....foundation.safe_warn import safe_warn as _diagnostics
from ...values.unstorable import ESCAPE as NUL_ESCAPE
from ...values.unstorable import NUL
from ....generated.samples import (
    CommitIn,
    GroupIn,
    LiveTurnIn,
    PlanIn,
    SamplePartIn,
    SealIn,
    TaskIn,
    WeightVersionIn,
)


class BatchList(StrEnum):
    """The lists a samples batch body carries (`SampleBatchIn`); the drain concatenates each when
    it merges ops. `plan` is one object, not a list: ops with different plans never merge."""

    TASKS = "tasks"
    SAMPLES = "samples"
    GROUPS = "groups"
    SEALS = "seals"
    COMMITS = "commits"
    WEIGHTS = "weights"
    LIVE_TURNS = "live_turns"


#: Each list's item, as the contract shapes it: every item is checked here before it is journaled,
#: so a part sending a field its role does not own is dropped alone, never 422s its whole batch.
ITEM_MODELS: dict[BatchList, type[BaseModel]] = {
    BatchList.TASKS: TaskIn,
    BatchList.SAMPLES: SamplePartIn,
    BatchList.GROUPS: GroupIn,
    BatchList.SEALS: SealIn,
    BatchList.COMMITS: CommitIn,
    BatchList.WEIGHTS: WeightVersionIn,
    BatchList.LIVE_TURNS: LiveTurnIn,
}
#: The batch's one plan-change object (`PlanIn`).
PLAN_FIELD = "plan"
PLAN_FIELDS = tuple(PlanIn.model_fields)


def to_wire_item(name: BatchList, item: Mapping[str, Any]) -> tuple[dict, BaseModel]:
    """``item`` checked against its contract model; its JSON as sent (only the fields set) and the
    model. Raises the model's ValidationError."""
    model = ITEM_MODELS[name].model_validate(item)
    return model.model_dump(mode="json", exclude_unset=True), model


def to_wire_plan(plan: Mapping[str, Any]) -> dict:
    """A plan change checked against `PlanIn`: only the fields given."""
    return PlanIn.model_validate(plan).model_dump(mode="json", exclude_unset=True)


#: Text a row holds inline; longer goes whole to R2 as a blob (D2).
MAX_INLINE_TEXT_BYTES = 64 * 1024
#: The log tail kept on the row.
MAX_LOG_TAIL_BYTES = 4 * 1024
#: One sample's full log in its bundle, keeping the tail (§3.3b).
MAX_LOG_BYTES = 1024 * 1024
MAX_ERROR_MESSAGE_CHARS = 1024

#: Task fields a generator sample may carry; the SDK lifts them into one `tasks` item per task.
TASK_FIELDS = ("prompt", "label", "dataset", "reward_max")
#: SDK-only input names, never sent as such: the full log, the per-token arrays.
LOG_INPUTS = ("log_text",)
TOKEN_INPUTS = {"tokens": "token_arrays", "trainer_tokens": "trainer_token_arrays"}


def to_plain(value: Any) -> dict:
    """A sample given as a dict or a pydantic model, as a plain dict with no None fields."""
    if isinstance(value, Mapping):
        return {key: item for key, item in value.items() if item is not None}
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        return dump(mode="json", exclude_none=True)
    raise TypeError(f"a sample is a dict or a model, not {type(value).__name__}")


def cut_tail(text: str, limit: int) -> tuple[str, bool]:
    """The last ``limit`` bytes of ``text`` (on a character boundary) and whether it was cut."""
    raw = text.encode("utf-8")
    if len(raw) <= limit:
        return text, False
    return raw[-limit:].decode("utf-8", errors="ignore"), True


#: The contract's caps on a turn's names (`Message`, `MessageToolCall`, `TurnToolCall`, `TrialFile`), in characters.
MAX_ROLE_CHARS = 64
MAX_NAME_CHARS = 256
MAX_FILE_PATH_CHARS = 1024
MAX_TOOL_ERROR_CHARS = 1024


def fit_turns(turns: list) -> list:
    """``turns`` (copies) in the contract's shape where a framework's own shape differs: OpenAI tool calls
    (`{type, function: {name, arguments}}`, arguments a dict or text) made flat `MessageToolCall`s, ids and names cut
    to 256 characters, a role to 64, a reasoning that is not text dropped. A cut is a plain prefix, so a call's id and
    the tool message naming it are cut alike. Before this a raw OpenAI message cost its whole sample (A3)."""
    return [_fit_turn(turn) for turn in turns]


def _fit_turn(turn: Any) -> Any:
    if not isinstance(turn, Mapping):
        return turn
    fitted = dict(turn)
    if isinstance(fitted.get("messages"), list):
        fitted["messages"] = [_fit_message(message) for message in fitted["messages"]]
    if isinstance(fitted.get("tool_calls"), list):
        fitted["tool_calls"] = [_fit_names(dict(call), ("id", "name")) if isinstance(call, Mapping) else call
                                for call in fitted["tool_calls"]]  # fmt: skip
    return fitted


def _fit_message(message: Any) -> Any:
    if not isinstance(message, Mapping):
        return message
    fitted = _fit_names(dict(message), ("name", "tool_call_id"))
    if isinstance(fitted.get("role"), str):
        fitted["role"] = fitted["role"][:MAX_ROLE_CHARS]
    if "reasoning" in fitted and not isinstance(fitted["reasoning"], str):
        fitted.pop("reasoning")
    calls = fitted.get("tool_calls")
    if calls is not None:
        fitted["tool_calls"] = [call for call in map(to_message_tool_call, calls) if call is not None] \
            if isinstance(calls, list) else []  # fmt: skip
        if not fitted["tool_calls"]:
            fitted.pop("tool_calls")
    return fitted


def to_message_tool_call(item: Any) -> dict | None:
    """One tool call (OpenAI's `{id, type, function: {name, arguments}}`, or flat `{id, name, arguments}`, a dict or
    an object) as a `MessageToolCall`: arguments as JSON text, never re-serialized when they arrived as text; None
    with neither a name nor an id. A call with an id and no name is kept (`name=""`): a call the framework's parser
    dropped (verl's hermes on invalid JSON), recorded failed rather than lost."""
    function = _get_field(item, "function") or item
    name = _get_field(function, "name")
    call_id = _get_field(item, "id")
    has_id = isinstance(call_id, str) and bool(call_id)
    if not isinstance(name, str) or not (name or has_id):
        return None
    arguments = _get_field(function, "arguments")
    if not isinstance(arguments, str):
        arguments = "" if arguments is None else json.dumps(arguments, ensure_ascii=False, default=str)
    call: dict[str, Any] = {"name": name[:MAX_NAME_CHARS], "arguments": arguments}
    if has_id:
        call["id"] = call_id[:MAX_NAME_CHARS]
    return call


def fit_trial_file(found: Mapping[str, Any]) -> dict:
    """A rollout's file as a `TrialFile` fits it: its path cut to 1,024 characters, its role to 64."""
    fitted = dict(found)
    if isinstance(fitted.get("path"), str):
        fitted["path"] = fitted["path"][:MAX_FILE_PATH_CHARS]
    if isinstance(fitted.get("role"), str):
        fitted["role"] = fitted["role"][:MAX_ROLE_CHARS]
    return fitted


def _fit_names(fields: dict, names: tuple[str, ...]) -> dict:
    for name in names:
        if isinstance(fields.get(name), str):
            fields[name] = fields[name][:MAX_NAME_CHARS]
    return fields


def _get_field(target: Any, name: str) -> Any:
    return target.get(name) if isinstance(target, Mapping) else getattr(target, name, None)


def scrub_part(part: dict, scrub) -> dict:
    """Logs, the error line and every turn's message text, reasoning, tool-call arguments and tool-run errors through
    the scrubber (``scrub``: str -> str), before anything is journaled: tool output can carry keys. The turns
    are copied first: the caller's own objects are never rewritten. A scrubbed tail is cut to
    4 KiB again (a redaction marker can be longer than the key it replaced)."""
    for name in ("log_text", "log_tail", "error_message"):
        if isinstance(part.get(name), str):
            part[name] = scrub(part[name])
    if isinstance(part.get("log_tail"), str):
        part["log_tail"] = cut_tail(part["log_tail"], MAX_LOG_TAIL_BYTES)[0]
    turns = part.get("turns")
    if isinstance(turns, list):
        part["turns"] = [_scrub_turn(turn, scrub) for turn in turns]
    return part


def _scrub_turn(turn: Any, scrub) -> Any:
    if not isinstance(turn, Mapping):
        return turn
    copied = dict(turn)
    messages = copied.get("messages")
    if isinstance(messages, list):
        copied["messages"] = [_scrub_message(message, scrub) for message in messages]
    runs = copied.get("tool_calls")
    if isinstance(runs, list):
        copied["tool_calls"] = [
            {**run, "error": " ".join(scrub(run["error"]).split())[:MAX_TOOL_ERROR_CHARS]}
            if isinstance(run, Mapping) and isinstance(run.get("error"), str)
            else run
            for run in runs
        ]
    return copied


def _scrub_message(message: Any, scrub) -> Any:
    """A message's content and reasoning through the scrubber, and each tool call's arguments by value."""
    if not isinstance(message, Mapping):
        return message
    copied = dict(message)
    for name in ("content", "reasoning"):
        if isinstance(copied.get(name), str):
            copied[name] = scrub(copied[name])
    calls = copied.get("tool_calls")
    if isinstance(calls, list):
        copied["tool_calls"] = [
            {**call, "arguments": scrub_arguments(call["arguments"], scrub)}
            if isinstance(call, Mapping) and isinstance(call.get("arguments"), str)
            else call
            for call in calls
        ]
    return copied


def scrub_arguments(text: str, scrub) -> str:
    """Tool-call arguments scrubbed by value, never by key (D6): JSON text has each string leaf and each key's own text
    scrubbed and is re-serialized only when one changed (else the bytes as sent); text that is not JSON is scrubbed
    whole. Scrubbing the JSON text itself would redact a harmless value under a key named `password`. Objects are
    parsed as their pairs, so a key that repeats is scrubbed in every copy (a dict keeps only the last, and the
    scrubber's own JSON pass reads it that way too)."""
    try:
        parsed = json.loads(text, object_pairs_hook=_Pairs)
    except (ValueError, TypeError, RecursionError):
        return scrub(text)
    if not isinstance(parsed, list):
        return scrub(text)
    scrubbed = _scrub_leaves(parsed, scrub)
    return text if scrubbed == parsed else _to_json_text(scrubbed)


class _Pairs(list):
    """A JSON object as its (key, value) pairs in order, a repeated key kept each time."""


def _scrub_leaves(value: Any, scrub) -> Any:
    if isinstance(value, str):
        return scrub(value)
    if isinstance(value, _Pairs):
        return _Pairs((scrub(key), _scrub_leaves(item, scrub)) for key, item in value)
    if isinstance(value, list):
        return [_scrub_leaves(item, scrub) for item in value]
    return value


def _to_json_text(value: Any) -> str:
    """`json.dumps` (its separators) that writes `_Pairs` as an object with every pair, repeats included."""
    if isinstance(value, _Pairs):
        return "{" + ", ".join(f"{json.dumps(key, ensure_ascii=False)}: {_to_json_text(item)}"
                               for key, item in value) + "}"  # fmt: skip
    if isinstance(value, list):
        return "[" + ", ".join(_to_json_text(item) for item in value) + "]"
    return json.dumps(value, ensure_ascii=False)


#: The turn fields an older server would drop with a 2xx (`samples_turn_capture`, D7), by where they sit.
TURN_CAPTURE_FIELDS = ("Sample.turns_source", "Message.tool_calls", "Message.reasoning", "TurnToolCall.id")
#: The plan's field an older server would drop the same way.
PLAN_CAPTURE_FIELD = "PlanIn.unsupported"
#: The server feature that stores them (D7).
TURN_CAPTURE_FEATURE = "samples_turn_capture"


def strip_turn_capture(part: dict) -> list[str]:
    """Take the fields an older server would drop silently off ``part`` (in place, on the part's own copies);
    the ones it held (`TURN_CAPTURE_FIELDS` names), so the caller can say what was not stored."""
    found: set[str] = set()
    if part.pop("turns_source", None) is not None:
        found.add("Sample.turns_source")
    turns = part.get("turns")
    if not isinstance(turns, list):
        return [name for name in TURN_CAPTURE_FIELDS if name in found]
    stripped = []
    for turn in turns:
        if not isinstance(turn, Mapping):
            stripped.append(turn)
            continue
        turn = dict(turn)
        messages = []
        for message in turn.get("messages") or ():
            if isinstance(message, Mapping):
                message = dict(message)
                if message.pop("tool_calls", None):
                    found.add("Message.tool_calls")
                if message.pop("reasoning", None) is not None:
                    found.add("Message.reasoning")
            messages.append(message)
        if "messages" in turn:
            turn["messages"] = messages
        calls = []
        for call in turn.get("tool_calls") or ():
            if isinstance(call, Mapping) and "id" in call:
                call = {key: value for key, value in call.items() if key != "id"}
                found.add("TurnToolCall.id")
            calls.append(call)
        if "tool_calls" in turn:
            turn["tool_calls"] = calls
        stripped.append(turn)
    part["turns"] = stripped
    return [name for name in TURN_CAPTURE_FIELDS if name in found]


#: Per base URL: (whether the server stores the turn capture fields, until when that answer holds). A drain builds
#: its clients per pass, so their own feature cache would ask on every pass.
_TURN_CAPTURE_KNOWN: dict[str, tuple[bool, float]] = {}
#: How long an answer holds; a failed ask is remembered (as "send them") for the shorter time.
_KNOWN_FOR_S = 600.0
_FAILED_ASK_FOR_S = 60.0
_WARNED_FIELDS: set[str] = set()
_WARNED_LOCK = threading.Lock()


def gate_turn_capture(client: Any, body: dict) -> dict:
    """At SEND time (D7): a `/samples/batch` body as ``client``'s server stores it. Without `samples_turn_capture`
    the fields it would drop with a 2xx come off a copy (the rest of each sample goes) and one warning per field names
    them. A body without them never asks; a failed ask sends them (the server deploys first) and asks again after 60 s.
    The drain (`OP_HANDLERS["samples_gate"]`) and a direct send call it; `log()` never asks the network. A server
    already known to store them gets ``body`` itself, never copied or walked (every send of a long drain)."""
    if get_known_turn_capture(client) is True:
        return body
    samples = body.get("samples")
    stripped: list = []
    names: set[str] = set()
    for part in samples if isinstance(samples, list) else ():
        if isinstance(part, Mapping):
            part = dict(part)
            names.update(strip_turn_capture(part))
        stripped.append(part)
    plan = body.get("plan")
    has_plan_field = isinstance(plan, Mapping) and "unsupported" in plan
    if has_plan_field:
        names.add(PLAN_CAPTURE_FIELD)
    if not names or is_turn_capture_stored(client):
        return body
    gated = {**body, "samples": stripped} if isinstance(samples, list) else dict(body)
    if has_plan_field:
        gated["plan"] = {key: value for key, value in plan.items() if key != "unsupported"}
    warn_turn_capture(names, was_sent=True)
    return gated


def is_turn_capture_stored(client: Any) -> bool:
    """Whether ``client``'s server stores the turn capture fields: its own feature cache, else this process's answer
    for its server, else asked once (`GET /v1/server/features`). A failed ask is "yes", remembered 60 s."""
    known = get_known_turn_capture(client)
    if known is not None:
        return known
    base = _get_base_url(client)
    try:
        answer = bool(client.supports_feature(TURN_CAPTURE_FEATURE))
        hold_for = _KNOWN_FOR_S
    except Exception:  # noqa: BLE001 -- cannot ask: send them, as `run_config_merge` does
        answer, hold_for = True, _FAILED_ASK_FOR_S
    if base:
        _TURN_CAPTURE_KNOWN[base] = (answer, time.monotonic() + hold_for)
    return answer


def get_known_turn_capture(client: Any) -> bool | None:
    """What this process already knows of ``client``'s server and `samples_turn_capture`, or None. Never asks."""
    cached = getattr(client, "_server_features_cache", None)
    if isinstance(cached, frozenset):
        return TURN_CAPTURE_FEATURE in cached
    known = _TURN_CAPTURE_KNOWN.get(_get_base_url(client))
    if known is not None and time.monotonic() < known[1]:
        return known[0]
    return None


def warn_turn_capture(names: set[str] | list[str], *, was_sent: bool) -> None:
    """Once per field and process: what an older server does not store (D7). ``was_sent``: they were taken off a body
    just sent; else `log()` saw a server known not to store them, and the send will take them off."""
    with _WARNED_LOCK:
        new = [name for name in (*TURN_CAPTURE_FIELDS, PLAN_CAPTURE_FIELD) if name in names and name not in _WARNED_FIELDS]
        _WARNED_FIELDS.update(new)
    if new:
        done = "they were left out of the samples sent" if was_sent else "they are left out when the samples are sent"
        _diagnostics.warn(
            f"probe: this Probe server does not store {', '.join(new)} yet (feature {TURN_CAPTURE_FEATURE}), so "
            f"{done}; the rest of each sample is stored. Upgrade the server to keep tool calls, reasoning and what a "
            "framework cannot capture."
        )


def _get_base_url(client: Any) -> str:
    return str(getattr(getattr(client, "settings", None), "base_url", "") or "")


def replace_nul_text(value: Any) -> Any:
    """Every string in ``value`` with NUL written as a literal `\\0`: the outbox refuses a whole op
    over one NUL (a model can emit one), which would cost every sample in it."""
    if isinstance(value, str):
        return value.replace(NUL, NUL_ESCAPE) if NUL in value else value
    if isinstance(value, Mapping):
        return {key: replace_nul_text(item) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_nul_text(item) for item in value]
    return value


def split_log(part: dict) -> str | None:
    """Take the full log off ``part`` (``log_text``, or ``log`` given as text): sets ``log_tail``
    when the caller set none and returns the log to bundle, capped at 1 MiB keeping the tail."""
    text = part.pop("log_text", None)
    if isinstance(part.get("log"), str):
        text = part.pop("log")
    if not isinstance(text, str) or not text:
        return None
    if "log_tail" not in part:
        part["log_tail"] = cut_tail(text, MAX_LOG_TAIL_BYTES)[0]
    return text


def cap_error_message(part: dict) -> None:
    """One line, at most 1,024 characters (the contract's cap)."""
    message = part.get("error_message")
    if isinstance(message, str):
        line = " ".join(message.split())
        part["error_message"] = line[:MAX_ERROR_MESSAGE_CHARS]


def get_default_seal_step(part: Mapping[str, Any]) -> int | None:
    """The step a part counts toward when the caller names none: its consuming step, else its
    scheduled step."""
    for name in ("consumed_step", "scheduled_step"):
        value = part.get(name)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def measure_bytes(value: Any) -> int:
    """The JSON size of ``value`` (what the batch caps count)."""
    return len(json.dumps(value, default=str))
