from typing import (
    Any,
    Dict,
    List,
    Type,
    TypeVar,
    Union,
)

import attr

from ..types import UNSET, Unset
from ..models.processing_status_code import ProcessingStatusCode


T = TypeVar("T", bound="ChildProcessingStatus")


@attr.s(auto_attribs=True)
class ChildProcessingStatus:
    """
    Status reported by a child processor in the pipeline.

    A subset of ProcessingStatus fields relevant to individual processor outcomes.
    All fields are optional to support cases where the child entity cannot be
    fully identified (e.g., missing fragments known only by index).

    ### Attributes:
    * `entity_id (Union[Unset, str])`: Identifier of the child entity
    * `entity_type (Union[Unset, str])`: Type of the entity
    * `entity_label (Union[Unset, str])`: Human-readable label for the entity
    * `status_code (Union[Unset, ProcessingStatusCode])`: Processing status code
    * `reason (Union[Unset, str])`: Reason for the status
    * `timestamp (Union[Unset, str])`: ISO timestamp when status was reported
    """

    entity_id: Union[Unset, str] = UNSET
    entity_type: Union[Unset, str] = UNSET
    entity_label: Union[Unset, str] = UNSET
    status_code: Union[Unset, ProcessingStatusCode] = UNSET
    reason: Union[Unset, str] = UNSET
    timestamp: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self.entity_id
        entity_type = self.entity_type
        entity_label = self.entity_label

        status_code: Union[Unset, str] = UNSET
        if not isinstance(self.status_code, Unset):
            status_code = self.status_code.value

        reason = self.reason
        timestamp = self.timestamp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        if entity_id is not UNSET:
            field_dict["entity_id"] = entity_id
        if entity_type is not UNSET:
            field_dict["entity_type"] = entity_type
        if entity_label is not UNSET:
            field_dict["entity_label"] = entity_label
        if status_code is not UNSET:
            field_dict["status_code"] = status_code
        if reason is not UNSET:
            field_dict["reason"] = reason
        if timestamp is not UNSET:
            field_dict["timestamp"] = timestamp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        entity_id = d.pop("entity_id", UNSET)

        entity_type = d.pop("entity_type", UNSET)
        entity_label = d.pop("entity_label", UNSET)

        _status_code = d.pop("status_code", UNSET)
        status_code: Union[Unset, ProcessingStatusCode]
        if isinstance(_status_code, Unset):
            status_code = UNSET
        else:
            status_code = ProcessingStatusCode(_status_code)

        reason = d.pop("reason", UNSET)
        timestamp = d.pop("timestamp", UNSET)

        child_processing_status = cls(
            entity_id=entity_id,
            entity_type=entity_type,
            entity_label=entity_label,
            status_code=status_code,
            reason=reason,
            timestamp=timestamp,
        )

        child_processing_status.additional_properties = d
        return child_processing_status

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
