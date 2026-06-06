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
from temporalio.service import ConnectConfig, HttpConnectProxyConfig
from temporalio.service import ServiceClient as TemporalServiceClient

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
            from mistralai.workflows.core.config.config import config
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
    dump = _safe_serialize(config.model_dump())
    try:
        dump["_effective_task_queue"] = config.get_effective_task_queue()
    except Exception as exc:
        dump["_effective_task_queue"] = f"ERROR: {exc}"
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


# Pollers opened per internal Temporal worker (5 workflow + 5 activity).
_POLLERS_PER_WORKER = 10

_NOT_REGISTERED_NOTE = (
    "  Note: pass your worker module to see registered workflows and activities:\n    wf-diagnose my_package.worker"
)


def _print_workflows() -> None:
    _header("REGISTERED WORKFLOWS")
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
        rows.append(
            {
                "name": spec.name,
                "execution_timeout_seconds": spec.execution_timeout.total_seconds(),
                "enforce_determinism": spec.enforce_determinism,
                "schedules": [expr for s in spec.schedules for expr in s.cron_expressions] if spec.schedules else [],
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


def _print_activities() -> None:
    _header("REGISTERED ACTIVITIES")
    try:
        from mistralai.workflows.core.activity import get_all_temporal_activities
        from mistralai.workflows.core.rate_limiting.rate_limit import get_rate_limit
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
    rate_limit_keys: set[str] = set()
    has_sticky = False

    for fn in activities:
        params: dict[str, Any] = getattr(fn, "__wf_activity_params__", {})
        rl = get_rate_limit(fn)

        sticky = params.get("sticky_to_worker", False)
        if sticky:
            has_sticky = True

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
            effective_key = rl.key if rl.key is not None else fn.__name__
            # Sticky activities are routed to the sticky worker before the
            # rate-limit check in _create_temporal_workers (elif branch), so
            # they never create a separate rate-limit worker. Exclude them from
            # the count to avoid inflating internal workers and estimated pollers.
            if not sticky:
                rate_limit_keys.add(effective_key)
            entry["rate_limit"] = {
                "key": effective_key,
                "max_execution": rl.max_execution,
                "time_window_in_sec": rl.time_window_in_sec,
            }
        rows.append(entry)

    for line in json.dumps(rows, indent=2).splitlines():
        print(f"  {line}")

    n_rl_workers = len(rate_limit_keys)
    n_sticky_workers = 1 if has_sticky else 0
    total_workers = 1 + n_sticky_workers + n_rl_workers
    total_pollers = total_workers * _POLLERS_PER_WORKER

    print()
    print("  Summary:")
    print(f"    total activities        : {len(activities)}")
    print(f"    distinct rate-limit keys: {n_rl_workers}  {sorted(rate_limit_keys)}")
    print(f"    sticky activities       : {has_sticky}")
    print(
        f"    internal workers        : {total_workers}  (1 main + {n_sticky_workers} sticky + {n_rl_workers} rate-limited)"
    )
    print(
        f"    estimated pollers       : {total_pollers}  ({total_workers} workers × {_POLLERS_PER_WORKER} pollers each)"
    )
    if total_pollers >= 100:
        print()
        print(f"  WARNING: {total_pollers} pollers may exhaust the namespace concurrent-poller quota.")
        print("  Reduce rate-limit key cardinality: share one key across activities")
        print("  that hit the same external resource.")


async def _check_mistral_api(mistral_server: str, mistral_api_key: str | None) -> None:
    try:
        from mistralai.workflows.client import _get_async_client

        async with _get_async_client(timeout=10, api_key=mistral_api_key) as client:
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
    temporal_tls: bool,
    temporal_api_key: str | None,
    http_connect_proxy_config: HttpConnectProxyConfig | None = None,
) -> None:
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
        print(f"  [OK]   Temporal ({temporal_server}, tls={temporal_tls})")
    except Exception as exc:
        print(f"  [FAIL] Temporal ({temporal_server}, tls={temporal_tls}): {exc}")


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

    if not isinstance(config, Exception):
        temporal_api_key = config.temporal.api_key.get_secret_value() if config.temporal.api_key else mistral_api_key
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

    await _check_temporal(temporal_server, temporal_tls, temporal_api_key, http_connect_proxy_config)


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

    config, plugins = _load_sdk()

    if args.module:
        _header("IMPORTING USER MODULE")
        try:
            importlib.import_module(args.module)
            print(f"  [OK] {args.module}")
        except Exception as exc:
            print(f"  [FAIL] {args.module}: {exc}")

    _print_env_vars()
    _print_config(config)
    _print_plugins(plugins)
    _print_workflows()
    _print_activities()
    asyncio.run(_check_connectivity(config))

    print(f"\n{'=' * width}")
    print("  End of diagnostic report")
    print("=" * width)


if __name__ == "__main__":
    main()
