# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import os
import threading
from collections.abc import Callable
from typing import Any

import attrs
import kubernetes
from kubernetes import client
from kubernetes.client import ApiException
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from geneva.cluster import K8sConfigMethod
from geneva.eks import build_api_client

_LOG = logging.getLogger(__name__)


def _get_max_retries_from_env() -> int:
    val = os.getenv("GENEVA_K8S_AUTH_MAX_RETRIES", "3")
    try:
        n = int(val)
        return max(1, n)
    except Exception:
        _LOG.warning("Invalid GENEVA_K8S_AUTH_MAX_RETRIES=%r; falling back to 3", val)
        return 3


_MAX_AUTH_RETRIES = _get_max_retries_from_env()


def _make_retry_wrapper(
    *,
    clients: "KuberayClients",
    api_provider: Callable[[], Any],
    method_name: str,
) -> Callable:
    """Return a callable that resolves the latest API method each time and
    retries on 401 with a full auth refresh, and retries on transient errors.
    """

    def _is_401(e: BaseException) -> bool:
        return isinstance(e, ApiException) and getattr(e, "status", None) == 401

    def _is_transient_error(e: BaseException) -> bool:
        """Check if this is a transient k8s API error that should be retried."""
        if isinstance(e, ApiException):
            status = getattr(e, "status", None)
            # Retry on rate limiting, server errors, service unavailable
            return status in (429, 500, 503)
        # Retry on connection/timeout errors
        return isinstance(e, ConnectionError | TimeoutError | OSError)

    def _should_retry(e: BaseException) -> bool:
        return _is_401(e) or _is_transient_error(e)

    def _before_sleep_refresh(retry_state) -> None:
        exc = retry_state.outcome.exception()
        if _is_401(exc):
            _LOG.info("token expired, reauthenticating with k8s")
            clients.refresh()
        else:
            _LOG.warning(
                "transient k8s API error (attempt %d/%d), retrying: %s",
                retry_state.attempt_number,
                _MAX_AUTH_RETRIES,
                exc,
            )

    @retry(
        retry=retry_if_exception(_should_retry),
        stop=stop_after_attempt(_MAX_AUTH_RETRIES),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        before_sleep=_before_sleep_refresh,
        reraise=True,
    )
    def _invoke(*args, **kwargs) -> Any:  # type: ignore[no-redef]
        api = api_provider()
        method_func = getattr(type(api), method_name)
        return method_func(api, *args, **kwargs)

    def wrapper(*args, **kwargs) -> Any:
        return _invoke(*args, **kwargs)

    return wrapper


def _wrap_api_methods(
    api_instance: Any,
    api_provider: Callable[[], Any],
    clients: "KuberayClients",
) -> Any:
    """Wrap all methods of an API instance to dynamically resolve methods and
    retry on 401 using refreshed auth.
    """
    # Port forwarding methods use WebSocket upgrades and cannot be wrapped
    # (wrapping breaks the HTTP upgrade handshake)
    portforward_methods = {
        "connect_get_namespaced_pod_portforward",
        "connect_get_namespaced_pod_portforward_with_http_info",
        "connect_post_namespaced_pod_portforward",
        "connect_post_namespaced_pod_portforward_with_http_info",
    }
    for attr_name in dir(api_instance):
        if not attr_name.startswith("_") and attr_name not in portforward_methods:
            attr = getattr(api_instance, attr_name)
            if callable(attr):
                setattr(
                    api_instance,
                    attr_name,
                    _make_retry_wrapper(
                        clients=clients,
                        api_provider=api_provider,
                        method_name=attr_name,
                    ),
                )
    return api_instance


@attrs.define()
class KuberayClients:
    """
    Wrap kubernetes clients required for Kuberay operations
    """

    core_api: client.CoreV1Api = attrs.field(init=False)
    custom_api: client.CustomObjectsApi = attrs.field(init=False)
    auth_api: client.AuthorizationV1Api = attrs.field(init=False)
    scheduling_api: client.SchedulingV1Api = attrs.field(init=False)

    config_method: K8sConfigMethod = attrs.field(default=K8sConfigMethod.LOCAL)
    """
    Method to retrieve kubeconfig
    """

    region: str | None = attrs.field(
        default=None,
    )
    """
    Optional cloud region where the cluster is located
    """

    cluster_name: str | None = attrs.field(
        default=None,
    )
    """
    Optional k8s cluster name, required for EKS auth
    """

    role_name: str | None = attrs.field(
        default=None,
    )
    """
    Optional IAM role name, required for EKS auth
    """

    _refresh_lock: threading.Lock = attrs.field(
        init=False, factory=threading.Lock, repr=False
    )
    """
    Lock to prevent concurrent refresh operations
    """

    def __attrs_post_init__(self) -> None:
        self.init_clients()

    def refresh(self) -> None:
        with self._refresh_lock:
            _LOG.debug("acquiring refresh lock for k8s client reauth")
            self.init_clients()
            _LOG.debug("released refresh lock after k8s client reauth")

    def init_clients(self) -> None:
        self._validate()

        # Initialize API clients based on config_method
        # If refresh is set, it will re-authenticate instead of using cached client
        client = build_api_client(
            self.config_method, self.region, self.cluster_name, self.role_name
        )

        # Create API clients
        self.custom_api = kubernetes.client.CustomObjectsApi(api_client=client)
        self.core_api = kubernetes.client.CoreV1Api(api_client=client)
        self.auth_api = kubernetes.client.AuthorizationV1Api(api_client=client)
        self.scheduling_api = kubernetes.client.SchedulingV1Api(api_client=client)

        # Wrap all API methods with refresh_auth decorator
        _wrap_api_methods(self.custom_api, lambda: self.custom_api, self)
        _wrap_api_methods(self.core_api, lambda: self.core_api, self)
        _wrap_api_methods(self.auth_api, lambda: self.auth_api, self)
        _wrap_api_methods(self.scheduling_api, lambda: self.scheduling_api, self)

    def _validate(self) -> None:
        if self.config_method == K8sConfigMethod.EKS_AUTH:
            # log these and fallback to defaults
            if not self.cluster_name:
                _LOG.warning(
                    "Using default cluster name for config method "
                    "EKS_AUTH because cluster_name is not set"
                )
            if not self.region:
                _LOG.warning(
                    "Using default region for config method "
                    "EKS_AUTH because region is not set"
                )
            if not self.role_name:
                _LOG.warning(
                    "Using default role name for config method "
                    "EKS_AUTH because role_name is not set"
                )
