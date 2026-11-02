"""repo.py — Repo Facade：组装 transport + store + 三资源客户端。"""
from __future__ import annotations

import logging
import os
import posixpath

logger = logging.getLogger(__name__)

from . import bootstrap
from . import paths as P
from .clients.config import (
    ENV_API_KEY,
    LEGACY_ENV_API_KEY,
    business_metadata_model,
    fetch_repo_config,
    load_profile,
    resolve_config_value,
)
from .clients.benchmarks import BenchmarksClient
from .clients.datasets import DatasetsClient
from .clients.images import ImageClient
from .clients.instances import InstancesClient
from .clients.reports import ReportsClient
from .clients.scaffold import ScaffoldClient
from .clients.splits import SplitsClient
from .clients.versions import VersionsClient
from .clients.workflows import WorkflowsClient
from .concurrency import ItemError
from .errors import JobFailed, RegistrationFailed, SchemaError
from .store.acr import AcrImageStore
from .store.oss import OssContentStore
from .store.registry import ApiMetadataRegistry
from .transport import Transport


class Repo:
    """SDK 入口。所有 OSS/ACR 操作经此，先向 apiserver 换 STS 再直连。

    为可测：transport 与两个数据面执行器（bucket_factory / runner）均可注入。
    """

    def __init__(self, profile: str = "default", *, token: str | None = None,
                 env: str | None = None, transport=None,
                 bucket_factory=None, runner=None,
                 profile_overrides: dict | None = None,
                 api_env: str | None = None,
                 api_base: str | None = None,
                 cluster: str | None = None,
                 storage_env: str | None = None,
                 metadata_model: str | None = None) -> None:
        # v0.8「三参数起步」：token + api_env（控制面）+ storage_env（数据面）。
        # 其余寻址字段（oss_bucket / acr_host / acr_namespace / oss_prefix）由 bootstrap
        # 向 apiserver 的 repo-config 自动拉取，用户无需手填。
        self.profile = load_profile(profile, overrides=profile_overrides,
                                    api_env=api_env, api_base=api_base,
                                    cluster=cluster, storage_env=storage_env,
                                    metadata_model=metadata_model)
        tok = resolve_config_value(
            token, ENV_API_KEY, LEGACY_ENV_API_KEY)
        # Env 头：显式 env 优先，否则跟随解析出的 api_env（参数 / IR_API_ENV）；二者都
        # 未提供时由配置解析器使用 "product"，与 load_profile 的运行时契约一致。
        env_header = env if env is not None else self.profile.api_env
        self.transport = transport or Transport(
            self.profile.api_base, tok, env=env_header)
        # 自动发现：只填空字段，显式 overrides 与遗留环境变量优先。**失败不抛**——纯控制面
        # 操作（list/get/create/claim/whoami）不需要数据面寻址，构造期硬失败会把它们一起
        # 阻断；真正缺字段的报错延迟到首次用到该字段时给出，那时才说得清缺什么、为什么。
        bootstrap.resolve_profile(self.transport, self.profile)
        self._bucket_factory = bucket_factory
        self._content = OssContentStore(
            self.transport, self.profile.oss_bucket,
            bucket_factory=bucket_factory)
        self._image = AcrImageStore(
            self.transport, runner=runner,
            prefer_public=self.profile.prefer_public_registry)
        # 读路径必须与写路径对称下发 environment 与 metadata_model：
        # ingest 按 storage_env 写 pre 集合、默认 split_first，读若不下发会查 online/
        # version_first 而闭环断裂（历史真实缺陷，见 store/registry.py）。
        self._registry = ApiMetadataRegistry(
            self.transport,
            environment=self.profile.dataset_environment,
            metadata_model=business_metadata_model(self.profile.metadata_model))
        self.datasets = DatasetsClient(
            self.transport,
            profile=self.profile,
            content_store=self._content,
            oss_prefix=self.profile.oss_prefix,
            metadata_model=self.profile.metadata_model)
        self.versions = VersionsClient(
            self.transport, self.profile,
            content_store=self._content,
            oss_prefix=self.profile.oss_prefix)
        # split 管理模块（1.0.10）：split-first 记录的 list/get/update，
        # dataset 级全量视角（version_scope=all 缺省）。
        self.splits = SplitsClient(
            self.transport, self.profile,
            content_store=self._content,
            oss_prefix=self.profile.oss_prefix)
        # benchmark 目录 / 发布工作流查询（1.0.10）：claim 候选与 publish 状态。
        self.benchmarks = BenchmarksClient(self.transport)
        self.workflows = WorkflowsClient(self.transport)
        # push(register=True) 的上传后写库经 ingest 完成（:commit 端点缺失），
        # 注入 versions.ingest 作为 ingester 回调。
        self.instances = InstancesClient(
            self.transport, self.profile, self._content, self._image,
            self._registry,
            ingester=lambda *args, **kwargs: self.versions.ingest(
                *args, **kwargs))
        self.reports = ReportsClient(self._content, self.profile)
        # 独立镜像能力（v0.8 新增）：push / pull / copy / exists 不再依赖实例目录。
        self.images = ImageClient(self.transport, self.profile, self._image)
        # AgentPlatformScaffoldPackage：仅存储（无元数据）；目标桶/根前缀由 profile 提供
        self.scaffold = ScaffoldClient(
            self.transport, bucket=self.profile.scaffold_bucket,
            root=self.profile.scaffold_root, bucket_factory=bucket_factory)

    def refresh_config(self) -> dict:
        """强制重新拉取数据面寻址（绕过缓存）并回填当前 profile。

        寻址配置变更频率极低，默认缓存一小时；改了服务端配置想立刻生效时调用本方法。
        返回本次解析出的寻址字段字典。
        """
        bootstrap.resolve_profile(self.transport, self.profile, refresh=True)
        return {f: getattr(self.profile, f)
                for f in bootstrap.DISCOVERABLE_FIELDS
                if getattr(self.profile, f, "")}

    # ── 高吞吐批量交付（并发 push(register=False) + 一次 ingest 入库）──
    def deliver(self, dataset: str, version: str, local_dirs, *,
                owner_reference=None,
                split: str = "default", push_image: bool = True,
                overwrite: bool = False, concurrency: int = 8,
                publish: bool = False, ingest: bool = True,
                continue_on_error: bool = False,
                image_release_dst_acr: str | None = None,
                skip_unchanged: bool = False,
                hash_func=None,
                content_hashes: dict | None = None,
                prune: bool = False,
                progress_callback=None,
                executor=None,
                compress_level: int | None = None,
                **ingest_kwargs) -> dict:
        """上传一批实例并只注册实际成功的 instance ID（增量，绝不回退整 split 扫描）。

        Registration includes uploaded and OSS-skipped results, is chunked by the
        instances client, and never widens to a whole-split scan. ``publish=True``
        is the explicit full-intent exception: after every selected chunk completes
        and no upload failed, one full reconcile runs with publish enabled.

        参数:
          owner_reference : 整批共用同一来源引用（批量交付通常同源；需要逐实例不同来源
            时自行循环 ``instances.push``）。CLI 的 push / push-many / deliver 都把它
            设为必填——交付路径必须能追溯上游来源。
          split           : push 与注册共用的 split 名（缺省 ``"default"``）。
          push_image      : 是否推送 harbor 镜像（缺省 True）。
          overwrite       : 覆盖已存在对象（published split 会被前置拒绝）。
          concurrency     : 并发上传线程数（缺省 8）。
          publish         : 显式整 split 发布意图（缺省 False）。True 时在增量注册
            全部完成后执行一次 full reconcile+publish；任一上传失败即抛
            ``RegistrationFailed``（report 为 ``RegistrationReport``），绝不部分发布。
          ingest          : 是否把上传成功的 ID 增量注册入库（缺省 True）。
          continue_on_error : True 时失败项以 ``ItemError`` 占位返回、不阻断成功子集
            注册（缺省 False=全或无）。
          image_release_dst_acr : 可选目标 ACR host，把「实例↔镜像」分发映射写进
            ``extend_meta`` 随本次 ingest 入库。
          skip_unchanged  : 按 ``source_hash`` 跳过未变化实例（配合 hash_func/content_hashes）。
          hash_func / content_hashes : skip_unchanged 的哈希函数 / 预计算映射。
          prune           : **不支持**（缺省 False）。True 在任何 I/O 前抛
            ``SchemaError``——破坏性删除必须先做显式远端/本地对账。
          progress_callback : 每实例完成回调 ``(completed, total, result)``。
          executor        : 外部 ``ThreadPoolExecutor``（复用，不关闭）。
          compress_level  : gzip 压缩级别（1-9），None 用默认。

        其余关键字原样透传给 ``versions.ingest``（full-only 选项在增量模式下前置拒绝；
        ``dry_run`` 不允许——注册必须写库）。返回
        ``{"pushed", "skipped", "failed", "ingest", "ingests", "registration"}``。
        """
        if prune:
            raise SchemaError(
                "prune=True is not supported by deliver; perform an explicit "
                "remote/local reconciliation before any destructive deletion")
        if publish and not ingest:
            raise SchemaError("publish=True requires ingest=True")
        full_only = {
            "storage_path", "splits", "allow_layout_inference",
            "run_type", "split_run_types",
        }
        provided_full_only = sorted(full_only.intersection(ingest_kwargs))
        if provided_full_only and not publish:
            raise SchemaError(
                "incremental deliver does not support full-ingest options: "
                + ", ".join(provided_full_only))
        if ingest_kwargs.get("dry_run"):
            raise SchemaError("deliver cannot use dry_run because registration must write")
        selected_ingest_kwargs = {
            key: value for key, value in ingest_kwargs.items()
            if key not in full_only and key not in {"publish", "dry_run"}
        }

        batch = self.instances.push_many_with_report(
            local_dirs, dataset, version, owner_reference=owner_reference,
            split=split, push_image=push_image,
            overwrite=overwrite, register=ingest, concurrency=concurrency,
            continue_on_error=continue_on_error,
            image_release_dst_acr=image_release_dst_acr,
            skip_unchanged=skip_unchanged,
            hash_func=hash_func,
            content_hashes=content_hashes,
            progress_callback=progress_callback,
            executor=executor,
            compress_level=compress_level,
            ingest_kwargs=selected_ingest_kwargs)
        results = list(batch.results)
        registration = batch.registration
        pushed = [r for r in results
                  if not isinstance(r, ItemError)
                  and not getattr(r, "skipped", False)]
        skipped = [r for r in results
                   if not isinstance(r, ItemError)
                   and getattr(r, "skipped", False)]
        failed = [r for r in results if isinstance(r, ItemError)]
        jobs = [report.job for report in registration.ingests if report.job]

        if publish and not pushed and not skipped and not failed:
            raise SchemaError(
                "publish requires at least one successful or skipped upload")
        if publish and registration.selected_ids:
            if failed:
                # report 统一为 RegistrationReport（与 instances.ingest 抛出的
                # RegistrationFailed 同型，调用方可按同一 schema 恢复）；失败上传项
                # 作为附带诊断挂在报告实例上，不并入注册字段语义。
                registration.failed_uploads = list(failed)
                raise RegistrationFailed(
                    "publish refused after partial upload; selected registration "
                    "is preserved and failed uploads must be reconciled explicitly",
                    report=registration)
            registration_unfinished = (
                registration.pending or registration.failed
                or registration.unknown or registration.not_submitted
                or registration.completed != registration.selected_ids)
            if registration_unfinished:
                last_report = (registration.ingests[-1]
                               if registration.ingests else None)
                raise JobFailed(
                    "selected registration did not complete; refusing full "
                    "reconcile and publish",
                    status=registration.job_status or None,
                    job=(last_report.job if last_report else None),
                    report=registration)
            full_kwargs = dict(ingest_kwargs)
            full_kwargs.pop("publish", None)
            if "splits" not in full_kwargs and "split" not in full_kwargs:
                full_kwargs["split"] = split
            full_job = self.versions.ingest(
                dataset, version, publish=True, **full_kwargs)
            full_status = ((full_job or {}).get("status") or "").lower()
            if full_status != "completed":
                raise JobFailed(
                    "full reconcile did not complete; refusing publish flow",
                    status=full_status or None, job=full_job)
            jobs.append(full_job)

        legacy_job = jobs[0] if len(jobs) == 1 else None
        return {"pushed": pushed, "skipped": skipped, "failed": failed,
                "ingest": legacy_job, "ingests": jobs,
                "registration": registration}

    # ── 源到目标交付：上传 → 元数据入库 → 发布 workflow ────────────────────────
    def deliver_to_prod(self, dataset: str, version: str, local_dirs, *,
                        owner_reference=None,
                        split: str = "default", push_image: bool = True,
                        overwrite: bool = False, concurrency: int = 8,
                        continue_on_error: bool = False,
                        target: str = "", target_overrides: dict | None = None,
                        granularity: str = "instance",
                        images: str | None = None,
                        approval_mode: str = "internal", backend: str = "acr",
                        description: str = "", wait_approval: bool = False,
                        rewrite_task_toml_image: bool = True,
                        raise_on_failure: bool = True,
                        poll_sec: float = 5.0, timeout_sec: float = 1800.0,
                        ingest_raise_on_failure: bool = True,
                        ingest_poll_sec: float = 5.0,
                        ingest_timeout_sec: float = 1800.0,
                        **ingest_kwargs) -> dict:
        """把一批实例从当前 Repo 的源数据面交付到运行时配置的目标数据面。

        尽管方法名保留 ``deliver_to_prod`` 以兼容现有调用，它不绑定 ``dev``、``prod``
        或 ``production`` profile。源 OSS/ACR 来自当前 Repo 的 ``profile_overrides``、
        环境变量或 ``repo-config`` 查询结果；目标 OSS/ACR 由 ``target_overrides`` 提供，
        也可直接使用另一目标的 ``repo-config`` 查询结果。``profile`` / ``target`` 只作标签，
        SDK 不内置任何环境到 bucket、registry 或权限策略的映射。

        调用顺序：

          ① ``push_many(register=False)``  → 写入运行时配置的源 OSS/ACR
          ② 增量注册（selected ingest）   → 只把本次实际成功（含 OSS skipped）的
             instance ID 分块注册入库；**不整 split 发布/锁定**——源侧绝不发送
             ``publish_after_validation``，也不执行 full reconcile
          ③ ``versions.publish``（workflow）→ prod 侧发布：按运行时源/目标寻址把
             对象与镜像分发到目标数据面（审批 / RBAC / 幂等等 workflow 语义原样保留）

        ② **不可跳过**：workflow 按 dataset/version 读取已入库元数据，数据集必须先可查、
        可被下游引用。源侧注册与目标侧发布是两件事：本次交付**不改变源 split 的
        published 状态**，源 split 的发布/锁定必须显式走 ``versions.ingest(publish=True)``
        或 ``splits.update(status='published')``。源与目标访问是否允许完全由运行时服务
        策略决定。

        失败即停（不静默走完后续阶段）：push 阶段按 ``continue_on_error`` 决定全或无；
        增量注册失败抛 ``RegistrationFailed``（附累计 ``RegistrationReport``），
        上架段到失败终态抛 ``JobFailed``。全部 push 失败时不会触发注册与上架
        （返回 ingest=None、release=None）。

        ``images`` 缺省跟随 ``push_image``（推了镜像就同步镜像）。上架只会分发**确实
        位于运行时源 ACR** 的镜像；复用公共/共享 base 的实例其 ``docker_image`` 指向别的
        registry，会被 ``build_image_distributions`` 跳过（见 ``skipped_images``），
        这些 base 由独立的镜像转储流程治理，不随数据集上架搬运。

        ``approval_mode="internal"``（默认）时 workflow 会停在人工审批：
        ``wait_approval=False`` 即在该状态返回，审批通过后由平台继续；置 True 则一直等到终态。
        合法值由 apiserver 定义为 ``internal`` | ``bpms``（其它值 400）。

        ``raise_on_failure`` / ``poll_sec`` / ``timeout_sec`` 作用于**上架段**；
        ingest 段用 ``ingest_raise_on_failure`` / ``ingest_poll_sec`` /
        ``ingest_timeout_sec``（同名具名参数会遮蔽 ``**ingest_kwargs``，故两段必须各有入口）。
        上架段置 ``raise_on_failure=False`` 时返回失败终态的 workflow 供诊断。

        **注册未到 ``completed`` 绝不上架**：增量注册还有"不报错但也没成功"的出口
        （``wait=False`` 提前返回、``raise_on_failure=False`` 时失败终态不抛），此时
        元数据并未真正入库，若继续上架会因源数据不可用而失败。这里显式拦一道并抛
        ``JobFailed``。``dry_run=True`` 与增量注册互斥，会更早地被 ``SchemaError``
        拒绝（见 ``versions.ingest``）。

        返回 ``{"pushed", "failed", "ingest", "release", "skipped_images"}``。
        """
        # 从运行时目标配置解析 ACR host：让 push 阶段就把「实例↔镜像」分发映射写进
        # extend_meta，随本次 ingest 入库（source==docker_ref，与 publish 的
        # image_distributions 同口径）。未提供目标 ACR 时不阻断交付，仅不写该映射。
        image_release_dst_acr = None
        want_images = (images is None and push_image) or (images == "on")
        if want_images:
            # 目标 ACR host 来自 target_overrides（SDK 不内置任何环境的仓地址）。
            image_release_dst_acr = (target_overrides or {}).get("acr_host") or None
        out = self.deliver(dataset, version, local_dirs,
                           owner_reference=owner_reference, split=split,
                           push_image=push_image, overwrite=overwrite,
                           concurrency=concurrency, ingest=True,
                           continue_on_error=continue_on_error,
                           image_release_dst_acr=image_release_dst_acr,
                           raise_on_failure=ingest_raise_on_failure,
                           poll_sec=ingest_poll_sec,
                           timeout_sec=ingest_timeout_sec, **ingest_kwargs)
        out["release"] = None
        out["skipped_images"] = []
        successful = out["pushed"] + out.get("skipped", [])
        if not successful:
            return out                      # 无一成功：不上架（deliver 也未 ingest）
        # deliver 只完成 selected 增量注册（源侧不整 split 发布/锁定、不发
        # publish_after_validation）；多 job 时旧 ingest 字段按契约为 None，
        # 因此必须检查完整 ingests 列表。
        ingest_jobs = out.get("ingests") or []
        ing_status = ((ingest_jobs[-1] if ingest_jobs else {}).get("status")
                      or "").lower()
        if ing_status != "completed":
            last_job = ingest_jobs[-1] if ingest_jobs else None
            raise JobFailed(
                f"ingest 未到 completed（当前 {ing_status or 'unknown'}），拒绝上架："
                f"元数据未入库时上架必然 source_path does not exist",
                status=ing_status or None, job=last_job)
        instances = [r.instance_id for r in successful]
        if not images:                      # None 或 "" 都跟随 push_image（对齐 Go）
            images = "on" if push_image else "off"

        # v0.8：把生产副本 task.toml 的 [environment].docker_image 改写为生产镜像引用。
        # 运行期真正决定拉哪个镜像的是 content.tgz 里的 task.toml，不是元数据里的
        # docker_image 字段；上架只逐字节复制 content.tgz，不改写则生产实例仍拉开发态
        # registry。这里在上架前本地改写并直传目标桶，避免「先复制再下载改回传」的多一趟。
        instance_objects = "all"
        retargeted: list[str] = []
        if rewrite_task_toml_image and images == "on":
            instance_objects, retargeted = self._retarget_prod_task_toml(
                dataset, version, split, local_dirs, out["pushed"],
                target=target, target_overrides=target_overrides,
                overwrite=overwrite)

        wf, skipped = self.versions.publish_with_report(
            dataset, version, instances=instances, target=target,
            target_overrides=target_overrides,
            granularity=granularity, images=images, overwrite=overwrite,
            split=split,          # 与 push 同一 split，否则上架源路径拼错（真机踩过）
            instance_objects=instance_objects,
            approval_mode=approval_mode, backend=backend,
            description=description or f"deliver_to_prod {dataset}/{version} "
                                       f"({len(instances)} instances)",
            wait_approval=wait_approval, raise_on_failure=raise_on_failure,
            poll_sec=poll_sec, timeout_sec=timeout_sec)
        out["release"] = wf
        out["skipped_images"] = skipped
        out["retargeted_task_toml"] = retargeted
        return out

    def _retarget_prod_task_toml(self, dataset, version, split, local_dirs,
                                 pushed, *, target, target_overrides, overwrite):
        """为上架把每个 harbor 实例的 task.toml 指向生产镜像并直传目标桶。

        仅处理 **harbor** 实例且其 ``docker_image`` 确实位于源 ACR（与
        ``build_image_distributions`` 同口径——只有这些镜像会随数据集搬到目标 ACR）。
        对每个这样的实例：本地重写 task.toml → 重打包 content.tgz → 重算 digest →
        重建 {id}.json，直传**目标桶**；随后 publish 用 ``instance_objects="report_only"``，
        workflow 只复制 report.jsonl，content.tgz 与 {id}.json 由本步骤直接写好。

        约束（保证正确性，宁可 fail-fast）：本批必须**全部**是可改写的 harbor 实例；
        若混入 SWE 实例或镜像不在源 ACR 上的实例，抛 SchemaError 说明为何不能整体
        report_only，并给出出路（设 rewrite_task_toml_image=False 接受生产 task.toml
        仍指向源 registry，或拆分批次）。

        重要限制：SDK 直传目标桶发生在 workflow 审批**之前/之外**，等于绕过审批门；
        被拒的上架会在目标桶留下未注册的孤儿对象。这是本能力的已知取舍，见使用指南。
        """
        from pathlib import Path as _Path
        import shutil as _shutil
        from .clients.config import load_profile
        from .validate import detect_format

        dst = load_profile(target or "target", overrides=target_overrides)
        if not dst.oss_bucket:
            raise SchemaError(
                "rewrite_task_toml_image 需要目标 oss_bucket（用 target_overrides 提供），"
                "否则无法把改写后的 content.tgz 直传目标桶")
        src_acr = self.profile.effective_acr_host
        dst_acr = dst.effective_acr_host
        dst_ns = dst.acr_namespace

        # instance_id → 本地目录（仅 harbor 目录；SWE 是 .json 文件，没有 task.toml）
        dir_by_id: dict[str, _Path] = {}
        for d in local_dirs:
            p = _Path(d)
            if detect_format(p) != "swe":
                dir_by_id[self.instances.validate(p).instance_id] = p

        # 落库镜像（权威源引用），与 build_image_distributions 同口径过滤
        recorded = self.versions._recorded_images(
            dataset, version, [r.instance_id for r in pushed], split)

        ineligible: list[str] = []
        plan: list[tuple[str, _Path, str]] = []   # (iid, dir, target_ref)
        for r in pushed:
            iid = r.instance_id
            src_ref = (recorded.get(iid) or r.docker_image or "").strip()
            if iid not in dir_by_id or not src_ref or not src_ref.startswith(src_acr + "/"):
                ineligible.append(iid)
                continue
            plan.append((iid, dir_by_id[iid],
                         P.retarget_image(src_ref, src_acr, dst_acr, dst_ns)))

        if ineligible:
            raise SchemaError(
                "rewrite_task_toml_image=True 需要本批实例全部是「镜像在源 ACR 上的 "
                f"harbor 实例」，但以下实例不满足：{ineligible}（SWE 实例无 task.toml，"
                "复用共享 base 的实例镜像不在源 ACR、不随数据集搬运）。出路：设 "
                "rewrite_task_toml_image=False 接受生产 task.toml 仍指向源 registry，"
                "或把可改写实例单独成批。")

        target_store = OssContentStore(
            self.transport, dst.oss_bucket, bucket_factory=self._bucket_factory)
        lay = self.instances._layout()
        for iid, d, target_ref in plan:
            tgz, digest, meta_json, _ck, _mk = self.instances.retarget_prod_content(
                d, dataset, version, split, target_ref)
            try:
                target_store.put(iid, dataset, version, split, tgz, meta_json,
                                 overwrite=True, layout=lay)
            finally:
                _shutil.rmtree(_Path(tgz).parent, ignore_errors=True)
        return "report_only", [iid for iid, _, _ in plan]

    # ── 用户输入数据（插件 / 数据合成输入）：swe/user-data/users/{uid}/ ─────────
    # users/ 这一层不能省：user-data 域根是 swe/user-data/，其下除 users/ 外还可能有
    # 别的子目录（如共享语料，仅系统白名单可只读）。apiserver 从 users/ 之后取 uid 段，
    # 把工号直接挂在域根下（swe/user-data/{uid}/）会被 94011 拒签。
    USER_DATA_ROOT = "swe/user-data/users/"

    @staticmethod
    def _user_data_prefix(uid: str) -> str:
        return Repo.USER_DATA_ROOT + (uid or "").strip().strip("/") + "/"

    @staticmethod
    def _clean_user_data_subpath(sub: str) -> str:
        """归一并校验用户子路径：去首尾 '/'、显式拒绝任何 '..' 段、禁止空。

        显式拒绝 '..'（而非依赖 normpath 静默消解）：'../x' 多为误用或恶意，
        直接失败比静默改写成 'x' 更可诊断、更安全。
        """
        sub = (sub or "").strip()
        if not sub:
            raise SchemaError("user-data subpath must not be empty")
        if any(seg == ".." for seg in sub.split("/")):
            raise SchemaError(f"invalid user-data subpath {sub!r}: '..' not allowed")
        cleaned = posixpath.normpath("/" + sub.lstrip("/")).lstrip("/")
        if not cleaned or cleaned == ".":
            raise SchemaError(f"invalid user-data subpath {sub!r}")
        return cleaned

    def whoami(self) -> str:
        """返回当前 apikey 对应的工号（user_id），供拼 user-data 前缀。

        工号可能带前导零（如 '0xxxxx'），须逐字符原样用于 prefix，切勿数字归一化。
        """
        resp = self.transport.get("/apis/v1/me/identity")
        uid = (resp or {}).get("user_id", "")
        if not str(uid).strip():
            raise SchemaError("empty user_id in /me/identity response")
        return str(uid)

    # ── 存储配置查询（从 apiserver 拉数据面寻址信息，无任何密钥）──
    def get_repo_config(self, *, cluster: str = "", storage_env: str = "") -> dict:
        """查询某 cluster/env 的数据面存储配置（oss_bucket/oss_prefix/acr_host/acr_namespace）。

        从 apiserver GET /apis/v1/repo-config 拉取，只含寻址信息、**不含 AK/SK/STS**。
        返回的 dict 可直接作为 profile_overrides 传给 Repo(...)，免去手工填桶名/仓库地址。
        cluster 与 storage_env 二选一，cluster 优先（apiserver 先由 cluster 解析出 storage_env）。
        """
        return fetch_repo_config(self.transport, cluster=cluster, storage_env=storage_env)

    def get_cluster_storage_env_map(self) -> dict:
        """查询 cluster → storage_env 的映射表（GET /apis/v1/repo-config/cluster-storage-env-map）。

        用于在不确定某执行集群对应哪个存储环境时先查映射，再用 storage_env 查 get_repo_config。
        """
        resp = self.transport.get("/apis/v1/repo-config/cluster-storage-env-map")
        if not isinstance(resp, dict):
            raise SchemaError("unexpected cluster-storage-env-map response shape")
        return resp

    def upload_user_data(self, uid: str, local_path, remote_subpath: str, *,
                         overwrite: bool = False) -> dict:
        """上传本地文件到 swe/user-data/users/{uid}/{remote_subpath}。"""
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        sub = self._clean_user_data_subpath(remote_subpath)
        pfx = self._user_data_prefix(uid)
        # sts_prefix 用精确对象 key（而非 uid 目录前缀）：跨用户 subpath 授权时，
        # apiserver 从 STS 请求的 prefix 里提取 subpath 做分层匹配——目录级 prefix
        # 提取不出 subpath，会退化为 uid 级判定，子路径授权形同虚设。
        return self._content.put_object(pfx + sub, str(local_path),
                                        overwrite=overwrite, sts_prefix=pfx + sub)

    def upload_user_data_dir(self, uid: str, local_dir, remote_subdir: str, *,
                             overwrite: bool = False) -> list[dict]:
        """递归上传本地目录到 swe/user-data/users/{uid}/{remote_subdir}/。"""
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        base = self._clean_user_data_subpath(remote_subdir)
        if not os.path.isdir(local_dir):
            raise SchemaError(f"{local_dir!r} is not a directory")
        outcomes: list[dict] = []
        for root, _dirs, files in os.walk(local_dir):
            for name in files:
                fp = os.path.join(root, name)
                rel = os.path.relpath(fp, local_dir).replace(os.sep, "/")
                outcomes.append(self.upload_user_data(
                    uid, fp, base + "/" + rel, overwrite=overwrite))
        return outcomes

    def download_user_data(self, uid: str, remote_subpath: str, local_path) -> str:
        """下载 swe/user-data/users/{uid}/{remote_subpath} 到本地 local_path。"""
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        sub = self._clean_user_data_subpath(remote_subpath)
        pfx = self._user_data_prefix(uid)
        # sts_prefix 同 upload：精确对象 key，让 apiserver 按 subpath 分层匹配授权。
        return str(self._content.get_object(pfx + sub, local_path,
                                            sts_prefix=pfx + sub))

    def list_user_data(self, uid: str, subpath: str = "") -> list[str]:
        """列举 swe/user-data/users/{uid}/{subpath} 下的对象 key（subpath 空=整个 uid 目录）。"""
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        pfx = self._user_data_prefix(uid)
        if str(subpath).strip():
            pfx += self._clean_user_data_subpath(subpath)
        return self._content.list_objects(pfx)

    # ── Artifact 下载（AP HTTP 链接，由服务端执行权限校验）──

    def download_artifact(self, job_id: str, cluster: str | None = None,
                          output_dir: str = ".", *,
                          ap_endpoint: str | None = None,
                          include_files: list[str] | None = None,
                          exclude_files: list[str] | None = None,
                          extract: bool = False) -> str:
        """下载单个 job 的 artifact (result.tgz) 到本地。

        鉴权：由 AP artifact 接口执行，SDK 不再查询 Job 详情作预检查。
        并发模型：单 job = 单文件单线程。

        Args:
            job_id: AP job ID
            cluster: 数据面名（默认使用 SDK profile 绑定的 cluster）
            output_dir: 本地输出目录
            ap_endpoint: AP 控制面 URL（可选，默认从环境变量或内置常量取）

        Returns:
            下载文件的本地路径
        """
        from .artifacts import download_artifact as _dl
        cluster = cluster or self.profile.cluster or ""
        return _dl(self.transport, self.transport.token, job_id,
                   cluster, output_dir, ap_endpoint,
                   include_files=include_files, exclude_files=exclude_files, extract=extract)

    def download_artifacts(self, job_ids: list[str],
                           cluster: str | None = None,
                           output_dir: str = ".", *,
                           max_concurrent: int = 8,
                           ap_endpoint: str | None = None,
                           include_files: list[str] | None = None,
                           exclude_files: list[str] | None = None,
                           extract: bool = False,
                           ) -> dict[str, str | Exception]:
        """批量下载多个 job 的 artifact。

        并发粒度是跨 job（不是单文件内多线程）。下载使用 AP 返回的 HTTP 链接。

        Args:
            job_ids: AP job ID 列表
            cluster: 数据面名
            output_dir: 本地输出目录
            max_concurrent: 最大并发下载数（默认 8）
            ap_endpoint: AP 控制面 URL

        Returns:
            {job_id: 本地文件路径 或 Exception}
        """
        from .artifacts import download_artifacts as _dl_many
        cluster = cluster or self.profile.cluster or ""
        return _dl_many(self.transport, self.transport.token, job_ids,
                        cluster, output_dir, max_concurrent, ap_endpoint,
                        include_files=include_files, exclude_files=exclude_files, extract=extract)

    def download_artifacts_from_group(self, group_id: str,
                                      cluster: str | None = None,
                                      output_dir: str = ".", *,
                                      max_concurrent: int = 8,
                                      ap_endpoint: str | None = None,
                                      include_files: list[str] | None = None,
                                      exclude_files: list[str] | None = None,
                                      extract: bool = False,
                                      ) -> dict[str, str | Exception]:
        """下载某个 group 下全部 job 的 artifact。

        先调 AP GET /groups/{group_id}/jobs 分页收集 job_id，再批量下载。

        Args:
            group_id: AP group ID
            cluster: 数据面名
            output_dir: 本地输出目录
            max_concurrent: 最大并发下载数
            ap_endpoint: AP 控制面 URL

        Returns:
            {job_id: 本地文件路径 或 Exception}
        """
        from .artifacts import fetch_group_job_ids, download_artifacts as _dl_many
        cluster = cluster or self.profile.cluster or ""
        job_ids = fetch_group_job_ids(
            self.transport.token, group_id, cluster, ap_endpoint)
        if not job_ids:
            logger.warning("group %s has no jobs", group_id)
            return {}
        return _dl_many(self.transport, self.transport.token, job_ids,
                        cluster, output_dir, max_concurrent, ap_endpoint,
                        include_files=include_files, exclude_files=exclude_files, extract=extract)

    # ── 用户数据 ACL（role-bindings 接口，resource_type=user_data）──
    _USER_DATA_ROLE_MAP = {
        "reader": "built-in:user-data-reader",
        "writer": "built-in:user-data-writer",
        "admin": "built-in:user-data-admin",
    }

    @staticmethod
    def _validate_user_data_acl_subpath(subpath: str) -> str:
        """校验子路径粒度授权的 subpath；空串合法（=uid 整目录级授权）。

        与 apiserver 对 resource_id 中 subpath 段的校验对齐：拒绝前导/尾随
        '/'、空段（'//'）、'..' 段与通配符（'*'/'?'）。注意这里**不做归一化**
        （区别于 _clean_user_data_subpath）：授权路径必须与存储 key 逐字符
        一致，静默改写（如剥掉首尾 '/'）会让授权指到错误资源。
        """
        sub = str(subpath or "").strip()
        if not sub:
            return ""
        if sub.startswith("/"):
            raise SchemaError(
                f"invalid user-data ACL subpath {subpath!r}: leading '/' not allowed")
        if sub.endswith("/"):
            raise SchemaError(
                f"invalid user-data ACL subpath {subpath!r}: trailing '/' not allowed")
        if "//" in sub:
            raise SchemaError(
                f"invalid user-data ACL subpath {subpath!r}: empty segment ('//') not allowed")
        if any(seg == ".." for seg in sub.split("/")):
            raise SchemaError(
                f"invalid user-data ACL subpath {subpath!r}: '..' not allowed")
        if "*" in sub or "?" in sub:
            raise SchemaError(
                f"invalid user-data ACL subpath {subpath!r}: wildcards ('*', '?') not allowed")
        return sub

    def _user_data_acl_resource_id(self, uid: str, subpath: str = "") -> str:
        """拼 user-data ACL 的 resource_id：{storage_env}/{uid}（subpath 非空时
        追加 /{subpath}，即 {storage_env}/{uid}/{subpath}）。"""
        sub = self._validate_user_data_acl_subpath(subpath)
        rid = f"{self.profile.storage_env}/{uid}"
        return f"{rid}/{sub}" if sub else rid

    def grant_user_data(self, uid: str, principal: str, role: str, *,
                        principal_type: str = "user", subpath: str = "") -> None:
        """授予 principal 对某用户数据目录（或其子路径）的角色。

        role: "reader" / "writer" / "admin"
        principal: 工号字符串（或 user_group id，配合 principal_type="user_group"）
        subpath: 子路径粒度授权（如 "plugins/cursor"），resource_id 相应为
            {storage_env}/{uid}/{subpath}；空（默认）=uid 整目录级授权。
        """
        role_id = self._USER_DATA_ROLE_MAP.get(role)
        if not role_id:
            raise SchemaError(
                f"invalid role '{role}'; valid values: "
                f"{', '.join(sorted(self._USER_DATA_ROLE_MAP))}")
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        self.transport.post("/apis/v1/role-bindings", {
            "scope": "resource",
            "resource_type": "user_data",
            "resource_id": self._user_data_acl_resource_id(uid, subpath),
            "principal_type": principal_type,
            "principal_id": str(principal),
            "role_id": role_id,
        })

    def revoke_user_data(self, uid: str, principal: str, role: str = "", *,
                         principal_type: str = "user", subpath: str = "") -> None:
        """撤销 principal 对某用户数据目录（或其子路径）的一条角色绑定。

        通过 DELETE /apis/v1/role-bindings?… 发送：apiserver 的 Remove 按
        (scope, resource_type, resource_id, principal_type, principal_id,
        role_id) 六元组唯一键定位，参数走 **query string**（非 body），
        role_id 必填。role 取 reader/writer/admin（映射 built-in:…）或
        完整 role_id；留空时默认撤销 reader（最常见——reader 绑定唯一时
        即等于全部撤销）。
        subpath 非空时只撤销子路径级绑定，不影响 uid 级绑定。

        注意：撤销不自动重试——第一次 DELETE 可能已生效但响应丢失，
        重试会因绑定已不存在返回 24401，把成功误报为失败。遇到传输
        错误先 ``list_user_data_acl`` 对账再决定是否重试。
        """
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        role = (role or "").strip() or "reader"
        role_id = self._USER_DATA_ROLE_MAP.get(role, role)
        if not role_id or ":" not in role_id:
            raise SchemaError(
                f"invalid role '{role}'; valid values: "
                f"{', '.join(sorted(self._USER_DATA_ROLE_MAP))} 或完整 role_id")
        resource_id = self._user_data_acl_resource_id(uid, subpath)
        from urllib.parse import quote
        qs = (f"scope=resource&resource_type=user_data"
              f"&resource_id={quote(resource_id, safe='')}"
              f"&principal_type={quote(principal_type, safe='')}"
              f"&principal_id={quote(str(principal), safe='')}"
              f"&role_id={quote(role_id, safe='')}")
        self.transport.request("DELETE", f"/apis/v1/role-bindings?{qs}", None)

    def list_user_data_acl(self, uid: str, subpath: str = "") -> list[dict]:
        """列举某用户数据资源上的全部角色绑定（ACL 条目）。

        subpath 非空时查 {storage_env}/{uid}/{subpath}；空（默认）时查 uid 级
        {storage_env}/{uid}。role-bindings 列表接口按 resource_id **精确匹配**
        （不支持前缀查询）：子路径授权是独立资源，须用其精确 subpath 单独
        查询，uid 级列举不会包含子路径上的绑定。

        返回 list[dict]，每个 dict 含 principal_type/principal_id/role_id 等字段。
        """
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        from urllib.parse import quote
        resource_id = self._user_data_acl_resource_id(uid, subpath)
        path = (f"/apis/v1/role-bindings?scope=resource"
                f"&resource_type=user_data"
                f"&resource_id={quote(resource_id, safe='')}")
        data = self.transport.get(path)
        # apiserver 可能返回列表或包在 data 里的 dict；统一归一化为 list。
        if isinstance(data, dict):
            return data.get("role_bindings", data.get("items", [data]))
        return list(data or [])

    def my_user_data_permissions(self, uid: str, subpath: str = "") -> list[str]:
        """返回当前用户对某用户数据资源（uid 级或子路径级）拥有的角色名列表。

        经 GET /apis/v1/me/resource-permissions 自查有效动作（get=读、use=写、
        assign=管 ACL），再映射回短名：assign→admin、use→writer、get→reader
        （取能力最高档）。目录主人恒为 admin（与服务端 owner 快路径语义一致）。

        历史实现走 GET /apis/v1/role-bindings 列表再客户端过滤，但该端点对非
        owner 调用方有 assign 门控，被授权者查自己 principal 恒得空列表，故改用
        /me/resource-permissions 自查端点。
        """
        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        from urllib.parse import quote
        # 先构造 resource_id：subpath 校验在任何网络请求之前完成（对称 Go/Java）。
        resource_id = self._user_data_acl_resource_id(uid, subpath)
        if str(uid).strip() == str(self.whoami()).strip():
            return ["admin"]
        path = (f"/apis/v1/me/resource-permissions?resource_type=user_data"
                f"&resource_id={quote(resource_id, safe='')}")
        data = self.transport.get(path)
        actions = data.get("actions", []) if isinstance(data, dict) else []
        if not actions:
            return []
        if "assign" in actions:
            return ["admin"]
        if "use" in actions:
            return ["writer"]
        if "get" in actions:
            return ["reader"]
        return []
