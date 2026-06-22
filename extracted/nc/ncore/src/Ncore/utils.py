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
import tgcrypto

from io import BytesIO
from hashlib import sha1


from . import rsa
from .tl_object import (
    CoreMessage, parser,
    PQInnerData, ReqPqMulti, ReqDHParams, ServerDHInnerData, ClientDHInnerData,
    SetClientDHParams, ResPQ, ServerDHParamsOk, ServerDHParamsFail, DhGenOk
)


def get_tl_object(data):
    cid = data[0:4]

    if cid == b"c$\x16\x05": # ResPQ 0x05162463
        return ResPQ.read(BytesIO(data[4:]))
    if cid == b"\\\x07\xe8\xd0": # ServerDHParamsOk 0xd0e8075c
        return ServerDHParamsOk.read(BytesIO(data[4:]))
    if cid == b"]\x04\xcby": # ServerDHParamsFail 0x79cb045d
        return ServerDHParamsFail.read(BytesIO(data[4:]))
    if cid == b"4\xf7\xcb;": # DhGenOk 0x3bcbf734
        return DhGenOk.read(BytesIO(data[4:]))

    raise ValueError(f"Не известный конструктор {cid}")


class MsgFactory:
    __slots__ = ("session", "_msg_id", "_content_messages")

    def __init__(self, session):
        self.session = session

        self._msg_id = 0
        self._content_messages = 0

    def get_msg_id(self):
        msg_id = int(self.session.server_time() * 4294967296) & ~0b11
        if msg_id <= self._msg_id:
            msg_id = self._msg_id + 4

        self._msg_id = msg_id

        return msg_id

    def get_seq_no(self, body: dict):
        if body["_"] in {"ping", "msgsAck", "msgContainer", "msgCopy", "gzipPacked"}:
            seq_no = self._content_messages * 2
        else:
            seq_no = self._content_messages * 2 + 1
            self._content_messages += 1

        return seq_no

    def create(self, body: dict):
        msg_id = self.get_msg_id()
        seq_no = self.get_seq_no(body)

        body_bytes = parser.pack(body)
        return CoreMessage(msg_id, seq_no, len(body_bytes), body_bytes)


class Auth:
    __slots__ = ("client", "loop", "connection", "_last_sync_time", "_last_monotonic")

    def __init__(self, client, connection):
        self.client = client
        self.loop = client.loop
        self.connection = connection

        self._last_sync_time = time.time()
        self._last_monotonic = time.monotonic()

    async def invoke(self, body: bytes):
        data = struct.pack("<8sqi",
            b"\x00\x00\x00\x00\x00\x00\x00\x00",
            int((self._last_sync_time + (time.monotonic() - self._last_monotonic)) * 4294967296) & ~0b11,
            len(body)
        ) + body

        await self.connection.send(data)

        packet = await self.connection.recv()

        if len(packet) == 4:
            if packet == b"l\xfe\xff\xff": # 404 AuthKeyNotFound
                self.client.error("Ошибка 404 (AuthKeyNotFound) указанный идентификатор ключ не может быть найден DC / какой-либо из указанных запросов неправильный / некоторые поля MTProto неверны")
            elif packet == b"S\xfe\xff\xff": # 429 TransportFlood
                self.client.error("Ошибка 429 (TransportFlood) слишком много транспортных соединений с одним IP / какой-либо из ограничений контейнера (сервисного сообщения) достигнут")
            elif packet == b"D\xfe\xff\xff": # 444 InvalidDC
                self.client.error("Ошибка 444 (InvalidDC) возвращается при создании ключей, подключающегося к MTProxy если указан неверный DC ID")
            else:
                self.client.error(f"Неизвестная ошибка сервера - {struct.unpack('<i', packet)[0]}")
            raise ConnectionAbortedError()

        return get_tl_object(packet[20:])

    async def __call__(self, retrying=3):
        for _ in range(retrying):
            try:
                await self.connection.connect()
            except ConnectionError:
                continue

            nonce = int.from_bytes(os.urandom(16), "little", signed=True)
            try:
                res_pq = await self.invoke(ReqPqMulti(nonce=nonce).write())
            except ConnectionAbortedError:
                continue

            for i in res_pq.server_public_key_fingerprints:
                if i in rsa.server_public_keys:
                    public_key_fingerprint = i
                    break
            else:
                raise KeyError("Серверный ключ не найден")

            pq = int.from_bytes(res_pq.pq, "big")
            g = rsa.decompose(pq)
            p, q = sorted((g, pq // g))

            server_nonce = res_pq.server_nonce
            new_nonce = int.from_bytes(os.urandom(32), "little", signed=True)

            data = PQInnerData(
                pq=res_pq.pq,
                p=p.to_bytes(4, "big"),
                q=q.to_bytes(4, "big"),
                nonce=nonce,
                server_nonce=server_nonce,
                new_nonce=new_nonce,
            ).write()

            sha = sha1(data).digest()
            padding = os.urandom(-(len(data) + len(sha)) % 255)
            encrypted_data = rsa.encrypt(sha + data + padding, public_key_fingerprint)

            try:
                server_dh_params = await self.invoke(
                    ReqDHParams(
                        nonce=nonce,
                        server_nonce=server_nonce,
                        p=p.to_bytes(4, "big"),
                        q=q.to_bytes(4, "big"),
                        public_key_fingerprint=public_key_fingerprint,
                        encrypted_data=encrypted_data
                    ).write()
                )
            except ConnectionAbortedError:
                continue

            encrypted_answer = server_dh_params.encrypted_answer

            server_nonce = server_nonce.to_bytes(16, "little", signed=True)
            new_nonce = new_nonce.to_bytes(32, "little", signed=True)

            tmp_aes_key = sha1(new_nonce + server_nonce).digest() + sha1(server_nonce + new_nonce).digest()[:12]
            tmp_aes_iv = sha1(server_nonce + new_nonce).digest()[12:] + sha1(new_nonce + new_nonce).digest() + new_nonce[:4]

            server_nonce = int.from_bytes(server_nonce, "little", signed=True)

            answer_with_hash = tgcrypto.ige256_decrypt(encrypted_answer, tmp_aes_key, tmp_aes_iv)
            server_dh_inner_data = ServerDHInnerData.read(BytesIO(answer_with_hash[24:]))

            dh_prime = int.from_bytes(server_dh_inner_data.dh_prime, "big")

            g = server_dh_inner_data.g
            b = int.from_bytes(os.urandom(256), "big")
            g_b = pow(g, b, dh_prime).to_bytes(256, "big")

            retry_id = 0

            data = ClientDHInnerData(
                nonce=nonce,
                server_nonce=server_nonce,
                retry_id=retry_id,
                g_b=g_b
            ).write()

            sha = sha1(data).digest()
            padding = os.urandom(-(len(data) + len(sha)) % 16)
            encrypted_data = tgcrypto.ige256_encrypt((sha + data + padding), tmp_aes_key, tmp_aes_iv)

            set_client_dh_params_answer = await self.invoke(
                SetClientDHParams(
                    nonce=nonce,
                    server_nonce=server_nonce,
                    encrypted_data=encrypted_data
                ).write()
            )

            g_a = int.from_bytes(server_dh_inner_data.g_a, "big")
            auth_key = pow(g_a, b, dh_prime).to_bytes(256, "big")
            server_nonce = server_nonce.to_bytes(16, "little", signed=True)

            try:
                if not dh_prime == 25135566567101483196994790440833279750474660393232382279277736257066266618532493517139001963526957179514521981877335815379755618191324858392834843718048308951653115284529736874534289456833723962912807104017411854314007953484461899139734367756070456068592886771130491355511301923675421649355211882120329692353507392677087555292357140606251171702417804959957862991259464749806480821163999054978911727901705780417863120490095024926067731615229486812312187386108568833026386220686253160504779704721744600638258183939573405528962511242337923530869616215532193967628076922234051908977996352800560160181197923404454023908443:
                    raise ValueError("Ошибка безопасности dh_prime(0)")
                if not 1 < g < dh_prime - 1:
                    raise ValueError("Ошибка безопасности dh_prime(1)")
                if not 1 < g_a < dh_prime - 1:
                    raise ValueError("Ошибка безопасности dh_prime(2)")
                g_b = int.from_bytes(g_b, "big")
                if not 1 < g_b < dh_prime - 1:
                    raise ValueError("Ошибка безопасности dh_prime(3)")
                check = 1751908409537131537220509645351687597690304110853111572994449976845956819751541616602568796259317428464425605223064365804210081422215355425149431390635151955247955156636234741221447435733643262808668929902091770092492911737768377135426590363166295684370498604708288556044687341394398676292971255828404734517580702346564613427770683056761383955397564338690628093211465848244049196353703022640400205739093118270803778352768276670202698397214556629204420309965547056893233608758387329699097930255380715679250799950923553703740673620901978370802540218870279314810722790539899334271514365444369275682816
                if not check < g_a < dh_prime - check:
                    raise ValueError("Ошибка безопасности dh_prime(4)")
                if not check < g_b < dh_prime - check:
                    raise ValueError("Ошибка безопасности dh_prime(5)")

                answer = server_dh_inner_data.write()
                if not answer_with_hash[:20] == sha1(answer).digest():
                    raise ValueError("Ошибка безопасности answer_with_hash")

                if not nonce == res_pq.nonce:
                    raise ValueError("Ошибка безопасности nonce(0)")
                if not nonce == server_dh_params.nonce:
                    raise ValueError("Ошибка безопасности nonce(1)")
                server_nonce = int.from_bytes(server_nonce, "little", signed=True)
                if not server_nonce == server_dh_params.server_nonce:
                    raise ValueError("Ошибка безопасности server_nonce(0)")
                if not nonce == set_client_dh_params_answer.nonce:
                    raise ValueError("Ошибка безопасности nonce(2)")
                if not server_nonce == set_client_dh_params_answer.server_nonce:
                    raise ValueError("Ошибка безопасности server_nonce(1)")
            except ValueError as ex:
                self.client.error(f"Повторное получение ключа. Ошбика -> {ex}")
                continue

            self.client.storage["auth_key"] = auth_key

            return auth_key
