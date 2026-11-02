"""clients/datasets.py — DatasetSeries 操作（→ apiserver）。"""
from __future__ import annotations

from urllib.parse import quote

from .config import Profile, business_metadata_model
from ..errors import SchemaError, TransportError
from ..models import (ClaimWorkspace, DatasetDetail, DatasetSeries,
                      PagedResult, RoleBinding, VISIBILITY_VALUES)


class DatasetsClient:
    # apiserver 实际路由是 /apis/v1/datasets/series（见 apiserver
    # pkg/api/router/router.go 的 datasets.Group("/series")）。
    # 曾误写成 /apis/v1/datasets，该路径在 apiserver 上不存在，所有调用恒 404。
    _BASE = "/apis/v1/datasets/series"

    def __init__(self, transport, *, profile: Profile | None = None, content_store=None,
                 oss_prefix: str = "swe/datasets",
                 metadata_model: str | None = None) -> None:
        self._t = transport
        self._p = profile
        self._content = content_store
        self._oss_prefix = oss_prefix
        # 正常Dataset业务客户端固定split_first；legacy discovery仍可直接调用低层helper。
        self._metadata_model = business_metadata_model(metadata_model)

    def list(self, l1: str | None = None) -> list[DatasetSeries]:
        """列出 dataset（便利语义：自动翻页取全量，见 :meth:`list_paged` 单页对照）。

        ``l1`` 为客户端本地过滤（按 dataset_l1 前缀）：**服务端 /datasets/series
        并无 dataset_l1 query 参数**（它是 detail 响应字段）——历史版本误当过滤
        参数发送、静默无效。现改为拉取后本地过滤，行为终于与参数名一致；模糊
        搜索请用 :meth:`list_paged` 的 ``q``（服务端 dataset_name+display_name
        不区分大小写子串）。
        """
        out: list[DatasetSeries] = []
        page = 1
        while True:
            res = self.list_paged(page=page, page_size=200)
            out.extend(res.items)
            if not res.has_more or not res.items:
                break
            page += 1
        if l1:
            prefix = l1 if l1.endswith("/") else l1 + "/"
            out = [s for s in out if (s.dataset_l1 + "/").startswith(prefix)]
        return out

    def list_paged(self, *, q: str | None = None,
                   teacher_direction: str | None = None,
                   teacher_type: str | None = None,
                   visibility: str | None = None,
                   owned_by_me: bool | None = None,
                   updated_from: str | None = None,
                   updated_to: str | None = None,
                   sort_by: str | None = None, order: str | None = None,
                   benchmark_id: str | None = None,
                   include_deprecated: bool | None = None,
                   environment: str | None = None,
                   metadata_model: str | None = None,
                   page: int = 1, page_size: int = 20) -> PagedResult:
        """dataset 分页列表（单页，``GET /apis/v1/datasets/series``）。

        参数逐项对齐服务端 ListDatasets（非 SDK 发明）：``q`` 模糊搜索
        dataset_name+display_name（不区分大小写子串）；``visibility`` 逗号分隔
        多值（"public,private"）；``owned_by_me`` 按 owner=caller 过滤；
        ``updated_from/to`` RFC3339 闭区间；``sort_by`` updated_at（默认）|
        dataset_name；``order`` desc（默认）|asc；``benchmark_id`` 精确（
        ``"none"`` 查未绑定）；``environment`` online（默认）|pre；
        ``metadata_model`` 为兼容参数，正常业务只接受并显式发送 split_first。

        items 为 :class:`~instance_repo.models.DatasetSeries`（含服务端返回的
        version_count/split_count/latest_version/claimable 统计字段，见模块
        model 的 optional 字段）。
        """
        params: list[tuple[str, str]] = []
        if (q or "").strip():
            params.append(("q", q.strip()))
        if (teacher_direction or "").strip():
            params.append(("teacher_direction", teacher_direction.strip()))
        if (teacher_type or "").strip():
            params.append(("teacher_type", teacher_type.strip()))
        if (visibility or "").strip():
            v = visibility.strip()
            for part in v.split(","):
                if part.strip() and part.strip() not in VISIBILITY_VALUES:
                    raise SchemaError(
                        f"invalid visibility value {part.strip()!r}; allowed: "
                        f"{', '.join(VISIBILITY_VALUES)}")
            params.append(("visibility", v))
        if owned_by_me is not None:
            params.append(("owned_by_me", "true" if owned_by_me else "false"))
        if (updated_from or "").strip():
            params.append(("updated_from", updated_from.strip()))
        if (updated_to or "").strip():
            params.append(("updated_to", updated_to.strip()))
        if (sort_by or "").strip():
            sb = sort_by.strip()
            if sb not in ("updated_at", "dataset_name"):
                raise SchemaError(
                    f"invalid sort_by {sb!r}; must be updated_at or dataset_name")
            params.append(("sort_by", sb))
        if (order or "").strip():
            od = order.strip()
            if od not in ("asc", "desc"):
                raise SchemaError(
                    f"invalid order {od!r}; must be asc or desc")
            params.append(("order", od))
        if (benchmark_id or "").strip():
            params.append(("benchmark_id", benchmark_id.strip()))
        if include_deprecated is not None:
            params.append(("include_deprecated",
                           "true" if include_deprecated else "false"))
        if (environment or "").strip():
            params.append(("environment", environment.strip()))
        mm = business_metadata_model(metadata_model)
        params.append(("metadata_model", mm))
        params.append(("page", str(int(page))))
        params.append(("page_size", str(int(page_size))))
        query = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
        data, pagination = self._t.request_with_meta(
            "GET", f"{self._BASE}?{query}")
        rows = data.get("datasets", data) if isinstance(data, dict) else data
        rows = rows if isinstance(rows, list) else []
        items = [DatasetSeries(**_pick_series(r)) for r in rows if isinstance(r, dict)]
        return PagedResult.from_response(items, pagination, int(page), int(page_size))

    def get(self, name: str, *, environment: str | None = None,
            metadata_model: str | None = None,
            fallback_to_oss: bool = True) -> DatasetSeries:
        mm = business_metadata_model(metadata_model)
        try:
            q = (f"dataset_name={quote(name, safe='')}"
                 f"&metadata_model={quote(mm, safe='')}")
            if (environment or "").strip():
                q += f"&environment={quote(environment.strip(), safe='')}"
            data = self._t.get(f"{self._BASE}/detail?{q}")
            return DatasetSeries(**_pick_series(data))
        except TransportError as e:
            if (e.biz_code == 92001 and fallback_to_oss
                    and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_series(name)
            raise

    def get_detail(self, name: str, *, environment: str | None = None,
                   metadata_model: str | None = None,
                   fallback_to_oss: bool = True) -> DatasetDetail:
        """dataset 富详情（``GET /datasets/series/detail`` 完整响应）。

        相比 :meth:`get` 的轻量 series 字段：新增 version_count / split_count /
        latest_version / stats{instance_count,file_count,size_bytes} /
        available_envs / claimable——控制台 Overview 页的统计块即此数据源。
        RBAC 非 dataset 级 Full 时服务端返回 parent shell（仅标识字段），
        ``parent_shell=True`` 可据此识别。
        """
        if not (name or "").strip():
            raise SchemaError("dataset name is required for get_detail")
        mm = business_metadata_model(metadata_model)
        try:
            q = f"dataset_name={quote(name, safe='')}"
            if (environment or "").strip():
                q += f"&environment={quote(environment.strip(), safe='')}"
            q += f"&metadata_model={quote(mm, safe='')}"
            data = self._t.get(f"{self._BASE}/detail?{q}")
            return DatasetDetail.from_dict(data) if isinstance(data, dict) else DatasetDetail()
        except TransportError as e:
            if (e.biz_code == 92001 and fallback_to_oss
                    and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_detail(name, storage_env=environment,
                                             metadata_model=metadata_model)
            raise

    def update(self, name: str, *, display_name: str | None = None,
               visibility: str | None = None, owner_team_id: str | None = None,
               default_scaffold: str | None = None,
               description: str | None = None,
               benchmark_id: str | None = None,
               status: str | None = None) -> DatasetDetail:
        """更新 dataset 元信息（``PATCH /datasets/series/detail``）。

        服务端 body 白名单 8 字段；全部 None 时前置拒绝（无意义请求）。
        注意治理语义：``visibility`` / ``owner_team_id`` / ``status`` 任一出现
        时 RBAC 升级为 Admin-only（ActionAssign）；``benchmark_id`` 传空串会被
        服务端拒绝（默认禁止解绑），SDK 对空串直接前置报错而非发送。
        ``status`` 仅接受 ""（恢复正常）或 "deprecated"；teacher_* 不在白名单
        （由 benchmark 派生），SDK 不暴露。
        """
        if not (name or "").strip():
            raise SchemaError("dataset name is required for update")
        body: dict = {}
        if display_name is not None:
            body["display_name"] = display_name
        if visibility is not None:
            if visibility not in VISIBILITY_VALUES:
                raise SchemaError(
                    f"invalid visibility {visibility!r}; valid values: "
                    f"{', '.join(VISIBILITY_VALUES)}")
            body["visibility"] = visibility
        if owner_team_id is not None:
            body["owner_team_id"] = owner_team_id
        if default_scaffold is not None:
            body["default_scaffold"] = default_scaffold
        if description is not None:
            body["description"] = description
        if benchmark_id is not None:
            if not benchmark_id.strip():
                raise SchemaError(
                    "benchmark_id cannot be empty (server forbids unbinding; "
                    "pass a real source_id or omit the field)")
            body["benchmark_id"] = benchmark_id
        if status is not None:
            if status not in ("", "deprecated"):
                raise SchemaError(
                    f"invalid status {status!r}; must be '' (restore) or "
                    f"'deprecated'")
            body["status"] = status
        if not body:
            raise SchemaError(
                "datasets.update requires at least one field (display_name / "
                "visibility / owner_team_id / default_scaffold / description / "
                "benchmark_id / status)")
        data = self._t.patch(
            f"{self._BASE}/detail?dataset_name={quote(name, safe='')}", body)
        return DatasetDetail.from_dict(data) if isinstance(data, dict) else DatasetDetail()

    def create(self, series: DatasetSeries, *,
               require_benchmark: bool = True) -> DatasetSeries:
        """创建 DatasetSeries（``POST /apis/v1/datasets/series``）。

        ``benchmark_id`` 默认必填：apiserver 用它绑定 benchmark 并**派生**
        teacher_direction/teacher_type（取 benchmark 的 teacher_directions[0]/[1]），
        所以不要自行传 teacher（传了会被服务端忽略，SDK 也不发送）。
        建议使用标准化 benchmark id；如果没有，可以填入 ``default``（需服务端 benchmark
        registry 里存在 source_id="default" 的条目，否则服务端回 92005 benchmark not found）。

        若服务端关掉了开关 ``dataset.require_benchmark_binding``，传
        ``require_benchmark=False`` 可跳过本地必填校验。

        幂等语义（注意）：dataset_name 已存在时 apiserver 也回 201 并带
        ``claim_status="exists"``，但本方法只解析 series 字段，**无法区分"新建"与
        "已存在"**；且当调用方对已存在的 dataset 没有完整读权限时，服务端返回的是
        92001（404 dataset not found）而非 201。
        visibility 始终显式发送（apiserver 缺省值在版本间变化过，显式传更稳）。
        """
        series.validate()
        if require_benchmark and not series.benchmark_id:
            raise SchemaError(
                "benchmark_id is required to create a dataset (apiserver derives "
                "teacher_direction/teacher_type from it); pass require_benchmark=False "
                "if the server has dataset.require_benchmark_binding disabled")
        data = self._t.post(self._BASE, series.to_create_body())
        return DatasetSeries(**_pick_series(data))

    def grant(self, name: str, user: str, role: str, *,
              principal_type: str = "user") -> None:
        """给指定主体授予 dataset 角色（通过 role-bindings 接口）。

        role: "reader" / "writer" / "admin"
        user: 工号字符串；principal_type="user_group" 时为 user_group id。
        principal_type: "user"（默认）/ "user_group"。

        服务端约束：通用 role-bindings 写 dataset 绑定仅允许 **dataset 级 +
        user/user_group 主体**（version/split 级与 workspace 主体须走 Dataset
        ACL API，不在 SDK 通用 grant 范围）；writer/admin 只能绑 dataset 级。
        向后兼容：原有三参调用 ``grant(name, user, role)`` 行为不变。
        """
        _ROLE_MAP = {
            "reader": "built-in:dataset-reader",
            "writer": "built-in:dataset-writer",
            "admin": "built-in:dataset-admin",
        }
        role_id = _ROLE_MAP.get(role)
        if not role_id:
            raise SchemaError(
                f"invalid role '{role}'; valid values: "
                f"{', '.join(sorted(_ROLE_MAP))}")
        if principal_type not in ("user", "user_group"):
            raise SchemaError(
                f"invalid principal_type {principal_type!r}; must be user or "
                f"user_group")
        series = self.get(name)
        if not series.dataset_id:
            raise SchemaError(
                f"dataset '{name}' has no dataset_id; cannot grant")
        self._t.post("/apis/v1/role-bindings", {
            "scope": "resource",
            "resource_type": "dataset",
            "resource_id": series.dataset_id,
            "principal_type": principal_type,
            "principal_id": str(user),
            "role_id": role_id,
        })

    def revoke(self, name: str, user: str, role: str, *,
               principal_type: str = "user") -> None:
        """撤销主体的 dataset 角色绑定（``DELETE /apis/v1/role-bindings``）。

        服务端按六元组复合键删除；无此绑定时 404（SDK 透传 TransportError，
        biz_code 可供区分）。参数语义与 :meth:`grant` 一致。
        """
        _ROLE_MAP = {
            "reader": "built-in:dataset-reader",
            "writer": "built-in:dataset-writer",
            "admin": "built-in:dataset-admin",
        }
        role_id = _ROLE_MAP.get(role)
        if not role_id:
            raise SchemaError(
                f"invalid role '{role}'; valid values: "
                f"{', '.join(sorted(_ROLE_MAP))}")
        if principal_type not in ("user", "user_group"):
            raise SchemaError(
                f"invalid principal_type {principal_type!r}; must be user or "
                f"user_group")
        series = self.get(name)
        if not series.dataset_id:
            raise SchemaError(
                f"dataset '{name}' has no dataset_id; cannot revoke")
        self._t.delete(
            "/apis/v1/role-bindings?"
            f"scope=resource&resource_type=dataset"
            f"&resource_id={quote(series.dataset_id, safe='')}"
            f"&principal_type={quote(principal_type, safe='')}"
            f"&principal_id={quote(str(user), safe='')}"
            f"&role_id={quote(role_id, safe='')}")

    def list_access(self, name: str, *, page: int = 1,
                    page_size: int = 20) -> PagedResult:
        """列出 dataset 的角色绑定（``GET /role-bindings?scope=resource&...``）。

        服务端要求 caller 对该 dataset 持 assign 权限（Admin），否则 403。
        items 为 :class:`~instance_repo.models.RoleBinding`。
        """
        series = self.get(name)
        if not series.dataset_id:
            raise SchemaError(
                f"dataset '{name}' has no dataset_id; cannot list access")
        q = (f"scope=resource&resource_type=dataset"
             f"&resource_id={quote(series.dataset_id, safe='')}"
             f"&page={int(page)}&page_size={int(page_size)}")
        data, pagination = self._t.request_with_meta(
            "GET", f"/apis/v1/role-bindings?{q}")
        rows = data if isinstance(data, list) else (
            data.get("bindings", []) if isinstance(data, dict) else [])
        items = [RoleBinding.from_dict(r) for r in rows if isinstance(r, dict)]
        return PagedResult.from_response(items, pagination, int(page), int(page_size))

    def list_claim_workspaces(self) -> list[ClaimWorkspace]:
        """claim 候选 workspace（``GET /datasets/claim-workspaces``）。

        无参数；返回调用方可用的 ``[{queue_id, name}]`` 列表（控制台 claim
        弹窗的 Workspace 候选即此数据源）。**注意**：该路由仅在服务端
        dataset RBAC 开启时注册——未开启时 404，SDK 转译为带 hint 的
        Forbidden（避免静默空列表掩盖配置问题），非 200/404 照常抛出。
        """
        try:
            data = self._t.get("/apis/v1/datasets/claim-workspaces")
        except TransportError as e:
            if e.status == 404:
                raise TransportError(
                    "claim-workspaces 不可用：服务端未开启 dataset RBAC "
                    "（AuthzDatasetEnabled=false 时该路由不注册）或当前环境"
                    "不支持；请核对服务端配置", status=e.status,
                    biz_code=e.biz_code) from e
            raise
        rows = data if isinstance(data, list) else (
            data.get("workspaces", []) if isinstance(data, dict) else [])
        return [ClaimWorkspace.from_dict(r) for r in rows if isinstance(r, dict)]

    def claim(self, dataset_id: str, workspace_id: str, benchmark_id: str, *,
              owner: str | None = None, require_benchmark: bool = True) -> dict:
        """认领 dataset：调用方成为 Dataset Admin。

        对齐 apiserver master 的 ``datasetClaimRequest``（仅 owner / workspace_id /
        queue_id / benchmark_id 四字段）：

        * ``workspace_id`` **必填**——缺失服务端回 92013（403）。
        * ``benchmark_id`` **默认必填**——服务端据它绑定 benchmark 并派生 teacher。
          若已绑定到**不同** benchmark 回 92016（409，claim 不允许改绑）；同值幂等。
        * ``owner`` 可选，缺省取调用方工号；已有非空 owner **不会被覆盖**。

        认领请求**没有 teacher 字段**（teacher 一律由 benchmark 派生），因此 SDK 不再
        接受 teacher 参数——传了也只会被服务端 JSON 绑定静默丢弃。

        其他常见终态：92010（409 已有 admin）、92014（429 认领限流）、92001（404 不存在）。
        """
        if not workspace_id:
            raise SchemaError("workspace_id is required to claim a dataset")
        if require_benchmark and not benchmark_id:
            raise SchemaError(
                "benchmark_id is required to claim a dataset (apiserver derives "
                "teacher_direction/teacher_type from it); pass require_benchmark=False "
                "if the server has dataset.require_benchmark_binding disabled")
        body: dict = {"workspace_id": workspace_id}
        if benchmark_id:
            body["benchmark_id"] = benchmark_id
        if owner:
            body["owner"] = owner
        return self._t.post(
            f"{self._BASE}/{quote(dataset_id, safe='')}/claim", body)

    # ── OSS fallback discovery (private) ─────────────────────────────────

    def _discovery_env_match(self, environment: str | None) -> bool:
        """OSS 回退环境兼容性检查：请求的 environment 须与 profile storage_env 派生环境一致。"""
        req = (environment or "").strip()
        if not req:
            return True
        if self._p is None:
            return True
        from .config import dataset_environment_for
        derived = dataset_environment_for(
            getattr(self._p, "storage_env", ""))
        if not derived:
            return True
        return req == derived

    def _discover_detail(self, name: str, *,
                         storage_env: str | None = None,
                         metadata_model: str | None = None) -> DatasetDetail:
        from ..store.oss_discovery import (
            parse_dataset_level, build_synthetic_dataset_detail,
            _warn_if_truncated)
        info = parse_dataset_level(
            self._content, name, oss_prefix=self._oss_prefix,
            metadata_model=metadata_model or self._metadata_model)
        _warn_if_truncated(info, name, 500)
        if not info.versions and not info.unversioned_splits:
            from ..errors import DatasetNotFound
            raise DatasetNotFound(f"dataset {name!r} not found in OSS")
        return build_synthetic_dataset_detail(
            name, info, storage_env=storage_env)

    def _discover_series(self, name: str) -> DatasetSeries:
        detail = self._discover_detail(name)
        return DatasetSeries(
            dataset_name=detail.dataset_name,
            dataset_l1=detail.dataset_l1,
            dataset_l2=detail.dataset_l2,
            dataset_id=detail.dataset_id or None,
            version_count=detail.version_count,
            split_count=detail.split_count,
            latest_version=detail.latest_version,
            available_envs=detail.available_envs,
            registered=False,
        )


# 与 apiserver `DatasetListItem`（pkg/server/dataset_service.go:231）逐字段对齐。
_SERIES_FIELDS = ("dataset_name", "dataset_l1", "dataset_l2", "dataset_id",
                  "teacher_direction", "teacher_type", "benchmark_id", "visibility",
                  "owner_team_id", "display_name", "description", "default_scaffold",

                  "owner", "status", "version_count", "split_count", "latest_version",
                  "claimable", "updated_at", "available_envs")



# TEACHER_ENUMS 是 teacher 级联标签（teacher_direction → 允许的 teacher_type 列表）的
# **参考快照**，供本地填参/校验提示使用。
#
# 权威来源是 apiserver 配置 ``dataset.teacher_enums``（可经
# ``GET /apis/v1/datasets/teacher-enums`` 实时获取）；此处静态副本仅为方便，可能滞后。
# 每个 direction 的 type 列表末尾均含小写 "others" 兜底。
#
# **注意（对齐 apiserver master）**：该 taxonomy 已**不再承担写入校验职责**。create /
# update / claim 都不接受 teacher 入参，teacher_direction/teacher_type 由服务端从
# benchmark 的 teacher_directions（[0]=direction、[1]=type）派生。故本表仅供展示/选型
# 参考，不要用它拼 create/claim 的请求体。
TEACHER_ENUMS: dict[str, list[str]] = {
    "General": ["General", "LongContext", "MultiLingual", "Vertical", "Safety", "others"],
    "Coding": ["SWECoding", "CliCoding", "LongHorizonCoding", "WebDevCoding", "UXCoding", "RLAlgorithm", "others"],
    "Cyber": ["CyberSecurity", "others"],
    "Working": ["Cowork", "GDPVal", "others"],
    "Reasoning": ["Reasoning", "others"],
    "Agent": ["GeneralAgent", "SearchAgent", "LongHorizonAgent", "AutoResearch", "others"],
    "VL": ["PerceptionOrReasoning", "RLHF", "Video", "VisualAgent", "VisualCoding", "GUI", "CoWork", "Coding", "others"],
    "Omni": ["Harness-agent", "VideoSearchAndC", "VideoAudioMcpOrCI", "VideoAudioCaption", "VideoReasoning", "AudioReasoning", "Instruct", "Proactive learning", "others"],
    "GroupBusinessConsolidation": ["GroupBusinessConsolidation", "others"],
    "TeacherModelConsolidation": ["TeacherModelConsolidation", "others"],
    "Evaluation": ["Evaluation", "others"],
}


def _pick_series(d: dict) -> dict:
    out = {k: d[k] for k in _SERIES_FIELDS if k in d}
    out.setdefault("dataset_name", d.get("dataset_name", ""))
    out.setdefault("dataset_l1", d.get("dataset_l1", ""))
    out.setdefault("dataset_l2", d.get("dataset_l2", ""))
    return out
