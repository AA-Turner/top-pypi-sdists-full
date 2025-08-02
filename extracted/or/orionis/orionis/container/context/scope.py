import contextvars

class ScopedContext:
    """
    Holds scoped instances for the current context.
    """
    _active_scope = contextvars.ContextVar(
        "orionis_scope",
        default=None
    )

    @classmethod
    def getCurrentScope(cls):
        """
        Get the currently active scope.

        Returns
        -------
        object or None
            The current active scope or None if no scope is active.
        """
        return cls._active_scope.get()

    @classmethod
    def setCurrentScope(cls, scope):
        """
        Set the current active scope.

        Parameters
        ----------
        scope : object
            The scope object to set as active.
        """
        cls._active_scope.set(scope)

    @classmethod
    def clear(cls):
        """
        Clear the current active scope.

        Sets the active scope to None.
        """
        cls._active_scope.set(None)