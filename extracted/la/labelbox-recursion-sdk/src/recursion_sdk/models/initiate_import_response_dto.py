from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="InitiateImportResponseDto")



@_attrs_define
class InitiateImportResponseDto:
    """ Signed URL and metadata for initiating a GCS resumable upload session for the import archive.

        Example:
            {'importId': '30a8ee9f-3543-42b7-9cca-c4996ef2e9a0', 'uploadUrl': 'https://storage.googleapis.com/recursion-
                example-imports/784e2386-e297-4f9d-a886-838422383b65/problems-export.tar.gz?x-goog-
                signature=a1b2c3d4e5f6&x-goog-expires=3600', 'contentType': 'application/gzip'}

        Attributes:
            import_id (UUID): Identifier of the newly created import job.
            upload_url (str): GCS resumable-upload signed URL. POST this URL with header x-goog-resumable: start to obtain a
                session URI, then PUT byte-range chunks against it using Content-Range headers.
            content_type (str): Content-Type to send on both the session-init POST and each chunk PUT. Must match what the
                backend signed or GCS rejects the upload.
     """

    import_id: UUID
    upload_url: str
    content_type: str





    def to_dict(self) -> dict[str, Any]:
        import_id = str(self.import_id)

        upload_url = self.upload_url

        content_type = self.content_type


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "importId": import_id,
            "uploadUrl": upload_url,
            "contentType": content_type,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        import_id = UUID(d.pop("importId"))




        upload_url = d.pop("uploadUrl")

        content_type = d.pop("contentType")

        initiate_import_response_dto = cls(
            import_id=import_id,
            upload_url=upload_url,
            content_type=content_type,
        )

        return initiate_import_response_dto

