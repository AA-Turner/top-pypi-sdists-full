import time
import threading

from datetime import datetime
from typing import Any

from nsj_sql_utils_lib.dbconnection import DBConnection
from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

from nsj_queue_lib.client.lock_client import LockClient
from nsj_queue_lib.client.retry_util import RetryUtil
from nsj_queue_lib.client.socket_client import SocketClient
from nsj_queue_lib.client.tarefa_dao import TarefaDAO
from nsj_queue_lib.settings import (
    CLIENT_SERVER_MODE,
    DB_DRIVER,
    DB_HOST,
    DB_PORT,
    DB_BASE,
    DB_USER,
    DB_PASS,
    QUEUE_MINUTE_RETRY_THREAD,
    QUEUE_TABLE,
    GLOBAL_RUN,
    SERVER_HOST,
    LOCK_SERVICE_PORT,
    logger,
)


class RetryThread(threading.Thread):
    """
    Reenfilera as tarefas que se perdaram em status 'processando'.
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Roda um loop de reinserção das tentativas que falharam.

        A thread só roda de fato nos minutos configurados na
        variável de ambiente: QUEUE_MINUTE_RETRY_THREAD (com
        valor padrão: 0,5,10,15,20,25,30,35,40,45,50,55).

        Além disso, é pego um lock no BD, para que apenas um
        worker realize essa operação por vez (para não
        sobrecarregar o banco).
        """

        logger.info("Thread de retentativas iniciada.")
        while GLOBAL_RUN:
            # Aguardando 15 segundos a cada verificação se deve rodar
            time.sleep(15)
            logger.debug("Nova verificação da thread de retry")

            # Recuperando o minuto atual
            now = datetime.now()
            if not (str(now.minute) in QUEUE_MINUTE_RETRY_THREAD.split(",")):
                continue

            logger.debug("Vai iniciar, de fato, a thread de retry")

            # Realizando de fato a lógica de execução
            try:
                dbconn = None
                db = None
                socket_client = None
                try:
                    if not CLIENT_SERVER_MODE:
                        dbconn = DBConnection(
                            DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                        )
                        dbconn.open()
                        db = DBAdapter3(dbconn.conn)
                    else:
                        socket_client = SocketClient(SERVER_HOST, LOCK_SERVICE_PORT)
                        socket_client.open()

                    lock_client = LockClient(db, socket_client)

                    lock = False
                    try:
                        if lock_client.try_lock_retry():
                            lock = True
                        else:
                            logger.debug(
                                "Desistindo da thread de retentativas, porque já há outro worker operando o mesmo."
                            )
                            continue

                        logger.info("Iniciando tratamento de retentativas...")

                        # Abrindo conexão com o BD (se ainda não foi aberta;
                        # a saber, não é aberta quando o lock se faz por socket;
                        # então a abertura de conexão com o BD é feita só se necessário.
                        if dbconn is None:
                            dbconn = DBConnection(
                                DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                            )
                            dbconn.open()
                            db = DBAdapter3(dbconn.conn)

                        tarefa_dao = TarefaDAO(db, QUEUE_TABLE)
                        # self._retry_falhas(tarefa_dao)
                        self._retry_perdidas(tarefa_dao, lock_client)

                    finally:
                        if lock:
                            lock_client.unlock_retry()

                finally:
                    if dbconn is not None:
                        dbconn.close()

                    if socket_client is not None:
                        socket_client.close()

            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o banco de dados."
                )
                time.sleep(5)

        logger.info("Thread de retentativas finalizada.")

    def _retry_perdidas(self, tarefa_dao: TarefaDAO, lock_client: LockClient):
        """
        Reenfilera as tarefas que se perdaram em status 'processando'
        """

        # Recuperando lista de tarefas a reenfileirar
        count, processando = tarefa_dao.list_recuperacao_processando()
        logger.info(f"Quantidade de tarefas pendentes, a verificar: {count}.")

        # Tratando cada tarefa
        for item in processando:
            id_inicial = item["id_inicial"] or item["id"]

            # Tentando pegar o lock da tarefa (não pode ser possível,
            # se estiver de fato em processamento):
            locked = False
            try:
                if not lock_client.try_lock(item["id"]):
                    # Tarefa em processamento, não precisa fazer nada.
                    continue
                else:
                    locked = True

                    # Verificando se a tarefa ainda está como processando no BD
                    # (pois pode ter acabado durante o loop)
                    tarefa = tarefa_dao.get(item["id"])
                    if tarefa["status"] == "processando":
                        logger.info(
                            f"Reenfileirando a tarefa de id: {item['id']} e id_inicial: {id_inicial}."
                        )
                        RetryUtil().reenfileir_tarefa(tarefa_dao, item, True)
            finally:
                if locked:
                    lock_client.unlock(item["id"])
