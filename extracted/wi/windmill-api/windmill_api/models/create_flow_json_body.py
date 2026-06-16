from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateFlowJsonBody")


@_attrs_define
class CreateFlowJsonBody:
    """
    Attributes:
        deployment_message (Union[Unset, str]):
        skip_draft_deletion (Union[Unset, bool]): When true (set by the CLI / git sync), deploying this flow does not
            delete an existing user draft at the same path.
    """

    deployment_message: Union[Unset, str] = UNSET
    skip_draft_deletion: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        deployment_message = self.deployment_message
        skip_draft_deletion = self.skip_draft_deletion

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if deployment_message is not UNSET:
            field_dict["deployment_message"] = deployment_message
        if skip_draft_deletion is not UNSET:
            field_dict["skip_draft_deletion"] = skip_draft_deletion

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        deployment_message = d.pop("deployment_message", UNSET)

        skip_draft_deletion = d.pop("skip_draft_deletion", UNSET)

        create_flow_json_body = cls(
            deployment_message=deployment_message,
            skip_draft_deletion=skip_draft_deletion,
        )

        create_flow_json_body.additional_properties = d
        return create_flow_json_body

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
