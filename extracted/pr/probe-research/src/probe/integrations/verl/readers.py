"""verl batches as `VerlRow`s (RL plan §6.5), read in memory with no dump directory: a `DataProto` training batch
(the legacy, one-step-off and fully async trainers), a V1 batch whose rows live in the TransferQueue, and a
validation pass. Duck-typed on verl's objects, no verl import. Line refs are `verl-project/verl@b17218ba58a6`."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from .rows import INFERENCE_ARRAYS, LIVE_KEY_FIELD, STOP_REASON_FIELD, TRAINER_ARRAYS, Split, VerlRow, make_sample_key
from .tool_loop import ROLLOUT_EVAL_FIELD, ROLLOUT_FIELD, read_stamp

#: Per-token arrays a training batch may carry, by verl's names.
ARRAY_FIELDS = (*INFERENCE_ARRAYS, *TRAINER_ARRAYS)
#: V1 fields every row has once its advantage is computed (`v1/trainer_base.py:1754-1815`).
CORE_FIELDS = ("prompts", "responses", "response_mask", "rm_scores")
#: V1 fields a row may have: the dataset's own columns ride with it (`v1/agent_loop_tq.py:197-208`).
OPTIONAL_FIELDS = (*ARRAY_FIELDS, "extra_info", "data_source", "reward_model", "extra_fields", "num_turns", "raw_prompt",
                   "agent_name")
#: A TransferQueue key is `{uid}_{session_id}_{index}` (`v1/agent_loop_tq.py:182-198`).
KEY_PARTS = 3


@dataclass
class PromptFacts:
    """What a validation pass knows of one prompt only from its dataset row: `extra_info` and the reference answer."""

    extra_info: Mapping[str, Any] | None = None
    ground_truth: Any = None


@dataclass
class ValidationPass:
    """One `_validate()` call as verl hands it out: the texts, scores and uids of every final response
    (`_maybe_log_val_generations`) and the per-response facts verl computes metrics from (`_val_metrics_update`)."""

    inputs: Sequence[str] = ()
    outputs: Sequence[str] = ()
    scores: Sequence[Any] = ()
    uids: Sequence[Any] = ()
    data_sources: Sequence[Any] = ()
    reward_extras: Mapping[str, Sequence[Any]] | None = None
    turns: Sequence[Any] = ()
    #: Legacy: the generated batches' rows in order (`ray_trainer.py:640-650`), each its loop's live key and stop
    #: reason (`live.stamp_output`). V1: each final response's `(uid, session)`, from the TransferQueue keys the pass
    #: sampled (`v1/trainer_base.py:1089-1096`).
    live_keys: list[str] = field(default_factory=list)
    stop_reasons: list[str] = field(default_factory=list)
    sessions: list[tuple[str, str]] = field(default_factory=list)
    #: Legacy, scored in the trainer: each generated row's capture stamp (`tool_loop.ROLLOUT_EVAL_FIELD`), as above.
    rollouts: list[str] = field(default_factory=list)


def read_dataproto_rows(batch: Any) -> list[VerlRow]:
    """A `DataProto` about to train (`ray_trainer.py:1327`): padded tensors in `batch.batch`, one numpy array per
    column in `batch.non_tensor_batch`. Prompts are left-padded and responses right-padded; the attention mask says
    which tokens are real (`agent_loop.py:1150-1180`)."""
    tensors, columns, meta = batch.batch, batch.non_tensor_batch, batch.meta_info or {}
    responses = to_rows(_get_field(tensors, "responses"))
    prompts = to_rows(_get_field(tensors, "prompts"))
    attention = to_rows(_get_field(tensors, "attention_mask"))
    masks = to_rows(_get_field(tensors, "response_mask"))
    scores = to_rows(_get_field(tensors, "token_level_scores")) or to_rows(_get_field(tensors, "rm_scores"))
    arrays = {name: to_rows(_get_field(tensors, name)) for name in ARRAY_FIELDS}
    uids = _get_column(columns, "uid")
    reward_names = [str(name) for name in meta.get("reward_extra_keys") or ()]
    rows: list[VerlRow] = []
    seen: Counter = Counter()
    for row, response in enumerate(responses):
        width = len(prompts[row]) if row < len(prompts) else 0
        mask = attention[row] if row < len(attention) else []
        prompt_ids = [token for token, bit in zip(prompts[row], mask[:width]) if bit] if width else []
        length = int(sum(mask[width:])) if mask else len(response)
        uid = str(_pick(uids, row, row))
        rows.append(VerlRow(
            uid=uid,
            index=str(seen[uid]),
            prompt_ids=[int(token) for token in prompt_ids],
            response_ids=[int(token) for token in response[:length]],
            score=_get_total(scores[row]) if row < len(scores) else None,
            reward_parts=_get_reward_parts({name: _pick(_get_column(columns, name), row) for name in reward_names}),
            extra_info=_as_mapping(_pick(_get_column(columns, "extra_info"), row)),
            data_source=_as_text(_pick(_get_column(columns, "data_source"), row)),
            ground_truth=_get_ground_truth(_pick(_get_column(columns, "reward_model"), row)),
            turn_count=_as_int(_pick(_get_column(columns, "__num_turns__"), row)),
            min_version=_as_int(_pick(_get_column(columns, "min_global_steps"), row)),
            max_version=_as_int(_pick(_get_column(columns, "max_global_steps"), row)),
            response_mask=[int(bit) for bit in masks[row]] if row < len(masks) else None,
            arrays={name: values[row] for name, values in arrays.items() if row < len(values)},
            raw_prompt=_as_messages(_pick(_get_column(columns, "raw_prompt"), row)),
            agent_name=_as_text(_pick(_get_column(columns, "agent_name"), row)),
            position=_as_int(_pick(_get_column(columns, "priority"), row)),
            stop_reason=_as_text(_pick(_get_column(columns, STOP_REASON_FIELD), row)) or None,
            rollout=read_stamp(_pick(_get_column(columns, ROLLOUT_FIELD), row)),
        ))
        seen[uid] += 1
    return rows


def read_row_keys(batch: Any, step: int) -> list[str]:
    """Each row's train sample key on a legacy `DataProto`, as `read_dataproto_rows` and the recorder name it
    (`rows.make_sample_key`: the uid, then the row's place among its uid's rows), from the `uid` column alone: the
    critic trains on the step's batch before the actor's update records it, and needs only its keys."""
    size = getattr(getattr(batch, "batch", None), "batch_size", None)
    uids = _get_column(getattr(batch, "non_tensor_batch", None), "uid")
    count = int(size[0]) if size else len(uids)
    seen: Counter = Counter()
    keys = []
    for row in range(count):
        uid = str(_pick(uids, row, row))
        keys.append(make_sample_key(Split.TRAIN, step, VerlRow(uid=uid, index=str(seen[uid]))))
        seen[uid] += 1
    return keys


def fetch_transfer_queue_rows(batch: Any, kv_batch_get: Callable[..., Any]) -> list[VerlRow]:
    """A V1 `KVBatchMeta` about to train (`v1/trainer_base.py:1840`): its keys and tags are in hand, its fields in
    the TransferQueue until the step clears them (`:512`). ``kv_batch_get`` is `transfer_queue.kv_batch_get`. Fields
    a row may lack (no reference policy, no rollout logprobs) are fetched one by one when the whole set fails."""
    keys, tags = list(batch.keys), list(batch.tags)
    real = [position for position, tag in enumerate(tags) if not (isinstance(tag, Mapping) and tag.get("is_padding"))]
    if not real:
        return []
    real_keys = [keys[position] for position in real]

    def fetch(fields: Sequence[str]) -> Any:
        return kv_batch_get(keys=real_keys, partition_id=batch.partition_id, select_fields=list(fields))

    data: dict[str, Any] = {}
    try:
        found = fetch((*CORE_FIELDS, *OPTIONAL_FIELDS))
        data.update({name: _get_field(found, name) for name in (*CORE_FIELDS, *OPTIONAL_FIELDS)})
    except Exception:  # noqa: BLE001 -- a field this run never wrote: fetch the rest one by one
        found = fetch(CORE_FIELDS)
        data.update({name: _get_field(found, name) for name in CORE_FIELDS})
        for name in OPTIONAL_FIELDS:
            try:
                data[name] = _get_field(fetch((name,)), name)
            except Exception:  # noqa: BLE001 -- absent for this run
                data[name] = None
    return read_transfer_queue_rows(real_keys, [tags[position] for position in real], data)


def read_transfer_queue_rows(keys: Sequence[str], tags: Sequence[Mapping[str, Any]],
                             data: Mapping[str, Any]) -> list[VerlRow]:
    """Rows from fetched V1 fields: unpadded (jagged) prompts and responses, one `extra_fields` dict per row
    (`reward_extra_info`, `agent_loop.py:1116`), the weight versions and the scheduling step from the tags
    (`v1/agent_loop_tq.py:210-224`). One session's several outputs are one attempt's segments."""
    columns = {name: to_rows(data.get(name)) for name in (*CORE_FIELDS, *OPTIONAL_FIELDS)}
    names = [_split_key(key) for key in keys]
    totals = Counter((uid, session) for uid, session, _index in names)
    rows: list[VerlRow] = []
    for row, (uid, session, index) in enumerate(names):
        tag = tags[row] if row < len(tags) and isinstance(tags[row], Mapping) else {}
        extra_fields = _as_mapping(_pick(columns["extra_fields"], row)) or {}
        reward_info = extra_fields.get("reward_extra_info")
        rows.append(VerlRow(
            uid=uid,
            index=f"{session}" if totals[(uid, session)] == 1 else f"{session}.{index}",
            prompt_ids=[int(token) for token in _pick(columns["prompts"], row, [])],
            response_ids=[int(token) for token in _pick(columns["responses"], row, [])],
            score=_get_total(_pick(columns["rm_scores"], row)),
            reward_parts=_get_reward_parts(reward_info if isinstance(reward_info, Mapping) else {}),
            extra_info=_as_mapping(_pick(columns["extra_info"], row)),
            data_source=_as_text(_pick(columns["data_source"], row)),
            ground_truth=_get_ground_truth(_pick(columns["reward_model"], row)),
            turn_count=_as_int(_pick(columns["num_turns"], row)),
            min_version=_as_int(tag.get("min_global_steps")),
            max_version=_as_int(tag.get("max_global_steps")),
            scheduled_step=_as_int(tag.get("global_steps")),
            segment=int(index) if index.isdigit() else None,
            segment_count=totals[(uid, session)],
            response_mask=[int(bit) for bit in _pick(columns["response_mask"], row, [])] or None,
            arrays={name: columns[name][row] for name in ARRAY_FIELDS if row < len(columns[name])},
            raw_prompt=_as_messages(_pick(columns["raw_prompt"], row)),
            agent_name=_as_text(_pick(columns["agent_name"], row)),
            session=session,
            stop_reason=_as_text(extra_fields.get(STOP_REASON_FIELD)) or None,
            rollout=read_stamp(extra_fields.get(ROLLOUT_FIELD)),
        ))
    return rows


def read_prompt_facts(columns: Mapping[str, Any]) -> dict[str, PromptFacts]:
    """uid -> the dataset row's facts, from a batch's non-tensor columns (a `DataProto.non_tensor_batch`, or a V1
    validation batch dict, `v1/trainer_base.py:1048-1052`)."""
    uids = _get_column(columns, "uid")
    extras = _get_column(columns, "extra_info")
    answers = _get_column(columns, "reward_model")
    return {
        str(uid): PromptFacts(extra_info=_as_mapping(_pick(extras, row)), ground_truth=_get_ground_truth(_pick(answers, row)))
        for row, uid in enumerate(uids)
    }


def read_generated(batch: Any, count: int | None = None) -> tuple[list[str], list[str]]:
    """A generated validation `DataProto`'s first ``count`` rows (the rest is `pad_dataproto_to_divisor` padding,
    `ray_trainer.py:638-640`): each loop's live key and stop reason, `""` when it carried none."""
    columns = getattr(batch, "non_tensor_batch", None) or {}
    keys, reasons = _get_column(columns, LIVE_KEY_FIELD), _get_column(columns, STOP_REASON_FIELD)
    size = len(keys or reasons) if count is None else count
    return ([_as_text(_pick(keys, row)) or "" for row in range(size)],
            [_as_text(_pick(reasons, row)) or "" for row in range(size)])


def read_generated_rollouts(batch: Any, count: int | None = None) -> list[str]:
    """A generated validation `DataProto`'s first ``count`` rows' capture stamps, `""` when a row carried none (the
    rows past ``count`` are padding, as `read_generated`)."""
    columns = getattr(batch, "non_tensor_batch", None) or {}
    stamps = _get_column(columns, ROLLOUT_EVAL_FIELD)
    size = len(stamps) if count is None else count
    return [_as_text(_pick(stamps, row)) or "" for row in range(size)]


def read_final_sessions(keys: Sequence[str]) -> list[tuple[str, str]]:
    """The `(uid, session)` of each session's final output, in the order V1's `_validate` takes them: the highest
    index per `{uid}_{session}`, ordered by where it sat (`v1/trainer_base.py:1081-1096`)."""
    final: dict[tuple[str, str], tuple[int, int]] = {}
    for position, key in enumerate(keys):
        uid, session, index = _split_key(key)
        number = int(index) if index.isdigit() else 0
        if (uid, session) not in final or number > final[(uid, session)][0]:
            final[(uid, session)] = (number, position)
    return [name for name, _ in sorted(final.items(), key=lambda item: item[1][1])]


def read_versions(batch: Any) -> list[int]:
    """The weight versions a generated `DataProto`'s responses ended under (`max_global_steps`, the agent loop's
    column, `agent_loop.py:1210-1223`); rows with none (padding) are left out."""
    columns = getattr(batch, "non_tensor_batch", None) or {}
    return [version for value in _get_column(columns, "max_global_steps") if (version := _as_int(value)) is not None]


def build_validation_rows(validation: ValidationPass, prompts: Mapping[str, PromptFacts]) -> list[VerlRow]:
    """A validation pass's final responses as rows: verl's decoded texts and scores, each uid's reward parts and
    turns, and the dataset facts of its prompt. Empty when the two halves disagree on length."""
    count = len(validation.outputs)
    if not count or len(validation.inputs) != count or len(validation.uids) != count:
        return []
    reward_extras = dict(validation.reward_extras or {})
    carried = [_as_text(key) or "" for key in reward_extras.pop(LIVE_KEY_FIELD, None) or ()]
    if len(carried) != count:
        carried = validation.live_keys if len(validation.live_keys) == count else []
    reasons = [_as_text(reason) or "" for reason in reward_extras.pop(STOP_REASON_FIELD, None) or ()]
    if len(reasons) != count:
        reasons = validation.stop_reasons if len(validation.stop_reasons) == count else []
    sessions = validation.sessions if len(validation.sessions) == count else []
    rollouts = list(reward_extras.pop(ROLLOUT_EVAL_FIELD, None) or ())
    if len(rollouts) != count:
        rollouts = validation.rollouts if len(validation.rollouts) == count else []
    extras = {name: list(values) for name, values in reward_extras.items()
              if name != "reward" and len(values) == count}
    turns = _flatten(validation.turns)
    sources = list(validation.data_sources)
    seen: Counter = Counter()
    rows: list[VerlRow] = []
    for row in range(count):
        uid = str(validation.uids[row])
        facts = prompts.get(uid) or PromptFacts()
        rows.append(VerlRow(
            uid=uid,
            index=str(seen[uid]),
            prompt_text=str(validation.inputs[row]),
            response_text=str(validation.outputs[row]),
            score=_as_number(_pick(validation.scores, row)),
            reward_parts=_get_reward_parts({name: values[row] for name, values in extras.items()}),
            extra_info=facts.extra_info,
            data_source=_as_text(_pick(sources, row)),
            ground_truth=facts.ground_truth,
            turn_count=_as_int(turns[row]) if len(turns) == count else None,
            attempt_key=carried[row] or None if carried else None,
            session=sessions[row][1] if sessions and sessions[row][0] == uid else None,
            stop_reason=reasons[row] or None if reasons else None,
            rollout=read_stamp(rollouts[row]) if rollouts else None,
        ))
        seen[uid] += 1
    return rows


def to_rows(value: Any) -> list:
    """A batch field as one Python list per row: a jagged (nested) tensor row by row, a padded tensor or a numpy
    column through `tolist`, a TensorDict non-tensor stack through its own `tolist`, a TensorDict `LinkedList` (what
    the TransferQueue returns for non-tensor fields, `v1/trainer_base.py:1558-1562`) as the list it is."""
    if value is None:
        return []
    if getattr(value, "is_nested", False):
        return [row.tolist() for row in value.unbind()]
    tolist = getattr(value, "tolist", None)
    if callable(tolist):
        rows = tolist()
        return list(rows) if isinstance(rows, (list, tuple)) else [rows]
    if isinstance(value, (list, tuple)):
        return list(value)
    return []


# -- inside ----------------------------------------------------------------------------------------------
def _get_field(container: Any, name: str) -> Any:
    """A TensorDict / mapping field, or None when it has none."""
    try:
        if name not in container.keys():
            return None
        return container[name]
    except Exception:  # noqa: BLE001 -- a container that cannot say: no such field
        return None


def _get_column(columns: Mapping[str, Any] | None, name: str) -> list:
    if not columns or name not in columns:
        return []
    return to_rows(columns[name])


def _pick(values: Sequence[Any], position: int, default: Any = None) -> Any:
    return values[position] if position < len(values) else default


def _split_key(key: str) -> tuple[str, str, str]:
    parts = str(key).rsplit("_", KEY_PARTS - 1)
    if len(parts) == KEY_PARTS:
        return parts[0], parts[1], parts[2]
    return str(key), "0", "0"


def _flatten(values: Sequence[Any]) -> list:
    """verl's legacy pass keeps turns as one array per batch (`ray_trainer.py:688-689`), V1 as one list."""
    flat: list = []
    for value in values or ():
        rows = to_rows(value) if not isinstance(value, (int, float)) else [value]
        flat.extend(rows)
    return flat


def _get_total(value: Any) -> float | None:
    if isinstance(value, (list, tuple)):
        numbers = [_as_number(item) for item in value]
        return float(sum(number for number in numbers if number is not None))
    return _as_number(value)


def _get_reward_parts(values: Mapping[str, Any]) -> dict[str, float]:
    parts = {}
    for name, value in values.items():
        number = _as_number(value)
        if number is not None:
            parts[str(name)] = number
    return parts


def _get_ground_truth(reward_model: Any) -> Any:
    """`reward_model.ground_truth` (`utils/dataset/rl_dataset.py`, `ray_trainer.py:528`) when it is plain JSON."""
    if not isinstance(reward_model, Mapping):
        return None
    answer = reward_model.get("ground_truth")
    item = getattr(answer, "item", None)
    if callable(item) and not isinstance(answer, (str, bytes)):
        try:
            answer = item()
        except Exception:  # noqa: BLE001 -- not a scalar: kept as text below
            answer = str(answer)
    if answer is None or isinstance(answer, (str, int, float, bool)):
        return answer
    return to_rows(answer) if hasattr(answer, "tolist") else str(answer)


def _as_mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _as_messages(value: Any) -> list[Mapping[str, Any]] | None:
    """The dataset's chat messages: a list (or numpy array) of role/content mappings."""
    rows = to_rows(value) if not isinstance(value, (list, tuple)) else list(value)
    messages = [message for message in rows if isinstance(message, Mapping)]
    return messages or None


def _as_text(value: Any) -> str | None:
    return None if value is None else str(value)


def _as_int(value: Any) -> int | None:
    if isinstance(value, (list, tuple)) and len(value) == 1:  # a TransferQueue scalar can come back boxed
        value = value[0]
    item = getattr(value, "item", None)
    if callable(item) and not isinstance(value, (int, float)):
        try:
            value = item()
        except Exception:  # noqa: BLE001 -- not a scalar
            return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return int(value) if math.isfinite(float(value)) else None


def _as_number(value: Any) -> float | None:
    item = getattr(value, "item", None)
    if callable(item) and not isinstance(value, (int, float)):
        try:
            value = item()
        except Exception:  # noqa: BLE001 -- not a scalar
            return None
    if isinstance(value, bool):
        return float(value)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None
