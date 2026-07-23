"""Modified-entropy membership inference (Song & Mittal 2021).

A named variant of the confidence-threshold attack with the signal pinned to
prediction entropy: members are predicted with lower entropy (higher negative
entropy). Reuses the query-and-score loop in
:mod:`dreadnode.airt.membership.threshold`.
"""

import typing as t

from dreadnode.airt.membership._base import MembershipInferenceAttack, MembershipResult
from dreadnode.airt.membership.threshold import run as _threshold_run
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: MembershipInferenceAttack) -> MembershipResult:
    return await _threshold_run(attack)


def entropy_membership(
    target: PredictionTargetSpec,
    members: t.Sequence[QueryInput],
    nonmembers: t.Sequence[QueryInput],
    **kwargs: t.Any,
) -> MembershipInferenceAttack:
    """Modified-entropy membership inference (Song & Mittal 2021). Thresholds the
    prediction entropy - members are predicted with lower entropy."""
    return MembershipInferenceAttack(
        method="entropy", target=target, members=members, nonmembers=nonmembers, **kwargs
    )
