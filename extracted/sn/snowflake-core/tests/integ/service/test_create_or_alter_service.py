#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.service import Service
from tests.utils import random_string


@pytest.mark.flaky
@pytest.mark.min_sf_ver("8.37.0")
def test_create_or_alter(services, service_spec_file_on_stage, shared_compute_pool, warehouse):
    service_name = random_string(5, "test_create_or_alter_service_")

    test_service = Service(
        name=service_name,
        compute_pool=shared_compute_pool,
        spec=service_spec_file_on_stage,
        min_instances=1,
        max_instances=1,
        comment="test_service_comment"
    )

    service_ref = None

    try:
        # Test create when the Service does not exist.
        service_ref = services[service_name]
        service_ref.create_or_alter(test_service)
        service_list = services.iter(like=service_name)
        result = next(service_list)
        assert result.name == test_service.name.upper()
        assert result.compute_pool == test_service.compute_pool.upper()
        assert result.min_instances == test_service.min_instances
        assert result.max_instances == test_service.max_instances
        assert result.comment == test_service.comment

        assert result.auto_resume is True
        # Make sure that issuing an empty alter doesn't create a malformed SQL
        service_ref.create_or_alter(test_service)

        # Test introducing property which was not set before
        test_service_new_1 = Service(name=service_name,
                                     spec=service_spec_file_on_stage,
                                     compute_pool=shared_compute_pool,
                                     min_instances=1,
                                     max_instances=1,
                                     auto_resume=False,
                                     comment="test_service_comment")
        service_ref.create_or_alter(test_service_new_1)
        service_list = services.iter(like=service_name)
        result = next(service_list)
        assert result.name == test_service_new_1.name.upper()
        assert result.compute_pool == test_service.compute_pool.upper()
        assert result.min_instances == test_service_new_1.min_instances
        assert result.max_instances == test_service_new_1.max_instances
        assert result.comment == test_service.comment
        assert result.auto_resume == test_service_new_1.auto_resume

        # Test altering the property which we set before
        test_service_new_2 = Service(name=service_name,
                                     spec=service_spec_file_on_stage,
                                     compute_pool=shared_compute_pool,
                                     min_instances=1,
                                     max_instances=1,
                                     auto_resume=False,
                                     comment="comment")
        service_ref.create_or_alter(test_service_new_2)
        service_list = services.iter(like=service_name)
        result = next(service_list)
        assert result.name == test_service_new_2.name.upper()
        assert result.compute_pool == test_service.compute_pool.upper()
        assert result.min_instances == test_service_new_2.min_instances
        assert result.max_instances == test_service_new_2.max_instances
        assert result.comment == test_service_new_2.comment
        assert result.auto_resume == test_service_new_2.auto_resume

        # Test not providing the property and checking that it is unset now and adding a new property at the same time
        test_service_new_3 = Service(name=service_name,
                                     spec=service_spec_file_on_stage,
                                     compute_pool=shared_compute_pool,
                                     min_instances=1,
                                     max_instances=1,
                                     query_warehouse=warehouse.name,
                                     comment="comment")
        service_ref.create_or_alter(test_service_new_3)
        service_list = services.iter(like=service_name)
        result = next(service_list)
        assert result.name == test_service_new_3.name.upper()
        assert result.compute_pool == test_service.compute_pool.upper()
        assert result.query_warehouse == test_service_new_3.query_warehouse.upper()
        assert result.min_instances == test_service_new_3.min_instances
        assert result.max_instances == test_service_new_3.max_instances
        assert result.comment == test_service_new_3.comment

        # Uncomment when SNOW-1664511 is fixed; CoA does not seem to be properly unsetting properties
        # that are not filled.
        # This should be reset to the default value which is True
        # assert result.auto_resume is True

    finally:
        with suppress(NotFoundError):
            service_ref.drop()
