from orionis.test.exceptions import OrionisTestValueError

class __ValidThrowException:

    def __call__(self, throw_exception) -> bool:
        """
        __ValidThrowException is a validator class that ensures the `throw_exception` parameter is a boolean.

        Methods
        -------
        __call__(throw_exception) -> bool
            Validates that the input `throw_exception` is of type `bool`. If not, raises an OrionisTestValueError
            with a descriptive message. Returns the validated boolean value.

        Parameters
        ----------
        throw_exception : Any
            The value to be validated as a boolean.

        Raises
        ------
        OrionisTestValueError
            If `throw_exception` is not a boolean.

        Returns
        -------
        bool
            The validated boolean value of `throw_exception`.
        """

        if not isinstance(throw_exception, bool):
            raise OrionisTestValueError(
                f"Invalid throw_exception: Expected a boolean, got '{throw_exception}' ({type(throw_exception).__name__})."
            )

        return throw_exception

# Exported singleton instance
ValidThrowException = __ValidThrowException()