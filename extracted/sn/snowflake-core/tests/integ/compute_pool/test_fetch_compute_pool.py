#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

from snowflake.core.compute_pool import (
    ComputePool,
)
from tests.utils import random_string


def test_fetch(compute_pools, temp_cp, instance_family):
    cp_ref = compute_pools[temp_cp.name]

    # testing with correct instance name
    # check default values
    cp = cp_ref.fetch()
    assert (
        cp.name == temp_cp.name.upper()  # for upper/lower case names
    )
    assert cp.min_nodes == 1
    assert cp.max_nodes == 1
    assert cp.created_on
    assert cp.comment == "created by temp_cp"
    assert not cp.auto_resume
    assert cp.auto_suspend_secs == 3600
    assert cp.num_services is not None
    assert cp.num_jobs is not None
    assert cp.active_nodes is not None
    assert cp.state is not None
    # TODO(SNOW-1707268): Uncomment the line below once the issue is fixed
    # assert cp.idle_nodes is not None
    assert cp.target_nodes is not None
    assert cp.resumed_on is None
    assert cp.updated_on is not None
    assert cp.owner is not None
    assert cp.is_exclusive is not None

    # check the set properties
    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=5,
        comment="created by test_cp",
        auto_resume=True,
        auto_suspend_secs=500,
    )
    try:
        cp_ref = compute_pools.create(test_cp, initially_suspended=True)
        cp = cp_ref.fetch()
        assert cp.name == test_cp.name.upper()
        assert cp.min_nodes == 1
        assert cp.max_nodes == 5
        assert cp.created_on
        assert cp.comment == "created by test_cp"
        assert cp.auto_resume
        assert cp.state in ("SUSPENDED", "STOPPING")
        assert cp.auto_suspend_secs == 500
    finally:
        cp_ref.drop()
