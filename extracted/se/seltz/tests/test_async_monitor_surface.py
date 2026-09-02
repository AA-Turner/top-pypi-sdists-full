"""Every AsyncMonitorService method is a real async body, not an inherited one.

AsyncMonitorService subclasses MonitorService, so a method it forgets to
override is silently inherited and returns an un-awaited call object. That
failure reaches a user as an AttributeError on a field of an awaitable, or as
an RPC that is never sent, rather than as anything that looks like a bug in the
SDK. Delegating to the synchronous body does not fix it either: the sync body
reads fields off the response and catches grpc.RpcError around the call, and on
the aio stub the field access happens before the RPC completes and the error
surfaces at the await, outside the except.
"""

import inspect

import pytest

from seltz.services.monitor_service import AsyncMonitorService, MonitorService

UNARY = (
    "create",
    "get",
    "list",
    "update",
    "delete",
    "list_runs",
    "get_run",
    "list_run_requests",
    "list_records",
    "list_run_records",
)
PUBLIC = UNARY + ("stream_records",)


@pytest.mark.parametrize("name", PUBLIC)
def test_the_async_service_defines_its_own_body(name: str) -> None:
    assert getattr(AsyncMonitorService, name) is not getattr(MonitorService, name)


@pytest.mark.parametrize("name", UNARY)
def test_every_unary_method_is_a_coroutine(name: str) -> None:
    assert inspect.iscoroutinefunction(getattr(AsyncMonitorService, name))


def test_stream_records_is_an_async_generator() -> None:
    assert inspect.isasyncgenfunction(AsyncMonitorService.stream_records)
    assert inspect.isgeneratorfunction(MonitorService.stream_records)


@pytest.mark.parametrize("name", PUBLIC)
def test_the_two_services_take_the_same_arguments(name: str) -> None:
    """A `*args, **kwargs` override would pass every check above and still drop
    keyword names from the public surface."""
    asynchronous = inspect.signature(getattr(AsyncMonitorService, name))
    synchronous = inspect.signature(getattr(MonitorService, name))
    assert list(asynchronous.parameters) == list(synchronous.parameters)
