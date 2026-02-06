"""
Child Table Helpers for router/bgp

Auto-generated helper classes for managing child tables in singleton endpoints.
Provides intuitive CRUD operations without replacing entire parent config.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from hfortix_fortios.objects import FortiObject

class ConfederationPeersHelper:
    """
    Helper for managing confederation-peers child table in router/bgp.
    
    Confederation peers.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.confederation_peers.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.confederation_peers.get(peer="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.confederation_peers.set(
        ...     peer="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.confederation_peers.delete(peer="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.confederation_peers.exists(peer="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.confederation_peers.put([
        ...     {'peer': "value1"},
        ...     {'peer': "value2"},
        ... ])
    """
    
    def __init__(self, parent: Any):
        """
        Initialize helper.
        
        Args:
            parent: Parent endpoint instance
        """
        self._parent = parent
        self._table_name = 'confederation_peers'
        self._mkey = 'peer'
    
    def get(
        self,
        peer: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get confederation-peers entries.
        
        Args:
            peer: If provided, return only the entry with this peer
            vdom: Virtual domain
            
        Returns:
            List of all entries if peer is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.confederation_peers.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.confederation_peers.get(peer="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if peer is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == peer:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a confederation-peers entry.
        
        If entry with same peer exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include peer)
            
        Returns:
            API response
            
        Raises:
            ValueError: If peer not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.confederation_peers.set(
            ...     peer="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.confederation_peers.set(
            ...     peer="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        peer: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a confederation-peers entry.
        
        Args:
            peer: Peer of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.confederation_peers.delete(peer="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != peer]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire confederation-peers table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.confederation_peers.put([
            ...     {'peer': "value1"},
            ...     {'peer': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        peer: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a confederation-peers entry exists.
        
        Args:
            peer: Peer to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.confederation_peers.exists(peer="value"):
            ...     print("Entry exists")
        """
        entry = self.get(peer=peer, vdom=vdom)
        return entry is not None




class AggregateAddressHelper:
    """
    Helper for managing aggregate-address child table in router/bgp.
    
    BGP aggregate address table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.aggregate_address.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.aggregate_address.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.aggregate_address.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.aggregate_address.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.aggregate_address.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.aggregate_address.put([
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
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get aggregate-address entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.aggregate_address.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.aggregate_address.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a aggregate-address entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.aggregate_address.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.aggregate_address.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a aggregate-address entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.aggregate_address.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire aggregate-address table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.aggregate_address.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a aggregate-address entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.aggregate_address.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class AggregateAddress6Helper:
    """
    Helper for managing aggregate-address6 child table in router/bgp.
    
    BGP IPv6 aggregate address table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.aggregate_address6.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.aggregate_address6.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.aggregate_address6.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.aggregate_address6.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.aggregate_address6.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.aggregate_address6.put([
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
        self._table_name = 'aggregate_address6'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get aggregate-address6 entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.aggregate_address6.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.aggregate_address6.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a aggregate-address6 entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.aggregate_address6.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.aggregate_address6.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a aggregate-address6 entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.aggregate_address6.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire aggregate-address6 table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.aggregate_address6.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a aggregate-address6 entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.aggregate_address6.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class NeighborHelper:
    """
    Helper for managing neighbor child table in router/bgp.
    
    BGP neighbor table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.neighbor.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.neighbor.get(ip="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.neighbor.set(
        ...     ip="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.neighbor.delete(ip="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.neighbor.exists(ip="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.neighbor.put([
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
        self._table_name = 'neighbor'
        self._mkey = 'ip'
    
    def get(
        self,
        ip: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get neighbor entries.
        
        Args:
            ip: If provided, return only the entry with this ip
            vdom: Virtual domain
            
        Returns:
            List of all entries if ip is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.neighbor.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.neighbor.get(ip="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if ip is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == ip:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a neighbor entry.
        
        If entry with same ip exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include ip)
            
        Returns:
            API response
            
        Raises:
            ValueError: If ip not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.neighbor.set(
            ...     ip="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.neighbor.set(
            ...     ip="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        ip: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a neighbor entry.
        
        Args:
            ip: Ip of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor.delete(ip="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != ip]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire neighbor table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor.put([
            ...     {'ip': "value1"},
            ...     {'ip': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        ip: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a neighbor entry exists.
        
        Args:
            ip: Ip to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.neighbor.exists(ip="value"):
            ...     print("Entry exists")
        """
        entry = self.get(ip=ip, vdom=vdom)
        return entry is not None




class NeighborGroupHelper:
    """
    Helper for managing neighbor-group child table in router/bgp.
    
    BGP neighbor group table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.neighbor_group.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.neighbor_group.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.neighbor_group.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.neighbor_group.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.neighbor_group.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.neighbor_group.put([
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
        self._table_name = 'neighbor_group'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get neighbor-group entries.
        
        Args:
            name: If provided, return only the entry with this name
            vdom: Virtual domain
            
        Returns:
            List of all entries if name is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.neighbor_group.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.neighbor_group.get(name="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if name is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == name:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a neighbor-group entry.
        
        If entry with same name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.neighbor_group.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.neighbor_group.set(
            ...     name="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a neighbor-group entry.
        
        Args:
            name: Name of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor_group.delete(name="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != name]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire neighbor-group table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor_group.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a neighbor-group entry exists.
        
        Args:
            name: Name to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.neighbor_group.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name, vdom=vdom)
        return entry is not None




class NeighborRangeHelper:
    """
    Helper for managing neighbor-range child table in router/bgp.
    
    BGP neighbor range table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.neighbor_range.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.neighbor_range.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.neighbor_range.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.neighbor_range.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.neighbor_range.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.neighbor_range.put([
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
        self._table_name = 'neighbor_range'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get neighbor-range entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.neighbor_range.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.neighbor_range.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a neighbor-range entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.neighbor_range.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.neighbor_range.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a neighbor-range entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor_range.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire neighbor-range table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor_range.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a neighbor-range entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.neighbor_range.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class NeighborRange6Helper:
    """
    Helper for managing neighbor-range6 child table in router/bgp.
    
    BGP IPv6 neighbor range table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.neighbor_range6.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.neighbor_range6.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.neighbor_range6.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.neighbor_range6.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.neighbor_range6.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.neighbor_range6.put([
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
        self._table_name = 'neighbor_range6'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get neighbor-range6 entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.neighbor_range6.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.neighbor_range6.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a neighbor-range6 entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.neighbor_range6.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.neighbor_range6.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a neighbor-range6 entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor_range6.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire neighbor-range6 table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.neighbor_range6.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a neighbor-range6 entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.neighbor_range6.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class NetworkHelper:
    """
    Helper for managing network child table in router/bgp.
    
    BGP network table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.network.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.network.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.network.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.network.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.network.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.network.put([
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
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get network entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.network.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.network.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a network entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.network.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.network.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a network entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.network.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire network table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.network.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a network entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.network.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class Network6Helper:
    """
    Helper for managing network6 child table in router/bgp.
    
    BGP IPv6 network table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.network6.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.network6.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.network6.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.network6.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.network6.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.network6.put([
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
        self._table_name = 'network6'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get network6 entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.network6.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.network6.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a network6 entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.network6.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.network6.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a network6 entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.network6.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire network6 table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.network6.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a network6 entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.network6.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class RedistributeHelper:
    """
    Helper for managing redistribute child table in router/bgp.
    
    BGP IPv4 redistribute table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.redistribute.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.redistribute.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.redistribute.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.redistribute.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.redistribute.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.redistribute.put([
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
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get redistribute entries.
        
        Args:
            name: If provided, return only the entry with this name
            vdom: Virtual domain
            
        Returns:
            List of all entries if name is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.redistribute.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.redistribute.get(name="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if name is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == name:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a redistribute entry.
        
        If entry with same name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.redistribute.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.redistribute.set(
            ...     name="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a redistribute entry.
        
        Args:
            name: Name of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.redistribute.delete(name="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != name]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire redistribute table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.redistribute.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a redistribute entry exists.
        
        Args:
            name: Name to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.redistribute.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name, vdom=vdom)
        return entry is not None




class Redistribute6Helper:
    """
    Helper for managing redistribute6 child table in router/bgp.
    
    BGP IPv6 redistribute table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.redistribute6.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.redistribute6.get(name="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.redistribute6.set(
        ...     name="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.redistribute6.delete(name="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.redistribute6.exists(name="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.redistribute6.put([
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
        self._table_name = 'redistribute6'
        self._mkey = 'name'
    
    def get(
        self,
        name: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get redistribute6 entries.
        
        Args:
            name: If provided, return only the entry with this name
            vdom: Virtual domain
            
        Returns:
            List of all entries if name is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.redistribute6.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.redistribute6.get(name="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if name is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == name:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a redistribute6 entry.
        
        If entry with same name exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include name)
            
        Returns:
            API response
            
        Raises:
            ValueError: If name not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.redistribute6.set(
            ...     name="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.redistribute6.set(
            ...     name="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a redistribute6 entry.
        
        Args:
            name: Name of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.redistribute6.delete(name="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != name]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire redistribute6 table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.redistribute6.put([
            ...     {'name': "value1"},
            ...     {'name': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a redistribute6 entry exists.
        
        Args:
            name: Name to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.redistribute6.exists(name="value"):
            ...     print("Entry exists")
        """
        entry = self.get(name=name, vdom=vdom)
        return entry is not None




class AdminDistanceHelper:
    """
    Helper for managing admin-distance child table in router/bgp.
    
    Administrative distance modifications.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.admin_distance.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.admin_distance.get(id="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.admin_distance.set(
        ...     id="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.admin_distance.delete(id="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.admin_distance.exists(id="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.admin_distance.put([
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
        self._table_name = 'admin_distance'
        self._mkey = 'id'
    
    def get(
        self,
        id: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get admin-distance entries.
        
        Args:
            id: If provided, return only the entry with this id
            vdom: Virtual domain
            
        Returns:
            List of all entries if id is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.admin_distance.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.admin_distance.get(id="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if id is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == id:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a admin-distance entry.
        
        If entry with same id exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include id)
            
        Returns:
            API response
            
        Raises:
            ValueError: If id not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.admin_distance.set(
            ...     id="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.admin_distance.set(
            ...     id="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        id: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a admin-distance entry.
        
        Args:
            id: Id of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.admin_distance.delete(id="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != id]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire admin-distance table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.admin_distance.put([
            ...     {'id': "value1"},
            ...     {'id': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        id: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a admin-distance entry exists.
        
        Args:
            id: Id to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.admin_distance.exists(id="value"):
            ...     print("Entry exists")
        """
        entry = self.get(id=id, vdom=vdom)
        return entry is not None




class VrfHelper:
    """
    Helper for managing vrf child table in router/bgp.
    
    BGP VRF leaking table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.vrf.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.vrf.get(vrf="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.vrf.set(
        ...     vrf="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.vrf.delete(vrf="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.vrf.exists(vrf="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.vrf.put([
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
        self._table_name = 'vrf'
        self._mkey = 'vrf'
    
    def get(
        self,
        vrf: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get vrf entries.
        
        Args:
            vrf: If provided, return only the entry with this vrf
            vdom: Virtual domain
            
        Returns:
            List of all entries if vrf is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.vrf.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.vrf.get(vrf="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if vrf is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == vrf:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a vrf entry.
        
        If entry with same vrf exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include vrf)
            
        Returns:
            API response
            
        Raises:
            ValueError: If vrf not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.vrf.set(
            ...     vrf="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.vrf.set(
            ...     vrf="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        vrf: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a vrf entry.
        
        Args:
            vrf: Vrf of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.vrf.delete(vrf="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != vrf]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire vrf table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.vrf.put([
            ...     {'vrf': "value1"},
            ...     {'vrf': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        vrf: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a vrf entry exists.
        
        Args:
            vrf: Vrf to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.vrf.exists(vrf="value"):
            ...     print("Entry exists")
        """
        entry = self.get(vrf=vrf, vdom=vdom)
        return entry is not None




class Vrf6Helper:
    """
    Helper for managing vrf6 child table in router/bgp.
    
    BGP IPv6 VRF leaking table.
    
    Provides intuitive CRUD operations on individual table entries without
    needing to replace the entire parent configuration.
    
    Example:
        >>> # Get all entries
        >>> entries = fgt.api.router.bgp.vrf6.get()
        
        >>> # Get specific entry
        >>> entry = fgt.api.router.bgp.vrf6.get(vrf="value")
        
        >>> # Add or update entry
        >>> result = fgt.api.router.bgp.vrf6.set(
        ...     vrf="value",
        ...     # ... other fields
        ... )
        
        >>> # Delete entry
        >>> result = fgt.api.router.bgp.vrf6.delete(vrf="value")
        
        >>> # Check if entry exists
        >>> exists = fgt.api.router.bgp.vrf6.exists(vrf="value")
        
        >>> # Replace entire table
        >>> result = fgt.api.router.bgp.vrf6.put([
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
        self._table_name = 'vrf6'
        self._mkey = 'vrf'
    
    def get(
        self,
        vrf: str | None = None,
        vdom: str | bool | None = None,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Get vrf6 entries.
        
        Args:
            vrf: If provided, return only the entry with this vrf
            vdom: Virtual domain
            
        Returns:
            List of all entries if vrf is None, specific entry dict if found,
            or None if specific entry not found
            
        Example:
            >>> # Get all entries
            >>> all_entries = fgt.api.router.bgp.vrf6.get()
            
            >>> # Get specific entry
            >>> entry = fgt.api.router.bgp.vrf6.get(vrf="value")
        """
        # Get parent config
        config = self._parent.get(vdom=vdom)
        
        # Extract child table
        entries = getattr(config, self._table_name, [])
        
        # If no filter, return all
        if vrf is None:
            return list(entries) if entries else []
        
        # Find specific entry
        for entry in entries:
            if entry.get(self._mkey) == vrf:
                return dict(entry)
        
        return None
    
    def set(
        self,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
        **kwargs: Any,
    ) -> FortiObject:
        """
        Add or update a vrf6 entry.
        
        If entry with same vrf exists, it will be updated.
        Otherwise, a new entry will be added.
        
        Args:
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            **kwargs: Entry fields (must include vrf)
            
        Returns:
            API response
            
        Raises:
            ValueError: If vrf not provided
            
        Example:
            >>> # Add new entry
            >>> result = fgt.api.router.bgp.vrf6.set(
            ...     vrf="value",
            ...     # ... other fields
            ... )
            
            >>> # Update existing entry
            >>> result = fgt.api.router.bgp.vrf6.set(
            ...     vrf="existing_value",
            ...     field="new_value",
            ... )
        """
        # Validate mkey present
        if self._mkey not in kwargs:
            raise ValueError(f"{self._mkey} is required")
        
        mkey_value = kwargs[self._mkey]
        
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Find and update or append
        found = False
        for i, entry in enumerate(entries):
            if entry.get(self._mkey) == mkey_value:
                # Update existing entry
                entries[i] = {**entry, **kwargs}
                found = True
                break
        
        if not found:
            # Add new entry
            entries.append(kwargs)
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def delete(
        self,
        vrf: str,
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Delete a vrf6 entry.
        
        Args:
            vrf: Vrf of entry to delete
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.vrf6.delete(vrf="value")
        """
        # Get current config
        config = self._parent.get(vdom=vdom)
        
        # Get current entries
        entries = list(getattr(config, self._table_name, []))
        
        # Remove matching entry
        entries = [e for e in entries if e.get(self._mkey) != vrf]
        
        # Put back entire config with updated child table
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = None,
        error_mode: Literal["raise", "return", "print"] | None = None,
        error_format: Literal["detailed", "simple", "code_only"] | None = None,
    ) -> FortiObject:
        """
        Replace entire vrf6 table.
        
        Args:
            entries: List of entry dicts
            vdom: Virtual domain
            error_mode: Error handling mode
            error_format: Error message format
            
        Returns:
            API response
            
        Example:
            >>> result = fgt.api.router.bgp.vrf6.put([
            ...     {'vrf': "value1"},
            ...     {'vrf': "value2"},
            ... ])
        """
        return self._parent.put(
            **{self._table_name: entries},
            vdom=vdom,
            error_mode=error_mode,
            error_format=error_format,
        )
    
    def exists(
        self,
        vrf: str,
        vdom: str | bool | None = None,
    ) -> bool:
        """
        Check if a vrf6 entry exists.
        
        Args:
            vrf: Vrf to check
            vdom: Virtual domain
            
        Returns:
            True if entry exists, False otherwise
            
        Example:
            >>> if fgt.api.router.bgp.vrf6.exists(vrf="value"):
            ...     print("Entry exists")
        """
        entry = self.get(vrf=vrf, vdom=vdom)
        return entry is not None


