"""Every AsyncAgentService method is a real async body, not an inherited one.

Same guarantee as the monitor surface test: AsyncAgentService subclasses
AgentService, so a forgotten override is silently inherited and hands back an
un-awaited call object — and for the waiters, a sync body would block the
event loop with time.sleep.
"""

import inspect

import pytest

from seltz.services.agent_service import AgentService, AsyncAgentService

PUBLIC = ("create", "get", "list", "cancel", "wait", "create_and_wait")


@pytest.mark.parametrize("name", PUBLIC)
def test_the_async_service_defines_its_own_body(name: str) -> None:
    assert getattr(AsyncAgentService, name) is not getattr(AgentService, name)


@pytest.mark.parametrize("name", PUBLIC)
def test_every_method_is_a_coroutine(name: str) -> None:
    assert inspect.iscoroutinefunction(getattr(AsyncAgentService, name))


@pytest.mark.parametrize("name", PUBLIC)
def test_the_two_services_take_the_same_arguments(name: str) -> None:
    """A `*args, **kwargs` override would pass every check above and still drop
    keyword names from the public surface."""
    asynchronous = inspect.signature(getattr(AsyncAgentService, name))
    synchronous = inspect.signature(getattr(AgentService, name))
    assert list(asynchronous.parameters) == list(synchronous.parameters)
