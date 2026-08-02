"""``pysae-ai-tools pysae api spec`` — explore the Pysae OpenAPI document.

The spec is cached locally for one day per (environment, variant), so repeated
discovery is fast. Pass ``--refresh`` to force a re-fetch — do this whenever an
endpoint seems missing or the user mentions a path that does not exist, in case
the API changed since the cache was written. Use this to find the right
path/method/params, then call them with ``pysae api request``.

Examples:
    pysae-ai-tools pysae api spec --search vehicle
    pysae-ai-tools pysae api spec --path /api/v4/groups --method get
    pysae-ai-tools pysae api spec --tag Networks --env prod --refresh
"""

import json
import sys
import time
from pathlib import Path
from typing import Annotated

import httpx
import typer

from ...config import CACHE_DIR
from .common.config import get_env

app = typer.Typer()

_HTTP_METHODS = ("get", "post", "put", "patch", "delete", "options", "head")
_SPEC_PATHS = {
    "internal": "/api/docs/internal/openapi.json",
    "public": "/api/docs/public/openapi.json",
}
# How long a cached spec stays fresh.
_CACHE_TTL_SECONDS = 24 * 3600


def _err(msg: str) -> None:
    print(msg, file=sys.stderr)


def _cache_path(env_name: str, variant: str) -> Path:
    return CACHE_DIR / f"pysae-api-spec-{env_name}-{variant}.json"


def _read_cache(env_name: str, variant: str) -> dict[str, object] | None:
    path = _cache_path(env_name, variant)
    try:
        if time.time() - path.stat().st_mtime > _CACHE_TTL_SECONDS:
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _write_cache(env_name: str, variant: str, spec: dict[str, object]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        _cache_path(env_name, variant).write_text(json.dumps(spec), encoding="utf-8")
    except OSError:
        pass


def _download_spec(api_base: str, variant: str) -> dict[str, object]:
    url = api_base + _SPEC_PATHS[variant]
    with httpx.Client(timeout=30.0, follow_redirects=True) as client:
        resp = client.get(url, headers={"Accept": "application/json"})
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, dict):
        raise ValueError("unexpected OpenAPI payload (not an object)")
    return data


def load_spec(env_name: str, api_base: str, variant: str, *, refresh: bool) -> tuple[dict[str, object], bool]:
    """Return ``(spec, from_cache)``, fetching and caching on miss or ``refresh``."""
    if not refresh:
        cached = _read_cache(env_name, variant)
        if cached is not None:
            return cached, True
    spec = _download_spec(api_base, variant)
    _write_cache(env_name, variant, spec)
    return spec, False


def _as_dict(value: object) -> dict[str, object]:
    return value if isinstance(value, dict) else {}


def _tag_list(op: dict[str, object]) -> list[str]:
    tags = op.get("tags")
    return [str(t) for t in tags] if isinstance(tags, list) else []


def _resolve_ref(spec: dict[str, object], ref: str) -> object:
    node: object = spec
    for part in ref.lstrip("#/").split("/"):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return {"$ref": ref}
    return node


def _resolve(spec: dict[str, object], node: object, seen: frozenset[str], depth: int) -> object:
    """Inline local ``$ref`` pointers for readable display (cycle/depth guarded)."""
    if depth <= 0:
        return node
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str):
            if ref in seen:
                return {"$ref": ref}
            return _resolve(spec, _resolve_ref(spec, ref), seen | {ref}, depth - 1)
        return {k: _resolve(spec, v, seen, depth - 1) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve(spec, item, seen, depth - 1) for item in node]
    return node


def _operations(spec: dict[str, object]) -> list[tuple[str, str, dict[str, object]]]:
    out: list[tuple[str, str, dict[str, object]]] = []
    for path, item in _as_dict(spec.get("paths")).items():
        if not isinstance(item, dict):
            continue
        for method, op in item.items():
            if method.lower() in _HTTP_METHODS and isinstance(op, dict):
                out.append((path, method.lower(), op))
    return out


def _matches(path: str, method: str, op: dict[str, object], term: str) -> bool:
    haystack = " ".join(
        [path, method, str(op.get("summary", "")), str(op.get("operationId", "")), " ".join(_tag_list(op))]
    ).lower()
    return term.lower() in haystack


@app.command()
def main(
    env: Annotated[str, typer.Option("--env", help="Target environment.")] = "dev",
    variant: Annotated[
        str,
        typer.Option("--variant", help="Which spec to fetch: 'internal' (default, full) or 'public'."),
    ] = "internal",
    search: Annotated[
        str | None,
        typer.Option("--search", "-s", help="Filter operations by substring (path, summary, operationId, tag)."),
    ] = None,
    tag: Annotated[str | None, typer.Option("--tag", help="Filter operations by exact tag.")] = None,
    path: Annotated[
        str | None,
        typer.Option("--path", help="Show full detail for one path (params, body, responses)."),
    ] = None,
    method: Annotated[
        str | None,
        typer.Option("--method", help="Restrict --path detail to one HTTP method."),
    ] = None,
    refresh: Annotated[
        bool,
        typer.Option("--refresh", help="Bypass the 1-day cache and re-fetch the live spec."),
    ] = False,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Emit the filtered spec fragment as JSON."),
    ] = False,
) -> None:
    """List or detail Pysae API operations from the OpenAPI document."""
    if variant not in _SPEC_PATHS:
        _err(f"FAILED: --variant must be one of {', '.join(_SPEC_PATHS)}")
        raise typer.Exit(1)
    auth0 = get_env(env)

    try:
        spec, from_cache = load_spec(env, auth0.api_base, variant, refresh=refresh)
    except (httpx.HTTPError, ValueError) as e:
        _err(f"FAILED: could not fetch OpenAPI spec: {e}")
        raise typer.Exit(1) from None

    info = _as_dict(spec.get("info"))
    title = info.get("title", "Pysae API")
    version = info.get("version", "?")
    source = "cached" if from_cache else "live"

    # Detail mode: one path.
    if path is not None:
        item = _as_dict(spec.get("paths")).get(path)
        if not isinstance(item, dict):
            _err(f"FAILED: path '{path}' not found in the {variant} spec (try --refresh if the API changed)")
            raise typer.Exit(1)
        detail = {
            m: _resolve(spec, op, frozenset(), depth=6)
            for m, op in item.items()
            if m.lower() in _HTTP_METHODS and (method is None or m.lower() == method.lower())
        }
        if not detail:
            _err(f"FAILED: no matching method for '{path}'")
            raise typer.Exit(1)
        print(json.dumps({"path": path, "operations": detail}, indent=2, ensure_ascii=False))
        return

    # List mode.
    ops = _operations(spec)
    if tag:
        ops = [(p, m, op) for (p, m, op) in ops if tag in _tag_list(op)]
    if search:
        ops = [(p, m, op) for (p, m, op) in ops if _matches(p, m, op, search)]
    ops.sort(key=lambda t: (t[0], t[1]))

    if json_output:
        print(
            json.dumps(
                [
                    {
                        "method": m.upper(),
                        "path": p,
                        "summary": op.get("summary", ""),
                        "operationId": op.get("operationId", ""),
                        "tags": _tag_list(op),
                    }
                    for (p, m, op) in ops
                ],
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    suffix = " matching" if (search or tag) else ""
    _err(f"{title} {version} [{variant}, {source}] — {len(ops)} operation(s){suffix}")
    for p, m, op in ops:
        summary = str(op.get("summary", "")).strip()
        print(f"{m.upper():7} {p}" + (f"  — {summary}" if summary else ""))


if __name__ == "__main__":
    app()
