from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey
)
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash

from .connection import Connection
from .protocol.message import MessageProtocol
from .protocol.signed import SignedProtocol
from .transport.abc import Transport


async def auth(
    transport: Transport,
    privkey_b: bytes,
    peer_pubkey_b: bytes
) -> Connection:
    privkey = Ed25519PrivateKey.from_private_bytes(privkey_b)
    peer_pubkey = Ed25519PublicKey.from_public_bytes(peer_pubkey_b)
    return await _auth(transport, privkey, peer_pubkey)


async def _auth(
    transport: Transport,
    privkey: Ed25519PrivateKey,
    peer_pubkey: Ed25519PublicKey
) -> Connection:
    auth_key = await _exchange_auth_key(transport, privkey, peer_pubkey)
    protocol = MessageProtocol(auth_key)
    connection = Connection(transport, protocol)
    return connection


async def _exchange_auth_key(
    transport: Transport,
    privkey: Ed25519PrivateKey,
    peer_pubkey: Ed25519PublicKey
) -> bytes:
    protocol = SignedProtocol(privkey, peer_pubkey)
    connection = Connection(transport, protocol)

    dh_privkey = X25519PrivateKey.generate()
    dh_pubkey = dh_privkey.public_key()

    dh_pubkey_b = dh_pubkey.public_bytes_raw()
    await connection.send(dh_pubkey_b)

    peer_dh_pubkey_b = await connection.receive()
    peer_dh_pubkey = X25519PublicKey.from_public_bytes(peer_dh_pubkey_b)

    shared_key = dh_privkey.exchange(peer_dh_pubkey)

    kdf = ConcatKDFHash(hashes.SHA256(), 32, None)
    auth_key = kdf.derive(shared_key)

    return auth_key
