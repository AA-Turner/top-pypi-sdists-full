from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import hashlib
import json
import time
import fire
from vmodal.errors import ValidationFailed
from vmodal.utils_userid import os_cache_dir


def os_file_stat(path: str) -> Dict[str, int]:
    st = os.stat(path)
    return {
        "device": int(st.st_dev),
        "inode": int(st.st_ino),
        "size": int(st.st_size),
        "mtime_ns": int(st.st_mtime_ns),
    }


def os_file_stat_same(left: Dict[str, int], right: Dict[str, int]) -> bool:
    keys = ("device", "inode", "size", "mtime_ns")
    return all(int(left.get(key, -1)) == int(right.get(key, -2)) for key in keys)


def os_file_range_md5(path: str, offset: int, size: int, read_size: int = 1024 * 1024) -> str:
    md5 = hashlib.md5()
    left = int(size)
    with open(path, "rb") as fh:
        fh.seek(int(offset))
        while left:
            data = fh.read(min(int(read_size), left))
            if not data:
                raise OSError("local file ended before multipart range")
            md5.update(data)
            left -= len(data)
    return md5.hexdigest()


def os_upload_checkpoint_path(user_id: str, path: str) -> str:
    raw = (str(user_id) + "\0" + os.path.abspath(path)).encode("utf-8")
    name = hashlib.sha256(raw).hexdigest() + ".json"
    return os.path.join(os_cache_dir(), "uploads", name)


def os_upload_checkpoint_load(path: str) -> Optional[Dict[str, Any]]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if int(data.get("version", 0)) != 1:
            raise ValueError("unsupported checkpoint version")
        return data
    except Exception as exc:
        bad = path + f".corrupt.{int(time.time())}"
        os.replace(path, bad)
        raise ValidationFailed(
            "multipart upload checkpoint is corrupt",
            status_code=422,
            details=bad,
        ) from exc


def os_upload_checkpoint_save(path: str, data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + f".tmp.{os.getpid()}"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, sort_keys=True, separators=(",", ":"))
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def os_upload_checkpoint_delete(path: str) -> None:
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass


def os_upload_lock_acquire(checkpoint_path: str) -> str:
    lock = checkpoint_path + ".lock"
    os.makedirs(os.path.dirname(lock), exist_ok=True)
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(str(os.getpid()))
                fh.flush()
                os.fsync(fh.fileno())
            return lock
        except FileExistsError:
            try:
                with open(lock, "r", encoding="utf-8") as fh:
                    pid = int(fh.read().strip())
                os.kill(pid, 0)
            except ProcessLookupError:
                os.unlink(lock)
                continue
            except (ValueError, OSError):
                raise ValidationFailed("multipart upload already active", status_code=409, details=lock)
            raise ValidationFailed("multipart upload already active", status_code=409, details=lock)


def os_upload_lock_release(lock: str) -> None:
    try:
        os.unlink(lock)
    except FileNotFoundError:
        pass


class OsPartStream:
    def __init__(self, path: str, offset: int, size: int, read_size: int = 1024 * 1024):
        self.path = path
        self.offset = int(offset)
        self.size = int(size)
        self.read_size = int(read_size)
        self.md5 = hashlib.md5()
        self.read_bytes = 0

    async def __aiter__(self):
        self.md5 = hashlib.md5()
        self.read_bytes = 0
        left = self.size
        with open(self.path, "rb") as fh:
            fh.seek(self.offset)
            while left:
                data = fh.read(min(self.read_size, left))
                if not data:
                    raise OSError("local file ended before multipart range")
                self.md5.update(data)
                self.read_bytes += len(data)
                left -= len(data)
                yield data

    def str_md5(self) -> str:
        return self.md5.hexdigest()


if __name__ == "__main__":
    fire.Fire()
