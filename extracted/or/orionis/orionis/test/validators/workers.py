from orionis.support.facades.workers import Workers
from orionis.test.exceptions import OrionisTestValueError

class __ValidWorkers:
    """
    Validator that ensures max_workers is a positive integer within allowed range.
    """

    def __call__(self, max_workers: int) -> int:
        """
        Ensures that the provided max_workers is a positive integer within allowed range.

        Parameters
        ----------
        max_workers : int
            The max_workers value to validate.

        Raises
        ------
        OrionisTestValueError
            If max_workers is not a positive integer within allowed range.
        """
        max_allowed = Workers.calculate()
        if not isinstance(max_workers, int) or max_workers < 1 or max_workers > max_allowed:
            raise OrionisTestValueError(
                f"Invalid max_workers: Expected a positive integer between 1 and {max_allowed}, got '{max_workers}' ({type(max_workers).__name__})."
            )
        return max_workers

# Exported singleton instance
ValidWorkers = __ValidWorkers()