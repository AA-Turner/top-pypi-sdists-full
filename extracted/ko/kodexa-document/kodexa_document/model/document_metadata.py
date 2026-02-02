"""
DocumentMetadata class for legacy_python compatibility.

Provides dict-like access with dot notation support, matching the legacy_python
DocumentMetadata that extends addict.Dict.
"""
import json
from typing import Any
from addict import Dict


class DocumentMetadata(Dict):
    """
    A cached metadata object that writes all changes to Go immediately.

    This class extends addict.Dict to provide dot notation access.
    Any modification triggers a complete write of all metadata to Go.
    """

    def __init__(self, *args, document=None, **kwargs):
        """
        Initialize DocumentMetadata.

        Args:
            *args: Initial data (typically a dict)
            document: The Document instance this metadata belongs to
            **kwargs: Additional keyword arguments
        """
        # Store document reference using object.__setattr__ to avoid triggering addict
        object.__setattr__(self, '_document', document)

        # Initialize with data
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
        Set a value and immediately write all metadata to Go.
        """
        # Convert plain dicts to Dict for dot notation support
        if isinstance(value, dict) and not isinstance(value, Dict):
            value = Dict(value)

        # Update local dict
        super().__setitem__(key, value)

        # Write everything to Go
        self._save_to_go()

    def __setattr__(self, key, value):
        """
        Set an attribute and immediately write all metadata to Go.
        """
        # Convert plain dicts to Dict for dot notation support
        if not key.startswith('_') and isinstance(value, dict) and not isinstance(value, Dict):
            value = Dict(value)

        # Let addict handle the dot notation
        super().__setattr__(key, value)

        # For non-internal attributes, save to Go
        if not key.startswith('_'):
            self._save_to_go()

    def __delitem__(self, key):
        """
        Delete a key and immediately write all metadata to Go.
        """
        super().__delitem__(key)
        self._save_to_go()

    def _save_to_go(self):
        """Write all metadata to Go backend."""
        document = object.__getattribute__(self, '_document')
        if not document:
            return

        # Import here to avoid circular dependency
        from .._native import lib, ffi
        from ..errors import check_error

        # Clear existing metadata first
        handle = document._handle

        # Get current keys from Go to clear them
        metadata_ptr = lib.GetDocumentMetadata(handle)
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

        # Clear all existing keys
        for key in current_keys:
            key_bytes = key.encode('utf-8')
            lib.SetDocumentMetadata(handle, key_bytes, b'')
            check_error()

        # Write all our keys
        for key, value in self.items():
            if not key.startswith('_'):
                key_bytes = key.encode('utf-8')
                value_json = json.dumps(self._to_plain(value))
                value_bytes = value_json.encode('utf-8')
                lib.SetDocumentMetadata(handle, key_bytes, value_bytes)
                check_error()

    def _to_plain(self, obj):
        """Convert nested Dict objects to plain dicts for JSON serialization."""
        if isinstance(obj, Dict):
            return {k: self._to_plain(v) for k, v in obj.items()}
        elif isinstance(obj, dict):
            return {k: self._to_plain(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._to_plain(item) for item in obj]
        else:
            return obj
