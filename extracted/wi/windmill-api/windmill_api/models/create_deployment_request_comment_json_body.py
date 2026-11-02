from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateDeploymentRequestCommentJsonBody")


@_attrs_define
class CreateDeploymentRequestCommentJsonBody:
    """
    Attributes:
        body (str):
        parent_id (Union[Unset, None, int]):
        anchor_kind (Union[Unset, None, str]):
        anchor_path (Union[Unset, None, str]):
    """

    body: str
    parent_id: Union[Unset, None, int] = UNSET
    anchor_kind: Union[Unset, None, str] = UNSET
    anchor_path: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        body = self.body
        parent_id = self.parent_id
        anchor_kind = self.anchor_kind
        anchor_path = self.anchor_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
            }
        )
        if parent_id is not UNSET:
            field_dict["parent_id"] = parent_id
        if anchor_kind is not UNSET:
            field_dict["anchor_kind"] = anchor_kind
        if anchor_path is not UNSET:
            field_dict["anchor_path"] = anchor_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("body")

        parent_id = d.pop("parent_id", UNSET)

        anchor_kind = d.pop("anchor_kind", UNSET)

        anchor_path = d.pop("anchor_path", UNSET)

        create_deployment_request_comment_json_body = cls(
            body=body,
            parent_id=parent_id,
            anchor_kind=anchor_kind,
            anchor_path=anchor_path,
        )

        create_deployment_request_comment_json_body.additional_properties = d
        return create_deployment_request_comment_json_body

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
