import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.list_eval_cases_response_200_cases_item_input import ListEvalCasesResponse200CasesItemInput


T = TypeVar("T", bound="ListEvalCasesResponse200CasesItem")


@_attrs_define
class ListEvalCasesResponse200CasesItem:
    """
    Attributes:
        id (str):
        created_at (datetime.datetime):
        created_by (str):
        input_ (Union[Unset, ListEvalCasesResponse200CasesItemInput]): The inputs a standalone run feeds the agent.
        expected (Union[Unset, Any]): Reference output a scorer compares a rerun against.
    """

    id: str
    created_at: datetime.datetime
    created_by: str
    input_: Union[Unset, "ListEvalCasesResponse200CasesItemInput"] = UNSET
    expected: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        created_at = self.created_at.isoformat()

        created_by = self.created_by
        input_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        expected = self.expected

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "created_at": created_at,
                "created_by": created_by,
            }
        )
        if input_ is not UNSET:
            field_dict["input"] = input_
        if expected is not UNSET:
            field_dict["expected"] = expected

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.list_eval_cases_response_200_cases_item_input import ListEvalCasesResponse200CasesItemInput

        d = src_dict.copy()
        id = d.pop("id")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        _input_ = d.pop("input", UNSET)
        input_: Union[Unset, ListEvalCasesResponse200CasesItemInput]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = ListEvalCasesResponse200CasesItemInput.from_dict(_input_)

        expected = d.pop("expected", UNSET)

        list_eval_cases_response_200_cases_item = cls(
            id=id,
            created_at=created_at,
            created_by=created_by,
            input_=input_,
            expected=expected,
        )

        list_eval_cases_response_200_cases_item.additional_properties = d
        return list_eval_cases_response_200_cases_item

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
