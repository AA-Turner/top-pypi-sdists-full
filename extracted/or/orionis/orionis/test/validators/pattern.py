from orionis.test.exceptions import OrionisTestValueError

class __ValidPattern:

    def __call__(self, pattern) -> str:
        """
        Validates that the input is a non-empty string.

        Parameters
        ----------
        pattern : Any
            The value to validate as a non-empty string.

        Returns
        -------
        str
            The validated and stripped string.

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