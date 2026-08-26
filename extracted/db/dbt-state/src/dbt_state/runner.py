from __future__ import annotations

import threading
import time
import typing as t
from copy import deepcopy
from dataclasses import replace
from datetime import datetime

from dbt.adapters.factory import get_adapter
from dbt.config.runtime import RuntimeConfig
from dbt.contracts.graph.manifest import Manifest
from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ManifestNode,
    ModelNode,
    SeedNode,
    SingularTestNode,
    SnapshotNode,
)
from dbt.contracts.results import RunResult, RunStatus
from dbt.events.types import LogTestResult as DbtLogTestResult
from dbt.events.types import green, red, yellow

from dbt_state.auth.sso import Org
from dbt_state.errors import (
    AuthenticationError,
    RecoverableAuthenticationError,
    UnsupportedClientVersionError,
)

try:
    from dbt_common.events.format import format_fancy_output_line
except ImportError:
    from dbt.events.format import format_fancy_output_line  # type: ignore

try:
    from dbt_common.exceptions import DbtRuntimeError
except ImportError:
    # dbt 1.7
    from dbt.exceptions import DbtRuntimeError

try:
    from dbt.task.run import MicrobatchBatchRunner
except ImportError:
    # dbt < 1.9 has no microbatch batch runner
    MicrobatchBatchRunner = None  # type: ignore[assignment,misc]

from query_cache_common.constants import NO_OP_STATUS

from dbt_state import events
from dbt_state.adapters import ADAPTER_EXTENSION_MAPPING
from dbt_state.auth import sso_auth
from dbt_state.config import DBT_RUN_CACHE_PATH, RunCacheConfig
from dbt_state.dispatcher import (
    AsyncTelemetryDispatcher,
    NoOpTelemetryDispatcher,
    TelemetryDispatcher,
)
from dbt_state.grpc.client import QueryCacheGrpcClient
from dbt_state.run_cache import NoRunResult, RunCache
from dbt_state.session import SessionManager
from dbt_state.system_info import (
    get_cloud_run_id,
    get_invocation_id,
    get_os_name,
    get_system_user_id,
)
from dbt_state.utils import (
    DBT_VERSION,
    format_time_saved,
    is_ci_environment,
    is_non_interactive_environment,
)
from dbt_state.version import __version__

if t.TYPE_CHECKING:
    from dbt.adapters.sql import SQLAdapter
    from dbt.task.compile import CompileRunner
    from dbt.task.run import MicrobatchModelRunner, ModelRunner
    from dbt.task.runnable import GraphRunnableTask
    from dbt.task.test import TestRunner

    from dbt_state._typing import ModelOrSnapshotNode


class RunnerOverride:
    def __init__(
        self,
        original_execute: t.Callable[[ModelRunner, ModelOrSnapshotNode, Manifest], RunResult],
        original_run_with_hooks: t.Callable[[ModelRunner, Manifest], RunResult],
        original_microbatch_execute: t.Optional[
            t.Callable[[MicrobatchModelRunner, ModelNode, Manifest], RunResult]
        ],
        original_generate_runtime_model_context: t.Callable[
            [ManifestNode, RuntimeConfig, Manifest], t.Dict[str, t.Any]
        ],
        original_build_test_run_result: t.Optional[t.Callable] = None,
        telemetry_dispatcher: TelemetryDispatcher | None = None,
        query_cache_client: QueryCacheGrpcClient | None = None,
    ) -> None:
        self._original_execute = original_execute
        self._original_run_with_hooks = original_run_with_hooks
        self._original_microbatch_execute = original_microbatch_execute
        self._original_generate_runtime_model_context = original_generate_runtime_model_context
        self._original_build_test_run_result = original_build_test_run_result
        self._query_cache_client = query_cache_client
        self._run_cache: RunCache | None = None
        self._run_cache_lock = threading.Lock()
        self._disabled = False
        self._telemetry_dispatcher = telemetry_dispatcher
        self._session: t.Optional[SessionManager] = None
        self._org_info: t.Optional[Org] = None
        self._runtime_config: RuntimeConfig | None = None
        events.register_callback("runner-override-end-of-run-message", self._on_event)

    def set_runtime_config(self, config: RuntimeConfig) -> None:
        """Set the runtime config early so it's available for selector creation."""
        self._runtime_config = config

    def build_test_run_result_override(
        self, runner: TestRunner, test: t.Any, result: t.Any
    ) -> RunResult:
        """Attach a State decision ID and mark cached passing data tests as reused."""
        if self._original_build_test_run_result is None:
            raise RuntimeError("Test result override is not configured")

        run_result = self._original_build_test_run_result(runner, test, result)
        if self._run_cache is None:
            return run_result

        self._run_cache.attach_state_decision_id(t.cast(ManifestNode, run_result.node), run_result)
        if str(run_result.status) != "pass":
            return run_result

        try:
            message = (run_result.adapter_response or {}).get("_message") or ""
            if not message.startswith(NO_OP_STATUS):
                return run_result
            reused_status = self._run_cache._cache_hit_run_status()  # noqa: SLF001
            if reused_status is not RunStatus.Success:
                run_result.status = reused_status
        except Exception as e:
            events.fire_warn_event_with_cache_bypass(
                "build_test_run_result: dbt State failed for node {}:\n{}",
                getattr(run_result.node, "unique_id", "unknown"),
                str(e),
            )
        return run_result

    def run_with_hooks_override(self, runner: ModelRunner, manifest: Manifest) -> RunResult:
        """Attach a State decision ID to dbt Core's final per-node result."""
        result = self._original_run_with_hooks(runner, manifest)

        # Microbatch batch runners share the model unique ID, but the State decision belongs
        # to the outer model result rather than each internal batch result.
        if MicrobatchBatchRunner is not None and isinstance(runner, MicrobatchBatchRunner):
            return result

        if self._run_cache is not None:
            self._run_cache.attach_state_decision_id(t.cast(ManifestNode, result.node), result)
        return result

    def create_state_selector_override(
        self,
        manifest: Manifest,
        previous_state: t.Any,
        arguments: t.List[str],
        original_selector: t.Callable[..., t.Any],
        **kwargs: t.Any,
    ) -> t.Any:
        """Create a state selector configured for the current dbt invocation.

        If dbt-state cannot initialize its selector dependencies, return dbt's
        built-in selector so node selection can continue normally.
        """
        from dbt_state.selector import StateSelector

        try:
            if self._runtime_config is None:
                raise RuntimeError("Runtime config is not available")
            run_cache_config = RunCacheConfig.from_runtime_config(self._runtime_config)
            client = self._get_or_create_client(run_cache_config)
            return StateSelector(
                manifest=manifest,
                previous_state=previous_state,
                arguments=arguments,
                runtime_config=self._runtime_config,
                run_cache_config=run_cache_config,
                query_cache_client=client,
                **kwargs,
            )
        except Exception as e:
            events.fire_debug_event("Failed to set up selector context: {}", str(e))
            return original_selector(manifest, previous_state, arguments, **kwargs)

    def defer_to_manifest_override(self, task: GraphRunnableTask) -> None:
        """Sets defer_relation on unselected manifest nodes to enable dbt's native deferral."""
        manifest = task.manifest
        if manifest is None:
            return

        adapter = get_adapter(task.config)
        run_cache = self._run_cache_get_or_create(task.config, adapter, manifest)
        if run_cache is None:
            return

        run_cache.prewarm_connections()
        run_cache.resolve_state_deferred_relations()

        any_deferred = False
        for unique_id, node in manifest.nodes.items():
            if not isinstance(node, (ModelNode, SeedNode, SnapshotNode)):
                continue
            defer_rel = run_cache.get_defer_relation(node)
            if defer_rel is not None:
                attrs_to_replace: t.Dict[str, t.Any] = dict(defer_relation=defer_rel)
                if DBT_VERSION < (1, 8, 0) and self._should_defer(node, task.config, adapter):
                    # In dbt 1.7.* the manifest node is replaced in place, while in later versions
                    # setting defer_relation on the node is sufficient
                    attrs_to_replace.update(
                        dict(
                            database=defer_rel.database,
                            schema=defer_rel.schema,
                            alias=defer_rel.alias,
                            deferred=True,
                        )
                    )
                manifest.nodes[unique_id] = replace(node, **attrs_to_replace)
                any_deferred = True

        if any_deferred:
            # Flags is a frozen dataclass, so we use object.__setattr__
            object.__setattr__(task.config.args, "defer", True)

    def execute_override(
        self, runner: ModelRunner, node: ModelOrSnapshotNode, manifest: Manifest
    ) -> RunResult:
        # Microbatch batch runners inherit ModelRunner.execute but are orchestrated by
        # microbatch_execute_override, which makes a single per-model cache decision.
        # Individual batches must never make their own cache calls, so bypass straight
        # to the original execute.
        if MicrobatchBatchRunner is not None and isinstance(runner, MicrobatchBatchRunner):
            return self._original_execute(runner, node, manifest)

        return self._execute_with_cache(
            runner,
            node,
            manifest,
            original=self._original_execute,
            submit=lambda run_cache: run_cache.on_execute(node),
            should_confirm=lambda result: True,
        )

    def microbatch_execute_override(
        self, runner: MicrobatchModelRunner, node: ModelNode, manifest: Manifest
    ) -> RunResult:
        """Makes a single per-model cache decision for a microbatch model.

        Microbatch models are orchestrated batch-by-batch by dbt, but every batch
        writes into the same target table and shares the model-level query hash. A
        per-batch cache decision is therefore unsound. This override consults the
        cache once for the whole model (with the event-time window folded into the
        request), and honors whatever the backend returns: a skip/clone result is
        returned directly (no batches run), otherwise it delegates to the original
        orchestrator, which runs the batches through the (bypassed) per-batch runner.

        Args:
            runner: The microbatch model runner (orchestrator).
            node: The model node being executed.
            manifest: The dbt manifest.

        Returns:
            The RunResult for the model: the cache skip/clone result, or the result
            of running the batches.
        """
        if self._original_microbatch_execute is None:
            raise RuntimeError(
                "microbatch_execute_override was installed without a captured "
                "MicrobatchModelRunner.execute; this indicates a plugin wiring bug."
            )

        if getattr(node, "previous_batch_results", None) is not None:
            # dbt retry sets previous_batch_results and reruns only the failed
            # batches. A whole-model cache skip would wrongly abort the retry, so
            # bypass the per-model cache decision entirely and let dbt orchestrate
            # the (partial) batch set normally.
            return self._original_microbatch_execute(runner, node, manifest)

        window = self._resolve_microbatch_window(runner, node)
        if window is None:
            # Fail open: without a resolvable window we cannot form a stable
            # per-model cache key, so let dbt orchestrate the batches normally.
            events.fire_warn_event_with_cache_bypass(
                "execute: could not resolve microbatch window for node {}; bypassing dbt State",
                node.unique_id,
            )
            return self._original_microbatch_execute(runner, node, manifest)

        def submit(run_cache: RunCache) -> t.Union[RunResult, NoRunResult, None]:
            # Compile the model body without batch context so on_execute hashes a
            # stable, window-independent query. A compile failure surfaces here and
            # is handled by the shared fail-open path.
            self._ensure_microbatch_model_compiled(runner, node, manifest)
            return run_cache.on_execute(node, microbatch_window=window)

        return self._execute_with_cache(
            runner,
            node,
            manifest,
            original=self._original_microbatch_execute,
            submit=submit,
            # Only confirm a fully-successful run: a PartialSuccess/Error status means
            # some batches failed, and confirming would wrongly record the whole
            # window as a clean execution.
            should_confirm=lambda result: result.status == RunStatus.Success,
        )

    def _execute_with_cache(
        self,
        runner: ModelRunner,
        node: ModelOrSnapshotNode,
        manifest: Manifest,
        *,
        original: t.Callable[..., RunResult],
        submit: t.Callable[[RunCache], t.Union[RunResult, NoRunResult, None]],
        should_confirm: t.Callable[[RunResult], bool],
    ) -> RunResult:
        """Shared model-execution flow around the run cache.

        Consults the cache via ``submit``; if that yields a ready RunResult (a
        cache skip/clone) it is returned directly. Otherwise ``original`` runs the
        node, the outcome is recorded, and the execution is confirmed when
        ``should_confirm(result)`` holds. Fails open on any cache error (runs
        ``original`` and marks the state request failed), and always flushes the
        decision logger for the node.

        Args:
            runner: The dbt runner executing the node.
            node: The model/snapshot node being executed.
            manifest: The dbt manifest.
            original: The un-overridden execute to run the node normally.
            submit: Consults the cache (e.g. ``run_cache.on_execute(node)``) and
                returns its response.
            should_confirm: Given the execution result, whether to confirm the
                execution with the cache.
        """
        try:
            run_cache = self._run_cache_get_or_create(runner.config, runner.adapter, manifest)
            if run_cache is None:
                return original(runner, node, manifest)

            try:
                on_execute_result = submit(run_cache)
            except Exception as e:
                events.fire_warn_event_with_cache_bypass(
                    "execute: dbt State failed for node {}:\n{}",
                    node.unique_id,
                    str(e),
                )
                result = original(runner, node, manifest)
                run_cache.on_state_request_failed(node)
                return result

            if isinstance(on_execute_result, RunResult):
                return on_execute_result

            execute_start_ts = time.perf_counter()
            result = original(runner, node, manifest)

            run_cache.on_run_result(node, result)

            if isinstance(on_execute_result, NoRunResult) and should_confirm(result):
                try:
                    elapsed_ms = int((time.perf_counter() - execute_start_ts) * 1000)
                    run_cache.confirm_execution(
                        node,
                        on_execute_result.request_id,
                        on_execute_result.failed_to_clone,
                        execution_runtime_ms=elapsed_ms,
                    )
                except Exception as e:
                    events.fire_warn_event_with_cache_bypass(
                        "execute: request confirmation failed for node {}:\n{}",
                        node.unique_id,
                        str(e),
                    )
            else:
                run_cache.on_state_request_failed(node)
            return result
        finally:
            self.flush_logger(node.name)

    @staticmethod
    def _ensure_microbatch_model_compiled(
        runner: MicrobatchModelRunner, node: ModelNode, manifest: Manifest
    ) -> None:
        """Populates node.compiled_code with the model body compiled without any
        batch/event-time context, so the model-level query hash is stable across
        windows. No-op if the node already carries a compiled body.

        The helper must not set node.batch or the __dbt_internal_microbatch_event_time_*
        config keys, otherwise the compiled body would carry a batch-specific event-time
        filter and the cache key would differ per batch.

        Compilation runs against a throwaway deep copy of the node rather than the
        live node. ``compile_node`` injects ephemeral CTEs and latches
        ``extra_ctes_injected = True`` on whatever node it touches, and dbt never
        resets that flag; if we compiled the live node, dbt's later per-batch
        recompiles would overwrite ``compiled_code`` from ``raw_code`` but skip
        re-prepending the CTE definitions (the latch is still set), leaving the
        batch SQL referencing undefined ``__dbt__cte__*`` names. Compiling a copy
        keeps the live node's compilation state pristine so the per-batch pipeline
        works normally; we then copy only the window-independent ``compiled_code``
        back onto the live node for the cache hash.
        """
        if getattr(node, "compiled_code", None):
            return
        compiler = runner.compiler if hasattr(runner, "compiler") else runner.adapter.get_compiler()
        node_copy = deepcopy(node)
        compiler.compile_node(node_copy, manifest, {})
        node.compiled_code = node_copy.compiled_code

    def compile_override(self, runner: CompileRunner, manifest: Manifest) -> t.Any:
        run_cache = self._run_cache_get_or_create(runner.config, runner.adapter, manifest)
        if run_cache is not None:
            try:
                run_cache._decision_logger.log_node_start(runner.node)  # noqa: SLF001
                run_cache.on_compile(runner.node)
                for dep_id in getattr(runner.node.depends_on, "nodes", []):
                    dep_node = manifest.nodes.get(dep_id)
                    if dep_node and (defer_rel := getattr(dep_node, "defer_relation", None)):
                        run_cache._decision_logger.log_deferral(  # noqa: SLF001
                            node_name=runner.node.name,
                            relation_name=dep_node.name,
                            deferred_to_fqn=defer_rel.relation_name,
                        )
            except Exception as e:
                events.fire_warn_event_with_cache_bypass(
                    "compile: dbt State failed for node {}:\n{}",
                    runner.node.unique_id,
                    str(e),
                )

        if isinstance(runner.node, SeedNode):
            return runner.node
        compiler = runner.compiler if hasattr(runner, "compiler") else runner.adapter.get_compiler()
        compiled_node = compiler.compile_node(runner.node, manifest, {})

        if run_cache is not None:
            try:
                run_cache.cache_compiled_view_sql(compiled_node)
            except Exception as e:
                events.fire_debug_event(
                    "compile: failed to cache view SQL for node {}:\n{}",
                    runner.node.unique_id,
                    str(e),
                )

        return compiled_node

    def print_result_line_override(self, runner: TestRunner, result: RunResult) -> None:
        """Override for printing test results to include NO-OP status."""
        try:
            model = t.cast(ManifestNode, result.node)
            if self._run_cache is not None and self._original_build_test_run_result is None:
                self._run_cache.attach_state_decision_id(model, result)
            kwargs: t.Dict[str, t.Any] = {}
            try:
                from dbt.task import group_lookup

                kwargs["group"] = group_lookup.get(model.unique_id)
                kwargs["attached_node"] = (
                    result.node.attached_node if isinstance(result.node, GenericTestNode) else None
                )
            except ImportError:
                pass

            try:
                name = runner.describe_node_name()
            except Exception:
                name = model.name

            log_test_result = LogTestResult(
                name=name,
                status=str(result.status),
                index=runner.node_index,
                num_models=runner.num_nodes,
                execution_time=result.execution_time,
                node_info=model.node_info,
                num_failures=result.failures,
                **kwargs,
            )
            log_test_result.set_is_no_op(
                (result.adapter_response.get("_message") or "").startswith(NO_OP_STATUS)
            )
            events.dbt_fire_event(
                log_test_result, level=LogTestResult.status_to_level(str(result.status))
            )
        finally:
            self.flush_logger(result.node.name)

    def _on_event(self, msg: events.EventMsg) -> None:
        if msg.info.name == "CommandCompleted":
            savings = self._savings_summary_message()
            free_trial = self._free_trial_message()
            if savings or free_trial:
                events.fire_formatting()
            if savings:
                events.fire_info_event(savings)
            if free_trial:
                events.fire_info_event(free_trial)

    def generate_runtime_model_context_override(
        self, node: ManifestNode, config: RuntimeConfig, manifest: Manifest
    ) -> t.Dict[str, t.Any]:
        context = self._original_generate_runtime_model_context(node, config, manifest)
        # Only override for test nodes. Other kinds of nodes handled by compile_override, so we don't want to interfere with them here.
        if not isinstance(node, (GenericTestNode, SingularTestNode)):
            return context

        adapter = context["adapter"]._adapter  # noqa: SLF001
        run_cache = self._run_cache_get_or_create(config, adapter, manifest)
        if run_cache is None or not run_cache.run_cache_config.enable_data_tests:
            return context

        try:
            run_cache._decision_logger.log_node_start(node)  # noqa: SLF001
            context["adapter"]._adapter = run_cache.data_test_adapter_proxy(node)  # noqa: SLF001
        except Exception as e:
            events.fire_warn_event_with_cache_bypass(
                "generate_runtime_model_context: dbt State failed for node {}:\n{}",
                node.unique_id,
                str(e),
            )
        return context

    def flush_logger(self, node_name: str) -> None:
        if rc := self._run_cache:
            try:
                rc._decision_logger.log_node_end(node_name)  # noqa: SLF001
            except Exception as e:
                events.fire_debug_event(
                    "Failed to flush explainer log entry for {}: {}", node_name, str(e)
                )

    def _get_or_create_client(self, run_cache_config: RunCacheConfig) -> QueryCacheGrpcClient:
        if self._query_cache_client is None:
            self._session = SessionManager()
            self._query_cache_client = QueryCacheGrpcClient.create(
                run_cache_config=run_cache_config,
                session_id=self._session._session_id,  # noqa: SLF001
                system_user_id=get_system_user_id(DBT_RUN_CACHE_PATH),
                os_name=get_os_name(),
                invocation_id=get_invocation_id(),
                cloud_run_id=get_cloud_run_id(),
            )
            self._telemetry_dispatcher = (
                NoOpTelemetryDispatcher()
                if run_cache_config.disable_telemetry
                else AsyncTelemetryDispatcher(
                    query_cache_client=self._query_cache_client,
                )
            )
            self._session.start(
                run_cache_config=run_cache_config, telemetry_dispatcher=self._telemetry_dispatcher
            )
        return self._query_cache_client

    def _run_cache_get_or_create(
        self, config: RuntimeConfig, adapter: SQLAdapter, manifest: Manifest
    ) -> RunCache | None:
        if not self._disabled and self._run_cache is None:
            with self._run_cache_lock:
                if self._run_cache is None and not self._disabled:
                    adapter_type = adapter.type()
                    if adapter_type not in ADAPTER_EXTENSION_MAPPING:
                        events.fire_warn_event(
                            "dbt State disabled: target type '{}' is not supported. "
                            "Supported target types are: {}.",
                            adapter_type,
                            ", ".join(sorted(ADAPTER_EXTENSION_MAPPING.keys())),
                        )
                        self._disabled = True
                        return None

                    run_cache_config = RunCacheConfig.from_runtime_config(config)
                    sso = None
                    try:
                        sso = sso_auth(
                            org_id=run_cache_config.org_id,
                            client_id=run_cache_config.oauth_client_id,
                            client_secret=run_cache_config.oauth_client_secret,
                            dbt_platform_tokens=run_cache_config.dbt_platform_tokens,
                        )
                    except Exception as e:
                        # Fails open: an inability to even construct the auth helper (e.g. an
                        # unwritable/foreign-owned config dir) shouldn't block the run. The
                        # headless pre-check below is skipped in this case, and real auth is
                        # still attempted inside _get_or_create_client further down.
                        events.fire_debug_event(
                            "Failed to construct dbt State auth client: {}", str(e)
                        )

                    if (
                        sso is not None
                        and (is_ci_environment() or is_non_interactive_environment())
                        and not sso.has_noninteractive_credential()
                    ):
                        events.fire_warn_event(
                            "No credentials for dbt State detected. To authenticate without a browser, "
                            "set DBT_CLOUD_TOKEN and DBT_CLOUD_ACCOUNT_HOST environment variables. "
                            "Otherwise, invoke dbt from an attached terminal to log in through the browser. "
                            "See https://docs.getdbt.com/docs/deploy/dbt-state-cicd for more information."
                        )
                        self._disabled = True
                        return None

                    try:
                        client = self._get_or_create_client(run_cache_config)
                    except RecoverableAuthenticationError as e:
                        # Fail open: the account is disabled/locked or the auth service
                        # is unavailable. Disable dbt State and let the dbt run proceed.
                        # Strip a trailing period from the exception text: the helper appends
                        # its own punctuation (and " Continuing without state"), so passing
                        # "...disabled." here would render "...disabled.. Continuing". We keep
                        # the message as a "{}" arg (rather than f-string it into base_msg) so
                        # arbitrary exception text containing braces stays safe.
                        events.fire_warn_event_with_cache_bypass(
                            "dbt State disabled: {}", str(e).removesuffix(".")
                        )
                        self._disabled = True
                        return None
                    except AuthenticationError as e:
                        # Don't print a stack trace to console for AuthenticationError
                        # Raising it as a DbtRuntimeError prints just the message and halts execution
                        raise DbtRuntimeError(str(e)) from e

                    try:
                        client_version_is_supported = client.is_client_version_supported()
                    except Exception as e:
                        events.fire_warn_event("Failed to validate client version: %s", str(e))
                    else:
                        if not client_version_is_supported:
                            raise UnsupportedClientVersionError(
                                "Client version %s is not supported", __version__
                            )

                    assert self._telemetry_dispatcher is not None
                    assert self._session is not None
                    self._run_cache = RunCache.create(
                        run_cache_config,
                        config,
                        adapter,
                        manifest,
                        client,
                        self._telemetry_dispatcher,
                        self._session,
                    )

                    try:
                        if sso is None:
                            sso = sso_auth(org_id=run_cache_config.org_id)
                        self._org_info = sso.get_org_info(sso.org_id(login=False))
                    except Exception:
                        self._org_info = None
        return self._run_cache

    def _should_defer(self, node: ManifestNode, config: RuntimeConfig, adapter: SQLAdapter) -> bool:
        # Check whetehr the original relation already exists and the user did not opt into favoring the state
        return self._favor_state(config) or not adapter.get_relation(
            node.database, node.schema, node.identifier
        )

    @staticmethod
    def _favor_state(config: RuntimeConfig) -> bool:
        return getattr(config.args, "favor_state", False)

    @staticmethod
    def _resolve_microbatch_window(
        runner: MicrobatchModelRunner, node: ModelNode
    ) -> t.Optional[t.Tuple[datetime, datetime]]:
        """Resolves the effective event-time window for a whole microbatch model run.

        This is the run-level window dbt uses to compute the batch set (from
        --event-time-start/end or begin/lookback/now); it is folded into the
        per-model cache key, not keyed per batch.

        Args:
            runner: The microbatch model runner (orchestrator).
            node: The model node being executed.

        Returns:
            A (start, end) tuple for the run's event-time window, or None if it
            could not be resolved.
        """
        try:
            builder = runner.get_microbatch_builder(node)
            end = builder.build_end_time()
            start = builder.build_start_time(end)
            return start, end
        except Exception as e:
            events.fire_debug_event(
                "Failed to resolve microbatch window for node {}: {}",
                node.unique_id,
                str(e),
            )
            return None

    def _savings_summary_message(self) -> t.Optional[str]:
        if self._run_cache and self._run_cache.total_cache_hits:
            return (
                f"dbt State saved you {format_time_saved(self._run_cache.total_time_saved_ms)}"
                f" on {self._run_cache.total_cache_hits}"
                f" {'nodes' if self._run_cache.total_cache_hits != 1 else 'node'} in this job."
            )
        return None

    def _free_trial_message(self) -> t.Optional[str]:
        org = self._org_info
        if org is None or org.dimensions is None:
            return None
        if "free" in org.flags or "internal" in org.flags:
            return None
        if not org.dimensions.free_trial_end_date:
            return None

        message = ""
        if org.dimensions.in_free_trial:
            message += f"Your free trial ends on {org.dimensions.free_trial_end_date}."
        else:
            message += (
                "Your dbt State trial has ended and is no longer reducing your compute usage."
            )

        if org.is_dbt and org.account_host is not None:
            account_link = (
                f"https://{org.account_host}/settings/accounts/{org.org_id}/pages/dbt-state"
            )
            message += f" Go to {account_link} to set up billing and continue using dbt State."

        return yellow(message)


class LogTestResult(DbtLogTestResult):
    """The override for the LogTestResult event to modify the status to include the NO-OP status.

    NOTE: Don't change the name of the class. It must be exactly LogTestResult to match the corresponding protobuf message type.
    """

    def set_is_no_op(self, is_no_op: bool) -> None:
        # This is a hack to workaround the fact that the base class overrides __settattr__
        object.__setattr__(self, "_is_no_op", is_no_op)

    def get_is_no_op(self) -> bool:
        return self.__getattribute__("_is_no_op")

    def message(self) -> str:
        if self.status == "error":
            info = "ERROR"
            style = red
        elif self.status in ("reused", "pass"):
            info = "PASS"
            style = green
        elif self.status == "warn":
            info = f"WARN {self.num_failures}"
            style = yellow
        else:  # self.status == "fail":
            info = f"FAIL {self.num_failures}"
            style = red

        msg = f"{info} {self.name}"

        # This is what the whole struggle is about
        if self.get_is_no_op():
            info += f" ({NO_OP_STATUS})"
        status = style(info)

        result = format_fancy_output_line(
            msg=msg,
            status=status,
            index=self.index,
            total=self.num_models,
            execution_time=self.execution_time,
        )
        return result
