from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_eval_dataset_json_body_cases_item import UpdateEvalDatasetJsonBodyCasesItem
    from ..models.update_eval_dataset_json_body_scorers_item import UpdateEvalDatasetJsonBodyScorersItem


T = TypeVar("T", bound="UpdateEvalDatasetJsonBody")


@_attrs_define
class UpdateEvalDatasetJsonBody:
    """
    Attributes:
        path (Union[Unset, str]): Renames the dataset. Its cases and experiments follow through the foreign keys, so a
            rename keeps the history it already has.
        summary (Union[Unset, str]): Left out to keep the stored summary; sent as "" to clear it.
        scorers (Union[Unset, List['UpdateEvalDatasetJsonBodyScorersItem']]): Left out to keep the dataset's columns as
            they are; sent to replace them wholesale.
        cases (Union[Unset, List['UpdateEvalDatasetJsonBodyCasesItem']]): The cases as they should stand afterwards: all
            of them, each carrying its id if the dataset already has it. Sent with the rest of an edit so that a rename the
            dataset refuses refuses the case edits with it.
    """

    path: Union[Unset, str] = UNSET
    summary: Union[Unset, str] = UNSET
    scorers: Union[Unset, List["UpdateEvalDatasetJsonBodyScorersItem"]] = UNSET
    cases: Union[Unset, List["UpdateEvalDatasetJsonBodyCasesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        scorers: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.scorers, Unset):
            scorers = []
            for scorers_item_data in self.scorers:
                scorers_item = scorers_item_data.to_dict()

                scorers.append(scorers_item)

        cases: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.cases, Unset):
            cases = []
            for cases_item_data in self.cases:
                cases_item = cases_item_data.to_dict()

                cases.append(cases_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if summary is not UNSET:
            field_dict["summary"] = summary
        if scorers is not UNSET:
            field_dict["scorers"] = scorers
        if cases is not UNSET:
            field_dict["cases"] = cases

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_eval_dataset_json_body_cases_item import UpdateEvalDatasetJsonBodyCasesItem
        from ..models.update_eval_dataset_json_body_scorers_item import UpdateEvalDatasetJsonBodyScorersItem

        d = src_dict.copy()
        path = d.pop("path", UNSET)

        summary = d.pop("summary", UNSET)

        scorers = []
        _scorers = d.pop("scorers", UNSET)
        for scorers_item_data in _scorers or []:
            scorers_item = UpdateEvalDatasetJsonBodyScorersItem.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        cases = []
        _cases = d.pop("cases", UNSET)
        for cases_item_data in _cases or []:
            cases_item = UpdateEvalDatasetJsonBodyCasesItem.from_dict(cases_item_data)

            cases.append(cases_item)

        update_eval_dataset_json_body = cls(
            path=path,
            summary=summary,
            scorers=scorers,
            cases=cases,
        )

        update_eval_dataset_json_body.additional_properties = d
        return update_eval_dataset_json_body

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
