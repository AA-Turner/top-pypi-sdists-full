from collections.abc import Callable
import asyncio
import asyncssh
from ..exceptions import ComponentError
from .RunSSH import RunSSH


class Rsync(RunSSH):
    """
    Rsync.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Rsync:
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
        self.flags: str = "azrv"
        super(Rsync, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        super(Rsync, self).start(**kwargs)
        if hasattr(self, "source"):  # using the destination filosophy
            try:
                if hasattr(self, "masks"):
                    self.source_dir = self.mask_replacement(self.source["directory"])
                else:
                    self.source_dir = self.source["directory"]
            except KeyError as exc:
                raise ComponentError(
                    "Rsync Error: you must specify a source directory"
                ) from exc
        if hasattr(self, "destination"):
            if hasattr(self, "masks"):
                self.destination_dir = self.mask_replacement(
                    self.destination["directory"]
                )
            else:
                self.destination_dir = self.destination["directory"]
            # also, calculate the destination server:
            self.dest_server = self.mask_replacement(self.destination["server"])
            self.dest_user = self.mask_replacement(self.destination["user"])
            try:
                self.dest_port = self.mask_replacement(self.destination["port"])
            except KeyError:
                self.dest_port = None
        return True

    async def run(self):
        await self.open(
            host=self.host,
            port=self.port,
            tunnel=self.tunnel,
            credentials=self.credentials,
        )
        rsync = "rsync -{flags} {source} {destination}"
        if self.dest_port is not None:
            rsync = rsync + f" --port={self.dest_port}"
        destination = f"{self.dest_user}@{self.dest_server}:{self.destination_dir}"
        command = rsync.format(
            flags=self.flags, destination=destination, source=self.source_dir
        )
        try:
            rst = await self._connection.run(command, check=True)
            result = {
                "exit_status": rst.exit_status,
                "returncode": rst.returncode,
                "error": rst.stderr,
                # "stdout": rst.stdout
            }
        except asyncssh.process.ProcessError as err:
            self._logger.error(f"Error executing command: {err}")
        self.add_metric("SSH: COMMAND", command)
        self.add_metric("SSH: RESULT", result)
        self._result = result
        return result
