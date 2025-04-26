#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from io import BytesIO
from textwrap import dedent

import pytest

from snowflake.core.service import (
    Service,
    ServiceContainer,
    ServiceEndpoint,
    ServiceInstance,
    ServiceRole,
    ServiceSpecStageFile,
)
from tests.utils import random_string


@pytest.mark.usefixtures("qa_mode_enabled")
def test_get_commands(services, session, imagerepo, shared_compute_pool, database, schema,
                      setup_with_connector_execution):
    # Mock resource set status
    with setup_with_connector_execution(["alter session set ENABLE_MOCK_RESOURCE_SET_STATUS=true"], []):
        # Create a service
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
                          - name: main-container
                            image: {imagerepo}/hello-world:latest
                          - name: other-container
                            image: {imagerepo}/hello-world:latest
                          endpoints:
                          - name: echo
                            port: 8080
                        serviceRoles:
                        - name: role1
                          endpoints:
                          - echo
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
        svc = services.create(test_service)

        try:
            # Verify the output of get_containers command
            expected_containers = [ServiceContainer.from_dict({
                "database_name": database.name.upper(),
                "schema_name": schema.name.upper(),
                "service_name": service_name.upper(),
                "instance_id": "0",
                "container_name": "main-container",
                "status": "DONE",
                "message": "DONE",
                "image_name": f"{imagerepo}/hello-world:latest",
                "image_digest": None,
                "restart_count": 0,
                "start_time": "2023-01-01T00:00:00Z"
            }), ServiceContainer.from_dict({
                "database_name": database.name.upper(),
                "schema_name": schema.name.upper(),
                "service_name": service_name.upper(),
                "instance_id": "0",
                "container_name": "other-container",
                "status": "DONE",
                "message": "DONE",
                "image_name": f"{imagerepo}/hello-world:latest",
                "image_digest": None,
                "restart_count": 0,
                "start_time": "2023-01-01T00:00:00Z"
            })]

            actual_containers = list(svc.get_containers())
            assert actual_containers == expected_containers

            # Verify the output of get_instances command
            expected_instances = [ServiceInstance.from_dict({
                "database_name": database.name.upper(),
                "schema_name": schema.name.upper(),
                "service_name": service_name.upper(),
                "instance_id": "0",
                "status": "SUCCEEDED",
                "spec_digest": "",
                "creation_time": "2023-01-01T00:00:00Z",
                "start_time": "2023-01-01T00:00:00Z"
            })]

            actual_instances = list(svc.get_instances())
            assert actual_instances == expected_instances

            # Verify the output of get_roles command
            expected_roles = [ServiceRole.from_dict({
                "created_on": "1967-06-23T07:00:00.123+00:00",
                "name": "ALL_ENDPOINTS_USAGE",
                "comment": None
            }), ServiceRole.from_dict({
                "created_on": "1967-06-23T07:00:00.123+00:00",
                "name": "ROLE1",
                "comment": None
            })]

            actual_roles = list(svc.get_roles())
            assert actual_roles == expected_roles

            # Verify the output of get_endpoints command
            expected_endpoints = [ServiceEndpoint.from_dict({
                "name": "echo",
                "port": 8080,
                "port_range": None,
                "protocol": "HTTP",
                "is_public": False,
                "ingress_url": None
            })]

            actual_endpoints = list(svc.get_endpoints())
            assert actual_endpoints == expected_endpoints
        finally:
            svc.drop()

