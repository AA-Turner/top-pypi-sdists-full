from nsj_queue_lib.worker_base import WorkerBase

from nsj_queue_lib.settings import logger


class WorkerFilaTeste(WorkerBase):
    def execute(self, payload: str, tarefa: dict[str, any], bd_conn) -> str:
        logger.debug(f"{tarefa}")
        return f"Mensagem de sucesso personalizada! Payload: {payload}"

    def execute_dead(self, payload: str, tarefa: dict[str, any], bd_conn) -> str:
        logger.debug(f"{tarefa}")
        return f"Mensagem personalizada para o sucesso da execução da fila de mortos. Payload: {payload}"


if __name__ == "__main__":
    WorkerFilaTeste().run()
