import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_capture_response_200_trigger_kind import GetCaptureResponse200TriggerKind

T = TypeVar("T", bound="GetCaptureResponse200")


@_attrs_define
class GetCaptureResponse200:
    """
    Attributes:
        trigger_kind (GetCaptureResponse200TriggerKind):
        main_args (Any):
        preprocessor_args (Any):
        id (int):
        created_at (datetime.datetime):
    """

    trigger_kind: GetCaptureResponse200TriggerKind
    main_args: Any
    preprocessor_args: Any
    id: int
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trigger_kind = self.trigger_kind.value

        main_args = self.main_args
        preprocessor_args = self.preprocessor_args
        id = self.id
        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger_kind": trigger_kind,
                "main_args": main_args,
                "preprocessor_args": preprocessor_args,
                "id": id,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trigger_kind = GetCaptureResponse200TriggerKind(d.pop("trigger_kind"))

        main_args = d.pop("main_args")

        preprocessor_args = d.pop("preprocessor_args")

        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        get_capture_response_200 = cls(
            trigger_kind=trigger_kind,
            main_args=main_args,
            preprocessor_args=preprocessor_args,
            id=id,
            created_at=created_at,
        )

        get_capture_response_200.additional_properties = d
        return get_capture_response_200

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
