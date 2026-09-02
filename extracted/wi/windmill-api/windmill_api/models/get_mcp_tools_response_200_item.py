from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_mcp_tools_response_200_item_annotations import GetMcpToolsResponse200ItemAnnotations
    from ..models.get_mcp_tools_response_200_item_input_schema import GetMcpToolsResponse200ItemInputSchema


T = TypeVar("T", bound="GetMcpToolsResponse200Item")


@_attrs_define
class GetMcpToolsResponse200Item:
    """
    Attributes:
        name (str):
        input_schema (GetMcpToolsResponse200ItemInputSchema):
        description (Union[Unset, str]):
        annotations (Union[Unset, GetMcpToolsResponse200ItemAnnotations]):
    """

    name: str
    input_schema: "GetMcpToolsResponse200ItemInputSchema"
    description: Union[Unset, str] = UNSET
    annotations: Union[Unset, "GetMcpToolsResponse200ItemAnnotations"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        input_schema = self.input_schema.to_dict()

        description = self.description
        annotations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.annotations, Unset):
            annotations = self.annotations.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "inputSchema": input_schema,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if annotations is not UNSET:
            field_dict["annotations"] = annotations

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_mcp_tools_response_200_item_annotations import GetMcpToolsResponse200ItemAnnotations
        from ..models.get_mcp_tools_response_200_item_input_schema import GetMcpToolsResponse200ItemInputSchema

        d = src_dict.copy()
        name = d.pop("name")

        input_schema = GetMcpToolsResponse200ItemInputSchema.from_dict(d.pop("inputSchema"))

        description = d.pop("description", UNSET)

        _annotations = d.pop("annotations", UNSET)
        annotations: Union[Unset, GetMcpToolsResponse200ItemAnnotations]
        if isinstance(_annotations, Unset):
            annotations = UNSET
        else:
            annotations = GetMcpToolsResponse200ItemAnnotations.from_dict(_annotations)

        get_mcp_tools_response_200_item = cls(
            name=name,
            input_schema=input_schema,
            description=description,
            annotations=annotations,
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
