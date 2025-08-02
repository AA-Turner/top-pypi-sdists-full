from orionis.foundation.config.testing.enums.drivers import PersistentDrivers
from orionis.test.exceptions import OrionisTestValueError

class __ValidPersistentDriver:

    def __call__(self, persistent_driver) -> str:
        """
        Validator class for persistent driver types.
        This class is intended to validate the value of a persistent driver, ensuring
        that it is a string or PersistentDrivers enum and one of the accepted values.
        Methods
        -------
        __call__(persistent_driver: str | PersistentDrivers) -> str
            Validates the given persistent driver. Raises an OrionisTestValueError if
            the input is not a string or enum or not one of the accepted values.
        Parameters
        ----------
        persistent_driver : str | PersistentDrivers
            The persistent driver to validate. Must be either 'sqlite', 'json', or the corresponding enum.
        Returns
        -------
        str
            The validated persistent driver as a string.
        Raises
        ------
        OrionisTestValueError
            If the input is not a string/enum or not one of the accepted values.
        """

        if not isinstance(persistent_driver, (str, PersistentDrivers)):
            raise OrionisTestValueError(
            f"Invalid type for persistent_driver: Expected str or PersistentDrivers, got {type(persistent_driver).__name__}."
            )
        if isinstance(persistent_driver, PersistentDrivers):
            return persistent_driver.value
        if persistent_driver in [e.value for e in PersistentDrivers]:
            return persistent_driver
        raise OrionisTestValueError(
            f"Invalid persistent_driver: Expected one of {[e.value for e in PersistentDrivers]}, got '{persistent_driver}'."
        )

# Export the validator instance singleton
ValidPersistentDriver = __ValidPersistentDriver()