import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_workspace_fairness_events_response_200_item_parameters import (
        GetWorkspaceFairnessEventsResponse200ItemParameters,
    )


T = TypeVar("T", bound="GetWorkspaceFairnessEventsResponse200Item")


@_attrs_define
class GetWorkspaceFairnessEventsResponse200Item:
    """
    Attributes:
        timestamp (datetime.datetime):
        operation (str):
        workspace_id (Union[Unset, None, str]):
        parameters (Union[Unset, None, GetWorkspaceFairnessEventsResponse200ItemParameters]):
    """

    timestamp: datetime.datetime
    operation: str
    workspace_id: Union[Unset, None, str] = UNSET
    parameters: Union[Unset, None, "GetWorkspaceFairnessEventsResponse200ItemParameters"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        timestamp = self.timestamp.isoformat()

        operation = self.operation
        workspace_id = self.workspace_id
        parameters: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.parameters, Unset):
            parameters = self.parameters.to_dict() if self.parameters else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "timestamp": timestamp,
                "operation": operation,
            }
        )
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if parameters is not UNSET:
            field_dict["parameters"] = parameters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_workspace_fairness_events_response_200_item_parameters import (
            GetWorkspaceFairnessEventsResponse200ItemParameters,
        )

        d = src_dict.copy()
        timestamp = isoparse(d.pop("timestamp"))

        operation = d.pop("operation")

        workspace_id = d.pop("workspace_id", UNSET)

        _parameters = d.pop("parameters", UNSET)
        parameters: Union[Unset, None, GetWorkspaceFairnessEventsResponse200ItemParameters]
        if _parameters is None:
            parameters = None
        elif isinstance(_parameters, Unset):
            parameters = UNSET
        else:
            parameters = GetWorkspaceFairnessEventsResponse200ItemParameters.from_dict(_parameters)

        get_workspace_fairness_events_response_200_item = cls(
            timestamp=timestamp,
            operation=operation,
            workspace_id=workspace_id,
            parameters=parameters,
        )

        get_workspace_fairness_events_response_200_item.additional_properties = d
        return get_workspace_fairness_events_response_200_item

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
