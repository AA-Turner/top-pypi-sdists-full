"""One owned spawned rank process and its private coordination channel."""

from dataclasses import dataclass
from multiprocessing.connection import Connection
from multiprocessing.process import BaseProcess


@dataclass(frozen=True)
class RankProcess:
    """Reap the physical rank before its logical group's scientific grant is disarmed."""

    rank: int
    process: BaseProcess
    channel: Connection

    def close(self) -> None:
        """Kill an unfinished rank, join its exit, then release only owned handles."""
        try:
            if self.process.pid is not None:
                if self.process.exitcode is None:
                    self.process.kill()
                self.process.join()
        finally:
            self.channel.close()
            self.process.close()
