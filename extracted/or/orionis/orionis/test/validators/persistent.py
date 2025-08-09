from orionis.test.exceptions import OrionisTestValueError

class __ValidPersistent:

    def __call__(self, persistent) -> bool:
        """
        Validates that the input is a boolean value.

        Parameters
        ----------
        persistent : Any
            The value to validate as a boolean.

        Returns
        -------
        bool
            The input value if it is a boolean.

        Raises
        ------
        OrionisTestValueError
            If the input is not a boolean.
        """
        if not isinstance(persistent, bool):
            raise OrionisTestValueError(
                f"Invalid persistent: Expected a boolean, got '{persistent}' ({type(persistent).__name__})."
            )

        return persistent

# Exported singleton instance
ValidPersistent = __ValidPersistent()