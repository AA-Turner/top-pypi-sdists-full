"""Tests for **kwargs support in signal/query/update handlers."""

from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict

from mistralai.workflows import get_workflow_definition, workflow

from .utils import create_test_worker


class SignalInput(BaseModel):
    message: str


class StrictSignalInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str


class ReceivedEntries(BaseModel):
    entries: list[dict]


@workflow.define(name="test_signal_kwargs")
class SignalKwargsWorkflow:
    def __init__(self) -> None:
        self.received: list[dict] = []

    @workflow.entrypoint
    async def run(self) -> ReceivedEntries:
        await workflow.wait_condition(lambda: len(self.received) >= 2)
        return ReceivedEntries(entries=self.received)

    @workflow.signal(name="notify")
    async def notify(self, name: str, **kwargs: Any) -> None:
        self.received.append({"name": name, **kwargs})


@workflow.define(name="test_signal_only_kwargs")
class SignalOnlyKwargsWorkflow:
    def __init__(self) -> None:
        self.received: list[dict] = []

    @workflow.entrypoint
    async def run(self) -> ReceivedEntries:
        await workflow.wait_condition(lambda: len(self.received) >= 1)
        return ReceivedEntries(entries=self.received)

    @workflow.signal(name="notify")
    async def notify(self, **kwargs: Any) -> None:
        self.received.append(dict(kwargs))


@workflow.define(name="test_signal_basemodel_kwargs")
class SignalBaseModelKwargsWorkflow:
    def __init__(self) -> None:
        self.received: list[dict] = []

    @workflow.entrypoint
    async def run(self) -> ReceivedEntries:
        await workflow.wait_condition(lambda: len(self.received) >= 1)
        return ReceivedEntries(entries=self.received)

    @workflow.signal(name="notify")
    async def notify(self, data: SignalInput, **kwargs: Any) -> None:
        self.received.append({"message": data.message, **kwargs})


@workflow.define(name="test_signal_strict_basemodel_kwargs")
class SignalStrictBaseModelKwargsWorkflow:
    def __init__(self) -> None:
        self.received: list[dict] = []

    @workflow.entrypoint
    async def run(self) -> ReceivedEntries:
        await workflow.wait_condition(lambda: len(self.received) >= 1)
        return ReceivedEntries(entries=self.received)

    @workflow.signal(name="notify")
    async def notify(self, data: StrictSignalInput, **kwargs: Any) -> None:
        self.received.append({"message": data.message, **kwargs})


@workflow.define(name="test_query_kwargs")
class QueryKwargsWorkflow:
    def __init__(self) -> None:
        self.data = {"a": 1, "b": 2, "c": 3}

    @workflow.entrypoint
    async def run(self) -> dict:
        await workflow.wait_condition(lambda: False)
        return {}

    @workflow.query(name="get_data")
    def get_data(self, key: str, **kwargs: Any) -> dict:
        return {"key": key, "value": self.data.get(key), **kwargs}

    @workflow.query(name="get_all")
    def get_all(self, **kwargs: Any) -> dict:
        return {**self.data, **kwargs}


@workflow.define(name="test_update_kwargs")
class UpdateKwargsWorkflow:
    def __init__(self) -> None:
        self.store: dict = {}
        self.done = False

    @workflow.entrypoint
    async def run(self) -> dict:
        await workflow.wait_condition(lambda: self.done)
        return self.store

    @workflow.update(name="set_value")
    async def set_value(self, key: str, **kwargs: Any) -> dict:
        self.store[key] = kwargs
        return {"key": key, "stored": kwargs}

    @workflow.update(name="set_all")
    async def set_all(self, **kwargs: Any) -> dict:
        self.store.update(kwargs)
        return dict(kwargs)

    @workflow.signal(name="finish")
    async def finish(self) -> None:
        self.done = True


class TestSignalKwargs:
    @pytest.mark.asyncio
    async def test_signal_with_explicit_param_and_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SignalKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(SignalKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-signal-kwargs-explicit",
                task_queue="test-task-queue",
            )

            await handle.signal("notify", {"name": "alice", "priority": 10, "tag": "urgent"})
            await handle.signal("notify", {"name": "bob"})

            result = await handle.result()

            assert result["entries"][0] == {"name": "alice", "priority": 10, "tag": "urgent"}
            assert result["entries"][1] == {"name": "bob"}

    @pytest.mark.asyncio
    async def test_signal_with_only_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SignalOnlyKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(SignalOnlyKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-signal-only-kwargs",
                task_queue="test-task-queue",
            )

            await handle.signal("notify", {"x": 1, "y": "two", "z": True})

            result = await handle.result()

            assert result["entries"][0] == {"x": 1, "y": "two", "z": True}

    @pytest.mark.asyncio
    async def test_signal_with_basemodel_param_and_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[SignalBaseModelKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(SignalBaseModelKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-signal-basemodel-kwargs",
                task_queue="test-task-queue",
            )

            await handle.signal("notify", {"data": {"message": "hello"}, "source": "api"})

            result = await handle.result()

            assert result["entries"][0] == {"message": "hello", "source": "api"}

    @pytest.mark.asyncio
    async def test_signal_with_strict_basemodel_param_and_kwargs(self, temporal_env: Any) -> None:
        """Test that extra="forbid" on the BaseModel doesn't prevent kwargs from working.

        Extra fields should go to **kwargs, not into the BaseModel.
        """
        async with create_test_worker(temporal_env, workflows=[SignalStrictBaseModelKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(SignalStrictBaseModelKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-signal-strict-basemodel-kwargs",
                task_queue="test-task-queue",
            )

            await handle.signal("notify", {"data": {"message": "hello"}, "source": "api"})

            result = await handle.result()

            assert result["entries"][0] == {"message": "hello", "source": "api"}


class TestQueryKwargs:
    @pytest.mark.asyncio
    async def test_query_with_explicit_param_and_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[QueryKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(QueryKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-query-kwargs-explicit",
                task_queue="test-task-queue",
            )

            result = await handle.query("get_data", {"key": "a", "format": "json"})

            assert result == {"key": "a", "value": 1, "format": "json"}

    @pytest.mark.asyncio
    async def test_query_with_no_extra_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[QueryKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(QueryKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-query-kwargs-no-extra",
                task_queue="test-task-queue",
            )

            result = await handle.query("get_data", {"key": "b"})

            assert result == {"key": "b", "value": 2}

    @pytest.mark.asyncio
    async def test_query_with_only_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[QueryKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(QueryKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-query-only-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.query("get_all", {"extra_key": "extra_val"})

            assert result == {"a": 1, "b": 2, "c": 3, "extra_key": "extra_val"}


class TestUpdateKwargs:
    @pytest.mark.asyncio
    async def test_update_with_explicit_param_and_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[UpdateKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(UpdateKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-update-kwargs-explicit",
                task_queue="test-task-queue",
            )

            result = await handle.execute_update("set_value", {"key": "config", "timeout": 30, "retries": 3})

            assert result == {"key": "config", "stored": {"timeout": 30, "retries": 3}}

    @pytest.mark.asyncio
    async def test_update_with_only_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[UpdateKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(UpdateKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-update-only-kwargs",
                task_queue="test-task-queue",
            )

            result = await handle.execute_update("set_all", {"foo": "bar", "count": 42})

            assert result == {"foo": "bar", "count": 42}

    @pytest.mark.asyncio
    async def test_update_with_no_extra_kwargs(self, temporal_env: Any) -> None:
        async with create_test_worker(temporal_env, workflows=[UpdateKwargsWorkflow], activities=[]):
            workflow_def = get_workflow_definition(UpdateKwargsWorkflow)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {},
                id="test-update-kwargs-no-extra",
                task_queue="test-task-queue",
            )

            result = await handle.execute_update("set_value", {"key": "simple"})

            assert result == {"key": "simple", "stored": {}}
