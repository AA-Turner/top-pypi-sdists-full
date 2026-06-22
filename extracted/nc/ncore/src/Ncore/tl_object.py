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
import json
import struct

from io import BytesIO
from gzip import decompress


from . import tl


def Int128(value, signed=True):
    return value.to_bytes(16, "little", signed=signed)

def Int128_read(data, signed=True):
    return int.from_bytes(data.read(16), "little", signed=signed)

def Int256(value, signed=True):
    return value.to_bytes(32, "little", signed=signed)

def Int256_read(data, signed=True):
    return int.from_bytes(data.read(32), "little", signed=signed)

def Bytes(value):
    length = len(value)
    if length < 254:
        return bytes([length]) + value + bytes(-(length + 1) % 4)
    return bytes([254]) + length.to_bytes(3, "little") + value + bytes(-length % 4)

def Bytes_read(data):
    if not data:
        return b""

    length = data[0]
    if length < 254:
        x = data[1:1+length]
    else:
        length = int.from_bytes(data[1:4], "little")
        x = data[4:4+length]

    return x

def BytesBytesIO_read(data):
    if not data:
        return b""
    length = data.read(1)[0]
    if length < 254:
        x = data.read(length)
        data.read(-(length + 1) % 4)
        return x
    length = int.from_bytes(data.read(3), "little")
    x = data.read(length)
    data.read(-length % 4)
    return x

def get_tl_object(data):
    cid = data[0:4]

    if cid == b"\xa1\xcfr0": # GzipPacked 0x3072CFA1
        data = decompress(Bytes_read(data[4:]))
        cid = data[0:4] 
    if cid == b"\x11\xe5\xb8[": # Message 0x5BB8E511
        return CoreMessage.read(BytesIO(data[4:]))
    if cid == b"\xdc\xf8\xf1s": # MsgContainer 0x73F1F8DC
        return MsgContainer.read(BytesIO(data[4:]))
    if cid == b"\x01m\\\xf3": # RpcResult 0xF35C6D01
        return RpcResult.read(data[4:])

    return parser.unpack(data)


class MsgContainer:
    ID = b"\xdc\xf8\xf1s" # 0x73F1F8DC
    __slots__ = ("messages")

    def __init__(self, messages):
        self.messages = messages

    @staticmethod
    def read(data):
        count = struct.unpack("<i", data.read(4))[0]
        return {"_": "msgContainer", "messages": [CoreMessage.read(data) for _ in range(count)]}

    def write(self):
        return self.ID + struct.pack("<i", len(self.messages)) + b"".join(msg.write() for msg in self.messages)


class DhGenOk:
    ID = b"4\xf7\xcb;" # 0x3bcbf734
    __slots__ = ("nonce", "server_nonce", "new_nonce_hash1",)

    def __init__(self, nonce, server_nonce, new_nonce_hash1):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash1 = new_nonce_hash1

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        new_nonce_hash1 = Int128_read(data)

        return DhGenOk(nonce, server_nonce, new_nonce_hash1)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + Int128(self.new_nonce_hash1)


class ServerDHParamsFail:
    ID = b"]\x04\xcby" # 0x79cb045d
    __slots__ = ("nonce", "server_nonce", "new_nonce_hash",)

    def __init__(self, nonce, server_nonce, new_nonce_hash):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash = new_nonce_hash

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        new_nonce_hash = Int128_read(data)

        return ServerDHParamsFail(nonce, server_nonce, new_nonce_hash)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + Int128(self.new_nonce_hash)


class ServerDHParamsOk:
    ID = b"\\\x07\xe8\xd0" # 0xd0e8075c
    __slots__ = ("nonce", "server_nonce", "encrypted_answer",)

    def __init__(self, nonce, server_nonce, encrypted_answer):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_answer = encrypted_answer

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        encrypted_answer = BytesBytesIO_read(data)

        return ServerDHParamsOk(nonce, server_nonce, encrypted_answer)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + Bytes(self.encrypted_answer)


class ResPQ:
    ID = b"c$\x16\x05" # 0x05162463
    __slots__ = ("nonce", "server_nonce", "pq", "server_public_key_fingerprints")

    def __init__(self, nonce, server_nonce, pq, server_public_key_fingerprints):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.pq = pq
        self.server_public_key_fingerprints = server_public_key_fingerprints

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        pq = BytesBytesIO_read(data)

        data.read(4)
        c = struct.unpack("<i", data.read(4))[0]
        server_public_key_fingerprints = list(struct.unpack(f"<{c}q", data.read(8 * c)))

        return ResPQ(nonce, server_nonce, pq, server_public_key_fingerprints)

    def write(self):
        return (
            self.ID +
            Int128(self.nonce) +
            Int128(self.server_nonce) +
            Bytes(self.pq) +
            b"\x15\xc4\xb5\x1c" +
            struct.pack("<i", len(self.server_public_key_fingerprints)) +
            struct.pack(f"<{len(self.server_public_key_fingerprints)}q", **self.server_public_key_fingerprints)
        )


class SetClientDHParams:
    ID = b"\x1f_\x04\xf5" # 0xf5045f1f
    __slots__ = ("nonce", "server_nonce", "encrypted_data",)

    def __init__(self, nonce, server_nonce, encrypted_data):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_data = encrypted_data

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        encrypted_data = BytesBytesIO_read(data)

        return SetClientDHParams(nonce, server_nonce, encrypted_data)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + Bytes(self.encrypted_data)


class ClientDHInnerData:
    ID = b"T\xb6Cf" # 0x6643b654
    __slots__ = ("nonce", "server_nonce", "retry_id", "g_b",)

    def __init__(self, nonce, server_nonce, retry_id, g_b):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.retry_id = retry_id
        self.g_b = g_b

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        retry_id = struct.unpack("<q", data.read(8))[0]
        g_b = BytesBytesIO_read(data)

        return ClientDHInnerData(nonce, server_nonce, retry_id, g_b)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + struct.pack("<q", self.retry_id) + Bytes(self.g_b)


class ServerDHInnerData:
    ID = b"\xba\r\x89\xb5" # 0xb5890dba
    __slots__ = ("nonce", "server_nonce", "g", "dh_prime", "g_a", "server_time",)

    def __init__(self, nonce, server_nonce, g, dh_prime, g_a, server_time):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.g = g
        self.dh_prime = dh_prime
        self.g_a = g_a
        self.server_time = server_time

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        g = struct.unpack("<i", data.read(4))[0]
        dh_prime = BytesBytesIO_read(data)
        g_a = BytesBytesIO_read(data)
        server_time = struct.unpack("<i", data.read(4))[0]

        return ServerDHInnerData(nonce, server_nonce,g, dh_prime, g_a, server_time)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + struct.pack("<i", self.g) + Bytes(self.dh_prime) + Bytes(self.g_a) + struct.pack("<i", self.server_time)


class ReqDHParams:
    ID = b"\xbe\xe4\x12\xd7" # 0xd712e4be
    __slots__ = ("nonce", "server_nonce", "p", "q", "public_key_fingerprint", "encrypted_data",)

    def __init__(self, nonce, server_nonce, p, q, public_key_fingerprint, encrypted_data):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.p = p
        self.q = q
        self.public_key_fingerprint = public_key_fingerprint
        self.encrypted_data = encrypted_data

    @staticmethod
    def read(data):
        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        p = BytesBytesIO_read(data)
        q = BytesBytesIO_read(data)
        public_key_fingerprint = struct.unpack("<q", data.read(8))[0]
        encrypted_data = BytesBytesIO_read(data)

        return ReqDHParams(nonce, server_nonce, p, q, public_key_fingerprint, encrypted_data)

    def write(self):
        return self.ID + Int128(self.nonce) + Int128(self.server_nonce) + Bytes(self.p) + Bytes(self.q) + struct.pack("<q", self.public_key_fingerprint) + Bytes(self.encrypted_data)


class PQInnerData:
    ID = b"\xecZ\xc9\x83" # 0x83c95aec
    __slots__ = ("pq", "p", "q", "nonce", "server_nonce", "new_nonce",)

    def __init__(self, pq, p, q, nonce, server_nonce, new_nonce):
        self.pq = pq
        self.p = p
        self.q = q
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce = new_nonce

    @staticmethod
    def read(data):
        pq = BytesBytesIO_read(data)
        p = BytesBytesIO_read(data)
        q = BytesBytesIO_read(data)

        nonce = Int128_read(data)
        server_nonce = Int128_read(data)
        new_nonce = Int256_read(data)

        return PQInnerData(pq, p, q, nonce, server_nonce, new_nonce)

    def write(self):
        return self.ID + Bytes(self.pq) + Bytes(self.p) + Bytes(self.q) + Int128(self.nonce) + Int128(self.server_nonce) + Int256(self.new_nonce)


class ReqPqMulti:
    ID = b"\xf1\x8e~\xbe" # 0xbe7e8ef1
    __slots__ = ("nonce",)

    def __init__(self, nonce):
        self.nonce = nonce

    @staticmethod
    def read(data):
        return ReqPqMulti(Int128_read(data))

    def write(self):
        return self.ID + Int128(self.nonce)


class RpcResult:
    ID = b"\x01m\\\xf3" # 0xF35C6D01
    __slots__ = ("req_msg_id", "result",)

    def __init__(self, req_msg_id, result):
        self.req_msg_id = req_msg_id
        self.result = result

    @staticmethod
    def read(data):
        return {"_": "rpcResult", "req_msg_id": struct.unpack("<q", data[0:8])[0], "result": get_tl_object(data[8:])}

    def write(self):
        return self.ID + struct.pack("<q", self.req_msg_id) + self.result.write()


class CoreMessage:
    ID = b"\x11\xe5\xb8[" # 0x5BB8E511
    __slots__ = ("msg_id", "seq_no", "length", "body",)

    def __init__(self, msg_id, seq_no, length, body):
        self.msg_id = msg_id
        self.seq_no = seq_no
        self.length = length
        self.body = body

    @staticmethod
    def read(data):
        msg_id, seq_no, length = struct.unpack("<qii", data.read(16))
        body = get_tl_object(data.read(length))
        return CoreMessage(msg_id, seq_no, length, body)

    def write(self):
        return struct.pack("<qii", self.msg_id, self.seq_no, self.length) + (self.body if isinstance(self.body, bytes) else parser.pack(self.body))


try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tl_schema.json")) as f:
        tl_shema = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Файл не найден. Скачайте https://core.telegram.org/schema/json и поместите в Ncore\\tl_schema.json")


upwork_schema = [
    {
        "id": 0x7abe77ec,
        "predicate": "ping",
        "params": [
            {
                "name": "ping_id",
                "type": "long"
            }
        ],
        "type": "Ping"
    },
    {
        "id": 0x347773c5,
        "predicate": "pong",
        "params": [
            {
                "name": "msg_id",
                "type": "long"
            },
            {
                "name": "ping_id",
                "type": "long"
            }
        ],
        "type": "Pong"
    },
    {
        "id": 0xedd4882a,
        "predicate": "getState",
        "params": [],
        "type": "GetState"
    },
    {
        "id": 0xc4f9186b,
        "predicate": "getConfig",
        "params": [],
        "type": "GetConfig"
    },
    {
        "id": 0xf3427b8c,
        "predicate": "pingDelayDisconnect",
        "params": [
            {
                "name": "ping_id",
                "type": "long"
            },
            {
                "name": "disconnect_delay",
                "type": "int"
            }
        ],
        "type": "PingDelayDisconnect"
    },
    {
        "id": 0x2144ca19,
        "predicate": "rpcError",
        "params": [
            {
                "name": "error_code",
                "type": "int"
            },
            {
                "name": "error_message",
                "type": "string"
            }
        ],
        "type": "RpcError"
    },
    {
        "id": 0xbe7e8ef1,
        "predicate": "ReqPqMulti",
        "params": [
            {
                "name": "nonce",
                "type": "int"
            }
        ],
        "type": "ReqPqMulti"
    },
    {
        "id": 0xedab447b,
        "predicate": "badServerSalt",
        "params": [
            {
                "name": "bad_msg_id",
                "type": "long"
            },
            {
                "name": "bad_msg_seqno",
                "type": "int"
            },
            {
                "name": "error_code",
                "type": "int"
            },
            {
                "name": "new_server_salt",
                "type": "long"
            }
        ],
        "type": "BadServerSalt"
    },
    {
        "id": 0x9ec20908,
        "predicate": "newSessionCreated",
        "params": [
            {
                "name": "first_msg_id",
                "type": "long"
            },
            {
                "name": "unique_id",
                "type": "long"
            },
            {
                "name": "server_salt",
                "type": "long"
            }
        ],
        "type": "NewSessionCreated"
    },
    {
        "id": 0x62d6b459,
        "predicate": "msgsAck",
        "params": [
            {
                "name": "msg_ids",
                "type": "Vector<long>"
            }
        ],
        "type": "MsgsAck"
    },
]


tl_shema["constructors"].extend(upwork_schema)

parser = tl.TLParser(tl_shema)
