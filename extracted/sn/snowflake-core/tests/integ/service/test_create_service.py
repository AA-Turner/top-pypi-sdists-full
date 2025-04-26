#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import APIError, ConflictError
from snowflake.core.service import Service, ServiceSpecStageFile
from tests.utils import random_string


def test_create(services, service_spec_file_on_stage, shared_compute_pool):
    try:
        service_name = random_string(5, "test_service_")

        test_service = Service(
            name=service_name,
            compute_pool=shared_compute_pool,
            spec=service_spec_file_on_stage,
            min_instances=1,
            max_instances=1,
        )
        s = services.create(test_service)

        fetched_service = s.fetch()
        assert fetched_service.name == service_name.upper()

        # already existing service
        with pytest.raises(
            ConflictError,
        ):
            services.create(test_service)

        s = services.create(test_service, mode=CreateMode.if_not_exists)

        s.drop()

        # case sensitive name for service is not supported
        service_name = random_string(5, "test_service_")
        service_name = f'"{service_name}"'
        test_service = Service(
            name=service_name,
            compute_pool=shared_compute_pool,
            spec=service_spec_file_on_stage,
            min_instances=1,
            max_instances=1,
        )

        with pytest.raises(APIError):
            services.create(test_service)
    finally:
        services[service_name].drop(if_exists=True)


def test_create_or_replace(services, session, imagerepo, shared_compute_pool):
    service_name = random_string(5, "test_service_")
    stage_name = random_string(5, "test_stage_")
    spec_file = "spec.yaml"
    test_service = Service(
        name=service_name,
        compute_pool=shared_compute_pool,
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )
    with pytest.raises(ValueError):
        services.create(test_service, mode=CreateMode.or_replace)


def test_create_with_spec_inline(services, temp_service_from_spec_inline, database):
    service = services[temp_service_from_spec_inline.name].fetch()
    assert (
        service.name == temp_service_from_spec_inline.name  # for mixed case names
        or service.name.upper() == temp_service_from_spec_inline.name.upper()  # for upper/lower case names
    )
    assert 'name: "hello-world"' in service.spec.spec_text
    assert service.comment == "created by temp_service_from_spec_inline"
