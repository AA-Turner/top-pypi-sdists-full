from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.attach_customer_secret_dto_injection_mode import AttachCustomerSecretDtoInjectionMode
from ..types import UNSET, Unset






T = TypeVar("T", bound="AttachCustomerSecretDto")



@_attrs_define
class AttachCustomerSecretDto:
    """ Request body for attaching a customer secret to a run-config version.

        Example:
            {'injectionMode': 'proxy'}

        Attributes:
            injection_mode (AttachCustomerSecretDtoInjectionMode | Unset): Injection mode for this attachment. Must match
                the secret: 'proxy' for a secret with an upstream host and header, 'direct' for one without. Omit to use the
                secret's mode.
     """

    injection_mode: AttachCustomerSecretDtoInjectionMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        injection_mode: str | Unset = UNSET
        if not isinstance(self.injection_mode, Unset):
            injection_mode = self.injection_mode.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if injection_mode is not UNSET:
            field_dict["injectionMode"] = injection_mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _injection_mode = d.pop("injectionMode", UNSET)
        injection_mode: AttachCustomerSecretDtoInjectionMode | Unset
        if isinstance(_injection_mode,  Unset):
            injection_mode = UNSET
        else:
            injection_mode = AttachCustomerSecretDtoInjectionMode(_injection_mode)




        attach_customer_secret_dto = cls(
            injection_mode=injection_mode,
        )


        attach_customer_secret_dto.additional_properties = d
        return attach_customer_secret_dto

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
