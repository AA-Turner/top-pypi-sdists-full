from abc import ABC, abstractmethod
from typing import Optional

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.tag import TagCollection, TagResource, TagValue

from .fixtures.constants import (
    TEST_SHARED_TAG_VALUE,
)


class BaseTagTests(ABC):
    """Base class for testing tag operations on Snowflake resources.

    This class provides common test methods and helper functions for testing
    tag set/unset/get operations on various Snowflake resources.

    Subclasses must implement abstract methods to provide resource-specific
    configuration and API access.
    """

    @property
    @abstractmethod
    def resource_level_name(self) -> str:
        """Return the level name used in tag lineage (e.g., 'TASK', 'POLICY')."""

    @abstractmethod
    def set_tags(
        self, tags: dict[TagResource, TagValue], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> None:
        """Set tags on the test resource."""

    @abstractmethod
    def unset_tags(
        self, tag_resources: set[TagResource], if_exists: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> None:
        """Unset tags from the test resource."""

    @abstractmethod
    def get_tags(
        self, with_lineage: Optional[bool] = False, resource_name: Optional[str] = None
    ) -> dict[TagResource, TagValue]:
        """Get tag assignments for the test resource."""

    def test_set_tags(self, temp_tag_upper_case: TagResource, tag: TagResource):
        tags = {
            tag: TagValue(value="value"),
            temp_tag_upper_case: TagValue(value="other_value", level="should-be-ignored"),
        }

        self.set_tags(tags)

        expected_tags = {
            tag: TagValue(value="value", level=self.resource_level_name),
            temp_tag_upper_case: TagValue(value="other_value", level=self.resource_level_name),
        }

        fetched_tags = self.get_tags()
        assert fetched_tags == expected_tags

    def test_set_tag_which_does_not_exist(self, tags: TagCollection):
        with pytest.raises(NotFoundError):
            self.set_tags({tags["does_not_exist"]: TagValue(value="value")})

    def test_set_tag_on_resource_which_does_not_exist(self, tag: TagResource):
        tags = {tag: TagValue(value="value")}
        with pytest.raises(NotFoundError):
            self.set_tags(tags, if_exists=False, resource_name="non_existent")

        assert self.set_tags(tags, if_exists=True, resource_name="non_existent") is None

    def test_unset_tag(self, tag: TagResource):
        self.set_tags({tag: TagValue(value="value")})
        assert self.get_tags() == {tag: TagValue(value="value", level=self.resource_level_name)}

        self.unset_tags({tag})
        assert self.get_tags() == {}

    def test_unset_tag_which_does_not_exist(self, tags):
        with pytest.raises(NotFoundError):
            self.unset_tags({tags["does_not_exist"]})

    def test_unset_tag_from_resource_which_does_not_exist(self, tag: TagResource):
        with pytest.raises(NotFoundError):
            self.unset_tags({tag}, if_exists=False, resource_name="non_existent")

        assert self.unset_tags({tag}, if_exists=True, resource_name="non_existent") is None

    def test_get_tags(
        self,
        tag: TagResource,
        shared_account_tag: TagResource,
    ):
        self.set_tags({tag: TagValue(value="value")})

        expected_tags_without_lineage: dict[TagResource, TagValue] = {
            tag: TagValue(
                "value",
                self.resource_level_name,
            )
        }
        tags_without_lineage = self.get_tags(with_lineage=False)
        assert len(tags_without_lineage) == 1, f"Expected 1 tag without lineage, got {len(tags_without_lineage)}"
        assert tags_without_lineage == expected_tags_without_lineage, (
            f"Expected tags {expected_tags_without_lineage} but got {tags_without_lineage}"
        )

        tags_with_lineage = self.get_tags(with_lineage=True)
        expected_tags_with_lineage: dict[TagResource, TagValue] = expected_tags_without_lineage | {
            shared_account_tag: TagValue(
                TEST_SHARED_TAG_VALUE,
                "ACCOUNT",
            ),
        }
        assert len(tags_with_lineage) == 2, f"Expected 2 tags with lineage, got {len(tags_with_lineage)}"
        assert tags_with_lineage == expected_tags_with_lineage, (
            f"Expected tags {expected_tags_with_lineage} but got {tags_with_lineage}"
        )

    def test_get_tags_on_a_resource_which_does_not_exist(self):
        with pytest.raises(NotFoundError):
            self.get_tags(resource_name="non_existent_resource")
