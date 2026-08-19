# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# manage ray cluster setup

"""
Why?
Setting up a cluster involves a lot of state and resource management
for different users the resources created during cluster setup can
include:
- Kuberay Cluster
- Portforwarding Server
- packaged zips
- ray context initialization

There are three issues:
1. We want to make sure the api for setting up a cluster is simple, which
means everything should be in a single place instead of requiring a bunch
of different context managers to be created. Consider
```python
with(
    KuberayCluster(),
    PortforwardingServer(),
    PackagedZips(),
    RayContextInit()
):
    # do something with the cluster
)
```
We do not want to require the user to do this. However if we keep everything
in a single context manager a second issue arises.

2. We want to make sure that the resources are cleaned up when the context
manager exits, that includes when resource setup fails. Doing this in a single
context manager is difficult. Consider
```python
def __enter__(self):
    try:
        do_kuberay_cluster_setup()
    except Exception as e:
        # cleanup resources
        raise e

    try:
        start_portforwarding_server()
    except Exception as e:
        # cleanup resources
        raise e

    ...

def __exit__(self, exc_type, exc_value, traceback):
    try:
        shutdown_ray_context()
    except Exception as e:
        # cleanup resources
        raise e

    try:
        shutdown_portforwarding_server()
    except Exception as e:
        # cleanup resources
        raise e

    ...
```

3. Users may want start at any one of the following points:
  - only has k8s + kuberay installed
  - has a ray cluster
  - has dependency already setup in the ray cluster
  We need a way to allow users to start at any one of these points

To solve the first two issues we create a setup_cluster func, to help with
entering and exiting the context manager
```python
with ray_cluster(
    cluster_settings={...},
    use_portforwarding=True,
    delete_packaged_zips=False,
    ...
) as m:
    # do something with the cluster
```
As long as the manager deligates the setup and teardown error handling
to contextlib.ExitStack, we can be sure that all resources are cleaned up
correctly.

The third issue is solved by allowing the user to pass in a ray address
to the setup_cluster function.
"""

import base64
import contextlib
import json
import logging
import os
import re
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, cast

import ray
from emoji import emojize
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

import geneva
from geneva import telemetry
from geneva._context import LocalRayContext
from geneva.manifest.mgr import GenevaManifest
from geneva.packager.autodetect import upload_local_env
from geneva.packager.uploader import Uploader
from geneva.runners.ray._portforward import PortForward
from geneva.runners.ray.raycluster import _DEFAULT_LANCE_LOG, ExitMode, RayCluster

if TYPE_CHECKING:
    from kubernetes import client

_LOG = logging.getLogger(__name__)

# Default number of retry attempts for ray.init() connection failures
# Can be overridden via GENEVA_RAY_INIT_MAX_RETRIES environment variable
RAY_INIT_MAX_RETRIES = int(os.environ.get("GENEVA_RAY_INIT_MAX_RETRIES", "5"))

# Private PyPI indexes that carry Geneva and its Lance/LanceDB dependencies.
_EXTRA_PIP_INDEX_URLS = [
    "https://pypi.fury.io/lancedb/",
    "https://pypi.fury.io/lance-format/",
]


def _force_ray_cleanup() -> None:
    """Best-effort cleanup of stale Ray client / driver state.

    Each step is independently guarded so a failure in one does not
    prevent the others from running.

    When a cluster is deleted the gRPC channel dies.  The internal
    ``_ClientContext.disconnect()`` then raises before it can reset
    ``client_worker = None`` and before ``RayAPIStub.disconnect()``
    can execute ``_all_contexts = set()``.  This leaves two pieces
    of stale state that break the *next* ``ray.init()``:

    1. ``_default_context.client_worker is not None`` →
       "ray.init() called, but ray client is already connected"
    2. ``len(_all_contexts) > 0`` →
       "The client has already connected … allow_multiple=True"

    After the graceful disconnect attempt we forcibly reset both.
    """
    with contextlib.suppress(Exception):
        ray.util.client.ray.disconnect()  # type: ignore[attr-defined]
    # Forcibly reset internal state that disconnect() may have failed
    # to clear (e.g. gRPC close raised on a dead channel).
    with contextlib.suppress(Exception):
        ctx = ray.util.client._default_context  # type: ignore[attr-defined]
        ctx.client_worker = None
        ctx._connected_with_init = False
    with contextlib.suppress(Exception), ray.util.client._lock:  # type: ignore[attr-defined]
        ray.util.client._all_contexts = set()  # type: ignore[attr-defined]
    with contextlib.suppress(Exception):
        if ray.is_initialized():
            ray.shutdown()


def _get_head_pod_diagnostics(cluster: RayCluster | None) -> str:
    """Query the head pod and return container-level diagnostics."""
    if cluster is None:
        return ""
    try:
        pod_name = cluster._get_podname()
        pod = cast(
            "client.V1Pod",
            cluster.clients.core_api.read_namespaced_pod(
                name=pod_name, namespace=cluster.namespace
            ),
        )
        parts: list[str] = []
        for cs in pod.status.container_statuses or []:  # type: ignore[union-attr]
            state = cs.state
            if state is None:
                continue
            if state.waiting and state.waiting.reason:
                parts.append(f"container '{cs.name}': waiting ({state.waiting.reason})")
            if state.terminated:
                parts.append(
                    f"container '{cs.name}': terminated "
                    f"(reason={state.terminated.reason}, "
                    f"exit_code={state.terminated.exit_code})"
                )
            last = cs.last_state
            if last and last.terminated:
                t = last.terminated
                parts.append(
                    f"container '{cs.name}': last terminated "
                    f"(reason={t.reason}, exit_code={t.exit_code})"
                )
        if parts:
            return " | Pod diagnostics: " + "; ".join(parts)
    except Exception:
        _LOG.debug("Failed to fetch head pod diagnostics", exc_info=True)
    return ""


class _GrpcModule(Protocol):
    def ssl_channel_credentials(
        self, root_certificates: bytes | None = None
    ) -> Any: ...


def _needs_tls_setup(addr: str | None, ray_init_kwargs: dict[str, Any] | None) -> bool:
    """Return True when the Ray connection needs TLS credential setup.

    Triggers when:
    - ``_geneva_tls_ca_cert`` is present in ray_init_kwargs
    - explicit env var ``GENEVA_RAY_CLIENT_SECURE=1|true|yes``
    - explicit ``{"_geneva_secure_client": True}`` in ray_init_kwargs
    - any external Ray address ending in ``:443``

    Any explicit ``_geneva_tls_ca_cert`` value routes through the TLS setup
    path, where Geneva validates that it is a non-empty file path string.
    """
    if not addr or not addr.startswith("ray://"):
        return False

    if (
        ray_init_kwargs is not None
        and "_geneva_tls_ca_cert" in ray_init_kwargs
        and ray_init_kwargs["_geneva_tls_ca_cert"] is not None
    ):
        return True

    if os.environ.get("GENEVA_RAY_CLIENT_SECURE", "").lower() in {
        "1",
        "true",
        "yes",
    }:
        return True

    if ray_init_kwargs and ray_init_kwargs.get("_geneva_secure_client") is True:
        return True

    return addr.rsplit(":", 1)[-1] == "443"


def _normalize_tls_ca_cert_path(ca_cert_path: object) -> str | None:
    """Normalize a raw `_geneva_tls_ca_cert` value into a usable path."""
    if ca_cert_path is None:
        return None

    if not isinstance(ca_cert_path, str):
        raise ValueError("_geneva_tls_ca_cert must be a file path string when provided")

    if ca_cert_path == "":
        raise ValueError(
            "_geneva_tls_ca_cert must be a non-empty file path string when provided"
        )

    return ca_cert_path


def _import_grpc() -> _GrpcModule:
    try:
        import grpc
    except ImportError as exc:
        raise RuntimeError(
            "TLS-enabled Ray client connections require `grpcio` to be installed"
        ) from exc

    return grpc


def _setup_tls_and_init(addr: str, init_kwargs: dict[str, Any]) -> None:
    """Set up TLS credentials and connect via ray.init().

    Uses ``ray.init()`` directly so ``py_modules`` remain part of the
    runtime environment and are uploaded for Ray Client actor deserialization.

    TLS CA certificate is configured via:
    - ``_geneva_tls_ca_cert`` in ray_init_kwargs (path to CA cert file)
    - Falls back to ``_credentials`` (grpc.ChannelCredentials object)
    - Otherwise uses the system trust store

    When both ``_geneva_tls_ca_cert`` and ``_credentials`` are provided,
    the CA cert takes precedence and Geneva rebuilds TLS credentials from it.
    """
    clean_kwargs = dict(init_kwargs)
    connect_addr = clean_kwargs.get("address")
    if connect_addr != addr:
        raise ValueError(
            "Mismatched Ray TLS init addresses: "
            f"addr={addr!r}, init_kwargs.address={connect_addr!r}"
        )

    ca_cert_path = _normalize_tls_ca_cert_path(
        clean_kwargs.pop("_geneva_tls_ca_cert", None)
    )
    credentials = clean_kwargs.pop("_credentials", None)
    clean_kwargs.pop("_geneva_secure_client", None)

    if ca_cert_path:
        if credentials is not None:
            _LOG.warning(
                "Both _geneva_tls_ca_cert and _credentials were provided; "
                "rebuilding Ray TLS credentials from _geneva_tls_ca_cert"
            )
        _LOG.debug(
            "Using CA cert from _geneva_tls_ca_cert for Ray TLS: %s",
            ca_cert_path,
        )
        try:
            ca_cert_data = Path(ca_cert_path).read_bytes()
        except OSError as exc:
            raise ValueError(
                "Failed to read CA cert file at "
                f"_geneva_tls_ca_cert={ca_cert_path}: {exc}"
            ) from exc

        grpc = _import_grpc()
        credentials = grpc.ssl_channel_credentials(root_certificates=ca_cert_data)
    elif credentials is not None:
        _LOG.info(
            "Using explicit Ray TLS credentials: %s",
            type(credentials).__name__,
        )
    else:
        _LOG.info(
            "No CA cert or credentials provided for Ray TLS; using system trust store"
        )
        grpc = _import_grpc()
        credentials = grpc.ssl_channel_credentials()

    clean_kwargs["_credentials"] = credentials

    _LOG.info("Calling ray.init(address=%s) with TLS", addr)
    ray.init(**clean_kwargs)
    _LOG.info("ray.init() succeeded with TLS")


def _align_uv_project_environment() -> None:
    """Point uv at the active venv so its workers stop warning about VIRTUAL_ENV.

    Ray re-invokes ``uv run`` for workers from its own session directory, where
    uv resolves the project environment as ``<session>/.venv`` -- different from
    the absolute ``VIRTUAL_ENV`` of the real venv, which uv then warns about and
    ignores. Setting ``UV_PROJECT_ENVIRONMENT`` to ``VIRTUAL_ENV`` makes uv use
    the intended environment, resolving the cause rather than hiding the message.

    No-op when no venv is active or when ``UV_PROJECT_ENVIRONMENT`` is already
    set by the caller.
    """
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        os.environ.setdefault("UV_PROJECT_ENVIRONMENT", venv)


@contextlib.contextmanager
def init_ray(
    *,
    addr: str | None,
    zips: list[list[str]],
    pip: list[str] | None = None,
    requirements_path: str | None = None,
    conda: dict[str, Any] | None = None,
    conda_environment_path: str | None = None,
    pip_extra_index_urls: list[str] | None = None,
    local: bool = False,
    py_modules: list | None = None,
    extra_env: dict[str, str] | None = None,
    log_to_driver: bool = False,
    logging_level=logging.INFO,
    ray_init_kwargs: dict | None = None,
    uploader: Uploader | None = None,
    zip_namespace: dict[str, Any] | None = None,
    cluster: RayCluster | None = None,
) -> Generator[None, None, None]:
    # Local mode with Ray already initialized (e.g. by test fixture): just yield.
    # Context management is handled by LocalRayContext.__enter__/__exit__.
    if local and ray.is_initialized():
        yield
        return

    if ray.is_initialized() or ray.util.client.num_connected_contexts() > 0:  # type: ignore[attr-defined]
        # Stale Ray state from a previous session whose cleanup failed.
        # Force-clean instead of aborting so sequential cluster uses
        # (e.g. back-to-back tests) can proceed.
        _LOG.warning(
            "Ray is already initialized (likely stale state from a prior "
            "session). Forcing shutdown before starting new cluster."
        )
        _force_ray_cleanup()

    if pip is not None and len(pip) > 0 and requirements_path is not None:
        raise ValueError("Cannot set both pip and requirements_path")
    if conda is not None and len(conda) > 0 and conda_environment_path is not None:
        raise ValueError("Cannot set both conda and conda_environment_path")
    ray_conda: str | dict[str, Any] | None = (
        conda_environment_path if conda_environment_path else (conda if conda else None)
    )

    # Install geneva via pip so workers get its transitive dependencies.
    # Geneva's code is shipped as a py_module (which takes precedence on import),
    # but the py_module doesn't carry deps — pip does. Pinning the exact version
    # ensures the installed deps match the running environment.
    #
    # When requirements_path is provided we inline it as a list so we can prepend
    # the geneva pin; Ray only accepts pip as a list OR a path, not both.
    # -r include directives reference local files that workers can't access, so
    # we raise early with a clear message rather than letting pip fail confusingly.
    #
    # When conda manages the environment we leave it alone — the user is
    # responsible for ensuring Geneva's deps are present.
    if ray_conda is None and requirements_path is None:
        pip = [f"geneva=={geneva.__version__}", *(pip or [])]
    elif ray_conda is None and requirements_path is not None:
        reqs_lines = Path(requirements_path).read_text().splitlines()
        user_reqs = []
        for ln in reqs_lines:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            if re.match(r"-r\S*|--requirement(\s|=)", ln):
                raise ValueError(
                    f"requirements_path contains an -r include directive ({ln!r}). "
                    "-r includes reference local files that Ray workers cannot "
                    "access. Flatten all requirements into a single file first."
                )
            user_reqs.append(ln)
        pip = [f"geneva=={geneva.__version__}", *user_reqs]
        requirements_path = None

    # Local workers share the driver's environment, so pip installs via
    # runtime_env are unnecessary and incompatible with `uv run`.
    ray_pip: str | list[str] | None = (
        None
        if local
        else (requirements_path if requirements_path else (pip if pip else None))
    )

    # Build payload with namespace info for downloading zips
    payload: dict[str, Any] = {"zips": zips}
    if zip_namespace is not None:
        payload["namespace"] = zip_namespace
    elif uploader is not None:
        ns = uploader.namespace_config
        if ns is not None and ns.namespace_client_impl is not None:
            payload["namespace"] = {
                "impl": ns.namespace_client_impl,
                "properties": ns.namespace_client_properties,
                "table_id": uploader.table_id,
            }
    geneva_zip_payload = base64.b64encode(json.dumps(payload).encode()).decode()

    # Only upload geneva as a py_module; pyarrow is installed on workers via
    # pip and is too large (~130 MiB) to upload through Ray's GCS object store.
    default_modules = [geneva]
    # Use explicit None check so empty list [] can skip py_modules upload
    # (useful when zips already contain the modules)
    if py_modules is None:
        py_modules = default_modules

    # modules result in "TypeError: cannot pickle 'module' object" in local ray
    modules = [] if local else py_modules

    all_indexes = _EXTRA_PIP_INDEX_URLS + (pip_extra_index_urls or [])
    pip_extra_index_url = " ".join(all_indexes)

    # Suppress lance DataReplacement warning unless user explicitly sets LANCE_LOG
    if "LANCE_LOG" not in (extra_env or {}):
        extra_env = {
            **(extra_env or {}),
            "LANCE_LOG": _DEFAULT_LANCE_LOG,
        }
    else:
        _LOG.info(
            "LANCE_LOG is set; to suppress DataReplacement warnings, "
            "add 'lance::dataset::transaction=error' to your LANCE_LOG value"
        )

    # Suppress Pydantic "protected namespace model_" warnings from third-party
    # libs (e.g. lancedb embeddings: SigLipEmbeddings, ColPaliEmbeddings) unless
    # user explicitly sets PYTHONWARNINGS.
    if "PYTHONWARNINGS" not in (extra_env or {}):
        extra_env = {
            **(extra_env or {}),
            "PYTHONWARNINGS": "ignore::UserWarning:pydantic._internal._fields",
        }

    # Pass Azure storage account name to workers (needed for az:// URI handling).
    # AZURE_STORAGE_ACCOUNT_KEY and AZURE_STORAGE_TOKEN are not implicitly
    # passed; workers use workload identity (DefaultAzureCredential).
    azure_account = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME") or os.environ.get(
        "AZURE_STORAGE_ACCOUNT"
    )
    if azure_account and "AZURE_STORAGE_ACCOUNT_NAME" not in (extra_env or {}):
        extra_env = {**(extra_env or {}), "AZURE_STORAGE_ACCOUNT_NAME": azure_account}

    # Extend GCS temporary-reference TTL for runtime_env packages.
    # Default 600s can be too short when cloud providers (especially
    # Azure AKS) take >10 min to provision worker nodes.
    os.environ.setdefault("RAY_RUNTIME_ENV_TEMPORARY_REFERENCE_EXPIRATION_S", "1800")

    _align_uv_project_environment()

    # Forward OTLP telemetry config from the driver process into the Ray worker
    telemetry_env = {
        key: os.environ[key]
        for key in (
            "LANCEDB_OTEL_COLLECTOR_URL",
            telemetry.LANCE_METRICS_ENV,
            "LANCE_OBJECT_STORE_METRICS_LABEL",
        )
        if key in os.environ
    }

    runtime_env = {
        "env_vars": {
            "PIP_EXTRA_INDEX_URL": pip_extra_index_url,
            "GENEVA_ZIPS": geneva_zip_payload,
            # Workers init telemetry at `import geneva` (see geneva/__init__.py).
            # An env var, not worker_process_setup_hook: Ray Client doesn't
            # export the hook.
            telemetry.TELEMETRY_INIT_ON_IMPORT_ENV: "1",
            **telemetry_env,
            **(extra_env or {}),
        },
        **(
            {"pip": ray_pip} if ray_pip else {}
        ),  # Ray: list[str] or str (requirements.txt path)
        **(
            {"conda": ray_conda} if ray_conda else {}
        ),  # Ray: dict[str, str] or str (environment.yml path)
    }
    if modules:
        runtime_env.update(py_modules=modules)

    # Merge runtime_env from ray_init_kwargs if provided
    # Note on Ray runtime_env constraints:
    # - conda and pip cannot be specified simultaneously
    # - container works alone or only with config/env_vars
    # If user creates invalid combinations (e.g., Geneva sets pip via parameter
    # and user sets conda via ray_init_kwargs), Ray will validate and raise an
    # error. Users can override by explicitly setting conflicting fields to None.
    if ray_init_kwargs and "runtime_env" in ray_init_kwargs:
        # Shallow-copy both dicts so we never mutate the caller's input.
        user_runtime_env = dict(ray_init_kwargs["runtime_env"] or {})
        ray_init_kwargs = {
            k: v for k, v in ray_init_kwargs.items() if k != "runtime_env"
        }

        # Merge env_vars
        if "env_vars" in user_runtime_env:
            runtime_env["env_vars"] = {
                **runtime_env["env_vars"],
                **user_runtime_env["env_vars"],
            }
            user_runtime_env = {
                k: v for k, v in user_runtime_env.items() if k != "env_vars"
            }
        # Merge pip lists: assembled pip first, then user packages so they can
        # override versions. Explicit None clears pip entirely (e.g. user is
        # switching to conda via ray_init_kwargs). Other runtime_env keys are
        # user-wins.
        if "pip" in user_runtime_env:
            user_pip = user_runtime_env.pop("pip")
            if user_pip is None:
                runtime_env.pop("pip", None)
            else:
                assembled_pip = runtime_env.get("pip") or []
                if isinstance(assembled_pip, str):
                    # defensive: caller manually set runtime_env["pip"] to a path
                    # string before we got here; can't splice a list into a str,
                    # so let user override win
                    runtime_env["pip"] = user_pip
                elif isinstance(user_pip, str):
                    # user supplied a requirements path — can't merge, user wins
                    runtime_env["pip"] = user_pip
                else:
                    runtime_env["pip"] = [*assembled_pip, *user_pip]
        runtime_env = {**runtime_env, **user_runtime_env}

    _LOG.debug(f"initializing ray at {addr or 'local'} with {runtime_env=}")

    if ray_init_kwargs and "address" in ray_init_kwargs:
        if ray_init_kwargs["address"] != addr:
            raise ValueError(
                "ray_init_kwargs['address'] must match `addr` when both are provided"
            )
        ray_init_kwargs = {k: v for k, v in ray_init_kwargs.items() if k != "address"}

    # Build ray.init kwargs
    init_kwargs = {
        "address": addr,
        "runtime_env": runtime_env,
        "log_to_driver": log_to_driver,
        "logging_level": logging_level,
        **(ray_init_kwargs or {}),
    }

    # Local Ray has no head/worker split. Advertise GENEVA_RAY_HEAD on
    # the single node so tasks using ``head_pin_options()`` (pipeline
    # drivers) can still be scheduled in unit tests and local development.
    # On kuberay this resource is advertised by the head pod's
    # rayStartParams instead (raycluster.py).
    if local:
        from geneva.utils.ray import GENEVA_RAY_HEAD

        user_resources = init_kwargs.get("resources") or {}
        init_kwargs["resources"] = {GENEVA_RAY_HEAD: 1, **user_resources}

    # Define tenacity-decorated inner function for retrying ray.init()
    # Retries on transient connection errors with exponential backoff + jitter
    @retry(
        retry=retry_if_exception_type((ConnectionError, TimeoutError, OSError)),
        stop=stop_after_attempt(RAY_INIT_MAX_RETRIES),
        wait=wait_exponential_jitter(initial=1, max=30),
        before_sleep=before_sleep_log(_LOG, logging.WARNING),
        reraise=True,
    )
    def _ray_init_with_retry() -> None:
        # Clean up stale state from a previous failed attempt so that
        # ray.init() starts fresh: re-uploads runtime_env packages to
        # GCS (the old ones may have been GC'd when the prior client
        # disconnected) and avoids "already connected" errors.
        _force_ray_cleanup()
        _LOG.warning(
            "Initializing Ray cluster. This could take a few minutes, especially if "
            "there are lots of dependencies to install."
        )
        if _needs_tls_setup(addr, ray_init_kwargs):
            assert addr is not None
            _setup_tls_and_init(addr, init_kwargs)
        else:
            ray.init(**init_kwargs)

    try:
        with telemetry.span("init_ray", {"ray_address": addr or ""}):
            telemetry.add_span_event("cluster-init.started")
            _ray_init_with_retry()
            telemetry.add_span_event("cluster-init.provisioned")
        yield
    except ConnectionError as e:
        pod_diag = _get_head_pod_diagnostics(cluster)
        raise RuntimeError(
            "Geneva was unable to connect to the Ray head. "
            "The Ray head probably failed to start. Please ensure "
            "the head image matches the node architecture. "
            f"Ray cluster: {cluster.definition if cluster else None}"
            f"{pod_diag}"
        ) from e
    finally:
        _force_ray_cleanup()


@contextlib.contextmanager
def ray_cluster(
    addr: str | None = None,
    *,
    use_portforwarding: bool = True,
    zip_output_dir: Path | str | None = None,
    uploader: Uploader | None = None,
    delete_local_packaged_zips: bool = False,
    skip_site_packages: bool = True,
    pip: list[str] | None = None,
    requirements_path: str | None = None,
    conda: dict[str, Any] | None = None,
    conda_environment_path: str | None = None,
    ray_cluster: RayCluster | None = None,
    manifest: GenevaManifest | None = None,
    local: bool = False,
    extra_env: dict[str, str] | None = None,
    log_to_driver: bool = False,
    logging_level=logging.INFO,
    ray_init_kwargs: dict | None = None,
    zip_namespace: dict[str, Any] | None = None,
    **ray_cluster_kwargs,
) -> Generator[None, None, None]:
    """
    Context manager for setting up a Ray cluster.

    Args:
        addr: The address of the Ray cluster. If None, a new cluster will be
            created.
        use_portforwarding: Whether to use port forwarding for the cluster.
            Defaults to True.
        zip_output_dir: The output directory for the zip files. If None, a
            temporary directory will be used.
        uploader: The uploader to use for uploading the zip files. If None,
            the default uploader will be used.
        delete_local_packaged_zips: Whether to delete the local zip files
            after uploading them. Defaults to False.
        skip_site_packages: Do not include files in site-packages in the manifest.
            Defaults to True (meaning automatic dependency shipping from site
            packages will be skipped). Overridden if a manifest is provided.
        pip: A list of pip packages to install in the Ray cluster. If None,
            no pip packages will be installed.
        requirements_path: Path to a requirements.txt file. Mutually exclusive
            with pip, conda, and conda_environment_path; passed through to Ray
            runtime_env as "pip".
        conda: A dict of conda dependencies. Mutually exclusive with
            pip, requirements_path, and conda_environment_path; passed through
            to Ray runtime_env as "conda".
        conda_environment_path: Path to a conda environment.yml file. Mutually
            exclusive with conda, pip, and requirements_path; passed through to
            Ray runtime_env as "conda".
        ray_cluster: An optional RayCluster. If provided, the ray_cluster_kwargs
            will be ignored.
        manifest: A GenevaManifest. If provided, the skip_site_packages, pip,
            requirements_path, and conda, and conda_environment_path parameters
            will be ignored.
        local: If set, will use a local Ray cluster using ray.init()
        extra_env: Extra environment variables to pass to Ray workers via
            runtime_env. These override manifest env_vars on conflict.
        ray_init_kwargs: Arbitrary kwargs to pass to ray.init(). These will be
            merged with kwargs from the RayCluster (if any), with these taking
            precedence. Can be used to pass runtime_env, namespace, etc.
        zip_namespace: Namespace metadata for downloading manifest zips through
            LanceFileSession when the manifest was uploaded earlier.
        **ray_cluster_kwargs: Additional arguments to pass to the RayCluster
            constructor.

    Environment variable precedence (highest wins):
        1. ray_init_kwargs runtime_env env_vars
        2. extra_env (caller)
        3. manifest env_vars (AI engineer)
        4. cluster env_vars (infra engineer, K8s container spec)

    Manifest env_vars override cluster env_vars for Ray worker processes
    because they are injected via Ray's runtime_env, which takes precedence
    over the container-level environment.

    If addr is provided and use_portforwarding is True, a ValueError will be
    raised. This is because port forwarding is not supported for existing
    clusters.

    Similarly, if addr is None and ray_cluster_kwargs are provided, a
    ValueError will be raised.
    """
    if addr is not None and ray_cluster_kwargs:
        raise ValueError(
            "Cannot provide both addr and ray_cluster_kwargs. "
            "If addr is provided, use_portforwarding will be ignored."
        )

    # TODO: allow inspecting an existing RayCluster in k8s and allow
    # port forwarding to it
    # https://linear.app/lancedb/issue/GEN-23/define-geneva-ray-hookup-api-and-document
    if addr is not None and use_portforwarding:
        raise ValueError(
            "Cannot use port forwarding with an existing cluster. "
            "If addr is provided, use_portforwarding will be ignored."
        )

    cluster = None
    with contextlib.ExitStack() as stack:
        # Extract ray_init_kwargs from RayCluster if available
        cluster_ray_init_kwargs = {}
        if addr is None:
            if local:
                _LOG.info("starting local ray cluster")
                # Enter LocalRayContext for symmetric context management
                stack.enter_context(LocalRayContext())
            else:
                _LOG.debug(f"creating ray cluster {ray_cluster_kwargs=}")
                cluster = (
                    ray_cluster
                    if ray_cluster is not None
                    else RayCluster(**ray_cluster_kwargs)
                )
                # Attach manifest to cluster for job tracking
                if manifest is not None:
                    cluster.manifest = manifest
                # Extract ray_init_kwargs from the cluster
                cluster_ray_init_kwargs = cluster.ray_init_kwargs or {}
                ray_ip = stack.enter_context(cluster)
                ray_port = "10001"
                if use_portforwarding:
                    pf = stack.enter_context(PortForward.to_head_node(cluster))
                    ray_ip = "localhost"
                    ray_port = pf.local_port

                    ui_pf = PortForward.to_ui(cluster)
                    if ui_pf:
                        # start a portforward to the remote UI if it is
                        # deployed and running
                        ui_pf_ctx = stack.enter_context(ui_pf)

                        # todo: can we deep link with db url populated?
                        _LOG.info(
                            emojize(
                                f"   :sparkles: Geneva UI is available "
                                f"at http://localhost:{ui_pf_ctx.local_port}"
                            )
                        )

                addr = f"ray://{ray_ip}:{ray_port}"
                _LOG.info(f"connecting to ray cluster at {addr}")

        py_modules = None
        manifest_pip_extra_index_urls: list[str] | None = None
        if manifest is not None:
            # use a previously defined manifest
            zips = manifest.zips
            manifest_pip = manifest.pip
            manifest_requirements_path = manifest.requirements_path
            manifest_conda = manifest.conda
            manifest_conda_environment_path = manifest.conda_environment_path
            manifest_pip_extra_index_urls = manifest.pip_extra_index_urls
            # Combine manifest py_modules with geneva (always needed on workers).
            # pyarrow is installed via pip, not uploaded as a py_module.
            py_modules = [geneva] + (manifest.py_modules or [])

            # Merge manifest env_vars into extra_env.
            # Precedence (highest wins):
            #   ray_init_kwargs > caller extra_env > manifest env_vars
            #   > cluster env_vars
            # Manifest (AI engineer) overrides cluster (infra engineer) env vars
            # for Ray workers via runtime_env.
            if manifest.env_vars:
                extra_env = {**manifest.env_vars, **(extra_env or {})}

        else:
            # build an ad-hoc manifest
            manifest_pip = pip
            manifest_requirements_path = requirements_path
            manifest_conda = conda
            manifest_conda_environment_path = conda_environment_path
            zips = (
                stack.enter_context(
                    upload_local_env(
                        zip_output_dir=zip_output_dir,
                        uploader=uploader,
                        delete_local_zips=delete_local_packaged_zips,
                        skip_site_packages=skip_site_packages,
                    )
                )
                if not local
                else []
            )

        # Merge ray_init_kwargs: parameter > cluster > default
        merged_ray_init_kwargs = {**cluster_ray_init_kwargs, **(ray_init_kwargs or {})}

        stack.enter_context(
            init_ray(
                addr=addr,
                zips=zips,
                pip=manifest_pip,
                requirements_path=manifest_requirements_path,
                conda=manifest_conda,
                conda_environment_path=manifest_conda_environment_path,
                pip_extra_index_urls=manifest_pip_extra_index_urls,
                local=local,
                py_modules=py_modules,
                extra_env=extra_env,
                log_to_driver=log_to_driver,
                logging_level=logging_level,
                ray_init_kwargs=merged_ray_init_kwargs,
                uploader=uploader,
                zip_namespace=zip_namespace,
                cluster=cluster,
            )
        )

        try:
            yield
        finally:
            # For DELETE and RETAIN_ON_FAILURE, wait for tracked
            # jobs before the ExitStack unwinds (which calls ray.shutdown()
            # then RayCluster.__exit__). We must wait while Ray is still up.
            # This runs even when the with-body raises — jobs launched
            # before the error are still running on the cluster and
            # should be allowed to finish.
            if cluster is not None and cluster.on_exit in (
                ExitMode.DELETE,
                ExitMode.RETAIN_ON_FAILURE,
            ):
                cluster._jobs_had_failures = cluster._wait_for_tracked_jobs()
