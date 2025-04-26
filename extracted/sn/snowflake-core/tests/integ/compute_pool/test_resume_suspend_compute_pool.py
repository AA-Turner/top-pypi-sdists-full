#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.exceptions import APIError


def test_resume_suspend(compute_pools, temp_cp):
    assert compute_pools[temp_cp.name].fetch().state in ("SUSPENDED", "STOPPING")

    compute_pools[temp_cp.name].resume()
    assert compute_pools[temp_cp.name].fetch().state in (
        "IDLE",
        "RUNNING",
        "STARTING",
        "ACTIVE",
    )

    # it's already resumed
    with pytest.raises(
            APIError,
    ):
        compute_pools[temp_cp.name].resume()

    compute_pools[temp_cp.name].suspend()
    assert compute_pools[temp_cp.name].fetch().state in ("SUSPENDED", "STOPPING")

    # suspend when it is already suspended
    compute_pools[temp_cp.name].suspend()
    assert compute_pools[temp_cp.name].fetch().state in ("SUSPENDED", "STOPPING")
