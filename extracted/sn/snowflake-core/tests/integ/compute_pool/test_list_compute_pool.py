#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import datetime

import pytest

from pydantic_core._pydantic_core import ValidationError


@pytest.mark.usefixtures("qa_mode_enabled")
def test_iter(compute_pools, temp_cp, instance_family):
    for cp in compute_pools.iter(like=temp_cp.name):
        assert cp.name == temp_cp.name.upper()
        assert cp.instance_family == instance_family.upper()
        assert cp.min_nodes == 1
        assert cp.max_nodes == 1
        assert not cp.auto_resume
        assert cp.comment == "created by temp_cp"
        assert cp.state in ("SUSPENDED", "STOPPING")
        assert cp.num_services == 0
        assert cp.num_jobs == 0
        assert cp.auto_suspend_secs == 600
        assert cp.active_nodes == 0
        assert cp.idle_nodes is None
        assert cp.target_nodes == 1
        assert cp.created_on == datetime.datetime(1967, 6, 23, 7, 0, 0, 123000, tzinfo=datetime.timezone.utc)
        assert cp.resumed_on == datetime.datetime(1967, 6, 23, 7, 0, 0, 123000, tzinfo=datetime.timezone.utc)
        assert cp.updated_on == datetime.datetime(1967, 6, 23, 7, 0, 0, 123000, tzinfo=datetime.timezone.utc)
        assert cp.owner == "ACCOUNTADMIN"
        assert cp.is_exclusive is False
        assert cp.application is None
        assert cp.budget is None

    compute_pools_names = [cp.name for cp in compute_pools.iter(like="test_%")]
    assert temp_cp.name.upper() in compute_pools_names

    compute_pools_names = [cp.name for cp in compute_pools.iter(starts_with="test_")]
    assert temp_cp.name.upper() not in compute_pools_names

    compute_pools_names = [cp.name for cp in compute_pools.iter(starts_with="TEST_")]
    assert temp_cp.name.upper() in compute_pools_names


def test_iter_limit(compute_pools):
    with pytest.raises(
        ValidationError,
    ):
        assert len(compute_pools.iter(starts_with="TEST_", limit=0)) == 0

    compute_pools_names = [cp.name for cp in compute_pools.iter(starts_with="TEST_", limit=1)]
    assert len(compute_pools_names) <= 1

    with pytest.raises(
        ValidationError,
    ):
        compute_pools.iter(starts_with="TEST_", limit=10001)
