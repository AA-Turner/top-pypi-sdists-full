from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arrow_credentials_validation_response_partner_info import (
        ArrowCredentialsValidationResponsePartnerInfo,
    )


T = TypeVar("T", bound="ArrowCredentialsValidationResponse")


@_attrs_define
class ArrowCredentialsValidationResponse:
    """
    Attributes:
        valid (bool):
        message (Union[Unset, str]):
        error (Union[Unset, str]):
        partner_info (Union[Unset, ArrowCredentialsValidationResponsePartnerInfo]):
    """

    valid: bool
    message: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    partner_info: Union[Unset, "ArrowCredentialsValidationResponsePartnerInfo"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        valid = self.valid

        message = self.message

        error = self.error

        partner_info: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.partner_info, Unset):
            partner_info = self.partner_info.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "valid": valid,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if error is not UNSET:
            field_dict["error"] = error
        if partner_info is not UNSET:
            field_dict["partner_info"] = partner_info

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_credentials_validation_response_partner_info import (
            ArrowCredentialsValidationResponsePartnerInfo,
        )

        d = dict(src_dict)
        valid = d.pop("valid")

        message = d.pop("message", UNSET)

        error = d.pop("error", UNSET)

        _partner_info = d.pop("partner_info", UNSET)
        partner_info: Union[Unset, ArrowCredentialsValidationResponsePartnerInfo]
        if isinstance(_partner_info, Unset):
            partner_info = UNSET
        else:
            partner_info = ArrowCredentialsValidationResponsePartnerInfo.from_dict(_partner_info)

        arrow_credentials_validation_response = cls(
            valid=valid,
            message=message,
            error=error,
            partner_info=partner_info,
        )

        arrow_credentials_validation_response.additional_properties = d
        return arrow_credentials_validation_response

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
