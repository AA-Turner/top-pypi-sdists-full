from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsTestLogAccessRequest")



@_attrs_define
class ManagedAgentsTestLogAccessRequest:
    """ Request for one bounded Google Cloud Logging read through an integration connection. The project and optional filter
    select this check only; they do not restrict the service account's IAM access.

        Example:
            {'filter': 'example', 'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a'}

        Attributes:
            project_id (str): Explicit Google Cloud project ID; not a restriction on the service account's IAM access.
            filter_ (str | Unset): Optional Logging filter, intersected with the last 24 hours.
     """

    project_id: str
    filter_: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        project_id = self.project_id

        filter_ = self.filter_


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "project_id": project_id,
        })
        if filter_ is not UNSET:
            field_dict["filter"] = filter_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project_id = d.pop("project_id")

        filter_ = d.pop("filter", UNSET)

        managed_agents_test_log_access_request = cls(
            project_id=project_id,
            filter_=filter_,
        )


        managed_agents_test_log_access_request.additional_properties = d
        return managed_agents_test_log_access_request

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
