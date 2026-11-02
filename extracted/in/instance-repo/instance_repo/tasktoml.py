"""tasktoml.py — 就地改写 harbor 实例的 ``task.toml``（只碰 ``[environment].docker_image``）。

为什么需要这个模块：**运行期真正决定拉哪个镜像的是 ``task.toml`` 里的
``[environment].docker_image``**，不是实例元数据（MongoDB / ``{id}.json``）里的
``docker_image`` 字段。harbor runner 从 OSS 取 ``content.tgz``、解包、读 ``task.toml``，
把该值喂给容器编排去 pull；apiserver 侧没有任何执行路径读元数据里的 ``docker_image``。

而上架（benchmark-release）是**逐字节复制** ``content.tgz`` 到目标桶的，于是生产副本里的
``task.toml`` 仍写着开发态 registry。上架把镜像层搬到了生产 ACR，运行期却仍按开发态地址
去拉——在配了镜像源兜底的集群上静默无害，在默认配置的集群上就是从生产 VPC 拉开发 registry。
本模块是修这个缺口的第一块砖：把目标引用写进 ``task.toml``，再重新打包。

**为什么用行级正则而不是 TOML 序列化器**：往回写 TOML 会丢注释、重排键序、改动引号风格，
让生产副本与开发副本产生大量无意义 diff，审计时无法一眼看出"只改了镜像地址"。这里改成
定位到 ``[environment]`` 段内的那一行做替换，其余字节原样保留——**改动最小、可审计**。
标准库的 ``tomllib`` 只读，也没有官方 writer，所以这不是绕路而是唯一稳妥选择。
"""
from __future__ import annotations

import re

from .errors import SchemaError

#: 段头：行首（允许前导空白）的 ``[section]``；不匹配 ``[[array.of.tables]]``。
_SECTION_RE = re.compile(r"^[ \t]*\[[ \t]*([^\[\]]+?)[ \t]*\][ \t]*(?:#.*)?$")
#: ``docker_image = "..."``（含单引号、裸值与行尾注释）。
_KEY_RE = re.compile(
    r"""^(?P<lead>[ \t]*)(?P<key>docker_image)(?P<mid>[ \t]*=[ \t]*)(?P<val>.*?)(?P<trail>[ \t]*(?:\#.*)?)$"""
)
_ENVIRONMENT = "environment"


def _quote(value: str) -> str:
    """TOML 基本字符串字面量（只转义反斜杠与双引号，够用且可读）。"""
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _unquote(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        inner = raw[1:-1]
        if raw[0] == '"':
            return inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner
    return raw


def read_docker_image(text: str) -> str:
    """读 ``[environment].docker_image``；缺段或缺键返回空串。"""
    in_env = False
    for line in text.splitlines():
        section = _SECTION_RE.match(line)
        if section is not None:
            in_env = section.group(1).strip() == _ENVIRONMENT
            continue
        if not in_env:
            continue
        m = _KEY_RE.match(line)
        if m is not None:
            return _unquote(m.group("val"))
    return ""


def set_docker_image(text: str, image: str) -> tuple[str, str]:
    """把 ``[environment].docker_image`` 设为 ``image``；返回 ``(新文本, 原值)``。

    三种形态都覆盖：段内已有该键则**只替换值**（保留缩进、等号周围空白与行尾注释）；
    有 ``[environment]`` 段但没有该键则在段首插入；连段都没有则在文件末尾追加一个段。

    只改**第一个** ``[environment]`` 段里的**第一个** ``docker_image``——TOML 本身不允许
    重复段/重复键，出现第二个说明文件已经非法，这里不去猜测意图。
    """
    if not image or not image.strip():
        raise SchemaError("docker_image must not be empty")
    image = image.strip()

    lines = text.splitlines(keepends=True)
    env_start = None          # [environment] 段头所在行号
    env_end = len(lines)      # 该段结束（下一个段头，或文件末尾）
    for i, line in enumerate(lines):
        section = _SECTION_RE.match(line.rstrip("\r\n"))
        if section is None:
            continue
        name = section.group(1).strip()
        if env_start is None and name == _ENVIRONMENT:
            env_start = i
        elif env_start is not None:
            env_end = i
            break

    if env_start is None:
        # 没有 [environment] 段：追加一个。保证与前文之间恰有一个空行。
        suffix = "" if not text or text.endswith("\n") else "\n"
        sep = "" if text.rstrip("\n") == "" else "\n"
        return (f"{text}{suffix}{sep}[{_ENVIRONMENT}]\n"
                f"docker_image = {_quote(image)}\n"), ""

    for i in range(env_start + 1, env_end):
        raw = lines[i]
        m = _KEY_RE.match(raw.rstrip("\r\n"))
        if m is None:
            continue
        old = _unquote(m.group("val"))
        eol = raw[len(raw.rstrip("\r\n")):]
        lines[i] = (f"{m.group('lead')}{m.group('key')}{m.group('mid')}"
                    f"{_quote(image)}{m.group('trail')}{eol}")
        return "".join(lines), old

    # 有段无键：插到段头之后，保持"新键紧跟段头"的常规排版。
    lines.insert(env_start + 1, f"docker_image = {_quote(image)}\n")
    return "".join(lines), ""
