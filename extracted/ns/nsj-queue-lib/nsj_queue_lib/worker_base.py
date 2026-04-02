import abc

from nsj_queue_lib.client.main_thread import MainThread
from nsj_queue_lib.client.retry_thread import RetryThread
from nsj_queue_lib.client.purge_thread import PurgeThread
from nsj_queue_lib.client.notify_thread import NotifyThread

from nsj_queue_lib.settings import logger


class WorkerBase(abc.ABC):
    def run(self):
        logger.info("Iniciando worker...")

        # Iniciando thread de retry
        retry_thread = RetryThread()
        retry_thread.start()

        # Iniciando thread de purge
        purge_thread = PurgeThread()
        purge_thread.start()

        # Iniciando thread de notify
        notify_thread = NotifyThread()
        notify_thread.start()

        # Iniciando thread principal
        main_thread = MainThread(self)
        main_thread.run()

    def internal_execute(self, tarefa: dict[str, any], bd_conn, multi_db_conn) -> str:
        payload = tarefa["payload"]

        if multi_db_conn is not None:
            return self.execute(payload, tarefa, bd_conn, multi_db_conn)
        else:
            return self.execute(payload, tarefa, bd_conn)

    def internal_execute_dead(
        self, tarefa: dict[str, any], bd_conn, multi_db_conn
    ) -> str:
        payload = tarefa["payload"]

        if multi_db_conn is not None:
            return self.execute_dead(payload, tarefa, bd_conn, multi_db_conn)
        else:
            return self.execute_dead(payload, tarefa, bd_conn)

    @abc.abstractmethod
    def execute(
        self, payload: str, tarefa: dict[str, any], bd_conn, multi_db_conn=None
    ) -> str:
        """
        Deve ser sobrescrito para a execução da tarefa.
        """
        pass

    def execute_dead(
        self, payload: str, tarefa: dict[str, any], bd_conn, multi_db_conn=None
    ) -> str:
        """
        Sobreescreva esse método, se desejar customizar o comportamento da fila de mortos.

        O comportamento padrão é o simples registro em log.
        """
        mensagem = f"Tarefa com ID {tarefa['id']} excedeu o número de tentativas, sem sucesso. Será necessária intervenção manual."
        logger.warning(mensagem)

        return mensagem
