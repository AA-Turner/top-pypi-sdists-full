from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.duplicate_environment_result_dto_run_field_config_attempt_count import DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount





T = TypeVar("T", bound="DuplicateEnvironmentResultDtoRunFieldConfig")



@_attrs_define
class DuplicateEnvironmentResultDtoRunFieldConfig:
    """ Default attempt count for the Run problem modal. Image and model policy is governed by run-config bindings and
    curated menus.

        Attributes:
            attempt_count (DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount): Per-field config for the attempt-count
                input on the Run problem modal.
     """

    attempt_count: DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount





    def to_dict(self) -> dict[str, Any]:
        from ..models.duplicate_environment_result_dto_run_field_config_attempt_count import DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount # noqa: PLC0415
        attempt_count = self.attempt_count.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "attemptCount": attempt_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.duplicate_environment_result_dto_run_field_config_attempt_count import DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount # noqa: PLC0415
        d = dict(src_dict)
        attempt_count = DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount.from_dict(d.pop("attemptCount"))




        duplicate_environment_result_dto_run_field_config = cls(
            attempt_count=attempt_count,
        )

        return duplicate_environment_result_dto_run_field_config

