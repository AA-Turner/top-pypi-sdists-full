"""`ProbeExp`: SkyRL's `BasePPOExp` with Probe wired through its own doors (`get_tracker`, `get_generator`,
`get_trainer`, `entrypoints/main_base.py:182-194, 420-431`), synchronous or fully async. Imports SkyRL: load it
only where SkyRL runs. Line refs are `NovaSky-AI/SkyRL@d87004689e3a`. Why: DESIGN.md."""

from __future__ import annotations

import os
import socket
from typing import Any

from skyrl.train.entrypoints.main_base import BasePPOExp
from skyrl.train.utils.tracking import Tracking
from skyrl.train.utils.utils import Timer

from probe.foundation.safe_warn import safe_warn as _diagnostics

from .. import _rl_owner
from .._live import refuse_commands
from . import phases
from .hooks import SkyrlHooks
from .live import COMMAND_REFUSAL, SkyrlLive
from .outputs import OutputMapper
from .recorder import SkyrlRecorder
from .training import build_training_plan
from .runs import (
    UNSUPPORTED, get_config, get_external_id, get_resume_folder, get_rewind_step, get_run_name, read_resume_step,
    record_base_model,
)

#: The producer a SkyRL training process writes samples as (generation and training share it).
PRODUCER = "skyrl"
#: Comma-separated `env_extras` columns that pose a task (besides a `scenario` object column).
SCENARIO_KEYS_ENV = "PROBE_SKYRL_SCENARIO"
#: SkyRL's tracker backends (`utils/tracking.py:34`): W&B is never used under Probe.
WANDB_BACKEND = "wandb"
CONSOLE_BACKEND = "console"


class ProbeTracking(Tracking):
    """SkyRL's tracker, its backend kept (console by default), with every scalar row also on Probe."""

    def __init__(self, *args: Any, hooks: SkyrlHooks | None = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._probe_hooks = hooks

    def log(self, data: Any, step: Any, commit: bool = False) -> None:
        super().log(data, step, commit=commit)
        hooks = self._probe_hooks
        if hooks is not None and isinstance(step, int):
            hooks.guard.call("metrics", hooks.log_metrics, data, step)


class ProbeExp(BasePPOExp):
    """A SkyRL experiment on Probe. Under the Probe entrypoint it joins the run the driver opened
    (`PROBE_RUN_ID`) as producer `skyrl`; run on its own, it opens the run and owns it."""

    def __init__(self, cfg: Any) -> None:
        super().__init__(cfg)
        self.guard = _rl_owner.HookGuard("SkyRL")
        self.hooks: SkyrlHooks | None = None
        self.final_step: int | None = None
        self._probe_run: Any = None
        self._is_owner = False

    def run(self) -> None:
        self.guard.call("run open", self._open_probe)
        status = "failed"
        try:
            super().run()
            status = "completed"
        finally:
            self.guard.call("run close", self._close_probe, status)

    def get_tracker(self) -> Tracking:
        """SkyRL's own backend beside Probe, never W&B: `wandb` (SkyRL's default, `config.py:1818`) becomes
        `console`, with one warning."""
        backend = self.cfg.trainer.logger
        if backend == WANDB_BACKEND:
            _diagnostics.warn(
                "probe.integrations.skyrl: trainer.logger=wandb is replaced by console; Probe records this run "
                "(set trainer.logger=console, mlflow, tensorboard or swanlab to choose)."
            )
            backend = CONSOLE_BACKEND
        return ProbeTracking(
            project_name=self.cfg.trainer.project_name,
            experiment_name=self.cfg.trainer.run_name,
            backend=backend,
            config=self.cfg,
            tags=self.cfg.trainer.tags,
            hooks=self.hooks,
        )

    def get_generator(self, cfg: Any, tokenizer: Any, inference_engine_client: Any) -> Any:
        generator = super().get_generator(cfg, tokenizer, inference_engine_client)
        if self.hooks is not None:
            self.guard.call("the generator", self.hooks.wrap_generator, generator, inference_engine_client)
        return generator

    def get_trainer(self, cfg: Any, tracker: Any, tokenizer: Any, train_dataset: Any, eval_dataset: Any,
                    inference_engine_client: Any, generator: Any, colocate_pg: Any) -> Any:
        """The synchronous trainer, or the fully async one when `trainer.fully_async.enabled` (as SkyRL's own
        `examples/train/fully_async/main_fully_async.py` does), with the Probe hooks."""
        is_fully_async = bool(cfg.trainer.fully_async.enabled)
        if is_fully_async:
            from skyrl.train.fully_async_trainer import FullyAsyncRayPPOTrainer as trainer_class
        else:
            from skyrl.train.trainer import RayPPOTrainer as trainer_class
        trainer = trainer_class(
            cfg=cfg, tracker=tracker, tokenizer=tokenizer, train_dataset=train_dataset, eval_dataset=eval_dataset,
            inference_engine_client=inference_engine_client, generator=generator, colocate_pg=colocate_pg,
        )
        if self.hooks is not None:
            self.guard.call("the trainer", self.hooks.wrap_trainer, trainer, is_fully_async=is_fully_async)
        return trainer

    # -- the run -----------------------------------------------------------------------------------------
    def _open_probe(self) -> None:
        from probe.sdk.settings.settings import env_run_id

        cfg = self.cfg
        resume = read_resume_step(cfg)
        if env_run_id():
            from probe.sdk.run.samples import attach_producer

            run = attach_producer(PRODUCER)
            _rl_owner.send_missing_config(run, get_config(cfg))
        else:
            run, self._is_owner = _rl_owner.open_run(
                name=get_run_name(cfg), external_id=get_external_id(cfg),
                rewind_step=get_rewind_step(resume) if resume > 0 else None,
                config=get_config(cfg), init_kwargs={},
                resume_from=get_resume_folder(cfg, resume), should_stamp_checkpoints=True,
            )
        self._probe_run = run
        samples = run.samples.as_producer(PRODUCER)
        tokenizer = self.tokenizer
        mapper = OutputMapper(
            decode=lambda ids: tokenizer.decode(ids, skip_special_tokens=False),
            tokens_to_text=getattr(tokenizer, "convert_ids_to_tokens", None),
            scenario_keys=[name for name in os.environ.get(SCENARIO_KEYS_ENV, "").split(",") if name.strip()],
            host=socket.gethostname(),
            worker=f"pid:{os.getpid()}",
        )
        recorder = SkyrlRecorder(
            samples, mapper, is_zero_variance_filter=bool(cfg.trainer.algorithm.zero_variance_filter),
            floor=get_rewind_step(resume) if resume > 0 else 0,
        )
        self.hooks = SkyrlHooks(run, recorder, self.guard, live=SkyrlLive(samples, mapper, self.guard))
        phases.set_active_clock(self.hooks.phases)
        self.guard.call("phases", phases.install_phase_timer, Timer)
        self.guard.call("base model", record_base_model, run, cfg)
        training = build_training_plan(getattr(cfg.trainer.algorithm, "policy_loss_type", None))
        plan: dict[str, Any] = {"producers": [PRODUCER], "training": training, "unsupported": UNSUPPORTED}
        if cfg.trainer.fully_async.enabled:
            plan["max_staleness"] = int(cfg.trainer.fully_async.max_staleness_steps)
        samples.plan(**plan)
        refuse_commands(samples, COMMAND_REFUSAL)

    def _close_probe(self, status: str) -> None:
        """This producer's end: its last seals and the final step; the owner (here, or the driver) closes."""
        run, hooks = self._probe_run, self.hooks
        if run is None or hooks is None:
            return
        phases.set_active_clock(None)
        self.final_step = hooks.recorder.close()
        samples = run.samples.as_producer(PRODUCER)
        if self.final_step is not None:
            samples.plan(final_step=self.final_step)
        if self._is_owner:
            _rl_owner.close_run(run, samples, final_step=self.final_step, should_finish=True, status=status)
        else:
            samples.close()
            run.finish(status)  # the producer's lease, released with how it ended; never the run's status
