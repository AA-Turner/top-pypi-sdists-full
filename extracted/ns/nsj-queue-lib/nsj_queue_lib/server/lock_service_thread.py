import select
import socket
import threading
import time

from nsj_queue_lib.server.rpc_interpreter import RPCInterpreter
from nsj_queue_lib.server.lock_service import LockService
from nsj_queue_lib.server.socket_io import (
    SockerIO,
    MissedSocketException,
    GenericSocketException,
    TimeoutSocketException,
)
from nsj_queue_lib.server.server_settings import (
    LOCK_SERVICE_WAIT_CONN_INTERVAL,
    MAX_CLIENT_THREADS,
)
from nsj_queue_lib.settings import LOCK_SERVICE_PORT, logger


class LockServiceThread(threading.Thread):
    def __init__(
        self,
        server_main,
        lock_service: LockService,
    ):
        super().__init__()
        self.running = True
        self._server_main = server_main
        self.lock_service = lock_service
        self.mutex_lock = threading.Lock()
        self._sockets: list[socket.socket] = []
        self._client_listener_socket = None

    def run(self):
        """
        Método de controle principal da thread.
        """

        logger.info("Thread de recepção de clientes para o serviço de lock iniciada.")
        while self.running:
            try:
                with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                ) as client_listener_socket:
                    client_listener_socket.bind(("", LOCK_SERVICE_PORT))
                    client_listener_socket.listen(MAX_CLIENT_THREADS)

                    self.listen_clients(client_listener_socket)
            except OSError as e:
                logger.exception(
                    f"Ocorreu um erro ao configurar o orquestrador: {e}",
                    stack_info=True,
                )
            except Exception as e:
                logger.exception(
                    f"Erro desconhecido ao iniciar o orquestrador: {e}", stack_info=True
                )

            logger.info("Aguardando 5 segundos, para tentar abrir novamente o socket.")
            time.sleep(5)

        logger.info("Thread de recepção de clientes para o serviço de lock finalizada.")

    def listen_clients(self, client_listener_socket: socket.socket):
        """
        Método responsável por ouvir novas conexões, a partir do socket.
        """
        # Adicionando o socket principal na lista de sockets
        self._client_listener_socket = client_listener_socket
        self._sockets.append(client_listener_socket)

        # Loop principal (sempre esperando nova conexão):
        while self.running:

            file_descriptors = select.select(
                self._sockets, [], [], LOCK_SERVICE_WAIT_CONN_INTERVAL
            )
            if file_descriptors == (
                [],
                [],
                [],
            ):
                logger.debug(
                    "Timeout - Na espera de dados do descritores de arquivo que representam as conexões via socket. Estratégia para evitar espera ocupada."
                )
            else:
                ready_sockets = file_descriptors[0]

                for ready_socket in ready_sockets:

                    if ready_socket == client_listener_socket:
                        # Recebendo a nova conexão
                        conn_socket, addr = client_listener_socket.accept()
                        logger.info(
                            f"LockService - Nova conexão do cliente no endereço {addr}."
                        )

                        self._sockets.append(conn_socket)
                    else:
                        # Recebendo a requisição de um dos clientes
                        self._listen_client(ready_socket)

    def _listen_client(self, client_socket: socket.socket):
        """
        Ouve o cliente a partir do socket, e executa as funções de travamento
        e liberação de lock.

        Só esse serviço é disponibilizado por esse canal.
        """
        client_address = None
        try:
            # Ouvindo o cliente por meio do socket
            socket_io = SockerIO(client_socket)
            msg = socket_io.listen(True)

            # Trata a mensagem recebida, antes de esperar outra,
            # e executa a função correspondente (se houver uma)
            client_address = client_socket.getpeername()[0]
            listener_msg_aux = RPCInterpreter(
                client_address,
                self.lock_service,
                None,
                None,
                None,
                self._client_closed,
            )
            resp = listener_msg_aux.handle_msg(msg)

            # Retornando a resposta para o cliente
            socket_io.send_msg(f"{resp}", False, True)

        except GenericSocketException as e:
            logger.exception(
                f"Erro desconhecido de comunicação com o cliente de endereço: {client_address}",
                stack_info=True,
            )
            self._sockets.remove(client_socket)
            client_socket.close()
        except TimeoutSocketException as e:
            logger.exception(
                f"Timeout na comunicação com o cliente de endereço: {client_address}",
                stack_info=True,
            )
            self._sockets.remove(client_socket)
            client_socket.close()
        except MissedSocketException as e:
            logger.exception(
                f"Perda de comunicação com o cliente de endereço: {client_address}",
                stack_info=True,
            )
            self._sockets.remove(client_socket)
            client_socket.close()

    def _client_closed(self, client_addr: str) -> bool:
        """
        Notifica que um cliente será desconectado, e, portanto, não precisa mais ser ouvido.
        """
        to_remove = None

        # Localizando o socket a remover:
        for socket in self._sockets:
            if (
                socket != self._client_listener_socket
                and socket.getpeername()[0] == client_addr
            ):
                to_remove = socket

        if to_remove is not None:
            # Removendo do controle (não houve mais o socket, já que o mesmo
            # será fechado pelo cliente).
            self._sockets.remove(to_remove)
