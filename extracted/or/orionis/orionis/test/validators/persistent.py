from orionis.test.exceptions import OrionisTestValueError

class __ValidPersistent:

    def __call__(self, persistent) -> bool:
        """
        Validator that ensures the `persistent` parameter is a boolean.

        This class is intended to be used as a callable validator to check if the
        provided value for `persistent` is of type `bool`. If the value is not a
        boolean, an `OrionisTestValueError` is raised.

        Methods
        -------
        __call__(persistent) -> bool
            Validates that `persistent` is a boolean.

        Parameters
        ----------
        persistent : Any
            The value to be validated as a boolean.

        Returns
        -------
        bool
            Returns the value of `persistent` if it is a boolean.

        Raises
        ------
        OrionisTestValueError
            If `persistent` is not a boolean.
        """

        if not isinstance(persistent, bool):
            raise OrionisTestValueError(
                f"Invalid persistent: Expected a boolean, got '{persistent}' ({type(persistent).__name__})."
            )

        return persistent

# Exported singleton instance
ValidPersistent = __ValidPersistent()