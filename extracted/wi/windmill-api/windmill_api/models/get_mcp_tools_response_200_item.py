from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_mcp_tools_response_200_item_parameters import GetMcpToolsResponse200ItemParameters


T = TypeVar("T", bound="GetMcpToolsResponse200Item")


@_attrs_define
class GetMcpToolsResponse200Item:
    """
    Attributes:
        name (str):
        parameters (GetMcpToolsResponse200ItemParameters):
        description (Union[Unset, str]):
    """

    name: str
    parameters: "GetMcpToolsResponse200ItemParameters"
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        parameters = self.parameters.to_dict()

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "parameters": parameters,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_mcp_tools_response_200_item_parameters import GetMcpToolsResponse200ItemParameters

        d = src_dict.copy()
        name = d.pop("name")

        parameters = GetMcpToolsResponse200ItemParameters.from_dict(d.pop("parameters"))

        description = d.pop("description", UNSET)

        get_mcp_tools_response_200_item = cls(
            name=name,
            parameters=parameters,
            description=description,
        )

        get_mcp_tools_response_200_item.additional_properties = d
        return get_mcp_tools_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
