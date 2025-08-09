from orionis.container.context.scope import ScopedContext

class ScopeManager:
    """
    Manages scoped lifetimes for instances within a container context.

    This class acts as a context manager to handle the storage, retrieval,
    and cleanup of instances associated with a specific scope. It provides
    dictionary-like access to instances and ensures proper scope activation
    and cleanup when used in a context.
    """

    def __init__(self):
        """
        Initialize the ScopeManager.

        Initializes an empty dictionary to store scoped instances.
        """
        self._instances = {}

    def __getitem__(self, key):
        """
        Retrieve an instance associated with the given key.

        Parameters
        ----------
        key : hashable
            The key identifying the instance.

        Returns
        -------
        object or None
            The instance associated with the key, or None if not found.
        """
        return self._instances.get(key)

    def __setitem__(self, key, value):
        """
        Store an instance under the specified key.

        Parameters
        ----------
        key : hashable
            The key to associate with the instance.
        value : object
            The instance to store.
        """
        self._instances[key] = value

    def __contains__(self, key):
        """
        Check if an instance exists for the given key.

        Parameters
        ----------
        key : hashable
            The key to check for existence.

        Returns
        -------
        bool
            True if the key exists in the scope, False otherwise.
        """
        return key in self._instances

    def clear(self):
        """
        Remove all instances from the current scope.

        Clears the internal dictionary of all stored instances.
        """
        self._instances.clear()

    def __enter__(self):
        """
        Activate this scope as the current context.

        Sets this ScopeManager as the active scope in ScopedContext.

        Returns
        -------
        ScopeManager
            The current ScopeManager instance.
        """
        ScopedContext.setCurrentScope(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Deactivate the current scope and perform cleanup.

        Clears all stored instances and resets the active scope in ScopedContext.

        Parameters
        ----------
        exc_type : type or None
            The exception type if an exception was raised, otherwise None.
        exc_val : Exception or None
            The exception instance if an exception was raised, otherwise None.
        exc_tb : traceback or None
            The traceback if an exception was raised, otherwise None.
        """
        self.clear()
        ScopedContext.clear()