"""Fixtures: Routines"""

from collections.abc import Generator

import pytest
from standardbots import StandardBotsRobot
from standardbots.auto_generated import models

SAMPLE_ROUTINE_NAME = "Test Public API"


@pytest.fixture(scope="session")
def routine_sample(client_live: StandardBotsRobot) -> models.Routine:
    """Fixture: Get a sample routine.

    Relies on `StandardBotsRobot#routine_editor#routines#list`
    """
    limit = 100
    offset = 0
    i = 0
    while i < 100:
        try:
            with client_live.connection():
                res = client_live.routine_editor.routines.list(
                    limit=limit, offset=offset
                )

            data = res.ok()
        except Exception as e:
            raise ValueError("Failed to fetch a sample routine.") from e

        if len(data.items) == 0:
            break

        routines = [r for r in data.items if r.name == SAMPLE_ROUTINE_NAME]
        if len(routines) != 0:
            return routines[0]

        offset += limit
        i += 1

    raise ValueError(
        f"Failed to find a routine named '{SAMPLE_ROUTINE_NAME}'. Please create a routine with this name in order to continue testing."
    )


@pytest.fixture(scope="session")
def routine_sample_id(routine_sample: models.Routine) -> str:
    """Fixture: ID of sample routine"""
    return routine_sample.id


@pytest.fixture()
def routine_running_live_fixt(
    unbrake_robot_fixt: None, routine_sample_id: str, client_live: StandardBotsRobot
) -> Generator[None, None, None]:
    """Fixture: Running routine while running the test. Plays a routine, yields then stops at end"""
    with client_live.connection():
        res = client_live.routine_editor.routines.play(
            routine_id=routine_sample_id, body=models.PlayRoutineRequest()
        )
        assert not res.isNotOk()
        assert res.status == 200
        assert res.data.status == models.RobotStatusEnum.RoutineRunning

    try:
        yield
    finally:
        with client_live.connection():
            res = client_live.routine_editor.routines.stop()
            assert not res.isNotOk()
