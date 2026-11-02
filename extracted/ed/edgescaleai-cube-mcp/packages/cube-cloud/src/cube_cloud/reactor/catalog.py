"""The AI Reactor catalog: which gateway and which models the console may deploy.

Loaded from `catalog.yaml` beside this file and validated strictly, so a malformed
entry fails at import (and in CI) rather than at a user's click. A model absent from
the catalog cannot be deployed from the console: the catalog is the enumerated-args
boundary for the deploy routes (AGENTS.md console rule 2).
"""

from __future__ import annotations

import copy
import functools
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from cube_common import secret_names

CATALOG_PATH = Path(__file__).with_name("catalog.yaml")

# A catalog id is also the gateway alias clients call, a URL-safe slug.
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9.-]{0,62}$")
# A Kubernetes Service name (RFC 1035 label) and namespace.
_DNS_LABEL_RE = re.compile(r"^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$")
_PRODUCT_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+:[A-Za-z0-9_.-]+$")
_VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
TASKS = frozenset({"chat", "embedding", "audio_transcription"})
PLATFORMS = frozenset({"x86", "jetson", "dgx-spark"})


class CatalogError(ValueError):
    """The catalog file does not describe a valid catalog."""


# Install overrides (docs/ai-reactor-deploy-spec.md §3) adjust a chart's defaults so
# it installs on any cube, the way an FDE's hand-written override did. Two kinds of
# key are refused:
#  * the gateway's wiring. The gateway reaches a model by its Service name, port and
#    served name, which the catalog states and the check script verifies against the
#    chart WITH these overrides applied; an override moving the Service or port would
#    wire the gateway to nothing. (`model.name` is allowed, and is how a model swaps in
#    a different checkpoint; the check script then holds served_model to it.)
#  * `createNamespace`. The release would own the namespace the gateway lives in, so
#    removing the model would delete the gateway with it.
_FORBIDDEN_OVERRIDES = frozenset({
    ("model", "releaseName"), ("model", "port"), ("model", "servedName"),
    ("model", "servedModelName"), ("service", "port"), ("deployment", "port"),
    ("createNamespace",),
})
# The catalog is checked in and its overrides are written to Apollo config, so it
# never carries a credential. A key NAMED like one is refused outright, by the repo's one
# secret-name rule (`cube_common/secret_names.py`), which also catches camelCase names
# such as `masterKey`, `existingSecret` and `hfToken` that a narrower pattern missed.


def merge_overrides(base: dict, top: dict) -> dict:
    """`top` deep-merged over `base`; neither is modified."""
    out = copy.deepcopy(base)
    for key, value in top.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge_overrides(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _check_overrides(raw: object, where: str, path: tuple[str, ...] = ()) -> dict:
    if not isinstance(raw, dict):
        raise CatalogError(f"{where}: overrides must be a mapping")
    for key, value in raw.items():
        here = (*path, str(key))
        if here in _FORBIDDEN_OVERRIDES:
            raise CatalogError(f"{where}: an override may not set {'.'.join(here)}")
        if secret_names.is_secret_name(str(key)):
            raise CatalogError(f"{where}: an override may not carry a credential ({'.'.join(here)})")
        if isinstance(value, dict):
            _check_overrides(value, where, here)
    return raw


@dataclass(frozen=True)
class GatewaySpec:
    product_id: str
    entity_name: str
    namespace: str
    service: str
    port: int
    config_block_version: str
    release_channel: str | None
    base_overrides: dict


@dataclass(frozen=True)
class ModelSpec:
    id: str
    display_name: str
    description: str
    task: str
    platform: str
    gpu_count: int
    min_vram_gb: int
    product_id: str
    entity_name: str
    config_block_version: str
    service: str
    port: int
    served_model: str
    storage_gb: int
    # The catalog-wide model overrides with this model's own merged over them: what
    # the console installs the model entity with. Never compared or hashed.
    install_overrides: dict = field(default_factory=dict, compare=False, hash=False)

    @property
    def hosted_model(self) -> str:
        """The LiteLLM `model` string for this backend."""
        return f"hosted_vllm/{self.served_model}"

    def api_base(self, namespace: str) -> str:
        """The in-cluster URL the gateway calls for this model."""
        return f"http://{self.service}.{namespace}.svc.cluster.local:{self.port}/v1"


@dataclass(frozen=True)
class ShownModel:
    """A model the AI tab SHOWS when it is installed, and never deploys.

    The Reactor serves more than the deployable catalog (the decision models reach it
    through pass-through routes), and a cube page that left them out would understate
    what is running. Carries only what the page displays; no service, port or served
    name, because the console never wires one. Same attribute names as ModelSpec for
    the fields the serializer reads.
    """
    id: str
    display_name: str
    description: str
    task: str
    platform: str
    gpu_count: int
    min_vram_gb: int
    product_id: str
    entity_name: str
    storage_gb: int = 0


@dataclass(frozen=True)
class Catalog:
    version: int
    gateway: GatewaySpec
    models: tuple[ModelSpec, ...]
    shown: tuple[ShownModel, ...] = ()

    def model(self, model_id: str) -> ModelSpec | None:
        return next((m for m in self.models if m.id == model_id), None)

    def model_for_product(self, product_id: str) -> ModelSpec | None:
        return next((m for m in self.models if m.product_id == product_id), None)


def _require(raw: dict, key: str, kind: type, where: str):
    value = raw.get(key)
    if not isinstance(value, kind) or isinstance(value, bool) and kind is not bool:
        raise CatalogError(f"{where}: '{key}' must be a {kind.__name__}")
    if isinstance(value, str) and not value.strip():
        raise CatalogError(f"{where}: '{key}' must not be empty")
    return value


def _match(value: str, pattern: re.Pattern, where: str, key: str) -> str:
    if not pattern.match(value):
        raise CatalogError(f"{where}: '{key}' has an invalid value {value!r}")
    return value


def _gateway(raw: object) -> GatewaySpec:
    where = "gateway"
    if not isinstance(raw, dict):
        raise CatalogError("'gateway' must be a mapping")
    channel = raw.get("release_channel")
    if channel is not None and (not isinstance(channel, str) or not channel.strip()):
        raise CatalogError("gateway: 'release_channel' must be null or a channel name")
    base = _require(raw, "base_overrides", dict, where)
    if base.get("localModels") != []:
        raise CatalogError("gateway: base_overrides.localModels must be an empty list")
    if (base.get("apolloSecrets") or {}).get("enabled") is not True:
        raise CatalogError("gateway: base_overrides must enable apolloSecrets")
    return GatewaySpec(
        product_id=_match(_require(raw, "product_id", str, where), _PRODUCT_ID_RE, where, "product_id"),
        entity_name=_require(raw, "entity_name", str, where),
        namespace=_match(_require(raw, "namespace", str, where), _DNS_LABEL_RE, where, "namespace"),
        service=_match(_require(raw, "service", str, where), _DNS_LABEL_RE, where, "service"),
        port=_require(raw, "port", int, where),
        config_block_version=_match(
            _require(raw, "config_block_version", str, where), _VERSION_RE, where,
            "config_block_version",
        ),
        release_channel=channel,
        base_overrides=base,
    )


def _model(raw: object, index: int, defaults: dict) -> ModelSpec:
    where = f"models[{index}]"
    if not isinstance(raw, dict):
        raise CatalogError(f"{where} must be a mapping")
    gpu = _require(raw, "gpu", dict, where)
    task = _require(raw, "task", str, where)
    platform = _require(raw, "platform", str, where)
    if task not in TASKS:
        raise CatalogError(f"{where}: 'task' must be one of {sorted(TASKS)}")
    if platform not in PLATFORMS:
        raise CatalogError(f"{where}: 'platform' must be one of {sorted(PLATFORMS)}")
    return ModelSpec(
        id=_match(_require(raw, "id", str, where), _ID_RE, where, "id"),
        display_name=_require(raw, "display_name", str, where),
        description=_require(raw, "description", str, where),
        task=task,
        platform=platform,
        gpu_count=_require(gpu, "count", int, f"{where}.gpu"),
        min_vram_gb=_require(gpu, "min_vram_gb", int, f"{where}.gpu"),
        product_id=_match(_require(raw, "product_id", str, where), _PRODUCT_ID_RE, where, "product_id"),
        entity_name=_require(raw, "entity_name", str, where),
        config_block_version=_match(
            _require(raw, "config_block_version", str, where), _VERSION_RE, where,
            "config_block_version",
        ),
        service=_match(_require(raw, "service", str, where), _DNS_LABEL_RE, where, "service"),
        port=_require(raw, "port", int, where),
        served_model=_require(raw, "served_model", str, where),
        storage_gb=_require(raw, "storage_gb", int, where),
        install_overrides=merge_overrides(
            defaults, _check_overrides(raw.get("install_overrides") or {}, where),
        ),
    )


def _shown(raw: object, index: int) -> ShownModel:
    where = f"other_models[{index}]"
    if not isinstance(raw, dict):
        raise CatalogError(f"{where} must be a mapping")
    gpu = _require(raw, "gpu", dict, where)
    task = _require(raw, "task", str, where)
    platform = _require(raw, "platform", str, where)
    if task not in TASKS | {"decision"}:
        raise CatalogError(f"{where}: 'task' must be one of {sorted(TASKS | {'decision'})}")
    if platform not in PLATFORMS:
        raise CatalogError(f"{where}: 'platform' must be one of {sorted(PLATFORMS)}")
    return ShownModel(
        id=_match(_require(raw, "id", str, where), _ID_RE, where, "id"),
        display_name=_require(raw, "display_name", str, where),
        description=_require(raw, "description", str, where),
        task=task,
        platform=platform,
        gpu_count=_require(gpu, "count", int, f"{where}.gpu"),
        min_vram_gb=_require(gpu, "min_vram_gb", int, f"{where}.gpu"),
        product_id=_match(_require(raw, "product_id", str, where), _PRODUCT_ID_RE, where, "product_id"),
        entity_name=_require(raw, "entity_name", str, where),
    )


def parse_catalog(text: str) -> Catalog:
    """Parse and validate catalog YAML. Raises CatalogError on anything invalid."""
    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise CatalogError(f"catalog is not valid YAML ({type(e).__name__})") from None
    if not isinstance(raw, dict):
        raise CatalogError("catalog must be a mapping")
    if raw.get("version") != 1:
        raise CatalogError("catalog 'version' must be 1")
    gateway = _gateway(raw.get("gateway"))
    models_raw = raw.get("models")
    if not isinstance(models_raw, list) or not models_raw:
        raise CatalogError("'models' must be a non-empty list")
    defaults = _check_overrides(raw.get("model_overrides") or {}, "model_overrides")
    models = tuple(_model(m, i, defaults) for i, m in enumerate(models_raw))
    for key in ("id", "product_id", "entity_name", "service"):
        values = [getattr(m, key) for m in models]
        dupes = sorted({v for v in values if values.count(v) > 1})
        if dupes:
            raise CatalogError(f"models: duplicate {key} {dupes}")
    if gateway.product_id in {m.product_id for m in models}:
        raise CatalogError("models: a model may not share the gateway's product_id")
    shown_raw = raw.get("other_models") or []
    if not isinstance(shown_raw, list):
        raise CatalogError("'other_models' must be a list")
    shown = tuple(_shown(m, i) for i, m in enumerate(shown_raw))
    for key in ("id", "product_id"):
        values = [getattr(m, key) for m in (*models, *shown)]
        dupes = sorted({v for v in values if values.count(v) > 1})
        if dupes:
            raise CatalogError(f"models and other_models: duplicate {key} {dupes}")
    return Catalog(version=1, gateway=gateway, models=models, shown=shown)


@functools.lru_cache(maxsize=1)
def load_catalog() -> Catalog:
    """The packaged catalog, parsed once per process."""
    return parse_catalog(CATALOG_PATH.read_text(encoding="utf-8"))
