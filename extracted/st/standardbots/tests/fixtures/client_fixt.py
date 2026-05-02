"""Fixtures: API Clients"""

import pytest
from standardbots import StandardBotsRobot
from standardbots.auto_generated.apis import RobotKind


@pytest.fixture(scope="session")
def client_live(api_url: str, api_token: str):
    """StandardBotsRobot API client - Live mode"""
    return StandardBotsRobot(
        url=api_url,
        token=api_token,
        robot_kind=RobotKind.Live,
    )


@pytest.fixture(scope="session")
def client_sim(api_url: str, api_token: str):
    """StandardBotsRobot API client - Simulated mode"""
    return StandardBotsRobot(
        url=api_url, token=api_token, robot_kind=RobotKind.Simulated
    )
