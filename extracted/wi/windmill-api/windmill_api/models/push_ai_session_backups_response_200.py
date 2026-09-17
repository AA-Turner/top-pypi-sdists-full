from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.push_ai_session_backups_response_200_results_item import PushAiSessionBackupsResponse200ResultsItem


T = TypeVar("T", bound="PushAiSessionBackupsResponse200")


@_attrs_define
class PushAiSessionBackupsResponse200:
    """
    Attributes:
        enabled (bool):
        results (List['PushAiSessionBackupsResponse200ResultsItem']):
        storage_id (Union[Unset, str]):
        backup_generation (Union[Unset, int]):
        fallback (Union[Unset, bool]):
    """

    enabled: bool
    results: List["PushAiSessionBackupsResponse200ResultsItem"]
    storage_id: Union[Unset, str] = UNSET
    backup_generation: Union[Unset, int] = UNSET
    fallback: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        results = []
        for results_item_data in self.results:
            results_item = results_item_data.to_dict()

            results.append(results_item)

        storage_id = self.storage_id
        backup_generation = self.backup_generation
        fallback = self.fallback

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "results": results,
            }
        )
        if storage_id is not UNSET:
            field_dict["storage_id"] = storage_id
        if backup_generation is not UNSET:
            field_dict["backup_generation"] = backup_generation
        if fallback is not UNSET:
            field_dict["fallback"] = fallback

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.push_ai_session_backups_response_200_results_item import (
            PushAiSessionBackupsResponse200ResultsItem,
        )

        d = src_dict.copy()
        enabled = d.pop("enabled")

        results = []
        _results = d.pop("results")
        for results_item_data in _results:
            results_item = PushAiSessionBackupsResponse200ResultsItem.from_dict(results_item_data)

            results.append(results_item)

        storage_id = d.pop("storage_id", UNSET)

        backup_generation = d.pop("backup_generation", UNSET)

        fallback = d.pop("fallback", UNSET)

        push_ai_session_backups_response_200 = cls(
            enabled=enabled,
            results=results,
            storage_id=storage_id,
            backup_generation=backup_generation,
            fallback=fallback,
        )

        push_ai_session_backups_response_200.additional_properties = d
        return push_ai_session_backups_response_200

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
