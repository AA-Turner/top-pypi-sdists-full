from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_eval_dataset_json_body_cases_item_input import CreateEvalDatasetJsonBodyCasesItemInput


T = TypeVar("T", bound="CreateEvalDatasetJsonBodyCasesItem")


@_attrs_define
class CreateEvalDatasetJsonBodyCasesItem:
    """
    Attributes:
        input_ (Union[Unset, CreateEvalDatasetJsonBodyCasesItemInput]): The inputs a standalone run feeds the agent.
        expected (Union[Unset, Any]): Reference output a scorer compares a rerun against.
    """

    input_: Union[Unset, "CreateEvalDatasetJsonBodyCasesItemInput"] = UNSET
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
        from ..models.create_eval_dataset_json_body_cases_item_input import CreateEvalDatasetJsonBodyCasesItemInput

        d = src_dict.copy()
        _input_ = d.pop("input", UNSET)
        input_: Union[Unset, CreateEvalDatasetJsonBodyCasesItemInput]
        if isinstance(_input_, Unset):
            input_ = UNSET
        else:
            input_ = CreateEvalDatasetJsonBodyCasesItemInput.from_dict(_input_)

        expected = d.pop("expected", UNSET)

        create_eval_dataset_json_body_cases_item = cls(
            input_=input_,
            expected=expected,
        )

        create_eval_dataset_json_body_cases_item.additional_properties = d
        return create_eval_dataset_json_body_cases_item

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
