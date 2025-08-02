from orionis.test.exceptions import OrionisTestValueError

class __ValidNamePattern:

    def __call__(self, test_name_pattern) -> str:
        """
        Validator that ensures the `test_name_pattern` parameter is a non-empty string.

        This class is intended to be used as a callable validator to check that the
        provided `test_name_pattern` argument is a non-empty string. If the value is not a valid
        string, an `OrionisTestValueError` is raised with a descriptive error message.

        Parameters
        ----------
        test_name_pattern : Any
            The value to be validated as a non-empty string.

        Returns
        -------
        str
            The validated and stripped string value of `test_name_pattern`.

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
