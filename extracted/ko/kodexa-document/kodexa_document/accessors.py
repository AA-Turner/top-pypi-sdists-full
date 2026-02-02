"""
Accessor classes for native document operations.

These accessors provide a consistent pattern for accessing document data
through the Go native library, matching the Java and TypeScript implementations.
"""

import json
import base64
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, TYPE_CHECKING

from ._native import ffi, get_library
from .errors import check_error

if TYPE_CHECKING:
    from .model.document import Document

lib = get_library()


def _parse_json_result(json_ptr) -> Any:
    """Parse a JSON result from the native library."""
    if json_ptr == ffi.NULL:
        return None
    try:
        json_str = ffi.string(json_ptr).decode('utf-8')
        if not json_str or json_str == 'null' or json_str == '[]':
            return None
        return json.loads(json_str)
    finally:
        lib.FreeString(json_ptr)


def _to_c_string(s: Optional[str]) -> Any:
    """Convert a Python string to a C string, or NULL if None."""
    if s is None:
        return ffi.NULL
    return s.encode('utf-8')


# ============================================================================
# Data Attribute Accessor
# ============================================================================

@dataclass
class DataAttributeInput:
    """Input for creating/updating a data attribute."""
    tag: Optional[str] = None
    tag_uuid: Optional[str] = None
    value: Optional[Any] = None
    string_value: Optional[str] = None
    decimal_value: Optional[float] = None
    date_value: Optional[str] = None
    boolean_value: Optional[bool] = None
    confidence: Optional[float] = None
    type_at_creation: Optional[str] = None
    path: Optional[str] = None
    owner_uri: Optional[str] = None
    data_features: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {}
        if self.tag is not None:
            result['tag'] = self.tag
        if self.tag_uuid is not None:
            result['tagUUID'] = self.tag_uuid
        if self.value is not None:
            result['value'] = str(self.value)
        if self.string_value is not None:
            result['stringValue'] = self.string_value
        if self.decimal_value is not None:
            result['decimalValue'] = self.decimal_value
        if self.date_value is not None:
            result['dateValue'] = self.date_value
        if self.boolean_value is not None:
            result['booleanValue'] = self.boolean_value
        if self.confidence is not None:
            result['confidence'] = self.confidence
        if self.type_at_creation is not None:
            result['typeAtCreation'] = self.type_at_creation
        if self.path is not None:
            result['path'] = self.path
        if self.owner_uri is not None:
            result['ownerUri'] = self.owner_uri
        if self.data_features is not None:
            result['dataFeatures'] = self.data_features
        return result


class DataAttributeAccessor:
    """
    Accessor for data attributes in a document.

    Access via document.data_attributes property.
    """

    def __init__(self, document: 'Document'):
        self._document = document

    def get_for_data_object(self, data_object_id: int) -> List[Dict[str, Any]]:
        """
        Get data attributes for a specific data object.

        Args:
            data_object_id: The data object ID

        Returns:
            List of data attribute dictionaries
        """
        json_ptr = lib.DocumentGetDataAttributes(self._document._handle, data_object_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_by_id(self, attr_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a data attribute by ID.

        Args:
            attr_id: The attribute ID

        Returns:
            The data attribute dictionary, or None if not found
        """
        json_ptr = lib.DocumentGetDataAttributeByID(self._document._handle, attr_id)
        check_error()
        return _parse_json_result(json_ptr)

    def create(self, data_object_id: int, input: DataAttributeInput) -> Optional[Dict[str, Any]]:
        """
        Create a new data attribute for a data object.

        Args:
            data_object_id: The data object ID
            input: The attribute input data

        Returns:
            The created data attribute, or None on failure
        """
        attr_data = input.to_dict()
        attr_data['dataObjectId'] = data_object_id
        json_str = json.dumps(attr_data).encode('utf-8')

        new_id = lib.DocumentCreateDataAttribute(self._document._handle, json_str)
        check_error()

        if new_id <= 0:
            return None

        return self.get_by_id(new_id)

    def update(self, attr_id: int, input: DataAttributeInput) -> Optional[Dict[str, Any]]:
        """
        Update a data attribute by ID.

        Args:
            attr_id: The attribute ID
            input: The attribute input data

        Returns:
            The updated data attribute, or None on failure
        """
        existing = self.get_by_id(attr_id)
        if not existing:
            return None

        attr_data = input.to_dict()
        attr_data['id'] = attr_id
        attr_data['uuid'] = existing.get('uuid', '')
        attr_data['dataObjectId'] = existing.get('dataObjectId', 0)
        json_str = json.dumps(attr_data).encode('utf-8')

        result = lib.DocumentUpdateDataAttribute(self._document._handle, json_str)
        check_error()

        if result <= 0:
            return None

        return self.get_by_id(attr_id)

    def delete(self, attr_id: int) -> bool:
        """
        Delete a data attribute by ID.

        Args:
            attr_id: The attribute ID

        Returns:
            True if deleted successfully, False otherwise
        """
        result = lib.DocumentDeleteDataAttribute(self._document._handle, attr_id)
        check_error()
        return result > 0


# ============================================================================
# Data Object Accessor
# ============================================================================

@dataclass
class DataObjectInput:
    """Input for creating/updating a data object.

    Note: UUID now serves as the group identifier (previously separate group_uuid field).
    Parent relationships use parent_id (database FK) instead of parent_group_uuid.
    """
    uuid: Optional[str] = None  # UUID serves as the group identifier
    parent_id: Optional[int] = None  # Direct FK to parent DataObject ID
    taxonomy_ref: Optional[str] = None
    path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {}
        if self.uuid is not None:
            result['uuid'] = self.uuid
        if self.parent_id is not None:
            result['parentId'] = self.parent_id
        if self.taxonomy_ref is not None:
            result['taxonomyRef'] = self.taxonomy_ref
        if self.path is not None:
            result['path'] = self.path
        return result


class DataObjectAccessor:
    """
    Accessor for data objects in a document.

    Access via document.data_objects property.
    """

    def __init__(self, document: 'Document'):
        self._document = document

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all data objects in the document.

        Returns:
            List of data object dictionaries
        """
        json_ptr = lib.DocumentGetDataObjects(self._document._handle)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        """
        Get a data object by UUID.

        Args:
            uuid: The data object UUID

        Returns:
            The data object dictionary, or None if not found
        """
        if not uuid:
            return None
        json_ptr = lib.DocumentGetDataObjectByUUID(self._document._handle, uuid.encode('utf-8'))
        check_error()
        return _parse_json_result(json_ptr)

    def get_by_group_uuid(self, uuid: str) -> List[Dict[str, Any]]:
        """
        Get data objects by UUID (which serves as the group identifier).

        Note: UUID now serves as the group identifier (previously separate group_uuid field).

        Args:
            uuid: The data object UUID (serves as group identifier)

        Returns:
            List of data object dictionaries
        """
        if not uuid:
            return []
        json_ptr = lib.DocumentGetDataObjectsByGroupUUID(self._document._handle, uuid.encode('utf-8'))
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def create(self, input: DataObjectInput) -> Optional[Dict[str, Any]]:
        """
        Create a new data object in the document.

        Args:
            input: The data object input data

        Returns:
            The created data object, or None on failure
        """
        json_str = json.dumps(input.to_dict()).encode('utf-8')
        result_ptr = lib.DocumentCreateDataObject(self._document._handle, json_str)
        check_error()

        result = _parse_json_result(result_ptr)
        return result

    def update(self, uuid: str, input: DataObjectInput) -> Optional[Dict[str, Any]]:
        """
        Update a data object.

        Args:
            uuid: The data object UUID
            input: The data object input data

        Returns:
            The updated data object, or None on failure
        """
        if not uuid:
            return None

        obj_data = input.to_dict()
        obj_data['uuid'] = uuid
        json_str = json.dumps(obj_data).encode('utf-8')

        result_ptr = lib.DocumentUpdateDataObject(self._document._handle, uuid.encode('utf-8'), json_str)
        check_error()

        result = _parse_json_result(result_ptr)
        return result

    def delete(self, uuid: str) -> bool:
        """
        Delete a data object.

        Args:
            uuid: The data object UUID

        Returns:
            True if deleted successfully, False otherwise
        """
        if not uuid:
            return False

        existing = self.get_by_uuid(uuid)
        if not existing:
            return False

        result = lib.DocumentDeleteDataObject(self._document._handle, existing.get('id', 0))
        check_error()
        return result > 0

    def get_roots(self) -> List[Dict[str, Any]]:
        """
        Get root data objects (objects with no parent).

        Returns:
            List of root data object dictionaries
        """
        all_objects = self.get_all()
        return [obj for obj in all_objects if not obj.get('parentGroupUuid')]

    def get_children(self, parent_group_uuid: str) -> List[Dict[str, Any]]:
        """
        Get child data objects for a given parent.

        Args:
            parent_group_uuid: The parent group UUID

        Returns:
            List of child data object dictionaries
        """
        all_objects = self.get_all()
        return [obj for obj in all_objects if obj.get('parentGroupUuid') == parent_group_uuid]


# ============================================================================
# Audit Accessor
# ============================================================================

class AuditAccessor:
    """
    Accessor for audit data in a document.

    Provides methods to query audit revisions and audit history for data objects,
    data attributes, and tags.

    Access via document.audit property.
    """

    def __init__(self, document: 'Document'):
        self._document = document

    def list_revisions(self) -> List[Dict[str, Any]]:
        """
        Get all audit revisions in the document.

        Returns:
            List of audit revisions, ordered by timestamp descending
        """
        json_ptr = lib.DocumentListAuditRevisions(self._document._handle)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_revision(self, revision_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific audit revision by ID.

        Args:
            revision_id: The revision ID

        Returns:
            The audit revision, or None if not found
        """
        json_ptr = lib.DocumentGetAuditRevision(self._document._handle, revision_id)
        check_error()
        return _parse_json_result(json_ptr)

    def get_revision_details(self, revision_id: int) -> Optional[Dict[str, Any]]:
        """
        Get the complete details for a revision, including all audit entries.

        Args:
            revision_id: The revision ID

        Returns:
            The revision details, or None if not found
        """
        json_ptr = lib.DocumentGetRevisionDetails(self._document._handle, revision_id)
        check_error()
        return _parse_json_result(json_ptr)

    def get_data_object_history(self, data_object_id: int) -> List[Dict[str, Any]]:
        """
        Get the audit history for a specific data object.

        Args:
            data_object_id: The data object ID

        Returns:
            List of audit entries for the data object
        """
        json_ptr = lib.DocumentGetDataObjectAuditHistory(self._document._handle, data_object_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_data_attribute_history(self, data_attribute_id: int) -> List[Dict[str, Any]]:
        """
        Get the audit history for a specific data attribute.

        Args:
            data_attribute_id: The data attribute ID

        Returns:
            List of audit entries for the data attribute
        """
        json_ptr = lib.DocumentGetDataAttributeAuditHistory(self._document._handle, data_attribute_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_tag_history(self, tag_id: int) -> List[Dict[str, Any]]:
        """
        Get the audit history for a specific tag.

        Args:
            tag_id: The tag ID

        Returns:
            List of audit entries for the tag
        """
        json_ptr = lib.DocumentGetTagAuditHistory(self._document._handle, tag_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_data_object_audits_by_revision(self, revision_id: int) -> List[Dict[str, Any]]:
        """
        Get all data object audits for a specific revision.

        Args:
            revision_id: The revision ID

        Returns:
            List of data object audit entries for the revision
        """
        json_ptr = lib.DocumentGetDataObjectAuditsByRevision(self._document._handle, revision_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_data_attribute_audits_by_revision(self, revision_id: int) -> List[Dict[str, Any]]:
        """
        Get all data attribute audits for a specific revision.

        Args:
            revision_id: The revision ID

        Returns:
            List of data attribute audit entries for the revision
        """
        json_ptr = lib.DocumentGetDataAttributeAuditsByRevision(self._document._handle, revision_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_tag_audits_by_revision(self, revision_id: int) -> List[Dict[str, Any]]:
        """
        Get all tag audits for a specific revision.

        Args:
            revision_id: The revision ID

        Returns:
            List of tag audit entries for the revision
        """
        json_ptr = lib.DocumentGetTagAuditsByRevision(self._document._handle, revision_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []


# ============================================================================
# Native Document Accessor
# ============================================================================

@dataclass
class NativeDocumentInput:
    """Input for creating a native document."""
    filename: str
    mime_type: str
    data: bytes
    checksum: Optional[str] = None


class NativeDocumentAccessor:
    """
    Accessor for native documents (embedded files) in a document.

    Native documents are binary files (PDFs, images, Word docs, etc.) that are
    stored within the KDDB document.

    Access via document.native_documents property.
    """

    def __init__(self, document: 'Document'):
        self._document = document

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all native documents in the document.
        Note: Binary data is not included in the response. Use get_data(id) to retrieve the bytes.

        Returns:
            List of native documents (metadata only)
        """
        json_ptr = lib.DocumentGetNativeDocuments(self._document._handle)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Get a native document by ID.
        Note: Binary data is not included. Use get_data(id) to retrieve the bytes.

        Args:
            id: The native document ID

        Returns:
            The native document, or None if not found
        """
        json_ptr = lib.DocumentGetNativeDocumentByID(self._document._handle, id)
        check_error()
        return _parse_json_result(json_ptr)

    def get_first(self) -> Optional[Dict[str, Any]]:
        """
        Get the first native document.
        Note: Binary data is not included. Use get_data(id) to retrieve the bytes.

        Returns:
            The first native document, or None if no native documents exist
        """
        json_ptr = lib.DocumentGetFirstNativeDocument(self._document._handle)
        check_error()
        return _parse_json_result(json_ptr)

    def get_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Get a native document by filename.
        Note: Binary data is not included. Use get_data(id) to retrieve the bytes.

        Args:
            filename: The filename to search for

        Returns:
            The native document, or None if not found
        """
        if not filename:
            return None
        json_ptr = lib.DocumentGetNativeDocumentByFilename(self._document._handle, filename.encode('utf-8'))
        check_error()
        return _parse_json_result(json_ptr)

    def get_data(self, id: int) -> Optional[bytes]:
        """
        Get the binary data for a native document.

        Args:
            id: The native document ID

        Returns:
            The raw bytes, or None if not found or on error
        """
        out_len = ffi.new("int*")
        data_ptr = lib.DocumentGetNativeDocumentData(self._document._handle, id, out_len)
        check_error()

        if data_ptr == ffi.NULL:
            return None

        try:
            # The data is returned as base64-encoded string
            base64_str = ffi.string(data_ptr).decode('utf-8')
            return base64.b64decode(base64_str)
        except Exception:
            return None
        finally:
            lib.FreeString(data_ptr)

    def create(self, input: NativeDocumentInput) -> Optional[Dict[str, Any]]:
        """
        Create a new native document with binary data.

        Args:
            input: The native document input (filename, mime_type, data, optional checksum)

        Returns:
            The created native document, or None on failure
        """
        if not input.filename:
            raise ValueError("Filename cannot be null or empty")
        if not input.mime_type:
            raise ValueError("MIME type cannot be null or empty")
        if not input.data:
            raise ValueError("Data cannot be null or empty")

        # Base64 encode the data for transport
        base64_data = base64.b64encode(input.data).decode('utf-8')

        new_id = lib.DocumentCreateNativeDocument(
            self._document._handle,
            input.filename.encode('utf-8'),
            input.mime_type.encode('utf-8'),
            base64_data.encode('utf-8'),
            len(base64_data),
            input.checksum.encode('utf-8') if input.checksum else ffi.NULL
        )
        check_error()

        if new_id <= 0:
            return None

        return self.get_by_id(new_id)

    def delete(self, id: int) -> bool:
        """
        Delete a native document by ID.

        Args:
            id: The native document ID

        Returns:
            True if deleted successfully, False otherwise
        """
        result = lib.DocumentDeleteNativeDocument(self._document._handle, id)
        check_error()
        return result > 0

    def delete_all(self) -> bool:
        """
        Delete all native documents in the document.

        Returns:
            True if deleted successfully, False otherwise
        """
        result = lib.DocumentDeleteAllNativeDocuments(self._document._handle)
        check_error()
        return result > 0


# ============================================================================
# Note Accessor
# ============================================================================

class NoteType(Enum):
    """
    The NoteType enumeration represents the different formats a note can have.
    This includes MARKDOWN, TEXT, and HTML formats.
    """
    markdown = "MARKDOWN"
    text = "TEXT"
    html = "HTML"


@dataclass
class NoteInput:
    """Input for creating/updating a note."""
    content: str
    uuid: Optional[str] = None
    title: Optional[str] = None
    note_type: NoteType = NoteType.text
    data_object_id: Optional[int] = None
    data_attribute_id: Optional[int] = None
    group_uuid: Optional[str] = None
    parent_note_id: Optional[int] = None
    properties: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {'content': self.content}
        if self.uuid is not None:
            result['uuid'] = self.uuid
        if self.title is not None:
            result['title'] = self.title
        # Convert enum to its string value
        result['noteType'] = self.note_type.value if isinstance(self.note_type, NoteType) else self.note_type
        if self.data_object_id is not None:
            result['dataObjectId'] = self.data_object_id
        if self.data_attribute_id is not None:
            result['dataAttributeId'] = self.data_attribute_id
        if self.group_uuid is not None:
            result['groupUuid'] = self.group_uuid
        if self.parent_note_id is not None:
            result['parentNoteId'] = self.parent_note_id
        if self.properties is not None:
            result['properties'] = self.properties
        return result


class NoteAccessor:
    """
    Accessor for notes in a document.

    Notes are document-level annotations that can be attached to DataObjects
    and/or DataAttributes. They support different content types (TEXT, MARKDOWN, HTML).

    Access via document.notes property.
    """

    def __init__(self, document: 'Document'):
        self._document = document

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all notes in the document."""
        json_ptr = lib.DocumentGetAllNotes(self._document._handle)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_by_data_object_id(self, data_object_id: int) -> List[Dict[str, Any]]:
        """Get all notes attached to a specific data object."""
        json_ptr = lib.DocumentGetNotesByDataObjectID(self._document._handle, data_object_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_by_data_attribute_id(self, data_attribute_id: int) -> List[Dict[str, Any]]:
        """Get all notes attached to a specific data attribute."""
        json_ptr = lib.DocumentGetNotesByDataAttributeID(self._document._handle, data_attribute_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def create(self, input: NoteInput) -> Optional[Dict[str, Any]]:
        """Create a new note."""
        json_str = json.dumps(input.to_dict()).encode('utf-8')
        new_id = lib.DocumentCreateNote(self._document._handle, json_str)
        check_error()
        if new_id <= 0:
            return None
        # Return the created note by fetching all and finding by ID
        all_notes = self.get_all()
        for note in all_notes:
            if note.get('id') == new_id:
                return note
        return None

    def update(self, note_id: int, input: NoteInput) -> bool:
        """Update an existing note."""
        note_data = input.to_dict()
        note_data['id'] = note_id
        json_str = json.dumps(note_data).encode('utf-8')
        result = lib.DocumentUpdateNote(self._document._handle, json_str)
        check_error()
        return result > 0

    def delete(self, note_id: int) -> bool:
        """Delete a note by ID."""
        result = lib.DocumentDeleteNote(self._document._handle, note_id)
        check_error()
        return result > 0

    def get_by_uuid(self, uuid: str) -> Optional[Dict[str, Any]]:
        """Get a note by its UUID."""
        json_ptr = lib.DocumentGetNoteByUUID(self._document._handle, uuid.encode('utf-8'))
        check_error()
        result = _parse_json_result(json_ptr)
        return result

    def get_by_type(self, note_type: str) -> List[Dict[str, Any]]:
        """Get all notes of a specific type (TEXT, MARKDOWN, HTML)."""
        json_ptr = lib.DocumentGetNotesByType(self._document._handle, note_type.encode('utf-8'))
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_by_group_uuid(self, group_uuid: str) -> List[Dict[str, Any]]:
        """Get all notes in a specific group."""
        json_ptr = lib.DocumentGetNotesByGroupUUID(self._document._handle, group_uuid.encode('utf-8'))
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_root_notes(self) -> List[Dict[str, Any]]:
        """Get all notes without a parent (top-level notes)."""
        json_ptr = lib.DocumentGetRootNotes(self._document._handle)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []

    def get_child_notes(self, parent_note_id: int) -> List[Dict[str, Any]]:
        """Get all child notes of a given parent note."""
        json_ptr = lib.DocumentGetChildNotes(self._document._handle, parent_note_id)
        check_error()
        result = _parse_json_result(json_ptr)
        return result if result else []
