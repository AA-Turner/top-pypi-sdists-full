#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.compute_pool import (
    ComputePool,
)
from snowflake.core.exceptions import APIError, ConflictError
from tests.utils import random_string


def test_create_compute_pool(compute_pools, instance_family):
    cp_name = random_string(5, "test_cp_case_sensitiv_")
    cp_name = f'"{cp_name}"'
    test_cp = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=1,
        auto_resume=False,
        comment="created by temp_cp",
    )

    # case-sensitive name for compute pools is not supported
    with pytest.raises(APIError):
        compute_pools.create(test_cp, initially_suspended=True)

    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=1,
        auto_resume=False,
        comment="created by temp_cp",
    )
    try:
        cp_ref = compute_pools.create(test_cp, initially_suspended=True)
        cp = cp_ref.fetch()
        assert (
            cp.name == test_cp.name.upper()  # for upper/lower case names
        )

        cp_ref = compute_pools.create(test_cp, mode=CreateMode.if_not_exists, initially_suspended=True)

        with pytest.raises(ConflictError):
            compute_pools.create(test_cp, initially_suspended=True)
    finally:
        if cp_ref:
            cp_ref.drop()


def test_create_from_fetch_compute_pool(compute_pools, instance_family):
    try:
        cp_name = random_string(5, "test_cp_")
        test_cp = ComputePool(
            name=cp_name,
            instance_family=instance_family,
            min_nodes=1,
            max_nodes=1,
            auto_resume=False,
            comment="created by temp_cp",
        )
        cp_ref = compute_pools.create(test_cp, initially_suspended=True)
        fetched_cp_ref = cp_ref.fetch()
        fetched_cp_ref.name = random_string(5, "test_cp_")
        cp_ref_2 = compute_pools.create(fetched_cp_ref, initially_suspended=True)
    finally:
        if cp_ref:
            cp_ref.drop()
        if cp_ref_2:
            cp_ref_2.drop()


def test_create_not_initially_suspended(compute_pools, instance_family):
    cp_name = random_string(5, "test_cp_")
    test_cp1 = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=1,
        auto_resume=False,
        comment="created by temp_cp",
    )
    try:
        cp_ref = compute_pools.create(test_cp1, mode=CreateMode.or_replace, initially_suspended=False)
        cp = cp_ref.fetch()
        assert cp.state in ("STARTING", "STOPPING")
    finally:
        cp_ref.drop()
