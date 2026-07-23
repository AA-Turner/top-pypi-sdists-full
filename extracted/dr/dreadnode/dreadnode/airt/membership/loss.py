"""Loss-threshold membership inference (Yeom et al. 2018).

A named variant of the confidence-threshold attack with the signal pinned to the
per-record loss (needs per-record labels): members have lower loss (higher
negative loss). Reuses the query-and-score loop in
:mod:`dreadnode.airt.membership.threshold`.
"""

import typing as t

from dreadnode.airt.membership._base import MembershipInferenceAttack, MembershipResult
from dreadnode.airt.membership.threshold import run as _threshold_run
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: MembershipInferenceAttack) -> MembershipResult:
    return await _threshold_run(attack)


def loss_membership(
    target: PredictionTargetSpec,
    members: t.Sequence[QueryInput],
    nonmembers: t.Sequence[QueryInput],
    **kwargs: t.Any,
) -> MembershipInferenceAttack:
    """Loss-threshold membership inference (Yeom et al. 2018). Thresholds the
    per-record loss (needs per-record labels) - members have lower loss."""
    return MembershipInferenceAttack(
        method="loss", target=target, members=members, nonmembers=nonmembers, **kwargs
    )
