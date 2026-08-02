"""Test the actuator functionalities."""
import asyncio

import pytest

from elmax_api.model.command import SwitchCommand
from elmax_api.model.panel import PanelStatus
from tests.conftest import async_init_test


@pytest.mark.asyncio
async def test_device_command():
    client = await async_init_test()
    # Retrieve its status
    panel = await client.get_current_panel_status()  # type: PanelStatus
    assert isinstance(panel, PanelStatus)

    # Store old status into a dictionary for later comparison
    expected_actuator_status = { actuator.endpoint_id:actuator.opened for actuator in panel.actuators}

    # Toggle the first 3 actuators actuators
    actuators = list(expected_actuator_status.items())[:min(len(expected_actuator_status.items()),3)]

    tasks = []
    for endpoint_id, curr_status in actuators:
        command = SwitchCommand.TURN_OFF if curr_status else SwitchCommand.TURN_ON
        print(f"Actuator {endpoint_id} was {curr_status}, issuing {command}...")
        tasks.append(client.execute_command(endpoint_id=endpoint_id, command=command))
        # Set actuator expected status
        expected_actuator_status[endpoint_id] = not curr_status
    await asyncio.gather(*tasks)

    # Ensure all the actuators switched correctly
    await asyncio.sleep(3)
    panel = await client.get_current_panel_status()  # type: PanelStatus

    for actuator in panel.actuators:
        expected_status = expected_actuator_status[actuator.endpoint_id]
        print(f"Actuator {actuator.endpoint_id} expected {expected_status}, was {actuator.opened}...")
        assert actuator.opened == expected_status
