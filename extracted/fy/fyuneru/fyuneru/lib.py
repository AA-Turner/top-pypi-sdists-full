# /bin/env python
# -*- coding: utf-8 -*-
"""
@author: inklov3
@date: 2025-07-16
@description: molar function tools
"""

import base64
from bisect import bisect_left
import datetime
import hashlib
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Callable, Generator, Iterable, Sequence, TextIO, Tuple
from urllib.parse import unquote, urlparse

import numpy as np
from tqdm import tqdm
from blake3 import blake3
from loguru import logger
from loguru._logger import Logger as LoguruLogger
from returns.result import safe


@safe
def mkdir(path: Path) -> None:
    """创建目录"""
    path.mkdir(parents=True, exist_ok=True)


@safe
def init_logger(level: str = "WARNING", logs_path: Path = Path("logs")) -> LoguruLogger:
    """
    初始化日志
    """
    print("Logger initializing...")
    if getattr(logger, "_configured", False):
        return logger
    format = "{time:YYYY-MM-DD HH:mm:ss}<level>|{level}|{message}</level>"

    logger.remove()
    logger.add(
        sink=sys.stdout,
        format=format,
        level=level,
    )
    if logs_path:
        logs_path.mkdir(parents=True, exist_ok=True)
        log_path = logs_path / f"{datetime.datetime.now():%Y-%m-%d_%H-%M-%S}.log"
        logger.add(
            str(log_path),
            format=format,
            level=level,
            enqueue=True,
            encoding="utf-8",
        )
    setattr(logger, "_configured", True)
    logger.info("Logger initialized")
    return logger


@safe
def log_message(logger: LoguruLogger, message: str, level: str = "INFO") -> None:
    logger.log(level, message)


@safe
def log_info(message: str) -> None:
    log_message(logger, message, "INFO")


@safe
def log_warning(message: str) -> None:
    log_message(logger, message, "WARNING")


@safe
def log_error(message: str) -> None:
    log_message(logger, message, "ERROR")


@safe
def log_debug(message: str) -> None:
    log_message(logger, message, "DEBUG")


def tqdm_loguru(iterable, level="INFO", **tqdm_kwargs):
    """
    使用 loguru 打印 tqdm 进度的函数式包装器

    Args:
        iterable: 可迭代对象
        level: loguru 日志级别 (默认 INFO)
        **tqdm_kwargs: 传给 tqdm 的其它参数
    """

    class TqdmToLoguru:
        def __init__(self, log_level):
            self.log_level = log_level

        def write(self, buf):
            buf = buf.strip()
            if buf:
                logger.log(self.log_level, buf)

        def flush(self):
            pass

    return tqdm(iterable, file=TqdmToLoguru(level), **tqdm_kwargs)


def read_json(file: Path) -> dict:
    """
    读json
    """
    return json.loads(file.read_text())


class NonSerializable:
    """标记字段为不可序列化：序列化时将跳过此字段"""

    def __repr__(self):
        return "<NonSerializable>"


NON_SERIALIZABLE = NonSerializable()


def serialize(obj) -> any:
    """
    序列化
    """
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    # 处理 pathlib.Path 对象
    if isinstance(obj, Path):
        return str(obj)
    # 先处理namedtuple
    if callable(getattr(obj, "_asdict", None)):
        return serialize(obj._asdict())
    if isinstance(obj, (list, tuple, set)):
        return [serialize(v) for v in obj if not isinstance(v, NonSerializable)]
    if isinstance(obj, dict):
        return {
            k: serialize(v)
            for k, v in obj.items()
            if not isinstance(v, NonSerializable)
        }

    if hasattr(obj, "__dict__"):
        filtered = {
            k: v for k, v in vars(obj).items() if not isinstance(v, NonSerializable)
        }
        return serialize(filtered)
    if isinstance(obj, (np.generic,)):
        return obj.item()
    # NumPy 数组 -> Python 原生嵌套 list
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Unsupported serialization type: {type(obj)}")


def write_json(file: Path, data: any, indent=2):
    """
    写json
    """
    with open(file, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=indent, default=serialize)


def to_json_string(data: any) -> str:
    return json.dumps(serialize(data), ensure_ascii=False)


def hash_string(s: str, method="md5") -> str:
    """
    字符串hash
    """
    h = hashlib.new(method)
    h.update(s.encode("utf-8"))
    return h.hexdigest()


def partial_hash(file: Path, chunk_size=4 * 1024 * 1024) -> str:
    """
    分块hash
    """
    size = file.stat().st_size
    md5 = hashlib.md5()

    ranges = []
    ranges.append((0, chunk_size))  # 开头

    if size > chunk_size * 2:
        middle = max((size // 2) - (chunk_size // 2), chunk_size)
        ranges.append((middle, chunk_size))  # 中间

    if size > chunk_size:
        ranges.append((size - chunk_size, chunk_size))  # 结尾

    with file.open("rb") as f:
        for offset, length in ranges:
            f.seek(offset)
            md5.update(f.read(length))

    return md5.hexdigest()


def get_uuid() -> str:
    """
    获取uuid
    """
    random_uuid = uuid.uuid4()
    return str(random_uuid)


def get_timestamp() -> str:
    """
    获取时间戳
    """
    time = datetime.datetime.now()
    return time.strftime("%Y.%m.%d-%H:%M:%S.%f")


def search_with_suffix(path: Path, suffixes: set[str]) -> Generator[Path, None, None]:
    """递归查找目录后缀文件"""
    for f in path.rglob(r"*"):
        if f.suffix not in suffixes:
            continue
        yield f


def url_to_path(url: str) -> Path:
    """url转换为路径"""
    url_parsed = urlparse(url)
    unquote_path = unquote(url_parsed.path)
    return Path(unquote_path)


def recursive_replace(s: str, replace_map: dict[str, str]) -> str:
    """假递归替换"""
    for k, v in replace_map.items():
        s = s.replace(k, v)
    return s


def recursive_clean(s: str, clean_words: Iterable[str]) -> str:
    """假递归清理"""
    return recursive_replace(s, {word: "" for word in clean_words})


def to_hash(data: bytes, scheme: str = "blake3") -> str:
    match scheme:
        case "blake3":
            return blake3(data).hexdigest()
        case "md5":
            return hashlib.md5(data).hexdigest()
        case _:
            raise NotImplementedError(f"Unsupported hash scheme: {scheme}")


def to_base64(data: bytes) -> str:
    """
    转换为base64
    """
    return base64.b64encode(data).decode("utf-8")


def sort_dict(data: dict, sort_rule: Callable[any, int]) -> dict:
    """
    排序字典
    """
    return dict(sorted(data.items(), key=lambda x: sort_rule(x)))


def find_nearest(sorted_seq: Sequence, target: Any) -> Tuple[Any, int]:
    """
    有序列中最近 target 元素

    :param sorted_seq: 已排序的序列 (必须支持索引操作)
    :param target: 待查询的值
    :return: (最接近的元素, 该元素的索引)
    """
    pos = bisect_left(sorted_seq, target)

    if pos == 0:
        return sorted_seq[0], 0
    if pos == len(sorted_seq):
        return sorted_seq[-1], len(sorted_seq) - 1

    before, after = sorted_seq[pos - 1], sorted_seq[pos]
    nearest = after if after - target < target - before else before
    idx = pos if nearest == after else pos - 1
    return nearest, idx
