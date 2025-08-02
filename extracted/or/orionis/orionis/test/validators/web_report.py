from orionis.test.exceptions import OrionisTestValueError

class __ValidWebReport:

    def __call__(self, web_report) -> bool:
        """
        Validator class to check if the input is a boolean value.
        This class is intended to be used as a callable to validate whether the provided
        `web_report` argument is of type `bool`. If the input is not a boolean, an
        `OrionisTestValueError` is raised with a descriptive error message.

        Parameters
        ----------
        None

        Methods
        -------
        __call__(web_report)
            Validates that `web_report` is a boolean value.

        Raises
        ------
        OrionisTestValueError
            If `web_report` is not of type `bool`.
        """

        if not isinstance(web_report, bool):
            raise OrionisTestValueError(
                f"Invalid web_report: Expected a boolean, got '{web_report}' ({type(web_report).__name__})."
            )

        return web_report

# Exported singleton instance
ValidWebReport = __ValidWebReport()
