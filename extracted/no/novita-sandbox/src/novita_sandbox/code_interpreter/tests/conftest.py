import pytest
import pytest_asyncio
import os

from logging import warning

from novita_sandbox.code_interpreter import AsyncSandbox
from novita_sandbox.code_interpreter.code_interpreter_sync import Sandbox

timeout = 60


@pytest.fixture()
def template():
    return os.getenv("NOVITA_TESTS_TEMPLATE") or "code-interpreter-v1"


@pytest.fixture()
def sandbox(template, debug):
    sandbox = Sandbox.create(template, timeout=timeout, debug=debug)

    try:
        yield sandbox
    finally:
        try:
            sandbox.kill()
        except:
            if not debug:
                warning(
                    "Failed to kill sandbox — this is expected if the test runs with local envd."
                )


@pytest_asyncio.fixture
async def async_sandbox(template, debug):
    async_sandbox = await AsyncSandbox.create(template, timeout=timeout, debug=debug)

    try:
        yield async_sandbox
    finally:
        try:
            await async_sandbox.kill()
        except:
            if not debug:
                warning(
                    "Failed to kill sandbox — this is expected if the test runs with local envd."
                )


@pytest.fixture
def debug():
    return os.getenv("NOVITA_DEBUG") is not None


@pytest.fixture(autouse=True)
def skip_by_debug(request, debug):
    if request.node.get_closest_marker("skip_debug"):
        if debug:
            pytest.skip("skipped because NOVITA_DEBUG is set")
