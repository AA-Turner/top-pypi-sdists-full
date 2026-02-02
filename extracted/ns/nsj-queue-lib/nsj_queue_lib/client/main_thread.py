import select
import time


from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
from nsj_sql_utils_lib.dbconnection import DBConnection

from nsj_queue_lib.client.exception import NotFoundException
from nsj_queue_lib.client.lock_client import LockClient
from nsj_queue_lib.client.multidabase_client import MultiDatabaseClient
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
    QUEUE_NAME,
    GLOBAL_RUN,
    QUEUE_MAX_RETRY,
    QUEUE_TABLE,
    QUEUE_SUBSCRIBER_TABLE,
    QUEUE_WAIT_NOTIFY_INTERVAL,
    SERVER_HOST,
    NOTIFY_SERVICE_PORT,
    MULTI_DATABASE,
    logger,
)


class MainThread:
    def __init__(self, worker):
        self.worker = worker
        self._notificacao_inicial = False

    def run(self):
        """
        Método de entrada da Thread, reponsável pelo loop infinito,
        e por abrir conexão com o BD.
        """
        logger.info("Thread de principal iniciada.")
        while GLOBAL_RUN:
            try:
                dbconn = None
                socket_client = None
                try:
                    # Abrindo a conexão com o banco
                    dbconn = DBConnection(
                        DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
                    )
                    dbconn.open()

                    # Abrindo a conexão com o socket (se necessário)
                    if CLIENT_SERVER_MODE:
                        socket_client = SocketClient(SERVER_HOST, NOTIFY_SERVICE_PORT)
                        socket_client.open()
                        logger.info(
                            f"MainThread - Conectado ao servidor no endereço: {socket_client._socket.getpeername()}"
                        )

                        self._run_wait_notify_socket(dbconn.conn, socket_client)
                    else:
                        self._run_wait_notify_database(dbconn.conn)
                finally:
                    if dbconn is not None:
                        dbconn.close()

                    if socket_client is not None:
                        socket_client.close(False)
            except Exception as e:
                logger.exception(f"Erro desconhecido: {e}", stack_info=True)
                logger.info(
                    "Aguardando 5 segundos, para tentar nova conexão com o servidor."
                )
                time.sleep(5)

        logger.info("Thread de principal finalizada.")

    def _run_wait_notify_database(self, conn):
        """
        Lógica de ouvinte das notificações do BD.
        """

        # Como a variável é escrita, neste escopo, é preciso declarar que estamos usando
        # a mesma variável definida fora do escopo
        global GLOBAL_RUN

        with conn.cursor() as curs:
            curs.execute(f"LISTEN {QUEUE_NAME}")

            # Iniciando espera por notificações da fila
            logger.info(f"Esperando notificações na fila.")
            while GLOBAL_RUN:
                if select.select([conn], [], [], QUEUE_WAIT_NOTIFY_INTERVAL) == (
                    [],
                    [],
                    [],
                ):
                    logger.debug(
                        "Timeout - Na espera de dados do descritor de arquivo que representa a conexão com o BD. Estratégia para evitar espera ocupada."
                    )
                else:
                    conn.poll()
                    while conn.notifies:
                        notify = conn.notifies.pop(0)
                        logger.info(
                            f"NOTIFY - Notificação recebida. PID: {notify.pid} CHANNEL: {notify.channel} PAYLOAD: {notify.payload}"
                        )

                        # Desligando o worker, caso seja notificado para desligamento
                        if notify.payload == "HALT":
                            GLOBAL_RUN = False

                        # Tentando executar alguma tarefa da fila
                        self._run_tarefas(conn)

    def _run_wait_notify_socket(self, conn, socket_client: SocketClient):
        """
        Lógica de ouvinte das notificações via socket.
        """

        # Como a variável é escrita, neste escopo, é preciso declarar que estamos usando
        # a mesma variável definida fora do escopo
        global GLOBAL_RUN

        # Iniciando espera por notificações da fila
        logger.info(f"Esperando notificações na fila.")
        while GLOBAL_RUN:
            if select.select(
                [socket_client._socket], [], [], QUEUE_WAIT_NOTIFY_INTERVAL
            ) == (
                [],
                [],
                [],
            ):
                logger.debug(
                    "Timeout - Na espera de dados do descritor de arquivo que representa a conexão com o socket. Estratégia para evitar espera ocupada."
                )
            else:
                # Lendo a mensagem recebida pelo socket
                msg = socket_client.listen()

                # Confirmando a recepção da mensagem
                socket_client.send_msg("TRUE", True, False)

                # Verificando se era realmente um NOTIFY
                if msg.upper() == "NOTIFY":
                    try:
                        # Tentando executar alguma tarefa da fila
                        self._run_tarefas(conn, socket_client)

                    finally:
                        # Informando que o trabalho terminou
                        if not socket_client.sleep():
                            raise Exception(
                                "Erro informando fim do processamento de uma tarefa."
                            )
                else:
                    raise Exception(f"Recebida mensagem inesperada do servidor: {msg}")

    def _run_tarefas(self, conn, socket_client: SocketClient = None):
        """
        Recupera a lista de tarefas pendentes, e tenta executar uma de cada vez.
        """

        db = DBAdapter3(conn)
        lock_client = LockClient(db, socket_client)
        tarefa_dao = TarefaDAO(db, QUEUE_TABLE, QUEUE_SUBSCRIBER_TABLE)

        # Recuperando todas as tarefas pendentes
        logger.info("Recuperando tarefas pendentes.")
        count, pendentes = tarefa_dao.list_pendentes(QUEUE_MAX_RETRY)
        logger.info(f"Quantidade recuperada {count}.")

        for tarefa in pendentes:
            # Tentando pegar uma tarefa para trabalhar
            locked = False
            try:
                if not lock_client.try_lock(tarefa["id"]):
                    logger.debug(
                        f"Desisitindo da tarefa com ID {tarefa['id']}. Pois já estava sendo executada em outro worker."
                    )
                    continue
                else:
                    locked = True

                # Recuperando a tarefa em si
                try:
                    tarefa = tarefa_dao.get(tarefa["id"])
                except NotFoundException as e:
                    logger.exception(
                        f"Tarefa com ID {tarefa['id']} excluída indevidamente do BD.",
                        stack_info=True,
                    )
                    continue

                # Verificando se a tarefa ainda está pendente
                if tarefa["status"] != "pendente":
                    logger.debug(
                        f"Desisitindo da tarefa com ID {tarefa['id']}. Pois já havia sido pega para execução por outro worker."
                    )
                    continue

                # Tarefa pronta para trabalhar
                # TODO Refatorar para iniciar a tarefa em outra thread,
                # controlando o máximo de tarefas simultâneas,
                # por meio de uma configuração
                logger.info(f"Tarefa selecionada para trabalhar. ID: {tarefa['id']}")
                self._run_tarefa(tarefa_dao, tarefa)

            finally:
                if locked:
                    lock_client.unlock(tarefa["id"])

    def _run_tarefa(self, dao: TarefaDAO, tarefa: dict[str, any]):
        """
        Trata da execução de uma tarefa específica, porém cuidando apenas dos status
        processando e falha.

        Este método invoca o _run_worker, o qual de fato dispara o código customizado.
        """

        logger.info(f"Iniciando execução da tarefa com  ID: {tarefa['id']}")

        # Atualizando status da tarefa para processando.
        logger.debug(
            f"Atualizando status da tarefa com ID: {tarefa['id']}, para processando."
        )
        dao.update_status(tarefa["id"], "processando")

        try:
            if tarefa["dead"]:
                # Verificando se é uma tarefa já morta
                self._run_worker(tarefa, True)
            elif tarefa["pub_sub"]:
                # Verificando se é uma tarefa do tipo pub_sub
                self._publish(dao, tarefa)
            else:
                self._run_worker(tarefa, False)
        except Exception as e:
            logger.exception(
                f"Erro executando a tarefa com ID: {tarefa['id']}.", stack_info=True
            )

            RetryUtil().reenfileir_tarefa(dao, tarefa, False, str(e))

    def _open_multidatabase_connection(self, tarefa: dict[str, any]):
        """
        Chama API do multibanco para resolver a conexão com o banco de dados, a partir do tenant.
        """
        tenant = tarefa["tenant"]
        mult_db_client = MultiDatabaseClient()
        credentials = mult_db_client.get_erp_credentials(tenant)

        db_conn = DBConnection(
            "POSTGRES",
            credentials["hostname"],
            credentials["port"],
            credentials["db_name"],
            credentials["user"],
            credentials["password"],
        )
        db_conn.open()

        return db_conn

    def _run_worker(self, tarefa: dict[str, any], dead: bool):
        """
        Executa de fato o código do worker, para tratar uma tarefa. Passos:
        1. Abre nova conexão com o BD
        2. Abre nova transação
        3. Se tiver sucesso, commita e atualiza o status para sucesso
        4. Se tiver falha, faz rollback (mas, o status para falha dependerá do método
        anterior, que chama este, porque o controle de falha se dá na conexão da MainThread)
        """

        multi_db_conn = None
        try:
            if MULTI_DATABASE:
                multi_db_conn = self._open_multidatabase_connection(tarefa)

            # Iniciando nova conexão com o BD, para a tarefa
            with DBConnection(
                DB_DRIVER, DB_HOST, DB_PORT, DB_BASE, DB_USER, DB_PASS
            ) as new_dbconn:
                new_db = DBAdapter3(new_dbconn.conn)
                new_dao = TarefaDAO(new_db, QUEUE_TABLE)

                # Iniciando transação
                new_dao.db.begin()
                try:
                    # Invocando o código customizado para execução da tarefa.
                    if not dead:
                        mensagem = self.worker.internal_execute(
                            tarefa, new_dbconn, multi_db_conn
                        )
                    else:
                        mensagem = self.worker.internal_execute_dead(
                            tarefa, new_dbconn, multi_db_conn
                        )

                    if mensagem is None:
                        mensagem = "Concluído com sucesso"

                    # Atualizando o status para concluido com sucesso.
                    logger.debug(
                        f"Atualizando status da tarefa com ID: {tarefa['id']}, para concluido com sucesso."
                    )
                    new_dao.update_status(tarefa["id"], "sucesso", mensagem)

                    # Comitando as alterações
                    new_dao.db.commit()
                finally:
                    # Fazendo rollback (que não terá efeito,
                    # se já tiver sido feito commit)
                    new_dao.db.rollback()

        finally:
            if multi_db_conn is not None:
                multi_db_conn.close()

    def _publish(self, dao: TarefaDAO, tarefa: dict[str, any]):
        """
        Executa uma tarefa do tipo pub_sub, consultando as assinaturas, e enfileirando uma execução
        para cada assinatura.

        1. Recupera as assinaturas
        2. Enfileira uma nova tarefa para cada assinatura
        3. Se tiver sucesso, commita e atualiza o status para sucesso
        4. Se tiver falha, faz rollback (mas, o status para falha dependerá do método
        anterior, que chama este).
        """

        logger.info(f"Publicando tarefa do tipo pub_sub, com ID: {tarefa['id']}")

        dao.db.begin()
        try:
            # Recuperando as assinaturas da tarefa
            subscribers = dao.list_subscribers(
                tarefa["processo"], tarefa["tenant"], tarefa["grupo_empresarial"]
            )

            # Enfileirando uma cópia para cada assinante
            for sub in subscribers:
                logger.debug(
                    f"Publicando tarefa de ID {tarefa['id']}, para o assintante de ID {sub['id']}"
                )

                payload = {
                    "publication": tarefa["payload"],
                    "subscription": sub,
                }

                new_tarefa = {
                    "origem": tarefa["origem"],
                    "destino": tarefa["destino"],
                    "processo": tarefa["processo"],
                    "chave_externa": tarefa["chave_externa"],
                    "tentativa": 1,
                    "status": "pendente",
                    "mensagem": None,
                    "tenant": tarefa["tenant"],
                    "grupo_empresarial": tarefa["grupo_empresarial"],
                    "publication_id": tarefa["id"],
                    "subscriber_id": sub["id"],
                    "payload": payload,
                }

                dao.insert(new_tarefa)

            if len(subscribers) > 0:
                mensagem = "Publicado para os assinantes, com sucesso!"
            else:
                mensagem = "Não haviam assinantes configurados! Tarefa descartada sem nenhuma ação."

            logger.debug(mensagem)

            # Atualizando o status para concluido com sucesso.
            logger.debug(
                f"Atualizando status da tarefa com ID: {tarefa['id']}, para concluído com sucesso."
            )
            dao.update_status(tarefa["id"], "sucesso", mensagem)

            # Comitando as alterações
            dao.db.commit()
        finally:
            # Fazendo rollback (que não terá efeito,
            # se já tiver sido feito commit)
            dao.db.rollback()
