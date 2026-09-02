from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.save_eval_case_input import SaveEvalCaseInput


T = TypeVar("T", bound="SaveEvalCase")


@_attrs_define
class SaveEvalCase:
    """
    Attributes:
        id (Union[Unset, str]): Absent for a case the dataset does not hold yet.
        input_ (Union[Unset, SaveEvalCaseInput]): The inputs a standalone run feeds the agent.
        expected (Union[Unset, Any]): Reference output a scorer compares a rerun against.
    """

    id: Union[Unset, str] = UNSET
    input_: Union[Unset, "SaveEvalCaseInput"] = UNSET
    expected: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        input_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        expected = self.expected

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if expected is not UNSET:
            field_dict["expected"] = expected

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.save_eval_case_input import SaveEvalCaseInput

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _input_ = d.pop("input", UNSET)
        input_: Union[Unset, SaveEvalCaseInput]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = SaveEvalCaseInput.from_dict(_input_)

        expected = d.pop("expected", UNSET)

        save_eval_case = cls(
            id=id,
            input_=input_,
            expected=expected,
        )

        save_eval_case.additional_properties = d
        return save_eval_case

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
