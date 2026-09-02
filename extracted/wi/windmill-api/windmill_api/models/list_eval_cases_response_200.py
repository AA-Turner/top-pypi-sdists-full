from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.list_eval_cases_response_200_cases_item import ListEvalCasesResponse200CasesItem


T = TypeVar("T", bound="ListEvalCasesResponse200")


@_attrs_define
class ListEvalCasesResponse200:
    """
    Attributes:
        cases (List['ListEvalCasesResponse200CasesItem']):
    """

    cases: List["ListEvalCasesResponse200CasesItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        cases = []
        for cases_item_data in self.cases:
            cases_item = cases_item_data.to_dict()

            cases.append(cases_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cases": cases,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_eval_cases_response_200_cases_item import ListEvalCasesResponse200CasesItem

        d = src_dict.copy()
        cases = []
        _cases = d.pop("cases")
        for cases_item_data in _cases:
            cases_item = ListEvalCasesResponse200CasesItem.from_dict(cases_item_data)

            cases.append(cases_item)

        list_eval_cases_response_200 = cls(
            cases=cases,
        )

        list_eval_cases_response_200.additional_properties = d
        return list_eval_cases_response_200

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
