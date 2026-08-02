"""``figma fetch-node`` — compact, deterministic design context for one node.

Why this exists rather than the Figma MCP server: that server requires an
interactive OAuth flow and rejects personal access tokens, so it cannot run in
CI. REST plus a token is the only headless path.

Why the output is compact: the raw ``/v1/files/:key/nodes`` response measured
1.7 MB for a single component at depth 3. Feeding that to an agent is not an
option, so this command keeps only what identifies the node and describes its
resolved styling.

Known limitation, measured and not worked around: the REST API exposes bound
variables as opaque ``VariableID:…`` references and never their names. Resolving
a name requires ``/v1/files/:key/variables/local``, which is Enterprise-only.
The identifiers are surfaced as-is so a caller holding an exported variable
table can do the mapping.
"""

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer

from ..env import secret_store

SECRET_ID = "pysae/figma/tooling"
API_BASE = "https://api.figma.com"
_TIMEOUT = 30.0


class FigmaError(RuntimeError):
    """A Figma API call failed, or the token is missing."""


@dataclass
class Style:
    """Resolved styling of the node itself, not of its subtree."""

    size: dict[str, float] = field(default_factory=dict)
    fills: list[str] = field(default_factory=list)
    strokes: list[str] = field(default_factory=list)
    corner_radius: object | None = None
    padding: dict[str, float] = field(default_factory=dict)
    item_spacing: float | None = None
    layout_mode: str | None = None
    effects: list[str] = field(default_factory=list)


@dataclass
class Subtree:
    """Distinct values observed anywhere below the node.

    A container component carries no styling of its own: measured on the real
    ``button-group``, every fill, radius and bound variable lives on a
    descendant, and reading the root alone returns an empty context. Aggregating
    the subtree is what makes the result usable by an agent.
    """

    nodes: int = 0
    fills: list[str] = field(default_factory=list)
    corner_radii: list[object] = field(default_factory=list)
    item_spacings: list[float] = field(default_factory=list)
    bound_variables: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class NodeContext:
    """What an agent needs to act on a commented node, and nothing more."""

    file_key: str
    node_id: str
    name: str
    type: str
    variants: list[str] = field(default_factory=list)
    component_properties: dict[str, object] = field(default_factory=dict)
    style: Style = field(default_factory=Style)
    bound_variables: dict[str, list[str]] = field(default_factory=dict)
    subtree: Subtree = field(default_factory=Subtree)
    children: list[str] = field(default_factory=list)
    image: str | None = None
    raw_bytes: int = 0


def token() -> str:
    """Prefer the CI-injected variable, fall back to AWS Secrets Manager."""
    from_env = os.environ.get("FIGMA_TOKEN")
    if from_env:
        return from_env
    try:
        return secret_store.get_key(SECRET_ID, "pat")
    except secret_store.SecretError as exc:
        raise FigmaError(f"no Figma token: set FIGMA_TOKEN or grant access to {SECRET_ID} ({exc})") from None


def _get(path: str, tok: str, params: dict[str, str] | None = None) -> httpx.Response:
    response = httpx.get(
        f"{API_BASE}{path}",
        headers={"X-Figma-Token": tok},
        params=params,
        timeout=_TIMEOUT,
        follow_redirects=True,
    )
    if response.status_code >= 400:
        raise FigmaError(f"{path} returned {response.status_code}: {response.text[:200]}")
    return response


def _hex(color: dict[str, float]) -> str:
    red, green, blue = (round(float(color.get(channel, 0)) * 255) for channel in ("r", "g", "b"))
    alpha = float(color.get("a", 1))
    base = f"#{red:02x}{green:02x}{blue:02x}"
    return base if alpha >= 1 else f"{base}{round(alpha * 255):02x}"


def _paints(paints: object) -> list[str]:
    described: list[str] = []
    if not isinstance(paints, list):
        return described
    for paint in paints:
        if not isinstance(paint, dict):
            continue
        if paint.get("visible") is False:
            continue
        color = paint.get("color")
        if isinstance(color, dict):
            described.append(_hex(color))
        else:
            described.append(str(paint.get("type", "unknown")))
    return described


# The API spells corner radius two ways: a single value, or one per corner when
# they differ. Both are kept verbatim so a caller can tell them apart.
def _corner_radius(document: dict[str, Any]) -> object | None:
    radii: object | None = document.get("rectangleCornerRadii")
    if radii is not None:
        return radii
    single: object | None = document.get("cornerRadius")
    return single


def _padding(document: dict[str, Any]) -> dict[str, float]:
    keys = ("paddingLeft", "paddingRight", "paddingTop", "paddingBottom")
    return {key: float(document[key]) for key in keys if isinstance(document.get(key), (int, float))}


def _size(document: dict[str, Any]) -> dict[str, float]:
    box = document.get("absoluteBoundingBox")
    if not isinstance(box, dict):
        return {}
    return {key: float(box[key]) for key in ("width", "height") if isinstance(box.get(key), (int, float))}


def _bound_variables(document: dict[str, Any]) -> dict[str, list[str]]:
    bound = document.get("boundVariables")
    if not isinstance(bound, dict):
        return {}

    collected: dict[str, list[str]] = {}
    for prop, value in bound.items():
        ids = sorted(set(_variable_ids(value)))
        if ids:
            collected[prop] = ids
    return collected


def _variable_ids(value: object) -> list[str]:
    if isinstance(value, dict):
        identifier = value.get("id")
        if isinstance(identifier, str) and identifier.startswith("VariableID:"):
            return [identifier]
        return [found for nested in value.values() for found in _variable_ids(nested)]
    if isinstance(value, list):
        return [found for nested in value for found in _variable_ids(nested)]
    return []


def summarise_subtree(document: dict[str, Any]) -> Subtree:
    """Collect distinct styling values from the node and all its descendants."""
    aggregate = Subtree()
    fills: list[str] = []
    radii: list[object] = []
    spacings: list[float] = []
    variables: dict[str, list[str]] = {}

    def visit(node: dict[str, Any]) -> None:
        aggregate.nodes += 1
        fills.extend(_paints(node.get("fills")))

        radius = _corner_radius(node)
        if radius is not None and radius not in radii:
            radii.append(radius)

        spacing = node.get("itemSpacing")
        if isinstance(spacing, (int, float)):
            spacings.append(float(spacing))

        for prop, ids in _bound_variables(node).items():
            variables.setdefault(prop, []).extend(ids)

        for child in node.get("children", []):
            if isinstance(child, dict):
                visit(child)

    visit(document)

    aggregate.fills = sorted(set(fills))
    aggregate.corner_radii = radii
    aggregate.item_spacings = sorted(set(spacings))
    aggregate.bound_variables = {prop: sorted(set(ids)) for prop, ids in sorted(variables.items())}
    return aggregate


def compact(payload: dict[str, Any], file_key: str, node_id: str, raw_bytes: int) -> NodeContext:
    """Reduce a /nodes response to the fields an agent can act on."""
    node = payload.get("nodes", {}).get(node_id)
    if not isinstance(node, dict):
        raise LookupError(f"node {node_id} not found in file {file_key}")

    document = node.get("document")
    if not isinstance(document, dict):
        raise LookupError(f"node {node_id} has no document")

    children = [child.get("name", "") for child in document.get("children", []) if isinstance(child, dict)]
    variants = [
        child.get("name", "")
        for child in document.get("children", [])
        if isinstance(child, dict) and child.get("type") == "COMPONENT"
    ]

    return NodeContext(
        file_key=file_key,
        node_id=node_id,
        name=str(document.get("name", "")),
        type=str(document.get("type", "")),
        variants=variants,
        component_properties=document.get("componentPropertyDefinitions", {}) or {},
        style=Style(
            size=_size(document),
            fills=_paints(document.get("fills")),
            strokes=_paints(document.get("strokes")),
            corner_radius=_corner_radius(document),
            padding=_padding(document),
            item_spacing=(
                float(document["itemSpacing"]) if isinstance(document.get("itemSpacing"), (int, float)) else None
            ),
            layout_mode=document.get("layoutMode"),
            effects=[str(effect.get("type", "")) for effect in document.get("effects", []) if isinstance(effect, dict)],
        ),
        bound_variables=_bound_variables(document),
        subtree=summarise_subtree(document),
        children=children,
        raw_bytes=raw_bytes,
    )


def image_url(file_key: str, node_id: str, tok: str, scale: int) -> str | None:
    payload = _get(
        f"/v1/images/{file_key}",
        tok,
        params={"ids": node_id, "format": "png", "scale": str(scale)},
    ).json()
    url = payload.get("images", {}).get(node_id)
    return url if isinstance(url, str) else None


def _download(url: str, target: Path) -> None:
    response = httpx.get(url, timeout=_TIMEOUT, follow_redirects=True)
    if response.status_code >= 400:
        raise FigmaError(f"image download returned {response.status_code}")
    target.write_bytes(response.content)


def _summary(context: NodeContext) -> str:
    lines = [
        f"{context.name} ({context.type}) {context.node_id}",
        f"  size          {context.style.size or '-'}",
        f"  fills         {', '.join(context.style.fills) or '-'}",
        f"  corner radius {context.style.corner_radius if context.style.corner_radius is not None else '-'}",
        f"  padding       {context.style.padding or '-'}",
        f"  item spacing  {context.style.item_spacing if context.style.item_spacing is not None else '-'}",
        f"  variants      {len(context.variants)}",
        f"  children      {len(context.children)}",
        f"  variables     {sum(len(ids) for ids in context.bound_variables.values())} bound on the node (opaque ids)",
        f"  subtree       {context.subtree.nodes} nodes, "
        f"{len(context.subtree.fills)} distinct fills, "
        f"{sum(len(ids) for ids in context.subtree.bound_variables.values())} bound variables",
        f"  raw payload   {context.raw_bytes} bytes",
    ]
    if context.image:
        lines.append(f"  image         {context.image}")
    return "\n".join(lines)


def main(
    file_key: Annotated[str, typer.Option("--file-key", help="Figma file key, from the /design/<key>/ URL.")],
    node_id: Annotated[str, typer.Option("--node-id", help="Node id, e.g. 2126:8833 or 2126-8833.")],
    depth: Annotated[int, typer.Option("--depth", help="How deep to walk the node subtree.")] = 2,
    scale: Annotated[int, typer.Option("--scale", help="PNG render scale.")] = 2,
    out: Annotated[
        Path | None,
        typer.Option("--out", help="Write <node>.json and <node>.png into this directory."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Print the compact JSON instead of a summary.")] = False,
) -> None:
    """Fetch one Figma node as compact JSON, plus its PNG render."""
    normalised = node_id.replace("-", ":")

    try:
        tok = token()
        response = _get(
            f"/v1/files/{file_key}/nodes",
            tok,
            params={"ids": normalised, "depth": str(depth)},
        )
        context = compact(response.json(), file_key, normalised, len(response.content))
    except LookupError as exc:
        typer.echo(f"NOT FOUND: {exc}", err=True)
        raise typer.Exit(2) from None
    except (FigmaError, httpx.HTTPError) as exc:
        typer.echo(f"FAILED: {exc}", err=True)
        raise typer.Exit(1) from None

    if out is not None:
        out.mkdir(parents=True, exist_ok=True)
        stem = normalised.replace(":", "-")
        try:
            url = image_url(file_key, normalised, tok, scale)
            if url:
                target = out / f"{stem}.png"
                _download(url, target)
                context.image = str(target)
        except (FigmaError, httpx.HTTPError) as exc:
            typer.echo(f"WARNING: image not retrieved: {exc}", err=True)
        (out / f"{stem}.json").write_text(json.dumps(asdict(context), indent=2, ensure_ascii=False))

    typer.echo(json.dumps(asdict(context), indent=2, ensure_ascii=False) if as_json else _summary(context))
