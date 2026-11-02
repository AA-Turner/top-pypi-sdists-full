"""Apollo entity config blocks: read them as YAML, mask them for display, write block YAML.

An entity's `declaredState.config` is a list of strings, each a YAML document keyed by
a config-block version:

    17.0.0:
      overrides:
        roles: kube
        authToken: ...

That is how a module RENDERS an entity's config, and how the Apollo UI writes it. The
readers here used to `json.loads` the text after `overrides:`, which only understood
the JSON-in-YAML form this repo's own `update_entity_config` wrote. Every module-managed
entity therefore read as having a config version and NO overrides, and on
jacanda-orin-agx-nanocube an agent took that for an unconfigured entity and replaced
its module-rendered config by hand (2026-09-09), dropping the `cube` Teleport label for
six weeks. `yaml.safe_load` reads both forms: JSON is YAML, and PyYAML also accepts the
multi-line JSON that `json.dumps(indent=2)` wrote under a block key.

Writing goes the other way: `render_block` emits block YAML, because the Apollo UI
could not parse the JSON-in-YAML form the old writer produced.

Display always goes through `mask_secrets`, which masks by the same NAME rule as module
variables (`secret_names`). Entity config is where a cube's Teleport join token and an
app's master key live, so nothing here prints a value without it.
"""

from __future__ import annotations

import re
from typing import Any, NamedTuple

import yaml

from cube_common import secret_names


class ConfigBlock(NamedTuple):
    """One version block of an entity config string.

    ``readable`` is False when the text could not be parsed as YAML, or a block had no
    ``overrides`` mapping; ``overrides`` is then None and must not be shown as "none".
    """
    version: str
    overrides: Any
    readable: bool


# A top-level (unindented, uncommented) `<label>:` line. Read off the TEXT because
# YAML resolves an unquoted `1.10:` key to the float 1.1, which would misreport the
# version Apollo matches against a release.
_TOP_LEVEL_LABEL_RE = re.compile(r"^([^\s#'\"][^:]*):", re.M)

# What a version label may contain when we WRITE one. The label is interpolated into
# the YAML text unquoted (as module renders and the Apollo UI write it), so a newline
# or a colon would let a caller-supplied version inject keys into the block.
_VERSION_RE = re.compile(r"^[0-9A-Za-z][0-9A-Za-z.+_-]*$")


def parse_config(text: str) -> list[ConfigBlock]:
    """Every version block in one `declaredState.config` string, in order."""
    if not isinstance(text, str) or not text.strip():
        return []
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError:
        doc = None
    if not isinstance(doc, dict) or not doc:
        # Unparseable: report the version the way the old reader did (text before the
        # first colon) so the line does not vanish, and say nothing about overrides.
        version = text.split(":", 1)[0].strip() if ":" in text else ""
        return [ConfigBlock(version, None, False)] if version else []

    labels = [m.group(1).strip() for m in _TOP_LEVEL_LABEL_RE.finditer(text)]
    if len(labels) != len(doc):
        labels = [str(k) for k in doc]
    blocks = []
    for label, body in zip(labels, doc.values()):
        if isinstance(body, dict) and "overrides" in body:
            overrides = body["overrides"]
            # `overrides:` with nothing after it loads as None: an empty block.
            blocks.append(ConfigBlock(label, {} if overrides is None else overrides, True))
        else:
            blocks.append(ConfigBlock(label, None, False))
    return blocks


def mask_secrets(value: Any, name: object = None) -> Any:
    """A copy of ``value`` with every secret-named entry replaced by its mask.

    Recurses through mappings and lists. A secret-named key masks its WHOLE value,
    subtree included. Two further rules: a userinfo URL is masked whatever its key
    (`secret_names.value_is_sensitive`), and a Kubernetes env entry
    (`{name: DB_PASSWORD, value: ...}`) masks its `value` by the entry's `name`,
    since the key `value` says nothing.
    """
    if name is not None and secret_names.is_secret_name(str(name)):
        return secret_names.mask(value)
    if isinstance(value, dict):
        entry_name = value.get("name")
        secret_entry = isinstance(entry_name, str) and secret_names.is_secret_name(entry_name)
        return {
            k: (secret_names.mask(v) if (secret_entry and k == "value") else mask_secrets(v, k))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [mask_secrets(v) for v in value]
    if secret_names.value_is_sensitive(value):
        return secret_names.mask(value)
    return value


def display_lines(overrides: Any) -> list[str]:
    """``overrides`` as block YAML lines, secrets masked. Never call without masking."""
    text = yaml.safe_dump(
        mask_secrets(overrides), sort_keys=False, default_flow_style=False,
        allow_unicode=True, width=1000,
    )
    return text.rstrip("\n").split("\n")


def masked_paths(value: Any, path: str = "") -> list[str]:
    """Where in ``value`` a mask placeholder sits, as dotted paths.

    `update_entity_config` is a full replace, and `entity_health` shows a secret as
    `<hidden, N chars>`. An agent that copies the shown overrides back would store
    that literal as the Teleport join token, so the write paths refuse it.
    """
    if isinstance(value, dict):
        return [p for k, v in value.items() for p in masked_paths(v, f"{path}.{k}" if path else str(k))]
    if isinstance(value, list):
        return [p for i, v in enumerate(value) for p in masked_paths(v, f"{path}[{i}]")]
    return [path or "(root)"] if secret_names.is_masked_placeholder(value) else []


def valid_version(version: str) -> bool:
    return bool(_VERSION_RE.match(version or ""))


def render_block(version: str, overrides: Any) -> str:
    """One config block as block YAML, the form modules render and the Apollo UI reads.

    The caller checks ``valid_version`` first; the label is written unquoted.
    """
    body = yaml.safe_dump(
        {"overrides": overrides}, sort_keys=False, default_flow_style=False,
        allow_unicode=True, width=1000,
    )
    indented = "\n".join(f"  {line}" for line in body.rstrip("\n").split("\n"))
    return f"{version}:\n{indented}"
