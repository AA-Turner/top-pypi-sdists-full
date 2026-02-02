import datetime

from nsj_queue_lib.client.tarefa_dao import TarefaDAO
from nsj_queue_lib.settings import (
    QUEUE_MAX_RETRY,
    QUEUE_BASE_INTERVAL_RETRY,
    logger,
)


class RetryUtil:
    def reenfileir_tarefa(
        self,
        dao: TarefaDAO,
        tarefa: dict[str, any],
        falha_desconhecida: bool,
        msg: str = None,
    ):
        # Tratando do status e da mensagem de falha
        if falha_desconhecida:
            msg_reenfileirar = "Falha desconhecida de processamento (processamento abortado repentinamente). Tarefa reenfileirada."
            msg_max_tentativas = "Falha desconhecida de processamento (processamento abortado repentinamente), e máximo de tentativas atingido."
            status = "falha_processando"
        else:
            if msg is None:
                msg_reenfileirar = "Falha desconhecida. Tarefa reenfileirada."
                msg_max_tentativas = (
                    "Falha desconhecida, e máximo de tentativas atingido."
                )
            else:
                msg_reenfileirar = f"{msg}. Tarefa reenfileirada."
                msg_max_tentativas = f"{msg}. Máximo de tentativas atingido."

            status = "falha"

        # Realizando de fato a inserção da nova tarefa no banco, e atualização do status
        try:
            # Iniciando transação
            dao.db.begin()

            # Resolvendo o ID inicial
            id_inicial = tarefa["id_inicial"] or tarefa["id"]

            if tarefa["tentativa"] < QUEUE_MAX_RETRY:
                # Calculando a data e hora da próxima tentativa
                proxima_tentativa = tarefa["data_hora"] + datetime.timedelta(
                    minutes=(tarefa["tentativa"] * QUEUE_BASE_INTERVAL_RETRY)
                )

                # Atualizando status da tarefa para indicar falha,
                # e sinalizando que foi reenfileirada
                logger.info(
                    f"Atualizando status da tarefa com ID: {tarefa['id']}, para indicar falha, e sinalizando que foi reenfileirada."
                )
                dao.update_flag_reenfileiramento_falha(
                    tarefa["id"],
                    status,
                    msg_reenfileirar,
                    proxima_tentativa,
                )

                # Inserindo uma nova tentativa para a falha (mesmo que seja para a fila de mortos)
                tarefa = {
                    "id_inicial": id_inicial,
                    "data_hora": proxima_tentativa,
                    "data_hora_inicial": tarefa["data_hora_inicial"],
                    "origem": tarefa["origem"],
                    "destino": tarefa["destino"],
                    "processo": tarefa["processo"],
                    "chave_externa": tarefa["chave_externa"],
                    "tentativa": (tarefa["tentativa"] + 1),
                    "status": "agendada",
                    "proxima_tentativa": None,
                    "mensagem": None,
                    "id_anterior": tarefa["id"],
                    "data_hora_anterior": tarefa["data_hora"],
                    "status_anterior": tarefa["status"],
                    "mensagem_anterior": tarefa["mensagem"],
                    "tenant": tarefa["tenant"],
                    "grupo_empresarial": tarefa["grupo_empresarial"],
                    "payload_hash": tarefa["payload_hash"],
                    "pub_sub": tarefa["pub_sub"],
                    "publication_id": tarefa["publication_id"],
                    "subscriber_id": tarefa["subscriber_id"],
                    "dead": tarefa["dead"],
                    "live_id": tarefa["live_id"],
                }

                dao.insert(tarefa)
            else:
                # Atualizando status da tarefa para indicar falha,
                # e marcando estouro de tentativas
                logger.info(
                    f"Atualizando status da tarefa com ID: {tarefa['id']}, para indicar falha e estouro de tentativas."
                )
                dao.update_falha_max_retries(
                    tarefa["id"],
                    status,
                    msg_max_tentativas,
                )

                # Inserindo a primeira tentativa da fila de mortos nova tentativa para a falha (mesmo que seja para a fila de mortos)
                tarefa = {
                    "origem": tarefa["origem"],
                    "destino": tarefa["destino"],
                    "processo": tarefa["processo"],
                    "chave_externa": tarefa["chave_externa"],
                    "tentativa": 1,
                    "tenant": tarefa["tenant"],
                    "grupo_empresarial": tarefa["grupo_empresarial"],
                    "payload": tarefa["payload"],
                    "pub_sub": tarefa["pub_sub"],
                    "publication_id": tarefa["publication_id"],
                    "subscriber_id": tarefa["subscriber_id"],
                    "dead": True,
                    "live_id": id_inicial,
                }

                dao.insert(tarefa)

            # Commit na transação
            dao.db.commit()
        finally:
            # Rollback na transação (sao já tenha sido feito commit, não faz nada).
            dao.db.rollback()
