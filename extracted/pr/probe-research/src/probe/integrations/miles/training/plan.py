"""What the Miles adapter declares about its per-sample metrics (`plan(training=...)`): whether it sends loss
bookkeeping, how Miles builds its own `train/<key>` series from them (rows summed over every data- and context-parallel
rank, then divided by the update's denominator, `aggregate_train_losses`), and every path not proven, with why. A
critic declares its own `train/critic-*` (role critic) under its own producer, never a `*` stop (D4). Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from probe.foundation.compat.compat import StrEnum
from probe.generated.samples.points import Dtype, Grouping, LossRole, Reducer

from .names import OPSM_CLIPFRAC

#: [update: weighted mean with the update record's denominator, step: mean]. A Miles step (rollout) of one update
#: logs one point per update at `train/step` = rollout x updates + update (`log_utils.py:540`).
UPDATE_LEVELS = [{"by": Grouping.UPDATE, "reducer": Reducer.WEIGHTED_MEAN}, {"by": Grouping.STEP, "reducer": Reducer.MEAN}]


class Unsupported(StrEnum):
    """Miles' own names (its flags, its setting) for what the hook does not record: no rows are sent for them."""

    LOSS_TYPE = "loss_type"
    CUSTOM_REDUCER = "custom_pg_loss_reducer_function_path"
    PADDED_ROWS = "padded_rows"
    MULTI_LORA = "multi_lora"


#: Why each is not recorded.
UNSUPPORTED: dict[Unsupported, str] = {
    Unsupported.LOSS_TYPE: "a custom loss (custom_loss_function_path) or a loss type other than policy_loss, "
                           "value_loss, sft_loss and score_centering: Probe cannot know its maths",
    Unsupported.CUSTOM_REDUCER: "a custom pg_loss reducer is not Miles' sum_of_sample_mean: Probe cannot know its "
                                "maths",
    Unsupported.PADDED_ROWS: "PaddedRows (torchtitan on a platform without dynamic shapes: TPU only) reduces padded "
                             "logit rows with its own divisors; Probe's row map is CPU-tested but never run on such "
                             "hardware: no rows",
    Unsupported.MULTI_LORA: "multi-LoRA trains on Tinker client requests (batch loss_fn) through the Tinker gateway: "
                            "a datum is the client's, not a Miles rollout sample, so no sample key exists for a row, "
                            "and the loss carries the client's own normalization: no rows",
}  # fmt: skip
#: Why a context-parallel run sends no `opsm_clipfrac` rows (`loss.py`); its other keys still record.
OPSM_UNDER_CP = ("OPSM under context parallel: Miles builds the keep mask over each whole gathered sample on every "
                 "context-parallel rank (`math_utils.py:184-222`), which does not map onto a rank's token fragment; "
                 "unproven there, so not sent")  # fmt: skip


#: The key naming every key (`find_unsupported`'s pattern rule): a producer that stopped capturing for the whole run.
EVERY_KEY = "*"


class LossType(StrEnum):
    """Miles' loss types (`--loss-type`) the hook records (`loss/hub/losses.py:481`); any other, or a custom loss, is
    `Unsupported.LOSS_TYPE`. Score centering reduces through the policy path."""

    POLICY_LOSS = "policy_loss"
    VALUE_LOSS = "value_loss"
    SFT_LOSS = "sft_loss"
    SCORE_CENTERING = "score_centering"


def get_stop_key(namespace: str) -> str:
    """Where a stop is declared: `*` (every key: the run's only policy stopped), or on a multi-policy run that
    policy's own `<namespace>train/*`, so another policy's keys never read its reason."""
    return f"{namespace}train/*" if namespace else EVERY_KEY


def get_critic_key(namespace: str) -> str:
    """Where Miles logs a critic's series (`log_train_step`: `train/critic-<key>`, namespaced like the actor's)."""
    return f"{namespace}train/critic-*"


def get_role(args: Any) -> str | None:
    """Miles' trainer role for this process (`trainer_role`, which wins); without one, the critic by its `value_loss`;
    None when Miles names none (a single-policy actor)."""
    role = getattr(args, "trainer_role", None)
    if role:
        return str(role)
    # Miles' value model role (`megatron_config.py` `CRITIC_ROLE`) is the contract's `LossRole.CRITIC`.
    return LossRole.CRITIC if getattr(args, "loss_type", None) == LossType.VALUE_LOSS else None


def build_training_plan(*, namespace: str, dtype: Dtype | None, reasons: Iterable[Unsupported] = (),
                        role: str | None = None, updates_in_step: int | None = None,
                        is_context_parallel: bool = False) -> dict[str, Any]:  # fmt: skip
    """The declaration of one model's keys: the actor's `train/*`, a critic's `train/critic-*` only (role critic, so
    its plan never names or stops the actor's keys, D4). ``dtype``: the least precise precision Miles reduced a sent
    key in (None: nothing sent yet), so every key rolls up as Miles' series does, and every path the hook does not
    record is named. Until a row is sent, only the ``reasons`` this run hit are named, and the stop under
    `get_stop_key` ("<what>: <why>"; a critic's under its own keys), so any key of this model reads unsupported with
    its own reason (the server keeps the plan as JSONB: key order carries nothing). ``updates_in_step`` above 1
    (`num_steps_per_rollout`): Miles logs `train/*` once per update at `train/step` = rollout x updates + update, so
    the rollup is `logged_per: update`; each model's whole-update records count its own updates.
    ``is_context_parallel``: the actor's `opsm_clipfrac` is declared unsupported (`OPSM_UNDER_CP`)."""
    is_critic = role == LossRole.CRITIC
    keys = get_critic_key(namespace) if is_critic else f"{namespace}train/*"
    if dtype is None:
        hit = list(dict.fromkeys(reasons))
        unsupported = {str(reason): UNSUPPORTED[reason] for reason in hit}
        if hit:
            stop = keys if is_critic else get_stop_key(namespace)
            unsupported[stop] = "; ".join(f"{reason}: {UNSUPPORTED[reason]}" for reason in hit)
        return {"sends_loss_bookkeeping": False, "rollups": {}, "unsupported": unsupported}
    rollup: dict[str, Any] = {"levels": UPDATE_LEVELS, "dtype": dtype}
    if is_critic:
        rollup["role"] = LossRole.CRITIC
    if (updates_in_step or 1) > 1:
        rollup["logged_per"] = Grouping.UPDATE
    unsupported = {} if is_critic else {str(reason): why for reason, why in UNSUPPORTED.items()}
    if is_context_parallel and not is_critic:
        unsupported[f"{namespace}train/{OPSM_CLIPFRAC}"] = OPSM_UNDER_CP
    return {"sends_loss_bookkeeping": True, "rollups": {keys: rollup}, "unsupported": unsupported}


def get_unsupported_reason(args: Any, batch: Any, state: Any) -> Unsupported | None:
    """The path this micro-batch falls under that the hook does not record, or None when it records it."""
    if getattr(args, "loss_type", None) not in set(LossType) or getattr(args, "custom_loss_function_path", None):
        return Unsupported.LOSS_TYPE
    for reason in (Unsupported.CUSTOM_REDUCER, Unsupported.MULTI_LORA):
        if getattr(args, reason.value, None):
            return reason
    if batch.get("loss_fn") is not None:
        return Unsupported.MULTI_LORA
    if _is_padded_rows(args):
        return Unsupported.PADDED_ROWS
    return None  # tensor / pipeline parallel: tensor-parallel 0 of the last stage records (`training.open_call`)


def _is_padded_rows(args: Any) -> bool:
    try:
        from miles.backends.training_utils.loss.hub.response_layout import padded_rows_enabled

        return bool(padded_rows_enabled(args))
    except Exception:  # noqa: BLE001 -- a layout without the switch has no padded rows
        return False
