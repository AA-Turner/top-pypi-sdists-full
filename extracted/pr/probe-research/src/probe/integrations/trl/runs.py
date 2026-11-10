"""The run a TRL trainer writes to (RL plan §3.5, §6.6, §6.7): where a relaunch resumes, the run's name and config,
the models a sample names (a distillation teacher), and no W&B. Pure: reads a trainer by attribute. Line refs are
transformers 5.22 and `huggingface/trl@4ae4d34a86f3`."""

from __future__ import annotations

import json
import os
import re
from collections.abc import Mapping
from typing import Any

from probe.sdk.agent_session import ComposedName

#: transformers' checkpoint folders (`trainer_utils._re_checkpoint`) and the state file in each.
CHECKPOINT_FOLDER = re.compile(r"^checkpoint-(\d+)$")
TRAINER_STATE_FILE = "trainer_state.json"
#: The HF callback whose run identity a tracker opens with (`report_to="probe"`).
PROBE_CALLBACK = ("probe.integrations.huggingface", "ProbeCallback")
WANDB = "wandb"
WANDB_CALLBACK = "WandbCallback"
#: A Probe checkpoint named as a teacher: `checkpoint:<run id>@step<N>`, or `checkpoint:<artifact id>`.
PROBE_CHECKPOINT = re.compile(r"^checkpoint:([0-9a-fA-F-]{36})(?:@(?:step)?(\d+))?$")


def get_rewind_step(checkpoint_step: int) -> int:
    """`train(resume_from_checkpoint=checkpoint-k)` trains step k+1 next, so the run continues from R = k+1:
    `Rewind(step=k+1)`."""
    return checkpoint_step + 1


def read_resume_step(resume_from_checkpoint: Any, output_dir: str | None) -> int | None:
    """The step a `train(resume_from_checkpoint=...)` resumes from, as transformers picks the folder (`True` = the
    highest `checkpoint-N` in ``output_dir``, `trainer.py:1537`): its `trainer_state.json` `global_step`, else N.
    None for a fresh start or a folder that cannot be read."""
    if resume_from_checkpoint is None or resume_from_checkpoint is False:
        return None
    if resume_from_checkpoint is True:
        root = output_dir or "."
        try:
            names = [name for name in os.listdir(root)
                     if CHECKPOINT_FOLDER.match(name) and os.path.isdir(os.path.join(root, name))]
        except OSError:
            return None
        if not names:
            return None
        folder = os.path.join(root, max(names, key=lambda name: int(CHECKPOINT_FOLDER.match(name)[1])))
    else:
        folder = str(resume_from_checkpoint)
    try:
        with open(os.path.join(folder, TRAINER_STATE_FILE), encoding="utf-8") as handle:
            step = json.load(handle).get("global_step")
        if isinstance(step, int) and step >= 0:
            return step
    except (OSError, ValueError, AttributeError):
        pass
    match = CHECKPOINT_FOLDER.match(os.path.basename(os.path.normpath(folder)))
    return int(match[1]) if match else None


def parse_model_ref(value: Any) -> dict | None:
    """A model named by the caller: `probe.samples.generated_by(...)` text, a ModelRef dict, a Probe checkpoint
    (`checkpoint:<run>@step<N>` names that run, so the server writes its `derived_from` edge), or any other text
    as an outside model."""
    from probe.sdk.run.samples.refs import parse_generated_by

    if value is None:
        return None
    if isinstance(value, Mapping):
        return dict(value)
    text = str(value)
    parsed = parse_generated_by(text)
    if parsed is not None:
        return parsed
    match = PROBE_CHECKPOINT.match(text)
    if match and match[2] is not None:
        return {"kind": "run", "run_id": match[1].lower(), "step": int(match[2])}
    if match:
        return {"kind": "checkpoint", "artifact_id": match[1].lower()}
    return {"kind": "external", "name": text[:512]}


def get_teacher_ref(trainer: Any, teacher: Any) -> dict | None:
    """A distillation teacher: the one `track(teacher=...)` names, else TRL's teacher path and revision
    (`distillation_config.py:43-46`, `teacher_model_server_url` for the server trainer) as an outside model, or a
    local folder as a checkpoint by uri, else the teacher model's own Hub name."""
    if teacher is not None:
        return parse_model_ref(teacher)
    args = trainer.args
    name = getattr(args, "teacher_model_name_or_path", None) or getattr(args, "teacher_model_server_url", None)
    if not name:
        model = getattr(trainer, "teacher_model", None)
        for _ in range(4):  # under accelerate / DDP / DeepSpeed wrappers
            inner = getattr(model, "module", None)
            if inner is None:
                break
            model = inner
        name = getattr(model, "name_or_path", None) or getattr(getattr(model, "config", None), "_name_or_path", None)
    if not isinstance(name, str) or not name:
        return None
    if os.path.isdir(name):
        from probe.sdk.artifact.hashing import local_file_uri

        return {"kind": "checkpoint", "uri": local_file_uri(os.path.abspath(name))}
    ref = {"kind": "external", "name": name[:512]}
    revision = getattr(args, "teacher_model_revision", None)
    if isinstance(revision, str) and revision:
        ref["revision"] = revision[:256]
    return ref


def find_probe_callback(trainer: Any) -> Any:
    """The HF `ProbeCallback` on this trainer that logs (`report_to="probe"`, or one passed in `callbacks`)."""
    callbacks = getattr(getattr(trainer, "callback_handler", None), "callbacks", ())
    return next((callback for callback in callbacks
                 if (type(callback).__module__, type(callback).__name__) == PROBE_CALLBACK
                 and not getattr(callback, "_stood_down", False)), None)


def get_identity(trainer: Any, init_kwargs: Mapping[str, Any]) -> tuple[str, dict, Any]:
    """The run's name, `probe.init()` keywords and the HF callback they came from: its project and name when it
    has some, `track()`'s keywords over them, else the trainer's `run_name`, else its output folder's name. The
    job's run key is not the name (`run_key.py`); a checkpoint from before keys finds its run by `trl:<name>`."""
    callback = find_probe_callback(trainer)
    kwargs: dict[str, Any] = {}
    name = None
    if callback is not None:
        kwargs.update({key: value for key, value in (("project", getattr(callback, "_project", None)),
                                                     ("experiment", getattr(callback, "_experiment_name", None)))
                       if value})
        kwargs.update(getattr(callback, "_init_kwargs", None) or {})
        name = getattr(callback, "_run_name", None)
    kwargs.update(init_kwargs)
    name = kwargs.pop("name", None) or name or _get_args_name(
        trainer.args, _get_model_short_name(trainer), _get_trainer_suffixes(trainer) or TRL_DEFAULT_SUFFIXES
    )
    return name if isinstance(name, str) else str(name), kwargs, callback


def get_config(trainer: Any) -> dict:
    """`TrainingArguments.to_dict()` (it masks `*_token`) through the credential scrubber, when no HF callback is
    there to merge it."""
    from probe.sdk.redaction import default_scrub

    to_dict = getattr(trainer.args, "to_dict", None)
    try:
        config = dict(to_dict()) if callable(to_dict) else {}
    except Exception:  # noqa: BLE001 -- a config Probe cannot read never costs the run
        config = {}
    return {"trl": default_scrub(config)}


def drop_wandb(trainer: Any) -> bool:
    """Probe records RL runs without W&B: `wandb` leaves `report_to`, and its callback, built with the trainer,
    leaves the trainer (TRL's `log()` also reads `report_to` for its completions table, `grpo_trainer.py:3467`).
    True when there was one to drop."""
    args = getattr(trainer, "args", None)
    report_to = getattr(args, "report_to", None)
    names = [report_to] if isinstance(report_to, str) else list(report_to or [])
    is_dropped = WANDB in names
    if is_dropped:
        args.report_to = [name for name in names if name != WANDB]
    for callback in list(getattr(getattr(trainer, "callback_handler", None), "callbacks", ())):
        if type(callback).__name__ == WANDB_CALLBACK:
            trainer.remove_callback(callback)
            is_dropped = True
    return is_dropped


#: Folders transformers fills in when nobody names one (`TrainingArguments.output_dir`'s default, the
#: bare `Trainer`'s): none of the researcher's words, so composed.
LIBRARY_FOLDERS = frozenset({"trainer_output", "tmp_trainer"})
#: TRL's own default folder when a trainer gets `args=None` is `f"{model_name}-<suffix>"` (`grpo_trainer.py:330`
#: and its siblings): the suffix is the trainer class's name less `Trainer` (`AsyncGRPO`, `GMPO`, ...), the model
#: name the model id's last path part. Matched against THIS trainer's classes and model; these when it is unknown.
TRL_DEFAULT_SUFFIXES = ("SFT", "DPO", "GRPO", "KTO", "RLOO", "Reward", "Distillation")


def _get_trainer_suffixes(trainer: Any) -> tuple[str, ...]:
    """The default-folder suffixes this trainer's classes give (`GRPOTrainer` -> `GRPO`), the bare `Trainer` aside."""
    names = (cls.__name__ for cls in type(trainer).__mro__)
    return tuple(name.removesuffix("Trainer") for name in names if name.endswith("Trainer") and name != "Trainer")


def _get_model_short_name(trainer: Any) -> str | None:
    """The model id's last part as TRL takes it (`get_config_model_id(model.config).split("/")[-1]`), or None.
    Never raises: an odd model (a property that throws) only means no default-folder match."""
    try:
        model = getattr(trainer, "model", None)
        model_id = getattr(getattr(model, "config", None), "_name_or_path", None) or getattr(model, "name_or_path", None)
        return model_id.split("/")[-1] if isinstance(model_id, str) and model_id else None
    except Exception:  # noqa: BLE001 -- naming never costs the run
        return None


def _get_args_name(args: Any, model_short_name: str | None = None,
                   suffixes: tuple[str, ...] = TRL_DEFAULT_SUFFIXES) -> str:
    run_name = getattr(args, "run_name", None)
    output_dir = getattr(args, "output_dir", None)
    if run_name and run_name != (output_dir or "trl"):  # transformers 4.x defaulted run_name to output_dir
        return str(run_name)
    # A folder the researcher named is their name for the run; a library default or none is composed.
    folder = os.path.basename(os.path.normpath(str(output_dir))) if output_dir else ""
    # Composed keeps the text: a checkpoint from before run keys finds its run by `trl:<name>` (`run_key.py`).
    is_trl_default = model_short_name is not None and folder in {f"{model_short_name}-{s}" for s in suffixes}
    if folder in LIBRARY_FOLDERS or folder in (".", "..") or is_trl_default:
        return ComposedName(folder)
    return folder or ComposedName("trl")
