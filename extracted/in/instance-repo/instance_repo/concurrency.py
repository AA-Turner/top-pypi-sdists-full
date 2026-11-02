"""concurrency.py — 有界线程池并发映射（批量上传/下载用）。

对 IO 密集的 OSS 传输用线程池并发，显著提升批量交付吞吐；``concurrency`` 上限
避免压垮控制面/数据面。结果按输入顺序返回。

失败语义（重要）：
- ``return_exceptions=False``（默认）：任一项失败即抛该项的 ``ItemError``（按输入
  下标最靠前的失败），且会等待已在执行的其余任务结束（线程池 shutdown 语义）。
  已成功项的结果不会返回，但其外部副作用不会回滚；这是fail-fast报告语义，不是事务。
- ``return_exceptions=True``：不抛异常，返回值中失败项以 ``ItemError`` 占位，成功项
  为其结果，便于上层区分成功/失败清单（如交付时对成功子集继续 ingest）。
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, TypeVar, Union

I = TypeVar("I")
O = TypeVar("O")


class ItemError(Exception):
    """并发批处理中单项失败：携带原始 item 与底层异常，供上层做失败清单。"""

    def __init__(self, item, error: BaseException) -> None:
        super().__init__(f"item {item!r} failed: {error}")
        self.item = item
        self.error = error


def map_concurrent(fn: Callable[[I], O], items: Iterable[I], *,
                   concurrency: int = 8,
                   return_exceptions: bool = False
                   ) -> list[Union[O, "ItemError"]]:
    """并发对每个 item 执行 fn，按输入顺序返回结果。见模块 docstring 的失败语义。

    concurrency<=1 时退化为串行（便于调试/测试）。
    """
    items = list(items)
    if not items:
        return []
    if concurrency <= 1:
        return [_collect(fn, it, return_exceptions) for it in items]
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        return map_with_executor(
            fn, items, executor=ex, return_exceptions=return_exceptions)


def map_with_executor(fn: Callable[[I], O], items: Iterable[I], *, executor,
                      return_exceptions: bool = False
                      ) -> list[Union[O, "ItemError"]]:
    """Use a caller-owned executor with the same ItemError and ordering contract."""
    items = list(items)
    futures = [executor.submit(_run, fn, item) for item in items]
    out: list = []
    for future in futures:
        try:
            out.append(future.result())
        except ItemError as exc:
            if not return_exceptions:
                raise
            out.append(exc)
    return out


def _collect(fn, item, return_exceptions):
    try:
        return _run(fn, item)
    except ItemError as e:
        if not return_exceptions:
            raise
        return e


def _run(fn, item):
    try:
        return fn(item)
    except ItemError:
        raise
    except Exception as exc:  # 归一化为 ItemError 供上层定位；不吞 KeyboardInterrupt/SystemExit
        raise ItemError(item, exc) from exc
