from typing import Any

import pytest

from mistralai.workflows import Depends, activity, get_workflow_definition, workflow
from mistralai.workflows.core.execution.local_activity import run_activities_locally

from .utils import create_test_worker


class DatabaseService:
    def __init__(self, connection_string: str = "test-db"):
        self.connection_string = connection_string
        self.queries: list[str] = []

    async def query(self, sql: str) -> str:
        self.queries.append(sql)
        return f"DB[{self.connection_string}]: {sql}"


class LogService:
    def __init__(self):
        self.logs: list[str] = []
        self.call_count = 0

    def log(self, message: str) -> None:
        self.logs.append(message)
        self.call_count += 1


class CacheService:
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    def get(self, key: str) -> str | None:
        return self.store.get(key)

    def set(self, key: str, value: str) -> None:
        self.store[key] = value


def get_database() -> DatabaseService:
    return DatabaseService("injected-db-connection")


def get_logger() -> LogService:
    logger = LogService()
    logger.was_injected = True  # type: ignore[attr-defined]
    return logger


def get_cache_0() -> CacheService:
    return CacheService()


def get_cache_1() -> CacheService:
    return CacheService()


@activity()
async def process_with_db(
    text: str,
    db: DatabaseService = Depends(get_database),
) -> str:
    result = await db.query(f"SELECT * FROM messages WHERE text='{text}'")
    return result


@activity()
async def process_with_multiple_deps(
    text: str,
    db: DatabaseService = Depends(get_database),
    logger: LogService = Depends(get_logger),
) -> str:
    assert hasattr(logger, "was_injected"), "Logger was not properly injected"

    logger.log(f"Processing: {text}")
    result = await db.query(f"INSERT INTO messages VALUES ('{text}')")
    logger.log(f"Query executed: {result}")

    return f"{result} [logged {logger.call_count} times]"


@activity()
async def inner_activity_with_cache_0(
    key: str,
    cache: CacheService = Depends(get_cache_0),
) -> str:
    return f"cached0:{cache.get(key)}"


@activity()
async def inner_activity_with_cache_1(
    key: str,
    cache: CacheService = Depends(get_cache_1),
) -> str:
    return f"cached1:{cache.get(key)}"


@activity()
async def outer_activity_calling_inner(
    text: str,
    db: DatabaseService = Depends(get_database),
    cache: CacheService = Depends(get_cache_0),
) -> str:
    db_result = await db.query(f"SELECT '{text}'")
    cache.set(text, f"cached-{text}")
    inner_result_0 = await inner_activity_with_cache_0(text)
    inner_result_1 = await inner_activity_with_cache_1(text)
    return f"{db_result} | {inner_result_0} | {inner_result_1}"


@workflow.define(name="test-workflow-with-dependency-injection")
class WorkflowWithDependencyInjection:
    @workflow.entrypoint
    async def run(self, text: str) -> str:
        result = await process_with_db(text)
        return result


@workflow.define(name="test-workflow-with-multiple-deps")
class WorkflowWithMultipleDependencies:
    @workflow.entrypoint
    async def run(self, text: str) -> str:
        result = await process_with_multiple_deps(text)
        return result


@workflow.define(name="test-workflow-with-local-deps")
class WorkflowWithLocalDependencies:
    @workflow.entrypoint
    async def run(self, text: str) -> str:
        with run_activities_locally():
            result = await process_with_multiple_deps(text)
        return result


class TestDependencyInjection:
    @pytest.mark.asyncio
    async def test_activity_with_injected_dependency(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowWithDependencyInjection],
            activities=[process_with_db],
        ):
            workflow_def = get_workflow_definition(WorkflowWithDependencyInjection)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": "test message"},
                id="test-di-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert "DB[injected-db-connection]" in result["result"]
            assert "SELECT * FROM messages" in result["result"]
            assert "test message" in result["result"]

    @pytest.mark.asyncio
    async def test_activity_with_multiple_dependencies(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowWithMultipleDependencies],
            activities=[process_with_multiple_deps],
        ):
            workflow_def = get_workflow_definition(WorkflowWithMultipleDependencies)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": "multi-dep message"},
                id="test-multi-di-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert "DB[injected-db-connection]" in result["result"]
            assert "INSERT INTO messages" in result["result"]
            assert "[logged 2 times]" in result["result"]

    @pytest.mark.asyncio
    async def test_dependency_isolation_between_workflows(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowWithDependencyInjection],
            activities=[process_with_db],
        ):
            workflow_def = get_workflow_definition(WorkflowWithDependencyInjection)
            assert workflow_def is not None

            handle1 = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": "first"},
                id="test-di-isolation-1",
                task_queue="test-task-queue",
            )
            result1 = await handle1.result()

            handle2 = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": "second"},
                id="test-di-isolation-2",
                task_queue="test-task-queue",
            )
            result2 = await handle2.result()

            assert "first" in result1["result"]
            assert "second" in result2["result"]

    @pytest.mark.asyncio
    async def test_dependencies_not_in_input_schema(self, temporal_env: Any) -> None:
        workflow_def = get_workflow_definition(WorkflowWithDependencyInjection)

        assert workflow_def.input_schema is not None
        properties = workflow_def.input_schema.get("properties", {})

        assert "params" in properties or "text" in properties
        assert "db" not in properties
        assert "logger" not in properties

    @pytest.mark.asyncio
    async def test_dependency_injection_works_with_local_activities(self, temporal_env: Any) -> None:
        async with create_test_worker(
            temporal_env,
            workflows=[WorkflowWithLocalDependencies],
            activities=[process_with_multiple_deps],
        ):
            workflow_def = get_workflow_definition(WorkflowWithLocalDependencies)
            assert workflow_def is not None

            handle = await temporal_env.client.start_workflow(
                workflow_def.name,
                {"text": "local activity test"},
                id="test-local-di-workflow",
                task_queue="test-task-queue",
            )

            result = await handle.result()

            assert isinstance(result, dict)
            assert "DB[injected-db-connection]" in result["result"]
            assert "INSERT INTO messages" in result["result"]
            assert "[logged 2 times]" in result["result"]

    @pytest.mark.asyncio
    async def test_nested_local_activity_calls_with_different_deps(self) -> None:
        """Outer activity shares get_cache_0 with inner_activity_with_cache_0.

        The inner call must reuse the same instance (seeing the value set by outer),
        while inner_activity_with_cache_1 uses a different factory and gets its own instance.
        """
        result = await outer_activity_calling_inner("hello")
        assert result == "DB[injected-db-connection]: SELECT 'hello' | cached0:cached-hello | cached1:None"
