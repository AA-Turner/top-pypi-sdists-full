from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_gcp_trigger_json_body_retry_constant import CreateGcpTriggerJsonBodyRetryConstant
    from ..models.create_gcp_trigger_json_body_retry_exponential import CreateGcpTriggerJsonBodyRetryExponential


T = TypeVar("T", bound="CreateGcpTriggerJsonBodyRetry")


@_attrs_define
class CreateGcpTriggerJsonBodyRetry:
    """
    Attributes:
        constant (Union[Unset, CreateGcpTriggerJsonBodyRetryConstant]):
        exponential (Union[Unset, CreateGcpTriggerJsonBodyRetryExponential]):
    """

    constant: Union[Unset, "CreateGcpTriggerJsonBodyRetryConstant"] = UNSET
    exponential: Union[Unset, "CreateGcpTriggerJsonBodyRetryExponential"] = UNSET
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
        from ..models.create_gcp_trigger_json_body_retry_constant import CreateGcpTriggerJsonBodyRetryConstant
        from ..models.create_gcp_trigger_json_body_retry_exponential import CreateGcpTriggerJsonBodyRetryExponential

        d = src_dict.copy()
        _constant = d.pop("constant", UNSET)
        constant: Union[Unset, CreateGcpTriggerJsonBodyRetryConstant]
        if isinstance(_constant, Unset):
            constant = UNSET
        else:
            constant = CreateGcpTriggerJsonBodyRetryConstant.from_dict(_constant)

        _exponential = d.pop("exponential", UNSET)
        exponential: Union[Unset, CreateGcpTriggerJsonBodyRetryExponential]
        if isinstance(_exponential, Unset):
            exponential = UNSET
        else:
            exponential = CreateGcpTriggerJsonBodyRetryExponential.from_dict(_exponential)

        create_gcp_trigger_json_body_retry = cls(
            constant=constant,
            exponential=exponential,
        )

        create_gcp_trigger_json_body_retry.additional_properties = d
        return create_gcp_trigger_json_body_retry

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
