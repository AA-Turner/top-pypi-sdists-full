from .abstract import AbstractAction
from ...utils import cPrint

class DummyAction(AbstractAction):
    """DummyAction.

    Simply Print the Action object.
    """

    async def open(self):
        cPrint('Opening Action on Dummy.')

    async def run(self, hook, *args, **kwargs):
        print(
            f"Running action from hook {hook} with arguments:",
            args,
            self._args,
            kwargs,
            self._kwargs
        )

    async def close(self):
        cPrint("Closing Action on Dummy.")
