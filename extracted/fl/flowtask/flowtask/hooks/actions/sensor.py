from .abstract import AbstractAction
from ...utils import cPrint

class ProcessSensorData(AbstractAction):
    """ProcessSensorData.

    WIP example of to process Sensor data from MQTTT service.
    """

    async def open(self):
        cPrint('Opening Action on Process.')

    async def run(self, hook, *args, **kwargs):
        print(
            f"Running action from hook {hook} with arguments:",
            args,
            self._args,
            kwargs,
            self._kwargs
        )

    async def close(self):
        cPrint("Closing Action on Process.")
