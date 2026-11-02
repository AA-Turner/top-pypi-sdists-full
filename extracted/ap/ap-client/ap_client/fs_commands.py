"""``ap fs`` 命令族 —— InstanceRepo user-data(实现设计 §4.6)。

命令与后端映射:

* ``fs ls`` → ``repo.list_user_data(uid, subpath=...)``
* ``fs get/put`` → CLI 并发传输层,沿用 SDK 精确对象 STS 与网络路由
* ``fs access ls`` → ``repo.list_user_data_acl(uid, subpath=...)``
* ``fs access grant`` → ``repo.grant_user_data(..., subpath=...)``
* ``fs access revoke`` → ``repo.revoke_user_data(..., subpath=...)``

三条实现约束(设计 §4.6 / §8.4):

1. ``--user`` 是**空间归主的工号**,不是被授权人;``fs access grant/revoke`` 的
   被授权主体用 ``--principal``。``--principal`` 优先;只给了 ``--user`` 时把它
   当被授权主体、空间归主取当前用户,结果中的 owner/principal 字段反映最终解释。
2. 数据面寻址(含 ACL 资源 id 里的 storage_env)对客屏蔽:用户只需配 AP 基础环境
   变量(``AP_CLUSTER`` / ``AP_API_KEY``),storage_env 由 SDK 依据 cluster 自动发现
   (``repo.profile.storage_env``)。CLI 只把它用于**回显** ``{storage_env}/{uid}``,
   解析不出就只显示 ``uid``,**绝不因缺失而前置拒绝**——授权走
   ``grant_user_data``/``revoke_user_data``,不吃 storage_env,资源归属由 apiserver 判定。
3. ``list_user_data_acl`` 的返回形态跨 SDK 版本不同(``release/v1.0.0`` 是
   ``list[dict]``,``feat/sdk-user-data-acl`` 是 ``list[UserDataGrant]``),CLI 必须
   统一归一为 ``{principal_type, principal_id, role}``;``revoke_user_data`` 是否
   接受 ``role`` 也需按能力探测处理。
4. ``access *`` 的 ``--path`` 把授权收敛到子目录/文件粒度(资源 id 变为
   ``{storage_env}/{uid}/{subpath}``,1.0.7+ 的 SDK)。子路径是**独立资源**:
   uid 级列举不含子路径绑定,撤销也只作用于该子路径;旧 SDK 不接受 ``subpath``
   参数,能力探测失败时 exit 2 并提示升级,而不是把 ``subpath`` 静默吞掉。

``ap fs`` 全部是数据面命令,SDK 在命令函数内部懒加载:

    from .irepo_sdk import SdkMissing, load_repo, sdk_error_exit

``SdkMissing`` → 打印 ``str(exc)`` 到 stderr 并 ``typer.Exit(2)``;SDK 业务异常 →
``sdk_error_exit(exc, what=..., stage=...)``(94022/94023 的授权提示已在表里)。
"""

from __future__ import annotations

import inspect
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import typer

__all__ = ["fs_app", "fs_access_app", "register"]

fs_app = typer.Typer(help="User storage space file operations (InstanceRepo user-data)")
fs_access_app = typer.Typer(help="User storage space access control (user-data role bindings)")

fs_app.add_typer(fs_access_app, name="access")


def register(app: typer.Typer) -> None:
    """把 ``fs`` 挂到 ``ap`` 根命令上。"""
    app.add_typer(fs_app, name="fs")


# ---------------------------------------------------------------------------
# 常量与共用 helper
# ---------------------------------------------------------------------------

#: 语义角色名 → apiserver 内置角色 id(与 SDK ``acl.USER_DATA_ROLE_IDS`` 一致)。
#: 这些角色在当前 apiserver 代码里**并不存在**(设计 §8.4),真机可能被拒。
_ROLES = ("reader", "writer", "admin")
_ROLE_IDS = {role: f"built-in:user-data-{role}" for role in _ROLES}
_ROLE_BY_ID = {value: key for key, value in _ROLE_IDS.items()}

_PRINCIPAL_TYPES = ("user", "user_group")

_FORMAT_HELP = "Output format: plain/table/json/yaml (default: AP_FORMAT or command default)"
_USER_HELP = "Owner uid of the user storage space (default: resolved via the SDK whoami())"
_PATH_HELP = (
    "Sub-path (subdirectory or file) to scope the ACL to; omit for the whole user storage space"
)

_UID_HINT = "Cannot resolve the current uid automatically; pass --user <uid> explicitly"
_SUBPATH_HINT = "--path is a relative sub-path inside the space, e.g. plugins/cursor"
_SUBPATH_UPGRADE = "pip install -U 'instance-repo[oss]>=1.0.9'"

_ACL_COLUMNS: tuple[tuple[str, str], ...] = (
    ("principal_type", "PRINCIPAL_TYPE"),
    ("principal_id", "PRINCIPAL_ID"),
    ("role", "ROLE"),
)


def _fmt(output_format: Optional[str]) -> str:
    from .cli import _normalize_output_format

    return _normalize_output_format(output_format, keep_table=True)


def _fail(message: str, hint: str, exit_code: int = 1) -> "typer.Exit":
    typer.echo(f"error: {message}", err=True)
    typer.echo(f"hint: {hint}", err=True)
    return typer.Exit(exit_code)


def _describe(exc: BaseException) -> str:
    message = getattr(exc, "message", None)
    text = str(message or "").strip() or str(exc).strip()
    return text or type(exc).__name__


def _load_repo_or_exit():
    from .irepo_sdk import SdkMissing, load_repo

    try:
        return load_repo()
    except SdkMissing as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc


def _emit(payload, rows, columns, output_format: str) -> None:
    from .cli import _print_formatted, _print_plain_table, _print_rich_table

    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
        return
    if output_format == "table":
        _print_rich_table(rows, list(columns))
    else:
        _print_plain_table(rows, list(columns))


def _emit_detail(payload: dict, output_format: str) -> None:
    from .cli import _print_detail, _print_formatted

    if output_format in ("json", "yaml"):
        _print_formatted(payload, output_format)
    else:
        _print_detail(payload)


def _resolve_uid(repo, explicit: Optional[str]) -> str:
    """空间归主工号:``--user`` 优先,否则 ``repo.whoami()``。

    ``whoami()`` 打的是 ``GET /apis/v1/me/identity``——该路由在当前 apiserver 代码里
    **不存在**(设计 §8.5),所以这是 best-effort:失败或空结果**绝不静默继续**,
    直接退出码 2 要求显式传 ``--user``。
    """
    if explicit and explicit.strip():
        return explicit.strip()
    uid = ""
    whoami = getattr(repo, "whoami", None)
    if callable(whoami):
        try:
            uid = str(whoami() or "").strip()
        except Exception as exc:  # noqa: BLE001 - 路由缺失/无权限都按"解析不出"处理
            typer.echo(f"error: failed to resolve the current uid: {_describe(exc)}", err=True)
            typer.echo(f"hint: {_UID_HINT}", err=True)
            raise typer.Exit(2) from exc
    if not uid:
        raise _fail(
            "Failed to resolve the current uid: SDK whoami() returned no uid",
            _UID_HINT,
            exit_code=2,
        )
    return uid


def _acl_storage_env(repo) -> str:
    """ACL 资源 id 里的 storage_env,**仅用于回显**,解析不出就返回空串。

    对客只保留 AP 基础环境变量(AP_CLUSTER / AP_API_KEY),数据面寻址由 CLI + SDK
    自动完成:优先取 ``repo.profile.storage_env``(SDK 依据 cluster 自动发现的结果),
    退回旧环境变量 ``INSTANCE_REPO_STORAGE_ENV`` / ``IR_STORAGE_ENV`` 仅为兼容显式覆盖。
    授权本身走 ``grant_user_data``/``revoke_user_data``,不吃 storage_env,所以这里
    绝不因缺失而前置拒绝——真正的资源归属由 apiserver 判定。
    """
    profile = getattr(repo, "profile", None)
    resolved = str(getattr(profile, "storage_env", "") or "").strip()
    if resolved:
        return resolved
    from . import irepo_sdk

    return irepo_sdk._resolve_storage_env(None)


def _acl_resource_id(storage_env: str, uid: str, subpath: str = "") -> str:
    """``{storage_env}/{uid}``(带 ``--path`` 时追加 ``/{subpath}``);storage_env
    解析不出时只回显 uid,不拼出坏的 ``/uid``。"""
    rid = f"{storage_env}/{uid}" if storage_env else uid
    return f"{rid}/{subpath}" if subpath else rid


def _validate_subpath(value: Optional[str]) -> str:
    """``--path`` 的前置校验(设计 §7.5):空 = 整空间,其余与 SDK
    ``_validate_user_data_acl_subpath`` / apiserver ``ValidateUserDataSubpath`` 同口径。

    授权路径必须与存储 key 逐字符对齐:``..``、通配符、首尾斜杠与空段都会造出
    "绑定建得出来、凭据永远签不出/探测不到"的死绑定,在 CLI 侧就拦下(exit 2),
    不等 SDK 抛错。
    """
    sub = str(value or "").strip()
    if not sub:
        return ""
    if sub.startswith("/") or sub.endswith("/"):
        raise _fail("--path must not start or end with /", _SUBPATH_HINT, exit_code=2)
    if "//" in sub:
        raise _fail("--path must not contain empty segments (//)", _SUBPATH_HINT, exit_code=2)
    # 按"段"判定,与 SDK ``_validate_user_data_acl_subpath`` 一致:用子串会把
    # ``v1..v2/x`` 这类合法名字也拒掉(服务端是认的)。
    if any(segment == ".." for segment in sub.split("/")):
        raise _fail(
            "--path must not contain .. segments",
            "--path does not allow directory traversal",
            exit_code=2,
        )
    if "*" in sub or "?" in sub:
        raise _fail(
            "--path must not contain wildcards * or ?",
            "Sub-path grants are exact character matches; wildcards are not supported",
            exit_code=2,
        )
    return sub


def _method_accepts_subpath(repo, name: str) -> bool:
    """能力探测:SDK 的该方法签名是否接受 ``subpath``(1.0.7+ 才有)。"""
    fn = getattr(repo, name, None)
    if fn is None:
        return False
    try:
        signature = inspect.signature(fn)
    except (TypeError, ValueError):  # pragma: no cover - 只在异常打桩时触发
        return False
    return "subpath" in signature.parameters


def _require_subpath_support(repo, name: str) -> None:
    """用户显式给了 ``--path`` 而 SDK 不支持时,exit 2 并提示升级——绝不静默
    降级成整空间粒度(那是把授权范围悄悄放大)。"""
    if _method_accepts_subpath(repo, name):
        return
    raise _fail(
        f"The installed instance-repo {name} does not support sub-path scoped grants (--path)",
        f"Drop --path to operate on the whole space, or upgrade: {_SUBPATH_UPGRADE}",
        exit_code=2,
    )


def _check_choice(value: str, choices: tuple[str, ...], option: str) -> str:
    normalized = str(value or "").strip().lower()
    if normalized not in choices:
        raise _fail(
            f"{option} invalid value: {value!r}",
            f"{option} accepts only: {', '.join(choices)}",
            exit_code=2,
        )
    return normalized


def _remote_subpath(filepath: str, directory: Optional[str]) -> str:
    """``--dir`` 是子目录前缀,位置参数是目录内的文件路径。"""
    parts = [part.strip("/") for part in ((directory or ""), filepath) if part and part.strip("/")]
    if not parts:
        raise _fail(
            "Remote path is empty",
            "Provide at least <filepath>, or use --dir to pick a subdirectory",
            exit_code=2,
        )
    return "/".join(parts)


def _user_data_prefix(uid: str) -> str:
    return f"swe/user-data/users/{uid}/"


def _existing_policy(on_exist: str, overwrite: bool, skip_existing: bool):
    policy = _check_choice(on_exist, ("prompt", "overwrite", "skip", "error"), "--on-exist")
    if overwrite and skip_existing or (policy != "prompt" and (overwrite or skip_existing)):
        raise _fail(
            "Conflicting existing-file options",
            "Choose one of --on-exist, --overwrite, --skip-existing",
            2,
        )
    return "overwrite" if overwrite else "skip" if skip_existing else policy


def _replace_existing(path: str, policy: str) -> bool:
    if policy == "overwrite":
        return True
    if policy == "skip":
        return False
    if policy == "error" or not all(
        stream.isatty() for stream in (sys.stdin, sys.stdout, sys.stderr)
    ):
        raise FileExistsError(
            f"Destination already exists: {path}. Use --overwrite or --skip-existing; "
            "interactive confirmation requires a terminal."
        )
    return typer.confirm(f"Overwrite {path}?", default=False, err=True)


# ---------------------------------------------------------------------------
# ap fs ls / get / put
# ---------------------------------------------------------------------------


@fs_app.command("ls")
def fs_ls(
    path: Optional[str] = typer.Argument(None, help="Directory to list (default: space root)"),
    directory: Optional[str] = typer.Option(None, "--dir", help="Sub-directory prefix"),
    recursive: bool = typer.Option(False, "--recursive", "-R", help="List all descendants"),
    all_entries: bool = typer.Option(
        False, "--all", "-a", help="Include names starting with a dot"
    ),
    reverse: bool = typer.Option(False, "--reverse", "-r", help="Reverse name sort order"),
    long: bool = typer.Option(
        False, "--long", "-l", help="Show type, size in bytes and modified time"
    ),
    human_readable: bool = typer.Option(
        False, "--human-readable", "-h", help="Use readable sizes with -l"
    ),
    sort: str = typer.Option(
        "name", "--sort", help="Sort by name/size/time (size and time: largest/newest first)"
    ),
    directories_only: bool = typer.Option(False, "--dirs-only", help="Show directories only"),
    files_only: bool = typer.Option(False, "--files-only", help="Show files only"),
    limit: Optional[int] = typer.Option(
        None, "--limit", min=1, help="Maximum number of displayed entries"
    ),
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List one directory level; use -R to include descendants."""
    from .fs_storage import UserDataFiles
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    sort = _check_choice(sort, ("name", "size", "time"), "--sort")
    if path is not None and directory is not None:
        raise _fail("Specify a path or --dir, not both", "Example: ap fs ls probe", 2)
    if directories_only and files_only:
        raise _fail("--dirs-only conflicts with --files-only", "Choose one type filter", 2)
    directory = path if path is not None else directory or ""
    repo = _load_repo_or_exit()
    uid = _resolve_uid(repo, user)
    try:
        rows = UserDataFiles(repo).list(uid, directory, recursive=recursive)
    except Exception as exc:  # noqa: BLE001
        sdk_error_exit(exc, what=f"user storage {uid}", stage="list")

    def visible(row):
        return (
            row.get("explicit", False)
            or all_entries
            or not any(part.startswith(".") for part in row["name"].split("/"))
        )

    rows = [
        row
        for row in rows
        if visible(row)
        and (not directories_only or row["type"] == "directory")
        and (not files_only or row["type"] == "file")
    ]
    rows.sort(key=lambda row: row["path"])
    if sort != "name":
        field = "size" if sort == "size" else "modified"
        rows.sort(key=lambda row: row[field] or 0, reverse=True)
    if reverse:
        rows.reverse()
    if limit is not None:
        rows = rows[:limit]
    payload = {"user": uid, "dir": directory or "", "files": rows}
    display_rows = []
    for row in rows:
        shown = dict(row)
        size = row.get("size")
        if human_readable and size is not None:
            value = float(size)
            for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
                if value < 1024 or unit == "TiB":
                    shown["size"] = f"{value:g} {unit}"
                    break
                value /= 1024
        if row.get("modified") is not None:
            shown["modified"] = datetime.fromtimestamp(row["modified"], tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%SZ"
            )
        display_rows.append(shown)
    columns = (
        (("name", "PATH"), ("type", "TYPE"), ("size", "BYTES"), ("modified", "MODIFIED"))
        if long
        else (("name", "PATH"),)
    )
    _emit(payload, display_rows, columns, output_format)


@fs_app.command("mkdir")
def fs_mkdir(
    path: str = typer.Argument(..., help="Directory path inside the user storage space"),
    parents: bool = typer.Option(
        False, "--parents", "-p", help="Create missing parents; accept existing directories"
    ),
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Create an empty directory using an OSS directory marker."""
    from .fs_storage import UserDataFiles
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    repo = _load_repo_or_exit()
    uid = _resolve_uid(repo, user)
    try:
        result = UserDataFiles(repo).mkdir(uid, path, parents=parents)
    except Exception as exc:
        sdk_error_exit(exc, what=f"user storage {uid} {path}", stage="mkdir")
    _emit_detail({"user": uid, **result}, output_format)


@fs_app.command("get")
def fs_get(
    filepath: str = typer.Argument(..., help="Remote file path inside the user storage space"),
    directory: Optional[str] = typer.Option(None, "--dir", help="Sub-directory prefix"),
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    target: Optional[str] = typer.Option(
        None, "--target", help="Local target path (default: the remote file name in CWD)"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-f", help="Replace an existing destination"
    ),
    skip_existing: bool = typer.Option(
        False, "--skip-existing", "-n", help="Keep existing destinations"
    ),
    on_exist: str = typer.Option(
        "prompt", "--on-exist", help="Existing destination: prompt/overwrite/skip/error"
    ),
    concurrency: int = typer.Option(
        8, "--concurrency", "-j", min=1, max=64, help="Maximum concurrent transfer requests"
    ),
    progress: Optional[bool] = typer.Option(
        None,
        "--progress/--no-progress",
        help="Show transfer progress on stderr (default: terminal only)",
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Download one file from a user storage space."""
    from .fs_transfer import UserDataTransfer
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    policy = _existing_policy(on_exist, overwrite, skip_existing)
    repo = _load_repo_or_exit()
    uid = _resolve_uid(repo, user)
    remote = _remote_subpath(filepath, directory)
    local = Path(target) if target else Path(Path(remote).name)
    if local.is_dir() or (target and target.endswith("/")):
        local = local / Path(remote).name
    skipped = False
    try:
        if local.is_symlink():
            raise ValueError("Download target must not be a symbolic link")
        exists = local.exists()
        if exists and not local.is_file():
            raise ValueError("Download target must be a regular file")
        skipped = exists and not _replace_existing(str(local), policy)
        if local.parent and str(local.parent) not in ("", "."):
            local.parent.mkdir(parents=True, exist_ok=True)
        written = (
            str(local)
            if skipped
            else UserDataTransfer(repo, concurrency=concurrency, progress=progress).get(
                uid, remote, local, overwrite=exists or policy == "overwrite"
            )
        )
    except Exception as exc:  # noqa: BLE001
        sdk_error_exit(exc, what=f"user storage {uid} {remote}", stage="download")

    _emit_detail(
        {
            "user": uid,
            "remote": remote,
            "local": str(written or local),
            "downloaded": 0 if skipped else 1,
            "skipped": int(skipped),
        },
        output_format,
    )


@fs_app.command("put")
def fs_put(
    filepath: str = typer.Argument(..., help="Remote file path inside the user storage space"),
    directory: Optional[str] = typer.Option(None, "--dir", help="Sub-directory prefix"),
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    source: Optional[str] = typer.Option(
        None, "--source", help="Local source path (default: <filepath> relative to CWD)"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-f", help="Allow overwriting remote objects"
    ),
    skip_existing: bool = typer.Option(
        False, "--skip-existing", "-n", help="Keep existing remote objects"
    ),
    on_exist: str = typer.Option(
        "prompt", "--on-exist", help="Existing destination: prompt/overwrite/skip/error"
    ),
    concurrency: int = typer.Option(
        8, "--concurrency", "-j", min=1, max=64, help="Maximum concurrent transfer requests"
    ),
    progress: Optional[bool] = typer.Option(
        None,
        "--progress/--no-progress",
        help="Show transfer progress on stderr (default: terminal only)",
    ),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Upload a local file (or directory) into a user storage space."""
    from .fs_transfer import UserDataTransfer
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    policy = _existing_policy(on_exist, overwrite, skip_existing)
    local = Path(source or filepath)
    if not local.exists():
        raise _fail(
            f"Local path {local} does not exist",
            "Make sure --source points to an existing file/directory (the positional <filepath> is the local path when omitted)",
            exit_code=2,
        )

    repo = _load_repo_or_exit()
    uid = _resolve_uid(repo, user)
    remote = _remote_subpath(filepath, directory)
    is_dir = local.is_dir()
    if filepath.endswith("/") and not is_dir:
        remote = remote.rstrip("/") + "/" + local.name
    try:
        outcome: Any = UserDataTransfer(repo, concurrency=concurrency, progress=progress).put(
            uid,
            local,
            remote,
            overwrite=policy == "overwrite",
            on_conflict=lambda key: _replace_existing(key, policy),
        )
    except Exception as exc:  # noqa: BLE001
        sdk_error_exit(exc, what=f"user storage {uid} {remote}", stage="upload")

    results = outcome if isinstance(outcome, list) else [outcome]
    skipped = sum(isinstance(item, dict) and item.get("skipped", False) for item in results)
    _emit_detail(
        {
            "user": uid,
            "remote": remote,
            "local": str(local),
            "kind": "directory" if is_dir else "file",
            "objects": len(results),
            "uploaded": len(results) - skipped,
            "skipped": skipped,
        },
        output_format,
    )


# ---------------------------------------------------------------------------
# ap fs access
# ---------------------------------------------------------------------------


def _normalize_grant(entry: Any) -> dict:
    """把一条 ACL 归一为 ``{principal_type, principal_id, role}``(设计 §4.6 第 3 条)。

    ``release/v1.0.0`` 返回裸 ``dict``(只有 ``role_id``),``feat/sdk-user-data-acl``
    返回 ``UserDataGrant`` 数据类(``role`` 已翻译好)。两种都要能读。
    """
    if isinstance(entry, dict):
        data = dict(entry)
    else:
        to_dict = getattr(entry, "to_dict", None)
        if callable(to_dict):
            raw = to_dict()
            data = dict(raw) if isinstance(raw, dict) else {}
        else:
            data = {}
        for field in ("principal_type", "principal_id", "role_id", "role"):
            if field not in data:
                value = getattr(entry, field, "")
                if value:
                    data[field] = value
    role = str(data.get("role") or "").strip()
    if not role:
        role = _ROLE_BY_ID.get(str(data.get("role_id") or "").strip(), "")
    return {
        "principal_type": str(data.get("principal_type") or ""),
        "principal_id": str(data.get("principal_id") or ""),
        "role": role or str(data.get("role_id") or ""),
    }


@fs_access_app.command("ls")
def fs_access_ls(
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    path: Optional[str] = typer.Option(None, "--path", help=_PATH_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """List the role bindings on a user storage space (or one sub-path of it)."""
    from .irepo_sdk import sdk_error_exit

    output_format = _fmt(output_format)
    subpath = _validate_subpath(path)
    repo = _load_repo_or_exit()
    storage_env = _acl_storage_env(repo)
    uid = _resolve_uid(repo, user)
    if subpath:
        _require_subpath_support(repo, "list_user_data_acl")
    try:
        # 子路径是独立资源,列表接口按 resource_id 精确匹配:uid 级列举不含
        # 子路径上的绑定,反之亦然(设计 §7.5)。
        entries = (
            repo.list_user_data_acl(uid)
            if not subpath
            else repo.list_user_data_acl(uid, subpath=subpath)
        )
    except Exception as exc:  # noqa: BLE001
        sdk_error_exit(exc, what=f"user storage {uid} access", stage="list")

    rows = [_normalize_grant(entry) for entry in list(entries or [])]
    payload = {
        "user": uid,
        "subpath": subpath,
        "resource_id": _acl_resource_id(storage_env, uid, subpath),
        "acl": rows,
    }
    _emit(payload, rows, _ACL_COLUMNS, output_format)


def _resolve_principal(repo, *, user: Optional[str], principal: Optional[str]) -> tuple[str, str]:
    """返回 ``(空间归主 uid, 被授权主体)``(设计 §4.6 的兼容口径)。

    ``--principal`` 优先:此时 ``--user`` 就是空间归主。只给 ``--user`` 时按上游
    §11.4 的写法把它当被授权主体,空间归主取 ``whoami()``,并在 stderr 说明本次解释。
    """
    grantee = (principal or "").strip()
    if grantee:
        return _resolve_uid(repo, user), grantee
    fallback = (user or "").strip()
    if not fallback:
        raise _fail(
            "Missing the grantee principal",
            "Use --principal <uid|user-group-id> for the grantee; --user means the space owner",
            exit_code=2,
        )
    owner = _resolve_uid(repo, None)
    return owner, fallback


@fs_access_app.command("grant")
def fs_access_grant(
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    role: str = typer.Option(..., "--role", help=f"Role to grant: {'/'.join(_ROLES)}"),
    principal: Optional[str] = typer.Option(
        None, "--principal", help="Grantee (uid or user_group id); takes precedence over --user"
    ),
    principal_type: str = typer.Option(
        "user", "--principal-type", help=f"Principal type: {'/'.join(_PRINCIPAL_TYPES)}"
    ),
    path: Optional[str] = typer.Option(None, "--path", help=_PATH_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Grant a role on a user storage space (or one sub-path of it)."""
    from .irepo_sdk import is_already_satisfied, sdk_error_exit

    output_format = _fmt(output_format)
    resolved_role = _check_choice(role, _ROLES, "--role")
    resolved_type = _check_choice(principal_type, _PRINCIPAL_TYPES, "--principal-type")
    subpath = _validate_subpath(path)

    repo = _load_repo_or_exit()
    storage_env = _acl_storage_env(repo)
    owner, grantee = _resolve_principal(repo, user=user, principal=principal)
    if subpath:
        _require_subpath_support(repo, "grant_user_data")

    already = False
    try:
        if subpath:
            repo.grant_user_data(
                owner, grantee, resolved_role, principal_type=resolved_type, subpath=subpath
            )
        else:
            repo.grant_user_data(owner, grantee, resolved_role, principal_type=resolved_type)
    except Exception as exc:  # noqa: BLE001
        if not is_already_satisfied(exc):
            sdk_error_exit(exc, what=f"user storage {owner} access", stage="grant")
        already = True

    _emit_detail(
        {
            "user": owner,
            "subpath": subpath,
            "resource_id": _acl_resource_id(storage_env, owner, subpath),
            "principal_type": resolved_type,
            "principal_id": grantee,
            "role": resolved_role,
            "already_granted": already,
        },
        output_format,
    )


def _revoke_accepts_role(repo) -> bool:
    """能力探测(设计 §8.4):``revoke_user_data`` 是否支持按角色撤销。

    0.8.1 的签名是 ``revoke_user_data(uid, principal_id, role, *, principal_type)``
    ——**按角色**逐条撤销;release/v1.0.0 是 ``(uid, principal, *, principal_type)``
    ——一次撤销该主体的全部角色。两者不能互相模拟,只能探测后分别处理。
    """
    fn = getattr(repo, "revoke_user_data", None)
    if fn is None:
        return False
    try:
        signature = inspect.signature(fn)
    except (TypeError, ValueError):  # pragma: no cover - 只在异常打桩时触发
        return False
    return "role" in signature.parameters


@fs_access_app.command("revoke")
def fs_access_revoke(
    user: Optional[str] = typer.Option(None, "--user", help=_USER_HELP),
    role: Optional[str] = typer.Option(
        None, "--role", help=f"Role to revoke ({'/'.join(_ROLES)}); omit to revoke every role"
    ),
    principal: Optional[str] = typer.Option(
        None, "--principal", help="Grantee (uid or user_group id); takes precedence over --user"
    ),
    principal_type: str = typer.Option(
        "user", "--principal-type", help=f"Principal type: {'/'.join(_PRINCIPAL_TYPES)}"
    ),
    path: Optional[str] = typer.Option(None, "--path", help=_PATH_HELP),
    output_format: str = typer.Option(None, "--format", help=_FORMAT_HELP),
):
    """Revoke a role (or every role) on a user storage space (or one sub-path of it)."""
    from .irepo_sdk import is_already_satisfied, sdk_error_exit

    output_format = _fmt(output_format)
    resolved_role = _check_choice(role, _ROLES, "--role") if role else ""
    resolved_type = _check_choice(principal_type, _PRINCIPAL_TYPES, "--principal-type")
    subpath = _validate_subpath(path)

    repo = _load_repo_or_exit()
    storage_env = _acl_storage_env(repo)
    owner, grantee = _resolve_principal(repo, user=user, principal=principal)
    per_role = _revoke_accepts_role(repo)
    if subpath:
        # 子路径级撤销只作用于该子路径上的绑定,不影响整空间(uid 级)绑定。
        _require_subpath_support(repo, "revoke_user_data")

    if not per_role and resolved_role:
        raise _fail(
            f"The installed instance-repo revoke_user_data does not support role-scoped revoke (--role {resolved_role})",
            "Drop --role to revoke all roles of the principal on this directory; role-scoped revoke needs an SDK with the role parameter",
            exit_code=2,
        )

    targets = [resolved_role] if resolved_role else []
    if per_role and not targets:
        targets = _roles_of(repo, owner, grantee, resolved_type, subpath)
        if not targets:
            _emit_detail(
                _revoke_payload(owner, storage_env, resolved_type, grantee, subpath, [], []),
                output_format,
            )
            return

    revoked: list[str] = []
    missing: list[str] = []
    calls = targets or [""]
    for target in calls:
        try:
            if per_role:
                if subpath:
                    repo.revoke_user_data(
                        owner, grantee, target, principal_type=resolved_type, subpath=subpath
                    )
                else:
                    repo.revoke_user_data(owner, grantee, target, principal_type=resolved_type)
            elif subpath:
                repo.revoke_user_data(owner, grantee, principal_type=resolved_type, subpath=subpath)
            else:
                repo.revoke_user_data(owner, grantee, principal_type=resolved_type)
        except Exception as exc:  # noqa: BLE001
            if not is_already_satisfied(exc):
                sdk_error_exit(exc, what=f"user storage {owner} access", stage="revoke")
            missing.append(target or "*")
        else:
            revoked.append(target or "*")

    _emit_detail(
        _revoke_payload(owner, storage_env, resolved_type, grantee, subpath, revoked, missing),
        output_format,
    )


def _revoke_payload(
    owner: str,
    storage_env: str,
    principal_type: str,
    grantee: str,
    subpath: str,
    revoked: list[str],
    missing: list[str],
) -> dict:
    return {
        "user": owner,
        "subpath": subpath,
        "resource_id": _acl_resource_id(storage_env, owner, subpath),
        "principal_type": principal_type,
        "principal_id": grantee,
        "revoked": revoked,
        "already_absent": missing,
    }


def _roles_of(repo, owner: str, grantee: str, principal_type: str, subpath: str = "") -> list[str]:
    """按角色撤销的 SDK 上,``--role`` 缺省要先查该主体现有的角色逐个撤。

    子路径是独立资源,查询同样要落在该子路径上(uid 级列举不含子路径绑定)。
    """
    from .irepo_sdk import sdk_error_exit

    if subpath:
        _require_subpath_support(repo, "list_user_data_acl")
    try:
        entries = (
            repo.list_user_data_acl(owner, subpath=subpath)
            if subpath
            else repo.list_user_data_acl(owner)
        )
    except Exception as exc:  # noqa: BLE001
        typer.echo(
            f"error: failed to list access grants of user storage {owner}: {_describe(exc)}",
            err=True,
        )
        typer.echo(
            "hint: the installed SDK only supports role-scoped revoke; pass --role <reader|writer|admin> explicitly when existing roles cannot be listed",
            err=True,
        )
        if os.environ.get("AP_VERBOSE"):  # pragma: no cover - 仅用于排查
            sdk_error_exit(exc, what=f"user storage {owner} access", stage="list")
        raise typer.Exit(2) from exc
    roles = []
    for entry in list(entries or []):
        row = _normalize_grant(entry)
        if row["principal_id"] != grantee:
            continue
        if row["principal_type"] and row["principal_type"] != principal_type:
            continue
        if row["role"] in _ROLES and row["role"] not in roles:
            roles.append(row["role"])
    return roles
