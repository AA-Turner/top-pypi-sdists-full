from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ManagedAgentsStartIntegrationInstallRequest")



@_attrs_define
class ManagedAgentsStartIntegrationInstallRequest:
    """ Optional input for starting or continuing an integration authorization. It may select a provider-defined
    continuation or an existing connection to re-authorize; organization identity always comes from the authenticated
    caller.

        Example:
            {'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'option': 'example'}

        Attributes:
            connection_id (UUID | Unset): Existing connection to re-authorize in place, keeping its id and therefore the
                vault grants that reference it. Omit to create a new connection. The connection must belong to the caller's
                organization and use this provider; it is recorded server-side against the returned state, never read back from
                the provider callback.
            option (str | Unset): Short opaque provider option: either a continuation value returned by a prior completion,
                or -- for a provider whose catalog entry reports preset_fixed_at_authorization -- the permission preset to
                authorize (see ProviderInfo.permissions). Omit for a provider needing neither.
     """

    connection_id: UUID | Unset = UNSET
    option: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_id: str | Unset = UNSET
        if not isinstance(self.connection_id, Unset):
            connection_id = str(self.connection_id)

        option = self.option


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if connection_id is not UNSET:
            field_dict["connection_id"] = connection_id
        if option is not UNSET:
            field_dict["option"] = option

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _connection_id = d.pop("connection_id", UNSET)
        connection_id: UUID | Unset
        if isinstance(_connection_id,  Unset):
            connection_id = UNSET
        else:
            connection_id = UUID(_connection_id)




        option = d.pop("option", UNSET)

        managed_agents_start_integration_install_request = cls(
            connection_id=connection_id,
            option=option,
        )


        managed_agents_start_integration_install_request.additional_properties = d
        return managed_agents_start_integration_install_request

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
