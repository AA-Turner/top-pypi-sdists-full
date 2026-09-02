from __future__ import annotations

import errno
import os
from typing import NoReturn


def raise_enoent(path: str) -> NoReturn:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)


def raise_eisdir(path: str) -> NoReturn:
    raise IsADirectoryError(errno.EISDIR, os.strerror(errno.EISDIR), path)


def raise_enotdir(path: str) -> NoReturn:
    raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), path)


def raise_eexist(path: str) -> NoReturn:
    raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), path)


def raise_enotempty(path: str) -> NoReturn:
    raise OSError(errno.ENOTEMPTY, os.strerror(errno.ENOTEMPTY), path)


def raise_eacces(path: str) -> NoReturn:
    raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), path)


def raise_einval(path: str, msg: str | None = None) -> NoReturn:
    raise OSError(errno.EINVAL, msg or os.strerror(errno.EINVAL), path)


def raise_exdev(path: str) -> NoReturn:
    raise OSError(errno.EXDEV, os.strerror(errno.EXDEV), path)
