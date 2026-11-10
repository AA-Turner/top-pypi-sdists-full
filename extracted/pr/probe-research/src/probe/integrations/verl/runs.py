"""The run a verl job writes to (RL plan §6.5, §6.7): where a relaunch resumes, the run's identity and config, and
the Ray job runtime env that carries Probe's setup hook and `PROBE_*` to every worker. Pure: reads a verl config by
attribute or key. Line refs are `verl-project/verl@b17218ba58a6`."""

from __future__ import annotations

import json
import os
import re
from collections.abc import Mapping, MutableMapping
from typing import Any

#: verl's checkpoint folders and its pointer to the newest (`utils/checkpoint/checkpoint_manager.py:222-252`).
GLOBAL_STEP_FOLDER = re.compile(r"global_step_(\d+)")
LATEST_STEP_FILE = "latest_checkpointed_iteration.txt"
#: Ray's driver reads its job config, runtime env included, from this variable at `ray.init`; `ray job submit
#: --runtime-env-json` arrives the same way, and verl reads it too (`trainer/constants_ppo.py:139`).
JOB_CONFIG_ENV = "RAY_JOB_CONFIG_JSON_ENV_VAR"
SETUP_HOOK = "probe.integrations.verl.setup_worker"
#: A setup hook the job already had; `setup_worker` runs it after Probe's (Ray takes one hook).
NEXT_SETUP_HOOK_ENV = "PROBE_VERL_NEXT_SETUP_HOOK"
#: A credential the job hands its workers instead of a minted run token (a project-bound token).
WORKER_TOKEN_ENV = "PROBE_VERL_WORKER_TOKEN"
#: `trainer.logger` names: Probe's backend, and the W&B ones verl defaults to (`trainer/config/ppo_trainer.yaml:156`).
PROBE_BACKEND = "probe"
WANDB_BACKENDS = ("wandb", "tracking", "vemlp_wandb")


def get_rewind_step(checkpoint_step: int) -> int:
    """verl's `global_step_k` resumes training at step k+1 (`v1/trainer_base.py:876`, `:455`; the fully async trainer's
    `global_step_k` is weight version k, whose next update is step k+1, `fully_async_trainer.py:1010`):
    `Rewind(step=k+1)`."""
    return checkpoint_step + 1


def read_resume_step(config: Any) -> int:
    """The checkpoint step a launch resumes from, as verl's `_load_checkpoint` picks it (`v1/trainer_base.py:850-877`,
    `ray_trainer.py:1052`): `trainer.resume_mode` `auto` reads the pointer in `default_local_dir`, `resume_path`
    names the folder. 0 for a fresh start or a pointer this machine cannot read."""
    trainer = _get(config, "trainer")
    mode = str(_get(trainer, "resume_mode") or "disable").lower()
    if mode == "resume_path":
        match = GLOBAL_STEP_FOLDER.search(str(_get(trainer, "resume_from_path") or ""))
        return int(match.group(1)) if match else 0
    if mode != "auto":
        return 0
    folder = str(_get(trainer, "default_local_dir") or "")
    if not folder:
        return 0
    folder = folder if os.path.isabs(folder) else os.path.join(os.getcwd(), folder)
    try:
        with open(os.path.join(folder, LATEST_STEP_FILE), encoding="utf-8") as handle:
            step = int(handle.read().strip())
    except (OSError, ValueError):
        return 0
    return step if os.path.isdir(os.path.join(folder, f"global_step_{step}")) else 0


#: verl's shipped `trainer.experiment_name`s, nobody's choice: `gsm8k` (`ppo_trainer.yaml`) and `test`
#: (`sft_trainer_engine.yaml`), at the pinned commit (tests/integrations/verl/pinned.py).
VERL_DEFAULT_EXPERIMENTS = frozenset({"gsm8k", "test"})


def get_run_name(experiment: Any) -> str:
    """The run's name: the experiment's, else "verl". Verl's shipped default and the bare fallback are names nobody
    chose, so a ComposedName (text unchanged: the launcher and the session key the run by config, not by name)."""
    from probe.sdk.agent_session import ComposedName

    if not experiment:
        return ComposedName("verl")
    name = str(experiment)
    return ComposedName(name) if name in VERL_DEFAULT_EXPERIMENTS else name


def get_resume_folder(config: Any, step: int) -> str | None:
    """The `global_step_{step}` folder a launch resumes from (``step`` from `read_resume_step`, read once), whose
    stamp names the attempt that wrote it (`_rl_owner.stamp_checkpoint`); None for a fresh start."""
    trainer = _get(config, "trainer")
    if not step:
        return None
    if str(_get(trainer, "resume_mode") or "disable").lower() == "resume_path":
        return str(_get(trainer, "resume_from_path") or "") or None
    folder = str(_get(trainer, "default_local_dir") or "")
    return os.path.join(folder, f"global_step_{step}") if folder else None


def get_names(config: Any) -> tuple[str, str]:
    """`trainer.project_name` and `trainer.experiment_name`."""
    trainer = _get(config, "trainer")
    return str(_get(trainer, "project_name") or ""), str(_get(trainer, "experiment_name") or "")


def make_backends(logger: Any) -> list[str]:
    """`trainer.logger` under the launcher: the configured backends with `probe` added and W&B taken out (verl's
    default is `["console", "wandb"]`; Probe records this run)."""
    current = [logger] if isinstance(logger, str) else [str(name) for name in (logger or ())]
    kept = [name for name in current if name not in WANDB_BACKENDS]
    return kept if PROBE_BACKEND in kept else [*kept, PROBE_BACKEND]


def get_external_id(config: Any, chosen_name: Any = None) -> str:
    """One verl job's identity across relaunches: its project and experiment name. A name the caller chose
    (`init_kwargs["name"]`) stands in for no experiment or a shipped default (`gsm8k`, `test`): the run then sends
    that name and mints no key, so the key must be the name's, or every such job would share one."""
    from probe.sdk.agent_session import ComposedName

    project, experiment = get_names(config)
    is_chosen = isinstance(chosen_name, str) and bool(chosen_name) and not isinstance(chosen_name, ComposedName)
    if is_chosen and (not experiment or experiment in VERL_DEFAULT_EXPERIMENTS):
        experiment = chosen_name
    return f"verl:{project}/{experiment}"


def get_run_config(config: Any) -> dict:
    """The verl config (an OmegaConf DictConfig, or the container `Tracking` gets) as the run's config, through the
    credential scrubber (keys and values)."""
    from probe.sdk.redaction import default_scrub

    raw = config
    try:
        from omegaconf import OmegaConf

        if OmegaConf.is_config(config):
            raw = OmegaConf.to_container(config, resolve=True, throw_on_missing=False)
    except Exception:  # noqa: BLE001 -- unresolvable or no OmegaConf: the raw mapping below
        pass
    if not isinstance(raw, Mapping):
        return {}
    try:
        return {"verl": default_scrub(dict(raw))}
    except Exception:  # noqa: BLE001 -- a config Probe cannot read never costs the run
        return {}


def build_runtime_env(run: Any, environ: Mapping[str, str]) -> dict:
    """The setup hook, this driver's `PROBE_*` settings (never a credential: the Ray dashboard shows the runtime
    env), and what a worker needs to join the run as a producer: its id, epoch, server and a credential for this
    run only (`PROBE_VERL_WORKER_TOKEN`, else a run token; `_rl_owner.build_worker_env`)."""
    from .. import _rl_owner

    env_vars = _rl_owner.get_worker_settings(environ)
    env_vars.pop(NEXT_SETUP_HOOK_ENV, None)
    env_vars.update(_rl_owner.build_worker_env(run, environ, worker_token_env=WORKER_TOKEN_ENV))
    return {"worker_process_setup_hook": SETUP_HOOK, "env_vars": env_vars}


def add_to_job_config(environ: MutableMapping[str, str], runtime_env: dict) -> None:
    """Merge ours into the job config Ray will read at `ray.init`; the job's own values win, and a setup hook it
    already had runs after ours (Ray takes one hook). verl's own `ray.init(runtime_env=...)` merges with it
    (`trainer/main_ppo.py:57-78`)."""
    config = json.loads(environ.get(JOB_CONFIG_ENV) or "{}")
    job_env = config.get("runtime_env") or {}
    env_vars = {**runtime_env["env_vars"], **(job_env.get("env_vars") or {})}
    existing_hook = job_env.get("worker_process_setup_hook")
    if isinstance(existing_hook, str) and existing_hook != SETUP_HOOK:
        env_vars[NEXT_SETUP_HOOK_ENV] = existing_hook
    config["runtime_env"] = {**job_env, **runtime_env, "env_vars": env_vars}
    environ[JOB_CONFIG_ENV] = json.dumps(config)


def _get(target: Any, name: str) -> Any:
    if target is None:
        return None
    if isinstance(target, Mapping):
        return target.get(name)
    try:
        return getattr(target, name, None)
    except Exception:  # noqa: BLE001 -- an OmegaConf interpolation that cannot resolve here
        return None
