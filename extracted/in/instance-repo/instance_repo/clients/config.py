"""clients/config.py — 运行时配置解析（v0.8 起「三参数起步」）。

调用方使用三个规范环境变量：

* ``AP_API_KEY`` —— 凭据；
* ``IR_API_ENV`` —— 控制面环境（下发为 ``Env`` 请求头）；
* ``INSTANCE_REPO_STORAGE_ENV`` —— 数据面存储环境。

其余寻址信息（OSS bucket/prefix、ACR registry/namespace）由 ``Repo()`` 构造时自动向
apiserver 的 ``repo-config`` 拉取、校验并缓存，见 ``bootstrap.py``。规范控制面根地址变量为
``AP_BASE_URL``，未设置时使用站点默认值（``DEFAULT_API_BASE``）。旧名称
``INSTANCEREPO_TOKEN``、``IR_STORAGE_ENV``、``INSTANCEREPO_API_BASE`` 仅作为兼容别名保留。

两件**正交**的事分开表达：

* ``storage_env`` 决定**数据面**落在哪：OSS bucket、ACR host/namespace、oss_prefix；
* ``api_base`` / ``api_env`` 决定**控制面**：连哪个 apiserver、下发的 ``Env`` 头值。

发布安全：除控制面默认地址外，SDK 源码**不硬编码**任何 profile 到业务环境的映射、
OSS bucket/endpoint/region 或 ACR registry/namespace，这些一律运行时取得。长期 AK 不落
配置（数据面凭证一律由 apiserver 签发 STS）。

手工寻址环境变量 ``IR_OSS_BUCKET`` / ``IR_ACR_HOST`` / ``IR_ACR_NAMESPACE`` 自 v0.8
起**弃用**，保留一个版本并在命中时提示一次；确需覆盖自动发现结果时请改用
``Repo(profile_overrides=...)``。
"""
from __future__ import annotations

import logging
import os
import warnings
from dataclasses import dataclass, field
from urllib.parse import urlencode

from .. import _site_defaults

_logger = logging.getLogger(__name__)

# ── 规范参数与兼容别名 ──
AP_API_KEY = "AP_API_KEY"
AP_BASE_URL = "AP_BASE_URL"
AP_CLUSTER = "AP_CLUSTER"
INSTANCE_REPO_STORAGE_ENV = "INSTANCE_REPO_STORAGE_ENV"

INSTANCEREPO_TOKEN = "INSTANCEREPO_TOKEN"
INSTANCEREPO_API_BASE = "INSTANCEREPO_API_BASE"
IR_STORAGE_ENV = "IR_STORAGE_ENV"

ENV_API_KEY = AP_API_KEY
ENV_API_BASE = AP_BASE_URL
ENV_CLUSTER = AP_CLUSTER
ENV_STORAGE_ENV = INSTANCE_REPO_STORAGE_ENV
LEGACY_ENV_API_KEY = INSTANCEREPO_TOKEN
LEGACY_ENV_API_BASE = INSTANCEREPO_API_BASE
LEGACY_ENV_STORAGE_ENV = IR_STORAGE_ENV

# ── 控制面 ──
ENV_API_ENV = "IR_API_ENV"               # Env 请求头值（apiserver 据此路由；原样下发）

#: apiserver 根地址的站点默认值，来自 ``_site_defaults.API_BASE``。
#:
#: **源码与公网 PyPI 包里恒为空串**；内网渠道（ArtLab / OSS）在构建期注入部署方地址。
#: 这样「三参数起步」与「公网包不含任何内网域名」两个目标可以同时成立——把域名硬编码进
#: 源码会让公网包泄漏内网拓扑，正是发布流水线泄漏门禁要拦的东西。详见 ``_site_defaults``。
#:
#: 为空时行为与 v0.7.x 一致：真正发控制面请求时报错并引导配置 ``AP_BASE_URL``。
DEFAULT_API_BASE = _site_defaults.API_BASE

# ── 数据面：v0.8 只需 storage_env，其余寻址字段由 Repo 自动发现（见 bootstrap.py）──

# ── 数据面 profile 字段（v0.8 起弃用；保留一个版本，命中时提示）──
ENV_OSS_BUCKET = "IR_OSS_BUCKET"
ENV_ACR_HOST = "IR_ACR_HOST"
ENV_ACR_NAMESPACE = "IR_ACR_NAMESPACE"
ENV_OSS_PREFIX = "IR_OSS_PREFIX"
ENV_SCAFFOLD_BUCKET = "IR_SCAFFOLD_BUCKET"
ENV_SCAFFOLD_ROOT = "IR_SCAFFOLD_ROOT"

# 公网 ACR registry：runner 不在 VPC 内网时，可显式切换使用公网 registry。
ENV_ACR_PUBLIC_HOST = "IR_ACR_PUBLIC_HOST"
# 是否优先使用公网 registry（"1"/"true"/"on"，大小写不敏感）。
ENV_ACR_PREFER_PUBLIC = "IR_ACR_PREFER_PUBLIC"

#: v0.8 弃用的手工寻址环境变量 → 建议替代。scaffold 两项不在其中：scaffold 包不在
#: repo-config 的返回范围内，仍须显式提供。
DEPRECATED_ADDRESS_ENVS = {
    ENV_OSS_BUCKET: ENV_STORAGE_ENV,
    ENV_ACR_HOST: ENV_STORAGE_ENV,
    ENV_ACR_NAMESPACE: ENV_STORAGE_ENV,
}

# oss_prefix 是 **bucket 内的对象目录布局约定**（与 apiserver 契约强绑定），不暴露
# 任何基础设施位置信息，作为协议常量保留默认值；可用 IR_OSS_PREFIX / overrides 覆盖。
DEFAULT_OSS_PREFIX = "swe/datasets"

# ── storage_env → dataset environment 派生 ──
# 对接分支 codex/dataset-split-first-metadata 的 ingest 只认 environment（online|pre），
# 没有 storage_env 字段，且未知字段被 gin 静默丢弃。故 SDK 自行派生 environment 并显式
# 下发；storage_env 仅附带下发以便将来两条分支合并后自动生效。
STORAGE_ENV_PROD = "prod"
STORAGE_ENV_DEV = "dev"
STORAGE_ENV_INTERNAL_DEV = "internal-dev"
STORAGE_ENV_EXTERNAL_DEV = "external-dev"
DATASET_ENV_ONLINE = "online"
DATASET_ENV_PRE = "pre"

_STORAGE_ENV_TO_DATASET_ENV = {
    STORAGE_ENV_PROD: DATASET_ENV_ONLINE,
    STORAGE_ENV_DEV: DATASET_ENV_PRE,
    STORAGE_ENV_INTERNAL_DEV: DATASET_ENV_PRE,
    STORAGE_ENV_EXTERNAL_DEV: DATASET_ENV_PRE,
}


_warned_envs: set[str] = set()


def resolve_config_value(explicit: str | None, primary: str,
                         legacy: str | None = None, site_default: str = "",
                         environ=None) -> str:
    """按 explicit > primary > legacy > site default 解析单个配置值。

    空字符串（含纯空白）视为未配置。只要非空旧别名存在就发一次 ``FutureWarning``；
    新旧冲突时仍使用新值，告警只列变量名、绝不回显配置值。
    """
    env = os.environ if environ is None else environ
    primary_value = env.get(primary, "") if primary else ""
    legacy_value = env.get(legacy, "") if legacy else ""

    def configured(value) -> bool:
        return value is not None and bool(str(value).strip())

    if legacy and configured(legacy_value) and legacy not in _warned_envs:
        _warned_envs.add(legacy)
        if configured(primary_value) and primary_value != legacy_value:
            message = f"{legacy} 已弃用且与 {primary} 冲突；将使用 {primary}。"
        else:
            message = f"{legacy} 已弃用；请改用 {primary}。"
        warnings.warn(message, FutureWarning, stacklevel=2)

    for value in (explicit, primary_value, legacy_value, site_default):
        if configured(value):
            return value
    return ""


def normalize_storage_env(storage_env: str | None) -> str:
    return (storage_env or "").strip().lower()


def business_metadata_model(metadata_model: str | None) -> str:
    """Normalize a normal business entry to the only supported model.

    ``None``, the empty compatibility value, and ``split_first`` are accepted.
    ``version_first`` remains available only through low-level ``Layout`` and
    legacy discovery helpers, never through Repo/client business I/O.
    """
    from ..errors import SchemaError

    if metadata_model is not None and not isinstance(metadata_model, str):
        raise SchemaError("metadata_model must be a string or None")
    requested = (metadata_model or "").strip()
    if requested not in ("", "split_first"):
        if requested == "version_first":
            raise SchemaError(
                "normal business entry is fixed to metadata_model=split_first; "
                "version_first is retained only for low-level legacy reads")
        raise SchemaError(
            f"invalid metadata_model {requested!r}; normal business entry only "
            "accepts split_first")
    return "split_first"


def dataset_environment_for(storage_env: str | None) -> str:
    """由 storage_env 派生 ingest 的 ``environment``；无法派生时返回空串。

    返回空串而非抛错：storage_env 是服务端可扩展的枚举，SDK 不该因为不认识某个新值就
    阻断调用；派生不出来时退回不下发 ``environment``，由服务端自己的默认值决定。
    """
    return _STORAGE_ENV_TO_DATASET_ENV.get(normalize_storage_env(storage_env), "")


def _warn_deprecated_envs(present: dict) -> None:
    """遗留手工寻址环境变量命中时提示一次（不重复污染批量作业日志）。"""
    for name, replacement in DEPRECATED_ADDRESS_ENVS.items():
        if not present.get(name) or name in _warned_envs:
            continue
        _warned_envs.add(name)
        warnings.warn(
            f"{name} 自 v0.8 起弃用，将在下一个大版本移除：改配 {replacement} 让 "
            f"Repo() 自动从 apiserver 的 repo-config 发现数据面寻址；确需手工覆盖时"
            f"请用 Repo(profile_overrides=...)。",
            DeprecationWarning, stacklevel=3)


def normalize_api_env(env: str) -> str:
    """规范化 Env 头取值：仅去空白、转小写。

    **不做任何具名别名映射**（不内置任何具体环境名）；调用方须传服务端实际认的环境
    标识，SDK 原样下发。
    """
    return (env or "").strip().lower()


@dataclass
class Profile:
    name: str
    oss_bucket: str = ""
    acr_host: str = ""
    acr_public_host: str = ""
    acr_namespace: str = ""
    oss_prefix: str = DEFAULT_OSS_PREFIX
    scaffold_bucket: str = ""
    scaffold_root: str = ""
    api_base: str = ""
    api_env: str = ""
    cluster: str = ""
    storage_env: str = ""
    #: storage_env 已经由 repo-config 校验/解析时所绑定的 cluster；空表示尚无绑定证明。
    storage_env_cluster: str = ""
    #: 元数据模型（version_first | split_first）；空即由 layout 归一为 SDK 默认。
    metadata_model: str = ""
    #: 本 profile 的寻址字段各自来自哪里（explicit / env / discovery），用于报错诊断。
    sources: dict = field(default_factory=dict)
    #: 自动发现失败时的真实错误信息（OSError / InstanceRepoError 等），由
    #: ``bootstrap.discover()`` 捕获异常时写入；``require()`` 据此在报错消息里
    #: 透传根因，避免"返回里没有 acr_host"这类误导性口径。
    discovery_error: str = ""
    #: 优先使用公网 ACR registry（默认 False=走 VPC 内网）。runner 不在 VPC
    #: 内网时置 True，配合 ``acr_public_host``（repo-config 的 public_registry）
    #: 生效；公网值缺失时静默回落到 ``acr_host``。
    prefer_public_registry: bool = False

    @property
    def effective_acr_host(self) -> str:
        """ACR 操作实际使用的 registry host。

        默认返回 ``acr_host``（repo-config 的 registry，通常是 VPC 内网域名）；
        ``prefer_public_registry=True`` 且 ``acr_public_host`` 非空时返回公网域名。
        """
        if self.prefer_public_registry and self.acr_public_host:
            return self.acr_public_host
        return self.acr_host

    @property
    def dataset_environment(self) -> str:
        """由 storage_env 派生的 ingest ``environment``（online|pre）；派生不出为空串。"""
        return dataset_environment_for(self.storage_env)


def resolve_api_base(api_env: str | None = None, *, api_base: str | None = None,
                     environ=None) -> tuple[str, str]:
    """解析控制面，返回 ``(api_base, api_env)``。

    ``api_base`` 按显式参数、``AP_BASE_URL``、旧别名 ``INSTANCEREPO_API_BASE``、
    ``DEFAULT_API_BASE`` 依次解析。``api_env`` 为下发的 ``Env`` 头值，来自显式参数或
    ``IR_API_ENV``；均未提供时默认 ``"product"``（生产环境）。
    """
    values = os.environ if environ is None else environ
    base = resolve_config_value(
        api_base, ENV_API_BASE, LEGACY_ENV_API_BASE, DEFAULT_API_BASE, values)
    env = normalize_api_env(api_env or values.get(ENV_API_ENV) or "product")
    return str(base).rstrip("/"), env


def load_profile(name: str = "default", *, overrides: dict | None = None,
                 api_env: str | None = None,
                 api_base: str | None = None,
                 cluster: str | None = None,
                 storage_env: str | None = None,
                 metadata_model: str | None = None) -> Profile:
    """组装运行时 Profile。``name`` 仅作标签，**不查任何内置取值**。

    数据面字段来源优先级：``overrides`` > 遗留寻址环境变量 > 空（留给自动发现填充，见
    ``bootstrap.resolve_profile``）。规范参数按显式参数 > 新环境变量 > 旧兼容别名 >
    站点默认值解析；``api_env``（Env 头）仍取参数或 ``IR_API_ENV``。

    关键字段（如 oss_bucket / acr_host）允许为空——仅在对应数据面操作真正用到时才校验，
    纯控制面元数据操作（list/get/create/claim/whoami）不需要它们。
    """
    requested_model = business_metadata_model(metadata_model)
    base, env = resolve_api_base(api_env, api_base=api_base)
    cluster_value = resolve_config_value(cluster, ENV_CLUSTER)
    storage_value = resolve_config_value(
        storage_env, ENV_STORAGE_ENV, LEGACY_ENV_STORAGE_ENV)
    env_values = {k: os.environ.get(k, "") for k in
                  (ENV_OSS_BUCKET, ENV_ACR_HOST, ENV_ACR_NAMESPACE,
                   ENV_ACR_PUBLIC_HOST,
                   ENV_OSS_PREFIX, ENV_SCAFFOLD_BUCKET, ENV_SCAFFOLD_ROOT)}
    _warn_deprecated_envs(env_values)
    cfg = {
        "oss_bucket": env_values[ENV_OSS_BUCKET],
        "acr_host": env_values[ENV_ACR_HOST],
        "acr_namespace": env_values[ENV_ACR_NAMESPACE],
        "acr_public_host": env_values[ENV_ACR_PUBLIC_HOST],
        "oss_prefix": env_values[ENV_OSS_PREFIX] or DEFAULT_OSS_PREFIX,
        "scaffold_bucket": env_values[ENV_SCAFFOLD_BUCKET],
        "scaffold_root": env_values[ENV_SCAFFOLD_ROOT],
        "api_base": base,
    }
    sources = {k: ("env" if v else "") for k, v in cfg.items()}
    # api_env 来源追踪：显式参数 > 环境变量 > 默认值（空表示可被自动发现覆盖）。
    if api_env is not None and str(api_env).strip():
        sources["api_env"] = "explicit"
    elif os.environ.get(ENV_API_ENV, "").strip():
        sources["api_env"] = "env"
    else:
        sources["api_env"] = ""
    prefer_public = False
    if overrides:
        # 只接受已知字段，避免把 api_env 之类误当数据面字段；
        # prefer_public_registry 单独取（非寻址字段，不进 **cfg 传 Profile）。
        for k in ("oss_bucket", "acr_host", "acr_namespace", "acr_public_host",
                  "oss_prefix", "scaffold_bucket", "scaffold_root", "api_base"):
            if k in overrides and overrides[k] is not None:
                cfg[k] = overrides[k]
                sources[k] = "explicit"
        if overrides.get("prefer_public_registry") is not None:
            prefer_public = bool(overrides["prefer_public_registry"])
    if cfg["api_base"]:
        cfg["api_base"] = str(cfg["api_base"]).rstrip("/")
    if not prefer_public:
        # 环境变量开关：IR_ACR_PREFER_PUBLIC=1/true/on（大小写不敏感）
        prefer_public = os.environ.get(ENV_ACR_PREFER_PUBLIC, "").strip().lower() \
            in ("1", "true", "on")
    return Profile(name=name, api_env=env,
                   cluster=str(cluster_value).strip(),
                   storage_env=normalize_storage_env(storage_value),
                   metadata_model=requested_model,
                   prefer_public_registry=bool(prefer_public),
                   sources=sources, **cfg)


def fetch_repo_config(transport, *, cluster: str = "", storage_env: str = "") -> dict:
    """从 apiserver GET /apis/v1/repo-config 拉取存储寻址配置（无密钥）。

    返回 dict 可直接作为 profile_overrides 传给 load_profile / Repo()：
    {"oss_bucket": ..., "acr_host": ..., "acr_namespace": ..., "oss_prefix": ...}。

    需要先有一个能发控制面请求的 transport（已配 api_base + token）。
    cluster 与 storage_env 二选一；cluster 优先（apiserver 先由 cluster 解析出 storage_env）。

    如果 cluster 是集群 ID（c 前缀 + 32 位 hex）或 url_cluster，会先通过
    ``GET /apis/v1/clusters`` 解析为集群 Name 再下发——apiserver 的 repo-config
    只按 Name 精确匹配（大小写敏感），用户不需要区分 cluster name / cluster id /
    url_cluster。

    用法示例::

        from instance_repo.clients.config import fetch_repo_config
        from instance_repo.transport import Transport

        t = Transport(base_url, token)
        overrides = fetch_repo_config(t, cluster="<your-cluster-name>")  # 或 storage_env="dev"
        repo = Repo(profile_overrides=overrides)
    """
    if cluster:
        cluster = resolve_cluster(transport, cluster)
        query = urlencode({"cluster": cluster})
    elif storage_env:
        query = urlencode({"storage_env": storage_env})
    else:
        raise ValueError("fetch_repo_config requires 'cluster' or 'storage_env'")
    data = transport.get(f"/apis/v1/repo-config?{query}")
    # 映射 apiserver 响应字段到 SDK profile_overrides 的 key；cluster 查询的顶层
    # storage_env 是服务端解析结果，必须保留给 Profile 与 ingest 使用。cluster 键回传
    # 解析后的**规范 Name**（可能是 id/url_cluster 的解析结果），供 bootstrap 记录绑定
    # 证明、ingest 下发 body——两个消费方都需要服务端按 Name 精确匹配的规范值。
    result = {}
    if cluster:
        result["cluster"] = cluster
    if cluster and data.get("storage_env"):
        result["storage_env"] = normalize_storage_env(data["storage_env"])
    if oss := data.get("oss"):
        if oss.get("bucket"):
            result["oss_bucket"] = oss["bucket"]
        if oss.get("prefix"):
            result["oss_prefix"] = oss["prefix"]
    if acr := data.get("acr"):
        if acr.get("registry"):
            result["acr_host"] = acr["registry"]
        if acr.get("public_registry"):
            result["acr_public_host"] = acr["public_registry"]
        if acr.get("namespace"):
            result["acr_namespace"] = acr["namespace"]
    # api_env 由 apiserver 在 repo-config 响应中下发（omitempty，旧版不返回）。
    # 仅在非空时写入 result，调用方据此判断是否需要填充 profile。
    api_env_raw = data.get("api_env")
    if isinstance(api_env_raw, str) and api_env_raw.strip():
        result["api_env"] = normalize_api_env(api_env_raw)
    return result


# ── cluster ID / url_cluster → Name 解析 ──

#: 集群列表缓存时间（秒）。集群拓扑变更频率极低，1 小时足够。
_CLUSTER_MAP_TTL = 3600.0

#: 缓存按 transport 身份（api_base + Env 头）隔离：不同控制面部署的集群拓扑各自独立，
#: 共享一个进程里先后连两个 apiserver 时不会串味。
_cluster_map_cache: dict = {}    # (api_base, env) → 映射表
_cluster_map_expiry: dict = {}   # (api_base, env) → 过期时刻


def _cluster_cache_key(transport) -> tuple:
    return (
        str(getattr(transport, "base_url", "") or "").rstrip("/"),
        str(getattr(transport, "env", "") or ""),
        id(transport) if getattr(transport, "_custom_send", False) else 0,
    )


def _empty_cluster_map() -> dict:
    return {"id_to_name": {}, "url_to_name": {}, "names": set()}


def fetch_cluster_map(transport) -> dict:
    """从 ``GET /apis/v1/clusters`` 拉取集群列表，构建 ``id→Name`` 与 ``url_cluster→Name`` 映射。

    apiserver 的 repo-config 只按集群 Name 精确匹配（大小写敏感），因此 SDK 把用户可能
    提供的三种标识（cluster ID / url_cluster / Name）都规范化为 Name 再下发。结果缓存在
    进程内存中（按 transport 身份隔离），TTL 与 discover 一致（3600 秒）。拉取失败不缓存
    新结果：已有该 transport 的成功缓存时回退使用（stale 拓扑好过没有），否则返回空映射。
    """
    import time
    global _cluster_map_cache, _cluster_map_expiry
    key = _cluster_cache_key(transport)
    now = time.time()
    cached = _cluster_map_cache.get(key)
    if cached is not None and now < _cluster_map_expiry.get(key, 0.0):
        return cached
    try:
        data = transport.get("/apis/v1/clusters")
        clusters = data.get("clusters", data) if isinstance(data, dict) else (data or [])
        id_to_name: dict[str, str] = {}
        url_to_name: dict[str, str] = {}
        names: set[str] = set()
        for entry in (clusters or []):
            if not isinstance(entry, dict):
                continue
            cid = str(entry.get("cluster_id") or "").strip()
            url = str(entry.get("url_cluster") or "").strip()
            name = str(entry.get("name") or "").strip()
            if not name:
                continue
            names.add(name)
            if cid and cid not in id_to_name:
                id_to_name[cid] = name
            if url and url not in url_to_name:
                url_to_name[url] = name
        fresh = {
            "id_to_name": id_to_name,
            "url_to_name": url_to_name,
            "names": names,
        }
        _cluster_map_cache[key] = fresh
        _cluster_map_expiry[key] = now + _CLUSTER_MAP_TTL
        return fresh
    except Exception:
        _logger.debug("fetch_cluster_map failed", exc_info=True)
        return cached if cached is not None else _empty_cluster_map()


def resolve_cluster(transport, cluster_value: str) -> str:
    """将 cluster ID 或 url_cluster 解析为集群 Name；已是 Name 则原样返回。

    调用 ``GET /apis/v1/clusters`` 获取映射后解析。优先级：Name 本身 > cluster ID >
    url_cluster。映射失败时保留原值（让 apiserver 返回明确的 "unknown cluster" 错误）。
    入参先去除首尾空白（与 Go/Java 的 ResolveCluster 一致）；纯空白直接返回，不发请求。
    """
    value = str(cluster_value or "").strip()
    if not value:
        return value
    cmap = fetch_cluster_map(transport)
    if value in cmap["names"]:
        return value
    for key in ("id_to_name", "url_to_name"):
        resolved = cmap[key].get(value)
        if resolved:
            return resolved
    return value


def clear_cluster_map_cache() -> None:
    """清空集群映射缓存（测试用）。"""
    global _cluster_map_cache, _cluster_map_expiry
    _cluster_map_cache = {}
    _cluster_map_expiry = {}
