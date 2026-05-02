from collections.abc import Callable
import asyncio
from asyncdb.utils.functions import colors, cPrint
from ..utils import SafeDict
from .flow import FlowComponent


class PrintMessage(FlowComponent):
    """
    PrintMessage

        Overview

            This component prints a formatted message to the console with optional coloring and logging.

        :widths: auto


        | message     |   Yes    | The message to print, with optional variable substitution.        |
        | color       |   No     | The color to use for the message. Overrides the level-based color.|
        | level       |   No     | The log level of the message ("INFO", "DEBUG", "WARN", "ERROR",   |
        |             |          | "CRITICAL"). Default is "INFO".                                   |
        | condition   |   No     | A condition to evaluate before printing the message. The message  |
        |             |          | is printed only if the condition is True.                         |
        |  first      |   Yes    | First message                                                     |
        |  last       |   Yes    | Last message                                                      |

        Returns

        This component returns the printed message.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PrintMessage:
          message: 'End Form Metadata: {orgid}/{formid}'
          color: green
          level: WARN
        ```
    """
    _version = "1.0.0"

    coloring = None
    color = None
    level = "INFO"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.message: str = kwargs.get("message", '')
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Initialize the color setup."""
        if self.previous:
            self.data = self.input
        try:
            if self.color:
                try:
                    self.coloring = colors.bold + getattr(colors.fg, self.color)
                except Exception as err:
                    self._logger.error(f"Wrong color schema {self.color}, error: {err}")
                    self.coloring = colors.reset
            elif self.level:
                if self.level == "INFO":
                    self.coloring = colors.bold + colors.fg.green
                elif self.level == "DEBUG":
                    self.coloring = colors.fg.lightblue
                elif self.level == "WARN":
                    self.coloring = colors.bold + colors.fg.yellow
                elif self.level == "ERROR":
                    self.coloring = colors.fg.lightred
                elif self.level == "CRITICAL":
                    self.coloring = colors.bold + colors.fg.red
                else:
                    self.coloring = colors.reset
            else:
                self.coloring = colors.reset
            return True
        except (NameError, ValueError):
            self.coloring = colors.reset

    async def run(self):
        """Run Message."""
        self._result = self.data
        try:
            if hasattr(self, "condition"):
                for val in self._variables:
                    self.condition = self.condition.replace(
                        "{{{}}}".format(str(val)), str(self._variables[val])
                    )
                # if not eval(self.condition):  # pylint: disable=W0123
                #     return False
            msg = self.message.format_map(SafeDict(**self._params))
            for val in self._variables:
                msg = msg.replace("{{{}}}".format(str(val)), str(self._variables[val]))
            print(self.coloring + msg, colors.reset)
            if self._debug:
                self._logger.debug(msg)
            if "PRINT_MESSAGE" not in self._variables:
                self._variables["PRINT_MESSAGE"] = {}
            if self.level not in self._variables["PRINT_MESSAGE"]:
                self._variables["PRINT_MESSAGE"][self.level] = []
            self._variables["PRINT_MESSAGE"][self.level].append(msg)
            self.add_metric("message", msg)
        except Exception as err:
            self._logger.exception(f"PrintMessage Error: {err}")
            return False
        return self._result

    async def close(self):
        """Method."""
