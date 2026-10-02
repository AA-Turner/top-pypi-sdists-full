from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_resource_request import ManagedAgentsSessionResourceRequest





T = TypeVar("T", bound="ManagedAgentsAddSessionResourcesRequest")



@_attrs_define
class ManagedAgentsAddSessionResourcesRequest:
    """ Request body for attaching files to a running session. The files are staged into the sandbox on the session's next
    tool call and are visible to the agent from its next turn.

        Example:
            {'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'mount_path': 'example', 'relative_path':
                'example', 'type': 'file'}]}

        Attributes:
            resources (list[ManagedAgentsSessionResourceRequest] | None | Unset): Files to attach. All-or-nothing: one
                unknown file_id or one path collision refuses the whole batch and attaches nothing.
     """

    resources: list[ManagedAgentsSessionResourceRequest] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_resource_request import ManagedAgentsSessionResourceRequest # noqa: PLC0415
        resources: list[dict[str, Any]] | None | Unset
        if isinstance(self.resources, Unset):
            resources = UNSET
        elif isinstance(self.resources, list):
            resources = []
            for resources_type_0_item_data in self.resources:
                resources_type_0_item = resources_type_0_item_data.to_dict()
                resources.append(resources_type_0_item)


        else:
            resources = self.resources


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if resources is not UNSET:
            field_dict["resources"] = resources

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_resource_request import ManagedAgentsSessionResourceRequest # noqa: PLC0415
        d = dict(src_dict)
        def _parse_resources(data: object) -> list[ManagedAgentsSessionResourceRequest] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                resources_type_0 = []
                _resources_type_0 = data
                for resources_type_0_item_data in (_resources_type_0):
                    resources_type_0_item = ManagedAgentsSessionResourceRequest.from_dict(resources_type_0_item_data)



                    resources_type_0.append(resources_type_0_item)

                return resources_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSessionResourceRequest] | None | Unset, data)

        resources = _parse_resources(d.pop("resources", UNSET))


        managed_agents_add_session_resources_request = cls(
            resources=resources,
        )


        managed_agents_add_session_resources_request.additional_properties = d
        return managed_agents_add_session_resources_request

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
