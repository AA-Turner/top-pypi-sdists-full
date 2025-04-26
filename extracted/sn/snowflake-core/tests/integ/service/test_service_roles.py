#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from io import BytesIO
from textwrap import dedent

import pytest

from snowflake.core.role import Role, Securable
from snowflake.core.service import (
    GrantOf,
    Service,
    ServiceRoleGrantTo,
    ServiceSpecStageFile,
)
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.39.0")
@pytest.mark.usefixtures("qa_mode_enabled")
def test_service_roles(session, database, schema, services, roles, imagerepo, shared_compute_pool):
    role = None
    svc = None

    try:
        # Creating a custom role
        role_name = random_string(4, "test_role_")
        test_role = Role(name=role_name, comment="test role")
        role = roles.create(test_role)

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
                          - name: anotherecho
                            port: 8085
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

        # Grant service role to the test role
        assert len(list(role.iter_grants_to())) == 0
        role.grant_role(
            role_type="SERVICE ROLE",
            role=Securable(database=database.name, schema=schema.name, service=service_name, name="role1")
        )
        assert len(list(role.iter_grants_to())) == 1

        # Verify the output of the iter_grants_of_service_role command
        expected_grants_of = [GrantOf.from_dict({
            "created_on": "2012-08-01T07:00:00.000+00:00",
            "role": f"{database.name.upper()}.{schema.name.upper()}.{service_name.upper()}.ROLE1",
            "granted_to": "ROLE",
            "grantee_name": "ACCOUNTADMIN",
            "granted_by": "",
        }), GrantOf.from_dict({
            "created_on": "2012-08-01T07:00:00.000+00:00",
            "role": f"{database.name.upper()}.{schema.name.upper()}.{service_name.upper()}.ROLE1",
            "granted_to": "ROLE",
            "grantee_name": role_name.upper(),
            "granted_by": "ACCOUNTADMIN",
        })]

        actual_grants_of = list(svc.iter_grants_of_service_role("role1"))
        assert actual_grants_of == expected_grants_of

        # Verify the output of the iter_grants_to_service_role command
        expected_grants_to = [ServiceRoleGrantTo.from_dict({
            "created_on": "2012-08-01T07:00:00.000+00:00",
            "privilege": "USAGE",
            "granted_on": "SERVICE_ENDPOINT",
            "name": f"{database.name.upper()}.{schema.name.upper()}.{service_name.upper()}!echo",
            "granted_to": "SERVICE ROLE",
            "grantee_name": "ROLE1",
        })]

        actual_grants_to = list(svc.iter_grants_to_service_role("role1"))
        assert actual_grants_to == expected_grants_to

        # Revoke service role from account role
        role.revoke_role(
            role_type="SERVICE ROLE",
            role=Securable(database=database.name, schema=schema.name, service=service_name, name="role1")
        )
        assert len(list(role.iter_grants_to())) == 0
    finally:
        if role is not None:
            role.drop()

        if svc is not None:
            svc.drop()
