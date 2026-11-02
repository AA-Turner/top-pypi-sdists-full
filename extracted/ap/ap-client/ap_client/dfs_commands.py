"""DFS commands over server-bound OSS storage; optional dependencies stay lazy."""

from __future__ import annotations

import json
import re
import threading
import unicodedata
from pathlib import Path
from typing import Annotated, Optional
from urllib.parse import unquote, urlsplit

import typer

from .ossutil_io import OssBinding, OssFiles, OssUsageError, _relative, safe_error

dfs_app = typer.Typer(
    help=(
        "Raw file operations within the server-configured storage prefix; no ingest or registration. "
        "Use ans:// for remote cp, mkdir and hash; cp uploads, downloads or copies remotely. "
        "Directories require -r. cat reads full content; hash reads full content locally, with "
        "--download, or if remote hash metadata is missing/invalid. Content downloads require "
        "private-network access. "
        "Examples: ap dfs ls ans://team/bench/train; "
        "ap dfs cp ./abc ans://team/bench/train/; ap dfs hash md5 ./abc."
    ),
    no_args_is_help=True,
)


def register(app: typer.Typer) -> None:
    app.add_typer(dfs_app, name="dfs")


_DFS_ACCESS_DENIED_CODES = frozenset({94016, 94018, 10002})


def _files() -> OssFiles:
    from .cli import app
    from .irepo_sdk import load_ossutil_repo

    app.pretty_exceptions_show_locals = False
    try:
        repo, config = load_ossutil_repo()
    except Exception as exc:
        biz_code = getattr(exc, "biz_code", None)
        status = getattr(exc, "status", None) or getattr(exc, "status_code", None)
        msg = str(exc).lower()
        is_forbidden = (
            biz_code in _DFS_ACCESS_DENIED_CODES
            or status == 403
            or "forbidden" in msg
            or "permission" in msg
            or "not allowed" in msg
        )
        if is_forbidden:
            typer.echo(
                "ap dfs is currently available to platform admins and allow-listed users only.",
                err=True,
            )
            raise typer.Exit(1) from exc
        raise
    return OssFiles(repo, OssBinding.from_payload(config))


def _validate_options(encoding_type: Optional[str], payer: Optional[str]) -> None:
    if encoding_type not in (None, "url"):
        raise OssUsageError("--encoding-type must be url")
    if payer not in (None, "requester"):
        raise OssUsageError("--payer must be requester")


def _configure(files: OssFiles, encoding_type: Optional[str], payer: Optional[str]) -> None:
    files.encoding_type, files.payer = encoding_type, payer


def _decoded_path(value: str, encoding_type: Optional[str]) -> str:
    if encoding_type != "url":
        return value
    if re.search(r"%(?![0-9a-fA-F]{2})", value):
        raise OssUsageError("Remote path has invalid percent encoding")
    try:
        return unquote(value, errors="strict")
    except UnicodeError as exc:
        raise OssUsageError("Remote path has invalid UTF-8 encoding") from exc


def _parse_ans_path(value: str, *, encoding_type: Optional[str] = None) -> str:
    """Validate a copy; only remove the scheme, leaving binding.resolve to decode once."""
    _validate_options(encoding_type, None)
    if not value.startswith("ans://"):
        raise OssUsageError("Remote paths must start with ans:// (lowercase)")
    raw = value[len("ans://") :]
    _relative(raw)
    _relative(_decoded_path(raw, encoding_type))
    return raw


def _local_operand(value: str) -> str:
    if not value:
        raise OssUsageError("A non-empty local path is required")
    # A Windows drive (including drive-relative C:file) is not a URI scheme.
    drive = re.match(r"^[A-Za-z]:", value)
    if not drive and re.match(r"(?i)^ans:", value):
        raise OssUsageError("Unsupported ans URI; remote paths must start with ans://")
    if not drive and re.match(r"^[A-Za-z][\w+.-]*:", value):
        raise OssUsageError("Unsupported URI; local paths cannot be URLs")
    return value


def _cp_operands(
    src: str, dst: str, *, encoding_type: Optional[str] = None
) -> tuple[str, str, str]:
    remote_src, remote_dst = src.startswith("ans://"), dst.startswith("ans://")
    src = _parse_ans_path(src, encoding_type=encoding_type) if remote_src else _local_operand(src)
    dst = _parse_ans_path(dst, encoding_type=encoding_type) if remote_dst else _local_operand(dst)
    if remote_src and remote_dst:
        return "copy", src, dst
    if remote_src:
        return "download", src, dst
    if remote_dst:
        return "upload", src, dst
    raise OssUsageError(
        "cp requires at least one ans:// operand; two local paths are not supported"
    )


def _read_operand(
    value: str,
    encoding_type: Optional[str],
    *,
    directory: bool = False,
    allow_empty: bool = False,
) -> str:
    """Preserve legacy read operands, checking only syntax before server binding exists."""
    if not value and not allow_empty:
        raise OssUsageError("A non-empty remote path is required")
    if any(unicodedata.category(character) == "Cc" for character in value):
        raise OssUsageError("Remote paths cannot contain control characters")
    if value.startswith("ans://"):
        raw = _parse_ans_path(value, encoding_type=encoding_type)
        decoded = _decoded_path(raw, encoding_type)
    elif value.startswith("oss://"):
        try:
            parsed = urlsplit(value)
            if (
                not parsed.netloc
                or parsed.username
                or parsed.password
                or parsed.port
                or parsed.query
                or parsed.fragment
            ):
                raise OssUsageError("OSS URI cannot include userinfo, port, query or fragment")
            decoded = _decoded_path(parsed.path.removeprefix("/"), encoding_type)
        except ValueError as exc:
            raise OssUsageError(str(exc)) from exc
        raw = value
    else:
        raw = value
        decoded = _decoded_path(value, encoding_type)
    _relative(decoded, allow_empty=allow_empty)
    if not directory and (not decoded or decoded.endswith("/")):
        raise OssUsageError("This operation requires a file path")
    return raw


def _format(value: Optional[str]) -> str:
    from .cli import _normalize_output_format

    return _normalize_output_format(value, keep_table=True)


def _tree(entries: list[dict], root: str) -> None:
    from rich.console import Console
    from rich.text import Text
    from rich.tree import Tree

    base = root.rstrip("/") + "/" if root else ""
    if entries and not all(row["path"].startswith(base) for row in entries):
        base = root.rsplit("/", 1)[0] + "/" if "/" in root else ""
    tree = Tree(Text(_display(base or "./"), style="bold cyan"), guide_style="dim")
    nodes: dict = {}
    for row in entries:
        relative = row["path"][len(base) :] if row["path"].startswith(base) else row["path"]
        if not relative.rstrip("/"):
            continue
        parts = relative.rstrip("/").split("/")
        children = nodes
        for index, part in enumerate(parts):
            directory = (
                index < len(parts) - 1 or row["type"] == "directory" or row["path"].endswith("/")
            )
            key = (part, directory)
            node = children.setdefault(key, {"children": {}})
            if index == len(parts) - 1:
                node["size"] = row.get("size")
            children = node["children"]

    def add(parent, children):
        for (name, directory), node in sorted(
            children.items(), key=lambda item: (not item[0][1], item[0][0].casefold(), item[0][0])
        ):
            label = Text(
                _display(name) + ("/" if directory else ""),
                style="bold blue" if directory else "",
            )
            if not directory and node.get("size") is not None:
                size = float(node["size"])
                for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
                    if size < 1024 or unit == "TiB":
                        break
                    size /= 1024
                label.append(f"  {int(size) if unit == 'B' else f'{size:.1f}'} {unit}", style="dim")
            add(parent.add(label), node["children"])

    add(tree, nodes)
    Console().print(tree)


def _display(value) -> str:
    if not isinstance(value, str):
        return str(value)
    # JSON escapes C0 controls. With ensure_ascii=False, escape the remaining
    # Unicode C1 controls explicitly while preserving ordinary Unicode text.
    escaped = json.dumps(value, ensure_ascii=False)[1:-1]
    return "".join(
        f"\\u{ord(character):04x}" if unicodedata.category(character) == "Cc" else character
        for character in escaped
    )


def _emit(value: dict, output_format: str, *, short: bool = False, root: str = "") -> None:
    if output_format in ("json", "yaml"):
        from .cli import _print_formatted

        _print_formatted(value, output_format)
    elif "entries" in value and "is_truncated" in value:
        if short:
            for row in value["entries"]:
                typer.echo(_display(row["path"]))
        else:
            _tree(value["entries"], root)
        if value["is_truncated"]:
            typer.echo(
                "Listing truncated; continue with --marker " + _display(value["next_marker"]),
                err=True,
            )
    elif "entries" in value:
        for row in value["entries"]:
            typer.echo(
                f"{_display(row['path'])}: {_display(row['algorithm'])} {_display(row['hash'])}"
            )
        for item in value["failed"]:
            typer.echo(f"error: {_display(item['path'])}: {_display(item['error'])}", err=True)
    elif "completed" in value:
        typer.echo(
            f"Completed: {value['completed_count']}; skipped: {value['skipped_count']}; "
            f"failed: {value['failed_count']}"
        )
        for item in value["failed"]:
            typer.echo(f"error: {_display(item['path'])}: {_display(item['error'])}", err=True)
    else:
        for key, item in value.items():
            typer.echo(f"{_display(key)}: {_display(item)}")


def _fail(exc: Exception) -> None:
    from .config import ConfigurationError
    from .irepo_sdk import SdkMissing

    if isinstance(exc, SdkMissing):
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from exc
    input_errors = (OssUsageError, ConfigurationError, typer.BadParameter)
    message = (
        str(exc) if isinstance(exc, (ConfigurationError, typer.BadParameter)) else safe_error(exc)
    )
    typer.echo("error: " + _display(message), err=True)
    if getattr(exc, "biz_code", None):
        typer.echo(f"hint: Check the Dataset access grant (API code {exc.biz_code})", err=True)
    elif getattr(exc, "code", None) == "AccessDenied":
        typer.echo("hint: Check the Dataset reader/writer grant for this operation", err=True)
    raise typer.Exit(2 if isinstance(exc, input_errors) else 1) from exc


@dfs_app.command("ls")
def dfs_ls(
    path: str = typer.Argument(..., help="ans://, repo-relative prefix or full oss:// URI"),
    directory: bool = typer.Option(
        False,
        "--directory",
        "-d",
        help="List only the current level (directory semantics without a trailing slash)",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Expand all directory levels; without a trailing slash PATH is a key prefix",
    ),
    short: bool = typer.Option(False, "--short-format", "-s", help="Print only paths"),
    limited_num: Optional[int] = typer.Option(None, "--limited-num", min=1),
    marker: str = typer.Option(
        "", "--marker", help="Resume after ans://, a relative path or full oss:// URI"
    ),
    include: Optional[list[str]] = typer.Option(None, "--include"),
    exclude: Optional[list[str]] = typer.Option(None, "--exclude"),
    encoding_type: Optional[str] = typer.Option(None, "--encoding-type"),
    payer: Optional[str] = typer.Option(None, "--payer"),
    output_format: Optional[str] = typer.Option(None, "--output-format", "--format"),
):
    """List remote paths, without reading object content; default is one level, -r expands all.

    Accepts ans://, repo-relative paths or full oss:// URIs; output stays repo-relative.
    Omitting the trailing slash means directory semantics only at the default one level;
    with -r, a path without a trailing slash is a key prefix, so add a trailing slash
    (or use -d) to list one directory instead.
    Uses AP-managed reader/list-only credentials; listing prefers private networking with
    a public endpoint fallback. Example: ap dfs ls ans://team/bench/train -r --format json.
    """
    try:
        fmt = _format(output_format)
        _validate_options(encoding_type, payer)
        if recursive and directory:
            raise OssUsageError("Use either --recursive or --directory")
        path = _read_operand(path, encoding_type, directory=True)
        marker = _read_operand(marker, encoding_type, directory=True, allow_empty=True)
        files = _files()
        _configure(files, encoding_type, payer)
        remote = (
            files.resolve(path, prefix=True) if recursive else files.resolve(path, directory=True)
        )
        _emit(
            files.list(
                remote,
                recursive=recursive,
                limit=limited_num,
                marker=marker,
                include=tuple(include or ()),
                exclude=tuple(exclude or ()),
            ),
            fmt,
            short=short,
            root=remote.path,
        )
    except Exception as exc:
        _fail(exc)


@dfs_app.command("stat")
def dfs_stat(
    path: str = typer.Argument(..., help="ans://, repo-relative path or full oss:// URI"),
    encoding_type: Optional[str] = typer.Option(None, "--encoding-type"),
    payer: Optional[str] = typer.Option(None, "--payer"),
    output_format: Optional[str] = typer.Option(None, "--output-format", "--format"),
):
    """Show remote object metadata and ACL using reader credentials; no content download.

    Accepts ans://, repo-relative or full oss:// paths. Uses AP-managed reader credentials;
    metadata prefers private networking with a public endpoint fallback. Example:
    ap dfs stat ans://team/bench/train/T001.json --format json.
    """
    try:
        fmt = _format(output_format)
        _validate_options(encoding_type, payer)
        path = _read_operand(path, encoding_type)
        files = _files()
        _configure(files, encoding_type, payer)
        _emit(files.stat(files.resolve(path)), fmt)
    except Exception as exc:
        _fail(exc)


@dfs_app.command("cat")
def dfs_cat(
    path: str = typer.Argument(..., help="ans://, repo-relative path or full oss:// URI"),
    encoding_type: Optional[str] = typer.Option(None, "--encoding-type"),
    payer: Optional[str] = typer.Option(None, "--payer"),
):
    """Stream full remote content as original bytes to stdout; requires private-network access.

    Accepts ans://, repo-relative or full oss:// paths; no metadata or progress on stdout.
    Uses AP-managed reader credentials and private networking only, with no public fallback.
    Example: ap dfs cat ans://team/bench/train/T001.json > T001.json.
    """
    import sys

    try:
        _validate_options(encoding_type, payer)
        path = _read_operand(path, encoding_type)
        files = _files()
        _configure(files, encoding_type, payer)
        files.cat(files.resolve(path), sys.stdout.buffer)
    except BrokenPipeError:
        import os
        import sys

        try:
            fd = os.open(os.devnull, os.O_WRONLY)
            try:
                os.dup2(fd, sys.stdout.fileno())
            finally:
                os.close(fd)
        except (OSError, ValueError):
            pass
        raise typer.Exit(0)
    except Exception as exc:
        _fail(exc)


Recursive = Annotated[bool, typer.Option("--recursive", "-r")]
Force = Annotated[bool, typer.Option("--force", "-f", help="Overwrite without confirmation")]
Update = Annotated[bool, typer.Option("--update", "-u", help="Copy only missing or older targets")]
Jobs = Annotated[int, typer.Option("--jobs", "--job", "-j", min=1, max=10000)]
Parallel = Annotated[int, typer.Option("--parallel", min=1, max=10000)]
BigFileThreshold = Annotated[int, typer.Option("--bigfile-threshold", min=0)]
PartSize = Annotated[Optional[int], typer.Option("--part-size", min=1)]
CheckpointDir = Annotated[Optional[Path], typer.Option("--checkpoint-dir")]
Include = Annotated[Optional[list[str]], typer.Option("--include")]
Exclude = Annotated[Optional[list[str]], typer.Option("--exclude")]
OnlyCurrentDir = Annotated[bool, typer.Option("--only-current-dir")]
DisableIgnoreError = Annotated[bool, typer.Option("--disable-ignore-error")]
DisableCrc64 = Annotated[bool, typer.Option("--disable-crc64")]
DisableAllSymlink = Annotated[bool, typer.Option("--disable-all-symlink")]
ByteRange = Annotated[
    Optional[str], typer.Option("--range", help="Download bytes: START-END, START-, or -END")
]
Meta = Annotated[
    Optional[str], typer.Option("--meta", help="Object metadata: header:value#header:value")
]
StartTime = Annotated[Optional[int], typer.Option("--start-time", min=0)]
EndTime = Annotated[Optional[int], typer.Option("--end-time", min=0)]
EncodingType = Annotated[Optional[str], typer.Option("--encoding-type")]
Payer = Annotated[Optional[str], typer.Option("--payer")]
OutputFormat = Annotated[Optional[str], typer.Option("--output-format", "--format")]


def _range(value: Optional[str]) -> tuple[Optional[int], Optional[int]] | None:
    if value is None:
        return None
    if not re.fullmatch(r"\d*-\d*", value) or value == "-":
        raise OssUsageError("--range must be START-END, START-, or -END")
    start, end = value.split("-", 1)
    lowest, highest = int(start) if start else None, int(end) if end else None
    if lowest is None and highest == 0:
        raise OssUsageError("--range suffix length must be positive")
    if lowest is not None and highest is not None and lowest > highest:
        raise OssUsageError("--range start cannot exceed end")
    # oss2 requires (None, END) for the last END bytes, never (0, END).
    return lowest, highest


def _metadata(value: Optional[str]) -> dict[str, str]:
    headers: dict[str, str] = {}
    if value is None:
        return headers
    for item in value.split("#"):
        key, separator, content = item.partition(":")
        allowed = key.lower() in (
            "cache-control",
            "content-disposition",
            "content-encoding",
            "content-type",
            "expires",
        ) or key.lower().startswith("x-oss-meta-")
        if not separator or not allowed or any(c in key + content for c in "\r\n"):
            raise OssUsageError("--meta requires standard content headers or x-oss-meta-* headers")
        headers[key] = content
    return headers


def _transfer(direction: str, src: str, dst: str, ctx: typer.Context) -> None:
    options = ctx.params
    recursive = bool(options.get("recursive"))
    force = bool(options.get("force"))
    update = bool(options.get("update"))
    only_current_dir = bool(options.get("only_current_dir"))
    disable_ignore_error = bool(options.get("disable_ignore_error"))
    disable_crc64 = bool(options.get("disable_crc64"))
    disable_all_symlink = bool(options.get("disable_all_symlink"))
    byte_range = options.get("byte_range")
    meta = options.get("meta")
    start_time = options.get("start_time")
    end_time = options.get("end_time")
    lock = threading.Lock()

    def progress(path, done, total):
        with lock:
            typer.echo(f"{_display(path)}: {done}/{total} bytes", err=True)

    def confirm(path):
        import sys

        with lock:
            while True:
                typer.echo(f"Overwrite {_display(path)}? [y/N]: ", err=True, nl=False)
                answer = sys.stdin.readline()
                if not answer:
                    raise OssUsageError(
                        "Overwrite confirmation requires input; use --force for batch operations"
                    )
                answer = answer.strip().lower()
                if answer in ("y", "yes"):
                    return True
                if answer in ("", "n", "no"):
                    return False
                typer.echo("Enter y or n", err=True)

    try:
        fmt = _format(options.get("output_format"))
        if start_time is not None and end_time is not None and start_time > end_time:
            raise OssUsageError("--start-time cannot be later than --end-time")
        encoding_type, payer = options.get("encoding_type"), options.get("payer")
        _validate_options(encoding_type, payer)
        if byte_range is not None and (
            direction != "download" or recursive or _decoded_path(src, encoding_type).endswith("/")
        ):
            raise OssUsageError("--range requires a non-recursive single-object download")
        if direction != "upload":
            _read_operand(src, encoding_type, directory=recursive)
        if meta is not None and direction == "download":
            raise OssUsageError("--meta is only allowed for upload or copy")
        if disable_all_symlink and direction != "upload":
            raise OssUsageError("--disable-all-symlink is only allowed for upload")
        parsed_range = _range(byte_range)
        headers = _metadata(meta)
        files = _files()
        from .irepo_sdk import _is_verbose

        files.verbose = _is_verbose()
        _configure(files, encoding_type, payer)
        files.disable_crc64 = disable_crc64
        files.disable_all_symlink = disable_all_symlink
        files.byte_range = parsed_range
        files.write_headers = headers
        files.multipart_threshold = options.get("bigfile_threshold", 100 * 1024 * 1024)
        files.part_size = options.get("part_size")
        checkpoint_dir = options.get("checkpoint_dir")
        if checkpoint_dir is not None:
            # ctx.params carries the raw value; Typer only converts to Path in the callback.
            files.state_dir = Path(checkpoint_dir)
        result = files.cp(
            src,
            dst,
            direction=direction,
            recursive=recursive,
            overwrite=force,
            jobs=options.get("jobs", 3),
            parallel=options.get("parallel", 4),
            progress=progress,
            update=update,
            include=tuple(options.get("include") or ()),
            exclude=tuple(options.get("exclude") or ()),
            only_current_dir=only_current_dir,
            stop_on_error=disable_ignore_error,
            confirm=None if force or update else confirm,
            start_time=start_time,
            end_time=end_time,
        )
    except Exception as exc:
        _fail(exc)
        return
    _emit(result, fmt)
    if result["failed_count"]:
        raise typer.Exit(1)


@dfs_app.command("cp")
def dfs_cp(
    ctx: typer.Context,
    src: str = typer.Argument(..., help="Local path or ans:// repo-relative source"),
    dst: str = typer.Argument(..., help="Required local path or ans:// repo-relative destination"),
    recursive: Recursive = False,
    force: Force = False,
    update: Update = False,
    jobs: Jobs = 3,
    parallel: Parallel = 4,
    bigfile_threshold: BigFileThreshold = 100 * 1024 * 1024,
    part_size: PartSize = None,
    checkpoint_dir: CheckpointDir = None,
    include: Include = None,
    exclude: Exclude = None,
    only_current_dir: OnlyCurrentDir = False,
    disable_ignore_error: DisableIgnoreError = False,
    disable_crc64: DisableCrc64 = False,
    disable_all_symlink: DisableAllSymlink = False,
    byte_range: ByteRange = None,
    meta: Meta = None,
    start_time: StartTime = None,
    end_time: EndTime = None,
    encoding_type: EncodingType = None,
    payer: Payer = None,
    output_format: OutputFormat = None,
):
    """Upload local -> ans://, download ans:// -> local, or copy ans:// -> ans://.

    Both SRC and DST are required; two local paths and other URI schemes are rejected.
    Directories still require -r, copying contents without adding the source directory name.
    Uploading a file to a remote trailing slash preserves its basename; otherwise DST is exact.
    Downloads read full content unless --range is set (non-recursive single-object download only).
    --meta is upload/copy-only; --disable-all-symlink is upload-only.
    Downloads use AP-managed reader credentials and private networking only. Uploads and
    remote copies use writer credentials, preferring private networking with public fallback.
    Remote copy stays server-side. No ingest.

    Examples: ap dfs cp ans://team/bench/train/T001.json ./;
    ap dfs cp ans://team/bench/train ./ -r;
    ap dfs cp ./abc ans://team/bench/train/;
    ap dfs cp ans://team/bench/train/T001.json ans://team/bench/test/T001.json.
    """
    try:
        direction, src, dst = _cp_operands(src, dst, encoding_type=encoding_type)
    except Exception as exc:
        _fail(exc)
        return
    _transfer(direction, src, dst, ctx)


@dfs_app.command("mkdir")
def dfs_mkdir(
    path: str = typer.Argument(..., help="Remote directory, required ans:// repo-relative path"),
    encoding_type: EncodingType = None,
    payer: Payer = None,
    output_format: OutputFormat = None,
):
    """Create a remote directory marker using writer credentials; no content read or ingest.

    Only ans:// remote directories are accepted, not local or legacy relative paths.
    Uses AP-managed writer credentials, preferring private networking with public fallback.
    Example: ap dfs mkdir ans://team/bench/train/ --format json.
    """
    try:
        fmt = _format(output_format)
        _validate_options(encoding_type, payer)
        raw = _parse_ans_path(path, encoding_type=encoding_type)
        files = _files()
        _configure(files, encoding_type, payer)
        _emit(files.mkdir(files.resolve(raw, directory=True)), fmt)
    except Exception as exc:
        _fail(exc)


@dfs_app.command("hash")
def dfs_hash(
    algorithm: str = typer.Argument(..., help="Hash algorithm: md5 or crc64"),
    path: str = typer.Argument(..., help="Local path or ans:// repo-relative path"),
    download: bool = typer.Option(
        False,
        "--download",
        help="Read full remote content instead of stored metadata; private network required",
    ),
    base64_output: bool = typer.Option(False, "--base64", help="Print MD5 in base64; md5-only"),
    recursive: Recursive = False,
    encoding_type: EncodingType = None,
    payer: Payer = None,
    output_format: OutputFormat = None,
):
    """Hash ALGORITHM PATH: md5 or crc64, locally or remotely with ans://.

    Local hashing always reads full content, with no SDK or credentials, and requires secure
    dirfd/no-follow platform support; unsupported platforms can still use ans:// remote hash.
    --download, --encoding-type and --payer are remote-only.
    Remote hashing uses AP-managed reader credentials. Metadata prefers private networking with
    public fallback. Missing/invalid metadata or --download reads full content through private
    networking only, with no public fallback.
    --base64 is md5-only. Directories require --recursive/-r.
    Examples: ap dfs hash md5 ./abc; ap dfs hash crc64 ans://team/bench/train/T001.json;
    ap dfs hash md5 ans://team/bench/train -r --download --base64.
    """
    try:
        fmt = _format(output_format)
        _validate_options(encoding_type, payer)
        if algorithm not in ("md5", "crc64"):
            raise OssUsageError("Hash algorithm must be md5 or crc64")
        if base64_output and algorithm != "md5":
            raise OssUsageError("--base64 is only allowed for md5")
        if path.startswith("ans://"):
            raw = _parse_ans_path(path, encoding_type=encoding_type)
            _read_operand(path, encoding_type, directory=recursive)
            files = _files()
            _configure(files, encoding_type, payer)
            result = files.hash(
                raw,
                algorithm,
                download=download,
                base64_output=base64_output,
                recursive=recursive,
            )
        else:
            if download or encoding_type is not None or payer is not None:
                raise OssUsageError(
                    "--download, --encoding-type and --payer are only supported for remote ans:// hash"
                )
            local = _local_operand(path)
            from .ossutil_hash import hash_local

            result = hash_local(local, algorithm, base64_output=base64_output, recursive=recursive)
        _emit(result, fmt)
        if result.get("failed_count"):
            raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as exc:
        _fail(exc)
