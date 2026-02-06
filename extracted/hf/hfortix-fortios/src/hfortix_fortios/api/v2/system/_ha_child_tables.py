"""
Child Table Helpers for system/ha

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class AutoVirtualMacInterfaceDict(TypedDict, total=False):
    """Type definition for auto_virtual_mac_interface child table entry."""
    interface_name: str

class BackupHbdevDict(TypedDict, total=False):
    """Type definition for backup_hbdev child table entry."""
    name: str | None

class HaMgmtInterfacesDict(TypedDict, total=False):
    """Type definition for ha_mgmt_interfaces child table entry."""
    id: int | None
    interface: str
    dst: str | None
    gateway: str | None
    dst6: str | None
    gateway6: str | None

class UnicastPeersDict(TypedDict, total=False):
    """Type definition for unicast_peers child table entry."""
    id: int | None
    peer_ip: str | None

class VclusterDict(TypedDict, total=False):
    """Type definition for vcluster child table entry."""
    vcluster_id: int | None
    override: str | None
    priority: int | None
    override_wait_time: int | None
    monitor: str | None
    pingserver_monitor_interface: str | None
    pingserver_failover_threshold: int | None
    pingserver_secondary_force_reset: str | None
    pingserver_flip_timeout: int | None
    vdom: list[Any] | None

class AutoVirtualMacInterfaceHelper:
    """
    Helper for managing auto-virtual-mac-interface child table in system/ha.
    
    The physical interface that will be assigned an auto-generated virtual MAC address.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.ha.auto_virtual_mac_interface.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.ha.auto_virtual_mac_interface.get(interface_name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.ha.auto_virtual_mac_interface.set(
        ...     interface_name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.ha.auto_virtual_mac_interface.delete(interface_name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.ha.auto_virtual_mac_interface.exists(interface_name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.ha.auto_virtual_mac_interface.put([
        ...     {'interface_name': "value1"},
        ...     {'interface_name': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'auto_virtual_mac_interface'
        self._mkey = 'interface_name'
    
    def get(
        self,
        interface_name: str | None = None,
    ) -> list[FortiObject[AutoVirtualMacInterfaceDict]] | FortiObject[AutoVirtualMacInterfaceDict] | None:
        """
        Get auto-virtual-mac-interface entries.
        
        Args:
            interface_name: If provided, return only the entry with this interface-name
            
        Returns:
            List of FortiObjects if interface_name is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.ha.auto_virtual_mac_interface.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.ha.auto_virtual_mac_interface.get(interface_name="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if interface_name is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == interface_name:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(interface_name):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a auto-virtual-mac-interface entry.
        
        If entry with same interface-name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include interface_name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If interface_name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.system.ha.auto_virtual_mac_interface.set(
            ...     interface_name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.ha.auto_virtual_mac_interface.set(
            ...     interface_name="existing_value",
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
        interface_name: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a auto-virtual-mac-interface entry.
        
        Args:
            interface_name: Interface-name of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.auto_virtual_mac_interface.delete(interface_name="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != interface_name and str(entry_value) != str(interface_name)
        
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
        Replace entire auto-virtual-mac-interface table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.auto_virtual_mac_interface.put([
            ...     {'interface_name': "value1"},
            ...     {'interface_name': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        interface_name: str,
    ) -> bool:
        """
        Check if a auto-virtual-mac-interface entry exists.
        
        Args:
            interface_name: Interface-name to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.ha.auto_virtual_mac_interface.exists(interface_name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(interface_name=interface_name)
        return entry is not None




class BackupHbdevHelper:
    """
    Helper for managing backup-hbdev child table in system/ha.
    
    Backup heartbeat interfaces. Must be the same for all members.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.ha.backup_hbdev.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.ha.backup_hbdev.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.ha.backup_hbdev.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.ha.backup_hbdev.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.ha.backup_hbdev.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.ha.backup_hbdev.put([
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
        self._table_name = 'backup_hbdev'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
    ) -> list[FortiObject[BackupHbdevDict]] | FortiObject[BackupHbdevDict] | None:
        """
        Get backup-hbdev entries.
        
        Args:
            name: If provided, return only the entry with this name
            
        Returns:
            List of FortiObjects if name is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.ha.backup_hbdev.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.ha.backup_hbdev.get(name="value")
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
        Add or update a backup-hbdev entry.
        
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
            >>> result = fgt.api.system.ha.backup_hbdev.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.ha.backup_hbdev.set(
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
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
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
        Delete a backup-hbdev entry.
        
        Args:
            name: Name of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.backup_hbdev.delete(name="value")
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
        Replace entire backup-hbdev table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.backup_hbdev.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check if a backup-hbdev entry exists.
        
        Args:
            name: Name to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.ha.backup_hbdev.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name)
        return entry is not None




class HaMgmtInterfacesHelper:
    """
    Helper for managing ha-mgmt-interfaces child table in system/ha.
    
    Reserve interfaces to manage individual cluster units.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.ha.ha_mgmt_interfaces.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.ha.ha_mgmt_interfaces.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.ha.ha_mgmt_interfaces.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.ha.ha_mgmt_interfaces.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.ha.ha_mgmt_interfaces.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.ha.ha_mgmt_interfaces.put([
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
        self._table_name = 'ha_mgmt_interfaces'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[HaMgmtInterfacesDict]] | FortiObject[HaMgmtInterfacesDict] | None:
        """
        Get ha-mgmt-interfaces entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.ha.ha_mgmt_interfaces.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.ha.ha_mgmt_interfaces.get(id="value")
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
        Add or update a ha-mgmt-interfaces entry.
        
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
            >>> result = fgt.api.system.ha.ha_mgmt_interfaces.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.ha.ha_mgmt_interfaces.set(
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
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
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
        Delete a ha-mgmt-interfaces entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.ha_mgmt_interfaces.delete(id="value")
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
        Replace entire ha-mgmt-interfaces table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.ha_mgmt_interfaces.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a ha-mgmt-interfaces entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.ha.ha_mgmt_interfaces.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class UnicastPeersHelper:
    """
    Helper for managing unicast-peers child table in system/ha.
    
    Number of unicast peers.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.ha.unicast_peers.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.ha.unicast_peers.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.ha.unicast_peers.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.ha.unicast_peers.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.ha.unicast_peers.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.ha.unicast_peers.put([
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
        self._table_name = 'unicast_peers'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
    ) -> list[FortiObject[UnicastPeersDict]] | FortiObject[UnicastPeersDict] | None:
        """
        Get unicast-peers entries.
        
        Args:
            id: If provided, return only the entry with this id
            
        Returns:
            List of FortiObjects if id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.ha.unicast_peers.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.ha.unicast_peers.get(id="value")
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
        Add or update a unicast-peers entry.
        
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
            >>> result = fgt.api.system.ha.unicast_peers.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.ha.unicast_peers.set(
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
        
        # Put back entire config with updated child table (singleton endpoint)
        return self._parent.put(
            **{self._table_name: entries_as_dicts},
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
        Delete a unicast-peers entry.
        
        Args:
            id: Id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.unicast_peers.delete(id="value")
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
        Replace entire unicast-peers table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.unicast_peers.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
    ) -> bool:
        """
        Check if a unicast-peers entry exists.
        
        Args:
            id: Id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.ha.unicast_peers.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id)
        return entry is not None




class VclusterHelper:
    """
    Helper for managing vcluster child table in system/ha.
    
    Virtual cluster table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.ha.vcluster.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.ha.vcluster.get(vcluster_id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.ha.vcluster.set(
        ...     vcluster_id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.ha.vcluster.delete(vcluster_id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.ha.vcluster.exists(vcluster_id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.ha.vcluster.put([
        ...     {'vcluster_id': "value1"},
        ...     {'vcluster_id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'vcluster'
        self._mkey = 'vcluster_id'
    
    def get(
        self,
        vcluster_id: str | None = None,
    ) -> list[FortiObject[VclusterDict]] | FortiObject[VclusterDict] | None:
        """
        Get vcluster entries.
        
        Args:
            vcluster_id: If provided, return only the entry with this vcluster-id
            
        Returns:
            List of FortiObjects if vcluster_id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.ha.vcluster.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.ha.vcluster.get(vcluster_id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if vcluster_id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == vcluster_id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(vcluster_id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a vcluster entry.
        
        If entry with same vcluster-id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include vcluster_id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If vcluster_id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.system.ha.vcluster.set(
            ...     vcluster_id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.ha.vcluster.set(
            ...     vcluster_id="existing_value",
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
        vcluster_id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a vcluster entry.
        
        Args:
            vcluster_id: Vcluster-id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.vcluster.delete(vcluster_id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != vcluster_id and str(entry_value) != str(vcluster_id)
        
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
        Replace entire vcluster table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.ha.vcluster.put([
            ...     {'vcluster_id': "value1"},
            ...     {'vcluster_id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        vcluster_id: str,
    ) -> bool:
        """
        Check if a vcluster entry exists.
        
        Args:
            vcluster_id: Vcluster-id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.ha.vcluster.exists(vcluster_id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(vcluster_id=vcluster_id)
        return entry is not None


