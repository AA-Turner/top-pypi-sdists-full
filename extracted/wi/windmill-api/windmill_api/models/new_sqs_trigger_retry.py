from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.new_sqs_trigger_retry_constant import NewSqsTriggerRetryConstant
    from ..models.new_sqs_trigger_retry_exponential import NewSqsTriggerRetryExponential


T = TypeVar("T", bound="NewSqsTriggerRetry")


@_attrs_define
class NewSqsTriggerRetry:
    """
    Attributes:
        constant (Union[Unset, NewSqsTriggerRetryConstant]):
        exponential (Union[Unset, NewSqsTriggerRetryExponential]):
    """

    constant: Union[Unset, "NewSqsTriggerRetryConstant"] = UNSET
    exponential: Union[Unset, "NewSqsTriggerRetryExponential"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        constant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.constant, Unset):
            constant = self.constant.to_dict()

        exponential: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exponential, Unset):
            exponential = self.exponential.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if constant is not UNSET:
            field_dict["constant"] = constant
        if exponential is not UNSET:
            field_dict["exponential"] = exponential

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.new_sqs_trigger_retry_constant import NewSqsTriggerRetryConstant
        from ..models.new_sqs_trigger_retry_exponential import NewSqsTriggerRetryExponential

        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, NewSqsTriggerRetryConstant]
        if isinstance(_constant, Unset):
            constant = UNSET
        else:
            constant = NewSqsTriggerRetryConstant.from_dict(_constant)

        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, NewSqsTriggerRetryExponential]
        if isinstance(_exponential, Unset):
            exponential = UNSET
        else:
            exponential = NewSqsTriggerRetryExponential.from_dict(_exponential)

        new_sqs_trigger_retry = cls(
            constant=constant,
            exponential=exponential,
        )

        new_sqs_trigger_retry.additional_properties = d
        return new_sqs_trigger_retry

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
