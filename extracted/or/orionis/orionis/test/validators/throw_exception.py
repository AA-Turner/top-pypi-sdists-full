from orionis.test.exceptions import OrionisTestValueError

class __ValidThrowException:

    def __call__(self, throw_exception) -> bool:
        """
        Validates that the input is a boolean.

        Parameters
        ----------
        throw_exception : Any
            The value to validate as a boolean.

        Returns
        -------
        bool
            The validated boolean value.

        Raises
        ------
        OrionisTestValueError
            If `throw_exception` is not a boolean.
        """
        if not isinstance(throw_exception, bool):
            raise OrionisTestValueError(
                f"Invalid throw_exception: Expected a boolean, got '{throw_exception}' ({type(throw_exception).__name__})."
            )

        return throw_exception

# Exported singleton instance
ValidThrowException = __ValidThrowException()