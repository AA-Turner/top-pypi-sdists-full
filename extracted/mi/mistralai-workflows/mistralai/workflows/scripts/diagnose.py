#!/usr/bin/env python3
import argparse
import asyncio
import importlib
import importlib.metadata
import io
import json
import os
import platform
import socket
import sys
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any

from pydantic import AliasChoices, SecretStr
from temporalio.runtime import Runtime, TelemetryConfig
from temporalio.service import ConnectConfig, HttpConnectProxyConfig, TLSConfig
from temporalio.service import ServiceClient as TemporalServiceClient

from mistralai.workflows.core.config.config import (
    AppConfig,
    WorkerConfig,
    WorkflowDecoratorConfig,
    get_workflow_decorator_config,
    resolve_worker_config,
)
from mistralai.workflows.core.definition._workflow_preparation import (
    WorkflowDecoratorMetadata,
    registered_identity,
)

_SECRET_HEADER_NAMES = {"authorization", "x-api-key", "api-key", "x-auth-token", "x-api-secret"}

_SECRET_ENV_VARS = {
    "MISTRAL_API_KEY",
    "MISTRAL_CLIENT_API_KEY",
    "TEMPORAL_API_KEY",
    "TEMPORAL_HTTP_PROXY_BASIC_AUTH_PASS",
}

# Env vars that influence worker behaviour but are not pydantic fields:
# read via os.environ.get() directly, or accessed via env_nested_delimiter paths.
# Also serves as the fallback list shown when config cannot be imported.
_SUPPLEMENTAL_ENV_VARS = {
    "CA_BUNDLE",
    "DEPLOYMENT_NAME",
    "KUBERNETES_SERVICE_HOST",
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "SERVER_URL",
    "TEMPORAL_DEPLOYMENT_NAME",
    "TEMPORAL_PAYLOAD_COMPRESSION__MIN_SIZE_BYTES",
    "TEMPORAL_PAYLOAD_ENCRYPTION__MODE",
    "TEMPORAL_PAYLOAD_OFFLOADING__ENABLED",
    "TEMPORAL_SERVER_URL",
    "TEMPORAL_WORKER_BUILD_ID",
}


def _env_vars_from_models() -> list[str]:
    """Derive relevant env var names from the pydantic config models.

    Automatically picks up new fields so this list never drifts from the actual
    config. Falls back to _SUPPLEMENTAL_ENV_VARS only if config cannot be imported.
    """
    from mistralai.workflows.core.config.config import (
        AgentConfig,
        CommonConfig,
        DeploymentLocationConfig,
        TemporalConfig,
        WorkerConfig,
        WorkerVersioningConfig,
    )

    def _from_model(cls: type) -> set[str]:
        prefix = cls.model_config.get("env_prefix", "").upper()  # type: ignore[union-attr]
        vars_: set[str] = set()
        for name, info in cls.model_fields.items():
            va = info.validation_alias
            a = info.alias
            if isinstance(va, AliasChoices):
                for choice in va.choices:
                    if isinstance(choice, str):
                        vars_.add(choice.upper())
            elif isinstance(va, str):
                vars_.add(va.upper())
            elif isinstance(a, str):
                vars_.add(a.upper())
            else:
                vars_.add(f"{prefix}{name.upper()}")
        return vars_

    vars_: set[str] = set()
    for cls in (
        CommonConfig,
        WorkerConfig,
        TemporalConfig,
        WorkerVersioningConfig,
        DeploymentLocationConfig,
        AgentConfig,
    ):
        vars_ |= _from_model(cls)
    vars_ |= _SUPPLEMENTAL_ENV_VARS
    return sorted(vars_)


def _header(title: str) -> None:
    width = 60
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}")


def _safe_serialize(obj: Any, _key: str | None = None) -> Any:
    if isinstance(obj, SecretStr):
        return "***"
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "value"):  # StrEnum / IntEnum
        return obj.value
    if isinstance(obj, dict):
        return {k: "***" if k.lower() in _SECRET_HEADER_NAMES else _safe_serialize(v, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_safe_serialize(v) for v in obj]
    return obj


def _load_sdk() -> tuple[Any, list]:
    buf = io.StringIO()
    with redirect_stdout(buf), redirect_stderr(buf):
        try:
            config = resolve_worker_config(None)
        except Exception as exc:
            return exc, []
        try:
            from mistralai.workflows.plugins._discovery import list_plugins

            plugins = list_plugins()
        except Exception:
            plugins = []
    return config, plugins


def _print_system_info() -> None:
    _header("SYSTEM")
    rows = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "hostname": socket.gethostname(),
        "cwd": os.getcwd(),
    }
    print(f"  {json.dumps(rows, indent=2)[1:-1].strip()}")


def _print_sdk_versions() -> None:
    _header("INSTALLED PACKAGES")
    packages = ["mistralai-workflows", "mistralai", "temporalio", "pydantic", "structlog", "httpx"]
    rows = {}
    for pkg in packages:
        try:
            rows[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError:
            rows[pkg] = "(not installed)"
    print(f"  {json.dumps(rows, indent=2)[1:-1].strip()}")


def _print_env_vars() -> None:
    _header("ENVIRONMENT VARIABLES")
    try:
        vars_to_check = _env_vars_from_models()
    except Exception:
        vars_to_check = sorted(_SUPPLEMENTAL_ENV_VARS | _SECRET_ENV_VARS)
    rows = {}
    for var in vars_to_check:
        val = os.environ.get(var)
        if val is not None:
            rows[var] = "*** (set)" if var in _SECRET_ENV_VARS else val
    if not rows:
        print("  (none of the relevant worker env vars are set)")
        return
    for key, val in rows.items():
        print(f"  {key}: {val}")
    not_set = [v for v in vars_to_check if v not in os.environ]
    if not_set:
        print(f"\n  not set: {', '.join(not_set)}")


def _print_config(config: Any) -> None:
    _header("WORKER CONFIG")
    if isinstance(config, Exception):
        print(f"  ERROR: {config}")
        return
    # Use the same redaction as startup logging so config.http proxy credentials are stripped from
    # the dump operators share with support (SecretStr / header names are masked by _safe_serialize).
    from mistralai.workflows.core.config.config import _loggable_config

    dump = _safe_serialize(_loggable_config(config))
    for line in json.dumps(dump, indent=2).splitlines():
        print(f"  {line}")


def _print_plugins(plugins: list) -> None:
    _header("PLUGINS")
    if not plugins:
        print("  (no plugins installed)")
        return
    rows = [{"name": p.name, "dist": p.dist_name, "version": p.dist_version} for p in plugins]
    for line in json.dumps(rows, indent=2).splitlines():
        print(f"  {line}")


_NOT_REGISTERED_NOTE = (
    "  Note: pass your worker module to see registered workflows and activities:\n    wf-diagnose my_package.worker"
)


def _print_workflows(config: AppConfig | Exception) -> None:
    _header("REGISTERED WORKFLOWS")
    if isinstance(config, AppConfig):
        worker_config: WorkerConfig | WorkflowDecoratorConfig = config.worker
    else:
        print("  Configuration failed to load: names and determinism are SDK defaults, not what a worker registers.")
        worker_config = get_workflow_decorator_config()
    try:
        from mistralai.workflows.core.definition.workflow_definition import get_workflow_definition
        from mistralai.workflows.core.workflow import get_all_registered_workflows
    except Exception as exc:
        print(f"  ERROR: could not import workflow registry: {exc}")
        return

    rows = []
    for cls in get_all_registered_workflows():
        try:
            spec = get_workflow_definition(cls)
        except Exception:
            continue
        if spec.is_technical:
            continue
        metadata = getattr(cls, "__workflows_decorator_metadata", None)
        if not isinstance(metadata, WorkflowDecoratorMetadata):
            continue
        identity = registered_identity(metadata, worker_config)
        rows.append(
            {
                "name": identity.name,
                "execution_timeout_seconds": spec.execution_timeout.total_seconds(),
                "enforce_determinism": identity.enforce_determinism,
                "signals": [s.name for s in spec.signals],
                "queries": [q.name for q in spec.queries],
                "updates": [u.name for u in spec.updates],
                "is_technical": spec.is_technical,
            }
        )

    if not rows:
        print("  (no workflows registered)")
        print(_NOT_REGISTERED_NOTE)
        return

    for line in json.dumps(rows, indent=2).splitlines():
        print(f"  {line}")


def _print_activities(config: Any) -> None:
    _header("REGISTERED ACTIVITIES")
    try:
        from mistralai.workflows.core.activity import get_all_temporal_activities
        from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import (
            check_activity_is_sticky_to_worker,
        )
        from mistralai.workflows.core.rate_limiting.rate_limit import get_rate_limit
        from mistralai.workflows.core.worker_polls import (
            distinct_rate_limit_keys,
            estimate_connection_polls,
            format_poll_warning,
            group_activities_by_worker_config,
        )
    except Exception as exc:
        print(f"  ERROR: could not import activity registry: {exc}")
        return

    all_activities = get_all_temporal_activities()
    activities = [fn for fn in all_activities if not fn.__name__.startswith("__")]
    if not activities:
        print("  (no user activities registered)")
        print(_NOT_REGISTERED_NOTE)
        return

    rows = []

    for fn in activities:
        params: dict[str, Any] = getattr(fn, "__wf_activity_params__", {})
        rl = get_rate_limit(fn)

        sticky = check_activity_is_sticky_to_worker(fn)

        entry: dict[str, Any] = {
            "name": fn.__name__,
            "start_to_close_timeout_seconds": params.get("start_to_close_timeout_seconds"),
            "heartbeat_timeout_seconds": params.get("heartbeat_timeout_seconds"),
            "retry_policy_max_attempts": params.get("retry_policy_max_attempts"),
            "retry_policy_backoff_coefficient": params.get("retry_policy_backoff_coefficient"),
            "sticky_to_worker": sticky,
            "rate_limit": None,
        }
        if rl is not None:
            entry["rate_limit"] = {
                "key": rl.key if rl.key is not None else fn.__name__,
                "max_execution": rl.max_execution,
                "time_window_in_sec": rl.time_window_in_sec,
            }
        rows.append(entry)

    for line in json.dumps(rows, indent=2).splitlines():
        print(f"  {line}")

    main_task_queue = "<main>" if isinstance(config, Exception) else config.get_effective_task_queue()
    try:
        activity_groups = group_activities_by_worker_config(
            activities, main_task_queue, f"{main_task_queue}-sticky-worker-session"
        )
    except Exception as exc:
        print(f"  ERROR: could not split activities into workers: {exc}")
        return

    n_sticky_workers = sum(1 for g in activity_groups if g.is_sticky)
    n_rl_workers = sum(1 for g in activity_groups if not g.is_main and not g.is_sticky)
    rate_limit_keys = distinct_rate_limit_keys(activity_groups)
    total_workers = len(activity_groups)

    print()
    print("  Summary:")
    print(f"    total activities        : {len(activities)}")
    print(f"    distinct rate-limit keys: {len(rate_limit_keys)}  {rate_limit_keys}")
    print(f"    rate-limit workers      : {n_rl_workers}")
    print(f"    sticky activities       : {n_sticky_workers > 0}")
    print(
        f"    internal workers        : {total_workers}  (1 main + {n_sticky_workers} sticky + {n_rl_workers} rate-limited)"
    )
    if isinstance(config, Exception):
        print("    min poll streams        : unknown (worker config unavailable)")
        return

    estimate = estimate_connection_polls(
        activity_groups,
        activity_polls_per_worker=config.worker.max_activity_task_pollers,
        workflow_polls=config.worker.max_workflow_task_pollers,
        connection_stream_limit=config.worker.connection_stream_limit,
    )
    print(
        f"    min poll streams        : {estimate.total_polls}  "
        f"({total_workers} workers × {estimate.activity_polls_per_worker} activity + "
        f"1 main × {estimate.main_workflow_polls} workflow; respond/heartbeat streams not included)"
    )
    if estimate.headroom is None:
        print("    stream headroom         : no connection stream limit configured")
    else:
        print(f"    stream headroom         : {estimate.headroom} of {estimate.connection_stream_limit}")
    if poll_warning := format_poll_warning(estimate):
        print()
        print(f"  WARNING: {poll_warning}")


async def _check_mistral_api(mistral_server: str, mistral_api_key: str | None) -> None:
    try:
        from mistralai.workflows.client import _get_async_client
        from mistralai.workflows.core.auth import RunAs

        async with _get_async_client(timeout=10, api_key=mistral_api_key, run_as=RunAs.DEPLOYMENT) as client:
            resp = await client.get(f"{mistral_server}/v1/models")
        status = "OK" if resp.status_code < 500 else "FAIL"
        print(f"  [{status}]   Mistral API ({mistral_server}): HTTP {resp.status_code}")
    except Exception as exc:
        print(f"  [FAIL] Mistral API ({mistral_server}): {exc}")


async def _check_whoami(mistral_server: str, mistral_api_key: str | None) -> Any:
    try:
        from mistralai.workflows.client import translate_model
        from mistralai.workflows.core.worker_client import get_worker_client
        from mistralai.workflows.protocol.v1.worker import WorkerInfo

        async with get_worker_client(base_url=mistral_server, api_key=mistral_api_key) as wc:
            result = await wc.whoami_async()
            whoami = translate_model(WorkerInfo, result)
        for line in json.dumps(_safe_serialize(whoami.model_dump()), indent=2).splitlines():
            print(f"  {line}")
        return whoami
    except Exception as exc:
        print(f"  [FAIL] /whoami: {exc}")
        return None


async def _check_temporal(
    temporal_server: str,
    temporal_tls: bool | TLSConfig,
    temporal_api_key: str | None,
    http_connect_proxy_config: HttpConnectProxyConfig | None = None,
) -> None:
    # A TLSConfig repr would dump the whole PEM into the report, so label what it carries instead
    # (it can hold a pinned root CA, an mTLS client identity, or both).
    if isinstance(temporal_tls, TLSConfig):
        carried = [
            label
            for label, present in (("pinned-ca", temporal_tls.server_root_ca_cert), ("mtls", temporal_tls.client_cert))
            if present
        ]
        tls_label = "+".join(carried) or "on"
    else:
        tls_label = str(bool(temporal_tls))
    try:
        await TemporalServiceClient.connect(
            ConnectConfig(
                target_host=temporal_server,
                api_key=temporal_api_key,
                tls=temporal_tls,
                runtime=Runtime(telemetry=TelemetryConfig()),
                http_connect_proxy_config=http_connect_proxy_config,
            )
        )
        print(f"  [OK]   Temporal ({temporal_server}, tls={tls_label})")
    except Exception as exc:
        print(f"  [FAIL] Temporal ({temporal_server}, tls={tls_label}): {exc}")


async def _check_connectivity(config: Any) -> None:
    if isinstance(config, Exception):
        mistral_server = os.environ.get("SERVER_URL", "https://api.mistral.ai")
        mistral_api_key = os.environ.get("MISTRAL_API_KEY")
    else:
        mistral_server = config.worker.server_url
        mistral_api_key = config.common.mistral_api_key.get_secret_value() if config.common.mistral_api_key else None

    _header("WHOAMI")
    await _check_mistral_api(mistral_server, mistral_api_key)
    whoami = await _check_whoami(mistral_server, mistral_api_key)

    _header("CONNECTIVITY CHECKS")
    if whoami is not None:
        from mistralai.workflows.core.config.config_discovery import normalize_temporal_url

        temporal_server = normalize_temporal_url(whoami.scheduler_url)
        temporal_tls = whoami.tls
    elif not isinstance(config, Exception):
        temporal_server = config.temporal.server_url
        temporal_tls = config.temporal.tls
    else:
        temporal_server = os.environ.get("TEMPORAL_SERVER_URL", "localhost:7233")
        temporal_tls = False

    temporal_tls_setting: bool | TLSConfig = temporal_tls
    tls_failed = False
    if not isinstance(config, Exception):
        temporal_api_key = config.temporal.api_key.get_secret_value() if config.temporal.api_key else mistral_api_key
        if config.temporal.tls_server_root_ca_cert_path or config.common.mtls_client_identity is not None:
            from mistralai.workflows.core.config.config import adopt_remote_default
            from mistralai.workflows.core.temporal.temporal_client import _resolve_temporal_tls

            # Diagnose never calls apply_worker_runtime_config(), so adopt whoami's flag the way the
            # worker does: local configuration wins if it set `tls`, otherwise whoami supplies it.
            adopt_remote_default(config.temporal, "tls", temporal_tls)
            try:
                temporal_tls_setting = _resolve_temporal_tls(
                    config.temporal.tls,
                    config.temporal.tls_server_root_ca_cert_path,
                    config.common.mtls_client_identity,
                )
            except Exception as exc:
                print(f"  [FAIL] Temporal TLS setup: {exc}")
                tls_failed = True
        http_connect_proxy_config: HttpConnectProxyConfig | None = None
        if config.temporal.http_proxy_target_host:
            from mistralai.workflows.core.temporal.temporal_client import _get_proxy_basic_auth

            basic_auth = _get_proxy_basic_auth(
                config.temporal.http_proxy_basic_auth_user,
                config.temporal.http_proxy_basic_auth_pass,
            )
            http_connect_proxy_config = HttpConnectProxyConfig(
                target_host=config.temporal.http_proxy_target_host,
                basic_auth=basic_auth,
            )
    else:
        temporal_api_key = os.environ.get("TEMPORAL_API_KEY") or mistral_api_key
        http_connect_proxy_config = None

    if tls_failed:
        # Connecting anyway would use the default trust roots and could report [OK] for a
        # configuration a worker refuses to start with.
        print(f"  [SKIP] Temporal ({temporal_server}): unusable TLS setup, a worker would fail to start")
        return

    await _check_temporal(temporal_server, temporal_tls_setting, temporal_api_key, http_connect_proxy_config)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wf-diagnose",
        description="mistralai-workflows diagnostic tool",
    )
    parser.add_argument(
        "module",
        nargs="?",
        help="Python module to import before running the diagnostic (e.g. my_package.worker). "
        "Import triggers @workflow.define and @activity decorators, populating the registries.",
    )
    args = parser.parse_args()

    width = 60
    print("=" * width)
    print("  mistralai-workflows diagnostic report")
    print("=" * width)

    _print_system_info()
    _print_sdk_versions()

    # The user module may load a dotenv file or set environment variables, so import it before
    # resolving configuration, as run_worker would.
    if args.module:
        _header("IMPORTING USER MODULE")
        try:
            importlib.import_module(args.module)
            print(f"  [OK] {args.module}")
        except Exception as exc:
            print(f"  [FAIL] {args.module}: {exc}")

    config, plugins = _load_sdk()

    _print_env_vars()
    _print_config(config)
    _print_plugins(plugins)
    _print_workflows(config)
    _print_activities(config)
    asyncio.run(_check_connectivity(config))

    print(f"\n{'=' * width}")
    print("  End of diagnostic report")
    print("=" * width)


if __name__ == "__main__":
    main()
