"""
ContentNode class with C bindings to Go implementation.
"""

import json
import weakref
from typing import Optional, Any, Dict, List, Union
from .._native import lib, ffi
from ..errors import check_error
from .content_feature import ContentFeature
from .tag import Tag
from .enums import Traverse


class ContentNode:
    """
    ContentNode represents a node in the document tree.
    
    This class provides a Python interface to the Go ContentNode implementation,
    using C bindings for communication.
    """
    
    def __init__(self, handle=None, document=None, node_type: Optional[str] = None, 
                 content: Optional[str] = None, index: Optional[int] = None):
        """
        Initialize a ContentNode.
        
        Args:
            handle: Internal handle for existing nodes (do not use directly)
            document: Parent document for creating new nodes
            node_type: Type of node (e.g., 'paragraph', 'line', 'word')
            content: Text content of the node
            index: Optional index for ordering
        """
        self._handle = handle
        self._document = document
        self._closed = False
        
        # If no handle provided but we have document and node_type, create new node
        if handle is None and document is not None and node_type is not None:
            # Create through document
            content_bytes = (content or "").encode('utf-8') if content is not None else b""
            node_type_bytes = node_type.encode('utf-8')
            
            # Use CreateContentNode with index parameter
            index_val = index if index is not None else -1
            handle = lib.CreateContentNode(
                document._handle,
                node_type_bytes,
                content_bytes,
                index_val
            )
            check_error()
            
            if handle == 0:
                raise RuntimeError("Failed to create content node")
            
            self._handle = handle
            
        # Set up finalizer for cleanup
        if self._handle:
            self._finalizer = weakref.finalize(self, self._cleanup_handle, self._handle)
    
    @staticmethod
    def _cleanup_handle(handle):
        """Clean up a handle when object is garbage collected."""
        if handle and handle != 0:
            try:
                lib.FreeHandle(handle)
            except:
                pass  # Ignore errors during cleanup
    
    @classmethod
    def _from_handle(cls, handle):
        """Create a ContentNode instance from an existing handle."""
        if handle == 0:
            return None
        
        # Create wrapper instance without going through __init__
        node = cls.__new__(cls)
        node._handle = handle
        node._document = None  # Will be set by caller if needed
        node._closed = False
        node._finalizer = weakref.finalize(node, cls._cleanup_handle, handle)
        return node
    
    def _check_not_closed(self):
        """Check that the node hasn't been closed."""
        if self._closed:
            raise ValueError("ContentNode has been closed")
        if not self._handle:
            raise ValueError("ContentNode has no handle")

    @property
    def document(self):
        """
        Get the document this node belongs to (legacy_python parity).

        Returns:
            The Document instance, or None if not set.
        """
        return self._document

    @property
    def node_type(self) -> str:
        """Get the node type."""
        self._check_not_closed()
        result = lib.GetNodeType(self._handle)
        check_error()
        if result == ffi.NULL:
            return ""
        try:
            return ffi.string(result).decode('utf-8')
        finally:
            lib.FreeString(result)
    
    @node_type.setter
    def node_type(self, value: str):
        """Set the node type (legacy_python compatibility)."""
        self.set_node_type(value)
    
    
    @property
    def content(self) -> str:
        """Get the node content."""
        self._check_not_closed()
        result = lib.GetNodeContent(self._handle)
        check_error()
        if result == ffi.NULL:
            return ""
        try:
            return ffi.string(result).decode('utf-8')
        finally:
            lib.FreeString(result)
    
    @content.setter
    def content(self, value: str):
        """Set the node content."""
        self._check_not_closed()
        content_bytes = value.encode('utf-8') if value else b""
        success = lib.SetNodeContent(self._handle, content_bytes)
        check_error()
        if not success:
            raise RuntimeError("Failed to set node content")
    
    @property
    def index(self) -> Optional[int]:
        """Get the node index."""
        self._check_not_closed()
        idx = lib.GetNodeIndex(self._handle)
        check_error()
        return idx if idx >= 0 else None
    
    @index.setter
    def index(self, value: Optional[int]):
        """Set the node index."""
        self._check_not_closed()
        idx_val = value if value is not None else -1
        success = lib.SetNodeIndex(self._handle, idx_val)
        check_error()
        if not success:
            raise RuntimeError("Failed to set node index")
    
    @property
    def id(self) -> int:
        """Get the node database ID."""
        self._check_not_closed()
        node_id = lib.GetNodeID(self._handle)
        check_error()
        return node_id
    
    @property
    def uuid(self) -> str:
        """Get the node UUID."""
        self._check_not_closed()
        result = lib.GetNodeUUID(self._handle)
        check_error()
        if result == ffi.NULL:
            return ""
        try:
            return ffi.string(result).decode('utf-8')
        finally:
            lib.FreeString(result)
    
    @property
    def virtual(self) -> bool:
        """Check if the node is virtual."""
        self._check_not_closed()
        is_virtual = lib.IsNodeVirtual(self._handle)
        check_error()
        return bool(is_virtual)
    
    @virtual.setter
    def virtual(self, value: bool):
        """Set the virtual flag (legacy_python compatibility)."""
        self.set_virtual(value)
    
    
    # Tree Navigation Methods
    
    def get_parent(self):
        """Get the parent node."""
        self._check_not_closed()
        parent_handle = lib.GetNodeParent(self._handle)
        check_error()
        
        if parent_handle == 0:
            return None
        
        return ContentNode(handle=parent_handle, document=self._document)
    
    def get_children(self):
        """Get all child nodes."""
        # Return cached children for deleted nodes (legacy SDK compatibility)
        # Legacy SDK caches children during remove_content_node and returns them after deletion
        if getattr(self, '_deleted', False):
            if hasattr(self, '_deleted_cache') and 'children' in self._deleted_cache:
                return self._deleted_cache['children']
            return []
        self._check_not_closed()
        count_ptr = ffi.new("int*")
        handles_ptr = lib.GetNodeChildren(self._handle, count_ptr)
        check_error()
        
        count = count_ptr[0]
        if count == 0 or handles_ptr == ffi.NULL:
            return []
        
        try:
            # Convert C array to Python list
            children = []
            handles = ffi.cast("unsigned long long*", handles_ptr)
            for i in range(count):
                child_handle = handles[i]
                children.append(ContentNode(handle=child_handle, document=self._document))
            return children
        finally:
            # Free the allocated array
            lib.FreeHandleArray(handles_ptr)
    
    def add_child(self, child, index=None):
        """
        Add a child node.

        Args:
            child: ContentNode to add as child
            index: Optional position to insert at
        """
        self._check_not_closed()
        if not hasattr(child, '_handle'):
            raise ValueError("Invalid ContentNode object")

        # Legacy SDK compatibility: if child was deleted, recreate it from cached data
        # Legacy SDK re-inserts deleted nodes when adding them to a new parent
        if getattr(child, '_deleted', False) and hasattr(child, '_deleted_cache'):
            child = self._recreate_deleted_node(child)

        index_val = index if index is not None else -1
        success = lib.AddNodeChild(self._handle, child._handle, index_val)
        check_error()
        if not success:
            raise RuntimeError("Failed to add child node")

    def reparent(self, new_parent, index=-1):
        """
        Move this node to a new parent without deleting it.

        This is more efficient than remove_child + add_child when reorganizing
        the tree, as it just updates the parent_id rather than deleting and
        recreating nodes. This preserves node IDs and works correctly with
        preloaded caches.

        Args:
            new_parent: New parent ContentNode, or None to make this an orphan
            index: Position among siblings (-1 to append)
        """
        self._check_not_closed()

        # Get new parent handle (0 for orphan)
        new_parent_handle = 0
        if new_parent is not None:
            if not hasattr(new_parent, '_handle'):
                raise ValueError("Invalid new_parent ContentNode object")
            new_parent_handle = new_parent._handle

        success = lib.ReparentNode(self._handle, new_parent_handle, index)
        check_error()
        if not success:
            raise RuntimeError("Failed to reparent node")

    def _recreate_deleted_node(self, deleted_node):
        """Recreate a deleted node from its cached data (legacy SDK compatibility)."""
        cache = deleted_node._deleted_cache

        # Create new node with cached data
        node_type = cache.get('node_type', 'unknown')
        content = cache.get('content', '')
        idx = cache.get('index', 0)

        # Create the node through the document
        new_node = self._document.create_node(node_type=node_type, content=content)
        if idx is not None:
            new_node.index = idx

        # Restore bbox if available
        bbox = cache.get('bbox')
        if bbox:
            new_node.set_bbox(bbox)

        # Recursively recreate children
        cached_children = cache.get('children', [])
        for cached_child in cached_children:
            if getattr(cached_child, '_deleted', False) and hasattr(cached_child, '_deleted_cache'):
                recreated_child = self._recreate_deleted_node(cached_child)
                new_node.add_child(recreated_child)

        # Transfer handle ownership from new_node to deleted_node
        # IMPORTANT: Detach new_node's finalizer so it doesn't free the handle
        # when new_node goes out of scope
        if hasattr(new_node, '_finalizer'):
            new_node._finalizer.detach()

        # Update the original deleted_node with the new handle
        deleted_node._handle = new_node._handle
        deleted_node._deleted = False
        deleted_node._closed = False

        # Set up finalizer on deleted_node for the new handle
        deleted_node._finalizer = weakref.finalize(
            deleted_node, self._cleanup_handle, deleted_node._handle
        )

        return deleted_node
    
    def remove_child(self, child):
        """
        Remove a child node (deletes the node from the document).

        Note: For legacy SDK compatibility, this just deletes the child node
        without validating that it's actually a child of this node.
        The child node's data is cached before deletion so it can still be
        accessed after removal (matching legacy SDK behavior).

        Args:
            child: ContentNode to remove
        """
        self._check_not_closed()
        if not hasattr(child, '_handle'):
            raise ValueError("Invalid ContentNode object")

        # Already deleted - no-op (legacy SDK compatibility)
        if getattr(child, '_deleted', False) or child._handle == 0:
            return

        # Recursively cache all node data before deletion (legacy SDK kept data in Python memory)
        # Legacy SDK's remove_content_node calls get_children() recursively to gather all child IDs,
        # which populates the cache. We replicate this by caching the entire subtree.
        self._cache_node_recursive(child)

        # Legacy SDK behavior: remove_child just deletes the node without
        # validating parent-child relationship. Use DeleteContentNode directly.
        success = lib.DeleteContentNode(child._handle)
        check_error()
        if not success:
            raise RuntimeError("Failed to remove child node")

        # Mark entire subtree as deleted so getters return cached data
        self._mark_deleted_recursive(child)

    def _cache_node_recursive(self, node):
        """Recursively cache node data before deletion (matches legacy SDK behavior)."""
        if getattr(node, '_deleted', False) or hasattr(node, '_deleted_cache'):
            return

        try:
            # Get children BEFORE caching - this populates the children list
            children = node.get_children()

            # Cache this node's data
            node._deleted_cache = {
                'content': node.content,
                'node_type': node.node_type,
                'uuid': node.uuid,
                'index': node.index,
                'bbox': node.get_bbox() if hasattr(node, 'get_bbox') else None,
                'children': children,
            }

            # Recursively cache all descendants
            for child in children:
                self._cache_node_recursive(child)
        except:
            node._deleted_cache = {}

    def _mark_deleted_recursive(self, node):
        """Mark node and all descendants as deleted."""
        node._handle = 0
        node._deleted = True

        # Mark cached children as deleted
        if hasattr(node, '_deleted_cache') and 'children' in node._deleted_cache:
            for child in node._deleted_cache['children']:
                self._mark_deleted_recursive(child)
    
    def get_child(self, index):
        """
        Get child at specific index.
        
        Args:
            index: Index of child to get
            
        Returns:
            ContentNode or None if index out of bounds
        """
        self._check_not_closed()
        child_handle = lib.GetNodeChild(self._handle, index)
        # Don't check error - out of bounds returns 0 without error
        
        if child_handle == 0:
            return None
        
        return ContentNode(handle=child_handle, document=self._document)
    
    @property
    def child_count(self):
        """Get the number of child nodes."""
        self._check_not_closed()
        count = lib.GetNodeChildCount(self._handle)
        check_error()
        return count if count >= 0 else 0
    
    # Sibling Navigation Methods

    def next_node(
        self,
        node_type_re: str = ".*",
        skip_virtual: bool = False,
        has_no_content: bool = True,
        traverse: Union[Traverse, int] = Traverse.SIBLING,
    ) -> Optional["ContentNode"]:
        """Get the next sibling node.

        Args:
            node_type_re: Regular expression to match node types (default: ".*")
            skip_virtual: Skip virtual nodes (default: False)
            has_no_content: Allow nodes with no content (default: True)
            traverse: Traversal mode - Traverse.SIBLING, CHILDREN, PARENT, or ALL
                     (default: Traverse.SIBLING)

        Returns:
            The next node matching criteria, or None if not found
        """
        self._check_not_closed()

        # Convert traverse to int if it's an enum
        traverse_val = traverse.value if isinstance(traverse, Traverse) else int(traverse)

        # Encode node_type_re for C
        node_type_bytes = node_type_re.encode('utf-8') if node_type_re else b".*"

        next_handle = lib.GetNextNode(
            self._handle,
            node_type_bytes,
            int(skip_virtual),
            int(has_no_content),
            traverse_val
        )
        check_error()

        if next_handle == 0:
            return None

        return ContentNode(handle=next_handle, document=self._document)

    def previous_node(
        self,
        node_type_re: str = ".*",
        skip_virtual: bool = False,
        has_no_content: bool = False,
        traverse: Union[Traverse, int] = Traverse.SIBLING,
    ) -> Optional["ContentNode"]:
        """Get the previous sibling node.

        Args:
            node_type_re: Regular expression to match node types (default: ".*")
            skip_virtual: Skip virtual nodes (default: False)
            has_no_content: Allow nodes with no content (default: False)
            traverse: Traversal mode - Traverse.SIBLING, CHILDREN, PARENT, or ALL
                     (default: Traverse.SIBLING)

        Returns:
            The previous node matching criteria, or None if not found
        """
        self._check_not_closed()

        # Convert traverse to int if it's an enum
        traverse_val = traverse.value if isinstance(traverse, Traverse) else int(traverse)

        # Encode node_type_re for C
        node_type_bytes = node_type_re.encode('utf-8') if node_type_re else b".*"

        prev_handle = lib.GetPreviousNode(
            self._handle,
            node_type_bytes,
            int(skip_virtual),
            int(has_no_content),
            traverse_val
        )
        check_error()

        if prev_handle == 0:
            return None

        return ContentNode(handle=prev_handle, document=self._document)
    
    def get_siblings(self):
        """Get all sibling nodes (excludes this node)."""
        self._check_not_closed()
        count_ptr = ffi.new("int*")
        handles_ptr = lib.GetNodeSiblings(self._handle, count_ptr)
        check_error()
        
        count = count_ptr[0]
        if count == 0 or handles_ptr == ffi.NULL:
            return []
        
        try:
            # Convert C array to Python list
            siblings = []
            handles = ffi.cast("unsigned long long*", handles_ptr)
            for i in range(count):
                sibling_handle = handles[i]
                siblings.append(ContentNode(handle=sibling_handle, document=self._document))
            return siblings
        finally:
            # Free the allocated array
            if handles_ptr != ffi.NULL:
                lib.FreeHandleArray(handles_ptr)
    
    def get_path(self):
        """Get the path from root to this node as a list of nodes."""
        self._check_not_closed()
        count_ptr = ffi.new("int*")
        handles_ptr = lib.GetNodePath(self._handle, count_ptr)
        check_error()
        
        count = count_ptr[0]
        if count == 0 or handles_ptr == ffi.NULL:
            return []
        
        try:
            # Convert C array to Python list
            path = []
            handles = ffi.cast("unsigned long long*", handles_ptr)
            for i in range(count):
                node_handle = handles[i]
                path.append(ContentNode(handle=node_handle, document=self._document))
            return path
        finally:
            # Free the allocated array
            if handles_ptr != ffi.NULL:
                lib.FreeHandleArray(handles_ptr)
    
    def get_all_content(self, separator: str = ' ', strip: bool = False):
        """
        Get all text content from this node and its descendants.
        
        Args:
            separator: String to use to join content (default: ' ')
            strip: Whether to strip whitespace from each piece of content
            
        Returns:
            Combined text content
        """
        self._check_not_closed()
        
        # Convert separator to bytes
        separator_bytes = separator.encode('utf-8') if separator else None
        
        # Call C function
        content_ptr = lib.GetNodeAllContent(
            self._handle,
            separator_bytes if separator_bytes else ffi.NULL,
            1 if strip else 0
        )
        check_error()
        
        if content_ptr == ffi.NULL:
            return ""
        
        try:
            return ffi.string(content_ptr).decode('utf-8')
        finally:
            lib.FreeString(content_ptr)
    
    # Feature Management Methods
    
    def add_feature(self, feature_type: str, name: str, value: Any, single: bool = True, serialized: bool = False) -> Optional[ContentFeature]:
        """
        Add a feature to the node. If a feature with same type:name exists, appends the value.
        
        Args:
            feature_type: Type of feature
            name: Name of the feature
            value: Value of the feature (will be JSON serialized unless serialized=True)
            single: If True and serialized=False, wraps scalar values in an array
            serialized: If True, stores value exactly as provided without wrapping
            
        Returns:
            ContentFeature: The feature that was added to this ContentNode
        """
        self._check_not_closed()
        
        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')
        value_json = json.dumps(value).encode('utf-8')
        
        result = lib.AddNodeFeature(
            self._handle,
            feature_type_bytes,
            name_bytes,
            value_json,
            1 if single else 0,
            1 if serialized else 0
        )
        check_error()
        
        if result == ffi.NULL:
            raise RuntimeError(f"Failed to add feature {feature_type}:{name}")
        
        # Parse the returned JSON to create ContentFeature
        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)  # Free the C string
        
        # Parse the JSON and create ContentFeature instance
        feature_data = json.loads(json_str)
        created_feature = ContentFeature.from_dict(feature_data)
        return created_feature
    
    def set_feature(self, feature_type: str, name: str, value: Any):
        """
        Set a feature on the node, replacing any existing feature with same type:name.
        This is equivalent to remove_feature then add_feature.
        
        Args:
            feature_type: Type of feature
            name: Name of the feature
            value: Value of the feature (will be JSON serialized)
        """
        self._check_not_closed()
        
        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')
        value_json = json.dumps(value).encode('utf-8')
        
        success = lib.SetNodeFeature(
            self._handle,
            feature_type_bytes,
            name_bytes,
            value_json
        )
        check_error()
        
        if not success:
            raise RuntimeError(f"Failed to set feature {feature_type}:{name}")
    
    def get_feature(self, feature_type: str, name: str) -> Optional[ContentFeature]:
        """
        Get a specific feature by type and name.
        
        Args:
            feature_type: Type of feature
            name: Name of the feature
            
        Returns:
            ContentFeature object or None if not found
        """
        self._check_not_closed()
        
        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')
        
        result = lib.GetNodeFeature(self._handle, feature_type_bytes, name_bytes)
        check_error()
        
        if result == ffi.NULL:
            return None
        
        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)
        
        if not json_str or json_str == "null":
            return None
        
        # Parse the JSON and create ContentFeature instance
        feature_data = json.loads(json_str)
        return ContentFeature.from_dict(feature_data)
    
    def get_features(self) -> List[ContentFeature]:
        """
        Get all features on this node.
        
        Returns:
            List of ContentFeature objects on this node
        """
        self._check_not_closed()
        
        result = lib.GetAllNodeFeatures(self._handle)
        check_error()
        
        if result == ffi.NULL:
            return []
        
        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)
        
        if not json_str or json_str == "{}" or json_str == "[]":
            return []
        
        # Parse JSON response from Go - could be dict or list format
        try:
            data = json.loads(json_str)
            features = []
            
            if isinstance(data, dict):
                # If grouped by type, flatten to list of features
                for feature_type, type_features in data.items():
                    if isinstance(type_features, list):
                        for feature_dict in type_features:
                            features.append(ContentFeature.from_dict(feature_dict))
                    elif isinstance(type_features, dict):
                        features.append(ContentFeature.from_dict(type_features))
            elif isinstance(data, list):
                # If already a list of features
                for feature_dict in data:
                    features.append(ContentFeature.from_dict(feature_dict))
            
            return features
        except (json.JSONDecodeError, AttributeError):
            return []
    
    def get_features_of_type(self, feature_type: str) -> List[ContentFeature]:
        """
        Get all features of a specific type.
        
        Args:
            feature_type: Type of features to get
            
        Returns:
            List of ContentFeature objects of the specified type
        """
        self._check_not_closed()
        
        feature_type_bytes = feature_type.encode('utf-8')
        
        result = lib.GetNodeFeaturesOfType(self._handle, feature_type_bytes)
        check_error()
        
        if result == ffi.NULL:
            return []
        
        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)
        
        if not json_str or json_str == "[]":
            return []
        
        # Parse JSON and convert to ContentFeature instances
        try:
            feature_dicts = json.loads(json_str)
            if isinstance(feature_dicts, list):
                result_features = []
                for feature_dict in feature_dicts:
                    try:
                        cf = ContentFeature.from_dict(feature_dict)
                        result_features.append(cf)
                    except Exception:
                        pass  # Skip features that can't be parsed
                return result_features
            elif isinstance(feature_dicts, dict):
                # Single feature returned as dict instead of list
                return [ContentFeature.from_dict(feature_dicts)]
            else:
                return []
        except (json.JSONDecodeError, AttributeError):
            return []
    
    def remove_feature(self, feature_type: str, name: str, include_children: bool = False):
        """
        Remove a feature from the node.

        Args:
            feature_type: Type of feature to remove
            name: Name of the feature to remove
            include_children: If True, also remove the feature from all child nodes recursively
        """
        self._check_not_closed()

        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')

        success = lib.RemoveNodeFeature(self._handle, feature_type_bytes, name_bytes)
        check_error()

        if not success:
            raise RuntimeError(f"Failed to remove feature {feature_type}:{name}")

        # Recursively remove from children if requested
        if include_children:
            for child in self.get_children():
                child.remove_feature(feature_type, name, include_children=True)
    
    def get_feature_value(self, feature_type: str, name: str) -> Any:
        """
        Get the first value of a specific feature.
        This matches legacy_python's get_feature_value which returns feature.value[0].

        Args:
            feature_type: Type of feature
            name: Name of the feature

        Returns:
            First feature value or None if not found
        """
        self._check_not_closed()

        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')

        result = lib.GetNodeFeatureValue(self._handle, feature_type_bytes, name_bytes)
        check_error()

        if result == ffi.NULL:
            return None

        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)

        if not json_str or json_str == "null":
            return None

        value = json.loads(json_str)
        # Legacy behavior: return first element if it's a list
        if isinstance(value, list) and len(value) > 0:
            return value[0]
        return value

    def get_feature_values(self, feature_type: str, name: str) -> Optional[List[Any]]:
        """
        Get all values of a specific feature as a list.
        This matches legacy_python's get_feature_values behavior.

        Args:
            feature_type: Type of feature
            name: Name of the feature

        Returns:
            List of feature values or None if not found
        """
        self._check_not_closed()

        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')

        result = lib.GetNodeFeatureValue(self._handle, feature_type_bytes, name_bytes)
        check_error()

        if result == ffi.NULL:
            return None

        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)

        if not json_str or json_str == "null":
            return None

        value = json.loads(json_str)
        # Ensure we always return a list
        if isinstance(value, list):
            return value
        return [value]

    def has_feature(self, feature_type: str, name: str) -> bool:
        """
        Check if the node has a specific feature.
        
        Args:
            feature_type: Type of feature
            name: Name of the feature
            
        Returns:
            True if the feature exists, False otherwise
        """
        self._check_not_closed()
        
        feature_type_bytes = feature_type.encode('utf-8')
        name_bytes = name.encode('utf-8')
        
        has_feat = lib.HasNodeFeature(self._handle, feature_type_bytes, name_bytes)
        check_error()
        
        return bool(has_feat)
    
    # Tagging System Methods
    
    def tag(self, tag_to_apply: str, **options) -> None:
        """
        Tag this node with the specified tag name and options.

        Args:
            tag_to_apply: Name/path of the tag (e.g., 'important', 'section/header')
            **options: Tag options including:
                - content_re: Regular expression for content matching
                - tag_uuid: UUID for the tag
                - confidence: Confidence score (0.0-1.0)
                - value: Value associated with the tag
                - fixed_position: Whether position is fixed
                - group_uuid: UUID for grouping tags
                - cell_index: Cell index for the tag
                - group_uuid: Group UUID for the tag
                - parent_group_uuid: Parent group UUID for the tag
                - owner_uri: URI of the entity that created the tag
        """
        self._check_not_closed()

        tag_name_bytes = tag_to_apply.encode('utf-8')

        # Convert options to JSON
        if options:
            options_json = json.dumps(options).encode('utf-8')
        else:
            options_json = ffi.NULL

        success = lib.TagNode(self._handle, tag_name_bytes, options_json)
        check_error()

        if not success:
            raise RuntimeError(f"Failed to tag node with '{tag_to_apply}'")
    
    def get_tags(self) -> List[Tag]:
        """
        Get all tags on this node as Tag objects.
        
        Returns:
            List of Tag objects (matches legacy_python behavior)
        """
        self._check_not_closed()
        
        result = lib.GetNodeTags(self._handle)
        check_error()
        
        if result == ffi.NULL:
            return []
        
        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)
        
        if not json_str or json_str == "[]":
            return []
        
        # Parse the tag data and convert to Tag objects
        try:
            tag_dicts = json.loads(json_str)
            if isinstance(tag_dicts, list):
                return [Tag.from_go_dict(tag_dict) for tag_dict in tag_dicts]
            else:
                return []
        except (json.JSONDecodeError, AttributeError):
            return []
    
    def get_tag_names(self) -> List[str]:
        """
        Get all tag names on this node as strings.
        
        Returns:
            List of tag names (for backward compatibility)
        """
        tags = self.get_tags()
        return [getattr(tag, 'name', '') for tag in tags if hasattr(tag, 'name')]
    
    def get_tag_features(self) -> List[ContentFeature]:
        """
        Get all tag features on this node as ContentFeature objects.
        
        Returns:
            List of ContentFeature objects where feature_type="tag" (matches legacy_python behavior)
        """
        return self.get_features_of_type("tag")
    
    def get_tag(self, tag_name: str, tag_uuid: Optional[str] = None) -> Optional[Tag]:
        """
        Get a specific tag by name, optionally filtered by UUID.

        Args:
            tag_name: Name of the tag to get
            tag_uuid: Optional UUID to filter by - if specified, only return
                     the tag if its UUID matches

        Returns:
            Tag object or None if not found (or UUID doesn't match)
        """
        self._check_not_closed()

        # Convert to string if not already
        if tag_name is None:
            return None
        if not isinstance(tag_name, str):
            tag_name = str(tag_name)

        tag_name_bytes = tag_name.encode('utf-8')

        result = lib.GetNodeTag(self._handle, tag_name_bytes)
        check_error()

        if result == ffi.NULL:
            return None

        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)

        if not json_str or json_str == "{}":
            return None

        # Parse JSON and convert to Tag object
        try:
            tag_dict = json.loads(json_str)
            tag_obj = Tag.from_go_dict(tag_dict)

            # Filter by UUID if specified (legacy SDK compatibility)
            if tag_uuid is not None:
                tag_obj_uuid = getattr(tag_obj, 'uuid', None)
                if tag_obj_uuid != tag_uuid:
                    return None

            return tag_obj
        except (json.JSONDecodeError, AttributeError):
            return None
    
    def remove_tag(self, tag_name: str):
        """
        Remove a tag from this node.
        
        Args:
            tag_name: Name of the tag to remove
        """
        self._check_not_closed()
        
        tag_name_bytes = tag_name.encode('utf-8')
        
        success = lib.RemoveNodeTag(self._handle, tag_name_bytes)
        check_error()

        if not success:
            raise RuntimeError(f"Failed to remove tag '{tag_name}'")

    def update_tag(self, tag_name: str, value: Any) -> None:
        """
        Update an existing tag's value in place.

        This is more efficient than remove_feature + add_feature for updating
        existing tags, as it performs a single UPDATE operation instead of
        DELETE + INSERT.

        Args:
            tag_name: Name of the tag to update
            value: New value for the tag (will be JSON serialized)
        """
        self._check_not_closed()

        tag_name_bytes = tag_name.encode('utf-8')
        value_json = json.dumps(value).encode('utf-8')

        success = lib.UpdateNodeTag(self._handle, tag_name_bytes, value_json)
        check_error()

        if not success:
            raise RuntimeError(f"Failed to update tag '{tag_name}'")

    def has_tag(self, tag_name: str, include_children: bool = False) -> bool:
        """
        Check if this node has a specific tag.

        Args:
            tag_name: Name of the tag to check
            include_children: If True, also check child nodes recursively

        Returns:
            True if the node (or any child if include_children=True) has the tag, False otherwise
        """
        self._check_not_closed()

        tag_name_bytes = tag_name.encode('utf-8')

        has_tag_result = lib.HasNodeTag(self._handle, tag_name_bytes)
        check_error()

        if bool(has_tag_result):
            return True

        # Check children if requested
        if include_children:
            for child in self.get_children():
                if child.has_tag(tag_name, include_children=True):
                    return True

        return False
    
    def has_tags(self) -> bool:
        """
        Check if this node has any tags.
        
        Returns:
            True if the node has at least one tag, False otherwise
        """
        return len(self.get_tags()) > 0
    
    def add_tag(self, tag: Dict[str, Any]):
        """
        Add a tag object to the node.
        
        Args:
            tag: Dictionary containing tag data with 'name' (required) and optional
                 'value', 'confidence', 'group_uuid' fields
        
        Example:
            node.add_tag({
                'name': 'important',
                'value': 'high_priority',
                'confidence': 0.95,
                'group_uuid': 'some-uuid'
            })
        """
        self._check_not_closed()
        
        # Validate required field
        if not isinstance(tag, dict) or 'name' not in tag:
            raise ValueError("Tag must be a dictionary with required 'name' field")
        
        # Convert to JSON
        tag_json = json.dumps(tag).encode('utf-8')
        
        # Call C function
        result = lib.AddTag(self._handle, tag_json)
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to add tag")
    
    def delete(self):
        """
        Delete this node from its parent.
        
        Note: This follows the legacy_python pattern where a node is removed
        from its parent via parent.remove_child(node).
        """
        self._check_not_closed()
        
        # Call C function which handles the parent.remove_child logic
        result = lib.DeleteContentNode(self._handle)
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to delete content node")
        
        # Mark as closed since it's deleted
        self._closed = True
        if hasattr(self, '_finalizer'):
            self._finalizer.detach()
    
    
    
    # Note: node_type and virtual properties already exist in this class
    # We just need to add setters to make them compatible with legacy_python style
    
    def select(self, selector: str, variables: Optional[Dict[str, Any]] = None, first_only: bool = False):
        """
        Execute selector query on this node and return matching nodes.

        Args:
            selector: XPath-like selector string
            variables: Optional variables for parameterized queries
            first_only: If True, only return the first matching node (as a list with one element)

        Returns:
            List of ContentNode objects matching the selector
        """
        self._check_not_closed()

        # Optimization: use select_first when first_only is True (legacy SDK compatibility)
        if first_only:
            result = self.select_first(selector, variables)
            return [result] if result is not None else []

        # Convert parameters to C types
        selector_bytes = selector.encode('utf-8')
        variables_json = ffi.NULL
        if variables:
            variables_json = json.dumps(variables).encode('utf-8')

        # Call C function
        count_ptr = ffi.new("int*")
        handles_ptr = lib.SelectNodes(self._handle, selector_bytes, variables_json, count_ptr)
        check_error()

        if handles_ptr == ffi.NULL or count_ptr[0] == 0:
            return []

        # Convert handles to ContentNode objects
        nodes = []
        for i in range(count_ptr[0]):
            handle = handles_ptr[i]
            if handle != 0:
                node = ContentNode._from_handle(handle)
                node._document = self._document  # Preserve document reference
                nodes.append(node)

        # Free the handle array
        lib.FreeHandleArray(handles_ptr)

        return nodes

    def select_first(self, selector: str, variables: Optional[Dict[str, Any]] = None):
        """
        Execute selector query on this node and return the first matching node.
        
        Args:
            selector: XPath-like selector string
            variables: Optional variables for parameterized queries
            
        Returns:
            First ContentNode matching the selector, or None if no match
        """
        self._check_not_closed()
        
        # Convert parameters to C types
        selector_bytes = selector.encode('utf-8')
        variables_json = ffi.NULL
        if variables:
            variables_json = json.dumps(variables).encode('utf-8')
        
        # Call C function
        handle = lib.SelectSingleNode(self._handle, selector_bytes, variables_json)
        check_error()

        if handle == 0:
            return None

        # Convert handle to ContentNode object
        node = ContentNode._from_handle(handle)
        node._document = self._document  # Preserve document reference
        return node

    def set_node_type(self, node_type: str):
        """
        Set the type of this node.
        
        Args:
            node_type: New type for the node (e.g., 'paragraph', 'line', 'word')
        """
        self._check_not_closed()
        
        # Call C function
        node_type_bytes = node_type.encode('utf-8')
        result = lib.SetNodeType(self._handle, node_type_bytes)
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to set node type")
    
    def set_virtual(self, virtual: bool):
        """
        Set the virtual flag of this node.
        
        Args:
            virtual: True to mark node as virtual, False otherwise
        """
        self._check_not_closed()
        
        # Call C function
        virtual_int = 1 if virtual else 0
        result = lib.SetNodeVirtual(self._handle, virtual_int)
        check_error()
        
        if result != 1:
            raise RuntimeError("Failed to set node virtual flag")
    
    def close(self):
        """Close the node and free its resources."""
        if not self._closed and self._handle:
            lib.FreeHandle(self._handle)
            self._handle = None
            self._closed = True
            if hasattr(self, '_finalizer'):
                self._finalizer.detach()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
    
    def __repr__(self):
        """String representation."""
        if self._closed:
            return "ContentNode(closed)"
        
        try:
            content_preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
            return f"ContentNode(type='{self.node_type}', content='{content_preview}', id={self.id})"
        except:
            return f"ContentNode(handle={self._handle})"
    
    def __str__(self):
        """String conversion."""
        if self._closed:
            return "[Closed ContentNode]"
        
        try:
            return f"{self.node_type}: {self.content}"
        except:
            return "[ContentNode]"

    def __eq__(self, other):
        """Check equality by UUID."""
        if not isinstance(other, ContentNode):
            return False
        if self._closed or other._closed:
            return False
        try:
            return self.uuid == other.uuid
        except:
            return False

    def __hash__(self):
        """Hash by UUID for use in sets and dicts."""
        if self._closed:
            return hash(None)
        try:
            return hash(self.uuid)
        except:
            return hash(self._handle)

    def matches(self, pattern: str) -> bool:
        """
        Check if this node matches a selector pattern.
        
        This is equivalent to checking if select_first(pattern) returns this node,
        but may be more efficient for simple pattern matching.
        
        Args:
            pattern: Selector pattern to match against
            
        Returns:
            True if the node matches the pattern, False otherwise
            
        Raises:
            DocumentError: If the pattern is invalid or node is closed
        """
        if self._closed:
            raise DocumentError("Cannot check pattern on closed node")
        
        if not pattern:
            return False
            
        try:
            # Use the parent's select to see if this node is found
            # This is a simple implementation - could be optimized in the future
            if hasattr(self, '_document') and self._document:
                # Try to find this node using the pattern from the document root
                result = self._document.select_first(pattern)
                return result is not None and result.id == self.id
            else:
                # If no document reference, try pattern matching from this node's parent
                parent = self.get_parent()
                if parent:
                    result = parent.select_first(pattern)
                    return result is not None and result.id == self.id
                else:
                    # No parent, try from this node itself
                    result = self.select_first(pattern)
                    return result is not None and result.id == self.id
                    
        except Exception as e:
            from ..errors import DocumentError
            raise DocumentError(f"Pattern matching failed: {e}")
    
    def get_bbox(self) -> Optional[List[float]]:
        """
        Get the bounding box for the node.

        Returns:
            The bounding box array [x1, y1, x2, y2] if it exists, None otherwise
        """
        # Return cached bbox if node was deleted (legacy SDK compatibility)
        if getattr(self, '_deleted', False) and hasattr(self, '_deleted_cache'):
            return self._deleted_cache.get('bbox')

        bbox = self.get_feature_value("spatial", "bbox")
        if not bbox or not isinstance(bbox, (list, tuple)):
            return None

        # Feature values are stored as arrays - unwrap if needed
        # Format is [[x1, y1, x2, y2]] so we need to get the inner array
        if len(bbox) == 1 and isinstance(bbox[0], (list, tuple)):
            bbox = bbox[0]

        if len(bbox) >= 4:
            # Ensure all values are floats
            return [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])]
        return None
    
    def set_bbox(self, bbox: List[float]):
        """
        Set the bounding box for the node.
        
        Args:
            bbox: The bounding box array [x1, y1, x2, y2]
        """
        if not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
            raise ValueError("Bounding box must be a list/tuple of 4 values [x1, y1, x2, y2]")
        
        # Convert to floats to ensure consistent storage
        bbox_floats = [float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])]
        
        # Use set_feature which calls the C binding to save to Go
        self.set_feature("spatial", "bbox", bbox_floats)
    
    def get_x(self) -> Optional[float]:
        """
        Get the X position (left edge) of the node's bounding box.

        Returns:
            The X coordinate (x1) if bbox exists, None otherwise
        """
        bbox = self.get_bbox()
        if bbox:
            return bbox[0]
        return None

    def get_y(self) -> Optional[float]:
        """
        Get the Y position (top edge) of the node's bounding box.

        Returns:
            The Y coordinate (y1) if bbox exists, None otherwise
        """
        bbox = self.get_bbox()
        if bbox:
            return bbox[1]
        return None

    def get_width(self) -> Optional[float]:
        """
        Get the width of the node's bounding box.

        Returns:
            The width (x2 - x1) if bbox exists, None otherwise
        """
        bbox = self.get_bbox()
        if bbox:
            return bbox[2] - bbox[0]
        return None

    def get_height(self) -> Optional[float]:
        """
        Get the height of the node's bounding box.

        Returns:
            The height (y2 - y1) if bbox exists, None otherwise
        """
        bbox = self.get_bbox()
        if bbox:
            return bbox[3] - bbox[1]
        return None
    
    def get_rotate(self) -> Optional[float]:
        """
        Get the rotation of the node.

        Returns:
            The rotation value if it exists, None otherwise
        """
        rotate = self.get_feature_value("spatial", "rotate")
        if rotate is None:
            return None

        # Feature values are stored as arrays - unwrap if needed
        if isinstance(rotate, (list, tuple)) and len(rotate) == 1:
            rotate = rotate[0]

        if rotate is not None:
            return float(rotate)
        return None
    
    def set_rotate(self, rotate: float):
        """
        Set the rotation of the node.
        
        Args:
            rotate: The rotation value
        """
        # Use set_feature for cleaner behavior - ensures single value
        self.set_feature("spatial", "rotate", float(rotate))
    
    def get_content_parts(self) -> List[Any]:
        """
        Get the content parts for this node.

        Content parts can be either strings or integers. Integer values represent
        child node indices (for rollup operations where parent content references
        child nodes).

        Returns:
            List of content parts (strings and/or integers)
        """
        self._check_not_closed()

        result = lib.GetNodeContentParts(self._handle)
        check_error()

        if result == ffi.NULL:
            return []

        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)

        if not json_str:
            return []

        try:
            parts = json.loads(json_str)
            return parts if isinstance(parts, list) else []
        except (json.JSONDecodeError, AttributeError):
            return []

    def set_content_parts(self, content_parts: List[Any]):
        """
        Set the content parts for this node.

        Content parts can be either strings or integers. Integer values represent
        child node indices (for rollup operations where parent content references
        child nodes).

        Args:
            content_parts: List of content parts (strings and/or integers)
        """
        self._check_not_closed()

        if not isinstance(content_parts, list):
            raise ValueError("Content parts must be a list")

        # Validate each part is either string or integer
        for i, part in enumerate(content_parts):
            if not isinstance(part, (str, int)):
                raise ValueError(f"Content part at index {i} must be a string or integer, got {type(part).__name__}")

        # Convert to JSON
        json_str = json.dumps(content_parts)
        json_bytes = json_str.encode('utf-8')

        success = lib.SetNodeContentParts(self._handle, json_bytes)
        check_error()

        if not success:
            raise RuntimeError("Failed to set content parts")

    # Compatibility Methods (for migration from legacy kodexa SDK)

    def adopt_children(self, nodes_to_adopt: List['ContentNode'], replace: bool = False):
        """
        Adopt children from another node or list, preserving their order.

        This will take a list of content nodes and adopt them under this node,
        ensuring they are re-parented. The order of nodes in nodes_to_adopt
        determines their final index order.

        Args:
            nodes_to_adopt: List of ContentNodes to adopt
            replace: If True, remove children not in nodes_to_adopt

        Example:
            # select all nodes of type 'line', then the root node 'adopts' them
            document.content_node.adopt_children(document.select('//line'), replace=True)
        """
        # No-op for deleted nodes (legacy SDK compatibility)
        if getattr(self, '_deleted', False):
            return
        self._check_not_closed()

        # Convert to list to ensure we can iterate
        children = list(nodes_to_adopt)
        if not children:
            return

        # Build array of child handles for C bridge
        # Legacy SDK compatibility: recreate deleted nodes before passing to Go
        child_handles = ffi.new("unsigned long long[]", len(children))
        for i, child in enumerate(children):
            if not hasattr(child, '_handle'):
                raise ValueError(f"Invalid ContentNode object at index {i}")

            # If child was deleted, recreate it from cached data
            if getattr(child, '_deleted', False) and hasattr(child, '_deleted_cache'):
                child = self._recreate_deleted_node(child)
                children[i] = child  # Update list with recreated node

            child_handles[i] = child._handle

        # Call Go backend's AdoptChildren directly
        success = lib.AdoptNodeChildren(
            self._handle,
            child_handles,
            len(children),
            1 if replace else 0
        )
        check_error()
        if not success:
            raise RuntimeError("Failed to adopt children")

    def set_bbox_from_children(self):
        """
        Calculate and set bounding box from child nodes.

        Computes the union of all child bounding boxes and sets it on this node.
        Uses optimized Go implementation that leverages cached data when preloaded.
        """
        self._check_not_closed()

        # Use Go binding which is optimized and uses cached bbox data
        success = lib.SetBboxFromChildren(self._handle)
        check_error()

        if not success:
            # Fallback to Python implementation if Go fails
            children = self.get_children()
            if not children:
                return

            bboxes = [c.get_bbox() for c in children if c.get_bbox()]
            if not bboxes:
                return

            x1 = min(b[0] for b in bboxes)
            y1 = min(b[1] for b in bboxes)
            x2 = max(b[2] for b in bboxes)
            y2 = max(b[3] for b in bboxes)
            self.set_bbox([x1, y1, x2, y2])

    def set_statistics(self, statistics: Dict[str, Any]):
        """
        Set spatial statistics for this node.

        Statistics are stored as a feature under spatial:statistics,
        matching the legacy kodexa SDK behavior.

        Args:
            statistics: Dictionary of statistics to store
        """
        self._check_not_closed()

        self.add_feature("spatial", "statistics", statistics)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this node to a dictionary representation.

        This includes core fields (type, content), optional fields (index, virtual,
        confidence, uuid), features (including bbox), and children (recursive).

        The format matches the legacy kodexa SDK's to_dict() method.

        Returns:
            Dictionary representation of this node and its subtree
        """
        self._check_not_closed()

        result = lib.NodeToDict(self._handle)
        check_error()

        if result == ffi.NULL:
            return {}

        json_str = ffi.string(result).decode('utf-8')
        lib.FreeString(result)

        if not json_str or json_str == "{}":
            return {}

        return json.loads(json_str)

    # New methods exposed from Go backend

    def delete_children(self, nodes_to_delete: List['ContentNode'] = None, exclude_nodes: List['ContentNode'] = None):
        """
        Delete child nodes, optionally excluding specific nodes.

        Args:
            nodes_to_delete: List of ContentNodes to delete. If None, deletes all children.
            exclude_nodes: List of ContentNodes to exclude from deletion.
        """
        self._check_not_closed()

        # Build array of child handles to delete
        if nodes_to_delete:
            delete_handles = ffi.new("unsigned long long[]", len(nodes_to_delete))
            for i, child in enumerate(nodes_to_delete):
                if hasattr(child, '_handle'):
                    delete_handles[i] = child._handle
            delete_count = len(nodes_to_delete)
        else:
            delete_handles = ffi.NULL
            delete_count = 0

        # Build array of exclude handles
        if exclude_nodes:
            exclude_handles = ffi.new("unsigned long long[]", len(exclude_nodes))
            for i, child in enumerate(exclude_nodes):
                if hasattr(child, '_handle'):
                    exclude_handles[i] = child._handle
            exclude_count = len(exclude_nodes)
        else:
            exclude_handles = ffi.NULL
            exclude_count = 0

        success = lib.DeleteNodeChildren(
            self._handle,
            delete_handles,
            delete_count,
            exclude_handles,
            exclude_count
        )
        check_error()
        if not success:
            raise RuntimeError("Failed to delete children")

    def is_root(self) -> bool:
        """Check if this node is the root node (has no parent)."""
        self._check_not_closed()
        return bool(lib.IsNodeRoot(self._handle))

    def is_first_child(self) -> bool:
        """Check if this node is the first child of its parent."""
        self._check_not_closed()
        return bool(lib.IsNodeFirstChild(self._handle))

    def is_last_child(self) -> bool:
        """Check if this node is the last child of its parent."""
        self._check_not_closed()
        return bool(lib.IsNodeLastChild(self._handle))

    def is_leaf(self) -> bool:
        """Check if this node is a leaf node (has no children)."""
        self._check_not_closed()
        return bool(lib.IsNodeLeaf(self._handle))

    def get_depth(self) -> int:
        """Get the depth of this node in the tree (root is 0)."""
        self._check_not_closed()
        depth = lib.GetNodeDepth(self._handle)
        check_error()
        return depth

    def get_page(self) -> int:
        """Get the page number this node belongs to."""
        self._check_not_closed()
        page = lib.GetNodePage(self._handle)
        check_error()
        return page

    def get_first_child(self) -> Optional['ContentNode']:
        """Get the first child of this node."""
        self._check_not_closed()
        child_handle = lib.GetNodeFirstChild(self._handle)
        if child_handle == 0:
            return None
        node = ContentNode._from_handle(child_handle)
        node._document = self._document
        return node

    def get_last_child(self) -> Optional['ContentNode']:
        """Get the last child of this node."""
        self._check_not_closed()
        child_handle = lib.GetNodeLastChild(self._handle)
        if child_handle == 0:
            return None
        node = ContentNode._from_handle(child_handle)
        node._document = self._document
        return node

    def get_confidence(self) -> float:
        """Get the confidence score for this node."""
        self._check_not_closed()
        return float(lib.GetNodeConfidence(self._handle))

    def set_confidence(self, confidence: float):
        """Set the confidence score for this node."""
        self._check_not_closed()
        success = lib.SetNodeConfidence(self._handle, confidence)
        check_error()
        if not success:
            raise RuntimeError("Failed to set confidence")

    def has_confidence(self) -> bool:
        """Check if this node has a confidence score set."""
        self._check_not_closed()
        return bool(lib.HasNodeConfidence(self._handle))

    def clear_bbox(self):
        """Clear the bounding box for this node."""
        self._check_not_closed()
        success = lib.ClearNodeBBox(self._handle)
        check_error()
        if not success:
            raise RuntimeError("Failed to clear bounding box")

    def matches_type(self, pattern: str) -> bool:
        """
        Check if this node's type matches a regex pattern.

        Args:
            pattern: Regular expression pattern to match against node type

        Returns:
            True if the pattern matches the node type
        """
        self._check_not_closed()
        pattern_bytes = pattern.encode('utf-8')
        result = lib.NodeMatches(self._handle, pattern_bytes)
        check_error()
        if result == -1:
            raise RuntimeError("Failed to match pattern")
        return bool(result)

    def remove_all_tags(self):
        """Remove all tags from this node."""
        self._check_not_closed()
        success = lib.RemoveAllNodeTags(self._handle)
        check_error()
        if not success:
            raise RuntimeError("Failed to remove all tags")

    def remove_all_features(self):
        """Remove all features from this node."""
        self._check_not_closed()
        success = lib.RemoveAllNodeFeatures(self._handle)
        check_error()
        if not success:
            raise RuntimeError("Failed to remove all features")

    # ==========================================================================
    # Additional methods (previously unexposed Go methods)
    # ==========================================================================

    def has_next_node(self, node_type_re: str = ".*", skip_virtual: bool = False) -> bool:
        """
        Check if there is a next sibling node matching the criteria.

        Args:
            node_type_re: Regular expression to match node types (default: ".*" matches all)
            skip_virtual: If True, skip virtual nodes

        Returns:
            True if a matching next node exists, False otherwise
        """
        self._check_not_closed()
        result = lib.HasNextNode(self._handle, node_type_re.encode('utf-8'), 1 if skip_virtual else 0)
        check_error()
        if result == -1:
            return False
        return result == 1

    def has_previous_node(self, node_type_re: str = ".*", skip_virtual: bool = False) -> bool:
        """
        Check if there is a previous sibling node matching the criteria.

        Args:
            node_type_re: Regular expression to match node types (default: ".*" matches all)
            skip_virtual: If True, skip virtual nodes

        Returns:
            True if a matching previous node exists, False otherwise
        """
        self._check_not_closed()
        result = lib.HasPreviousNode(self._handle, node_type_re.encode('utf-8'), 1 if skip_virtual else 0)
        check_error()
        if result == -1:
            return False
        return result == 1

    def get_first_child_index(self) -> Optional[int]:
        """
        Get the index of the first child node.

        Returns:
            The index of the first child, or None if no children
        """
        self._check_not_closed()
        result = lib.GetFirstChildIndex(self._handle)
        check_error()
        if result == -1:
            return None
        return result

    def get_last_child_index(self) -> Optional[int]:
        """
        Get the index of the last child node.

        Returns:
            The index of the last child, or None if no children
        """
        self._check_not_closed()
        result = lib.GetLastChildIndex(self._handle)
        check_error()
        if result == -1:
            return None
        return result

    def get_node_at_index(self, index: int) -> Optional['ContentNode']:
        """
        Get the child node at the specified index.

        Args:
            index: The index of the child to retrieve

        Returns:
            The ContentNode at the specified index, or None if not found
        """
        self._check_not_closed()
        handle = lib.GetNodeAtChildIndex(self._handle, index)
        check_error()
        if handle == 0:
            return None
        node = ContentNode._from_handle(handle)
        node._document = self._document
        return node

    def add_child_content(self, node_type: str, content: str, index: int = None) -> 'ContentNode':
        """
        Create and add a new child node with the specified content.

        This is a convenience method that creates a new node and adds it as a child
        in a single operation.

        Args:
            node_type: The type of the new node
            content: The content for the new node
            index: Optional index position for the new child (-1 or None for end)

        Returns:
            The newly created ContentNode
        """
        self._check_not_closed()
        idx = -1 if index is None else index
        handle = lib.AddChildContent(
            self._handle,
            node_type.encode('utf-8'),
            content.encode('utf-8'),
            idx
        )
        check_error()
        if handle == 0:
            raise RuntimeError("Failed to add child content")
        node = ContentNode._from_handle(handle)
        node._document = self._document
        return node

    def get_ancestors(self) -> List['ContentNode']:
        """
        Get all ancestor nodes from this node up to (but not including) the root.

        Returns:
            List of ancestor ContentNode objects, from immediate parent to root
        """
        self._check_not_closed()
        count_ptr = ffi.new("int*")
        handles_ptr = lib.GetNodeAncestors(self._handle, count_ptr)
        check_error()

        if handles_ptr == ffi.NULL:
            return []

        count = count_ptr[0]
        nodes = []
        for i in range(count):
            node_handle = handles_ptr[i]
            if node_handle != 0:
                node = ContentNode._from_handle(node_handle)
                node._document = self._document
                nodes.append(node)

        lib.FreeHandleArray(handles_ptr)
        return nodes

    def get_descendants(self) -> List['ContentNode']:
        """
        Get all descendant nodes of this node (children, grandchildren, etc.).

        Returns:
            List of all descendant ContentNode objects in depth-first order
        """
        self._check_not_closed()
        count_ptr = ffi.new("int*")
        handles_ptr = lib.GetNodeDescendants(self._handle, count_ptr)
        check_error()

        if handles_ptr == ffi.NULL:
            return []

        count = count_ptr[0]
        nodes = []
        for i in range(count):
            node_handle = handles_ptr[i]
            if node_handle != 0:
                node = ContentNode._from_handle(node_handle)
                node._document = self._document
                nodes.append(node)

        lib.FreeHandleArray(handles_ptr)
        return nodes

    def copy_tag(self, selector: str = ".", existing_tag_name: Optional[str] = None, new_tag_name: Optional[str] = None):
        """
        Copy a tag from one name to another on selected nodes.

        Creates a new tag of 'new_tag_name' on the selected content node(s) with
        the same information as the tag with 'existing_tag_name'.

        Both existing_tag_name and new_tag_name are required and must be different
        from one another. If a tag with 'existing_tag_name' does not exist on a
        selected node, no action is taken for that node.

        Args:
            selector: The selector to identify the source nodes to work on (default "." - the current node)
            existing_tag_name: The name of the existing tag whose values will be copied
            new_tag_name: The name of the new tag. Must be different from existing_tag_name

        Example:
            >>> document.get_root().copy_tag('.', 'foo', 'bar')
        """
        if existing_tag_name is None or new_tag_name is None or existing_tag_name == new_tag_name:
            return  # do nothing, just exit function

        for node in self.select(selector):
            existing_tag_values = node.get_feature_values("tag", existing_tag_name)
            if existing_tag_values:
                for val in existing_tag_values:
                    # Create a copy of the tag value dict for the new tag name
                    if isinstance(val, dict):
                        # Construct tag dict with the same data
                        tag_dict = {
                            'name': new_tag_name,
                            'start': val.get('start'),
                            'end': val.get('end'),
                            'value': val.get('value'),
                            'uuid': val.get('uuid'),
                            'data': val.get('data'),
                        }
                        node.add_feature("tag", new_tag_name, tag_dict)
                    else:
                        # If it's already a tag-like object, add it directly
                        node.add_feature("tag", new_tag_name, val)

    def update_feature(self, feature: ContentFeature):
        """
        Update a feature on this node by removing and re-adding it.

        This is used to persist changes made to a ContentFeature object
        back to the document storage.

        Args:
            feature: The ContentFeature to update

        Example:
            >>> feature = node.get_feature("spatial", "bbox")
            >>> # modify feature...
            >>> node.update_feature(feature)
        """
        self._check_not_closed()

        # Remove the existing feature
        self.remove_feature(feature.feature_type, feature.name)

        # Re-add with the updated values
        # Use the feature's value directly since it's already been modified
        self.add_feature(feature.feature_type, feature.name, feature.value, serialized=True)

    def get_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Get the spatial statistics for this node.

        Statistics are stored as a feature under spatial:statistics.

        Returns:
            The statistics dictionary, or None if not set

        Example:
            >>> stats = document.select('//page')[0].get_statistics()
        """
        return self.get_feature_value("spatial", "statistics")

    def to_json(self) -> str:
        """
        Create a JSON string representation of this ContentNode.

        Returns:
            str: The JSON formatted string representation of this ContentNode

        Example:
            >>> json_str = node.to_json()
        """
        return json.dumps(self.to_dict())

    def update(self):
        """
        Persist changes to the node (legacy SDK compatibility).

        In the new SDK, this is a no-op because all changes are automatically
        persisted to the Go backend when properties are modified. This method
        exists only for API compatibility with legacy code.

        Example:
            >>> node.content = "new content"
            >>> node.update()  # No-op - changes already persisted
        """
        # No-op: new SDK auto-persists all changes to Go backend
        pass

