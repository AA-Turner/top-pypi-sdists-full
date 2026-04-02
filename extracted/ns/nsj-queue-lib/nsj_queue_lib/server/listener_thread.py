import re
import socket
import threading

from nsj_queue_lib.server.lock_service import LockService
from nsj_queue_lib.server.rpc_interpreter import RPCInterpreter
from nsj_queue_lib.server.socket_io import (
    SockerIO,
    MissedSocketException,
    GenericSocketException,
    TimeoutSocketException,
)
from nsj_queue_lib.settings import logger


class ListenerThread(threading.Thread):
    def __init__(
        self,
        address: str,
        listener_socket: socket.socket,
        lock_service: LockService,
        func_notify_closed_client: callable,
        func_halt_server: callable,
        func_notify_finish: callable,
    ):
        threading.Thread.__init__(self)
        self.running = False
        self.address = address
        self.listener_socket = listener_socket
        self.lock_service = lock_service
        self.func_notify_closed_client = func_notify_closed_client
        self.func_halt_server = func_halt_server
        self.func_notify_finish = func_notify_finish
        self.socket_io = SockerIO(self.listener_socket)

    def stop_listener(self):
        """
        Marca a flag de parada (para fim do loop principal).
        """
        self.running = False

    def run(self):
        """
        Método de controle principal da thread.
        """

        self.running = True

        # Ouvindo contínuamente o socket
        try:
            # Loop principal, ouvindo sempre a espera de novas mensagens
            while self.running:
                # Esperando uma mensagem
                try:
                    message = self.socket_io.listen(False)
                except TimeoutSocketException as e:
                    # Ignora o timeout para voltar a esperar o retorno (a tarefa pode estar em execução, e portanto pode demorar muito)
                    # TODO Verificar se vai ficar em espera eterna, ou se deve considerar perda após um período
                    logger.warning(
                        f"Timeout, esperando retorno do worker de endereço: {self.address}. Já notificado de um trabalho."
                    )

                # Trata a mensagem recebida, antes de esperar outra,
                # e executa a função correspondente (se houver uma)
                rpc_interpreter = RPCInterpreter(
                    self.address,
                    self.lock_service,
                    self._halt,
                    self._halt_all,
                    self._sleep,
                    None,
                )
                resp = rpc_interpreter.handle_msg(message)

                # Retornando a resposta (padrão True, se a execução interna retornar None)
                if resp is None:
                    resp = True

                self.socket_io.send_msg(f"{resp}", False, True)

        except MissedSocketException as e:
            # Derruba a thread e retirar o registro do cliente, pois A CONEXÂO CAIU!
            logger.exception(
                f"Conexão perdida com o worker de endereço: {self.address}",
                stack_info=True,
            )

            # Desalocando os controles de thread e socket
            self.func_notify_closed_client(self.address)

        except GenericSocketException as e:
            logger.exception(
                f"Erro ouvindo o socket de comunicação com o worker de endereço {self.address}.",
                stack_info=True,
            )

            # Desalocando os controles de thread e socket
            self.func_notify_closed_client(self.address)

    def _halt(self, _: re.Match):
        """
        Para a thread corrente (e avisa para que desaloque o socket sender correspondente)
        """
        logger.info(f"Halt chamado para o endereço: {self.address}.")
        self.running = False

    def _halt_all(self, _: re.Match):
        """
        Chama o método responsável por parar todas as threads e o servidor.
        """
        logger.info(f"Halt chamado para o servidor inteiro.")
        self.func_halt_server()

    def _sleep(self, _: re.Match):
        """
        Para a thread ouvinte, e aguarda novo push notification, pois o worker não tem mais trabalho a fazer.
        """
        logger.info(
            f"Parando a thread ouvinte do worker {self.address}. O worker espera novo trabalho."
        )
        self.func_notify_finish(self.address)
