from orionis.test.exceptions import OrionisTestValueError

class __ValidModuleName:

    def __call__(self, module_name) -> str:
        """
        Validates that the input is a non-empty string.

        Parameters
        ----------
        module_name : Any
            The value to validate as a non-empty string.

        Returns
        -------
        str
            The validated and stripped string value of `module_name`.

        Raises
        ------
        OrionisTestValueError
            If `module_name` is not a non-empty string.
        """
        if not module_name or not isinstance(module_name, str):
            raise OrionisTestValueError(
                f"Invalid module_name: Expected a non-empty string, got '{module_name}' ({type(module_name).__name__})."
            )
        return module_name

# Exported singleton instance
ValidModuleName = __ValidModuleName()