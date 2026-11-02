"""Instance metadata, directory browsing, transfer and source-hash commands.

SDK imports are lazy so help remains available without Dataset support.
Local validation and hashing do not construct a Repo or contact AP.
Remote operations share SDK configuration and the CLI output/error contract.
"""

from __future__ import annotations

import inspect
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, List, Optional

import typer

__all__ = ["instance_app", "register"]

instance_app = typer.Typer(help="Dataset instance operations")


def register(app: typer.Typer) -> None:
    """把 ``instance`` 挂到 ``ap`` 根命令上。"""
    app.add_typer(instance_app, name="instance")


# ---------------------------------------------------------------------------
# 共用 helper
# ---------------------------------------------------------------------------

#: 上游 §9.2 的默认列,顺序不可改(设计 §5)。
_INSTANCE_COLUMNS: tuple[tuple[str, str], ...] = (
    ("instance", "INSTANCE"),
    ("split", "SPLIT"),
    ("version", "VERSION"),
    ("digest", "DIGEST"),
    ("updated_at", "UPDATED_AT"),
    ("registered", "REGISTERED"),
)

_FORMAT_HELP = "Output format: plain/table/json/yaml (default: AP_FORMAT or command default)"

_VERSION_HELP = (
    "Dataset version. Omitting it means the version-less space "
    "(split_first) - it never implies 'latest'."
)


from . import instance_options  # noqa: E402
from .dataset_commands import (  # noqa: E402
    _ENVIRONMENT_HELP,
    _METADATA_MODEL_HELP,
    _version_label,  # noqa: E402
)
from .repo_read_guard import oss_fallback_kwargs  # noqa: E402


def _fmt(output_format: Optional[str]) -> str:
    from .cli import _normalize_output_format

    return _normalize_output_format(output_format, keep_table=True)


def _environment(value: Optional[str]) -> str:
    """``--environment`` 归一(与 dataset 命令同一口径:缺省 online)。"""
    from .dataset_commands import _environment as _dataset_environment

    return _dataset_environment(value)


def _metadata_model(value: Optional[str]) -> str:
    """``--metadata-model`` 归一(与 dataset 命令同一口径:没给就不下发)。"""
    from .dataset_commands import _metadata_model as _dataset_metadata_model

    return _dataset_metadata_model(value)


def _metadata_model_for_split(value: Optional[str], *, split: str) -> str:
    """``--metadata-model``;缺省不下发,**唯一例外是显式传空 split**。

    split_first 按 dataset/split 寻址 split 记录,空 split 在服务端直接报
    ``split is required``——"版本下没有 split 归属、直接挂在 version 上的实例"这套
    存量布局只有 version_first 认。所以 ``--split ""`` 时下发 version_first 保住既有
    行为;其它情况一律不下发,由 SDK 按 profile 派生(当前为 split_first)。
    """
    explicit = _metadata_model(value)
    if explicit:
        return explicit
    return "version_first" if not str(split or "").strip() else ""


def _model_dict(record: Any) -> dict:
    from .dataset_commands import _model_dict as _dataset_model_dict

    return _dataset_model_dict(record)


def _pagination_envelope(result: Any) -> dict:
    from .dataset_commands import _pagination_envelope as _dataset_pagination_envelope

    return _dataset_pagination_envelope(result)


def _fail(message: str, hint: str, exit_code: int = 1) -> "typer.Exit":
    """打设计 §5 的固定两行文案到 stderr 并返回待 raise 的 ``typer.Exit``。"""
    typer.echo(f"error: {message}", err=True)
    typer.echo(f"hint: {hint}", err=True)
    return typer.Exit(exit_code)


def _path_value(value: Optional[str]) -> Optional[str]:
    try:
        return instance_options.relative_path(value)
    except ValueError as exc:
        raise _fail(str(exc), "Use --path solution, --path tests/sealed, or --path .", 2) from exc


def _enhanced_options(owner: Any, method: str, options: dict[str, Any]) -> dict[str, Any]:
    try:
        return instance_options.sdk_options(owner, method, options)
    except (TypeError, ValueError) as exc:
        raise _fail(
            str(exc), "Upgrade Dataset support: pip install --upgrade 'ap-client[dataset]'", 2
        ) from exc


def _load_repo_or_exit():
    """懒加载 SDK;缺 extra → 安装提示 + 退出码 2(设计 §2)。

    存储永远按集群绑定寻址(设计 §4.2);environment 不进 ``Repo`` 构造,
    由元数据参数与同侧校验分别承载。
    """
    from .irepo_sdk import SdkMissing, load_repo, sdk_error_exit

    try:
        return load_repo()
    except SdkMissing as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc
    except Exception as exc:  # noqa: BLE001 - SDK configuration errors use the CLI error contract
        sdk_error_exit(exc, what="storage config", stage="resolve")


def _probe_pull_private_endpoint(repo: Any, dataset: str) -> bool | None:
    content = getattr(repo, "_content", None)
    instances = getattr(repo, "instances", None)
    credentials = getattr(content, "_credentials", None)
    probe = getattr(content, "_probe_private_endpoint", None)
    layout_factory = getattr(instances, "_layout", None)
    if not all(callable(value) for value in (credentials, probe, layout_factory)):
        return None

    from instance_repo._routing import _plan_oss_route

    layout = layout_factory()
    sts = credentials(layout.sts_prefix(dataset), dataset)
    route = _plan_oss_route(sts.get("endpoint", ""))
    if not route.standard:
        return None
    return bool(probe(route.private_endpoint))


#: SDK ``instance_repo.validate.detect_format`` 的取值 → 对应校验函数名。分派必须与 SDK
#: ``InstancesClient.validate`` 一致;认不出的格式回退 ``check_layout``(与 SDK 同样的兜底)。
_VALIDATOR_BY_FORMAT: dict[str, str] = {
    "swe": "check_swe_json",
    "custom": "check_custom",
    "harbor": "check_layout",
}


def _load_validator() -> dict[str, Any]:
    """返回纯本地的 ``{detect_format, check_layout, check_swe_json, check_custom}``。

    设计 §4.4 要求 ``instance validate`` **零远端请求**。``repo.instances.validate``
    只是按格式分派到这几个纯本地函数,但拿到 ``repo`` 就得先构造 ``Repo``,而
    ``Repo.__init__`` 会做一次 repo-config 自动发现(HTTP)。所以这里直接取
    ``instance_repo.validate`` 的函数。

    **分派必须与 SDK 的 ``InstancesClient.validate`` 一致**(见 :func:`_validator_for`):
    SDK 增加格式时这里要同步,否则会把新格式错按 harbor 布局校验(``tests/test_instance_commands.py``
    里有一条与真 SDK 逐字对齐的用例守着)。
    """
    from .irepo_sdk import SdkMissing

    try:
        from instance_repo.validate import (
            check_custom,
            check_layout,
            check_swe_json,
            detect_format,
        )
    except ImportError as exc:
        raise SdkMissing() from exc
    return {
        "detect_format": detect_format,
        "check_layout": check_layout,
        "check_swe_json": check_swe_json,
        "check_custom": check_custom,
    }


def _validator_for(fmt: str, validators: dict[str, Any]):
    """按检测出的格式挑本地校验函数(与 SDK ``InstancesClient.validate`` 同分派)。"""
    return validators[_VALIDATOR_BY_FORMAT.get(str(fmt), "check_layout")]


def _validate_paths(paths: list[str]) -> list[dict]:
    """逐个校验本地路径,返回逐条结果(不抛业务异常)。"""
    try:
        validators = _load_validator()
    except Exception as exc:  # SdkMissing
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc

    results: list[dict] = []
    for raw in paths:
        record: dict[str, Any] = {"path": str(raw), "ok": False, "instance": "", "format": ""}
        try:
            fmt = validators["detect_format"](raw)
            report = _validator_for(fmt, validators)(raw)
            record["format"] = getattr(report, "format", fmt) or fmt
            record["instance"] = getattr(report, "instance_id", "") or ""
            record["ok"] = bool(getattr(report, "ok", True))
            missing = list(getattr(report, "missing", None) or [])
            if missing:
                record["ok"] = False
                record["error"] = f"missing required files: {missing}"
            else:
                record["error"] = ""
        except Exception as exc:  # noqa: BLE001 - 逐条汇报,不让首个失败中断整批
            record["error"] = _describe(exc)
        results.append(record)
    return results


def _describe(exc: BaseException) -> str:
    message = getattr(exc, "message", None)
    text = str(message or "").strip() or str(exc).strip()
    return text or type(exc).__name__


def _sdk_read_kwargs(sdk_obj: Any, method: str, *, environment: str, metadata_model: str) -> dict:
    """按 SDK 能力下发 environment / metadata_model，不允许静默忽略显式值。"""
    fn = getattr(sdk_obj, method, None)
    accepted: set[str] = set()
    if fn is not None:
        try:
            params = inspect.signature(fn).parameters
        except (TypeError, ValueError):  # pragma: no cover - 打桩异常形态
            params = {}
        for name, param in params.items():
            if param.kind is inspect.Parameter.VAR_KEYWORD:
                accepted.update(("environment", "metadata_model"))
            elif name in ("environment", "metadata_model"):
                accepted.add(name)

    kwargs: dict[str, str] = {}
    dropped: list[str] = []
    for key, value in (("environment", environment), ("metadata_model", metadata_model)):
        # ``auto`` 是 CLI 层取值:跟随集群绑定,不下发(服务端契约只有 online/pre)。
        if key == "environment" and value == "auto":
            continue
        # 空值不下发:CLI 不替 SDK 决定 metadata_model(见 dataset_commands._metadata_model)。
        if key in accepted and value:
            kwargs[key] = value
        elif value:
            dropped.append(key)
    if dropped:
        raise _fail(
            f"The installed instance-repo does not support per-call {'/'.join(dropped)}",
            "Upgrade to instance-repo 1.1.4 or newer and retry",
            exit_code=2,
        )
    return kwargs


def _instance_record(instance: Any) -> dict:
    """SDK ``DatasetInstance`` → 服务端 ``GET /datasets/instances`` 的字段形状。

    服务端字段集(``pkg/model/dataset_metadata.go`` 的 ``DatasetInstance``)是
    ``id / instance_id / dataset / version / split?(omitempty) / manifest / tags? /
    difficulty? / docker_image? / extend_meta? / feedbacks? / created_at / updated_at``;
    SDK 模型把版本放在 ``dataset_version``、给 ``split`` 补了 ``default`` 哨兵、另有服务端
    不返回的 ``schema_version`` —— 必须显式投影才能保持既有 JSON 契约(迁移前是原样透出)。
    """
    served = _model_dict(instance)
    split = str(served.get("split") or "").strip()
    record: dict[str, Any] = {
        "id": served.get("id"),
        "instance_id": served.get("instance_id", ""),
        "dataset": served.get("dataset", ""),
        "version": served.get("dataset_version", ""),
        "manifest": served.get("manifest") or [],
        "created_at": served.get("created_at"),
        "updated_at": served.get("updated_at"),
        "registered": served.get("registered", True),
    }
    if split and split != "default":  # SDK 的 default 哨兵 = 无 split,服务端不返回该键
        record["split"] = split
    for key in ("tags", "difficulty", "docker_image", "extend_meta", "feedbacks"):
        if served.get(key):
            record[key] = served[key]
    return {k: v for k, v in record.items() if v not in (None, "", [], {})}


def _instance_row(record: dict) -> dict:
    """把服务端 instance 记录投影成上游 §9.2 的默认列。"""
    return {
        "instance": record.get("instance_id") or record.get("id") or "",
        "split": record.get("split") or "",
        "version": record.get("dataset_version") or record.get("version") or "",
        "digest": _record_digest(record),
        "updated_at": record.get("updated_at") or "",
        "registered": record.get("registered", True),
    }


def _record_digest(record: dict) -> str:
    """取内容 digest:优先 ``digests`` 字典,回退 manifest 里带 digest 的条目。"""
    digests = record.get("digests")
    if isinstance(digests, dict):
        for key in ("content.tgz", "instance.json"):
            value = digests.get(key)
            if value:
                return str(value)
        for value in digests.values():
            if value:
                return str(value)
    manifest = record.get("manifest")
    if isinstance(manifest, list):
        for entry in manifest:
            if isinstance(entry, dict) and entry.get("content_digest"):
                return str(entry["content_digest"])
    return ""


def _print_table(rows: list[dict], columns, output_format: str) -> None:
    from .cli import _print_plain_table, _print_rich_table

    if output_format == "table":
        _print_rich_table(rows, list(columns))
    else:
        _print_plain_table(rows, list(columns))


def _emit(payload, rows, columns, output_format: str) -> None:
    """``json``/``yaml`` 打 payload;``plain``/``table`` 打固定列表格。"""
    from .cli import _print_formatted

    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
        return
    _print_table(rows, columns, output_format)


def _emit_detail(payload: dict, output_format: str) -> None:
    from .cli import _print_detail, _print_formatted

    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
    else:
        _print_detail(payload)


def _version_value(version: Optional[str]) -> str:
    """省略 ``--version`` 就是**无版本空间**(空串),绝不隐式取 latest(设计 §4.3/§4.4)。"""
    return (version or "").strip()


# ---------------------------------------------------------------------------
# ap instance
# ---------------------------------------------------------------------------


@instance_app.command("validate")
def instance_validate(
    paths: List[str] = typer.Argument(..., help="Local instance paths (directory or .json)"),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Validate local instances. Purely local - no dataset, version or split needed."""
    output_format = _fmt(output_format)
    results = _validate_paths(list(paths))
    failed = [record for record in results if not record["ok"]]

    columns = (
        ("path", "PATH"),
        ("instance", "INSTANCE"),
        ("format", "FORMAT"),
        ("ok", "OK"),
        ("error", "ERROR"),
    )
    _emit({"validated": results, "failed": len(failed)}, results, columns, output_format)

    if failed:
        raise _fail(
            f"{len(failed)}/{len(results)} instances failed local validation",
            "Fix the missing files or task.toml / instance JSON per the ERROR column above, then rerun",
        )


@instance_app.command("list")
def instance_list(
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    split: str = typer.Option(..., "--split", help="Split name (required for remote operations)"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    page: int = typer.Option(1, "--page", help="Page number"),
    page_size: int = typer.Option(50, "--page-size", help="Page size"),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    metadata_model: Optional[str] = typer.Option(
        None, "--metadata-model", help=_METADATA_MODEL_HELP
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List instance metadata (SDK-backed; split may be empty for the unversioned space)."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    resolved_version = _version_value(version)
    repo = _load_repo_or_exit()
    env = _environment(environment)
    read_kwargs = _sdk_read_kwargs(
        repo.instances,
        "list_paged",
        environment=env,
        metadata_model=_metadata_model_for_split(metadata_model, split=split),
    )
    try:
        read_kwargs.update(oss_fallback_kwargs(repo, repo.instances, "list_paged", env))
        result = repo.instances.list_paged(
            dataset,
            resolved_version,
            split=split,
            page=page,
            page_size=page_size,
            **read_kwargs,
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Failed to list instances of dataset {dataset} version {_version_label(resolved_version)}: "
            f"{_reason(exc)}",
            "Check --dataset/--version/--split and read permission, then retry",
        ) from exc

    records = [_instance_record(item) for item in (getattr(result, "items", None) or [])]
    rows = [_instance_row(record) for record in records]
    payload = {
        "dataset": dataset,
        "version": resolved_version,
        "split": split,
        "instances": records,
        "pagination": _pagination_envelope(result),
    }
    _emit(payload, rows, _INSTANCE_COLUMNS, output_format)


@instance_app.command("get")
def instance_get(
    instance: str = typer.Argument(..., help="Instance id"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    split: str = typer.Option(..., "--split", help="Split name (required for remote operations)"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    metadata_model: Optional[str] = typer.Option(
        None, "--metadata-model", help=_METADATA_MODEL_HELP
    ),
    path: Optional[str] = typer.Option(
        None,
        "--path",
        help="List a subdirectory relative to the instance assets; use '.' for the root",
    ),
    page_size: int = typer.Option(
        100, "--page-size", min=1, max=1000, help="Directory listing page size"
    ),
    max_pages: int = typer.Option(50, "--max-pages", min=1, help="Maximum directory listing pages"),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Show instance metadata and root assets; use --path to browse a directory."""
    from .irepo_sdk import _reason

    output_format = _fmt(output_format)
    resolved_path = _path_value(path)
    resolved_version = _version_value(version)
    repo = _load_repo_or_exit()
    env = _environment(environment)
    if resolved_path is not None:
        _list_instance_objects(
            repo,
            dataset,
            resolved_version,
            instance,
            split,
            resolved_path,
            env,
            _metadata_model_for_split(metadata_model, split=split),
            page_size,
            max_pages,
            output_format,
        )
        return
    read_kwargs = _sdk_read_kwargs(
        repo.instances,
        "get",
        environment=env,
        metadata_model=_metadata_model_for_split(metadata_model, split=split),
    )
    try:
        read_kwargs.update(oss_fallback_kwargs(repo, repo.instances, "get", env))
        record = repo.instances.get(
            dataset,
            resolved_version,
            instance,
            split=split,
            **read_kwargs,
        )
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        raise _fail(
            f"Failed to query instance {instance}: {_reason(exc)}",
            "Check --dataset/--version/--split and read permission, then retry",
        ) from exc
    if record is None:
        raise _fail(
            f"Failed to query instance {instance}: not found",
            f"Check the instance id: ap instance list --dataset {dataset} --split {split}",
        )
    _list_instance_objects(
        repo,
        dataset,
        resolved_version,
        instance,
        split,
        "",
        env,
        _metadata_model_for_split(metadata_model, split=split),
        page_size,
        max_pages,
        output_format,
        metadata=_instance_record(record),
    )


def _list_instance_objects(
    repo: Any,
    dataset: str,
    version: str,
    instance: str,
    split: str,
    path: str,
    environment: str,
    metadata_model: str,
    page_size: int,
    max_pages: int,
    output_format: str,
    *,
    metadata: dict | None = None,
) -> None:
    from .irepo_sdk import _reason

    kwargs = _enhanced_options(
        repo.instances,
        "list_objects",
        {
            "version": version,
            "path": path,
            "page_size": page_size,
            "max_pages": max_pages,
        },
    )
    kwargs.update(
        _sdk_read_kwargs(
            repo.instances, "list_objects", environment=environment, metadata_model=metadata_model
        )
    )
    try:
        result = repo.instances.list_objects(dataset, instance, split=split, **kwargs)
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"Failed to list instance {instance} directory {path or '.'}: {_reason(exc)}",
            "Check the instance, directory, environment and read permission",
        ) from exc
    payload = _model_dict(result)
    payload.update(instance=instance, path=path or ".")
    rows = [dict(item, type="directory", size_bytes="") for item in payload.get("directories", [])]
    rows.extend(dict(item, type="file") for item in payload.get("files", []))
    from .manifest_view import _visible

    rows = [
        {key: _visible(value) if isinstance(value, str) else value for key, value in row.items()}
        for row in rows
    ]
    if metadata is not None and output_format in ("json", "yaml"):
        _emit_detail(dict(metadata, objects=payload), output_format)
    else:
        if metadata is not None:
            manifest = metadata.get("manifest")
            if isinstance(manifest, list):
                from .manifest_view import manifest_lines

                _emit_detail(
                    {key: value for key, value in metadata.items() if key != "manifest"},
                    output_format,
                )
                typer.echo()
                for line in manifest_lines(manifest):
                    typer.echo(line)
            else:
                _emit_detail(metadata, output_format)
            typer.echo("\nassets: .")
        _emit(
            payload,
            rows,
            (("type", "TYPE"), ("name", "NAME"), ("path", "PATH"), ("size_bytes", "BYTES")),
            output_format,
        )
    if payload.get("truncated"):
        typer.echo(
            "warning: directory listing is incomplete; increase --max-pages and retry", err=True
        )


def _check_version_autocreate(repo, dataset: str, version: str, *, environment: str) -> bool:
    """version 不存在时 push 会触发服务端自动创建;返回是否将发生自动创建。

    ``repo`` 由调用方构造并复用:``Repo.__init__`` 会做一次 best-effort 的
    repo-config 自动发现(HTTP),确认与推送共用一个实例,不重复触网。
    预检查是元数据读,按 ``environment`` 显式路由(``auto`` 省略下发)。
    """
    from .dataset_commands import _env_kwargs, _version_label
    from .irepo_sdk import _reason

    if not str(version or "").strip():
        # 无版本空间:没有"版本会被自动创建"这回事(数据面由 ingest 处理)。
        return False
    try:
        repo.versions.get(dataset, version, **_env_kwargs(environment))
    except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
        # 只有"版本不存在"(92002)才走自动创建;其它错误如实报错,不静默当成不存在。
        if getattr(exc, "biz_code", None) != 92002:
            raise _fail(
                f"Failed to read the status of dataset {dataset} version {_version_label(version)}: {_reason(exc)}",
                "Check the cluster and read permission, then retry",
            ) from exc
        return True
    return False


def _confirm_upload(
    dataset: str,
    version: str,
    split: str,
    count: int,
    *,
    yes: bool,
    auto_create: bool,
    prune: bool = False,
) -> None:
    """push 写远端前统一二次确认(可 ``-y/--yes`` 跳过),与 split publish 同口径。"""
    if yes:
        return
    label = _version_label(version)
    target = f"dataset {dataset} version {label} split {split}"
    note = f" Version {label} does not exist and will be auto-created." if auto_create else ""
    if prune:
        note += (
            " Remote instance records absent from these paths will be removed; OSS files remain."
        )
    if not sys.stdin.isatty():
        raise _fail(
            f"Uploading {count} instance(s) to {target} requires confirmation.{note}",
            "Add --yes (-y) to confirm the upload",
            exit_code=2,
        )
    if not typer.confirm(f"Upload {count} instance(s) to {target}?{note}"):
        raise _fail(
            "Upload canceled; nothing was written remotely",
            "Rerun with -y/--yes to skip the confirmation",
            1,
        )


@instance_app.command("push")
def instance_push(
    paths: List[str] = typer.Argument(..., help="Local instance paths (directory or .json)"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    split: str = typer.Option(..., "--split", help="Split name (required for remote operations)"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    overwrite: bool = typer.Option(False, "--overwrite", help="Allow overwriting existing objects"),
    skip_unchanged: bool = typer.Option(
        False, "--skip-unchanged", help="Skip cases with matching source hashes"
    ),
    content_hashes: Optional[str] = typer.Option(
        None, "--content-hashes", help="JSON file mapping instance IDs to source hashes"
    ),
    compress_level: Optional[int] = typer.Option(
        None,
        "--compress-level",
        min=1,
        max=9,
        help="Gzip compression level; 1 is fastest, 9 is smallest",
    ),
    concurrency: int = typer.Option(8, "--concurrency", min=1, help="Concurrent instance uploads"),
    continue_on_error: bool = typer.Option(
        False, "--continue-on-error", help="Finish other uploads and report failed cases"
    ),
    progress: bool = typer.Option(False, "--progress", help="Write SDK upload progress to stderr"),
    prune: bool = typer.Option(
        False,
        "--prune",
        help="Disabled: SDK safe pruning is unavailable; delete obsolete metadata explicitly",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Skip the upload confirmation",
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Upload local instances. Validates every path first, then pushes synchronously."""
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    env = _environment(environment)
    resolved = _version_value(version)
    targets = [str(path) for path in paths]

    # ① 全部路径先本地校验(上游 §9.4 "上传前先校验全部输入路径")。
    results = _validate_paths(targets)
    broken = [record for record in results if not record["ok"]]
    if broken:
        for record in broken:
            typer.echo(f"error: {record['path']} validation failed: {record['error']}", err=True)
        raise _fail(
            f"{len(broken)}/{len(results)} instances failed local validation; nothing was uploaded",
            "Run ap instance validate <path>... to fix the issues, then retry",
        )
    try:
        hashes = instance_options.upload_hashes(
            results, instance_options.read_hashes(content_hashes), skip_unchanged
        )
        if prune:
            if not resolved:
                raise ValueError("--prune requires an explicit --version")
            if any(not Path(record["path"]).is_dir() for record in results):
                raise ValueError("--prune requires a collection of instance directories")
            instance_options.require_working_prune()
        if skip_unchanged or prune:
            ids = [record["instance"] for record in results]
            if len(ids) != len(set(ids)):
                raise ValueError("Each supplied path must have a distinct instance ID")
    except (ImportError, OSError, ValueError) as exc:
        raise _fail(str(exc), "Check the hashes, input paths and installed Dataset SDK", 2) from exc

    # ② 写远端前统一二次确认(-y/--yes 跳过);版本不存在时提示将被自动创建。
    #   (split 已发布不可写由**服务端**裁决——pre 环境里 ingest 产出的 split 记录状态
    #    就是 published,客户端按它预判会把正常的二次上传全拦掉。)
    # ③ 数据面推送(repo 只构造一次,确认与推送复用,见 _check_version_autocreate)。
    #   存储继承集群绑定桶,先做同侧校验(设计 §4.2)。
    from .dataset_commands import _check_storage_side

    repo = _load_repo_or_exit()
    _check_storage_side(repo, env)
    enhanced: dict[str, Any] = {}
    if skip_unchanged:
        enhanced["skip_unchanged"] = True
    if compress_level is not None:
        enhanced["compress_level"] = compress_level
    # The SDK batch path compares stored hashes before selecting format-specific uploads.
    batch = len(targets) > 1 or prune or skip_unchanged
    if hashes:
        if batch:
            enhanced["content_hashes"] = hashes
        else:
            source_hash = hashes.get(results[0]["instance"])
            if source_hash:
                enhanced["content_hash"] = source_hash
    if batch and progress:
        enhanced["progress_callback"] = instance_options.progress_callback
    if batch and concurrency != 8:
        enhanced["concurrency"] = concurrency
    owner, method = (
        (repo, "deliver") if prune else (repo.instances, "push_many" if batch else "push")
    )
    if prune:
        enhanced["prune"] = True
    if enhanced:
        _enhanced_options(owner, method, enhanced)
    auto_create = _check_version_autocreate(repo, dataset, resolved, environment=env)
    _confirm_upload(
        dataset, resolved, split, len(targets), yes=yes, auto_create=auto_create, prune=prune
    )
    pushed: list[dict] = []
    skipped: list[dict] = []
    failed: list[dict] = []
    unconfirmed: list[str] = []
    result_count_mismatch = False
    if not batch:
        try:
            result = repo.instances.push(
                targets[0],
                dataset,
                resolved,
                split=split,
                push_image=False,
                overwrite=overwrite,
                register=True,
                **enhanced,
            )
        except Exception as exc:  # noqa: BLE001 - 统一走设计 §5.1 的映射
            failed.append({"path": targets[0], "error": _describe(exc)})
            _print_push_summary(
                dataset, resolved, split, pushed, failed, unconfirmed, output_format
            )
            sdk_error_exit(exc, what=f"instance {targets[0]}", stage="upload")
        else:
            row = _push_row(targets[0], result)
            (skipped if row["skipped"] else pushed).append(row)
            if progress:
                instance_options.progress_callback(1, 1, result)
    else:
        # 多路径:``continue_on_error=False`` 是"全或无",首个失败即抛 ItemError。
        try:
            if prune:
                delivered = repo.deliver(
                    dataset,
                    resolved,
                    targets,
                    split=split,
                    push_image=False,
                    overwrite=overwrite,
                    continue_on_error=continue_on_error,
                    **enhanced,
                )
                results_many = [
                    *delivered.get("pushed", []),
                    *delivered.get("skipped", []),
                    *delivered.get("failed", []),
                ]
            else:
                results_many = repo.instances.push_many(
                    targets,
                    dataset,
                    resolved,
                    split=split,
                    push_image=False,
                    overwrite=overwrite,
                    register=True,
                    continue_on_error=continue_on_error,
                    **enhanced,
                )
        except Exception as exc:  # noqa: BLE001
            item = getattr(exc, "item", None)
            cause = getattr(exc, "error", None) or exc
            failed_path = str(item) if item is not None else ""
            failed.append({"path": failed_path, "error": _describe(cause)})
            unconfirmed = [path for path in targets if path != failed_path]
            _print_push_summary(
                dataset, resolved, split, pushed, failed, unconfirmed, output_format
            )
            typer.echo(
                "error: batch upload aborted; content uploaded before the failure is NOT rolled back (see the UNCONFIRMED column)",
                err=True,
            )
            sdk_error_exit(
                exc, what=f"{len(targets)} instances of dataset {dataset}", stage="upload"
            )
        else:
            results_list = list(results_many or [])
            result_count_mismatch = len(results_list) != len(targets)
            pushed, skipped, failed, unconfirmed = _collect_upload_results(
                targets, results, results_list, by_id=skip_unchanged or prune
            )

    _print_push_summary(
        dataset,
        resolved,
        split,
        pushed,
        failed,
        unconfirmed,
        output_format,
        skipped=skipped if skip_unchanged or skipped else None,
    )
    if result_count_mismatch or unconfirmed:
        raise _fail(
            f"SDK returned {len(results_list)}/{len(targets)} upload results; cannot confirm the full write state",
            f"Verify the actual content with ap instance list --dataset {dataset} --split {split}",
        )
    if failed:
        raise _fail(
            f"{len(failed)} instance upload(s) failed",
            "Check the failure summary and retry the failed paths",
        )


def _collect_upload_results(
    targets: list[str],
    records: list[dict],
    values: list[Any],
    *,
    by_id: bool,
) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    remaining = list(targets)
    paths_by_id = {record["instance"]: record["path"] for record in records}
    pushed, skipped, failed = [], [], []
    for value in values:
        if isinstance(value, BaseException):
            item = str(getattr(value, "item", ""))
            path = next((raw for raw in remaining if Path(raw) == Path(item)), "") if item else ""
            if path:
                remaining.remove(path)
            failed.append({"path": path, "error": _describe(getattr(value, "error", value))})
            continue
        path = (
            paths_by_id.get(getattr(value, "instance_id", ""), "")
            if by_id
            else (remaining[0] if remaining else "")
        )
        if path not in remaining:
            continue
        remaining.remove(path)
        row = _push_row(path, value)
        (skipped if row["skipped"] else pushed).append(row)
    return pushed, skipped, failed, remaining


def _push_row(path: str, result: Any) -> dict:
    return {
        "path": path,
        "instance": getattr(result, "instance_id", "") or "",
        "uploaded": bool(getattr(result, "uploaded", False)),
        "skipped": bool(getattr(result, "skipped", False)),
    }


def _print_push_summary(
    dataset: str,
    version: str,
    split: str,
    pushed: list[dict],
    failed: list[dict],
    unconfirmed: list[str],
    output_format: str,
    *,
    skipped: Optional[list[dict]] = None,
) -> None:
    payload = {
        "dataset": dataset,
        "version": version,
        "split": split,
        "pushed": pushed,
        "failed": failed,
        "unconfirmed": unconfirmed,
    }
    rows = [dict(row, status="pushed", error="") for row in pushed]
    if skipped is not None:
        payload["skipped"] = skipped
        rows += [dict(row, status="skipped", error="") for row in skipped]
    rows += [
        {"path": row["path"], "instance": "", "status": "failed", "error": row["error"]}
        for row in failed
    ]
    rows += [
        {"path": path, "instance": "", "status": "unconfirmed", "error": ""} for path in unconfirmed
    ]
    columns = (
        ("path", "PATH"),
        ("instance", "INSTANCE"),
        ("status", "STATUS"),
        ("uploaded", "UPLOADED"),
        ("error", "ERROR"),
    )
    _emit(payload, rows, columns, output_format)


@instance_app.command("pull")
def instance_pull(
    instance: str = typer.Argument(..., help="Instance id"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    split: str = typer.Option(..., "--split", help="Split name (required for remote operations)"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output directory (default: current directory)"
    ),
    overwrite: bool = typer.Option(False, "--overwrite", help="Allow overwriting the target"),
    path: Optional[str] = typer.Option(
        None,
        "--path",
        help="Download a relative subdirectory (Custom/OSS assets); use '.' for all assets",
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Download instance content and metadata into <output>/<instance>/."""
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    resolved_path = _path_value(path)
    resolved = _version_value(version)
    root = Path(output or ".")
    target = root / instance
    if target.exists() and not overwrite:
        raise _fail(
            f"Pull target of instance {instance} already exists: {target}",
            "Choose another --output/-o directory, or add --overwrite to allow overwriting",
        )

    repo = _load_repo_or_exit()
    pull_options = {}
    if resolved_path is not None:
        pull_options = _enhanced_options(repo.instances, "pull", {"path": resolved_path})
    try:
        private_endpoint_reachable = _probe_pull_private_endpoint(repo, dataset)
    except Exception as exc:  # noqa: BLE001
        sdk_error_exit(exc, what=f"instance {instance}", stage="pull precheck")
    if private_endpoint_reachable is False:
        raise _fail(
            f"Failed to pull instance {instance}: the private OSS endpoint is unreachable from this network",
            "instance pull does not support public download; run inside an AP dev cluster / ROCK VPC",
        )

    # SDK 的 swe/custom 下载会先往输出目录写 <id>.json 与 .probe 中间文件,再由
    # _place_under_target 搬进 <id>/——把用户目录直接交给它,未加 --overwrite 也会
    # 覆盖目标同级的同名文件。先落到独立临时目录,归一后再整体搬入最终目标。
    staging = Path(tempfile.mkdtemp(prefix=f"ap-pull-{instance}-"))
    try:
        try:
            written = repo.instances.pull(
                dataset, resolved, instance, staging, split, **pull_options
            )
        except Exception as exc:  # noqa: BLE001
            sdk_error_exit(exc, what=f"instance {instance}", stage="pull")
        staged = _place_under_target(Path(str(written)), staging / instance)
        if resolved_path and not (staging / instance / resolved_path).is_dir():
            raise _fail(
                f"No files were downloaded for instance subdirectory {resolved_path}",
                "Check the directory with ap instance get --path; the SDK must support this instance format",
            )
        root.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if not overwrite:
                raise _fail(
                    f"Pull target of instance {instance} already exists: {target}",
                    "Choose another --output/-o directory, or add --overwrite to allow overwriting",
                )
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.move(str(staging / instance), str(target))
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    files, total_bytes = _tree_stats(target)
    payload = {
        "instance": instance,
        "dataset": dataset,
        "version": resolved,
        "split": split,
        "output": str(target),
        "destination": str(target.resolve()),
        "content": str(target / staged.name),
        "files": files,
        "bytes": total_bytes,
        "size": _format_size(total_bytes),
    }
    if resolved_path is not None:
        payload["path"] = resolved_path or "."
    _emit_detail(payload, output_format)


_SIZE_UNITS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB")


def _tree_stats(root: Path) -> tuple[int, int]:
    """统计落盘结果:(常规文件数, 文件总字节数)。

    只统计常规文件;目录、符号链接和断链不计入,避免把链接目标或设备/管道文件
    算成下载内容。在移动完成后对最终目标统计,口径与用户实际拿到的东西一致。
    """
    files = 0
    total = 0
    if not root.is_dir():
        return files, total
    for entry in root.rglob("*"):
        if entry.is_symlink() or not entry.is_file():
            continue
        files += 1
        total += entry.stat().st_size
    return files, total


def _format_size(total: int) -> str:
    """人类可读大小;1024 进制、保留一位小数,与 `ap dfs` 目录树的显示口径一致。"""
    size = float(total)
    for unit in _SIZE_UNITS:
        if size < 1024 or unit == _SIZE_UNITS[-1]:
            break
        size /= 1024
    return f"{int(size)} {unit}" if unit == "B" else f"{size:.1f} {unit}"


def _place_under_target(written: Path, target: Path) -> Path:
    """保证最终产物落在 ``<output>/<instance>/`` 里(上游 §9.5)。

    harbor 格式 SDK 本来就写 ``dest/{id}/content.tgz``;swe 格式写的是
    ``dest/{id}.json``——那不在 ``<output>/<instance>/`` 下,搬进去。
    """
    if not written.exists() or target in written.parents:
        return written
    target.mkdir(parents=True, exist_ok=True)
    final = target / written.name
    if written.resolve() == final.resolve():
        return final
    if final.exists():
        if final.is_dir():
            shutil.rmtree(final)
        else:
            final.unlink()
    shutil.move(str(written), str(final))
    return final


@instance_app.command("hash")
def instance_hash(
    paths: List[str] = typer.Argument(..., help="Local instance directories"),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Compute source hashes locally without contacting AP."""
    output_format = _fmt(output_format)
    try:
        from instance_repo import compute_source_hash
    except ImportError as exc:
        raise _fail(
            "Source hashing requires instance-repo 1.3.5.dev1 or newer",
            "Install Dataset support: pip install --upgrade 'ap-client[dataset]'",
            2,
        ) from exc
    hashes, failed = [], []
    for raw in paths:
        path = Path(raw)
        try:
            if not path.is_dir():
                raise ValueError("source hashing requires an existing instance directory")
            hashes.append(
                {"path": raw, "instance": path.name, "source_hash": compute_source_hash(path)}
            )
        except (OSError, ValueError) as exc:
            failed.append({"path": raw, "error": _describe(exc)})
    _emit(
        {"hashes": hashes, "failed": failed},
        hashes,
        (("path", "PATH"), ("instance", "INSTANCE"), ("source_hash", "SOURCE_HASH")),
        output_format,
    )
    if failed:
        raise _fail(f"{len(failed)} instance directory hash(es) failed", "Check the local paths")


@instance_app.command("hashes")
def instance_hashes(
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    split: str = typer.Option(..., "--split", help="Split name"),
    version: Optional[str] = typer.Option(None, "--version", help=_VERSION_HELP),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    metadata_model: Optional[str] = typer.Option(
        None, "--metadata-model", help=_METADATA_MODEL_HELP
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List source hashes stored on remote instances."""
    output_format = _fmt(output_format)
    resolved = _version_value(version)
    env = _environment(environment)
    repo = _load_repo_or_exit()
    _enhanced_options(repo.instances, "list_content_hashes", {})
    kwargs = _sdk_read_kwargs(
        repo.instances,
        "list_content_hashes",
        environment=env,
        metadata_model=_metadata_model_for_split(metadata_model, split=split),
    )
    try:
        try:
            fallback = oss_fallback_kwargs(repo, repo.instances, "list_content_hashes", env)
        except RuntimeError:
            # This SDK helper cannot disable its inner list() discovery yet.
            list_kwargs = _sdk_read_kwargs(
                repo.instances,
                "list",
                environment=env,
                metadata_model=_metadata_model_for_split(metadata_model, split=split),
            )
            list_kwargs.update(oss_fallback_kwargs(repo, repo.instances, "list", env))
            records = repo.instances.list(dataset, resolved, split=split, **list_kwargs)
            hashes = {}
            for record in records:
                served = _model_dict(record)
                source_hash = (served.get("extend_meta") or {}).get("source_hash")
                if source_hash:
                    hashes[served["instance_id"]] = source_hash
        else:
            hashes = repo.instances.list_content_hashes(
                dataset, resolved, split=split, **kwargs, **fallback
            )
    except Exception as exc:  # noqa: BLE001
        raise _fail(
            f"Failed to list source hashes of dataset {dataset}: {_describe(exc)}",
            "Check the environment, bound storage and read permission",
        ) from exc
    rows = [
        {"instance": instance, "source_hash": value} for instance, value in sorted(hashes.items())
    ]
    _emit(
        {"dataset": dataset, "version": resolved, "split": split, "hashes": hashes},
        rows,
        (("instance", "INSTANCE"), ("source_hash", "SOURCE_HASH")),
        output_format,
    )


@instance_app.command("delete")
def instance_delete(
    instance: str = typer.Argument(..., help="Instance id"),
    dataset: str = typer.Option(..., "--dataset", help="Dataset name"),
    version: str = typer.Option(..., "--version", help="Dataset version containing the instance"),
    split: str = typer.Option(..., "--split", help="Split name"),
    environment: Optional[str] = typer.Option(None, "--environment", help=_ENVIRONMENT_HELP),
    metadata_model: Optional[str] = typer.Option(
        None, "--metadata-model", help=_METADATA_MODEL_HELP
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm deleting instance metadata"),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Delete instance metadata. OSS content remains available to later ingest."""
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    env = _environment(environment)
    resolved = _version_value(version)
    if not resolved:
        raise _fail(
            "--version must be nonempty for metadata deletion", "Specify the dataset version", 2
        )
    repo = _load_repo_or_exit()
    _enhanced_options(repo.instances, "delete", {})
    kwargs = _sdk_read_kwargs(
        repo.instances,
        "delete",
        environment=env,
        metadata_model=_metadata_model_for_split(metadata_model, split=split),
    )
    if not yes:
        if not sys.stdin.isatty():
            raise _fail("Deleting instance metadata requires confirmation", "Add --yes (-y)", 2)
        if not typer.confirm(
            f"Delete metadata for {dataset} version {resolved} split {split} instance {instance}? OSS files remain."
        ):
            raise _fail(
                "Metadata deletion canceled", "Rerun when you want to delete the instance record"
            )
    try:
        repo.instances.delete(dataset, resolved, instance, split=split, **kwargs)
    except Exception as exc:  # noqa: BLE001
        sdk_error_exit(exc, what=f"instance {instance}", stage="metadata deletion")
    _emit_detail(
        {
            "dataset": dataset,
            "version": resolved,
            "split": split,
            "instance": instance,
            "deleted": True,
            "content_deleted": False,
        },
        output_format,
    )
