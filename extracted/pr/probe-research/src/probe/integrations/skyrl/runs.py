"""The run a SkyRL job writes to (RL plan §6.3, §6.7): where a relaunch resumes, the run's identity, and the
`PROBE_*` environment the Ray task needs (SkyRL forwards only an allowlist, `utils/utils.py:1004-1206`).
Reads a SkyRL config by attribute. Line refs are `NovaSky-AI/SkyRL@d87004689e3a`."""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from typing import Any

from probe.generated.samples import CaptureField

#: SkyRL's checkpoint folders and its pointer to the newest (`trainer.py:1771`, `:1805`).
GLOBAL_STEP_FOLDER = re.compile(r"global_step_(\d+)$")
LATEST_STEP_FILE = "latest_ckpt_global_step.txt"
#: A credential the job hands the Ray task instead of a minted run token (a project-bound token cannot mint one).
WORKER_TOKEN_ENV = "PROBE_SKYRL_WORKER_TOKEN"
#: What SkyRL cannot give a sample, declared as the run opens (`plan(unsupported=)`), and why
#: (`skyrl_gym_generator.py` at the pin).
UNSUPPORTED = {
    CaptureField.MESSAGES: ("the generator's chat history is local to agent_loop and discarded "
                            "(skyrl_gym_generator.py:394-397); a sample holds token ids, and step-wise rows text Probe "
                            "decodes from them"),
    CaptureField.TOOL_CALL_IDS: "the environment parses tool calls from the model's text itself and names none",
    CaptureField.TOOL_CALL_ARGUMENTS: ("the environment parses tool calls from the model's text itself and keeps no "
                                       "arguments"),
    CaptureField.TOOL_RESULT_LINKS: "a tool's result comes back as observation text, linked to no call",
    CaptureField.REASONING: "the generator keeps token ids only: no engine field holds reasoning apart from the content",
    CaptureField.ENVIRONMENT_FILES: ("env.step runs in a thread pool that carries no rollout context "
                                     "(skyrl_gym_generator.py:279-282, :537)"),
}


def get_rewind_step(checkpoint_step: int) -> int:
    """SkyRL's `global_step_k` resumes training at step k+1 (`trainer.py:325`, `:355`): `Rewind(step=k+1)`."""
    return checkpoint_step + 1


def read_resume_step(train_config: Any) -> int:
    """The checkpoint step a launch resumes from, as `load_checkpoints` will pick it (`trainer.py:1830-1885`),
    or 0 for a fresh start. A pointer this machine cannot read (a bucket path) reads as a fresh start."""
    trainer = getattr(train_config, "trainer", None)
    mode = str(getattr(trainer, "resume_mode", None) or "none").lower()
    if mode == "none":
        return 0
    if mode == "from_path":
        match = GLOBAL_STEP_FOLDER.search(str(getattr(trainer, "resume_path", "") or "").rstrip("/"))
        return int(match.group(1)) if match else 0
    pointer = os.path.join(str(getattr(trainer, "ckpt_path", "") or ""), LATEST_STEP_FILE)
    try:
        with open(pointer, encoding="utf-8") as handle:
            return int(handle.read().strip())
    except (OSError, ValueError):
        return 0


#: `trainer.run_name` SkyRL ships (`config.py`) when nobody names the run: kept as text (it keys the run), composed.
SKYRL_DEFAULT_RUN_NAMES = frozenset({"test_run", "skyrl_sft_run"})


def get_run_name(train_config: Any) -> Any:
    """The run's name: SkyRL's `trainer.run_name`; its shipped default is a ComposedName, so Probe may title it."""
    from probe.sdk.agent_session import ComposedName

    name = getattr(getattr(train_config, "trainer", None), "run_name", None)
    return ComposedName(name) if name in SKYRL_DEFAULT_RUN_NAMES else name


def get_resume_folder(train_config: Any, step: int) -> str | None:
    """The `global_step_{step}` folder a launch resumes from (``step`` from `read_resume_step`, read once), whose
    stamp names the attempt that wrote it (`_rl_owner.stamp_checkpoint`); None for a fresh start."""
    trainer = getattr(train_config, "trainer", None)
    if not step:
        return None
    if str(getattr(trainer, "resume_mode", None) or "none").lower() == "from_path":
        return str(getattr(trainer, "resume_path", "") or "").rstrip("/") or None
    root = str(getattr(trainer, "ckpt_path", "") or "")
    return os.path.join(root, f"global_step_{step}") if root else None


def get_external_id(train_config: Any) -> str:
    """One SkyRL job's identity across relaunches: its project and run name."""
    trainer = getattr(train_config, "trainer", None)
    return f"skyrl:{getattr(trainer, 'project_name', '')}/{getattr(trainer, 'run_name', '')}"


def build_task_env(run: Any, environ: Mapping[str, str] | None = None) -> dict[str, str]:
    """The Ray task's environment: this driver's `PROBE_*` settings (never a credential: Ray's dashboard shows the
    runtime env), and what the task needs to join the run: its id, epoch, server and a credential for this run
    only (`PROBE_SKYRL_WORKER_TOKEN`, else a run token; `_rl_owner.build_worker_env`)."""
    from .. import _rl_owner

    source = os.environ if environ is None else environ
    env = _rl_owner.get_worker_settings(source)
    if run is not None:
        env.update(_rl_owner.build_worker_env(run, source, worker_token_env=WORKER_TOKEN_ENV))
    return env


def get_config(train_config: Any) -> dict:
    """The SkyRL config (dataclasses, `config/config.py:2447-2450`) as the run's config, through the credential
    scrubber (keys and values)."""
    import dataclasses

    from probe.sdk.redaction import default_scrub

    try:
        raw = dataclasses.asdict(train_config) if dataclasses.is_dataclass(train_config) else dict(train_config)
    except Exception:  # noqa: BLE001 -- a config Probe cannot read never costs the run
        return {}
    return {"skyrl": default_scrub(raw)}


def record_base_model(run: Any, train_config: Any) -> None:
    """The Hub model the policy starts from (`trainer.policy.model.path`, `config/config.py:207-209, 856-857`) as
    the run's `init` use, by its uri (a run token may record it). A local folder records nothing. Off with read
    capture (`PROBE_CAPTURE_READS=0`)."""
    from probe.sdk.capture import lineage as inputs

    from .._hub import get_hub_model

    policy = getattr(getattr(train_config, "trainer", None), "policy", None)
    hub_ref = get_hub_model(getattr(getattr(policy, "model", None), "path", None))
    if hub_ref is not None and inputs.enabled(None):
        run.use_dataset(hub_ref.to_source(), role="init")
