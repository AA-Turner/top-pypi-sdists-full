"""One optimizer update on one Miles train rank, on the shared `UpdateLog` (`probe.sdk.run.samples.points`): what
Miles adds to it is its own normalization (sample or per-token mode, torch-native or Megatron scaling), context-parallel
fragments, and the update's step and ordinal, known only once the update ends. Pure Python: `loss.py` hands it floats.
Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples.points import Dtype, LossRole, UpdateLevel
from probe.sdk.run.samples.points import UpdateLog, UpdatePlace, get_lowest_dtype, keep_finite

from ..samples.mapping import join_train_key


@dataclass
class RankFacts:
    """This process's place in the update (data-, context- and tensor-parallel coordinates) and how Miles normalizes
    it."""

    dp: int
    dp_size: int
    cp: int
    cp_size: int
    #: The tensor-parallel rank: only tensor-parallel 0 records and declares (every tensor rank sees the same loss).
    tp: int
    is_per_token: bool
    is_megatron: bool
    #: Rollouts per optimizer step (`num_rollouts`, else the global batch size): sample mode's normalizer.
    rollouts: float | None
    #: The step's data-parallel token count `count_loss_tokens` (torch-native per-token: known before backward).
    step_tokens: float | None = None
    #: `trainer_model_id/` when the run trains several policies (Miles' own `namespace_metrics`).
    namespace: str = ""
    #: Updates per rollout the micro-batches imply (`stamp.py`), used when the backend does not pass it.
    steps_hint: int | None = None
    #: Miles' trainer role (`plan.get_role`): an actor declares `train/*`, a critic only its own `train/critic-*`.
    role: str | None = None

    def get_key(self, name: str) -> str:
        """The run's own series name for one of Miles' values (`log_train_step`: `train/<role->name>`, namespaced: a
        critic's `train/critic-<name>`, `metrics/log_utils.py:550`)."""
        role_tag = "" if self.role in (None, LossRole.ACTOR) else f"{self.role}-"
        return f"{self.namespace}train/{role_tag}{name}"

    def get_role_field(self) -> dict[str, LossRole]:
        """A critic's rows and records say so (`role`), so its update 0 never merges with the actor's (D4)."""
        return {"role": LossRole.CRITIC} if self.role == LossRole.CRITIC else {}

    def get_reduction(self) -> str:
        mode = "calculate_per_token_loss" if self.is_per_token else "sum_of_sample_mean"
        return f"{mode}/{'megatron' if self.is_megatron else 'torch_native'}"


@dataclass
class UpdateEnd:
    """What the backend knows once the update ran."""

    step: int
    update: int
    updates_in_step: int | None
    is_applied: bool | None
    optimizer_step: int | None
    #: Miles' own logged loss for the update (`aggregate_train_losses`' `loss`).
    reported_loss: float | None = None
    #: Update-level values under Miles' logged names without `train/` (`grad_norm`, `lr-pg_0`).
    metrics: Mapping[str, float | None] = field(default_factory=dict)
    skipped_reason: str | None = None
    #: Megatron per-token: `finalize_model_grads`' all-reduced token count (context parallel included).
    finalized_tokens: float | None = None


@dataclass
class OpenUpdate:
    """The update in progress: the shared log (its step and ordinal set at the end) and Miles' own facts."""

    facts: RankFacts
    log: UpdateLog
    #: Per row id: the rollout's `sample_indices` entry and the token digest (with the step, the trainer parts' key).
    identities: list[tuple[Any, str]] = field(default_factory=list)
    #: Miles' per-sample names any captured micro-batch sends (the whole update's denominators).
    names: set[str] = field(default_factory=set)
    #: The stamp of the newest micro-batch: a pass that goes back means the update was abandoned (a raise, a retry).
    source: int | None = None
    position: int = -1
    optimizer_steps_at_open: int = 0
    #: By call ordinal, each captured call's device-side summary, read on the host once the update ends.
    pending: list[tuple[int, Any]] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        """Every loss call captured (a call it could not capture makes the update unsendable, never smaller)."""
        log = self.log
        return log.broken_reason is None and bool(log.calls) and len(log.micro_batches) == log.calls

    def get_dtype(self) -> Dtype | None:
        return get_lowest_dtype(micro_batch.dtype for micro_batch in self.log.micro_batches.values())

    def finish(self, end: UpdateEnd) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """The ended update's rows (`log_metrics_many`) and records (`log_update` keyword arguments). Once."""
        self._set_end(end)
        return self._build_rows(end), self._build_records(end)

    def _build_rows(self, end: UpdateEnd) -> list[dict[str, Any]]:
        """Every row keyed as the trainer parts are, with its context-parallel fragment."""
        facts = self.facts
        rows = self.log.build_rows(optimizer_step=end.optimizer_step)
        for row in rows:
            row.update(fragment=facts.cp, fragments_expected=facts.cp_size, **facts.get_role_field())
        return rows

    def _build_records(self, end: UpdateEnd) -> list[dict[str, Any]]:
        """From context-parallel 0 of each data-parallel rank (the other fragments hold the same rows), the whole
        update from (0, 0): Miles' own `applied`, denominators and Megatron per-token normalizer."""
        facts = self.facts
        if facts.cp != 0:
            return []
        metrics = {facts.get_key(name): value for name, value in end.metrics.items()}
        records = self.log.build_records(grad_norm=None, metrics=metrics, optimizer_step=end.optimizer_step,
                                         reported_loss=end.reported_loss)  # fmt: skip
        if records and records[0]["level"] == UpdateLevel.UPDATE:
            whole = records[0]
            if end.is_applied is not None:
                whole["applied"] = end.is_applied
                if not end.is_applied and end.skipped_reason:
                    whole["skipped_reason"] = end.skipped_reason
            denominator = self.get_denominator(end)
            if denominator:
                whole["denominators"] = dict.fromkeys(sorted(facts.get_key(name) for name in self.names), denominator)
            if facts.is_per_token and facts.is_megatron and end.finalized_tokens:
                whole.update(normalizer=end.finalized_tokens, scale=float(facts.cp_size))
        for record in records:
            record.update(facts.get_role_field())
        return records

    def get_denominator(self, end: UpdateEnd) -> float | None:
        """What Miles divides a key's summed rows by in its logged series (`aggregate_train_losses`). Sample mode:
        Megatron's `num_rollouts`; torch-native's all-reduced sample count (`values[0]`), which is this rank's rows x
        data parallel (`get_data_iterator` gives every rank the same count). A fully masked sample counts as one.
        Per-token: the step's `count_loss_tokens` (a fully masked sample counts one token); Megatron's count from
        `finalize_model_grads`, over context parallel."""
        facts = self.facts
        if not facts.is_per_token:
            return facts.rollouts if facts.is_megatron else float(len(self.identities) * max(facts.dp_size, 1))
        if not facts.is_megatron:
            return facts.step_tokens
        return end.finalized_tokens / facts.cp_size if end.finalized_tokens else None

    def _set_end(self, end: UpdateEnd) -> None:
        """The step, ordinal and keys, known once the update ends; a micro-batch's loss as its rows rebuild it."""
        place = self.log.place
        place.step, place.update, place.updates_in_step = end.step, end.update, end.updates_in_step
        self.log.keys = [join_train_key(end.step, index, digest) for index, digest in self.identities]
        if self.facts.is_per_token and self.facts.is_megatron:  # gradients are divided by the all-reduced count
            for micro_batch in self.log.micro_batches.values():
                loss = micro_batch.reported_loss
                micro_batch.reported_loss = (keep_finite(loss / end.finalized_tokens)
                                             if loss is not None and end.finalized_tokens else None)  # fmt: skip


def open_update(facts: RankFacts, optimizer_steps: int) -> OpenUpdate:
    """A new update on this rank; its step and ordinal are set when it ends (`train_one_step` / `log_train_step`)."""
    place = UpdatePlace(step=0, update=0, rank=facts.dp, ranks=max(facts.dp_size, 1),
                        reduction=facts.get_reduction())  # fmt: skip
    return OpenUpdate(facts=facts, log=UpdateLog(place, []), optimizer_steps_at_open=optimizer_steps)
