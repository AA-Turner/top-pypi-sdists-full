# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Shared fixtures for the ``kcl-python`` end-to-end pytest suite.

These fixtures only run once a test in this directory has already opted in —
see ``test_e2e_consumer.py``'s module-level ``pytest.mark.skipif``, which
skips the whole suite unless ``AWS_ENDPOINT_URL`` is set (mirroring the Rust
``#[ignore]`` integration tests' explicit opt-in; see the "Running integration
tests" section of CLAUDE.md). Nothing here talks to AWS at import time, so
plain ``pytest kcl-python/tests/`` (no env var) collects and skips cleanly.

Credentials are never hardcoded here: boto3 and ``kcl_rs.Scheduler`` both fall
back to the standard AWS credential chain (env vars, profile, IMDS, ...); in
CI/local runs against LocalStack that means exporting
``AWS_ACCESS_KEY_ID``/``AWS_SECRET_ACCESS_KEY=test`` yourself.
"""
from __future__ import annotations

import os
import time
import uuid
from dataclasses import dataclass

import boto3
import pytest

# Mirrors the Rust integration harness's `kclrs-it-` convention
# (kcl/tests/common/mod.rs) so e2e leftovers are easy to spot/clean up.
RESOURCE_PREFIX = "kclrs-e2e-"


def unique_name(prefix: str) -> str:
    """A `kclrs-e2e-<prefix>-<random>` name, unique per call."""
    return f"{RESOURCE_PREFIX}{prefix}-{uuid.uuid4().hex[:10]}"


@pytest.fixture(scope="session")
def aws_region() -> str:
    return os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"


@pytest.fixture(scope="session")
def endpoint_url() -> str | None:
    return os.environ.get("AWS_ENDPOINT_URL")


@pytest.fixture(scope="session")
def await_budget_secs() -> float:
    """How long a poll-until-condition wait may run before a test gives up.

    Configurable via ``KCLRS_E2E_AWAIT_SECS`` (default 300s) — a cold Scheduler
    start against LocalStack (lease table creation, shard sync, and for
    FANOUT, fan-out consumer registration) takes ~30-90s on its own.
    """
    return float(os.environ.get("KCLRS_E2E_AWAIT_SECS", "300"))


@pytest.fixture(scope="session")
def kinesis_client(aws_region, endpoint_url):
    return boto3.client("kinesis", region_name=aws_region, endpoint_url=endpoint_url)


@pytest.fixture(scope="session")
def dynamodb_client(aws_region, endpoint_url):
    return boto3.client("dynamodb", region_name=aws_region, endpoint_url=endpoint_url)


@dataclass
class KinesisApp:
    """A Kinesis stream + KCL application name, created together by
    ``stream_app_factory`` and torn down together at test end.

    The DynamoDB lease table (named after ``application_name``) doesn't exist
    until the first ``Scheduler`` run creates it — teardown deletes it too, if
    present.
    """

    stream_name: str
    application_name: str
    kinesis: object
    dynamodb: object

    def wait_active(self, timeout: float = 60.0) -> None:
        deadline = time.monotonic() + timeout
        while True:
            desc = self.kinesis.describe_stream(StreamName=self.stream_name)["StreamDescription"]
            if desc["StreamStatus"] == "ACTIVE":
                return
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"stream {self.stream_name!r} did not become ACTIVE within {timeout}s "
                    f"(last status: {desc['StreamStatus']!r})"
                )
            time.sleep(1.0)

    def put_records(self, payloads: list[bytes]) -> None:
        """Put each payload as its own record (distinct partition keys)."""
        for i, payload in enumerate(payloads):
            self.kinesis.put_record(
                StreamName=self.stream_name,
                Data=payload,
                PartitionKey=f"pk-{i}-{uuid.uuid4().hex[:6]}",
            )


@pytest.fixture
def stream_app_factory(kinesis_client, dynamodb_client):
    """Factory fixture: call it to create a fresh stream + app name.

    Creates a Kinesis stream, waits for ACTIVE, and remembers it; on test
    teardown deletes every stream created this way plus the DynamoDB lease
    table named after each app (ignoring "already gone").
    """
    created: list[KinesisApp] = []

    def _make(shard_count: int = 1) -> KinesisApp:
        stream_name = unique_name("stream")
        application_name = unique_name("app")
        kinesis_client.create_stream(StreamName=stream_name, ShardCount=shard_count)
        app = KinesisApp(
            stream_name=stream_name,
            application_name=application_name,
            kinesis=kinesis_client,
            dynamodb=dynamodb_client,
        )
        app.wait_active()
        created.append(app)
        return app

    yield _make

    for app in created:
        try:
            kinesis_client.delete_stream(StreamName=app.stream_name, EnforceConsumerDeletion=True)
        except Exception:
            pass
        try:
            dynamodb_client.delete_table(TableName=app.application_name)
        except dynamodb_client.exceptions.ResourceNotFoundException:
            pass
        except Exception:
            pass
