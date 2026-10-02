import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserOfferingConsent")


@_attrs_define
class UserOfferingConsent:
    """
    Attributes:
        uuid (UUID):
        user_uuid (UUID):
        offering_uuid (UUID):
        agreement_date (datetime.datetime):
        revocation_date (Union[None, datetime.datetime]):
        created (datetime.datetime):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_full_name (str):
        user_email (str):
        offering_name (str):
        offering_slug (str):
        offering_url (str):
        modified (datetime.datetime):
        has_consent (bool):
        requires_reconsent (bool):
        collected_attributes (list[str]): List of user attributes that will be shared with service provider
        version (Union[Unset, str]):
    """

    uuid: UUID
    user_uuid: UUID
    offering_uuid: UUID
    agreement_date: datetime.datetime
    revocation_date: Union[None, datetime.datetime]
    created: datetime.datetime
    user_username: str
    user_full_name: str
    user_email: str
    offering_name: str
    offering_slug: str
    offering_url: str
    modified: datetime.datetime
    has_consent: bool
    requires_reconsent: bool
    collected_attributes: list[str]
    version: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user_uuid = str(self.user_uuid)

        offering_uuid = str(self.offering_uuid)

        agreement_date = self.agreement_date.isoformat()

        revocation_date: Union[None, str]
        if isinstance(self.revocation_date, datetime.datetime):
            revocation_date = self.revocation_date.isoformat()
        else:
            revocation_date = self.revocation_date

        created = self.created.isoformat()

        user_username = self.user_username

        user_full_name = self.user_full_name

        user_email = self.user_email

        offering_name = self.offering_name

        offering_slug = self.offering_slug

        offering_url = self.offering_url

        modified = self.modified.isoformat()

        has_consent = self.has_consent

        requires_reconsent = self.requires_reconsent

        collected_attributes = self.collected_attributes

        version = self.version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user_uuid": user_uuid,
                "offering_uuid": offering_uuid,
                "agreement_date": agreement_date,
                "revocation_date": revocation_date,
                "created": created,
                "user_username": user_username,
                "user_full_name": user_full_name,
                "user_email": user_email,
                "offering_name": offering_name,
                "offering_slug": offering_slug,
                "offering_url": offering_url,
                "modified": modified,
                "has_consent": has_consent,
                "requires_reconsent": requires_reconsent,
                "collected_attributes": collected_attributes,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user_uuid = UUID(d.pop("user_uuid"))

        offering_uuid = UUID(d.pop("offering_uuid"))

        agreement_date = isoparse(d.pop("agreement_date"))

        def _parse_revocation_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revocation_date_type_0 = isoparse(data)

                return revocation_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        revocation_date = _parse_revocation_date(d.pop("revocation_date"))

        created = isoparse(d.pop("created"))

        user_username = d.pop("user_username")

        user_full_name = d.pop("user_full_name")

        user_email = d.pop("user_email")

        offering_name = d.pop("offering_name")

        offering_slug = d.pop("offering_slug")

        offering_url = d.pop("offering_url")

        modified = isoparse(d.pop("modified"))

        has_consent = d.pop("has_consent")

        requires_reconsent = d.pop("requires_reconsent")

        collected_attributes = cast(list[str], d.pop("collected_attributes"))

        version = d.pop("version", UNSET)

        user_offering_consent = cls(
            uuid=uuid,
            user_uuid=user_uuid,
            offering_uuid=offering_uuid,
            agreement_date=agreement_date,
            revocation_date=revocation_date,
            created=created,
            user_username=user_username,
            user_full_name=user_full_name,
            user_email=user_email,
            offering_name=offering_name,
            offering_slug=offering_slug,
            offering_url=offering_url,
            modified=modified,
            has_consent=has_consent,
            requires_reconsent=requires_reconsent,
            collected_attributes=collected_attributes,
            version=version,
        )

        user_offering_consent.additional_properties = d
        return user_offering_consent

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
