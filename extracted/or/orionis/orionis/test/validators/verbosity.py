from orionis.foundation.config.testing.enums.verbosity import VerbosityMode
from orionis.test.exceptions import OrionisTestValueError

class __ValidVerbosity:
    """
    Validator that ensures the verbosity level is a non-negative integer or a valid VerbosityMode.
    """

    def __call__(self, verbosity) -> int:
        """
        Ensures that the provided verbosity is a non-negative integer or a valid VerbosityMode.

        Parameters
        ----------
        verbosity : int or VerbosityMode
            The verbosity level to validate.

        Raises
        ------
        OrionisTestValueError
            If the verbosity is not a non-negative integer or a valid VerbosityMode.
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
