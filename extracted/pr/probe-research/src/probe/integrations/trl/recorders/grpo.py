"""GRPO and RLOO samples (RL plan §6.6): every `_generate_and_score_completions` call's rows, read from the entries it
just appended to `self._logs` (gathered from every process, as TRL logs them), so nothing depends on `log_completions`
or `logging_steps`. Line refs are `huggingface/trl@4ae4d34a86f3` `trl/trainer/grpo_trainer.py`."""

from __future__ import annotations

import functools
from collections.abc import Mapping, Sequence
from typing import Any

from probe.generated.samples import CaptureField
from probe.sdk.run.samples.rollout import RolloutCapture
from probe.sdk.run.samples.tokens import summarize_tokens

from ..harbor import is_harbor_env, make_harbor_scorer, read_harbor_task
from ..live import LiveBatch
from ..recorder import Recorder
from ..tool_rollouts import ToolRollouts
from ..rows import (
    MAX_SCENARIO_TEXT,
    TOOL_FIELDS,
    build_completion,
    has_response_schema,
    make_prompt_key,
    pick_rows,
    render_prompt,
    split_extras,
    to_finite,
    to_ints,
    to_numbers,
)

#: The column this adapter adds through TRL's own `log_extra` door (`_log_completion_extra`, `:1634-1643`), so each
#: row's task facts ride TRL's gather (`:2969-2975`) from every process; taken out again before TRL logs a table.
ROW_COLUMN = "_probe_row"
#: A completion every reward function returned None for: TRL leaves it unscored and zeroes its advantage (`:2852`).
UNSCORED = "reward_fn: no reward function scored this completion"
#: Where a `rollout_func`'s own fields ride a row's facts (`_generate` returns them, `:2320`, `:2435`).
ROLLOUT_FIELDS = "rollout_fields"
#: Where a row's facts carry the tools TRL runs as coroutines for it: their results come after the sync ones (O1).
#: Always set, so a row without facts (unknown tools) links no reply TRL may have reordered.
ASYNC_TOOLS = "async_tools"
#: Where a row's facts carry its async calls that raised when TRL called them: their results come with the sync ones.
#: Set on every process whose tools were watched; a row without it links no reply holding an async call.
FAILED_ASYNC_CALLS = "failed_async_calls"
#: What GRPO cannot give a sample (`plan(unsupported=)`), and why. TRL's parser names no tool call (`parse_response`).
NUMBERED_IDS = ("TRL's parser gives tool calls no id: Probe numbers them probe-<turn>-<i> and links each result by "
                "TRL's own order (sync and failed calls first, then async ones), checked by tool name")
NO_SCHEMA = ("the tokenizer has no response schema, so TRL decodes each completion as plain text: no tool calls, "
             "no reasoning apart from the content")
RLOO_TEXT = "RLOO decodes each completion as plain text: no tool calls, no reasoning apart from the content"
PLAIN_TEXT = ("this run's dataset is plain text, not conversational: TRL keeps each completion as one string, with no "
              "messages, tool calls, tools run or reasoning apart from the text")
OTHER_RANKS = ("only the main process records: tools on the other ranks run where Probe has no run, so their "
               "samples carry no files")


class GrpoRecorder(Recorder):
    """`_generate` (unpadded token lists, the rows' task facts) and `_generate_and_score_completions` (the logged
    rows, the per-token tensors) on this trainer instance."""

    names = ("GRPOTrainer", "RLOOTrainer")

    def __init__(self, tracker: Any) -> None:
        super().__init__(tracker)
        self._inputs: Sequence[Any] = ()
        self._generated: tuple | None = None
        self._scorers: list[dict] | None = None
        #: The extra columns this call's reward functions logged: an older column's deque still ends in old rows.
        self._columns: set[str] = set()
        #: This call's live samples (`live.py`), and each row's task facts read once (`_read_facts`).
        self._live = LiveBatch()
        self._facts: dict[int, tuple[Any, dict]] = {}
        #: This call's rows' tool calls, each inside its sample's rollout capture (sync GRPO, main process).
        self._tool_rollouts = ToolRollouts()
        self._call_prefix: str | None = None
        self._is_plain_text_declared = False

    def get_unsupported(self) -> dict[CaptureField, str]:
        """GRPO: call ids are Probe's, and without a response schema TRL keeps no tool calls or reasoning; with
        several processes only the main one's samples carry files. RLOO decodes plain text."""
        trainer = self.trainer
        if any(cls.__name__ == "RLOOTrainer" for cls in type(trainer).__mro__):
            return {**dict.fromkeys(TOOL_FIELDS, RLOO_TEXT), CaptureField.REASONING: RLOO_TEXT}
        tokenizer = getattr(trainer, "_tokenizer", None) or self.tracker.get_tokenizer()
        if not has_response_schema(tokenizer):
            unsupported = dict.fromkeys((CaptureField.TOOL_CALL_IDS, CaptureField.TOOL_CALL_ARGUMENTS,
                                         CaptureField.TOOL_RESULT_LINKS, CaptureField.REASONING), NO_SCHEMA)
        else:
            unsupported = {CaptureField.TOOL_CALL_IDS: NUMBERED_IDS}
        if int(getattr(getattr(trainer, "accelerator", None), "num_processes", 1) or 1) > 1:
            unsupported[CaptureField.ENVIRONMENT_FILES] = OTHER_RANKS
        return unsupported

    def _send_plain_text_plan(self, completions: Sequence[Any]) -> None:
        """The first string completion of a training row (a plain-text training dataset; an eval set's own shape
        says nothing of it): no field but the text can be held. Re-declared whole, as a producer's map replaces its
        earlier one."""
        if self._is_plain_text_declared or not any(isinstance(completion, str) for completion in completions):
            return
        self._is_plain_text_declared = True
        self.tracker.samples.plan(unsupported=dict.fromkeys(CaptureField, PLAIN_TEXT))

    def install(self) -> None:
        trainer = self.trainer
        generate = trainer._generate
        calculate = trainer._calculate_rewards
        score = trainer._generate_and_score_completions
        guard = self.tracker.guard

        @functools.wraps(generate)
        def call_generate(prompts: Any, *args: Any, **kwargs: Any) -> Any:
            # A start that fails leaves this batch unwatched (its links refused), never the last batch's failures.
            self._tool_rollouts.reset()
            guard.call("a rollout's files", self._start_tool_rollouts, len(prompts))
            result = generate(prompts, *args, **kwargs)
            guard.call("a generation", self._record_generation, prompts, result)
            return result

        @functools.wraps(calculate)
        def call_calculate(*args: Any, **kwargs: Any) -> Any:
            guard.call("a live sample", self._live.mark_scoring)
            result = calculate(*args, **kwargs)
            self._columns = set(getattr(trainer, "_pending_extra_logs", None) or ())  # flushed right after (`:2972`)
            return result

        @functools.wraps(score)
        def call_score(inputs: Any, *args: Any, **kwargs: Any) -> Any:
            self._inputs, self._generated, self._columns, self._facts = inputs, None, set(), {}
            step = self.tracker.get_step()
            split = "train" if getattr(trainer.model, "training", True) else "eval"
            call = self.tracker.take_call(split, step)
            self._call_prefix = f"{split}:{step}:{call}"
            self._live = guard.call("a live sample", self._start_live, inputs, step, split, call) or LiveBatch()
            try:
                output = score(inputs, *args, **kwargs)
            except BaseException as exc:
                guard.call("a live sample", self._live.end_rest, exc)
                raise
            guard.call("a generation batch", self._record, inputs, output, step, split, call)
            guard.call("a live sample", self._live.end_rest)
            return output

        self.tracker.install(trainer, "_generate", call_generate)
        self.tracker.install(trainer, "_calculate_rewards", call_calculate)
        self.tracker.install(trainer, "_generate_and_score_completions", call_score)

    # -- every process -----------------------------------------------------------------------------------------
    def _record_generation(self, prompts: Sequence[Any], result: Sequence[Any]) -> None:
        """Keep this process's unpadded lists (GRPO returns 9 values, `:2425`; RLOO 3) and hand each row's task facts
        to TRL's extra-column gather: the main process then has them for every process's rows."""
        prompt_ids, completion_ids = result[0], result[1]
        is_grpo = len(result) >= 9
        self._generated = (completion_ids, result[2] if is_grpo else None, result[4] if is_grpo else None)
        rollout_fields = result[6] if is_grpo and isinstance(result[6], Mapping) else {}
        trainer = self.trainer
        environments = getattr(trainer, "environments", None) or []
        stops = set(getattr(trainer, "eos_token_ids", None) or ())
        stops.add(getattr(getattr(trainer, "_tokenizer", None), "pad_token_id", None))
        sync_dicts = getattr(trainer, "_sync_tool_dicts", None) or []  # this call's, built before `_generate` (:2480)
        async_dicts = getattr(trainer, "_async_tool_dicts", None) or []
        facts = []
        for index, ids in enumerate(completion_ids):
            row = self._inputs[index] if index < len(self._inputs) else {}
            row_prompt = row.get("prompt") if isinstance(row, Mapping) else None
            prompt = row_prompt if render_prompt(row_prompt).strip() else prompts[index]
            fact = self._read_facts(index, row, prompt, environments)
            fact["prompt_tokens"] = len(prompt_ids[index])
            fact["response_tokens"] = len(ids)
            fields = _pick_rollout_fields(rollout_fields, index)
            if fields:
                fact[ROLLOUT_FIELDS] = fields
            fact["finish_reason"] = "length" if len(ids) and ids[-1] not in stops else "stop"  # `:2401-2403`
            fact[ASYNC_TOOLS] = _get_async_names(sync_dicts, async_dicts, index)
            failed = self._tool_rollouts.get_failed_async_calls(index)
            if failed is not None:
                fact[FAILED_ASYNC_CALLS] = failed
            facts.append(fact)
        log_extra = getattr(trainer, "_log_completion_extra", None)
        if callable(log_extra):
            log_extra(ROW_COLUMN, facts)

    def _start_tool_rollouts(self, count: int) -> None:
        """This process's rows' tools, watched on every process for the async calls that fail when called (every
        row's result links need them); on the main process with an open run each also runs inside its sample's
        rollout capture (keyed as `_record` keys it), so a tool's `probe.samples.attach_file` reaches its sample."""
        run = self.tracker.run if self._call_prefix is not None and self.tracker.is_recording() else None
        process = int(getattr(self.trainer.accelerator, "process_index", 0) or 0)
        self._tool_rollouts.start(self.trainer, run,
                                  [f"{self._call_prefix}:{process}:{position}" for position in range(count)])  # fmt: skip

    def _read_facts(self, index: int, row: Any, prompt: Any, environments: Sequence[Any]) -> dict:
        """One row's task facts: the dataset's, read once per call (the live start and the generation share them, so
        an image is hashed once), then a Harbor environment's task identity over them (known once it was reset)."""
        found = self._facts.get(index)
        if found is None or found[0] is not prompt:
            found = self._facts[index] = (prompt, self.tracker.rows.read_task(row, prompt))
        fact = dict(found[1])
        environment = environments[index] if index < len(environments) else None
        if environment is not None and is_harbor_env(environment):
            harbor = read_harbor_task(environment)
            digest = harbor.pop("task_digest", None)
            fact.update(harbor)
            if digest:  # the connector's task identity: the same folder is the same task on every door
                fact["scenario"] = {**(fact.get("scenario") or {}), "task_digest": digest}
        return fact

    def _start_live(self, inputs: Sequence[Any], step: int, split: str, call: int) -> LiveBatch:
        """The main process's rows as live samples, keyed as `_record` keys them, before TRL generates."""
        if not self.tracker.is_main:
            return LiveBatch()
        trainer = self.trainer
        process = int(getattr(trainer.accelerator, "process_index", 0) or 0)
        group_size = self._get_group_size(split)
        seal_step = step + 1 if split == "train" else step
        environments = getattr(trainer, "environments", None) or []
        prefix = f"{split}:{step}:{call}"
        starts = []
        for position, row in enumerate(inputs):
            prompt = row.get("prompt") if isinstance(row, Mapping) else None
            fact = self._read_facts(position, row, prompt, environments)
            index = process * len(inputs) + position
            starts.append({"key": f"{prefix}:{process}:{position}", "task_key": fact["task_key"],
                           "scenario": fact.get("scenario") or {}, "group_key": f"{prefix}:g{index // group_size}",
                           "scheduled_step": seal_step, "weight_version": step, "host": self.tracker.host})
        return self.tracker.start_live(starts)

    def _get_group_size(self, split: str) -> int:
        trainer = self.trainer
        return int((trainer.num_generations if split == "train" else
                    getattr(trainer, "num_generations_eval", None) or trainer.num_generations) or 1)

    def _record(self, inputs: Sequence[Any], output: Mapping[str, Any], step: int, split: str, call: int) -> None:
        logs = self.trainer._logs
        row_facts = logs["extra"].pop(ROW_COLUMN, None)
        if not self.tracker.is_recording():
            return
        accelerator = self.trainer.accelerator
        local = len(inputs)
        # TRL itself slices the gathered rows as process_index * len(prompts) (`:2908-2911`): equal shards.
        wanted = local * int(getattr(accelerator, "num_processes", 1) or 1)
        prompts = pick_rows(logs["prompt"], wanted)
        if len(prompts) < wanted:
            self.tracker.guard.record_failure(
                "a generation batch", ValueError(f"TRL's log buffer held {len(prompts)} of {wanted} rows")
            )
        count = len(prompts)
        offset = wanted - count
        completions = pick_rows(logs["completion"], count)
        if split == "train":
            self.tracker.guard.call("what TRL cannot capture", self._send_plain_text_plan, completions)
        rewards = {name: pick_rows(values, count) for name, values in logs["rewards"].items()}
        advantages = pick_rows(logs["advantages"], count)
        extras = {name: pick_rows(values, count) for name, values in logs["extra"].items()
                  if name in self._columns and name != ROW_COLUMN}
        facts = pick_rows(row_facts, count)
        trainer = self.trainer
        group_size = self._get_group_size(split)
        seal_step = step + 1 if split == "train" else step
        until = self.tracker.get_window_end(
            step, int(getattr(trainer.args, "steps_per_generation", 1) or 1) * int(getattr(trainer, "num_iterations", 1) or 1)
        )
        process = int(getattr(accelerator, "process_index", 0) or 0)
        parts: list[dict] = []
        groups: dict[str, dict] = {}
        for position in range(count):
            index = offset + position
            fact = facts[position] if position < len(facts) and isinstance(facts[position], Mapping) else {}
            prefix = f"{split}:{step}:{call}"
            key = f"{prefix}:{index // local}:{index % local}"
            part = self._map_row(
                fact, prompts[position], completions[position],
                {name: values[position] for name, values in rewards.items() if position < len(values)},
                advantages[position] if position < len(advantages) else None,
                {name: values[position] for name, values in extras.items() if position < len(values)},
            )
            part.update(key=key, group_key=f"{prefix}:g{index // group_size}", split=split, scheduled_step=seal_step,
                        generated_by=[{"model": {"kind": "policy", "version": step}}])
            if int(getattr(accelerator, "num_processes", 1) or 1) > 1:
                part["worker"] = f"rank{index // local}"
            arrays = self._get_token_arrays(index % local, output) if index // local == process else None
            if arrays is not None:
                part["token_arrays"] = arrays[0]
            if index // local == process:
                RolloutCapture.update_part(part, self.tracker.guard.call(
                    "a rollout's files", self._tool_rollouts.finish, index % local))  # fmt: skip
            self._live.link(part)
            parts.append(part)
            groups.setdefault(part["group_key"], {
                "group_key": part["group_key"], "size": group_size, "task_key": part["task_key"],
                "scenario": part["scenario"], "scheduled_step": seal_step,
            })
            if split == "train":
                consumption: dict[str, Any] = {"key": key, "role": "trainer", "consumed_step": step + 1,
                                               "consumed_until_step": until, "consumed_version": step}
                if arrays is not None and arrays[1]:
                    consumption["trainer_token_arrays"] = arrays[1]
                    stats = summarize_tokens({**arrays[0], **arrays[1]})
                    if stats:
                        consumption["token_stats"] = stats
                parts.append(consumption)
        self.tracker.send(parts, seal_step, list(groups.values()))
        self._live.end(parts)

    # -- one row -------------------------------------------------------------------------------------------------
    def _map_row(self, fact: Mapping[str, Any], prompt: Any, completion: Any, rewards: Mapping[str, Any],
                 advantage: Any, extras: Mapping[str, Any]) -> dict:
        part: dict[str, Any] = {
            "task_key": str(fact.get("task_key") or make_prompt_key(prompt)),
            "scenario": dict(fact.get("scenario") or {}),
            "prompt": render_prompt(prompt),
            **build_completion(completion, async_tools=fact.get(ASYNC_TOOLS),
                               failed_async_calls=fact.get(FAILED_ASYNC_CALLS)),
            "host": self.tracker.host,
        }
        for name in ("label", "finish_reason", "prompt_tokens", "response_tokens", "environment_type"):
            if fact.get(name) is not None:
                part[name] = fact[name]
        parts = {str(name): value for name, value in ((name, to_finite(value)) for name, value in rewards.items())
                 if value is not None}
        weights = self._get_reward_weights()
        if parts:
            part["reward_parts"] = parts
            part["reward"] = sum(parts[name] * weights.get(name, 1.0) for name in parts)  # TRL's `reward` (`:2945`)
        else:
            part["error_reason"], part["error_message"] = "reward_fn", UNSCORED
        normalized = to_finite(advantage)
        if normalized is not None:
            part["normalized_reward"] = normalized
        numbers, others = split_extras({**(fact.get(ROLLOUT_FIELDS) or {}), **extras})
        if numbers:
            part["metrics"] = numbers
        if others:
            part["extras"] = {**(part.get("extras") or {}), **others}
        part["scored_by"] = [make_harbor_scorer()] if fact.get("scorer") else self._get_scorers()
        return part

    def _get_token_arrays(self, row: int, output: Mapping[str, Any]) -> tuple[dict, dict] | None:
        """This process's row as per-token arrays: the generator's (token ids and text, vLLM's sampling logprobs)
        and the trainer's (logprobs before the update, the reference's, the loss mask), cut to the completion."""
        if self._generated is None:
            return None
        completion_ids, tool_masks, logprobs = self._generated
        if row >= len(completion_ids):
            return None
        ids = to_ints(completion_ids[row])
        length = len(ids)
        generator: dict[str, Any] = {"token_ids": ids}
        text = self.tracker.decode_tokens(ids)
        if text is not None:
            generator["token_text"] = text
        if logprobs is not None and row < len(logprobs) and logprobs[row] is not None:
            generator["inference_logprobs"] = to_numbers(logprobs[row])[:length]
        trainer: dict[str, Any] = {}
        mask = output.get("completion_mask")
        if mask is not None:
            values = to_ints(mask[row][:length])
            tools = output.get("tool_mask")
            if tools is not None:
                values = [value * tool for value, tool in zip(values, to_ints(tools[row][:length]))]
            trainer["loss_mask"] = values
        for source, name in (("old_per_token_logps", "trainer_logprobs"), ("ref_per_token_logps", "ref_logprobs")):
            if output.get(source) is not None:
                trainer[name] = to_numbers(output[source][row][:length])
        return generator, trainer

    def _get_reward_weights(self) -> dict[str, float]:
        names = list(getattr(self.trainer, "reward_func_names", None) or [])
        weights = getattr(self.trainer, "reward_weights", None)
        values = to_numbers(weights) if weights is not None else []
        return {name: (value if value is not None else 1.0) for name, value in zip(names, values)}

    def _get_scorers(self) -> list[dict]:
        """One scorer per reward function: a model is a reward model (by its Hub name), a function a verifier."""
        if self._scorers is None:
            scorers = []
            for name, function in zip(getattr(self.trainer, "reward_func_names", None) or [],
                                      getattr(self.trainer, "reward_funcs", None) or []):
                config = getattr(function, "config", None)
                scorer: dict[str, Any] = {"name": str(name)[:256], "kind": "reward_model" if config else "verifier"}
                path = getattr(config, "_name_or_path", None)
                if isinstance(path, str) and path:
                    scorer["model"] = {"kind": "external", "name": path[:512]}
                scorers.append(scorer)
            self._scorers = scorers
        return list(self._scorers)


def _get_async_names(sync_dicts: Sequence[Any], async_dicts: Sequence[Any], index: int) -> list[str]:
    """The names TRL runs as coroutines for completion ``index``: its async tools a sync tool of the same name does
    not shadow (TRL looks a name up in the sync dict first, `:2069-2072`)."""
    sync_tools = sync_dicts[index] if index < len(sync_dicts) else None
    async_tools = async_dicts[index] if index < len(async_dicts) else None
    if not isinstance(async_tools, Mapping):
        return []
    shadowed = sync_tools if isinstance(sync_tools, Mapping) else {}
    return sorted(str(name) for name in async_tools if name not in shadowed)


def _pick_rollout_fields(fields: Mapping[str, Any], row: int) -> dict[str, Any]:
    """One completion's `rollout_func` fields as TRL hands them to the reward functions (a list holds one value per
    completion, anything else is every row's, `:2871-2878`): numbers, booleans and short text only, the rest (a
    per-token list) dropped before TRL gathers the facts."""
    picked: dict[str, Any] = {}
    for name, values in fields.items():
        value = (values[row] if row < len(values) else None) if isinstance(values, list) else values
        if isinstance(value, bool) or (isinstance(value, str) and len(value) <= MAX_SCENARIO_TEXT):
            picked[str(name)] = value
        elif (number := to_finite(value)) is not None:
            picked[str(name)] = number
    return picked
