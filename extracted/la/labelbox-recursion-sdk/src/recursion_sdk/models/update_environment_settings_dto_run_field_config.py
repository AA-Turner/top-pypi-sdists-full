from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.update_environment_settings_dto_run_field_config_attempt_count import UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount





T = TypeVar("T", bound="UpdateEnvironmentSettingsDtoRunFieldConfig")



@_attrs_define
class UpdateEnvironmentSettingsDtoRunFieldConfig:
    """ Full replacement of the attempt-count default for the Run problem modal. Omit to leave unchanged.

        Attributes:
            attempt_count (UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount): Per-field config for the attempt-count
                input on the Run problem modal.
     """

    attempt_count: UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_environment_settings_dto_run_field_config_attempt_count import UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount # noqa: PLC0415
        attempt_count = self.attempt_count.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "attemptCount": attempt_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_environment_settings_dto_run_field_config_attempt_count import UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount # noqa: PLC0415
        d = dict(src_dict)
        attempt_count = UpdateEnvironmentSettingsDtoRunFieldConfigAttemptCount.from_dict(d.pop("attemptCount"))




        update_environment_settings_dto_run_field_config = cls(
            attempt_count=attempt_count,
        )

        return update_environment_settings_dto_run_field_config

