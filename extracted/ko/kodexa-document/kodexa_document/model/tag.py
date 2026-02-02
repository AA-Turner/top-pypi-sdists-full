"""
Tag class for legacy_python compatibility.

Provides a mutable Dict subclass that supports dot notation and dict access
for tag data, matching the legacy_python Tag class structure exactly.
"""
import json
import uuid
from typing import Optional, List, Dict, Any, Union


class Tag(dict):
    """
    Tag class that matches legacy_python structure.
    
    Inherits from dict to support both tag.field and tag['field'] access patterns.
    Provides full compatibility with legacy_python Tag class constructor and behavior.
    """
    
    def __init__(self, start: Optional[int] = None, end: Optional[int] = None,
                 value: Optional[str] = None, uuid_val: Optional[str] = None,
                 data: Any = None, confidence: Optional[float] = None,
                 group_uuid: Optional[str] = None, parent_group_uuid: Optional[str] = None,
                 cell_index: Optional[int] = None, index: Optional[int] = None,
                 bbox: Optional[List[int]] = None, note: Optional[str] = None,
                 status: Optional[str] = None, owner_uri: Optional[str] = None,
                 is_dirty: Optional[bool] = None, **kwargs):
        """
        Initialize Tag with legacy_python-compatible constructor.
        
        Args:
            start: Start position in content (zero-indexed)
            end: End position in content (zero-indexed)
            value: Labeled value
            uuid_val: Tag UUID (auto-generated if not provided)
            data: Associated data object (JSON serializable)
            confidence: Tag confidence (0-1 range)
            group_uuid: Group UUID for grouping tags
            parent_group_uuid: Parent group UUID
            cell_index: Cell index for table-like structures
            index: Tag index for ordering
            bbox: Bounding box for spatial labels (IGNORED - not supported)
            note: Associated note
            status: Tag status
            owner_uri: Owner URI (e.g., model://kodexa/narrative:1.0.0)
            is_dirty: Whether tag has been modified
            **kwargs: Additional fields for forward compatibility
        """
        super().__init__()
        
        # Store all fields that will be persisted
        if start is not None:
            self['start'] = start
        if end is not None:
            self['end'] = end
        if value is not None:
            self['value'] = value
        if uuid_val is not None:
            self['uuid'] = uuid_val
        else:
            self['uuid'] = str(uuid.uuid4())  # Auto-generate like legacy
        if data is not None:
            self['data'] = data
        if confidence is not None:
            self['confidence'] = confidence
        if group_uuid is not None:
            self['group_uuid'] = group_uuid
        if parent_group_uuid is not None:
            self['parent_group_uuid'] = parent_group_uuid
        if cell_index is not None:
            self['cell_index'] = cell_index
        if index is not None:
            self['index'] = index
        if note is not None:
            self['note'] = note
        if status is not None:
            self['status'] = status
        if owner_uri is not None:
            self['owner_uri'] = owner_uri
        if is_dirty is not None:
            self['is_dirty'] = is_dirty
            
        # Handle bbox parameter for compatibility but don't store it
        # (intentionally excluded from our implementation)
        if bbox is not None:
            pass  # Accept parameter but ignore it
            
        # Handle any additional kwargs
        for key, value in kwargs.items():
            if value is not None:
                self[key] = value
    
    def __getattr__(self, name):
        """Support dot notation access: tag.field"""
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'Tag' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        """Support dot notation assignment: tag.field = value"""
        if name.startswith('_'):
            # Allow private attributes for internal use
            super(dict, self).__setattr__(name, value)
        else:
            self[name] = value
    
    def __delattr__(self, name):
        """Support dot notation deletion: del tag.field"""
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'Tag' object has no attribute '{name}'")
    
    def to_go_dict(self) -> Dict[str, Any]:
        """
        Convert Tag to format expected by Go backend.
        
        Handles field name conversion from Python (snake_case/legacy names) 
        to Go (camelCase/Go struct field names).
        
        Returns:
            Dict suitable for JSON serialization to Go backend
        """
        go_dict = {}
        
        # Handle field name conversions
        field_mapping = {
            'start': 'startPos',           # start -> startPos  
            'end': 'endPos',               # end -> endPos
            'value': 'value',              # value -> value (no change)
            'uuid': 'uuid',                # uuid -> uuid (no change)
            'data': 'data',                # data -> data (no change)
            'confidence': 'confidence',    # confidence -> confidence (no change)
            'group_uuid': 'groupUuid',     # group_uuid -> groupUuid
            'parent_group_uuid': 'parentGroupUuid',  # parent_group_uuid -> parentGroupUuid
            'cell_index': 'cellIndex',     # cell_index -> cellIndex
            'index': 'index',              # index -> index (no change)
            'note': 'note',                # note -> note (no change)
            'status': 'status',            # status -> status (no change)
            'owner_uri': 'ownerUri',       # owner_uri -> ownerUri
            'is_dirty': 'isDirty'          # is_dirty -> isDirty
        }
        
        for python_key, go_key in field_mapping.items():
            if python_key in self and self[python_key] is not None:
                go_dict[go_key] = self[python_key]
        
        # Handle any additional fields not in mapping
        for key, value in self.items():
            if key not in field_mapping and value is not None:
                go_dict[key] = value
        
        return go_dict
    
    @classmethod
    def from_go_dict(cls, go_data: Dict[str, Any]) -> 'Tag':
        """
        Create Tag from Go backend data.
        
        Handles field name conversion from Go (camelCase) to Python (legacy names).
        
        Args:
            go_data: Dictionary from Go backend with Go field names
            
        Returns:
            Tag instance with legacy_python field names
        """
        if not go_data:
            return cls()
        
        # Handle field name conversions (reverse of to_go_dict)
        field_mapping = {
            'startPos': 'start',           # startPos -> start
            'endPos': 'end',               # endPos -> end
            'value': 'value',              # value -> value (no change)
            'uuid': 'uuid_val',            # uuid -> uuid_val (avoid conflict with uuid module)
            'data': 'data',                # data -> data (no change)
            'confidence': 'confidence',    # confidence -> confidence (no change)
            'groupUuid': 'group_uuid',     # groupUuid -> group_uuid
            'parentGroupUuid': 'parent_group_uuid',  # parentGroupUuid -> parent_group_uuid
            'cellIndex': 'cell_index',     # cellIndex -> cell_index
            'index': 'index',              # index -> index (no change)
            'note': 'note',                # note -> note (no change)
            'status': 'status',            # status -> status (no change)
            'ownerUri': 'owner_uri',       # ownerUri -> owner_uri
            'isDirty': 'is_dirty'          # isDirty -> is_dirty
        }
        
        # Convert field names
        python_data = {}
        for go_key, python_key in field_mapping.items():
            if go_key in go_data and go_data[go_key] is not None:
                python_data[python_key] = go_data[go_key]
        
        # Handle any additional fields not in mapping
        for key, value in go_data.items():
            if key not in field_mapping and value is not None:
                python_data[key] = value
        
        return cls(**python_data)
    
    def to_json(self) -> str:
        """Convert Tag to JSON string using Go field names."""
        return json.dumps(self.to_go_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Tag':
        """Create Tag from JSON string with Go field names."""
        go_data = json.loads(json_str)
        return cls.from_go_dict(go_data)
    
    def copy(self) -> 'Tag':
        """Create a copy of this Tag."""
        return Tag(**self)
    
    def __eq__(self, other) -> bool:
        """Support equality comparison with strings (for backward compatibility)."""
        if isinstance(other, str):
            # Allow comparison with tag name for backward compatibility
            return self.get('name', '') == other
        elif isinstance(other, Tag):
            # Tag-to-Tag comparison by UUID
            return self.get('uuid') == other.get('uuid')
        return False
    
    def __hash__(self) -> int:
        """Make Tag hashable based on UUID."""
        return hash(self.get('uuid', ''))
    
    def __repr__(self) -> str:
        """String representation of Tag."""
        fields = []
        for key in ['uuid', 'value', 'start', 'end', 'confidence']:
            if key in self and self[key] is not None:
                if key == 'uuid':
                    # Show abbreviated UUID
                    uuid_val = self[key]
                    if len(uuid_val) > 8:
                        uuid_val = uuid_val[:8] + '...'
                    fields.append(f"{key}='{uuid_val}'")
                elif isinstance(self[key], str):
                    fields.append(f"{key}='{self[key]}'")
                else:
                    fields.append(f"{key}={self[key]}")
        
        return f"Tag({', '.join(fields)})"