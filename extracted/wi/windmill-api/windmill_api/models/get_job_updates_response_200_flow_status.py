from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_job_updates_response_200_flow_status_additional_property import (
        GetJobUpdatesResponse200FlowStatusAdditionalProperty,
    )


T = TypeVar("T", bound="GetJobUpdatesResponse200FlowStatus")


@_attrs_define
class GetJobUpdatesResponse200FlowStatus:
    """ """

    additional_properties: Dict[str, "GetJobUpdatesResponse200FlowStatusAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_job_updates_response_200_flow_status_additional_property import (
            GetJobUpdatesResponse200FlowStatusAdditionalProperty,
        )

        d = src_dict.copy()
        get_job_updates_response_200_flow_status = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = GetJobUpdatesResponse200FlowStatusAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        get_job_updates_response_200_flow_status.additional_properties = additional_properties
        return get_job_updates_response_200_flow_status

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "GetJobUpdatesResponse200FlowStatusAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "GetJobUpdatesResponse200FlowStatusAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
