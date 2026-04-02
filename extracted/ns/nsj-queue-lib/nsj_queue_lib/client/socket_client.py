from nsj_queue_lib.client.socket_connection import SocketConnection
from nsj_queue_lib.server.socket_io import SockerIO


class SocketClient(SocketConnection):

    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        self._socket_io = None

    def _get_socket_io(self):
        if self._socket is None:
            raise Exception("Primeiro abra a conexão com o socket")

        if self._socket_io is None:
            self._socket_io = SockerIO(self._socket)

        return self._socket_io

    def try_lock(self, number: int) -> bool:
        msg = f"try_lock({number})"
        resp = self.send_msg(msg, True)

        return resp.upper() == "TRUE"

    def release_lock(self, number: int) -> bool:
        msg = f"release_lock({number})"
        resp = self.send_msg(msg, True)

        return resp.upper() == "TRUE"

    def halt(self) -> bool:
        msg = f"halt()"
        resp = self.send_msg(msg, True)

        return resp.upper() == "TRUE"

    def halt_server(self) -> bool:
        msg = f"halt_server()"
        resp = self.send_msg(msg, True)

        return resp.upper() == "TRUE"

    def sleep(self) -> bool:
        msg = f"sleep()"
        resp = self.send_msg(msg, True)

        return resp.upper() == "TRUE"

    def close(self, notify_close: bool = True):
        if notify_close:
            self._notify_close()

        super().close()

    def _notify_close(self) -> bool:
        msg = f"close()"
        resp = self.send_msg(msg, True)

        return resp.upper() == "TRUE"

    def send_msg(self, message: str, timeout: bool = True, wait_response: bool = True):
        """
        Enviando uma mensagem de texto pelo socket.
        """
        return self._get_socket_io().send_msg(message, wait_response, timeout)

    def listen(self, timeout: bool = True) -> str:
        """
        Esperando uma mensagem de texto pelo socket.
        """
        return self._get_socket_io().listen(timeout)
