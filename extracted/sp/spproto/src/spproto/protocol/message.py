import os
import struct

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from .abc import Protocol


class MessageProtocol(Protocol):
    """
    Scheme:
    -------------------------------------------
    | Nonce | Authentication Tag + Ciphertext |
    -------------------------------------------
    Plaintext (decrypted Ciphertext) scheme:
    -----------------
    | Seq | Payload |
    -----------------
    """
    _SEQ_STRUCT = struct.Struct('<Q')

    def __init__(self,
        auth_key: bytes
    ) -> None:
        self._aead = ChaCha20Poly1305(auth_key)
        self._send_seq = 0
        self._recv_seq = 0

    def pack(self,
        payload: bytes
    ) -> bytes:
        seq = self._get_send_seq()
        seq_b = self._SEQ_STRUCT.pack(seq)
        plaintext = seq_b + payload

        nonce = os.urandom(12)
        ciphertext = self._aead.encrypt(nonce, plaintext, None)
        data = nonce + ciphertext

        return data

    def unpack(self,
        data: bytes
    ) -> bytes:
        nonce, ciphertext = data[:12], data[12:]
        plaintext = self._aead.decrypt(nonce, ciphertext, None)

        seq_b, payload = plaintext[:self._SEQ_STRUCT.size], \
            plaintext[self._SEQ_STRUCT.size:]
        seq, = self._SEQ_STRUCT.unpack(seq_b)
        assert self._get_recv_seq() == seq

        return payload

    def _get_send_seq(self) -> int:
        self._send_seq += 1
        return self._send_seq

    def _get_recv_seq(self) -> int:
        self._recv_seq += 1
        return self._recv_seq
