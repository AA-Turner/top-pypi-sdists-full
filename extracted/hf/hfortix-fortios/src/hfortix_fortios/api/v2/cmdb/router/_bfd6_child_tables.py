"""
Child Table Helpers for cmdb.router.bfd6

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class NeighborHelper:
    """
    Helper for managing neighbor child table in cmdb.router.bfd6.
    
    Configure neighbor of IPv6 BFD.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.bfd6.neighbor.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.bfd6.neighbor.get(ip6_address="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.bfd6.neighbor.set(
        ...     ip6_address="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.bfd6.neighbor.delete(ip6_address="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.bfd6.neighbor.exists(ip6_address="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.bfd6.neighbor.put([
        ...     {'ip6_address': "value1"},
        ...     {'ip6_address': "value2"},
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
        self._mkey = 'ip6_address'
    
    def get(
        self,
        ip6_address: str | None = None,
    ) -> list[FortiObject[NeighborDict]] | FortiObject[NeighborDict] | None:
        """
        Get neighbor entries.
        
        Args:
            ip6_address: If provided, return only the entry with this ip6-address
            
        Returns:
            List of FortiObjects if ip6_address is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.bfd6.neighbor.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.bfd6.neighbor.get(ip6_address="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if ip6_address is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == ip6_address:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(ip6_address):
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
        
        If entry with same ip6-address exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include ip6_address)
            
        Returns:
            API response
            
        Raises:
            ValueError: If ip6_address not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.bfd6.neighbor.set(
            ...     ip6_address="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.bfd6.neighbor.set(
            ...     ip6_address="existing_value",
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
        ip6_address: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a neighbor entry.
        
        Args:
            ip6_address: Ip6-address of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.bfd6.neighbor.delete(ip6_address="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != ip6_address and str(entry_value) != str(ip6_address)
        
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
            >>> result = fgt.api.cmdb.router.bfd6.neighbor.put([
            ...     {'ip6_address': "value1"},
            ...     {'ip6_address': "value2"},
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
        ip6_address: str,
    ) -> bool:
        """
        Check if a neighbor entry exists.
        
        Args:
            ip6_address: Ip6-address to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.bfd6.neighbor.exists(ip6_address="value"):
            ...     print("Entry exists")
        """
        entry = self.get(ip6_address=ip6_address)
        return entry is not None




class MultihopTemplateHelper:
    """
    Helper for managing multihop-template child table in cmdb.router.bfd6.
    
    BFD IPv6 multi-hop template table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.bfd6.multihop_template.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.bfd6.multihop_template.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.bfd6.multihop_template.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.bfd6.multihop_template.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.bfd6.multihop_template.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.bfd6.multihop_template.put([
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
        self._table_name = 'multihop_template'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[MultihopTemplateDict]] | FortiObject[MultihopTemplateDict] | None:
        """
        Get multihop-template entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.bfd6.multihop_template.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.bfd6.multihop_template.get(id="value")
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
        Add or update a multihop-template entry.
        
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
            >>> result = fgt.api.cmdb.router.bfd6.multihop_template.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.bfd6.multihop_template.set(
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
        Delete a multihop-template entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.bfd6.multihop_template.delete(id="value")
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
        Replace entire multihop-template table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.bfd6.multihop_template.put([
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
        Check if a multihop-template entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.bfd6.multihop_template.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None


