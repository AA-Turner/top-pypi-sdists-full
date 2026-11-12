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

from ..cache import transport_cache_identity

import contextlib
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


def business_metadata_model(metadata_model: str | None, *,
                            allow_version_first: bool = False) -> str:
    """Normalize a business model, optionally allowing explicit legacy reads.

    ``None``, the empty compatibility value, and ``split_first`` are accepted.
    ``version_first`` remains rejected by normal business I/O unless the caller
    explicitly opts into legacy metadata addressing.
    """
    from ..errors import SchemaError

    if metadata_model is not None and not isinstance(metadata_model, str):
        raise SchemaError("metadata_model must be a string or None")
    requested = (metadata_model or "").strip()
    if allow_version_first and requested == "version_first":
        return requested
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
    #: user-data 域独立 OSS bucket（F2-R1）：显式配置优先于 scope=user-data
    #: 自动发现（零发现网络调用）。空 = 走发现。
    user_data_bucket: str = ""
    #: user-data 域独立 OSS endpoint（F2-R1）：显式配置优先（须与 user_data_bucket
    #: 配套使用——bucket 走发现时该字段忽略，endpoint 以发现结果为准）。空=不覆盖。
    user_data_endpoint: str = ""

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
                  "oss_prefix", "scaffold_bucket", "scaffold_root", "api_base",
                  "user_data_bucket", "user_data_endpoint"):
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
                   user_data_bucket=str(cfg.pop("user_data_bucket", "") or "").strip(),
                   user_data_endpoint=str(cfg.pop("user_data_endpoint", "") or "").strip(),
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
    from ..errors import SchemaError
    if cluster:
        cluster = resolve_cluster(transport, cluster)
        query = urlencode({"cluster": cluster})
    elif storage_env:
        query = urlencode({"storage_env": storage_env})
    else:
        raise ValueError("fetch_repo_config requires 'cluster' or 'storage_env'")
    data = transport.get(f"/apis/v1/repo-config?{query}")
    # Discovery failures must remain typed so bootstrap can defer them until
    # the first data-plane operation. Do not expose malformed response values.
    if not isinstance(data, dict):
        raise SchemaError("repo-config response must be an object")
    for section in ("oss", "acr"):
        value = data.get(section)
        if value is not None and not isinstance(value, dict):
            raise SchemaError(f"repo-config {section} must be an object")
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

#: 缓存按 transport 实例、主体、api_base 与 Env 隔离：各调用方拓扑独立，
#: 共享一个进程里先后连两个 apiserver 时不会串味。
_cluster_map_cache: dict = {}    # (api_base, env, instance/subject) → 映射表
_cluster_map_expiry: dict = {}   # (api_base, env, instance/subject) → 过期时刻


def _cluster_cache_key(transport) -> tuple:
    return (
        str(getattr(transport, "base_url", "") or "").rstrip("/"),
        str(getattr(transport, "env", "") or ""),
        transport_cache_identity(transport),
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
        for stale in list(_cluster_map_cache):
            if now >= _cluster_map_expiry.get(stale, 0.0):
                _cluster_map_cache.pop(stale, None)
                _cluster_map_expiry.pop(stale, None)
        if key not in _cluster_map_cache and len(_cluster_map_cache) >= 512:
            stale = next(iter(_cluster_map_cache))
            _cluster_map_cache.pop(stale, None)
            _cluster_map_expiry.pop(stale, None)
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


# ── scope=user-data 独立配置发现（T-SDK-USERDATA，对齐 apiserver F1 schema1）────

#: user-data scope 的合法取值（apiserver repo_config_handler.repoConfigScopeUserData）。
USER_DATA_SCOPE = "user-data"

#: user-data 响应契约版本（apiserver userDataSchemaVersion；SDK 只认 1）。
USER_DATA_SCHEMA_VERSION = 1

#: user-data 域根前缀锚（apiserver userDataPrefixRoot / Repo.USER_DATA_ROOT）。
USER_DATA_PREFIX_ROOT = "swe/user-data/users/"


@dataclass(frozen=True)
class UserDataConfig:
    """scope=user-data 的解析结果：仅 OSS 寻址 + 能力声明，**不含任何密钥**。

    ``production_read_enabled`` / ``production_write_enabled`` 只是当前部署的
    gate **能力声明**，不构成授权——真实 STS 每次按认证主体与 RBAC 重新判定，
    调用方不得据此假定签发结果。旧服务（不认识 scope）经 ``allow_fallback``
    兼容时，这两个字段恒为 False（能力未知 → 关闭，不猜生产开启）。
    """

    schema_version: int = USER_DATA_SCHEMA_VERSION
    storage_env: str = ""
    prefix_root: str = USER_DATA_PREFIX_ROOT
    production_read_enabled: bool = False
    production_write_enabled: bool = False
    oss_bucket: str = ""
    oss_prefix: str = ""
    oss_endpoint: str = ""
    oss_region: str = ""

    def to_profile_overrides(self) -> dict:
        """转成 user-data **独立** profile overrides（只含 OSS 寻址 + storage_env）。

        独立性：不含任何 acr_*（user-data 域只用 OSS、不要求 ACR）、不含 cluster。
        用于为 user-data 上下文单独构造 Store/Content；**不要**并入 Dataset/
        artifact 的 profile——会污染其寻址。"""
        ov = {"storage_env": self.storage_env,
              "oss_bucket": self.oss_bucket,
              "oss_prefix": self.oss_prefix}
        if self.oss_endpoint:
            ov["oss_endpoint"] = self.oss_endpoint
        if self.oss_region:
            ov["oss_region"] = self.oss_region
        return ov


def _parse_user_data_config(data: dict, *, storage_env: str) -> "UserDataConfig":
    """校验并解析 scope=user-data 响应体（schema_version=1 契约，fail-closed）。

    P2-③ 严格校验：schema_version 必须是**精确整数 1**（bool 是 int 子类须显式排除，
    True==1 陷阱）；能力字段必须是真 bool（"false" 字符串不得被 truthy）；oss 必须
    dict 且 bucket 非空；storage_env 缺失拒绝（不默默取调用方 env 变 dev）。
    """
    from ..errors import SchemaError
    if not isinstance(data, dict):
        raise SchemaError("unexpected user-data repo-config response shape")
    v = data.get("schema_version")
    if isinstance(v, bool) or not isinstance(v, int) or v != USER_DATA_SCHEMA_VERSION:
        raise SchemaError(
            f"unsupported user-data repo-config schema_version: {v!r} "
            f"(supported: exact int {USER_DATA_SCHEMA_VERSION})")
    prefix_root = str(data.get("prefix_root") or "")
    if prefix_root != USER_DATA_PREFIX_ROOT:
        raise SchemaError(
            f"user-data prefix_root mismatch: {prefix_root!r} "
            f"(expected {USER_DATA_PREFIX_ROOT!r}; server/SDK 常量须一致)")
    for key in ("production_read_enabled", "production_write_enabled"):
        flag = data.get(key)
        if not isinstance(flag, bool):
            raise SchemaError(
                f"user-data {key} must be a boolean, got {flag!r}")
    oss = data.get("oss")
    if not isinstance(oss, dict) or not str(oss.get("bucket") or "").strip():
        raise SchemaError(
            "user-data repo-config oss must be an object with non-empty bucket "
            f"(fail-closed), got {oss!r}")
    env_raw = data.get("storage_env")
    if not isinstance(env_raw, str) or not env_raw.strip():
        raise SchemaError(
            "user-data repo-config storage_env is required (missing/empty; "
            "refusing to silently default)")
    env = normalize_storage_env(env_raw)
    return UserDataConfig(
        schema_version=USER_DATA_SCHEMA_VERSION,
        storage_env=env,
        prefix_root=prefix_root,
        production_read_enabled=data["production_read_enabled"],
        production_write_enabled=data["production_write_enabled"],
        oss_bucket=str(oss.get("bucket") or ""),
        oss_prefix=str(oss.get("prefix") or ""),
        oss_endpoint=str(oss.get("endpoint") or ""),
        oss_region=str(oss.get("region") or ""),
    )


def fetch_user_data_config(transport, *, cluster: str = "", storage_env: str = "",
                           allow_fallback: bool = False) -> "UserDataConfig":
    """从 apiserver ``GET /apis/v1/repo-config?…&scope=user-data`` 拉取 user-data
    独立配置（schema1：仅 OSS 寻址 + 生产读写能力声明，无密钥）。

    * ``cluster`` / ``storage_env`` 二选一；**同时给出时两个键都下发服务端**
      （P1-①：不得丢显式 env——服务端按 cluster 解析并做同语义冲突 400）。
    * **客户端预检**：cluster→storage_env 映射表（真实形状 ``{"clusters": {name:
      env}}`` 封套）与显式 env 冲突 → SchemaError（对齐 apiserver 400
      cluster_env_conflict：不静默换环境）。映射请求 401/403/5xx 等故障**原样
      抛出**（不得吞成"查不到"继续——那会在权限故障时静默跳过冲突检查）；
      仅"200 但封套里无该 cluster"（新集群未配）才跳过预检交服务端兜底。
    * **响应 env 核对**（P1-①）：scope 响应的 storage_env 与显式 env 不一致 →
      SchemaError（防服务端映射变更后的静默换环境）。
    * **旧服务兼容**（``allow_fallback=True``）：400 invalid scope 时回退一次
      **无 scope 旧 repo-config（保留 cluster 与显式 env 双键）**；旧响应的
      storage_env 与显式 env 也不一致 → SchemaError。能力字段恒 False。
    * 认证(401)/权限(403)/5xx/404 等不当版本 fallback，原样抛出。
    """
    from ..errors import SchemaError
    explicit_env = str(storage_env or "").strip()
    resolved_env = ""
    if cluster:
        cluster = resolve_cluster(transport, cluster)
        # 客户端预检：cluster→env 映射（真实封套 {"clusters": {name: env}}）。
        # 请求失败（401/403/DB 故障等异常）原样抛——不得吞成兼容继续。
        m = transport.get("/apis/v1/repo-config/cluster-storage-env-map")
        if not isinstance(m, dict):
            raise SchemaError("unexpected cluster-storage-env-map response shape")
        entries = m.get("clusters") if isinstance(m.get("clusters"), dict) else m
        if isinstance(entries, dict):
            resolved_env = str(entries.get(cluster) or "").strip()
        if resolved_env and explicit_env and explicit_env != resolved_env:
            raise SchemaError(
                f"cluster {cluster!r} maps to storage_env {resolved_env!r}; "
                f"conflicts with storage_env {explicit_env!r}")
        query = {"cluster": cluster, "scope": USER_DATA_SCOPE}
        if explicit_env:
            query["storage_env"] = explicit_env      # P1-①：双键一起下发
    elif explicit_env:
        query = {"storage_env": explicit_env, "scope": USER_DATA_SCOPE}
    else:
        raise SchemaError("fetch_user_data_config requires 'cluster' or 'storage_env'")
    try:
        data = transport.get("/apis/v1/repo-config?" + urlencode(query))
    except Exception as exc:
        status = getattr(exc, "status", None)
        msg = str(getattr(exc, "message", "") or exc)
        is_invalid_scope = (status == 400 and "invalid scope" in msg.lower())
        if allow_fallback and is_invalid_scope:
            # 旧服务不认识 scope：回退旧 repo-config（保留 cluster + 显式 env 双键）。
            if cluster:
                old_query = {"cluster": cluster}
                if explicit_env:
                    old_query["storage_env"] = explicit_env
            elif explicit_env:
                old_query = {"storage_env": explicit_env}
            else:
                raise SchemaError(
                    "fallback requires cluster or storage_env") from exc
            old = transport.get("/apis/v1/repo-config?" + urlencode(old_query))
            if not isinstance(old, dict):
                raise SchemaError(
                    "unexpected legacy repo-config response shape") from exc
            oss = old.get("oss")
            if not isinstance(oss, dict) or not str(oss.get("bucket") or "").strip():
                raise SchemaError(
                    "legacy repo-config oss must be an object with "
                    "non-empty bucket") from exc
            env_raw = str(old.get("storage_env") or "").strip()
            # P1-①：旧响应 env 与显式 env 不一致 → 拒绝（不静默换环境）。
            if env_raw and explicit_env and env_raw != explicit_env:
                raise SchemaError(
                    f"legacy repo-config resolved storage_env {env_raw!r} "
                    f"conflicts with explicit storage_env {explicit_env!r}")
            env = normalize_storage_env(env_raw or explicit_env)
            return UserDataConfig(
                schema_version=USER_DATA_SCHEMA_VERSION,
                storage_env=env,
                production_read_enabled=False,   # 能力未知 → 关闭，不猜
                production_write_enabled=False,
                oss_bucket=str(oss.get("bucket") or ""),
                oss_prefix=str(oss.get("prefix") or ""),
                oss_endpoint=str(oss.get("endpoint") or ""),
                oss_region=str(oss.get("region") or ""),
            )
        raise
    cfg = _parse_user_data_config(data, storage_env=explicit_env)
    # P1-①：响应 env 与显式 env 不一致 → 拒绝（不静默换环境）。
    if explicit_env and cfg.storage_env and \
            cfg.storage_env != normalize_storage_env(explicit_env):
        raise SchemaError(
            f"repo-config resolved storage_env {cfg.storage_env!r} conflicts "
            f"with explicit storage_env {explicit_env!r}")
    return cfg
