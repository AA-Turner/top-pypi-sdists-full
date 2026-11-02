"""Read and merge the gateway's Apollo config override (docs/ai-reactor-deploy-spec.md §6).

Pure functions, no I/O. The rules they enforce are the safety case for editing a
gateway the console did not install:

1. Only `localModels` entries carrying the Edgeport marker are ever added, changed or
   removed. Every other key, and every unmarked entry, passes through unchanged.
2. The override block keeps the version it was read with: it can differ from the
   chart's version (staging runs block 0.3.3 on chart 0.3.4).
3. The block is read and written the way `cube_common.entity_config` reads and writes
   every other entity config: either form in (block YAML, as modules, the Apollo UI and
   `update_entity_config` write it, or the JSON-in-YAML an older writer left), block
   YAML out. Reading only JSON locked the console out of a gateway someone had edited
   through those, and writing JSON-in-YAML left a config the Apollo UI cannot parse.
4. Anything that is not exactly one readable block is refused rather than rewritten,
   and so is a block a rewrite would change in passing: one carrying a comment (dropped)
   or an unquoted value YAML retypes (`tag: 1.10` reads as the float 1.1 and would be
   written back as `1.10`'s float, `1.1`). A second block makes "which one applies" a
   guess.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

import yaml
from yaml.representer import SafeRepresenter

from cube_cloud.reactor.catalog import ModelSpec
from cube_common import entity_config

# The key and value that mark a `localModels` entry (and a gateway) as Edgeport's.
# The chart template reads only name/hostedModel/apiBase from an entry and nothing
# at the top level under this key, so the marker renders nothing.
MARKER_KEY = "managedBy"
MARKER_VALUE = "edgeport"

# A YAML comment: `#` at the start of a line or after whitespace. A `#` inside a quoted
# value can match too, which refuses a block the console could have rewritten; that is
# the safe direction.
_COMMENT_RE = re.compile(r"(^|\s)#", re.M)


_STR_TAG = "tag:yaml.org,2002:str"


def _rewrite_changes_a_value(text: str) -> bool:
    """Whether writing the parsed block back would change how a value is written.

    A plain (unquoted) scalar that YAML resolves to a non-string is safe only when its
    canonical form is the text as written: `true`, `8000` and `0.95` are; `1.10`, `no`,
    `~` and `1:30` are not. Version labels are read and written as text, so only what
    sits under them is checked.
    """
    representer = SafeRepresenter()

    def changed(node) -> bool:
        if isinstance(node, yaml.ScalarNode):
            if node.style is not None or node.tag == _STR_TAG:
                return False
            return representer.represent_data(yaml.safe_load(node.value)).value != node.value
        if isinstance(node, yaml.MappingNode):
            return any(changed(k) or changed(v) for k, v in node.value)
        if isinstance(node, yaml.SequenceNode):
            return any(changed(item) for item in node.value)
        return False

    root = yaml.compose(text, Loader=yaml.SafeLoader)
    return isinstance(root, yaml.MappingNode) and any(changed(v) for _, v in root.value)


class OverrideUnreadable(ValueError):
    """The declared config is not something the console will rewrite.

    `reason` is a stable code the console maps to its own wording; the message never
    carries config content (it can hold credentials on a gateway without apolloSecrets).
    """

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class ConfigBlock:
    version: str
    overrides: dict


def parse_declared_config(config: list | None, default_version: str) -> ConfigBlock:
    """The single override block of a gateway's `declaredState.config`.

    No block at all is an empty override at `default_version` (a gateway installed
    with none). Raises OverrideUnreadable for more than one block, a block carrying a
    comment or a value a rewrite would retype, or one that is not a version label over
    an `overrides` mapping.
    """
    texts = [c for c in (config or []) if isinstance(c, str) and c.strip()]
    if not texts:
        return ConfigBlock(version=default_version, overrides={})
    if len(texts) > 1:
        raise OverrideUnreadable("multiple_blocks")
    if _COMMENT_RE.search(texts[0]):
        raise OverrideUnreadable("has_comments")
    blocks = entity_config.parse_config(texts[0])
    if len(blocks) > 1:
        raise OverrideUnreadable("multiple_blocks")
    if not blocks:
        raise OverrideUnreadable("unreadable")
    block = blocks[0]
    # The version is written back unquoted, so it must be one `render_block` accepts.
    if not block.readable or not isinstance(block.overrides, dict) \
            or not entity_config.valid_version(block.version):
        raise OverrideUnreadable("unreadable")
    if _rewrite_changes_a_value(texts[0]):
        raise OverrideUnreadable("ambiguous_values")
    return ConfigBlock(version=block.version, overrides=block.overrides)


def render_config_block(block: ConfigBlock) -> str:
    """The config string to write: block YAML, the form modules and the Apollo UI use."""
    return entity_config.render_block(block.version, block.overrides)


def is_marked(entry: object) -> bool:
    return isinstance(entry, dict) and entry.get(MARKER_KEY) == MARKER_VALUE


def gateway_is_marked(overrides: dict) -> bool:
    """Whether the console installed this gateway (it stamps the marker at the top)."""
    return overrides.get(MARKER_KEY) == MARKER_VALUE


def local_models(overrides: dict) -> list:
    value = overrides.get("localModels")
    return value if isinstance(value, list) else []


def marked_names(overrides: dict) -> list[str]:
    """Aliases of the Edgeport-marked `localModels` entries, in order."""
    return [e.get("name") for e in local_models(overrides) if is_marked(e) and isinstance(e.get("name"), str)]


def marked_entry(model: ModelSpec, namespace: str) -> dict:
    """The `localModels` entry the console writes for a catalog model."""
    return {
        "name": model.id,
        "hostedModel": model.hosted_model,
        "apiBase": model.api_base(namespace),
        MARKER_KEY: MARKER_VALUE,
    }


def with_models(
    overrides: dict, add: list[dict] | None = None, remove: list[str] | None = None,
) -> dict:
    """A copy of `overrides` with marked entries added or removed. Nothing else changes.

    `add` entries must be marked; an existing MARKED entry of the same name is
    replaced in place. An UNMARKED entry of the same name is left alone and raises
    OverrideUnreadable("name_taken"): the console never takes over someone else's
    alias. `remove` names only marked entries; an unmarked entry of that name stays.
    """
    add = add or []
    remove = set(remove or [])
    if any(not is_marked(e) for e in add):
        raise ValueError("with_models only adds marked entries")
    current = list(local_models(overrides))
    for entry in add:
        if any(not is_marked(e) and isinstance(e, dict) and e.get("name") == entry["name"] for e in current):
            raise OverrideUnreadable("name_taken")
    result: list = []
    added: set[str] = set()
    seen_marked: set[str] = set()
    for e in current:
        if is_marked(e) and e.get("name") in remove:
            continue
        if is_marked(e):
            # One marked entry per alias. Two pending writes merged by Apollo once left
            # the same alias twice (cube-m9u9i4lc, 2026-10-07); the next write heals it.
            if e.get("name") in seen_marked:
                continue
            seen_marked.add(e.get("name"))
        replacement = next((a for a in add if is_marked(e) and a["name"] == e.get("name")), None)
        if replacement is not None:
            result.append(dict(replacement))
            added.add(replacement["name"])
        else:
            result.append(e)
    for entry in add:
        if entry["name"] not in added:
            result.append(dict(entry))
    merged = dict(overrides)
    merged["localModels"] = result
    return merged
