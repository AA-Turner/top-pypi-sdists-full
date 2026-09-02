from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _is_printable_ascii(data: bytes) -> bool:
    if not data:
        return True
    for b in data:
        if b == 0x09 or b == 0x0A or b == 0x0D:
            continue
        if 0x20 <= b < 0x7F:
            continue
        return False
    return True


def _is_utf8_text(data: bytes) -> bool:
    try:
        decoded = data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    for ch in decoded:
        cp = ord(ch)
        if cp == 0x09 or cp == 0x0A or cp == 0x0D:
            continue
        if cp < 0x20:
            return False
    return True


def _looks_like_json(data: bytes) -> bool:
    stripped = data.lstrip()
    if not stripped:
        return False
    return stripped[0:1] in (b"{", b"[")


def _identify_known_signature(data: bytes) -> str | None:
    if data.startswith(b"\x7fELF"):
        return "ELF executable"
    if data.startswith(b"%PDF"):
        return "PDF document"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG image data"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "GIF image data"
    if data.startswith(b"\xff\xd8\xff"):
        return "JPEG image data"
    if data.startswith(b"PK\x03\x04"):
        return "Zip archive data"
    if data.startswith(b"\x1f\x8b"):
        return "gzip compressed data"
    return None


def _identify_script(first_line: bytes, path: str) -> str | None:
    lower = path.lower()
    if first_line.startswith(b"#!"):
        interpreter = first_line[2:].strip().decode("latin-1", errors="replace")
        if "python" in interpreter:
            return "Python script, ASCII text executable"
        if "bash" in interpreter:
            return "Bourne-Again shell script, ASCII text executable"
        if interpreter.startswith("/bin/sh") or interpreter.endswith("/sh"):
            return "POSIX shell script, ASCII text executable"
        if "node" in interpreter:
            return "Node.js script, ASCII text executable"
        return "a script text executable"
    if lower.endswith(".py"):
        return "Python script, ASCII text"
    if lower.endswith(".sh"):
        return "Bourne-Again shell script, ASCII text"
    return None


def _classify_content(data: bytes, path: str) -> str:
    if not data:
        return "empty"

    sig = _identify_known_signature(data)
    if sig is not None:
        return sig

    sample = data[:512]
    has_null = b"\x00" in sample

    first_nl = data.find(b"\n")
    first_line = data[: first_nl if first_nl >= 0 else len(data)]
    script = _identify_script(first_line, path)

    lower = path.lower()
    if lower.endswith(".json") or _looks_like_json(sample):
        if not has_null and _is_utf8_text(sample):
            return "JSON text data"

    if has_null:
        return "data"

    if script is not None:
        return script

    if _is_printable_ascii(sample):
        return "ASCII text"

    if _is_utf8_text(sample):
        return "UTF-8 Unicode text"

    return "data"


@register("file")
async def cmd_file(ctx: CommandContext) -> CommandResult:
    args = ctx.args

    paths: list[str] = []
    end_of_opts = False
    for a in args:
        if end_of_opts:
            paths.append(a)
            continue
        if a == "--":
            end_of_opts = True
            continue
        if a.startswith("-") and len(a) > 1:
            # We accept and silently ignore common flags (-b, -L, -i, -h, etc.).
            continue
        paths.append(a)

    if not paths:
        return ok()

    out = bytearray()
    for display in paths:
        abs_path = display if display.startswith("/") else resolve_cwd(ctx.env, display)
        try:
            info = await ctx.vfs._info(abs_path)
        except FileNotFoundError:
            out.extend(
                encode(f"{display}: cannot open `{display}' (No such file or directory)\n")
            )
            continue
        except OSError:
            out.extend(
                encode(f"{display}: cannot open `{display}' (No such file or directory)\n")
            )
            continue

        kind = info.get("type", "file")
        if kind == "directory":
            out.extend(encode(f"{display}: directory\n"))
            continue
        if kind == "link":
            target = info.get("symlink_target") or ""
            out.extend(encode(f"{display}: symbolic link to {target}\n"))
            continue

        try:
            data = await ctx.vfs._cat_file(abs_path)
        except OSError:
            out.extend(encode(f"{display}: data\n"))
            continue
        description = _classify_content(data, abs_path)
        out.extend(encode(f"{display}: {description}\n"))

    return CommandResult(stdout=bytes(out), stderr=b"", exit_code=0)
