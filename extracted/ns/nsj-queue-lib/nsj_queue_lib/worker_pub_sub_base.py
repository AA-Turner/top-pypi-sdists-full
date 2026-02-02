import abc

from nsj_gcf_utils.json_util import json_loads

from nsj_queue_lib.client.exception import SubscriberNotRegistered
from nsj_queue_lib.settings import logger
from nsj_queue_lib.worker_base import WorkerBase
from nsj_queue_lib.worker_webhook import WorkerWebhook


class Subscriber:
    METHOD_SUBSCRIBER_DICT = {}

    def __init__(self, subscriber_id: str) -> None:
        self.subscriber_id = subscriber_id

    def __call__(self, func):
        Subscriber.METHOD_SUBSCRIBER_DICT[self.subscriber_id] = func
        return func


class SubscriberWebhook:
    METHOD_WEBHOOK_SUBSCRIBE_DICT = set()

    def __init__(self, subscriber_id: str) -> None:
        self.subscriber_id = subscriber_id

    def __call__(self, obj):
        SubscriberWebhook.METHOD_WEBHOOK_SUBSCRIBE_DICT.add(self.subscriber_id)
        return obj


class DeadSubscriber:
    METHOD_DEAD_SUBSCRIBER_DICT = {}

    def __init__(self, subscriber_id: str) -> None:
        self.subscriber_id = subscriber_id

    def __call__(self, func):
        DeadSubscriber.METHOD_DEAD_SUBSCRIBER_DICT[self.subscriber_id] = func
        return func


class WorkerPubSubBase(WorkerBase, abc.ABC):
    def internal_execute(self, tarefa: dict[str, any], bd_conn, multi_db_conn) -> str:
        payload = tarefa["payload"]
        return self.execute(payload, tarefa, bd_conn, multi_db_conn)

    def internal_execute_dead(
        self, tarefa: dict[str, any], bd_conn, multi_db_conn
    ) -> str:
        payload = tarefa["payload"]
        return self.execute_dead(payload, tarefa, bd_conn, multi_db_conn)

    def execute(
        self, payload: str, tarefa: dict[str, any], bd_conn, multi_db_conn
    ) -> str:
        logger.info(f"Executando a tarefa PubSub de ID: {tarefa['id']}")
        logger.debug(f"Dados da tarefa: {tarefa}")

        # Recuperando os dados da tarefa
        payload = json_loads(payload)
        subscription = payload["subscription"]
        subscriber_id = subscription["id"]

        # Executando o método registrado para o subscriber_id
        if subscriber_id in Subscriber.METHOD_SUBSCRIBER_DICT:
            if multi_db_conn is None:
                return Subscriber.METHOD_SUBSCRIBER_DICT[subscriber_id](
                    self,
                    payload,
                    subscription,
                    tarefa,
                    bd_conn,
                )
            else:
                return Subscriber.METHOD_SUBSCRIBER_DICT[subscriber_id](
                    self,
                    payload,
                    subscription,
                    tarefa,
                    bd_conn,
                    multi_db_conn,
                )
        elif subscriber_id in SubscriberWebhook.METHOD_WEBHOOK_SUBSCRIBE_DICT:
            return WorkerWebhook().execute(payload, tarefa, bd_conn)
        else:
            raise SubscriberNotRegistered(
                f"Subscriber '{subscriber_id}' não registrado."
            )

    def execute_dead(
        self, payload: str, tarefa: dict[str, any], bd_conn, multi_db_conn
    ) -> str:
        """
        Sobreescreva esse método, se desejar customizar o comportamento da fila de mortos.

        O comportamento padrão é o simples registro em log.
        """
        logger.info(f"Executando fila de mortos da tarefa PubSub de ID: {tarefa['id']}")
        logger.debug(f"Dados da tarefa: {tarefa}")

        # Recuperando os dados da tarefa
        payload = json_loads(payload)
        subscription = payload["subscription"]
        subscriber_id = subscription["id"]

        # Recuperando a função da fila de mortos registrada para o subscriber_id
        if subscriber_id not in DeadSubscriber.METHOD_DEAD_SUBSCRIBER_DICT:
            if multi_db_conn is None:
                return super().execute_dead(payload, tarefa, bd_conn)
            else:
                return super().execute_dead(payload, tarefa, bd_conn, multi_db_conn)

        # Executando o método registrado para o subscriber_id
        if multi_db_conn is None:
            return DeadSubscriber.METHOD_DEAD_SUBSCRIBER_DICT[subscriber_id](
                self,
                payload,
                subscription,
                tarefa,
                bd_conn,
            )
        else:
            return DeadSubscriber.METHOD_DEAD_SUBSCRIBER_DICT[subscriber_id](
                self,
                payload,
                subscription,
                tarefa,
                bd_conn,
                multi_db_conn,
            )
