from orionis.test.exceptions import OrionisTestValueError

class __ValidNamePattern:

    def __call__(self, test_name_pattern) -> str:
        """
        Validates that the input is a non-empty string.

        Parameters
        ----------
        test_name_pattern : Any
            The value to validate as a non-empty string.

        Returns
        -------
        str
            The validated and stripped string if valid, otherwise returns the original value if None.

        Raises
        ------
        OrionisTestValueError
            If `test_name_pattern` is not a non-empty string.
        """
        if test_name_pattern is not None:

            if not isinstance(test_name_pattern, str) or not test_name_pattern.strip():
                raise OrionisTestValueError(
                    f"Invalid test_name_pattern: Expected a non-empty string, got '{str(test_name_pattern)}' ({type(test_name_pattern).__name__})."
                )
            return test_name_pattern.strip()

        return test_name_pattern

# Exported singleton instance
ValidNamePattern = __ValidNamePattern()