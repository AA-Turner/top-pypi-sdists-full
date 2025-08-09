import contextvars

class ScopedContext:
    """
    Manages scoped instances using Python's context variables, allowing for context-local storage of active scopes.
    """

    _active_scope = contextvars.ContextVar(
        "orionis_context_scope",
        default=None
    )

    @classmethod
    def getCurrentScope(cls):
        """
        Retrieve the currently active scope for the current context.

        Returns
        -------
        object or None
            The currently active scope object, or None if no scope is set.
        """
        return cls._active_scope.get()

    @classmethod
    def setCurrentScope(cls, scope):
        """
        Set the active scope for the current context.

        Parameters
        ----------
        scope : object
            The scope object to be set as the active scope for the current context.
        """
        cls._active_scope.set(scope)

    @classmethod
    def clear(cls):
        """
        Clear the active scope for the current context.

        Resets the active scope to None.
        """
        cls._active_scope.set(None)