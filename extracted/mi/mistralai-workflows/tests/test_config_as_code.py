import asyncio
import gc
import importlib
import json
import os
from collections.abc import AsyncIterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import AsyncExitStack, ExitStack, asynccontextmanager
from pathlib import Path
from threading import Event, Lock
from unittest.mock import patch

import pytest
from pydantic import BaseModel
from temporalio import workflow as temporal_workflow
from temporalio.common import VersioningBehavior, WorkerDeploymentVersion
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Replayer, Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows import (
    CommonConfig,
    GraphConfig,
    HttpConfig,
    TemporalConfig,
    WorkerConfig,
    WorkflowsConfig,
    activity,
    get_workflow_definition,
    prepare_workflows,
    workflow,
)
from mistralai.workflows.core.config.config import (
    config as legacy_config,
)
from mistralai.workflows.core.config.config import (
    resolve_worker_config,
    use_config,
)
from mistralai.workflows.core.config.config_discovery import WorkerRuntimeConfig
from mistralai.workflows.core.definition._workflow_preparation import (
    _use_workflow_config_for_worker,
    configure_workflow_for_worker,
)
from mistralai.workflows.core.definition.workflow_definition import (
    get_mounted_workflow,
    get_workflow_search_key_info,
    is_workflow_on_behalf_of,
    replace_workflow_definition,
)
from mistralai.workflows.core.execution.concurrency import ParallelExecutionWorkflow
from mistralai.workflows.core.sandbox import get_sandbox_restrictions
from mistralai.workflows.core.worker import _create_temporal_workers
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.models import WorkflowSpec
from mistralai.workflows.protocol.v1.worker import WorkerFeatures
from mistralai.workflows.testing import create_test_worker
from tests.fixtures import ChildWorkflow, ParentWorkflow
from tests.subprocess_helpers import run_python

_TEMPORAL_DEFINITION_CONFIG_ATTR = "__workflows_temporal_definition_config"


@asynccontextmanager
async def _hold_preparation(
    workflows: list[type],
    config: WorkflowsConfig,
    *,
    replay_only: bool = False,
) -> AsyncIterator[list[type]]:
    prepared_future: asyncio.Future[list[type]] = asyncio.get_running_loop().create_future()
    release = asyncio.Event()

    async def hold() -> None:
        try:
            with prepare_workflows(workflows, config=config, replay_only=replay_only) as prepared:
                prepared_future.set_result(prepared)
                await release.wait()
        except BaseException as exc:
            if not prepared_future.done():
                prepared_future.set_exception(exc)
            raise

    task = asyncio.create_task(hold())
    prepared = await prepared_future
    try:
        yield prepared
    finally:
        release.set()
        await task


@workflow.define(name="direct-temporal")
class DirectTemporalWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "done"


@temporal_workflow.defn(sandboxed=False)
class RawTemporalWorkflow:
    @temporal_workflow.run
    async def run(self) -> float:
        return legacy_config.common.otel_sample_rate


class RuntimeConfigValues(BaseModel):
    task_queue: str
    maximum_attempts: int
    backoff_coefficient: float


def _runtime_config_values() -> RuntimeConfigValues:
    return RuntimeConfigValues(
        task_queue=legacy_config.get_effective_task_queue(),
        maximum_attempts=legacy_config.worker.retry_policy_max_attempts,
        backoff_coefficient=legacy_config.worker.retry_policy_backoff_coefficient,
    )


@activity()
async def inspect_runtime_config_activity() -> RuntimeConfigValues:
    return _runtime_config_values()


@workflow.define(name="runtime-config-visibility")
class RuntimeConfigVisibilityWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, RuntimeConfigValues]:
        return {
            "workflow": _runtime_config_values(),
            "activity": await inspect_runtime_config_activity(),
        }


@workflow.define(name="runtime-config-handlers")
class RuntimeConfigHandlersWorkflow:
    def __init__(self) -> None:
        self.values: dict[str, RuntimeConfigValues] = {}

    @workflow.entrypoint
    async def run(self) -> dict[str, RuntimeConfigValues]:
        self.values["workflow"] = _runtime_config_values()
        self.values["activity"] = await inspect_runtime_config_activity()
        await workflow.wait_condition(lambda: "signal" in self.values and "update" in self.values)
        return self.values

    @workflow.signal(name="inspect-config-signal")
    async def inspect_signal_config(self) -> None:
        self.values["signal"] = _runtime_config_values()

    @workflow.query(name="inspect-config-query")
    def inspect_query_config(self) -> RuntimeConfigValues:
        return _runtime_config_values()

    @workflow.update(name="inspect-config-update")
    async def inspect_update_config(self) -> RuntimeConfigValues:
        values = _runtime_config_values()
        self.values["update"] = values
        return values


@workflow.define(name="reusable-test-worker")
class ReusableTestWorkerWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "done"


def _clear_temporal_definition(workflow_type: type) -> None:
    # Test-only process isolation: production code must use workflow.defn() and must never
    # read, replace, or delete Temporal's private class definition.
    temporal_definition = getattr(workflow_type, "__temporal_workflow_definition", None)
    if temporal_definition is not None:
        delattr(workflow_type, "__temporal_workflow_definition")
        delattr(temporal_definition.run_fn, "__temporal_workflow_definition")
    if hasattr(workflow_type, _TEMPORAL_DEFINITION_CONFIG_ATTR):
        delattr(workflow_type, _TEMPORAL_DEFINITION_CONFIG_ATTR)


class TestImportConfiguration:
    @pytest.mark.parametrize("source", ["environment", "dotenv"])
    @pytest.mark.parametrize(
        ("name", "value", "error_location"),
        [
            ("BLOB_STORAGE_CONFIGS", "not-json", ("blob_storage_configs",)),
            ("VERSIONING__ENABLED", "invalid", ("versioning", "enabled")),
            ("DEFAULT_ENFORCE_DETERMINISM", "invalid", ("default_enforce_determinism",)),
            ("WORKER_AUTO_REGISTER_AS_CURRENT", "invalid", ("WORKER_AUTO_REGISTER_AS_CURRENT",)),
        ],
    )
    def test_import_and_decoration_defer_validation(
        self, tmp_path: Path, source: str, name: str, value: str, error_location: tuple[str, ...]
    ) -> None:
        env = {key: item for key, item in os.environ.items() if key not in {name, "PYTEST_VERSION"}}
        if source == "environment":
            env[name] = value
        else:
            (tmp_path / ".env").write_text(f"{name}={value}\n")

        script = """
import json
import sys

from pydantic import ValidationError
from pydantic_settings.exceptions import SettingsError

from mistralai import workflows

expected_location = tuple(json.loads(sys.argv[1]))
expected_source = sys.argv[2]

@workflows.workflow.define(name="import-safe")
class ImportSafeWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> str:
        return "done"

assert workflows.get_workflow_definition(ImportSafeWorkflow).name == "import-safe"
assert workflows.get_workflow_definition(ImportSafeWorkflow).enforce_determinism is True

try:
    with workflows.prepare_workflows([ImportSafeWorkflow]):
        raise AssertionError("Invalid settings were not validated")
except SettingsError as exc:
    assert len(expected_location) == 1
    assert f'field "{expected_location[0]}"' in str(exc)
    assert f'source "{expected_source}"' in str(exc)
except ValidationError as exc:
    locations = [error["loc"] for error in exc.errors(include_input=False, include_context=False)]
    assert expected_location in locations, locations
"""
        result = run_python(
            script,
            json.dumps(error_location),
            "EnvSettingsSource" if source == "environment" else "DotEnvSettingsSource",
            cwd=tmp_path,
            env=env,
        )

        assert result.returncode == 0, result.stderr

    def test_unrelated_invalid_worker_setting_does_not_break_import(self, tmp_path: Path) -> None:
        env = {**os.environ, "MAX_CONCURRENT_ACTIVITIES": "invalid"}
        script = """
from mistralai import workflows

@workflows.workflow.define(name="import-safe")
class ImportSafeWorkflow:
    @workflows.workflow.entrypoint
    async def run(self) -> str:
        return "done"
"""
        result = run_python(script, cwd=tmp_path, env=env)

        assert result.returncode == 0, result.stderr

    def test_decorator_environment_is_resolved_at_preparation(self, tmp_path: Path) -> None:
        env = {
            **os.environ,
            "WORKFLOW_NAME_PREFIX": "first_",
            "DEFAULT_ENFORCE_DETERMINISM": "false",
        }
        script = """
import os

from mistralai.workflows import get_workflow_definition, prepare_workflows, workflow

@workflow.define(name="one")
class FirstWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "done"

os.environ["WORKFLOW_NAME_PREFIX"] = "second_"
os.environ["DEPLOYMENT_NAME"] = "test-deployment"
os.environ["BUILD_ID"] = "test-build"

@workflow.define(name="two")
class SecondWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "done"

assert get_workflow_definition(FirstWorkflow).name == "one"
assert get_workflow_definition(SecondWorkflow).name == "two"
assert get_workflow_definition(FirstWorkflow).enforce_determinism is True
assert get_workflow_definition(SecondWorkflow).enforce_determinism is True

with prepare_workflows([FirstWorkflow, SecondWorkflow]):
    for cls, name in [(FirstWorkflow, "second_one"), (SecondWorkflow, "second_two")]:
        definition = get_workflow_definition(cls)
        assert definition.name == name
        assert definition.enforce_determinism is False
"""
        result = run_python(script, cwd=tmp_path, env=env)

        assert result.returncode == 0, result.stderr


def test_explicit_values_override_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SERVER_URL", "https://environment.example")
    monkeypatch.setenv("DEPLOYMENT_NAME", "environment-deployment")

    config = WorkflowsConfig(
        worker={
            "server_url": "https://code.example",
            "deployment_name": "code-deployment",
        }
    )

    assert config.worker.server_url == "https://code.example"
    assert config.worker.deployment_name == "code-deployment"


def test_explicit_config_accepts_public_nested_models() -> None:
    graph = GraphConfig(upload_graph=False)
    worker = WorkerConfig(server_url="https://code.example", graph=graph)
    common = CommonConfig(app_name="configured-in-code")
    temporal = TemporalConfig(namespace="configured-in-code")
    http = HttpConfig(timeout=30.0)

    config = WorkflowsConfig(common=common, worker=worker, temporal=temporal, http=http)

    assert config.common == common
    assert config.worker == worker
    assert config.temporal == temporal
    assert config.http == http
    assert config.worker.graph == graph
    assert config.worker.retry_policy_max_attempts == 3
    assert config.worker.graph.graph_summarise_enabled is True


def test_explicit_values_override_remote_defaults() -> None:
    config = WorkflowsConfig(worker={"graph": {"upload_graph": False}})
    runtime_config = WorkerRuntimeConfig(
        scheduler_url="https://temporal.example:7233",
        namespace="workspace",
        features=WorkerFeatures(upload_graph=True),
    )

    runtime_config.apply(config)

    assert config.worker.graph.upload_graph is False


def test_remote_defaults_apply_to_public_nested_models() -> None:
    config = WorkflowsConfig(worker=WorkerConfig(graph=GraphConfig()))
    runtime_config = WorkerRuntimeConfig(
        scheduler_url="https://temporal.example:7233",
        namespace="workspace",
        features=WorkerFeatures(upload_graph=True),
    )

    runtime_config.apply(config)

    assert config.worker.graph.upload_graph is True


def test_worker_config_re_resolves_decorator_settings() -> None:
    @workflow.define(name="invoice")
    class InvoiceWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    config = WorkflowsConfig(
        worker={
            "workflow_name_prefix": "code_",
            "default_enforce_determinism": False,
            "versioning": {"deployment_name": "deployment", "BUILD_ID": "build"},
        }
    )

    assert not hasattr(InvoiceWorkflow, "__temporal_workflow_definition")
    with ExitStack() as mounts:
        configure_workflow_for_worker(InvoiceWorkflow, config, mounts)

    workflow_definition = get_workflow_definition(InvoiceWorkflow)
    temporal_definition = InvoiceWorkflow.__temporal_workflow_definition
    assert workflow_definition.name == "code_invoice"
    assert workflow_definition.enforce_determinism is False
    assert temporal_definition.name == "code_invoice"
    assert temporal_definition.sandboxed is False
    assert temporal_definition.versioning_behavior == VersioningBehavior.PINNED

    with ExitStack() as mounts:
        configure_workflow_for_worker(InvoiceWorkflow, config, mounts)
    assert InvoiceWorkflow.__temporal_workflow_definition is temporal_definition


@pytest.mark.asyncio
async def test_prepare_workflows_supports_direct_temporal_worker_and_replayer(
    temporal_env: WorkflowEnvironment,
) -> None:
    assert not hasattr(DirectTemporalWorkflow, "__temporal_workflow_definition")
    task_queue = "test-direct-temporal"
    workflow_runner = SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions())

    with prepare_workflows(
        [DirectTemporalWorkflow],
        config=WorkflowsConfig(
            worker={
                "deployment_name": task_queue,
                "workflow_name_prefix": "prepared-",
            }
        ),
    ) as prepared:
        async with Worker(
            temporal_env.client,
            task_queue=task_queue,
            workflows=prepared,
            workflow_runner=workflow_runner,
        ):
            handle = await temporal_env.client.start_workflow(
                "prepared-direct-temporal",
                id="test-direct-temporal",
                task_queue=task_queue,
            )
            assert await handle.result() == {"result": "done"}
            history = await handle.fetch_history()

        await Replayer(workflows=prepared, workflow_runner=workflow_runner).replay_workflow(history)


@pytest.mark.asyncio
async def test_raw_temporal_workflow_uses_legacy_config_without_prepare(
    temporal_env: WorkflowEnvironment,
) -> None:
    task_queue = "test-raw-temporal"

    async with Worker(
        temporal_env.client,
        task_queue=task_queue,
        workflows=[RawTemporalWorkflow],
    ):
        result = await temporal_env.client.execute_workflow(
            RawTemporalWorkflow.run,
            id="test-raw-temporal",
            task_queue=task_queue,
        )

    assert result == legacy_config.common.otel_sample_rate


@pytest.mark.asyncio
async def test_explicit_config_is_visible_in_sandboxed_workflow_and_replay(
    temporal_env: WorkflowEnvironment,
) -> None:
    task_queue = "test-runtime-config-visibility"
    workflow_runner = SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions())
    config = WorkflowsConfig(
        worker={
            "deployment_name": task_queue,
            "retry_policy_max_attempts": 7,
            "retry_policy_backoff_coefficient": 1.5,
        }
    )

    with prepare_workflows([RuntimeConfigVisibilityWorkflow], config=config) as prepared:
        async with Worker(
            temporal_env.client,
            task_queue=task_queue,
            workflows=prepared,
            activities=[inspect_runtime_config_activity],
            workflow_runner=workflow_runner,
        ):
            handle = await temporal_env.client.start_workflow(
                "runtime-config-visibility",
                id="test-runtime-config-visibility",
                task_queue=task_queue,
            )
            result = await asyncio.wait_for(handle.result(), timeout=5)
            history = await handle.fetch_history()

        expected = {
            "task_queue": task_queue,
            "maximum_attempts": 7,
            "backoff_coefficient": 1.5,
        }
        assert result["result"] == {"workflow": expected, "activity": expected}
        scheduled_activity = next(
            event.activity_task_scheduled_event_attributes
            for event in history.events
            if event.HasField("activity_task_scheduled_event_attributes")
        )
        assert scheduled_activity.task_queue.name == task_queue
        assert scheduled_activity.retry_policy.maximum_attempts == 7
        assert scheduled_activity.retry_policy.backoff_coefficient == 1.5
        await Replayer(workflows=prepared, workflow_runner=workflow_runner).replay_workflow(history)


def test_nested_preparations_reject_different_config() -> None:
    queue_a = "nested-config-a"
    queue_b = "nested-config-b"
    config_a = WorkflowsConfig(common={"app_name": "queue-a"}, worker={"deployment_name": queue_a})
    config_b = WorkflowsConfig(common={"app_name": "queue-b"}, worker={"deployment_name": queue_b})

    with prepare_workflows([RuntimeConfigVisibilityWorkflow], config=config_a):
        with pytest.raises(WorkflowsException, match="cannot be nested with a different configuration"):
            with prepare_workflows([RuntimeConfigVisibilityWorkflow], config=config_b):
                pass


@pytest.mark.asyncio
async def test_parallel_preparations_route_activity_config_by_task_queue(
    temporal_env: WorkflowEnvironment,
) -> None:
    async def execute_with_config(queue: str, app_name: str) -> dict:
        config = WorkflowsConfig(common={"app_name": app_name}, worker={"deployment_name": queue})
        with prepare_workflows([RuntimeConfigVisibilityWorkflow], config=config) as prepared:
            async with Worker(
                temporal_env.client,
                task_queue=queue,
                workflows=prepared,
                activities=[inspect_runtime_config_activity],
                workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
            ):
                return await temporal_env.client.execute_workflow(
                    "runtime-config-visibility",
                    id=queue,
                    task_queue=queue,
                )

    # See test_same_workflow_type_supports_different_task_queues: time skipping can expire
    # one workflow before its worker starts polling.
    with temporal_env.auto_time_skipping_disabled():
        result_a, result_b = await asyncio.gather(
            execute_with_config("parallel-config-a", "queue-a"),
            execute_with_config("parallel-config-b", "queue-b"),
        )

    assert result_a["result"]["activity"]["task_queue"] == "parallel-config-a"
    assert result_b["result"]["activity"]["task_queue"] == "parallel-config-b"


@pytest.mark.asyncio
async def test_explicit_config_is_visible_in_every_workflow_handler(
    temporal_env: WorkflowEnvironment,
) -> None:
    task_queue = "test-runtime-config-handlers"
    expected = {
        "task_queue": task_queue,
        "maximum_attempts": 7,
        "backoff_coefficient": 1.5,
    }
    config = WorkflowsConfig(
        worker={
            "deployment_name": task_queue,
            "retry_policy_max_attempts": 7,
            "retry_policy_backoff_coefficient": 1.5,
        }
    )

    with prepare_workflows([RuntimeConfigHandlersWorkflow], config=config) as prepared:
        async with Worker(
            temporal_env.client,
            task_queue=task_queue,
            workflows=prepared,
            activities=[inspect_runtime_config_activity],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            handle = await temporal_env.client.start_workflow(
                "runtime-config-handlers",
                id="test-runtime-config-handlers",
                task_queue=task_queue,
            )
            assert await handle.query("inspect-config-query") == expected
            await handle.signal("inspect-config-signal")
            assert await handle.execute_update("inspect-config-update") == expected
            result = await asyncio.wait_for(handle.result(), timeout=5)

    assert result["result"] == {
        "workflow": expected,
        "activity": expected,
        "signal": expected,
        "update": expected,
    }


@pytest.mark.asyncio
async def test_same_workflow_type_supports_different_task_queues(
    temporal_env: WorkflowEnvironment,
) -> None:
    @workflow.define(name="multi-queue-runtime-config", enforce_determinism=False)
    class MultiQueueRuntimeConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> dict[str, object]:
            return _runtime_config_values().model_dump()

    first_config = WorkflowsConfig(
        worker={
            "deployment_name": "queue-a",
            "retry_policy_max_attempts": 3,
        }
    )
    second_config = WorkflowsConfig(
        common={"app_name": "queue-b"},
        worker={
            "deployment_name": "queue-b",
            "retry_policy_max_attempts": 7,
        },
    )

    async def execute(config: WorkflowsConfig, queue: str, workflow_id: str) -> dict:
        with prepare_workflows([MultiQueueRuntimeConfigWorkflow], config=config) as prepared:
            async with Worker(temporal_env.client, task_queue=queue, workflows=prepared):
                return await temporal_env.client.execute_workflow(
                    "multi-queue-runtime-config",
                    id=workflow_id,
                    task_queue=queue,
                )

    # Each task waits on its own result while the other worker may still be starting.
    # Auto time skipping could otherwise jump past the execution timeout of the
    # workflow whose worker has not started polling yet.
    with temporal_env.auto_time_skipping_disabled():
        first_result, second_result = await asyncio.gather(
            execute(first_config, "queue-a", "multi-queue-runtime-config-a"),
            execute(second_config, "queue-b", "multi-queue-runtime-config-b"),
        )

    assert first_result == {
        "result": {
            "task_queue": "queue-a",
            "maximum_attempts": 3,
            "backoff_coefficient": 2.0,
        }
    }
    assert second_result == {
        "result": {
            "task_queue": "queue-b",
            "maximum_attempts": 7,
            "backoff_coefficient": 2.0,
        }
    }


@pytest.mark.asyncio
async def test_different_workflow_types_support_different_configs_on_the_same_task_queue() -> None:
    @workflow.define(name="same-queue-first-config")
    class FirstConfiguredWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "first"

    @workflow.define(name="same-queue-second-config")
    class SecondConfiguredWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "second"

    task_queue = "different-workflows-same-queue"
    first_config = WorkflowsConfig(common={"app_name": "first"}, worker={"deployment_name": task_queue})
    second_config = WorkflowsConfig(common={"app_name": "second"}, worker={"deployment_name": task_queue})

    async with (
        _hold_preparation([FirstConfiguredWorkflow], first_config),
        _hold_preparation([SecondConfiguredWorkflow], second_config),
    ):
        pass


def test_different_workflow_classes_cannot_reuse_a_reserved_workflow_name() -> None:
    @workflow.define(name="reserved-workflow-name")
    class FirstWorkflowOwner:
        @workflow.entrypoint
        async def run(self) -> str:
            return "first"

    @workflow.define(name="reserved-workflow-name")
    class SecondWorkflowOwner:
        @workflow.entrypoint
        async def run(self) -> str:
            return "second"

    config = WorkflowsConfig(
        worker={
            "deployment_name": "reserved-workflow-name",
            "workflow_name_prefix": "prefixed-",
        }
    )

    with prepare_workflows([FirstWorkflowOwner], config=config):
        with pytest.raises(WorkflowsException, match="reserved by workflow class 'FirstWorkflowOwner'"):
            with prepare_workflows([SecondWorkflowOwner], config=config):
                pass

        # Replay of another class never blocks, nor is blocked by, the worker that holds the name.
        with prepare_workflows([SecondWorkflowOwner], config=config, replay_only=True):
            assert get_mounted_workflow("prefixed-reserved-workflow-name") is FirstWorkflowOwner


def test_replay_reads_its_own_class_metadata_while_a_worker_holds_the_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    @workflow.define(name="replay-scoped-name", search_keys=["customer_id"])
    class LiveWorkflow:
        @workflow.entrypoint
        async def run(self, customer_id: str) -> str:
            return customer_id

    @workflow.define(name="replay-scoped-name", on_behalf_of=True, search_keys=["order_id"])
    class ReplayedWorkflow:
        @workflow.entrypoint
        async def run(self, order_id: str) -> str:
            return order_id

    config = WorkflowsConfig(worker={"deployment_name": "replay-scoped-name"})
    definition_module = importlib.import_module("mistralai.workflows.core.definition.workflow_definition")
    current_namespace: str | None = None
    monkeypatch.setattr(definition_module, "_current_workflow_namespace", lambda: current_namespace)

    with prepare_workflows([LiveWorkflow], config=config):
        with prepare_workflows([ReplayedWorkflow], config=config, replay_only=True, replay_namespace="replay-ns"):
            current_namespace = "replay-ns"
            assert get_workflow_search_key_info("replay-scoped-name").search_keys == ("order_id",)
            assert is_workflow_on_behalf_of("replay-scoped-name") is True

            current_namespace = "live-ns"
            assert get_workflow_search_key_info("replay-scoped-name").search_keys == ("customer_id",)
            assert is_workflow_on_behalf_of("replay-scoped-name") is False


def test_replay_of_another_class_is_rejected_in_the_namespace_a_worker_uses() -> None:
    @workflow.define(name="namespace-shared-name")
    class LiveWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "live"

    @workflow.define(name="namespace-shared-name")
    class ReplayedWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "replayed"

    config = WorkflowsConfig(
        worker={"deployment_name": "namespace-shared-name"},
        temporal={"namespace": "shared-ns"},
    )

    with prepare_workflows([LiveWorkflow], config=config):
        # Inside the worker's namespace the two classes could not be told apart.
        with pytest.raises(WorkflowsException, match="reserved by workflow class 'LiveWorkflow' in namespace"):
            with prepare_workflows([ReplayedWorkflow], config=config, replay_only=True, replay_namespace="shared-ns"):
                pass

        # The same class can replay under its worker's namespace.
        with prepare_workflows([LiveWorkflow], config=config, replay_only=True, replay_namespace="shared-ns"):
            pass

    with prepare_workflows([ReplayedWorkflow], config=config, replay_only=True, replay_namespace="shared-ns"):
        # And a worker cannot start in the namespace a replay of another class uses.
        with pytest.raises(WorkflowsException, match="reserved by workflow class 'ReplayedWorkflow' in replay"):
            with prepare_workflows([LiveWorkflow], config=config):
                pass


def test_workflow_name_is_released_when_its_last_preparation_closes() -> None:
    @workflow.define(name="released-workflow-name", search_keys=["customer_id"])
    class FirstWorkflowOwner:
        @workflow.entrypoint
        async def run(self, customer_id: str) -> str:
            return customer_id

    @workflow.define(name="released-workflow-name", on_behalf_of=True, search_keys=["order_id"])
    class SecondWorkflowOwner:
        @workflow.entrypoint
        async def run(self, order_id: str) -> str:
            return order_id

    config = WorkflowsConfig(
        worker={
            "deployment_name": "released-workflow-name",
            "workflow_name_prefix": "p_",
        }
    )
    name = "p_released-workflow-name"

    with prepare_workflows([FirstWorkflowOwner], config=config):
        with prepare_workflows([FirstWorkflowOwner], config=config):
            pass
        # The inner preparation of the same class must not release the name.
        with pytest.raises(WorkflowsException, match="reserved by workflow class 'FirstWorkflowOwner'"):
            with prepare_workflows([SecondWorkflowOwner], config=config):
                pass
        assert get_workflow_search_key_info(name).search_keys == ("customer_id",)
        assert is_workflow_on_behalf_of(name) is False

    assert get_mounted_workflow(name) is None

    with prepare_workflows([SecondWorkflowOwner], config=config):
        assert get_workflow_definition(SecondWorkflowOwner).name == name
        assert get_workflow_search_key_info(name).search_keys == ("order_id",)
        assert is_workflow_on_behalf_of(name) is True


def test_failed_preparation_leaves_definitions_and_names_unchanged() -> None:
    @workflow.define(name="atomic-held-name")
    class HeldWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "held"

    @workflow.define(name="atomic-free-name")
    class FreeWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "free"

    @workflow.define(name="atomic-held-name")
    class ConflictingWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "conflict"

    config = WorkflowsConfig(worker={"deployment_name": "atomic-preparation"})
    free_definition = get_workflow_definition(FreeWorkflow)

    with prepare_workflows([HeldWorkflow], config=config):
        with pytest.raises(WorkflowsException, match="reserved by workflow class 'HeldWorkflow'"):
            with prepare_workflows([FreeWorkflow, ConflictingWorkflow], config=config):
                pass

        assert get_mounted_workflow("atomic-free-name") is None
        assert get_workflow_definition(FreeWorkflow) == free_definition
        assert not hasattr(FreeWorkflow, _TEMPORAL_DEFINITION_CONFIG_ATTR)
        assert not hasattr(FreeWorkflow, "__temporal_workflow_definition")

    # The failed attempt pinned nothing, so the class can still be prepared with other settings.
    with prepare_workflows(
        [FreeWorkflow],
        config=WorkflowsConfig(worker={"deployment_name": "atomic-preparation", "workflow_name_prefix": "retry_"}),
    ):
        assert get_workflow_definition(FreeWorkflow).name == "retry_atomic-free-name"


@pytest.mark.asyncio
async def test_same_workflow_and_task_queue_routes_config_by_deployment_version() -> None:
    @workflow.define(name="different-deployment-version-config")
    class DifferentDeploymentVersionConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return legacy_config.common.app_name

    task_queue = "different-deployment-version-config"
    deployment_name = "config-routing"
    first_config = WorkflowsConfig(
        common={"app_name": "deployment-v1"},
        worker={
            "deployment_name": task_queue,
            "versioning": {
                "deployment_name": deployment_name,
                "build_id": "v1",
                "auto_register_as_current": False,
            },
        },
    )
    second_config = WorkflowsConfig(
        common={"app_name": "deployment-v2"},
        worker={
            "deployment_name": task_queue,
            "versioning": {
                "deployment_name": deployment_name,
                "build_id": "v2",
                "auto_register_as_current": False,
            },
        },
    )

    async with (
        _hold_preparation([DifferentDeploymentVersionConfigWorkflow], first_config),
        _hold_preparation([DifferentDeploymentVersionConfigWorkflow], second_config),
    ):
        current_build_id = ["v1"]
        current_run_id = ["run-v1-a"]

        class WorkflowInfo:
            workflow_type = "different-deployment-version-config"
            task_queue = "different-deployment-version-config"
            workflow_id = "different-deployment-version-config"

            @property
            def run_id(self) -> str:
                return current_run_id[0]

            def get_current_deployment_version(self) -> WorkerDeploymentVersion:
                return WorkerDeploymentVersion(
                    deployment_name=deployment_name,
                    build_id=current_build_id[0],
                )

        with (
            patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True),
            patch("mistralai.workflows.core.config.config.temporalio.workflow.info", return_value=WorkflowInfo()),
        ):
            assert legacy_config.common.app_name == "deployment-v1"
            mutable_view = legacy_config.common
            mutable_view.app_name = "mutated"
            assert legacy_config.common.app_name == "mutated"
            current_run_id[0] = "run-v1-b"
            assert legacy_config.common.app_name == "deployment-v1"
            current_build_id[0] = "v2"
            current_run_id[0] = "run-v2"
            assert legacy_config.common.app_name == "deployment-v2"
            current_build_id[0] = "missing"
            with pytest.raises(WorkflowsException, match="deployment version.*missing"):
                _ = legacy_config.common.app_name


@pytest.mark.asyncio
async def test_test_worker_releases_workflow_config_registration(
    temporal_env: WorkflowEnvironment,
) -> None:
    for task_queue in ("test-worker-queue-a", "test-worker-queue-b"):
        async with create_test_worker(
            temporal_env,
            workflows=[ReusableTestWorkerWorkflow],
            task_queue=task_queue,
        ):
            pass


@pytest.mark.asyncio
async def test_temporal_worker_lifecycle_releases_workflow_config_registration(
    temporal_env: WorkflowEnvironment,
) -> None:
    for task_queue in ("worker-queue-a", "worker-queue-b"):
        worker_config = WorkflowsConfig(worker={"deployment_name": task_queue})
        with use_config(worker_config), ExitStack() as registrations:
            workers, _ = _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[ReusableTestWorkerWorkflow],
                config=worker_config,
                task_queue=task_queue,
                workflow_config_registrations=registrations,
            )
            async with AsyncExitStack() as worker_stack:
                for worker in workers:
                    await worker_stack.enter_async_context(worker)


@pytest.mark.asyncio
async def test_unversioned_worker_routes_config_through_synthetic_deployment_version(
    temporal_env: WorkflowEnvironment,
) -> None:
    task_queue = "synthetic-deployment-version"
    worker_name = "synthetic-worker"
    synthetic_id = "synthetic-id"
    worker_config = WorkflowsConfig(
        common={"app_name": "synthetic-deployment-config"},
        worker={"deployment_name": task_queue, "worker_name": worker_name},
    )

    class WorkflowInfo:
        workflow_type = "reusable-test-worker"
        task_queue = "synthetic-deployment-version"

        def get_current_deployment_version(self) -> WorkerDeploymentVersion:
            return WorkerDeploymentVersion(
                deployment_name=task_queue,
                build_id=f"{worker_name}-{task_queue}-{synthetic_id}",
            )

    with (
        use_config(worker_config),
        ExitStack() as registrations,
        patch("mistralai.workflows.core.worker.uuid4") as uuid4_mock,
    ):
        uuid4_mock.return_value.hex = synthetic_id
        _create_temporal_workers(
            temporal_client=temporal_env.client,
            workflows=[ReusableTestWorkerWorkflow],
            config=worker_config,
            task_queue=task_queue,
            workflow_config_registrations=registrations,
        )
        with (
            patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True),
            patch("mistralai.workflows.core.config.config.temporalio.workflow.info", return_value=WorkflowInfo()),
        ):
            assert legacy_config.common.app_name == "synthetic-deployment-config"


@pytest.mark.parametrize(
    "conflicting_config_overrides",
    [
        {"worker": {"retry_policy_max_attempts": 7}},
        {"worker": {"local_retry_backoff_coefficient": 1.5}},
        {"worker": {"worker_name": "another-worker"}},
        {"common": {"app_name": "another-app"}},
        {"http": {"timeout": 17.0}},
    ],
)
@pytest.mark.asyncio
async def test_same_workflow_and_task_queue_rejects_conflicting_config(
    conflicting_config_overrides: dict[str, dict[str, object]],
) -> None:
    @workflow.define(name="conflicting-runtime-config")
    class ConflictingRuntimeConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    task_queue = "test-conflicting-runtime-config"
    first_config = WorkflowsConfig(
        worker={
            "deployment_name": task_queue,
            "retry_policy_max_attempts": 3,
        }
    )
    conflicting_config = WorkflowsConfig(
        common=conflicting_config_overrides.get("common", {}),
        worker={
            "deployment_name": task_queue,
            "retry_policy_max_attempts": 3,
            **conflicting_config_overrides.get("worker", {}),
        },
        http=conflicting_config_overrides.get("http", {}),
    )

    async with _hold_preparation([ConflictingRuntimeConfigWorkflow], first_config):
        with pytest.raises(WorkflowsException, match="different workflow configuration"):
            with prepare_workflows([ConflictingRuntimeConfigWorkflow], config=conflicting_config):
                pass


def test_same_workflow_and_task_queue_accepts_identical_complete_config() -> None:
    @workflow.define(name="identical-runtime-config")
    class IdenticalRuntimeConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    task_queue = "test-identical-runtime-config"
    first_config = WorkflowsConfig(
        common={"app_name": "identical-app"},
        worker={"deployment_name": task_queue, "worker_name": "identical-worker"},
        http={"timeout": 17.0},
    )
    identical_config = first_config.model_copy(deep=True)

    with (
        prepare_workflows([IdenticalRuntimeConfigWorkflow], config=first_config),
        prepare_workflows([IdenticalRuntimeConfigWorkflow], config=identical_config),
    ):
        pass


def test_prepare_workflows_rejects_default_worker_task_queue() -> None:
    config = WorkflowsConfig(worker={"deployment_name": None})

    with pytest.raises(ValueError, match="DEPLOYMENT_NAME is required"):
        with prepare_workflows([DirectTemporalWorkflow], config=config):
            pass


def test_prepare_workflows_allows_default_task_queue_for_replay_only() -> None:
    @workflow.define(name="replay-only")
    class ReplayOnlyWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    config = WorkflowsConfig(worker={"deployment_name": None})

    with prepare_workflows([ReplayOnlyWorkflow], config=config, replay_only=True) as prepared:
        Replayer(
            workflows=prepared,
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        )


def test_replay_only_config_matches_versioned_history_from_another_task_queue() -> None:
    @workflow.define(name="versioned-replay-config")
    class VersionedReplayConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return legacy_config.common.app_name

    config = WorkflowsConfig(
        common={"app_name": "replay-snapshot"},
        worker={"deployment_name": None},
    )

    class WorkflowInfo:
        workflow_type = "versioned-replay-config"
        task_queue = "original-deployment-queue"
        namespace = "ReplayNamespace"

        def get_current_deployment_version(self) -> WorkerDeploymentVersion:
            return WorkerDeploymentVersion(deployment_name="original-deployment", build_id="build-1")

    with prepare_workflows([VersionedReplayConfigWorkflow], config=config, replay_only=True):
        with (
            patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True),
            patch("mistralai.workflows.core.config.config.temporalio.workflow.info", return_value=WorkflowInfo()),
        ):
            assert legacy_config.common.app_name == "replay-snapshot"


@pytest.mark.asyncio
async def test_replay_config_does_not_leak_into_live_versioned_activation() -> None:
    @workflow.define(name="unversioned-worker-config")
    class UnversionedWorkerConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return legacy_config.common.app_name

    configured_task_queue = "unversioned-worker-config"
    worker_config = WorkflowsConfig(
        common={"app_name": "live-worker-snapshot"},
        worker={"deployment_name": configured_task_queue},
    )
    replay_config = WorkflowsConfig(
        common={"app_name": "replay-snapshot"},
        worker={"deployment_name": None},
    )

    class WorkflowInfo:
        workflow_type = "unversioned-worker-config"
        task_queue = configured_task_queue
        namespace = "production-namespace"

        def get_current_deployment_version(self) -> WorkerDeploymentVersion:
            return WorkerDeploymentVersion(deployment_name="unexpected-deployment", build_id="build-2")

    async with _hold_preparation([UnversionedWorkerConfigWorkflow], worker_config):
        with prepare_workflows([UnversionedWorkerConfigWorkflow], config=replay_config, replay_only=True):
            with (
                patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True),
                patch("mistralai.workflows.core.config.config.temporalio.workflow.info", return_value=WorkflowInfo()),
            ):
                assert legacy_config.common.app_name == "live-worker-snapshot"


@pytest.mark.asyncio
async def test_replay_uses_its_prepared_config_while_a_live_worker_serves_the_same_queue() -> None:
    @workflow.define(name="replay-beside-live-worker")
    class ReplayBesideLiveWorkerWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return legacy_config.common.app_name

    task_queue = "replay-beside-live-worker"
    worker_config = WorkflowsConfig(
        common={"app_name": "live-worker-snapshot"},
        worker={"deployment_name": task_queue},
    )
    replay_config = WorkflowsConfig(
        common={"app_name": "replay-snapshot"},
        worker={"deployment_name": None},
    )

    class WorkflowInfo:
        workflow_type = "replay-beside-live-worker"
        namespace = "ReplayNamespace"

        def __init__(self, task_queue: str) -> None:
            self.task_queue = task_queue

        def get_current_deployment_version(self) -> None:
            return None

    async with _hold_preparation([ReplayBesideLiveWorkerWorkflow], worker_config):
        with prepare_workflows([ReplayBesideLiveWorkerWorkflow], config=replay_config, replay_only=True):
            with patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True):
                with patch(
                    "mistralai.workflows.core.config.config.temporalio.workflow.info",
                    return_value=WorkflowInfo(task_queue),
                ):
                    assert legacy_config.common.app_name == "replay-snapshot"
                live_info = WorkflowInfo(task_queue)
                live_info.namespace = "default"
                with patch(
                    "mistralai.workflows.core.config.config.temporalio.workflow.info",
                    return_value=live_info,
                ):
                    assert legacy_config.common.app_name == "live-worker-snapshot"


@pytest.mark.asyncio
async def test_unversioned_worker_falls_back_for_a_stale_synthetic_version() -> None:
    @workflow.define(name="unversioned-restart-config")
    class UnversionedRestartConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return legacy_config.common.app_name

    task_queue = "unversioned-restart-config"
    config = WorkflowsConfig(common={"app_name": "current-worker"}, worker={"deployment_name": task_queue})

    class WorkflowInfo:
        workflow_type = "unversioned-restart-config"
        workflow_id = "unversioned-restart-config"
        run_id = "run-from-previous-process"
        namespace = "default"

        def __init__(self) -> None:
            self.task_queue = task_queue

        def get_current_deployment_version(self) -> WorkerDeploymentVersion:
            return WorkerDeploymentVersion(deployment_name=task_queue, build_id="previous-process-uuid")

    # run_worker() registers an unversioned worker twice: once without a version and once
    # under its synthetic build ID. A run from a previous process reports another synthetic ID.
    with prepare_workflows([UnversionedRestartConfigWorkflow], config=config) as prepared:
        with _use_workflow_config_for_worker(
            prepared[0],
            config,
            task_queue,
            deployment_version_override=(task_queue, "current-process-uuid"),
        ):
            with (
                patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True),
                patch("mistralai.workflows.core.config.config.temporalio.workflow.info", return_value=WorkflowInfo()),
            ):
                assert legacy_config.common.app_name == "current-worker"


@pytest.mark.asyncio
async def test_versioned_run_falls_back_to_the_single_config_on_its_task_queue() -> None:
    @workflow.define(name="version-recovery-config")
    class VersionRecoveryConfigWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return legacy_config.common.app_name

    task_queue = "version-recovery-config"
    v2_config = WorkflowsConfig(
        common={"app_name": "deployment-v2"},
        worker={
            "deployment_name": task_queue,
            "versioning": {
                "deployment_name": "recovery",
                "build_id": "v2",
                "auto_register_as_current": False,
            },
        },
    )

    class WorkflowInfo:
        workflow_type = "version-recovery-config"
        workflow_id = "version-recovery-config"
        run_id = "run-started-on-v1"
        namespace = "default"

        def __init__(self, queue: str) -> None:
            self.task_queue = queue

        def get_current_deployment_version(self) -> WorkerDeploymentVersion:
            return WorkerDeploymentVersion(deployment_name="recovery", build_id="v1")

    async with _hold_preparation([VersionRecoveryConfigWorkflow], v2_config):
        with patch("mistralai.workflows.core.config.config.temporalio.workflow.in_workflow", return_value=True):
            with patch(
                "mistralai.workflows.core.config.config.temporalio.workflow.info",
                return_value=WorkflowInfo(task_queue),
            ):
                assert legacy_config.common.app_name == "deployment-v2"
            with patch(
                "mistralai.workflows.core.config.config.temporalio.workflow.info",
                return_value=WorkflowInfo("another-task-queue"),
            ):
                with pytest.raises(WorkflowsException, match="deployment version"):
                    _ = legacy_config.common.app_name


@pytest.mark.parametrize(
    ("initial_worker_config", "conflicting_worker_config"),
    [
        pytest.param(
            {"workflow_name_prefix": "first_"},
            {"workflow_name_prefix": "second_"},
            id="workflow-name",
        ),
        pytest.param(
            {"default_enforce_determinism": True},
            {"default_enforce_determinism": False},
            id="determinism",
        ),
        pytest.param(
            {"versioning": {"deployment_name": "deployment", "BUILD_ID": "build"}},
            {"versioning": {"enabled": False, "deployment_name": None, "BUILD_ID": None}},
            id="versioning-behavior",
        ),
    ],
)
def test_workflow_class_rejects_conflicting_worker_definition_config(
    initial_worker_config: dict[str, object],
    conflicting_worker_config: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TEMPORAL_DEPLOYMENT_NAME", raising=False)
    monkeypatch.delenv("TEMPORAL_WORKER_BUILD_ID", raising=False)

    @workflow.define(name="invoice")
    class InvoiceWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    initial_config = WorkflowsConfig(worker=initial_worker_config)
    conflicting_config = WorkflowsConfig(worker=conflicting_worker_config)
    with ExitStack() as mounts:
        configure_workflow_for_worker(InvoiceWorkflow, initial_config, mounts)
    initial_workflow_definition = get_workflow_definition(InvoiceWorkflow)
    initial_temporal_definition = InvoiceWorkflow.__temporal_workflow_definition

    with ExitStack() as mounts, pytest.raises(WorkflowsException, match="cannot be reused in the same process"):
        configure_workflow_for_worker(InvoiceWorkflow, conflicting_config, mounts)

    assert get_workflow_definition(InvoiceWorkflow) == initial_workflow_definition
    assert InvoiceWorkflow.__temporal_workflow_definition is initial_temporal_definition


def test_workflow_class_allows_non_definition_config_changes() -> None:
    @workflow.define(name="invoice")
    class InvoiceWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    with ExitStack() as mounts:
        configure_workflow_for_worker(
            InvoiceWorkflow,
            WorkflowsConfig(worker={"server_url": "https://first.example"}),
            mounts,
        )
    temporal_definition = InvoiceWorkflow.__temporal_workflow_definition

    with ExitStack() as mounts:
        configure_workflow_for_worker(
            InvoiceWorkflow,
            WorkflowsConfig(worker={"server_url": "https://second.example"}),
            mounts,
        )

    assert InvoiceWorkflow.__temporal_workflow_definition is temporal_definition


def test_concurrent_workflow_preparation_serializes_metadata_updates(monkeypatch: pytest.MonkeyPatch) -> None:
    @workflow.define(name="concurrent-metadata-config", search_keys=["value"])
    class ConcurrentMetadataWorkflow:
        @workflow.entrypoint
        async def run(self, value: str) -> str:
            return value

    preparation = importlib.import_module("mistralai.workflows.core.definition._workflow_preparation")
    original_set = preparation.set_workflow_definition
    first_set_started = Event()
    release_first_set = Event()
    second_set_started = Event()
    call_count_lock = Lock()
    call_count = 0

    def blocking_set(workflow_type: type, definition: WorkflowSpec) -> None:
        nonlocal call_count
        with call_count_lock:
            call_count += 1
            current_call = call_count
        if current_call == 1:
            first_set_started.set()
            assert release_first_set.wait(timeout=5)
        else:
            second_set_started.set()
        original_set(workflow_type, definition)

    monkeypatch.setattr(preparation, "set_workflow_definition", blocking_set)
    config = WorkflowsConfig(worker={"workflow_name_prefix": "code_"})

    with ExitStack() as first_mounts, ExitStack() as second_mounts:
        with ThreadPoolExecutor(max_workers=2) as executor:
            first = executor.submit(configure_workflow_for_worker, ConcurrentMetadataWorkflow, config, first_mounts)
            assert first_set_started.wait(timeout=5)
            second = executor.submit(configure_workflow_for_worker, ConcurrentMetadataWorkflow, config, second_mounts)
            try:
                assert not second_set_started.wait(timeout=0.1)
            finally:
                release_first_set.set()
            first.result(timeout=5)
            second.result(timeout=5)

        configured_name = "code_concurrent-metadata-config"
        assert get_workflow_definition(ConcurrentMetadataWorkflow).name == configured_name
        assert get_workflow_search_key_info(configured_name).search_keys == ("value",)


def test_worker_config_mounts_workflow_metadata_under_the_configured_name() -> None:
    @workflow.define(
        name="metadata-config-test",
        on_behalf_of=True,
        search_keys=["invoice_id"],
    )
    class MetadataWorkflow:
        @workflow.entrypoint
        async def run(self, invoice_id: str) -> str:
            return invoice_id

    configured_name = "code_metadata-config-test"
    with ExitStack() as mounts:
        configure_workflow_for_worker(
            MetadataWorkflow,
            WorkflowsConfig(worker={"workflow_name_prefix": "code_"}),
            mounts,
        )

        assert is_workflow_on_behalf_of(configured_name) is True
        assert get_workflow_search_key_info(configured_name).search_keys == ("invoice_id",)
        assert is_workflow_on_behalf_of("metadata-config-test") is False
        with pytest.raises(KeyError):
            get_workflow_search_key_info("metadata-config-test")

    assert is_workflow_on_behalf_of(configured_name) is False
    with pytest.raises(KeyError):
        get_workflow_search_key_info(configured_name)


def test_worker_config_preserves_metadata_when_prefixed_names_overlap() -> None:
    @workflow.define(
        name="prefix-collision-invoice",
        search_keys=["invoice_id"],
    )
    class InvoiceWorkflow:
        @workflow.entrypoint
        async def run(self, invoice_id: str) -> str:
            return invoice_id

    @workflow.define(
        name="p_prefix-collision-invoice",
        on_behalf_of=True,
        search_keys=["prefixed_invoice_id"],
    )
    class PrefixedInvoiceWorkflow:
        @workflow.entrypoint
        async def run(self, prefixed_invoice_id: str) -> str:
            return prefixed_invoice_id

    config = WorkflowsConfig(
        worker={
            "deployment_name": "prefix-collision",
            "workflow_name_prefix": "p_",
        }
    )

    with prepare_workflows([InvoiceWorkflow, PrefixedInvoiceWorkflow], config=config):
        assert get_workflow_search_key_info("p_prefix-collision-invoice").search_keys == ("invoice_id",)
        assert get_workflow_search_key_info("p_p_prefix-collision-invoice").search_keys == ("prefixed_invoice_id",)
        assert is_workflow_on_behalf_of("p_prefix-collision-invoice") is False
        assert is_workflow_on_behalf_of("p_p_prefix-collision-invoice") is True


@pytest.mark.asyncio
@pytest.mark.parametrize("config_source", ["environment", "code"])
async def test_workflow_prefix_routes_child_workflows_for_every_config_source(
    config_source: str,
    monkeypatch: pytest.MonkeyPatch,
    temporal_env: WorkflowEnvironment,
) -> None:
    prefix = f"{config_source}_"
    config_module = importlib.import_module("mistralai.workflows.core.config.config")
    lazy_config = config_module._lazy_config
    previously_loaded_config = lazy_config.get_if_loaded()
    object.__setattr__(lazy_config, "_value", None)
    configured_workflow_types = [ParentWorkflow, ChildWorkflow, ParallelExecutionWorkflow]
    original_workflow_definitions = {
        workflow_type: get_workflow_definition(workflow_type) for workflow_type in configured_workflow_types
    }
    original_temporal_definitions = {
        workflow_type: getattr(workflow_type, "__temporal_workflow_definition", None)
        for workflow_type in configured_workflow_types
    }
    original_temporal_configs = {
        workflow_type: getattr(workflow_type, _TEMPORAL_DEFINITION_CONFIG_ATTR, None)
        for workflow_type in configured_workflow_types
    }
    for workflow_type in configured_workflow_types:
        _clear_temporal_definition(workflow_type)
    plugin_workflow_names: list[str] = []

    def collect_plugin_metadata(workflow_types: list[type]) -> list[object]:
        plugin_workflow_names.extend(get_workflow_definition(workflow_type).name for workflow_type in workflow_types)
        return []

    monkeypatch.setattr(
        "mistralai.workflows.core.worker.collect_plugin_interceptors",
        collect_plugin_metadata,
    )

    if config_source == "environment":
        monkeypatch.setenv("WORKFLOW_NAME_PREFIX", prefix)
        explicit_config = None
    else:
        monkeypatch.delenv("WORKFLOW_NAME_PREFIX", raising=False)
        explicit_config = WorkflowsConfig(worker={"workflow_name_prefix": prefix})

    resolved_config = resolve_worker_config(explicit_config)
    task_queue = f"test-config-as-code-{config_source}"

    try:
        with use_config(resolved_config), ExitStack() as registrations:
            workers, _ = _create_temporal_workers(
                temporal_client=temporal_env.client,
                workflows=[ParentWorkflow, ChildWorkflow],
                config=resolved_config,
                task_queue=task_queue,
                workflow_config_registrations=registrations,
            )
            async with AsyncExitStack() as stack:
                for worker in workers:
                    await stack.enter_async_context(worker)

                handle = await temporal_env.client.start_workflow(
                    f"{prefix}parent_workflow",
                    {"name": "config-as-code"},
                    id=f"test-config-as-code-{config_source}",
                    task_queue=task_queue,
                )
                result = await asyncio.wait_for(handle.result(), timeout=5)

        assert result["result"] == "Parent got: Child says: config-as-code"
        assert plugin_workflow_names == [
            f"{prefix}parent_workflow",
            f"{prefix}child_workflow",
            f"{prefix}__parallel_execution__",
        ]
    finally:
        object.__setattr__(lazy_config, "_value", previously_loaded_config)
        for workflow_type in configured_workflow_types:
            original_workflow_definition = original_workflow_definitions[workflow_type]
            replace_workflow_definition(workflow_type, original_workflow_definition)
            _clear_temporal_definition(workflow_type)
            original_temporal_definition = original_temporal_definitions[workflow_type]
            if original_temporal_definition is not None:
                setattr(workflow_type, "__temporal_workflow_definition", original_temporal_definition)
                setattr(
                    original_temporal_definition.run_fn,
                    "__temporal_workflow_definition",
                    original_temporal_definition,
                )
            original_temporal_config = original_temporal_configs[workflow_type]
            if original_temporal_config is not None:
                setattr(workflow_type, _TEMPORAL_DEFINITION_CONFIG_ATTR, original_temporal_config)
        # Finalize Temporal's completed sandbox coroutines here so they cannot surface as
        # unraisable exceptions in a later test that deliberately installs an unraisable hook.
        gc.collect()


def test_explicit_decorator_determinism_wins_over_worker_config() -> None:
    @workflow.define(name="explicit-determinism", enforce_determinism=True)
    class ExplicitDeterminismWorkflow:
        @workflow.entrypoint
        async def run(self) -> str:
            return "done"

    config = WorkflowsConfig(worker={"default_enforce_determinism": False})

    with ExitStack() as mounts:
        configure_workflow_for_worker(ExplicitDeterminismWorkflow, config, mounts)

    assert get_workflow_definition(ExplicitDeterminismWorkflow).enforce_determinism is True
    assert ExplicitDeterminismWorkflow.__temporal_workflow_definition.sandboxed is True
