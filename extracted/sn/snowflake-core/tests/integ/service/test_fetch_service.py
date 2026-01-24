#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from io import BytesIO
from textwrap import dedent
from time import sleep

import pytest

from snowflake.core.exceptions import APIError
from snowflake.core.service import Service, ServiceSpecStageFile
from tests.utils import random_string


pytestmark = [pytest.mark.skip_gov]


def test_fetch(services, temp_service, database, shared_compute_pool):
    service = services[temp_service.name].fetch()
    assert service.name == temp_service.name.upper()
    assert service.compute_pool == shared_compute_pool.upper()
    assert service.auto_resume
    assert service.comment == "created by temp_service"
    assert service.database_name == database.name
    assert service.spec is not None
    assert service.current_instances is not None
    assert service.target_instances is not None
    assert service.min_instances is not None
    assert service.max_instances is not None
    assert service.owner is not None
    assert service.dns_name is not None
    assert service.created_on is not None
    assert service.updated_on is not None
    assert service.owner_role_type is not None
    assert service.is_job is not None
    assert service.spec_digest is not None
    assert service.is_upgrading is not None


@pytest.mark.flaky
def test_fetch_service_logs(services, temp_service, instance_family):
    service_name = temp_service.name
    logs = None

    for _ in range(10):
        try:
            logs = services[service_name].get_service_logs("0", "hello-world")
        except APIError:
            pass
        if logs:
            break
        sleep(5)

    if instance_family.lower() != "fake":
        message = "your installation appears to be working"
    else:
        message = "test 999"
    assert message in logs

    trimmed_logs = services[temp_service.name].get_service_logs("0", "hello-world", num_lines=10)
    assert trimmed_logs in logs
    assert len(trimmed_logs) < len(logs)


def test_fetch_service_status(services, session, imagerepo, shared_compute_pool):
    service_name = random_string(5, "test_service_")
    stage_name = random_string(5, "test_stage_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    stage_file = f"@{stage_name}"
    spec = f"{stage_file}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(f"""
                spec:
                  containers:
                  - name: hello-world
                    image: {imagerepo}/hello-world:latest
                """).encode()
        ),
        spec,
    )
    test_service = Service(
        name=service_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )

    try:
        s = services.create(test_service)
        status = s.get_service_status(timeout=10)
        assert status[0]["status"] in ["UNKNOWN", "PENDING", "READY", "DONE"]
        status = s.get_service_status()
        assert status[0]["status"] in ["UNKNOWN", "PENDING", "READY", "DONE"]
        s.suspend()
        for _ in range(10):
            status = s.get_service_status(timeout=10)
            if not status:
                break
            sleep(1)
        else:
            pytest.fail(f"Service status did not become empty after suspend. Last status: {status}")
        assert not status
        status = s.get_service_status()
        assert not status
    finally:
        services[test_service.name].drop()
