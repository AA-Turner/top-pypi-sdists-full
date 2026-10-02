from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingUserPosixUpdateResponse")


@_attrs_define
class OfferingUserPosixUpdateResponse:
    """
    Attributes:
        uidnumber (Union[None, Unset, int]): The UID now stored for the account.
        primarygroup (Union[None, Unset, int]): The primary GID now stored for the account.
        warnings (Union[Unset, list[str]]): Non-fatal advisories about the accepted values: a reserved POSIX id (65534
            or 65535) or a value of 2^31 or above. Out-of-range and already-allocated values are rejected with 400 instead.
    """

    uidnumber: Union[None, Unset, int] = UNSET
    primarygroup: Union[None, Unset, int] = UNSET
    warnings: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uidnumber: Union[None, Unset, int]
        if isinstance(self.uidnumber, Unset):
            uidnumber = UNSET
        else:
            uidnumber = self.uidnumber

        primarygroup: Union[None, Unset, int]
        if isinstance(self.primarygroup, Unset):
            primarygroup = UNSET
        else:
            primarygroup = self.primarygroup

        warnings: Union[Unset, list[str]] = UNSET
        if not isinstance(self.warnings, Unset):
            warnings = self.warnings

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uidnumber is not UNSET:
            field_dict["uidnumber"] = uidnumber
        if primarygroup is not UNSET:
            field_dict["primarygroup"] = primarygroup
        if warnings is not UNSET:
            field_dict["warnings"] = warnings

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_uidnumber(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        uidnumber = _parse_uidnumber(d.pop("uidnumber", UNSET))

        def _parse_primarygroup(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        primarygroup = _parse_primarygroup(d.pop("primarygroup", UNSET))

        warnings = cast(list[str], d.pop("warnings", UNSET))

        offering_user_posix_update_response = cls(
            uidnumber=uidnumber,
            primarygroup=primarygroup,
            warnings=warnings,
        )

        offering_user_posix_update_response.additional_properties = d
        return offering_user_posix_update_response

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
