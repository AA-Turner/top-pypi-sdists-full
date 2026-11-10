"""The train ranks' side (RL plan §6.1 W15): after each train step, every data-parallel shard writer
(TP rank 0, last PP stage, CP rank 0) sends a trainer part per sample it trained (consumed step and
version, its DP rank, the trainer-side per-token arrays), Miles' normalized reward as a scorer part,
seals and commits the step; weight pushes become weight versions, saved iterations their checkpoints."""

from __future__ import annotations

import glob
import logging
import os
import re
import threading
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from string import Formatter
from typing import Any

from probe.integrations.miles.samples.mapping import build_train_key, to_finite_lists, to_list, to_number
from probe.integrations.miles.samples.producers import PROCESS, ROLLOUT, get_trainer_name

logger = logging.getLogger(__name__)

#: Trainer-side per-token fields in a train shard (`dashboard/dump_reader.py:200-230`) by their Probe name.
TRAINER_ARRAYS = {
    "trainer_logprobs": "log_probs",
    "ref_logprobs": "ref_log_probs",
    "entropy": "entropy",
    "ref_entropy": "ref_entropy",
    "advantages": "advantages",
    "returns": "returns",
    "loss_mask": "loss_masks",
}
#: Megatron's last saved iteration (`backends/training_utils/checkpoint/tracker.py:5`).
TRACKER_FILE = "latest_checkpointed_iteration.txt"
#: An FSDP save of rollout N is `iter_{N+1}` (its tracker says N+1) and records N here as `rollout_id`
#: (`fsdp_utils/checkpoint.py:209-265`); Megatron's folder is the rollout itself and has no such file.
FSDP_META_FILE = "meta.json"
#: A LoRA save writes no tracker: `{save}/iter_N/adapter` (`megatron_utils/lora/checkpoint.py:652-674`) is a
#: relative link to `.adapter.<16 hex>/`, put in place by rank 0 once every rank wrote it (`adapter/commit.py:3-4,
#: 137-150`); a save still being written has the folder and no link.
ADAPTER_LINK = "adapter"
_COMMITTED_ADAPTER = re.compile(r"\.adapter\.[0-9a-f]{16}")
_ITERATION_FOLDER = re.compile(r"iter_(\d+)")
#: In a `--save-hf` folder once every rank finished its export (`hf_utils/config.py:151-156`, `hf_export.py:99`).
HF_COMPLETE_MARKER = ".complete"
#: The `--save-hf` template's field (`save_hf.format(rollout_id=...)`, `megatron_utils/actor.py:977`).
HF_STEP_FIELD = "rollout_id"


class Position:
    """Where this rank sits: tensor, pipeline, data and context parallel coordinates."""

    def __init__(self, *, tp: int, is_pp_last: bool, dp: int, dp_size: int, cp: int, cp_size: int) -> None:
        self.tp, self.is_pp_last, self.dp, self.dp_size, self.cp, self.cp_size = tp, is_pp_last, dp, dp_size, cp, cp_size

    @property
    def is_shard_writer(self) -> bool:
        """One process per data-parallel shard holds its per-token outputs (`train_dump.py:14-16`)."""
        return self.tp == 0 and self.is_pp_last and self.cp == 0


def read_position() -> Position | None:
    """Upstream's parallel state (`backends/training_utils/parallel.py:20`), else Megatron's (the fork)."""
    try:
        from miles.backends.training_utils.parallel import get_parallel_state

        state = get_parallel_state()
        dp = state.effective_dp  # intra or independent data parallel, whichever this run uses
        return Position(tp=state.tp.rank, is_pp_last=bool(state.is_pp_last_stage), dp=dp.rank, dp_size=dp.size,
                        cp=state.cp.rank, cp_size=state.cp.size)
    except Exception:  # noqa: BLE001 -- the fork, or no parallel state yet
        pass
    try:
        from megatron.core import mpu

        return Position(tp=mpu.get_tensor_model_parallel_rank(), is_pp_last=mpu.is_pipeline_last_stage(),
                        dp=mpu.get_data_parallel_rank(), dp_size=mpu.get_data_parallel_world_size(),
                        cp=mpu.get_context_parallel_rank(), cp_size=mpu.get_context_parallel_world_size())
    except Exception:  # noqa: BLE001
        return None


class TrainerCapture:
    """One train process's state: the last weight version it pushed, its last trained step, the
    checkpoints it recorded and whether it declared the producers."""

    def __init__(self) -> None:
        self.pushed_version: int | None = None
        self.trained_step: int | None = None
        self._version_after: dict[int, int] = {}
        self._checkpoints: set[int] = set()
        self._has_declared = False
        self._lock = threading.Lock()

    def on_train_data(self, args: Any, rollout_id: int, rollout_data: dict, position: Position | None = None) -> None:
        """A train step finished on this rank (`megatron_utils/actor.py:881`)."""
        position = position or read_position()
        with self._lock:
            self.trained_step = rollout_id
        if position is None or not position.is_shard_writer:
            return
        model_id = getattr(args, "trainer_model_id", None)
        name = get_trainer_name(position.dp, model_id)
        writer = PROCESS.get_samples(name, args)
        if writer is None:
            return
        if position.dp == 0:
            self._send_producer_plan(writer, position.dp_size, model_id)
            self.record_checkpoints(writer, args, model_id)
        trainer_parts, scorer_parts = build_trainer_parts(rollout_data, rollout_id, position, self.pushed_version)
        writer.log(trainer_parts, role="trainer", step=rollout_id)
        writer.log(scorer_parts, role="scorer", step=rollout_id)
        writer.seal(rollout_id)
        writer.commit(rollout_id, consumed_at=datetime.now(timezone.utc))

    def on_weights_pushed(self, args: Any, version: int, position: Position | None = None) -> None:
        """A weight sync went through (`weight_update/updater.py:140`); the shard-0 writer records it, with the step's
        save when it is already committed: Miles saves a step before pushing its weights (`train_async.py:137-157`,
        `train.py:153-174`), and the run's last save is never seen by a later train step."""
        with self._lock:
            self.pushed_version = version
            if self.trained_step is not None:
                self._version_after.setdefault(self.trained_step, version)
        position = position or read_position()
        if position is None or not position.is_shard_writer or position.dp != 0:
            return
        model_id = getattr(args, "trainer_model_id", None)
        writer = PROCESS.get_samples(get_trainer_name(0, model_id), args)
        if writer is not None:
            writer.weights(version, after_step=self.trained_step, policy_id=model_id or None)
            self.record_checkpoints(writer, args, model_id)

    def record_checkpoints(self, writer: Any, args: Any, model_id: str | None) -> None:
        """The newest committed save (full-model, LoRA or `--save-hf`) as a checkpoint reference, and on the
        weight version that came out of that step (the version pushed after it: versions count optimizer steps,
        `megatron_utils/model.py:678-680`). Looked for after each train step and each weight push: an async save
        commits a step late, a sync one (the run's last, `train_async.py:142`) before its push."""
        saved = find_new_checkpoint(args, self._checkpoints)
        if saved is None:
            return
        self._checkpoints.add(saved.step)
        record_checkpoint(PROCESS.get_handle(args), saved)
        version = self._version_after.get(saved.step)
        if version is not None:
            writer.weights(version, after_step=saved.step, checkpoint={"uri": saved.uri, "step": saved.step},
                           policy_id=model_id or None)

    def _send_producer_plan(self, writer: Any, dp_size: int, model_id: str | None) -> None:
        if self._has_declared:
            return
        self._has_declared = True
        writer.plan(producers=[ROLLOUT, *(get_trainer_name(dp, model_id) for dp in range(max(1, dp_size)))])


def build_trainer_parts(data: dict, rollout_id: int, position: Position, version: int | None) -> tuple[list, list]:
    """Each trained row's trainer part (and its normalized reward as a scorer part). Keys are rebuilt
    the way the rollout hook built them (`build_train_key`). Context parallelism leaves this rank a
    slice of each array, so its arrays are left out and the sample reads misaligned."""
    # Columns may be numpy arrays (`train_data_conversion.py:44-70`): never test them for truth.
    raw_indices, tokens = data.get("sample_indices"), data.get("tokens")
    indices = to_list(raw_indices) if raw_indices is not None else []
    tokens = tokens if tokens is not None else []
    occurrences = Counter(indices)
    rewards = data.get("rewards")
    trainer_parts, scorer_parts = [], []
    for row, index in enumerate(indices):
        if row >= len(tokens):
            break
        key = build_train_key(rollout_id, index, tokens[row])
        part: dict[str, Any] = {"key": key, "consumed_step": rollout_id, "trainer_rank": position.dp,
                                "occurrence": occurrences[index]}
        if version is not None:
            part["consumed_version"] = version
        if position.cp_size > 1:
            part["is_misaligned"] = True
        else:
            arrays = {name: to_finite_lists(to_list(data[field][row])) for name, field in TRAINER_ARRAYS.items()
                      if data.get(field) is not None and row < len(data[field])}
            if arrays:
                part["trainer_token_arrays"] = arrays
        trainer_parts.append(part)
        if rewards is not None and row < len(rewards) and (normalized := to_number(rewards[row])) is not None:
            scorer_parts.append({"key": key, "normalized_reward": normalized})
    return trainer_parts, scorer_parts


class SavedCheckpoint:
    """One saved iteration: the rollout it holds, where Miles wrote it (a local path, or a bucket uri), in which
    format, and its HF export when that finished. An HF-only save (`--save-hf` without `--save`) has no
    ``location``. ``name`` is its folder's (`iter_N`; an FSDP save of rollout N is `iter_{N+1}`)."""

    def __init__(self, step: int, location: str | None, hf_location: str | None = None, *,
                 save_format: str = "megatron", name: str | None = None) -> None:
        self.step, self.location, self.hf_location, self.save_format = step, location, hf_location, save_format
        self.name = name or f"iter_{step:07d}"

    @property
    def uri(self) -> str:
        """The uri the artifact row and the weight version both carry, so the server joins them."""
        return to_checkpoint_uri(str(self.location or self.hf_location))


def find_new_checkpoint(args: Any, known: set[int]) -> SavedCheckpoint | None:
    """The newest committed save, when not yet recorded: a full-model save (the tracker file), a LoRA save (a
    committed `iter_N/adapter`), or with no `--save` a finished `--save-hf` folder; the step's finished HF export
    rides along. With `--save`, an export never names a step itself: an async full-model save writes its tracker
    after the export finished (`actor.py:495-499`), and would never be recorded."""
    save = getattr(args, "save", None) or getattr(getattr(args, "backend", None), "save", None)
    template = getattr(args, "save_hf", None)
    template = template if isinstance(template, str) and template else None
    iteration = read_tracker_step(save) if save else None
    tracked = read_saved_rollout(save, iteration) if iteration is not None else None
    adapters = list_committed_adapters(save) if save else {}
    exports = list_finished_exports(template, {tracked, *adapters} - {None}) if template else {}
    steps = {tracked, *adapters} - {None} if save else set(exports)
    if not steps or max(steps) in known:
        return None
    step = max(steps)
    if step in adapters:
        return SavedCheckpoint(step, adapters[step], exports.get(step), save_format="lora")
    if step == tracked:
        folder = f"iter_{iteration:07d}"
        return SavedCheckpoint(step, str(Path(str(save)) / folder), exports.get(step), name=folder)
    return SavedCheckpoint(step, None, exports[step], save_format="hf")


def read_tracker_step(save: Any) -> int | None:
    """Megatron's tracker file (`{save}/latest_checkpointed_iteration.txt`): a full-model save's iteration."""
    try:
        text = (Path(str(save)) / TRACKER_FILE).read_text().strip()
    except OSError:
        return None
    return int(text) if text.isdigit() else None


def read_saved_rollout(save: Any, iteration: int) -> int:
    """The rollout the full-model save `{save}/iter_{iteration}` holds: the `rollout_id` an FSDP save records (its
    folder is one past it), else the iteration itself (Megatron)."""
    meta = read_fsdp_meta(Path(str(save)) / f"iter_{iteration:07d}")
    rollout = meta.get("rollout_id")
    return rollout if isinstance(rollout, int) and not isinstance(rollout, bool) and rollout >= 0 else iteration


def read_fsdp_meta(folder: Path) -> dict:
    """An FSDP save folder's `meta.json` (`fsdp_utils/checkpoint.py:252-262`), or {} for any other save."""
    import json

    try:
        meta = json.loads((folder / FSDP_META_FILE).read_text())
    except (OSError, ValueError):
        return {}
    return meta if isinstance(meta, dict) else {}


def list_committed_adapters(save: Any) -> dict[int, str]:
    """Each iteration's committed LoRA save, `{save}/iter_N/adapter`, by its step."""
    try:
        folders = list(Path(str(save)).iterdir())
    except OSError:
        return {}
    found = {}
    for folder in folders:
        match = _ITERATION_FOLDER.fullmatch(folder.name)
        link = folder / ADAPTER_LINK
        try:
            target = os.readlink(link) if match and link.is_symlink() else ""
        except OSError:
            continue
        if _COMMITTED_ADAPTER.fullmatch(target) and (folder / target).is_dir():
            found[int(match.group(1))] = str(link)
    return found


def list_finished_exports(template: str, steps: set[int]) -> dict[int, str]:
    """Each finished `--save-hf` export by its step. A template with no `{rollout_id}` is one folder each save
    overwrites: it is the newest of ``steps`` (the saves it was written with) when finished."""
    try:
        pieces = list(Formatter().parse(template))
    except ValueError:
        return {}
    fields = {field for _text, field, _spec, _conversion in pieces if field is not None}
    if not fields:
        return {max(steps): template} if steps and os.path.isfile(os.path.join(template, HF_COMPLETE_MARKER)) else {}
    if fields != {HF_STEP_FIELD}:
        return {}  # another field: Miles' own `format(rollout_id=...)` would fail on it
    regex, wildcard, group = "", "", r"(?P<step>\d+)"
    for text, field, _spec, _conversion in pieces:
        regex, wildcard = regex + re.escape(text), wildcard + glob.escape(text)
        if field is not None:  # the step, and the same step again wherever the template repeats it
            regex, wildcard, group = regex + group, wildcard + "*", "(?P=step)"
    pattern, found = re.compile(regex), {}
    for path in glob.glob(wildcard):
        match = pattern.fullmatch(path)
        if match and os.path.isfile(os.path.join(path, HF_COMPLETE_MARKER)):
            found[int(match.group("step"))] = path
    return found


def to_checkpoint_uri(location: str) -> str:
    """A bucket uri as is; a bucket mount as its bucket (`/gcs/<bucket>/x` is `gs://<bucket>/x`); any
    other path as the `file://` uri a path reference records (`sdk/artifact/hashing.py:38`)."""
    if "://" in location:
        return location
    resolved = str(Path(location).expanduser().absolute())
    if resolved.startswith("/gcs/") and resolved.count("/") >= 2:
        return "gs://" + resolved[len("/gcs/"):]
    return Path(resolved).as_uri()


def record_checkpoint(run: Any, saved: SavedCheckpoint) -> None:
    """Checkpoint references (no upload): Miles' save (an iteration folder, or its LoRA adapter), and its HF
    export when finished. The export goes first, so the save is the newer row of its step: the best and latest reads
    break a same-step tie by the newer row (`app/files/catalog/checkpoints/best.py` `_pick`, `checkpoints.select`),
    and the save is the one training resumes from and the weight version names."""
    for name, location, save_format in ((f"{saved.name}-hf", saved.hf_location, "hf"),
                                        (saved.name, saved.location, saved.save_format)):
        if not location:
            continue
        uri = to_checkpoint_uri(location)
        is_local = uri.startswith("file://")
        run.log_artifact(name, uri=uri, path=location if is_local else None, reference=is_local,
                         allow_missing=True, kind="checkpoint", step_index=saved.step,
                         meta={"miles": {"rollout_id": saved.step, "format": save_format}}, strict=False)


TRAINER = TrainerCapture()
