import asyncio
import logging
from dataclasses import dataclass, field

import httpx

from mtmlib.queue.queue import (
    MessageAckRequest,
    MessagePullItem,
    MessagePullReq,
    MessagePullResponse,
    MessageSendPublic,
)

logger = logging.getLogger("mtqueue-client")

max_read_count = 10


@dataclass
class MtQueueClient:
    backend: str

    handler_dict: dict[str, callable] = field(default_factory=dict)

    def register_consumer(self, *, queue_name, consumer_fn):
        self.handler_dict[queue_name] = consumer_fn

    async def run(self):
        logger.info("mt queue client run")
        await self._start_consumers()

    async def _start_consumers(self):
        """Start all consumers concurrently."""
        tasks = [
            self._consume_messages(queue_name, consumer_fn)
            for queue_name, consumer_fn in self.handler_dict.items()
        ]
        await asyncio.gather(*tasks)

    async def send_msgs(self, msgs: list[dict]):
        try:
            req = MessageSendPublic(queue="test1", messages=msgs)
            async with httpx.AsyncClient() as client:
                send_url = f"{self.backend}/api/v1/tasks_queue"
                response = await client.post(send_url, json=req.model_dump())
                response.raise_for_status()
                logger.info("消息发送成功: %s", msgs)
        except Exception as e:
            logger.exception("An unexpected error occurred during sending: %s", e)  # noqa: TRY401

    async def pull_messages(self, queue_name: str):
        while True:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        f"{self.backend}/api/v1/tasks_queue/pull",
                        json=MessagePullReq(
                            items=[MessagePullItem(queue=queue_name)]
                        ).model_dump(),
                    )
                    resp.raise_for_status()
                    content = resp.json()
                    msg_response = MessagePullResponse(**content)
                    data = msg_response.data
                    if len(data) <= 0:
                        await asyncio.sleep(5)
                    for list_items in data:
                        for message in list_items.messages:
                            try:
                                yield message
                                # consumer_fn(msg)
                                # await self.ask_msgs(queue_name, [msg.msg_id])
                            except Exception as e:
                                logger.exception("消息处理函数出错 %s", e)  # noqa: TRY401
            except Exception as e:
                logger.exception("An unexpected error occurred: %s", e)  # noqa: TRY401
                await asyncio.sleep(3)

    async def _consume_messages(self, queue_name: str, consumer_fn: callable):
        """Consume messages from a queue and process them using the registered consumer function."""
        async for msg in self.pull_messages(queue_name=queue_name):
            try:
                consumer_fn(msg)
                await self.ask_msgs(queue_name, [msg.msg_id])
            except Exception as e:
                logger.exception("消息处理函数出错 %s", e)  # noqa: TRY401

    async def ask_msgs(self, queue_name: str, msg_ids: list[int]):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.backend}/api/v1/tasks_queue/ack",
                json=MessageAckRequest(
                    queue=queue_name, msg_ids=[str(msg_id) for msg_id in msg_ids]
                ).model_dump(),
            )
            resp.raise_for_status()
