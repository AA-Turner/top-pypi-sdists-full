"""store/registry.py — 元数据后端（调 apiserver 实体 API）。

register→pending / commit→ready / get / query / feedback。published 版本
由 apiserver 侧拒写（transport 抛 Immutable）。
"""
from __future__ import annotations

import contextlib
from urllib.parse import quote

from ..clients.config import business_metadata_model
from ..errors import TransportError
from ..models import DatasetInstance
from .base import BaseMetadataRegistry

# apiserver 数字业务码：两者都以 HTTP 404 返回，但语义必须区分开。
CODE_DATASET_NOT_FOUND = 92001    # 数据集不存在（名字拼错等）——应当报错
CODE_INSTANCE_NOT_FOUND = 92003   # 实例不存在——"没有"不是错误，get 返回 None


@contextlib.contextmanager
def _unimplemented(endpoint: str, hint: str):
    """把实例写端点的**路由级 404** 翻译成可操作的报错。

    apiserver 尚未注册 register/commit 两个写端点，命中时返回 Go mux
    的纯文本 ``404 page not found``（应用级 404 是 JSON 信封，两者要区分）。裸 404
    对调用方毫无信息量，这里补上"哪个端点没实现、该改用什么"。status 原样保留，
    不影响重试与上层 HTTP 语义。
    """
    try:
        yield
    except TransportError as e:
        if e.status == 404 and "page not found" in str(e):
            raise TransportError(
                f"{endpoint} 未在当前 apiserver 部署上实现（路由级 404）。{hint}",
                status=404) from e
        raise


def _q(dataset: str, version: str, split: str | None = None,
       instance_id: str | None = None, *, keep_default_split: bool = False) -> str:
    # 注意：apiserver 端 datasetNameFromQuery 只认 dataset_name（不是 dataset）；
    # 用 dataset= 会 404/"dataset_name is required"。此处务必对齐服务端契约。
    parts = [f"dataset_name={quote(dataset, safe='')}",
             f"version={quote(version, safe='')}"]
    if split and (split != "default" or keep_default_split):
        # version_first / 未声明 metadata_model："default" 是"无 split"的哨兵 → 省略 split
        # 参数让 apiserver 跨 split 匹配（含空 split）。split_first："default" 是真实 split
        # 名 → 必须显式下发，否则 apiserver 在 split_first 语义下报 92005 "split is required"。
        parts.append(f"split={quote(split, safe='')}")
    if instance_id:
        parts.append(f"instance_id={quote(instance_id, safe='')}")
    return "&".join(parts)


class ApiMetadataRegistry(BaseMetadataRegistry):
    _BASE = "/apis/v1/datasets/instances"

    def __init__(self, transport, *, environment: str = "",
                 metadata_model: str = "") -> None:
        self._t = transport
        self._environment = (environment or "").strip()
        self._metadata_model = business_metadata_model(metadata_model)

    def _q(self, dataset: str, version: str, split: str | None = None,
           instance_id: str | None = None, *,
           environment: str | None = None,
           metadata_model: str | None = None) -> str:
        """读路径查询串：与写路径（ingest）对称下发 metadata_model 与 environment。

        两个字段都**必须**对称：写路径由 storage_env 派生 environment（dev→pre）写入 pre
        集合，读路径若不发，服务端缺省 online → push→ingest→list/get/pull 闭环断裂；
        服务端对读请求同样把空 metadata_model 归一为 version_first，而 SDK 默认
        split_first，不显式下发就会用旧语义去查 split-first 数据。environment 为空时
        省略（服务端按 online 缺省，保留未配置 storage_env 的旧行为）。

        ``environment`` / ``metadata_model`` 传 None 用构造期值，传非 None（含空串）
        覆盖本次调用——调用方（如 CLI 的 ``--environment``）需要显式指定集合时用它，
        不必按环境重建整个 Repo。
        """
        requested_model = (self._metadata_model if metadata_model is None
                           else metadata_model)
        model = business_metadata_model(requested_model)
        env = (self._environment if environment is None else environment).strip()
        base = _q(dataset, version, split, instance_id,
                  keep_default_split=(model == "split_first"))
        extra = []
        if model:
            extra.append(f"metadata_model={quote(model, safe='')}")
        if env:
            extra.append(f"environment={quote(env, safe='')}")
        return base + ("&" + "&".join(extra) if extra else "")

    def register(self, meta: DatasetInstance) -> DatasetInstance:
        """注册实例元数据（pending）。

        apiserver 契约（POST /apis/v1/datasets/instances）：

        * dataset / version / split 走 **query string**（``dataset_name`` /
          ``version`` / ``split``），body 里没有 dataset 字段——handler 用
          ``DisallowUnknownFields`` 解码，发 ``dataset``/``dataset_version`` 会被
          400 拒；query 缺 dataset_name 则在 split_first 定位时 92005。
        * body 只接受 ``instance_id`` / ``split`` / ``manifest`` / ``tags`` /
          ``difficulty`` / ``docker_image`` / ``extend_meta``（
          createDatasetInstanceRequest 白名单）。
        * split 的 ``default`` 哨兵归一为空串（与写路径 _version_prefix 对称）。

        owner_reference 等其余字段在 register 端点无承接位（owner 由 apiserver
        据 caller 派生），故不进 body。
        """
        meta.validate()
        if self._metadata_model == "split_first":
            # split_first: "default" 是真实 split 名，不作哨兵归一 → 必须显式下发
            split = meta.split or ""
        else:
            split = "" if meta.split == "default" else (meta.split or "")
        body: dict = {"instance_id": meta.instance_id, "split": split}
        if meta.manifest:
            body["manifest"] = [m.to_dict() for m in meta.manifest]
        if meta.tags:
            body["tags"] = meta.tags
        if meta.difficulty is not None:
            body["difficulty"] = meta.difficulty
        if meta.docker_image:
            body["docker_image"] = meta.docker_image
        if meta.extend_meta:
            body["extend_meta"] = meta.extend_meta
        path = f"{self._BASE}?{self._q(meta.dataset, meta.dataset_version, split)}"
        with _unimplemented(
                "POST /apis/v1/datasets/instances（实例注册）",
                "当前可用路径：push(register=False) 只传 OSS，再用 versions.ingest() 扫描入库。"):
            data = self._t.post(path, body)
        return DatasetInstance.from_dict(data)

    def commit(self, instance_uid: str, digests: dict | None,
               manifest: list | None = None) -> DatasetInstance:
        # digests=None 时**省略**该字段（apiserver 保留原值），而非发 null——与 Go 对齐。
        # skip 分支据此不覆盖 OSS 上别的生产者的 digest。
        body: dict = {"id": instance_uid}
        if digests is not None:
            body["digests"] = digests
        if manifest is not None:
            body["manifest"] = [m.to_dict() for m in manifest]
        with _unimplemented(
                "POST /apis/v1/datasets/instances:commit（实例提交）",
                "当前可用路径：push(register=False) 只传 OSS，再用 versions.ingest() 扫描入库。"):
            data = self._t.post(f"{self._BASE}:commit", body)
        return DatasetInstance.from_dict(data)

    def get(self, dataset: str, version: str, instance_id: str,
            split: str | None = None, *,
            environment: str | None = None,
            metadata_model: str | None = None) -> DatasetInstance | None:
        """取单个实例；**实例不存在返回 None**（"没有"不是错误）。

        apiserver 对"实例不存在"回 HTTP 404 + 业务码 92003，对"数据集不存在"回 404 +
        92001。只吞前者：数据集名拼错必须照常报错，否则会被静默当成"没有这个实例"。
        """
        try:
            data = self._t.get(
                f"{self._BASE}/detail?"
                f"{self._q(dataset, version, split, instance_id, environment=environment, metadata_model=metadata_model)}")
        except TransportError as e:
            if e.status == 404 and e.biz_code == CODE_INSTANCE_NOT_FOUND:
                return None
            raise
        if not data:
            return None
        return DatasetInstance.from_dict(data)

    def query(self, dataset: str, version: str,
              split: str | None = None, *,
              environment: str | None = None,
              metadata_model: str | None = None) -> list[DatasetInstance]:
        # 分页遍历：服务端 page_size 上限 200，默认只回第一页（真机踩坑：1580 实例
        # 只读回 50）。显式传 page_size=200 并按 pagination.total 翻页取满；
        # 旧服务端不带 pagination 信封时单页即全部，行为与修复前一致。
        all_rows: list[dict] = []
        page = 1
        while True:
            data, pagination = self._t.request_with_meta(
                "GET", f"{self._BASE}?"
                       f"{self._q(dataset, version, split, environment=environment, metadata_model=metadata_model)}"
                       f"&page={page}&page_size=200")
            rows = data.get("instances", data) if isinstance(data, dict) else data
            rows = rows if isinstance(rows, list) else []  # 非列表（裸 dict 等）→ 空结果
            all_rows.extend(rows)
            if not rows:
                break  # 空页防御：即使 pagination 声称还有 total，也不再翻页（避免死循环）
            if not isinstance(pagination, dict):
                break
            total = pagination.get("total")
            # int/float 都接受：Go 服务端 JSON 整数解成 int，其他实现可能给 float，
            # 只认 int 会把 float total 当成"无 total"而静默截断（与 Go/Java 对齐）。
            if not isinstance(total, (int, float)) or len(all_rows) >= total:
                break
            page += 1
        return [DatasetInstance.from_dict(r) for r in all_rows]

    def feedback_append(self, dataset: str, version: str, instance_id: str,
                        feedback: dict, split: str | None = None) -> DatasetInstance:
        # apiserver 契约（POST /apis/v1/datasets/instances/feedbacks）：
        # dataset_name/version/split/instance_id 走 **query**（复用 _q，与 get/query 对称），
        # body 只放单个 Feedback 本体；响应返回更新后的 DatasetInstance。
        data = self._t.post(
            f"{self._BASE}/feedbacks?{self._q(dataset, version, split, instance_id)}",
            feedback)
        return DatasetInstance.from_dict(data)
