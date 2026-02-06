"""
Child Table Helpers for cmdb.router.ripng

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class DistanceHelper:
    """
    Helper for managing distance child table in cmdb.router.ripng.
    
    Distance.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.distance.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.distance.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.distance.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.distance.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.distance.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.distance.put([
        ...     {'id': "value1"},
        ...     {'id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'distance'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[DistanceDict]] | FortiObject[DistanceDict] | None:
        """
        Get distance entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.distance.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.distance.get(id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a distance entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.distance.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.distance.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a distance entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.distance.delete(id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != id and str(entry_value) != str(id)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire distance table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.distance.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a distance entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.distance.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class DistributeListHelper:
    """
    Helper for managing distribute-list child table in cmdb.router.ripng.
    
    Distribute list.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.distribute_list.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.distribute_list.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.distribute_list.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.distribute_list.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.distribute_list.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.distribute_list.put([
        ...     {'id': "value1"},
        ...     {'id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'distribute_list'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[DistributeListDict]] | FortiObject[DistributeListDict] | None:
        """
        Get distribute-list entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.distribute_list.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.distribute_list.get(id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a distribute-list entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.distribute_list.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.distribute_list.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a distribute-list entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.distribute_list.delete(id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != id and str(entry_value) != str(id)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire distribute-list table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.distribute_list.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a distribute-list entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.distribute_list.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class NeighborHelper:
    """
    Helper for managing neighbor child table in cmdb.router.ripng.
    
    Neighbor.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.neighbor.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.neighbor.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.neighbor.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.neighbor.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.neighbor.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.neighbor.put([
        ...     {'id': "value1"},
        ...     {'id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'neighbor'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[NeighborDict]] | FortiObject[NeighborDict] | None:
        """
        Get neighbor entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.neighbor.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.neighbor.get(id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a neighbor entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.neighbor.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.neighbor.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a neighbor entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.neighbor.delete(id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != id and str(entry_value) != str(id)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire neighbor table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.neighbor.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a neighbor entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.neighbor.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class NetworkHelper:
    """
    Helper for managing network child table in cmdb.router.ripng.
    
    Network.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.network.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.network.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.network.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.network.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.network.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.network.put([
        ...     {'id': "value1"},
        ...     {'id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'network'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[NetworkDict]] | FortiObject[NetworkDict] | None:
        """
        Get network entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.network.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.network.get(id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a network entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.network.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.network.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a network entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.network.delete(id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != id and str(entry_value) != str(id)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire network table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.network.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a network entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.network.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class AggregateAddressHelper:
    """
    Helper for managing aggregate-address child table in cmdb.router.ripng.
    
    Aggregate address.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.aggregate_address.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.aggregate_address.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.aggregate_address.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.aggregate_address.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.aggregate_address.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.aggregate_address.put([
        ...     {'id': "value1"},
        ...     {'id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'aggregate_address'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[AggregateAddressDict]] | FortiObject[AggregateAddressDict] | None:
        """
        Get aggregate-address entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.aggregate_address.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.aggregate_address.get(id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a aggregate-address entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.aggregate_address.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.aggregate_address.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a aggregate-address entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.aggregate_address.delete(id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != id and str(entry_value) != str(id)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire aggregate-address table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.aggregate_address.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a aggregate-address entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.aggregate_address.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class OffsetListHelper:
    """
    Helper for managing offset-list child table in cmdb.router.ripng.
    
    Offset list.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.offset_list.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.offset_list.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.offset_list.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.offset_list.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.offset_list.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.offset_list.put([
        ...     {'id': "value1"},
        ...     {'id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'offset_list'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[OffsetListDict]] | FortiObject[OffsetListDict] | None:
        """
        Get offset-list entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.offset_list.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.offset_list.get(id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a offset-list entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.offset_list.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.offset_list.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a offset-list entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.offset_list.delete(id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != id and str(entry_value) != str(id)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire offset-list table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.offset_list.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a offset-list entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.offset_list.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class PassiveInterfaceHelper:
    """
    Helper for managing passive-interface child table in cmdb.router.ripng.
    
    Passive interface configuration.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.passive_interface.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.passive_interface.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.passive_interface.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.passive_interface.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.passive_interface.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.passive_interface.put([
        ...     {'name': "value1"},
        ...     {'name': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'passive_interface'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
    ) -> list[FortiObject[PassiveInterfaceDict]] | FortiObject[PassiveInterfaceDict] | None:
        """
        Get passive-interface entries.
        
        Args:
            name: If provided, return only the entry with this name
            
        Returns:
            List of FortiObjects if name is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.passive_interface.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.passive_interface.get(name="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if name is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == name:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(name):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a passive-interface entry.
        
        If entry with same name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.passive_interface.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.passive_interface.set(
            ...     name="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a passive-interface entry.
        
        Args:
            name: Name of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.passive_interface.delete(name="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != name and str(entry_value) != str(name)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire passive-interface table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.passive_interface.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if a passive-interface entry exists.
        
        Args:
            name: Name to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.passive_interface.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name)
        return entry is not None




class RedistributeHelper:
    """
    Helper for managing redistribute child table in cmdb.router.ripng.
    
    Redistribute configuration.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.redistribute.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.redistribute.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.redistribute.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.redistribute.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.redistribute.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.redistribute.put([
        ...     {'name': "value1"},
        ...     {'name': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'redistribute'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
    ) -> list[FortiObject[RedistributeDict]] | FortiObject[RedistributeDict] | None:
        """
        Get redistribute entries.
        
        Args:
            name: If provided, return only the entry with this name
            
        Returns:
            List of FortiObjects if name is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.redistribute.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.redistribute.get(name="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if name is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == name:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(name):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a redistribute entry.
        
        If entry with same name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.redistribute.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.redistribute.set(
            ...     name="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a redistribute entry.
        
        Args:
            name: Name of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.redistribute.delete(name="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != name and str(entry_value) != str(name)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire redistribute table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.redistribute.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if a redistribute entry exists.
        
        Args:
            name: Name to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.redistribute.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name)
        return entry is not None




class InterfaceHelper:
    """
    Helper for managing interface child table in cmdb.router.ripng.
    
    RIPng interface configuration.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.ripng.interface.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.ripng.interface.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.ripng.interface.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.ripng.interface.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.ripng.interface.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.ripng.interface.put([
        ...     {'name': "value1"},
        ...     {'name': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'interface'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
    ) -> list[FortiObject[InterfaceDict]] | FortiObject[InterfaceDict] | None:
        """
        Get interface entries.
        
        Args:
            name: If provided, return only the entry with this name
            
        Returns:
            List of FortiObjects if name is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.ripng.interface.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.ripng.interface.get(name="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if name is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == name:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(name):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a interface entry.
        
        If entry with same name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.ripng.interface.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.ripng.interface.set(
            ...     name="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Convert Python snake_case keys to FortiOS kebab-case
        fortios_kwargs = {k.replace('_', '-'): v for k, v in kwargs.items()}
        
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            entry_value = entry.get(self._mkey)
            # Handle both exact match and string comparison for int/string mismatches
            if entry_value == mkey_value or str(entry_value) == str(mkey_value):
                # Get raw dict from FortiObject (which has hyphenated keys)
                entry_dict = entry.to_dict() if hasattr(entry, 'to_dict') else entry
                # Update existing entry
                entries[i] = {**entry_dict, **fortios_kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(fortios_kwargs)
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        name: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a interface entry.
        
        Args:
            name: Name of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.interface.delete(name="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != name and str(entry_value) != str(name)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Get all fields from current config to preserve other fields
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries_as_dicts
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire interface table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.ripng.interface.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        # Get current config to preserve other fields
        config = self._parent.get()
        config_dict = config.to_dict() if hasattr(config, 'to_dict') else {}
        
        # Update only the child table field
        config_dict[self._table_name.replace('_', '-')] = entries
        
        return self._parent.put(
            payload_dict=config_dict,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if a interface entry exists.
        
        Args:
            name: Name to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.ripng.interface.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name)
        return entry is not None


