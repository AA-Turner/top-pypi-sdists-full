"""
Child Table Helpers for system/saml

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, TypedDict

if TYPE_CHECKING:
    from hfortix_fortios.models import FortiObject



class ServiceProvidersDict(TypedDict, total=False):
    """Type definition for service_providers child table entry."""
    name: str
    prefix: str
    sp_binding_protocol: str | None
    sp_cert: str | None
    sp_entity_id: str
    sp_single_sign_on_url: str
    sp_single_logout_url: str | None
    sp_portal_url: str | None
    idp_entity_id: str | None
    idp_single_sign_on_url: str | None
    idp_single_logout_url: str | None
    assertion_attributes: list[Any] | None

class ServiceProvidersHelper:
    """
    Helper for managing service-providers child table in system/saml.
    
    Authorized service providers.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.system.saml.service_providers.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.system.saml.service_providers.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.system.saml.service_providers.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.system.saml.service_providers.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.system.saml.service_providers.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.system.saml.service_providers.put([
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
        self._table_name = 'service_providers'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
    ) -> list[FortiObject[ServiceProvidersDict]] | FortiObject[ServiceProvidersDict] | None:
        """
        Get service-providers entries.
        
        Args:
            name: If provided, return only the entry with this name
            
        Returns:
            List of FortiObjects if name is None, specific FortiObject if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.system.saml.service_providers.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.system.saml.service_providers.get(name="value")
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
        Add or update a service-providers entry.
        
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
            >>> result = fgt.api.system.saml.service_providers.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.system.saml.service_providers.set(
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
        Delete a service-providers entry.
        
        Args:
            name: Name of entry to delete
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.saml.service_providers.delete(name="value")
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
        Replace entire service-providers table.
        
        Args:
            entries: List of entry dicts
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.system.saml.service_providers.put([
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
        Check if a service-providers entry exists.
        
        Args:
            name: Name to check
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.system.saml.service_providers.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name)
        return entry is not None


