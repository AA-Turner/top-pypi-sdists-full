import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.check_schema_contracts_response_200_warnings_item_kind import (
    CheckSchemaContractsResponse200WarningsItemKind,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="CheckSchemaContractsResponse200WarningsItem")


@_attrs_define
class CheckSchemaContractsResponse200WarningsItem:
    """One save-time schema-contract warning: a consumer reference that does
    not match the referenced asset's latest captured schema.
    `schema_version`/`captured_at` identify the capture the check ran
    against (as-of the producer's last run, not its latest save).

        Attributes:
            kind (CheckSchemaContractsResponse200WarningsItemKind):
            asset_path (str):
            message (str):
            column (Union[Unset, str]):
            expected_type (Union[Unset, str]):
            found_type (Union[Unset, str]):
            schema_version (Union[Unset, int]):
            captured_at (Union[Unset, datetime.datetime]):
    """

    kind: CheckSchemaContractsResponse200WarningsItemKind
    asset_path: str
    message: str
    column: Union[Unset, str] = UNSET
    expected_type: Union[Unset, str] = UNSET
    found_type: Union[Unset, str] = UNSET
    schema_version: Union[Unset, int] = UNSET
    captured_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        asset_path = self.asset_path
        message = self.message
        column = self.column
        expected_type = self.expected_type
        found_type = self.found_type
        schema_version = self.schema_version
        captured_at: Union[Unset, str] = UNSET
        if not isinstance(self.captured_at, Unset):
            captured_at = self.captured_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "asset_path": asset_path,
                "message": message,
            }
        )
        if column is not UNSET:
            field_dict["column"] = column
        if expected_type is not UNSET:
            field_dict["expected_type"] = expected_type
        if found_type is not UNSET:
            field_dict["found_type"] = found_type
        if schema_version is not UNSET:
            field_dict["schema_version"] = schema_version
        if captured_at is not UNSET:
            field_dict["captured_at"] = captured_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = CheckSchemaContractsResponse200WarningsItemKind(d.pop("kind"))

        asset_path = d.pop("asset_path")

        message = d.pop("message")

        column = d.pop("column", UNSET)

        expected_type = d.pop("expected_type", UNSET)

        found_type = d.pop("found_type", UNSET)

        schema_version = d.pop("schema_version", UNSET)

        _captured_at = d.pop("captured_at", UNSET)
        captured_at: Union[Unset, datetime.datetime]
        if isinstance(_captured_at, Unset):
            captured_at = UNSET
        else:
            captured_at = isoparse(_captured_at)

        check_schema_contracts_response_200_warnings_item = cls(
            kind=kind,
            asset_path=asset_path,
            message=message,
            column=column,
            expected_type=expected_type,
            found_type=found_type,
            schema_version=schema_version,
            captured_at=captured_at,
        )

        check_schema_contracts_response_200_warnings_item.additional_properties = d
        return check_schema_contracts_response_200_warnings_item

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
