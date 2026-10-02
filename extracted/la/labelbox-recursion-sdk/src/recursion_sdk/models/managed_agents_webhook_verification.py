from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_webhook_verification_type import ManagedAgentsWebhookVerificationType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_webhook_signed_part import ManagedAgentsWebhookSignedPart





T = TypeVar("T", bound="ManagedAgentsWebhookVerification")



@_attrs_define
class ManagedAgentsWebhookVerification:
    """ Provider-neutral rules for authenticating an inbound webhook before its payload can trigger automations.

        Example:
            {'invalid_signature_status': 1, 'maximum_age_seconds': 1, 'secret_credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'secret_vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'signature_header': 'example', 'signature_prefix': 'example', 'signed_parts': [{'kind': 'body', 'value':
                'example'}], 'timestamp_header': 'example', 'type': 'hmac_sha256'}

        Attributes:
            type_ (ManagedAgentsWebhookVerificationType): Verification algorithm. Use hmac_sha256 for signed webhooks; none
                accepts unsigned deliveries.
            invalid_signature_status (int | Unset): HTTP status returned for failed verification; defaults to 401.
            maximum_age_seconds (int | Unset): Maximum accepted age of the timestamp in seconds; requires timestamp_header.
            secret_credential_id (str | Unset): Credential whose secret value verifies the HMAC when type is hmac_sha256.
            secret_vault_id (str | Unset): Vault containing the HMAC secret credential when type is hmac_sha256.
            signature_header (str | Unset): HTTP header carrying the hexadecimal HMAC signature.
            signature_prefix (str | Unset): Optional prefix removed from the signature header before hexadecimal decoding,
                for example sha256=.
            signed_parts (list[ManagedAgentsWebhookSignedPart] | Unset): Ordered inputs concatenated before HMAC
                verification; must include the raw request body.
            timestamp_header (str | Unset): Optional header containing a Unix timestamp used to reject replayed deliveries.
     """

    type_: ManagedAgentsWebhookVerificationType
    invalid_signature_status: int | Unset = UNSET
    maximum_age_seconds: int | Unset = UNSET
    secret_credential_id: str | Unset = UNSET
    secret_vault_id: str | Unset = UNSET
    signature_header: str | Unset = UNSET
    signature_prefix: str | Unset = UNSET
    signed_parts: list[ManagedAgentsWebhookSignedPart] | Unset = UNSET
    timestamp_header: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_webhook_signed_part import ManagedAgentsWebhookSignedPart # noqa: PLC0415
        type_ = self.type_.value

        invalid_signature_status = self.invalid_signature_status

        maximum_age_seconds = self.maximum_age_seconds

        secret_credential_id = self.secret_credential_id

        secret_vault_id = self.secret_vault_id

        signature_header = self.signature_header

        signature_prefix = self.signature_prefix

        signed_parts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.signed_parts, Unset):
            signed_parts = []
            for signed_parts_item_data in self.signed_parts:
                signed_parts_item = signed_parts_item_data.to_dict()
                signed_parts.append(signed_parts_item)



        timestamp_header = self.timestamp_header


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if invalid_signature_status is not UNSET:
            field_dict["invalid_signature_status"] = invalid_signature_status
        if maximum_age_seconds is not UNSET:
            field_dict["maximum_age_seconds"] = maximum_age_seconds
        if secret_credential_id is not UNSET:
            field_dict["secret_credential_id"] = secret_credential_id
        if secret_vault_id is not UNSET:
            field_dict["secret_vault_id"] = secret_vault_id
        if signature_header is not UNSET:
            field_dict["signature_header"] = signature_header
        if signature_prefix is not UNSET:
            field_dict["signature_prefix"] = signature_prefix
        if signed_parts is not UNSET:
            field_dict["signed_parts"] = signed_parts
        if timestamp_header is not UNSET:
            field_dict["timestamp_header"] = timestamp_header

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_webhook_signed_part import ManagedAgentsWebhookSignedPart # noqa: PLC0415
        d = dict(src_dict)
        type_ = ManagedAgentsWebhookVerificationType(d.pop("type"))




        invalid_signature_status = d.pop("invalid_signature_status", UNSET)

        maximum_age_seconds = d.pop("maximum_age_seconds", UNSET)

        secret_credential_id = d.pop("secret_credential_id", UNSET)

        secret_vault_id = d.pop("secret_vault_id", UNSET)

        signature_header = d.pop("signature_header", UNSET)

        signature_prefix = d.pop("signature_prefix", UNSET)

        _signed_parts = d.pop("signed_parts", UNSET)
        signed_parts: list[ManagedAgentsWebhookSignedPart] | Unset = UNSET
        if _signed_parts is not UNSET:
            signed_parts = []
            for signed_parts_item_data in _signed_parts:
                signed_parts_item = ManagedAgentsWebhookSignedPart.from_dict(signed_parts_item_data)



                signed_parts.append(signed_parts_item)


        timestamp_header = d.pop("timestamp_header", UNSET)

        managed_agents_webhook_verification = cls(
            type_=type_,
            invalid_signature_status=invalid_signature_status,
            maximum_age_seconds=maximum_age_seconds,
            secret_credential_id=secret_credential_id,
            secret_vault_id=secret_vault_id,
            signature_header=signature_header,
            signature_prefix=signature_prefix,
            signed_parts=signed_parts,
            timestamp_header=timestamp_header,
        )


        managed_agents_webhook_verification.additional_properties = d
        return managed_agents_webhook_verification

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
