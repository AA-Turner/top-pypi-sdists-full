# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Stress test-specific fixtures.

Common fixtures are inherited from src/conftest.py, including:
- standard_cluster: Standard cluster configuration
- All other common fixtures

Provides a shared ``local_ray`` fixture so stress tests run on local Ray
without the overhead of creating a k8s cluster or uploading a runtime env.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Any

import pytest
import ray

if TYPE_CHECKING:
    from collections.abc import Generator

_LOG = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def tmp_dataset_uri(geneva_test_bucket: str, request: pytest.FixtureRequest) -> str:
    """Module-scoped temporary GCS URI for test data.

    Derives a unique path from ``geneva_test_bucket`` and the test module name
    so each module gets its own namespace in the bucket.
    """
    module_name = request.module.__name__.rsplit(".", 1)[-1]
    uri = f"{geneva_test_bucket}/{module_name}"
    _LOG.info("tmp_dataset_uri: %s", uri)
    return uri


@pytest.fixture
def local_ray() -> Generator[Any, None, None]:
    """Function-scoped local Ray instance.

    Each test gets a fresh Ray to prevent OOM damage from one test
    cascading into subsequent tests.  The ~3s init overhead is negligible
    for stress tests that run 30–120s each.
    """
    _LOG.info("Initializing local Ray for stress tests")
    ray.init(num_cpus=32, ignore_reinit_error=True)
    yield
    ray.shutdown()
    # Give worker processes time to exit before the next test starts a
    # fresh Ray instance.  Without this, stale processes from high-scale
    # tests (800+ actors) accumulate and push the runner into OOM.
    time.sleep(5)
