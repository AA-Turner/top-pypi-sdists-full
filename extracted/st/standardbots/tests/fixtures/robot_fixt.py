from collections.abc import Generator

import pytest
from standardbots import StandardBotsRobot
from standardbots.auto_generated import models


@pytest.fixture()
def unbrake_robot_fixt(client_live: StandardBotsRobot) -> Generator[None, None, None]:
    """Fixture: Ensure robot is unbraked"""
    with client_live.connection():
        res = client_live.movement.brakes.get_brakes_state()
        if res.data.state == models.BrakesStateEnum.Engaged:
            client_live.movement.brakes.set_brakes_state(
                models.BrakesState(state=models.BrakesStateEnum.Disengaged)
            )

    yield


@pytest.fixture()
def brake_robot_fixt(client_live: StandardBotsRobot) -> Generator[None, None, None]:
    """Fixture: Ensure robot is braked"""
    with client_live.connection():
        res = client_live.movement.brakes.get_brakes_state()
        if res.data.state == models.BrakesStateEnum.Disengaged:
            client_live.movement.brakes.set_brakes_state(
                models.BrakesState(state=models.BrakesStateEnum.Engaged)
            )

    yield


@pytest.fixture()
def move_robot_to_home_fixt(
    client_live: StandardBotsRobot,
    unbrake_robot_fixt: None,
) -> Generator[None, None, None]:
    """Fixture: Move robot to home position"""
    with client_live.connection():
        target_position = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        target_position_body = models.ArmPositionUpdateRequest(
            kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
            joint_rotation=models.ArmJointRotations(joints=target_position),
        )
        res = client_live.movement.position.set_arm_position(body=target_position_body)
        assert not res.isNotOk()

    yield
