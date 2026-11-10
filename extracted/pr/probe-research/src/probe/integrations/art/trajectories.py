"""ART trajectories as sample parts (RL plan §6.2): the task key and scenario from metadata, the prompt, the
response and turns (sub-agent histories' turns after the main conversation's), per-token logprobs, the policy versions
as `generated_by`, and a group's exceptions as error samples. Pure: no run, no network. Line refs are
`OpenPipe/ART@414acc5`."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta, timezone
from typing import Any

from probe.sdk.run.samples.refs import parse_generated_by

from .live import ATTEMPT_KEY, read_attempt_key

#: A trajectory's own task id, then the scenario id PipelineTrainer copies onto the group (`pipeline_trainer/trainer.py:814`).
TASK_KEYS = ("task_id", "scenario_id")
#: PipelineTrainer copies a scenario's metadata onto the group as `scenario_<key>` (`pipeline_trainer/trainer.py:816`).
GROUP_SCENARIO_PREFIX = "scenario_"
#: Where `probe.samples.generated_by(...)` rides on an SFT trajectory's metadata.
GENERATED_BY_KEY = "probe_generated_by"
#: Per-turn rewards ride a trajectory's metrics as `turn_reward/<turn index>`.
TURN_REWARD_PREFIX = "turn_reward/"
#: ART splits: `train` trains, `discarded` holds zero-variance groups (`pipeline_trainer/trainer.py:874`); the rest are evals.
TRAIN_SPLIT = "train"
DISCARDED_SPLIT = "discarded"
#: `train_sft`'s examples (the adapter's own split name; ART logs SFT metrics as `train`).
SFT_SPLIT = "sft"
#: `extras` key: how many turns each conversation holds, the main one first, then each additional history.
HISTORY_TURNS_KEY = "history_turns"
#: vLLM's token text when it returns token ids (`return_tokens_as_token_ids`).
TOKEN_ID_PREFIX = "token_id:"
MAX_METADATA_EXTRAS_BYTES = 4 * 1024
#: A group's exceptions onto `SampleErrorReason`, first match wins, by the type's name, then the message.
ERROR_REASONS = (
    ("timeout", "timeout"),
    ("outofmemory", "oom"),
    ("out of memory", "oom"),
    ("connect", "network"),
    ("network", "network"),
    ("remoteprotocol", "network"),
    ("readerror", "network"),
    ("sandbox", "sandbox"),
    ("verifier", "verifier"),
    ("reward", "reward_fn"),
    ("abort", "engine_abort"),
    ("cancel", "engine_abort"),
)
#: Chat roles onto `MessageSource`.
SOURCES = {"system": "system", "user": "user", "assistant": "model", "tool": "tool", "function": "tool"}
#: OpenAI finish reasons onto `FinishReason`.
FINISH_REASONS = {"stop": "stop", "length": "length", "tool_calls": "stop", "function_call": "stop"}

#: Metadata key names, or a callable ``(trajectory, group) -> {name: value}``.
ScenarioSpec = Iterable[str] | Callable[[Any, Any], Mapping[str, Any]] | None


def get_error_reason(type_name: str, message: str) -> str:
    """One ART exception's `SampleErrorReason`."""
    for text in (type_name.lower(), message.lower()):
        for needle, reason in ERROR_REASONS:
            if needle in text:
                return reason
    return "unknown"


def make_policy_pieces(first: int | None, last: int | None) -> list[dict]:
    """`generated_by` for a response made by this run's weights: one piece per version seen (the versions
    at its start and end, `Trajectory.initial/final_policy_version`; no token ranges)."""
    versions = [version for version in dict.fromkeys((first, last)) if isinstance(version, int) and version >= 0]
    return [{"model": {"kind": "policy", "version": version}} for version in versions]


class TrajectoryMapper:
    """Turns ART objects into `SamplePartIn`-shaped dicts. ``run_id`` turns a `run(...)` ref naming this run
    into `policy(version)`; ``host`` and ``engine`` say where it ran."""

    def __init__(
        self,
        *,
        scenario: ScenarioSpec = None,
        base_model: str | None = None,
        run_id: str | None = None,
        host: str | None = None,
        engine: str | None = None,
    ) -> None:
        self._scenario = scenario
        self._base_model = base_model
        self._run_id = run_id
        self.where = {name: value for name, value in (("host", host), ("engine", engine)) if value}

    def map_trajectory(
        self, trajectory: Any, group: Any, *, key: str, group_key: str, split: str, version: int | None
    ) -> dict:
        """A generator part for one RL or eval attempt. ``version`` stands in for missing policy versions:
        the model's step when the adapter first saw it (a plain ART loop serves its latest step)."""
        items = list(getattr(trajectory, "messages_and_choices", None) or [])
        first = getattr(trajectory, "initial_policy_version", None)
        scheduled = first if isinstance(first, int) else version
        part = self._map_common(trajectory, group, items, key=key, group_key=group_key, split=split,
                                scheduled_step=scheduled)
        pieces = make_policy_pieces(first, getattr(trajectory, "final_policy_version", None))
        part["generated_by"] = pieces or make_policy_pieces(version, version)
        reward = getattr(trajectory, "reward", None)
        if _is_number(reward):
            part["reward"] = float(reward)
        if split == DISCARDED_SPLIT:
            part["drop_reason"] = "zero_variance"
        return part

    def map_sft(self, trajectory: Any, *, key: str) -> dict:
        """An SFT example: `generated_by` from `metadata["probe_generated_by"]`, else the base model. A reward
        only when the caller set one (ART's default 0.0 is no grade)."""
        items = list(getattr(trajectory, "messages_and_choices", None) or [])
        part = self._map_common(trajectory, None, items, key=key, group_key=None, split=SFT_SPLIT, scheduled_step=None)
        ref = parse_generated_by((getattr(trajectory, "metadata", None) or {}).get(GENERATED_BY_KEY))
        if ref is None and self._base_model:
            ref = {"kind": "external", "name": self._base_model}
        if ref is not None:
            part["generated_by"] = [{"model": self._resolve_own_run(ref)}]
        if "reward" in (getattr(trajectory, "model_fields_set", None) or ()) and _is_number(trajectory.reward):
            part["reward"] = float(trajectory.reward)
        return part

    def map_exception(
        self, exception: Any, group: Any, *, key: str, group_key: str, split: str, version: int | None
    ) -> dict:
        """An attempt that raised (`TrajectoryGroup.exceptions`): result `error`, never trained on."""
        type_name = str(getattr(exception, "type", "") or "")
        message = str(getattr(exception, "message", "") or "")
        short_type = type_name.removeprefix("<class '").removesuffix("'>").rsplit(".", 1)[-1] or "Exception"
        siblings = list(getattr(group, "trajectories", None) or [])
        task_key = self._get_task_key(siblings[0], group) if siblings else self._get_group_task_key(group)
        part: dict[str, Any] = {
            "key": key,
            "task_key": task_key,
            "scenario": self._get_scenario(siblings[0] if siblings else None, group),
            "group_key": group_key,
            "split": _get_split(split),
            "error_reason": get_error_reason(type_name, message),
            "error_message": f"{short_type}: {message}",
            "log_text": "\n".join([*_get_logs(group), str(getattr(exception, "traceback", "") or "")]).strip(),
            **self.where,
        }
        if split in (TRAIN_SPLIT, DISCARDED_SPLIT):
            part["drop_reason"] = "error"
        if version is not None:
            part["scheduled_step"] = version
            part["generated_by"] = make_policy_pieces(version, version)
        extras = _get_split_extras(split)
        if extras:
            part["extras"] = extras
        return part

    # -- inside ------------------------------------------------------------------------------------------
    def _map_common(
        self, trajectory: Any, group: Any, items: list, *, key: str, group_key: str | None, split: str,
        scheduled_step: int | None,
    ) -> dict:
        prompt_items, reply_items = _split_prompt(items)
        messages = [_to_message(item) for item in items]
        part: dict[str, Any] = {
            "key": key,
            "task_key": self._get_task_key(trajectory, group, prompt_items),
            "scenario": self._get_scenario(trajectory, group),
            "split": _get_split(split),
            "prompt": render_prompt([_to_message(item) for item in prompt_items]),
            "response": _get_response(messages),
            **self.where,
        }
        if group_key is not None:
            part["group_key"] = group_key
        if scheduled_step is not None:
            part["scheduled_step"] = scheduled_step
        attempt_key = read_attempt_key(trajectory)
        if attempt_key is not None:
            part["attempt_key"] = attempt_key  # its live sample (`live.py`): a decorated rollout made it
        choices = [item for item in reply_items if _is_choice(item)]
        finish = _get(choices[-1], "finish_reason") if choices else None
        if finish is not None:
            part["finish_reason"] = FINISH_REASONS.get(str(finish), "other")
        metrics, turn_rewards = _split_metrics(getattr(trajectory, "metrics", None) or {})
        if metrics:
            part["metrics"] = metrics
        histories = [list(getattr(history, "messages_and_choices", None) or [])
                     for history in getattr(trajectory, "additional_histories", None) or ()]
        history_turns: list[int] = []
        if _is_multi_turn(messages) or histories:
            turns = build_turns(messages, items, {})
            history_turns.append(len(turns))
            for history in histories:  # ART trains each with the trajectory's advantage (`preprocessing/tokenize.py:262-277`)
                found = build_turns([_to_message(item) for item in history], history, {})
                turns += found
                history_turns.append(len(found))
            _add_turn_rewards(turns, turn_rewards)
            part["turns"] = turns
            part["turn_count"] = len(turns)
            part["tool_call_count"] = sum(len(turn.get("tool_calls", ())) for turn in turns)
        arrays = _get_token_arrays(choices)
        if arrays is not None:
            part["token_arrays"] = arrays
            part["response_tokens"] = len(arrays["loss_mask"])
        logs = [*_get_logs(group), *(str(line) for line in getattr(trajectory, "logs", None) or ())]
        if logs:
            part["log_text"] = "\n".join(logs)
        timing = _get_timing(trajectory)
        if timing:
            part["timing"] = timing
        extras = {**_get_split_extras(split), **_get_metadata_extras(trajectory)}
        if histories:
            extras[HISTORY_TURNS_KEY] = history_turns
        if extras:
            part["extras"] = extras
        return part

    def _get_task_key(self, trajectory: Any, group: Any, prompt_items: list | None = None) -> str:
        for source in (getattr(trajectory, "metadata", None), getattr(group, "metadata", None)):
            for name in TASK_KEYS:
                value = (source or {}).get(name)
                if value is not None and str(value):
                    return str(value)
        if prompt_items is None:
            prompt_items, _ = _split_prompt(list(getattr(trajectory, "messages_and_choices", None) or []))
        return make_prompt_key([_to_message(item) for item in prompt_items])

    def _get_group_task_key(self, group: Any) -> str:
        for name in TASK_KEYS:
            value = (getattr(group, "metadata", None) or {}).get(name)
            if value is not None and str(value):
                return str(value)
        return "unknown"

    def _get_scenario(self, trajectory: Any, group: Any) -> dict:
        spec = self._scenario
        if spec is None:
            return {}
        if callable(spec):
            return dict(spec(trajectory, group) or {})
        found: dict[str, Any] = {}
        for name in spec:
            value = _lookup_metadata(trajectory, group, name)
            if value is not None:
                found[name] = value
        return found

    def _resolve_own_run(self, ref: dict) -> dict:
        """A ref naming this very run (an SFT step on its own RL samples) is this run's policy."""
        if ref.get("kind") == "run" and self._run_id and str(ref.get("run_id")) == str(self._run_id):
            if isinstance(ref.get("version"), int):
                return {"kind": "policy", "version": ref["version"], "policy_id": ref.get("policy_id") or "policy"}
        return ref


def render_prompt(messages: list[dict]) -> str:
    """The prompt as text: one message's content alone, else one `role: content` block per message."""
    if len(messages) == 1:
        return messages[0]["content"]
    return "\n\n".join(f"{message['role']}: {message['content']}" for message in messages)


def make_prompt_key(messages: list[dict]) -> str:
    """A task key from the prompt itself when the metadata names none: the same prompt, the same key."""
    canonical = json.dumps([[message["role"], message["content"]] for message in messages], ensure_ascii=False)
    return "prompt:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def build_turns(messages: list[dict], items: list, turn_rewards: dict[int, float]) -> list[dict]:
    """One turn per model reply, holding the messages since the last reply; trailing messages are a last
    turn. Each message keeps its source and whether the trainer learns from it (ART's Choice = trainable)."""
    turns: list[dict] = []
    current: list[dict] = []
    calls: list[dict] = []
    for message, item in zip(messages, items):
        current.append({
            "role": message["role"],
            "source": SOURCES.get(message["role"], "environment"),
            "is_trainable": _is_choice(item),
            "content": message["content"],
            **({"name": message["name"]} if message.get("name") else {}),
            **({"tool_call_id": message["tool_call_id"]} if message.get("tool_call_id") else {}),
        })
        calls.extend({"name": name} for name in message.get("tool_names", ()))
        if message["role"] == "assistant":
            turns.append({"messages": current, "tool_calls": calls})
            current, calls = [], []
    if current:
        turns.append({"messages": current, "tool_calls": calls})
    _add_turn_rewards(turns, turn_rewards)
    return turns


def _add_turn_rewards(turns: list[dict], turn_rewards: dict[int, float]) -> None:
    for index, reward in turn_rewards.items():
        if 0 <= index < len(turns):
            turns[index]["reward"] = reward


def _is_choice(item: Any) -> bool:
    """An OpenAI `Choice` (or litellm `Choices`): a model reply ART trains on (`trajectories.py:87`, `:100`)."""
    return not isinstance(item, Mapping) and hasattr(item, "message") and hasattr(item, "finish_reason")


def _get(target: Any, name: str) -> Any:
    return target.get(name) if isinstance(target, Mapping) else getattr(target, name, None)


def _get_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = [str(_get(part, "text")) for part in content if _get(part, "text") is not None]
        if texts:
            return "\n".join(texts)
    return json.dumps(content, default=str, ensure_ascii=False)


def _to_message(item: Any) -> dict:
    message = _get(item, "message") if _is_choice(item) else item
    role = "assistant" if _is_choice(item) else str(_get(message, "role") or "user")
    calls = _get(message, "tool_calls") or []
    names = [str(_get(_get(call, "function"), "name") or "tool") for call in calls]
    return {
        "role": role,
        "content": _get_text(_get(message, "content")),
        "name": _get(message, "name") if isinstance(_get(message, "name"), str) else None,
        "tool_call_id": _get(message, "tool_call_id") if isinstance(_get(message, "tool_call_id"), str) else None,
        "tool_names": names,
    }


def _split_prompt(items: list) -> tuple[list, list]:
    """The messages before the first model reply, and the rest."""
    for index, item in enumerate(items):
        if _is_choice(item) or _get(item, "role") == "assistant":
            return items[:index], items[index:]
    return items, []


def _get_response(messages: list[dict]) -> str:
    for message in reversed(messages):
        if message["role"] == "assistant":
            return message["content"]
    return ""


def _is_multi_turn(messages: list[dict]) -> bool:
    replies = sum(1 for message in messages if message["role"] == "assistant")
    return replies > 1 or any(message["role"] in ("tool", "function") for message in messages)


def _split_metrics(metrics: Mapping[str, Any]) -> tuple[dict[str, float], dict[int, float]]:
    numbers: dict[str, float] = {}
    turn_rewards: dict[int, float] = {}
    for name, value in metrics.items():
        if not _is_number(value):
            continue
        if str(name).startswith(TURN_REWARD_PREFIX) and str(name)[len(TURN_REWARD_PREFIX):].isdigit():
            turn_rewards[int(str(name)[len(TURN_REWARD_PREFIX):])] = float(value)
        else:
            numbers[str(name)] = float(value)
    return numbers, turn_rewards


def _get_token_arrays(choices: list) -> dict | None:
    """The sampled tokens and their inference logprobs from each reply's `logprobs.content`."""
    texts: list[str] = []
    logprobs: list[float | None] = []
    ids: list[int | None] = []
    for choice in choices:
        for entry in _get(_get(choice, "logprobs"), "content") or ():
            token = _get(entry, "token")
            if token is None:
                continue
            value = _get(entry, "logprob")
            texts.append(str(token))
            logprobs.append(float(value) if _is_number(value) else None)
            raw = str(token)
            ids.append(int(raw[len(TOKEN_ID_PREFIX):]) if raw.startswith(TOKEN_ID_PREFIX) and raw[len(TOKEN_ID_PREFIX):].isdigit() else None)
    if not texts:
        return None
    arrays: dict[str, list] = {"inference_logprobs": logprobs, "loss_mask": [1] * len(texts)}
    if all(token_id is not None for token_id in ids):
        arrays["token_ids"] = ids
    else:
        arrays["token_text"] = texts
    return arrays


def _get_logs(group: Any) -> list[str]:
    return [str(line) for line in getattr(group, "logs", None) or ()]


def _get_timing(trajectory: Any) -> dict:
    """`start_time` is a naive local time (`trajectories.py:48`); `finish()` puts the duration in metrics."""
    started = getattr(trajectory, "start_time", None)
    if not isinstance(started, datetime):
        return {}
    started = started.astimezone(timezone.utc)
    timing = {"started_at": started.isoformat()}
    duration = (getattr(trajectory, "metrics", None) or {}).get("duration")
    if _is_number(duration) and duration >= 0:
        timing["ended_at"] = (started + timedelta(seconds=float(duration))).isoformat()
    return timing


def _get_split(split: str) -> str:
    if split == SFT_SPLIT:
        return SFT_SPLIT
    return "train" if split in (TRAIN_SPLIT, DISCARDED_SPLIT) else "eval"


def _get_split_extras(split: str) -> dict:
    return {} if split in (TRAIN_SPLIT, SFT_SPLIT) else {"art_split": split}


def _get_metadata_extras(trajectory: Any) -> dict:
    metadata = {
        str(name): value
        for name, value in (getattr(trajectory, "metadata", None) or {}).items()
        if name not in (GENERATED_BY_KEY, ATTEMPT_KEY) and isinstance(value, (str, int, float, bool))
    }
    if not metadata or len(json.dumps(metadata, default=str)) > MAX_METADATA_EXTRAS_BYTES:
        return {}
    from probe.sdk.redaction import default_scrub

    return {"metadata": default_scrub(metadata)}


def _lookup_metadata(trajectory: Any, group: Any, name: str) -> Any:
    own = getattr(trajectory, "metadata", None) or {}
    shared = getattr(group, "metadata", None) or {}
    for source, key in ((own, name), (shared, name), (shared, GROUP_SCENARIO_PREFIX + name)):
        if source.get(key) is not None:
            return source[key]
    return None


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))
