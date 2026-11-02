"""cli.py — irepo 命令行入口。

子命令：validate / push / push-many / deliver / list / get / pull / publish /
grant / feedback / report / create / claim / version / whoami / repo-config /
user-data / image。纯参数解析 + 分发到 Repo；便于单测（main(argv, repo=注入)）。

v0.8「三参数起步」：只需 ``INSTANCEREPO_TOKEN`` + ``--api-env``（或 ``IR_API_ENV``）
+ ``--storage-env``（或 ``IR_STORAGE_ENV``），数据面寻址由 SDK 自动向 apiserver 的
repo-config 拉取，无需再手配 ``IR_OSS_BUCKET`` / ``IR_ACR_HOST`` 等（后者已弃用）。

寻址统一约定：凡是要定位 dataset/version/instance 的子命令，都同时接受
**位置参数 ref**（如 ``{L1}/{L2}/{version}``）与 **flag 形式**
（``--dataset/--version/--instance-id``），二选一，同时给出即报错。
flag 形式与 push/push-many/deliver 的传参风格一致；位置 ref 保留为向后兼容的简写。
"""
from __future__ import annotations

import argparse
import json
import sys

from . import paths as P
from .concurrency import ItemError
from .errors import InstanceRepoError
from .models import DatasetSeries, Feedback, OwnerReference, RolloutReport
from .repo import Repo

_STATUS_CHOICES = ["draft", "published", "deprecated", "archived"]


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="irepo", description="InstanceRepo CLI")
    ap.add_argument("--profile", default="default",
                    help="数据面标签（仅作标签，不选择环境或地址）")
    ap.add_argument("--api-env", default=None,
                    help="下发的 Env 请求头值（服务端据此路由；亦可用 IR_API_ENV）")
    ap.add_argument("--api-base", default=None,
                    help="apiserver 根地址（亦可用 AP_BASE_URL；旧别名 "
                         "INSTANCEREPO_API_BASE 仍兼容）")
    ap.add_argument("--cluster", dest="global_cluster", default=None,
                    help="默认目标集群（亦可用 AP_CLUSTER）；deliver/repo-config 的"
                         "子命令级 --cluster 优先")
    ap.add_argument("--storage-env", dest="global_storage_env", default=None,
                    help="数据面存储环境（亦可用 IR_STORAGE_ENV）；SDK 据此自动向 "
                         "apiserver 的 repo-config 拉取 OSS/ACR 寻址并缓存")
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="本地校验 Instance 目录")
    v.add_argument("dir")

    p = sub.add_parser("push", help="上传 Instance（元数据先行）")
    p.add_argument("dir")
    p.add_argument("--dataset", required=True)
    p.add_argument("--version", default="",
                   help="版本号；split-first 可省略为空版本")
    p.add_argument("--owner-ref", required=True, help="OwnerReference JSON")
    p.add_argument("--split", default="default")
    p.add_argument("--no-image", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--no-register", action="store_true",
                   help="只传 OSS 不写库（默认上传后自动 ingest 写库；"
                        "置上则跳过 ingest，之后自行 ingest 扫描入库）")
    p.add_argument("--no-verify", action="store_true",
                   help="跳过上传后的回读校验（默认校验 OSS 对象/ACR 镜像确已落库）")

    pm = sub.add_parser("push-many",
                        help="并发上传一批 Instance（不入库；父目录用 shell 通配展开）")
    pm.add_argument("dirs", nargs="+",
                    help="实例路径，可给多个；整批父目录用通配展开，如 ./staging/*")
    pm.add_argument("--dataset", required=True, help="{L1}/{L2}")
    pm.add_argument("--version", default="",
                    help="版本号；split-first 可省略为空版本")
    pm.add_argument("--owner-ref", required=True, help="OwnerReference JSON（整批共用）")
    pm.add_argument("--split", default="default")
    pm.add_argument("--no-image", action="store_true")
    pm.add_argument("--overwrite", action="store_true")
    pm.add_argument("--register", action="store_true",
                    help="按成功实例ID分块ingest写库（缺省只传OSS，不写库）")
    pm.add_argument("--no-verify", action="store_true")
    pm.add_argument("--concurrency", type=int, default=8)
    pm.add_argument("--continue-on-error", action="store_true",
                    help="缺省任一失败即非零退出（已完成上传不回滚）；置上则逐项汇报")

    dl = sub.add_parser("deliver",
                        help="批量交付：并发上传 + 成功实例定向ingest")
    dl.add_argument("dirs", nargs="+",
                    help="实例路径，可给多个；整批父目录用通配展开，如 ./staging/*")
    dl.add_argument("--dataset", required=True, help="{L1}/{L2}")
    dl.add_argument("--version", default="",
                    help="版本号；split-first 可省略为空版本")
    dl.add_argument("--owner-ref", required=True, help="OwnerReference JSON（整批共用）")
    dl.add_argument("--split", default="default")
    dl.add_argument("--no-image", action="store_true")
    dl.add_argument("--overwrite", action="store_true")
    dl.add_argument("--concurrency", type=int, default=8)
    dl.add_argument("--continue-on-error", action="store_true",
                    help="缺省任一失败即非零退出（已完成上传不回滚）；"
                         "置上则只注册成功子集并逐项汇报失败")
    dl.add_argument("--no-ingest", action="store_true", help="只上传不入库")
    dl.add_argument("--publish", action="store_true",
                    help="ingest 完成后把 version 置 published")
    dl.add_argument("--cluster", dest="command_cluster", default=None,
                    help="运行时 cluster slug；优先于全局 --cluster，服务端据 repo-config "
                         "映射解析源数据面")

    lst = sub.add_parser("list", help="列出 dataset/version 下实例")
    lst.add_argument("ref", nargs="?",
                     help="{L1}/{L2}/{version}（或用 --dataset/--version）")
    lst.add_argument("--dataset", default=None, help="{L1}/{L2}")
    lst.add_argument("--version", default=None)
    lst.add_argument("--split", default=None,
                     help="按 split 过滤；缺省为跨 split 检索")
    # 1.0.10：分页/模糊搜索/过滤模式。任一给定 → 走 list_paged 单页语义；
    # 都没给时仍走 list 自动翻页取全量（向后兼容）。
    lst.add_argument("--q", default=None,
                     help="instance_id 子串模糊搜索（不区分大小写；给定即单页模式）")
    lst.add_argument("--instance-id", default=None, dest="instance_id",
                     help="instance_id 精确等值（给定即单页模式）")
    lst.add_argument("--tags", default=None,
                     help="k1:v1,k2:v2 等值过滤（key 含 ./$ 服务端拒绝；给定即单页模式）")
    lst.add_argument("--difficulty", choices=["easy", "medium", "hard"], default=None,
                     help="按难度过滤（给定即单页模式）")
    lst.add_argument("--page", type=int, default=1,
                     help="分页页码（默认 1；与 --q/--tags/--difficulty 配合生效）")
    lst.add_argument("--page-size", type=int, default=50, dest="page_size",
                     help="分页大小（默认 50；服务端上限 200）")

    pl = sub.add_parser("pull", help="拉取并解包（digest 校验）")
    pl.add_argument("ref", nargs="?",
                    help="{L1}/{L2}/{version}/{id}（或用 --dataset/--version/--instance-id）")
    pl.add_argument("--dataset", default=None, help="{L1}/{L2}")
    pl.add_argument("--version", default=None)
    pl.add_argument("--instance-id", default=None)
    pl.add_argument("-o", "--out", default="./work")
    pl.add_argument("--split", default="default",
                    help="实例所在 split（写入时用了非默认 split 就必须带上）")

    pub = sub.add_parser("publish", help="发布到运行时配置的目标数据面（benchmark-release）")
    pub.add_argument("ref", nargs="?",
                     help="{L1}/{L2}/{version}；split_first 无版本 split 发布用 {L1}/{L2}"
                          "（或用 --dataset/--version[--split]）")
    pub.add_argument("--dataset", default=None, help="{L1}/{L2}")
    pub.add_argument("--version", default=None,
                     help="版本号；split_first 的 split 发布可省略（省略时必须给 --split）")
    pub.add_argument("--instances", default=None,
                     help="逗号分隔的 KEEP 实例 id；granularity=instance 或 images=on 时必填")
    pub.add_argument("--target", default="",
                     help="目标标签（不解析寻址）；目标地址须用 --target-* 显式提供；"
                          "repo-config 输出不会被 CLI 自动应用")
    pub.add_argument("--target-bucket", default=None,
                     help="运行时目标 OSS bucket（可将显式 repo-config 查询结果手工填入）")
    pub.add_argument("--target-acr", default=None, help="目标 ACR host（images=on 时用）")
    pub.add_argument("--target-acr-namespace", default=None, help="目标 ACR namespace")
    pub.add_argument("--split", default="",
                     help="**必须与 push 时一致**：instance 粒度按 split 拼源路径，"
                          "split_first 下镜像 tag 也用 split；传错会让上架 validate 报 "
                          "source_path does not exist")
    pub.add_argument("--granularity", choices=["dataset", "instance"], default="dataset")
    pub.add_argument("--images", choices=["off", "on"], default="off")
    pub.add_argument("--overwrite", action="store_true")
    pub.add_argument("--wait-approval", action="store_true", help="等待人工审批直到终态")
    pub.add_argument("--description", default="")
    pub.add_argument("--request-json", default=None,
                     help="逃生舱：直接透传 workflow 请求体 JSON 文件（给定时忽略上面 typed 参数）")

    # ── 独立镜像能力（v0.8 新增）：不依赖实例目录 ──────────────────────────────
    img = sub.add_parser("image", help="独立镜像操作：push/pull/copy/exists/ref")
    isub = img.add_subparsers(dest="image_cmd", required=True)

    iref = isub.add_parser("ref", help="按当前元数据模型算某实例的 ACR 引用")
    iref.add_argument("--dataset", required=True, help="{L1}/{L2}")
    iref.add_argument("--instance-id", required=True)
    iref.add_argument("--split", default=None, help="split-first 正常业务下必填")
    iref.add_argument("--version", default=None, help="可选版本号")
    iref.add_argument("--acr-host", default=None, help="缺省取自动发现结果")
    iref.add_argument("--acr-namespace", default=None, help="缺省取自动发现结果")

    ipush = isub.add_parser("push", help="本地 docker-archive tar → registry")
    ipush.add_argument("tar", help="docker-archive tar 路径")
    ipush.add_argument("ref", help="目标镜像引用 {host}/{ns}/{repo}:{tag}")
    ipush.add_argument("--overwrite", action="store_true",
                       help="目标已存在时覆盖（缺省跳过：tag 承载实例身份，重复推可疑）")

    ipull = isub.add_parser("pull", help="registry → 本地 docker-archive tar（仅私网）")
    ipull.add_argument("ref", help="源镜像引用")
    ipull.add_argument("tar", help="输出 docker-archive tar 路径")
    ipull.add_argument("--overwrite", action="store_true", help="覆盖已存在的 tar")

    icopy = isub.add_parser("copy", help="registry → registry（源以 digest 固定）")
    icopy.add_argument("src", help="源镜像引用")
    icopy.add_argument("dst", help="目标镜像引用")
    icopy.add_argument("--overwrite", action="store_true")

    iex = isub.add_parser("exists", help="存在性探测（退出码 0=存在，1=不存在）")
    iex.add_argument("ref", help="镜像引用")
    iex.add_argument("--retries", type=int, default=0,
                     help="一致性重试次数（刚推完立即探测可能假 False，建议 3）")

    g = sub.add_parser("grant", help="授权")
    # 位置参数 dest 用 ref：argparse 的位置参数与同名 option 会共享 dest 相互覆盖，必须错开。
    g.add_argument("ref", nargs="?", metavar="dataset",
                   help="{L1}/{L2}（或用 --dataset）")
    g.add_argument("--dataset", default=None, help="{L1}/{L2}")
    g.add_argument("--user", required=True)
    g.add_argument("--role", required=True)

    fb = sub.add_parser("feedback", help="回写反馈（append）")
    fb.add_argument("ref", nargs="?",
                    help="{L1}/{L2}/{version}/{id}（或用 --dataset/--version/--instance-id）")
    fb.add_argument("--dataset", default=None, help="{L1}/{L2}")
    fb.add_argument("--version", default=None)
    fb.add_argument("--instance-id", default=None,
                    help="目标实例 id（与下面的 --id 不同：--id 是反馈来源 id）")
    fb.add_argument("--type", required=True)
    fb.add_argument("--id", required=True)
    fb.add_argument("--score", type=float, required=True)
    fb.add_argument("--message", default="")

    rp = sub.add_parser("report", help="质检 report 存取（OSS）")
    rp.add_argument("action", choices=["get", "put", "assemble"])
    rp.add_argument("ref", nargs="?",
                    help="get/put: {L1}/{L2}/{version}/{id}；assemble: {L1}/{L2}/{version}"
                         "（或用 --dataset/--version[/--instance-id]）")
    rp.add_argument("--dataset", default=None, help="{L1}/{L2}")
    rp.add_argument("--version", default=None)
    rp.add_argument("--instance-id", default=None, help="get/put 用")
    rp.add_argument("--file", default=None, help="put: 输入 report.jsonl；get: 输出(缺省打印)；assemble: 输出 jsonl")
    rp.add_argument("--instances", default=None, help="assemble: 逗号分隔的实例 id")
    rp.add_argument("--overwrite", action="store_true")

    sub.add_parser("whoami", help="打印当前 apikey 对应的工号(user_id)")

    rc = sub.add_parser(
        "repo-config",
        help="查看某 cluster/storage-env 的数据面寻址（诊断用；日常无需手工套用——"
             "全局 --storage-env 会让 SDK 自动应用同样的结果）")
    rc.add_argument("--cluster", dest="command_cluster", default=None,
                    help="执行集群名（优先于全局 --cluster，并优先于 --storage-env）")
    rc.add_argument("--storage-env", default="", help="运行时存储环境标识（由部署配置定义）")
    rc.add_argument("--map", action="store_true",
                    help="改为打印 cluster→storage_env 映射表(忽略 --cluster/--storage-env)")

    ud = sub.add_parser("user-data", help="用户输入数据(插件/合成输入) put/get/ls")
    ud.add_argument("action", choices=["put", "get", "ls"])
    ud.add_argument("pos", nargs="*",
                    help="put: <local> <remote>；get: <remote> <local>；ls: [subpath]")
    ud.add_argument("--uid", default=None,
                    help="目标 uid（缺省=自己 whoami；系统白名单读他人时指定）")
    ud.add_argument("--overwrite", action="store_true", help="put 时覆盖已存在对象")

    cr = sub.add_parser("create", help="创建 DatasetSeries")
    cr.add_argument("ref", nargs="?", metavar="dataset",
                    help="{L1}/{L2}（或用 --dataset）")
    cr.add_argument("--dataset", default=None, help="{L1}/{L2}")
    cr.add_argument("--benchmark-id", default=None,
                    help="绑定的 benchmark source_id（默认必填；apiserver 据它派生 teacher）。"
                         "建议使用标准化 benchmark id；如果没有，可以填入 default")
    cr.add_argument("--visibility", choices=["public", "private"], default="private")
    cr.add_argument("--display-name", default=None)
    cr.add_argument("--description", default=None)
    cr.add_argument("--default-scaffold", default=None)
    cr.add_argument("--owner", default=None, help="归属人工号（缺省取调用方）")
    cr.add_argument("--owner-team-id", default=None)
    cr.add_argument("--workspace-id", default=None, help="归属 workspace/queue（可选）")
    cr.add_argument("--no-require-benchmark", action="store_true",
                    help="跳过 benchmark_id 本地必填校验（仅服务端关掉强制绑定时用）")

    cl = sub.add_parser("claim", help="认领 dataset（成为 admin）")
    cl.add_argument("dataset_id", help="dataset 业务 ID（ds- 前缀）")
    cl.add_argument("--workspace-id", required=True, help="归属 workspace/queue ID")
    cl.add_argument("--benchmark-id", default=None,
                    help="绑定的 benchmark source_id（默认必填；apiserver 据它派生 teacher）。"
                         "建议使用标准化 benchmark id；如果没有，可以填入 default")
    cl.add_argument("--owner", default=None,
                    help="归属人工号（缺省取调用方；已有非空 owner 不会被覆盖）")
    cl.add_argument("--no-require-benchmark", action="store_true",
                    help="跳过 benchmark_id 本地必填校验（仅服务端关掉强制绑定时用）")

    gt = sub.add_parser("get", help="取单个实例元数据")
    gt.add_argument("ref", nargs="?",
                    help="{L1}/{L2}/{version}/{id}（或用 --dataset/--version/--instance-id）")
    gt.add_argument("--dataset", default=None, help="{L1}/{L2}")
    gt.add_argument("--version", default=None)
    gt.add_argument("--instance-id", default=None)
    gt.add_argument("--split", default=None,
                    help="实例所在 split；缺省为跨 split 检索")

    ver = sub.add_parser("version", help="版本管理（create/list/status/update/set-run-type/ingest）")
    ver.add_argument("action",
                     choices=["create", "list", "status", "update",
                              "set-run-type", "get", "ingest"])
    ver.add_argument("ref", nargs="?",
                     help="create/list/ingest: {L1}/{L2}；"
                          "status/update/set-run-type: {L1}/{L2}/{version}"
                          "（或用 --dataset[/--version]）")
    ver.add_argument("--dataset", default=None, help="{L1}/{L2}")
    ver.add_argument("--version", default=None,
                     help="create/ingest: 要处理的版本号（split_first 可省略）；"
                          "status/update/set-run-type: 目标版本（寻址用）")
    ver.add_argument("--storage-path", default=None,
                     help="create 用：oss://{bucket}/{prefix}")
    ver.add_argument("--storage-type", choices=["oss"], default="oss")
    ver.add_argument("--splits", default=None,
                     help="逗号分隔 split 名（create/ingest 用；ingest 与 --split 互斥）")
    ver.add_argument("--split", default=None,
                     help="status 用：查 split 级真实记录；"
                          "ingest 用：只 ingest 该 split（与 --splits 互斥）——"
                          "version 下 split 很多时强烈建议传，避免全量扫描拖垮事务")
    ver.add_argument("--status", choices=_STATUS_CHOICES, default=None,
                     help="update 用：版本状态流转")
    ver.add_argument("--run-type", choices=["train", "eval"], default=None,
                     help="version 级用途标签")
    ver.add_argument("--split-run-types", default=None,
                     help="split 级打标，格式 name=train,name2=eval（与 --run-type 互斥）")
    ver.add_argument("--environment", default=None,
                     help="create/get/ingest 用：覆盖 profile 派生的 environment（pre/online）")
    ver.add_argument("--instance-id", action="append", default=None,
                     dest="instance_ids",
                     help="ingest用：定向注册实例ID；可重复，也可逗号分隔")
    ver.add_argument("--dry-run", action="store_true",
                     help="ingest 用：只预览扫描结果不落库")
    ver.add_argument("--publish", action="store_true",
                     help="ingest 用：完成后把 version 置 published")
    ver.add_argument("--no-wait", action="store_true",
                     help="ingest 用：立即返回 job 不轮询终态")
    ver.add_argument("--poll-sec", type=float, default=5.0, dest="poll_sec",
                     help="ingest 用：轮询间隔（秒）")
    ver.add_argument("--timeout", type=float, default=1800.0, dest="timeout_sec",
                     help="ingest 用：轮询超时（秒）")
    ver.add_argument("--allow-layout-inference", action="store_true",
                     help="ingest 用：放弃「split_first 无 version 必须给 splits」"
                          "前置检查，交给服务端推断布局")
    ver.add_argument("--cluster", default=None,
                     help="ingest 用：运行时 cluster slug（覆盖 profile）")

    # ── 1.0.10 控制面管理子命令 ─────────────────────────────────────────────────
    sp = sub.add_parser("split", help="split 记录管理（list/get/create/set-run-type）")
    sp.add_argument("action", choices=["list", "get", "create", "set-run-type"])
    sp.add_argument("ref", nargs="?",
                    help="list: {L1}/{L2}；get/set-run-type: {L1}/{L2}/{split}；"
                         "create: {L1}/{L2}/{split}（或用 --dataset/--split）")
    sp.add_argument("--dataset", default=None, help="{L1}/{L2}")
    sp.add_argument("--split", default=None,
                    help="目标 split 名（get/set-run-type 用）")
    sp.add_argument("--version", default=None,
                    help="list 按 version 精确过滤；get/create 可选定位版本")
    sp.add_argument("--scope", choices=["unversioned", "exact", "all"], default=None,
                    help="list 跨版本策略：缺省无 version → all（SDK 取全量哲学），"
                         "有 version 省略（服务端只接受 exact）")
    sp.add_argument("--status", choices=_STATUS_CHOICES, default=None,
                    help="list 按状态过滤")
    sp.add_argument("--run-type", choices=["train", "eval", ""], default=None,
                    dest="run_type",
                    help="set-run-type/create 用：train/eval 或空串清除")
    sp.add_argument("--storage-path", default=None, dest="storage_path",
                    help="create 的 1.2.1 兼容参数；非空值会被拒绝，路径由服务端推导")
    sp.add_argument("--page", type=int, default=1)
    sp.add_argument("--page-size", type=int, default=50, dest="page_size")
    sp.add_argument("--environment", default=None,
                    help="create 覆盖 profile 派生的 environment（pre/online）")

    ds = sub.add_parser("dataset",
                        help="数据集/基准/工作流管理（list/get/update/access/"
                             "revoke/benchmarks/workflows）")
    ds.add_argument("action",
                    choices=["list", "get", "update", "access", "revoke",
                             "benchmarks", "workflows"])
    ds.add_argument("ref", nargs="?", metavar="dataset",
                    help="list/get/update/access/revoke: {L1}/{L2}；"
                         "benchmarks: source_id（get）；workflows: wf-id（get）")
    ds.add_argument("--dataset", default=None, help="{L1}/{L2}")
    ds.add_argument("--q", default=None,
                    help="list/benchmarks 模糊搜索；list 对 name+display_name，"
                         "benchmarks 对 name")
    ds.add_argument("--status", default=None,
                    help="list/benchmarks 过滤；workflows 过滤"
                         "（pending/running/awaiting_approval/succeeded/failed/canceled）")
    ds.add_argument("--visibility", default=None,
                    help="list 逗号分隔过滤（public/private）")
    ds.add_argument("--owned-by-me", action="store_true", dest="owned_by_me",
                    help="list 按 owner=caller 过滤")
    ds.add_argument("--sort-by", choices=["updated_at", "dataset_name"],
                    default=None, dest="sort_by")
    ds.add_argument("--order", choices=["asc", "desc"], default=None)
    ds.add_argument("--include-deprecated", action="store_true",
                    dest="include_deprecated")
    ds.add_argument("--environment", default=None,
                    help="get/update 覆盖 profile 派生的 environment")
    # update 用（至少一项）
    ds.add_argument("--display-name", default=None, dest="display_name")
    ds.add_argument("--description", default=None)
    ds.add_argument("--benchmark-id", default=None, dest="benchmark_id")
    ds.add_argument("--owner-team-id", default=None, dest="owner_team_id")
    ds.add_argument("--default-scaffold", default=None, dest="default_scaffold")
    # access/revoke 用
    ds.add_argument("--principal", default=None, help="工号或 user_group id")
    ds.add_argument("--role", choices=["reader", "writer", "admin"], default=None)
    ds.add_argument("--principal-type", choices=["user", "user_group"],
                    default="user", dest="principal_type")
    # benchmarks/workflows 用
    ds.add_argument("--is-core", action="store_true", dest="is_core")
    ds.add_argument("--source", default=None, help="benchmarks source 精确过滤")
    ds.add_argument("--kind", default=None, help="workflows kind 过滤")
    ds.add_argument("--creator", default=None, help="workflows creator 过滤")
    ds.add_argument("--page", type=int, default=1)
    ds.add_argument("--page-size", type=int, default=20, dest="page_size")

    # ── Artifact 下载（STS 直连 OSS，workspace ACL 鉴权）──
    art = sub.add_parser("artifact",
                         help="AP job artifact 下载（AP HTTP 链接）")
    asub = art.add_subparsers(dest="artifact_cmd", required=True)

    adl = asub.add_parser("download", help="下载单个 job 的 artifact")
    adl.add_argument("--job-id", required=True, help="AP job ID")
    adl.add_argument("--cluster", default=None,
                     help="数据面名（缺省取 SDK profile 绑定的 cluster）")
    adl.add_argument("--output-dir", default=".", dest="output_dir",
                     help="本地输出目录")
    adl.add_argument("--ap-endpoint", default=None, dest="ap_endpoint",
                     help="AP 控制面 URL（可选）")

    adlm = asub.add_parser("download-many", help="批量下载多个 job 的 artifact")
    adlm.add_argument("--job-ids", required=True, dest="job_ids",
                      help="逗号分隔的 job ID 列表")
    adlm.add_argument("--cluster", default=None)
    adlm.add_argument("--output-dir", default=".", dest="output_dir")
    adlm.add_argument("--concurrent", type=int, default=8,
                      help="最大并发下载数（默认 8）")
    adlm.add_argument("--ap-endpoint", default=None, dest="ap_endpoint")

    adlg = asub.add_parser("download-group",
                           help="下载某 group 下全部 job 的 artifact")
    adlg.add_argument("--group-id", required=True, dest="group_id",
                      help="AP group ID")
    adlg.add_argument("--cluster", default=None)
    adlg.add_argument("--output-dir", default=".", dest="output_dir")
    adlg.add_argument("--concurrent", type=int, default=8)
    adlg.add_argument("--ap-endpoint", default=None, dest="ap_endpoint")

    for artifact_parser in (adl, adlm, adlg):
        artifact_parser.add_argument(
            "--include-files", action="append", default=None,
            help="Only download matching artifact files or folders (repeatable; comma-separated)")
        artifact_parser.add_argument(
            "--exclude-files", action="append", default=None,
            help="Skip matching artifact files or folders (repeatable; comma-separated)")
        artifact_parser.add_argument("--extract", action="store_true",
                                     help="Extract the complete archive (default: keep archive only)")

    return ap


def _split_ref(ref: str, parts: int) -> list[str]:
    segs = ref.split("/")
    if len(segs) != parts:
        raise SystemExit(f"ref must have {parts} segments, got {ref!r}")
    return segs


def _page_count(res) -> int:
    """分页结果的总页数（total<0 表示服务端无分页信封 → 1）。"""
    if getattr(res, "total", -1) < 0 or not getattr(res, "page_size", 0):
        return 1
    return max(1, (res.total + res.page_size - 1) // res.page_size)


def _split_instance_count(split) -> int:
    """取 split 的实例计数：优先 manifest.instance_count，回落 0。"""
    m = getattr(split, "manifest", None)
    if m is not None:
        c = getattr(m, "instance_count", None)
        if isinstance(c, int):
            return c
    return 0


def _resolve_split_ref(args) -> tuple[str, str]:
    """定位 dataset + split：位置 ref（{L1}/{L2}/{split}）或 --dataset/--split。"""
    if args.dataset:
        if not args.split:
            raise SystemExit("给定 --dataset 时 split 需要 --split")
        return args.dataset, args.split
    if args.ref:
        segs = _split_ref(args.ref, 3)
        return f"{segs[0]}/{segs[1]}", segs[2]
    raise SystemExit("split get/create/set-run-type 需要 {L1}/{L2}/{split} 或 "
                     "--dataset/--split")


def _split_dataset(dataset: str) -> tuple[str, str]:
    """校验 ``--dataset`` 并返回模型回显所需的 ``(L1, L2)``。"""
    try:
        name = P.DatasetName.parse(dataset)
    except InstanceRepoError as exc:
        raise SystemExit(
            f"--dataset must be one or two canonical segments, got "
            f"{dataset!r}") from exc
    return name.l1, name.l2


_TARGET_SHAPE = {
    2: ("{L1}/{L2}", "--dataset"),
    3: ("{L1}/{L2}/{version}", "--dataset --version"),
    4: ("{L1}/{L2}/{version}/{id}", "--dataset --version --instance-id"),
}


def _resolve_target(args, parts: int) -> tuple[str, str | None, str | None]:
    """统一寻址：位置参数 ``ref`` 与 ``--dataset/--version/--instance-id`` 二选一。

    返回 ``(dataset, version, instance_id)``；``version``/``instance_id`` 仅在
    ``parts`` 覆盖到时才有值，否则为 None。

    两种形式同时给出即报错，不做"某一方优先"的静默取舍——静默偏向任一方会把
    "我明明传了却没生效"变成极难自查的问题。

    ``parts`` 决定考察哪些 flag（2 只看 dataset，3 加 version，4 再加 instance-id），
    因此 ``version create/list``（parts=2）不会把用作"新版本号"的 ``--version``
    误判成寻址 flag。
    """
    shape, flag_hint = _TARGET_SHAPE[parts]
    ref = getattr(args, "ref", None)
    dataset = getattr(args, "dataset", None)
    version = getattr(args, "version", None) if parts >= 3 else None
    iid = getattr(args, "instance_id", None) if parts >= 4 else None

    given = [n for n, v in (("--dataset", dataset), ("--version", version),
                            ("--instance-id", iid)) if v]
    if ref and given:
        raise SystemExit(
            f"位置参数 ref 与 {' / '.join(given)} 二选一，不能同时给出"
            f"（ref={ref!r}）")
    if ref:
        segs = _split_ref(ref, parts)
        return ("/".join(segs[:2]),
                segs[2] if parts >= 3 else None,
                segs[3] if parts >= 4 else None)
    if not given:
        raise SystemExit(
            f"需要位置参数 ref（{shape}）或 flag 形式（{flag_hint}）")
    missing = [n for n, v in (("--dataset", dataset),
                              ("--version", version if parts >= 3 else "-"),
                              ("--instance-id", iid if parts >= 4 else "-"))
               if not v]
    if missing:
        raise SystemExit(
            f"flag 形式缺少 {' '.join(missing)}（或改用位置参数 ref：{shape}）")
    _split_dataset(dataset)
    return (dataset, version, iid)


def _parse_split_run_types(s: str) -> list[dict]:
    """解析 CLI 的 ``name=train,name2=eval`` 格式为 [{name, run_type}] 列表。

    run_type 合法性交由 SDK versions.update 校验（会列出合法值）。"""
    out: list[dict] = []
    for pair in s.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise SystemExit(
                f"--split-run-types 每项须为 name=run_type，got {pair!r}")
        name, rt = pair.split("=", 1)
        out.append({"name": name.strip(), "run_type": rt.strip()})
    return out


_OVERFLOW_POSITIONAL = {"report": "ref", "version": "ref", "user-data": "pos"}


def _parse_args(argv):
    """解析 argv，并修补 argparse 对「必填位置参数 + 可选位置参数」的贪婪匹配缺陷。

    CPython 3.12 之前，这种形状中间夹 option 会解析失败：可选位置参数在第一个
    位置参数组里被匹配成 0 个并从待匹配列表移除，真正的值落进 extras，报
    ``unrecognized arguments``。实测 3.11 下 ``report put --file r.jsonl REF``
    与 ``version set-run-type --run-type train REF`` 都会失败，而 3.12+ 正常
    （CPython 在 ``_match_arguments_partial`` 加了丢弃尾部零匹配的保护）。
    本项目 ``requires-python = ">=3.10"``，故必须自行兜住。

    改用 ``parse_known_args``：option 的取值 argparse 已正确消费（``--f v``、
    ``--f=v``、``store_true`` 均验证过），extras 里剩下的非 flag token 恰好就是
    被饿死的位置参数，回填到该子命令的溢出 dest 即可。未知 flag 仍按原样报错，
    不会被静默吞掉。

    只有 ``report`` / ``version`` / ``user-data`` 是这个形状（action + 可选 ref）；
    其余子命令最多一个位置参数，不受影响，此处也不会改变它们的行为。
    """
    parser = build_parser()
    args, extras = parser.parse_known_args(argv)
    if not extras:
        return args
    # 未知 flag：维持 argparse 的报错口径，不当成位置参数回填
    if any(e.startswith("-") and e != "-" for e in extras):
        raise SystemExit(f"unrecognized arguments: {' '.join(extras)}")
    dest = _OVERFLOW_POSITIONAL.get(getattr(args, "cmd", None))
    if dest is None:
        raise SystemExit(f"unrecognized arguments: {' '.join(extras)}")
    current = getattr(args, dest, None)
    if isinstance(current, list):
        setattr(args, dest, current + extras)
        return args
    if current:                      # argparse 已填上该位置参数，又多出别的
        raise SystemExit(f"unrecognized arguments: {' '.join(extras)}")
    if len(extras) > 1:
        raise SystemExit(f"unrecognized arguments: {' '.join(extras[1:])}")
    setattr(args, dest, extras[0])
    return args


def _effective_cluster(args) -> str | None:
    """子命令级兼容 flag 优先，否则使用全局 cluster。"""
    return (getattr(args, "command_cluster", None)
            or getattr(args, "global_cluster", None))


def main(argv=None, *, repo: Repo | None = None, out=None) -> int:
    args = _parse_args(argv)
    out = out or sys.stdout
    if args.cmd == "artifact":
        for name in ("include_files", "exclude_files"):
            raw = getattr(args, name)
            values = list(dict.fromkeys(v.strip() for item in (raw or [])
                                        for v in item.split(",") if v.strip()))
            if raw is not None and not values:
                raise InstanceRepoError(f"--{name.replace('_', '-')} 至少需要一个非空的文件或目录选择器")
            setattr(args, name, values or None)
        if args.extract and (args.include_files or args.exclude_files):
            raise InstanceRepoError("--extract 不能与 --include-files 或 --exclude-files 同时使用")
    cluster = _effective_cluster(args)
    r = repo or Repo(profile=args.profile, api_env=getattr(args, "api_env", None),
                     api_base=getattr(args, "api_base", None), cluster=cluster,
                     storage_env=getattr(args, "global_storage_env", None))

    if args.cmd == "validate":
        rep = r.instances.validate(args.dir)
        print(f"OK {rep.instance_id} (metadata keys: {sorted(rep.metadata)})", file=out)
        return 0

    if args.cmd == "push":
        owner = OwnerReference.from_json(args.owner_ref)
        res = r.instances.push(args.dir, args.dataset, args.version,
                               owner_reference=owner, split=args.split,
                               push_image=not args.no_image,
                               overwrite=args.overwrite,
                               register=not args.no_register,
                               verify=not args.no_verify)
        print(f"{res.instance_id} uploaded={res.uploaded} "
              f"image_pushed={res.image_pushed}", file=out)
        if res.ingest:
            stats = res.ingest.get("stats", {}) or {}
            print(f"ingest {res.ingest.get('ingest_id')} "
                  f"status={res.ingest.get('status')} "
                  f"instances={stats.get('instance_count')}", file=out)
        if not args.no_register:
            status = ((res.ingest or {}).get("status") or "").lower()
            return 0 if status == "completed" else 1
        return 0

    if args.cmd == "push-many":
        if args.concurrency < 1:
            raise SystemExit("--concurrency 必须 >= 1")
        owner = OwnerReference.from_json(args.owner_ref)
        results = r.instances.push_many(
            args.dirs, args.dataset, args.version,
            owner_reference=owner, split=args.split,
            push_image=not args.no_image, overwrite=args.overwrite,
            register=args.register, verify=not args.no_verify,
            concurrency=args.concurrency,
            continue_on_error=args.continue_on_error)
        failed = 0
        for d, res in zip(args.dirs, results):
            if isinstance(res, Exception):   # continue_on_error 下的 ItemError 占位
                failed += 1
                # 不直接打印 ItemError 的字符串：两套 SDK 的包装文案不同
                # （Python "item 'x' failed: ..." vs Go "item[0] x failed: ..."），
                # 直接打印会让两侧输出无法用同一脚本解析。取底层错误自行拼三列。
                print(f"FAILED\t{d}\t{getattr(res, 'error', res)}", file=out)
            else:
                print(f"{res.instance_id}\tuploaded={res.uploaded}\t"
                      f"image_pushed={res.image_pushed}", file=out)
        unfinished_registration = (
            args.register and any(
                not isinstance(res, Exception)
                and ((res.ingest or {}).get("status") or "").lower()
                != "completed"
                for res in results))
        print(f"pushed={len(results) - failed} failed={failed}", file=out)
        return 1 if failed or unfinished_registration else 0

    if args.cmd == "deliver":
        if args.concurrency < 1:
            raise SystemExit("--concurrency 必须 >= 1")
        owner = OwnerReference.from_json(args.owner_ref)
        res = r.deliver(args.dataset, args.version, args.dirs,
                        owner_reference=owner, split=args.split,
                        push_image=not args.no_image,
                        overwrite=args.overwrite,
                        concurrency=args.concurrency,
                        continue_on_error=args.continue_on_error,
                        ingest=not args.no_ingest,
                        publish=args.publish,
                        cluster=cluster)
        for e in res["failed"]:
            print(f"FAILED\t{getattr(e, 'item', '?')}\t{getattr(e, 'error', e)}",
                  file=out)
        job = res.get("ingest") or {}
        registration = res.get("registration")
        pending = len(getattr(registration, "pending", []))
        reg_failed = len(getattr(registration, "failed", []))
        unknown = len(getattr(registration, "unknown", []))
        not_submitted = len(getattr(registration, "not_submitted", []))
        print(f"pushed={len(res['pushed'])} failed={len(res['failed'])} "
              f"skipped={len(res.get('skipped', []))} jobs={len(res.get('ingests', []))} "
              f"ingest={job.get('ingest_id', '-')} status={job.get('status', '-')} "
              f"pending={pending} registration_failed={reg_failed} "
              f"unknown={unknown} not_submitted={not_submitted}", file=out)
        unfinished = (res["failed"] or pending or reg_failed
                      or unknown or not_submitted)
        return 1 if unfinished else 0

    if args.cmd == "list":
        dataset, version, _ = _resolve_target(args, 3)
        # 1.0.10：任一过滤/分页 flag 给定 → 走 list_paged 单页；否则仍走
        # list 自动翻页取全量（向后兼容）。
        paged = any([args.q, args.instance_id, args.tags, args.difficulty,
                     args.page != 1, args.page_size != 50])
        if paged:
            tags_dict = None
            if args.tags:
                tags_dict = {}
                for pair in args.tags.split(","):
                    if ":" not in pair:
                        raise SystemExit(f"--tags expects k1:v1,k2:v2, got {args.tags!r}")
                    k, v = pair.split(":", 1)
                    tags_dict[k] = v
            res = r.instances.list_paged(dataset, args.version, split=args.split,
                                         q=args.q, instance_id=args.instance_id,
                                         tags=tags_dict, difficulty=args.difficulty,
                                         page=args.page, page_size=args.page_size)
            for inst in res.items:
                src = "\t[oss]" if not inst.registered else ""
                print(f"{inst.instance_id}\t{inst.difficulty}\t{inst.docker_image}{src}",
                      file=out)
            print(f"page={res.page}/{(res.total+res.page_size-1)//res.page_size if res.total>0 else 1} "
                  f"total={res.total} has_more={res.has_more}", file=out)
            return 0
        for inst in r.instances.list(dataset, version, args.split):
            src = "\t[oss]" if not inst.registered else ""
            print(f"{inst.instance_id}\t{inst.difficulty}\t{inst.docker_image}{src}",
                  file=out)
        return 0

    if args.cmd == "pull":
        dataset, version, iid = _resolve_target(args, 4)
        path = r.instances.pull(dataset, version, iid, args.out,
                                split=args.split)
        print(str(path), file=out)
        return 0

    if args.cmd == "publish":
        # split-first 的 split 发布：给了 --split 且没给 version 时允许只寻址 dataset
        # （{L1}/{L2} 或 --dataset），version 置空走 dataset_distributions 协议。
        need_version = not (args.split and not args.version)
        dataset, version, _ = _resolve_target(args, 3 if need_version else 2)
        if args.request_json:
            with open(args.request_json, encoding="utf-8") as f:
                body = json.load(f)
            wf = r.versions.publish(dataset, version or "", request_body=body,
                                    wait_approval=args.wait_approval)
        else:
            insts = ([s.strip() for s in args.instances.split(",") if s.strip()]
                     if args.instances else None)
            # 目标数据面配置由 CLI 显式提供（SDK 不内置任何环境的桶/仓地址）。
            tgt_ovr = {}
            if args.target_bucket:
                tgt_ovr["oss_bucket"] = args.target_bucket
            if args.target_acr:
                tgt_ovr["acr_host"] = args.target_acr
            if args.target_acr_namespace:
                tgt_ovr["acr_namespace"] = args.target_acr_namespace
            wf = r.versions.publish(
                dataset, version or "", instances=insts, target=args.target,
                target_overrides=(tgt_ovr or None),
                granularity=args.granularity, images=args.images,
                overwrite=args.overwrite, wait_approval=args.wait_approval,
                split=args.split, description=args.description)
        print(f"workflow {wf.get('id','')} status={wf.get('status','')}", file=out)
        return 0

    if args.cmd == "image":
        if args.image_cmd == "ref":
            print(r.images.ref_for(
                args.dataset, args.instance_id, split=args.split,
                version=args.version, acr_host=args.acr_host,
                namespace=args.acr_namespace), file=out)
            return 0
        if args.image_cmd == "push":
            print(r.images.push(args.tar, args.ref,
                                overwrite=args.overwrite), file=out)
            return 0
        if args.image_cmd == "pull":
            # 返回 digest 固定引用：tag 可能已被覆盖，digest 才能复现同一份字节
            print(r.images.pull(args.ref, args.tar,
                                overwrite=args.overwrite), file=out)
            return 0
        if args.image_cmd == "copy":
            print(r.images.copy(args.src, args.dst,
                                overwrite=args.overwrite), file=out)
            return 0
        if args.image_cmd == "exists":
            found = r.images.exists(args.ref, retries=args.retries)
            print("present" if found else "absent", file=out)
            return 0 if found else 1

    if args.cmd == "whoami":
        print(r.whoami(), file=out)
        return 0

    if args.cmd == "repo-config":
        if args.map:
            print(json.dumps(r.get_cluster_storage_env_map(), ensure_ascii=False, indent=2), file=out)
        else:
            if not cluster and not args.storage_env:
                raise SystemExit("repo-config 需要 --cluster 或 --storage-env（或用 --map）")
            cfg = r.get_repo_config(cluster=cluster or "", storage_env=args.storage_env)
            print(json.dumps(cfg, ensure_ascii=False, indent=2), file=out)
        return 0

    if args.cmd == "user-data":
        uid = args.uid or r.whoami()
        if args.action == "put":
            if len(args.pos) < 2:
                raise SystemExit("user-data put 需要 <local> <remote>")
            res = r.upload_user_data(uid, args.pos[0], args.pos[1],
                                     overwrite=args.overwrite)
            tag = "skipped (exists): " if res.get("skipped") else "put: "
            print(tag + res.get("key", ""), file=out)
            return 0
        if args.action == "get":
            if len(args.pos) < 2:
                raise SystemExit("user-data get 需要 <remote> <local>")
            path = r.download_user_data(uid, args.pos[0], args.pos[1])
            print(f"got: {path}", file=out)
            return 0
        # ls
        subpath = args.pos[0] if args.pos else ""
        for k in r.list_user_data(uid, subpath):
            print(k, file=out)
        return 0

    if args.cmd == "grant":
        dataset, _, _ = _resolve_target(args, 2)
        r.datasets.grant(dataset, args.user, args.role)
        print(f"granted {args.role} to {args.user} on {dataset}", file=out)
        return 0

    if args.cmd == "report":
        if args.action == "assemble":
            dataset, version, _ = _resolve_target(args, 3)
            insts = [s.strip() for s in (args.instances or "").split(",") if s.strip()]
            dest = args.file or "train.jsonl"
            path = r.reports.assemble_jsonl(dataset, version, insts, dest)
            print(str(path), file=out)
            return 0
        dataset, version, iid = _resolve_target(args, 4)
        if args.action == "put":
            with open(args.file, encoding="utf-8") as f:
                rpt = RolloutReport.from_jsonl_line(f.read().strip())
            # 寻址与 report 内容必须一致，否则会把 report 写到与寻址不符的 key（静默错位）
            if rpt.datasetname != dataset or rpt.instanceid != iid:
                raise SystemExit(
                    f"寻址 {dataset}/{version}/{iid} 与 report 内容不一致 "
                    f"(report={rpt.datasetname}/{rpt.instanceid})")
            r.reports.put(rpt, version, overwrite=args.overwrite)
            print(f"report put {rpt.instanceid}", file=out)
            return 0
        # get
        rpt = r.reports.get(dataset, version, iid)
        line = rpt.to_jsonl_line()
        if args.file:
            with open(args.file, "w", encoding="utf-8") as f:
                f.write(line + "\n")
            print(str(args.file), file=out)
        else:
            print(line, file=out)
        return 0

    if args.cmd == "feedback":
        dataset, version, iid = _resolve_target(args, 4)
        fb = Feedback(type=args.type, id=args.id, score=args.score, message=args.message)
        r.instances.add_feedback(dataset, version, iid, fb)
        print(f"feedback appended to {iid}", file=out)
        return 0

    if args.cmd == "create":
        dataset, _, _ = _resolve_target(args, 2)
        l1, l2 = _split_dataset(dataset)
        # teacher 由 apiserver 从 benchmark 派生，CLI 不再提供 teacher 参数。
        series = DatasetSeries(
            dataset_name=dataset, dataset_l1=l1, dataset_l2=l2,
            benchmark_id=args.benchmark_id,
            visibility=args.visibility,
            display_name=args.display_name,
            description=args.description,
            default_scaffold=args.default_scaffold,
            owner=args.owner,
            owner_team_id=args.owner_team_id,
            workspace_id=args.workspace_id)
        created = r.datasets.create(
            series, require_benchmark=not args.no_require_benchmark)
        print(f"created {created.dataset_name} (dataset_id={created.dataset_id})",
              file=out)
        return 0

    if args.cmd == "claim":
        res = r.datasets.claim(
            args.dataset_id, args.workspace_id, args.benchmark_id or "",
            owner=args.owner,
            require_benchmark=not args.no_require_benchmark)
        print(f"claimed {res.get('dataset_id', args.dataset_id)} "
              f"by {res.get('user_id', '')}", file=out)
        return 0

    if args.cmd == "get":
        dataset, version, iid = _resolve_target(args, 4)
        inst = r.instances.get(dataset, version, iid, args.split)
        # 实例不存在时库层返回 None（apiserver 92003），显式区分"查不到"与"字段为空"。
        if inst is None:
            raise SystemExit(f"instance {dataset}/{version}/{iid} not found")
        src = "\t[oss]" if not inst.registered else ""
        print(f"{inst.instance_id}\t{inst.difficulty}\t{inst.docker_image}{src}",
              file=out)
        return 0

    if args.cmd == "version":
        # 非法 flag 组合显式报错（此前静默忽略，用户传了却不生效极难自查）：
        # --splits 只有 create/ingest 消费；--split 只有 status/ingest 消费
        # （ingest 的 --split/--splits 互斥由 SDK 层拦截）。
        if args.splits is not None and args.action in (
                "status", "get", "set-run-type", "update"):
            raise SystemExit(
                f"argument --splits: not allowed with version action {args.action}")
        if args.split is not None and args.action in (
                "create", "update", "list", "get", "set-run-type"):
            raise SystemExit(
                f"argument --split: not allowed with version action {args.action}")
        srt = (_parse_split_run_types(args.split_run_types)
               if args.split_run_types else None)
        if args.action in ("create", "list"):
            dataset, _, _ = _resolve_target(args, 2)
            if args.action == "list":
                for v in r.versions.list(dataset):
                    src = "\t[oss]" if not v.registered else ""
                    print(f"{v.version}\t{v.status}\t{v.storage_path}{src}",
                          file=out)
                return 0
            if not args.version:
                raise SystemExit("version create 需要 --version")
            splits = ([s.strip() for s in args.splits.split(",") if s.strip()]
                      if args.splits else None)
            dv = r.versions.create(dataset, args.version,
                                   storage_path=args.storage_path, splits=splits,
                                   status=args.status or "draft",
                                   storage_type=args.storage_type,
                                   environment=args.environment)
            print(f"created version {dv.dataset}/{dv.version} status={dv.status}",
                  file=out)
            return 0
        if args.action == "ingest":
            # ingest 寻址与 create/list 同为 parts=2（split_first 下 version 可省略）；
            # --version 是业务参数不是寻址参数，故不能走 parts=3 的 _resolve_target。
            dataset, _, _ = _resolve_target(args, 2)
            splits = ([s.strip() for s in args.splits.split(",") if s.strip()]
                      if args.splits else None)
            selected_ids = None
            if args.instance_ids is not None:
                unsupported = []
                if args.dry_run:
                    unsupported.append("--dry-run")
                if args.publish:
                    unsupported.append("--publish")
                if args.allow_layout_inference:
                    unsupported.append("--allow-layout-inference")
                if args.storage_path is not None:
                    unsupported.append("--storage-path")
                if args.run_type is not None:
                    unsupported.append("--run-type")
                if args.split_run_types is not None:
                    unsupported.append("--split-run-types")
                if unsupported:
                    raise SystemExit(
                        "--instance-id selected ingest 不支持 "
                        + ", ".join(unsupported))
                selected_ids = sorted(set(
                    value.strip()
                    for item in args.instance_ids
                    for value in item.split(",") if value.strip()))
                if not selected_ids:
                    raise SystemExit("--instance-id 至少需要一个非空ID")
                if splits:
                    raise SystemExit(
                        "--instance-id 只允许一个 --split，不能与 --splits 同用")
                registration = r.instances.ingest(
                    dataset, args.version or None, selected_ids,
                    split=args.split or "default",
                    environment=args.environment,
                    wait=not args.no_wait, poll_sec=args.poll_sec,
                    timeout_sec=args.timeout_sec, cluster=args.cluster)
                print(
                    f"jobs={len(registration.ingests)} "
                    f"completed={len(registration.completed)} "
                    f"pending={len(registration.pending)} "
                    f"failed={len(registration.failed)} "
                    f"unknown={len(registration.unknown)} "
                    f"not_submitted={len(registration.not_submitted)}",
                    file=out)
                unfinished = (registration.pending or registration.failed
                              or registration.unknown
                              or registration.not_submitted
                              or len(registration.completed)
                              != len(registration.selected_ids))
                return 1 if unfinished else 0

            job = r.versions.ingest(
                dataset, args.version or None,
                storage_path=args.storage_path, splits=splits,
                split=args.split, environment=args.environment,
                allow_layout_inference=args.allow_layout_inference,
                publish=args.publish, dry_run=args.dry_run,
                wait=not args.no_wait, poll_sec=args.poll_sec,
                timeout_sec=args.timeout_sec, cluster=args.cluster)
            if args.dry_run:
                for dv in job.get("versions") or []:
                    print(f"version\t{dv.get('version', '')}\t"
                          f"instances={dv.get('instance_count') or 0}"
                          f"\tsplits={len(dv.get('splits') or [])}", file=out)
                return 0
            status = (job.get("status") or "").lower()
            print(f"ingest {job.get('ingest_id', '')} "
                  f"status={job.get('status', '')} "
                  f"instances={job.get('stats', {}).get('instance_count') or 0}",
                  file=out)
            return 0 if status == "completed" else 1
        dataset, version, _ = _resolve_target(args, 3)
        if args.action == "status":
            if args.split:
                sp = r.versions.split_detail(dataset, version, args.split)
                print(f"{sp.get('name', args.split)}\t{sp.get('status', '')}\t"
                      f"{sp.get('storage_path', '')}\t"
                      f"published_at={sp.get('published_at') or ''}", file=out)
            else:
                print(r.versions.status(dataset, version), file=out)
            return 0
        if args.action == "get":
            # 1.0.10：取版本完整详情（splits 明细 + manifest + 时间戳）。
            # split_first 分支时服务端聚合 legacy 投影。
            dv = r.versions.get(dataset, version, environment=args.environment)
            # versions.get 返回 DatasetVersion dataclass（字段访问，非 dict 取值）。
            print(f"version\t{dv.version}\tstatus={dv.status}"
                  f"\tstorage_path={dv.storage_path or ''}", file=out)
            print(f"published_at={dv.published_at or ''}"
                  f"\tlast_ingested_at={dv.last_ingested_at or ''}", file=out)
            print(f"dataset_version_id={dv.dataset_version_id or ''}", file=out)
            for s in dv.splits:
                print(f"  split\t{s.get('name', '')}\tstatus={s.get('status', '')}"
                      f"\toss_prefix={s.get('oss_prefix', '')}"
                      f"\tinstance_count={s.get('instance_count') or 0}", file=out)
            manifest = dv.manifest or {}
            print(f"manifest\tinstance_count={manifest.get('instance_count') or 0}"
                  f"\tfile_count={manifest.get('file_count') or 0}"
                  f"\tsize_bytes={manifest.get('size_bytes') or 0}", file=out)
            return 0
        if args.action == "set-run-type":
            r.versions.set_run_type(dataset, version,
                                    run_type=args.run_type, split_run_types=srt)
            print(f"run_type set on {dataset}/{version}", file=out)
            return 0
        # update
        splits = ([s.strip() for s in args.splits.split(",") if s.strip()]
                  if args.splits else None)
        r.versions.update(dataset, version, status=args.status,
                          splits=splits, run_type=args.run_type,
                          split_run_types=srt)
        print(f"updated {dataset}/{version}", file=out)
        return 0

    # ── 1.0.10 控制面管理子命令 dispatch ────────────────────────────────────────
    if args.cmd == "split":
        if args.action == "list":
            dataset = (args.dataset or args.ref or "").strip()
            if not dataset:
                raise SystemExit("split list 需要 --dataset 或位置 ref（{L1}/{L2}）")
            res = r.splits.list(dataset,
                                version=args.version, version_scope=args.scope,
                                status=args.status,
                                page=args.page, page_size=args.page_size)
            for s in res.items:
                src = "projected" if s.projected else (
                    "oss" if not s.registered else "record")
                print(f"{s.name}\tversion={s.version or ''}\tstatus={s.status}"
                      f"\trun_type={s.run_type or ''}\t"
                      f"instance_count={_split_instance_count(s)}\t[{src}]",
                      file=out)
            print(f"page={res.page}/{_page_count(res)} total={res.total}", file=out)
            return 0
        if args.action == "create":
            dataset, split_name = _resolve_split_ref(args)
            sp = r.splits.create(dataset, split_name,
                                 version=args.version,
                                 run_type=args.run_type,
                                 storage_path=args.storage_path,
                                 environment=args.environment)
            src = "projected" if sp.projected else "record"
            print(f"created split\t{sp.name}\tversion={sp.version or ''}"
                  f"\tstatus={sp.status}\trun_type={sp.run_type or ''}"
                  f"\t[{src}]", file=out)
            print(f"storage_path={sp.storage_path}", file=out)
            return 0
        # get / set-run-type：需要定位到具体 split
        dataset, split_name = _resolve_split_ref(args)
        if args.action == "get":
            sp = r.splits.get(dataset, split_name, version=args.version)
            if sp is None:
                raise SystemExit(f"split {dataset}/{split_name} not found")
            src = "projected" if sp.projected else "record"
            print(f"split\t{sp.name}\tversion={sp.version or ''}"
                  f"\tstatus={sp.status}\trun_type={sp.run_type or ''}"
                  f"\t[{src}]", file=out)
            print(f"storage_path={sp.storage_path}", file=out)
            print(f"published_at={sp.published_at or ''}"
                  f"\tlast_ingested_at={sp.last_ingested_at or ''}", file=out)
            print(f"instance_count={_split_instance_count(sp)}", file=out)
            return 0
        # set-run-type
        if args.run_type is None:
            raise SystemExit("split set-run-type 需要 --run-type（train/eval/''）")
        r.splits.update(dataset, split_name,
                        version=args.version, run_type=args.run_type)
        print(f"split {dataset}/{split_name} run_type={args.run_type or '(cleared)'}",
              file=out)
        return 0

    if args.cmd == "dataset":
        if args.action == "list":
            res = r.datasets.list_paged(
                q=args.q, visibility=args.visibility,
                owned_by_me=args.owned_by_me or None,
                sort_by=args.sort_by, order=args.order,
                include_deprecated=args.include_deprecated or None,
                environment=args.environment,
                page=args.page, page_size=args.page_size)
            for ds in res.items:
                print(f"{ds.dataset_name}\tvisibility={ds.visibility}"
                      f"\tversion_count={ds.version_count}"
                      f"\tsplit_count={ds.split_count}"
                      f"\tlatest={ds.latest_version or ''}", file=out)
            print(f"page={res.page}/{_page_count(res)} total={res.total}", file=out)
            return 0
        # 其余动作需要 dataset 名（位置 ref 或 --dataset）
        dataset = (args.dataset or args.ref or "").strip()
        if args.action in ("get", "update", "access", "revoke") and not dataset:
            raise SystemExit(f"dataset {args.action} 需要 --dataset 或位置 ref")
        if args.action == "get":
            d = r.datasets.get_detail(dataset, environment=args.environment)
            src = "oss" if not d.registered else "mongodb"
            print(f"dataset\t{d.dataset_name}\tid={d.dataset_id}"
                  f"\tvisibility={d.visibility}\t[{src}]", file=out)
            print(f"version_count={d.version_count}\tsplit_count={d.split_count}"
                  f"\tlatest={d.latest_version or ''}", file=out)
            print(f"instance_count={d.stats.instance_count}"
                  f"\tfile_count={d.stats.file_count}"
                  f"\tsize_bytes={d.stats.size_bytes}", file=out)
            if not d.registered:
                print("warning: dataset not registered in MongoDB, "
                      "data from OSS discovery", file=sys.stderr)
            return 0
        if args.action == "update":
            kwargs = {}
            if args.display_name is not None:
                kwargs["display_name"] = args.display_name
            if args.description is not None:
                kwargs["description"] = args.description
            if args.visibility is not None:
                kwargs["visibility"] = args.visibility
            if args.benchmark_id is not None:
                kwargs["benchmark_id"] = args.benchmark_id
            if args.owner_team_id is not None:
                kwargs["owner_team_id"] = args.owner_team_id
            if args.default_scaffold is not None:
                kwargs["default_scaffold"] = args.default_scaffold
            if not kwargs:
                raise SystemExit(
                    "dataset update 至少给一个：--display-name / --description / "
                    "--visibility / --benchmark-id / --owner-team-id / "
                    "--default-scaffold")
            r.datasets.update(dataset, **kwargs)
            print(f"updated {dataset}", file=out)
            return 0
        if args.action in ("access", "revoke"):
            if args.action == "access":
                # 自动翻页取全量（服务端默认 20 会漏绑定量大的 dataset）
                page_n, all_items = 1, []
                while True:
                    res = r.datasets.list_access(dataset,
                                                 page=page_n, page_size=200)
                    all_items.extend(res.items)
                    if not res.has_more or not res.items:
                        break
                    page_n += 1
                for rb in all_items:
                    print(f"{rb.principal_type}\t{rb.principal_id}\t{rb.role_id}"
                          f"\tadded_by={rb.added_by}\tadded_at={rb.added_at}",
                          file=out)
                print(f"total={len(all_items)}", file=out)
                return 0
            if not (args.principal and args.role):
                raise SystemExit("dataset revoke 需要 --principal + --role")
            r.datasets.revoke(dataset, args.principal, args.role,
                              principal_type=args.principal_type)
            print(f"revoked {args.principal} ({args.principal_type}) "
                  f"{args.role} from {dataset}", file=out)
            return 0
        if args.action == "benchmarks":
            if args.ref and not args.q:
                b = r.benchmarks.get(args.ref)
                if b is None:
                    raise SystemExit(f"benchmark {args.ref} not found")
                print(f"benchmark\t{b.source_id}\tname={b.name}"
                      f"\tteacher_directions={','.join(b.teacher_directions)}"
                      f"\tis_core={b.is_core}", file=out)
                return 0
            res = r.benchmarks.list(
                q=args.q, source=args.source, is_core=args.is_core or None,
                page=args.page, page_size=args.page_size)
            for b in res.items:
                print(f"{b.source_id}\tname={b.name}\tis_core={b.is_core}"
                      f"\tdirections={','.join(b.teacher_directions)}", file=out)
            print(f"page={res.page}/{_page_count(res)} total={res.total}", file=out)
            return 0
        # workflows
        if args.ref:
            wf = r.workflows.get(args.ref)
            print(f"workflow\t{wf.id}\tkind={wf.kind}\tstatus={wf.status}"
                  f"\tcurrent_step={wf.current_step}", file=out)
            if wf.approval:
                print(f"approval\tprovider={wf.approval.provider}"
                      f"\tticket={wf.approval.ticket_link}"
                      f"\tstatus={wf.approval.status}", file=out)
            return 0
        res = r.workflows.list(
            kind=args.kind, status=args.status, creator=args.creator,
            page=args.page, page_size=args.page_size)
        for wf in res.items:
            print(f"{wf.id}\tkind={wf.kind}\tstatus={wf.status}"
                  f"\tcurrent_step={wf.current_step}", file=out)
        print(f"page={res.page}/{_page_count(res)} total={res.total}", file=out)
        return 0

    if args.cmd == "artifact":
        if args.artifact_cmd == "download":
            path = r.download_artifact(
                args.job_id, cluster=args.cluster,
                output_dir=args.output_dir,
                ap_endpoint=args.ap_endpoint,
                include_files=args.include_files, exclude_files=args.exclude_files,
                extract=args.extract)
            print(str(path), file=out)
            return 0
        if args.artifact_cmd == "download-many":
            job_ids = [j.strip() for j in args.job_ids.split(",") if j.strip()]
            results = r.download_artifacts(
                job_ids, cluster=args.cluster,
                output_dir=args.output_dir,
                max_concurrent=args.concurrent,
                ap_endpoint=args.ap_endpoint,
                include_files=args.include_files, exclude_files=args.exclude_files,
                extract=args.extract)
            ok, fail = 0, 0
            for jid, res in results.items():
                if isinstance(res, Exception):
                    print(f"FAIL  {jid}: {res}", file=out)
                    fail += 1
                else:
                    print(f"OK    {jid}: {res}", file=out)
                    ok += 1
            print(f"\ntotal={len(results)} ok={ok} failed={fail}", file=out)
            return 1 if fail else 0
        if args.artifact_cmd == "download-group":
            results = r.download_artifacts_from_group(
                args.group_id, cluster=args.cluster,
                output_dir=args.output_dir,
                max_concurrent=args.concurrent,
                ap_endpoint=args.ap_endpoint,
                include_files=args.include_files, exclude_files=args.exclude_files,
                extract=args.extract)
            ok, fail = 0, 0
            for jid, res in results.items():
                if isinstance(res, Exception):
                    print(f"FAIL  {jid}: {res}", file=out)
                    fail += 1
                else:
                    print(f"OK    {jid}: {res}", file=out)
                    ok += 1
            print(f"\ntotal={len(results)} ok={ok} failed={fail}", file=out)
            return 1 if fail else 0

    return 2  # pragma: no cover - argparse 已保证 cmd 合法


def cli_main(argv=None) -> int:
    """入口包装：把 SDK 异常收敛成单行报错，不向用户抛 Python traceback。

    与 Go CLI 的 ``irepo: error: …`` 输出对齐。``main()`` 保持原样抛异常，
    便于单测直接断言异常类型。

    ``ItemError`` 必须一并捕获：它继承自 ``Exception`` 而非 ``InstanceRepoError``，
    而 push-many/deliver 的默认「全或无」模式下单实例失败就是抛它——该路径在批量
    能力暴露到 CLI 之前不可达，现在可达了，漏捕会给用户一个 traceback。
    """
    try:
        return main(argv)
    except (InstanceRepoError, ItemError) as e:
        print(f"irepo: error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(cli_main())
