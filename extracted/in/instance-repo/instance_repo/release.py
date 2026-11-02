"""release.py — benchmark-release workflow 请求体的纯构造器（无 I/O）。

publish 的真实发布逻辑（源/目标 OSS CopyObject + ACR RepoSync、审批、RBAC、幂等）
在 apiserver 的 benchmark-release workflow；SDK 只负责把业务意图构造成 workflow
请求体、提交并轮询。源地址来自当前 Repo 的运行时配置，目标地址由调用方显式提供；若使用
repo-config，调用方须显式指定 cluster 或 storage_env 查询，并把结果传给对应源/目标配置。
这里是纯函数 builder，便于单测与复用（VersionsClient.publish 调用）。

路径/host 约定复用 paths.py（与 oss_upload/acr_push 写入约定一致）：
  OSS  oss://<bucket>/swe/datasets/<L1>/<L2>/<version>[-assets]/<id>/content.tgz
       oss://<bucket>/swe/datasets/<L1>/<L2>/<version>/<id>.json
  ACR  <host>/<ns>/<sanitize(L2)>:<version>-<id>
"""
from __future__ import annotations

import hashlib
import json

from . import layout as L
from . import paths as P
from .errors import SchemaError

KIND = "benchmark-release"
# workflow.status 终态（见对接文档 §4）
TERMINAL_OK = {"succeeded"}
TERMINAL_BAD = {"failed", "canceled", "cancelled"}
AWAITING_APPROVAL = "awaiting_approval"


def _split_first_layout(layout: "L.Layout | None") -> "L.Layout":
    """Return the explicit layout for normal release builders.

    Legacy layouts remain available through the low-level :class:`Layout`
    decoder, but public release construction is a normal business operation and
    must never emit version-first paths.
    """
    lay = layout or L.Layout(L.MODEL_SPLIT_FIRST)
    if lay.model != L.MODEL_SPLIT_FIRST:
        raise SchemaError(
            "normal release builders require metadata_model=split_first; "
            "version_first is retained only for low-level legacy reads")
    return lay


def build_oss_distributions(dataset: str, version: str, instances: list[str], *,
                            src_bucket: str, dst_bucket: str,
                            granularity: str, overwrite: bool = False,
                            split: str = "",
                            instance_objects: str = "all",
                            layout: "L.Layout | None" = None) -> list[dict]:
    """构造 oss_distributions 数组。

    granularity:
      * 'dataset'  → 单条，覆盖整个 dataset 前缀（oss://.../swe/datasets/<L1>/<L2>/），
                     payload 最小；假定运行时源前缀只含 KEEP 内容。
      * 'instance' → 逐 KEEP id 枚举，每实例 3 条（content.tgz + index json + report.jsonl）。

    ``split`` **必须与 push 时一致**。正常发布固定 split-first；漏传会在拼路径前被
    拒绝，避免 workflow 到 validate 阶段才报 "source_path does not exist"。

    ``split`` 默认空串是为了强制调用方明确发布单元，而不是静默替调用方选择
    ``"default"``。``layout`` 是兼容形参，只接受 split-first；version 可为空串，
    此时对象少一层版本目录。

    不变量（上架必带 report）：instance 粒度会为每个 id 列出 `report.jsonl` 作为拷贝源，
    因此发布前【须】先经 ReportsClient.put 把各实例 report 上传到运行时源地址；否则 apiserver
    的拷贝 workflow 会在源对象缺失处失败（本纯函数不做 I/O 预检，故调用方负责保证）。
    """
    lay = _split_first_layout(layout)
    if granularity == "dataset":
        root = lay.dataset_root(dataset)
        return [{
            "source_path": P.oss_uri(src_bucket, root),
            "target_path": P.oss_uri(dst_bucket, root),
            "overwrite": overwrite,
        }]
    if granularity == "instance":
        if not instances:
            raise SchemaError("granularity='instance' 需要非空 instances 列表")
        if instance_objects not in ("all", "report_only"):
            raise SchemaError(
                f"unknown instance_objects {instance_objects!r} "
                f"(use 'all'|'report_only')")
        dists: list[dict] = []
        for iid in instances:
            if instance_objects == "report_only":
                # SDK 已把「task.toml 改写为生产镜像」的 content.tgz 与 {id}.json 直传
                # 目标桶，workflow 只需复制 report.jsonl（见 deliver_to_prod 的
                # rewrite_task_toml_image）。
                keys = (lay.report_key(dataset, iid, version=version, split=split),)
            else:
                keys = (lay.content_key(dataset, iid, version=version, split=split),
                        lay.metadata_key(dataset, iid, version=version, split=split),
                        lay.report_key(dataset, iid, version=version, split=split))
            for key in keys:
                dists.append({
                    "source_path": P.oss_uri(src_bucket, key),
                    "target_path": P.oss_uri(dst_bucket, key),
                    "overwrite": overwrite,
                })
        return dists
    raise SchemaError(f"unknown granularity {granularity!r} (use 'dataset'|'instance')")


# extend_meta 里承载「实例↔镜像」可追溯记录的扁平键名。用扁平字符串（而非嵌套
# object）：SDK 的 extend_meta 值类型为 str（Py dict[str,str] / Go map[string]string），
# apiserver 的 extend_meta 是 map[string]any，扁平 str 三者皆兼容、顶层可直接查询。
IMAGE_RELEASE_SOURCE_KEY = "image_release_source"
IMAGE_RELEASE_TARGET_KEY = "image_release_target"
IMAGE_ON_SOURCE_ACR_KEY = "image_on_source_acr"


def image_release_meta(docker_ref: str | None, src_acr: str, dst_acr: str,
                       dst_namespace: str = "") -> dict[str, str]:
    """算单个实例发布时「源镜像→目标镜像」的可追溯记录（写进 {id}.json.extend_meta）。

    过滤口径与 :func:`build_image_distributions` 完全一致（同一判断，避免漂移）：
      * ``docker_ref`` 位于 ``src_acr`` 下 → 随数据集发布搬运，记 source + target(换 host
        与可选 namespace) + ``on_source_acr="true"``；
      * ``docker_ref`` 指向别的 registry（共享/公共 base，不随发布搬运）→ 只记 source +
        ``on_source_acr="false"``，不产出 target（避免记一个从未搬运的假目标地址）；
      * ``docker_ref`` 为空 → 返回 {}。

    返回可直接并入 ``extend_meta`` 的扁平 str→str dict。

    重要口径说明：本记录**不等于**元数据改写。上架 workflow 只搬运镜像层，不会把已入库的
    ``docker_image`` 字段改成目标地址（apiserver 侧全链路零改写，已核实）。这里写入
    extend_meta 是让映射关系可查、可追溯，运行期仍按原 ``docker_image`` 拉取。
    """
    ref = (docker_ref or "").strip()
    if not ref:
        return {}
    if ref.startswith(src_acr + "/"):
        return {
            IMAGE_RELEASE_SOURCE_KEY: ref,
            IMAGE_RELEASE_TARGET_KEY: P.retarget_image(
                ref, src_acr, dst_acr, dst_namespace),
            IMAGE_ON_SOURCE_ACR_KEY: "true",
        }
    return {IMAGE_RELEASE_SOURCE_KEY: ref, IMAGE_ON_SOURCE_ACR_KEY: "false"}


def build_image_distributions(dataset: str, version: str, instances: list[str], *,
                              src_acr: str, src_namespace: str, dst_acr: str,
                              dst_namespace: str = "",
                              recorded_images: dict[str, str] | None = None,
                              layout: "L.Layout | None" = None,
                              split: str = "") -> list[dict]:
    """按 KEEP 实例逐个枚举 ACR 镜像分发（API 不支持整仓同步，每条须带 tag）。

    源镜像解析顺序 —— **落库优先、命名规则回落**：
      1. ``recorded_images[iid]``：push 时写入实例元数据的真实 ``docker_image``（权威值）；
      2. 缺失时按正常 split-first 写入规则重建为
         ``<src_acr>/<ns>/<sanitize(L2)>:<split>-<id>``。

    为什么不能只用规则重建（这是实测过的真实缺陷）：实例若**不自带 image.tar.gz**、而是
    复用共享 base（harbor 常见形态），push 时 ``docker_image`` 记的是 Dockerfile 的 FROM
    （如 ``<acr>/<ns>/<base-runtime>:<tag>``），与规则重建出的引用**完全不同**；只按规则拼会
    指向一个**从未推送过的镜像**，release 的 image validate 必然失败。

    过滤规则：**只保留源镜像确实位于 ``src_acr`` 的条目**。落库值若指向别的 registry（例如
    共享/公共 base 或另一运行时地址），直接跳过，避免生成 ``source==target``
    的无意义分发，也避免 workflow 尝试无法完成的跨 registry 拷贝。实例元数据里的
    ``docker_image`` 保持不变，runner 仍按原始引用拉镜像。

    ``dst_namespace`` 非空时目标引用同时替换命名空间。v0.8 之前三语言 CLI 都解析了
    ``--target-acr-namespace`` 却从未把它用上（只换 host），本参数是该缺陷的修复。

    instances 为空则返回 []。
    """
    lay = _split_first_layout(layout)
    recorded = recorded_images or {}
    dists: list[dict] = []
    for iid in sorted(instances):
        src = (recorded.get(iid) or "").strip() or lay.image_ref(
            src_acr, src_namespace, dataset, iid, version=version, split=split)
        if not src.startswith(src_acr + "/"):
            continue
        dists.append({
            "source_image": src,
            "target_image": P.retarget_image(src, src_acr, dst_acr, dst_namespace),
        })
    return dists


def build_dataset_distributions(dataset: str, *,
                                split: str = "",
                                version: str = "",
                                metadata_model: str = "",
                                src_bucket: str,
                                overwrite: bool = False,
                                layout: "L.Layout | None" = None) -> list[dict]:
    """构造 ``dataset_distributions`` 数组（apiserver master 的 dataset release 协议）。

    与 :func:`build_oss_distributions` 的纯前缀拷贝不同，本协议每项携带
    ``metadata_model/dataset/split/version/source_path``，服务端据此解析发布单元、
    从 online Dataset base 派生目标路径（SDK 不提供 target_path），发布成功后以
    ``publish_after_validation=true`` 只 ingest 该单元并置 published。

    正常发布固定 ``split_first``：split 必填、version 可选。无 version 时源目录是
    ``swe/datasets/<L1>/<L2>/<split>/``；有 version 时是
    ``swe/datasets/<L1>/<L2>/<version>/<split>/``。传入 legacy model/layout 会在
    构造任何分发项前拒绝。

    返回单元素数组（一次发布一个 split）；多个单元多次调用后合并提交。
    """
    lay = _split_first_layout(layout)
    model = L.normalize_metadata_model(metadata_model)
    if model != L.MODEL_SPLIT_FIRST:
        raise SchemaError(
            "normal release builders require metadata_model=split_first; "
            "version_first is retained only for low-level legacy reads")
    ver, spl = L.check_locator(model, version, split)
    key = f"{lay.dataset_root(dataset)}{ver + '/' if ver else ''}{spl}/"
    return [{
        "source_path": P.oss_uri(src_bucket, key),
        "dataset": dataset,
        "metadata_model": model,
        "version": ver,
        "split": spl if model == L.MODEL_SPLIT_FIRST else "",
        "overwrite": overwrite,
    }]


def make_idempotency_key(dataset: str, version: str, scope: str,
                         oss_dists: list[dict], image_dists: list[dict],
                         dataset_dists: list[dict] | None = None) -> str:
    """内容寻址幂等 key：相同内容→相同 key→平台复用已有 workflow（安全重试）。
    形如 ``<sanitize(dataset)>-<version>-release-<scope>-<sha1[:10]>``。

    ``dataset_dists`` 为空时不进载荷——保持与三语言 conformance golden 的旧 key
    逐字节一致（纯拷贝协议的既有调用方 key 不变）；非空时才参与哈希，使两种协议
    互不串用同一个 workflow。
    """
    payload = {"oss": oss_dists, "image": image_dists}
    if dataset_dists:
        payload["dataset"] = dataset_dists
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return f"{P.sanitize_repo(dataset)}-{version}-release-{scope}-{digest}"


def build_release_request(*, idempotency_key: str, description: str,
                          oss_dists: list[dict], image_dists: list[dict],
                          dataset_dists: list[dict] | None = None,
                          approval_mode: str = "internal",
                          backend: str = "acr") -> dict:
    """组装 benchmark-release workflow 请求体；空的分发数组省略（均可选）。

    ``dataset_dists`` 走 apiserver master 的 ``dataset_distributions`` 发布协议
    （split-first 的 split 发布 / version-first 的版本发布），与 ``oss_dists``
    的纯前缀拷贝语义不同：前者发布成功后由服务端 ingest 并置 published。

    ``backend`` 自 v0.8 起默认 ``"acr"``（v0.7.x 为 ``"bp"``）：镜像分发的真实执行后端就是
    ACR 仓库同步，默认值应与之一致，避免调用方每次都要显式纠正。
    """
    spec: dict = {"approval_mode": approval_mode, "backend": backend}
    if image_dists:
        spec["image_distributions"] = image_dists
    if dataset_dists:
        spec["dataset_distributions"] = dataset_dists
    if oss_dists:
        spec["oss_distributions"] = oss_dists
    return {
        "kind": KIND,
        "idempotency_key": idempotency_key,
        "description": description,
        "spec": spec,
    }
