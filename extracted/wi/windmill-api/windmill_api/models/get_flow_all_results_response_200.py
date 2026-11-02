from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_flow_all_results_response_200_entries_item import GetFlowAllResultsResponse200EntriesItem


T = TypeVar("T", bound="GetFlowAllResultsResponse200")


@_attrs_define
class GetFlowAllResultsResponse200:
    """
    Attributes:
        entries (List['GetFlowAllResultsResponse200EntriesItem']):
        enclosing_job (Union[Unset, str]): set when the requested job is itself a step of a larger flow run; id of the
            flow run directly enclosing it
        truncated (Union[Unset, bool]): true when the tree has more jobs than the entry cap; entries then hold the
            depth-first prefix
        scope_filtered (Union[Unset, bool]): true when the caller's token is tag-scoped; steps running on other tags are
            omitted
        step_error (Union[Unset, str]): set when step was provided but could not be resolved; a diagnostic listing
            available step ids or iteration statuses
    """

    entries: List["GetFlowAllResultsResponse200EntriesItem"]
    enclosing_job: Union[Unset, str] = UNSET
    truncated: Union[Unset, bool] = UNSET
    scope_filtered: Union[Unset, bool] = UNSET
    step_error: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        entries = []
        for entries_item_data in self.entries:
            entries_item = entries_item_data.to_dict()

            entries.append(entries_item)

        enclosing_job = self.enclosing_job
        truncated = self.truncated
        scope_filtered = self.scope_filtered
        step_error = self.step_error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entries": entries,
            }
        )
        if enclosing_job is not UNSET:
            field_dict["enclosing_job"] = enclosing_job
        if truncated is not UNSET:
            field_dict["truncated"] = truncated
        if scope_filtered is not UNSET:
            field_dict["scope_filtered"] = scope_filtered
        if step_error is not UNSET:
            field_dict["step_error"] = step_error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_flow_all_results_response_200_entries_item import GetFlowAllResultsResponse200EntriesItem

        d = src_dict.copy()
        entries = []
        _entries = d.pop("entries")
        for entries_item_data in _entries:
            entries_item = GetFlowAllResultsResponse200EntriesItem.from_dict(entries_item_data)

            entries.append(entries_item)

        enclosing_job = d.pop("enclosing_job", UNSET)

        truncated = d.pop("truncated", UNSET)

        scope_filtered = d.pop("scope_filtered", UNSET)

        step_error = d.pop("step_error", UNSET)

        get_flow_all_results_response_200 = cls(
            entries=entries,
            enclosing_job=enclosing_job,
            truncated=truncated,
            scope_filtered=scope_filtered,
            step_error=step_error,
        )

        get_flow_all_results_response_200.additional_properties = d
        return get_flow_all_results_response_200

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
