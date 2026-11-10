"""The driver's run (RL plan §6.1 W16): opened once per job, by the launcher before Ray starts (so every
worker can join it) or else by the driver's backend; resumed with an explicit rewind when Miles loads a
checkpoint; closed only after the terminal manifest and the producers' last seals."""

from __future__ import annotations

import argparse
import hashlib
import logging
import os
import uuid
from collections.abc import MutableMapping, Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from probe.integrations.miles.spec import build_run_spec

logger = logging.getLogger(__name__)

#: Megatron's last saved iteration in a checkpoint directory (`checkpoint/tracker.py:5`).
TRACKER_FILE = "latest_checkpointed_iteration.txt"
#: In a LoRA save (`--lora-adapter-path`): the rollout it ends, `{"iteration": N, ...}`
#: (`training_utils/checkpoint/adapter/adapter_dir.py:63, 158-161`).
ADAPTER_STATE_FILE = "training_state.json"
#: An FSDP save folder's own record: `next_rollout_id` is where a load of it continues (`fsdp_utils/checkpoint.py:178-188`).
FSDP_META_FILE = "meta.json"
#: A credential the job hands its workers instead of a minted run token (a project-bound token).
WORKER_TOKEN_ENV = "PROBE_MILES_WORKER_TOKEN"
#: The Miles flags the launcher reads before the script parses its own (`--load iter_N`, `--save`).
_LAUNCH_FLAGS = ("load", "save", "ckpt_step", "start_rollout_id", "wandb_group", "num_rollout", "lora_adapter_path")
_NUMBER_FLAGS = ("ckpt_step", "start_rollout_id", "num_rollout")
#: Without an optimizer a LoRA load restores weights only and the run starts over (`lora/checkpoint.py:742-744`).
_NO_OPTIMIZER_FLAG = "debug_disable_optimizer"


def read_launch_args(argv: Sequence[str]) -> SimpleNamespace:
    """The few Miles flags the run's identity and resume point need, read from the script's argv."""
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    for name in _LAUNCH_FLAGS:
        parser.add_argument("--" + name.replace("_", "-"), dest=name, type=int if name in _NUMBER_FLAGS else str,
                            default=None)
    parser.add_argument("--" + _NO_OPTIMIZER_FLAG.replace("_", "-"), dest=_NO_OPTIMIZER_FLAG, action="store_true")
    known, _ = parser.parse_known_args(list(argv))
    return SimpleNamespace(**vars(known))


def find_resume_step(load: Any, ckpt_step: Any = None, start_rollout_id: Any = None, *,
                     lora_adapter_path: Any = None, has_optimizer: bool = True) -> int | None:
    """The step the run continues from, R in `Rewind(step=R)`; None when nothing is loaded (a fresh run). An explicit
    `--start-rollout-id` wins (`ray/placement_group.py:222-230`). A LoRA resume (`--lora-adapter-path`) continues after
    the rollout its adapter saved, whatever `--load` holds (`megatron_utils/model.py:1082-1121`). Else Miles loading
    `iter_N` resumes at rollout N+1 (`:1121-1122`), and an FSDP save at the `next_rollout_id` it records (its folder
    is one past its rollout)."""
    if isinstance(start_rollout_id, int) and not isinstance(start_rollout_id, bool) and start_rollout_id > 0:
        return start_rollout_id
    adapter_step = read_adapter_rollout(lora_adapter_path) if lora_adapter_path and has_optimizer else None
    if adapter_step is not None:
        return adapter_step + 1
    if not load:
        return None
    path = Path(str(load)).expanduser()
    if isinstance(ckpt_step, int) and not isinstance(ckpt_step, bool) and ckpt_step >= 0:
        return _read_next_rollout(path / f"iter_{ckpt_step:07d}", ckpt_step)
    if path.name.startswith("iter_") and path.name[5:].isdigit():
        return _read_next_rollout(path, int(path.name[5:]))
    try:
        text = (path / TRACKER_FILE).read_text().strip()
    except OSError:
        return None
    return _read_next_rollout(path / f"iter_{int(text):07d}", int(text)) if text.isdigit() else None


def read_adapter_rollout(adapter_path: Any) -> int | None:
    """The last rollout a LoRA save trained (its `training_state.json` `iteration`), or None for a source with no
    training state (an outside PEFT adapter: Miles then resumes from `--load` alone)."""
    import json

    try:
        state = json.loads((Path(str(adapter_path)).expanduser() / ADAPTER_STATE_FILE).read_text())
    except (OSError, ValueError):
        return None
    iteration = state.get("iteration") if isinstance(state, dict) else None
    return iteration if isinstance(iteration, int) and not isinstance(iteration, bool) and iteration >= 0 else None


def _read_next_rollout(folder: Path, iteration: int) -> int:
    """Where a load of `iter_{iteration}` continues: the `next_rollout_id` an FSDP save records, else iteration + 1."""
    import json

    try:
        meta = json.loads((folder / FSDP_META_FILE).read_text())
    except (OSError, ValueError):
        meta = {}
    following = meta.get("next_rollout_id") if isinstance(meta, dict) else None
    return following if isinstance(following, int) and not isinstance(following, bool) and following >= 0 else iteration + 1


def make_external_id(args: Any, environ: MutableMapping[str, str]) -> str:
    """The run's external id: `MILES_RUN_ID` when set; else one derived from the folder this run saves
    to (`--save`), so a relaunch that loads it finds the same run; else a fresh one. Never from `--load`
    alone: unrelated runs load the same base checkpoint."""
    if configured := getattr(args, "probe_external_id", None) or environ.get("MILES_RUN_ID"):
        return str(configured)
    folder = getattr(args, "save", None)
    if folder:
        digest = hashlib.sha256(os.path.abspath(os.path.expanduser(str(folder))).encode()).hexdigest()[:16]
        return f"miles:save:{digest}"
    return f"miles:{uuid.uuid4()}"


def open_owner_run(args: Any, *, external_id: str, has_config: bool = True) -> Any:
    """Open the run and bind it as this process's active run (the RL adapters' shared open,
    `integrations/_rl_owner.py`). A resume (`--load` of a saved iteration) reopens it rewound to its resume
    step, in the same reopen that drops the newer metric points; a fresh launch onto a run of the same id
    starts a retry of it (`supersede`): training starts over at step 0. ``has_config=False`` (the launcher,
    which has only a few flags) leaves the config to the driver's backend. Raises when the run cannot open."""
    from probe.integrations._rl_owner import open_run

    spec = build_run_spec(args, external_id)
    links = spec.pop("links", {})
    resume_step = find_resume_step(getattr(args, "load", None), getattr(args, "ckpt_step", None),
                                   getattr(args, "start_rollout_id", None),
                                   lora_adapter_path=getattr(args, "lora_adapter_path", None),
                                   has_optimizer=not getattr(args, _NO_OPTIMIZER_FLAG, False))
    # The driver only orchestrates: the files Miles reads and writes are its actors', not this process's.
    spec.update(capture_reads=False, capture_outputs=False, snapshot=getattr(args, "probe_snapshot", None))
    config = spec.pop("config")
    from probe.sdk.capture.logs import early

    with early.keep_held_window():  # files off is not the log off: the driver's log takes the held tee below
        run, _ = open_run(name=spec.pop("name"), external_id=spec.pop("external_id"), rewind_step=resume_step,
                          config=config if has_config else None, init_kwargs=spec)
    # What the driver prints IS the job's console: kept as the run's log, files off (T17).
    try:
        run._start_capture(should_keep_files=False)
    except Exception as exc:  # noqa: BLE001 -- the log is a convenience
        logger.warning("Probe could not keep the Miles driver's log: %s", exc)
    try:
        run.link(**links)
    except Exception as exc:  # noqa: BLE001 -- links are a convenience
        logger.warning("Probe could not link the Miles run's native ids: %s", exc)
    return run


def record_base_model(run: Any, args: Any) -> None:
    """`--hf-checkpoint`, the model the policy starts from, as the run's `init` use (`POST /runs/{run}/uses` by uri, so
    a run token records it; idempotent): a Hub id by its Hub uri, as HF, ART and SkyRL send theirs; a local folder by
    its path (`local:/root/Qwen2.5-0.5B-Instruct`), since a Miles job loads its base model from disk. Off with read
    capture (`PROBE_CAPTURE_READS=0`); the driver's own `capture_reads=False` is about its files, not this."""
    from probe.sdk.capture import lineage as inputs
    from probe.sdk.catalog import SourceRef

    from .._hub import get_hub_model

    checkpoint = getattr(args, "hf_checkpoint", None)
    if not isinstance(checkpoint, str) or not checkpoint.strip() or not inputs.enabled(None):
        return
    hub_ref = get_hub_model(checkpoint)
    if hub_ref is not None:
        source = hub_ref.to_source()
    elif "://" in checkpoint:
        source = SourceRef(uri=checkpoint.strip(), kind="model")  # a bucket path names itself
    else:
        source = SourceRef(uri=Path(checkpoint).expanduser().absolute().as_uri(), kind="model")
    run.use_dataset(source, role="init")


def build_worker_env(run: Any, environ: MutableMapping[str, str]) -> dict[str, str]:
    """What every Ray worker needs to join the run as a producer, with a credential for this run only
    (`PROBE_MILES_WORKER_TOKEN` when set): the RL adapters' shared rule (`_rl_owner.build_worker_env`)."""
    from probe.integrations._rl_owner import build_worker_env as build_run_worker_env

    return build_run_worker_env(run, environ, worker_token_env=WORKER_TOKEN_ENV)


def close_owner_run(run: Any, args: Any, *, status: str | None) -> None:
    """The owner's finish (`_rl_owner.close_run`): the terminal manifest (final step = `num_rollout - 1`),
    the bounded wait for every declared producer's last seal (`PROBE_SAMPLES_CLOSE_WAIT`), then the run's
    close when ``status`` is given (None leaves it to whoever opened it: the launcher)."""
    from probe.integrations._rl_owner import close_run

    rollout_count = getattr(args, "num_rollout", None)
    has_count = isinstance(rollout_count, int) and not isinstance(rollout_count, bool) and rollout_count > 0
    if has_count:
        run.samples.plan(expected_steps=rollout_count)
    close_run(run, run.samples, final_step=rollout_count - 1 if has_count else None,
              should_finish=status is not None, status=status)
