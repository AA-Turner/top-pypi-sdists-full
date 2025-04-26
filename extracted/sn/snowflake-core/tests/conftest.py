import pytest

import snowflake.core._internal.telemetry


pytest_plugins = [
    "tests.integ.deflake",
]


def pytest_configure(config):
    snowflake.core._internal.telemetry._called_from_test = True

def pytest_collection_modifyitems(items):
    for item in items:
        # Mark every test that uses session to need SnowPark
        if "session" in item.fixturenames:
            item.add_marker(pytest.mark.snowpark)
