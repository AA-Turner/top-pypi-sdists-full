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
    QUEUE_NAME,
    QUEUE_MINUTE_NOTIFY_THREAD,
    QUEUE_TABLE,
    QUEUE_WAIT_NOTIFY_INTERVAL,
    GLOBAL_RUN,
    SERVER_HOST,
    LOCK_SERVICE_PORT,
    logger,
)


class NotifyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """
        Roda um loop de disparo de notificações para tarefas
        agendadas (e que já possam ser executadas).

        A thread só roda de fato nos minutos configurados na
        variável de ambiente: QUEUE_MINUTE_NOTIFY_THREAD (com
        valor padrão: 0,5,10,15,20,25,30,35,40,45,50,55).

        Além disso, é pego um lock no BD, para que apenas um
        worker realize essa operação por vez (para não
        sobrecarregar o banco).
        """

        logger.info("Thread de notify iniciada.")
        while GLOBAL_RUN:
            # Aguardando 15 segundos a cada verificação se deve rodar
            time.sleep(15)
            logger.debug("Nova verificação da thread de notify")

            # Recuperando o minuto atual
            now = datetime.now()
            if not (str(now.minute) in QUEUE_MINUTE_NOTIFY_THREAD.split(",")):
                continue

            logger.debug("Vai iniciar, de fato, a thread de notify")

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
                        if lock_client.try_lock_notify():
                            lock = True
                        else:
                            logger.debug(
                                "Desistindo do notify, porque já há outro worker operando o mesmo."
                            )
                            continue

                        logger.info("Iniciando tratamento de notify...")

                        # Abrindo conexão com o BD (se ainda não foi aberta;
                        # a saber, não é aberta quando o lock se faz por socket;
                        # então a abertura de conexão com o BD é feita só se necessário.
                        if dbconn is None:
                            dbconn = DBConnection(
                                DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                            )
                            dbconn.open()
                            db = DBAdapter3(dbconn.conn)

                        # Realizando o ajuste das tarefas agendadas, e disparando as
                        # notificações se necessário:
                        dao = TarefaDAO(db, QUEUE_TABLE)
                        self._notify_agendadas(dao)

                        # Se não estiver no modelo client X server, dispara notificação
                        # para tarefas atrasadas:
                        if not CLIENT_SERVER_MODE:
                            self._notify_perdidas(dao)

                    finally:
                        if lock:
                            lock_client.unlock_notify()

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

    def _notify_agendadas(self, dao: TarefaDAO):
        """
        Recupera as tarefas agendadas que precisam de notify,
        marcando-as como pendentes, disparando o notify para elas.
        """

        count, agendadas = dao.list_agendadas_para_notificacao()
        logger.info(
            f"Verificando tarefas agendadas e pendentes de notificação para execução. Quantidade recuperada: {count}"
        )

        dispara_notify = False
        for tarefa in agendadas:
            try:
                logger.debug(
                    f"Atualizando tarefa de agendada para pendente. ID: {tarefa['id']}"
                )

                # Abrindo transação
                dao.db.begin()

                # Atualizando status da tarefa para pendente
                dao.update_status(tarefa["id"], "pendente")

                # Commitando transação
                dao.db.commit()

                # Guardando a informação de que é preciso disparar a notificação para acordar os workers
                dispara_notify = True
            finally:
                # Fazendo rollback (se houver commit anterior, não faz nada)
                dao.db.rollback()

        if dispara_notify and not CLIENT_SERVER_MODE:
            # Notificando a fila (para acordar os workers)
            dao.notify(QUEUE_NAME)

    def _notify_perdidas(self, dao: TarefaDAO):
        """
        Recupera as tarefas pendentes há mais tempo que o intervalo de espera por uma notificação,
        definido para os workers.

        Isso é necessário para garantir que uma notificação não foi disparada no exato momento que
        não havia ninguém ouvindo.
        """

        _, contagem = dao.count_pendentes_perdidas(QUEUE_WAIT_NOTIFY_INTERVAL)

        qtd = contagem[0]["qtd"]
        logger.info(
            f"Quantidade de tarefas pendentes, porém não pegas há mais tempo que o intervalo padrão de espera por notificações: {qtd}"
        )

        if qtd > 0:
            # Notificando a fila (para acordar os workers)
            dao.notify(QUEUE_NAME)
