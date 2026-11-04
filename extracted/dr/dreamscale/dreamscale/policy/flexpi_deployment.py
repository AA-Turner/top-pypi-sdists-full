"""Server-described Flex-π deployment wire: its robot preset, its actions and its RTC
(scaffolded by scripts/new_model.py). The block is checked against the robot its transport
module declares (dreamscale_transport.flexpi_deploy, read through its base's ``UNITS``) by the
shared preset session (dreamscale.policy.preset_deployment).

Flex-π anchors each chunk on the last command the robot executed (its training data's state is
the previous command, not the measured pose), so every request carries that command
(``action_history``): the unit builds the model's end-effector state from it.
"""

from __future__ import annotations

import dataclasses
from typing import Any

from dreamscale_transport import flexpi_deploy as C

from dreamscale.deploy_bases.flexpi import UNITS
from dreamscale.policy.preset_deployment import PresetSessionDeployment, preset_runtime_contract


class FlexpiSessionDeployment(PresetSessionDeployment):
    units = UNITS


def runtime_contract(resolved: Any, deployment: Any) -> Any:
    contract = preset_runtime_contract(FlexpiSessionDeployment, resolved, deployment)
    return dataclasses.replace(contract, action_history=C.ACTION_HISTORY)
