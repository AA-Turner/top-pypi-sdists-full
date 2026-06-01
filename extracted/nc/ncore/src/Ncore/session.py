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

import os
import time
import struct
import socket
import asyncio
import tgcrypto

from io import BytesIO
from base64 import b64encode
from hashlib import sha1, sha256
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor


from .utils import Auth, MsgFactory
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


class Connect:
    __slots__ = (
        "client", "loop", "sock", "address", "_state", "_isAuth", "session_id", "auth_key", "auth_key_id", 
        "__ak_036", "__ak_4076", "__ak_88120", "__ak_844", "__ak_4884", "__ak_96128", "salt",
    )

    def __init__(self, address: tuple[str, int]=("149.154.167.51", 443)):
        self.address = address

        self._state = 0
        self._isAuth = 0

        self.set_salt(0)
        self.session_id = os.urandom(8)

    async def init(self):
        self.loop = self.client.loop

        if not self.client.storage["auth_key"]:
            self.client.warn("Получение auth_key")
            await Auth(self.client, self)()

            self._isAuth = 1
            self.client.info("Получен auth_key")

        self.auth_key = self.client.storage["auth_key"]
        self.auth_key_id = sha1(self.auth_key).digest()[-8:]

        self.__ak_036 = self.auth_key[0:36]
        self.__ak_4076 = self.auth_key[40:76]
        self.__ak_88120 = self.auth_key[88:120]

        self.__ak_844 = self.auth_key[8:44]
        self.__ak_4884 = self.auth_key[48:84]
        self.__ak_96128 = self.auth_key[96:128]

    def set_salt(self, value):
        self.salt = struct.pack("<Q", value)

    def kdf_pack(self, msg_key):
        h_a = sha256(msg_key)
        h_a.update(self.__ak_036)
        sha256_a = h_a.digest()

        h_b = sha256(self.__ak_4076)
        h_b.update(msg_key)
        sha256_b = h_b.digest()

        return (
            sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32],
            sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
        )

    def kdf_unpack(self, msg_key):
        h_a = sha256(msg_key)
        h_a.update(self.__ak_844)
        sha256_a = h_a.digest()

        h_b = sha256(self.__ak_4884)
        h_b.update(msg_key)
        sha256_b = h_b.digest()

        return (
            sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32],
            sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]
        )

    def pack(self, message):
        data = self.salt + self.session_id + message.write()

        padding_len = 16 - (len(data) % 16)
        if padding_len < 12:
            padding_len += 16
        data_padding = data + os.urandom(padding_len)

        h_msg = sha256(self.__ak_88120)
        h_msg.update(data_padding)
        msg_key = h_msg.digest()[8:24]

        aes_key, aes_iv = self.kdf_pack(msg_key)

        return self.auth_key_id + msg_key + tgcrypto.ige256_encrypt(data_padding, aes_key, aes_iv)

    def unpack(self, data):
        if data[0:8] != self.auth_key_id:
            raise ValueError("Ошибка безопасности не верный auth_key_id")

        msg_key = data[8:24]
        aes_key, aes_iv = self.kdf_unpack(msg_key)
        decrypted_data = tgcrypto.ige256_decrypt(data[24:], aes_key, aes_iv)
        data = decrypted_data[8:]

        if data[0:8] != self.session_id:
            raise ValueError("Ошибка безопасности не верный session_id")
        if msg_key != sha256(self.__ak_96128 + decrypted_data).digest()[8:24]:
            raise ValueError("Ошибка безопасности не верный msg_key")

        message = CoreMessage.read(BytesIO(data[8:]))
        payload_len = len(decrypted_data) - 32

        if not 12 <= (payload_len - message.length) <= 1024:
            raise ValueError("Ошибка безопасности не верный length padding")
        if not payload_len % 4 == 0:
            raise ValueError("Ошибка безопасности не верный length payload")
        if not message.msg_id % 2 != 0:
            raise ValueError("Ошибка безопасности не верный msg_id")

        return message

    def disconnect(self):
        try:
            self.sock.close()
        except:
            pass
        self._state = 0

    async def proxy_handshake_socks5(self, address, target_address, username, password):
        await self.loop.sock_connect(self.sock, address)

        if username and password:
            await self.loop.sock_sendall(self.sock, b"\x05\x01\x02")
            res = await self.loop.sock_recv(self.sock, 2)
            if res != b"\x05\x02":
                self.client.error("Прокси не поддерживает авторизацию")
                raise ConnectionError()

            user_b, pass_b = username.encode(), password.encode()
            u_len, p_len = len(user_b), len(pass_b)
            auth_req = struct.pack(f"<BB{u_len}sB{p_len}s", 0x01, u_len, user_b, p_len, pass_b)

            await self.loop.sock_sendall(self.sock, auth_req)

            auth_res = await self.loop.sock_recv(self.sock, 2)
            if auth_res != b"\x01\x00":
                self.client.error("Ошибка авторизации прокси")
                raise ConnectionError()
        else:
            await self.loop.sock_sendall(self.sock, b"\x05\x01\x00")
            res = await self.loop.sock_recv(self.sock, 2)
            if res != b"\x05\x00":
                self.client.error("Прокси требует авторизацию / Не доступен")
                raise ConnectionError()

        ip_bytes = socket.inet_aton(target_address[0])
        connect_req = struct.pack(">BBBB4sH", 0x05, 0x01, 0x00, 0x01, ip_bytes, target_address[1])

        await self.loop.sock_sendall(self.sock, connect_req)

        conn_res = await self.loop.sock_recv(self.sock, 10)
        if len(conn_res) < 2 or conn_res[1] != 0x00:
            err_code = conn_res[1] if len(conn_res) > 1 else "Unknown"
            self.client.error(f"Ошибка подключения: {err_code}")
            raise ConnectionError()

    async def proxy_handshake_http(self, address, target_address, username, password):
        await self.loop.sock_connect(self.sock, address)

        headers = f"CONNECT {target_address[0]}:{target_address[1]} HTTP/1.1\r\nHost: {target_address[0]}:{target_address[1]}\r\n"
        if username and password:
            b64_auth = b64encode(f"{username}:{password}".encode()).decode()
            headers += f"Proxy-Authorization: Basic {b64_auth}\r\n"
        headers += "\r\n"

        await self.loop.sock_sendall(self.sock, headers.encode())

        response = await self.loop.sock_recv(self.sock, 4096)
        if b" 200" not in response.split(b"\r\n")[0]:
            self.client.error(f"Ошибка прокси: {response.decode(errors='ignore')}")
            raise ConnectionError()

    async def connect(self, socket_timeout=10, retrying=3):
        address = self.address

        if self._state != 0:
            return self.client.info("Клиент уже подключён")

        handshake = None

        if self.client.proxy:
            proxy_data = urlparse(self.client.proxy)
            ptype = proxy_data.scheme.lower()

            if ptype.startswith("socks5"):
                handshake = self.proxy_handshake_socks5
            elif ptype.startswith("http"):
                handshake = self.proxy_handshake_http
            else:
                self.client.error(f"Не известный тип прокси - {ptype}. Доступно [socks5/http]")
                raise ConnectionError()

        for _ in range(retrying):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(socket_timeout)
                self.sock.setblocking(False)

                if handshake is not None:
                    await handshake((proxy_data.hostname, proxy_data.port), address, proxy_data.username, proxy_data.password)
                else:
                    await self.loop.sock_connect(self.sock, address)

                await self.loop.sock_sendall(self.sock, b"\xef")
            except BaseException as ex:
                self.client.error(f"Ошибка подключения -> {ex}")
                await asyncio.sleep(1.5)
            else:
                self.client.info(f"Подключено к {address}")
                self._state = 1
                return
        self.client.error(f"Не подключился к {address}, после {retrying} попыток")
        raise ConnectionError()

    async def send(self, data):
        length = len(data) // 4

        try:
            if length < 127:
                data = struct.pack(f"<B{len(data)}s", length, data)
            else:
                data = struct.pack(f"<I{len(data)}s", (length << 8) | 0x7f, data)
            await self.loop.sock_sendall(self.sock, data)
        except BaseException as ex:
            self.client.error(f"Ошибка отправки -> {ex}")

    async def recv(self):
        length = await self.loop.sock_recv(self.sock, 1)

        if not length:
            return None
        if length == b"\x7f":
            length = await self.loop.sock_recv(self.sock, 3)
            if not length:
                return None
            length = struct.unpack("<I", length + b"\x00")[0] * 4
        else:
            length = length[0] * 4

        buf = bytearray(length)
        view = memoryview(buf)

        try:
            lbytes = await asyncio.wait_for(self.loop.sock_recv_into(self.sock, view), timeout=10)
        except (OSError, asyncio.TimeoutError):
            return None
        if lbytes == length:
            return view
        if lbytes == 0:
            return None

        while lbytes < length:
            try:
                chunk_size = await asyncio.wait_for(self.loop.sock_recv_into(self.sock, view[lbytes:]), timeout=10)
            except (OSError, asyncio.TimeoutError):
                return None
            if chunk_size == 0:
                return None
            lbytes += chunk_size
        return view


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
        except BaseException as ex:
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
            except:
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
        except BaseException as ex:
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
                    raise

                botauth = botauth["result"]

                self.client.storage["id"] = botauth["user"]["id"]
                self.client.storage["first_name"] = botauth["user"]["first_name"]
                self.client.storage["username"] = botauth["user"]["username"]
                self.client.save_storage()

            self._ping_task = self.loop.create_task(self.ping_worker())

            self._state = 2
        except Exception as ex:
            self._state = 0
            self.client.error(f"Ошибка запуска сессии -> {ex}")
