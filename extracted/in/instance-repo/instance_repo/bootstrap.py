"""bootstrap.py — 数据面寻址自动发现（v0.8「三参数起步」的实现）。

调用方只提供 token + ``IR_API_ENV`` + ``IR_STORAGE_ENV``，``Repo()`` 构造时由本模块
自动向 apiserver 拉取该 storage_env 的数据面寻址（OSS bucket/prefix、ACR
registry/namespace），校验并缓存。

三条设计约束：

**一、失败必须延迟且可诊断。** 构造 ``Repo()`` 时若控制面不可达或 ``IR_STORAGE_ENV``
未配置，**不立刻抛错**——纯控制面操作（list / get / create / claim / whoami）根本不需要
数据面寻址，构造期硬失败会把这些操作一并阻断。改为在首次真正需要某个寻址字段时抛
``SchemaError``，消息里同时说明缺了哪个字段、自动发现走到哪一步、以及可用的手工覆盖方式。

**二、优先级固定为 显式 > 遗留环境变量 > 自动发现。** 已经显式配好的调用方不会因为
引入自动发现而行为漂移；反过来，自动发现也不会覆盖调用方的明确意图。

**三、缓存按 ``(api_base, api_env, selector_type, selector_value)`` 四元组。** cluster
与 storage_env 即使值相同也不会串味；默认 TTL 内复用，``refresh=True`` 可强制重新拉取。
"""
from __future__ import annotations

import logging
import threading
import time

from .cache import TTLCache
from .clients.config import (
    Profile, fetch_repo_config, normalize_storage_env,
)
from .errors import InstanceRepoError, SchemaError

_logger = logging.getLogger(__name__)

#: 自动发现结果的缓存存活时间（秒）。寻址配置变更频率极低，一小时足够；
#: 需要立刻生效时用 ``resolve_profile(..., refresh=True)`` 或 ``clear_cache()``。
DISCOVERY_TTL_SECONDS = 3600.0

#: 由自动发现填充的字段（scaffold 两项不在 repo-config 返回范围内，仍须显式提供）。
DISCOVERABLE_FIELDS = ("oss_bucket", "oss_prefix", "acr_host",
                       "acr_public_host", "acr_namespace")

_cache = TTLCache(safety=0.0)
_lock = threading.Lock()


def clear_cache() -> None:
    """清空自动发现缓存（测试与「改了配置要立刻生效」场景用）。"""
    _cache.clear()


def _selector(profile: Profile) -> tuple[str, str]:
    if profile.cluster:
        return "cluster", profile.cluster
    if profile.storage_env:
        return "storage_env", profile.storage_env
    return "", ""


def _cache_key(profile: Profile) -> tuple:
    selector_type, selector_value = _selector(profile)
    return (profile.api_base, profile.api_env, selector_type, selector_value)


def discover(transport, profile: Profile, *, refresh: bool = False) -> dict:
    """拉取（或复用缓存的）cluster/storage_env 数据面寻址。

    cluster 优先于 storage_env。返回 ``{}`` 而不抛错的两种情况：选择器未配置，或控制面
    查询失败。两者都不是立刻要失败的错误——调用方可能只用控制面能力，也可能已经显式
    配好了寻址。真正缺字段的失败在 :func:`require` 里报。
    """
    selector_type, selector_value = _selector(profile)
    if not selector_type:
        return {}
    key = _cache_key(profile)
    if not refresh:
        cached = _cache.get(key)
        if cached is not None:
            return cached
    with _lock:
        if not refresh:
            cached = _cache.get(key)
            if cached is not None:
                return cached
        try:
            found = fetch_repo_config(transport, **{selector_type: selector_value})
        except (InstanceRepoError, OSError) as exc:
            # 控制面错误以及 DNS/连接层 OSError 都按延迟失败处理：构造 Repo 不应阻断
            # 纯控制面操作。记空结果避免每次数据面调用都重试，TTL 到期后仍会恢复。
            #
            # 不缓存空结果：缓存空结果会让"修复了集群名拼写"或"network 恢复"后仍需等 1 小时。
            # 改为每次数据面操作都重试（apiserver 的 repo-config 是轻量 GET，无副作用）。
            #
            # 把真实错误写进 profile.discovery_error：require() 报错时会透传根因，
            # 避免用户看到"返回里没有 acr_host"而实际是 TCP 连接就没成功。
            profile.discovery_error = f"{type(exc).__name__}: {exc}"
            _logger.warning(
                "repo-config 自动发现失败（selector=%s=%s），后续数据面操作会报 "
                "oss_bucket is required。如非网络问题，请检查 cluster 名是否正确："
                "用 irepo repo-config --cluster <值> 可直接看到错误。",
                selector_type, selector_value, exc_info=True)
            return {}
        # 发现成功时清空错误记录，避免上一次失败信息残留。
        profile.discovery_error = ""
        _cache.put(key, dict(found), _expiry())
        return dict(found)


def _expiry() -> float:
    return time.time() + DISCOVERY_TTL_SECONDS


def resolve_profile(transport, profile: Profile, *, refresh: bool = False
                    ) -> Profile:
    """把自动发现结果填进 profile 的**空字段**（不覆盖显式值与遗留环境变量值）。

    就地修改并返回同一个 ``Profile`` 对象——``Repo`` 已经把它分发给多个 client，替换成
    新对象会让各 client 看到不同快照。同时在 ``profile.sources`` 记下每个字段的来源，
    供 :func:`require` 生成可诊断的报错。

    ``oss_prefix`` 例外说明：它有协议默认值，来源为空即表示当前值就是默认值，可以被
    发现结果替换；这与其它字段"空即未解析"的判定是同一条规则，无需特殊分支。
    """
    found = discover(transport, profile, refresh=refresh)
    if not found:
        return profile

    resolved_storage_env = normalize_storage_env(found.get("storage_env"))
    if profile.cluster and resolved_storage_env:
        storage_source = profile.sources.get("storage_env")
        if profile.storage_env and profile.storage_env != resolved_storage_env \
                and storage_source != "discovery":
            raise SchemaError(
                f"cluster={profile.cluster!r} 与显式 profile storage_env="
                f"{profile.storage_env!r} 冲突：服务端解析为 {resolved_storage_env!r}")
        if not profile.storage_env or storage_source == "discovery":
            profile.storage_env = resolved_storage_env
            profile.sources["storage_env"] = "discovery"
        # 无论 storage_env 是查询所得，还是显式值经本次查询确认一致，都记录二者绑定。
        # ingest 只复用带这个证明的双 selector，避免方法级 cluster 覆盖后夹带旧环境。
        # 绑定值取 repo-config 响应回传的**规范 Name**（cluster 入参为 id/url_cluster 时
        # 已被 resolve_cluster 解析），与 ingest body 下发值同源，服务端按 Name 精确匹配。
        profile.storage_env_cluster = (
            found.get("cluster") or profile.cluster)

    for field in DISCOVERABLE_FIELDS:
        value = found.get(field)
        if not value:
            continue
        if profile.sources.get(field) in ("explicit", "env"):
            continue          # 显式 / 遗留环境变量优先，不被自动发现覆盖
        setattr(profile, field, value)
        profile.sources[field] = "discovery"

    # api_env 自动发现：repo-config 响应里携带 api_env 时，仅在用户未显式配置
    # IR_API_ENV / api_env 参数的情况下填充。与 storage_env 的发现逻辑平行但独立。
    discovered_api_env = found.get("api_env")
    if discovered_api_env:
        api_env_source = profile.sources.get("api_env")
        if api_env_source not in ("explicit", "env"):
            profile.api_env = discovered_api_env
            profile.sources["api_env"] = "discovery"

    return profile


def require(profile: Profile, field: str, *, action: str) -> str:
    """取某个必需的寻址字段；缺失时抛出带完整诊断信息的 ``SchemaError``。

    ``action`` 用于说明是哪个操作需要它（如 ``"上传实例内容"``），让报错自解释。
    """
    value = getattr(profile, field, "") or ""
    if value:
        return value
    if profile.cluster:
        tried = (f"已按 AP_CLUSTER={profile.cluster!r} 向 "
                 f"{profile.api_base or '<未配置的 apiserver 地址>'} 查询 repo-config，"
                 f"但返回里没有 {field}")
    elif profile.storage_env:
        tried = (f"已按 INSTANCE_REPO_STORAGE_ENV={profile.storage_env!r} 向 "
                 f"{profile.api_base or '<未配置的 apiserver 地址>'} 查询 repo-config，"
                 f"但返回里没有 {field}")
    else:
        tried = "未配置 IR_STORAGE_ENV，因此没有执行自动发现"
    # 如果自动发现本身失败了（网络错误 / 控制面错误 / 非法响应），把真实根因
    # 追加到报错消息里——否则用户只看到"返回里没有 acr_host"，完全看不到底层
    # 是 TCP 连接失败或 HTML 响应被当成空 dict。
    detail = ""
    if profile.discovery_error:
        detail = f"（自动发现失败：{profile.discovery_error}）"
    raise SchemaError(
        f"{action} 需要 {field}，但当前未解析出取值：{tried}{detail}。"
        f"两条出路：① 配置 AP_CLUSTER 或 INSTANCE_REPO_STORAGE_ENV"
        f"（旧别名 IR_STORAGE_ENV；推荐，让 SDK 自动发现）；"
        f"② 显式覆盖 Repo(profile_overrides={{'{field}': '<值>'}})。")
