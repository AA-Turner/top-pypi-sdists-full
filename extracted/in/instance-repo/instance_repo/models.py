"""models.py — 三实体 + 子结构（stdlib dataclasses，无第三方依赖）。

字段与 ``schema/dataset_metadata.schema.json`` 对齐（含 v0.3.0 新增 4 字段）。
提供 Canonical JSON 序列化（key 字典序、无多余空白、ensure_ascii=False、无结尾
换行），保证 content_digest 跨语言可复现、conformance 逐字节比对。
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Any

from .errors import SchemaError

VISIBILITY_VALUES = ("public", "private")
VERSION_STATUS_VALUES = ("draft", "published", "deprecated", "archived")
# run_type 是 version/split 级用途标签（apiserver model.DatasetRunType）；
# 仅 train/eval 两值，写入端点 PATCH /apis/v1/datasets/versions/detail。
RUN_TYPE_VALUES = ("train", "eval")
# storage_type 目前 apiserver 仅支持 oss（DatasetStorageTypeOSS）；缺省即 oss。
STORAGE_TYPE_VALUES = ("oss",)
# permission 是签发 OSS 凭据时的**权限封顶**（apiserver credential_handler 的 permission
# 字段）：只能把本次令牌收窄到不高于调用方真实角色，绝不提权。ACR 分支不支持该字段。
# 发现模式（list-only）走独立字段 list_only，不与封顶枚举混用。
PERMISSION_VALUES = ("admin", "writer", "reader")


def canonical_json(obj: Any) -> str:
    """Canonical JSON：key 排序、紧凑分隔符、非 ASCII 直出、无结尾换行。"""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate_tag_key(key: str) -> str:
    if not isinstance(key, str):
        raise SchemaError("tag keys must be strings")
    key = key.strip()
    if not key:
        raise SchemaError("tag key must not be empty or whitespace-only")
    if "." in key or "$" in key:
        raise SchemaError("tag keys must not contain '.' or '$'")
    return key


def _normalize_tag_array(values: Any) -> list[str]:
    if not isinstance(values, list):
        raise SchemaError("tag values must be a string array")
    if len(values) > 64:
        raise SchemaError("tag values must contain at most 64 raw values")
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise SchemaError("tag values must be non-empty strings")
        value = value.strip()
        if "," in value:
            raise SchemaError(f"tag value {value!r} must not contain ','")
        if value not in normalized:
            normalized.append(value)
    return normalized


def normalize_tag_values(tags: Any, *, keep_empty: bool = False) -> dict[str, list[str]]:
    """Normalize multi-value tags; commas are forbidden in individual values.

    Empty arrays are deletion markers. Partial mutations keep them until merging;
    whole-map writes omit their keys. Limits apply before trimming/deduplication.
    """
    if not isinstance(tags, dict):
        raise SchemaError("tag_values must be an object")
    if len(tags) > 64:
        raise SchemaError("tag_values must contain at most 64 keys")
    normalized: dict[str, list[str]] = {}
    seen: set[str] = set()
    for raw_key, value in tags.items():
        key = _validate_tag_key(raw_key)
        if key in seen:
            raise SchemaError(f"duplicate tag key {key!r} after normalization")
        seen.add(key)
        values = _normalize_tag_array([value] if isinstance(value, str) else value)
        if values or keep_empty:
            normalized[key] = values
    return normalized


@dataclass
class OwnerReference:
    """上游数据来源；SDK 可选（若提供则 instance.owner_reference = 本结构的 json）。"""
    type: str = "UTS"
    id: str = ""
    message: str = ""

    def to_dict(self) -> dict:
        return {"type": self.type, "id": self.id, "message": self.message}

    def to_json(self) -> str:
        return canonical_json(self.to_dict())

    @classmethod
    def from_json(cls, s: str) -> "OwnerReference":
        d = json.loads(s)
        return cls(type=d.get("type", ""), id=d.get("id", ""),
                   message=d.get("message", ""))

    def validate(self) -> None:
        if not self.type:
            raise SchemaError("OwnerReference.type is required")
        if not self.id:
            raise SchemaError("OwnerReference.id is required")


@dataclass
class Feedback:
    """下游反馈项（instance.feedbacks = json of List[Feedback]，append 语义）。"""
    type: str
    id: str
    score: float
    message: str = ""

    def to_dict(self) -> dict:
        return {"type": self.type, "id": self.id, "score": self.score,
                "message": self.message}

    def validate(self) -> None:
        if not self.type or not self.id:
            raise SchemaError("Feedback.type and Feedback.id are required")
        if not (0.0 <= float(self.score) <= 1.0):
            raise SchemaError("Feedback.score must be in [0.0, 1.0]")


@dataclass
class ManifestEntry:
    file_path: str
    content_type: str = "file"
    content_format: str = "json"
    content_digest: str | None = None
    #: 服务端返回的对象相对路径（`GET /datasets/instances` 的 manifest 项带
    #: `object_path`）；本地扫描出的条目为 None，不进 to_dict，保证推送载荷不变。
    object_path: str | None = None

    def to_dict(self) -> dict:
        d = {"file_path": self.file_path, "content_type": self.content_type,
             "content_format": self.content_format}
        if self.content_digest is not None:
            d["content_digest"] = self.content_digest
        if self.object_path is not None:
            d["object_path"] = self.object_path
        return d


@dataclass
class DatasetSeries:
    dataset_name: str
    dataset_l1: str
    dataset_l2: str
    dataset_id: str | None = None
    # teacher_direction / teacher_type 是**服务端派生的只读字段**：apiserver 从
    # benchmark_id 对应 benchmark 的 teacher_directions（[0]=direction、[1]=type）派生，
    # create/update/claim 三处统一。请求体里传它们会被 apiserver 直接忽略，故 SDK
    # 在 create 时**不发送**（见 to_create_body），仅用于承载响应回显。
    teacher_direction: str | None = None
    teacher_type: str | None = None
    benchmark_id: str | None = None  # 绑定的 benchmark source_id；apiserver 默认强制绑定
    visibility: str = "private"
    owner_team_id: str | None = None
    workspace_id: str | None = None  # 可选（Create 时指定归属 workspace）
    queue_id: str | None = None      # 可选（workspace_id 别名）
    display_name: str | None = None
    description: str | None = None
    default_scaffold: str | None = None
    owner: str | None = None         # 缺省由 apiserver 取调用方工号
    # ── 列表统计字段（GET /datasets/series 每项返回；detail 走 DatasetDetail）──
    version_count: int | None = None
    split_count: int | None = None
    latest_version: str | None = None
    claimable: bool | None = None
    updated_at: str | None = None
    available_envs: list[str] = field(default_factory=list)
    # 服务端 `DatasetSeriesStatus`（"" 正常 / "deprecated"）；列表项
    # `DatasetListItem.Status` 带 `omitempty`，正常态不出现。
    status: str = ""
    registered: bool = True

    def validate(self) -> None:
        if self.visibility not in VISIBILITY_VALUES:
            raise SchemaError(f"invalid visibility '{self.visibility}'; valid values: {', '.join(VISIBILITY_VALUES)}")
        if not self.dataset_name:
            raise SchemaError("dataset_name is required")

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k != "registered"}

    def to_create_body(self) -> dict:
        """create 请求体：剔除服务端派生/服务端分配的字段。

        teacher_direction / teacher_type 由 apiserver 从 benchmark 派生（传了也被忽略），
        dataset_id 由服务端分配；dataset_l1 / dataset_l2 由 dataset_name 推导。status
        是服务端 DatasetSeriesStatus（deprecated 打标），create 不接受。都不发送，
        避免让调用方误以为这些值能由客户端决定。
        """
        drop = {"teacher_direction", "teacher_type", "dataset_id",
                "dataset_l1", "dataset_l2", "status", "registered"}
        return {k: v for k, v in self.to_dict().items() if k not in drop}


@dataclass
class DatasetVersion:
    version: str
    dataset: str
    status: str = "draft"
    dataset_version_id: str | None = None
    storage_path: str | None = None
    published_at: str | None = None
    # ── 完整详情字段（versions.get 装载；旧构造不传不受影响）──
    storage_type: str = "oss"
    # splits 列表项 dict 键集：{name, run_type?, oss_prefix, is_default,
    # instance_count?, file_count?, size_bytes?}——无 per-split status/
    # published_at/storage_path（那些要走 repo.splits 读真实 split 记录）。
    splits: list[dict] = field(default_factory=list)
    # manifest 键集：{instance_count?, file_count?, size_bytes?,
    # validation_status?, validation_message?}
    manifest: dict = field(default_factory=dict)
    run_type: str | None = None
    created_by: str | None = None
    last_ingested_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    parent_shell: bool = False

    # ── 列表项统计字段（GET /datasets/versions 每项返回 instance_count/split_count）──

    instance_count: int | None = None
    split_count: int | None = None
    registered: bool = True

    def validate(self) -> None:
        if self.status not in VERSION_STATUS_VALUES:
            raise SchemaError(f"invalid status '{self.status}'; valid values: {', '.join(VERSION_STATUS_VALUES)}")

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None and k != "registered"}

    @classmethod
    def from_dict_full(cls, d: dict) -> "DatasetVersion":
        """从 versions/detail 完整响应装载（含 splits/manifest/时间戳）。"""
        return cls(
            version=d.get("version", ""),
            dataset=d.get("dataset", ""),
            status=d.get("status", "draft"),
            dataset_version_id=d.get("dataset_version_id"),
            storage_path=d.get("storage_path"),
            published_at=d.get("published_at"),
            storage_type=d.get("storage_type", "oss"),
            splits=list(d.get("splits") or []),
            manifest=dict(d.get("manifest") or {}),
            run_type=d.get("run_type"),
            created_by=d.get("created_by"),
            last_ingested_at=d.get("last_ingested_at"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            parent_shell=bool(d.get("parent_shell", False)),
            registered=d.get("registered", True))


@dataclass
class DatasetInstance:
    instance_id: str
    dataset: str
    dataset_version: str
    owner_reference: str = ""                  # SDK 非必填(若给则须为 OwnerReference JSON)
    split: str = "default"
    id: str | None = None
    manifest: list[ManifestEntry] = field(default_factory=list)
    tags: dict[str, str] = field(default_factory=dict)
    difficulty: str | None = None
    docker_image: str | None = None
    extend_meta: dict[str, str] = field(default_factory=dict)
    instance_status: str | None = None
    instance_version: str | None = None
    feedbacks: str | None = None
    schema_version: str = "1.0"
    #: 服务端返回的时间戳；本地扫描构造的实例为 None，不进 to_dict（推送载荷不变）。
    created_at: str | None = None
    updated_at: str | None = None
    registered: bool = True

    def __init__(
        self,
        instance_id: str,
        dataset: str,
        dataset_version: str,
        owner_reference: str = "",
        split: str = "default",
        id: str | None = None,
        manifest: list[ManifestEntry] | None = None,
        tags: dict[str, str] | None = None,
        difficulty: str | None = None,
        docker_image: str | None = None,
        extend_meta: dict[str, str] | None = None,
        instance_status: str | None = None,
        instance_version: str | None = None,
        feedbacks: str | None = None,
        schema_version: str = "1.0",
        created_at: str | None = None,
        updated_at: str | None = None,
        registered: bool = True,
        tag_values: dict[str, list[str]] | None = None,
    ):
        self.instance_id = instance_id
        self.dataset = dataset
        self.dataset_version = dataset_version
        self.owner_reference = owner_reference
        self.split = split
        self.id = id
        self.manifest = list(manifest) if manifest is not None else []
        self.tags = dict(tags) if tags is not None else {}
        self.difficulty = difficulty
        self.docker_image = docker_image
        self.extend_meta = dict(extend_meta) if extend_meta is not None else {}
        self.instance_status = instance_status
        self.instance_version = instance_version
        self.feedbacks = feedbacks
        self.schema_version = schema_version
        self.created_at = created_at
        self.updated_at = updated_at
        self.registered = registered
        if tag_values is not None:
            norm = normalize_tag_values(tag_values)
            self.tags.update({k: ",".join(v) for k, v in norm.items() if v})

    @property
    def tag_values(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for k, v in self.tags.items():
            if isinstance(v, str):
                parts = [p.strip() for p in v.split(",") if p.strip()]
                seen: set[str] = set()
                unique_parts: list[str] = []
                for p in parts:
                    if p not in seen:
                        seen.add(p)
                        unique_parts.append(p)
                out[k] = unique_parts
            elif isinstance(v, list):
                out[k] = [str(p).strip() for p in v if str(p).strip()]
        return out

    @tag_values.setter
    def tag_values(self, val: dict[str, list[str]] | None) -> None:
        if val is None:
            self.tags = {}
            return
        norm = normalize_tag_values(val)
        self.tags = {k: ",".join(v) for k, v in norm.items() if v}

    def validate(self) -> None:
        if not self.instance_id:
            raise SchemaError("instance_id is required")
        # owner_reference 非必填；若提供则须为合法 OwnerReference JSON
        if self.owner_reference:
            OwnerReference.from_json(self.owner_reference).validate()

    def to_dict(self) -> dict:
        d: dict[str, Any] = {
            "instance_id": self.instance_id,
            "dataset": self.dataset,
            "dataset_version": self.dataset_version,
            "split": self.split,
            "owner_reference": self.owner_reference,
            "manifest": [m.to_dict() for m in self.manifest],
            "tags": self.tags,
            "extend_meta": self.extend_meta,
            "schema_version": self.schema_version,
        }
        for k in ("id", "difficulty", "docker_image", "instance_status",
                  "instance_version", "feedbacks", "created_at", "updated_at"):
            v = getattr(self, k)
            if v is not None:
                d[k] = v
        return d

    def to_canonical_json(self) -> str:
        return canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetInstance":
        """从 apiserver/OSS 读回；容忍旧字段名（version→dataset_version，
        extra→extend_meta），owner_reference 缺省补空字符串。"""
        manifest = [
            ManifestEntry(
                file_path=m.get("file_path", ""),
                content_type=m.get("content_type", "file"),
                content_format=m.get("content_format", "json"),
                content_digest=m.get("content_digest"),
                object_path=m.get("object_path"),
            )
            for m in (d.get("manifest") or [])
        ]
        tags = d.get("tags") or {}
        if isinstance(tags, list):  # 旧口径 []string → 忽略成空 map（兼容读取）
            tags = {}
        elif not isinstance(tags, dict):
            tags = {}
        if not tags and d.get("tag_values"):
            norm = normalize_tag_values(d["tag_values"])
            tags = {k: ",".join(v) for k, v in norm.items() if v}
        return cls(
            instance_id=d.get("instance_id", ""),
            dataset=d.get("dataset", ""),
            dataset_version=d.get("dataset_version") or d.get("version", ""),
            owner_reference=d.get("owner_reference", ""),
            split=d.get("split", "default"),
            id=d.get("id"),
            manifest=manifest,
            tags=tags,
            difficulty=d.get("difficulty"),
            docker_image=d.get("docker_image"),
            extend_meta=d.get("extend_meta") or d.get("extra") or {},
            instance_status=d.get("instance_status"),
            instance_version=d.get("instance_version"),
            feedbacks=d.get("feedbacks"),
            schema_version=d.get("schema_version", "1.0"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            registered=d.get("registered", True),
        )


@dataclass
class Identity:
    user: str
    orgs: list[str] = field(default_factory=list)
    roles: dict[str, str] = field(default_factory=dict)


@dataclass
class IngestReport:
    """一次 dataset-ingest job 对所选 instance IDs 的可诊断结果。"""

    job: dict | None = None
    job_status: str = ""
    selected_ids: list[str] = field(default_factory=list)
    completed: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    not_submitted: list[str] = field(default_factory=list)
    commit_unknown: bool = False

    @classmethod
    def from_job(cls, job: dict | None, selected_ids) -> "IngestReport":
        ids = list(selected_ids or [])
        status = ((job or {}).get("status") or "").strip().lower()
        if status == "completed":
            return cls(job=job, job_status=status, selected_ids=ids,
                       completed=ids)
        if status == "failed":
            return cls(job=job, job_status=status, selected_ids=ids,
                       failed=ids, unknown=ids, commit_unknown=bool(ids))
        if status in ("created", "scanning", "indexing"):
            return cls(job=job, job_status=status, selected_ids=ids,
                       pending=ids)
        if status in ("canceled", "cancelled"):
            return cls(job=job, job_status=status, selected_ids=ids,
                       unknown=ids, commit_unknown=bool(ids))
        return cls(job=job, job_status=status, selected_ids=ids,
                   unknown=ids, commit_unknown=bool(ids))


@dataclass
class RegistrationReport:
    """一个批次的分块增量 ingest 汇总。"""

    selected_ids: list[str] = field(default_factory=list)
    ingests: list[IngestReport] = field(default_factory=list)
    job_status: str = ""
    completed: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    not_submitted: list[str] = field(default_factory=list)
    commit_unknown: bool = False


@dataclass
class PushResult:
    instance_id: str
    uploaded: bool = False
    skipped: bool = False
    image_pushed: bool = False
    docker_image: str | None = None
    digests: dict[str, str] = field(default_factory=dict)
    # register=True 时经 ingest 写库：所属 chunk 的原始 ingest job；
    # register=False（只传 OSS）时为 None。
    ingest: dict | None = None


@dataclass
class PushManyReport:
    """保留逐项结果，并附带批次注册汇总。"""

    results: list = field(default_factory=list)
    registration: RegistrationReport = field(default_factory=RegistrationReport)


@dataclass
class InstanceDeleteResult:
    """``instances.delete()`` 的结果（服务端受限 STS 删除流程）。

    ``content_deleted``：OSS 文件是否被本次流程删除（``delete_files=True``
    且服务端完成校验后为 True）。
    ``metadata_deleted``：元数据记录是否已删除（幂等重放 completed 时仍为
    True；纯元数据删除恒 True——历史行为里删除失败会抛错，不静默）。
    ``operation_id``：服务端删除操作 ID（``delete_files=True`` 时非空；可
    用作失败重试的 ``delete_operation_id`` 与排障凭据）。
    ``state``：服务端操作终态（"completed"；纯元数据删除为 None）。
    ``stats_state``：服务端统计修复状态（"pending" 表示后台异步修复大小
    统计；None 表示无该信息）。
    """

    instance_id: str
    content_deleted: bool = False
    metadata_deleted: bool = True
    operation_id: str | None = None
    state: str | None = None
    stats_state: str | None = None


# ── RolloutReport（质检 report，服务下游 verl 训练；键名对齐 verl 无下划线口径） ──
@dataclass
class RolloutJob:
    """一次模型 rollout 的 group/job/模型/尝试次数/均分（report.rolloutjob[] 元素）。"""
    groupid: str
    jobid: str
    modelname: str
    attempt: int
    avgscore: float

    def to_dict(self) -> dict:
        return {"groupid": self.groupid, "jobid": self.jobid,
                "modelname": self.modelname, "attempt": self.attempt,
                "avgscore": self.avgscore}

    def validate(self) -> None:
        if int(self.attempt) < 1:
            raise SchemaError("RolloutJob.attempt must be >= 1")
        if not (0.0 <= float(self.avgscore) <= 1.0):
            raise SchemaError("RolloutJob.avgscore must be in [0.0, 1.0]")

    @classmethod
    def from_dict(cls, d: dict) -> "RolloutJob":
        return cls(groupid=d.get("groupid", ""), jobid=d.get("jobid", ""),
                   modelname=d.get("modelname", ""), attempt=int(d.get("attempt", 1)),
                   avgscore=float(d.get("avgscore", 0.0)))


def _str_list(v: object) -> list[str]:
    """读 JSON 字符串数组的统一入口：**只收字符串元素**，其余一律丢弃。

    对应 Go 侧的 ``mapStrSliceStrict``。两条规则都是跨语言一致性要求：

    * 非 list（含 ``None``、字符串）→ ``[]``。若写成 ``list(v)``，传字符串时会被拆成
      单字符列表，是静默数据损坏。
    * list 内非字符串元素**丢弃**，不做 ``str()`` 归一——归一无法跨语言对齐：Python
      ``str()`` 对 ``None`` / dict / list / 超 int64 整数分别给 ``"None"`` /
      ``"{'a': 1}"`` / ``"['x']"`` / ``"99999999999999999999"``，Go ``fmt.Sprint``
      给 ``"<nil>"`` / ``"map[a:1]"`` / ``"[x]"``，大整数还会退成 ``"1e+20"``。
      丢弃是唯一两侧可保证逐字节同形的处理，也与 schema 里 ``items = string`` 一致。
    """
    if not isinstance(v, list):
        return []
    return [x for x in v if isinstance(x, str)]


@dataclass
class ScaffoldConfig:
    """训练 scaffold 配置（透传给 verl；空/None 字段序列化时省略以保持紧凑）。"""
    version: str = ""
    max_iterations: int | None = None
    resources: dict = field(default_factory=dict)
    cpu_limit: str = ""
    memory_limit: str = ""
    scaffold_envs: dict = field(default_factory=dict)
    allowed_tools: list[str] = field(default_factory=list)
    disallowed_tools: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d: dict = {}
        if self.version:
            d["version"] = self.version
        if self.max_iterations is not None:
            d["max_iterations"] = self.max_iterations
        if self.resources:
            d["resources"] = self.resources
        if self.cpu_limit:
            d["cpu_limit"] = self.cpu_limit
        if self.memory_limit:
            d["memory_limit"] = self.memory_limit
        if self.scaffold_envs:
            d["scaffold_envs"] = self.scaffold_envs
        if self.allowed_tools:
            d["allowed_tools"] = list(self.allowed_tools)
        if self.disallowed_tools:
            d["disallowed_tools"] = list(self.disallowed_tools)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "ScaffoldConfig":
        return cls(
            version=d.get("version", ""),
            max_iterations=d.get("max_iterations"),
            resources=dict(d.get("resources") or {}),
            cpu_limit=d.get("cpu_limit", ""),
            memory_limit=d.get("memory_limit", ""),
            scaffold_envs=dict(d.get("scaffold_envs") or {}),
            # 与 rubrics 同一口径：只收字符串元素（见 _str_list）。原先的 list(... or [])
            # 会把非字符串元素原样留下，而 Go 侧对同一输入做 fmt.Sprint 归一，
            # 同一份 report.jsonl 会在两侧序列化出不同字节。
            allowed_tools=_str_list(d.get("allowed_tools")),
            disallowed_tools=_str_list(d.get("disallowed_tools")),
        )


@dataclass
class RolloutReport:
    """质检 rollout report（每实例一条，存 {version}-report/{id}/report.jsonl，一行）。
    键名采用 verl 无下划线口径，供 verl 训练配置零转换直接读取。

    ``instruction`` / ``rubrics`` 是质检对齐方案要求随 report 一起落地的两个字段：
    前者是该实例交给模型的原始任务书（含大量换行），后者是扁平的评分点清单
    （profsynth 口径的 ``[+N]`` 加分 / ``[+-N]` 扣分字符串）。**SDK 只做承载与搬运，
    不解析权重前缀**——判分是上游质检链路的职责。两者均可选：存量 report 没有它们，
    设为必填会让旧数据解析/校验直接失败；为空时序列化省略，与 scaffold_config 一致。
    """
    instanceid: str
    datasetname: str
    split: str
    scaffold: str = "claude-code"
    scaffold_config: ScaffoldConfig | None = None
    rolloutjob: list[RolloutJob] = field(default_factory=list)
    instruction: str = ""
    rubrics: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # 显式传 None 归一成空值：Go 侧 "" / nil 本就是合法的"未设置"，若 Python 让 None
        # 一路走到 validate 才报错，同一份语义在两侧一个通过一个失败。
        if self.instruction is None:
            self.instruction = ""
        if self.rubrics is None:
            self.rubrics = []

    def to_dict(self) -> dict:
        d: dict = {"instanceid": self.instanceid, "datasetname": self.datasetname,
                   "split": self.split, "scaffold": self.scaffold}
        if self.instruction:
            d["instruction"] = self.instruction
        if self.rubrics:
            d["rubrics"] = list(self.rubrics)
        if self.scaffold_config is not None:
            d["scaffold_config"] = self.scaffold_config.to_dict()
        d["rolloutjob"] = [j.to_dict() for j in self.rolloutjob]
        return d

    def to_jsonl_line(self) -> str:
        """单行 canonical JSON（report.jsonl 一行 = 一个实例）。"""
        return canonical_json(self.to_dict())

    def validate(self) -> None:
        if not self.instanceid or not self.datasetname or not self.split:
            raise SchemaError("RolloutReport.instanceid/datasetname/split are required")
        if not isinstance(self.instruction, str):
            raise SchemaError("RolloutReport.instruction must be a string")
        # rubrics 必须是**字符串列表**：直接构造时在此处拒脏数据。非字符串标量能被
        # json 序列化（`[3]` 会原样落到 report.jsonl，而 Go 的 []string 根本表达不出
        # 这种形状），所以不能指望序列化阶段报错兜底。
        if not isinstance(self.rubrics, list):
            raise SchemaError("RolloutReport.rubrics must be a list of strings")
        for i, item in enumerate(self.rubrics):
            if not isinstance(item, str):
                raise SchemaError(
                    f"RolloutReport.rubrics[{i}] must be a string, got "
                    f"{type(item).__name__}")
        for j in self.rolloutjob:
            j.validate()

    @classmethod
    def from_dict(cls, d: dict) -> "RolloutReport":
        sc = d.get("scaffold_config")
        # 非字符串 instruction 回落 ""（否则 int 会漏进 canonical JSON 变成裸数字，
        # 而 Go 的 mapStr 给的是 ""）；rubrics 走 _str_list（只收字符串元素，理由见其
        # docstring），与 Go 的 mapStrSliceStrict 一一对应。
        instr = d.get("instruction")
        return cls(
            instanceid=d.get("instanceid", ""),
            datasetname=d.get("datasetname", ""),
            split=d.get("split", ""),
            scaffold=d.get("scaffold", "claude-code"),
            scaffold_config=ScaffoldConfig.from_dict(sc) if sc else None,
            rolloutjob=[RolloutJob.from_dict(x) for x in (d.get("rolloutjob") or [])],
            instruction=instr if isinstance(instr, str) else "",
            rubrics=_str_list(d.get("rubrics")),
        )

    @classmethod
    def from_jsonl_line(cls, line: str) -> "RolloutReport":
        return cls.from_dict(json.loads(line))


def parse_feedbacks(feedbacks_json: str | None) -> list[Feedback]:
    """把 instance.feedbacks(JSON str) 解析成 List[Feedback]；None/空 → []。"""
    if not feedbacks_json:
        return []
    out = []
    for f in json.loads(feedbacks_json):
        out.append(Feedback(type=f.get("type", ""), id=f.get("id", ""),
                            score=f.get("score", 0.0), message=f.get("message", "")))
    return out


def append_feedback(feedbacks_json: str | None, fb: Feedback) -> str:
    """append 语义：在既有 feedbacks 上追加一条，返回新的 Canonical JSON 串。"""
    fb.validate()
    items = [f.to_dict() for f in parse_feedbacks(feedbacks_json)]
    items.append(fb.to_dict())
    return canonical_json(items)


# ─────────────────────────────────────────────────────────────────────────────
# 控制面管理模型（1.0.10）：split / dataset 详情统计 / benchmark / workflow /
# role-binding / 分页结果。字段与 apiserver master 响应对齐（handler 逐端点核实）。
# ─────────────────────────────────────────────────────────────────────────────

# split 记录状态机与 version 一致（recordsvc 校验同一套枚举）。
SPLIT_STATUS_VALUES = ("draft", "published", "deprecated", "archived")


@dataclass
class PagedResult:
    """分页列表结果（单页语义，``*_list_paged`` 系列返回）。

    ``items`` 是**当前页**数据；``total`` 是服务端 pagination.total（全量计数）；
    ``has_more`` 按 page*page_size < total 推导（服务端不直接返回该字段）。
    服务端无 pagination 信封时 total=-1、has_more=False（旧服务端单页即全部）。
    """
    items: list
    total: int = -1
    page: int = 1
    page_size: int = 0
    has_more: bool = False
    #: 服务端返回的**原始**分页信封（键名原样,如 ``pageSize``）；无信封时为 None。
    #: 给需要逐字透出服务端响应的调用方（CLI 的 ``pagination`` 字段就是原样透出,
    #: 用归一化后的 ``page_size`` 会改变既有 JSON 契约）。
    raw: dict | None = None

    @classmethod
    def from_response(cls, items: list, pagination: dict | None,
                      page: int, page_size: int) -> "PagedResult":
        if isinstance(pagination, dict):
            total = pagination.get("total")
            total = total if isinstance(total, (int, float)) else -1
            return cls(items=items, total=int(total), page=page,
                       page_size=page_size,
                       has_more=page * page_size < total,
                       raw=dict(pagination))
        return cls(items=items, total=-1, page=page, page_size=page_size,
                   has_more=False)


@dataclass
class SplitManifest:
    """split 记录内嵌 manifest（与 version manifest 同构，均可为空）。"""
    instance_count: int | None = None
    file_count: int | None = None
    size_bytes: int | None = None
    validation_status: str | None = None
    validation_message: str | None = None

    @classmethod
    def from_dict(cls, d: dict | None) -> "SplitManifest | None":
        if not isinstance(d, dict):
            return None
        return cls(
            instance_count=d.get("instance_count"),
            file_count=d.get("file_count"),
            size_bytes=d.get("size_bytes"),
            validation_status=d.get("validation_status"),
            validation_message=d.get("validation_message"))


@dataclass
class DatasetSplit:
    """split-first 记录（GET /datasets/splits 系列返回的 DatasetSplitRecord）。

    ``version`` 为空表示 unversioned split（split_first 无版本布局）。
    ``projected=True`` 表示本对象来自 version 内嵌 ``splits[]`` 的兼容投影
    （存量 version_first 数据无独立 split 记录，SplitsClient 回退投影）：
    ``dataset_split_id``/``status``/``published_at`` 均为空，``storage_path``
    取自内嵌 ``oss_prefix``。
    """
    dataset_split_id: str = ""
    projected: bool = False
    dataset: str = ""
    dataset_id: str = ""
    dataset_version_id: str | None = None
    version: str | None = None
    name: str = ""
    run_type: str | None = None
    status: str = ""
    storage_type: str = "oss"
    storage_path: str = ""
    manifest: SplitManifest | None = None
    created_by: str | None = None
    published_at: str | None = None
    last_ingested_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    registered: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetSplit":
        m = d.get("manifest")
        return cls(
            dataset_split_id=d.get("dataset_split_id", ""),
            projected=bool(d.get("projected", False)),
            dataset=d.get("dataset", ""),
            dataset_id=d.get("dataset_id", ""),
            dataset_version_id=d.get("dataset_version_id"),
            version=d.get("version"),
            name=d.get("name", ""),
            run_type=d.get("run_type"),
            status=d.get("status", ""),
            storage_type=d.get("storage_type", "oss"),
            storage_path=d.get("storage_path", ""),
            manifest=SplitManifest.from_dict(m) if isinstance(m, dict) else None,
            created_by=d.get("created_by"),
            published_at=d.get("published_at"),
            last_ingested_at=d.get("last_ingested_at"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            registered=d.get("registered", True))


@dataclass
class DatasetDetailStats:
    """dataset 详情统计（控制台 Overview 的 Versions/split/Instances/Size 数据源）。"""
    instance_count: int = 0
    file_count: int = 0
    size_bytes: int = 0

    @classmethod
    def from_dict(cls, d: dict | None) -> "DatasetDetailStats":
        d = d or {}
        return cls(instance_count=d.get("instance_count", 0),
                   file_count=d.get("file_count", 0),
                   size_bytes=d.get("size_bytes", 0))


@dataclass
class DatasetDetail:
    """dataset 富详情（GET /datasets/series/detail 完整响应）。

    相比轻量 DatasetSeries：新增版本/split 统计、最新版本、全量统计与可用环境。
    """
    dataset_name: str = ""
    dataset_l1: str = ""
    dataset_l2: str = ""
    dataset_id: str = ""
    display_name: str | None = None
    default_scaffold: str | None = None
    owner: str | None = None
    owner_team_id: str | None = None
    visibility: str = "private"
    benchmark_id: str | None = None
    status: str | None = None
    description: str | None = None
    teacher_direction: str | None = None
    teacher_type: str | None = None
    workspace_id: str | None = None
    queue_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    available_envs: list[str] = field(default_factory=list)
    version_count: int = 0
    split_count: int = 0
    latest_version: str | None = None
    stats: DatasetDetailStats = field(default_factory=DatasetDetailStats)
    parent_shell: bool = False
    claimable: bool | None = None
    registered: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetDetail":
        return cls(
            dataset_name=d.get("dataset_name", ""),
            dataset_l1=d.get("dataset_l1", ""),
            dataset_l2=d.get("dataset_l2", ""),
            dataset_id=d.get("dataset_id", ""),
            display_name=d.get("display_name"),
            default_scaffold=d.get("default_scaffold"),
            owner=d.get("owner"),
            owner_team_id=d.get("owner_team_id"),
            visibility=d.get("visibility", "private"),
            benchmark_id=d.get("benchmark_id"),
            status=d.get("status"),
            description=d.get("description"),
            teacher_direction=d.get("teacher_direction"),
            teacher_type=d.get("teacher_type"),
            workspace_id=d.get("workspace_id"),
            queue_id=d.get("queue_id"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            available_envs=list(d.get("available_envs") or []),
            version_count=d.get("version_count", 0),
            split_count=d.get("split_count", 0),
            latest_version=d.get("latest_version"),
            stats=DatasetDetailStats.from_dict(d.get("stats")),
            parent_shell=bool(d.get("parent_shell", False)),
            claimable=d.get("claimable"),
            registered=d.get("registered", True))


@dataclass
class ClaimWorkspace:
    """claim 候选 workspace（GET /datasets/claim-workspaces 每项）。"""
    queue_id: str = ""
    name: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "ClaimWorkspace":
        return cls(queue_id=d.get("queue_id", ""), name=d.get("name", ""))


@dataclass
class Benchmark:
    """benchmark 目录项（GET /benchmarks；主键是 source_id，无独立 id 字段）。"""
    source_id: str = ""
    name: str = ""
    teacher_directions: list[str] = field(default_factory=list)
    methods: list[str] = field(default_factory=list)
    is_core: bool | None = None
    source: str | None = None
    benchmark_create_time: str | None = None
    benchmark_update_time: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    synced_at: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> "Benchmark":
        return cls(
            source_id=d.get("source_id", ""),
            name=d.get("name", ""),
            teacher_directions=list(d.get("teacher_directions") or []),
            methods=list(d.get("methods") or []),
            is_core=d.get("is_core"),
            source=d.get("source"),
            benchmark_create_time=d.get("benchmark_create_time"),
            benchmark_update_time=d.get("benchmark_update_time"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
            synced_at=d.get("synced_at"))


@dataclass
class WorkflowStep:
    """workflow 单步执行记录。status: wait|process|finish|error。"""
    name: str = ""
    status: str = ""
    message: str = ""
    detail: dict = field(default_factory=dict)
    attempts: int = 0
    started_at: str | None = None
    finished_at: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> "WorkflowStep":
        return cls(
            name=d.get("name", ""),
            status=d.get("status", ""),
            message=d.get("message", ""),
            detail=d.get("detail") if isinstance(d.get("detail"), dict) else {},
            attempts=d.get("attempts", 0),
            started_at=d.get("started_at"),
            finished_at=d.get("finished_at"))


@dataclass
class WorkflowApproval:
    """审批信息（approval 工作流才有）。status: pending|approved|rejected。"""
    provider: str = ""
    approve_id: str = ""
    instance_id: str = ""
    ticket_link: str = ""
    status: str = ""
    reason: str = ""
    approver: str = ""

    @classmethod
    def from_dict(cls, d: dict | None) -> "WorkflowApproval | None":
        if not isinstance(d, dict):
            return None
        return cls(
            provider=d.get("provider", ""),
            approve_id=d.get("approve_id", ""),
            instance_id=d.get("instance_id", ""),
            ticket_link=d.get("ticket_link", ""),
            status=d.get("status", ""),
            reason=d.get("reason", ""),
            approver=d.get("approver", ""))


@dataclass
class Workflow:
    """发布工作流（GET /workflows/{id}）。outputs 按_step 名为 key，结构随 kind
    演进（当前仅 benchmark-release），SDK 保持原始 dict 不做强类型映射。"""
    id: str = ""
    kind: str = ""
    status: str = ""
    current_step: str = ""
    description: str = ""
    creator: str = ""
    idempotency_key: str = ""
    spec: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    steps: list[WorkflowStep] = field(default_factory=list)
    approval: WorkflowApproval | None = None
    error_msg: str = ""
    version: int = 0
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> "Workflow":
        return cls(
            id=d.get("id", ""),
            kind=d.get("kind", ""),
            status=d.get("status", ""),
            current_step=d.get("current_step", ""),
            description=d.get("description", ""),
            creator=d.get("creator", ""),
            idempotency_key=d.get("idempotency_key", ""),
            spec=d.get("spec") if isinstance(d.get("spec"), dict) else {},
            outputs=d.get("outputs") if isinstance(d.get("outputs"), dict) else {},
            steps=[WorkflowStep.from_dict(s) for s in (d.get("steps") or [])],
            approval=WorkflowApproval.from_dict(d.get("approval")),
            error_msg=d.get("error_msg", ""),
            version=d.get("version", 0),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"))


@dataclass
class RoleBinding:
    """role-binding 记录（GET /role-bindings 每项）。"""
    scope: str = ""
    resource_type: str | None = None
    resource_id: str | None = None
    workspace_id: str | None = None
    principal_type: str = ""
    principal_id: str = ""
    principal_name: str | None = None
    principal_realname: str | None = None
    role_id: str = ""
    added_by: str = ""
    added_at: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "RoleBinding":
        return cls(
            scope=d.get("scope", ""),
            resource_type=d.get("resource_type"),
            resource_id=d.get("resource_id"),
            workspace_id=d.get("workspace_id"),
            principal_type=d.get("principal_type", ""),
            principal_id=d.get("principal_id", ""),
            principal_name=d.get("principal_name"),
            principal_realname=d.get("principal_realname"),
            role_id=d.get("role_id", ""),
            added_by=d.get("added_by", ""),
            added_at=d.get("added_at", ""))


# ── Dataset Objects（目录/文件列举）──────────────────────────────────

@dataclass
class DatasetObjectDirectory:
    """``GET /datasets/objects`` 返回的目录项。"""
    name: str
    path: str

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetObjectDirectory":
        return cls(name=d.get("name", ""), path=d.get("path", ""))

    def to_dict(self) -> dict:
        return {"name": self.name, "path": self.path}


@dataclass
class DatasetObjectFile:
    """``GET /datasets/objects`` 返回的文件项。"""
    name: str
    path: str
    size_bytes: int = 0
    content_type: str = ""
    previewable: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetObjectFile":
        return cls(
            name=d.get("name", ""),
            path=d.get("path", ""),
            size_bytes=int(d.get("size_bytes", 0)),
            content_type=d.get("content_type", ""),
            previewable=bool(d.get("previewable", False)))

    def to_dict(self) -> dict:
        return {"name": self.name, "path": self.path,
                "size_bytes": self.size_bytes,
                "content_type": self.content_type,
                "previewable": self.previewable}


@dataclass
class DatasetObjectListResult:
    """``GET /datasets/objects`` 分页响应。

    ``directories`` 和 ``files`` 为当前页条目；``truncated`` 为 True 时
    可用 ``next_token`` 继续翻页。
    """
    dataset: str = ""
    version: str = ""
    prefix: str = ""
    directories: list[DatasetObjectDirectory] = field(default_factory=list)
    files: list[DatasetObjectFile] = field(default_factory=list)
    next_token: str = ""
    truncated: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> "DatasetObjectListResult":
        return cls(
            dataset=d.get("dataset", ""),
            version=d.get("version", ""),
            prefix=d.get("prefix", ""),
            directories=[DatasetObjectDirectory.from_dict(x)
                         for x in d.get("directories", [])],
            files=[DatasetObjectFile.from_dict(x)
                   for x in d.get("files", [])],
            next_token=d.get("next_token", ""),
            truncated=bool(d.get("truncated", False)))

    def to_dict(self) -> dict:
        return {
            "dataset": self.dataset, "version": self.version,
            "prefix": self.prefix,
            "directories": [d.to_dict() for d in self.directories],
            "files": [f.to_dict() for f in self.files],
            "next_token": self.next_token,
            "truncated": self.truncated}
