"""One sample part made ready to journal: its task lifted out, logs and turns scrubbed, the full log
and per-token arrays put in bundles, token summaries computed and text over 64 KiB spilled to R2."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .bundles import BundleKind, Bundles
from .tokens import PerTokenPolicy, pick_token_arrays, summarize_tokens
from .wire import (
    MAX_INLINE_TEXT_BYTES,
    MAX_LOG_BYTES,
    TASK_FIELDS,
    TOKEN_INPUTS,
    cap_error_message,
    cut_tail,
    replace_nul_text,
    get_default_seal_step,
    measure_bytes,
    scrub_part,
    split_log,
    to_plain,
)


#: A text spilled to a temp file, waiting to be stored: (path, sha256, size in bytes).
PendingBlob = tuple[Path, str, int]


@dataclass
class PreparedPart:
    """A part ready to journal, the task item it lifted (first time only), whether it has_bundled
    for its step's bundles to close (its refs carry no sha256 until then), and the texts it spilled,
    stored by `store_blobs` after the writer's lock is released."""

    part: dict
    task: dict | None = None
    is_waiting_for_bundles: bool = False
    blobs: list[PendingBlob] = field(default_factory=list)


class PartPreparer:
    """Turns caller samples into parts. ``upload_text(path, sha256, size)`` stores one blob (the
    run's artifact door); ``scrub`` is the credential scrubber, str -> str."""

    def __init__(
        self,
        bundles: Bundles,
        *,
        scrub: Callable[[str], str],
        upload_text: Callable[[Path, str, int], None],
        policy: PerTokenPolicy | None = None,
    ) -> None:
        self._bundles = bundles
        self._scrub = scrub
        self._upload_text = upload_text
        self._policy = policy or PerTokenPolicy.from_env()
        self._tasks_sent: set[tuple[str, str]] = set()

    def prepare(self, sample: Any, *, role: str, seal_step: int | None) -> PreparedPart:
        """``sample`` as a part. Spilled texts are only written to temp files here: the caller stores them
        (`store_blobs`) outside its lock, so a slow upload holds no other producer thread (rl-scale C9)."""
        blobs: list[PendingBlob] = []
        try:
            return self._prepare(sample, role=role, seal_step=seal_step, blobs=blobs)
        except BaseException:
            _delete_files(blobs)
            raise

    def store_blobs(self, blobs: list[PendingBlob]) -> list[Exception]:
        """Store each spilled text through the run's artifact door, then delete its temp file; the
        failures, one per text that could not be stored."""
        failed: list[Exception] = []
        for path, digest, size in blobs:
            try:
                self._upload_text(path, digest, size)
            except Exception as exc:  # noqa: BLE001 -- one text never costs the rest
                failed.append(exc)
        _delete_files(blobs)
        return failed

    def _prepare(self, sample: Any, *, role: str, seal_step: int | None, blobs: list[PendingBlob]) -> PreparedPart:
        # A copy, NULs escaped, before anything else: refs handed out below must stay this dict's.
        part = replace_nul_text(to_plain(sample))
        part.setdefault("role", role)
        if seal_step is not None:
            part["seal_step"] = seal_step
        elif part.get("seal_step") is None:
            default = get_default_seal_step(part)
            if default is not None:
                part["seal_step"] = default
        prepared = PreparedPart(part=part, blobs=blobs)
        prepared.task = self._take_task(part, blobs)
        log_text = split_log(part)
        if log_text is not None:
            log_text, is_cut = cut_tail(log_text, MAX_LOG_BYTES)
            part["log_text"] = log_text  # scrubbed below with the tail and the turns
        scrub_part(part, self._scrub)
        cap_error_message(part)
        if log_text is not None:
            ref = self._bundles.append(
                BundleKind.LOGS, part.get("seal_step"), part.pop("log_text").encode("utf-8")
            )
            ref["is_cut"] = is_cut
            part["log"] = ref
            prepared.is_waiting_for_bundles = True
        if self._store_tokens(part):
            prepared.is_waiting_for_bundles = True
        self._store_long_text(part, "response", "response_blob", blobs)
        self._store_long_turns(part, blobs)
        return prepared

    def _take_task(self, part: dict, blobs: list[PendingBlob]) -> dict | None:
        """The task's own fields (prompt, label, dataset, full reward) come off the part; the first
        time this process meets a (task_key, scenario) they become one `tasks` item."""
        fields = {name: part.pop(name) for name in TASK_FIELDS if name in part}
        task_key = part.get("task_key")
        if not fields or not isinstance(task_key, str):
            return None
        scenario = part.get("scenario") or {}
        identity = (task_key, json.dumps(scenario, sort_keys=True, default=str))
        if identity in self._tasks_sent:
            return None
        self._tasks_sent.add(identity)
        task = {"task_key": task_key, "scenario": scenario, **fields}
        prompt = task.get("prompt")
        if isinstance(prompt, str) and len(prompt.encode("utf-8")) > MAX_INLINE_TEXT_BYTES:
            task["prompt_blob"] = self._save_spill(task.pop("prompt"), blobs)
        return task

    def _store_tokens(self, part: dict) -> bool:
        """Per-token arrays (``token_arrays`` / ``trainer_token_arrays``, or ``tokens`` given as
        arrays) into the step's tokens bundle; summaries computed whether or not they are kept."""
        has_bundled = False
        for wire_name, input_name in TOKEN_INPUTS.items():
            arrays = part.pop(input_name, None)
            given = part.get(wire_name)
            if arrays is None and isinstance(given, dict) and "sha256" not in given and "offset" not in given:
                arrays = part.pop(wire_name)
            if not isinstance(arrays, dict):
                continue
            picked = pick_token_arrays(arrays)
            stats = summarize_tokens(picked)
            if stats:
                part["token_stats"] = {**stats, **(part.get("token_stats") or {})}
            is_error = part.get("error_reason") is not None
            if picked and self._policy.should_keep(str(part.get("key")), is_error=is_error):
                payload = json.dumps(picked, separators=(",", ":"), default=float).encode("utf-8")
                part[wire_name] = self._bundles.append(BundleKind.TOKENS, part.get("seal_step"), payload)
                has_bundled = True
        return has_bundled

    def _store_long_text(self, part: dict, name: str, blob_name: str, blobs: list[PendingBlob]) -> None:
        value = part.get(name)
        if isinstance(value, str) and len(value.encode("utf-8")) > MAX_INLINE_TEXT_BYTES:
            part[blob_name] = self._save_spill(part.pop(name), blobs)

    def _store_long_turns(self, part: dict, blobs: list[PendingBlob]) -> None:
        turns = part.get("turns")
        if isinstance(turns, list) and turns and measure_bytes(turns) > MAX_INLINE_TEXT_BYTES:
            part.setdefault("turn_count", len(turns))
            part["turns_blob"] = self._save_spill(json.dumps(part.pop("turns"), default=str), blobs)

    def _save_spill(self, text: str, blobs: list[PendingBlob]) -> dict:
        """Text over 64 KiB, whole, to a temp file that `store_blobs` makes its own R2 object: the part keeps
        `{sha256, size_bytes}`."""
        raw = text.encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        handle, name = tempfile.mkstemp(prefix="probe-sample-text-", suffix=".txt")
        path = Path(name)
        try:
            with os.fdopen(handle, "wb") as out:
                out.write(raw)
        except BaseException:
            _delete_files([(path, digest, len(raw))])
            raise
        blobs.append((path, digest, len(raw)))
        return {"sha256": digest, "size_bytes": len(raw)}


def _delete_files(blobs: list[PendingBlob]) -> None:
    for path, _digest, _size in blobs:
        try:
            path.unlink()
        except OSError:
            pass
