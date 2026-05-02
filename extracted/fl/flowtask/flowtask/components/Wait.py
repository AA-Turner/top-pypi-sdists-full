import asyncio
from .flow import FlowComponent


class Wait(FlowComponent):
    """
    Wait.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Wait:
          # attributes here
        ```
    """
    _version = "1.0.0"
    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        return True

    async def close(self):
        pass

    async def run(self):
        await asyncio.sleep(self.wait)
        self.add_metric("WAIT", self.wait)
        self._result = self.data
        return self._result
