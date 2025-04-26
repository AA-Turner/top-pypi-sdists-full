#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import datetime

from io import BytesIO
from textwrap import dedent

import pytest

from snowflake.core.service import Service, ServiceSpecStageFile
from tests.utils import random_string


@pytest.mark.usefixtures("qa_mode_enabled")
def test_iter(services, temp_service, session, imagerepo, shared_compute_pool, database, schema):
    service_name = random_string(5, "test_service_a_")
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
        service_names = [sr.name for sr in services.iter()]
        assert temp_service.name.upper() in service_names

        service_names = [sr.name for sr in services.iter(like="TESt_Serv%")]
        assert temp_service.name.upper() in service_names
        assert service_name.upper() in service_names
        service_names = [sr.name for sr in services.iter(starts_with="TESt_Serv")]
        assert temp_service.name.upper() not in service_names
        assert service_name.upper() not in service_names

        service_names = [sr.name for sr in services.iter(starts_with="TEST_SERVICE")]
        assert temp_service.name.upper() in service_names
        assert service_name.upper() in service_names

        service_names = [sr.name for sr in services.iter(starts_with="test_service")]
        assert temp_service.name.upper() not in service_names
        assert service_name.upper() not in service_names

        service_names = [sr.name for sr in services.iter(like="test_service_%")]
        assert temp_service.name.upper() in service_names

        service_names = [sr.name for sr in services.iter(like="test_service_%")]
        assert len(service_names) >= 2
        assert temp_service.name.upper() in service_names
        assert service_name.upper() in service_names

        service_names = [sr.name for sr in services.iter(like="test_service_%", limit=1)]
        assert len(service_names) == 1

        service_names = [sr.name for sr in services.iter(from_name="TEST_SERVICE_%", limit=1)]
        assert len(service_names) == 1

        service_names = [sr.name for sr in services.iter(from_name="TEST_SERVICE_%")]
        assert len(service_names) >= 2

        # Verifying the output of the show service command for the service created in the test file
        result = list(services.iter(like=f"{service_name.upper()}"))
        assert len(result) == 1
        expected_spec_for_new_service = (
            '---\nspec:\n  containers:\n  - name: "hello-world"'
            f'\n    image: "{imagerepo}/hello-world:latest"\n    resources:\n      '
            'limits:\n        memory: "6Gi"\n        cpu: "8"\n      requests:\n        '
            'memory: "0.5Gi"\n        cpu: "0.5"\n'
        )
        assert_service_output(
            result[0],
            service_name,
            shared_compute_pool,
            expected_spec_for_new_service,
            database.name,
            schema.name,
            1,
            1,
        )
        assert s.fetch().to_dict() == result[0].to_dict()

        # Verifying the output of the show service command for the temp created by the test setup
        result = list(services.iter(like=f"{temp_service.name.upper()}"))
        assert len(result) == 1
        expected_spec_for_temp_service = (
            '---\nspec:\n  containers:\n  - name: "hello-world"'
            f'\n    image: "{imagerepo}/hello-world:latest"\n    resources:\n      '
            'limits:\n        memory: "6Gi"\n        cpu: "8"\n      requests:\n   '
            '     memory: "0.5Gi"\n        cpu: "0.5"\n  endpoints:\n  - name: '
            '"default"\n    port: 8080\n'
        )
        assert_service_output(
            result[0],
            temp_service.name,
            shared_compute_pool,
            expected_spec_for_temp_service,
            database.name,
            schema.name,
            1,
            5,
            "created by temp_service",
        )
        assert temp_service.fetch().to_dict() == result[0].to_dict()
    finally:
        s.drop()


def assert_service_output(
    service,
    expected_service_name,
    expected_compute_pool_name,
    expected_spec_text,
    expected_database_name,
    expected_schema_name,
    expected_min_instances,
    expected_max_instances,
    expected_comment=None,
):
    assert service.name == expected_service_name.upper()
    assert service.status in ["PENDING", "RUNNING"]
    assert service.compute_pool == expected_compute_pool_name.upper()
    assert service.spec is not None
    assert service.spec.spec_text == expected_spec_text
    assert service.external_access_integrations is None
    assert service.query_warehouse is None
    assert service.comment == expected_comment
    assert service.auto_resume is True
    assert service.current_instances == 1
    assert service.target_instances == 1
    assert service.min_instances == expected_min_instances
    assert service.max_instances == expected_max_instances
    assert service.database_name == expected_database_name.upper()
    assert service.schema_name == expected_schema_name.upper()
    assert service.owner == "ACCOUNTADMIN"
    assert service.dns_name is not None and f"{expected_service_name.lower().replace('_', '-')}" in service.dns_name
    assert service.created_on == datetime.datetime(1967, 6, 23, 7, 0, 0, 123000, tzinfo=datetime.timezone.utc)
    assert service.updated_on == datetime.datetime(1967, 6, 23, 7, 0, 0, 123000, tzinfo=datetime.timezone.utc)
    assert service.resumed_on == datetime.datetime(1967, 6, 23, 7, 0, 0, 123000, tzinfo=datetime.timezone.utc)
    assert service.owner_role_type == "ROLE"
    assert service.is_job is False
    assert service.spec_digest is not None
    assert service.is_upgrading is False
    assert service.managing_object_domain is None
    assert service.managing_object_name is None
