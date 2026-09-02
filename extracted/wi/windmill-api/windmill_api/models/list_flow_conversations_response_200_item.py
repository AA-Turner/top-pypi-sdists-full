import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListFlowConversationsResponse200Item")


@_attrs_define
class ListFlowConversationsResponse200Item:
    """
    Attributes:
        id (str): Unique identifier for the conversation
        workspace_id (str): The workspace ID where the conversation belongs
        flow_path (str): Path of the flow this conversation is for
        created_at (datetime.datetime): When the conversation was created
        updated_at (datetime.datetime): When the conversation was last updated
        created_by (str): Username who created the conversation
        title (Union[Unset, None, str]): Optional title for the conversation
    """

    id: str
    workspace_id: str
    flow_path: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str
    title: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        flow_path = self.flow_path
        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by = self.created_by
        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "workspace_id": workspace_id,
                "flow_path": flow_path,
                "created_at": created_at,
                "updated_at": updated_at,
                "created_by": created_by,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        flow_path = d.pop("flow_path")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        created_by = d.pop("created_by")

        title = d.pop("title", UNSET)

        list_flow_conversations_response_200_item = cls(
            id=id,
            workspace_id=workspace_id,
            flow_path=flow_path,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            title=title,
        )

        list_flow_conversations_response_200_item.additional_properties = d
        return list_flow_conversations_response_200_item

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
