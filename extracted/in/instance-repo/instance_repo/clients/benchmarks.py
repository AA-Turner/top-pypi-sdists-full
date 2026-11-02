"""clients/benchmarks.py — benchmark 目录查询（→ apiserver /apis/v1/benchmarks）。

服务端契约（meta_handler / meta_service 实测）：
* ``GET /benchmarks``：分页信封（默认 page=1/page_size=20，上限 200）；
  ``q`` 对 name 模糊匹配（不区分大小写子串）；``is_core`` 布尔（非法值服务端
  静默忽略，SDK 不做额外校验）；``source`` 精确。按 updated_at 倒序。
* ``GET /benchmarks/{source_id}``：点查；不存在 404。认证可选（combinedAuthOptional）。

主键是 ``source_id``（无独立 id 字段）。claim 弹窗的 Benchmark 候选即
``list(q=...)``；控制台"Benchmark maintainer is not allowed"的禁用态是**前端
逻辑**（apiserver 无 enabled/allowed 字段），SDK 不模拟——调用方按自身权限过滤。
"""
from __future__ import annotations

from urllib.parse import quote

from ..errors import TransportError
from ..models import Benchmark, PagedResult


class BenchmarksClient:
    _BASE = "/apis/v1/benchmarks"

    def __init__(self, transport) -> None:
        self._t = transport

    def list(self, *, q: str | None = None, is_core: bool | None = None,
             source: str | None = None, page: int = 1,
             page_size: int = 20) -> PagedResult:
        """benchmark 分页列表（单页）。``q`` 模糊搜索 name（不区分大小写子串）。"""
        params: list[tuple[str, str]] = []
        if (q or "").strip():
            params.append(("q", q.strip()))
        if is_core is not None:
            params.append(("is_core", "true" if is_core else "false"))
        if (source or "").strip():
            params.append(("source", source.strip()))
        params.append(("page", str(int(page))))
        params.append(("page_size", str(int(page_size))))
        query = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
        data, pagination = self._t.request_with_meta("GET", f"{self._BASE}?{query}")
        rows = data if isinstance(data, list) else (
            data.get("benchmarks", []) if isinstance(data, dict) else [])
        items = [Benchmark.from_dict(r) for r in rows if isinstance(r, dict)]
        return PagedResult.from_response(items, pagination, int(page), int(page_size))

    def get(self, source_id: str) -> Benchmark | None:
        """按 source_id 点查；不存在返回 None（"没有"不是错误）。"""
        if not (source_id or "").strip():
            raise ValueError("source_id is required")
        try:
            data = self._t.get(f"{self._BASE}/{quote(source_id.strip(), safe='')}")
        except TransportError as e:
            if e.status == 404:
                return None
            raise
        return Benchmark.from_dict(data) if isinstance(data, dict) else None
