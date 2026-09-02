import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.list_trigger_history_response_200_item_operation import ListTriggerHistoryResponse200ItemOperation
from ..models.list_trigger_history_response_200_item_source import ListTriggerHistoryResponse200ItemSource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_trigger_history_response_200_item_changes import ListTriggerHistoryResponse200ItemChanges


T = TypeVar("T", bound="ListTriggerHistoryResponse200Item")


@_attrs_define
class ListTriggerHistoryResponse200Item:
    """
    Attributes:
        id (int):
        trigger_kind (str): 'schedule' or a trigger type (http, kafka, ...)
        path (str):
        operation (ListTriggerHistoryResponse200ItemOperation):
        source (ListTriggerHistoryResponse200ItemSource): The kind of client the change came from. `worker` means the
            server disabled the trigger on its own after a failure.
        created_at (datetime.datetime):
        username (Union[Unset, None, str]): Unset when the server acted on its own.
        changes (Union[Unset, None, ListTriggerHistoryResponse200ItemChanges]): {field: {old, new}} for the fields that
            actually changed. Unset for a delete.
    """

    id: int
    trigger_kind: str
    path: str
    operation: ListTriggerHistoryResponse200ItemOperation
    source: ListTriggerHistoryResponse200ItemSource
    created_at: datetime.datetime
    username: Union[Unset, None, str] = UNSET
    changes: Union[Unset, None, "ListTriggerHistoryResponse200ItemChanges"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        trigger_kind = self.trigger_kind
        path = self.path
        operation = self.operation.value

        source = self.source.value

        created_at = self.created_at.isoformat()

        username = self.username
        changes: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.changes, Unset):
            changes = self.changes.to_dict() if self.changes else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "trigger_kind": trigger_kind,
                "path": path,
                "operation": operation,
                "source": source,
                "created_at": created_at,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if changes is not UNSET:
            field_dict["changes"] = changes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_trigger_history_response_200_item_changes import ListTriggerHistoryResponse200ItemChanges

        d = src_dict.copy()
        id = d.pop("id")

        trigger_kind = d.pop("trigger_kind")

        path = d.pop("path")

        operation = ListTriggerHistoryResponse200ItemOperation(d.pop("operation"))

        source = ListTriggerHistoryResponse200ItemSource(d.pop("source"))

        created_at = isoparse(d.pop("created_at"))

        username = d.pop("username", UNSET)

        _changes = d.pop("changes", UNSET)
        changes: Union[Unset, None, ListTriggerHistoryResponse200ItemChanges]
        if _changes is None:
            changes = None
        elif isinstance(_changes, Unset):
            changes = UNSET
        else:
            changes = ListTriggerHistoryResponse200ItemChanges.from_dict(_changes)

        list_trigger_history_response_200_item = cls(
            id=id,
            trigger_kind=trigger_kind,
            path=path,
            operation=operation,
            source=source,
            created_at=created_at,
            username=username,
            changes=changes,
        )

        list_trigger_history_response_200_item.additional_properties = d
        return list_trigger_history_response_200_item

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
