"""Utility functions for the Matrice package.

This module was historically a single junk-drawer. It has been decomposed into
cohesive submodules:

  - ``matrice_common.errors``    — error types, deduplication, error logging,
                                   and the ``log_errors`` decorator.
  - ``matrice_common.packaging`` — pip dependency management.
  - ``matrice_common.metrics``   — ``BenchmarkMetrics``.

``utils.py`` is kept as a 100%-backward-compatible re-export shim. Every name
that was importable from ``matrice_common.utils`` before the split remains
importable here. The API/project-service response helpers (``handle_response``
and friends) continue to live in this module directly.
"""

import logging
import os  # noqa: F401  (re-exported; `matrice_common.utils.os` patch target)
import subprocess  # noqa: F401  (re-exported; `matrice_common.utils.subprocess` patch target)
from importlib.metadata import version  # noqa: F401  (re-exported; patch target)
from typing import Any, Dict, Optional, Tuple

# ---------------------------------------------------------------------------
# Re-exports from the decomposed submodules (frozen public API + privates that
# sibling SDKs and the test-suite import directly from matrice_common.utils).
# ---------------------------------------------------------------------------
from .errors import (
    _DEDUPLICATION_ENABLED,
    _ERROR_CACHE_MAX,
    _ERROR_CACHE_TTL,
    _ERROR_TYPE_MAP,
    ERROR_TYPE_TO_MESSAGE,
    AppError,
    ErrorLog,
    ErrorType,
    LoggingIntegration,
    SentryConfig,
    _error_cache,
    _error_cache_lock,
    _extract_error_location,
    _extract_function_params,
    _extract_http_context,
    _get_error_logging_producer,
    _get_sentry_client,
    _make_hashable,
    cacheable,
    configure_scope,
    extract_service_from_path,
    generate_error_dedup_key,
    get_deduplication_config,
    hash_error,
    log_errors,
    process_error_log,
    seen_error,
    send_error_log,
    send_sentry_log,
    sentry_sdk,
)
from .metrics import BenchmarkMetrics
from .packaging import (
    _INSTALLED_THIS_PROCESS,
    _acquire_install_lock,
    _install_package,
    _is_package_installed,
    _release_install_lock,
    dependencies_check,
)

logger = logging.getLogger(__name__)


# =============================================================================
# API response handling / project-service helpers (kept in utils directly).
# =============================================================================


def handle_response(
    response: Optional[Dict[str, Any]],
    success_message: str,
    failure_message: str,
) -> Tuple[Any, Optional[str], str]:
    """Handle API response and return appropriate result."""
    if response and response.get("success"):
        result = response.get("data")
        error = None
        message = success_message
    else:
        result = None
        error = response.get("message") if response else "No response received"
        message = failure_message
    return result, error, message


def check_for_duplicate(session: Any, service: str, name: str) -> Tuple[Any, Optional[str], str]:
    """Check if an item with the given name already exists for the specified service."""
    service_config = {
        "dataset": {
            "path": f"/v1/dataset/check_for_duplicate?datasetName={name}",
            "item_name": "Dataset",
        },
        "annotation": {
            "path": f"/v1/annotations/check_for_duplicate?annotationName={name}",
            "item_name": "Annotation",
        },
        "model_export": {
            "path": f"/v1/model/model_export/check_for_duplicate?modelExportName={name}",
            "item_name": "Model export",
        },
        "model": {
            "path": f"/v1/model/model_train/check_for_duplicate?modelTrainName={name}",
            "item_name": "Model Train",
        },
        "projects": {
            "path": f"/v1/project/check_for_duplicate?name={name}",
            "item_name": "Project",
        },
        "deployment": {
            "path": f"/v1/inference/check_for_duplicate?deploymentName={name}",
            "item_name": "Deployment",
        },
    }
    if service not in service_config:
        return (
            None,
            f"Invalid service: {service}",
            "Service not supported",
        )
    config = service_config[service]
    resp = session.rpc.get(path=config["path"])
    if resp and resp.get("success"):
        if resp.get("data") == "true":
            return handle_response(
                resp,
                f"{config['item_name']} with this name already exists",
                f"Could not check for this {service} name",
            )
        return handle_response(
            resp,
            f"{config['item_name']} with this name does not exist",
            f"Could not check for this {service} name",
        )
    return handle_response(
        resp,
        "",
        f"Could not check for this {service} name",
    )


def get_summary(session: Any, project_id: str, service_name: str) -> Tuple[Any, Optional[str]]:
    """Fetch a summary of the specified service in the project."""
    service_paths = {
        "annotations": "/v1/annotations/summary",
        "models": "/v1/model/summary",
        "exports": "/v1/model/summaryExported",
        "deployments": "/v1/inference/summary",
    }
    success_messages = {
        "annotations": "Annotation summary fetched successfully",
        "models": "Model summary fetched successfully",
        "exports": "Model Export Summary fetched successfully",
        "deployments": "Deployment summary fetched successfully",
    }
    error_messages = {
        "annotations": "Could not fetch annotation summary",
        "models": "Could not fetch models summary",
        "exports": "Could not fetch models export summary",
        "deployments": "An error occurred while trying to fetch deployment summary.",
    }
    if service_name not in service_paths:
        return (
            None,
            f"Invalid service name: {service_name}",
        )
    path = f"{service_paths[service_name]}?projectId={project_id}"
    resp = session.rpc.get(path=path)
    result, error, _message = handle_response(
        resp,
        success_messages.get(service_name, "Operation successful"),
        error_messages.get(service_name, "Operation failed"),
    )
    return result, error


__all__ = [
    # errors
    "ERROR_TYPE_TO_MESSAGE",
    "AppError",
    "ErrorLog",
    "ErrorType",
    "SentryConfig",
    "_ERROR_TYPE_MAP",
    "_DEDUPLICATION_ENABLED",
    "_ERROR_CACHE_MAX",
    "_ERROR_CACHE_TTL",
    "_error_cache",
    "_error_cache_lock",
    "_extract_error_location",
    "_extract_function_params",
    "_extract_http_context",
    "_get_error_logging_producer",
    "_get_sentry_client",
    "_make_hashable",
    "cacheable",
    "configure_scope",
    "extract_service_from_path",
    "generate_error_dedup_key",
    "get_deduplication_config",
    "hash_error",
    "log_errors",
    "process_error_log",
    "seen_error",
    "send_error_log",
    "send_sentry_log",
    "sentry_sdk",
    "LoggingIntegration",
    # metrics
    "BenchmarkMetrics",
    # packaging
    "_INSTALLED_THIS_PROCESS",
    "_acquire_install_lock",
    "_install_package",
    "_is_package_installed",
    "_release_install_lock",
    "dependencies_check",
    # re-exported stdlib patch targets
    "os",
    "subprocess",
    "version",
    # response helpers (defined here)
    "handle_response",
    "check_for_duplicate",
    "get_summary",
]
