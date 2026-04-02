from nsj_queue_lib.worker_pub_sub_base import (
    WorkerPubSubBase,
    Subscriber,
    DeadSubscriber,
    SubscriberWebhook,
)
from nsj_queue_lib.settings import logger


# Esse primeiro decorator não é obrigatório.
#
# É apenas um exemplo de como registrar que um subscriber_id se destina ao disparo de webhook,
# por meio de uma fila PubSub.
#
# A ideia é que uma fila PubSub pode servir tanto para atualizar um índice local (por exemplo), quanto para
# disparar mensagens para aplciações externas (misturando implementação específica, com disparo de webhooks).
@SubscriberWebhook("webhook")
class WorkerPubSubTest(WorkerPubSubBase):
    @Subscriber("teste")
    def execute_subscriber_teste(
        self,
        payload: dict[str, any],
        subscription: dict[str, any],
        tarefa: dict[str, any],
        bd_conn,
    ) -> str:
        msg = f"Executando tarefa da assinatura teste. Payload: {payload}"
        logger.debug(msg)
        return msg

    @DeadSubscriber("teste")
    def execute_dead_subscriber_teste(
        self,
        payload: dict[str, any],
        subscription: dict[str, any],
        tarefa: dict[str, any],
        bd_conn,
    ) -> str:
        msg = f"Executando tarefa na fila de mortos, da assinatura teste. Payload: {payload}"
        logger.debug(msg)
        return msg


if __name__ == "__main__":
    WorkerPubSubTest().run()
