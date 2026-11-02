"""clients/workflows.py — 发布工作流查询（→ apiserver /apis/v1/workflows）。

服务端契约（workflow_handler / workflow_service 实测）：
* ``GET /workflows/{id}``：无 query；裸 Workflow 对象（无信封）。status 枚举
  pending/running/awaiting_approval/succeeded/failed/canceled；kind 当前仅
  benchmark-release（5 步：validate/approval/image_distribute/oss_distribute/
  dataset_ingest）；approval 结构仅审批型 kind 有。不存在 404 CodeWorkflowNotFound。
* ``GET /workflows``：kind/status/creator 过滤 + 分页（默认 20，上限 200），
  created_at 倒序。**无 dataset/version 过滤参数**（服务端未提供）。

设计（方案 D3）：标量 + steps + approval 强类型；``spec``/``outputs`` 保持
原始 dict——结构随 kind 演进（服务端加 step 时 SDK 不需要发版），AP CLI 自行
按键取用。``versions.publish()`` 的返回体带 workflow id，随后可用
``workflows.get(id)`` 轮询终态（awaiting_approval 时 approval.ticket_link 是
审批单链接）。
"""
from __future__ import annotations

from urllib.parse import quote

from ..models import PagedResult, Workflow

WORKFLOW_STATUS_VALUES = ("pending", "running", "awaiting_approval",
                          "succeeded", "failed", "canceled")


class WorkflowsClient:
    _BASE = "/apis/v1/workflows"

    def __init__(self, transport) -> None:
        self._t = transport

    def get(self, workflow_id: str) -> Workflow:
        """查单个工作流（publish 进度/审批单/失败原因）。不存在时抛
        TransportError(404)——与 instances.get 的 None 语义不同：这里 404 只能
        是 id 不存在或无权限，调用方需要显式处理，静默 None 会掩盖拼错 id。"""
        if not (workflow_id or "").strip():
            raise ValueError("workflow_id is required")
        data = self._t.get(f"{self._BASE}/{quote(workflow_id.strip(), safe='')}")
        return Workflow.from_dict(data) if isinstance(data, dict) else Workflow()

    def list(self, *, kind: str | None = None, status: str | None = None,
             creator: str | None = None, page: int = 1,
             page_size: int = 20) -> PagedResult:
        """工作流分页列表（单页，created_at 倒序）。kind 当前仅 benchmark-release。

        服务端无 dataset/version 过滤参数（WorkflowListQuery 只有
        Kind/Status/Creator/Page）——SDK 不造不存在的开关；找某 dataset 的
        publish 记录请用 ``versions.publish()`` 返回的 workflow id 直查。
        """
        if (status or "").strip() and status.strip() not in WORKFLOW_STATUS_VALUES:
            raise ValueError(
                f"invalid status {status!r}; must be one of "
                f"{', '.join(WORKFLOW_STATUS_VALUES)}")
        params: list[tuple[str, str]] = []
        if (kind or "").strip():
            params.append(("kind", kind.strip()))
        if (status or "").strip():
            params.append(("status", status.strip()))
        if (creator or "").strip():
            params.append(("creator", creator.strip()))
        params.append(("page", str(int(page))))
        params.append(("page_size", str(int(page_size))))
        query = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
        data, pagination = self._t.request_with_meta("GET", f"{self._BASE}?{query}")
        rows = data if isinstance(data, list) else (
            data.get("workflows", []) if isinstance(data, dict) else [])
        items = [Workflow.from_dict(r) for r in rows if isinstance(r, dict)]
        return PagedResult.from_response(items, pagination, int(page), int(page_size))
