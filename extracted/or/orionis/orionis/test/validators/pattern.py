from orionis.test.exceptions import OrionisTestValueError

class __ValidPattern:

    def __call__(self, pattern) -> str:
        """
        Validator that ensures the `pattern` parameter is a non-empty string.

        This class is intended to be used as a callable validator to check that the
        provided `pattern` argument is a non-empty string. If the value is not a valid
        string, an `OrionisTestValueError` is raised with a descriptive error message.

        Parameters
        ----------
        pattern : Any
            The value to be validated as a non-empty string.

        Returns
        -------
        str
            The validated and stripped string value of `pattern`.

        Raises
        ------
        OrionisTestValueError
            If `pattern` is not a non-empty string.
        """

        if not isinstance(pattern, str) or not pattern.strip():
            raise OrionisTestValueError(
                f"Invalid pattern: Expected a non-empty string, got '{str(pattern)}' ({type(pattern).__name__})."
            )
        return pattern.strip()

# Exported singleton instance
ValidPattern = __ValidPattern()
