"""Give the inline schemas in fern/openapi.json the names in fern/schemas.yaml.

Each named schema becomes components/schemas/<Name>, and every structurally
identical schema elsewhere (ignoring descriptions and examples) becomes a $ref
to it. Locations that no longer resolve are skipped with a warning, so a spec
change never blocks generation; it only falls back to Fern's default names.

    python3 scripts/name_schemas.py fern/openapi.json fern/openapi.sdk.json
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
NAMES = ROOT / "fern" / "schemas.yaml"
IGNORED_KEYS = {"description", "example", "examples", "title"}
# Request bodies stay inline: Fern turns their fields into keyword arguments.
REQUEST_BODY = re.compile(r"^/paths/[^/]+/[a-z]+/requestBody/content/[^/]+/schema$")

Json = Any


def warn(message: str) -> None:
    prefix = "::warning::" if "GITHUB_ACTIONS" in os.environ else "warning: "
    print(f"{prefix}schemas.yaml: {message}", file=sys.stderr)


def load_names() -> list[tuple[str, str]]:
    names = []
    for line in NAMES.read_text().splitlines():
        line = line.split(" #", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        name, _, location = line.partition(":")
        names.append((name.strip(), location.strip().strip('"')))
    return names


def escape(key: str) -> str:
    return key.replace("~", "~0").replace("/", "~1")


def get(spec: Json, pointer: str) -> Json:
    node = spec
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def resolve(spec: Json, location: str) -> str:
    """Turn a schemas.yaml location into a JSON pointer, checking it exists."""
    if location.startswith("#"):
        pointer = location[1:]
        get(spec, pointer)
        return pointer
    method, path, rest = location.split(" ", 2)
    match = re.match(r"(param:\w+|body|\d{3})(.*)", rest)
    if not match:
        raise KeyError(rest)
    where, selector = match.groups()
    op = f"/paths/{escape(path)}/{method.lower()}"
    get(spec, op)
    if where == "body":
        content = get(spec, f"{op}/requestBody/content")
        pointer = f"{op}/requestBody/content/{escape(next(iter(content)))}/schema"
    elif where.startswith("param:"):
        params = get(spec, f"{op}/parameters")
        index = next(i for i, p in enumerate(params) if p["name"] == where[6:])
        pointer = f"{op}/parameters/{index}/schema"
    else:
        pointer = f"{op}/responses/{where}/content/application~1json/schema"
    for token in re.findall(r"\.\w+|\[\]|\?|\{\}|\(\w+=[\w-]+\)", selector):
        node = get(spec, pointer)
        if token.startswith("("):
            field, value = token[1:-1].split("=")
            key = "oneOf" if "oneOf" in node else "anyOf"
            index = next(i for i, b in enumerate(node[key]) if _literal(b, field) == value)
            pointer += f"/{key}/{index}"
        elif token == "[]":
            pointer += "/items"
        elif token == "{}":
            pointer += "/additionalProperties"
        elif token == "?":
            key = "anyOf" if "anyOf" in node else "oneOf"
            index = next(i for i, b in enumerate(node[key]) if b.get("type") != "null")
            pointer += f"/{key}/{index}"
        else:
            pointer += f"/properties/{token[1:]}"
    get(spec, pointer)
    return pointer


def _literal(schema: Json, field: str) -> Json:
    prop = schema.get("properties", {}).get(field, {})
    return prop.get("const", (prop.get("enum") or [None])[0])


def canonical(node: Json) -> str:
    def strip(value: Json) -> Json:
        if isinstance(value, dict):
            return {k: strip(v) for k, v in value.items() if k not in IGNORED_KEYS}
        if isinstance(value, list):
            return [strip(v) for v in value]
        return value

    return json.dumps(strip(node), sort_keys=True)


def replace_all(spec: Json, key: str, ref: str, skip: str, source: str) -> int:
    """Replace every schema whose canonical form is `key` with a $ref."""
    count = 0

    def visit(node: Json, pointer: str) -> Json:
        nonlocal count
        if isinstance(node, dict):
            inline_body = REQUEST_BODY.match(pointer) and pointer != source
            if pointer != skip and not inline_body and canonical(node) == key:
                count += 1
                replacement: dict[str, Json] = {"$ref": ref}
                if "description" in node:
                    replacement["description"] = node["description"]
                return replacement
            return {k: visit(v, f"{pointer}/{escape(k)}") for k, v in node.items()}
        if isinstance(node, list):
            return [visit(v, f"{pointer}/{i}") for i, v in enumerate(node)]
        return node

    for top in ("paths", "components"):
        spec[top] = visit(spec[top], f"/{top}")
    return count


def main(source: str, target: str) -> None:
    spec = json.loads(Path(source).read_text())
    existing = set(spec.setdefault("components", {}).setdefault("schemas", {}))
    resolved: list[tuple[str, str]] = []
    for name, location in load_names():
        if name in existing:
            warn(f"{name} already exists in the spec; skipped")
            continue
        try:
            resolved.append((name, resolve(spec, location)))
        except (KeyError, IndexError, StopIteration, ValueError):
            warn(f"{name}: {location} not found; skipped")
    # Innermost first, so outer schemas compare equal after their parts are named.
    resolved.sort(key=lambda item: -item[1].count("/"))
    names_by_pointer = dict((pointer, name) for name, pointer in resolved)
    for pointer, name in names_by_pointer.items():
        try:
            node = get(spec, pointer)
        except (KeyError, IndexError):
            warn(f"{name}: moved by an earlier name; skipped")
            continue
        if "$ref" in node:
            warn(f"{name}: already named {node['$ref'].rsplit('/', 1)[-1]}; skipped")
            continue
        spec["components"]["schemas"][name] = node  # replace_all rebuilds "components"
        replace_all(
            spec,
            canonical(node),
            f"#/components/schemas/{name}",
            skip=f"/components/schemas/{escape(name)}",
            source=pointer,
        )
    Path(target).write_text(json.dumps(spec, indent=2) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
