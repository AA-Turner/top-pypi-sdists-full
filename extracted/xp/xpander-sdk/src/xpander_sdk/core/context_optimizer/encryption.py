"""
Encryption utilities for context optimization files.

Uses a stdlib-only XOR stream cipher with SHA-256 derived key.
No external dependencies required — works everywhere.

Key derivation: sha256("{org_id}_{agent_id}_{task_id}")
Encryption: XOR with SHA-256 counter-mode key stream, base64-encoded output.
Symmetric: same function encrypts and decrypts the raw bytes.
"""

import asyncio
import base64
import hashlib

# offload encrypt/decrypt of large payloads to a thread so even the linear XOR
# pass (session backups can be multi-MB) doesn't block the event loop
_THREAD_OFFLOAD_BYTES = 256 * 1024


def derive_key(org_id: str, agent_id: str, task_id: str) -> bytes:
    """Derive a 256-bit encryption key from context identifiers."""
    material = f"{org_id}_{agent_id}_{task_id}"
    return hashlib.sha256(material.encode()).digest()


def conversation_scope_id(task) -> str:
    """Scope id for an offloaded file's key. The root (gateway) execution id when
    the task is a sub-execution, else the task's own id — so content offloaded in
    one sub-execution can be decrypted from a sibling sub-execution of the same
    conversation."""
    return (getattr(task, "parent_execution", None) or getattr(task, "id", "")) or ""


def candidate_scope_ids(task) -> list:
    """Decrypt key-scope candidates, most-specific first: the task's own id, then
    the conversation root. Covers same-task files, sibling sub-execution files,
    and legacy per-task files written before the conversation-scoped key."""
    ids = []
    for cand in (getattr(task, "id", ""), getattr(task, "parent_execution", None)):
        if cand and cand not in ids:
            ids.append(cand)
    return ids


def try_decrypt(data: str, keys: list) -> str:
    """Decrypt *data* trying each key in order; return the first that yields valid
    UTF-8. A wrong XOR key almost always trips ``UnicodeDecodeError`` on a real
    payload, so the first clean decode is the right key. Raises if none work."""
    last_err: Exception = ValueError("no keys provided")
    for key in keys:
        try:
            return decrypt(data, key)
        except Exception as e:
            last_err = e
    raise last_err


def _xor_stream(data: bytes, key: bytes) -> bytes:
    """XOR data with a SHA-256 counter-mode key stream."""
    n = len(data)
    if not n:
        return b""
    # collect blocks then join once (avoids O(n^2) bytes concat in the loop)
    blocks = []
    produced = 0
    counter = 0
    while produced < n:
        block = hashlib.sha256(key + counter.to_bytes(4, "big")).digest()
        blocks.append(block)
        produced += len(block)
        counter += 1
    key_stream = b"".join(blocks)[:n]
    # single big-int XOR instead of a per-byte Python loop
    xored = int.from_bytes(data, "big") ^ int.from_bytes(key_stream, "big")
    return xored.to_bytes(n, "big")


def _encrypt_bytes(data: bytes, key: bytes) -> str:
    """XOR-encrypt raw bytes and return base64 ciphertext."""
    return base64.b64encode(_xor_stream(data, key)).decode("ascii")


def encrypt(data: str, key: bytes) -> str:
    """Encrypt a string and return base64-encoded ciphertext.

    Base64 encoding ensures the output survives text-based file I/O
    (workspace file_read/file_write operate on UTF-8 strings).
    """
    return _encrypt_bytes(data.encode("utf-8"), key)


def decrypt(data: str, key: bytes) -> str:
    """Decrypt a base64-encoded ciphertext back to plaintext string."""
    encrypted = base64.b64decode(data.encode("ascii"))
    return _xor_stream(encrypted, key).decode("utf-8")


async def aencrypt(data: str, key: bytes) -> str:
    """Async encrypt; offloads big payloads to a thread to keep the loop free."""
    # gate on UTF-8 byte size (the actual work), not character count
    data_bytes = data.encode("utf-8")
    if len(data_bytes) >= _THREAD_OFFLOAD_BYTES:
        return await asyncio.to_thread(_encrypt_bytes, data_bytes, key)
    return _encrypt_bytes(data_bytes, key)


def is_context_optimization_file(path: str) -> bool:
    """Check if a path refers to a context optimization file.

    Matches both root-relative (/CONTEXT_OPTIMIZATION/uuid.xp) and
    absolute (/agent/data/CONTEXT_OPTIMIZATION/uuid.xp) paths.
    """
    return "CONTEXT_OPTIMIZATION/" in path and path.endswith(".xp")
