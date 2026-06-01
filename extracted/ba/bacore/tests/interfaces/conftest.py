"""Conftest file for test cases for interfaces."""

import pytest
from bacore.interactors.network_handler import connected_to_gateway


@pytest.fixture(scope="session")
def fixt_internet_connection_established():
    """Assess if connected to the internet by inspecting if a gateway is found."""
    if connected_to_gateway():
        yield
    else:
        pytest.skip("No internet connection detected, skipping internet-dependent tests.")
