from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)

from .abc import Protocol


class SignedProtocol(Protocol):
    """
    Scheme:
    -----------------------
    | Signature | Payload |
    -----------------------
    """

    def __init__(self,
        privkey: Ed25519PrivateKey,
        peer_pubkey: Ed25519PublicKey
    ) -> None:
        self._privkey = privkey
        self._peer_pubkey = peer_pubkey

    def pack(self,
        payload: bytes
    ) -> bytes:
        signature = self._privkey.sign(payload)
        data = signature + payload
        return data

    def unpack(self,
        data: bytes
    ) -> bytes:
        signature, payload = data[:64], data[64:]
        self._peer_pubkey.verify(signature, payload)
        return payload
