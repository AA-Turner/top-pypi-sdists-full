from orionis.test.exceptions import OrionisTestValueError

class __ValidPrintResult:

    def __call__(self, print_result) -> bool:
        """
        Validator that ensures the `print_result` parameter is a boolean.

        This class is intended to be used as a callable validator to check that the
        provided `print_result` argument is of type `bool`. If the validation fails,
        an `OrionisTestValueError` is raised.

        Parameters
        ----------
        print_result : Any
            The value to be validated as a boolean.

        Returns
        -------
        bool
            Returns the validated boolean value of `print_result`.

        Raises
        ------
        OrionisTestValueError
            If `print_result` is not of type `bool`.
        """

        if not isinstance(print_result, bool):
            raise OrionisTestValueError(
                f"Invalid print_result: Expected a boolean, got '{print_result}' ({type(print_result).__name__})."
            )

        return print_result

# Exported singleton instance
ValidPrintResult = __ValidPrintResult()
