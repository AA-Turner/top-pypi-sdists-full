# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Fixtures for the E2E suite.

The suite runs against the gateway named in ``OPENSHELL_GATEWAY``, for example
the one ``scripts/e2e/start-gateway.sh`` registers as ``e2e``. Without it,
every test is skipped. See ``mise run e2e``.
"""

from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import grpc
import pytest

from openshell import Sandbox, SandboxClient, WorkspaceClient

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from openshell._proto import openshell_pb2


@pytest.fixture(scope="session")
def cluster_name() -> str:
    name = os.environ.get("OPENSHELL_GATEWAY")
    if not name:
        pytest.skip("OPENSHELL_GATEWAY not set")
    return name


@pytest.fixture(scope="session")
def sandbox_client(cluster_name: str) -> Iterator[SandboxClient]:
    # Direct deletes can wait out the Kubernetes pod grace period.
    with SandboxClient.from_active_cluster(
        cluster=cluster_name, timeout=120.0
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def ensure_sandbox_persistence_ready(sandbox_client: SandboxClient) -> None:
    for _ in range(60):
        try:
            sandbox_client.list_ids(workspace="default", page_size=1)
            return
        except grpc.RpcError as exc:
            details = exc.details() or ""
            if exc.code() == grpc.StatusCode.UNAVAILABLE:
                time.sleep(2)
                continue
            if (
                exc.code() == grpc.StatusCode.INTERNAL
                and "no such table: objects" in details
            ):
                time.sleep(1)
                continue
            raise

    pytest.fail(
        "openshell-server persistence is not initialized (missing sqlite objects table); "
        "restart the gateway and rerun the E2E suite"
    )


@pytest.fixture
def sandbox(cluster_name: str) -> Callable[..., Sandbox]:
    def _create(
        *, spec: openshell_pb2.SandboxSpec | None = None, delete_on_exit: bool = True
    ) -> Sandbox:
        return Sandbox(
            workspace="default",
            cluster=cluster_name,
            spec=spec,
            delete_on_exit=delete_on_exit,
            # Allow time to pull an explicitly supplied workload fixture.
            ready_timeout_seconds=300.0,
            # Kubernetes holds DeleteSandbox open until the pod terminates
            # (30s grace plus API headroom), which can exceed the 30s default.
            delete_timeout_seconds=120.0,
        )

    return _create


@pytest.fixture(scope="session")
def workspace_client(sandbox_client: SandboxClient) -> WorkspaceClient:
    return WorkspaceClient.from_sandbox_client(sandbox_client)
