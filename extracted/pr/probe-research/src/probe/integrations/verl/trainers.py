"""The verl trainer methods Probe wraps (RL plan §6.5, D33), one family per way verl holds a batch: the V1 trainer
(rows in the TransferQueue, `trainer.use_v1=True`, the default), the legacy `RayPPOTrainer` and the trainers built
on it (one-step-off), the fully async trainer (steps are weight versions) and its rollouter (validation only); plus
the V1 replay buffer's group evictions. Class-level wraps in the recording process only, installed when its session
starts, on the module classes and on the class Ray builds for an actor; each fails open. Line refs are
`verl-project/verl@b17218ba58a6`. Why: DESIGN.md."""

from __future__ import annotations

import functools
import inspect
import os
import sys
import threading
from collections.abc import Callable, Iterable, Iterator
from typing import Any

from .. import _rl_owner
from .readers import (
    PromptFacts,
    ValidationPass,
    build_validation_rows,
    fetch_transfer_queue_rows,
    read_dataproto_rows,
    read_final_sessions,
    read_generated,
    read_prompt_facts,
    read_versions,
)
from .rows import CRITIC_WARMUP_DROP, RowMapper, VerlRow

#: Marks a verl method Probe already wrapped (installs are idempotent).
WRAPPED_MARK = "__probe_verl_wrapped__"
#: verl method -> the `TrainerWraps` method that wraps it.
WRAPPERS = {
    "_update_actor": "_wrap_update",
    "_update_critic": "_wrap_critic_update",
    "_save_checkpoint": "_wrap_checkpoint",
    "_validate": "_wrap_validation",
    "_maybe_log_val_generations": "_wrap_validation_texts",
    "_val_metrics_update": "_wrap_validation_metrics",
    "_get_gen_batch": "_wrap_generation_batch",
}
#: What Ray puts in the class it builds for an actor (`ray/actor.py` `_modify_class`): the class it was made from.
RAY_ACTOR_CLASS_MARK = "__ray_actor_class__"
#: The rollouter's running count of stale-dropped groups, copied onto every fully async batch
#: (`fully_async_policy/detach_utils.py:111-113`, `fully_async_rollouter.py:1166-1186`).
STALE_COUNT_KEY = "fully_async/count/dropped_stale_samples"
#: The V1 replay buffer (`trainer/ppo/v1/replay_buffer.py:64`, `ReplayBufferAsync` at :514 inherits its eviction).
REPLAY_BUFFER_MODULE = "verl.trainer.ppo.v1.replay_buffer"
#: verl's SFT trainer saves through `CheckpointHandler.save_checkpoint(step)`, not a trainer's `_save_checkpoint`
#: (`trainer/sft_trainer.py:443`, `utils/checkpoint/checkpoint_handler.py:90`).
SFT_CHECKPOINT_MODULE = "verl.utils.checkpoint.checkpoint_handler"
#: Groups a training poll evicted (`_evict_terminal_groups`, :345-381) and the sync sampler's discarded surplus
#: (`sample`, :494-500), by verl's metric name under `training/`, as seal drop reasons (`DropReason`).
EVICTION_DROPS = {
    "filter_groups/evicted_samples": "zero_variance",  # DAPO: one metric value across the whole group (:261-315)
    "rollout_failure/evicted_samples": "error",  # a session failed and the group is refilled (:330-334)
    "off_policy/evicted_samples": "stale",  # past `max_off_policy_threshold` (async, :520-530)
}
SURPLUS_DROPS = {"filter_groups/discarded_surplus_samples": "oversampling"}
#: The prefix verl gives the training partition's metrics (`_metrics_prefix`, :238-239).
TRAIN_METRICS_PREFIX = "training/"


class TrainerFamily:
    """How the wraps read one family of verl trainers: its class, the methods it defines that are wrapped, how a
    training batch becomes rows and how it numbers steps. Default: verl's `global_steps` is the step being trained
    (it trains on the weights of the step before) and the step a validation pass or checkpoint belongs to."""

    module = ""
    class_name = ""
    methods: tuple[str, ...] = ()

    def get_class(self) -> type | None:
        """The family's class when its module is already imported (never imports verl)."""
        module = sys.modules.get(self.module)
        found = getattr(module, self.class_name, None) if module is not None else None
        found = getattr(found, RAY_ACTOR_CLASS_MARK, found)  # a `@ray.remote` class (`fully_async_trainer.py:53`)
        return found if isinstance(found, type) else None

    def is_base_of(self, cls: type) -> bool:
        """``cls`` is the family's class or built on it. By name too: a Ray actor's process unpickles its own copy
        of the class (`fully_async_trainer.py:53`), which is not the one its module holds."""
        own = self.get_class()
        return any(base is own or (base.__module__, base.__qualname__) == (self.module, self.class_name)
                   for base in cls.__mro__)

    def get_train_step(self, trainer: Any) -> int:
        return int(trainer.global_steps)

    def is_pushing_weights(self, trainer: Any) -> bool:
        return True

    def get_checkpoint_step(self, trainer: Any) -> int:
        return int(trainer.global_steps)

    def get_eval_step(self, trainer: Any, capture: ValidationCapture) -> int | None:
        return int(trainer.global_steps)

    def is_critic_warmup(self, trainer: Any) -> bool:
        """The actor is not updated this step: verl trains the critic alone while `trainer.critic_warmup >
        global_steps` (`ray_trainer.py:1684`, `v1/trainer_base.py:608`, `separation/ray_trainer.py:646`)."""
        warmup = getattr(getattr(trainer.config, "trainer", None), "critic_warmup", 0) or 0
        return int(warmup) > int(trainer.global_steps)

    def get_total_steps(self, trainer: Any) -> int | None:
        total = getattr(trainer, "total_training_steps", None)
        return total if isinstance(total, int) else None

    def read_train_rows(self, trainer: Any, batch: Any) -> list[VerlRow]:
        raise NotImplementedError

    def get_stale_count(self, batch: Any) -> Any:
        return None

    def watch_validation(self, trainer: Any, capture: ValidationCapture) -> Callable[[], None]:
        """Start collecting what the validation pass's prompts were; returns what puts things back."""
        return lambda: None


class DataProtoFamily(TrainerFamily):
    """`RayPPOTrainer` (`trainer/ppo/ray_trainer.py:285`) and trainers built on it (`OneStepOffRayTrainer`): the
    whole batch is a `DataProto` in this process."""

    module = "verl.trainer.ppo.ray_trainer"
    class_name = "RayPPOTrainer"
    methods = ("_update_actor", "_update_critic", "_save_checkpoint", "_validate", "_maybe_log_val_generations",
               "_val_metrics_update", "_get_gen_batch")

    def read_train_rows(self, trainer: Any, batch: Any) -> list[VerlRow]:
        return read_dataproto_rows(batch)

    def watch_validation(self, trainer: Any, capture: ValidationCapture) -> Callable[[], None]:
        """Keep each generated batch's rows from the rollout manager `_validate` calls (`ray_trainer.py:640`), on the
        instance for the pass only: their weight versions (`max_global_steps`, `agent_loop.py:1210-1223`), live keys
        and stop reasons (`live.stamp_output`; with colocated scoring the batch is the only place the key reaches).
        verl's `auto_await` (`utils/ray_utils.py:97-139`) reads its caller's frame to pick sync or async, so an async
        caller is handed a coroutine as before."""
        manager = getattr(trainer, "async_rollout_manager", None)
        if manager is None:
            return lambda: None
        original = manager.generate_sequences

        def keep(output: Any) -> Any:
            try:
                capture.keep_generated(output)
            except Exception:  # noqa: BLE001 -- fail open: no version (the rollouter's pass is not recorded), no links
                pass
            return output

        def generate_sequences(*args: Any, **kwargs: Any) -> Any:
            if sys._getframe(1).f_code.co_flags & inspect.CO_COROUTINE:
                async def generate_awaited() -> Any:
                    return keep(await original(*args, **kwargs))

                return generate_awaited()
            return keep(original(*args, **kwargs))

        return patch_for_pass(manager, "generate_sequences", generate_sequences)


class FullyAsyncFamily(DataProtoFamily):
    """`FullyAsyncTrainer` (`fully_async_policy/fully_async_trainer.py:53-54`, a Ray actor class: the module holds Ray's
    wrapper, the actor process an instance of a subclass of the class itself): `global_steps` counts mini-steps; the
    step is the weight version an update makes (`current_param_version` + 1, `:676-688`), which is also where its
    metrics and checkpoints go (`:783-786`, `:917-926`). Validation runs in the rollouter process: not recorded."""

    module = "verl.experimental.fully_async_policy.fully_async_trainer"
    class_name = "FullyAsyncTrainer"
    methods = ("_save_checkpoint",)

    def get_train_step(self, trainer: Any) -> int:
        return int(trainer.current_param_version) + 1

    def is_pushing_weights(self, trainer: Any) -> bool:
        """Weights are pushed once every `trigger_parameter_sync_step` updates (`:684-688`, `:700-701`)."""
        return int(trainer.local_trigger_step) >= int(trainer.trigger_parameter_sync_step)

    def get_checkpoint_step(self, trainer: Any) -> int:
        return int(trainer.current_param_version)

    def get_total_steps(self, trainer: Any) -> int | None:
        total = getattr(trainer, "total_train_steps", None)
        return total if isinstance(total, int) else None

    def get_stale_count(self, batch: Any) -> Any:
        return (getattr(batch, "meta_info", None) or {}).get(STALE_COUNT_KEY)


class RollouterFamily(DataProtoFamily):
    """`FullyAsyncRollouter` (`fully_async_policy/fully_async_rollouter.py:329-330`, a Ray actor built on
    `RayPPOTrainer`): it generates and validates in its own process (`do_validate`, :648-653). Its `global_steps`
    counts samples, so a validation pass is placed at the weight version its responses were generated with, the one
    the trainer logs the pass's metrics at (`update_weights(global_steps=current_param_version)` then
    `_fit_validate`, `fully_async_trainer.py:734-736, 812-830`). It defines none of the wrapped methods itself."""

    module = "verl.experimental.fully_async_policy.fully_async_rollouter"
    class_name = "FullyAsyncRollouter"
    methods = ()

    def get_eval_step(self, trainer: Any, capture: ValidationCapture) -> int | None:
        return max(capture.versions) if capture.versions else None

    def get_total_steps(self, trainer: Any) -> int | None:
        return None



class TransferQueueFamily(TrainerFamily):
    """The V1 `PPOTrainer` (`trainer/ppo/v1/trainer_base.py:114`; `sync`, `colocate_async`, `separate_async`): a
    batch is keys and tags, its rows live in the TransferQueue until the step clears them (`:512`)."""

    module = "verl.trainer.ppo.v1.trainer_base"
    class_name = "PPOTrainer"
    methods = ("_update_actor", "_update_critic", "_save_checkpoint", "_validate", "_maybe_log_val_generations",
               "_val_metrics_update")

    def read_train_rows(self, trainer: Any, batch: Any) -> list[VerlRow]:
        import transfer_queue

        return fetch_transfer_queue_rows(batch, transfer_queue.kv_batch_get)

    def watch_validation(self, trainer: Any, capture: ValidationCapture) -> Callable[[], None]:
        """`_validate` gives each validation batch dict its uids in place (`:1048-1052`): a loader that remembers
        the dicts it hands out reads them afterwards."""
        buffer = trainer.replay_buffer
        sample = buffer.sample

        def call_sample(*args: Any, **kwargs: Any) -> Any:
            """The keys the pass sampled (`:1074-1076`): each final response's session, should its loop's carried key
            be gone (a colocated reward that replaced `reward_extra_info`)."""
            result = sample(*args, **kwargs)
            try:
                capture.keep_sampled(result[0].keys)
            except Exception:  # noqa: BLE001 -- fail open: no sessions, the carried keys alone link
                pass
            return result

        restore_sample = patch_for_pass(buffer, "sample", call_sample)
        try:
            restore_loader = patch_for_pass(trainer, "val_dataloader",
                                            RecordingLoader(trainer.val_dataloader, capture))
        except BaseException:
            restore_sample()
            raise

        def restore() -> None:
            try:
                restore_loader()
            finally:
                restore_sample()

        return restore


def patch_for_pass(owner: Any, name: str, replacement: Any) -> Callable[[], None]:
    """Set ``owner.<name>`` to ``replacement`` for one pass. The undo puts back what was there (or drops an instance
    attribute that only shadowed the class's), and only while the attribute is still ``replacement``, so it never
    undoes someone else's later patch."""
    had_own = name in getattr(owner, "__dict__", {})
    original = getattr(owner, name)
    setattr(owner, name, replacement)

    def restore() -> None:
        if getattr(owner, "__dict__", {}).get(name) is not replacement:
            return
        if had_own:
            setattr(owner, name, original)
        else:
            delattr(owner, name)

    return restore


#: Most specific first: a fully async trainer and its rollouter are also `RayPPOTrainer`s.
FAMILIES: tuple[TrainerFamily, ...] = (FullyAsyncFamily(), RollouterFamily(), DataProtoFamily(), TransferQueueFamily())


class ValidationCapture:
    """One `_validate()` call: what verl handed out, and the dataset facts of its prompts."""

    def __init__(self) -> None:
        self.validation = ValidationPass()
        self.prompts: dict[str, PromptFacts] = {}
        self.batch_dicts: list[Any] = []
        self.versions: list[int] = []
        self._rows: int | None = None

    def keep_texts(self, inputs: Any, outputs: Any, scores: Any) -> None:
        self.validation.inputs, self.validation.outputs, self.validation.scores = (
            list(inputs), list(outputs), list(scores))

    def keep_metrics_inputs(self, data_sources: Any, uids: Any, reward_extras: Any, turns: Any) -> None:
        validation = self.validation
        validation.data_sources, validation.uids, validation.turns = list(data_sources), list(uids), list(turns)
        validation.reward_extras = dict(reward_extras or {})

    def keep_prompts(self, batch: Any) -> None:
        """A `DataProto` validation batch's dataset facts by uid (`_get_gen_batch`, `ray_trainer.py:626`), and its
        size: the generated batch's rows past it are padding (`ray_trainer.py:638-640`)."""
        self.prompts.update(read_prompt_facts(batch.non_tensor_batch))
        self._rows = len(batch.non_tensor_batch["uid"])  # every row has one (`ray_trainer.py:608-611`)

    def keep_generated(self, batch: Any) -> None:
        """A generated `DataProto`'s weight versions (padding rows carry none), and its real rows' live keys and stop
        reasons, in the order `_validate` lists them."""
        self.versions += read_versions(batch)
        keys, reasons = read_generated(batch, self._rows)
        self.validation.live_keys += keys
        self.validation.stop_reasons += reasons
        self._rows = None

    def keep_sampled(self, keys: Any) -> None:
        """V1: the TransferQueue keys one validation batch sampled."""
        self.validation.sessions += read_final_sessions(list(keys))

    def get_prompts(self) -> dict[str, PromptFacts]:
        for batch in self.batch_dicts:
            self.prompts.update(read_prompt_facts(batch))
        return self.prompts


class RecordingLoader:
    """A validation dataloader that hands out the same batch dicts and remembers them."""

    def __init__(self, loader: Any, capture: ValidationCapture) -> None:
        self._loader = loader
        self._capture = capture

    def __iter__(self) -> Iterator[Any]:
        for batch in self._loader:
            if isinstance(batch, dict):
                self._capture.batch_dicts.append(batch)
            yield batch

    def __len__(self) -> int:
        return len(self._loader)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._loader, name)


def get_family(trainer: Any) -> TrainerFamily | None:
    for family in FAMILIES:
        if family.is_base_of(type(trainer)):
            return family
    return None


def find_actor_classes() -> list[type]:
    """The classes Ray built in this process for trainer actors (`ray/actor.py` `_modify_class`): each holds its own
    copy of every method (Ray's tracing wrap, `ray/util/tracing/tracing_helper.py` `_inject_tracing_into_class`),
    and those copies are what the actor runs, so a wrap on the module class never fires there."""
    found: list[type] = []
    seen: set[type] = set()
    todo = [cls for family in FAMILIES if (cls := family.get_class()) is not None]
    while todo:
        for sub in todo.pop().__subclasses__():
            if sub in seen:
                continue
            seen.add(sub)
            todo.append(sub)
            if RAY_ACTOR_CLASS_MARK in vars(sub):
                found.append(sub)
    return found


class TrainerWraps:
    """The wraps, bound to the session that records (``get_session`` returns it, or None to record nothing)."""

    def __init__(self, get_session: Callable[[], Any]) -> None:
        self._get_session = get_session
        self._local = threading.local()
        self._validations: dict[int, ValidationCapture] = {}

    def install(self) -> list[str]:
        """Wrap each imported family class's methods, each Ray actor class's copies of them, and the V1 replay
        buffer's evictions, once. Returns what was wrapped now."""
        wrapped = []
        for family in FAMILIES:
            cls = family.get_class()
            if cls is not None:
                wrapped += self._wrap_methods(cls, family.methods)
        for cls in find_actor_classes():
            names = [name for family in FAMILIES if family.is_base_of(cls) for name in family.methods]
            wrapped += self._wrap_methods(cls, dict.fromkeys(names))
        buffer = getattr(sys.modules.get(REPLAY_BUFFER_MODULE), "ReplayBuffer", None)
        if isinstance(buffer, type):
            wrapped += self._wrap_buffer(buffer, "_evict_terminal_groups", EVICTION_DROPS, lambda result: result[3])
            wrapped += self._wrap_buffer(buffer, "sample", SURPLUS_DROPS, lambda result: result[1])
        handler = getattr(sys.modules.get(SFT_CHECKPOINT_MODULE), "CheckpointHandler", None)
        if isinstance(handler, type):
            wrapped += self._wrap_sft_checkpoint(handler)
        return wrapped

    def _wrap_sft_checkpoint(self, cls: type) -> list[str]:
        """An SFT save stamps `global_step_{step}` with the run's attempt (`_rl_owner.stamp_checkpoint`), so a resume
        from it reopens that run, as a PPO save does. From the process with the session (SFT's logging rank, which
        under pipeline parallelism is not global rank 0), before the save into a folder that already exists (an
        older attempt's stamp must not outlive this save) and after it."""
        original = vars(cls).get("save_checkpoint")
        if not callable(original) or getattr(original, WRAPPED_MARK, False):
            return []

        @functools.wraps(original)
        def call_save(handler: Any, *args: Any, **kwargs: Any) -> Any:
            session = self._get_session()
            step = kwargs.get("step", args[0] if args else None)
            folder = os.path.join(str(getattr(handler, "default_local_dir", "")), f"global_step_{step}")
            if session is not None and step is not None and os.path.isdir(folder):
                _rl_owner.stamp_checkpoint(session.run, folder)  # never raises
            result = original(handler, *args, **kwargs)
            if session is not None and step is not None:
                _rl_owner.stamp_checkpoint(session.run, folder)
            return result

        setattr(call_save, WRAPPED_MARK, True)
        setattr(cls, "save_checkpoint", call_save)
        return [f"{cls.__name__}.save_checkpoint"]

    def _wrap_buffer(self, cls: type, name: str, reasons: dict[str, str],
                     get_metrics: Callable[[Any], Any]) -> list[str]:
        """A replay buffer method whose returned metrics count the training groups it threw away: each count, by
        reason, goes to the seal of the step it was sampling for (its `global_steps`)."""
        original = vars(cls).get(name)
        if not callable(original) or getattr(original, WRAPPED_MARK, False):
            return []

        @functools.wraps(original)
        def call_buffer(buffer: Any, global_steps: Any, partition_id: Any, *args: Any, **kwargs: Any) -> Any:
            result = original(buffer, global_steps, partition_id, *args, **kwargs)
            session = self._get_session()
            if session is not None and partition_id == "train":
                session.guard.call("a group drop", self._record_drops, session, global_steps, reasons,
                                   get_metrics, result)
            return result

        setattr(call_buffer, WRAPPED_MARK, True)
        setattr(cls, name, call_buffer)
        return [f"{cls.__name__}.{name}"]

    @staticmethod
    def _record_drops(session: Any, step: Any, reasons: dict[str, str], get_metrics: Callable[[Any], Any],
                      result: Any) -> None:
        metrics = get_metrics(result) or {}
        for name, reason in reasons.items():
            session.recorder.add_drops(int(step), reason, metrics.get(TRAIN_METRICS_PREFIX + name))

    def _wrap_methods(self, cls: type, names: Iterable[str]) -> list[str]:
        """Wrap each method where ``cls`` finds it, on ``cls``: its own, or the one it inherits."""
        wrapped = []
        for name in names:
            original = next((vars(base)[name] for base in cls.__mro__ if name in vars(base)), None)
            if not callable(original) or getattr(original, WRAPPED_MARK, False):
                continue
            wrapper = getattr(self, WRAPPERS[name])(original)
            setattr(wrapper, WRAPPED_MARK, True)
            setattr(cls, name, wrapper)
            wrapped.append(f"{cls.__name__}.{name}")
        return wrapped

    # -- training ----------------------------------------------------------------------------------------
    def _wrap_update(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_update_actor(trainer: Any, batch: Any, *args: Any, **kwargs: Any) -> Any:
            session, family = self._get_recording(trainer, "_update_actor")
            if session is None:
                return original(trainer, batch, *args, **kwargs)
            step = session.guard.call("a training batch", self._record_batch, session, family, trainer, batch)
            with self._mark_inside("_update_actor"):
                result = original(trainer, batch, *args, **kwargs)
            if isinstance(step, int):
                session.guard.call("a commit", self._commit, session, family, trainer, step)
            return result

        return call_update_actor

    def _wrap_critic_update(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_update_critic(trainer: Any, batch: Any, *args: Any, **kwargs: Any) -> Any:
            session, family = self._get_recording(trainer, "_update_critic")
            if session is None:
                return original(trainer, batch, *args, **kwargs)
            with self._mark_inside("_update_critic"):
                result = original(trainer, batch, *args, **kwargs)
            if session.guard.call("the critic warmup", family.is_critic_warmup, trainer):
                session.guard.call("a critic warmup batch", self._record_warmup, session, family, trainer, batch)
            return result

        return call_update_critic

    def _wrap_checkpoint(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_save_checkpoint(trainer: Any, *args: Any, **kwargs: Any) -> Any:
            session, family = self._get_recording(trainer, "_save_checkpoint")
            if session is None:
                return original(trainer, *args, **kwargs)
            with self._mark_inside("_save_checkpoint"):
                result = original(trainer, *args, **kwargs)
            session.guard.call("a checkpoint", self._record_checkpoint, session, family, trainer)
            return result

        return call_save_checkpoint

    # -- validation --------------------------------------------------------------------------------------
    def _wrap_validation(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_validate(trainer: Any, *args: Any, **kwargs: Any) -> Any:
            session, family = self._get_recording(trainer, "_validate")
            if session is None:
                return original(trainer, *args, **kwargs)
            capture = ValidationCapture()
            self._validations[id(trainer)] = capture
            restore = session.guard.call("a validation pass", family.watch_validation, trainer, capture)
            try:
                with self._mark_inside("_validate"):
                    result = original(trainer, *args, **kwargs)
            finally:
                self._validations.pop(id(trainer), None)
                if callable(restore):  # its own label: the guard warns once per label
                    session.guard.call("undoing a validation watch", restore)
            session.guard.call("a validation pass", self._record_validation, session, family, trainer, capture)
            return result

        return call_validate

    def _wrap_validation_texts(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_log_generations(trainer: Any, inputs: Any, outputs: Any, scores: Any, *args: Any,
                                      **kwargs: Any) -> Any:
            capture = self._validations.get(id(trainer))
            if capture is not None:
                self._guard_capture(capture.keep_texts, inputs, outputs, scores)
            return original(trainer, inputs, outputs, scores, *args, **kwargs)

        return call_log_generations

    def _wrap_validation_metrics(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_update_metrics(trainer: Any, data_sources: Any, sample_uids: Any, reward_extra_infos_dict: Any,
                               sample_turns: Any, *args: Any, **kwargs: Any) -> Any:
            capture = self._validations.get(id(trainer))
            if capture is not None:
                self._guard_capture(capture.keep_metrics_inputs, data_sources, sample_uids, reward_extra_infos_dict,
                                    sample_turns)
            return original(trainer, data_sources, sample_uids, reward_extra_infos_dict, sample_turns, *args, **kwargs)

        return call_update_metrics

    def _wrap_generation_batch(self, original: Callable) -> Callable:
        @functools.wraps(original)
        def call_get_generation_batch(trainer: Any, batch: Any, *args: Any, **kwargs: Any) -> Any:
            capture = self._validations.get(id(trainer))
            if capture is not None:
                self._guard_capture(capture.keep_prompts, batch)
            return original(trainer, batch, *args, **kwargs)

        return call_get_generation_batch

    # -- inside ------------------------------------------------------------------------------------------
    def _guard_capture(self, keep: Callable[..., None], *args: Any) -> None:
        """Keep what verl hands a validation method, failing open (counted on the session's guard)."""
        session = self._get_session()
        if session is not None:
            session.guard.call("a validation pass", keep, *args)

    def _get_recording(self, trainer: Any, name: str) -> tuple[Any, TrainerFamily]:
        """The session and family when this call records: never for a nested call of the same method."""
        session = self._get_session()
        family = get_family(trainer) if session is not None else None
        if session is None or family is None or name in self._get_inside():
            return None, None  # type: ignore[return-value]
        session.guard.call("the trainer", session.setup_trainer, trainer, family)
        return session, family

    def _record_batch(self, session: Any, family: TrainerFamily, trainer: Any, batch: Any) -> int:
        """The batch's rows, consumed by its step; a step whose batch could not be read is never sealed."""
        step = family.get_train_step(trainer)
        try:
            session.recorder.add_stale_drops(step, family.get_stale_count(batch))
            rows = family.read_train_rows(trainer, batch)
        except Exception:
            session.recorder.mark_failed(step)
            raise
        session.recorder.record_train(step, rows)
        return step

    @staticmethod
    def _record_warmup(session: Any, family: TrainerFamily, trainer: Any, batch: Any) -> None:
        """A critic-warmup step's rows (read after the critic update, before the step clears them): generated,
        dropped from the actor's training."""
        step = family.get_train_step(trainer)
        try:
            rows = family.read_train_rows(trainer, batch)
        except Exception:
            session.recorder.mark_failed(step)
            raise
        session.recorder.record_dropped(step, rows, CRITIC_WARMUP_DROP)

    @staticmethod
    def _commit(session: Any, family: TrainerFamily, trainer: Any, step: int) -> None:
        session.recorder.commit(step, is_pushing_weights=family.is_pushing_weights(trainer))

    @staticmethod
    def _record_checkpoint(session: Any, family: TrainerFamily, trainer: Any) -> None:
        session.record_checkpoint(trainer, family.get_checkpoint_step(trainer))

    def _record_validation(self, session: Any, family: TrainerFamily, trainer: Any,
                           capture: ValidationCapture) -> None:
        step = family.get_eval_step(trainer, capture)
        if step is None:
            raise ValueError("a validation pass with no weight version: its step is unknown")
        try:
            rows = build_validation_rows(capture.validation, capture.get_prompts())
        except Exception:
            session.recorder.mark_failed(step)
            raise
        if rows:
            session.recorder.record_eval(step, rows)

    def _get_inside(self) -> set[str]:
        inside = getattr(self._local, "names", None)
        if inside is None:
            inside = self._local.names = set()
        return inside

    def _mark_inside(self, name: str) -> _Inside:
        return _Inside(self._get_inside(), name)


class _Inside:
    """Marks a wrapped method as running on this thread, so a subclass calling `super()` records once."""

    def __init__(self, names: set[str], name: str) -> None:
        self._names, self._name = names, name

    def __enter__(self) -> None:
        self._names.add(self._name)

    def __exit__(self, *exc: Any) -> None:
        self._names.discard(self._name)


def build_mapper(trainer: Any) -> RowMapper:
    """The row mapper for this trainer: its tokenizer decodes (`skip_special_tokens=True`, as verl's own dump),
    `data.max_response_length` tells a cut-off response."""
    import socket

    tokenizer = getattr(trainer, "tokenizer", None)
    decode = None
    if tokenizer is not None:
        def decode(ids: list[int]) -> str:
            return tokenizer.decode(ids, skip_special_tokens=True)

    config = getattr(trainer, "config", None)
    data = getattr(config, "data", None)
    limit = getattr(data, "max_response_length", None) if data is not None else None
    return RowMapper(
        decode=decode,
        tokens_to_text=getattr(tokenizer, "convert_ids_to_tokens", None),
        max_response_length=int(limit) if isinstance(limit, int) else None,
        host=socket.gethostname(),
        worker=f"pid:{os.getpid()}",
    )
