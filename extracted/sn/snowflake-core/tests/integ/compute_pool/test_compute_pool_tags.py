from typing import Optional

import pytest

from snowflake.core.compute_pool import ComputePool, ComputePoolCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


pytestmark = [pytest.mark.skip_gov]


class TestComputePoolTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, compute_pools: ComputePoolCollection, instance_family):
        self.compute_pools = compute_pools
        pool_name = random_string(6, "compute_pool_for_tag_tests_")
        compute_pool = ComputePool(
            name=pool_name,
            instance_family=instance_family,
            min_nodes=1,
            max_nodes=1,
            auto_resume=False,
        )
        self.pool_res = compute_pools.create(compute_pool, initially_suspended=True)
        try:
            yield
        finally:
            self.pool_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "COMPUTE_POOL"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.compute_pools[resource_name or self.pool_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.compute_pools[resource_name or self.pool_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.compute_pools[resource_name or self.pool_res.name].get_tags(with_lineage)
