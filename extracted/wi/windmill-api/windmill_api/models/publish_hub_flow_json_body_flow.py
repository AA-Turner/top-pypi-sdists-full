from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_hub_flow_json_body_flow_schema import PublishHubFlowJsonBodyFlowSchema
    from ..models.publish_hub_flow_json_body_flow_value import PublishHubFlowJsonBodyFlowValue


T = TypeVar("T", bound="PublishHubFlowJsonBodyFlow")


@_attrs_define
class PublishHubFlowJsonBodyFlow:
    """
    Attributes:
        summary (str):
        value (PublishHubFlowJsonBodyFlowValue):
        description (Union[Unset, str]):
        schema (Union[Unset, PublishHubFlowJsonBodyFlowSchema]):
    """

    summary: str
    value: "PublishHubFlowJsonBodyFlowValue"
    description: Union[Unset, str] = UNSET
    schema: Union[Unset, "PublishHubFlowJsonBodyFlowSchema"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        summary = self.summary
        value = self.value.to_dict()

        description = self.description
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "summary": summary,
                "value": value,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_hub_flow_json_body_flow_schema import PublishHubFlowJsonBodyFlowSchema
        from ..models.publish_hub_flow_json_body_flow_value import PublishHubFlowJsonBodyFlowValue

        d = src_dict.copy()
        summary = d.pop("summary")

        value = PublishHubFlowJsonBodyFlowValue.from_dict(d.pop("value"))

        description = d.pop("description", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, PublishHubFlowJsonBodyFlowSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = PublishHubFlowJsonBodyFlowSchema.from_dict(_schema)

        publish_hub_flow_json_body_flow = cls(
            summary=summary,
            value=value,
            description=description,
            schema=schema,
        )

        publish_hub_flow_json_body_flow.additional_properties = d
        return publish_hub_flow_json_body_flow

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
