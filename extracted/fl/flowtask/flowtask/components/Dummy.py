from ..utils import cPrint, SafeDict
from .flow import FlowComponent


class Dummy(FlowComponent):
    """
    Dummy.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Dummy:
          # attributes here
        ```
    """
    _version = "1.0.0"
    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        

        Example:

        ```yaml
        Dummy:
          message: 'Dummy Date: {firstdate} and {lastdate}'
          masks:
            firstdate:
            - date_diff_dow
            - day_of_week: monday
              diff: 8
              mask: '%Y-%m-%d'
            lastdate:
            - date_diff_dow
            - day_of_week: monday
              diff: 2
              mask: '%Y-%m-%d'
        ```

    """
        return True

    async def run(self):
        """
        run.

        Close (if needed) a task
        """
        try:
            self.message = self.message.format_map(SafeDict(**self._mask))
            cPrint(f"Message IS: {self.message}")
            self.add_metric("message", self.message)
        except Exception:
            self.save_traceback()
            raise
        return True

    async def close(self):
        """
        close.

        Close (if needed) a task
        """

    def save_stats(self):
        """
        Extension to save stats for this component
        """
