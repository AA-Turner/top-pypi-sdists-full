# Copyright 2026 zovdev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import struct
import asyncio

from concurrent.futures import ThreadPoolExecutor


from .utils import MsgFactory
from .tl_object import CoreMessage, MsgContainer


BADMSGNOTIFICATIONS = {
    16: "Не верный msg_id, требуется синхронизация времени.",
    17: "Не верный msg_id, требуется синхронизация времени.",
    18: "Не верный msg_id, клиентский msg_id должен быть кратен 4.",
    19: "Не верный msg_id, msg_id контейнера == msg_id предыдущего сообщения.",
    20: "Очень старое сообщение.",
    32: "Не верный msg_seqno.",
    33: "Не верный msg_seqno.",
    34: "Не верный msg_seqno, отправленно нечетное значение.",
    35: "Не верный msg_seqno, получено четное значение.",
    48: "Неправильная соль сервера.",
    64: "Недопустимый контейнер."
}

TIME_DIFF_30_SEC = 30 * 4294967296
TIME_DIFF_5_MIN = -300 * 4294967296


class Session:
    __slots__ = (
        "client", "loop",
        "msg_factory", "connection", "pool_executor",
        "_state", "_start_config", "_batch_list", "_batch_event",
        "ignore_error", "wait_packet", "time_offset", "pending_acks", "recent_msg_ids",
        "_recv_task", "_batch_task", "_ping_task"
    )

    def __init__(self, client, mt_workers=2):
        self.client = client
        self.loop = client.loop

        self.msg_factory = MsgFactory(self)
        self.pool_executor = ThreadPoolExecutor(max_workers=mt_workers)
        self.connection = self.client.connection

        self._state = 0
        self._start_config = {}
        self._batch_list = []
        self._batch_event = asyncio.Event()

        self.ignore_error = 0
        self.wait_packet = {}
        self.time_offset = None
        self.pending_acks = set()
        self.recent_msg_ids  = set()

    def server_time(self):
        return time.time() + (self.time_offset or 0)

    async def handle_message(self, msg):
        if msg.seq_no % 2 != 0:
            if msg.msg_id in self.pending_acks:
                return
            else:
                self.pending_acks.add(msg.msg_id)

        if self.ignore_error > 10:
            return await self.stop()

        time_diff = msg.msg_id - self.msg_factory.get_msg_id()

        if time_diff > TIME_DIFF_30_SEC:
            self.client.error("Ошибка времени, разница во времени 30 секунд")
            self.ignore_error += 1
            return
        if time_diff < TIME_DIFF_5_MIN:
            self.client.error("Ошибка времени, разница во времени -5 минут")
            self.ignore_error += 1
            return
        if msg.msg_id in self.recent_msg_ids:
            self.client.error("Ошибка дубликата, msg_id уже существует!")
            self.ignore_error += 1
            return

        if msg.body["_"] == "newSessionCreated":
            self.client.info("NewSessionCreated")
            return

        msg_id = None

        if msg.body["_"] in {"rpcResult", "futureSalts"}:
            msg_id = msg.body["req_msg_id"]
        elif msg.body["_"] == "pong":
            msg_id = msg.body["msg_id"]
        elif msg.body["_"] in {"badMsgNotification", "badServerSalt"}:
            msg_id = msg.body["bad_msg_id"]
        else:
            self.loop.create_task(self.client.handle_updates(msg.body))

        if msg_id in self.wait_packet:
            self.wait_packet[msg_id].set_result(msg.body)

    async def handle_packet(self, packet):
        try:
            data = await self.loop.run_in_executor(
                self.pool_executor,
                self.connection.unpack,
                packet
            )
        except Exception as ex:
            self.client.error(ex)
            return await self.stop()

        new_offset = (data.msg_id >> 32) - time.time()
        if self.time_offset is None or abs(new_offset - self.time_offset) > 5:
            self.time_offset = new_offset

        if data.body["_"] == "msgContainer":
            for msg in data.body["messages"]:
                self.loop.create_task(self.handle_message(msg))
        else:
            self.loop.create_task(self.handle_message(data))

        if len(self.pending_acks) > 10:
            await self.send({
                "_": "msgsAck",
                "msg_ids": list(self.pending_acks)
            }, False)
            self.pending_acks.clear()

    async def recv_worker(self):
        while True:
            packet = await self.connection.recv()

            if packet is None:
                self.client.error("Сервер ничего не отправил")
                break
            if len(packet) == 4:
                if packet == b"l\xfe\xff\xff":
                    self.client.error("Ошибка 404 (AuthKeyNotFound) указанный идентификатор ключ не может быть найден DC / какой-либо из указанных запросов неправильный / некоторые поля MTProto неверны")
                elif packet == b"S\xfe\xff\xff":
                    self.client.error("Ошибка 429 (TransportFlood) слишком много транспортных соединений с одним IP / какой-либо из ограничений контейнера (сервисного сообщения) достигнут")
                elif packet == b"D\xfe\xff\xff":
                    self.client.error("Ошибка 444 (InvalidDC) возвращается при создании ключей, подключающегося к MTProxy если указан неверный DC ID")
                else:
                    self.client.error(f"Неизвестная ошибка сервера - {struct.unpack('<i', packet)[0]}")
                break

            self.loop.create_task(self.handle_packet(packet))

        await self.stop()

    async def ping_worker(self):
        while True:
            await asyncio.sleep(20)
            try:
                await self.send({
                    "_": "pingDelayDisconnect",
                    "ping_id": self.msg_factory.get_msg_id(),
                    "disconnect_delay": 25
                }, False)
            except Exception:
                break

        await self.stop()

    async def send(self, body: dict, response=True, timeout=10) -> dict | None:
        message = self.msg_factory.create(body)

        if response:
            self.wait_packet[message.msg_id] = self.loop.create_future()

        data = await self.loop.run_in_executor(
            self.pool_executor,
            self.connection.pack,
            message
        )

        try:
            await self.connection.send(data)
        except Exception as ex:
            self.wait_packet.pop(message.msg_id, None)
            raise ex

        if not response:
            return None

        result = await self.wait_packet[message.msg_id]

        if result is None:
            self.client.error("Время запроса вышло")
            raise TimeoutError("Время запроса вышло")
        elif result["_"] == "rpcError":
            raise Exception(f"RpcError [{result['error_code']}] - {result['error_message']} (by {body['_']})")
        elif result["_"] == "badMsgNotification":
            if result.error_code in BADMSGNOTIFICATIONS:
                self.client.warn(f"BadMsgNotification [{result['error_code']}] - {BADMSGNOTIFICATIONS[result['error_code']]}")
            else:
                self.client.warn(f"BadMsgNotification [{result['error_code']}] - Неизвестный код ошибки")
        elif result["_"] == "badServerSalt":
            self.connection.set_salt(result["new_server_salt"])
            return await self.send(body, response, timeout)

        return result

    async def _invoke_batch_worker(self):
        while True:
            await self._batch_event.wait()

            await asyncio.sleep(0.02)

            batch = self._batch_list
            self._batch_list = []
            self._batch_event.clear()

            if not batch:
                continue

            try:
                if len(batch) == 1:
                    message_to_send = batch[0]
                else:
                    container = MsgContainer(batch).write()
                    message_to_send = CoreMessage(
                        msg_id=self.msg_factory.get_msg_id(),
                        seq_no=self.msg_factory.get_seq_no({"_": "msgContainer"}),
                        length=len(container),
                        body=container
                    )

                data = await self.loop.run_in_executor(
                    self.pool_executor,
                    self.connection.pack,
                    message_to_send
                )

                if self._state in {1, 2}:
                    await self.connection.send(data)
            except Exception as ex:
                self.client.error(ex)
                [self.wait_packet.pop(msg.msg_id).set_result(None) for msg in batch if msg.msg_id in self.wait_packet]

    async def stop(self, r=1):
        if self._state != 2:
            return self.client.warn(f"Статус сессии == {self._state}, остановка пропущена")

        self._state = 3

        try:
            self._recv_task.cancel()
        except:
            pass
        try:
            self._batch_task.cancel()
        except:
            pass
        try:
            self._ping_task.cancel()
        except:
            pass

        self.connection.disconnect()

        self._state = 0

        if r:
            await self.start()

    async def start(self):
        if self._state != 0:
            return self.client.warn(f"Статус сессии == {self._state}, запуск пропущен")

        try:
            self._state = 1

            await self.connection.init()
            await self.connection.connect()

            self._recv_task = self.loop.create_task(self.recv_worker())
            self._batch_task = self.loop.create_task(self._invoke_batch_worker())

            await self.send({"_": "ping", "ping_id": 0}, timeout=5)

            await self.send({
                "_": "invokeWithLayer",
                "layer": 223,
                "query": {
                    "_": "initConnection",
                    "api_id": self.client.api_id,
                    **self.client._init_config,
                    "query": {
                        "_": "getConfig"
                    }
                }
            }, timeout=5)

            if self.connection._isAuth == 1:
                botauth = await self.send({
                    "_": "auth.importBotAuthorization",
                    "flags": 0,
                    "api_id": self.client.api_id,
                    "api_hash": self.client.api_hash,
                    "bot_auth_token": self.client.bot_token,
                })

                if botauth and "result" not in botauth:
                    raise RuntimeError(f"Ошибка авторизации бота -> {botauth}")

                botauth = botauth["result"]

                if botauth["_"] == "rpcError":
                    if "USER_MIGRATE_" in botauth["error_message"]:
                        self.client.storage["dc_id"] = int(botauth["error_message"][-1])
                        self.client.storage["auth_key"] = None
                        self._state = 2
                        await self.stop()
                        return

                    raise ValueError(f"rpcError ({botauth['error_code']}) {botauth['error_message']}")

                self.client.storage["id"] = botauth["user"]["id"]
                self.client.storage["first_name"] = botauth["user"]["first_name"]
                self.client.storage["username"] = botauth["user"]["username"]
                self.client.save_storage()

            self._ping_task = self.loop.create_task(self.ping_worker())

            self._state = 2
        except Exception as ex:
            self._state = 0
            self.client.error(f"Ошибка запуска сессии -> {ex}")
