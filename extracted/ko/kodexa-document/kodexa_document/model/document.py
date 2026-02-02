"""
Minimal Document class - thin wrapper around Go C bindings.
All state management happens in Go, this is just a pass-through layer.
"""

import json
import logging
import weakref
from typing import Optional, Dict, Any, List, Union
from pathlib import Path

logger = logging.getLogger(__name__)

from .._native import lib, ffi
from ..errors import check_error, DocumentError
from .document_metadata import DocumentMetadata
from .source_metadata import SourceMetadata
from ..accessors import DataAttributeAccessor, DataObjectAccessor, AuditAccessor, NativeDocumentAccessor, NoteAccessor


class Document:
    """
    Thin wrapper around Go Document - all state lives in Go.
    No UUID generation, no state management, just pass-through to C functions.
    """
    
    def __init__(self, metadata: Optional[Dict[str, Any]] = None, 
                 content_node: Optional[Any] = None,
                 source: Optional[Dict[str, Any]] = None,
                 inmemory: bool = True,
                 kddb_path: Optional[str] = None,
                 delete_on_close: bool = False,
                 **kwargs):  # Accept and ignore other args for compatibility
        """Create a new document - Go generates UUID and manages all state."""
        self._handle = None
        self._closed = False
        self._metadata_cache = None
        self._source_cache = None
        self._data_attributes_accessor = None
        self._data_objects_accessor = None
        self._audit_accessor = None
        self._native_documents_accessor = None
        self._notes_accessor = None
        
        # If opening existing document
        if kddb_path:
            path_bytes = str(kddb_path).encode('utf-8')
            # Pass detached, inmemory, and delete_on_close parameters to OpenDocument
            # Extract detached from kwargs if provided, default to True
            detached = kwargs.get('detached', True)
            handle = lib.OpenDocument(
                path_bytes, 
                1 if detached else 0,
                1 if inmemory else 0,
                1 if delete_on_close else 0
            )
            check_error()
            if handle == 0:
                raise RuntimeError(f"Failed to open document from {kddb_path}")
            self._handle = handle
        else:
            # Create new document
            input_data = {
                "metadata": metadata or {},
                "inmemory": inmemory,
                "delete_on_close": delete_on_close
            }
            
            # Add source if provided
            if source:
                input_data["source"] = source
            
            # TODO: Handle content_node when ContentNode class is implemented
            if content_node is not None:
                raise NotImplementedError("ContentNode support not yet implemented")
            
            # Call Go to create document
            json_input = json.dumps(input_data).encode('utf-8')
            handle = lib.CreateDocument(json_input)
            check_error()
            
            if handle == 0:
                raise RuntimeError("Failed to create document - got null handle")
            
            self._handle = handle
        
        # Set up finalizer to clean up if not explicitly closed
        self._finalizer = weakref.finalize(self, self._cleanup_handle, handle)
    
    @staticmethod
    def _cleanup_handle(handle):
        """Cleanup function for finalizer - must be static.
        Only called if close() was not explicitly called.
        In this case, we just free the handle without calling CloseDocument."""
        if handle:
            try:
                # Only free the handle - document wasn't properly closed
                # This prevents resource leaks but may not save changes
                lib.FreeHandle(handle)
            except:
                pass  # Ignore errors during cleanup
    
    @property
    def uuid(self) -> str:
        """Get document UUID from Go - no local storage."""
        self._ensure_not_closed()
        uuid_ptr = lib.GetDocumentUUID(self._handle)
        check_error()
        if uuid_ptr == ffi.NULL:
            return None
        try:
            uuid_str = ffi.string(uuid_ptr).decode('utf-8')
            return uuid_str
        finally:
            lib.FreeString(uuid_ptr)
    
    @property
    def version(self) -> str:
        """Get document version from Go - no local storage."""
        self._ensure_not_closed()
        version_ptr = lib.GetDocumentVersion(self._handle)
        check_error()
        if version_ptr == ffi.NULL:
            return None
        try:
            version_str = ffi.string(version_ptr).decode('utf-8')
            return version_str
        finally:
            lib.FreeString(version_ptr)
    
    @property
    def metadata(self) -> DocumentMetadata:
        """Get cached metadata that auto-saves to Go on changes."""
        self._ensure_not_closed()
        
        # If we don't have a cache, create it
        if self._metadata_cache is None:
            # Fetch current metadata from Go
            metadata_ptr = lib.GetDocumentMetadata(self._handle)
            check_error()
            metadata_dict = {}
            if metadata_ptr != ffi.NULL:
                try:
                    metadata_str = ffi.string(metadata_ptr).decode('utf-8')
                    if metadata_str:
                        metadata_dict = json.loads(metadata_str)
                except json.JSONDecodeError:
                    pass
                finally:
                    lib.FreeString(metadata_ptr)
            
            # Create cached DocumentMetadata
            self._metadata_cache = DocumentMetadata(metadata_dict, document=self)
        
        return self._metadata_cache
    
    @metadata.setter
    def metadata(self, value: Union[Dict[str, Any], DocumentMetadata]):
        """Set metadata in Go document. Note: This replaces ALL metadata."""
        self._ensure_not_closed()

        # Clear the cache
        self._metadata_cache = None

        # Convert to dict if needed - use duck typing to support DocumentMetadata
        # from different modules (e.g., kodexa.model vs kdx_document)
        # DocumentMetadata inherits from dict, so isinstance(value, dict) handles it
        if not isinstance(value, dict):
            # Try to convert dict-like objects
            if hasattr(value, 'keys') and callable(getattr(value, 'keys', None)):
                value = dict(value)
            else:
                raise TypeError("Metadata must be a dictionary or dict-like object")
        
        # Clear all existing metadata in Go
        metadata_ptr = lib.GetDocumentMetadata(self._handle)
        check_error()
        current_keys = []
        if metadata_ptr != ffi.NULL:
            try:
                metadata_str = ffi.string(metadata_ptr).decode('utf-8')
                if metadata_str:
                    current_data = json.loads(metadata_str)
                    current_keys = list(current_data.keys())
            except:
                pass
            finally:
                lib.FreeString(metadata_ptr)
        
        for key in current_keys:
            key_bytes = key.encode('utf-8')
            lib.SetDocumentMetadata(self._handle, key_bytes, b'')
            check_error()
        
        # Set the new metadata values
        for key, val in value.items():
            if not isinstance(key, str):
                raise TypeError(f"Metadata keys must be strings, got {type(key).__name__}")
            
            # Convert value to JSON for storage
            val_json = json.dumps(val)
            
            # Call Go function to set the metadata
            key_bytes = key.encode('utf-8')
            val_bytes = val_json.encode('utf-8')
            result = lib.SetDocumentMetadata(self._handle, key_bytes, val_bytes)
            check_error()
            if result == 0:
                raise RuntimeError(f"Failed to set metadata key '{key}'")
    
    @property
    def source(self) -> SourceMetadata:
        """Get cached source metadata that auto-saves to Go on changes."""
        self._ensure_not_closed()
        
        if self._source_cache is None:
            # Fetch current source from Go
            source_ptr = lib.GetDocumentSource(self._handle)
            check_error()
            source_dict = {}
            if source_ptr != ffi.NULL:
                try:
                    source_str = ffi.string(source_ptr).decode('utf-8')
                    if source_str and source_str != '{}':
                        source_dict = json.loads(source_str)
                except json.JSONDecodeError:
                    pass
                finally:
                    lib.FreeString(source_ptr)
            
            # Create cached SourceMetadata
            self._source_cache = SourceMetadata.from_dict(source_dict, document=self)
        
        return self._source_cache
    
    @source.setter
    def source(self, value: Union[Dict[str, Any], SourceMetadata]):
        """Set source metadata."""
        self._ensure_not_closed()
        
        # Clear cache
        self._source_cache = None
        
        # Convert to dict if needed - use duck typing to support SourceMetadata
        # from different modules (e.g., kodexa.model vs kdx_document)
        if hasattr(value, 'original_filename') and not isinstance(value, dict):
            # It's a SourceMetadata-like object - convert to JSON format
            source_dict = {}
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
                attr_value = getattr(value, python_key, None)
                if attr_value is not None:
                    source_dict[json_key] = attr_value
            value = source_dict
        
        # Set via C binding
        source_json = json.dumps(value).encode('utf-8')
        result = lib.SetDocumentSource(self._handle, source_json)
        check_error()
        
        if result == 0:
            raise RuntimeError("Failed to set document source")
    
    @property
    def ref(self) -> Optional[str]:
        """Get the document reference (platform origin)."""
        self._ensure_not_closed()
        ref_ptr = lib.Document_GetRef(self._handle)
        check_error()
        if ref_ptr == ffi.NULL:
            return None
        try:
            return ffi.string(ref_ptr).decode('utf-8')
        finally:
            lib.FreeString(ref_ptr)
    
    @ref.setter
    def ref(self, value: Optional[str]):
        """Set the document reference (platform origin)."""
        self._ensure_not_closed()
        if value is None:
            lib.Document_SetRef(self._handle, ffi.NULL)
        else:
            if not isinstance(value, str):
                raise TypeError("ref must be a string or None")
            lib.Document_SetRef(self._handle, value.encode('utf-8'))
        check_error()
    
    @property
    def delete_on_close(self) -> bool:
        """Get the delete_on_close flag for this document."""
        self._ensure_not_closed()
        result = lib.Document_GetDeleteOnClose(self._handle)
        check_error()
        return bool(result)

    @property
    def data_attributes(self) -> DataAttributeAccessor:
        """
        Access data attributes in this document.
        Usage: document.data_attributes.get_for_data_object(id), document.data_attributes.get_by_id(id), etc.
        """
        self._ensure_not_closed()
        if self._data_attributes_accessor is None:
            self._data_attributes_accessor = DataAttributeAccessor(self)
        return self._data_attributes_accessor

    @property
    def data_objects(self) -> DataObjectAccessor:
        """
        Access data objects in this document.
        Usage: document.data_objects.get_all(), document.data_objects.get_by_uuid(uuid), etc.
        """
        self._ensure_not_closed()
        if self._data_objects_accessor is None:
            self._data_objects_accessor = DataObjectAccessor(self)
        return self._data_objects_accessor

    @property
    def audit(self) -> AuditAccessor:
        """
        Access audit data in this document.
        Usage: document.audit.list_revisions(), document.audit.get_data_object_history(id), etc.
        """
        self._ensure_not_closed()
        if self._audit_accessor is None:
            self._audit_accessor = AuditAccessor(self)
        return self._audit_accessor

    @property
    def native_documents(self) -> NativeDocumentAccessor:
        """
        Access native documents (embedded files) in this document.
        Usage: document.native_documents.get_all(), document.native_documents.get_data(id), etc.
        """
        self._ensure_not_closed()
        if self._native_documents_accessor is None:
            self._native_documents_accessor = NativeDocumentAccessor(self)
        return self._native_documents_accessor

    @property
    def notes(self) -> NoteAccessor:
        """
        Access notes in this document.
        Usage: document.notes.get_all(), document.notes.create(NoteInput(...)), etc.
        """
        self._ensure_not_closed()
        if self._notes_accessor is None:
            self._notes_accessor = NoteAccessor(self)
        return self._notes_accessor

    def get_uuid(self) -> str:
        """Alias for uuid property."""
        return self.uuid
    
    def get_version(self) -> str:
        """Alias for version property."""
        return self.version
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get document statistics including node counts, types, and other metrics.

        Returns:
            Dict containing statistics like total_nodes, node_type_count, total_tags, etc.
        """
        self._ensure_not_closed()
        stats_ptr = lib.GetDocumentStatistics(self._handle)
        check_error()
        if stats_ptr == ffi.NULL:
            return {}
        try:
            stats_str = ffi.string(stats_ptr).decode('utf-8')
            if not stats_str:
                return {}
            stats = json.loads(stats_str)
            # Convert camelCase keys from Go to snake_case for Python
            return self._convert_dict_keys_to_snake(stats)
        finally:
            lib.FreeString(stats_ptr)
    
    def get_validations(self) -> List[Dict[str, Any]]:
        """
        Get document-level taxon validations.

        Returns:
            List of DocumentTaxonValidation objects as dictionaries with snake_case keys.
        """
        self._ensure_not_closed()
        validations_ptr = lib.GetValidations(self._handle)
        check_error()
        if validations_ptr == ffi.NULL:
            return []
        try:
            validations_str = ffi.string(validations_ptr).decode('utf-8')
            if not validations_str:
                return []
            validations = json.loads(validations_str)
            # Convert camelCase keys from Go to snake_case for Python
            return [self._convert_dict_keys_to_snake(v) for v in validations]
        finally:
            lib.FreeString(validations_ptr)

    def set_validations(self, validations: List[Dict[str, Any]]):
        """
        Set document-level taxon validations.

        Args:
            validations: List of DocumentTaxonValidation objects as dictionaries.
                Each validation should have: taxonomy_ref, taxon_path, and validation fields.
        """
        self._ensure_not_closed()

        if not isinstance(validations, list):
            raise TypeError("validations must be a list")

        # Convert snake_case keys to camelCase for Go backend
        go_validations = [self._convert_dict_keys_to_camel(v) for v in validations]

        # Convert to JSON for C binding
        validations_json = json.dumps(go_validations).encode('utf-8')
        result = lib.SetDocumentValidationsList(self._handle, validations_json)
        check_error()

        if result != 1:
            raise RuntimeError("Failed to set document validations")
    
    def get_steps(self):
        """
        Get document processing steps.
        
        Returns:
            List of ProcessingStep objects representing the processing history.
            For backward compatibility, if a string is stored, returns the string.
        """
        from ..processing import ProcessingStep
        
        self._ensure_not_closed()
        steps_ptr = lib.GetDocumentProcessingSteps(self._handle)
        check_error()
        if steps_ptr == ffi.NULL:
            return []
        try:
            steps_str = ffi.string(steps_ptr).decode('utf-8')
            if not steps_str:
                return []
            
            # Try to parse as JSON array
            try:
                import json
                steps_data = json.loads(steps_str)
                if isinstance(steps_data, list):
                    # Create a cache for reconstructing relationships
                    step_cache = {}
                    steps = []
                    
                    # First pass: Create all steps
                    for step_dict in steps_data:
                        step = ProcessingStep.from_dict(step_dict, step_cache)
                        steps.append(step)
                    
                    # Second pass: Reconstruct full relationships if needed
                    # The from_dict method handles most relationships already
                    return steps
                else:
                    # If it's not a list, return as is for backward compatibility
                    return steps_str
            except (json.JSONDecodeError, ValueError):
                # If it's not valid JSON, return the string for backward compatibility
                return steps_str
        finally:
            lib.FreeString(steps_ptr)

    def _fix_step_ids(self, step_dict: dict, uuid_module) -> dict:
        """Recursively fix id/uuid fields in step dicts for Go compatibility.

        Python ProcessingStep uses 'id' as a string UUID.
        Go ProcessingStep uses 'id' as int64 (auto-generated) and 'uuid' as string.
        """
        def fix_step(s):
            if not isinstance(s, dict):
                return s
            # Convert id to uuid
            if 'uuid' not in s and 'id' in s:
                s['uuid'] = s.pop('id')
            elif 'id' in s and isinstance(s['id'], str):
                del s['id']
            if 'uuid' not in s:
                s['uuid'] = str(uuid_module.uuid4())
            return s

        # Fix nested step lists: children, parents, internalSteps
        for key in ['children', 'parents', 'internalSteps']:
            if key in step_dict and step_dict[key]:
                fixed_list = []
                for item in step_dict[key]:
                    if isinstance(item, dict):
                        item = fix_step(item)
                        item = self._fix_step_ids(item, uuid_module)
                    fixed_list.append(item)
                step_dict[key] = fixed_list

        return step_dict

    def set_steps(self, steps):
        """
        Set document processing steps.

        Args:
            steps: Either a list of ProcessingStep objects/dicts, or None to clear.
        """
        from ..processing import ProcessingStep

        self._ensure_not_closed()

        if steps is None:
            # Pass empty array to clear the steps
            result = lib.SetDocumentProcessingSteps(self._handle, b'[]')
        elif isinstance(steps, str):
            # Support JSON string input for backward compatibility
            import uuid as uuid_module
            steps_data = json.loads(steps)
            if not isinstance(steps_data, list):
                raise TypeError("JSON string must contain a list of steps")
            # Ensure each step has a uuid
            for step_dict in steps_data:
                if isinstance(step_dict, dict) and 'uuid' not in step_dict:
                    step_dict['uuid'] = step_dict.pop('id', None) or str(uuid_module.uuid4())
            steps_bytes = json.dumps(steps_data).encode('utf-8')
            result = lib.SetDocumentProcessingSteps(self._handle, steps_bytes)
        elif isinstance(steps, list):
            # Convert list of ProcessingStep objects to JSON array
            import uuid as uuid_module
            steps_list = []
            for step in steps:
                if isinstance(step, ProcessingStep):
                    steps_list.append(step.to_dict())
                elif isinstance(step, dict):
                    # Ensure dict has a uuid field for Go's UNIQUE constraint
                    step_copy = step.copy()
                    if 'uuid' not in step_copy:
                        # Support legacy 'id' field, or generate new uuid
                        step_copy['uuid'] = step_copy.pop('id', None) or str(uuid_module.uuid4())
                    steps_list.append(step_copy)
                elif hasattr(step, 'model_dump'):
                    # Handle Pydantic models (e.g., kodexa.model.model.ProcessingStep)
                    step_dict = step.model_dump(by_alias=True, exclude_none=True)
                    # Python uses 'id' as string UUID, Go uses 'uuid' for string and 'id' for int64 DB ID
                    # Convert 'id' to 'uuid' and remove 'id' to let Go auto-generate it
                    if 'uuid' not in step_dict and 'id' in step_dict:
                        step_dict['uuid'] = step_dict.pop('id')
                    elif 'id' in step_dict:
                        # Remove string id since Go expects int64
                        del step_dict['id']
                    if 'uuid' not in step_dict:
                        step_dict['uuid'] = str(uuid_module.uuid4())
                    # Recursively fix children if present
                    step_dict = self._fix_step_ids(step_dict, uuid_module)
                    steps_list.append(step_dict)
                elif hasattr(step, 'to_dict'):
                    # Handle other objects with to_dict method
                    step_dict = step.to_dict()
                    if 'uuid' not in step_dict:
                        step_dict['uuid'] = step_dict.pop('id', None) or str(uuid_module.uuid4())
                    steps_list.append(step_dict)
                else:
                    raise TypeError(f"Invalid step type: {type(step)}")
            steps_json = json.dumps(steps_list)
            steps_bytes = steps_json.encode('utf-8')
            result = lib.SetDocumentProcessingSteps(self._handle, steps_bytes)
        else:
            raise TypeError("steps must be a list of ProcessingStep objects/dicts, a JSON string, or None")
        
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to set document processing steps")
    
    @property
    def labels(self) -> List[str]:
        """
        Get document labels as a list of strings (legacy_python parity).

        Returns:
            List of label strings.
        """
        self._ensure_not_closed()
        labels_ptr = lib.GetDocumentLabels(self._handle)
        check_error()
        if labels_ptr == ffi.NULL:
            return []
        try:
            labels_str = ffi.string(labels_ptr).decode('utf-8')
            return json.loads(labels_str) if labels_str else []
        finally:
            lib.FreeString(labels_ptr)

    @labels.setter
    def labels(self, value: List[str]):
        """
        Set document labels, replacing any existing labels (legacy_python parity).

        Args:
            value: List of label strings to set.
        """
        self._ensure_not_closed()
        if not isinstance(value, (list, tuple)):
            raise TypeError("labels must be a list or tuple of strings")

        # Clear existing labels
        for label in self.labels:
            self.remove_label(label)

        # Add new labels
        for label in value:
            self.add_label(label)

    def add_label(self, label: str):
        """
        Add a label to the document (legacy_python parity).
        
        Args:
            label: String label to add. Duplicates are ignored.
            
        Returns:
            The document (for method chaining).
        """
        self._ensure_not_closed()
        if not isinstance(label, str):
            raise TypeError("label must be a string")
        
        label_bytes = label.encode('utf-8')
        result = lib.AddDocumentLabel(self._handle, label_bytes)
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to add document label")
        
        return self  # For method chaining like legacy_python
    
    def remove_label(self, label: str):
        """
        Remove a label from the document (legacy_python parity).
        
        Args:
            label: String label to remove.
            
        Returns:
            The document (for method chaining).
            
        Raises:
            ValueError: If the label is not found (matches legacy_python).
        """
        self._ensure_not_closed()
        if not isinstance(label, str):
            raise TypeError("label must be a string")
        
        label_bytes = label.encode('utf-8')
        result = lib.RemoveDocumentLabel(self._handle, label_bytes)
        
        # Check for Go error and convert to ValueError for legacy_python compatibility
        try:
            check_error()
        except Exception as e:
            # Convert Go error to ValueError to match legacy_python behavior
            raise ValueError(f"label not found: {label}") from e
        
        if result != 1:
            # This matches the legacy_python behavior of raising ValueError
            raise ValueError(f"label not found: {label}")
        
        return self  # For method chaining like legacy_python
    
    def get_labels(self) -> List[str]:
        """
        Get document labels as a list of strings (legacy_python parity).
        
        Returns:
            List of label strings.
        """
        return self.labels  # Use the property
    
    def get_mixins(self) -> List[str]:
        """
        Get document mixins as a list of strings (legacy_python parity).
        
        Returns:
            List of mixin strings.
        """
        self._ensure_not_closed()
        mixins_ptr = lib.GetDocumentMixins(self._handle)
        check_error()
        if mixins_ptr == ffi.NULL:
            return []
        try:
            mixins_str = ffi.string(mixins_ptr).decode('utf-8')
            return json.loads(mixins_str) if mixins_str else []
        finally:
            lib.FreeString(mixins_ptr)
    
    def add_mixin(self, mixin: str):
        """
        Add a mixin to the document (legacy_python parity).

        Args:
            mixin: String mixin to add. Duplicates are ignored.

        Returns:
            The document (for method chaining).
        """
        self._ensure_not_closed()
        if not isinstance(mixin, str):
            raise TypeError("mixin must be a string")

        mixin_bytes = mixin.encode('utf-8')
        result = lib.AddDocumentMixin(self._handle, mixin_bytes)
        check_error()

        if result != 1:
            raise RuntimeError("Failed to add document mixin")

        return self  # For method chaining like legacy_python

    def get_document_knowledge_features(self) -> List[Any]:
        """
        Get all document knowledge features.

        Returns:
            List of DocumentKnowledgeFeature objects with knowledge_feature_ref and properties.
        """
        from .objects import DocumentKnowledgeFeature

        self._ensure_not_closed()
        features_ptr = lib.GetDocumentKnowledgeFeatures(self._handle)
        check_error()
        if features_ptr == ffi.NULL:
            return []
        try:
            features_str = ffi.string(features_ptr).decode('utf-8')
            if not features_str:
                return []
            features_data = json.loads(features_str)
            # Convert dicts to DocumentKnowledgeFeature objects
            result = []
            for f in features_data:
                result.append(DocumentKnowledgeFeature(**f))
            return result
        finally:
            lib.FreeString(features_ptr)

    def set_document_knowledge_features(self, features: List[Any]):
        """
        Set document knowledge features.

        Args:
            features: List of DocumentKnowledgeFeature objects or dicts with
                      knowledgeFeatureRef and properties (camelCase keys).
        """
        self._ensure_not_closed()

        if not isinstance(features, list):
            raise TypeError("features must be a list")

        # Convert to list of dicts for Go backend
        go_features = []
        for feature in features:
            if hasattr(feature, 'model_dump'):
                # Pydantic v2 model - use aliases for camelCase
                feature_dict = feature.model_dump(by_alias=True)
            elif hasattr(feature, 'dict'):
                # Pydantic v1 model - use aliases for camelCase
                feature_dict = feature.dict(by_alias=True)
            elif isinstance(feature, dict):
                # Pass through as-is (expect camelCase keys)
                feature_dict = feature
            else:
                raise TypeError(f"Invalid feature type: {type(feature)}")
            go_features.append(feature_dict)

        features_json = json.dumps(go_features).encode('utf-8')
        result = lib.SetDocumentKnowledgeFeatures(self._handle, features_json)
        check_error()

        if result != 1:
            raise RuntimeError("Failed to set document knowledge features")

    def get_knowledge(self) -> List["KnowledgeItem"]:
        """
        Get all knowledge items.

        Returns:
            List of KnowledgeItem objects.
        """
        from .objects import KnowledgeItem

        self._ensure_not_closed()
        items_ptr = lib.GetKnowledge(self._handle)
        check_error()
        if items_ptr == ffi.NULL:
            return []
        try:
            items_str = ffi.string(items_ptr).decode('utf-8')
            if not items_str:
                return []
            items_data = json.loads(items_str)
            return [KnowledgeItem.model_validate(item) for item in items_data]
        finally:
            lib.FreeString(items_ptr)

    def set_knowledge(self, items: List[Any]):
        """
        Set knowledge items.

        Args:
            items: List of KnowledgeItem objects or dicts.
        """
        self._ensure_not_closed()

        if not isinstance(items, list):
            raise TypeError("items must be a list")

        # Convert to list of dicts for Go backend
        go_items = []
        for item in items:
            if hasattr(item, 'model_dump'):
                # Pydantic v2 model - use aliases for camelCase
                item_dict = item.model_dump(by_alias=True)
            elif hasattr(item, 'dict'):
                # Pydantic v1 model - use aliases for camelCase
                item_dict = item.dict(by_alias=True)
            elif isinstance(item, dict):
                # Pass through as-is
                item_dict = item
            else:
                raise TypeError(f"Invalid item type: {type(item)}")
            go_items.append(item_dict)

        items_json = json.dumps(go_items).encode('utf-8')
        result = lib.SetKnowledge(self._handle, items_json)
        check_error()

        if result != 1:
            raise RuntimeError("Failed to set knowledge items")

    @staticmethod
    def _camel_to_snake(name: str) -> str:
        """Convert camelCase to snake_case."""
        import re
        # Insert underscore before uppercase letters and convert to lowercase
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def _snake_to_camel(name: str) -> str:
        """Convert snake_case to camelCase."""
        components = name.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def _convert_dict_keys_to_snake(d: Dict[str, Any]) -> Dict[str, Any]:
        """Convert all dictionary keys from camelCase to snake_case."""
        return {Document._camel_to_snake(k): v for k, v in d.items()}

    @staticmethod
    def _convert_dict_keys_to_camel(d: Dict[str, Any]) -> Dict[str, Any]:
        """Convert all dictionary keys from snake_case to camelCase."""
        return {Document._snake_to_camel(k): v for k, v in d.items()}

    def get_exceptions(self) -> List[Dict[str, Any]]:
        """
        Get document exceptions as a list of dictionaries (legacy_python parity).

        Returns:
            List of exception dictionaries with snake_case keys.
        """
        self._ensure_not_closed()
        exceptions_ptr = lib.GetDocumentExceptions(self._handle)
        check_error()
        if exceptions_ptr == ffi.NULL:
            return []
        try:
            exceptions_str = ffi.string(exceptions_ptr).decode('utf-8')
            if not exceptions_str:
                return []
            exceptions = json.loads(exceptions_str)
            # Convert camelCase keys from Go to snake_case for Python
            return [self._convert_dict_keys_to_snake(exc) for exc in exceptions]
        finally:
            lib.FreeString(exceptions_ptr)
    
    def add_exception(self, exception: Union[Dict[str, Any], 'ContentException']):
        """
        Add an exception to the document (legacy_python parity).

        Args:
            exception: Exception dictionary or ContentException-like object with
                      message, exception_type, and optional severity, node_uuid, etc.

        Returns:
            The document (for method chaining).
        """
        self._ensure_not_closed()

        # Convert to dict if it's an object with attributes
        if hasattr(exception, 'message') and hasattr(exception, 'exception_type'):
            exception_dict = {
                'message': exception.message,
                'exception_type': exception.exception_type,
                'severity': getattr(exception, 'severity', 'ERROR'),
                'node_uuid': getattr(exception, 'node_uuid', ''),
                'exception_details': getattr(exception, 'exception_details', ''),
                'path': getattr(exception, 'path', ''),
                'closing_comment': getattr(exception, 'closing_comment', ''),
                'open': getattr(exception, 'open', True),
                'exception_type_id': getattr(exception, 'exception_type_id', ''),
                'tag': getattr(exception, 'tag', None),
                'group_uuid': getattr(exception, 'group_uuid', None),
                'tag_uuid': getattr(exception, 'tag_uuid', None),
            }
        elif isinstance(exception, dict):
            exception_dict = exception.copy()
        else:
            raise TypeError("exception must be a dictionary or ContentException-like object")

        # Ensure required fields (check both snake_case and camelCase)
        message = exception_dict.get('message') or exception_dict.get('message', '')
        exc_type = exception_dict.get('exception_type') or exception_dict.get('exceptionType', '')
        if not message:
            raise ValueError("exception must have a non-empty message")
        if not exc_type:
            raise ValueError("exception must have a non-empty exception_type")

        # Set defaults
        exception_dict.setdefault('severity', 'ERROR')
        exception_dict.setdefault('open', True)

        # Convert snake_case keys to camelCase for Go backend
        go_exception = self._convert_dict_keys_to_camel(exception_dict)

        exception_json = json.dumps(go_exception)
        exception_bytes = exception_json.encode('utf-8')
        result = lib.AddDocumentException(self._handle, exception_bytes)
        check_error()

        if result != 1:
            raise RuntimeError("Failed to add document exception")

        return self  # For method chaining like legacy_python

    def get_open_exceptions(self) -> List[Dict[str, Any]]:
        """
        Get only open (unresolved) document exceptions.

        Returns:
            List of open exception dictionaries with snake_case keys.
        """
        self._ensure_not_closed()
        exceptions_ptr = lib.GetOpenExceptions(self._handle)
        check_error()
        if exceptions_ptr == ffi.NULL:
            return []
        try:
            exceptions_str = ffi.string(exceptions_ptr).decode('utf-8')
            if not exceptions_str:
                return []
            exceptions = json.loads(exceptions_str)
            # Convert camelCase keys from Go to snake_case for Python
            return [self._convert_dict_keys_to_snake(exc) for exc in exceptions]
        finally:
            lib.FreeString(exceptions_ptr)

    def close_exception(self, exception_id: int, closing_comment: str = "") -> 'Document':
        """
        Close (resolve) an exception by its ID.

        Args:
            exception_id: The ID of the exception to close.
            closing_comment: Optional comment explaining the resolution.

        Returns:
            The document (for method chaining).
        """
        self._ensure_not_closed()
        comment_bytes = closing_comment.encode('utf-8') if closing_comment else ffi.NULL
        result = lib.CloseException(self._handle, exception_id, comment_bytes)
        check_error()

        if result != 1:
            raise RuntimeError(f"Failed to close exception {exception_id}")

        return self  # For method chaining

    def get_lines(self) -> List[Dict[str, Any]]:
        """
        Get all line nodes in the document.

        Returns:
            List of line node dictionaries with id, level, typeId, nodeType, and content.
        """
        self._ensure_not_closed()
        lines_ptr = lib.GetDocumentLines(self._handle)
        check_error()
        if lines_ptr == ffi.NULL:
            return []
        try:
            lines_str = ffi.string(lines_ptr).decode('utf-8')
            return json.loads(lines_str) if lines_str else []
        finally:
            lib.FreeString(lines_ptr)

    def get_pretty_page(self, page_index: int) -> str:
        """
        Get a spatially-formatted text representation of a single page.

        The output preserves the visual layout of words based on their bounding boxes.

        Args:
            page_index: Zero-based index of the page to format.

        Returns:
            Pretty-printed text representation of the page.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetPrettyPage(self._handle, page_index)
        check_error()
        if result_ptr == ffi.NULL:
            return ""
        try:
            return ffi.string(result_ptr).decode('utf-8')
        finally:
            lib.FreeString(result_ptr)

    def get_pretty_pages(self) -> str:
        """
        Get a spatially-formatted text representation of all pages.

        Each page is separated by a header line. The output preserves the visual
        layout of words based on their bounding boxes.

        Returns:
            Pretty-printed text representation of all pages.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetPrettyPages(self._handle)
        check_error()
        if result_ptr == ffi.NULL:
            return ""
        try:
            return ffi.string(result_ptr).decode('utf-8')
        finally:
            lib.FreeString(result_ptr)

    def get_external_data(self, key: str = "default") -> Dict[str, Any]:
        """
        Get external data for a specific key.

        Args:
            key: The key to retrieve data for, defaults to "default"

        Returns:
            Dict containing the external data for the given key
        """
        self._ensure_not_closed()
        if key is None:
            key = ""
        key_bytes = key.encode('utf-8')
        data_ptr = lib.GetExternalData(self._handle, key_bytes)
        check_error()
        if data_ptr == ffi.NULL:
            return {}
        try:
            data_str = ffi.string(data_ptr).decode('utf-8')
            return json.loads(data_str) if data_str else {}
        except json.JSONDecodeError:
            return {}
        finally:
            lib.FreeString(data_ptr)
    
    def set_external_data(self, external_data: Dict[str, Any], key: str = "default"):
        """
        Set external data for a specific key.

        Args:
            external_data: Dictionary containing the data to store
            key: The key to store the data under, defaults to "default"
        """
        self._ensure_not_closed()
        if not isinstance(external_data, dict):
            raise TypeError("external_data must be a dictionary")

        if key is None:
            key = ""
        key_bytes = key.encode('utf-8')
        data_json = json.dumps(external_data).encode('utf-8')
        result = lib.SetExternalData(self._handle, key_bytes, data_json)
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to set external data")
    
    def get_external_data_keys(self) -> List[str]:
        """
        Get all keys that have external data stored.
        
        Returns:
            List of all external data keys
        """
        self._ensure_not_closed()
        keys_ptr = lib.GetExternalDataKeys(self._handle)
        check_error()
        if keys_ptr == ffi.NULL:
            return []
        try:
            keys_str = ffi.string(keys_ptr).decode('utf-8')
            return json.loads(keys_str) if keys_str else []
        except json.JSONDecodeError:
            return []
        finally:
            lib.FreeString(keys_ptr)

    def get_all_data_exceptions(self) -> List['DataException']:
        """
        Get all DataExceptions from all DataObjects in this document.

        This method retrieves all DataExceptions from the document's DataObjects
        and their DataAttributes, recursively traversing the entire hierarchy.

        Returns:
            List of DataException objects from all DataObjects and DataAttributes.
        """
        from ..extraction import DataException

        self._ensure_not_closed()
        exceptions_ptr = lib.GetAllDataExceptions(self._handle)
        check_error()
        if exceptions_ptr == ffi.NULL:
            return []
        try:
            exceptions_str = ffi.string(exceptions_ptr).decode('utf-8')
            if not exceptions_str:
                return []
            exceptions_data = json.loads(exceptions_str)
            return [DataException(exc_data) for exc_data in exceptions_data]
        finally:
            lib.FreeString(exceptions_ptr)

    def to_json(self, **kwargs) -> str:
        """Get JSON representation from Go."""
        self._ensure_not_closed()
        json_ptr = lib.GetDocumentJSON(self._handle)
        check_error()
        if json_ptr == ffi.NULL:
            raise RuntimeError("Failed to get document JSON")
        try:
            json_str = ffi.string(json_ptr).decode('utf-8')
            
            # Apply any JSON formatting options
            if kwargs:
                data = json.loads(json_str)
                return json.dumps(data, **kwargs)
            return json_str
        finally:
            lib.FreeString(json_ptr)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary representation (legacy_python parity).
        
        Returns:
            dict: Dictionary representation of the document
        """
        # We don't want to store the none values (matches legacy_python)
        def clean_none_values(d):
            """
            This function recursively cleans a dictionary by removing keys with None values.
            """
            clean = {}
            for k, v in d.items():
                if isinstance(v, dict):
                    nested = clean_none_values(v)
                    if len(nested.keys()) > 0:
                        clean[k] = nested
                elif v is not None:
                    clean[k] = v
            return clean
        
        # Load full JSON from Go to get all the data
        json_str = self.to_json()
        go_data = json.loads(json_str)
        
        # Build the dictionary exactly like legacy_python does
        result = {
            "version": self.version,  # Get version dynamically from this document
            "metadata": go_data.get("metadata", {}),
            "content_node": go_data.get("content_node") if go_data.get("content_node") else None,  # Match legacy: None if no content_node
            "uuid": self.uuid,
        }
        
        # Handle source with clean_none_values like legacy
        if "source" in go_data and go_data["source"]:
            result["source"] = clean_none_values(go_data["source"])
        
        # Handle mixins - get from Go data or our method
        if "mixins" in go_data:
            result["mixins"] = go_data["mixins"]
        else:
            # Fallback to our method if not in JSON
            result["mixins"] = self.get_mixins()
        
        # Handle labels - get from Go data or our method
        if "labels" in go_data:
            result["labels"] = go_data["labels"]
        else:
            # Fallback to our method if not in JSON
            result["labels"] = self.labels
        
        return result
    
    def save(self, path: str):
        """Save document to file via Go."""
        self._ensure_not_closed()
        path_bytes = str(path).encode('utf-8')
        result = lib.SaveDocument(self._handle, path_bytes)
        check_error()
        if result != 0:
            raise RuntimeError(f"Failed to save document to {path}")
    
    def to_kddb(self, path: Optional[str] = None):
        """
        Save document to KDDB file or return bytes.
        
        Args:
            path: Optional path to save to. If None, returns bytes.
            
        Returns:
            bytes if path is None, otherwise None
        """
        self._ensure_not_closed()
        
        if path is None:
            # Get document as bytes
            size_ptr = ffi.new("int*")
            bytes_ptr = lib.GetDocumentBytes(self._handle, size_ptr)
            check_error()
            
            if bytes_ptr == ffi.NULL:
                raise RuntimeError("Failed to get document bytes")
            
            try:
                # Copy bytes from C memory to Python bytes
                size = size_ptr[0]
                result = ffi.buffer(bytes_ptr, size)[:]
                return result
            finally:
                # Free the allocated C memory
                lib.FreeBytes(bytes_ptr)
        else:
            # Save to file
            self.save(path)
    
    # Metadata operations
    def get_metadata(self, key: str = None):
        """
        Get metadata value(s).
        
        Args:
            key: Optional specific key to get. If None, returns all metadata.
            
        Returns:
            All metadata dict if key is None, otherwise the specific value or None
        """
        if key is None:
            return self.metadata
        else:
            return self.metadata.get(key)
    
    def set_metadata(self, key: str, value: Any):
        """
        Set a metadata key-value pair.
        
        Args:
            key: Metadata key
            value: Metadata value (will be JSON serialized)
        """
        self._ensure_not_closed()
        
        key_bytes = key.encode('utf-8')
        # Convert value to JSON string
        value_json = json.dumps(value).encode('utf-8')
        
        result = lib.SetDocumentMetadata(self._handle, key_bytes, value_json)
        check_error()
        
        if result == 0:
            raise RuntimeError(f"Failed to set metadata key '{key}'")
    
    # ContentNode operations
    def create_node(self, node_type: str, content: str = "", virtual: bool = False, parent: Optional[Any] = None, index: Optional[int] = None):
        """
        Create a new content node.
        
        Args:
            node_type: Type of node (e.g., 'paragraph', 'line', 'word')
            content: Text content of the node  
            virtual: Whether node is virtual (default: False)
            parent: Parent ContentNode (default: None)
            index: Optional index for ordering (default: None)
            
        Returns:
            ContentNode: The created node
        """
        self._ensure_not_closed()
        
        from .content_node import ContentNode
        
        # If enhanced parameters are provided, use DocumentCreateNodeWithOptions
        if virtual or parent is not None or index is not None:
            node_type_bytes = node_type.encode('utf-8')
            content_bytes = content.encode('utf-8') if content else b""
            
            virtual_int = 1 if virtual else 0
            parent_handle = parent._handle if parent is not None else 0
            index_int = index if index is not None else -1
            
            handle = lib.DocumentCreateNodeWithOptions(
                self._handle, 
                node_type_bytes, 
                content_bytes, 
                virtual_int,
                parent_handle,
                index_int
            )
            check_error()
            
            if handle == 0:
                raise RuntimeError("Failed to create content node with options")
            
            return ContentNode(handle=handle, document=self)
        else:
            # Use simple DocumentCreateNode for basic case
            node_type_bytes = node_type.encode('utf-8')
            content_bytes = content.encode('utf-8') if content else b""
            
            handle = lib.DocumentCreateNode(self._handle, node_type_bytes, content_bytes)
            check_error()
            
            if handle == 0:
                raise RuntimeError("Failed to create content node")
            
            return ContentNode(handle=handle, document=self)
    
    @property
    def content_node(self):
        """
        Get the root content node.
        
        Returns:
            ContentNode or None: The root content node, or None if not set
        """
        self._ensure_not_closed()
        
        handle = lib.GetDocumentContentNode(self._handle)
        check_error()
        
        if handle == 0:
            return None
        
        from .content_node import ContentNode
        return ContentNode(handle=handle, document=self)
    
    @content_node.setter
    def content_node(self, node):
        """
        Set the root content node.
        
        Args:
            node: ContentNode to set as root, or None to clear
        """
        self._ensure_not_closed()
        
        if node is None:
            success = lib.SetDocumentContentNode(self._handle, 0)
        else:
            if not hasattr(node, '_handle'):
                raise ValueError("Invalid ContentNode object")
            success = lib.SetDocumentContentNode(self._handle, node._handle)
        
        check_error()
        if not success:
            raise RuntimeError("Failed to set content node")
    
    def get_root(self):
        """Get the root content node (alias for content_node property)."""
        return self.content_node
    
    def set_root(self, node):
        """Set the root content node (alias for content_node setter)."""
        self.content_node = node

    def preload_for_labelling(self) -> None:
        """
        Preload all entities into memory for fast access during labelling.

        Call this before labelling operations to avoid per-call database queries.
        After calling this, get_node_by_uuid, get_children, get_tags, get_features,
        get_bbox all return cached data with O(1) lookup time.
        """
        self._ensure_not_closed()
        result = lib.PreloadForLabelling(self._handle)
        if result != 0:
            error_msg = _get_last_error()
            raise RuntimeError(f"Failed to preload for labelling: {error_msg}")

    def clear_labelling_cache(self) -> None:
        """
        Clear all labelling caches to release memory.

        Call this after labelling operations are complete to free up memory
        used by the preloaded caches.
        """
        self._ensure_not_closed()
        result = lib.ClearLabellingCache(self._handle)
        if result != 0:
            check_error()
            raise RuntimeError("Failed to clear labelling cache")

    def cache_document(self) -> None:
        """
        Preload all content nodes and their relationships into the cache.

        This uses bulk queries to efficiently load the entire document tree
        in just 2 database queries. Call this before performing many read
        operations (like update_document_lines) to maximize cache hits and
        improve performance.

        Example:
            doc.cache_document()  # Preload everything
            update_document_lines(doc)  # Now much faster
        """
        self._ensure_not_closed()
        result = lib.CacheDocument(self._handle)
        if result != 0:
            check_error()
            raise RuntimeError("Failed to cache document")

    # ========== Transaction Support ==========

    def begin_transaction(self) -> None:
        """
        Begin a database transaction.

        All subsequent operations will be part of this transaction until
        commit_transaction() or rollback_transaction() is called.

        Use this to batch multiple database operations for better performance.
        """
        self._ensure_not_closed()
        result = lib.BeginTransaction(self._handle)
        check_error()
        if result == 0:
            raise RuntimeError("Failed to begin transaction")

    def commit_transaction(self) -> None:
        """
        Commit the current database transaction.

        All operations since begin_transaction() will be persisted atomically.
        """
        self._ensure_not_closed()
        result = lib.CommitTransaction(self._handle)
        check_error()
        if result == 0:
            raise RuntimeError("Failed to commit transaction")

    def rollback_transaction(self) -> None:
        """
        Rollback the current database transaction.

        All operations since begin_transaction() will be discarded.
        """
        self._ensure_not_closed()
        result = lib.RollbackTransaction(self._handle)
        check_error()
        if result == 0:
            raise RuntimeError("Failed to rollback transaction")

    def transaction(self):
        """
        Context manager for database transactions.

        Usage:
            with document.transaction():
                # All operations here are batched in a single transaction
                node.reparent(new_parent, 0)
                parent.remove_child(old_node)
                # ... more operations

        If an exception occurs, the transaction is rolled back.
        Otherwise, it is committed when the context exits.
        """
        return _TransactionContextManager(self)

    def close(self):
        """Close document and free resources."""
        if not self._closed and self._handle:
            # CloseDocument in Go handles both closing the document AND
            # removing from handle registry (see main.go line 208)
            result = lib.CloseDocument(self._handle)
            # Don't check error on close - resource cleanup should complete
            # DO NOT call FreeHandle here - CloseDocument already does it!
            self._handle = None
            self._closed = True
            if hasattr(self, '_finalizer'):
                self._finalizer.detach()
    
    def _ensure_not_closed(self):
        """Check that document is not closed."""
        if self._closed or not self._handle:
            raise RuntimeError("Document has been closed")
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup."""
        self.close()
    
    def __del__(self):
        """Cleanup on deletion - finalizer handles this."""
        pass
    
    def __repr__(self):
        """String representation."""
        status = "closed" if self._closed else "open"
        try:
            uuid = self.uuid if not self._closed else "N/A"
            version = self.version if not self._closed else "N/A"
        except:
            uuid = "N/A"
            version = "N/A"
        return f"Document(uuid='{uuid}', version='{version}', status='{status}')"
    
    # Factory methods
    @classmethod
    def from_text(cls, text: str, separator: Optional[str] = None, inmemory: bool = False, **kwargs):
        """Create document from text via Go."""
        text_bytes = text.encode('utf-8')
        separator_bytes = separator.encode('utf-8') if separator else ffi.NULL
        
        # Pass inmemory parameter to CreateDocumentFromText (1 for True, 0 for False)
        handle = lib.CreateDocumentFromText(text_bytes, separator_bytes, 1 if inmemory else 0)
        check_error()
        
        if handle == 0:
            raise RuntimeError("Failed to create document from text")

        # Create wrapper instance without going through __init__
        doc = cls.__new__(cls)
        doc._handle = handle
        doc._closed = False
        doc._metadata_cache = None
        doc._source_cache = None
        doc._data_attributes_accessor = None
        doc._data_objects_accessor = None
        doc._audit_accessor = None
        doc._native_documents_accessor = None
        doc._notes_accessor = None
        doc._finalizer = weakref.finalize(doc, cls._cleanup_handle, handle)
        return doc

    @classmethod
    def from_kddb(cls, source, detached: bool = True, inmemory: bool = False, delete_on_close: bool = False):
        """
        Open existing KDDB file or load from bytes via Go.
        
        Args:
            source: Either a string path to KDDB file or bytes containing KDDB data
            detached: If True, creates a copy to work on (only for file paths)
            inmemory: If True, loads database entirely into memory
            delete_on_close: If True, deletes the file when document is closed
                            (Note: when detached=True, the temp copy is always deleted)
            
        Returns:
            Document instance
        """
        if isinstance(source, str):
            # String path - use OpenDocument with detached parameter
            path_bytes = source.encode('utf-8')
            handle = lib.OpenDocument(
                path_bytes,
                1 if detached else 0,
                1 if inmemory else 0,
                1 if delete_on_close else 0
            )
            check_error()
        else:
            # Bytes input - use OpenDocumentFromBytes
            # Note: No detached parameter for bytes (always uses temp file)
            handle = lib.OpenDocumentFromBytes(
                source,
                len(source),
                1 if inmemory else 0
            )
            check_error()
        
        if handle == 0:
            raise DocumentError("Failed to open document from KDDB")

        # Create wrapper instance without going through __init__
        doc = cls.__new__(cls)
        doc._handle = handle
        doc._closed = False
        doc._metadata_cache = None
        doc._source_cache = None
        doc._data_attributes_accessor = None
        doc._data_objects_accessor = None
        doc._audit_accessor = None
        doc._native_documents_accessor = None
        doc._notes_accessor = None
        doc._finalizer = weakref.finalize(doc, cls._cleanup_handle, handle)
        return doc

    @classmethod
    def create_in_memory(cls, **kwargs):
        """Create in-memory document."""
        return cls(inmemory=True, **kwargs)
    
    @classmethod
    def from_dict(cls, doc_dict: Dict[str, Any], inmemory: bool = False, **kwargs):
        """
        Build a new Document from a dictionary (legacy_python parity).
        
        This method follows the same pattern as legacy_python where from_json
        calls json.loads() and passes the result to from_dict().
        
        Args:
            doc_dict: A dictionary representation of a Kodexa Document
            inmemory: Whether to create document in memory (default: False)
            **kwargs: Additional arguments (for compatibility)
            
        Returns:
            Document: A complete Kodexa Document
            
        Example:
            >>> doc_dict = {"uuid": "123", "metadata": {"key": "value"}}
            >>> doc = Document.from_dict(doc_dict)
        """
        if not isinstance(doc_dict, dict):
            raise TypeError("doc_dict must be a dictionary")
        
        # Convert dictionary to JSON string and use existing from_json
        json_str = json.dumps(doc_dict)
        return cls.from_json(json_str, inmemory=inmemory, **kwargs)
    
    @classmethod  
    def from_json(cls, json_str: str, inmemory: bool = False, **kwargs):
        """
        Create a document from JSON string.
        
        Args:
            json_str: JSON representation of the document
            inmemory: Whether to create document in memory (default: False)
            **kwargs: Additional arguments (for compatibility)
            
        Returns:
            Document: New document instance created from JSON
        """
        if not isinstance(json_str, str):
            raise TypeError("json_str must be a string")
        
        # Convert parameters
        json_bytes = json_str.encode('utf-8')
        inmemory_flag = 1 if inmemory else 0
        
        # Call C function
        handle = lib.CreateDocumentFromJSON(json_bytes, inmemory_flag)
        check_error()
        
        if handle == 0:
            raise RuntimeError("Failed to create document from JSON")

        # Create Document instance with handle
        doc = cls.__new__(cls)
        doc._handle = handle
        doc._closed = False
        doc._metadata_cache = None
        doc._source_cache = None
        doc._data_attributes_accessor = None
        doc._data_objects_accessor = None
        doc._audit_accessor = None
        doc._native_documents_accessor = None
        doc._notes_accessor = None
        doc._finalizer = weakref.finalize(doc, cls._cleanup_handle, handle)

        return doc


    def select(self, selector: str, variables: Optional[Dict[str, Any]] = None, first_only: bool = False):
        """Execute selector query and return matching nodes.
        
        Args:
            selector: The selector expression (e.g., "//paragraph")
            variables: Optional dictionary of variables for selector substitution
            first_only: If True, return only the first matching node as a single-item list
            
        Returns:
            list: List of matching ContentNode objects. Empty list if no matches.
                  If first_only=True, list will contain at most one element.
        """
        if self._closed:
            raise DocumentError("Document is closed")
        
        # Convert parameters to C types
        selector_bytes = selector.encode('utf-8')
        variables_json = ffi.NULL
        if variables:
            variables_json = json.dumps(variables).encode('utf-8')
        first_only_int = 1 if first_only else 0
        
        # Call C function with first_only parameter
        count_ptr = ffi.new("int*")
        handles_ptr = lib.DocumentSelect(self._handle, selector_bytes, variables_json, first_only_int, count_ptr)
        check_error()
        
        if handles_ptr == ffi.NULL or count_ptr[0] == 0:
            return []
        
        # Convert handles to ContentNode objects
        from .content_node import ContentNode
        nodes = []
        for i in range(count_ptr[0]):
            handle = handles_ptr[i]
            if handle != 0:
                node = ContentNode._from_handle(handle)
                node._document = self  # Preserve document reference
                nodes.append(node)

        # Free the handle array
        lib.FreeHandleArray(handles_ptr)

        return nodes

    def select_first(self, selector: str, variables: Optional[Dict[str, Any]] = None):
        """Execute selector query and return the first matching node, or None if no match."""
        if self._closed:
            raise DocumentError("Document is closed")
        
        # Convert parameters to C types
        selector_bytes = selector.encode('utf-8')
        variables_json = ffi.NULL
        if variables:
            variables_json = json.dumps(variables).encode('utf-8')
        
        # Call C function
        handle = lib.DocumentSelectFirst(self._handle, selector_bytes, variables_json)
        check_error()

        if handle == 0:
            return None

        # Convert handle to ContentNode object
        from .content_node import ContentNode
        node = ContentNode._from_handle(handle)
        node._document = self  # Preserve document reference
        return node

    def get_all_tags(self) -> List[str]:
        """
        Get all tag names in the document (legacy_python compatibility).
        
        Returns:
            List of tag names as strings
        """
        self._ensure_not_closed()
        
        # Call C function
        tags_ptr = lib.GetDocumentAllTags(self._handle)
        check_error()
        
        if tags_ptr == ffi.NULL:
            return []
        
        try:
            tags_str = ffi.string(tags_ptr).decode('utf-8')
            return json.loads(tags_str) if tags_str else []
        finally:
            lib.FreeString(tags_ptr)
    
    def get_nodes_by_type(self, node_type: str) -> List['ContentNode']:
        """
        Get all nodes of a specific type (legacy_python compatibility).
        
        Args:
            node_type: The node type to search for
            
        Returns:
            List of ContentNode objects matching the type
        """
        self._ensure_not_closed()
        
        # Call C function
        node_type_bytes = node_type.encode('utf-8')
        handles_ptr = lib.GetNodesByType(self._handle, node_type_bytes)
        check_error()
        
        if handles_ptr == ffi.NULL:
            return []
        
        try:
            handles_str = ffi.string(handles_ptr).decode('utf-8')
            handles_list = json.loads(handles_str) if handles_str else []
            
            # Convert handles to ContentNode objects
            from .content_node import ContentNode
            nodes = []
            for handle in handles_list:
                node = ContentNode._from_handle(handle)
                if node:
                    node._document = self  # Preserve document reference
                    nodes.append(node)

            return nodes
        finally:
            lib.FreeString(handles_ptr)

    def get_all_tagged_nodes(self) -> List[Dict[str, Any]]:
        """
        Get all nodes in the document that have at least one tag.
        
        Returns:
            List of dictionaries containing node data (id, uuid, type, content, index)
            TODO: Return actual ContentNode objects once handle management is improved
        """
        self._ensure_not_closed()
        
        # Call C function
        nodes_ptr = lib.GetAllTaggedNodes(self._handle)
        check_error()
        
        if nodes_ptr == ffi.NULL:
            return []
        
        try:
            nodes_str = ffi.string(nodes_ptr).decode('utf-8')
            nodes_data = json.loads(nodes_str) if nodes_str else []
            
            # For now, return the raw data as dicts since we can't easily
            # reconstruct ContentNode objects without proper handle management
            # TODO: Improve this to return actual ContentNode objects
            return nodes_data
        except json.JSONDecodeError:
            return []
        finally:
            lib.FreeString(nodes_ptr)

    def clear_tags_from_nodes_by_type(self, type_name: str) -> None:
        """
        Clear all tags from nodes of a specific type (e.g., 'word').

        This is a bulk operation that deletes all tag links for nodes of the specified
        type, then removes any orphaned tags that are no longer linked to any nodes.

        Args:
            type_name: The type of nodes to clear tags from (e.g., 'word', 'line')
        """
        self._ensure_not_closed()

        type_name_bytes = type_name.encode('utf-8')

        # Call C function
        result = lib.ClearTagsFromNodesByType(self._handle, type_name_bytes)
        check_error()

        if result == 0:
            raise RuntimeError(f"Failed to clear tags from nodes of type '{type_name}'")

    def get_tags_by_name(self, tag_name: str) -> List[Dict[str, Any]]:
        """
        Get all instances of a specific tag name in the document.
        
        Args:
            tag_name: Name of the tag to search for
            
        Returns:
            List of tag dictionaries with name, value, confidence, group_uuid
        """
        self._ensure_not_closed()
        
        tag_name_bytes = tag_name.encode('utf-8')
        
        # Call C function
        tags_ptr = lib.GetTagsByName(self._handle, tag_name_bytes)
        check_error()
        
        if tags_ptr == ffi.NULL:
            return []
        
        try:
            tags_str = ffi.string(tags_ptr).decode('utf-8')
            return json.loads(tags_str) if tags_str else []
        except json.JSONDecodeError:
            return []
        finally:
            lib.FreeString(tags_ptr)
    
    def get_node_by_uuid(self, uuid: str) -> Optional['ContentNode']:
        """
        Get a content node by its UUID.

        Args:
            uuid: The UUID of the node to find

        Returns:
            ContentNode instance if found, None otherwise
        """
        self._ensure_not_closed()

        # Convert to string if int is passed (e.g., node ID instead of UUID)
        if uuid is None:
            return None
        if not isinstance(uuid, str):
            uuid = str(uuid)

        # Call C function
        uuid_bytes = uuid.encode('utf-8')
        node_handle = lib.GetNodeByUUID(self._handle, uuid_bytes)
        
        # Check for error - if it's "not found", return None instead of throwing
        error_code = lib.KodexaGetLastError()
        if error_code != 0:
            # Get error message to check if it's a "not found" error
            msg_ptr = lib.KodexaGetLastErrorMessage()
            if msg_ptr != ffi.NULL:
                try:
                    error_msg = ffi.string(msg_ptr).decode('utf-8')
                    if "not found" in error_msg.lower():
                        lib.ClearError()  # Clear the error since we're handling it
                        return None
                finally:
                    lib.FreeString(msg_ptr)
            
            # If it's not a "not found" error, let check_error handle it
            check_error()
        
        if node_handle == 0:
            return None

        # Import here to avoid circular imports
        from .content_node import ContentNode
        node = ContentNode._from_handle(node_handle)
        if node:
            node._document = self  # Preserve document reference
        return node

    # TagInstance support (legacy_python parity)

    def get_tag_instances(self, tag: str) -> List['TagInstance']:
        """
        Get all tag instances for a given tag name.

        Groups nodes by tag UUID, where each group represents nodes that
        share the same tag UUID value. This provides organizational
        abstraction for working with related tagged content.

        Args:
            tag: Name of the tag to get instances for

        Returns:
            List of TagInstance objects, each representing nodes with same tag UUID

        Example:
            >>> # Tag multiple nodes with same UUID to group them
            >>> doc.content_node.tag('ServiceAddress', node_only=True)
            >>> instances = doc.get_tag_instances('ServiceAddress')
            >>> for instance in instances:
            ...     print(instance.get_value())  # Combined content from grouped nodes
        """
        self._ensure_not_closed()
        from .tag_instance import TagInstance
        from .content_node import ContentNode

        # Convert to string if not already
        if tag is None:
            return []
        if not isinstance(tag, str):
            tag = str(tag)

        # Call C function
        tag_bytes = tag.encode('utf-8')
        instances_ptr = lib.GetTagInstances(self._handle, tag_bytes)
        check_error()

        if instances_ptr == ffi.NULL:
            return []

        try:
            instances_str = ffi.string(instances_ptr).decode('utf-8')
            instances_data = json.loads(instances_str) if instances_str else []

            # Convert to TagInstance objects
            tag_instances = []
            for instance_dict in instances_data:
                # Convert node handles to ContentNode objects
                nodes = []
                for node_handle in instance_dict.get('nodeHandles', []):
                    node = ContentNode._from_handle(node_handle)
                    if node:
                        node._document = self  # Preserve document reference
                        nodes.append(node)

                tag_instance = TagInstance(
                    tag_name=instance_dict.get('tagName', tag),
                    tag_uuid=instance_dict.get('tagUuid', ''),
                    nodes=nodes,
                    value=instance_dict.get('value'),
                    data=instance_dict.get('data', {})
                )
                tag_instances.append(tag_instance)

            return tag_instances
        finally:
            lib.FreeString(instances_ptr)

    def get_tag_instance(self, tag: str) -> Optional['TagInstance']:
        """
        Get the first tag instance for a given tag name.

        This is a convenience method that returns the first TagInstance,
        matching the legacy_python behavior.

        Args:
            tag: Name of the tag to get instance for

        Returns:
            First TagInstance if found, None otherwise

        Example:
            >>> instance = doc.get_tag_instance('ServiceAddress')
            >>> if instance:
            ...     print(instance.get_value())
        """
        self._ensure_not_closed()
        from .tag_instance import TagInstance
        from .content_node import ContentNode

        # Convert to string if not already
        if tag is None:
            return None
        if not isinstance(tag, str):
            tag = str(tag)

        # Call C function
        tag_bytes = tag.encode('utf-8')
        instance_ptr = lib.GetTagInstance(self._handle, tag_bytes)
        check_error()

        if instance_ptr == ffi.NULL:
            return None

        try:
            instance_str = ffi.string(instance_ptr).decode('utf-8')
            instance_dict = json.loads(instance_str) if instance_str else {}

            if not instance_dict:
                return None

            # Convert node handles to ContentNode objects
            nodes = []
            for node_handle in instance_dict.get('nodeHandles', []):
                node = ContentNode._from_handle(node_handle)
                if node:
                    node._document = self  # Preserve document reference
                    nodes.append(node)

            return TagInstance(
                tag_name=instance_dict.get('tagName', tag),
                tag_uuid=instance_dict.get('tagUuid', ''),
                nodes=nodes,
                value=instance_dict.get('value'),
                data=instance_dict.get('data', {})
            )
        finally:
            lib.FreeString(instance_ptr)

    def add_tag_instance(self, tag_to_apply: str, node_list: List['ContentNode']):
        """
        Create a tag instance by tagging a group of nodes with the same tag UUID.

        This method tags all nodes in the list with the same tag name and UUID,
        creating a grouped relationship between them. The tag instance is then
        cached in the document for later retrieval.

        Args:
            tag_to_apply: Name of the tag to apply to all nodes
            node_list: List of ContentNode objects to group together

        Example:
            >>> # Create a tag instance grouping related address nodes
            >>> address_nodes = doc.content_node.select('//text')[1:4]
            >>> doc.add_tag_instance('ServiceAddress', address_nodes)
        """
        self._ensure_not_closed()

        if not node_list:
            raise ValueError("node_list cannot be empty")

        # Convert ContentNode objects to handles
        node_handles = []
        for node in node_list:
            if not hasattr(node, '_handle'):
                raise ValueError("Invalid ContentNode in node_list")
            node_handles.append(node._handle)

        # Call C function
        tag_bytes = tag_to_apply.encode('utf-8')
        handles_json = json.dumps(node_handles).encode('utf-8')
        result = lib.AddTagInstance(self._handle, tag_bytes, handles_json)
        check_error()

        if result != 1:
            raise RuntimeError("Failed to add tag instance")


    @property
    def tag_instances(self) -> List['TagInstance']:
        """
        Get all tag instances across all tags in the document (legacy_python parity).

        This property queries the database and returns all tag instances for all tags.
        Unlike legacy_python which maintained a cached list, this queries fresh from
        the database following lib/go's cache-through pattern.

        Returns:
            List of all TagInstance objects in the document

        Example:
            >>> # Get all tag instances
            >>> for instance in doc.tag_instances:
            ...     print(f"{instance.tag_name}: {instance.get_value()}")
        """
        self._ensure_not_closed()

        # Get all tags in document
        all_tags = self.get_all_tags()

        # Collect instances for each tag
        all_instances = []
        for tag_name in all_tags:
            instances = self.get_tag_instances(tag_name)
            all_instances.extend(instances)

        return all_instances

    def update_tag_instance(self, tag_uuid: str):
        """
        Update a tag instance by refreshing tag attributes from the database (legacy_python parity).

        In lib/go, this is effectively a no-op since we follow the cache-through pattern - all
        data is always queried fresh from the database. This method exists for API compatibility
        with legacy_python.

        Args:
            tag_uuid: UUID of the tag instance to update

        Example:
            >>> instance = doc.get_tag_instance('ServiceAddress')
            >>> doc.update_tag_instance(instance.tag_uuid)
        """
        self._ensure_not_closed()

        # In cache-through pattern, data is always fresh from database
        # This method is a no-op for API compatibility with legacy_python
        pass

    def remove_tags_by_owner(self, owner_uri: str):
        """
        Remove all tags that have matching owner_uri in their metadata (legacy_python parity).

        This iterates through all nodes in the document tree and removes tags
        when the tag's metadata contains an 'owner_uri' field matching the given value.

        Args:
            owner_uri: The owner URI to match against tag metadata

        Example:
            >>> # Remove all tags created by a specific processor
            >>> doc.remove_tags_by_owner('processor://my-tagger/v1.0')
        """
        self._ensure_not_closed()
        import base64

        # Helper function to recursively get all nodes in tree
        def get_all_nodes_in_tree(node):
            """Recursively collect all nodes from node and descendants."""
            nodes = [node]
            for child in node.get_children():
                nodes.extend(get_all_nodes_in_tree(child))
            return nodes

        # Get all nodes starting from root
        root = self.content_node
        if root is None:
            return  # No content, nothing to remove

        all_nodes = get_all_nodes_in_tree(root)

        # Iterate through all nodes and check each tag
        for node in all_nodes:
            # Get all tags on this node
            tags = node.get_tags()
            for tag in tags:
                # Check if tag has data with matching owner_uri
                if tag.data:
                    try:
                        # Decode base64 and parse JSON
                        decoded = base64.b64decode(tag.data)
                        tag_meta = json.loads(decoded)
                        if 'owner_uri' in tag_meta and tag_meta['owner_uri'] == owner_uri:
                            # Remove this tag from the node
                            node.remove_tag(tag.name)
                    except:
                        # Skip tags with invalid data
                        pass

    # Native Document methods

    def get_native_documents(self) -> List[Dict[str, Any]]:
        """
        Get all native documents stored in this KDDB.

        Native documents are binary files (PDF, Excel, Word, HTML, etc.)
        that have been stored alongside the document data.

        Returns:
            List of dictionaries with id, filename, mime_type, size, and checksum.
            Note: Does not include the binary data - use get_native_document_data() for that.
        """
        self._ensure_not_closed()
        docs_ptr = lib.DocumentGetNativeDocuments(self._handle)
        check_error()
        if docs_ptr == ffi.NULL:
            return []
        try:
            docs_str = ffi.string(docs_ptr).decode('utf-8')
            if not docs_str:
                return []
            docs = json.loads(docs_str)
            # Convert camelCase keys from Go to snake_case for Python
            return [self._convert_dict_keys_to_snake(doc) for doc in docs]
        except json.JSONDecodeError:
            return []
        finally:
            lib.FreeString(docs_ptr)

    def get_native_document_by_id(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a native document by its ID.

        Args:
            doc_id: The ID of the native document to retrieve.

        Returns:
            Dictionary with id, filename, mime_type, size, and checksum, or None if not found.
            Note: Does not include the binary data - use get_native_document_data() for that.
        """
        self._ensure_not_closed()
        doc_ptr = lib.DocumentGetNativeDocumentByID(self._handle, doc_id)
        check_error()
        if doc_ptr == ffi.NULL:
            return None
        try:
            doc_str = ffi.string(doc_ptr).decode('utf-8')
            if not doc_str:
                return None
            doc = json.loads(doc_str)
            return self._convert_dict_keys_to_snake(doc)
        except json.JSONDecodeError:
            return None
        finally:
            lib.FreeString(doc_ptr)

    def get_first_native_document(self) -> Optional[Dict[str, Any]]:
        """
        Get the first native document in this KDDB.

        Returns:
            Dictionary with id, filename, mime_type, size, and checksum, or None if no documents exist.
            Note: Does not include the binary data - use get_native_document_data() for that.
        """
        logger.info("get_first_native_document: starting")
        self._ensure_not_closed()
        logger.debug(f"get_first_native_document: document handle={self._handle}")

        doc_ptr = lib.DocumentGetFirstNativeDocument(self._handle)
        check_error()

        if doc_ptr == ffi.NULL:
            logger.info("get_first_native_document: no native document found (NULL pointer)")
            return None

        try:
            doc_str = ffi.string(doc_ptr).decode('utf-8')
            logger.debug(f"get_first_native_document: raw response length={len(doc_str) if doc_str else 0}")

            if not doc_str:
                logger.info("get_first_native_document: empty string response")
                return None

            doc = json.loads(doc_str)
            logger.debug(f"get_first_native_document: parsed JSON keys={list(doc.keys())}")

            result = self._convert_dict_keys_to_snake(doc)
            logger.info(f"get_first_native_document: found native doc id={result.get('id')}, "
                       f"filename={result.get('filename')}, mime_type={result.get('mime_type')}, "
                       f"size={result.get('size')}")
            return result
        except json.JSONDecodeError as e:
            logger.error(f"get_first_native_document: JSON decode error: {e}")
            return None
        finally:
            lib.FreeString(doc_ptr)

    def get_native_document_by_filename(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Get a native document by its filename.

        Args:
            filename: The filename of the native document to retrieve.

        Returns:
            Dictionary with id, filename, mime_type, size, and checksum, or None if not found.
            Note: Does not include the binary data - use get_native_document_data() for that.
        """
        self._ensure_not_closed()
        filename_bytes = filename.encode('utf-8')
        doc_ptr = lib.DocumentGetNativeDocumentByFilename(self._handle, filename_bytes)
        check_error()
        if doc_ptr == ffi.NULL:
            return None
        try:
            doc_str = ffi.string(doc_ptr).decode('utf-8')
            if not doc_str:
                return None
            doc = json.loads(doc_str)
            return self._convert_dict_keys_to_snake(doc)
        except json.JSONDecodeError:
            return None
        finally:
            lib.FreeString(doc_ptr)

    def get_native_document_data(self, doc_id: int) -> Optional[bytes]:
        """
        Get the binary data of a native document.

        Args:
            doc_id: The ID of the native document.

        Returns:
            The binary data as bytes, or None if the document is not found.
        """
        self._ensure_not_closed()
        out_len = ffi.new("int*")
        data_ptr = lib.DocumentGetNativeDocumentData(self._handle, doc_id, out_len)
        check_error()
        if data_ptr == ffi.NULL:
            return None
        try:
            length = out_len[0]
            return ffi.buffer(data_ptr, length)[:]
        finally:
            lib.FreeBytes(data_ptr)

    def create_native_document(self, filename: str, mime_type: str, data: bytes,
                               checksum: Optional[str] = None) -> int:
        """
        Create a new native document in this KDDB.

        Args:
            filename: The filename of the document.
            mime_type: The MIME type (e.g., "application/pdf", "text/html").
            data: The binary content of the document.
            checksum: Optional checksum for integrity verification.

        Returns:
            The ID of the created native document.

        Example:
            >>> with open("document.pdf", "rb") as f:
            ...     pdf_data = f.read()
            >>> doc_id = doc.create_native_document("document.pdf", "application/pdf", pdf_data)
        """
        self._ensure_not_closed()
        filename_bytes = filename.encode('utf-8')
        mime_type_bytes = mime_type.encode('utf-8')
        checksum_bytes = checksum.encode('utf-8') if checksum else ffi.NULL

        doc_id = lib.DocumentCreateNativeDocument(
            self._handle, filename_bytes, mime_type_bytes,
            data, len(data), checksum_bytes
        )
        check_error()

        if doc_id == 0:
            raise RuntimeError("Failed to create native document")

        return doc_id

    def delete_native_document(self, doc_id: int) -> bool:
        """
        Delete a native document by its ID.

        Args:
            doc_id: The ID of the native document to delete.

        Returns:
            True if the document was deleted successfully.
        """
        self._ensure_not_closed()
        result = lib.DocumentDeleteNativeDocument(self._handle, doc_id)
        check_error()
        return result == 1

    def delete_all_native_documents(self) -> bool:
        """
        Delete all native documents from this KDDB.

        Returns:
            True if all documents were deleted successfully.
        """
        self._ensure_not_closed()
        result = lib.DocumentDeleteAllNativeDocuments(self._handle)
        check_error()
        return result == 1

    # ==========================================================================
    # Additional methods (previously unexposed Go methods)
    # ==========================================================================

    def find_nodes_by_tag_uuid(self, tag_uuid: str) -> List['ContentNode']:
        """
        Find all content nodes that have a tag with the specified UUID.

        Args:
            tag_uuid: The UUID of the tag to search for.

        Returns:
            List of ContentNode objects that have the specified tag.
        """
        self._ensure_not_closed()
        from .content_node import ContentNode

        count_ptr = ffi.new("int*")
        handles_ptr = lib.GetTaggedNodesByTagUUID(self._handle, tag_uuid.encode('utf-8'), count_ptr)
        check_error()

        if handles_ptr == ffi.NULL:
            return []

        count = count_ptr[0]
        nodes = []
        for i in range(count):
            node_handle = handles_ptr[i]
            if node_handle != 0:
                nodes.append(ContentNode(document=self, handle=node_handle))

        lib.FreeHandleArray(handles_ptr)
        return nodes

    def get_node_by_id(self, node_id: int) -> Optional['ContentNode']:
        """
        Get a content node by its numeric database ID.

        Args:
            node_id: The numeric ID of the node.

        Returns:
            The ContentNode if found, None otherwise.
        """
        self._ensure_not_closed()
        from .content_node import ContentNode

        handle = lib.GetNodeByNumericID(self._handle, node_id)
        check_error()

        if handle == 0:
            return None

        return ContentNode(document=self, handle=handle)

    def get_node_count_by_type(self, type_name: str) -> int:
        """
        Get the count of nodes with the specified type name.

        Args:
            type_name: The node type name to count.

        Returns:
            The number of nodes with the specified type.
        """
        self._ensure_not_closed()
        count = lib.GetNodeCountByTypeName(self._handle, type_name.encode('utf-8'))
        check_error()
        return int(count)

    def get_feature_types_with_counts(self) -> List[Dict]:
        """
        Get all feature types with their instance counts.

        Returns:
            List of dicts with 'id', 'name', and 'count' keys.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetFeatureTypesWithCounts(self._handle)
        check_error()

        if result_ptr == ffi.NULL:
            return []

        result_str = ffi.string(result_ptr).decode('utf-8')
        lib.FreeString(result_ptr)
        return json.loads(result_str)

    def get_node_types_with_counts(self) -> List[Dict]:
        """
        Get all node types with their instance counts.

        Returns:
            List of dicts with 'id', 'name', and 'count' keys.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetNodeTypesWithCounts(self._handle)
        check_error()

        if result_ptr == ffi.NULL:
            return []

        result_str = ffi.string(result_ptr).decode('utf-8')
        lib.FreeString(result_ptr)
        return json.loads(result_str)

    def replace_exceptions(self, exceptions: List[Dict]) -> bool:
        """
        Replace all content exceptions with the provided list.

        Args:
            exceptions: List of exception dictionaries.

        Returns:
            True if successful.
        """
        self._ensure_not_closed()
        exceptions_json = json.dumps(exceptions).encode('utf-8')
        result = lib.ReplaceAllExceptions(self._handle, exceptions_json)
        check_error()
        return result == 1

    def get_tags_by_prefix(self, prefix: str) -> List[Dict]:
        """
        Get all tags whose names start with the specified prefix.

        Args:
            prefix: The prefix to match tag names against.

        Returns:
            List of tag dictionaries.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetTagsByPrefix(self._handle, prefix.encode('utf-8'))
        check_error()

        if result_ptr == ffi.NULL:
            return []

        result_str = ffi.string(result_ptr).decode('utf-8')
        lib.FreeString(result_ptr)
        return json.loads(result_str)

    def create_data_exception(self, exception: Dict) -> bool:
        """
        Create a new data exception.

        Args:
            exception: Dictionary with exception data (exception_type, message, severity, path, data_object_id).

        Returns:
            True if successful.
        """
        self._ensure_not_closed()
        exception_json = json.dumps(exception).encode('utf-8')
        result = lib.CreateDataException(self._handle, exception_json)
        check_error()
        return result == 1

    def get_data_objects_by_parent_id(self, parent_id: int) -> List[Dict]:
        """
        Get all data objects that are children of the specified parent.

        Args:
            parent_id: The ID of the parent data object.

        Returns:
            List of data object dictionaries.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetDataObjectsByParentID(self._handle, parent_id)
        check_error()

        if result_ptr == ffi.NULL:
            return []

        result_str = ffi.string(result_ptr).decode('utf-8')
        lib.FreeString(result_ptr)
        return json.loads(result_str)

    def get_all_features(self) -> List[Dict]:
        """
        Get all features in the document.

        Returns:
            List of feature dictionaries with 'id', 'value', and 'data' keys.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetAllFeatures(self._handle)
        check_error()

        if result_ptr == ffi.NULL:
            return []

        result_str = ffi.string(result_ptr).decode('utf-8')
        lib.FreeString(result_ptr)
        return json.loads(result_str)

    def get_document_filename(self) -> str:
        """
        Get the original filename of the document from source metadata.

        Returns:
            The filename string, or empty string if not available.
        """
        self._ensure_not_closed()
        result_ptr = lib.GetDocumentFilename(self._handle)
        check_error()

        if result_ptr == ffi.NULL:
            return ""

        result_str = ffi.string(result_ptr).decode('utf-8')
        lib.FreeString(result_ptr)
        return result_str

    def get_feature_set(self, owner_uri: Optional[str] = None) -> 'FeatureSet':
        """
        Get a FeatureSet containing all tag features from tagged nodes.

        A FeatureSet is a structured export of all tagged nodes and their
        tag features, useful for data extraction and export.

        Args:
            owner_uri: Optional filter - only include tags with this owner_uri

        Returns:
            FeatureSet containing node features for all tagged nodes

        Example:
            >>> feature_set = doc.get_feature_set()
            >>> for node_feat in feature_set.node_features:
            ...     print(f"Node {node_feat.node_uuid}: {len(node_feat.features)} features")
        """
        from .objects import FeatureSet, NodeFeatures, ContentFeature as PydanticContentFeature
        from .content_node import ContentNode

        self._ensure_not_closed()

        feature_set = FeatureSet()
        feature_set.node_features = []

        # Get all tagged nodes
        tagged_nodes_data = self.get_all_tagged_nodes()

        for node_data in tagged_nodes_data:
            # Get the node by UUID to access its features
            node_uuid = node_data.get('uuid')
            if not node_uuid:
                continue

            node = self.get_node_by_uuid(node_uuid)
            if node is None:
                continue

            node_features = NodeFeatures(node_uuid=str(node_uuid), features=[])
            feature_set.node_features.append(node_features)

            # Get all features and filter for tag features
            for feature in node.get_features():
                if feature.feature_type == "tag":
                    # Check owner_uri filter if specified
                    if owner_uri is not None:
                        # Tag feature values contain dicts with owner_uri
                        if feature.value and len(feature.value) > 0:
                            first_val = feature.value[0]
                            if isinstance(first_val, dict):
                                if first_val.get('owner_uri') != owner_uri:
                                    continue

                    # Convert to Pydantic ContentFeature for FeatureSet
                    feature_dict = feature.to_dict()
                    pydantic_feature = PydanticContentFeature(
                        feature_type=feature.feature_type,
                        name=feature.name,
                        value=feature.value
                    )
                    node_features.features.append(pydantic_feature)

        return feature_set


class _TransactionContextManager:
    """Context manager for database transactions."""

    def __init__(self, document: Document):
        self._document = document

    def __enter__(self):
        self._document.begin_transaction()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Exception occurred - rollback
            try:
                self._document.rollback_transaction()
            except Exception:
                # Ignore rollback errors when already handling an exception
                pass
            return False  # Re-raise the exception
        else:
            # No exception - commit
            self._document.commit_transaction()
            return False