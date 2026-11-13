"""One verl response as sample parts (RL plan §6.5): `VerlRow` is what the batch readers (`readers.py`) pull out of a
training or validation batch, and `RowMapper` turns rows into a generator part (the attempt) and, for training rows,
a trainer part (what the step consumed). Pure: no verl import. Line refs are `verl-project/verl@b17218ba58a6`."""

from __future__ import annotations

import hashlib
import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples import FinishReason, SampleErrorReason, TurnsSource
from probe.sdk.run.samples.rollout import RolloutCapture

from .tool_loop import FINISH_FIELD

#: Dataset `extra_info` keys (`utils/dataset/rl_dataset.py:400-410`) naming the task and its scenario.
TASK_KEY_FIELD = "task_id"
SCENARIO_FIELD = "scenario"
#: A scenario text value's cap (`records/samples/task.py`, `MAX_SCENARIO_TEXT_CHARS`).
MAX_SCENARIO_TEXT = 256
#: verl's per-token arrays onto Probe's (`sdk/run/samples/tokens.py`): the rollout's on the generator part, the
#: trainer's on the trainer part.
INFERENCE_ARRAYS = {"rollout_log_probs": "inference_logprobs"}
TRAINER_ARRAYS = {
    "old_log_probs": "trainer_logprobs",
    "ref_log_prob": "ref_logprobs",
    "entropys": "entropy",
    "advantages": "advantages",
    "returns": "returns",
}
#: Small `extra_info` values kept on the sample (verl's GSM8K preprocessing writes `index`, `split`, `answer`).
MAX_EXTRA_TEXT = 256
#: The agent loop whose non-model tokens are tool replies (`experimental/agent_loop/tool_agent_loop.py:101`); any
#: other loop's are an environment's (an interaction's user turns).
TOOL_AGENT = "tool_agent"
#: A chat role's source (`records/samples/turns.py` `MessageSource`).
ROLE_SOURCES = {"system": "system", "user": "user", "assistant": "model", "tool": "tool"}
#: Rows of a step critic warmup trains the critic on and not the actor (`ray_trainer.py:1684`,
#: `v1/trainer_base.py:608`): generated, never consumed.
CRITIC_WARMUP_DROP = "filter:critic_warmup"
#: The engine's stop reason (`TokenOutput.stop_reason`, `workers/rollout/replica.py:41`) as a finish reason, with the
#: error it means. vLLM answers `completed` for both stop and length, `aborted`, or its own reason as it is
#: (`vllm_async_server.py:800-807`); SGLang its `finish_reason.type` (`stop`, `length`, `abort`,
#: `async_sglang_server.py:667-668`, `:729`); TensorRT-LLM `aborted` (`trtllm_async_server.py:371-375`); verl's server
#: client `length` when the token budget ran out (`llm_server.py:351`) and retries `aborted` / `abort` (`:360`); the
#: legacy rollout's `tool_calls` (`schemas.py:41-43`). `completed` keeps the length rule, and the length rule beats an
#: engine `stop` / `tool_calls`: a model turn gets a fresh `response_length` budget each call (`llm_server.py:255-271`)
#: and can stop (`stop`) with the running total past it; the tool loop then ends (`tool_agent_loop.py:292`) and slices
#: the output (`:197`), and verl's `response_length/clip_ratio` counts it cut off.
#: Anything else is `other` with its text in `extras.stop_reason`.
_STOP, _LENGTH = FinishReason.STOP.value, FinishReason.LENGTH.value
_ABORTED = (FinishReason.ABORT.value, SampleErrorReason.ENGINE_ABORT.value)
STOP_REASONS: dict[str, tuple[str | None, str | None]] = {
    "completed": (None, None),
    "stop": (_STOP, None),
    "tool_calls": (_STOP, None),
    "length": (_LENGTH, None),
    "abort": _ABORTED,
    "aborted": _ABORTED,
    "cancelled": _ABORTED,
    "error": (FinishReason.ERROR.value, SampleErrorReason.UNKNOWN.value),
}
UNKNOWN_FINISH = FinishReason.OTHER.value
#: What a loop's last output carries to its sample: every loop's engine stop reason, in `extra_fields` (each key a
#: column of the legacy batch, `agent_loop.py:1203-1217`; V1 keeps the dict, `v1/agent_loop_tq.py:189`), and a
#: validation loop's live key and stop reason in `reward_extra_info` too (what verl's `_validate` hands its metrics,
#: `ray_trainer.py:678-686`, `v1/trainer_base.py:1131-1145`; text, so its metrics skip them, `metric_utils.py:1006`).
LIVE_KEY_FIELD = "probe_live_key"
STOP_REASON_FIELD = "probe_stop_reason"


class Split:
    TRAIN = "train"
    EVAL = "eval"


@dataclass
class VerlRow:
    """One response: its group (`uid`), its place in the group, the token ids (or the text verl already decoded),
    the grade, the dataset row's `extra_info`, the weight versions it was generated under and its per-token arrays
    (verl's names, `INFERENCE_ARRAYS` / `TRAINER_ARRAYS`)."""

    uid: str
    index: str
    prompt_ids: list[int] = field(default_factory=list)
    response_ids: list[int] = field(default_factory=list)
    prompt_text: str | None = None
    response_text: str | None = None
    score: float | None = None
    reward_parts: dict[str, float] = field(default_factory=dict)
    extra_info: Mapping[str, Any] | None = None
    data_source: str | None = None
    ground_truth: Any = None
    turn_count: int | None = None
    min_version: int | None = None
    max_version: int | None = None
    scheduled_step: int | None = None
    segment: int | None = None
    segment_count: int | None = None
    response_mask: list[int] | None = None
    arrays: dict[str, list[float]] = field(default_factory=dict)
    #: The dataset's chat messages (the agent loop's `raw_prompt`, `agent_loop.py:818`) and the loop's name.
    raw_prompt: list[Mapping[str, Any]] | None = None
    agent_name: str | None = None
    #: The agent loop it came from, for its live sample's key (`live.make_live_key`): its V1 `rollout.n` session
    #: (the TransferQueue key's middle part), else its row in the legacy generation batch (`priority`).
    session: str | None = None
    position: int | None = None
    #: The loop's last model call's stop reason (`STOP_REASONS`), and a validation row's live key as the loop carried it.
    stop_reason: str | None = None
    attempt_key: str | None = None
    #: The agent loop's capture as it carried it (`tool_loop`: `RolloutCapture.export` and the finish it saw): the
    #: messages as sent, `turns_source` and `environment`; None when the loop recorded none (decoded turns instead).
    rollout: Mapping[str, Any] | None = None

    def get_loss_mask(self) -> list[int] | None:
        """1 for a model token, 0 for a tool or environment token (verl's `response_mask`), cut to the response."""
        mask = self.response_mask
        if not isinstance(mask, list) or not self.response_ids or len(mask) < len(self.response_ids):
            return None
        return [int(bit) for bit in mask[: len(self.response_ids)]]


class RowMapper:
    """VerlRows -> `SamplePartIn`-shaped parts. ``decode`` turns token ids into text (verl's own dump decodes with
    `skip_special_tokens=True`, `ray_trainer.py:525-526`), ``tokens_to_text`` into one string per token; either may
    be None. ``max_response_length`` tells a cut-off response (`length`) from a finished one."""

    def __init__(
        self,
        *,
        decode: Callable[[list[int]], str] | None = None,
        tokens_to_text: Callable[[list[int]], list[str]] | None = None,
        max_response_length: int | None = None,
        host: str | None = None,
        worker: str | None = None,
    ) -> None:
        self._decode = decode
        self._tokens_to_text = tokens_to_text
        self._max_response_length = max_response_length
        self._where = {name: value for name, value in (("host", host), ("worker", worker)) if value}

    def map_train(self, rows: Sequence[VerlRow], step: int) -> list[dict]:
        """Rows the optimizer step ``step`` is about to train on: each a generator part and a trainer part consumed
        at ``step`` on the weights of the step before (version ``step - 1``)."""
        parts: list[dict] = []
        for row in rows:
            key = make_sample_key(Split.TRAIN, step, row)
            generator = self._map_attempt(row, key, Split.TRAIN, step, fallback_version=max(step - 1, 0))
            if row.scheduled_step is not None:
                generator["scheduled_step"] = row.scheduled_step
            _link_live_sample(generator, row, step)
            trainer: dict[str, Any] = {
                "key": key, "role": "trainer", "consumed_step": step, "consumed_version": max(step - 1, 0),
            }
            arrays = _pick_arrays(row.arrays, TRAINER_ARRAYS, len(row.response_ids))
            mask = row.get_loss_mask()
            if arrays:
                if mask is not None:
                    arrays["loss_mask"] = mask
                trainer["trainer_token_arrays"] = arrays
            parts += [generator, trainer]
        return parts

    def map_dropped(self, rows: Sequence[VerlRow], step: int, reason: str) -> list[dict]:
        """Rows ``step`` generated and never trained the actor on (``reason``, a `DropReason`): a generator part and
        a trainer part that drops it, so the seal counts it."""
        parts: list[dict] = []
        for row in rows:
            key = make_sample_key(Split.TRAIN, step, row)
            generator = self._map_attempt(row, key, Split.TRAIN, step, fallback_version=max(step - 1, 0))
            if row.scheduled_step is not None:
                generator["scheduled_step"] = row.scheduled_step
            _link_live_sample(generator, row, step)
            parts += [generator, {"key": key, "role": "trainer", "drop_reason": reason}]
        return parts

    def map_eval(self, rows: Sequence[VerlRow], step: int) -> list[dict]:
        """A validation pass at ``step``: generator parts only, generated by the weights of ``step``, scheduled at
        ``step`` (an eval part is never consumed, so this is the step it reads at, as TRL's, `trl/recorders/grpo.py`)."""
        parts = []
        for row in rows:
            part = self._map_attempt(row, make_sample_key(Split.EVAL, step, row), Split.EVAL, step,
                                     fallback_version=step)
            part["scheduled_step"] = step
            if row.attempt_key:
                part["attempt_key"] = row.attempt_key
            else:
                _link_live_sample(part, row, step, split=Split.EVAL)
            parts.append(part)
        return parts

    # -- inside ------------------------------------------------------------------------------------------
    def _map_attempt(self, row: VerlRow, key: str, split: str, step: int, *, fallback_version: int) -> dict:
        prompt = row.prompt_text if row.prompt_text is not None else self._decode_text(row.prompt_ids)
        response = row.response_text if row.response_text is not None else self._decode_text(row.response_ids)
        extra = row.extra_info if isinstance(row.extra_info, Mapping) else {}
        task_key = extra.get(TASK_KEY_FIELD)
        part: dict[str, Any] = {
            "key": key,
            "role": "generator",
            "split": split,
            "group_key": f"{split}:{step}:{row.uid}",
            "task_key": str(task_key) if isinstance(task_key, (str, int)) and str(task_key) else make_prompt_key(prompt),
            "scenario": get_scenario(extra),
            "prompt": prompt,
            "response": response,
            "generated_by": make_policy_pieces(row.min_version, row.max_version, fallback=fallback_version),
            **self._where,
        }
        if row.ground_truth is not None:
            part["label"] = row.ground_truth
        if row.response_ids:
            part["response_tokens"] = len(row.response_ids)
        finish, error, unknown = get_finish(row.stop_reason)
        if finish in (None, _STOP) and row.response_ids:
            finish = self._get_finish_reason(len(row.response_ids)) or finish
        if finish is not None:
            part["finish_reason"] = finish
        if error is not None:
            part["error_reason"] = error
        if row.prompt_ids:
            part["prompt_tokens"] = len(row.prompt_ids)
        if row.score is not None:
            part["reward"] = row.score
        if row.reward_parts:
            part["reward_parts"] = dict(row.reward_parts)
        if row.turn_count is not None:
            part["turn_count"] = row.turn_count
        rollout = row.rollout if isinstance(row.rollout, Mapping) else None
        if not (rollout and (rollout.get("turns") or rollout.get("turns_blob"))):
            turns = self._build_turns(row)
            if turns:
                part["turns"] = turns
                part["turns_source"] = TurnsSource.DECODED.value
        if rollout and rollout.get(FINISH_FIELD) == _LENGTH and part.get("finish_reason") in (None, _STOP, UNKNOWN_FINISH):
            part["finish_reason"] = _LENGTH  # F4: the loop ran past `response_length`; the engine said `completed`
        if row.segment_count is not None and row.segment_count > 1:
            part["segment"], part["segment_count"] = row.segment, row.segment_count
        extras = get_extras(extra, row.data_source)
        if unknown is not None:
            extras["stop_reason"] = unknown
        if extras:
            part["extras"] = extras
        arrays = self._get_inference_arrays(row)
        if arrays:
            part["token_arrays"] = arrays
        if rollout:  # the messages as sent, `turns_source`, `environment`; its `extras` merged into the part's
            RolloutCapture.update_part(part, rollout)
        return part

    def _get_inference_arrays(self, row: VerlRow) -> dict | None:
        if not row.response_ids:
            return None
        arrays: dict[str, list] = {"token_ids": list(row.response_ids)}
        if self._tokens_to_text is not None:
            arrays["token_text"] = [str(text) for text in self._tokens_to_text(list(row.response_ids))]
        arrays.update(_pick_arrays(row.arrays, INFERENCE_ARRAYS, len(row.response_ids)))
        mask = row.get_loss_mask()
        if mask is not None:
            arrays["loss_mask"] = mask
        return arrays

    def _build_turns(self, row: VerlRow) -> list[dict]:
        """The fallback when the loop captured no messages (another agent loop class, a worker that could not join),
        marked `turns_source=decoded`: a multi-turn response as its messages: the dataset's prompt messages, then each run of model tokens
        (`response_mask` 1) and of tool or environment tokens (0) decoded alone, one turn per model reply. A response
        with no 0 run is single-turn: no turns."""
        mask = row.get_loss_mask()
        if self._decode is None or not mask or 0 not in mask or 1 not in mask:
            return []
        other_role, other_source = ("tool", "tool") if row.agent_name == TOOL_AGENT else ("user", "environment")
        messages = [_to_message(message) for message in row.raw_prompt or () if isinstance(message, Mapping)]
        turns: list[dict] = []
        for is_model, ids in _split_runs(row.response_ids, mask):
            content = self._decode_text(ids)
            if is_model:
                messages.append({"role": "assistant", "source": "model", "is_trainable": True, "content": content})
                turns.append({"messages": messages})
                messages = []
            else:
                messages.append({"role": other_role, "source": other_source, "content": content})
        if messages:
            turns.append({"messages": messages})
        return turns

    def _get_finish_reason(self, length: int) -> str | None:
        """`length` when the response filled `data.max_response_length` (verl's own clip ratio,
        `trainer/ppo/metric_utils.py`), else `stop`; unknown without the limit."""
        if not self._max_response_length:
            return None
        return _LENGTH if length >= self._max_response_length else _STOP

    def _decode_text(self, ids: Sequence[int]) -> str:
        if self._decode is None or not ids:
            return ""
        return str(self._decode(list(ids)))


def make_sample_key(split: str, step: int, row: VerlRow) -> str:
    """`{split}:{step}:{uid}:{index}` (RL plan §3.5). verl draws a fresh uid per prompt per call
    (`ray_trainer.py:1482`, `v1/trainer_base.py:1050`), so two passes at one step never collide."""
    return f"{split}:{step}:{row.uid}:{row.index}"


def get_finish(stop_reason: str | None) -> tuple[str | None, str | None, str | None]:
    """(finish reason, error reason, the text of a reason not in `STOP_REASONS`) for an engine stop reason."""
    if not stop_reason:
        return None, None, None
    known = STOP_REASONS.get(stop_reason.strip().lower())
    if known is None:
        return UNKNOWN_FINISH, None, stop_reason[:MAX_EXTRA_TEXT]
    return known[0], known[1], None


def _link_live_sample(part: dict, row: VerlRow, step: int, *, split: str = Split.TRAIN) -> None:
    """A row names the agent loop's live sample it came from (`live.py`): keyed at the step it was scheduled at
    (V1's `global_steps` tag), else the step that trains it (the legacy trainers generate and train in one step) or
    the validation pass's."""
    from .live import make_live_key

    scheduled = row.scheduled_step if row.scheduled_step is not None else step
    key = make_live_key(split, scheduled, row.uid, session=row.session, position=row.position)
    if key is not None:
        part["attempt_key"] = key


def make_prompt_key(prompt: str) -> str:
    """A task key from the decoded prompt when `extra_info` names none: the same prompt, the same key."""
    return "prompt:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]


def make_policy_pieces(first: int | None, last: int | None, *, fallback: int) -> list[dict]:
    """`generated_by`: one piece per weight version the response was generated under (verl's `min_global_steps`
    / `max_global_steps`, `workers/rollout/llm_server.py:282-367`), no token ranges; else the fallback version."""
    seen = [v for v in dict.fromkeys((first, last)) if isinstance(v, int) and not isinstance(v, bool) and v >= 0]
    return [{"model": {"kind": "policy", "version": version}} for version in (seen or [fallback])]


def get_scenario(extra: Mapping[str, Any]) -> dict:
    """The task's scenario from `extra_info["scenario"]`: scenario-shaped values only (a number, short text, a bool,
    `{time}` or `{sha256}`), so one odd value never refuses the whole sample at the contract."""
    scenario = extra.get(SCENARIO_FIELD)
    if not isinstance(scenario, Mapping):
        return {}
    return {str(name): value for name, value in scenario.items() if _is_scenario_value(value)}


def get_extras(extra: Mapping[str, Any], data_source: str | None) -> dict:
    """Small dataset facts kept on the sample: the data source and short `extra_info` values (row index, split)."""
    extras: dict[str, Any] = {}
    if data_source:
        extras["data_source"] = str(data_source)
    for name, value in extra.items():
        if name in (TASK_KEY_FIELD, SCENARIO_FIELD):
            continue
        if isinstance(value, bool) or (isinstance(value, (int, float)) and math.isfinite(float(value))):
            extras[f"extra_info.{name}"] = value
        elif isinstance(value, str) and len(value) <= MAX_EXTRA_TEXT:
            extras[f"extra_info.{name}"] = value
    return extras


def _split_runs(ids: Sequence[int], mask: Sequence[int]) -> list[tuple[bool, list[int]]]:
    """The response's runs of equal mask bits: (is the model's, token ids), in order."""
    runs: list[tuple[bool, list[int]]] = []
    for token, bit in zip(ids, mask):
        if runs and runs[-1][0] == bool(bit):
            runs[-1][1].append(int(token))
        else:
            runs.append((bool(bit), [int(token)]))
    return runs


def _to_message(message: Mapping[str, Any]) -> dict:
    """A dataset chat message as a turn message; non-text content (an image part) is kept as its text parts only."""
    role = str(message.get("role") or "user")
    content = message.get("content")
    if isinstance(content, list):
        content = "".join(str(part.get("text", "")) for part in content if isinstance(part, Mapping))
    return {"role": role[:64], "source": ROLE_SOURCES.get(role, "environment"), "content": str(content or "")}


def _pick_arrays(arrays: Mapping[str, list], names: Mapping[str, str], length: int) -> dict[str, list]:
    """verl arrays renamed to Probe's, cut to the response's own tokens (verl pads to the batch's longest)."""
    picked: dict[str, list] = {}
    for verl_name, probe_name in names.items():
        values = arrays.get(verl_name)
        if isinstance(values, list) and values:
            picked[probe_name] = [_to_finite(value) for value in values[:length]]
    return picked


def _is_scenario_value(value: Any) -> bool:
    if isinstance(value, (bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, str):
        return len(value) <= MAX_SCENARIO_TEXT
    return isinstance(value, Mapping) and set(value) in ({"time"}, {"sha256"}, {"sha256", "uri"})


def _to_finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None
