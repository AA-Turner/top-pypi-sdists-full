import threading
import time

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
from nsj_sql_utils_lib.dbconnection import DBConnection

from nsj_queue_lib.settings import (
    DB_DRIVER,
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
    QUEUE_MAX_RETRY,
    QUEUE_TABLE,
    QUEUE_SUBSCRIBER_TABLE,
    logger,
)
from nsj_queue_lib.client.tarefa_dao import TarefaDAO

from nsj_queue_lib.server.server_settings import CHECK_TASKS_INTERVAL


class CheckTasksThread(threading.Thread):
    def __init__(
        self,
        server_main,
    ):
        super().__init__()
        self.running = True
        self._server_main = server_main

    def run(self):
        """
        Método de controle principal da thread.
        """

        logger.info("Thread de verificação de tarefas pendentes iniciada.")
        while self.running:
            try:
                with DBConnection(
                    DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                ) as dbconn:
                    self._run_check_tasks(dbconn.conn)
            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o banco de dados."
                )
                time.sleep(5)

        logger.info("Thread de verificação de tarefas pendentes finalizada.")

    def _run_check_tasks(self, conn):
        """
        Lógica de verificação de tarefas pendentes.
        """

        db = DBAdapter3(conn)
        tarefa_dao = TarefaDAO(db, QUEUE_TABLE, QUEUE_SUBSCRIBER_TABLE)

        while self.running:
            # Recuperando a quantidade de tarefas pendentes
            logger.info("Recuperando tarefas pendentes.")
            _, contagem = tarefa_dao.list_pendentes(QUEUE_MAX_RETRY, True)
            count = contagem[0]["qtd"]
            logger.info(f"Quantidade recuperada {count}.")

            # Verificando se ha tarefas para acordar algum worker
            if count > 0:
                self._server_main.notify(contagem)

            # Dormindo um intervalo (para não encher o BD de chamadas)
            time.sleep(CHECK_TASKS_INTERVAL)
