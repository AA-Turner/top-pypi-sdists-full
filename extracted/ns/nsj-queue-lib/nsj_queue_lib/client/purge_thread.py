import threading
import time

from datetime import datetime

from nsj_sql_utils_lib.dbconnection import DBConnection
from nsj_sql_utils_lib.dbadapter3 import DBAdapter3

from nsj_queue_lib.client.lock_client import LockClient
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
    QUEUE_MINUTE_PURGE_THREAD,
    QUEUE_PURGE_MAX_AGE,
    QUEUE_PURGE_LIMIT,
    QUEUE_PURGE_ROUND_LIMIT,
    QUEUE_TABLE,
    GLOBAL_RUN,
    SERVER_HOST,
    LOCK_SERVICE_PORT,
    logger,
)


class PurgeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Roda um loop de exclusão das tarefas muito antigas

        A thread só roda de fato nos minutos configurados na
        variável de ambiente: QUEUE_MINUTE_PURGE_THREAD (com
        valor padrão: 0).

        Além disso, é pego um lock no BD, para que apenas um
        worker realize essa operação por vez (para não
        sobrecarregar o banco).
        """

        logger.info("Thread de purge iniciada.")
        while GLOBAL_RUN:
            # Aguardando 15 segundos a cada verificação se deve rodar
            time.sleep(15)
            logger.debug("Nova verificação da thread de purge")

            # Recuperando o minuto atual
            now = datetime.now()
            if not (str(now.minute) in QUEUE_MINUTE_PURGE_THREAD.split(",")):
                continue

            logger.debug("Vai iniciar, de fato, a thread de purge")

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
                        if lock_client.try_lock_purge():
                            lock = True
                        else:
                            logger.debug(
                                "Desistindo do purge, porque já há outro worker operando o mesmo."
                            )
                            continue

                        logger.info("Iniciando tratamento de purge...")

                        # Abrindo conexão com o BD (se ainda não foi aberta;
                        # a saber, não é aberta quando o lock se faz por socket;
                        # então a abertura de conexão com o BD é feita só se necessário.
                        if dbconn is None:
                            dbconn = DBConnection(
                                DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                            )
                            dbconn.open()
                            db = DBAdapter3(dbconn.conn)

                        dao = TarefaDAO(db, QUEUE_TABLE)
                        self._purge(dao)

                    finally:
                        if lock:
                            lock_client.unlock_purge()

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

        logger.info("Thread de purge finalizada.")

    def _purge(self, dao: TarefaDAO):
        """
        Apaga as tarefas antigas, de acordo com a configuração
        (QUEUE_PURGE_MAX_AGE).
        """

        deleted = 1
        count = 1
        while count <= QUEUE_PURGE_ROUND_LIMIT:
            deleted, _ = dao.purge(QUEUE_PURGE_MAX_AGE, QUEUE_PURGE_LIMIT)
            logger.info(
                f"Purge executado. Registros excluídos: {deleted}. Rodada de purge: {count}"
            )

            # Parando a exclusão, caso a última rodada não tenha chegado ao limite
            # de registros (indicando que não há mais registros a excluir)
            if deleted < QUEUE_PURGE_LIMIT:
                break

            count += 1
