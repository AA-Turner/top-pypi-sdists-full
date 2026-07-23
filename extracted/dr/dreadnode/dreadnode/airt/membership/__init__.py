"""Membership-inference attacks against a black-box classifier predict API.

Given records known to be members (in the target's training set) and non-members,
these attacks decide membership from the target's outputs and report how well members
separate from non-members - the concrete training-data privacy leak.

Each algorithm lives in its own module for readability and easy extension; this
package re-exports the public factory functions, the shared result / family types,
and the pure metric helpers.

Methods:
- ``threshold_membership`` - confidence / entropy / loss thresholding (Yeom et al., CSF'18)
- ``entropy_membership`` / ``loss_membership`` - named entropy- and loss-threshold variants
- ``label_only_membership`` - robustness-to-perturbation membership using only the
  hard label (Choquette-Choo et al., arXiv 2007.14321); works when the endpoint
  returns no probabilities.
- ``shadow_model_membership`` - shadow model + in/out attack classifier (Shokri et al. 2017)
- ``lira_membership`` - offline likelihood-ratio via shadow models (Carlini et al. 2022)

The shadow-model methods train small local models (no extra target queries); the
rest are query-only. Every attack emits per-step traces of the intermediate
membership signal, so the scored records are visible in the Traces tab.
"""

from dreadnode.airt.membership._base import (
    MembershipInferenceAttack,
    MembershipMethod,
    MembershipResult,
    MembershipSignal,
    membership_advantage,
    membership_auc,
    membership_scores,
    roc_points,
    tpr_at_fpr,
)
from dreadnode.airt.membership.entropy import entropy_membership
from dreadnode.airt.membership.label_only import label_only_membership
from dreadnode.airt.membership.lira import lira_membership
from dreadnode.airt.membership.loss import loss_membership
from dreadnode.airt.membership.shadow_model import shadow_model_membership
from dreadnode.airt.membership.threshold import threshold_membership

__all__ = [
    "MembershipInferenceAttack",
    "MembershipMethod",
    "MembershipResult",
    "MembershipSignal",
    "entropy_membership",
    "label_only_membership",
    "lira_membership",
    "loss_membership",
    "membership_advantage",
    "membership_auc",
    "membership_scores",
    "roc_points",
    "shadow_model_membership",
    "threshold_membership",
    "tpr_at_fpr",
]
