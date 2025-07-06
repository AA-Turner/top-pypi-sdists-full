from supervisor.childutils import listener
from typing import BinaryIO, Dict, Tuple, NoReturn
from sys import stdin as sys_stdin, stderr as sys_stderr, stdout as sys_stdout


class CommunicationChannels:
    def __init__(
            self,
            *,
            stdout: BinaryIO = sys_stdout,
            stderr: BinaryIO = sys_stderr,
            stdin: BinaryIO = sys_stdin) -> None:
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr


class ProcessCommunicationEventHandler:
    def __init__(self, channels: CommunicationChannels = None) -> None:
        self.__channels = channels or CommunicationChannels()

    def handle_single_event(self) -> None:
        event_data: Tuple[Dict[str, str], str] = listener.wait(
            self.__channels.stdin,
            self.__channels.stdout)
        headers, payload = event_data
        listener.send(payload, self.__channels.stdout)

    def run_forever(self) -> NoReturn:
        while True:
            self.handle_single_event()
