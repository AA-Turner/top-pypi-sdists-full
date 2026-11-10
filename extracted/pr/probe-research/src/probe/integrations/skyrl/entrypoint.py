"""`trainer.override_entrypoint=probe.integrations.skyrl.entrypoint`: SkyRL's launch with Probe (RL plan §6.3).
The driver owns the run: it opens it (reopening it with a rewind on a resume), hands `PROBE_*` to the Ray task
SkyRL trains in, and after the task ends closes the run behind the producers' close barrier. Imports SkyRL and
Ray. Line refs are `NovaSky-AI/SkyRL@d87004689e3a`."""

from __future__ import annotations

import sys
from typing import Any

import ray

from .. import _rl_owner
from .runs import (
    build_task_env, get_resume_folder, get_config, get_external_id, get_rewind_step, get_run_name, read_resume_step,
)

#: SkyRL's dispatch flag (`entrypoints/main_base.py:420-430`): consumed there, not a config field to parse.
OVERRIDE_FLAG = "trainer.override_entrypoint="


@ray.remote(num_cpus=1)
def probe_entrypoint(train_config: Any) -> int | None:
    """SkyRL's `skyrl_entrypoint` with `ProbeExp` (`main_base.py:404-408`): the trainer runs off the head node.
    Returns the last sealed step."""
    from .skyrl import ProbeExp

    exp = ProbeExp(train_config)
    exp.run()
    return exp.final_step


def main() -> None:
    from skyrl.train.config import SkyRLTrainConfig
    from skyrl.train.utils import validate_cfg
    from skyrl.train.utils.utils import initialize_ray

    argv = [arg for arg in sys.argv[1:] if not arg.startswith(OVERRIDE_FLAG)]
    train_config = SkyRLTrainConfig.from_cli_overrides(argv)
    validate_cfg(train_config)
    guard = _rl_owner.HookGuard("SkyRL")
    opened = guard.call("run open", _open_owner_run, train_config)
    run, is_owner = opened if opened else (None, False)
    initialize_ray(train_config)
    final_step, status = None, "failed"
    try:
        # Task-level env vars merge into the job's (`initialize_ray`'s allowlist, `utils/utils.py:1357-1371`).
        task = probe_entrypoint.options(runtime_env={"env_vars": build_task_env(run)})
        final_step = ray.get(task.remote(train_config))
        status = "completed"
    finally:
        if run is not None:
            guard.call("run close", _close_owner_run, run, final_step, status, is_owner)


def _open_owner_run(train_config: Any) -> tuple[Any, bool]:
    resume = read_resume_step(train_config)
    return _rl_owner.open_run(
        name=get_run_name(train_config),
        external_id=get_external_id(train_config),
        rewind_step=get_rewind_step(resume) if resume > 0 else None,
        config=get_config(train_config),
        init_kwargs={},
        resume_from=get_resume_folder(train_config, resume), should_stamp_checkpoints=True,
    )


def _close_owner_run(run: Any, final_step: int | None, status: str, is_owner: bool) -> None:
    """The terminal manifest (the task wrote its last step), the barrier, the run's own status."""
    samples = run.samples.as_producer("driver")
    _rl_owner.close_run(run, samples, final_step=final_step, should_finish=is_owner, status=status)
