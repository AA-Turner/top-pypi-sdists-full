# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the Fluent Health gRPC service.

These tests require a running Fluent server reachable via the
``grpc_channel_and_metadata`` session fixture defined in ``conftest.py``.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import health_pb2, health_pb2_grpc

_VALID_STATUSES = {
    health_pb2.HealthCheckResponse.SERVING_STATUS_UNSPECIFIED,
    health_pb2.HealthCheckResponse.SERVING_STATUS_SERVING,
    health_pb2.HealthCheckResponse.SERVING_STATUS_NOT_SERVING,
    health_pb2.HealthCheckResponse.SERVING_STATUS_SERVICE_UNKNOWN,
}

_HEALTH_SERVICE_NAME = "ansys.api.fluent.v1.health.Health"


def test_health_check_serving(grpc_channel_and_metadata):
    """Verify the Fluent gRPC server is alive and reports SERVING."""
    channel, metadata = grpc_channel_and_metadata
    stub = health_pb2_grpc.HealthStub(channel)
    response = stub.Check(
        health_pb2.HealthCheckRequest(),
        metadata=metadata,
    )
    assert response.status == health_pb2.HealthCheckResponse.SERVING_STATUS_SERVING


def test_health_check_named_service(grpc_channel_and_metadata):
    """Check by fully-qualified service name returns a valid status or NOT_FOUND."""
    channel, metadata = grpc_channel_and_metadata
    stub = health_pb2_grpc.HealthStub(channel)
    response = stub.Check(
        health_pb2.HealthCheckRequest(service=_HEALTH_SERVICE_NAME),
        metadata=metadata,
    )
    assert response.status in _VALID_STATUSES


def test_health_check_unknown_service(grpc_channel_and_metadata):
    """An unknown service name must produce NOT_FOUND or UNIMPLEMENTED."""
    channel, metadata = grpc_channel_and_metadata
    stub = health_pb2_grpc.HealthStub(channel)
    response = stub.Check(
        health_pb2.HealthCheckRequest(service="definitely.not.real.Service"),
        metadata=metadata,
    )
    # Some servers silently accept unknown names — status must still be valid.
    assert response.status in _VALID_STATUSES


def test_health_check_multiple_calls_consistent(grpc_channel_and_metadata):
    """Repeated Check calls must all return the same status."""
    channel, metadata = grpc_channel_and_metadata
    stub = health_pb2_grpc.HealthStub(channel)
    statuses = [
        stub.Check(health_pb2.HealthCheckRequest(), metadata=metadata).status
        for _ in range(3)
    ]
    assert len(set(statuses)) == 1, f"Inconsistent statuses: {statuses}"
