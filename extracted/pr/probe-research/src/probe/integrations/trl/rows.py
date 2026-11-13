"""What a TRL dataset row and a completion say about a sample (RL plan §3.2, §3.3c): the task key, scenario (its images
as file pointers) and label from the row, the prompt and response text, the turns of a tool-calling completion, and
per-token arrays made JSON-safe. Pure: no run, no network, nothing from TRL imported."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from collections import OrderedDict, deque
from collections.abc import Callable, Collection, Iterable, Mapping, MutableMapping, Sequence
from typing import Any, NamedTuple

from probe.generated.samples import CaptureField, TurnsSource
from probe.sdk.run.samples.rollout import REASONING_KEYS, to_tool_call

#: A dataset column naming the task; else the prompt's hash is the key (`prompt:<sha256[:16]>`).
TASK_COLUMN = "task_id"
#: A dataset column holding the task's scenario: an object of named values, or that object as JSON text.
SCENARIO_COLUMN = "scenario"
#: Dataset columns read as the task's reference answer, first found (GSM `answer`, math `solution`).
LABEL_COLUMNS = ("label", "answer", "solution", "ground_truth")
#: A scenario text value's cap (`records/samples/task.py`, `MAX_SCENARIO_TEXT_CHARS`).
MAX_SCENARIO_TEXT = 256
MAX_LABEL_BYTES = 4 * 1024
#: A part's caps (`records/samples/`): scenario keys, task key length, extras (16 KiB; half kept for the adapter's own).
MAX_SCENARIO_KEYS = 32
MAX_TASK_KEY_CHARS = 512
MAX_EXTRAS_BYTES = 8 * 1024
#: A scenario key the contract takes (`records/samples/task.py`, `SCENARIO_KEY`): no dots, no spaces.
SCENARIO_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_\-]{0,63}$")
#: Chat roles onto `MessageSource`; a `user` message inside a completion is the environment answering.
SOURCES = {"system": "system", "assistant": "model", "tool": "tool", "function": "tool", "user": "environment"}

#: The capture fields a trainer that runs no tools cannot fill (`plan(unsupported=)`).
TOOL_FIELDS = (CaptureField.TOOL_CALL_IDS, CaptureField.TOOL_CALL_ARGUMENTS, CaptureField.TOOL_RESULT_LINKS,
               CaptureField.ENVIRONMENT_FILES)

#: `extras` key: replies whose tool results could not be linked to their calls by TRL's order (a name differed).
UNLINKED_TOOL_TURNS = "unlinked_tool_turns"

#: Collated rows remembered for the recorder; past it the oldest go (GKD collates eval rows it never records).
MAX_COLLATED_ROWS = 4096
#: The batch key a dataloader worker's collated batch carries its rows' task columns under, to the main process
#: (GKD with `dataloader_num_workers > 0`); taken out before TRL reads the batch (`CollatedRows.remember_carried`).
CARRIED_ROWS_KEY = "_probe_rows"
#: A VLM dataset's image columns: one image, or a list (`grpo_trainer.py:2518-2523`).
IMAGE_COLUMN = "image"
IMAGES_COLUMN = "images"
#: Where an image sat in a prompt's text.
IMAGE_MARK = "<image>"

#: Dataset column names, or a callable ``(row) -> {name: value}``.
ScenarioSpec = Iterable[str] | Callable[[Mapping[str, Any]], Mapping[str, Any]] | None


def make_prompt_key(prompt: Any) -> str:
    """A task key from the prompt itself when the row names none: the same prompt, the same key."""
    canonical = json.dumps(prompt, sort_keys=True, default=_get_type_name, ensure_ascii=False)
    return "prompt:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def _get_type_name(value: Any) -> str:
    """A value JSON cannot hold (an image) by its type: its repr carries a memory address, never the same twice."""
    return type(value).__name__


def render_prompt(prompt: Any) -> str:
    """A prompt as text: a string as it is, one message's content alone, else one `role: content` block each."""
    if isinstance(prompt, str):
        return prompt
    messages = [message for message in prompt or () if isinstance(message, Mapping)]
    if len(messages) == 1:
        return get_text(messages[0].get("content"))
    return "\n\n".join(f"{message.get('role', '')}: {get_text(message.get('content'))}" for message in messages)


def get_text(content: Any) -> str:
    """A message's content as text: a list of typed parts keeps its text parts, and an image part reads `<image>`
    where it sat (`prepare_multimodal_messages`, `data_utils.py`)."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        pieces = []
        for part in content:
            if isinstance(part, Mapping) and part.get("text") is not None:
                pieces.append(str(part["text"]))
            elif isinstance(part, Mapping) and part.get("type") == "image":
                pieces.append(IMAGE_MARK)
        if pieces:
            return "\n".join(pieces)
    return json.dumps(content, default=_get_type_name, ensure_ascii=False)


def get_image_digest(image: Any) -> str | None:
    """An image's sha256: of its encoded bytes when it carries them (raw bytes, or a `datasets` image left undecoded,
    `{"bytes": ..., "path": ...}`), else of its decoded pixels (a PIL image: mode and size, then `tobytes()`). None
    for anything else (a path or a URL: nothing to hash here)."""
    if isinstance(image, Mapping):
        image = image.get("bytes")
    if isinstance(image, (bytes, bytearray)):
        return hashlib.sha256(image).hexdigest()
    mode, size, to_bytes = getattr(image, "mode", None), getattr(image, "size", None), getattr(image, "tobytes", None)
    if not (isinstance(mode, str) and isinstance(size, tuple) and len(size) == 2 and callable(to_bytes)):
        return None
    digest = hashlib.sha256(f"{mode}:{size[0]}x{size[1]}:".encode("utf-8"))
    digest.update(to_bytes())
    return digest.hexdigest()


class RowReader:
    """A dataset row's task facts: key, scenario (``scenario`` = column names or a callable), label."""

    def __init__(self, scenario: ScenarioSpec = None) -> None:
        self._scenario = scenario
        self._columns = () if scenario is None or callable(scenario) else tuple(str(name) for name in scenario)

    def get_columns(self, dataset: Any = None) -> list[str]:
        """The dataset columns `read_task` reads; a scenario callable may read any, so then all of ``dataset``'s."""
        if callable(self._scenario):
            return [str(name) for name in getattr(dataset, "column_names", None) or ()]
        return [TASK_COLUMN, SCENARIO_COLUMN, *LABEL_COLUMNS, IMAGE_COLUMN, IMAGES_COLUMN, *self._columns]

    def read_task(self, row: Mapping[str, Any] | None, prompt: Any) -> dict:
        """``{task_key, scenario[, label]}`` for one row; a missing row keys the task by its prompt. The row's images
        join the scenario as file pointers (`image`, `image_1`, ...: `{"sha256"}`), so one question asked of two
        images is two tasks, and one image is the same task in every run."""
        row = row if isinstance(row, Mapping) else {}
        named = row.get(TASK_COLUMN)
        key = str(named) if isinstance(named, (str, int)) and str(named) else make_prompt_key(prompt)
        if len(key) > MAX_TASK_KEY_CHARS:  # the contract refuses a longer key: keep it unique, not cut
            key = "task:" + hashlib.sha256(key.encode("utf-8")).hexdigest()
        task: dict[str, Any] = {"task_key": key, "scenario": self._get_scenario(row, prompt)}
        label = _get_label(row)
        if label is not None:
            task["label"] = label
        return task

    def _get_scenario(self, row: Mapping[str, Any], prompt: Any = None) -> dict:
        """Scenario-shaped values only: one list in a column would otherwise refuse the whole sample."""
        if callable(self._scenario):
            values = dict(self._scenario(row) or {})
        else:
            values = _parse_scenario(row.get(SCENARIO_COLUMN))
            values.update({name: row[name] for name in self._columns if name in row})
        for index, digest in enumerate(self._get_image_digests(row, prompt)):
            values.setdefault(IMAGE_COLUMN if index == 0 else f"{IMAGE_COLUMN}_{index}", {"sha256": digest})
        kept = {str(name): value for name, value in values.items()
                if SCENARIO_KEY.match(str(name)) and _is_scenario_value(value)}
        return dict(list(kept.items())[:MAX_SCENARIO_KEYS])  # more would refuse the whole sample

    def _get_image_digests(self, row: Mapping[str, Any], prompt: Any) -> list[str]:
        """The row's images' digests, in order: its image columns, else the image parts of its prompt."""
        images = row.get(IMAGES_COLUMN)
        images = list(images) if isinstance(images, (list, tuple)) else []
        if not images and row.get(IMAGE_COLUMN) is not None:
            images = [row[IMAGE_COLUMN]]
        if not images and isinstance(prompt, list):
            images = [part.get("image") for message in prompt if isinstance(message, Mapping)
                      for part in (message.get("content") if isinstance(message.get("content"), list) else ())
                      if isinstance(part, Mapping) and part.get("type") == "image" and part.get("image") is not None]
        return [digest for digest in (get_image_digest(image) for image in images) if digest]


def has_response_schema(tokenizer: Any) -> bool:
    """Whether TRL can parse a completion's tool calls and reasoning with this tokenizer (`parse_response` needs a
    `response_template` or the older `response_schema`); without one it decodes plain text."""
    return any(getattr(tokenizer, name, None) is not None for name in ("response_template", "response_schema"))


class ToolDispatch(NamedTuple):
    """How TRL's tool loop runs one parsed call (`grpo_trainer.py:2064-2083`): the call's id, the names its result may
    carry, and whether TRL hands it to an async tool (deferred to the gather: only those take an async position)."""

    id: str
    names: frozenset[str | None]
    is_deferred: bool


def build_completion(completion: Any, *, async_tools: Iterable[str] | None = (),
                     failed_async_calls: Iterable[int] | None = None) -> dict:
    """The response text, plus turns and the tool-call count when the completion is a tool-calling conversation
    (more than one message, or a reply with tool calls or reasoning): each message keeps its source, whether the
    trainer learns from it, its tool calls (id, name, arguments as JSON text) and its reasoning. TRL's parser names no
    call id, so each is `probe-<turn>-<i>`, and its result is linked by TRL's own order (`link_tool_results`);
    ``async_tools`` are the names TRL ran as coroutines (None: unknown), ``failed_async_calls`` the positions, among
    the calls TRL handed to them (in call order, over the whole completion), of those that raised when called (sync
    GRPO only; None: not watched, so a reply holding such a call links nothing)."""
    if isinstance(completion, str):
        return {"response": completion}
    messages = [message for message in completion or () if isinstance(message, Mapping)]
    replies = [get_text(message.get("content")) for message in messages if message.get("role") == "assistant"]
    built: dict[str, Any] = {"response": replies[-1] if replies else render_prompt(messages)}
    if len(messages) <= 1 and not any(message.get("tool_calls") or _get_reasoning(message) for message in messages):
        return built
    turns: list[dict] = []
    current: list[dict] = []
    calls: list[dict] = []
    asked: list[ToolDispatch] = []  # the last reply's calls as TRL runs them, waiting for their results
    results: list[dict] = []
    mismatched = 0
    asynchronous = None if async_tools is None else frozenset(async_tools)
    failed = None if asynchronous is None or failed_async_calls is None else frozenset(failed_async_calls)
    async_position = 0  # the first of this reply's async calls, among the completion's
    for message in messages:
        role = str(message.get("role") or "assistant")
        if role != "tool" and results:
            mismatched += not link_tool_results(asked, results, failed, async_position)
            async_position += sum(call.is_deferred for call in asked)
            asked, results = [], []
        built_message = {
            "role": role[:64],
            "source": SOURCES.get(role, "environment"),
            "is_trainable": role == "assistant",
            "content": get_text(message.get("content")),
            **({"name": str(message["name"])[:256]} if message.get("name") else {}),
            **({"tool_call_id": str(message["tool_call_id"])[:256]} if message.get("tool_call_id") else {}),
        }
        reasoning = _get_reasoning(message)
        if reasoning is not None:
            built_message["reasoning"] = reasoning
        if role == "tool":
            results.append(built_message)
        current.append(built_message)
        raw_calls = list(message.get("tool_calls") or ())
        message_calls = [_to_tool_call(call, len(turns), index) for index, call in enumerate(raw_calls)]
        if message_calls:
            built_message["tool_calls"] = message_calls
        calls.extend({"id": call["id"], "name": call["name"]} for call in message_calls)
        if role == "assistant":  # one turn per model reply, holding what came since the last one
            turns.append({"messages": current, "tool_calls": calls})
            current, calls = [], []
            asked = [_read_dispatch(raw, call, asynchronous) for raw, call in zip(raw_calls, message_calls)]
    if results:
        mismatched += not link_tool_results(asked, results, failed, async_position)
    if current:
        turns.append({"messages": current, "tool_calls": calls})
    built["turns"] = turns
    built["turns_source"] = TurnsSource.AS_SENT
    built["turn_count"] = len(turns)
    built["tool_call_count"] = sum(len(turn["tool_calls"]) for turn in turns)
    if mismatched:
        built["extras"] = {UNLINKED_TOOL_TURNS: mismatched}
    return built


def link_tool_results(calls: Sequence[ToolDispatch], results: list[dict],
                      failed_async_calls: Collection[int] | None = None, first_async: int = 0) -> bool:
    """Set each tool result's `tool_call_id` from TRL's own order (O1): within a reply, the results of the calls run
    or failed at once come first, then the deferred calls' (`grpo_trainer.py:2064-2112`), each in call order
    (AsyncGRPO awaits every call in order: none is deferred). A deferred call that raised when called (its position,
    counted from ``first_async``, in ``failed_async_calls``) is a failed one; with ``failed_async_calls`` None (not
    watched) a reply holding a deferred call links nothing. Checked by name: when the count or any name differs,
    nothing in this reply is linked and it returns False, so the caller counts it (a wrong link is worse than none)."""
    if any(result.get("tool_call_id") for result in results):
        return True  # the framework linked them itself (a custom rollout): as sent
    if failed_async_calls is None and any(call.is_deferred for call in calls):
        return False
    expected: list[ToolDispatch] = []
    gathered: list[ToolDispatch] = []
    position = first_async
    for call in calls:
        if call.is_deferred:
            position += 1
            if position - 1 not in (failed_async_calls or ()):
                gathered.append(call)
                continue
        expected.append(call)
    expected += gathered
    if len(expected) != len(results) or any(result.get("name") not in call.names
                                            for call, result in zip(expected, results)):  # fmt: skip
        return False
    for call, result in zip(expected, results):
        result["tool_call_id"] = call.id
    return True


def to_numbers(values: Any) -> list[float | None]:
    """A tensor row, array or list as JSON-safe floats: a NaN or infinite value (vLLM's missing logprob, -inf
    padding) is None."""
    if values is None:
        return []
    listed = values.tolist() if hasattr(values, "tolist") else list(values)
    return [_to_finite(value) for value in listed]


def to_ints(values: Any) -> list[int]:
    if values is None:
        return []
    listed = values.tolist() if hasattr(values, "tolist") else list(values)
    return [int(value) for value in listed]


def to_finite(value: Any) -> float | None:
    """A number, or None for anything else (NaN, a tensor that is not one value, text)."""
    if hasattr(value, "item"):
        try:
            value = value.item()
        except (TypeError, ValueError, RuntimeError):
            return None
    return _to_finite(value)


def split_extras(values: Mapping[str, Any]) -> tuple[dict[str, float], dict[str, Any]]:
    """Reward-function extras: numbers as metrics, short text and booleans as extras (up to `MAX_EXTRAS_BYTES`:
    more would refuse the whole sample), the rest dropped."""
    numbers: dict[str, float] = {}
    others: dict[str, Any] = {}
    size = 0
    for name, value in values.items():
        if isinstance(value, bool) or (isinstance(value, str) and len(value) <= MAX_SCENARIO_TEXT):
            size += len(json.dumps({str(name): value}).encode("utf-8"))
            if size <= MAX_EXTRAS_BYTES:
                others[str(name)] = value
            continue
        number = to_finite(value)
        if number is not None:
            numbers[str(name)] = number
    return numbers, others


def _to_tool_call(call: Any, turn: int, index: int) -> dict:
    """One assistant tool call as a `MessageToolCall`: TRL's parsed arguments (a dict) as JSON text, the id TRL's
    parser never gives numbered `probe-<turn>-<i>`; a call with no name reads `tool` (TRL runs it as unknown)."""
    found = to_tool_call(call) if isinstance(call, Mapping) else None
    if found is None:
        found = {"name": "tool", "arguments": ""}
    found["name"] = str(found["name"])[:256]
    found.setdefault("id", f"probe-{turn}-{index}")
    return found


def _read_dispatch(raw: Any, call: Mapping[str, Any], async_tools: Collection[str] | None) -> ToolDispatch:
    """TRL calls a tool only for a `function` call, as `tool(**arguments)` (`:2066-2072`): any other type, or arguments
    that are not a str-keyed mapping, fail before the tool, with the results filed at once. ``async_tools`` None
    (unknown) counts every callable call as possibly deferred."""
    raw = raw if isinstance(raw, Mapping) else {}
    function = raw.get("function")
    if raw.get("type") != "function" or not isinstance(function, Mapping):
        # GRPO and Distillation name this result `tool_call.get("name", "unknown")` (`:2082`); AsyncGRPO the function's
        return ToolDispatch(call["id"], frozenset({call["name"], _to_result_name(raw.get("name", "unknown"))}), False)
    arguments = function.get("arguments")
    is_callable = isinstance(arguments, Mapping) and all(isinstance(key, str) for key in arguments)
    is_deferred = is_callable and (async_tools is None or function.get("name") in async_tools)
    return ToolDispatch(call["id"], frozenset({call["name"]}), is_deferred)


def _to_result_name(name: Any) -> str | None:
    """A name as a tool result message keeps it (`build_completion`): text cut to 256 characters, None when empty."""
    return str(name)[:256] if name else None


def _get_reasoning(message: Mapping[str, Any]) -> str | None:
    """The reasoning a tokenizer's response schema parsed apart from the content (`reasoning_content` / `thinking`),
    never found in the text itself (D4)."""
    return next((value for key in REASONING_KEYS if isinstance(value := message.get(key), str) and value), None)


def _parse_scenario(value: Any) -> dict:
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, str) and value.startswith("{"):
        try:
            parsed = json.loads(value)
        except ValueError:
            return {}
        return parsed if isinstance(parsed, dict) else {}
    return {}


def _get_label(row: Mapping[str, Any]) -> Any:
    for name in LABEL_COLUMNS:
        value = row.get(name)
        if value is None:
            continue
        try:
            text = json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError):
            continue
        return value if len(text.encode("utf-8")) <= MAX_LABEL_BYTES else None
    return None


def _is_scenario_value(value: Any) -> bool:
    if isinstance(value, (bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, str):
        return len(value) <= MAX_SCENARIO_TEXT
    return isinstance(value, Mapping) and set(value) in ({"time"}, {"sha256"}, {"sha256", "uri"})


def _to_finite(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


#: `labels` mark a collated row's prompt and padding with this, so only its completion is trained on (the ChatML
#: collator; `gkd_trainer.py:394-401`, `gold_trainer.py:1819-1836`).
IGNORED_LABEL = -100


#: An SFT eval example's key prefix: its own sample, apart from the same tokens trained on (`sft:`).
SFT_EVAL_PREFIX = "sft-eval:"


def make_sft_key(ids: Sequence[int], *, is_eval: bool = False) -> str:
    """An SFT example's sample key: the digest of its unpadded token ids (the SFT recorder and the loss hook agree);
    an eval example's under its own prefix."""
    digest = hashlib.sha256(",".join(str(token) for token in ids).encode("ascii")).hexdigest()[:32]
    return f"{SFT_EVAL_PREFIX if is_eval else 'sft:'}{digest}"


def get_segment_starts(batch: Mapping[str, Any]) -> list[int] | None:
    """Where each example starts in a padding-free (or packed) SFT row (`cu_seq_lens_q` without its end, host ints),
    or None for an unpacked batch (it has an `attention_mask`). The collator puts every example of a micro-batch in
    one row and restarts `position_ids` at each (`sft_trainer.py:197-216`)."""
    bounds = batch.get("cu_seq_lens_q")
    if "attention_mask" in batch or bounds is None:
        return None
    return [int(start) for start in to_ints(bounds)[:-1]]


def read_labeled_rows(batch: Mapping[str, Any]) -> list[tuple[list[int], list[int]]]:
    """Each row of a collated distillation batch as (prompt ids, completion ids): the prompt from `prompts` under
    `prompt_attention_mask`, the completion from `input_ids` where `labels` keep the token (all of it unlabelled)."""
    prompts, prompt_masks, labels = batch.get("prompts"), batch.get("prompt_attention_mask"), batch.get("labels")
    rows = []
    for row in range(len(batch["input_ids"])):
        ids = to_ints(batch["input_ids"][row])
        marks = to_ints(labels[row]) if labels is not None else [0] * len(ids)
        completion = [token for token, mark in zip(ids, marks) if mark != IGNORED_LABEL]
        prompt: list[int] = []
        if prompts is not None and prompt_masks is not None and row < len(prompts):
            prompt = [token for token, kept in zip(to_ints(prompts[row]), to_ints(prompt_masks[row])) if kept]
        rows.append((prompt, completion))
    return rows


class CollatedRows:
    """The dataset rows behind a collated distillation batch, by each row's prompt token ids, until its micro-batch is
    recorded: GKD and GOLD train on what `DataCollatorForChatML` makes, token ids only
    (`trl/experimental/utils.py:289-420`), so a row's task, scenario and label are gone by then. A row collated in a
    dataloader worker process (`dataloader_num_workers > 0`) reaches here only when its batch carried it
    (`CARRIED_ROWS_KEY`, GKD); else it keeps the prompt as its task."""

    def __init__(self, limit: int = MAX_COLLATED_ROWS) -> None:
        self._rows: OrderedDict[tuple[int, ...], deque] = OrderedDict()
        self._count = 0
        self._limit = limit

    def wrap(self, collate: Callable[[Any], Any], carried_columns: Sequence[str] | None = None) -> RememberingCollator:
        """``collate`` remembering each batch's rows; it never fails over Probe. With ``carried_columns``, a batch
        collated in a dataloader worker carries those columns of its rows to the main process."""
        return RememberingCollator(collate, self, carried_columns)

    def remember_carried(self, batch: Any) -> None:
        """A worker-collated batch's carried rows, taken out of the batch (TRL never sees the key) and remembered."""
        if isinstance(batch, MutableMapping):
            carried = batch.pop(CARRIED_ROWS_KEY, None)
            if carried is not None:
                self.remember(carried, batch)

    def __getstate__(self) -> dict:
        """A copy for a dataloader worker process remembers nothing: the recorder never reads it there."""
        return {"_rows": OrderedDict(), "_count": 0, "_limit": self._limit}

    def remember(self, examples: Any, batch: Any) -> None:
        if not isinstance(batch, Mapping) or batch.get("prompts") is None or not isinstance(examples, Sequence):
            return
        for example, (prompt, _completion) in zip(examples, read_labeled_rows(batch)):
            if isinstance(example, Mapping) and prompt:
                key = tuple(prompt)
                self._rows.setdefault(key, deque()).append(example)
                self._rows.move_to_end(key)
                self._count += 1
        while self._count > self._limit:
            key, rows = next(iter(self._rows.items()))
            rows.popleft()
            self._count -= 1
            if not rows:
                del self._rows[key]

    def get_rows(self, prompts: Sequence[Sequence[int]]) -> list[Mapping[str, Any] | None]:
        """The rows `take` would hand out for these prompts, in order, none of them taken (a live start reads a
        batch's tasks before its record takes them)."""
        seen: dict[tuple[int, ...], int] = {}
        found: list[Mapping[str, Any] | None] = []
        for prompt in prompts:
            key = tuple(prompt)
            rows = self._rows.get(key) or ()
            index = seen.get(key, 0)
            seen[key] = index + 1
            found.append(rows[index] if index < len(rows) else None)
        return found

    def take(self, prompt: Sequence[int]) -> Mapping[str, Any] | None:
        """The oldest remembered row with these prompt ids (a prompt seen twice is two rows, in collation order)."""
        key = tuple(prompt)
        rows = self._rows.get(key)
        if not rows:
            return None
        self._count -= 1
        row = rows.popleft()
        if not rows:
            del self._rows[key]
        return row


class RememberingCollator:
    """A collator that hands each batch's rows to `CollatedRows` as well. A class, not a closure: a dataloader that
    starts its workers by spawning (macOS's default) pickles its `collate_fn`. In a dataloader worker (another
    process than the one that wrapped it, forked or spawned) the rows cannot reach the recorder's `CollatedRows`, so
    with ``carried_columns`` the batch carries them: the worker sends the batch to the main process whole."""

    def __init__(self, collate: Callable[[Any], Any], rows: CollatedRows,
                 carried_columns: Sequence[str] | None = None) -> None:
        self.collate = collate
        self.rows = rows
        self.carried_columns = tuple(carried_columns) if carried_columns is not None else None
        self.owner_pid = os.getpid()

    def __call__(self, examples: Any) -> Any:
        batch = self.collate(examples)
        try:
            if self.carried_columns is not None and os.getpid() != self.owner_pid and isinstance(batch, MutableMapping):
                batch[CARRIED_ROWS_KEY] = [
                    {name: example[name] for name in self.carried_columns if name in example}
                    if isinstance(example, Mapping) else None for example in examples]
            else:
                self.rows.remember(examples, batch)
        except Exception:  # noqa: BLE001 -- a row Probe cannot read keeps the prompt as its task
            pass
        return batch


def pick_rows(values: Sequence[Any] | None, count: int) -> list[Any]:
    """The last ``count`` entries of a TRL log deque (what one call just appended), as a list."""
    if values is None or count <= 0:
        return []
    listed = list(values)
    return listed[-count:] if len(listed) >= count else listed
