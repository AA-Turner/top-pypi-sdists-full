#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from io import BytesIO
from textwrap import dedent
from time import sleep

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.service import Service, ServiceSpecStageFile

from ..utils import random_string


@pytest.fixture(scope="session")
def seed_temp_service_data():
    return


@pytest.mark.flaky
def test_suspend_resume(root, services, session, imagerepo, shared_compute_pool):
    stage_name = random_string(5, "test_stage_")
    s_name = random_string(5, "test_service_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    stage_file = f"@{stage_name}"
    spec = f"{stage_file}/{spec_file}"
    image_path = f"{imagerepo}/nginx:latest"
    session.file.put_stream(
        BytesIO(
            dedent(
                f"""
                spec:
                  containers:
                  - name: web-server
                    image: {image_path}
                 """
            ).encode()
        ),
        spec,
    )
    test_s = Service(
        name=s_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )

    ready_status = ("READY", "DONE", "PENDING")  # fake status might have DONE as status

    try:
        s = services.create(test_s)
        last_status = ""
        for _ in range(10):
            web_server = s.get_service_status(1)[0]
            last_status = web_server["status"]
            if last_status in ready_status:
                break
            sleep(1)
        else:
            pytest.fail(f"web_server never came online: {last_status}")
        services[test_s.name].suspend()
        for _ in range(10):
            web_server = s.get_service_status(1)[0]
            if web_server["status"] in ("SUSPENDED", "SUSPENDING"):
                break
            sleep(1)
        else:
            pytest.fail("web_server never went to sleep")
        services[test_s.name].resume()
        for _ in range(60):
            web_server = s.get_service_status(1)[0]
            if web_server["status"] in ready_status:
                break
            print(f"{web_server['status']}")
            sleep(1)
        else:
            pytest.fail("web_server never resumed")
    finally:
        s.drop()

    with pytest.raises(NotFoundError):
        services["RANDOM"].suspend()
    with pytest.raises(NotFoundError):
        services["RANDOM"].resume()
    services["RANDOM"].suspend(if_exists=True)
    services["RANDOM"].resume(if_exists=True)
