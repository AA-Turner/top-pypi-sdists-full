from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="RunConfigFileClashErrorDtoDetails")



@_attrs_define
class RunConfigFileClashErrorDtoDetails:
    """ Container mount paths shared by the run-config files and problem files.

        Attributes:
            colliding_paths (list[str]): Container paths where a run-config file collides with a problem file.
     """

    colliding_paths: list[str]





    def to_dict(self) -> dict[str, Any]:
        colliding_paths = self.colliding_paths




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "collidingPaths": colliding_paths,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        colliding_paths = cast(list[str], d.pop("collidingPaths"))


        run_config_file_clash_error_dto_details = cls(
            colliding_paths=colliding_paths,
        )

        return run_config_file_clash_error_dto_details

