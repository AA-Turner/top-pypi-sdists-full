"""python-dotenv's load_dotenv, without python-dotenv. Stdlib only.

Parses a ``.env`` file (KEY=VALUE lines) into ``os.environ``. Mirrors the
common python-dotenv behaviour:
  * ``#`` comments and blank lines are ignored
  * an optional ``export`` prefix is stripped
  * single-quoted values are literal; double-quoted values process ``\\n`` /
    ``\\t`` / ``\\r`` / ``\\"`` / ``\\\\`` escapes and allow ``${VAR}`` expansion
  * unquoted values allow ``${VAR}`` expansion and a trailing `` # comment``
  * quoted values may span multiple lines
  * existing ``os.environ`` keys are NOT overwritten unless ``override=True``
"""
from __future__ import annotations

import os
import re

__all__ = ["load_dotenv", "dotenv_values", "parse_dotenv"]

# ${VAR}, ${VAR:-default}, or $VAR
_VAR_RE = re.compile(r"\$\{([^}:]+)(?::-([^}]*))?\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def _interpolate(value: str, values: dict) -> str:
    def repl(m):
        name = m.group(1) or m.group(3)
        default = m.group(2) or ""
        if name in values:
            return values[name]
        return os.environ.get(name, default)
    return _VAR_RE.sub(repl, value)


def _process_double_quoted(inner: str) -> str:
    out, i = [], 0
    while i < len(inner):
        c = inner[i]
        if c == "\\" and i + 1 < len(inner):
            nxt = inner[i + 1]
            out.append({"n": "\n", "t": "\t", "r": "\r",
                        '"': '"', "\\": "\\"}.get(nxt, "\\" + nxt))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def parse_dotenv(text: str, interpolate: bool = True) -> dict:
    """Parse .env *text* into an ordered dict of ``{key: value}``."""
    values: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export ") or line.startswith("export\t"):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if not key:
            continue
        val = val.lstrip()

        if val[:1] in ("'", '"'):
            quote = val[0]
            body = val[1:]
            # gather until the closing quote (may span multiple lines)
            while True:
                end = body.find(quote)
                # a doubled backslash-escaped quote in double strings shouldn't close
                if end != -1 and not (quote == '"' and end > 0 and body[end - 1] == "\\"):
                    inner = body[:end]
                    break
                if i >= len(lines):
                    inner = body
                    break
                body += "\n" + lines[i]
                i += 1
            if quote == '"':
                inner = _process_double_quoted(inner)
                if interpolate:
                    inner = _interpolate(inner, values)
            value = inner
        else:
            # unquoted: strip trailing inline comment, then interpolate
            hash_idx = val.find(" #")
            if hash_idx != -1:
                val = val[:hash_idx]
            value = val.strip()
            if interpolate:
                value = _interpolate(value, values)

        values[key] = value
    return values


def dotenv_values(dotenv_path=None, encoding: str = "utf-8", interpolate: bool = True) -> dict:
    """Return ``{key: value}`` parsed from *dotenv_path* without touching os.environ."""
    if not dotenv_path or not os.path.isfile(dotenv_path):
        return {}
    with open(dotenv_path, "r", encoding=encoding) as fh:
        return parse_dotenv(fh.read(), interpolate=interpolate)


def load_dotenv(dotenv_path=None, override: bool = False,
                encoding: str = "utf-8", interpolate: bool = True, **_ignored) -> bool:
    """Load *dotenv_path* into ``os.environ``.

    Returns True if a file was found and read, else False. Existing environment
    variables are preserved unless ``override=True``.
    """
    if not dotenv_path or not os.path.isfile(dotenv_path):
        return False
    for key, value in dotenv_values(dotenv_path, encoding=encoding,
                                    interpolate=interpolate).items():
        if override or key not in os.environ:
            os.environ[key] = value
    return True
