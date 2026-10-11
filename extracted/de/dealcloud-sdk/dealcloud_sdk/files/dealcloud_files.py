"""
Files API operations for DealCloud.

The Files API provides file upload and download operations for
Binary/Attachment fields in DealCloud.

- Download: GET .../entryfiles/{entryId}/fields/{fieldId}
  See: https://api.docs.dealcloud.com/docs/data/files
- Upload (new attachment): POST .../entrydata/{object_id} with object_id="attachment"
  (multipart model + file). There is no separate /entrydata/attachment path; the
  endpoint is entrydata/{object_id} where object_id may be "attachment" or an integer.
  For new attachments use upload_attachment(); uploads must be proper MIME multipart
  (no raw bytes). See: https://api.docs.dealcloud.com/guides/how_to_upload_files
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from ..constants import field_types
from ..history.dealcloud_history import DealCloudHistory
from ..storage import LocalStorage, StorageBackend


@dataclass
class ExportResult:
    """Result of a bulk file export operation."""
    total_files: int = 0
    exported: int = 0
    failed: int = 0
    skipped: int = 0
    errors: List[Dict] = field(default_factory=list)
    files: List[str] = field(default_factory=list)
    output_path: Optional[str] = None
    
    @property
    def success_rate(self) -> float:
        """Percentage of files successfully exported."""
        if self.total_files == 0:
            return 100.0
        return (self.exported / self.total_files) * 100
    
    @property
    def has_errors(self) -> bool:
        """Check if any errors occurred."""
        return len(self.errors) > 0


class DealCloudFiles(DealCloudHistory):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Files API operations.
    
    Provides file upload/download for attachment fields.
    """
    
    @property
    def files_url(self) -> str:
        """
        Get the Files API base URL.
        
        Use this for custom file API calls not covered by SDK methods.
        
        Returns:
            str: Files API URL (e.g., "https://site.dealcloud.com/api/rest/v4/data/entryfiles")
        
        Example:
            >>> # Custom files endpoint call (API: entryfiles/{entryId}/fields/{fieldId})
            >>> url = f"{dc.files_url}/{entry_id}/fields/{field_id}"
            >>> response = dc.client.get_raw(url)
        """
        return self._files_url
    
    # =========================================================================
    # File Download
    # =========================================================================
    
    def download_file(
        self,
        entry_id: int,
        field_id: Union[int, str],
        output_path: Optional[str] = None,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
    ) -> Union[bytes, str]:
        """
        Download a file attachment with streaming (memory-efficient).

        API path: GET .../entryfiles/{entryId}/fields/{fieldId} (no object in path).

        Downloads large files without loading entire content into memory.
        Disk and URI destinations are written via the REST client's fsspec-backed
        streaming download; in-memory downloads use a ``BytesIO`` buffer.

        Args:
            entry_id: Entry ID containing the file
            field_id: Field ID or API name of the attachment field
            output_path: Optional local path or fsspec URI to save the file. If None, returns bytes.
            progress_callback: Optional callback called with (bytes_downloaded, total_bytes)

        Returns:
            If output_path is None: File content as bytes
            If output_path provided: Path to saved file

        Example:
            path = dc.download_file(123, "Logo", output_path="./logo.png")
            content = dc.download_file(123, "Logo")
        """
        from io import BytesIO
        
        # API: GET .../entryfiles/{entryId}/fields/{fieldId} (no object in path)
        url = f"{self._files_url}/{entry_id}/fields/{field_id}"
        
        if output_path:
            self._client.download_file(
                url,
                destination=output_path,
                progress_callback=progress_callback,
            )
            return str(output_path)
        else:
            # For in-memory, use BytesIO with streaming
            buffer = BytesIO()
            self._client.download_file(
                url,
                destination=buffer,
                progress_callback=progress_callback
            )
            return buffer.getvalue()
    
    def download_attachment(
        self,
        entry_id: int,
        field_id: Union[int, str],
        output_path: Optional[str] = None,
        progress_callback: Optional[Callable[[int, Optional[int]], None]] = None,
    ) -> Union[bytes, str]:
        """
        Download an attachment (alias for download_file).

        Same signature and behavior as download_file. Prefer this name when
        working with the Attachments object or attachment-style fields.
        """
        return self.download_file(
            entry_id=entry_id,
            field_id=field_id,
            output_path=output_path,
            progress_callback=progress_callback,
        )

    def download_attachment_metadata(
        self,
        object_id: Union[int, str],
        entry_id: int,
        field_id: Union[int, str],
    ) -> dict:
        """
        Get file metadata for an attachment field without downloading content.

        Uses the rows/query endpoint (POST with query by entryId) to fetch the
        row for the entry and returns the file field's metadata. There is no
        separate entryfiles/.../info endpoint; this is a helper that derives
        info from the object row.

        Args:
            object_id: Object ID or API name
            entry_id: Entry ID containing the file
            field_id: Field ID or API name of the attachment field

        Returns:
            File metadata dict with keys (when present in API response):
            - fileName: Original file name
            - fileSize: Size in bytes
            - contentType: MIME type
            - uploadDate: When file was uploaded
            Callers should use .get("contentType", "...") for defaults.
        """
        from ..utils.data_utils import query_by_entry_id, rows_query_payload_builder

        endpoint = f"{self._query_url}/{object_id}"
        body = rows_query_payload_builder(
            query_by_entry_id(entry_id),
            limit=1,
            skip=0,
        )
        response = self._client.post(endpoint, json=body)
        rows = response.get("rows") if isinstance(response, dict) else []
        if not rows:
            return {}
        row = rows[0]
        # Row may be keyed by field id (int/str) or api name
        raw = row.get(field_id) or row.get(str(field_id))
        if not isinstance(raw, dict):
            return {}
        # Normalize camelCase/snake_case to the shape callers expect
        return {
            "fileName": raw.get("fileName") or raw.get("file_name") or "",
            "fileSize": raw.get("fileSize") or raw.get("file_size"),
            "contentType": raw.get("contentType") or raw.get("content_type") or "application/octet-stream",
            "uploadDate": raw.get("uploadDate") or raw.get("upload_date"),
        }
    
    # =========================================================================
    # File Delete
    # =========================================================================
    
    def delete_file(
        self,
        entry_id: int,
        field_id: Union[int, str],
    ) -> bool:
        """
        Delete a file attachment.

        API path: DELETE .../entryfiles/{entryId}/fields/{fieldId} (no object in path).

        Args:
            entry_id: Entry ID containing the file
            field_id: Field ID or API name of the attachment field

        Returns:
            True if successful

        Example:
            dc.delete_file(123, "Logo")
        """
        url = f"{self._files_url}/{entry_id}/fields/{field_id}"
        self._client.delete(url)
        return True

    def delete_attachment(
        self,
        entry_id: int,
        field_id: Union[int, str],
    ) -> bool:
        """
        Delete an attachment (alias for delete_file).

        Same signature and behavior as delete_file. Prefer this name when
        working with the Attachments object or attachment-style fields.
        """
        return self.delete_file(entry_id=entry_id, field_id=field_id)

    # =========================================================================
    # Upload to Attachments (documented API flow)
    # =========================================================================

    def upload_attachment(
        self,
        object_id: Union[int, str],
        content: bytes,
        file_name: str,
        content_type: Optional[str] = None,
        title: Optional[str] = None,
    ) -> dict:
        """
        Upload a file to the attachments system object (documented flow).

        Uses POST .../entrydata/{object_id} (multipart model + file). Object names
        are site-configurable (typically "Attachment"). See how_to_upload_files
        guide. Use the returned entry_id with download_file() and delete_data(object_id, [entry_id])
        to remove the record.

        Args:
            object_id: Object ID or API name for the attachments object (e.g. "Attachment").
            content: File content as bytes.
            file_name: Name for the file (e.g. "report.pdf").
            content_type: MIME type (auto-detected from file_name extension if None).
            title: Title for the attachment record (defaults to file_name).

        Returns:
            Dict with "entry_id" (int, the new attachment row id), "document_field_id" (int),
            and "response" (list of cell results from the API).

        Example:
            result = dc.upload_attachment(
                "Attachment", b"content", "test.txt", content_type="text/plain"
            )
            entry_id = result["entry_id"]
            doc_field_id = result["document_field_id"]
            data = dc.download_file(entry_id, doc_field_id)
            dc.delete_data("Attachment", [entry_id])
        """
        if not content_type:
            content_type = self._get_content_type(Path(file_name).suffix)
        title_value = title if title is not None else file_name
        format_type = Path(file_name).suffix.lstrip(".").lower() or "bin"

        fields = self.get_fields(object_id)
        title_field = next((f for f in fields if getattr(f, "apiName", None) == "Title"), None)
        document_field = next(
            (f for f in fields if getattr(f, "fieldType", None) == field_types.BINARY),
            None,
        )
        if not title_field or not document_field:
            raise ValueError(
                f"Object {object_id!r} must have Title and Document (binary) fields. "
                f"Resolve via get_fields({object_id!r})."
            )
        title_field_id = getattr(title_field, "id", None)
        document_field_id = getattr(document_field, "id", None)
        if not title_field_id or not document_field_id:
            raise ValueError("Title and Document fields must have id.")

        model = {
            "storeRequests": [
                {
                    "value": title_value,
                    "ignoreNearDups": True,
                    "entryId": -1,
                    "fieldId": title_field_id,
                }
            ],
            "binaryStoreRequests": [
                {
                    "formatType": format_type,
                    "contentType": content_type,
                    "name": file_name,
                    "entryId": -1,
                    "fieldId": document_field_id,
                }
            ],
        }
        url = f"{self._entrydata_url}/{object_id}"
        response = self._client.post_raw(
            url,
            data={"model": json.dumps(model)},
            files={"attachment": (file_name, content, content_type)},
        )
        body = response.json() if response.content else []
        if not isinstance(body, list):
            return {"entry_id": None, "document_field_id": document_field_id, "response": body}
        row_id = None
        for item in body:
            if isinstance(item, dict) and "rowId" in item:
                row_id = item["rowId"]
                break
        return {
            "entry_id": row_id,
            "document_field_id": document_field_id,
            "response": body,
        }

    def upload_file_to_entry_field(
        self,
        object_id: Union[int, str],
        entry_id: int,
        field: Union[int, str],
        content: bytes,
        file_name: str,
        content_type: Optional[str] = None,
    ) -> dict:
        """
        Upload file bytes onto an existing row's IMAGE (16) or BINARY (13) field.

        Uses the same multipart POST .../entrydata/{object_id} flow as
        :meth:`upload_attachment`, but targets ``entry_id`` and the given field.
        Call once per file for multi-image fields.

        Args:
            object_id: Object API name or id containing the field.
            entry_id: Existing entry id (positive integer).
            field: Field API name or numeric field id.
            content: Raw file bytes.
            file_name: Filename sent to the API (drives format / MIME if needed).
            content_type: Optional MIME type (inferred from extension when omitted).

        Returns:
            Dict with ``entry_id``, ``field_id`` (int), and ``response`` (API body).
        """
        if not content_type:
            content_type = self._get_content_type(Path(file_name).suffix)
        format_type = Path(file_name).suffix.lstrip(".").lower() or "bin"

        fields = self.get_fields(object_id)
        if isinstance(field, str):
            fld = next((f for f in fields if f.apiName == field), None)
            if not fld or fld.id is None:
                raise ValueError(f"No field {field!r} on object {object_id!r}")
            field_id = fld.id
            ft = fld.fieldType
        else:
            fld = next((f for f in fields if f.id == field), None)
            if not fld:
                raise ValueError(f"No field id {field} on object {object_id!r}")
            field_id = fld.id
            ft = fld.fieldType

        if ft not in (field_types.IMAGE, field_types.BINARY):
            raise ValueError(
                f"Field {getattr(fld, 'apiName', field)!r} must be IMAGE or BINARY; "
                f"fieldType={ft}"
            )

        model = {
            "binaryStoreRequests": [
                {
                    "formatType": format_type,
                    "contentType": content_type,
                    "name": file_name,
                    "entryId": entry_id,
                    "fieldId": field_id,
                }
            ]
        }
        url = f"{self._entrydata_url}/{object_id}"
        response = self._client.post_raw(
            url,
            data={"model": json.dumps(model)},
            files={"attachment": (file_name, content, content_type)},
        )
        body = response.json() if response.content else []
        return {
            "entry_id": entry_id,
            "field_id": field_id,
            "response": body,
        }

    # =========================================================================
    # Helpers
    # =========================================================================

    # Extension -> MIME type (single source of truth; _get_extension reverse is derived)
    _EXTENSION_TO_CONTENT_TYPE = {
        # Documents – PDF & Office
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xls": "application/vnd.ms-excel",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".ppt": "application/vnd.ms-powerpoint",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".odt": "application/vnd.oasis.opendocument.text",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
        ".odp": "application/vnd.oasis.opendocument.presentation",
        ".rtf": "application/rtf",
        # Images
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".ico": "image/x-icon",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".heic": "image/heic",
        ".avif": "image/avif",
        ".jfif": "image/jpeg",
        # Audio
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4",
        ".flac": "audio/flac",
        ".aac": "audio/aac",
        ".weba": "audio/webm",
        ".wma": "audio/x-ms-wma",
        # Video
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        ".avi": "video/x-msvideo",
        ".wmv": "video/x-ms-wmv",
        ".mkv": "video/x-matroska",
        ".m4v": "video/x-m4v",
        ".ogv": "video/ogg",
        ".3gp": "video/3gpp",
        # Text / data
        ".txt": "text/plain",
        ".csv": "text/csv",
        ".html": "text/html",
        ".htm": "text/html",
        ".json": "application/json",
        ".xml": "application/xml",
        ".yaml": "application/x-yaml",
        ".yml": "application/x-yaml",
        ".md": "text/markdown",
        ".css": "text/css",
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".ts": "text/typescript",
        ".tsv": "text/tab-separated-values",
        # Archives
        ".zip": "application/zip",
        ".tar": "application/x-tar",
        ".gz": "application/gzip",
        ".gzip": "application/gzip",
        ".7z": "application/x-7z-compressed",
        ".rar": "application/vnd.rar",
        ".xz": "application/x-xz",
        ".bz2": "application/x-bzip2",
        # Email / messaging
        ".eml": "message/rfc822",
        ".msg": "application/vnd.ms-outlook",
        # Fonts
        ".woff": "font/woff",
        ".woff2": "font/woff2",
        ".ttf": "font/ttf",
        ".otf": "font/otf",
        ".eot": "application/vnd.ms-fontobject",
    }
    # Reverse map: content type -> canonical extension (first extension per type)
    _ct_to_ext = {}
    for _ext, _ct in _EXTENSION_TO_CONTENT_TYPE.items():
        if _ct not in _ct_to_ext:
            _ct_to_ext[_ct] = _ext
    _CONTENT_TYPE_TO_EXTENSION = _ct_to_ext

    def _get_content_type(self, suffix: str) -> str:
        """Get MIME type from file extension."""
        return self._EXTENSION_TO_CONTENT_TYPE.get(suffix.lower(), "application/octet-stream")

    def _get_extension(self, content_type: str) -> str:
        """Get file extension from MIME type (canonical extension per type)."""
        # Strip parameters (e.g. "text/plain; charset=utf-8" -> "text/plain")
        base_type = content_type.split(";")[0].strip().lower()
        return self._CONTENT_TYPE_TO_EXTENSION.get(base_type, "")
    
    def get_content_type(self, file_extension: str) -> str:
        """
        Get MIME content type from a file extension.
        
        Useful when uploading files programmatically and you need
        to determine the correct Content-Type header.
        
        Args:
            file_extension: File extension (e.g., ".pdf", "pdf", ".PDF")
        
        Returns:
            MIME type string (e.g., "application/pdf")
            Returns "application/octet-stream" for unknown extensions.
        
        Example:
            >>> dc.get_content_type(".pdf")
            'application/pdf'
            >>> dc.get_content_type("xlsx")
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            >>> dc.get_content_type(".unknown")
            'application/octet-stream'
        
        Supported extensions include PDF, Office (.doc/.docx, .xls/.xlsx, .ppt/.pptx),
        OpenDocument (.odt, .ods, .odp), images (.png, .jpg, .gif, .webp, .svg, .tiff, etc.),
        audio (.mp3, .wav, .m4a, .flac), video (.mp4, .webm, .mov), text (.txt, .csv, .html,
        .json, .xml, .yaml, .md), archives (.zip, .tar, .gz, .7z, .rar), and fonts (.woff, .ttf).
        Unknown extensions return "application/octet-stream".
        """
        # Normalize: ensure leading dot and lowercase
        suffix = file_extension if file_extension.startswith('.') else f".{file_extension}"
        return self._get_content_type(suffix.lower())
    
    def get_extension(self, content_type: str) -> str:
        """
        Get file extension from MIME content type.
        
        Useful when downloading files and you need to determine
        the file extension from the Content-Type header.
        
        Args:
            content_type: MIME type (e.g., "application/pdf", "image/png")
        
        Returns:
            File extension with leading dot (e.g., ".pdf")
            Returns empty string for unknown content types.
        
        Example:
            >>> dc.get_extension("application/pdf")
            '.pdf'
            >>> dc.get_extension("image/jpeg")
            '.jpg'
            >>> dc.get_extension("unknown/type")
            ''
            
            >>> # Use with file downloads
            >>> response = client.get_raw("/files/123")
            >>> ext = dc.get_extension(response.headers.get("Content-Type", ""))
            >>> with open(f"download{ext}", "wb") as f:
            ...     f.write(response.content)
        """
        return self._get_extension(content_type)

    # =========================================================================
    # Bulk Export Helpers
    # =========================================================================

    def _find_file_fields(
        self,
        object_id: Optional[Union[int, str]] = None,
        field_type: int = field_types.IMAGE,
    ) -> List[Dict]:
        """
        Find all fields of a specific type (IMAGE or BINARY).
        
        Args:
            object_id: Filter to specific object, or None for all objects
            field_type: Field type to find (16=IMAGE, 13=BINARY)
        
        Returns:
            List of {object_id, object_name, field} dicts
        """
        result = []
        
        if object_id:
            # Single object
            fields = self.get_fields(object_id)
            obj = self.get_objects()
            obj_info = next((o for o in obj if o.apiName == object_id or o.id == object_id), None)
            obj_name = obj_info.apiName if obj_info else str(object_id)
            
            for f in fields:
                if f.fieldType == field_type:
                    result.append({
                        "object_id": object_id,
                        "object_name": obj_name,
                        "field": f,
                    })
        else:
            # All objects
            objects = self.get_objects()
            for obj in objects:
                try:
                    fields = self.get_fields(obj.id)
                    for f in fields:
                        if f.fieldType == field_type:
                            result.append({
                                "object_id": obj.id,
                                "object_name": obj.apiName,
                                "field": f,
                            })
                except Exception as e:
                    self._logger.warning(f"Could not get fields for {obj.apiName}: {e}")
        
        return result

    def _find_attachment_fields(
        self,
        object_id: Optional[Union[int, str]] = None,
    ) -> List[Dict]:
        """
        Find all attachment reference fields (reference fields with isAttachment=True).
        
        These are fields that reference the Attachments system object.
        
        Args:
            object_id: Filter to specific object, or None for all objects
        
        Returns:
            List of {object_id, object_name, field} dicts
        """
        result = []
        
        if object_id:
            fields = self.get_fields(object_id)
            obj = self.get_objects()
            obj_info = next((o for o in obj if o.apiName == object_id or o.id == object_id), None)
            obj_name = obj_info.apiName if obj_info else str(object_id)
            
            for f in fields:
                if f.fieldType == field_types.REFERENCE and getattr(f, 'isAttachment', False):
                    result.append({
                        "object_id": object_id,
                        "object_name": obj_name,
                        "field": f,
                    })
        else:
            objects = self.get_objects()
            for obj in objects:
                try:
                    fields = self.get_fields(obj.id)
                    for f in fields:
                        if f.fieldType == field_types.REFERENCE and getattr(f, 'isAttachment', False):
                            result.append({
                                "object_id": obj.id,
                                "object_name": obj.apiName,
                                "field": f,
                            })
                except Exception as e:
                    self._logger.warning(f"Could not get fields for {obj.apiName}: {e}")
        
        return result
    
    # =========================================================================
    # Public File Discovery Methods
    # =========================================================================
    
    def find_file_fields(
        self,
        object_id: Optional[Union[int, str]] = None,
        field_type: str = "image",
    ) -> List[Dict]:
        """
        Find all file fields (IMAGE or BINARY) in the schema.
        
        Essential for building backup/migration tools that need to discover
        all file fields for export operations.
        
        Args:
            object_id: Filter to specific object, or None for all objects
            field_type: Type of field to find:
                - "image": Image fields (fieldType=16)
                - "binary": Binary/document fields (fieldType=13)
                - "all": Both image and binary fields
        
        Returns:
            List of dicts, each containing:
            - object_id: Object ID
            - object_name: Object API name
            - field: Field object
        
        Example:
            >>> # Find all image fields in the site
            >>> image_fields = dc.find_file_fields()
            >>> for f in image_fields:
            ...     print(f"{f['object_name']}.{f['field'].apiName}")
            Company.Logo
            Contact.Photo
            
            >>> # Find document fields in a specific object
            >>> doc_fields = dc.find_file_fields("Deal", field_type="binary")
            >>> for f in doc_fields:
            ...     print(f"Deal.{f['field'].apiName}")
            
            >>> # Find all file fields (images + documents)
            >>> all_files = dc.find_file_fields(field_type="all")
        
        Note:
            Use find_attachment_fields() for reference-based attachments.
        """
        if field_type == "image":
            return self._find_file_fields(object_id, field_types.IMAGE)
        elif field_type == "binary":
            return self._find_file_fields(object_id, field_types.BINARY)
        elif field_type == "all":
            images = self._find_file_fields(object_id, field_types.IMAGE)
            binaries = self._find_file_fields(object_id, field_types.BINARY)
            return images + binaries
        else:
            raise ValueError(f"field_type must be 'image', 'binary', or 'all', got: {field_type}")
    
    def find_attachment_fields(
        self,
        object_id: Optional[Union[int, str]] = None,
    ) -> List[Dict]:
        """
        Find all attachment reference fields in the schema.
        
        Attachment fields are reference fields (fieldType=5) that point to
        the Attachments system object (isAttachment=True). This is distinct
        from IMAGE and BINARY fields.
        
        Args:
            object_id: Filter to specific object, or None for all objects
        
        Returns:
            List of dicts, each containing:
            - object_id: Object ID
            - object_name: Object API name  
            - field: Field object
        
        Example:
            >>> # Find all attachment fields in the site
            >>> attachments = dc.find_attachment_fields()
            >>> for f in attachments:
            ...     print(f"{f['object_name']}.{f['field'].apiName}")
            Deal.Contracts
            Company.Documents
            
            >>> # Find attachment fields in a specific object
            >>> deal_attachments = dc.find_attachment_fields("Deal")
        
        Note:
            - Attachment fields are reference fields to the Attachments object
            - Use find_file_fields() for IMAGE and BINARY (inline) file fields
            - Both methods are needed for complete file discovery
        """
        return self._find_attachment_fields(object_id)

    def _build_export_path(
        self,
        naming: str,
        object_name: str,
        entry_id: int,
        field_name: str,
        extension: str,
    ) -> str:
        """
        Build export path from naming template.
        
        Supported placeholders:
        - {object}: Object API name
        - {entry_id}: Entry ID
        - {field_name}: Field API name
        - {ext}: File extension (without dot)
        """
        return naming.format(
            object=object_name,
            entry_id=entry_id,
            field_name=field_name,
            ext=extension.lstrip("."),
        )

    def export_images(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        storage: Optional[StorageBackend] = None,
        object_id: Optional[Union[int, str]] = None,
        entry_ids: Optional[List[int]] = None,
        field_ids: Optional[List[Union[int, str]]] = None,
        query: Optional[str] = None,
        naming: str = "{object}/{entry_id}_{field_name}.{ext}",
        overwrite: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> ExportResult:
        """
        Export images from DealCloud image fields (fieldType: 16).
        
        Supports three scopes:
        - Site-wide: No filters (exports all images from all objects)
        - Object-level: Specify object_id
        - Entry-level: Specify object_id + entry_ids
        
        Args:
            output_dir: Local directory path. Creates LocalStorage automatically.
                       Supports UNC paths for network shares.
            storage: Custom storage backend (overrides output_dir).
                    Implement StorageBackend protocol for cloud storage.
            object_id: Filter to specific object (e.g., "Company")
            entry_ids: Filter to specific entries (requires object_id)
            field_ids: Filter to specific image fields
            query: DealCloud query to filter entries
            naming: Path template with placeholders:
                   {object}, {entry_id}, {field_name}, {ext}
            overwrite: If True, overwrite existing files. If False, skip.
            on_progress: Callback(current, total) for progress updates
        
        Returns:
            ExportResult with counts and error details
        
        Example:
            >>> # Export all images to local disk
            >>> result = dc.export_images("./backup/images")
            >>> print(f"Exported {result.exported}/{result.total_files}")
            >>> 
            >>> # Export Company logos only
            >>> result = dc.export_images(
            ...     "./logos",
            ...     object_id="Company",
            ...     field_ids=["Logo"]
            ... )
            >>> 
            >>> # Export to network share
            >>> result = dc.export_images(r"\\\\server\\share\\images")
            >>> 
            >>> # Export to S3 (custom backend)
            >>> s3 = S3Storage("my-bucket", prefix="dealcloud/images")
            >>> result = dc.export_images(storage=s3, object_id="Company")
        """
        # Create storage backend
        if storage is None:
            if output_dir is None:
                raise ValueError("Either output_dir or storage must be provided")
            storage = LocalStorage(output_dir)
        
        result = ExportResult(output_path=str(output_dir) if output_dir else None)
        
        # Find image fields
        image_fields = self._find_file_fields(object_id, field_types.IMAGE)
        
        # Filter by field_ids if specified
        if field_ids:
            field_ids_set = set(str(f) for f in field_ids)
            image_fields = [
                f for f in image_fields
                if str(f["field"].id) in field_ids_set or f["field"].apiName in field_ids_set
            ]
        
        if not image_fields:
            self._logger.info("No image fields found")
            return result
        
        # Process each object/field combination
        for field_info in image_fields:
            obj_id = field_info["object_id"]
            obj_name = field_info["object_name"]
            fld = field_info["field"]
            
            # Get entries with this field
            try:
                if entry_ids:
                    # Specific entries
                    ids_csv = ",".join(str(eid) for eid in entry_ids)
                    q = f"EntryId in ({ids_csv})"
                    if query:
                        q = f"({query}) AND ({q})"
                elif query:
                    q = query
                else:
                    q = None
                
                # Read entries to find which have files
                entries = self.read_data(
                    object_id=obj_id,
                    fields=["EntryId", fld.apiName],
                    query=q,
                    output="list",
                )
                
                # Export each entry's file
                for entry in entries:
                    entry_id = entry.get("EntryId")
                    file_value = entry.get(fld.apiName)
                    
                    if not entry_id or not file_value:
                        continue
                    
                    result.total_files += 1
                    
                    try:
                        # Get file info first
                        file_info = self.download_attachment_metadata(obj_id, entry_id, fld.id)
                        content_type = file_info.get("contentType", "image/png")
                        ext = self._get_extension(content_type) or ".png"
                        
                        # Build output path
                        path = self._build_export_path(
                            naming, obj_name, entry_id, fld.apiName, ext
                        )
                        
                        # Check if exists
                        if not overwrite and storage.exists(path):
                            result.skipped += 1
                            continue
                        
                        # Download and save
                        content = self.download_file(entry_id, fld.id)
                        if isinstance(content, bytes):
                            saved_path = storage.write(path, content, content_type)
                            result.exported += 1
                            result.files.append(saved_path)
                        
                        if on_progress:
                            on_progress(result.exported + result.failed + result.skipped, result.total_files)
                            
                    except Exception as e:
                        result.failed += 1
                        result.errors.append({
                            "object": obj_name,
                            "entry_id": entry_id,
                            "field": fld.apiName,
                            "error": str(e),
                        })
                        self._logger.warning(f"Failed to export {obj_name}/{entry_id}/{fld.apiName}: {e}")
                        
            except Exception as e:
                self._logger.warning(f"Failed to read entries for {obj_name}.{fld.apiName}: {e}")
        
        return result

    def export_documents(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        storage: Optional[StorageBackend] = None,
        object_id: Optional[Union[int, str]] = None,
        entry_ids: Optional[List[int]] = None,
        field_ids: Optional[List[Union[int, str]]] = None,
        query: Optional[str] = None,
        naming: str = "{object}/{entry_id}_{field_name}.{ext}",
        overwrite: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> ExportResult:
        """
        Export documents from DealCloud binary/attachment fields (fieldType: 13).
        
        This exports files from BINARY fields, which typically hold documents
        like PDFs, Word docs, etc.
        
        Supports three scopes:
        - Site-wide: No filters (exports all documents from all objects)
        - Object-level: Specify object_id
        - Entry-level: Specify object_id + entry_ids
        
        Args:
            output_dir: Local directory path. Creates LocalStorage automatically.
                       Supports UNC paths for network shares.
            storage: Custom storage backend (overrides output_dir).
            object_id: Filter to specific object
            entry_ids: Filter to specific entries (requires object_id)
            field_ids: Filter to specific binary fields
            query: DealCloud query to filter entries
            naming: Path template with placeholders
            overwrite: If True, overwrite existing files
            on_progress: Callback(current, total) for progress updates
        
        Returns:
            ExportResult with counts and error details
        
        Example:
            >>> # Export all documents
            >>> result = dc.export_documents("./backup/docs")
            >>> 
            >>> # Export Deal documents only
            >>> result = dc.export_documents(
            ...     "./deal_docs",
            ...     object_id="Deal",
            ...     field_ids=["Contract", "Proposal"]
            ... )
            >>> 
            >>> # Export to Azure Blob
            >>> azure = AzureBlobStorage(conn_string, "documents")
            >>> result = dc.export_documents(storage=azure)
        """
        # Create storage backend
        if storage is None:
            if output_dir is None:
                raise ValueError("Either output_dir or storage must be provided")
            storage = LocalStorage(output_dir)
        
        result = ExportResult(output_path=str(output_dir) if output_dir else None)
        
        # Find binary fields
        binary_fields = self._find_file_fields(object_id, field_types.BINARY)
        
        # Filter by field_ids if specified
        if field_ids:
            field_ids_set = set(str(f) for f in field_ids)
            binary_fields = [
                f for f in binary_fields
                if str(f["field"].id) in field_ids_set or f["field"].apiName in field_ids_set
            ]
        
        if not binary_fields:
            self._logger.info("No binary/document fields found")
            return result
        
        # Process each object/field combination
        for field_info in binary_fields:
            obj_id = field_info["object_id"]
            obj_name = field_info["object_name"]
            fld = field_info["field"]
            
            try:
                if entry_ids:
                    ids_csv = ",".join(str(eid) for eid in entry_ids)
                    q = f"EntryId in ({ids_csv})"
                    if query:
                        q = f"({query}) AND ({q})"
                elif query:
                    q = query
                else:
                    q = None
                
                entries = self.read_data(
                    object_id=obj_id,
                    fields=["EntryId", fld.apiName],
                    query=q,
                    output="list",
                )
                
                for entry in entries:
                    entry_id = entry.get("EntryId")
                    file_value = entry.get(fld.apiName)
                    
                    if not entry_id or not file_value:
                        continue
                    
                    result.total_files += 1
                    
                    try:
                        file_info = self.download_attachment_metadata(obj_id, entry_id, fld.id)
                        content_type = file_info.get("contentType", "application/octet-stream")
                        file_name = file_info.get("fileName", "")
                        ext = Path(file_name).suffix if file_name else self._get_extension(content_type) or ".bin"
                        
                        path = self._build_export_path(
                            naming, obj_name, entry_id, fld.apiName, ext
                        )
                        
                        if not overwrite and storage.exists(path):
                            result.skipped += 1
                            continue
                        
                        content = self.download_file(entry_id, fld.id)
                        if isinstance(content, bytes):
                            saved_path = storage.write(path, content, content_type)
                            result.exported += 1
                            result.files.append(saved_path)
                        
                        if on_progress:
                            on_progress(result.exported + result.failed + result.skipped, result.total_files)
                            
                    except Exception as e:
                        result.failed += 1
                        result.errors.append({
                            "object": obj_name,
                            "entry_id": entry_id,
                            "field": fld.apiName,
                            "error": str(e),
                        })
                        self._logger.warning(f"Failed to export {obj_name}/{entry_id}/{fld.apiName}: {e}")
                        
            except Exception as e:
                self._logger.warning(f"Failed to read entries for {obj_name}.{fld.apiName}: {e}")
        
        return result

    def export_files(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        storage: Optional[StorageBackend] = None,
        object_id: Optional[Union[int, str]] = None,
        entry_ids: Optional[List[int]] = None,
        include_images: bool = True,
        include_documents: bool = True,
        naming: str = "{object}/{entry_id}_{field_name}.{ext}",
        overwrite: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> ExportResult:
        """
        Export all files (images and documents) from DealCloud.
        
        Combines export_images() and export_documents() functionality
        in a single operation.
        
        Args:
            output_dir: Local directory path
            storage: Custom storage backend (overrides output_dir)
            object_id: Filter to specific object
            entry_ids: Filter to specific entries
            include_images: Export image fields (fieldType: 16)
            include_documents: Export binary/document fields (fieldType: 13)
            naming: Path template with placeholders
            overwrite: If True, overwrite existing files
            on_progress: Callback(current, total) for progress updates
        
        Returns:
            Combined ExportResult from both operations
        
        Example:
            >>> # Export everything
            >>> result = dc.export_files("./backup/all_files")
            >>> print(f"Images: {images}, Documents: {docs}")
            >>> 
            >>> # Export from specific object
            >>> result = dc.export_files(
            ...     "./company_files",
            ...     object_id="Company"
            ... )
        """
        # Create storage backend
        if storage is None:
            if output_dir is None:
                raise ValueError("Either output_dir or storage must be provided")
            storage = LocalStorage(output_dir)
        
        combined = ExportResult(output_path=str(output_dir) if output_dir else None)
        
        if include_images:
            img_result = self.export_images(
                storage=storage,
                object_id=object_id,
                entry_ids=entry_ids,
                naming=naming,
                overwrite=overwrite,
                on_progress=on_progress,
            )
            combined.total_files += img_result.total_files
            combined.exported += img_result.exported
            combined.failed += img_result.failed
            combined.skipped += img_result.skipped
            combined.errors.extend(img_result.errors)
            combined.files.extend(img_result.files)
        
        if include_documents:
            doc_result = self.export_documents(
                storage=storage,
                object_id=object_id,
                entry_ids=entry_ids,
                naming=naming,
                overwrite=overwrite,
                on_progress=on_progress,
            )
            combined.total_files += doc_result.total_files
            combined.exported += doc_result.exported
            combined.failed += doc_result.failed
            combined.skipped += doc_result.skipped
            combined.errors.extend(doc_result.errors)
            combined.files.extend(doc_result.files)
        
        return combined

    def export_attachments(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        storage: Optional[StorageBackend] = None,
        object_id: Optional[Union[int, str]] = None,
        entry_ids: Optional[List[int]] = None,
        include_images: bool = True,
        include_documents: bool = True,
        naming: str = "{object}/{entry_id}_{field_name}.{ext}",
        overwrite: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> ExportResult:
        """
        Export all attachments (alias for export_files).

        Same signature and behavior as export_files. Prefer this name when
        exporting attachment-style file fields.
        """
        return self.export_files(
            output_dir=output_dir,
            storage=storage,
            object_id=object_id,
            entry_ids=entry_ids,
            include_images=include_images,
            include_documents=include_documents,
            naming=naming,
            overwrite=overwrite,
            on_progress=on_progress,
        )

    def export_entry_files(
        self,
        object_id: Union[int, str],
        entry_id: int,
        output_dir: Optional[Union[str, Path]] = None,
        storage: Optional[StorageBackend] = None,
        include_images: bool = True,
        include_documents: bool = True,
    ) -> ExportResult:
        """
        Export all files from a single entry.
        
        Convenience method for exporting all files attached to one record.
        
        Args:
            object_id: Object API name or ID
            entry_id: Entry ID to export files from
            output_dir: Local directory path
            storage: Custom storage backend (overrides output_dir)
            include_images: Export image fields
            include_documents: Export binary/document fields
        
        Returns:
            ExportResult for this entry's files
        
        Example:
            >>> # Export all files from Deal #12345
            >>> result = dc.export_entry_files("Deal", 12345, "./deal_12345_files")
            >>> print(f"Exported {result.exported} files")
            >>> 
            >>> # Export to S3
            >>> s3 = S3Storage("bucket", "deals/12345")
            >>> result = dc.export_entry_files("Deal", 12345, storage=s3)
        """
        return self.export_files(
            output_dir=output_dir,
            storage=storage,
            object_id=object_id,
            entry_ids=[entry_id],
            include_images=include_images,
            include_documents=include_documents,
            naming="{field_name}.{ext}",  # Simpler naming for single entry
        )
