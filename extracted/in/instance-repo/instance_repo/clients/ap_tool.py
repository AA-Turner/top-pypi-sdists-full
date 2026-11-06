"""Exact key builder/parser for the currently registered RewardKit profile.

Only pyz/tf-rewardkit/rewardkit-VERSION-linux-x86_64.pyz is supported under
swe/user-data/ap-tool/. VERSION uses the approved verbatim PEP440 subset;
component/version128bytes, full key512bytes. No hash/fileID/version directory,
normalization, percent decoding, extra tool registration or platform expansion.
"""
from __future__ import annotations

import re

from ..errors import SchemaError

#: ap-tool 域根（不可变；层级含义=ap-tool/包类型/工具名/文件名）。
TOOL_KEY_ROOT = "swe/user-data/ap-tool/"

#: 默认包类型（当前唯一正式类型；新类型须用户明确同意后扩展）。
DEFAULT_TOOL_KIND = "pyz"

#: tf-rewardkit 的文件名 stem（发布名=工具名去 ``tf-`` 前缀，H1 逐字节锚定）。

#: 工具名：小写字母开头，小写/数字/连字符（tf-rewardkit、t-rewardkit-2 等）。
# fullmatch：``tf-rewardkit.``/``tf rewardkit``/``tf\u2044rewardkit`` 全部拒收。
_TOOL_NAME_RE = re.compile(r"[a-z](?:[a-z0-9-]*[a-z0-9])?")

#: 包类型：纯小写字母（pyz；类型层不是自由命名空间）。
_KIND_RE = re.compile(r"[a-z]+")

#: 版本串：PEP440 **canonical** 形态（与真实 RewardKit publisher 对齐，
# Codex 退修 2026-10-30：已发版 1.1.0.dev2 必须支持；rc/post/local 支持）。
# canonical = N(.N)*[{a|b|rc}N][.postN][.devN][+local]——全部小写、无空白；
# local 段限定小写字母/数字/点（**禁连字符**：``-`` 是文件名中 version 与
# platform 的唯一分隔符，local 含 ``-`` 会造成 parse 歧义——``1.2.3+a-b`` 
# 无法区分 local 边界与 platform 开头，fail-closed 拒绝；PEP440 允许更宽的
# local 字符集，本协议收窄到文件名无歧义子集）；大写/下划线等非 canonical
# 形态直接拒绝——不做归一化，调用方必须传 canonical（零静默改写，
# "No silent normalization"）。
# 版本中的点属于版本语法本身——段字符白名单不适用于 version（单独校验）。
_VERSION_EPOCH = r"(?:0|[1-9][0-9]*)"
_VERSION_PRE = r"(?:(?:a|b|rc)(?:0|[1-9][0-9]*))?"
_VERSION_POST = r"(?:\.(?:post|rev|r)(?:0|[1-9][0-9]*))?"
_VERSION_DEV = r"(?:\.dev(?:0|[1-9][0-9]*))?"
_VERSION_LOCAL = r"(?:\+[a-z0-9]+(?:\.[a-z0-9]+)*)?"
_VERSION_RE = re.compile(
    _VERSION_EPOCH + r"(?:\." + _VERSION_EPOCH + r")*"
    + _VERSION_PRE + _VERSION_POST + _VERSION_DEV + _VERSION_LOCAL)

#: 平台串：小写/数字/连字符/下划线（linux-x86_64、linux-aarch64）。
_PLATFORM_RE = re.compile(r"[a-z0-9](?:[a-z0-9_-]*[a-z0-9_])?")

#: 文件名整体（stem-version-platform.pyz）：自右锚定，version 段为 PEP440
#: canonical 形态（含 dev/rc/post/local；点与 ``+`` 属版本语法，不与
#: stem 的 ``-`` 分隔混淆——分隔符仍为 ``-``，platform 无点无 ``+``）。
_FILENAME_RE = re.compile(
    r"(?P<stem>[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"
    r"-(?P<version>" + _VERSION_EPOCH + r"(?:\." + _VERSION_EPOCH + r")*"
    + _VERSION_PRE + _VERSION_POST + _VERSION_DEV + _VERSION_LOCAL + r")"
    r"-(?P<platform>[a-z0-9](?:[a-z0-9_-]*[a-z0-9_])?)"
    r"\.pyz")

#: 组件段长上限（字节）：tool_name/kind/platform 等段共用——与 API 侧
#: shared component 界限同值（128；Codex 03:30 统一裁定，替代先前的
#: 先行值 256）。防御异常超长输入（对齐 shared 路径安全风格）。
_MAX_SEGMENT_BYTES = 128

#: 最大版本串长度（字节，=A 侧 sharedNameVersionMaxLen=128；Codex 03:30
#: 统一裁定：64→128 放开——此前 64 是 B 侧先行值非约定，**勿任意收窄已
#: 约定有效版本**）。
MAX_VERSION_BYTES = 128

#: 最大文件名长度（字节）：'pyz'+'-'+tool_name(≤128)+'-'+filename(≤388)
#: 的组成上界 ≈ 496，与整 key 界限 512 严格相容（不出现"filename 合法
#: 但 key 必然越界"的死区）；生成侧与 parse 侧共用同一界限。
MAX_FILENAME_BYTES = 388

#: 整 key 长度（字节，=A/API 既有 key 上限 512；parse 前置检查——超长
#: key 在任何正则/切分前拒绝。Codex 03:30 统一裁定：1024→512）。
MAX_KEY_BYTES = 512


def _validate_segment(value: str, what: str, regex: re.Pattern) -> str:
    """通用段校验：非空、长度有界、无首尾空白、白名单 fullmatch。

    **不解码不变式**：``%`` 不在任何白名单字符集内——``%2e%2e``/``%2F``/
    ``%252e`` 在此被字面拒绝；控制符/空白/反斜杠/非 ASCII（含 Unicode
    斜杠变体）同理（字符集仅 ASCII 小写字母/数字/连字符/点/下划线子集）。
    """
    if not isinstance(value, str):
        raise SchemaError("ap-tool key component must be a string")
    v = value
    if not v:
        raise SchemaError(f"ap-tool key segment {what!r} must not be empty")
    if len(v.encode("utf-8")) > _MAX_SEGMENT_BYTES:
        raise SchemaError(
            f"ap-tool key segment {what!r} exceeds "
            f"{_MAX_SEGMENT_BYTES} bytes: {v!r}")
    if v != v.strip():
        raise SchemaError(
            f"ap-tool key segment {what!r} has leading/trailing "
            f"whitespace: {v!r}")
    if regex.fullmatch(v) is None:
        raise SchemaError(
            f"invalid ap-tool key segment {what!r}: {v!r} (allowed charset "
            "is a restrictive ASCII subset; percent-encodings, uppercase, "
            "whitespace, slashes and unicode variants are rejected "
            "literally without decoding)")
    return v


def validate_tool_version(version: str) -> str:
    """校验版本串：PEP440 **canonical** 形态（与 RewardKit publisher 对齐）。

    合法：``1.2.3``、``1.1.0.dev2``（已发版）、``1.2.3rc1``、``1.2.3.post1``、
    ``1.0a1``、``1.2.3+local.7``（local 限定小写/数字/点/连字符子集）。
    拒绝：非 canonical（``1.2.3.RC1`` 大写、``1.2.3-rc1`` 连字符分隔、
    ``1.02.3`` 前导零、``v1.2`` 前缀、``1.2.3..post1`` 空段）、斜杠/点段
    路径形态、编码逃逸（``%`` 不在字符集）、控制符、空白。
    **零静默归一化**：版本原样进入 key（canonical 要求由调用方保证——
    非 canonical 输入被拒而非被改写；validate 返回值恒等于输入原串）。
    """
    if not isinstance(version, str):
        raise SchemaError("ap-tool version must be a string")
    v = version
    if not v:
        raise SchemaError("ap-tool version must not be empty")
    # 长度界限先于任何正则（Codex 边界 review：超长数字版本曾通过）。
    if len(v.encode("utf-8")) > MAX_VERSION_BYTES:
        raise SchemaError(
            f"ap-tool version exceeds {MAX_VERSION_BYTES} bytes: "
            f"{len(v.encode('utf-8'))} bytes")
    if v != v.strip():
        raise SchemaError(
            f"invalid ap-tool version {v!r}: leading/trailing whitespace")
    if _VERSION_RE.fullmatch(v) is None:
        raise SchemaError(
            f"invalid ap-tool version {v!r}: must be PEP440 canonical "
            "(e.g. 1.2.3, 1.1.0.dev2, 1.2.3rc1, 1.2.3.post1, "
            "1.2.3+local; no leading zeros, uppercase, hyphen separators, "
            "prefix letters or escapes)")
    return v


def validate_tool_platform(platform: str) -> str:
    """校验平台串：小写字母/数字/连字符/下划线（linux-x86_64 等）。"""
    return _validate_segment(platform, "platform", _PLATFORM_RE)


def validate_tool_name(tool_name: str) -> str:
    """校验工具名：小写字母开头的小写/数字/连字符段（tf-rewardkit 等）。"""
    return _validate_segment(tool_name, "tool_name", _TOOL_NAME_RE)


def validate_tool_kind(kind: str) -> str:
    """校验包类型段：纯小写字母（pyz）。新类型须用户明确同意后扩展。"""
    return _validate_segment(kind, "kind", _KIND_RE)


def tool_filename(tool_name: str, version: str, *,
                  platform: str = "linux-x86_64") -> str:
    """version→文件名映射（协议锚定；version **verbatim** 原样入名）。

    tf-rewardkit + 1.1.0.dev2 → ``rewardkit-1.1.0.dev2-linux-x86_64.pyz``；
    tf-rewardkit + 1.2.3 → ``rewardkit-1.2.3-linux-x86_64.pyz``：
    Registered tool identity maps tf-rewardkit directory to rewardkit artifact.版本串不做任何
    归一化改写（canonical 由 validate 保证，文件名所见即调用方所传）。
    """
    name = validate_tool_name(tool_name)
    ver = validate_tool_version(version)
    plat = validate_tool_platform(platform)
    if name != "tf-rewardkit" or plat != "linux-x86_64":
        raise SchemaError("unsupported tool profile; only tf-rewardkit/linux-x86_64 is registered")
    stem = "rewardkit"
    if not stem:
        raise SchemaError(
            f"invalid ap-tool tool_name {tool_name!r}: 'tf-' alone has no "
            "file stem")
    filename = f"{stem}-{ver}-{plat}.pyz"
    # 生成侧界限（Codex 边界 review 2026-10-31）：合成文件名超过上限拒绝。
    if len(filename.encode("utf-8")) > MAX_FILENAME_BYTES:
        raise SchemaError(
            f"ap-tool filename exceeds {MAX_FILENAME_BYTES} bytes: "
            f"{len(filename.encode('utf-8'))} bytes")
    return filename


def tool_object_key(tool_name: str, version: str, *,
                    kind: str = DEFAULT_TOOL_KIND,
                    platform: str = "linux-x86_64") -> str:
    """正式工具对象 key（唯一入口；两桶同 key 的单一来源）。

    例：``tool_object_key("tf-rewardkit", "1.2.3")`` 逐字节返回
    ``swe/user-data/ap-tool/pyz/tf-rewardkit/rewardkit-1.2.3-linux-x86_64.pyz``；
    ``tool_object_key("tf-rewardkit", "1.1.0.dev2")`` 逐字节返回
    ``swe/user-data/ap-tool/pyz/tf-rewardkit/rewardkit-1.1.0.dev2-linux-x86_64.pyz``
    （实际已发版 key，roundtrip 锚点；A 报告 §8.4 H1-H5 同构）。

    设计约束（差异B §6.2）：SHA/size/generation 不入路径；调用方对主/从桶
    复用**同一返回值**（结构上杜绝两桶 key 分叉）。
    """
    name = validate_tool_name(tool_name)
    k = validate_tool_kind(kind)
    if k != "pyz":
        raise SchemaError("unsupported tool package; only pyz is registered")
    filename = tool_filename(tool_name, version, platform=platform)
    key = f"{TOOL_KEY_ROOT}{k}/{name}/{filename}"
    # 整 key 界限（生成侧；parse 侧同界限前置——两侧同一常量）。
    if len(key.encode("utf-8")) > MAX_KEY_BYTES:
        raise SchemaError(
            f"ap-tool key exceeds {MAX_KEY_BYTES} bytes: "
            f"{len(key.encode('utf-8'))} bytes")
    return key


def parse_tool_object_key(key: str) -> dict:
    """解析正式 key 为协议字段（消费侧对账/下载 URL 校验用，H2 同口径）。

    返回 ``{tool_name, kind, version, platform, filename}``；任何偏离协议
    模板的 key（域根下段数≠3、非 pyz 扩展、文件名不匹配
    ``stem-version-platform.pyz``、stem 与 tool_name 不一致）拒绝——用于把
    download URL / 回执 final_key 与正式协议三方对账（A 报告 H2/H3）。
    """
    v = str(key or "")
    # parse 前置整 key 界限（Codex 边界 review 2026-10-31：先于任何正则/
    # 切分——超长 key 在最前面拒绝，不进入解析路径）。
    if len(v.encode("utf-8")) > MAX_KEY_BYTES:
        raise SchemaError(
            f"ap-tool key exceeds {MAX_KEY_BYTES} bytes: "
            f"{len(v.encode('utf-8'))} bytes")
    if not v.startswith(TOOL_KEY_ROOT):
        raise SchemaError(
            f"key {v!r} is not under ap-tool root {TOOL_KEY_ROOT!r}")
    rest = v[len(TOOL_KEY_ROOT):]
    segs = rest.split("/")
    if len(segs) != 3:
        raise SchemaError(
            f"ap-tool key must have exactly 3 segments under the root "
            f"(kind/tool_name/filename), got {len(segs)}: {v!r}")
    kind, name, filename = segs
    validate_tool_kind(kind)
    validate_tool_name(name)
    # parse 侧文件名界限（先于 _FILENAME_RE——与生成侧同常量）。
    if len(filename.encode("utf-8")) > MAX_FILENAME_BYTES:
        raise SchemaError(
            f"ap-tool key filename exceeds {MAX_FILENAME_BYTES} bytes: "
            f"{len(filename.encode('utf-8'))} bytes")
    if not filename.endswith(".pyz"):
        raise SchemaError(
            f"ap-tool key filename must end with .pyz: {filename!r}")
    m = _FILENAME_RE.fullmatch(filename)
    if m is None:
        raise SchemaError(
            f"ap-tool key filename malformed (expected "
            f"stem-version-platform.pyz): {filename!r}")
    stem = m.group("stem")
    expected_stem = name[len("tf-"):] if name.startswith("tf-") else name
    if stem != expected_stem:
        raise SchemaError(
            f"ap-tool key filename stem {stem!r} does not match tool_name "
            f"{name!r} (expected {expected_stem!r})")
    validate_tool_version(m.group("version"))
    validate_tool_platform(m.group("platform"))
    if tool_object_key(name, m.group("version"), kind=kind, platform=m.group("platform")) != v:
        raise SchemaError("ap-tool key does not match registered tool profile")
    return {"tool_name": name, "kind": kind, "version": m.group("version"),
            "platform": m.group("platform"), "filename": filename}
