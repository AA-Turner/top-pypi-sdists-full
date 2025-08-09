from orionis.test.exceptions import OrionisTestValueError

class __ValidFailFast:

    def __call__(self, fail_fast) -> bool:
        """
        Validates that the `fail_fast` parameter is a boolean.

        Parameters
        ----------
        fail_fast : Any
            The value to validate as a boolean.

        Returns
        -------
        bool
            The validated boolean value.

        Raises
        ------
        OrionisTestValueError
            If `fail_fast` is not of type `bool`.
        """

        if not isinstance(fail_fast, bool):
            raise OrionisTestValueError(
                f"Invalid fail_fast: Expected a boolean, got '{fail_fast}' ({type(fail_fast).__name__})."
            )

        return fail_fast

# Exported singleton instance
ValidFailFast = __ValidFailFast()