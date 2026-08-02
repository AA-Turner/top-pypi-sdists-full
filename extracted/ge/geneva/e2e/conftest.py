# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Shared pytest options and fixtures for all e2e suites."""

from __future__ import annotations

import contextlib
import logging
import os
import random
import warnings

import kubernetes
import pytest

from geneva.cluster import K8sConfigMethod
from geneva.constants import DEFAULT_K8S_NS

DEFAULT_GCP_BUCKET_PREFIX = os.getenv(
    "GENEVA_E2E_GCP_BUCKET_PREFIX", "gs://lancedb-lancedb-dev-us-central1"
)
DEFAULT_AWS_BUCKET_PREFIX = os.getenv(
    "GENEVA_E2E_AWS_BUCKET_PREFIX", "s3://geneva-integ-test-devland-us-east-1"
)
DEFAULT_AZURE_BUCKET_PREFIX = os.getenv(
    "GENEVA_E2E_AZURE_BUCKET_PREFIX", "az://lancedbdatasets"
)


def default_bucket_prefix(csp: str) -> str:
    if csp == "gcp":
        return DEFAULT_GCP_BUCKET_PREFIX
    if csp == "aws":
        return DEFAULT_AWS_BUCKET_PREFIX
    if csp == "azure":
        return DEFAULT_AZURE_BUCKET_PREFIX
    raise ValueError(f"Unsupported CSP: {csp}")


def default_bucket_path(csp: str, slug: str) -> str:
    prefix = default_bucket_prefix(csp).rstrip("/")
    return f"{prefix}/{slug}/data"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
warnings.filterwarnings(
    "ignore", "Using port forwarding for Ray cluster is not recommended for production"
)

with contextlib.suppress(kubernetes.config.config_exception.ConfigException):
    kubernetes.config.load_kube_config()

_LOG = logging.getLogger(__name__)


# ==========================================================================
# Shared CLI options
# ==========================================================================


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--csp",
        action="store",
        default="gcp",
        choices=["gcp", "aws", "azure"],
        help="Target cloud service provider",
    )
    parser.addoption(
        "--test-slug",
        action="store",
        default=None,
        help="Slug to namespace buckets/resources",
    )
    parser.addoption(
        "--bucket-path",
        action="store",
        default=None,
        help="Override bucket path (gs://..., s3://..., or az://...)",
    )


# ==========================================================================
# Shared fixtures
# ==========================================================================


@pytest.fixture(scope="session")
def csp(request) -> str:
    return request.config.getoption("--csp")


@pytest.fixture(scope="session")
def slug(request) -> str:
    return request.config.getoption("--test-slug") or str(random.randint(0, 10000))


@pytest.fixture(scope="session")
def geneva_test_bucket(request, slug, csp) -> str:
    """Resolve the test bucket and configure Geneva upload/checkpoint paths."""
    from geneva.config import override_config_kv

    bucket_path = request.config.getoption("--bucket-path")
    if bucket_path is None:
        bucket_path = os.getenv("GENEVA_E2E_BUCKET_PATH")
    if bucket_path is not None:
        bucket_path = bucket_path.strip()
    if not bucket_path:
        bucket_path = default_bucket_path(csp, slug)
        _LOG.info("Using default bucket path: %s", bucket_path)
    else:
        _LOG.info("Using provided bucket path: %s", bucket_path)

    override_config_kv(
        {
            "job.checkpoint.mode": "object_store",
            "uploader.upload_dir": f"{bucket_path}/zips",
            "job.checkpoint.object_store.path": f"{bucket_path}/checkpoints",
        }
    )

    return bucket_path


@pytest.fixture(scope="session")
def geneva_k8s_service_account(csp: str) -> str:
    return "geneva-service-account"


@pytest.fixture(scope="session")
def region(csp: str) -> str:
    if csp == "aws":
        return "us-east-1"
    if csp == "azure":
        return "eastus"
    return "us-central1"


@pytest.fixture(scope="session")
def k8s_config_method(csp: str) -> K8sConfigMethod:
    return K8sConfigMethod.EKS_AUTH if csp == "aws" else K8sConfigMethod.LOCAL


@pytest.fixture(scope="session")
def k8s_namespace(csp: str) -> str:
    return DEFAULT_K8S_NS


@pytest.fixture(scope="session")
def k8s_cluster_name(csp: str) -> str:
    return "lancedb"


@pytest.fixture(scope="session")
def head_node_selector(csp: str) -> dict:
    return {"geneva.lancedb.com/ray-head": "true"}


@pytest.fixture(scope="session")
def worker_node_selector(csp: str) -> dict:
    return {"geneva.lancedb.com/ray-worker-cpu": "true"}
