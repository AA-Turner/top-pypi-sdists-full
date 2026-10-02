from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount")



@_attrs_define
class DuplicateEnvironmentResultDtoRunFieldConfigAttemptCount:
    """ Per-field config for the attempt-count input on the Run problem modal.

        Attributes:
            default (int | None): Default number of attempts pre-filled in the Run problem modal. Null leaves the field
                empty.
     """

    default: int | None





    def to_dict(self) -> dict[str, Any]:
        default: int | None
        default = self.default


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "default": default,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_default(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        default = _parse_default(d.pop("default"))


        duplicate_environment_result_dto_run_field_config_attempt_count = cls(
            default=default,
        )

        return duplicate_environment_result_dto_run_field_config_attempt_count

