from orionis.test.exceptions import OrionisTestValueError

class __ValidWebReport:
    def __call__(self, web_report) -> bool:
        """
        Validates that the input is a boolean value.

        Parameters
        ----------
        web_report : Any
            The value to be validated as a boolean.

        Returns
        -------
        bool
            The validated boolean value.

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
