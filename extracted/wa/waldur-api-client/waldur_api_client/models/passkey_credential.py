import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.attachment_enum import AttachmentEnum
from ..models.blank_enum import BlankEnum

if TYPE_CHECKING:
    from ..models.passkey_credential_transports import PasskeyCredentialTransports


T = TypeVar("T", bound="PasskeyCredential")


@_attrs_define
class PasskeyCredential:
    """
    Attributes:
        uuid (UUID):
        name (str):
        aaguid (str):
        transports (PasskeyCredentialTransports):
        attachment (Union[AttachmentEnum, BlankEnum]):
        rp_id (str):
        is_backup_eligible (bool):
        is_backed_up (bool):
        is_discoverable (bool):
        is_user_verified (bool):
        is_orphaned (bool):
        created (datetime.datetime):
        last_used_at (Union[None, datetime.datetime]):
        use_count (int):
        is_active (bool):
        revoked_at (Union[None, datetime.datetime]):
        revoked_by_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_
            characters
        revocation_reason (str):
    """

    uuid: UUID
    name: str
    aaguid: str
    transports: "PasskeyCredentialTransports"
    attachment: Union[AttachmentEnum, BlankEnum]
    rp_id: str
    is_backup_eligible: bool
    is_backed_up: bool
    is_discoverable: bool
    is_user_verified: bool
    is_orphaned: bool
    created: datetime.datetime
    last_used_at: Union[None, datetime.datetime]
    use_count: int
    is_active: bool
    revoked_at: Union[None, datetime.datetime]
    revoked_by_username: str
    revocation_reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        aaguid = self.aaguid

        transports = self.transports.to_dict()

        attachment: str
        if isinstance(self.attachment, AttachmentEnum):
            attachment = self.attachment.value
        else:
            attachment = self.attachment.value

        rp_id = self.rp_id

        is_backup_eligible = self.is_backup_eligible

        is_backed_up = self.is_backed_up

        is_discoverable = self.is_discoverable

        is_user_verified = self.is_user_verified

        is_orphaned = self.is_orphaned

        created = self.created.isoformat()

        last_used_at: Union[None, str]
        if isinstance(self.last_used_at, datetime.datetime):
            last_used_at = self.last_used_at.isoformat()
        else:
            last_used_at = self.last_used_at

        use_count = self.use_count

        is_active = self.is_active

        revoked_at: Union[None, str]
        if isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        revoked_by_username = self.revoked_by_username

        revocation_reason = self.revocation_reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "aaguid": aaguid,
                "transports": transports,
                "attachment": attachment,
                "rp_id": rp_id,
                "is_backup_eligible": is_backup_eligible,
                "is_backed_up": is_backed_up,
                "is_discoverable": is_discoverable,
                "is_user_verified": is_user_verified,
                "is_orphaned": is_orphaned,
                "created": created,
                "last_used_at": last_used_at,
                "use_count": use_count,
                "is_active": is_active,
                "revoked_at": revoked_at,
                "revoked_by_username": revoked_by_username,
                "revocation_reason": revocation_reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.passkey_credential_transports import PasskeyCredentialTransports

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        aaguid = d.pop("aaguid")

        transports = PasskeyCredentialTransports.from_dict(d.pop("transports"))

        def _parse_attachment(data: object) -> Union[AttachmentEnum, BlankEnum]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                attachment_type_0 = AttachmentEnum(data)

                return attachment_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            attachment_type_1 = BlankEnum(data)

            return attachment_type_1

        attachment = _parse_attachment(d.pop("attachment"))

        rp_id = d.pop("rp_id")

        is_backup_eligible = d.pop("is_backup_eligible")

        is_backed_up = d.pop("is_backed_up")

        is_discoverable = d.pop("is_discoverable")

        is_user_verified = d.pop("is_user_verified")

        is_orphaned = d.pop("is_orphaned")

        created = isoparse(d.pop("created"))

        def _parse_last_used_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_used_at_type_0 = isoparse(data)

                return last_used_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_used_at = _parse_last_used_at(d.pop("last_used_at"))

        use_count = d.pop("use_count")

        is_active = d.pop("is_active")

        def _parse_revoked_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = isoparse(data)

                return revoked_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        revoked_at = _parse_revoked_at(d.pop("revoked_at"))

        revoked_by_username = d.pop("revoked_by_username")

        revocation_reason = d.pop("revocation_reason")

        passkey_credential = cls(
            uuid=uuid,
            name=name,
            aaguid=aaguid,
            transports=transports,
            attachment=attachment,
            rp_id=rp_id,
            is_backup_eligible=is_backup_eligible,
            is_backed_up=is_backed_up,
            is_discoverable=is_discoverable,
            is_user_verified=is_user_verified,
            is_orphaned=is_orphaned,
            created=created,
            last_used_at=last_used_at,
            use_count=use_count,
            is_active=is_active,
            revoked_at=revoked_at,
            revoked_by_username=revoked_by_username,
            revocation_reason=revocation_reason,
        )

        passkey_credential.additional_properties = d
        return passkey_credential

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
