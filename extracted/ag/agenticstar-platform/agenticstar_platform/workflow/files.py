"""`/workspace` の展開・回収（marketplace-3.0 03 §3、AC-07）。

- input は契約上 read-only（展開後に 0444）。work は input のコピー。output は **契約 outputs に宣言された path だけ** 回収する
  （`source='work'` の output = 編集対象。任意 glob / 全 workspace 回収はしない）
- root は Agent 起動 **前** に開いた directory fd で固定する（Agent が output/ 自体を symlink に置き換えても外へ出ない）。
  ファイルは root fd からの相対 open（O_NOFOLLOW | O_NONBLOCK）→ fstat で regular file・リンク数 1・サイズ上限を確認 →
  **同じ fd から読んだ bytes** を digest・保存する（validated fd と保存 bytes が一致する）
- 上限: 1 ファイル 20MiB / 実行 100MiB・100 件 / 編集対象（source=work）1MiB
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .canonical import canonical_json
from .errors import InputIntegrityError, OutputCollectionError
from .schema import SchemaError, json_equal, parse_yaml_strict, validate_file_content

FILE_BYTES = 20 * 1024 * 1024
EXECUTION_BYTES = 100 * 1024 * 1024
EXECUTION_FILES = 100
EDIT_BYTES = 1024 * 1024
FORMATS = ("markdown", "yaml", "json", "text", "binary")


def relative_path(value: str) -> str:
    """契約 / manifest の相対 path。絶対 / `..` / backslash / 空は拒否。"""
    if not isinstance(value, str) or not value or value.startswith("/") or "\\" in value:
        raise OutputCollectionError(f"invalid relative path: {value!r}")
    parts = [p for p in value.split("/") if p not in ("", ".")]
    if not parts or any(p == ".." for p in parts):
        raise OutputCollectionError(f"invalid relative path: {value!r}")
    return "/".join(parts)


def safe_join(root: Path, rel: str) -> Path:
    """root 配下の path に限定する（展開 = Agent 起動前の書き込み用。回収は root fd 経由）。"""
    rel = relative_path(rel)
    root_r = root.resolve()
    candidate = (root_r / rel)
    resolved = candidate.resolve(strict=False)
    if resolved != root_r and root_r not in resolved.parents:
        raise OutputCollectionError(f"path escapes workspace root: {rel}")
    return candidate


class WorkspaceRoot:
    """Agent 起動前に開いた directory fd。以後の回収はこの fd からの相対 open だけを信用する。"""

    def __init__(self, path: Path):
        self.path = path
        path.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(path), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    def close(self) -> None:
        try:
            os.close(self.fd)
        except OSError:
            pass

    def read_regular(self, rel: str, limit: int) -> Optional[bytes]:
        """rel を root fd から O_NOFOLLOW で辿って読む。無ければ None。regular file 以外 / リンク / 上限超過は例外。"""
        rel = relative_path(rel)
        parts = rel.split("/")
        cur = self.fd
        opened: list[int] = []
        try:
            for i, part in enumerate(parts):
                last = i == len(parts) - 1
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | (0 if last else os.O_DIRECTORY)
                try:
                    nxt = os.open(part, flags, dir_fd=cur)
                except FileNotFoundError:
                    return None
                except OSError as e:
                    raise OutputCollectionError(f"cannot open {rel}: {e.strerror}")
                opened.append(nxt)
                cur = nxt
            try:
                st = os.fstat(cur)
            except OSError as e:
                raise OutputCollectionError(f"cannot stat {rel}: {e.strerror}")
            if not stat.S_ISREG(st.st_mode):
                raise OutputCollectionError(f"not a regular file: {rel}")
            if st.st_nlink != 1:
                raise OutputCollectionError(f"hard-linked file is not accepted: {rel}")
            if st.st_size > limit:
                raise OutputCollectionError(f"file exceeds limit ({st.st_size} > {limit}): {rel}")
            chunks: list[bytes] = []
            total = 0
            while True:
                try:
                    b = os.read(cur, 1024 * 1024)   # 読み出しの I/O エラーも回収失敗に正規化（例外を外へ出さない）
                except OSError as e:
                    raise OutputCollectionError(f"cannot read {rel}: {e.strerror}")
                if not b:
                    break
                total += len(b)
                if total > limit:
                    raise OutputCollectionError(f"file grew past limit during collection: {rel}")
                chunks.append(b)
            return b"".join(chunks)
        finally:
            for fd in reversed(opened):
                try:
                    os.close(fd)
                except OSError:
                    pass


@dataclass(frozen=True)
class CollectedFile:
    logical_name: str
    path: str            # 契約上の相対 path（output_dir または work_dir 基準）
    source: str          # "output" | "work"
    format: str
    content: bytes       # validated fd から読んだ bytes（これを保存する）
    sha256: str
    size: int
    required: bool


def write_input(root: Path, rel: str, data: bytes, *, expected_sha256: Optional[str], expected_size: Optional[int],
                fmt: Optional[str] = None, schema: Any = None) -> Path:
    """入力 artifact を root/rel に展開（digest / size / 形式 / schema を検証）。"""
    if len(data) > FILE_BYTES:
        raise InputIntegrityError(f"input exceeds per-file limit: {rel}")
    if expected_size is not None and len(data) != int(expected_size):
        raise InputIntegrityError(f"input size mismatch for {rel}")
    digest = hashlib.sha256(data).hexdigest()
    if expected_sha256 and digest != expected_sha256.lower():
        raise InputIntegrityError(f"input digest mismatch for {rel}")
    if fmt in ("json", "yaml"):
        try:
            validate_file_content(fmt, data, schema)
        except SchemaError as e:
            raise InputIntegrityError(f"input {rel} rejected: {e}")
    path = safe_join(root, rel)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".part")
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)
    os.chmod(path, 0o444)
    return path


def copy_input_to_work(input_dir: Path, work_dir: Path) -> None:
    """input → work のコピー（symlink は追わずコピーしない。work 側は書き込み可）。"""
    work_dir.mkdir(parents=True, exist_ok=True)
    for src in sorted(input_dir.rglob("*")):
        rel = src.relative_to(input_dir)
        if src.is_symlink():
            continue
        dst = work_dir / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            os.chmod(dst, 0o644)


def render_from_parameters(fmt: str, parameters: dict[str, Any], schema: Any = None) -> bytes:
    """`from_parameters=true` の設定ファイルを parameters から生成する（00 §2: env と YAML で別々の値を保存しない）。
    YAML は JSON 表記（JSON は YAML 1.2 の部分集合）で書く = 安全な parser でそのまま読める。schema があれば検証。"""
    if fmt not in ("json", "yaml"):
        raise OutputCollectionError(f"from_parameters file must be json or yaml, got {fmt}")
    if schema is not None:
        try:
            validate_file_content("json", json.dumps(parameters).encode("utf-8"), schema)
        except SchemaError as e:
            raise OutputCollectionError(f"parameters do not satisfy the file schema: {e}")
    if fmt == "json":
        return (json.dumps(parameters, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    rendered = (canonical_json(parameters) + "\n").encode("utf-8")
    try:
        if not json_equal(parse_yaml_strict(rendered), parameters):  # 生成した YAML を自分の parser で読み戻して同値を確認
            raise OutputCollectionError("rendered YAML does not round-trip the parameters")
    except SchemaError as e:
        raise OutputCollectionError(f"rendered YAML is not accepted by the strict parser: {e}")
    return rendered


def collect_outputs(*, output_root: WorkspaceRoot, work_root: WorkspaceRoot, outputs: list[dict[str, Any]],
                    files: list[dict[str, Any]], input_root: Optional[WorkspaceRoot] = None) -> list[CollectedFile]:
    """契約 outputs だけを回収する（front の artifact 保存 API は outputs に宣言された名前しか受けない）。
    `source='work'` の output は編集対象 = **常に** 1MiB 上限。input と同じ digest の任意（required でない）編集対象は
    未編集として回収しない（required なら同じ内容でも実行の output として保存する）。
    json / yaml は parse と `schema`（output 自身の宣言、無ければ **同じ work path の入力 file の schema**）を検証する。
    required の **欠落** は例外にしない（呼出し側が判定）。不正 / 読めない output は OutputCollectionError。"""
    editable_paths = {relative_path(str(f.get("path"))) for f in files if f.get("editable") and f.get("path")}
    file_schemas = {relative_path(str(f.get("path"))): f.get("schema") for f in files if f.get("path")}
    collected: list[CollectedFile] = []
    total = 0
    seen: set[str] = set()
    for o in outputs:
        name = str(o.get("name"))
        source = str(o.get("source") or "output")
        if source not in ("output", "work"):
            raise OutputCollectionError(f"unsupported output source: {source}")
        rel = relative_path(str(o.get("path")))
        key = f"{source}:{rel}"
        if key in seen:
            raise OutputCollectionError(f"duplicate output path: {key}")
        seen.add(key)
        fmt = str(o.get("format") or "text")
        if fmt not in FORMATS:
            raise OutputCollectionError(f"unsupported format {fmt} for {name}")
        root = output_root if source == "output" else work_root
        limit = EDIT_BYTES if source == "work" else FILE_BYTES  # work（編集対象）は宣言の有無に関わらず 1MiB
        content = root.read_regular(rel, limit)
        if content is None:
            continue  # 無い output は回収しない（required の欠落は runner が envelope の failed/required_output_missing にする）
        if source == "work" and input_root is not None and rel in editable_paths and not o.get("required"):
            original = input_root.read_regular(rel, limit)
            if original is not None and original == content:
                continue  # 未編集の任意 output は新しい出力版にしない
        schema = o.get("schema")
        if schema is None and source == "work":
            schema = file_schemas.get(rel)  # 入力 file の schema は同じ work path の編集にだけ適用（output/ には継承しない）
        try:
            validate_file_content(fmt, content, schema)
        except SchemaError as e:
            raise OutputCollectionError(f"output {name} rejected: {e}")
        total += len(content)
        if total > EXECUTION_BYTES or len(collected) + 1 > EXECUTION_FILES:
            raise OutputCollectionError("execution artifact limit exceeded")
        collected.append(CollectedFile(logical_name=name, path=rel, source=source, format=fmt, content=content,
                                       sha256=hashlib.sha256(content).hexdigest(), size=len(content),
                                       required=bool(o.get("required"))))
    return collected
