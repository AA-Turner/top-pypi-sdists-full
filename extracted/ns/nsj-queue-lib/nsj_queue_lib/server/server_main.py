import enum
import socket
import threading
import time

from nsj_queue_lib.server.check_tasks_thread import CheckTasksThread
from nsj_queue_lib.server.listener_thread import ListenerThread
from nsj_queue_lib.server.lock_service import LockService
from nsj_queue_lib.server.lock_service_thread import LockServiceThread
from nsj_queue_lib.server.server_settings import MAX_CLIENT_THREADS
from nsj_queue_lib.server.socket_io import (
    SockerIO,
    GenericSocketException,
    MissedSocketException,
    TimeoutSocketException,
)

from nsj_queue_lib.settings import (
    NOTIFY_SERVICE_PORT,
    logger,
)


class WorkerStatus(enum.Enum):
    LIBERADO = ("LIBERADO",)
    OCUPADO = "OCUPADO"


class WorkerRecord:
    socket_conn: socket.socket
    status: WorkerStatus
    listener_thread: ListenerThread

    def __init__(
        self,
        socket_conn: socket.socket,
        status: WorkerStatus,
        listener_thread: ListenerThread,
    ) -> None:
        self.socket_conn: socket.socket = socket_conn
        self.status: WorkerStatus = status
        self.listener_thread: ListenerThread = listener_thread


# TODO Testar mais o lock_service_thread (ainda está lançando uma exceção errada,
#    indicando que perdeu a comunicação com o cliente, mas o cliente precisa fechar mesmo a conexão)
# TODO Implementar suporte a mysql
# TODO Documentar


class ServerMain:
    def __init__(self) -> None:
        self.running = False
        self.workers: dict[str, WorkerRecord] = {}
        self.lock_service = LockService()
        self.mutex_lock = threading.Lock()
        self.check_tasks_thread = None
        self.lock_service_thread = None

    def run(self):
        self.running = True

        # Iniciando a thread de monitoramento da fila no BD
        self.check_tasks_thread = CheckTasksThread(self)
        self.check_tasks_thread.start()

        # Iniciando a thread de serviço de lock via socket (em porta distinta)
        self.lock_service_thread = LockServiceThread(self, self.lock_service)
        self.lock_service_thread.start()

        # Instanciando o socket
        while self.running:
            try:
                with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                ) as client_receiver_socket:
                    client_receiver_socket.bind(("", NOTIFY_SERVICE_PORT))
                    client_receiver_socket.listen(MAX_CLIENT_THREADS)

                    self.listen_workers(client_receiver_socket)
            except OSError as e:
                logger.exception(
                    f"Ocorreu um erro ao configurar o orquestrador: {e}",
                    stack_info=True,
                )
            except Exception as e:
                logger.exception(
                    f"Erro desconhecido ao iniciar o orquestrador: {e}", stack_info=True
                )

            logger.warning(
                f"Aguardano 5 segundos para tentar configurar o orquestrador novamente."
            )
            time.sleep(5)

    def listen_workers(self, client_receiver_socket: socket.socket):
        """
        Método responsável por ouvir novas conexões de workers, a partir do socket.
        """
        # Loop principal (sempre esperando nova conexão):
        while self.running:
            # Esperando uma conexão
            conn_socket, addr = client_receiver_socket.accept()
            logger.info(f"WorkerListener - Nova conexão do cliente no endereço {addr}.")

            with self.mutex_lock:
                # Verificando se este cliente já estava conectado numa thread de ouvinte
                if addr not in self.workers:
                    self.workers[addr] = WorkerRecord(
                        conn_socket,
                        WorkerStatus.LIBERADO,
                        None,
                    )

    def notify(self, qtd_tasks: int):
        """
        Procura por um worker livre, e o notifica para o trabalho.
        Se não houver nenhum, dorme até achar um.

        Ao notificar um worker, é criada uma thread ouvinte para esse
        worker (para ouvir o respectivo socket). E, é ouvindo o worker,
        que o mesmo demandará locks, etc.
        """

        logger.info(
            f"Acordando todos os workers disponíveis, para trabalharem nas {qtd_tasks} tarefa(s) pendente(s)."
        )
        worker_started = False

        # Tenta até conseguir acordar um worker
        while not worker_started:
            logger.info(f"Quantidade de workers registrados: {len(self.workers)}.")

            dead_workers = []

            for worker_addr in self.workers:
                worker = self.workers[worker_addr]

                if worker.status == WorkerStatus.LIBERADO:
                    recebido = False

                    # Acordando o worker
                    try:
                        recebido = self._notify_worker(worker.socket_conn, worker_addr)
                    except MissedSocketException as e:
                        logger.warning(
                            f"Perda de conexão ao tentar informar o worker de endereço {worker_addr}, para iniciar o trabalho."
                        )
                        dead_workers.append(worker_addr)
                    except GenericSocketException as e:
                        logger.exception(
                            f"Erro notificando (para iniciar o trabalho) o worker de endereço {worker_addr}.",
                            stack_info=True,
                        )
                        dead_workers.append(worker_addr)
                    except TimeoutSocketException as e:
                        logger.exception(
                            f"Timeout notificando (para iniciar o trabalho) o worker de endereço {worker_addr}.",
                            stack_info=True,
                        )
                        dead_workers.append(worker_addr)

                    # Verificando se o ouvinte confirmou o recebimento
                    if recebido:
                        self._start_worker_listening(worker_addr)
                        worker_started = True
                        # break Vou deixar acordar todos os workers, da mesma forma que o postgres faz

            # Removendo eventuais workers mortos do registro
            for dead_worker_addr in dead_workers:
                self.notify_closed_client(dead_worker_addr)

            if not worker_started:
                logger.info(
                    "Aguardando 5 segundos para verificar se haverá um worker liberado para o trabalho."
                )
                time.sleep(5)

    def _start_worker_listening(self, worker_addr: str):
        """
        Ativado a thread de comunicação com o worker, e marcando o worker como ocupado.
        """
        # Travando a lista de workers, enquanto manipula a mesma
        with self.mutex_lock:
            worker = self.workers[worker_addr]

            # Ativado a thread de comunicação com o worker
            worker.listener_thread = ListenerThread(
                worker_addr,
                worker.socket_conn,
                self.lock_service,
                self.notify_closed_client,
                self.halt_server,
                self._stop_worker_listening,
            )
            worker.listener_thread.start()
            worker.status = WorkerStatus.OCUPADO
            logger.info(f"Worker notificado do trabalho: {worker_addr}")

    def _stop_worker_listening(self, worker_addr: str):
        """
        Ativado a thread de comunicação com o worker, e marcando o worker como ocupado.
        """
        # Travando a lista de workers, enquanto manipula a mesma
        with self.mutex_lock:
            worker = self.workers[worker_addr]

            # Ativado a thread de comunicação com o worker
            worker.listener_thread.stop_listener()
            worker.listener_thread = None
            worker.status = WorkerStatus.LIBERADO
            logger.info(f"Worker liberado para novo trabalho: {worker_addr}")

    def _notify_worker(self, socket_conn: socket, addr: str):
        """
        Envia a mensagem que acorda um worker (pelo socket anteriormente estabelecido).
        """

        # Aguardando confirmação de entrega
        socket_io = SockerIO(socket_conn)
        resp = socket_io.send_msg("NOTIFY", True, True)

        return resp.upper() == "TRUE"

    def notify_closed_client(self, addr: str):
        """
        Recebe a notificação de que uma thread (listener) parou, e trata de garantir o fim dessa thread,
        assim como de sua respectiva thread sender.
        """

        logger.warning(f"Perdida a conexão com o worker de endereço: {addr}")

        # Tentando fechar o socket (se ainda estover aberto)
        try:
            self.workers[addr].socket_conn.close()
        except:
            pass

        # Removendo o worker dos controles (e parando a thread, se necessário)
        with self.mutex_lock:
            # Parando a thread ouvinte e liberando o controle da mesma
            if self.workers[addr].listener_thread is not None:
                self.workers[addr].listener_thread.stop_listener()
            del self.workers[addr]

            # Liberando todos os locks desse address
            self.lock_service.release_locks(addr)

    def halt_server(self, addr: str):
        """
        Para todas as threads, inclusive a principal do servidor (que aceita novas conexões)
        """
        self.running = False
        self.check_tasks_thread.running = False

        # Parando e liberando cada address controlado
        for addr in self.workers:
            self.notify_closed_client(addr)


if __name__ == "__main__":
    ServerMain().run()
