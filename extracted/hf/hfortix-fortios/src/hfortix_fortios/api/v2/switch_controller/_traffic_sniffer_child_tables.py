"""
Child Table Helpers for switch-controller/traffic-sniffer

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class TargetMacDict(TypedDict, total=False):
    """Type definition for target_mac child table entry."""
    mac: str
    description: str | None

class TargetIpDict(TypedDict, total=False):
    """Type definition for target_ip child table entry."""
    ip: str
    description: str | None

class TargetPortDict(TypedDict, total=False):
    """Type definition for target_port child table entry."""
    switch_id: str
    description: str | None
    in_ports: list[Any] | None
    out_ports: list[Any] | None

class TargetMacHelper:
    """
    Helper for managing target-mac child table in switch-controller/traffic-sniffer.
    
    Sniffer MACs to filter.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.switch-controller.traffic-sniffer.target_mac.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.switch-controller.traffic-sniffer.target_mac.get(mac="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.set(
        ...     mac="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.delete(mac="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.switch-controller.traffic-sniffer.target_mac.exists(mac="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.put([
        ...     {'mac': "value1"},
        ...     {'mac': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'target_mac'
        self._mkey = 'mac'
    
    def get(
        self,
        mac: str | None = None,
    ) -> list[FortiObject[TargetMacDict]] | FortiObject[TargetMacDict] | None:
        """
        Get target-mac entries.
        
        Args:
            mac: If provided, return only the entry with this mac
            
        Returns:
            List of FortiObjects if mac is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.switch-controller.traffic-sniffer.target_mac.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.switch-controller.traffic-sniffer.target_mac.get(mac="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if mac is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == mac:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(mac):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a target-mac entry.
        
        If entry with same mac exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include mac)
            
        Returns:
            API response
            
        Raises:
            ValueError: If mac not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.set(
            ...     mac="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.set(
            ...     mac="existing_value",
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
        mac: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a target-mac entry.
        
        Args:
            mac: Mac of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.delete(mac="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != mac and str(entry_value) != str(mac)
        
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
        Replace entire target-mac table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_mac.put([
            ...     {'mac': "value1"},
            ...     {'mac': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        mac: str,
    ) -> bool:
        """
        Check if a target-mac entry exists.
        
        Args:
            mac: Mac to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.switch-controller.traffic-sniffer.target_mac.exists(mac="value"):
            ...     print("Entry exists")
        """
        entry = self.get(mac=mac)
        return entry is not None




class TargetIpHelper:
    """
    Helper for managing target-ip child table in switch-controller/traffic-sniffer.
    
    Sniffer IPs to filter.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.switch-controller.traffic-sniffer.target_ip.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.switch-controller.traffic-sniffer.target_ip.get(ip="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.set(
        ...     ip="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.delete(ip="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.switch-controller.traffic-sniffer.target_ip.exists(ip="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.put([
        ...     {'ip': "value1"},
        ...     {'ip': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'target_ip'
        self._mkey = 'ip'
    
    def get(
        self,
        ip: str | None = None,
    ) -> list[FortiObject[TargetIpDict]] | FortiObject[TargetIpDict] | None:
        """
        Get target-ip entries.
        
        Args:
            ip: If provided, return only the entry with this ip
            
        Returns:
            List of FortiObjects if ip is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.switch-controller.traffic-sniffer.target_ip.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.switch-controller.traffic-sniffer.target_ip.get(ip="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if ip is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == ip:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(ip):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a target-ip entry.
        
        If entry with same ip exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include ip)
            
        Returns:
            API response
            
        Raises:
            ValueError: If ip not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.set(
            ...     ip="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.set(
            ...     ip="existing_value",
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
        ip: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a target-ip entry.
        
        Args:
            ip: Ip of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.delete(ip="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != ip and str(entry_value) != str(ip)
        
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
        Replace entire target-ip table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_ip.put([
            ...     {'ip': "value1"},
            ...     {'ip': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        ip: str,
    ) -> bool:
        """
        Check if a target-ip entry exists.
        
        Args:
            ip: Ip to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.switch-controller.traffic-sniffer.target_ip.exists(ip="value"):
            ...     print("Entry exists")
        """
        entry = self.get(ip=ip)
        return entry is not None




class TargetPortHelper:
    """
    Helper for managing target-port child table in switch-controller/traffic-sniffer.
    
    Sniffer ports to filter.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.switch-controller.traffic-sniffer.target_port.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.switch-controller.traffic-sniffer.target_port.get(switch_id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.set(
        ...     switch_id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.delete(switch_id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.switch-controller.traffic-sniffer.target_port.exists(switch_id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.put([
        ...     {'switch_id': "value1"},
        ...     {'switch_id': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'target_port'
        self._mkey = 'switch_id'
    
    def get(
        self,
        switch_id: str | None = None,
    ) -> list[FortiObject[TargetPortDict]] | FortiObject[TargetPortDict] | None:
        """
        Get target-port entries.
        
        Args:
            switch_id: If provided, return only the entry with this switch-id
            
        Returns:
            List of FortiObjects if switch_id is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.switch-controller.traffic-sniffer.target_port.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.switch-controller.traffic-sniffer.target_port.get(switch_id="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if switch_id is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == switch_id:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(switch_id):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a target-port entry.
        
        If entry with same switch-id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include switch_id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If switch_id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.set(
            ...     switch_id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.set(
            ...     switch_id="existing_value",
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
        switch_id: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a target-port entry.
        
        Args:
            switch_id: Switch-id of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.delete(switch_id="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != switch_id and str(entry_value) != str(switch_id)
        
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
        Replace entire target-port table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.switch-controller.traffic-sniffer.target_port.put([
            ...     {'switch_id': "value1"},
            ...     {'switch_id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        switch_id: str,
    ) -> bool:
        """
        Check if a target-port entry exists.
        
        Args:
            switch_id: Switch-id to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.switch-controller.traffic-sniffer.target_port.exists(switch_id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(switch_id=switch_id)
        return entry is not None


