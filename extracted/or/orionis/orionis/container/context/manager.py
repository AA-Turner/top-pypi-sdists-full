from orionis.container.context.scope import ScopedContext

class ScopeManager:
    """
    A context manager to manage scoped lifetimes in the container.
    """
    def __init__(self):
        """
        Initialize a new ScopeManager with an empty instances dictionary.
        """
        self._instances = {}

    def __getitem__(self, key):
        """
        Get an instance by key.

        Parameters
        ----------
        key : hashable
            The key of the instance to retrieve.

        Returns
        -------
        object or None
            The instance associated with the key or None if not found.
        """
        return self._instances.get(key)

    def __setitem__(self, key, value):
        """
        Store an instance by key.

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
        Check if a key exists in this scope.

        Parameters
        ----------
        key : hashable
            The key to check.

        Returns
        -------
        bool
            True if the key exists in the scope, False otherwise.
        """
        return key in self._instances

    def clear(self):
        """
        Clear all instances from this scope.
        """
        self._instances.clear()

    def __enter__(self):
        """
        Enter the scope context.

        Sets this scope as the current active scope.

        Returns
        -------
        ScopeManager
            This scope manager instance.
        """
        ScopedContext.setCurrentScope(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the scope context.

        Clears this scope and the active scope reference.

        Parameters
        ----------
        exc_type : type or None
            The exception type if an exception was raised, None otherwise.
        exc_val : Exception or None
            The exception instance if an exception was raised, None otherwise.
        exc_tb : traceback or None
            The exception traceback if an exception was raised, None otherwise.
        """
        self.clear()
        ScopedContext.clear()