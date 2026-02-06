"""
Child Table Helpers for cmdb.router.multicast

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class PimSmGlobalVrfHelper:
    """
    Helper for managing pim-sm-global-vrf child table in cmdb.router.multicast.
    
    per-VRF PIM sparse-mode global settings.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.get(vrf="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.set(
        ...     vrf="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.delete(vrf="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.exists(vrf="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.put([
        ...     {'vrf': "value1"},
        ...     {'vrf': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'pim_sm_global_vrf'
        self._mkey = 'vrf'
    
    def get(
        self,
        vrf: str | None = None,
    ) -> list[FortiObject[PimSmGlobalVrfDict]] | FortiObject[PimSmGlobalVrfDict] | None:
        """
        Get pim-sm-global-vrf entries.
        
        Args:
            vrf: If provided, return only the entry with this vrf
            
        Returns:
            List of FortiObjects if vrf is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.get(vrf="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if vrf is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == vrf:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(vrf):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a pim-sm-global-vrf entry.
        
        If entry with same vrf exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include vrf)
            
        Returns:
            API response
            
        Raises:
            ValueError: If vrf not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.set(
            ...     vrf="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.set(
            ...     vrf="existing_value",
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
        vrf: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a pim-sm-global-vrf entry.
        
        Args:
            vrf: Vrf of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.delete(vrf="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != vrf and str(entry_value) != str(vrf)
        
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
        Replace entire pim-sm-global-vrf table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.cmdb.router.multicast.pim_sm_global_vrf.put([
            ...     {'vrf': "value1"},
            ...     {'vrf': "value2"},
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
        vrf: str,
    ) -> bool:
        """
        Check if a pim-sm-global-vrf entry exists.
        
        Args:
            vrf: Vrf to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.cmdb.router.multicast.pim_sm_global_vrf.exists(vrf="value"):
            ...     print("Entry exists")
        """
        entry = self.get(vrf=vrf)
        return entry is not None




class InterfaceHelper:
    """
    Helper for managing interface child table in cmdb.router.multicast.
    
    PIM interfaces.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.cmdb.router.multicast.interface.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.cmdb.router.multicast.interface.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.cmdb.router.multicast.interface.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.cmdb.router.multicast.interface.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.cmdb.router.multicast.interface.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.cmdb.router.multicast.interface.put([
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
            >>> all_entries = fgt.api.cmdb.router.multicast.interface.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.cmdb.router.multicast.interface.get(name="value")
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
            >>> result = fgt.api.cmdb.router.multicast.interface.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.cmdb.router.multicast.interface.set(
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
            >>> result = fgt.api.cmdb.router.multicast.interface.delete(name="value")
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
            >>> result = fgt.api.cmdb.router.multicast.interface.put([
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
            >>> if fgt.api.cmdb.router.multicast.interface.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name)
        return entry is not None


