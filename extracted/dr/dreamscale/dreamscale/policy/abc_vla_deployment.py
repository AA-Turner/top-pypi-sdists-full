"""Server-described ABC-VLA deployment wire: the robot, its action meaning and its RTC."""

from __future__ import annotations

from dreamscale_core.abc_vla_deploy import (
    TRAINED_RTC_CONTRACT,
    YAM_PRESET,
)
from dreamscale_core.abc_vla_deploy import (
    AbcVlaSessionDeployment as _Descriptor,
)

from dreamscale.policy.deployment import PresetLayout
from dreamscale.policy.pi05_deployment import PRESET_LAYOUTS


class AbcVlaSessionDeployment(_Descriptor):
    """ABC-VLA's session descriptor with the SDK's observation adapter."""

    @property
    def layout(self) -> PresetLayout | None:
        """That robot's joint layout, units and observe helper (the shared YAM wire)."""
        return PRESET_LAYOUTS[YAM_PRESET] if self.robot else None


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, AbcVlaSessionDeployment):
        deployment = AbcVlaSessionDeployment.from_json(deployment)
    hold = "current_position" if deployment.joints else "wait"
    trained = deployment.rtc_method == "trained"
    expected = {
        "backend": "pytorch",
        "rtc": "on" if trained else "off",
        "rtc_contract": TRAINED_RTC_CONTRACT if trained else None,
        "action_hz": deployment.action_hz,
        "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim,
        "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("ABC-VLA runtime differs from the deployment's sealed contract")
    layout = deployment.layout
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        joint_unit=deployment.joint_unit,
        normalized_gripper_indices=deployment.normalized_gripper_indices,
        **(
            {
                "joint_groups": layout.joint_groups,
                "gripper_indices": layout.gripper_indices,
                "startup_motion_delay_s": layout.startup_motion_delay_s,
            }
            if layout is not None
            else {}
        ),
    )
