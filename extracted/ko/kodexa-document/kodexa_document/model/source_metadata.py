"""
SourceMetadata class for legacy_python compatibility.

Provides a mutable dataclass that supports dot notation for accessing and
modifying document source information, matching the legacy_python structure.
"""
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any


@dataclass
class SourceMetadata:
    """
    Source metadata for a document, matching legacy_python structure.

    This class is mutable and supports dot notation for field access.
    Any change triggers a save of the entire source to Go.
    """
    original_filename: Optional[str] = None
    original_path: Optional[str] = None
    checksum: Optional[str] = None
    cid: Optional[str] = None
    last_modified: Optional[str] = None
    created: Optional[str] = None
    connector: Optional[str] = None
    mime_type: Optional[str] = None
    headers: Optional[Dict] = field(default_factory=dict)
    lineage_document_uuid: Optional[str] = None
    source_document_uuid: Optional[str] = None
    pdf_document_uuid: Optional[str] = None

    # Private field for document reference
    _document: Any = field(default=None, repr=False, compare=False)

    def __setattr__(self, name, value):
        """Override to trigger save to Go on any change."""
        super().__setattr__(name, value)
        if not name.startswith('_') and self._document:
            self._save_to_go()

    def _save_to_go(self):
        """Save entire source metadata to Go."""
        if not self._document:
            return

        from .._native import lib, ffi
        from ..errors import check_error

        # Convert to dict, excluding private fields
        source_dict = {k: v for k, v in asdict(self).items()
                      if not k.startswith('_')}

        # Convert field names from Python snake_case to JSON camelCase
        json_dict = {}
        field_mapping = {
            'original_filename': 'originalFilename',
            'original_path': 'originalPath',
            'checksum': 'checksum',
            'cid': 'cid',
            'last_modified': 'lastModified',
            'created': 'created',
            'connector': 'connector',
            'mime_type': 'mimeType',
            'headers': 'headers',
            'lineage_document_uuid': 'lineageDocumentUuid',
            'source_document_uuid': 'sourceDocumentUuid',
            'pdf_document_uuid': 'pdfDocumentUuid'
        }

        for python_key, json_key in field_mapping.items():
            if python_key in source_dict and source_dict[python_key] is not None:
                json_dict[json_key] = source_dict[python_key]

        source_json = json.dumps(json_dict)
        source_bytes = source_json.encode('utf-8')

        result = lib.SetDocumentSource(self._document._handle, source_bytes)
        check_error()

        if result == 0:
            raise RuntimeError("Failed to set document source")

    @classmethod
    def from_dict(cls, data: Dict[str, Any], document=None) -> 'SourceMetadata':
        """
        Create SourceMetadata from a dictionary with JSON field names.

        Converts from camelCase (JSON) to snake_case (Python).
        """
        # Map JSON camelCase to Python snake_case
        field_mapping = {
            'originalFilename': 'original_filename',
            'originalPath': 'original_path',
            'checksum': 'checksum',
            'cid': 'cid',
            'lastModified': 'last_modified',
            'created': 'created',
            'connector': 'connector',
            'mimeType': 'mime_type',
            'headers': 'headers',
            'lineageDocumentUuid': 'lineage_document_uuid',
            'sourceDocumentUuid': 'source_document_uuid',
            'pdfDocumentUuid': 'pdf_document_uuid'
        }

        # Convert field names
        python_data = {}
        for json_key, python_key in field_mapping.items():
            if json_key in data:
                python_data[python_key] = data[json_key]

        # Create instance with document reference
        return cls(_document=document, **python_data)
