from orionis.support.facades.workers import Workers
from orionis.test.exceptions import OrionisTestValueError

class __ValidWorkers:
    """
    Validator for the `max_workers` parameter, ensuring it is a positive integer within the allowed range.
    """

    def __call__(self, max_workers: int) -> int:
        """
        Validate the `max_workers` argument.

        Parameters
        ----------
        max_workers : int
            The number of worker processes or threads to validate.

        Returns
        -------
        int
            The validated `max_workers` value.

        Raises
        ------
        OrionisTestValueError
            If `max_workers` is not a positive integer within the allowed range.
        """
        max_allowed = Workers.calculate()
        if not isinstance(max_workers, int) or max_workers < 1 or max_workers > max_allowed:
            raise OrionisTestValueError(
                f"Invalid max_workers: Expected a positive integer between 1 and {max_allowed}, got '{max_workers}' ({type(max_workers).__name__})."
            )
        return max_workers

# Exported singleton instance
ValidWorkers = __ValidWorkers()