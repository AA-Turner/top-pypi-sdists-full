"""Stock LeRobot checkpoints' policy releases: the served contract is the catalog's (the
n_action_steps LeRobot itself executes per plan), named by the model's public name."""

from __future__ import annotations

from dreamscale.model_names import public_model
from dreamscale.policy.runtime.contract import catalog_check


def check(model, resolved_config, **served):
    return catalog_check(model, public_model(model), resolved_config, **served)
