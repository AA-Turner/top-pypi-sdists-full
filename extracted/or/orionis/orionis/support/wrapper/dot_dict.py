from typing import Any, Optional, Dict

class DotDict(dict):

    __slots__ = ()

    def __getattr__(self, key: str) -> Optional[Any]:
        """
        Retrieve the value associated with the given key as an attribute.

        If the value is a dictionary (but not already a DotDict), it is converted
        to a DotDict and updated in-place. If the key does not exist, returns None.

        Parameters
        ----------
        key : str
            The attribute name to retrieve.

        Returns
        -------
        Any or None
            The value associated with the key. If the value is a dict, it is converted
            to a DotDict before returning. Returns None if the key is not present.

        Notes
        -----
        This method allows attribute-style access to dictionary keys. If the value
        is a plain dictionary, it is automatically wrapped as a DotDict for consistency.
        """
        try:
            value = self[key]  # Attempt to retrieve the value by key
            # Convert plain dicts to DotDict for attribute access
            if isinstance(value, dict) and not isinstance(value, DotDict):
                value = DotDict(value)
                self[key] = value  # Update the value in-place
            return value
        except KeyError:
            # Return None if the key does not exist
            return None

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Assign a value to an attribute of the DotDict instance.

        This method enables attribute-style assignment for dictionary keys. If the
        assigned value is a plain dictionary (not a DotDict), it is automatically
        converted to a DotDict for consistency and recursive attribute access.

        Parameters
        ----------
        key : str
            The attribute name to assign.
        value : Any
            The value to assign to the attribute. If it is a dict (but not a DotDict),
            it will be converted to a DotDict before assignment.

        Returns
        -------
        None
            This method does not return a value.

        Notes
        -----
        The attribute is stored as a key-value pair in the underlying dictionary.
        This allows seamless attribute-style access and assignment for dictionary keys.
        """

        # Convert plain dicts to DotDict for recursive attribute access
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)

        # Store the value in the underlying dictionary using the key
        self[key] = value

    def __delattr__(self, key: str) -> None:
        """
        Remove an attribute from the DotDict instance.

        This method deletes the key-value pair corresponding to the given attribute name
        from the underlying dictionary. If the key does not exist, an AttributeError is raised.

        Parameters
        ----------
        key : str
            The name of the attribute to remove.

        Returns
        -------
        None
            This method does not return a value.

        Raises
        ------
        AttributeError
            If the specified attribute does not exist in the DotDict.

        Notes
        -----
        This method enables attribute-style deletion for dictionary keys, allowing
        seamless removal of items using dot notation.
        """
        try:
            # Attempt to delete the key from the dictionary
            del self[key]
        except KeyError as e:
            # Raise AttributeError if the key is not present
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'") from e

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """
        Retrieve the value associated with the given key, returning a default value if the key is not found.

        If the retrieved value is a plain dictionary (not a DotDict), it is converted to a DotDict,
        stored back in the dictionary, and then returned. This ensures consistent attribute-style access
        for nested dictionaries.

        Parameters
        ----------
        key : str
            The key to look up in the dictionary.
        default : Any, optional
            The value to return if the key is not found. Defaults to None.

        Returns
        -------
        Any or None
            The value associated with the key, converted to a DotDict if it is a dict.
            If the key is not present, returns the specified default value.

        Notes
        -----
        This method overrides the standard dict.get() to provide automatic conversion of nested
        dictionaries to DotDict instances, enabling recursive attribute-style access.
        """
        # Retrieve the value using the base dict's get method
        value = super().get(key, default)
        # If the value is a plain dict, convert it to DotDict for consistency
        if isinstance(value, dict) and not isinstance(value, DotDict):
            value = DotDict(value)
            self[key] = value  # Store the converted value back in the dictionary
        return value

    def export(self) -> Dict[str, Any]:
        """
        Recursively export the contents of the DotDict as a standard Python dictionary.

        This method traverses the DotDict and converts all nested DotDict instances
        into regular dictionaries by recursively calling their `export` method.
        Non-DotDict values are included as-is. This ensures that the returned object
        is composed entirely of built-in Python types, making it suitable for serialization
        or interoperability with code expecting standard dictionaries.

        Parameters
        ----------
        None

        Returns
        -------
        result : dict
            A dictionary representation of the DotDict, where all nested DotDict instances
            are recursively converted to dictionaries. Non-DotDict values are returned unchanged.

        Notes
        -----
        This method is useful for converting a DotDict (which supports attribute-style access)
        into a plain dictionary for use with APIs, serialization, or other libraries that
        require standard dict objects.
        """
        result = {}
        # Iterate through all key-value pairs in the DotDict
        for k, v in self.items():
            if isinstance(v, DotDict):
                # Recursively export nested DotDicts
                result[k] = v.export()
            else:
                # Include non-DotDict values as-is
                result[k] = v
        return result

    def copy(self) -> 'DotDict':
        """
        Create a deep copy of the DotDict instance, recursively copying all nested DotDict and dict objects.

        This method traverses the DotDict and ensures that all nested DotDict and dict instances are
        copied recursively, so that the returned DotDict is fully independent of the original. Non-dict
        values are copied by reference.

        Returns
        -------
        DotDict
            A new DotDict instance containing a deep copy of the original contents. All nested DotDict
            and dict objects are recursively copied, ensuring no shared references with the original.

        Notes
        -----
        This method is useful when you need a completely independent copy of a DotDict, including all
        nested structures, to avoid unintended side effects from shared references.
        """
        copied = {}
        # Iterate through all key-value pairs in the DotDict
        for k, v in self.items():
            if isinstance(v, DotDict):
                # Recursively copy nested DotDict instances
                copied[k] = v.copy()
            elif isinstance(v, dict):
                # Convert plain dicts to DotDict and recursively copy
                copied[k] = DotDict(v).copy()
            else:
                # Copy non-dict values by reference
                copied[k] = v
        # Return a new DotDict containing the copied data
        return DotDict(copied)

    def __repr__(self) -> str:
        """
        Return a string representation of the DotDict instance.

        This method overrides the default `__repr__` implementation to provide a concise
        and informative string that displays the class name (`DotDict`) and the contents
        of the underlying dictionary. This is useful for debugging and logging, as it
        clearly distinguishes DotDict objects from regular dictionaries.

        Returns
        -------
        str
            A string representation of the DotDict object, formatted as
            'DotDict({...})', where {...} is the dictionary content.

        Notes
        -----
        The returned string uses the base dictionary's representation, but is prefixed
        with the DotDict class name for clarity.
        """
        # Use the base dict's __repr__ for the contents, but keep DotDict class name
        return super().__repr__()