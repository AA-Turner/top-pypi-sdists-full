"""
Extraction Engine Python wrapper classes for Go bindings.
"""

import json
import weakref
from typing import List, Dict, Any, Optional, Union

from .._native import ffi, get_library
from ..errors import check_error, KodexaError
from ..model.content_exception import ContentException


lib = get_library()


class DataException:
    """Represents a data exception from validation or extraction."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize from JSON data."""
        self.id = data.get('id', 0)
        self.uuid = data.get('uuid', '')
        self.message = data.get('message', '')
        self.exception_details = data.get('exception_details', '')
        self.exception_type = data.get('exception_type', '')
        self.severity = data.get('severity', '')
        self.path = data.get('path')
        self.closing_comment = data.get('closing_comment', '')
        self.open = data.get('open', False)
        self.data_object_id = data.get('data_object_id', 0)
        self.data_attribute_id = data.get('data_attribute_id')
        self.created_on = data.get('created_on')
        self.updated_on = data.get('updated_on')


class DataAttribute:
    """Represents a single data attribute from extraction results."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize from JSON data."""
        self.uuid = data.get('uuid', '')
        self.data_object_id = data.get('data_object_id')
        self.path = data.get('path', '')
        self.tag = data.get('tag', '')
        self.tag_uuid = data.get('tag_uuid', '')
        self.value = data.get('value')
        self.confidence = data.get('confidence')
        self.taxonomy_ref = data.get('taxonomy_ref', '')
        self.taxon_type = data.get('taxon_type')
        self.group_uuid = data.get('group_uuid', '')
        self.parent_group_uuid = data.get('parent_group_uuid')
        self.cell_index = data.get('cell_index', 0)
        self.node_uuid = data.get('node_uuid', '')
        self.node_id = data.get('node_id', 0)
        self.source = data.get('source', '')
        self.manual = data.get('manual', False)

        # Load data exceptions
        self.data_exceptions = []
        if 'dataExceptions' in data:
            for exc_data in data['dataExceptions']:
                self.data_exceptions.append(DataException(exc_data))


class DataObject:
    """Represents a data object from extraction results."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize from JSON data."""
        self.id = data.get('id')
        self.uuid = data.get('uuid', '')
        self.name = data.get('name', '')
        self.type = data.get('type', '')
        self.taxonomy_ref = data.get('taxonomy_ref', '')
        self.group_path = data.get('group_path', '')
        # Note: UUID now serves as the group identifier (previously separate group_uuid field)
        # For backward compatibility, check both group_uuid and uuid
        self.group_uuid = data.get('group_uuid', '') or data.get('uuid', '')
        # parent_group_uuid is deprecated - use parent_id instead
        # Keep for backward compatibility with old data
        self.parent_group_uuid = data.get('parent_group_uuid')
        # parent_id is the primary parent reference (database FK)
        self.parent_id = data.get('parent_id') or data.get('parentId')  # Support both snake_case and camelCase
        self.content_object_uuid = data.get('content_object_uuid')
        self.document_family_ref = data.get('document_family_ref')
        self.cell_index = data.get('cell_index', 0)
        self.created_on = data.get('created_on')
        self.updated_on = data.get('updated_on')

        # Load attributes
        self.attributes = []
        if 'attributes' in data:
            for attr_data in data['attributes']:
                self.attributes.append(DataAttribute(attr_data))

        # Load data exceptions
        self.data_exceptions = []
        if 'dataExceptions' in data:
            for exc_data in data['dataExceptions']:
                self.data_exceptions.append(DataException(exc_data))

        # Load child objects
        self.children = []
        if 'children' in data:
            for child_data in data['children']:
                self.children.append(DataObject(child_data))


# ContentException is now imported from content_exception module
# which provides legacy_python compatibility


class DocumentTaxonValidation:
    """Represents a document taxon validation."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize from JSON data."""
        self.taxonomy_ref = data.get('taxonomy_ref', data.get('taxonomyRef', ''))
        self.taxon_path = data.get('taxon_path', data.get('taxonPath', ''))
        self.validation = data.get('validation', {})


class Taxonomy:
    """Python wrapper for a taxonomy object."""
    
    def __init__(self, taxonomy_data: Optional[Dict[str, Any]] = None, 
                 taxonomy_path: Optional[str] = None):
        """
        Initialize a Taxonomy.
        
        Args:
            taxonomy_data: Dictionary containing taxonomy structure
            taxonomy_path: Path to taxonomy JSON file
        """
        self._handle: Optional[int] = None
        self._closed = False
        
        if taxonomy_data is not None:
            self._create_from_data(taxonomy_data)
        elif taxonomy_path is not None:
            self._create_from_file(taxonomy_path)
        else:
            raise ValueError("Either taxonomy_data or taxonomy_path must be provided")
            
        # Set up automatic cleanup
        self._finalizer = weakref.finalize(self, self._cleanup_handle, self._handle)
        
    def _create_from_data(self, taxonomy_data: Dict[str, Any]):
        """Create taxonomy from dictionary data."""
        json_data = json.dumps(taxonomy_data).encode('utf-8')
        self._handle = lib.LoadTaxonomy(json_data)
        check_error()
        
        if self._handle == 0:
            raise KodexaError("Failed to create taxonomy from data")
            
    def _create_from_file(self, taxonomy_path: str):
        """Create taxonomy from file path."""
        path_bytes = taxonomy_path.encode('utf-8')
        self._handle = lib.LoadTaxonomyFromFile(path_bytes)
        check_error()
        
        if self._handle == 0:
            raise KodexaError(f"Failed to load taxonomy from file: {taxonomy_path}")
            
    def _check_not_closed(self):
        """Check if taxonomy is closed and raise error if so."""
        if self._closed or self._handle is None:
            raise KodexaError("Taxonomy is closed")
            
    @staticmethod
    def _cleanup_handle(handle: Optional[int]):
        """Clean up the C handle."""
        if handle is not None and handle != 0:
            try:
                lib.FreeTaxonomy(handle)
            except:
                pass  # Ignore errors during cleanup
                
    def validate(self) -> bool:
        """
        Validate the taxonomy structure.
        
        Returns:
            True if valid, False otherwise
        """
        self._check_not_closed()
        
        # Get taxonomy JSON and validate it
        json_data = self.to_json()
        json_bytes = json_data.encode('utf-8')
        
        result = lib.ValidateTaxonomy(json_bytes)
        check_error()
        
        return result == 1
        
    def to_json(self) -> str:
        """
        Get taxonomy as JSON string.
        
        Returns:
            JSON representation of the taxonomy
        """
        self._check_not_closed()
        
        json_ptr = lib.GetTaxonomyJSON(self._handle)
        check_error()
        
        if json_ptr == ffi.NULL:
            return "{}"
            
        try:
            json_str = ffi.string(json_ptr).decode('utf-8')
            return json_str
        finally:
            lib.FreeString(json_ptr)
            
    def close(self):
        """Close the taxonomy and free resources."""
        if not self._closed and self._handle is not None:
            lib.FreeTaxonomy(self._handle)
            self._handle = None
            self._closed = True
            self._finalizer.detach()
            
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


class ExtractionEngine:
    """Python wrapper for the extraction engine."""
    
    def __init__(self, document, taxonomies: List[Union[Taxonomy, Dict[str, Any]]]):
        """
        Initialize an ExtractionEngine.
        
        Args:
            document: Document instance to extract from
            taxonomies: List of Taxonomy instances or taxonomy dictionaries
        """
        self._handle: Optional[int] = None
        self._closed = False
        self._document = document  # Keep reference to prevent GC
        self._taxonomies = []  # Keep references
        
        # Convert taxonomies to JSON
        taxonomy_list = []
        for taxonomy in taxonomies:
            if isinstance(taxonomy, Taxonomy):
                taxonomy_dict = json.loads(taxonomy.to_json())
                taxonomy_list.append(taxonomy_dict)
                self._taxonomies.append(taxonomy)  # Keep reference
            elif isinstance(taxonomy, dict):
                taxonomy_list.append(taxonomy)
            else:
                raise ValueError("Taxonomies must be Taxonomy instances or dictionaries")
                
        # Create extraction engine
        taxonomies_json = json.dumps(taxonomy_list).encode('utf-8')
        self._handle = lib.CreateExtractionEngine(document._handle, taxonomies_json)
        check_error()
        
        if self._handle == 0:
            raise KodexaError("Failed to create extraction engine")
            
        # Set up automatic cleanup
        self._finalizer = weakref.finalize(self, self._cleanup_handle, self._handle)
        
    def _check_not_closed(self):
        """Check if engine is closed and raise error if so."""
        if self._closed or self._handle is None:
            raise KodexaError("Extraction engine is closed")
            
    @staticmethod
    def _cleanup_handle(handle: Optional[int]):
        """Clean up the C handle."""
        if handle is not None and handle != 0:
            try:
                lib.FreeExtractionEngine(handle)
            except:
                pass  # Ignore errors during cleanup
                
    def process_and_save(self) -> int:
        """
        Process the extraction, persist all DataObjects and DataExceptions.

        This method combines extraction with persistence:
        1. Runs the extraction engine
        2. Saves all DataObjects to the document database
        3. Saves all DataExceptions (from DataObjects and DataAttributes)
        4. Recursively saves all children

        After calling this method, doc.get_all_data_exceptions() will return the persisted exceptions.

        Returns:
            The number of data objects extracted
        """
        self._check_not_closed()

        # Process extraction and save to database
        count = lib.ProcessAndSaveExtraction(self._handle)
        check_error()

        return count

    def get_content_exceptions(self) -> List[ContentException]:
        """
        Get content exceptions from extraction.
        
        Returns:
            List of ContentException instances
        """
        self._check_not_closed()
        
        json_ptr = lib.GetContentExceptions(self._handle)
        check_error()
        
        if json_ptr == ffi.NULL:
            return []
            
        try:
            json_str = ffi.string(json_ptr).decode('utf-8')
            if not json_str:
                return []
                
            exception_list = json.loads(json_str)
            return [ContentException.from_go_dict(data) for data in exception_list]
        except json.JSONDecodeError:
            return []
        finally:
            lib.FreeString(json_ptr)
            
    def get_document_taxon_validations(self) -> List[DocumentTaxonValidation]:
        """
        Get document taxon validations from extraction.

        Returns:
            List of DocumentTaxonValidation instances
        """
        self._check_not_closed()

        json_ptr = lib.GetDocumentTaxonValidations(self._handle)
        check_error()
        
        if json_ptr == ffi.NULL:
            return []
            
        try:
            json_str = ffi.string(json_ptr).decode('utf-8')
            if not json_str:
                return []
                
            validation_list = json.loads(json_str)
            return [DocumentTaxonValidation(data) for data in validation_list]
        except json.JSONDecodeError:
            return []
        finally:
            lib.FreeString(json_ptr)
            
    def close(self):
        """Close the extraction engine and free resources."""
        if not self._closed and self._handle is not None:
            lib.FreeExtractionEngine(self._handle)
            self._handle = None
            self._closed = True
            self._finalizer.detach()
            
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


