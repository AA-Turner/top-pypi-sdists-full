from nsj_gcf_utils.http_util import HttpUtil
from nsj_gcf_utils.json_util import json_loads

from nsj_queue_lib.worker_base import WorkerBase

from nsj_queue_lib.settings import DEFAULT_WEBHOOK_TIMEOUT, logger


class WorkerWebhook(WorkerBase):
    def execute(self, payload: str, tarefa: dict[str, any], _) -> str:
        logger.info(f"Disparando Webhook de ID: {tarefa['id']}")
        logger.debug(f"Dados do Webhook: {tarefa}")

        return self.make_request(payload)

    def make_request(self, payload: str) -> str:
        # Recuperando os dados da tarefa
        payload = json_loads(payload)
        subscription = payload["subscription"]

        # Fazendo a requisição
        logger.info(f"Chamando o endpoint: {subscription['url']}...")

        url = subscription["url"]
        headers = subscription["headers"]
        method = subscription["http_method"].upper()

        if method == "GET":
            response = HttpUtil.get_retry(
                url,
                headers,
                tries=1,
                timeout=DEFAULT_WEBHOOK_TIMEOUT,
            )
        elif method == "POST":
            response = HttpUtil.post_retry(
                url,
                payload["publication"],
                headers,
                tries=1,
                timeout=DEFAULT_WEBHOOK_TIMEOUT,
            )
        elif method == "PUT":
            response = HttpUtil.put_retry(
                url,
                payload["publication"],
                headers,
                tries=1,
                timeout=DEFAULT_WEBHOOK_TIMEOUT,
            )
        elif method == "DELETE":
            response = HttpUtil.delete_retry(
                url,
                headers,
                tries=1,
                timeout=DEFAULT_WEBHOOK_TIMEOUT,
            )
        else:
            raise Exception(f"Método HTTP não suportado: {method}")

        mensagem = f"Webhook disparado com sucesso na URL: {url}. Método HTTP: {method}. Status Resposta: {response.status_code}. Mensagem: {response.text}."
        logger.debug(mensagem)

        return mensagem[:500]


if __name__ == "__main__":
    WorkerWebhook().run()
