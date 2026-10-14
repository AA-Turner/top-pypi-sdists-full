from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectGroupGidRequest")


@_attrs_define
class ProjectGroupGidRequest:
    """
    Attributes:
        gid (int):
        allow_outside_range (Union[Unset, bool]): Accept a GID outside the range project groups draw from, e.g. one a
            directory assigned before Waldur managed it. Default: False.
    """

    gid: int
    allow_outside_range: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gid = self.gid

        allow_outside_range = self.allow_outside_range

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gid": gid,
            }
        )
        if allow_outside_range is not UNSET:
            field_dict["allow_outside_range"] = allow_outside_range

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gid = d.pop("gid")

        allow_outside_range = d.pop("allow_outside_range", UNSET)

        project_group_gid_request = cls(
            gid=gid,
            allow_outside_range=allow_outside_range,
        )

        project_group_gid_request.additional_properties = d
        return project_group_gid_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
