"""Render a ``ProjectConfig`` as the documented template with non-default values activated.

The output is the bundled ``.pysae-ai-tools.yaml`` template — every knob shown commented
at its default — but with the keys this config overrides **uncommented in place**. A repo's
file therefore documents every available option *and* shows exactly what it sets, instead of
carrying the active values in a separate block at the bottom.

A key whose value matches its schema default stays commented (documentation); a key that
differs is emitted uncommented with the config's value. ``k8s.environments`` and
``k8s.services`` are multi-line example blocks: when overridden they are rendered from the
real value (and the example lines dropped); otherwise the example stays commented.
"""

import re

import yaml

from ..common.project_config import ProjectConfig
from .template import get_template

# (path) of keys whose template form is a multi-line example block (a list of dicts).
_EXAMPLE_BLOCK_KEYS = {
    ("k8s", "environments"),
    ("k8s", "services"),
    ("aws", "s3", "buckets"),
    ("aws", "ecr"),
    ("aws", "elasticache"),
    ("aws", "secrets"),
    ("prefect", "workers"),
    ("prefect", "flows"),
}

_KEY_RE = re.compile(r"^(\s*)([\w-]+):(.*)$")


def _inline(value: object) -> str:
    """One-line YAML flow rendering of a scalar / list / dict value.

    ``yaml.safe_dump`` of a bare scalar appends a ``...`` document-end marker on its own
    line; drop it so the result stays a single inline token.
    """
    dumped = yaml.safe_dump(value, default_flow_style=True, allow_unicode=True, sort_keys=False, width=10**9)
    lines = dumped.strip().split("\n")
    if lines[-1] == "...":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _block(value: object, indent: int) -> list[str]:
    """Multi-line block YAML rendering, indented by ``indent`` spaces."""
    dumped = yaml.safe_dump(value, default_flow_style=False, allow_unicode=True, sort_keys=False, width=10**9)
    pad = " " * indent
    return [pad + line for line in dumped.rstrip("\n").splitlines()]


def _comment_indent(line: str) -> int | None:
    """Structural indent (spaces) of a ``# `` comment line, or ``None`` if not a comment."""
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return None
    body = stripped[1:]
    body = body[1:] if body.startswith(" ") else body
    return len(body) - len(body.lstrip(" "))


def activate_overrides(config: ProjectConfig) -> str:
    """Return the template with ``config``'s non-default values uncommented in place."""
    # exclude_defaults gives exactly the non-default fields (nested) — i.e. what to activate —
    # and naturally drops default noise (a service's None datadog_service, an env's slug: false).
    overrides = config.model_dump(mode="json", exclude_defaults=True)
    lines = get_template().splitlines()
    out: list[str] = []
    key_at_depth: dict[int, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        stripped = line.lstrip()
        if not stripped.startswith("#") or stripped == "#":
            out.append(line)  # version: 1, blank lines, bare "#"
            continue
        body = stripped[1:]
        body = body[1:] if body.startswith(" ") else body
        match = _KEY_RE.match(body)
        if not match:
            out.append(line)  # header prose / list-item example / anything non key:value
            continue
        indent = len(match.group(1))
        depth = indent // 2
        key = match.group(2)
        after = match.group(3).strip()
        is_header = after == "" or after.startswith("#")

        key_at_depth[depth] = key
        path = tuple(key_at_depth[d] for d in range(depth + 1))

        node: object = overrides
        overridden = True
        for part in path:
            if isinstance(node, dict) and part in node:
                node = node[part]
            else:
                overridden = False
                break

        if path in _EXAMPLE_BLOCK_KEYS:
            # Consume the example continuation lines (deeper-indented comments).
            block_start = i
            while i < len(lines) and (ci := _comment_indent(lines[i])) is not None and ci > indent:
                i += 1
            if overridden:
                out.append(f"{' ' * indent}{key}:")
                out.extend(_block(node, indent + 2))
            else:
                out.extend(lines[block_start - 1 : i])  # keep the example commented, verbatim
            continue

        if not overridden:
            out.append(line)
        elif is_header:
            out.append(f"{' ' * indent}{key}:")
        else:
            out.append(f"{' ' * indent}{key}: {_inline(node)}")
    return "\n".join(out) + "\n"
