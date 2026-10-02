from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_source_verification_response_type import ManagedAgentsEventSourceVerificationResponseType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef
  from ..models.managed_agents_event_source_signed_part import ManagedAgentsEventSourceSignedPart





T = TypeVar("T", bound="ManagedAgentsEventSourceVerificationResponse")



@_attrs_define
class ManagedAgentsEventSourceVerificationResponse:
    """ Verification policy for a custom webhook event source.

        Example:
            {'signatureHeader': 'example', 'signaturePrefix': 'example', 'signedParts': [{'kind': 'body'}], 'type': 'none',
                'verificationCredential': {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}

        Attributes:
            type_ (ManagedAgentsEventSourceVerificationResponseType): Verification algorithm configured for custom webhook
                deliveries.
            signature_header (str | Unset): HTTP header carrying the signature for signed deliveries.
            signature_prefix (str | Unset): Literal prefix removed before comparing a signature.
            signed_parts (list[ManagedAgentsEventSourceSignedPart] | Unset): Ordered delivery components used as the
                signature input.
            verification_credential (ManagedAgentsEventSourceCredentialRef | Unset): Reference to a managed credential;
                secret material is never returned. Example: {'credentialId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vaultId':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
     """

    type_: ManagedAgentsEventSourceVerificationResponseType
    signature_header: str | Unset = UNSET
    signature_prefix: str | Unset = UNSET
    signed_parts: list[ManagedAgentsEventSourceSignedPart] | Unset = UNSET
    verification_credential: ManagedAgentsEventSourceCredentialRef | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        from ..models.managed_agents_event_source_signed_part import ManagedAgentsEventSourceSignedPart # noqa: PLC0415
        type_ = self.type_.value

        signature_header = self.signature_header

        signature_prefix = self.signature_prefix

        signed_parts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.signed_parts, Unset):
            signed_parts = []
            for signed_parts_item_data in self.signed_parts:
                signed_parts_item = signed_parts_item_data.to_dict()
                signed_parts.append(signed_parts_item)



        verification_credential: dict[str, Any] | Unset = UNSET
        if not isinstance(self.verification_credential, Unset):
            verification_credential = self.verification_credential.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })
        if signature_header is not UNSET:
            field_dict["signatureHeader"] = signature_header
        if signature_prefix is not UNSET:
            field_dict["signaturePrefix"] = signature_prefix
        if signed_parts is not UNSET:
            field_dict["signedParts"] = signed_parts
        if verification_credential is not UNSET:
            field_dict["verificationCredential"] = verification_credential

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event_source_credential_ref import ManagedAgentsEventSourceCredentialRef # noqa: PLC0415
        from ..models.managed_agents_event_source_signed_part import ManagedAgentsEventSourceSignedPart # noqa: PLC0415
        d = dict(src_dict)
        type_ = ManagedAgentsEventSourceVerificationResponseType(d.pop("type"))




        signature_header = d.pop("signatureHeader", UNSET)

        signature_prefix = d.pop("signaturePrefix", UNSET)

        _signed_parts = d.pop("signedParts", UNSET)
        signed_parts: list[ManagedAgentsEventSourceSignedPart] | Unset = UNSET
        if _signed_parts is not UNSET:
            signed_parts = []
            for signed_parts_item_data in _signed_parts:
                signed_parts_item = ManagedAgentsEventSourceSignedPart.from_dict(signed_parts_item_data)



                signed_parts.append(signed_parts_item)


        _verification_credential = d.pop("verificationCredential", UNSET)
        verification_credential: ManagedAgentsEventSourceCredentialRef | Unset
        if isinstance(_verification_credential,  Unset):
            verification_credential = UNSET
        else:
            verification_credential = ManagedAgentsEventSourceCredentialRef.from_dict(_verification_credential)




        managed_agents_event_source_verification_response = cls(
            type_=type_,
            signature_header=signature_header,
            signature_prefix=signature_prefix,
            signed_parts=signed_parts,
            verification_credential=verification_credential,
        )

        return managed_agents_event_source_verification_response

