from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.environment_with_counts_page_dto_items_item_run_field_config_attempt_count import EnvironmentWithCountsPageDtoItemsItemRunFieldConfigAttemptCount





T = TypeVar("T", bound="EnvironmentWithCountsPageDtoItemsItemRunFieldConfig")



@_attrs_define
class EnvironmentWithCountsPageDtoItemsItemRunFieldConfig:
    """ Default attempt count for the Run problem modal. Image and model policy is governed by run-config bindings and
    curated menus.

        Attributes:
            attempt_count (EnvironmentWithCountsPageDtoItemsItemRunFieldConfigAttemptCount): Per-field config for the
                attempt-count input on the Run problem modal.
     """

    attempt_count: EnvironmentWithCountsPageDtoItemsItemRunFieldConfigAttemptCount





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_with_counts_page_dto_items_item_run_field_config_attempt_count import EnvironmentWithCountsPageDtoItemsItemRunFieldConfigAttemptCount # noqa: PLC0415
        attempt_count = self.attempt_count.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "attemptCount": attempt_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_with_counts_page_dto_items_item_run_field_config_attempt_count import EnvironmentWithCountsPageDtoItemsItemRunFieldConfigAttemptCount # noqa: PLC0415
        d = dict(src_dict)
        attempt_count = EnvironmentWithCountsPageDtoItemsItemRunFieldConfigAttemptCount.from_dict(d.pop("attemptCount"))




        environment_with_counts_page_dto_items_item_run_field_config = cls(
            attempt_count=attempt_count,
        )

        return environment_with_counts_page_dto_items_item_run_field_config

