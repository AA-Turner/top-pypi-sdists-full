"""`probe.integrations.trl.track(trainer)`: a TRL trainer's samples on its Probe run (RL plan §6.6), beside the metrics
`report_to="probe"` already records. Instance methods only, never a class; every hook fails open. DESIGN.md. Line
refs are `huggingface/trl@4ae4d34a86f3` and transformers 5.22."""

from __future__ import annotations

import functools
import os
import socket
import weakref
from collections import Counter, defaultdict
from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from probe.foundation.safe_warn import safe_warn as _diagnostics

from .. import _rl_owner
from .._live import LiveAttempts, refuse_commands
from .callback import TrlCallback
from .live import COMMAND_REFUSAL, LiveBatch
from .recorders import pick_recorder
from .rows import CollatedRows, RowReader, ScenarioSpec, make_prompt_key, read_labeled_rows
from .run_key import KEY_FILE, KEY_FOLDER, KEY_PREFIX, RunKey, find_legacy_parent, make_run_key
from .runs import drop_wandb, get_config, get_identity, get_rewind_step, get_teacher_ref, read_resume_step

#: The producer a TRL process writes samples as: generation and training share one process.
PRODUCER = "trl"

_TRACKERS: dict[int, tuple[weakref.ref, TrlTracker]] = {}
#: An attribute an instance did not hold before a wrap went on it.
_MISSING = object()


def track(
    trainer: Any,
    scenario: ScenarioSpec = None,
    record_sft: bool = False,
    *,
    teacher: Any = None,
    sft_generated_by: Any = None,
    reward_max: float | None = None,
    **init_kwargs: Any,
) -> TrlTracker:
    """Record ``trainer``'s samples on Probe: GRPO / RLOO completions, AsyncGRPO's queue, distillation (Distillation,
    ServerDistillation, GKD, GOLD, AsyncDistillation) and, with ``record_sft``, each SFT example once. ``scenario`` names
    the dataset columns that pose a task (or is a callable ``row -> dict``); a `task_id` column keys the task.
    ``teacher`` names a distillation teacher (`probe.samples.generated_by(...)`, `checkpoint:<run>@step<N>`);
    ``sft_generated_by`` names who wrote the SFT examples. Other keywords go to `probe.init()`. W&B in `report_to`
    is dropped with a warning: Probe records without it."""
    from probe.sdk.settings.settings import Mode, resolve_mode

    if resolve_mode(None) is Mode.DISABLED:
        return TrlTracker(trainer, is_enabled=False)
    found = _TRACKERS.get(id(trainer))
    tracker = found[1] if found is not None and found[0]() is trainer else None
    if tracker is not None and not tracker.is_finished:
        return tracker
    tracker = TrlTracker(
        trainer, scenario=scenario, should_record_sft=record_sft, teacher=teacher, sft_generated_by=sft_generated_by,
        reward_max=reward_max, init_kwargs=init_kwargs,
    )
    _TRACKERS[id(trainer)] = (weakref.ref(trainer), tracker)
    return tracker


class TrlTracker:
    """One TRL trainer's Probe samples. The world-zero process owns the record, as TRL logs from there; every hook
    fails open (`HookGuard`), so TRL's own call always runs with its arguments."""

    def __init__(
        self,
        trainer: Any,
        *,
        scenario: ScenarioSpec = None,
        should_record_sft: bool = False,
        teacher: Any = None,
        sft_generated_by: Any = None,
        reward_max: float | None = None,
        init_kwargs: Mapping[str, Any] | None = None,
        is_enabled: bool = True,
    ) -> None:
        self.trainer = trainer
        self.rows = RowReader(scenario)
        #: GKD and GOLD: the dataset row behind each collated row (`remember_collated_rows`).
        self.collated = CollatedRows()
        self.guard = _rl_owner.HookGuard("TRL")
        self.teacher = teacher
        self.sft_generated_by = sft_generated_by
        self.host = socket.gethostname()
        self.run: Any = None
        self.samples: Any = None
        #: This producer's running samples (`live.LiveBatch`), once the run is open.
        self.live: LiveAttempts | None = None
        self.recorder: Any = None
        self.floor = 0
        #: `training_step` calls since the last optimizer step: where a generation sits inside its step.
        self.micro_index = 0
        self.max_staleness: int | None = None
        self.is_finished = not is_enabled
        self._should_record_sft = should_record_sft
        self._reward_max = reward_max
        self._init_kwargs = dict(init_kwargs or {})
        self._is_owner = False
        self._is_open_failed = False
        self._is_closed = False
        self._next_seal = 0
        self._sealed: set[int] = set()
        self._stamped: set[int] = set()
        self._drops: dict[int, Counter] = defaultdict(Counter)
        self._ordinals: Counter = Counter()
        self._step_started_at: datetime | None = None
        self._installed: list[tuple[Any, str, Any, Any]] = []
        self._callback: TrlCallback | None = None
        if is_enabled:
            self.guard.call("the trainer", self._setup)

    # -- public ------------------------------------------------------------------------------------------
    @property
    def is_main(self) -> bool:
        """The world-zero process: the one TRL logs completions from (`accelerator.is_main_process`)."""
        accelerator = getattr(self.trainer, "accelerator", None)
        return bool(getattr(accelerator, "is_main_process", True))

    def finish(self, status: str | None = None) -> None:
        """Close the record (terminal manifest, the producers' barrier) and, when this tracker opened the run,
        finish it. TRL's methods are unwrapped. Never raises."""
        if self.is_finished:
            return
        self.is_finished = True
        try:
            self._close(should_finish=self._is_owner, status=status)
        finally:
            self._unwrap()
            found = _TRACKERS.get(id(self.trainer))
            if found is not None and found[1] is self:
                del _TRACKERS[id(self.trainer)]

    def close_at_exit(self) -> None:
        """At exit: the manifest and barrier only; `probe.init()`'s exit hooks give the run its status."""
        if not self.is_finished and not self._is_closed:
            self._close(should_finish=False, status=None)

    # -- what recorders call ---------------------------------------------------------------------------------
    def install(self, target: Any, name: str, value: Any) -> None:
        """``value`` as ``target.name`` on this instance alone; `finish()` puts the old one back."""
        before = getattr(target, "__dict__", {}).get(name, _MISSING)
        object.__setattr__(target, name, value)
        self._installed.append((target, name, value, before))

    def remember_collated_rows(self, *, should_carry: bool = False) -> None:
        """GKD and GOLD train on collated tensors: the trainer's collator (read when `train()` builds its dataloader)
        keeps each row's dataset facts here until its micro-batch is recorded (`make_labeled_parts`). GOLD drops the
        columns its model does not read before collating (`_remove_unused_columns`, `gold_trainer.py:1641`; GKD
        turns that off, `gkd_trainer.py:132`), so the task's columns join the ones it keeps (`:1582-1612`).
        ``should_carry``: a batch collated in a dataloader worker carries its rows' task columns in the batch (GKD,
        whose loss reads named keys only, `gkd_trainer.py:324-347`; the recorder takes them out first)."""
        trainer = self.trainer
        collate = getattr(trainer, "data_collator", None)
        if callable(collate):
            columns = self.rows.get_columns(getattr(trainer, "train_dataset", None)) if should_carry else None
            self.install(trainer, "data_collator", self.collated.wrap(collate, columns))
        find_columns = getattr(trainer, "_set_signature_columns_if_needed", None)
        if not callable(find_columns):
            return

        @functools.wraps(find_columns)
        def call_find_columns(*args: Any, **kwargs: Any) -> Any:
            result = find_columns(*args, **kwargs)
            kept = getattr(trainer, "_signature_columns", None)
            if isinstance(kept, list):
                kept.extend(name for name in self.rows.get_columns(getattr(trainer, "train_dataset", None))
                            if name not in kept)
            return result

        self.install(trainer, "_set_signature_columns_if_needed", call_find_columns)

    def is_recording(self) -> bool:
        """The world-zero process with an open run: parts can go."""
        if self.is_finished or not self.is_main:
            return False
        if self.run is None:
            self.ensure_run(None)
        return self.samples is not None

    def ensure_run(self, resume_step: int | None) -> None:
        if self.run is None and not self._is_open_failed and not self.is_finished and self.is_main:
            self.guard.call("the run", self._open, resume_step)
            self._is_open_failed = self.run is None

    def get_step(self) -> int:
        """The trainer's completed optimizer steps (`state.global_step`)."""
        return int(getattr(getattr(self.trainer, "state", None), "global_step", 0) or 0)

    def get_window_end(self, step: int, generate_every: int) -> int:
        """The last optimizer step a generation made inside step ``step + 1`` trains in: it serves the next
        ``generate_every`` micro-batches from where it sits (`micro_index`), each step taking gradient-accumulation
        many, never past `max_steps` (training ends there)."""
        accumulation = max(1, int(getattr(self.trainer.args, "gradient_accumulation_steps", 1) or 1))
        end = step + 1 + (self.micro_index + max(1, generate_every) - 1) // accumulation
        max_steps = int(getattr(getattr(self.trainer, "state", None), "max_steps", 0) or 0)
        return min(end, max_steps) if max_steps > 0 else end

    def take_call(self, split: str, step: int, count: int = 1) -> int:
        """The ordinal of this generation call at (split, step): two evals at one step never share a key. ``count``
        reserves that many in a row (GOLD's buffered slices) and returns the first."""
        ordinal = self._ordinals[(split, step)]
        self._ordinals[(split, step)] += max(1, count)
        return ordinal

    def start_live(self, starts: list[dict]) -> LiveBatch:
        """A generation call's rows as live samples: on the main process with an open run, else none."""
        if not starts or not self.is_recording():
            return LiveBatch()
        return LiveBatch.start(self.live, starts)

    def send(self, parts: list[dict], step: int, groups: list[dict] | None = None) -> None:
        """Parts counted toward ``step``'s seal, and their group rows."""
        if parts:
            self.samples.log(parts, step=step)
            self._stamped.add(step)
        if groups:
            self.samples.log_groups(groups)

    def add_drops(self, step: int, reason: str, count: int = 1) -> None:
        """Drops that exist only as counts, declared in ``step``'s seal."""
        if count > 0:
            self._drops[step][reason] += count

    def get_teacher_ref(self) -> dict | None:
        return get_teacher_ref(self.trainer, self.teacher)

    def make_teacher_scorer(self) -> dict:
        ref = self.get_teacher_ref()
        name = (ref or {}).get("name") or (ref or {}).get("uri") or (ref or {}).get("run_id") or "teacher"
        scorer: dict[str, Any] = {"name": str(name)[:256], "kind": "teacher"}
        if ref is not None:
            scorer["model"] = ref
        return scorer

    def make_labeled_parts(
        self, batch: Mapping[str, Any], step: int, *, split: str, writer: dict | None, extras: dict[str, Any],
        call: int | None = None,
    ) -> list[dict]:
        """A distillation micro-batch the step trains on (or an eval batch) as parts: one generator part per row
        (prompt and completion from the labels, the dataset row's task, scenario and label when the collator kept
        it, ``writer`` as its writer, graded by the teacher) and, for a train row, the trainer part of step
        ``step + 1`` that trains on it (GKD, GOLD). ``call``: the ordinal taken when the batch was generated (its live
        rows' keys), else a fresh one."""
        scorer = self.make_teacher_scorer()
        call = self.take_call(split, step) if call is None else call
        is_train = split == "train"
        parts: list[dict] = []
        for row, (prompt_ids, completion) in enumerate(read_labeled_rows(batch)):
            prompt = self.decode_text(prompt_ids)
            key = f"{split}:{step}:{call}:0:{row}"
            arrays: dict[str, Any] = {"token_ids": completion}
            text = self.decode_tokens(completion)
            if text is not None:
                arrays["token_text"] = text
            task = self.read_row_task(prompt_ids, self.collated.take(prompt_ids), prompt=prompt)
            part: dict[str, Any] = {
                "key": key, **task, "prompt": prompt,
                "response": self.decode_text(completion), "split": split,
                "scheduled_step": step + 1 if is_train else step, "scored_by": [scorer],
                "prompt_tokens": len(prompt_ids), "response_tokens": len(completion), "extras": dict(extras),
                "host": self.host, "token_arrays": arrays,
            }
            if writer is not None:
                part["generated_by"] = [{"model": writer}]
            parts.append(part)
            if is_train:
                parts.append({"key": key, "role": "trainer", "consumed_step": step + 1, "consumed_until_step": step + 1,
                              "consumed_version": step})
        return parts

    def read_row_task(self, prompt_ids: list[int], row: Mapping[str, Any] | None, *, prompt: str | None = None) -> dict:
        """A collated row's task: its dataset row's (``row``, as the collator kept it), else its decoded prompt's hash."""
        prompt = self.decode_text(prompt_ids) if prompt is None else prompt
        return self.rows.read_task(row, prompt) if row is not None else {"task_key": make_prompt_key(prompt),
                                                                          "scenario": {}}

    def decode_text(self, ids: list[int]) -> str:
        tokenizer = self._get_tokenizer()
        return str(tokenizer.decode(ids, skip_special_tokens=True)) if tokenizer is not None and ids else ""

    def decode_tokens(self, ids: list[int]) -> list[str] | None:
        """One string per token (the adapter has the tokenizer, the server does not)."""
        tokenizer = self._get_tokenizer()
        if tokenizer is None or not ids:
            return None
        return [str(text) for text in tokenizer.batch_decode([[token] for token in ids])]

    # -- callback events --------------------------------------------------------------------------------------
    def handle_train_begin(self, step: int) -> None:
        if not self.is_finished and self.is_main:
            self.guard.call("train begin", self._begin, step)

    def handle_step_end(self, step: int) -> None:
        self.micro_index = 0
        if self.is_recording():
            self.guard.call("a step", self._end_step, step)

    def handle_evaluate(self, step: int) -> None:
        if step in self._sealed and self.is_recording():
            self.guard.call("a seal", self._send_seals_through, step)

    def handle_save(self, step: int) -> None:
        if self.recorder is None or not self.is_recording():
            return
        from probe.sdk.artifact.hashing import local_file_uri

        folder = os.path.abspath(os.path.join(str(self.trainer.args.output_dir), f"checkpoint-{step}"))
        if os.path.isdir(folder):
            self.guard.call("a checkpoint", self.recorder.handle_save, step, {"uri": local_file_uri(folder), "step": step})

    def handle_train_end(self, step: int) -> None:
        if self.run is not None and self.is_main and not self.is_finished:
            self._send_seals_safely(step)
            self._close(should_finish=False, status=None)

    # -- inside ------------------------------------------------------------------------------------------------
    def _setup(self) -> None:
        if drop_wandb(self.trainer):
            _diagnostics.warn(
                "probe: this TRL trainer reported to W&B; Probe records RL runs without it, so 'wandb' was taken out "
                "of report_to and its callback removed. Metrics reach Probe through report_to='probe'."
            )
        cls = pick_recorder(self.trainer, should_record_sft=self._should_record_sft)
        self.recorder = cls(self) if cls is not None else None
        self._wrap_trainer()
        self._callback = TrlCallback(self)
        self.trainer.add_callback(self._callback)
        if self.recorder is not None:
            self.recorder.install()
        else:
            _diagnostics.warn(
                f"probe: track() records samples for GRPO, RLOO, AsyncGRPO and the distillation trainers (SFT with "
                f"record_sft=True); {type(self.trainer).__name__} gets its run and checkpoints only. Its metrics come "
                "from report_to='probe'."
            )

    def _wrap_trainer(self) -> None:
        trainer = self.trainer
        train = trainer.train
        training_step = trainer.training_step

        @functools.wraps(train)
        def call_train(*args: Any, **kwargs: Any) -> Any:
            if not self.is_finished:
                resume = kwargs.get("resume_from_checkpoint", args[0] if args else None)
                self.guard.call("the run", self._open_for_train, resume)
            return train(*args, **kwargs)

        @functools.wraps(training_step)
        def call_training_step(model: Any, inputs: Any, *args: Any, **kwargs: Any) -> Any:
            if self.micro_index == 0:
                self._step_started_at = datetime.now(timezone.utc)
            if self.recorder is not None and not self.is_finished:
                self.guard.call("a training batch", self.recorder.handle_micro_batch, inputs)
            try:
                return training_step(model, inputs, *args, **kwargs)
            finally:
                self.micro_index += 1

        self.install(trainer, "train", call_train)
        self.install(trainer, "training_step", call_training_step)

    def _open_for_train(self, resume: Any) -> None:
        """Before transformers' `train()` runs: the run opens (a resume reopens it with a rewind) here, so the HF
        callback adopts it at `on_train_begin` instead of opening its own."""
        if not self.is_main:
            return
        step = read_resume_step(resume, getattr(self.trainer.args, "output_dir", None))
        if self.run is None:
            self._is_open_failed = False
            self.ensure_run(step)
        elif step is not None:
            self.floor = max(self.floor, get_rewind_step(step))
        self._is_closed = False

    def _open(self, resume_step: int | None) -> None:
        start = get_rewind_step(resume_step) if resume_step is not None else None
        name, init_kwargs, callback = get_identity(self.trainer, self._init_kwargs)
        key = self._make_run_key(init_kwargs, is_resume=start is not None)
        _finish_trained_runs()
        run, owns = _rl_owner.open_run(
            name=name,
            external_id=key.external_id,
            rewind_step=start if key.is_continued else None,
            config=None if callback is not None else get_config(self.trainer),
            init_kwargs=init_kwargs,
        )
        if callback is not None:
            # The callback's own project / name went into this run: its "not applied" warning would be wrong.
            callback._warned.add("adopt")
            if callback._run is None:
                callback._adopt(run)  # its metrics go to this trainer's run even when another run stays bound
        self.run, self._is_owner = run, owns
        self.samples = run.samples.as_producer(PRODUCER)
        self.live = LiveAttempts(self.samples, reward_max=self._reward_max)
        self.floor = self._next_seal = start or self.get_step()
        plan: dict[str, Any] = {"producers": [PRODUCER]}
        if self._reward_max is not None:
            plan["reward_max"] = self._reward_max
        if self.max_staleness is not None:
            plan["max_staleness"] = self.max_staleness
        self.samples.plan(**plan)
        refuse_commands(self.samples, COMMAND_REFUSAL)
        _rl_owner.close_at_exit(self)
        if key.save_error is not None or (key.is_legacy_resume and owns):
            self.guard.call("the run key", self._warn_run_key, key, f"{KEY_PREFIX}{name}" if owns else None)

    def _make_run_key(self, init_kwargs: Mapping[str, Any], *, is_resume: bool) -> RunKey:
        """The job's key (`run_key.py`). A key the script passed is used as it is; under a launcher
        (`PROBE_RUN_ID`) the launcher chose the run, so no key is kept."""
        from probe.sdk.settings.settings import env_run_id

        if init_kwargs.get("external_id") is not None:
            return RunKey(str(init_kwargs["external_id"]), is_continued=True)
        if env_run_id():
            return RunKey(None)
        return make_run_key(getattr(self.trainer.args, "output_dir", None), is_resume=is_resume)

    def _warn_run_key(self, key: RunKey, legacy_external_id: str | None) -> None:
        """Say once why this run cannot be continued by key, or that it starts over from an old checkpoint."""
        folder = os.path.join(str(getattr(self.trainer.args, "output_dir", None)), KEY_FOLDER, KEY_FILE)
        if key.save_error is not None:
            _diagnostics.warn(
                f"probe: could not keep this TRL job's run key at {folder} ({key.save_error}); its run opens with "
                "no key, so a resume_from_checkpoint relaunch will start a new run instead of continuing this one."
            )
        if not key.is_legacy_resume or legacy_external_id is None:
            return
        parent = find_legacy_parent(self.run, legacy_external_id)
        if parent is not None:
            from probe.sdk.routes import WriteOp, path_for

            self.run._client.send("PATCH", path_for(WriteOp.RUN_PATCH, self.run.id),
                                  {"parent_run_id": parent, "parent_relation": "resume"})
        linked = (f"linked to run {parent} as resumed from it" if parent is not None else
                  "not linked: its first run was not found in this project")
        _diagnostics.warn(
            f"probe: this checkpoint was saved before Probe kept a run key in {folder}, so its run cannot be "
            f"continued safely; this resume starts a new run, {linked}."
        )

    def _begin(self, step: int) -> None:
        self.ensure_run(None)
        if self.samples is not None and self.recorder is not None:
            self.recorder.handle_train_begin(step)

    def _end_step(self, step: int) -> None:
        self.samples.commit(step, consumed_at=self._step_started_at)
        if self.recorder is not None:
            self.recorder.handle_step_end(step)
        self._send_seals_through(step - 1)  # the step's evals and saves come after this event: sealed at the next one

    def _send_seals_through(self, last: int) -> None:
        """Seal each step up to ``last`` with news (parts or drop counts; a step sealed before declares its totals
        again), and each step from the floor this producer had nothing at, so capture's 0..N finds one."""
        news = {step for step in self._stamped | set(self._drops) if step <= last}
        for step in sorted(news | set(range(self._next_seal, last + 1))):
            drops = self._drops.pop(step, None)
            self.samples.seal(step, dropped=dict(drops) if drops else None)
            self._sealed.add(step)
            self._stamped.discard(step)
        self._next_seal = max(self._next_seal, last + 1)

    def _send_seals_safely(self, last: int) -> None:
        if self.samples is not None:
            self.guard.call("a seal", self._send_seals_through, last)

    def _close(self, *, should_finish: bool, status: str | None) -> None:
        if self.run is None:
            return
        self._send_seals_safely(max({self.get_step()} | self._stamped | set(self._drops)))
        final = max(self._sealed) if self._sealed else None
        self._is_closed = True
        self.guard.call(
            "the close", _rl_owner.close_run, self.run, self.samples,
            final_step=final, should_finish=should_finish, status=status,
        )

    def _get_tokenizer(self) -> Any:
        processing = getattr(self.trainer, "processing_class", None)
        return getattr(processing, "tokenizer", None) or processing

    def _unwrap(self) -> None:
        for target, name, value, before in reversed(self._installed):
            try:
                if target.__dict__.get(name) is not value:
                    continue  # another wrap went on top: ours passes through
                if before is _MISSING:
                    del target.__dict__[name]
                else:
                    object.__setattr__(target, name, before)
            except Exception:  # noqa: BLE001 -- an object that will not give it back keeps the wrap
                pass
        self._installed.clear()
        if self._callback is not None:
            try:
                self.trainer.remove_callback(self._callback)
            except Exception:  # noqa: BLE001 -- a trainer that lost it already: nothing left to take off
                pass


def _finish_trained_runs() -> None:
    """A new trainer is its own run, as with the HF callback: a run an earlier tracker opened, whose training
    ended, is finished first (it is still bound), so the new run is the one `probe.active_run()` names."""
    import probe

    active = probe.active_run()
    for _ref, tracker in list(_TRACKERS.values()):
        if tracker.run is active and active is not None and tracker._is_owner and tracker._is_closed:
            tracker.finish()
