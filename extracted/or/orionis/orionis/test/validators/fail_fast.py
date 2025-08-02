from orionis.test.exceptions import OrionisTestValueError

class __ValidFailFast:

    def __call__(self, fail_fast) -> bool:
        """
        Validator that ensures the `fail_fast` parameter is a boolean.

        This class is intended to be used as a callable validator to check that the
        provided `fail_fast` argument is of type `bool`. If the value is not a boolean,
        an `OrionisTestValueError` is raised with a descriptive error message.

        Parameters
        ----------
        fail_fast : Any
            The value to be validated as a boolean.

        Returns
        -------
        bool
            The validated boolean value of `fail_fast`.

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
