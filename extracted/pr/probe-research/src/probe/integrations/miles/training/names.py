"""Which of Miles' log-dict names each reduction of one `loss_function` call is: by Miles' own reduction order first
(two reductions with equal outputs and different rows, e.g. `pg_clipfrac` and `tis_clipfrac` both 0.5, keep their
names), else by exact value. Line refs are `radixark/miles@bb18e6ab7811`. Why: DESIGN.md "Per-sample training
metrics"."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

#: `loss` = pg_loss - entropy_coef x entropy_loss + kl_loss_coef x kl_loss (`losses.py:276-302`): rebuilt per row.
LOSS = "loss"
#: Not through the reducer: the per-sample ESS ratio (`math_utils.py:36-81`).
ESS = "ess_ratio"
#: Not through the reducer: Miles sums OPSM's masked token fraction itself.
OPSM_CLIPFRAC = "opsm_clipfrac"
ENTROPY = "entropy_loss"
#: Reduced last by `policy_loss_function`, after every other name.
OPD_REVERSE_KL = "opd_reverse_kl"
#: The order `policy_loss_function` reduces in (`losses.py:263-389`); the log dict lists them in another. The TIS and
#: mismatch metrics follow `ois` in their own dict order.
POLICY_REDUCTION_ORDER = ("pg_loss", "pg_clipfrac", "ppo_kl", ENTROPY, "kl_loss", "train_rollout_logprob_abs_diff",
                          "train_rollout_kl", "ois")  # fmt: skip
_NOT_REDUCED = frozenset({LOSS, ESS, OPSM_CLIPFRAC})


def match_by_order(outputs: list[float | None], named: Mapping[str, float | None], args: Any) -> dict[str, int] | None:
    """Each name at its place in Miles' reduction order, every output equal to its name's logged value (exact
    float32). None when the order does not hold (a version that reduces differently): `match_by_value` decides."""
    reduced = [name for name in named if name not in _NOT_REDUCED and name not in get_unreduced(args)]
    known = [name for name in POLICY_REDUCTION_ORDER if name in reduced]
    rest = [name for name in reduced if name not in POLICY_REDUCTION_ORDER and name != OPD_REVERSE_KL]
    expected = known + rest + ([OPD_REVERSE_KL] if OPD_REVERSE_KL in reduced else [])
    if len(expected) != len(outputs):
        return None
    if any(outputs[j] is None or outputs[j] != named[name] for j, name in enumerate(expected)):
        return None
    return {name: j for j, name in enumerate(expected)}


def match_by_value(outputs: list[float | None], named: Mapping[str, float | None], table: list[list[float]],
                   per_call: int, unreduced: set[str]) -> dict[str, int]:  # fmt: skip
    """Each log-dict name whose value one reduction returned exactly (the same float32 tensor, cloned). `loss`,
    `ess_ratio` and `opsm_clipfrac` are rebuilt, never matched (under Miles' defaults `loss` IS `pg_loss`); an
    ``unreduced`` name (a constant Miles never reduced) is skipped so it cannot take another key's exact 0. Two
    reductions with the same output and different rows leave the name out (never a guess); same rows, the first."""
    used: set[int] = set()
    found: dict[str, int] = {}
    for name, value in named.items():
        if name in _NOT_REDUCED or name in unreduced or value is None:
            continue
        matches = [j for j, output in enumerate(outputs) if j not in used and output == value]
        if not matches:
            continue
        if len({tuple(row[2 + per_call * j] for row in table) for j in matches}) > 1:
            continue
        used.add(matches[0])
        found[name] = matches[0]
    return found


def get_unreduced(args: Any) -> set[str]:
    """Log-dict names Miles fills with a constant, not a reduction: `entropy_loss` is `new_zeros(())` unless entropy
    is computed (`losses.py:117`: `entropy_coef != 0 or observe_training_entropy`)."""
    computes_entropy = getattr(args, "entropy_coef", 0) != 0 or bool(getattr(args, "observe_training_entropy", False))
    return set() if computes_entropy else {ENTROPY}
