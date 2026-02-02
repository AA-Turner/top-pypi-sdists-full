import re

from nsj_queue_lib.server.lock_service import LockService
from nsj_queue_lib.settings import logger


class RPCInterpreter:
    def __init__(
        self,
        socket_address: str,
        lock_service: LockService,
        func_halt: callable,
        func_halt_server: callable,
        func_sleep: callable,
        func_close: callable,
    ) -> None:
        super().__init__()

        self._socket_address = socket_address
        self.MESSAGE_PATTERNS = {
            r"try_lock\((\d+)\)": self._try_lock,
            r"release_lock\((\d+)\)": self._release_lock,
            r"halt\(\)": func_halt if func_halt is not None else self._not_implement,
            r"halt_server\(\)": (
                func_halt_server
                if func_halt_server is not None
                else self._not_implement
            ),
            r"sleep\(\)": func_sleep if func_sleep is not None else self._not_implement,
            r"close\(\)": (
                self._close if func_close is not None else self._not_implement
            ),
        }

        self.lock_service = lock_service
        self._func_close = func_close

    def handle_msg(self, msg: str):
        """
        Tenta casar a função com algum dos padrões de mensagem suportados pelo servidor.

        Se houver um casamento, invoca a respectiva função, e retorna o que a função retornar.
        Se não, retorna False.
        """
        resp = False
        for pattern in self.MESSAGE_PATTERNS:
            match = re.match(pattern, msg)
            if not match:
                continue

            func = self.MESSAGE_PATTERNS[pattern]
            resp = func(match)
            # resp = f"{resp}"
            break

        return resp

    def _not_implement(self, match: re.Match):
        return False

    def _try_lock(self, match: re.Match) -> str:
        """
        Tenta bloquear o ID passado.
        """

        lock_number = int(match.group(1))
        logger.info(f"Travando o lock para o número: {lock_number}.")
        return self.lock_service.try_lock(lock_number, self._socket_address)

    def _release_lock(self, match: re.Match) -> str:
        """
        Libera o ID passado.
        """

        lock_number = int(match.group(1))
        logger.info(f"Liberando o lock para o número: {lock_number}.")
        self.lock_service.release_lock(lock_number)

    def _close(self, _: re.Match):
        """
        Chama a função de fechamento do conexão, por parte do cliente,
        passando, como parâmetro, o endereço do cliente.
        """
        return self._func_close(self._socket_address)
