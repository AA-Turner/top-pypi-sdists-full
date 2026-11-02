"""validate.py — Instance 本地校验（Layout / SWE JSON / Custom），纯本地无网络。

三种格式自动检测（detect_format）：
    - harbor（目录 + task.toml）：instruction.md · task.toml · environment/Dockerfile · tests/test.sh|test.ps1
    - swe（单 JSON 文件）：instance_id + docker_image 必备；数据和元数据合一
    - custom（目录无 task.toml / 单 JSON 文件 freeform）：仅强约束 instance_id；
      元数据 freeform，push 时目录输入由 SDK 生成最小 JSON、JSON 输入原样上传

测试脚本兼容 Linux（tests/test.sh）与 Windows（tests/test.ps1），二者至少其一。
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py<3.11 回退
    import tomli as tomllib  # type: ignore

from .errors import LayoutError, SchemaError

# ── 通用安全校验 ─────────────────────────────────────────────────────────────

# instance_id 允许的字符集：字母、数字、连字符、下划线、点号。
# 显式排除 / \ .. 和空白，防止路径注入（OSS key 由 SDK 拼接 instance_id 构成）。
_INSTANCE_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.\-]*$")
_INSTANCE_ID_MAX_LEN = 256


def validate_instance_id(instance_id: str, source: str = "") -> None:
    """校验 instance_id 安全性：不含路径注入字符、不超长、不为空。

    source 用于错误消息中标识来源（如文件名）。
    """
    ctx = f" (from {source})" if source else ""
    if not instance_id:
        raise SchemaError(f"instance_id is empty{ctx}")
    if len(instance_id) > _INSTANCE_ID_MAX_LEN:
        raise SchemaError(
            f"instance_id too long ({len(instance_id)} > {_INSTANCE_ID_MAX_LEN}){ctx}")
    if ".." in instance_id:
        raise SchemaError(f"instance_id must not contain '..'{ctx}: {instance_id!r}")
    if not _INSTANCE_ID_RE.match(instance_id):
        raise SchemaError(
            f"instance_id contains invalid characters{ctx}: {instance_id!r} "
            f"(allowed: [a-zA-Z0-9_.-], must start with alphanumeric)")


# ── 格式检测 ─────────────────────────────────────────────────────────────────

def detect_format(local_path: str | Path) -> Literal["harbor", "swe", "custom"]:
    """自动检测输入格式：

    - 目录 + 含 task.toml → harbor
    - 目录 + 不含 task.toml → custom（用户自定义格式，SDK 不校验具体字段）
    - .json 文件 → swe

    不做内容校验（那是 check_layout / check_swe_json / check_custom 的责任）。
    """
    p = Path(local_path)
    if p.is_dir():
        return "harbor" if (p / "task.toml").is_file() else "custom"
    if p.is_file() and p.suffix.lower() == ".json":
        return "swe"
    if not p.exists():
        raise LayoutError(f"path does not exist: {p}")
    raise SchemaError(
        f"unrecognized instance format: {p} "
        f"(expected a directory for harbor/custom or a .json file for swe)")


# ── Harbor 格式校验 ──────────────────────────────────────────────────────────

REQUIRED_FILES = (
    "instruction.md",
    "task.toml",
    "environment/Dockerfile",
)

# "多选一"必备组：每组内至少存在一个文件即可。测试脚本按平台二选一：
# Linux → tests/test.sh，Windows → tests/test.ps1。
REQUIRED_ONE_OF = (
    ("tests/test.sh", "tests/test.ps1"),
)


@dataclass
class ValidationReport:
    """Harbor 格式校验结果。"""
    instance_id: str
    format: str = "harbor"
    ok: bool = True
    missing: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


def check_layout(local_dir: str | Path) -> ValidationReport:
    """校验目录符合 harbor 格式并解析 task.toml [metadata]。缺 MUST 文件抛
    LayoutError；task.toml 非法抛 SchemaError。"""
    d = Path(local_dir)
    if not d.is_dir():
        raise LayoutError(f"not a directory: {d}")
    missing = [rel for rel in REQUIRED_FILES if not (d / rel).is_file()]
    for group in REQUIRED_ONE_OF:
        if not any((d / rel).is_file() for rel in group):
            missing.append(" | ".join(group))  # 展示为"其一"，如 tests/test.sh | tests/test.ps1
    if missing:
        raise LayoutError(f"{d.name}: missing required files: {missing}")
    tp = d / "task.toml"
    try:
        with open(tp, "rb") as f:
            toml = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise SchemaError(f"{d.name}: task.toml is not valid TOML: {e}") from e
    meta = toml.get("metadata", {})
    if not isinstance(meta, dict):
        raise SchemaError(f"{d.name}: task.toml [metadata] must be a table")
    instance_id = d.name
    validate_instance_id(instance_id, source=str(d))
    return ValidationReport(instance_id=instance_id, ok=True, missing=[], metadata=meta)


# ── SWE 格式校验 ─────────────────────────────────────────────────────────────

# SWE JSON 的最低必备字段（能让 ingest enrich 正常工作 + 能构造 OSS key）。
SWE_REQUIRED_FIELDS = ("instance_id",)

# 有 docker_image 的 SWE 实例（大部分），ingest 会从中提取镜像引用。
# 不做硬性要求（有些数据集如纯文本 benchmark 可能没有镜像），只在缺失时 warn。


@dataclass
class SWEValidationReport:
    """SWE 格式校验结果。"""
    instance_id: str
    format: str = "swe"
    ok: bool = True
    warnings: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    raw_data: dict = field(default_factory=dict)  # 解析后的完整 JSON（push 时需要）


def check_swe_json(json_path: str | Path) -> SWEValidationReport:
    """校验单 JSON 文件符合 SWE 格式。

    强制要求：
    - 合法 UTF-8 JSON，根为 object
    - 有 instance_id 字段且非空
    - instance_id 通过安全校验（无路径注入字符）
    - 文件名（去 .json 后缀）必须等于 instance_id（防止 ingest 用文件名 dedup 时错乱）

    推荐字段（缺失时 warn 不 error）：docker_image
    """
    p = Path(json_path)
    if not p.is_file():
        raise LayoutError(f"not a file: {p}")
    if p.suffix.lower() != ".json":
        raise SchemaError(f"SWE instance must be a .json file, got: {p.name}")

    try:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
    except UnicodeDecodeError as e:
        raise SchemaError(
            f"{p.name}: not valid UTF-8 (SWE JSON must be UTF-8 without BOM): {e}") from e
    except json.JSONDecodeError as e:
        raise SchemaError(f"{p.name}: invalid JSON: {e}") from e

    if not isinstance(data, dict):
        raise SchemaError(f"{p.name}: JSON root must be an object, got {type(data).__name__}")

    # 必备字段
    for fld in SWE_REQUIRED_FIELDS:
        val = data.get(fld)
        if not val or (isinstance(val, str) and not val.strip()):
            raise SchemaError(f"{p.name}: required field '{fld}' missing or empty")

    instance_id = data["instance_id"]
    if not isinstance(instance_id, str):
        raise SchemaError(
            f"{p.name}: instance_id must be a string, got {type(instance_id).__name__}")
    instance_id = instance_id.strip()
    validate_instance_id(instance_id, source=p.name)

    # 强制：文件名（去后缀）必须等于 instance_id，否则 ingest 用文件名做 dedup 时会错乱
    stem = p.stem  # 文件名去 .json
    if stem != instance_id:
        raise SchemaError(
            f"{p.name}: filename stem '{stem}' does not match instance_id "
            f"'{instance_id}' — file must be named '{instance_id}.json'")

    # 推荐字段（warn）
    warnings: list[str] = []
    if not data.get("docker_image"):
        warnings.append("missing 'docker_image' field (ingest won't populate image reference)")

    metadata: dict = {}
    for key in ("docker_image", "language", "difficulty"):
        val = data.get(key)
        if val is not None and not isinstance(val, str):
            warnings.append(f"'{key}' should be string, got {type(val).__name__} (will be set to None)")
            metadata[key] = None
        else:
            metadata[key] = val

    return SWEValidationReport(
        instance_id=instance_id, ok=True, warnings=warnings,
        metadata=metadata, raw_data=data)


# ── Custom 格式校验（用户自定义，freeform） ─────────────────────────────────

CUSTOM_SCHEMA_VERSION = "1.0"


@dataclass
class CustomValidationReport:
    """Custom 格式校验结果。"""
    instance_id: str
    format: str = "custom"
    ok: bool = True
    metadata: dict = field(default_factory=dict)  # 目录输入时 SDK 生成；JSON 输入时原样解析
    raw_data: dict = field(default_factory=dict)  # JSON 输入时的原始数据；目录输入时为空
    source: str = "directory"                     # "directory" 或 "json"


def check_custom(local_path: str | Path) -> CustomValidationReport:
    """校验 custom 格式输入。

    两种输入形态：

    - 目录：``instance_id`` = 目录名（强约束 charset），元数据由 SDK push 时生成
      （最小 schema：``instance_id`` / ``metadata_model`` / ``schema_version`` /
      ``created_at`` / ``updated_at``）。
    - ``.json`` 文件：必须含 ``instance_id`` 字段且与文件名 stem 一致；其余字段
      freeform，push 时原样上传。
    """
    p = Path(local_path)
    if p.is_dir():
        instance_id = p.name
        validate_instance_id(instance_id, source=str(p))
        return CustomValidationReport(
            instance_id=instance_id, source="directory")
    if p.is_file() and p.suffix.lower() == ".json":
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
        except UnicodeDecodeError as e:
            raise SchemaError(
                f"{p.name}: not valid UTF-8: {e}") from e
        except json.JSONDecodeError as e:
            raise SchemaError(f"{p.name}: invalid JSON: {e}") from e
        if not isinstance(data, dict):
            raise SchemaError(
                f"{p.name}: JSON root must be an object, got {type(data).__name__}")
        raw_id = data.get("instance_id")
        if not raw_id or (isinstance(raw_id, str) and not raw_id.strip()):
            raise SchemaError(f"{p.name}: required field 'instance_id' missing or empty")
        if not isinstance(raw_id, str):
            raise SchemaError(
                f"{p.name}: instance_id must be a string, got {type(raw_id).__name__}")
        instance_id = raw_id.strip()
        validate_instance_id(instance_id, source=p.name)
        stem = p.stem
        if stem != instance_id:
            raise SchemaError(
                f"{p.name}: filename stem '{stem}' does not match instance_id "
                f"'{instance_id}' — file must be named '{instance_id}.json'")
        return CustomValidationReport(
            instance_id=instance_id, source="json",
            metadata=dict(data), raw_data=dict(data))
    if not p.exists():
        raise LayoutError(f"path does not exist: {p}")
    raise SchemaError(
        f"custom format expects a directory or .json file, got: {p}")
