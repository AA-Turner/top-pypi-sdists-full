from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_eval_case_input import NewEvalCaseInput


T = TypeVar("T", bound="NewEvalCase")


@_attrs_define
class NewEvalCase:
    """
    Attributes:
        input_ (Union[Unset, NewEvalCaseInput]): The inputs a standalone run feeds the agent.
        expected (Union[Unset, Any]): Reference output a scorer compares a rerun against.
    """

    input_: Union[Unset, "NewEvalCaseInput"] = UNSET
    expected: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        expected = self.expected

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_ is not UNSET:
            field_dict["input"] = input_
        if expected is not UNSET:
            field_dict["expected"] = expected

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_eval_case_input import NewEvalCaseInput

        d = src_dict.copy()
        _input_ = d.pop("input", UNSET)
        input_: Union[Unset, NewEvalCaseInput]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = NewEvalCaseInput.from_dict(_input_)

        expected = d.pop("expected", UNSET)

        new_eval_case = cls(
            input_=input_,
            expected=expected,
        )

        new_eval_case.additional_properties = d
        return new_eval_case

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
