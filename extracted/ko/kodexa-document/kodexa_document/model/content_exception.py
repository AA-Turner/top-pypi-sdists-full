"""
ContentException class for legacy_python compatibility.

Provides a dict-based ContentException that matches the legacy_python model.py version,
supporting both manual creation and deserialization from Go extraction engine.
"""
from typing import Optional, Dict, Any


class ContentException(dict):
    """
    ContentException that matches legacy_python model.py structure.
    
    Inherits from dict to support both exception.field and exception['field'] access patterns.
    Represents an issue identified during labeling/validation at the document level.
    """
    
    def __init__(
        self,
        exception_type: str = None,
        message: str = None,
        severity: str = "ERROR",
        tag: Optional[str] = None,
        group_uuid: Optional[str] = None,
        tag_uuid: Optional[str] = None,
        exception_type_id: Optional[str] = None,
        exception_details: Optional[str] = None,
        node_uuid: Optional[str] = None,
        value: Optional[str] = None,
        boolean_value: Optional[bool] = None,
        *args,
        **kwargs
    ):
        """
        Initialize ContentException with legacy_python-compatible constructor.
        
        Args:
            exception_type: Type of the exception (required)
            message: Exception message (required)
            severity: Severity level (default: "ERROR")
            tag: Associated tag name
            group_uuid: Group UUID for grouping exceptions
            tag_uuid: Tag UUID
            exception_type_id: Exception type identifier
            exception_details: Detailed exception information
            node_uuid: UUID of the associated content node
            value: Associated string value
            boolean_value: Associated boolean value
            *args: Additional positional arguments (for flexibility)
            **kwargs: Additional keyword arguments (stored in dict)
        """
        super().__init__()
        
        # Handle dict as first argument (for backward compatibility with tests)
        if isinstance(exception_type, dict) and message is None:
            # Called with a dict as first argument
            data = exception_type
            exception_type = data.get('exception_type', '')
            message = data.get('message', '')
            severity = data.get('severity', severity)
            tag = data.get('tag', tag)
            group_uuid = data.get('group_uuid', group_uuid)
            tag_uuid = data.get('tag_uuid', tag_uuid)
            exception_type_id = data.get('exception_type_id', exception_type_id)
            exception_details = data.get('exception_details', exception_details)
            node_uuid = data.get('node_uuid', node_uuid)
            value = data.get('value', value)
            boolean_value = data.get('boolean_value', boolean_value)
            # Merge any additional fields from data into kwargs
            for key, val in data.items():
                if key not in ['exception_type', 'message', 'severity', 'tag', 'group_uuid',
                              'tag_uuid', 'exception_type_id', 'exception_details', 
                              'node_uuid', 'value', 'boolean_value']:
                    kwargs[key] = val
        
        # Store required fields (use empty strings if None for backward compat)
        self['exception_type'] = exception_type if exception_type is not None else ''
        self['message'] = message if message is not None else ''
        self['severity'] = severity
        
        # Store optional fields if provided
        if tag is not None:
            self['tag'] = tag
        if group_uuid is not None:
            self['group_uuid'] = group_uuid
        if tag_uuid is not None:
            self['tag_uuid'] = tag_uuid
        if exception_type_id is not None:
            self['exception_type_id'] = exception_type_id
        if exception_details is not None:
            self['exception_details'] = exception_details
        if node_uuid is not None:
            self['node_uuid'] = node_uuid
        if value is not None:
            self['value'] = value
        if boolean_value is not None:
            self['boolean_value'] = boolean_value
            
        # Store any additional kwargs
        for key, val in kwargs.items():
            if val is not None:
                self[key] = val
    
    def __getattr__(self, name):
        """Support dot notation access: exception.field"""
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'ContentException' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Support dot notation assignment: exception.field = value"""
        if name.startswith('_'):
            # Allow private attributes for internal use
            super(dict, self).__setattr__(name, value)
        else:
            self[name] = value
    
    def __delattr__(self, name):
        """Support dot notation deletion: del exception.field"""
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'ContentException' object has no attribute '{name}'")
    
    @classmethod
    def from_go_dict(cls, data: Dict[str, Any]) -> 'ContentException':
        """
        Create ContentException from Go backend data.
        
        Used by extraction engine to deserialize exceptions from Go.
        Handles field name mapping from Go (camelCase/snake_case) to Python.
        
        Args:
            data: Dictionary from Go backend with exception data
            
        Returns:
            ContentException instance with legacy_python field names
        """
        if not data:
            # Handle empty data gracefully
            return cls(exception_type="UNKNOWN", message="")
        
        # Map Go fields to legacy constructor parameters
        # Go struct uses snake_case for most fields
        return cls(
            exception_type=data.get('exception_type', data.get('exceptionType', '')),
            message=data.get('message', ''),
            severity=data.get('severity', 'ERROR'),
            tag=data.get('tag'),
            group_uuid=data.get('group_uuid', data.get('groupUuid')),
            tag_uuid=data.get('tag_uuid', data.get('tagUuid')),
            exception_type_id=data.get('exception_type_id', data.get('exceptionTypeId')),
            exception_details=data.get('exception_details', data.get('exceptionDetails')),
            node_uuid=data.get('node_uuid', data.get('nodeUuid')),
            value=data.get('value'),
            boolean_value=data.get('boolean_value', data.get('booleanValue')),
            # Include any additional fields from Go
            id=data.get('id'),
            path=data.get('path'),
            open=data.get('open'),
            closing_comment=data.get('closing_comment', data.get('closingComment')),
            created_at=data.get('created_at', data.get('createdAt')),
            updated_at=data.get('updated_at', data.get('updatedAt'))
        )
    
    def to_go_dict(self) -> Dict[str, Any]:
        """
        Convert ContentException to format expected by Go backend.
        
        Handles field name conversion from Python to Go struct field names (camelCase).
        
        Returns:
            Dict suitable for JSON serialization to Go backend
        """
        go_dict = {}
        
        # Map Python fields to Go field names (camelCase)
        field_mapping = {
            'exception_type': 'exceptionType',
            'message': 'message',
            'severity': 'severity',
            'tag': 'tag',
            'group_uuid': 'groupUuid',
            'tag_uuid': 'tagUuid',
            'exception_type_id': 'exceptionTypeId',
            'exception_details': 'exceptionDetails',
            'node_uuid': 'nodeUuid',
            'value': 'value',
            'boolean_value': 'booleanValue',
            'id': 'id',
            'path': 'path',
            'open': 'open',
            'closing_comment': 'closingComment',
            'created_at': 'createdAt',
            'updated_at': 'updatedAt'
        }
        
        for python_key, go_key in field_mapping.items():
            if python_key in self and self[python_key] is not None:
                go_dict[go_key] = self[python_key]
        
        # Include any additional fields not in mapping
        for key, value in self.items():
            if key not in field_mapping and value is not None:
                go_dict[key] = value
        
        return go_dict
    
    def __repr__(self) -> str:
        """String representation of ContentException."""
        return f"ContentException(exception_type='{self.get('exception_type', '')}', message='{self.get('message', '')}', severity='{self.get('severity', 'ERROR')}')"
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.get('severity', 'ERROR')}: [{self.get('exception_type', 'UNKNOWN')}] {self.get('message', '')}"