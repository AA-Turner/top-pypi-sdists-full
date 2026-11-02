from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PushAiSessionBackupsResponse200ResultsItem")


@_attrs_define
class PushAiSessionBackupsResponse200ResultsItem:
    """
    Attributes:
        id (str):
        error (Union[Unset, str]):
        needs_whole (Union[Unset, bool]): nothing was written and the session must be pushed whole again; an incremental
            part found no listed session to ride on (the backup was removed, or a push split over parts is in progress or
            was abandoned), or a later part of a push split over parts found another push had superseded it
    """

    id: str
    error: Union[Unset, str] = UNSET
    needs_whole: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        error = self.error
        needs_whole = self.needs_whole

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error
        if needs_whole is not UNSET:
            field_dict["needs_whole"] = needs_whole

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        error = d.pop("error", UNSET)

        needs_whole = d.pop("needs_whole", UNSET)

        push_ai_session_backups_response_200_results_item = cls(
            id=id,
            error=error,
            needs_whole=needs_whole,
        )

        push_ai_session_backups_response_200_results_item.additional_properties = d
        return push_ai_session_backups_response_200_results_item

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
