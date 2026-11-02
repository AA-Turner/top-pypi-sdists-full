"""image.py — Dockerfile 改写（final / base 两种 tar 语义）+ FROM 解析。

tar_role="final"：image.tar.gz 是构建好的最终镜像 → FROM 换成 ACR tag，
  RUN / 带 URL 的 ADD 已烘焙进镜像，改写为注释；保留 COPY/ENV/WORKDIR 等安全指令。
tar_role="base"：image.tar.gz 是私有 base → 只换第一个 FROM，后续步骤保留。
纯文本处理、无 I/O 之外副作用（除写回目标 Dockerfile），便于跨语言 conformance。
"""
from __future__ import annotations

from pathlib import Path

_SAFE_INSTRUCTIONS = {
    "COPY", "WORKDIR", "ENV", "USER", "ENTRYPOINT", "CMD", "LABEL",
    "EXPOSE", "VOLUME", "ARG", "SHELL", "STOPSIGNAL", "HEALTHCHECK",
}


def dockerfile_from(dockerfile_text: str) -> str:
    """返回第一个 FROM 的镜像引用；FROM $ARG 或无 FROM 返回空串。"""
    for ln in dockerfile_text.splitlines():
        s = ln.strip()
        if s.upper().startswith("FROM "):
            ref = s.split()[1]
            return "" if ref.startswith("$") else ref
    return ""


def _logical_lines(text: str) -> list[str]:
    """把物理行合并为逻辑指令（处理行尾续行 '\\'）。"""
    logical: list[str] = []
    buf: list[str] = []
    for ln in text.splitlines():
        if buf:
            buf.append(ln)
            if not ln.rstrip().endswith("\\"):
                logical.append("\n".join(buf))
                buf = []
            continue
        if ln.rstrip().endswith("\\") and not ln.lstrip().startswith("#"):
            buf = [ln]
        else:
            logical.append(ln)
    if buf:
        logical.append("\n".join(buf))
    return logical


def rewrite_base(dockerfile_text: str, target: str) -> str:
    """base 模式：只换第一个 FROM，其余保留。"""
    out, replaced = [], False
    for ln in dockerfile_text.splitlines():
        if ln.strip().upper().startswith("FROM ") and not replaced:
            out.append(f"FROM {target}")
            replaced = True
        else:
            out.append(ln)
    return "\n".join(out) + "\n"


def rewrite_final(dockerfile_text: str, target: str) -> tuple[str, list[str]]:
    """final 模式：FROM {target} + 仅保留安全指令，丢弃 RUN / URL-ADD（注释保留
    可追溯）。多阶段只看最后一个 FROM 之后。返回 (新文本, 被丢弃指令名列表)。"""
    lines = _logical_lines(dockerfile_text)
    last_from = -1
    for i, l in enumerate(lines):
        if l.strip().upper().startswith("FROM "):
            last_from = i
    tail = lines[last_from + 1:] if last_from >= 0 else lines
    out = [f"FROM {target}"]
    dropped: list[str] = []
    for l in tail:
        s = l.strip()
        if not s or s.startswith("#"):
            out.append(l)
            continue
        instr = s.split()[0].upper()
        low = s.lower()
        if instr in _SAFE_INSTRUCTIONS:
            out.append(l)
        elif instr == "ADD" and "http://" not in low and "https://" not in low:
            out.append(l)  # 本地 ADD ≈ COPY（无网络）
        else:
            dropped.append(instr)
            first = s.splitlines()[0][:100]
            more = " \\ ..." if "\n" in l else ""
            out.append(f"# [tar-role=final] dropped (baked into image): {first}{more}")
    return "\n".join(out) + "\n", dropped


def rewrite_dockerfile(dockerfile_path: str | Path, target: str, *,
                       tar_role: str = "final") -> list[str]:
    """就地改写 Dockerfile 文件；返回 final 模式下被丢弃的指令名（base 模式为 []）。"""
    p = Path(dockerfile_path)
    text = p.read_text()
    if tar_role == "final":
        new_text, dropped = rewrite_final(text, target)
    else:
        new_text, dropped = rewrite_base(text, target), []
    p.write_text(new_text)
    return dropped
