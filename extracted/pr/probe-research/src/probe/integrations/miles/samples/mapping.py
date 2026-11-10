"""One Miles `Sample` as a generator part for `run.samples.log` (RL plan §6.1 W15): its key, task,
provenance (weight-version spans, scorers), reward, result facts, engine stats and per-token arrays.
Reads by duck typing: upstream `radixark/miles@bb18e6ab7811` and the July fork both fit."""

from __future__ import annotations

import hashlib
import json
import math
import os
import socket
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

#: The generation phases a weight-version span stands for (`types.py:24-42`: `prefill_spans`, `spans`).
PREFILL, DECODE = "prefill", "decode"
#: Miles `Sample.Status` (`utils/types.py:236-245`) as a finish reason, and the error behind a broken one.
FINISH_OF_STATUS = {"completed": "stop", "truncated": "length", "aborted": "abort", "failed": "error"}
ERROR_OF_STATUS = {"aborted": "engine_abort", "failed": "unknown"}
#: Error reasons an agent function may name itself in `metadata["error_reason"]` (`SampleErrorReason`).
ERROR_REASONS = frozenset(
    {"engine_abort", "sandbox", "verifier", "reward_fn", "timeout", "oom", "network", "tool_backend", "unknown"}
)
#: The step a train sample's group began under, stamped by its live try (`../live/`): its group and fully async step.
SCHEDULED_STEP_KEY = "probe_scheduled_step"
_MISSING = object()


@dataclass(frozen=True)
class MappingConfig:
    """What the mapping needs from Miles' args: read once per hook call (`from_args`)."""

    reward_key: str | None = None
    #: Who graded it: `--custom-rm-path`, else `--rm-type`.
    scorer_name: str | None = None
    #: On-policy distillation's teacher (`--opd-teacher-load`, `--opd-teacher-ckpt-step`).
    teacher_load: str | None = None
    teacher_step: int | None = None
    #: `{"metric name": "dotted Sample path"}`: extra per-sample numbers (`--probe-sample-metrics`).
    metric_paths: Mapping[str, str] = field(default_factory=dict)
    run_id: str | None = None

    @classmethod
    def from_args(cls, args: Any, *, metric_paths: Mapping[str, str] | None = None, run_id: str | None = None):
        configured = getattr(args, "probe_sample_metrics", None)
        paths = {**(metric_paths or {}), **(dict(configured) if isinstance(configured, Mapping) else {})}
        step = getattr(args, "opd_teacher_ckpt_step", None)
        return cls(
            reward_key=getattr(args, "reward_key", None) or None,
            scorer_name=_get_text(getattr(args, "custom_rm_path", None)) or _get_text(getattr(args, "rm_type", None)),
            teacher_load=_get_text(getattr(args, "opd_teacher_load", None)),
            teacher_step=step if isinstance(step, int) and not isinstance(step, bool) and step >= 0 else None,
            metric_paths={str(k): str(v) for k, v in paths.items() if isinstance(k, str) and k and v},
            run_id=run_id,
        )


def hash_tokens(tokens: Any) -> str:
    """16 hex characters naming a token sequence, the same for a list, a numpy array or a tensor: the
    trainer side sees the same tokens (`train_data_conversion.py:113`) and nothing else that joins."""
    if hasattr(tokens, "tolist"):
        tokens = tokens.tolist()
    raw = b"".join(int(token).to_bytes(8, "little", signed=True) for token in tokens or ())
    return hashlib.sha256(raw).hexdigest()[:16]


def build_train_key(step: int, index: Any, tokens: Any) -> str:
    """A training sample's producer key, unique per attempt within an epoch. The trainer rank rebuilds
    it from `rollout_id`, `sample_indices` and `tokens` (no `group_index` reaches it); the token digest
    tells apart the leaves one rollout splits into, which share `Sample.index` (`dump_reader.py:79-94`)."""
    return f"train:{step}:{index}:{hash_tokens(tokens)}"


def build_group_key(step: Any, group_index: Any) -> str:
    """A train group's key, `train:{step}:{group_index}`: the live tries and the finished samples name it alike."""
    return f"train:{step}:{group_index}"


def read_scheduled_step(sample: Any) -> int | None:
    """The step its live try stamped (`SCHEDULED_STEP_KEY`), or None (Probe's live wrap was off)."""
    metadata = getattr(sample, "metadata", None)
    step = metadata.get(SCHEDULED_STEP_KEY) if isinstance(metadata, Mapping) else None
    return step if isinstance(step, int) and not isinstance(step, bool) and step >= 0 else None


def get_harbor_key(sample: Any) -> str | None:
    """Harbor's `external_key` when the attempt ran as a Harbor trial: the key both producers derive the
    one sample's id from (RL plan §3.5)."""
    metadata = getattr(sample, "metadata", None)
    key = metadata.get("external_key") if isinstance(metadata, Mapping) else None
    return key if isinstance(key, str) and key else None


def build_generator_part(sample: Any, *, key: str, split: str, step: int, config: MappingConfig,
                         scheduled_step: int | None = None, group_key: str | None = None,
                         drop_reason: str | None = None, events: list[dict] | None = None) -> dict:
    """The generator part for one sample. Raises only on a sample with no shape at all; the caller
    counts that and moves on."""
    metadata = getattr(sample, "metadata", None)
    metadata = metadata if isinstance(metadata, Mapping) else {}
    part: dict[str, Any] = {"key": key, "split": split, **build_task(sample, metadata)}
    attempt_key = metadata.get("probe_attempt_key")  # the live try it came from (rl-next W36, `../live/`)
    if isinstance(attempt_key, str) and attempt_key:
        part["attempt_key"] = attempt_key[:512]
    if scheduled_step is not None:
        part["scheduled_step"] = scheduled_step
    if group_key:
        part["group_key"] = group_key
    _add_lineage(part, sample)
    _add_response(part, sample)
    _add_result(part, sample, metadata, config)
    part["generated_by"] = build_generations(sample)
    part["scored_by"] = build_scorers(sample, config)
    part["metrics"] = read_sample_metrics(sample, metadata, config.metric_paths)
    _add_engine_facts(part, sample, metadata)
    part["extras"] = _build_extras(sample, metadata)
    if drop_reason:
        part["drop_reason"] = drop_reason
    if events:
        part["events"] = events[-256:]
    token_arrays = build_token_arrays(sample)
    if token_arrays:
        part["token_arrays"] = token_arrays
    harbor_key = get_harbor_key(sample)
    if harbor_key and config.run_id:
        from probe.sdk.capture.capture import stable_span_id

        part["trace_span_id"] = stable_span_id(config.run_id, harbor_key)
    return {name: value for name, value in part.items() if value not in (None, [], {})}


def build_task(sample: Any, metadata: Mapping) -> dict:
    """The task fields: `metadata["task_id"]`, else a hash of the prompt, as the key;
    `metadata["scenario"]` as the scenario; the prompt and Miles' `label`."""
    prompt = getattr(sample, "prompt", "")
    text = prompt if isinstance(prompt, str) else json.dumps(prompt, sort_keys=True, default=str)
    task_id = metadata.get("task_id")
    if isinstance(task_id, (str, int)) and not isinstance(task_id, bool) and str(task_id):
        task_key = str(task_id)
    else:
        task_key = "prompt:" + hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:16]
    task: dict[str, Any] = {"task_key": task_key[:512], "prompt": text or None}
    scenario = read_scenario(metadata.get("scenario"))
    if scenario:
        task["scenario"] = scenario
    label = getattr(sample, "label", None)
    if label is not None:
        task["label"] = label if isinstance(label, (str, int, float, bool, list, dict)) else str(label)
    return task


def read_scenario(value: Any) -> dict | None:
    """The scenario as the contract checks it; one Probe cannot store is left out (never the sample)."""
    if not isinstance(value, Mapping) or not value:
        return None
    from probe.generated.samples.task import validate_scenario

    try:
        validate_scenario(dict(value))
    except (ValueError, TypeError):
        return None
    return dict(value)


def read_reward(sample: Any, reward_key: str | None) -> tuple[float | None, dict[str, float]]:
    """The grade and its parts. A dict reward's scalar is `reward_key`'s entry (`types.py:347`), else its
    `"reward"` entry; `metadata["raw_reward"]` overrides it, as Miles' trainer does (conversion :124)."""
    reward = getattr(sample, "reward", None)
    parts: dict[str, float] = {}
    if isinstance(reward, Mapping):
        parts = {str(name): number for name, value in reward.items() if (number := to_number(value)) is not None}
        reward = reward.get(reward_key) if reward_key else reward.get("reward")
    metadata = getattr(sample, "metadata", None)
    if isinstance(metadata, Mapping) and to_number(metadata.get("raw_reward")) is not None:
        reward = metadata["raw_reward"]
    return to_number(reward), parts


def build_generations(sample: Any) -> list[dict]:
    """`generated_by`: upstream's per-call spans with exact token ranges, prefill and decode apart
    (`types.py:24-31`); the fork's version list (`weight_versions: list[str]`), with no ranges."""
    policy_id = _get_text(getattr(sample, "trainer_model_id", None)) or "policy"
    pieces: list[dict] = []
    calls = getattr(sample, "weight_versions", None) or []
    legacy = [call for call in calls if isinstance(call, (str, int))]
    legacy += list(getattr(sample, "legacy_weight_versions", None) or [])
    for call in calls:
        if isinstance(call, (str, int)):
            continue
        for phase, spans in ((PREFILL, getattr(call, "prefill_spans", ())), (DECODE, getattr(call, "spans", ()))):
            for span in spans or ():
                version = _read_version(getattr(span, "version", None))
                start, end = getattr(span, "abs_start", None), getattr(span, "abs_end", None)
                if version is None or not isinstance(start, int) or not isinstance(end, int) or end <= start:
                    continue
                pieces.append(_make_piece(version, policy_id, phase, start, end - 1))
    for version in dict.fromkeys(v for v in map(_read_version, legacy) if v is not None):
        pieces.append(_make_piece(version, policy_id, DECODE, None, None))
    return pieces


def build_scorers(sample: Any, config: MappingConfig) -> list[dict]:
    """Who graded it: the reward function, and the OPD teacher when the sample carries teacher scores."""
    scorers = []
    spec = getattr(sample, "reward_spec", None)
    name = _get_text(getattr(spec, "custom_rm_path", None)) or _get_text(getattr(spec, "rm_type", None))
    name = name or config.scorer_name
    if name:
        scorers.append({"name": name[:256], "kind": "verifier"})
    has_teacher = getattr(sample, "teacher_log_probs", None) is not None or getattr(sample, "opd_reverse_kl", None) is not None
    if has_teacher and config.teacher_load:
        model = {"kind": "checkpoint", "uri": config.teacher_load[:2048]}
        if config.teacher_step is not None:
            model["step"] = config.teacher_step
        scorers.append({"name": "opd_teacher", "kind": "teacher", "model": model})
    return scorers


def read_sample_metrics(sample: Any, metadata: Mapping, paths: Mapping[str, str]) -> dict[str, float]:
    """Per-sample numbers: `metadata["probe_metrics"]`, then the configured paths (they win)."""
    metrics: dict[str, float] = {}
    declared = metadata.get("probe_metrics")
    for name, value in (declared.items() if isinstance(declared, Mapping) else ()):
        if isinstance(name, str) and name and (number := to_number(value)) is not None:
            metrics[name] = number
    for name, path in paths.items():
        value = read_path(sample, path)
        if value is not _MISSING and (number := to_number(value)) is not None:
            metrics[name] = number
    kl = getattr(sample, "opd_reverse_kl", None)
    if kl is not None and (values := [number for value in kl if (number := to_number(value)) is not None]):
        metrics["opd/reverse_kl_mean"] = sum(values) / len(values)
    return metrics


def build_token_arrays(sample: Any) -> dict | None:
    """The rollout side's per-token arrays over the response: ids, inference logprobs, loss mask and
    top-k candidates (-inf pads become null). The SDK bundles them and computes the summaries."""
    length = getattr(sample, "response_length", 0) or 0
    tokens = getattr(sample, "tokens", None)
    if not length or tokens is None:
        return None
    ids = to_list(tokens)[-length:]
    arrays: dict[str, Any] = {"token_ids": [int(token) for token in ids]}
    for name, attr in (("inference_logprobs", "rollout_log_probs"), ("loss_mask", "loss_mask"),
                       ("top_k_ids", "rollout_topk_token_ids"), ("top_k_logprobs", "rollout_topk_log_probs")):
        value = getattr(sample, attr, None)
        if value is not None:
            arrays[name] = to_finite_lists(to_list(value))
    return arrays


def build_events(raw: Iterable[Mapping]) -> list[dict]:
    """Miles' trajectory events (`dashboard/store.py:167-190`) as `SampleEvent`s."""
    kinds = {"attempt_start": "attempt_start", "attempt_end": "attempt_end", "gen_start": "generation_start",
             "gen_end": "generation_end", "tool_start": "tool_start", "tool_end": "tool_end"}
    events = []
    for event in raw:
        kind = kinds.get(str(event.get("kind")))
        at = to_number(event.get("ts"))
        if kind is None or at is None:
            continue
        item: dict[str, Any] = {"kind": kind, "at": datetime.fromtimestamp(at, tz=timezone.utc).isoformat()}
        turn = event.get("turn")
        if isinstance(turn, int) and not isinstance(turn, bool) and turn >= 0:
            item["turn"] = turn
        if (version := _read_version(event.get("weight_version"))) is not None:
            item["weight_version"] = version
        if detail := _get_text(event.get("detail")):
            item["detail"] = detail[:1024]
        events.append(item)
    return events


def to_number(value: Any) -> float | None:
    """A finite float, or None (bools, NaN, inf and non-numbers are not numbers here)."""
    if hasattr(value, "item") and callable(value.item):
        try:
            value = value.item()
        except (TypeError, ValueError, RuntimeError):
            return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def to_list(value: Any) -> list:
    return value.tolist() if hasattr(value, "tolist") else list(value)


def to_finite_lists(values: list) -> list:
    """Nested numbers with -inf / NaN as None: JSON cannot carry them."""
    return [to_finite_lists(v) if isinstance(v, list) else (v if isinstance(v, int) else to_number(v)) for v in values]


def read_path(sample: Any, path: str) -> Any:
    """A dotted path across attributes and mapping keys (`metadata.agent_metrics.turns`)."""
    value: Any = sample
    for name in path.split("."):
        if not name:
            return _MISSING
        value = value.get(name, _MISSING) if isinstance(value, Mapping) else getattr(value, name, _MISSING)
        if value is _MISSING:
            return _MISSING
    return value


def get_status(sample: Any) -> str:
    status = getattr(sample, "status", None)
    return str(getattr(status, "value", status) or "").lower()


def _add_lineage(part: dict, sample: Any) -> None:
    lineage = getattr(sample, "lineage", None)
    index, count = getattr(lineage, "output_index", None), getattr(lineage, "output_count", None)
    if isinstance(index, int) and isinstance(count, int) and count >= 1:
        part.update(segment=index, segment_count=count)


def _add_response(part: dict, sample: Any) -> None:
    response = getattr(sample, "response", None)
    if isinstance(response, str) and response:
        part["response"] = response
    length = getattr(sample, "response_length", None)
    tokens = getattr(sample, "tokens", None)
    if isinstance(length, int) and length >= 0:
        part["response_tokens"] = length
        if tokens is not None and len(tokens) >= length:
            part["prompt_tokens"] = len(tokens) - length
    finish = FINISH_OF_STATUS.get(get_status(sample))
    if finish:
        part["finish_reason"] = finish


def _add_result(part: dict, sample: Any, metadata: Mapping, config: MappingConfig) -> None:
    """Reward, parts and the error facts the server derives `result` from: ABORTED is an engine abort,
    FAILED names its own reason or `unknown`; a finished sample nothing graded is a reward-function error."""
    reward, parts = read_reward(sample, config.reward_key)
    part["reward"], part["reward_parts"] = reward, parts
    status = get_status(sample)
    reason = ERROR_OF_STATUS.get(status)
    named = metadata.get("error_reason")
    if reason == "unknown" and isinstance(named, str) and named in ERROR_REASONS:
        reason = named
    if reason is None and reward is None and status in ("completed", "truncated"):
        reason = "reward_fn"
    if reason is not None:
        part["error_reason"] = reason
        message = _get_text(metadata.get("error")) or _get_text(metadata.get("exception"))
        part["error_message"] = message or f"Miles sample status {status or 'unknown'}"


def _add_engine_facts(part: dict, sample: Any, metadata: Mapping) -> None:
    stats: dict[str, float] = {}
    spec = getattr(sample, "spec_info", None)
    proposed = getattr(spec, "spec_num_proposed_drafts", getattr(spec, "spec_draft_token_num", 0))
    if spec is not None and proposed and (rate := to_number(getattr(spec, "spec_accept_rate", None))) is not None:
        stats["spec_accept_rate"] = min(1.0, max(0.0, rate))
    cache = getattr(sample, "prefix_cache_info", None)
    if getattr(cache, "total_prompt_tokens", 0) and (rate := to_number(getattr(cache, "prefix_cache_hit_rate", None))) is not None:
        stats["prefix_cache_hit_rate"] = min(1.0, max(0.0, rate))
    non_generation = to_number(getattr(sample, "non_generation_time", None))
    if non_generation is not None and non_generation > 0:
        stats["non_generation_s"] = non_generation
    part["engine_stats"] = stats
    part["host"], part["worker"] = HOST, _get_worker()
    if sandbox := _get_text(metadata.get("sandbox_id")):
        part["sandbox_id"] = sandbox[:256]
    segments = metadata.get("lifecycle")
    segments = [s for s in (segments if isinstance(segments, list) else [segments]) if isinstance(s, Mapping)]
    if segments:
        part["turn_count"] = len(segments)
        part["timing"] = _build_timing(segments)
    prompt = getattr(sample, "prompt", None)
    if isinstance(prompt, list):
        part["tool_call_count"] = sum(1 for m in prompt if isinstance(m, Mapping) and m.get("role") == "tool")


def _build_timing(segments: list[Mapping]) -> dict | None:
    starts = [at for segment in segments if (at := to_number(segment.get("t0"))) is not None]
    ends = [at for segment in segments if (at := to_number(segment.get("t1"))) is not None]
    spans = [t1 - t0 for s in segments if (t0 := to_number(s.get("t0"))) is not None
             and (t1 := to_number(s.get("t1"))) is not None and t1 >= t0]
    timing: dict[str, Any] = {}
    if starts:
        timing["started_at"] = datetime.fromtimestamp(min(starts), tz=timezone.utc).isoformat()
    if ends:
        timing["ended_at"] = datetime.fromtimestamp(max(ends), tz=timezone.utc).isoformat()
    if spans:
        timing["generation_s"] = sum(spans)
    return timing or None


def _build_extras(sample: Any, metadata: Mapping) -> dict:
    extras: dict[str, Any] = {}
    if model := _get_text(getattr(sample, "trainer_model_id", None)):
        extras["trainer_model_id"] = model
    if getattr(sample, "remove_sample", False) is True:
        extras["remove_sample"] = True
    execution = getattr(sample, "rollout_id", None)
    if isinstance(execution, int) and not isinstance(execution, bool):
        extras["rollout_execution_id"] = execution
    if (group := getattr(sample, "group_index", None)) is not None:
        extras["group_index"] = group if isinstance(group, int) else str(group)
    if (index := getattr(sample, "index", None)) is not None:
        extras["sample_index"] = index if isinstance(index, int) else str(index)
    retry_of = metadata.get("probe_retry_of")  # a retry's try names the one it replaced
    if isinstance(retry_of, str) and retry_of:
        extras["retry_of"] = retry_of[:512]
    return extras


def _make_piece(version: int, policy_id: str, phase: str, first: int | None, last: int | None) -> dict:
    piece: dict[str, Any] = {"model": {"kind": "policy", "version": version, "policy_id": policy_id[:128]},
                             "phase": phase}
    if first is not None and last is not None:
        piece.update(first_token=first, last_token=last)
    return piece


def _read_version(value: Any) -> int | None:
    """Miles' versions are digit strings (`compute_numeric_versions_of_spans`, types.py:153); others are skipped."""
    text = str(value) if value is not None else ""
    return int(text) if text.isdigit() else None


def _get_text(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _get_worker() -> str:
    """The Ray actor this runs in, else the process."""
    ray = sys.modules.get("ray")
    try:
        actor = ray.get_runtime_context().get_actor_id() if ray is not None and ray.is_initialized() else None
    except Exception:  # noqa: BLE001 -- a label, never a reason to fail
        actor = None
    return f"actor:{actor}" if actor else f"pid:{os.getpid()}"


HOST = socket.gethostname()[:256]
