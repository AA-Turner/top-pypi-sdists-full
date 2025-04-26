#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


from contextlib import suppress

import pytest

from snowflake.core.compute_pool import (
    ComputePool,
)
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.37.0")
def test_create_or_alter(compute_pools, instance_family):
    cp_name = random_string(5, "test_cp_create_or_alter_")
    test_cp = ComputePool(name=cp_name, instance_family=instance_family, min_nodes=1, max_nodes=1,
                          auto_resume=False, comment="created by temp_cp")
    cp_ref = None
    try:
        # Test create when the ComputePool does not exist.
        cp_ref = compute_pools[cp_name]
        cp_ref.create_or_alter(test_cp)
        # currently it is not possible to create ComputePool as initially suspended using CoA so we suspend it manually
        compute_pools[cp_name].suspend()
        cp_list = compute_pools.iter(like=cp_name)
        result = next(cp_list)
        assert result.name == test_cp.name.upper()
        assert result.instance_family == test_cp.instance_family
        assert result.min_nodes == test_cp.min_nodes
        assert result.max_nodes == test_cp.max_nodes
        assert result.comment == test_cp.comment
        assert result.auto_suspend_secs == 3600
        assert result.auto_resume is False
        assert result.state in ("SUSPENDED", "STOPPING")

        # Make sure that issuing an empty alter doesn't create a malformed SQL
        cp_ref.create_or_alter(test_cp)

        # Test introducing property which was not set before
        test_cp_new_1 = ComputePool(name=cp_name, instance_family=instance_family, min_nodes=1, max_nodes=1,
                                    auto_resume=False, comment="created by temp_cp", auto_suspend_secs=30)
        cp_ref.create_or_alter(test_cp_new_1)
        cp_list = compute_pools.iter(like=cp_name)
        result = next(cp_list)
        assert result.name == test_cp_new_1.name.upper()
        assert result.instance_family == test_cp_new_1.instance_family
        assert result.min_nodes == test_cp_new_1.min_nodes
        assert result.max_nodes == test_cp_new_1.max_nodes
        assert result.comment == test_cp_new_1.comment
        assert result.auto_suspend_secs == test_cp_new_1.auto_suspend_secs
        assert result.auto_resume is False
        assert result.state in ("SUSPENDED", "STOPPING")

        # Test altering the property which we set before
        test_cp_new_2 = ComputePool(name=cp_name, instance_family=instance_family, min_nodes=1, max_nodes=1,
                                    auto_resume=False, comment="new comment", auto_suspend_secs=90)
        cp_ref.create_or_alter(test_cp_new_2)
        cp_list = compute_pools.iter(like=cp_name)
        result = next(cp_list)
        assert result.name == test_cp_new_2.name.upper()
        assert result.instance_family == test_cp_new_2.instance_family
        assert result.min_nodes == test_cp_new_2.min_nodes
        assert result.max_nodes == test_cp_new_2.max_nodes
        assert result.comment == test_cp_new_2.comment
        assert result.auto_suspend_secs == test_cp_new_2.auto_suspend_secs
        assert result.auto_resume is False
        assert result.state in ("SUSPENDED", "STOPPING")

        # Test not providing the property and checking that it is unset now and adding a new property at the same time
        test_cp_new_3 = ComputePool(name=cp_name, instance_family=instance_family, min_nodes=1, max_nodes=1,
                                    auto_resume=False, comment="comment")
        cp_ref.create_or_alter(test_cp_new_3)
        cp_list = compute_pools.iter(like=cp_name)
        result = next(cp_list)
        assert result.name == test_cp_new_3.name.upper()
        assert result.instance_family == test_cp_new_3.instance_family
        assert result.min_nodes == test_cp_new_3.min_nodes
        assert result.max_nodes == test_cp_new_3.max_nodes
        assert result.comment == test_cp_new_3.comment
        assert result.auto_suspend_secs == 3600 # the default value
        assert result.auto_resume is False
        assert result.state in ("SUSPENDED", "STOPPING")


    finally:
        with suppress(NotFoundError):
            cp_ref.drop()
