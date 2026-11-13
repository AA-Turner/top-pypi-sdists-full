"""Each trajectory's exact training loss, read in the client process (plan rl-trajectory-gaps T9): LocalBackend
yields one `loss/train` per packed row when ART's trainer args keep `gradient_accumulation_steps` and `logging_steps`
at 1, and each row is one history. Rows are paired to trajectories by content. ART's maths is never touched.
DESIGN.md "Per-trajectory loss". Line refs are `OpenPipe/ART@414acc5`."""

from __future__ import annotations

import contextvars
import functools
import math
import sys
from array import array
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import Grouping, Reducer

#: ART's own logged series of a row's policy loss (`unsloth/train.py:490`, averaged at `local/backend.py:809-814`).
ART_LOSS_KEY = "loss/train"
#: The per-sample key each trajectory's row loss is sent under.
LOSS_KEY = "loss"
#: The module whose packing LocalBackend looks up at call time (`local/backend.py:543`).
BACKEND_MODULE = "art.local.backend"
PACK_FUNCTION = "packed_tensors_from_tokenized_results"
#: The trainer args that must stay 1 for one yield to be one row's loss (`dev/get_model_config.py:66,69`).
ONE_ROW_ARGS = ("gradient_accumulation_steps", "logging_steps")
PER_SAMPLE_LOSS = "per_sample_loss"
#: The class whose own `_train_model` and `_get_service` the row-per-yield reading is verified against.
LOCAL_BACKEND = "LocalBackend"
REASON_NOT_LOCAL = ("ART trains this model outside this machine or through a backend other than LocalBackend; "
                    "per-trajectory loss never reaches the client")
REASON_NOT_UNSLOTH = ("this backend trains through a service other than ART's Unsloth one (TinkerBackend, or "
                      "tinker_args set), whose yielded loss/train is not verified to be one packed row's loss")
REASON_TRAINER_ARGS = (
    "ART's Unsloth trainer averages loss/train over gradient_accumulation_steps x logging_steps packed rows in its "
    "spawned model-service process before LocalBackend._train_model yields it, so a single trajectory's loss is not "
    "reachable unless both are 1 (this model's trainer_args set {args})"
)
REASON_PACKED = "this backend packs several trajectories into one row, so a row's loss is not one trajectory's"

#: The capture of the train call in progress in this task (`RowLosses`, set by `ArtTracker`'s `backend.train` wrap).
CURRENT: contextvars.ContextVar = contextvars.ContextVar("probe_art_row_losses", default=None)


def get_trainer_args(model: Any) -> dict[str, Any]:
    """The `ONE_ROW_ARGS` the model's service trains with: ART's defaults (1) updated by `_internal_config`'s
    `trainer_args` (`dev/get_model_config.py:77`)."""
    internal = getattr(model, "_internal_config", None)
    given = internal.get("trainer_args") if isinstance(internal, Mapping) else None
    given = given if isinstance(given, Mapping) else {}
    return {name: given.get(name, 1) for name in ONE_ROW_ARGS}


def get_unsupported_reason(model: Any, backend: Any) -> str | None:
    """Why this model's per-trajectory loss cannot be read through ``backend`` (None: it can). Only ART's own
    `LocalBackend._train_model` yields per packed row in this process: `ServerlessBackend` has its own that streams
    remote gradient steps (`serverless/backend.py:397`), and a subclass may override it. Read from the loaded module
    only: a LocalBackend instance means it is already imported."""
    local = getattr(sys.modules.get(BACKEND_MODULE), LOCAL_BACKEND, None)
    if backend is None or local is None or getattr(type(backend), "_train_model", None) is not local._train_model:
        return REASON_NOT_LOCAL
    if getattr(backend, "_supports_result_packing", False):
        return REASON_PACKED
    internal = getattr(model, "_internal_config", None)
    has_tinker = isinstance(internal, Mapping) and internal.get("tinker_args") is not None
    if has_tinker or getattr(type(backend), "_get_service", None) is not getattr(local, "_get_service", None):
        return REASON_NOT_UNSLOTH  # `local/backend.py:417-421`, `tinker/backend.py:44`
    args = get_trainer_args(model)
    if any(value != 1 for value in args.values()):
        shown = ", ".join(f"{name}={value}" for name, value in args.items())
        return REASON_TRAINER_ARGS.format(args=shown)
    return None


def make_training_plan(reason: str | None) -> dict[str, Any]:
    """`PlanIn.training`: the loss rollup (ART's `loss/train` is the plain mean of its rows, one row per optimizer
    update) when rows can be read, else why not."""
    if reason is not None:
        return {"sends_loss_bookkeeping": False, "unsupported": {PER_SAMPLE_LOSS: reason}}
    levels = [{"by": Grouping.UPDATE, "reducer": Reducer.WEIGHTED_MEAN},
              {"by": Grouping.STEP, "reducer": Reducer.MEAN}]  # fmt: skip
    rollup = {"run_key": ART_LOSS_KEY, "split": SampleSplit.TRAIN, "levels": levels}
    return {"sends_loss_bookkeeping": False, "rollups": {LOSS_KEY: rollup}, "unsupported": {}}


def wrap_packing(module: Any) -> bool:
    """Wrap ``module``'s packing function, once per process, so the train call in progress (`CURRENT`) sees what was
    packed. With no capture active it is ART's own call, untouched, so it stays for the process (several trackers)."""
    original = getattr(module, PACK_FUNCTION, None)
    if not callable(original) or getattr(original, "__probe_art_losses__", False):
        return callable(original)

    @functools.wraps(original)
    def pack(tokenized_results: Any, *args: Any, **kwargs: Any) -> Any:
        capture = CURRENT.get()
        if capture is None:
            return original(tokenized_results, *args, **kwargs)
        results = list(tokenized_results)  # what ART packs: too-long results already dropped
        packed = original(results, *args, **kwargs)
        capture.add_packing(results, packed)
        return packed

    pack.__probe_art_losses__ = True  # type: ignore[attr-defined]
    setattr(module, PACK_FUNCTION, pack)
    return True


@dataclass
class RowLosses:
    """One train call's packed rows and the per-row losses LocalBackend yielded for them, in row order. ``owner`` is
    the tracker whose train call this is: on a backend shared by two tracked models, each one's `_train_model` wrap
    runs on every call, and only the owner's counts the yields."""

    owner: Any = None
    results: list = field(default_factory=list)
    packed: Any = None
    losses: list[float | None] = field(default_factory=list)
    packings: int = 0
    has_loss: bool = False

    def add_packing(self, results: list, packed: Any) -> None:
        self.results, self.packed = results, packed
        self.packings += 1

    def add_yield(self, metrics: Mapping[str, Any]) -> None:
        value = metrics.get(ART_LOSS_KEY) if isinstance(metrics, Mapping) else None
        self.has_loss = self.has_loss or value is not None
        number = float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None
        self.losses.append(number if number is not None and math.isfinite(number) else None)

    @property
    def is_skipped(self) -> bool:
        """ART trained nothing: it never packed (no tokenized result), or `_get_packed_tensors` returned None (no
        logprobs) and `_train_model` yielded its one skip result with no loss (`local/backend.py:877-930`)."""
        return self.packings == 0 or (len(self.losses) == 1 and not self.has_loss)

    def build_rows(self, keys_by_trajectory: Any, *, step: int) -> list[dict[str, Any]]:
        """`log_metrics_many` rows: row r's loss on its trajectory's sample key, at update r. Raises `ValueError` when
        the yields do not pair 1:1 with the packed rows or a row matches no packed result (nothing is sent then)."""
        if self.packings != 1 or self.packed is None:
            raise ValueError(f"ART packed {self.packings} times in one train call; expected once")
        tokens = self.packed["tokens"]
        rows = int(tokens.shape[0])
        if len(self.losses) != rows:
            raise ValueError(f"LocalBackend yielded {len(self.losses)} results for {rows} packed rows")
        matched = match_rows(self.packed, self.results)
        out: list[dict[str, Any]] = []
        for update, (result, loss) in enumerate(zip(matched, self.losses, strict=True)):
            key = keys_by_trajectory(getattr(result, "trajectory", None))
            if key is None or loss is None:
                continue  # a trajectory with no sample key, or a non-finite loss: that row only is left out
            out.append({"sample_key": key, "metrics": {LOSS_KEY: loss}, "step": step, "update": update,
                        "split": SampleSplit.TRAIN.value})  # fmt: skip
        return out


def match_rows(packed: Mapping[str, Any], results: Sequence[Any]) -> list[Any]:
    """The tokenized result each packed row holds. With result packing off (`local/backend.py:180`, `:549`) a row is
    one result, shuffled and with a random group id (`pack.py:85`, `:114`), so a row is found by its content: prompt
    id, token ids, logprobs (as float32) and advantage sign, unless the packed advantages sum to 0 (`advantage_balance`
    1.0 packs a negative advantage as 0, `pack.py`); equal candidates go in order (identical inputs)."""
    by_content: dict[tuple, list[Any]] = {}
    for result in results:
        by_content.setdefault((int(result.prompt_id), tuple(result.token_ids)), []).append(result)
    matched: list[Any] = []
    for row in range(int(packed["tokens"].shape[0])):
        length = int((packed["parent_ids"][row] != -1).sum())
        content = (int(packed["parent_ids"][row, 0]), tuple(packed["tokens"][row, :length].tolist()))
        logprobs = packed["logprobs"][row, :length].tolist()
        total = float(packed["advantages"][row].sum())
        free = by_content.get(content, [])
        hit = next((result for result in free if _has_logprobs(result, logprobs)
                    and (total == 0 or math.copysign(1.0, float(result.advantage)) == math.copysign(1.0, total))),
                   None)  # fmt: skip
        if hit is None:
            raise ValueError(f"packed row {row} matches no tokenized result")
        free.remove(hit)
        matched.append(hit)
    return matched


def _has_logprobs(result: Any, logprobs: list[float]) -> bool:
    own = array("f", (float(value) for value in result.logprobs)).tolist()  # packed as float32
    return len(own) == len(logprobs) and all(
        a == b or (math.isnan(a) and math.isnan(b)) for a, b in zip(own, logprobs, strict=True))
