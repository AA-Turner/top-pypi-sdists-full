"""
Child Table Helpers for system/vdom-dns

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class ServerHostnameDict(TypedDict, total=False):
    """Type definition for server_hostname child table entry."""
    hostname: str

class ServerHostnameHelper:
    """
    Helper for managing server-hostname child table in system/vdom-dns.
    
    DNS server host name list.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.vdom-dns.server_hostname.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.vdom-dns.server_hostname.get(hostname="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.vdom-dns.server_hostname.set(
        ...     hostname="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.vdom-dns.server_hostname.delete(hostname="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.vdom-dns.server_hostname.exists(hostname="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.vdom-dns.server_hostname.put([
        ...     {'hostname': "value1"},
        ...     {'hostname': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'server_hostname'
        self._mkey = 'hostname'
    
    def get(
        self,
        hostname: str | None = None,
    ) -> list[FortiObject[ServerHostnameDict]] | FortiObject[ServerHostnameDict] | None:
        """
        Get server-hostname entries.
        
        Args:
            hostname: If provided, return only the entry with this hostname
            
        Returns:
            List of FortiObjects if hostname is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.vdom-dns.server_hostname.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.vdom-dns.server_hostname.get(hostname="value")
        """
        # Get parent config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Extract child table (entries are already FortiObjects)
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if hostname is None:
            return list(entries) if entries else []
        
        # Find specific entry (handle both string and int comparison)
        for entry in entries:
            entry_value = entry.get(self._mkey) if hasattr(entry, 'get') else getattr(entry, self._mkey, None)
            # Try exact match first
            if entry_value == hostname:
                return entry
            # Try string comparison for int/string mismatches
            if str(entry_value) == str(hostname):
                return entry
        
        return None
    
    def set(
        self,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a server-hostname entry.
        
        If entry with same hostname exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include hostname)
            
        Returns:
            API response
            
        Raises:
            ValueError: If hostname not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.system.vdom-dns.server_hostname.set(
            ...     hostname="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.vdom-dns.server_hostname.set(
            ...     hostname="existing_value",
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
        hostname: str,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a server-hostname entry.
        
        Args:
            hostname: Hostname of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.vdom-dns.server_hostname.delete(hostname="value")
        """
        # Get current config (singleton endpoint, no vdom parameter)
        config = self._parent.get()
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry (handle both exact match and string comparison)
        def should_keep(e):
            entry_value = e.get(self._mkey)
            return entry_value != hostname and str(entry_value) != str(hostname)
        
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
        Replace entire server-hostname table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.vdom-dns.server_hostname.put([
            ...     {'hostname': "value1"},
            ...     {'hostname': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        hostname: str,
    ) -> bool:
        """
        Check if a server-hostname entry exists.
        
        Args:
            hostname: Hostname to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.vdom-dns.server_hostname.exists(hostname="value"):
            ...     print("Entry exists")
        """
        entry = self.get(hostname=hostname)
        return entry is not None


