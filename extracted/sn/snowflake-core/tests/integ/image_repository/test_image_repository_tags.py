from typing import Optional

import pytest

from snowflake.core import CreateMode
from snowflake.core.image_repository import ImageRepository, ImageRepositoryCollection
from snowflake.core.tag import TagResource, TagValue

from ..base_tag_tests import BaseTagTests
from ..utils import random_string


class TestImageRepositoryTags(BaseTagTests):
    @pytest.fixture(autouse=True)
    def setup(self, image_repositories: ImageRepositoryCollection):
        self.image_repositories = image_repositories
        image_repo_name = random_string(6, "image_repo_for_tag_tests_")
        image_repo = ImageRepository(name=image_repo_name)
        self.image_repo_res = image_repositories.create(image_repo, mode=CreateMode.if_not_exists)
        try:
            yield
        finally:
            self.image_repo_res.drop(if_exists=True)

    @property
    def resource_level_name(self) -> str:
        return "IMAGE_REPOSITORY"

    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.image_repositories[resource_name or self.image_repo_res.name].set_tags(tags, if_exists)

    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ):
        self.image_repositories[resource_name or self.image_repo_res.name].unset_tags(tag_resources, if_exists)

    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        return self.image_repositories[resource_name or self.image_repo_res.name].get_tags(with_lineage)
