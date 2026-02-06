"""
Child Table Helpers for system/federated-upgrade

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class KnownHaMembersDict(TypedDict, total=False):
    """Type definition for known_ha_members child table entry."""
    serial: str

class NodeListDict(TypedDict, total=False):
    """Type definition for node_list child table entry."""
    serial: str
    timing: str
    maximum_minutes: int
    time: str
    setup_time: str
    upgrade_path: str
    device_type: str
    allow_download: str | None
    coordinating_fortigate: str | None
    failure_reason: str | None

class KnownHaMembersHelper:
    """
    Helper for managing known-ha-members child table in system/federated-upgrade.
    
    Known members of the HA cluster. If a member is missing at upgrade time, the upgrade will be cancelled.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.federated-upgrade.known_ha_members.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.federated-upgrade.known_ha_members.get(serial="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.federated-upgrade.known_ha_members.set(
        ...     serial="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.federated-upgrade.known_ha_members.delete(serial="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.federated-upgrade.known_ha_members.exists(serial="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.federated-upgrade.known_ha_members.put([
        ...     {'serial': "value1"},
        ...     {'serial': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'known_ha_members'
        self._mkey = 'serial'
    
    def get(
        self,
        serial: str | None = None,
    ) -> list[FortiObject[KnownHaMembersDict]] | FortiObject[KnownHaMembersDict] | None:
        """
        Get known-ha-members entries.
        
        Args:
            serial: If provided, return only the entry with this serial
            
        Returns:
            List of FortiObjects if serial is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.federated-upgrade.known_ha_members.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.federated-upgrade.known_ha_members.get(serial="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if serial is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == serial:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(serial):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a known-ha-members entry.
        
        If entry with same serial exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include serial)
            
        Returns:
            API response
            
        Raises:
            ValueError: If serial not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.system.federated-upgrade.known_ha_members.set(
            ...     serial="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.federated-upgrade.known_ha_members.set(
            ...     serial="existing_value",
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
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        serial: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a known-ha-members entry.
        
        Args:
            serial: Serial of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.federated-upgrade.known_ha_members.delete(serial="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != serial and str(entry_value) != str(serial)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
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
        Replace entire known-ha-members table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.federated-upgrade.known_ha_members.put([
            ...     {'serial': "value1"},
            ...     {'serial': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        serial: str,
    ) -> bool:
        """
        Check if a known-ha-members entry exists.
        
        Args:
            serial: Serial to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.federated-upgrade.known_ha_members.exists(serial="value"):
            ...     print("Entry exists")
        """
        entry = self.get(serial=serial)
        return entry is not None




class NodeListHelper:
    """
    Helper for managing node-list child table in system/federated-upgrade.
    
    Nodes which will be included in the upgrade.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.federated-upgrade.node_list.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.federated-upgrade.node_list.get(serial="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.federated-upgrade.node_list.set(
        ...     serial="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.federated-upgrade.node_list.delete(serial="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.federated-upgrade.node_list.exists(serial="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.federated-upgrade.node_list.put([
        ...     {'serial': "value1"},
        ...     {'serial': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'node_list'
        self._mkey = 'serial'
    
    def get(
        self,
        serial: str | None = None,
    ) -> list[FortiObject[NodeListDict]] | FortiObject[NodeListDict] | None:
        """
        Get node-list entries.
        
        Args:
            serial: If provided, return only the entry with this serial
            
        Returns:
            List of FortiObjects if serial is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.federated-upgrade.node_list.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.federated-upgrade.node_list.get(serial="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if serial is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == serial:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(serial):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a node-list entry.
        
        If entry with same serial exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include serial)
            
        Returns:
            API response
            
        Raises:
            ValueError: If serial not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.system.federated-upgrade.node_list.set(
            ...     serial="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.federated-upgrade.node_list.set(
            ...     serial="existing_value",
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
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        serial: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a node-list entry.
        
        Args:
            serial: Serial of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.federated-upgrade.node_list.delete(serial="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != serial and str(entry_value) != str(serial)
        
        entries = [e for e in entries if should_keep(e)]
        
        # Convert all FortiObjects to dicts for API submission
        entries_as_dicts = [
            e.to_dict() if hasattr(e, 'to_dict') else e
            for e in entries
        ]
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
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
        Replace entire node-list table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.federated-upgrade.node_list.put([
            ...     {'serial': "value1"},
            ...     {'serial': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        serial: str,
    ) -> bool:
        """
        Check if a node-list entry exists.
        
        Args:
            serial: Serial to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.federated-upgrade.node_list.exists(serial="value"):
            ...     print("Entry exists")
        """
        entry = self.get(serial=serial)
        return entry is not None


