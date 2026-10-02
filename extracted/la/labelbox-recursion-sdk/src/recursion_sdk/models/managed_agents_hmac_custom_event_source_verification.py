from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_hmac_custom_event_source_verification_type import ManagedAgentsHmacCustomEventSourceVerificationType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef
  from ..models.managed_agents_event_source_signed_part import ManagedAgentsEventSourceSignedPart





T = TypeVar("T", bound="ManagedAgentsHmacCustomEventSourceVerification")



@_attrs_define
class ManagedAgentsHmacCustomEventSourceVerification:
    """ HMAC-SHA256 verification policy for a custom webhook.

        Example:
            {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts': [{'kind': 'body'}], 'type':
                'hmac_sha256', 'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}

        Attributes:
            signature_header (str): HTTP header carrying the delivery signature.
            signed_parts (list[ManagedAgentsEventSourceSignedPart]): The raw request body used as the HMAC input; v1
                requires exactly one body part.
            type_ (ManagedAgentsHmacCustomEventSourceVerificationType): Verify a hexadecimal HMAC-SHA256 signature before
                admitting the delivery.
            verification_credential (ManagedAgentsEventSourceCredentialRef): Reference to a managed credential; secret
                material is never returned. Example: {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            signature_prefix (str | Unset): Optional literal prefix removed from the signature header before comparison.
                Default: ''.
     """

    signature_header: str
    signed_parts: list[ManagedAgentsEventSourceSignedPart]
    type_: ManagedAgentsHmacCustomEventSourceVerificationType
    verification_credential: ManagedAgentsEventSourceCredentialRef
    signature_prefix: str | Unset = ''





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        from ..models.managed_agents_event_source_signed_part import ManagedAgentsEventSourceSignedPart # noqa: PLC0415
        signature_header = self.signature_header

        signed_parts = []
        for signed_parts_item_data in self.signed_parts:
            signed_parts_item = signed_parts_item_data.to_dict()
            signed_parts.append(signed_parts_item)



        type_ = self.type_.value

        verification_credential = self.verification_credential.to_dict()

        signature_prefix = self.signature_prefix


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "signatureHeader": signature_header,
            "signedParts": signed_parts,
            "type": type_,
            "verificationCredential": verification_credential,
        })
        if signature_prefix is not UNSET:
            field_dict["signaturePrefix"] = signature_prefix

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        from ..models.managed_agents_event_source_signed_part import ManagedAgentsEventSourceSignedPart # noqa: PLC0415
        d = dict(src_dict)
        signature_header = d.pop("signatureHeader")

        signed_parts = []
        _signed_parts = d.pop("signedParts")
        for signed_parts_item_data in (_signed_parts):
            signed_parts_item = ManagedAgentsEventSourceSignedPart.from_dict(signed_parts_item_data)



            signed_parts.append(signed_parts_item)


        type_ = ManagedAgentsHmacCustomEventSourceVerificationType(d.pop("type"))




        verification_credential = ManagedAgentsEventSourceCredentialRef.from_dict(d.pop("verificationCredential"))




        signature_prefix = d.pop("signaturePrefix", UNSET)

        managed_agents_hmac_custom_event_source_verification = cls(
            signature_header=signature_header,
            signed_parts=signed_parts,
            type_=type_,
            verification_credential=verification_credential,
            signature_prefix=signature_prefix,
        )

        return managed_agents_hmac_custom_event_source_verification

