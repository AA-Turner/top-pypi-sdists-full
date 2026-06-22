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
import hmac
import struct
import socket
import secrets
import asyncio

from os import urandom
from io import BytesIO
from base64 import b64encode
from hashlib import sha1, sha256
from urllib.parse import urlparse
from tgcrypto import ige256_encrypt, ige256_decrypt, ctr256_encrypt, ctr256_decrypt


from .utils import Auth
from .tl_object import CoreMessage


class Connect:
    __slots__ = (
        "client", "loop", "sock", "address", "send", "recv", "_state", "_isAuth", "session_id", "auth_key", "auth_key_id", 
        "__ak_036", "__ak_4076", "__ak_88120", "__ak_844", "__ak_4884", "__ak_96128", "salt",
        "__enc_key", "__enc_ctr", "__enc_iv", "__dec_key", "__dec_ctr", "__dec_iv", "__dec_buf", "__raw_buf", "__first_app_data",
        "_sock_sendall", "_sock_recv", "_sock_recv_into"
    )

    def __init__(self, address: tuple[str, int] | None=None):
        self.address = address
        self._state = 0
        self._isAuth = 0
        self.salt = struct.pack("<Q", 0)
        self.session_id = urandom(8)
        self.send = self._send
        self.recv = self._recv

    async def init(self):
        self.loop = self.client.loop
        if self.address is None:
            self.address = {
                1: "149.154.175.53", 2: "149.154.167.51", 3: "149.154.175.100",
                4: "149.154.167.91", 5: "91.108.56.130"
            }[self.client.storage["dc_id"]], 443
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
        ha = h_a.digest()
        h_b = sha256(self.__ak_4076)
        h_b.update(msg_key)
        hb = h_b.digest()
        return ha[:8] + hb[8:24] + ha[24:32], hb[:8] + ha[8:24] + hb[24:32]

    def kdf_unpack(self, msg_key):
        h_a = sha256(msg_key)
        h_a.update(self.__ak_844)
        ha = h_a.digest()
        h_b = sha256(self.__ak_4884)
        h_b.update(msg_key)
        hb = h_b.digest()
        return ha[:8] + hb[8:24] + ha[24:32], hb[:8] + ha[8:24] + hb[24:32]

    def pack(self, message):
        data = self.salt + self.session_id + message.write()
        padding_len = 16 - (len(data) % 16)
        if padding_len < 12: padding_len += 16
        data_padding = data + urandom(padding_len)
        h_msg = sha256(self.__ak_88120)
        h_msg.update(data_padding)
        msg_key = h_msg.digest()[8:24]
        aes_key, aes_iv = self.kdf_pack(msg_key)
        return self.auth_key_id + msg_key + ige256_encrypt(data_padding, aes_key, aes_iv)

    def unpack(self, data):
        if data[0:8] != self.auth_key_id: raise ValueError("Ошибка безопасности не верный auth_key_id")
        msg_key = data[8:24]
        aes_key, aes_iv = self.kdf_unpack(msg_key)
        decrypted_data = ige256_decrypt(data[24:24 + (len(data[24:]) // 16) * 16], aes_key, aes_iv)
        data = decrypted_data[8:]
        if data[0:8] != self.session_id: raise ValueError("Ошибка безопасности не верный session_id")
        hm = sha256(self.__ak_96128)
        hm.update(decrypted_data)
        if msg_key != hm.digest()[8:24]: raise ValueError("Ошибка безопасности не верный msg_key")
        message = CoreMessage.read(BytesIO(data[8:]))
        payload_len = len(decrypted_data) - 32
        if not 12 <= (payload_len - message.length) <= 1024 or payload_len % 4 != 0 or message.msg_id % 2 == 0:
            raise ValueError("Ошибка безопасности padding/length/msg_id")
        return message

    def disconnect(self):
        try: self.sock.close()
        except: pass
        self._state = 0

    async def proxy_handshake_socks5(self, address, target_address, username, password):
        await self.loop.sock_connect(self.sock, address)
        if username and password:
            await self._sock_sendall(self.sock, b"\x05\x01\x02")
            if await self._sock_recv(self.sock, 2) != b"\x05\x02":
                self.client.error("Прокси не поддерживает авторизацию")
                raise ConnectionError()
            user_b, pass_b = username.encode(), password.encode()
            u_len, p_len = len(user_b), len(pass_b)
            await self._sock_sendall(self.sock, struct.pack(f"<BB{u_len}sB{p_len}s", 0x01, u_len, user_b, p_len, pass_b))
            if await self._sock_recv(self.sock, 2) != b"\x01\x00":
                self.client.error("Ошибка авторизации прокси")
                raise ConnectionError()
        else:
            await self._sock_sendall(self.sock, b"\x05\x01\x00")
            if await self._sock_recv(self.sock, 2) != b"\x05\x00":
                self.client.error("Прокси требует авторизацию / Не доступен")
                raise ConnectionError()
        await self._sock_sendall(self.sock, struct.pack(">BBBB4sH", 0x05, 0x01, 0x00, 0x01, socket.inet_aton(target_address[0]), target_address[1]))
        conn_res = await self._sock_recv(self.sock, 10)
        if len(conn_res) < 2 or conn_res[1] != 0x00:
            self.client.error(f"Ошибка подключения: {conn_res[1] if len(conn_res)>1 else 'Unknown'}")
            raise ConnectionError()

    async def proxy_handshake_http(self, address, target_address, username, password):
        await self.loop.sock_connect(self.sock, address)
        headers = f"CONNECT {target_address[0]}:{target_address[1]} HTTP/1.1\r\nHost: {target_address[0]}:{target_address[1]}\r\n"
        if username and password: headers += f"Proxy-Authorization: Basic {b64encode(f'{username}:{password}'.encode()).decode()}\r\n"
        await self._sock_sendall(self.sock, (headers + "\r\n").encode())
        response = await self._sock_recv(self.sock, 4096)
        if b" 200" not in response.split(b"\r\n")[0]:
            self.client.error(f"Ошибка прокси: {response.decode(errors='ignore')}")
            raise ConnectionError()

    async def proxy_handshake_mtproxy(self, address, target_address, secret, password):
        if not secret: raise ValueError("Не найден/Не передан секрет MTPROXY")
        secret_bytes = bytes.fromhex(secret)
        if secret_bytes[0] in {0xDD, 0xEE}: secret_bytes = secret_bytes[1:]
        secret_bytes = secret_bytes[:16]
        if len(secret_bytes) != 16: raise ValueError("Не верный секрет")
        await self.loop.sock_connect(self.sock, (socket.gethostbyname(address[0]), address[1]))
        ban3, ban4 = {b"220", b"GET", b"\x05\x01\x00", b"\x00\x0e\x38"}, {b"PVrG", b"POST", b"\x05\x02\x00\x02", b"\x01\x00\x00\x00", b"\xee\xee\xee\xee", b"\x00\x00\x00\x00"}
        while True:
            h = urandom(64)
            if h[0] != 0xEF and h[:3] not in ban3 and h[:4] not in ban4: break
        handshake = bytearray(h)
        struct.pack_into("<h", handshake, 60, self.client.storage["dc_id"])
        
        hk_enc = sha256(handshake[8:40])
        hk_enc.update(secret_bytes)
        self.__enc_key, self.__enc_iv = hk_enc.digest(), bytearray(handshake[40:56])
        
        hk_dec = sha256(handshake[::-1][8:40])
        hk_dec.update(secret_bytes)
        self.__dec_key, self.__dec_iv = hk_dec.digest(), bytearray(handshake[::-1][40:56])
        
        self.__enc_ctr, self.__dec_ctr, self.__dec_buf, self.__raw_buf = bytearray(1), bytearray(1), bytearray(), bytearray()
        
        if secret.startswith("dd"):
            handshake[56:60] = b"\xdd\xdd\xdd\xdd"
            handshake[56:64] = ctr256_encrypt(handshake, self.__enc_key, self.__enc_iv, self.__enc_ctr)[56:64]
            self.send, self.recv = self.mtproxy_dd_send, self.mtproxy_dd_recv
            await self._sock_sendall(self.sock, handshake)
        elif secret.startswith("ee"):
            secret_bytes = bytes.fromhex(secret[2:])
            secret_key, domain_bytes = secret_bytes[:16], secret_bytes[16:]
            domain_len = len(domain_bytes)
            P = 2 ** 255 - 19
            fake_pubkey = (secrets.randbelow(P) ** 2 % P).to_bytes(32, "little")
            ClientHello = b"".join([
                b"\x16\x03\x01\x02\x00\x01\x00\x01\xfc\x03\x03", b"\x00" * 32, b"\x20", urandom(32), b"\x00\x20",
                b"\xfa\xfa\x13\x01\x13\x02\x13\x03\xc0\x2b\xc0\x2f\xc0\x2c\xc0\x30\xcc\xa9\xcc\xa8\xc0\x13\xc0\x14\x00\x9c\x00\x9d\x00\x2f\x00\x35",
                b"\x01\x00\x01\x93\x4a\x4a\x00\x00\x00\x00", struct.pack(">HH", 5 + domain_len, 3 + domain_len),
                b"\x00", struct.pack(">H", domain_len), domain_bytes,
                b"\x00\x17\x00\x00\xff\x01\x00\x01\x00\x00\x0a\x00\x0a\x00\x08\xba\xba\x00\x1d\x00\x17\x00\x18",
                b"\x00\x0b\x00\x02\x01\x00\x00\x23\x00\x00\x00\x10\x00\x0e\x00\x0c\x02\x68\x32\x08\x68\x74\x74\x70\x2f\x31\x2e\x31",
                b"\x00\x05\x00\x05\x01\x00\x00\x00\x00\x00\x0d\x00\x12\x00\x10\x04\x03\x08\x04\x04\x01\x05\x03\x08\x05\x05\x01\x08\x06\x06\x01",
                b"\x00\x12\x00\x00\x00\x33\x00\x2b\x00\x29\xba\xba\x00\x01\x00\x00\x1d\x00\x20", fake_pubkey,
                b"\x00\x2d\x00\x02\x01\x01\x00\x2b\x00\x0b\x0a\x9a\x9a\x03\x04\x03\x03\x03\x02\x03\x01",
                b"\x00\x1b\x00\x03\x02\x00\x02\x1a\x1a\x00\x01\x00\x00\x15",
                struct.pack(">H", 517 - (297 + domain_len)), b"\x00" * (517 - (297 + domain_len)),
            ])
            digest = bytearray(hmac.new(secret_key, ClientHello, sha256).digest())
            now = struct.pack("<I", int(time.time()))
            for i in range(4): digest[28 + i] ^= now[i]
            ClientHello = ClientHello[:11] + digest + ClientHello[43:]
            await self._sock_sendall(self.sock, ClientHello)
            
            server_hello = bytearray()
            for _ in range(3):
                header = await self._recv_exactly_cold(5)
                server_hello += header + await self._recv_exactly_cold(struct.unpack(">H", header[3:5])[0])
            
            sh_zero = bytearray(server_hello)
            sh_zero[11:43] = b"\x00" * 32
            
            hm_ex = hmac.new(secret_key, ClientHello[11:43], sha256)
            hm_ex.update(sh_zero)
            if not hmac.compare_digest(server_hello[11:43], hm_ex.digest()):
                raise ConnectionError("ServerHello HMAC mismatch")
                
            handshake[56:60] = b"\xdd\xdd\xdd\xdd"
            handshake[56:64] = ctr256_encrypt(handshake, self.__enc_key, self.__enc_iv, self.__enc_ctr)[56:64]
            self.__first_app_data = handshake
            self.send, self.recv = self.mtproxy_ee_send, self.mtproxy_ee_recv
        else:
            handshake[56:60] = b"\xef\xef\xef\xef"
            handshake[56:64] = ctr256_encrypt(handshake, self.__enc_key, self.__enc_iv, self.__enc_ctr)[56:64]
            self.send, self.recv = self.mtproxy_send, self.mtproxy_recv
            await self._sock_sendall(self.sock, handshake)

    async def connect(self, socket_timeout=10, retrying=3):
        if self._state != 0: return self.client.info("Клиент уже подключён")
        mtproxy, connp = False, ""
        if self.client.proxy:
            proxy_data = urlparse(self.client.proxy)
            ptype = proxy_data.scheme.lower()
            handshake = {"socks5": self.proxy_handshake_socks5, "http": self.proxy_handshake_http, "mtproxy": self.proxy_handshake_mtproxy}.get(ptype.replace("s", "") if ptype.startswith("socks") else ptype)
            if not handshake: raise ConnectionError()
            mtproxy = ptype.startswith("mtproxy")
        for _ in range(retrying):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.sock.settimeout(socket_timeout)
                self.sock.setblocking(False)
                self._sock_sendall = self.loop.sock_sendall
                self._sock_recv = self.loop.sock_recv
                self._sock_recv_into = self.loop.sock_recv_into
                if self.client.proxy:
                    await handshake((proxy_data.hostname, proxy_data.port), self.address, proxy_data.username, proxy_data.password)
                    connp = f" через {proxy_data.hostname}:{proxy_data.port}"
                    if not mtproxy: await self._sock_sendall(self.sock, b"\xef")
                else:
                    await self.loop.sock_connect(self.sock, self.address)
                    await self._sock_sendall(self.sock, b"\xef")
            except BaseException as ex:
                self.client.error(f"Ошибка подключения -> {ex}")
                await asyncio.sleep(1.5)
            else:
                self.client.info(f"Подключено к {self.address[0]}:{self.address[1]}{connp}")
                self._state = 1
                return
        self.client.error(f"Не подключился к {self.address[0]}:{self.address[1]}{connp}")
        raise ConnectionError()

    async def _send(self, data):
        length = len(data) // 4
        try: await self._sock_sendall(self.sock, (struct.pack("<B", length) + data) if length < 127 else (struct.pack("<I", (length << 8) | 0x7f) + data))
        except BaseException as ex: self.client.error(f"Ошибка отправки -> {ex}")

    async def _recv(self):
        length = await self._sock_recv(self.sock, 1)
        if not length: return None
        if length == b"\x7f":
            length3 = await self._sock_recv(self.sock, 3)
            if not length3: return None
            length = struct.unpack("<I", length3 + b"\x00")[0] * 4
        else: length = length[0] * 4
        view = memoryview(bytearray(length))
        lbytes = await self._sock_recv_into(self.sock, view)
        if not lbytes: return None
        while lbytes < length:
            chunk = await self._sock_recv_into(self.sock, view[lbytes:])
            if not chunk: return None
            lbytes += chunk
        return view

    async def mtproxy_send(self, data):
        length = len(data) // 4
        try: await self._sock_sendall(self.sock, ctr256_encrypt((struct.pack("<B", length) + data) if length < 127 else (struct.pack("<I", (length << 8) | 0x7f) + data), self.__enc_key, self.__enc_iv, self.__enc_ctr))
        except BaseException as ex: self.client.error(f"Ошибка отправки -> {ex}")

    async def mtproxy_recv(self):
        enc_length_byte = await self._sock_recv(self.sock, 1)
        if not enc_length_byte: return None
        length_byte = ctr256_decrypt(enc_length_byte, self.__dec_key, self.__dec_iv, self.__dec_ctr)
        if length_byte == b"\x7f":
            enc_length3 = await self._sock_recv(self.sock, 3)
            if not enc_length3: return None
            length = struct.unpack("<I", ctr256_decrypt(enc_length3, self.__dec_key, self.__dec_iv, self.__dec_ctr) + b"\x00")[0] * 4
        else: length = length_byte[0] * 4
        view = memoryview(bytearray(length))
        lbytes = await self._sock_recv_into(self.sock, view)
        if not lbytes: return None
        while lbytes < length:
            chunk = await self._sock_recv_into(self.sock, view[lbytes:])
            if not chunk: return None
            lbytes += chunk
        return memoryview(ctr256_decrypt(view, self.__dec_key, self.__dec_iv, self.__dec_ctr))

    async def mtproxy_dd_send(self, data):
        inner_packet = data + urandom((4 - len(data) % 4) % 4)
        try: await self._sock_sendall(self.sock, ctr256_encrypt(struct.pack("<i", len(inner_packet)) + inner_packet, self.__enc_key, self.__enc_iv, self.__enc_ctr))
        except BaseException as ex: self.client.error(f"Ошибка отправки DD -> {ex}")

    async def mtproxy_dd_recv(self):
        enc_header = await self._sock_recv(self.sock, 4)
        if not enc_header: return None
        enc_body = await self._sock_recv(self.sock, struct.unpack("<i", ctr256_decrypt(enc_header, self.__dec_key, self.__dec_iv, self.__dec_ctr))[0])
        if not enc_body: return None
        return memoryview(ctr256_decrypt(enc_body, self.__dec_key, self.__dec_iv, self.__dec_ctr))

    async def _recv_exactly_cold(self, n: int):
        buf = bytearray(n)
        view = memoryview(buf)
        lbytes = 0
        while lbytes < n:
            chunk = await self._sock_recv_into(self.sock, view[lbytes:])
            if not chunk: raise ConnectionError("Соединение закрыто сервером")
            lbytes += chunk
        return buf

    async def mtproxy_ee_send(self, data):
        inner_packet = data + urandom((4 - len(data) % 4) % 4)
        encrypted_data = ctr256_encrypt(struct.pack("<i", len(inner_packet)) + inner_packet, self.__enc_key, self.__enc_iv, self.__enc_ctr)
        if self.__first_app_data:
            hs, self.__first_app_data = self.__first_app_data, None
            first_chunk, encrypted_data = encrypted_data[:2878 - len(hs)], encrypted_data[2878 - len(hs):]
            await self._sock_sendall(self.sock, b"\x14\x03\x03\x00\x01\x01\x17\x03\x03" + struct.pack(">H", len(hs) + len(first_chunk)) + hs + first_chunk)
        for i in range(0, len(encrypted_data), 2878):
            chunk = encrypted_data[i:i + 2878]
            await self._sock_sendall(self.sock, b"\x17\x03\x03" + struct.pack(">H", len(chunk)) + chunk)

    async def _recv_decrypted_exactly(self, n: int):
        while len(self.__dec_buf) < n:
            while len(self.__raw_buf) >= 5:
                if self.__raw_buf[:3] != b"\x17\x03\x03":
                    raise ConnectionError("Invalid Fake-TLS header")
                payload_len = struct.unpack(">H", self.__raw_buf[3:5])[0]
                if len(self.__raw_buf) >= 5 + payload_len:
                    self.__dec_buf.extend(ctr256_decrypt(self.__raw_buf[5:5+payload_len], self.__dec_key, self.__dec_iv, self.__dec_ctr))
                    del self.__raw_buf[:5+payload_len]
                    continue
                break

            if len(self.__dec_buf) >= n:
                break

            chunk = await self._sock_recv(self.sock, 65536)
            if not chunk: raise ConnectionError("Соединение закрыто сервером")
            self.__raw_buf.extend(chunk)

        result = self.__dec_buf[:n]
        del self.__dec_buf[:n]
        return result

    async def mtproxy_ee_recv(self):
        dec_header = await self._recv_decrypted_exactly(4)
        if not dec_header: return None

        payload_len = struct.unpack("<i", dec_header)[0]
        dec_body = await self._recv_decrypted_exactly(payload_len)


        if not dec_body: return None
        return memoryview(dec_body)
