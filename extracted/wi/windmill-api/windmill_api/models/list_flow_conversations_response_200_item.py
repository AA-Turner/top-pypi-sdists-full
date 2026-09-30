import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_flow_conversations_response_200_item_running_turn import (
        ListFlowConversationsResponse200ItemRunningTurn,
    )


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
        is_test (bool): Started from the flow editor's test panel rather than a deployed run
        title (Union[Unset, None, str]): Optional title for the conversation
        running_turn (Union[Unset, None, ListFlowConversationsResponse200ItemRunningTurn]): The turn the conversation is
            still answering, set by the list endpoint: its newest user message, while the flow run it started is queued or
            running. A run into this conversation is refused with 409 until the turn ends.
    """

    id: str
    workspace_id: str
    flow_path: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str
    is_test: bool
    title: Union[Unset, None, str] = UNSET
    running_turn: Union[Unset, None, "ListFlowConversationsResponse200ItemRunningTurn"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        workspace_id = self.workspace_id
        flow_path = self.flow_path
        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        created_by = self.created_by
        is_test = self.is_test
        title = self.title
        running_turn: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.running_turn, Unset):
            running_turn = self.running_turn.to_dict() if self.running_turn else None

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
                "is_test": is_test,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title
        if running_turn is not UNSET:
            field_dict["running_turn"] = running_turn

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_flow_conversations_response_200_item_running_turn import (
            ListFlowConversationsResponse200ItemRunningTurn,
        )

        d = src_dict.copy()
        id = d.pop("id")

        workspace_id = d.pop("workspace_id")

        flow_path = d.pop("flow_path")

        created_at = isoparse(d.pop("created_at"))

        updated_at = isoparse(d.pop("updated_at"))

        created_by = d.pop("created_by")

        is_test = d.pop("is_test")

        title = d.pop("title", UNSET)

        _running_turn = d.pop("running_turn", UNSET)
        running_turn: Union[Unset, None, ListFlowConversationsResponse200ItemRunningTurn]
        if _running_turn is None:
            running_turn = None
        elif isinstance(_running_turn, Unset):
            running_turn = UNSET
        else:
            running_turn = ListFlowConversationsResponse200ItemRunningTurn.from_dict(_running_turn)

        list_flow_conversations_response_200_item = cls(
            id=id,
            workspace_id=workspace_id,
            flow_path=flow_path,
            created_at=created_at,
            updated_at=updated_at,
            created_by=created_by,
            is_test=is_test,
            title=title,
            running_turn=running_turn,
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
