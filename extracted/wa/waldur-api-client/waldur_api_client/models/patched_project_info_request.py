from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedProjectInfoRequest")


@_attrs_define
class PatchedProjectInfoRequest:
    """
    Attributes:
        project (Union[Unset, str]):
        shortname (Union[None, Unset, str]): A short, unique name for the project. It will be used to form the local
            username of any users in the project on any systems. Should only contain lower-case letters and digits and must
            start with a letter.
        allowed_destinations (Union[None, Unset, str]): A comma-separated list of allowable destinations of instances
            that              can be attached to this project. For example, a project may only allow
            'brics.aip1.*', meaning that only instances that start with 'brics.aip1.'              can be attached to this
            project.
    """

    project: Union[Unset, str] = UNSET
    shortname: Union[None, Unset, str] = UNSET
    allowed_destinations: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = self.project

        shortname: Union[None, Unset, str]
        if isinstance(self.shortname, Unset):
            shortname = UNSET
        else:
            shortname = self.shortname

        allowed_destinations: Union[None, Unset, str]
        if isinstance(self.allowed_destinations, Unset):
            allowed_destinations = UNSET
        else:
            allowed_destinations = self.allowed_destinations

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if project is not UNSET:
            field_dict["project"] = project
        if shortname is not UNSET:
            field_dict["shortname"] = shortname
        if allowed_destinations is not UNSET:
            field_dict["allowed_destinations"] = allowed_destinations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = d.pop("project", UNSET)

        def _parse_shortname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        shortname = _parse_shortname(d.pop("shortname", UNSET))

        def _parse_allowed_destinations(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        allowed_destinations = _parse_allowed_destinations(d.pop("allowed_destinations", UNSET))

        patched_project_info_request = cls(
            project=project,
            shortname=shortname,
            allowed_destinations=allowed_destinations,
        )

        patched_project_info_request.additional_properties = d
        return patched_project_info_request

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
