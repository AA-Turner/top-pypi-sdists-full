"""One SkyRL `generate()` call as sample parts (RL plan §6.3): each output row with its TrajectoryID, decoded
prompt and response, stop reason, reward (a token-level reward's sum), env metrics, the scenario and label from
`env_extras`, per-token ids and logprobs, and the weight versions the call ran under; a step-wise row is a turn of
its trajectory. Pure: no SkyRL import. Line refs are `NovaSky-AI/SkyRL@d87004689e3a`."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from probe.generated.samples import TurnsSource

#: A dataset column (it lands in `env_extras`, `generators/utils.py:597-598`) naming the task; else a prompt hash.
TASK_KEY_COLUMN = "task_id"
#: A dataset column holding the task's scenario as an object of named values.
SCENARIO_COLUMN = "scenario"
#: The task's grading spec, its reference answer under `ground_truth` (every SkyRL Gym env reads it, e.g.
#: `skyrl_gym/envs/gsm8k/env.py:15`): the task's `label`.
LABEL_COLUMN = "reward_spec"
MAX_LABEL_BYTES = 4 * 1024
#: SkyRL stop reasons onto `FinishReason` (`skyrl_gym_generator.py:453`, `:484`); `error` is not a grade.
FINISH_REASONS = {"stop": "stop", "length": "length", "abort": "abort", "error": "error"}
#: Chat roles onto `MessageSource`; a Gym observation arrives as `user` (RL plan §3.3).
SOURCES = {"system": "system", "user": "user", "assistant": "model", "tool": "tool"}
#: Non-zero entries of a token-level reward kept in extras (the sum is the reward).
MAX_TOKEN_REWARDS = 256
#: A scenario text value's cap (`records/samples/task.py`, `MAX_SCENARIO_TEXT_CHARS`).
MAX_SCENARIO_TEXT = 256
#: A row's grade: on a step-wise trajectory, every row carries its last row's (`trainer.py:1250-1254`).
GRADE_FIELDS = ("reward", "error_reason", "error_message")


@dataclass(frozen=True)
class CallVersions:
    """The policy versions a call ran under: at its start and its end (in-flight weight updates)."""

    first: int | None
    last: int | None


def make_policy_pieces(versions: CallVersions) -> list[dict]:
    """`generated_by` pieces: one per version seen, no token ranges (somewhere in this attempt)."""
    seen = [v for v in dict.fromkeys((versions.first, versions.last)) if isinstance(v, int) and v >= 0]
    return [{"model": {"kind": "policy", "version": version}} for version in seen]


def make_live_key(call_id: int, instance: str, repetition: int) -> str:
    """A trajectory's live sample key, `{call}:{instance}:{repetition}`: its rows' keys add `:{segment}` (rl-next W37)."""
    return f"{call_id}:{instance}:{repetition}"


def make_prompt_key(prompt: Any) -> str:
    """A task key from the prompt itself: the same prompt, the same key."""
    canonical = json.dumps(prompt, sort_keys=True, default=str, ensure_ascii=False)
    return "prompt:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def render_prompt(prompt: Any) -> str:
    """A conversation as text: one message's content alone, else one `role: content` block per message."""
    if isinstance(prompt, str):
        return prompt
    messages = [message for message in prompt or () if isinstance(message, Mapping)]
    if len(messages) == 1:
        return _get_text(messages[0].get("content"))
    return "\n\n".join(f"{message.get('role', '')}: {_get_text(message.get('content'))}" for message in messages)


class OutputMapper:
    """GeneratorInput + GeneratorOutput -> `SamplePartIn`-shaped generator parts. ``decode`` turns token ids into
    text (the tokenizer's `decode`), ``tokens_to_text`` into one string per token; either may be None."""

    def __init__(
        self,
        *,
        decode: Any = None,
        tokens_to_text: Any = None,
        scenario_keys: Sequence[str] = (),
        host: str | None = None,
        worker: str | None = None,
    ) -> None:
        self._decode = decode
        self._tokens_to_text = tokens_to_text
        self._scenario_keys = tuple(scenario_keys)
        self.where = {name: value for name, value in (("host", host), ("worker", worker)) if value}

    def map_starts(self, inputs: Mapping[str, Any], *, call_id: int, version: int | None = None,
                   scheduled_step: int | None = None) -> list[dict]:
        """Each input row as its trajectory's live sample start (rl-next W37), keyed as `map_call` names its rows'
        `attempt_key`, with the task, scenario and group its rows get."""
        prompts = list(inputs.get("prompts") or [])
        extras_in = list(inputs.get("env_extras") or [])
        trajectory_ids = inputs.get("trajectory_ids") or []
        metadata = inputs.get("batch_metadata")
        is_train = _get(metadata, "training_phase") != "eval"
        scheduled = scheduled_step if is_train and scheduled_step is not None else _get(metadata, "global_step")
        starts = []
        for row, prompt in enumerate(prompts):
            trajectory = trajectory_ids[row] if row < len(trajectory_ids) else None
            instance, repetition = get_identity(trajectory) or (str(row), 0)
            env_extras = extras_in[row] if row < len(extras_in) and isinstance(extras_in[row], Mapping) else {}
            start: dict[str, Any] = {
                "key": make_live_key(call_id, instance, repetition),
                "task_key": str(env_extras.get(TASK_KEY_COLUMN) or make_prompt_key(prompt)),
                "scenario": self._get_scenario(env_extras),
                "group_key": f"{call_id}:{instance}",
                **self.where,
            }
            if isinstance(scheduled, int):
                start["scheduled_step"] = scheduled
            if isinstance(version, int) and version >= 0:
                start["weight_version"] = version
            starts.append(start)
        return starts

    def map_call(self, inputs: Mapping[str, Any], output: Mapping[str, Any], *, call_id: int,
                 versions: CallVersions, harbor: Mapping[int, Any] | None = None,
                 scheduled_step: int | None = None) -> list[dict]:
        """One part per output row. A step-wise output carries its own TrajectoryIDs, one row per step (each
        row a `segment` of its trajectory); otherwise rows follow the input one to one. ``harbor`` maps
        `id(TrajectoryID)` to the Harbor trial that ran it (`harbor.HarborJoin.take`): its rows take the trial's
        key (`TrialResult.id`, `<id>:<segment>` past the first) and task, so the trial merges into the sample. Every
        row names its trajectory's live sample (`attempt_key`: `make_live_key`, or a Harbor trial's id).
        ``scheduled_step`` overrides `batch_metadata.global_step` for a train call (the fully async trainer's). A
        step-wise row is one turn holding its own step's reward, and carries its trajectory's grade (`_set_step_grades`)."""
        responses = list(output.get("response_ids") or [])
        trajectory_ids = output.get("trajectory_ids") or inputs.get("trajectory_ids") or []
        is_step_wise = output.get("trajectory_ids") is not None
        prompts = list(inputs.get("prompts") or [])
        extras_in = list(inputs.get("env_extras") or [])
        segments = _get_segments(trajectory_ids, len(responses)) if is_step_wise else None
        input_index = _index_inputs(inputs.get("trajectory_ids") or [])
        metadata = inputs.get("batch_metadata")
        split = "eval" if _get(metadata, "training_phase") == "eval" else "train"
        scheduled = scheduled_step if split == "train" and scheduled_step is not None else _get(metadata, "global_step")
        rows = []
        for row in range(len(responses)):
            trajectory = trajectory_ids[row] if row < len(trajectory_ids) else None
            source = input_index.get(get_identity(trajectory), row) if is_step_wise else row
            prompt = prompts[source] if source < len(prompts) else None
            env_extras = extras_in[source] if source < len(extras_in) and isinstance(extras_in[source], Mapping) else {}
            part = self._map_row(output, row, prompt=prompt, env_extras=env_extras, versions=versions,
                                 is_step_wise=is_step_wise)
            rows.append((trajectory, source, part))
        if is_step_wise:
            _set_step_grades([part for _, _, part in rows], [get_identity(trajectory) for trajectory, _, _ in rows],
                         output.get("is_last_step"))
        parts = []
        for row, (trajectory, source, part) in enumerate(rows):
            segment, segment_count = segments[row] if segments else (0, None)
            instance, repetition = get_identity(trajectory) or (str(source), 0)
            part["key"] = f"{make_live_key(call_id, instance, repetition)}:{segment}"
            part["attempt_key"] = make_live_key(call_id, instance, repetition)
            part["group_key"] = f"{call_id}:{instance}"
            trial = (harbor or {}).get(id(trajectory)) if trajectory is not None else None
            if trial is not None:
                _join_trial(part, trial, segment)
            part["split"] = split
            if isinstance(scheduled, int):
                part["scheduled_step"] = scheduled
            if segment_count is not None:
                part["segment"], part["segment_count"] = segment, segment_count
            parts.append(part)
        return parts

    # -- inside ------------------------------------------------------------------------------------------
    def _map_row(self, output: Mapping[str, Any], row: int, *, prompt: Any, env_extras: Mapping[str, Any],
                 versions: CallVersions, is_step_wise: bool = False) -> dict:
        response_ids = _pick(output, "response_ids", row) or []
        stop = _pick(output, "stop_reasons", row)
        part: dict[str, Any] = {
            "task_key": str(env_extras.get(TASK_KEY_COLUMN) or make_prompt_key(prompt)),
            "scenario": self._get_scenario(env_extras),
            "prompt": render_prompt(prompt),
            "response": self._decode_text(response_ids),
            "response_tokens": len(response_ids),
            "generated_by": make_policy_pieces(versions),
            **self.where,
        }
        label = _get_label(env_extras)
        if label is not None:
            part["label"] = label  # the SDK lifts it onto the task
        prompt_ids = _pick(output, "prompt_token_ids", row)
        if prompt_ids is not None:
            part["prompt_tokens"] = len(prompt_ids)
        if stop is not None:
            part["finish_reason"] = FINISH_REASONS.get(str(stop), "other")
        reward, token_rewards = read_reward(_pick(output, "rewards", row))
        if stop == "error":
            part["error_reason"] = "unknown"  # the attempt broke: no grade, whatever number SkyRL kept
            part["error_message"] = "SkyRL stop_reason=error"
        elif reward is not None:
            part["reward"] = reward
        metrics = _get_numbers(_pick(output, "env_metrics", row))
        if metrics:
            part["metrics"] = metrics
        if is_step_wise:  # the step's own reward rides its turn; the row is graded by its trajectory
            part["turns"] = [self._build_step_turn(response_ids, _pick(output, "loss_masks", row), reward,
                                                   is_graded=stop != "error")]
            part["turns_source"] = TurnsSource.DECODED  # text Probe decoded from the step's tokens, not messages as sent
        elif token_rewards:
            part["extras"] = {"token_rewards": token_rewards}
        arrays = self._get_token_arrays(output, row, response_ids)
        if arrays:
            part["token_arrays"] = arrays
        timing = _get_timing(output, row)
        if timing:
            part["timing"] = timing
        return part

    def _get_scenario(self, env_extras: Mapping[str, Any]) -> dict:
        """The task's scenario values. Only scenario-shaped ones (a number, short text, a bool, `{time}` or
        `{sha256}`): one list in a dataset column would otherwise refuse the whole sample at the contract."""
        column = env_extras.get(SCENARIO_COLUMN)
        scenario = dict(column) if isinstance(column, Mapping) else {}
        for name in self._scenario_keys:
            if env_extras.get(name) is not None:
                scenario[name] = env_extras[name]
        return {str(name): value for name, value in scenario.items() if _is_scenario_value(value)}

    def _build_step_turn(self, response_ids: Sequence[int], mask: Any, reward: float | None, *, is_graded: bool) -> dict:
        """A step-wise row as its one turn (`skyrl_gym_generator.py:571-590`): the model's tokens (loss mask 1) and
        the observation after them (0) decoded apart, with the step's own reward."""
        bits = list(mask) if isinstance(mask, (list, tuple)) and len(mask) == len(response_ids) else [1] * len(response_ids)
        messages = []
        if self._decode is not None:
            for is_model, ids in _split_runs(response_ids, bits):
                content = self._decode_text(ids)
                messages.append({"role": "assistant", "source": "model", "is_trainable": True, "content": content}
                                if is_model else {"role": "user", "source": "environment", "content": content})
        turn: dict[str, Any] = {"messages": messages}
        if is_graded and reward is not None:
            turn["reward"] = reward
        return turn

    def _decode_text(self, ids: Sequence[int]) -> str:
        if self._decode is None or not ids:
            return ""
        return str(self._decode(list(ids)))

    def _get_token_arrays(self, output: Mapping[str, Any], row: int, response_ids: Sequence[int]) -> dict | None:
        if not response_ids:
            return None
        arrays: dict[str, list] = {"token_ids": [int(token) for token in response_ids]}
        if self._tokens_to_text is not None:
            arrays["token_text"] = [str(text) for text in self._tokens_to_text(list(response_ids))]
        logprobs = _pick(output, "rollout_logprobs", row)
        if logprobs is not None:
            arrays["inference_logprobs"] = [_to_finite(value) for value in logprobs]
        mask = _pick(output, "loss_masks", row)
        if mask is not None:
            arrays["loss_mask"] = [int(bit) for bit in mask]
        return arrays


def get_trajectories(inputs: Mapping[str, Any], output: Mapping[str, Any]) -> list[tuple[str, int]]:
    """Each output row's (instance_id, repetition_id), as `OutputMapper.map_call` reads them."""
    rows = len(output.get("response_ids") or [])
    trajectory_ids = output.get("trajectory_ids") or inputs.get("trajectory_ids") or []
    found = []
    for row in range(rows):
        trajectory = trajectory_ids[row] if row < len(trajectory_ids) else None
        found.append(get_identity(trajectory) or (str(row), 0))
    return found


def _set_step_grades(parts: list[dict], identities: Sequence[tuple[str, int] | None], last_steps: Any) -> None:
    """Step-wise rows: SkyRL trains every step of a trajectory on its last step's reward and ignores the others
    (`trainer.py:1247-1254`), so each row's grade (reward, or the error that left it ungraded) is its trajectory's
    last row's; a step's own reward stays on its turn. The last row is the one `is_last_step` flags, else the last."""
    flags = last_steps if isinstance(last_steps, (list, tuple)) else []
    rows_of: dict[tuple[str, int], list[int]] = {}
    for index, identity in enumerate(identities):
        if identity is not None:
            rows_of.setdefault(identity, []).append(index)
    for indexes in rows_of.values():
        flagged = [index for index in indexes if index < len(flags) and flags[index]]
        last = parts[(flagged or indexes)[-1]]
        grade = {name: last[name] for name in GRADE_FIELDS if name in last}
        for index in indexes:
            for name in GRADE_FIELDS:
                parts[index].pop(name, None)
            parts[index].update(grade)


def _split_runs(ids: Sequence[int], bits: Sequence[Any]) -> list[tuple[bool, list[int]]]:
    """The response's runs of equal loss-mask bits: (is the model's, token ids), in order."""
    runs: list[tuple[bool, list[int]]] = []
    for token, bit in zip(ids, bits):
        if runs and runs[-1][0] == bool(bit):
            runs[-1][1].append(int(token))
        else:
            runs.append((bool(bit), [int(token)]))
    return runs


def _join_trial(part: dict, trial: Any, segment: int) -> None:
    """A row Harbor ran: the trial's key and task. A broken trial's own part names why, so a placeholder row's
    `stop_reason=error` guess is left out."""
    part["key"] = trial.key if segment == 0 else f"{trial.key}:{segment}"
    part["attempt_key"] = trial.key  # the try's live sample (`TrialResult.id`)
    part["task_key"] = trial.task_key
    part["scenario"] = dict(trial.scenario)
    if trial.has_error and part.get("error_reason") is not None:
        part.pop("error_reason")
        part.pop("error_message", None)


def _get_label(env_extras: Mapping[str, Any]) -> Any:
    """The row's grading spec (`reward_spec`, its `ground_truth` the reference answer), when JSON holds it small."""
    spec = env_extras.get(LABEL_COLUMN)
    if spec is None:
        return None
    try:
        text = json.dumps(spec, ensure_ascii=False)
    except (TypeError, ValueError):
        return None
    return spec if len(text.encode("utf-8")) <= MAX_LABEL_BYTES else None


def _get(target: Any, name: str) -> Any:
    return target.get(name) if isinstance(target, Mapping) else getattr(target, name, None)


def get_identity(trajectory: Any) -> tuple[str, int] | None:
    """A TrajectoryID's (instance_id, repetition_id) (`generators/base.py:16-23`)."""
    instance = _get(trajectory, "instance_id")
    repetition = _get(trajectory, "repetition_id")
    if instance is None:
        return None
    return str(instance), int(repetition or 0)


def _index_inputs(trajectory_ids: Sequence[Any]) -> dict[tuple[str, int], int]:
    found = {}
    for index, trajectory in enumerate(trajectory_ids):
        identity = get_identity(trajectory)
        if identity is not None:
            found.setdefault(identity, index)
    return found


def _get_segments(trajectory_ids: Sequence[Any], rows: int) -> list[tuple[int, int]]:
    """Each step-wise row's (segment, segment_count) within its trajectory, in row order."""
    identities = [get_identity(trajectory_ids[row]) if row < len(trajectory_ids) else None for row in range(rows)]
    totals = Counter(identities)
    seen: Counter = Counter()
    numbered = []
    for identity in identities:
        numbered.append((seen[identity], totals[identity]))
        seen[identity] += 1
    return numbered


def _pick(output: Mapping[str, Any], name: str, row: int) -> Any:
    values = output.get(name)
    if isinstance(values, (list, tuple)) and row < len(values):
        return values[row]
    return None


def read_reward(value: Any) -> tuple[float | None, list[list[float]]]:
    """A row's reward: a number, or a token-level list whose sum is the reward (`trainer.py:1186-1189`)."""
    if isinstance(value, (list, tuple)):
        numbers = [_to_finite(item) for item in value]
        nonzero = [[index, item] for index, item in enumerate(numbers) if item]
        total = sum(item for item in numbers if item is not None)
        return total, nonzero[:MAX_TOKEN_REWARDS]
    number = _to_finite(value)
    return number, []


def _get_numbers(values: Any) -> dict[str, float]:
    if not isinstance(values, Mapping):
        return {}
    return {str(name): float(value) for name, value in values.items() if _to_finite(value) is not None}


def _get_timing(output: Mapping[str, Any], row: int) -> dict:
    """Generation seconds per trajectory, and its engine / environment split when SkyRL recorded one."""
    timing = {}
    total = _to_finite(_pick(output, "trajectory_generation_times", row))
    splits = output.get("trajectory_time_splits")
    if isinstance(splits, Mapping):
        llm = _to_finite(_pick(splits, "llm", row))
        env = _to_finite(_pick(splits, "env", row))
        if llm is not None and llm >= 0:
            timing["generation_s"] = llm
        if env is not None and env >= 0:
            timing["environment_s"] = env
    if "generation_s" not in timing and total is not None and total >= 0:
        timing["generation_s"] = total
    return timing


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
