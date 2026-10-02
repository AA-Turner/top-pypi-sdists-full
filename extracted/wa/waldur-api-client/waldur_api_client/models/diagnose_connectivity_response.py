from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.diagnose_check import DiagnoseCheck


T = TypeVar("T", bound="DiagnoseConnectivityResponse")


@_attrs_define
class DiagnoseConnectivityResponse:
    """
    Attributes:
        target (str):
        target_address (Union[None, str]):
        checks (list['DiagnoseCheck']):
        root_cause (Union[None, str]):
    """

    target: str
    target_address: Union[None, str]
    checks: list["DiagnoseCheck"]
    root_cause: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        target = self.target

        target_address: Union[None, str]
        target_address = self.target_address

        checks = []
        for checks_item_data in self.checks:
            checks_item = checks_item_data.to_dict()
            checks.append(checks_item)

        root_cause: Union[None, str]
        root_cause = self.root_cause

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "target": target,
                "target_address": target_address,
                "checks": checks,
                "root_cause": root_cause,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.diagnose_check import DiagnoseCheck

        d = dict(src_dict)
        target = d.pop("target")

        def _parse_target_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        target_address = _parse_target_address(d.pop("target_address"))

        checks = []
        _checks = d.pop("checks")
        for checks_item_data in _checks:
            checks_item = DiagnoseCheck.from_dict(checks_item_data)

            checks.append(checks_item)

        def _parse_root_cause(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        root_cause = _parse_root_cause(d.pop("root_cause"))

        diagnose_connectivity_response = cls(
            target=target,
            target_address=target_address,
            checks=checks,
            root_cause=root_cause,
        )

        diagnose_connectivity_response.additional_properties = d
        return diagnose_connectivity_response

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
