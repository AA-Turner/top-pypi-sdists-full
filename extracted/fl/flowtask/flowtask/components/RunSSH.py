import asyncio
from collections.abc import Callable
import logging
import asyncssh
from .flow import FlowComponent
from ..interfaces.SSHClient import SSHClient


class RunSSH(SSHClient, FlowComponent):
    """
    RunSSH.

    Run any arbitrary command into an SSH server.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          RunSSH:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Start.

        Processing variables and credentials.
        """
        try:
            self.define_host()
            self.processing_credentials()
        except Exception as err:
            logging.error(err)
            raise

    async def run(self):
        result = {}
        await self.open(
            host=self.host,
            port=self.port,
            tunnel=self.tunnel,
            credentials=self.credentials,
        )
        for command in self.commands:
            command = self.mask_replacement(command)
            try:
                rst = await self._connection.run(command, check=True)
                result[command] = {
                    "exit_status": rst.exit_status,
                    "returncode": rst.returncode,
                    "error": rst.stderr,
                    # "stdout": rst.stdout
                }
            except asyncssh.process.ProcessError as err:
                logging.error(f"Error executing command: {err}")
        self.add_metric("SSH: COMMAND", result)
        self._result = result
        return result
