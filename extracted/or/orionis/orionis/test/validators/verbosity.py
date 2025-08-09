from orionis.foundation.config.testing.enums.verbosity import VerbosityMode
from orionis.test.exceptions import OrionisTestValueError

class __ValidVerbosity:
    """
    Validator for verbosity levels, ensuring the input is a non-negative integer corresponding to a valid
    VerbosityMode value or an instance of VerbosityMode.

    This class is intended to validate verbosity arguments for test configuration.
    """

    def __call__(self, verbosity) -> int:
        """
        Validate the verbosity level.

        Parameters
        ----------
        verbosity : int or VerbosityMode
            The verbosity level to validate. Must be a non-negative integer matching a VerbosityMode value,
            or an instance of VerbosityMode.

        Returns
        -------
        int
            The validated verbosity level as an integer.

        Raises
        ------
        OrionisTestValueError
            If the verbosity is not a non-negative integer corresponding to a VerbosityMode value,
            nor an instance of VerbosityMode.
        """
        if isinstance(verbosity, VerbosityMode):
            return verbosity.value
        if isinstance(verbosity, int) and verbosity >= 0:
            if verbosity in [mode.value for mode in VerbosityMode]:
                return verbosity
            else:
                raise OrionisTestValueError(
                    f"Invalid verbosity level: {verbosity} is not a valid VerbosityMode value."
                )
        raise OrionisTestValueError(
            f"Invalid verbosity level: Expected a non-negative integer or VerbosityMode, got '{verbosity}' ({type(verbosity).__name__})."
        )

# Exported singleton instance
ValidVerbosity = __ValidVerbosity()