"""`python -I -m probe.sdk.delivery.service.hashing.child <fd>`: one of the service's hashing children (plan
D24): nice 10 and best-effort I/O priority 7 (`ionice -c2 -n7`), so a checkpoint's hash never slows
a hook or a command. It takes jobs on the socket `fd` (a JSON line with the files' fds) and answers each."""

from __future__ import annotations

import ctypes
import hashlib
import json
import os
import platform
import socket
import sys
import time

CHUNK_BYTES = 1 << 20
#: A job's message (its JSON line) is at most this long.
MAX_JOB_BYTES = 1 << 20
#: `ioprio_set`'s number per Linux architecture (no libc wrapper exists).
_IOPRIO_SET = {"x86_64": 251, "aarch64": 30, "i686": 289, "armv7l": 314}
#: IOPRIO_CLASS_BE (2) << IOPRIO_CLASS_SHIFT (13) | level 7: `ionice -c2 -n7`.
_IOPRIO_BE_7 = (2 << 13) | 7


def set_low_priority() -> None:
    """nice 10, and the lowest best-effort I/O priority where the OS has one. Never raises."""
    try:
        os.nice(10)
    except OSError:
        pass
    try:
        if sys.platform.startswith("linux"):
            number = _IOPRIO_SET.get(platform.machine())
            if number is not None:
                ctypes.CDLL(None, use_errno=True).syscall(number, 1, 0, _IOPRIO_BE_7)  # IOPRIO_WHO_PROCESS, self
        elif sys.platform == "darwin":
            # setiopolicy_np(IOPOL_TYPE_DISK, IOPOL_SCOPE_PROCESS, IOPOL_THROTTLE)
            ctypes.CDLL("/usr/lib/libSystem.B.dylib").setiopolicy_np(0, 0, 3)
    except Exception:  # noqa: BLE001 -- a priority is a courtesy, never a reason not to hash
        pass


def hash_full(fd: int, deadline: float, should_count_lines: bool) -> dict:
    """sha256 of the whole file from byte 0 (by `pread`: the caller's offset never moves), its
    newlines and last byte when `count_lines`; `cut` with the bytes read when the deadline passed."""
    digest = hashlib.sha256()
    done = newlines = 0
    last = None
    while True:
        chunk = os.pread(fd, CHUNK_BYTES, done)
        if not chunk:
            break
        digest.update(chunk)
        if should_count_lines:
            newlines += chunk.count(b"\n")
            last = chunk[-1]
        done += len(chunk)
        if time.monotonic() >= deadline:
            if os.pread(fd, 1, done):
                return {"cut": True, "bytes": done}
            break
    return {"sha256": digest.hexdigest(), "bytes": done, "newlines": newlines, "last": last}


def hash_edges(fd: int, size: int, edge_bytes: int) -> dict:
    """sha256 over the first `edge_bytes` and, past twice that, the last `edge_bytes` of a file
    of the observed `size` (the lineage fingerprint, `identities.hash_file`)."""
    digest = hashlib.sha256()
    head = read_at(fd, edge_bytes, 0)
    digest.update(head)
    tail = read_at(fd, edge_bytes, size - edge_bytes if size > 2 * edge_bytes else len(head))
    digest.update(tail)
    return {"edges": digest.hexdigest(), "bytes": len(head) + len(tail)}


def read_at(fd: int, count: int, offset: int) -> bytes:
    """`count` bytes from `offset` by `pread`, looping on short reads (a network file system may
    give fewer than asked before the end, L1); fewer only at the end of the file."""
    parts = []
    done = 0
    while done < count:
        chunk = os.pread(fd, count - done, offset + done)
        if not chunk:
            break
        parts.append(chunk)
        done += len(chunk)
    return b"".join(parts)


def run_job(job: dict, fds: list[int]) -> list[dict]:
    deadline = time.monotonic() + max(0.0, float(job.get("timeout", 0.0)))
    results = []
    for item, fd in zip(job.get("files") or [], fds):
        try:
            if item.get("mode") == "edges":
                results.append(hash_edges(fd, int(item["size"]), int(item["edge_bytes"])))
            elif time.monotonic() >= deadline:
                results.append({"cut": True, "bytes": 0})
            else:
                results.append(hash_full(fd, deadline, bool(item.get("count_lines"))))
        except OSError as exc:
            results.append({"error": f"{type(exc).__name__}: {exc.strerror or exc}"})
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
    return results


def serve(sock: socket.socket) -> int:
    """One job per message until the service closes its end."""
    while True:
        try:
            data, fds, _flags, _addr = socket.recv_fds(sock, MAX_JOB_BYTES, 253)
        except OSError:
            return 1
        if not data:
            return 0
        try:
            job = json.loads(data.decode("utf-8"))
            answer = {"results": run_job(job, fds)}
        except (ValueError, TypeError, KeyError) as exc:
            for fd in fds:
                try:
                    os.close(fd)
                except OSError:
                    pass
            answer = {"error": f"{type(exc).__name__}: {exc}"}
        sock.sendall(json.dumps(answer).encode("utf-8") + b"\n")


def main(argv: list[str]) -> int:
    if len(argv) != 1 or not argv[0].isdigit():
        print("usage: python -m probe.sdk.delivery.service.hashing.child <socket fd>", file=sys.stderr)
        return 2
    set_low_priority()
    return serve(socket.socket(fileno=int(argv[0])))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
