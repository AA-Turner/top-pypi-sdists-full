from orionis.foundation.config.testing.enums.mode import ExecutionMode
from orionis.test.exceptions import OrionisTestValueError

class __ValidExecutionMode:

    def __call__(self, execution_mode: str | ExecutionMode) -> str:
        """
        Validate and normalize an execution mode value.

        Parameters
        ----------
        execution_mode : str or ExecutionMode
            The execution mode to validate. Can be a string (case-insensitive) matching
            an ExecutionMode enum member, or an ExecutionMode enum instance.

        Returns
        -------
        str
            The string value of the validated ExecutionMode.

        Raises
        ------
        OrionisTestValueError
            If `execution_mode` is not a string or ExecutionMode enum, or if the string
            does not correspond to a valid ExecutionMode member.
        """

        if not isinstance(execution_mode, (str, ExecutionMode)):
            raise OrionisTestValueError(
                f"Invalid execution_mode: Expected a string or ExecutionMode enum, got '{execution_mode}' ({type(execution_mode).__name__})."
            )

        if isinstance(execution_mode, ExecutionMode):
            return execution_mode.value

        elif isinstance(execution_mode, str):
            if execution_mode.upper() not in ExecutionMode.__members__:
                raise OrionisTestValueError(
                    f"Invalid execution_mode: '{execution_mode}' is not a valid ExecutionMode."
                )
            return ExecutionMode[execution_mode.upper()].value

# Exported singleton instance
ValidExecutionMode = __ValidExecutionMode()