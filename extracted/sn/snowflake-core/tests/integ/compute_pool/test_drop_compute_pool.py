#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.compute_pool import ComputePool
from snowflake.core.exceptions import NotFoundError

from ..utils import random_string


def test_drop(compute_pools, instance_family):
    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name,
        instance_family=instance_family,
        min_nodes=1,
        max_nodes=1,
        auto_resume=False,
    )
    compute_pools.create(test_cp, initially_suspended=True)
    compute_pools[test_cp.name].drop()
    with pytest.raises(
        NotFoundError,
    ):
        compute_pools[test_cp.name].fetch()

    # create again the same cp and drop
    compute_pools.create(test_cp, initially_suspended=True)
    compute_pools[test_cp.name].drop()

    # drop when not exists
    with pytest.raises(
        NotFoundError,
    ):
        compute_pools[test_cp.name].drop()

    # drop when not exists with if_exists
    compute_pools[test_cp.name].drop(if_exists=True)
