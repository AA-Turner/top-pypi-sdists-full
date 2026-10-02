from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_team_user import ProviderTeamUser


T = TypeVar("T", bound="ServiceProviderAccess")


@_attrs_define
class ServiceProviderAccess:
    """
    Attributes:
        offering_uuid (UUID):
        offering_name (str):
        provider_name (Union[None, str]):
        provider_uuid (Union[None, UUID]):
        exposed_fields (list[str]):
        consent_date (Union[None, str]):
        consent_version (Union[None, str]):
        provider_team (Union[Unset, list['ProviderTeamUser']]):
    """

    offering_uuid: UUID
    offering_name: str
    provider_name: Union[None, str]
    provider_uuid: Union[None, UUID]
    exposed_fields: list[str]
    consent_date: Union[None, str]
    consent_version: Union[None, str]
    provider_team: Union[Unset, list["ProviderTeamUser"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        provider_name: Union[None, str]
        provider_name = self.provider_name

        provider_uuid: Union[None, str]
        if isinstance(self.provider_uuid, UUID):
            provider_uuid = str(self.provider_uuid)
        else:
            provider_uuid = self.provider_uuid

        exposed_fields = self.exposed_fields

        consent_date: Union[None, str]
        consent_date = self.consent_date

        consent_version: Union[None, str]
        consent_version = self.consent_version

        provider_team: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.provider_team, Unset):
            provider_team = []
            for provider_team_item_data in self.provider_team:
                provider_team_item = provider_team_item_data.to_dict()
                provider_team.append(provider_team_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "provider_name": provider_name,
                "provider_uuid": provider_uuid,
                "exposed_fields": exposed_fields,
                "consent_date": consent_date,
                "consent_version": consent_version,
            }
        )
        if provider_team is not UNSET:
            field_dict["provider_team"] = provider_team

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_team_user import ProviderTeamUser

        d = dict(src_dict)
        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        def _parse_provider_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        provider_name = _parse_provider_name(d.pop("provider_name"))

        def _parse_provider_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                provider_uuid_type_0 = UUID(data)

                return provider_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        provider_uuid = _parse_provider_uuid(d.pop("provider_uuid"))

        exposed_fields = cast(list[str], d.pop("exposed_fields"))

        def _parse_consent_date(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        consent_date = _parse_consent_date(d.pop("consent_date"))

        def _parse_consent_version(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        consent_version = _parse_consent_version(d.pop("consent_version"))

        provider_team = []
        _provider_team = d.pop("provider_team", UNSET)
        for provider_team_item_data in _provider_team or []:
            provider_team_item = ProviderTeamUser.from_dict(provider_team_item_data)

            provider_team.append(provider_team_item)

        service_provider_access = cls(
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            provider_name=provider_name,
            provider_uuid=provider_uuid,
            exposed_fields=exposed_fields,
            consent_date=consent_date,
            consent_version=consent_version,
            provider_team=provider_team,
        )

        service_provider_access.additional_properties = d
        return service_provider_access

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
