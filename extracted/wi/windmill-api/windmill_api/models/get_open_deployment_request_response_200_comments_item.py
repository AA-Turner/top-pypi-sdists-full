import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetOpenDeploymentRequestResponse200CommentsItem")


@_attrs_define
class GetOpenDeploymentRequestResponse200CommentsItem:
    """
    Attributes:
        id (int):
        author (str):
        author_email (str):
        body (str):
        obsolete (bool):
        created_at (datetime.datetime):
        parent_id (Union[Unset, None, int]):
        anchor_kind (Union[Unset, None, str]):
        anchor_path (Union[Unset, None, str]):
    """

    id: int
    author: str
    author_email: str
    body: str
    obsolete: bool
    created_at: datetime.datetime
    parent_id: Union[Unset, None, int] = UNSET
    anchor_kind: Union[Unset, None, str] = UNSET
    anchor_path: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        author = self.author
        author_email = self.author_email
        body = self.body
        obsolete = self.obsolete
        created_at = self.created_at.isoformat()

        parent_id = self.parent_id
        anchor_kind = self.anchor_kind
        anchor_path = self.anchor_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "author": author,
                "author_email": author_email,
                "body": body,
                "obsolete": obsolete,
                "created_at": created_at,
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
        id = d.pop("id")

        author = d.pop("author")

        author_email = d.pop("author_email")

        body = d.pop("body")

        obsolete = d.pop("obsolete")

        created_at = isoparse(d.pop("created_at"))

        parent_id = d.pop("parent_id", UNSET)

        anchor_kind = d.pop("anchor_kind", UNSET)

        anchor_path = d.pop("anchor_path", UNSET)

        get_open_deployment_request_response_200_comments_item = cls(
            id=id,
            author=author,
            author_email=author_email,
            body=body,
            obsolete=obsolete,
            created_at=created_at,
            parent_id=parent_id,
            anchor_kind=anchor_kind,
            anchor_path=anchor_path,
        )

        get_open_deployment_request_response_200_comments_item.additional_properties = d
        return get_open_deployment_request_response_200_comments_item

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
