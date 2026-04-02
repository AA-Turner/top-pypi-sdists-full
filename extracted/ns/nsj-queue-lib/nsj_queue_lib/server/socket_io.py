import socket
import threading

from nsj_queue_lib.settings import END_MARK, SOCKET_BUFFER_SIZE, TIMEOUT_SOCKET_MESSAGE


class MissedSocketException(Exception):
    pass


class GenericSocketException(Exception):
    pass


class TimeoutSocketException(Exception):
    pass


class SockerIO:

    def __init__(self, socket: socket.socket) -> None:
        super().__init__()
        self._socket = socket
        self.mutex_lock = threading.Lock()

    def send_msg(self, message: str, wait_response: bool, timeout: bool):
        """
        Enviando uma mensagem de texto pelo socket.
        """
        try:
            # Pegando um mutex para acessar o socket
            with self.mutex_lock:
                # Formatando a mensagem para envio
                msg = f"{message}{END_MARK}"

                # Configurando um timeout para confirmação da entrega
                if timeout:
                    self._socket.settimeout(TIMEOUT_SOCKET_MESSAGE)

                # Enviando a mensagem
                self._socket.sendall(bytes(msg, "utf-8"))

                # Retornando a resposta
                if wait_response:
                    return self._receive(True)
        except socket.timeout as e:
            raise TimeoutSocketException(e)
        except socket.error as e:
            raise GenericSocketException(e)

    def listen(self, timeout: bool = True) -> str:
        """
        Esperando uma mensagem de texto pelo socket.
        """
        try:
            # Pegando um mutex para acessar o socket
            with self.mutex_lock:
                # Retornando a resposta
                return self._receive(timeout)
        except socket.timeout as e:
            raise TimeoutSocketException(e)
        except socket.error as e:
            raise GenericSocketException(e)

    def _receive(self, timeout: bool) -> str:
        """
        Recebe uma mensagem pelo socket.

        O parâmetro timeout permite configurar um timeout para a comunicação, impedindo uma espera infinita.
        """

        try:
            # Configurando um timeout para confirmação da entrega
            if timeout:
                self._socket.settimeout(TIMEOUT_SOCKET_MESSAGE)

            # Esperando a entrada, e a lendo por completo
            response = ""
            while True:
                data = self._socket.recv(SOCKET_BUFFER_SIZE)

                if not data:
                    raise MissedSocketException(
                        f"Conexão perdida com o socket: {self._socket}"
                    )

                str_data = data.decode("utf-8")
                response += str_data

                if END_MARK in str_data:
                    response = response[: (-1 * len(END_MARK))]
                    break

            # Retornando a resposta
            return response

        except socket.timeout as e:
            raise TimeoutSocketException(e)
        except socket.error as e:
            raise GenericSocketException(e)
