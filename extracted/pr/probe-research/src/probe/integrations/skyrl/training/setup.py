"""The job-level Ray setup hook that reaches SkyRL's policy workers (S0 N1): the workers are actors made inside the
training task with plain actor options (`worker.py:866-904`); the task's `runtime_env.env_vars` (`PROBE_RUN_ID`, a
run token) reach them, but only a JOB-level `worker_process_setup_hook` runs in them, and a job's hook is read from
`RAY_JOB_CONFIG_JSON_ENV_VAR` at `ray.init`. So the driver adds ours there before SkyRL's `initialize_ray`, as verl's
launcher does; a hook the job already had runs after ours."""

from __future__ import annotations

import importlib
import json
import logging
import os
from collections.abc import Callable, MutableMapping

logger = logging.getLogger(__name__)

JOB_CONFIG_ENV = "RAY_JOB_CONFIG_JSON_ENV_VAR"
SETUP_HOOK = "probe.integrations.skyrl.training.setup.setup_worker"
#: A setup hook the job already had; ours runs it after its own (Ray takes one hook).
NEXT_SETUP_HOOK_ENV = "PROBE_SKYRL_NEXT_SETUP_HOOK"


def add_setup_hook(environ: MutableMapping[str, str]) -> Callable[[], None]:
    """Our hook in the job config Ray reads at `ray.init`; the job's own values win, its own hook runs after. Returns
    what puts the variable back as it was (call it once `ray.init` has read it)."""
    before = environ.get(JOB_CONFIG_ENV)
    config = json.loads(before or "{}")
    runtime_env = dict(config.get("runtime_env") or {})
    env_vars = dict(runtime_env.get("env_vars") or {})
    existing = runtime_env.get("worker_process_setup_hook")
    if isinstance(existing, str) and existing != SETUP_HOOK:
        env_vars.setdefault(NEXT_SETUP_HOOK_ENV, existing)
    runtime_env["worker_process_setup_hook"] = SETUP_HOOK
    if env_vars:
        runtime_env["env_vars"] = env_vars
    config["runtime_env"] = runtime_env
    environ[JOB_CONFIG_ENV] = json.dumps(config)

    def restore() -> None:
        if before is None:
            environ.pop(JOB_CONFIG_ENV, None)
        else:
            environ[JOB_CONFIG_ENV] = before

    return restore


def setup_worker() -> None:
    """Ray's `worker_process_setup_hook`: watch for SkyRL's policy worker in this process, then the job's own hook.
    Never raises for Probe's own failure."""
    try:
        from .training import install_worker_training

        install_worker_training()
    except Exception as exc:  # noqa: BLE001 -- fail open: the worker trains unrecorded
        logger.warning("Probe could not watch SkyRL's policy worker in this Ray worker; SkyRL continues: %s", exc)
    if next_hook := os.environ.get(NEXT_SETUP_HOOK_ENV):
        module, _, name = next_hook.rpartition(".")
        getattr(importlib.import_module(module), name)()
