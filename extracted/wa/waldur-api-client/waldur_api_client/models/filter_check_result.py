from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.filter_check_result_rule_value_type_0 import FilterCheckResultRuleValueType0
    from ..models.filter_check_result_user_value_type_0 import FilterCheckResultUserValueType0


T = TypeVar("T", bound="FilterCheckResult")


@_attrs_define
class FilterCheckResult:
    """
    Attributes:
        name (str):
        configured (bool):
        matched (bool):
        reason (str):
        user_value (Union['FilterCheckResultUserValueType0', None, Unset]):
        rule_value (Union['FilterCheckResultRuleValueType0', None, Unset]):
    """

    name: str
    configured: bool
    matched: bool
    reason: str
    user_value: Union["FilterCheckResultUserValueType0", None, Unset] = UNSET
    rule_value: Union["FilterCheckResultRuleValueType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.filter_check_result_rule_value_type_0 import FilterCheckResultRuleValueType0
        from ..models.filter_check_result_user_value_type_0 import FilterCheckResultUserValueType0

        name = self.name

        configured = self.configured

        matched = self.matched

        reason = self.reason

        user_value: Union[None, Unset, dict[str, Any]]
        if isinstance(self.user_value, Unset):
            user_value = UNSET
        elif isinstance(self.user_value, FilterCheckResultUserValueType0):
            user_value = self.user_value.to_dict()
        else:
            user_value = self.user_value

        rule_value: Union[None, Unset, dict[str, Any]]
        if isinstance(self.rule_value, Unset):
            rule_value = UNSET
        elif isinstance(self.rule_value, FilterCheckResultRuleValueType0):
            rule_value = self.rule_value.to_dict()
        else:
            rule_value = self.rule_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "configured": configured,
                "matched": matched,
                "reason": reason,
            }
        )
        if user_value is not UNSET:
            field_dict["user_value"] = user_value
        if rule_value is not UNSET:
            field_dict["rule_value"] = rule_value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.filter_check_result_rule_value_type_0 import FilterCheckResultRuleValueType0
        from ..models.filter_check_result_user_value_type_0 import FilterCheckResultUserValueType0

        d = dict(src_dict)
        name = d.pop("name")

        configured = d.pop("configured")

        matched = d.pop("matched")

        reason = d.pop("reason")

        def _parse_user_value(data: object) -> Union["FilterCheckResultUserValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                user_value_type_0 = FilterCheckResultUserValueType0.from_dict(data)

                return user_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FilterCheckResultUserValueType0", None, Unset], data)

        user_value = _parse_user_value(d.pop("user_value", UNSET))

        def _parse_rule_value(data: object) -> Union["FilterCheckResultRuleValueType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                rule_value_type_0 = FilterCheckResultRuleValueType0.from_dict(data)

                return rule_value_type_0
            except:  # noqa: E722
                pass
            return cast(Union["FilterCheckResultRuleValueType0", None, Unset], data)

        rule_value = _parse_rule_value(d.pop("rule_value", UNSET))

        filter_check_result = cls(
            name=name,
            configured=configured,
            matched=matched,
            reason=reason,
            user_value=user_value,
            rule_value=rule_value,
        )

        filter_check_result.additional_properties = d
        return filter_check_result

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
