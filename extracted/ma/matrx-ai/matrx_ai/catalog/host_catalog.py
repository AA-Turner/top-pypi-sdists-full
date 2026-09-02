"""Host-injected model catalog — model lookup + routing without the ORM.

A client host (no Postgres — matrx-local) injects a catalog via
``matrx_ai.configure(model_catalog=...)``. The catalog serves plain model
dicts (the shape ``ai.model_definition`` rows serialize to via ``to_dict()``
— the aidream ``GET /api/ai-models`` payload); this module wraps them in
:class:`CatalogModel` so every consumer that reads attributes off an ORM
model row (``model.id`` / ``model.name`` /
``model.capabilities`` / ``model.pricing``) works unchanged.

``AiModelManager`` checks this catalog BEFORE the ORM path, and
``resolve_call_profile`` builds a synthetic :class:`ResolvedCallProfile`
directly from the model dict (no ai.endpoint / ai.api / ai.offering rows
exist in a client host).

Routing in catalog mode
-----------------------
A catalog model's wire route resolves in order:
1. an explicit ``wire_format`` key on the dict,
2. the first entry of an ``endpoints`` list that names a known wire format
   (the 0.1.x synthetic-model shape matrx-local already produces:
   ``{"endpoints": ["generic_openai_chat"]}``).
A model that resolves to no known wire format RAISES — never a silent
fallback. (The legacy ``api_class`` derivation died with the column; a
client host must supply routable data explicitly.)

Runtime models
--------------
``register_runtime_model(model)`` adds a synthetic, process-local entry —
matrx-local uses it to expose the currently-connected local llama-server as
``local/<model>`` with ``endpoints=["generic_openai_chat"]`` so
``UnifiedAIClient`` routes it to the registered ``GenericOpenAIChat``
instance. This is the PUBLIC replacement for poking
``AiModelManager._api_cache`` (0.1.x). Runtime models are checked first in
every lookup and work in both catalog and ORM hosts.

Offline baseline
----------------
``matrx_ai/local_data/models_data.py`` remains the packaged offline baseline
of per-provider model data (synced from the provider APIs). A host that needs
a zero-network catalog can build its ``list_models()`` from it; matrx-ai
itself does not auto-load it.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from matrx_utils import vcprint

from matrx_ai._ext import get_ext, has_ext

#: The _ext registry key under which the catalog is registered.
MODEL_CATALOG_KEY = "model_catalog"

#: Methods a ModelCatalog must implement (validation + structural check).
MODEL_CATALOG_METHODS: tuple[str, ...] = ("list_models", "get_model")


@runtime_checkable
class ModelCatalog(Protocol):
    """Host-implemented model catalog for client-host installs."""

    async def list_models(self) -> list[dict[str, Any]]:
        """Return every model dict (ai.model_definition ``to_dict()`` shape)."""
        ...

    async def get_model(self, id_or_name: str) -> dict[str, Any] | None:
        """Return the model dict whose id OR name matches, or None."""
        ...


def missing_catalog_methods(candidate: Any) -> list[str]:
    """Return the ModelCatalog method names ``candidate`` lacks."""
    return [
        name
        for name in MODEL_CATALOG_METHODS
        if not callable(getattr(candidate, name, None))
    ]


def get_model_catalog() -> ModelCatalog | None:
    """Return the host-injected ModelCatalog, or None when unset."""
    if not has_ext(MODEL_CATALOG_KEY):
        return None
    return get_ext(MODEL_CATALOG_KEY)


class CatalogModel:
    """Attribute-access wrapper over a plain model dict.

    Gives catalog-served dicts the same read surface as an ORM model row:
    ``model.id``, ``model.name``, ``model.capabilities``,
    ``model.pricing``, ``model.provider_id`` … — a missing key reads as
    None (matching a NULL column), and ``to_dict()`` returns the raw dict.
    """

    __slots__ = ("_data",)

    def __init__(self, data: dict[str, Any]) -> None:
        if not isinstance(data, dict):
            raise TypeError(
                f"CatalogModel expects a model dict; got {type(data).__name__!r}"
            )
        object.__setattr__(self, "_data", data)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        try:
            return self._data[name]
        except KeyError:
            return None

    def get(self, name: str, default: Any = None) -> Any:
        return self._data.get(name, default)

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    def __repr__(self) -> str:  # pragma: no cover — debug nicety
        return f"CatalogModel(name={self._data.get('name')!r}, id={self._data.get('id')!r})"


# ---------------------------------------------------------------------------
# Runtime model registry (synthetic local-LLM entries)
# ---------------------------------------------------------------------------

_DEFAULT_RUNTIME_CAPABILITIES: dict[str, Any] = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling"],
    "interaction": "turn",
    "multilingual": False,
}

_runtime_models: dict[str, dict[str, Any]] = {}


def register_runtime_model(model: dict[str, Any]) -> None:
    """Register (or replace) a synthetic runtime model entry.

    ``model`` must carry a non-empty ``name`` (used as the lookup key; ``id``
    defaults to it). matrx-local's local-LLM entry shape is supported as-is::

        register_runtime_model({
            "id": "local/qwen2.5",
            "name": "local/qwen2.5",
            "display_name": "qwen2.5 (Local)",
            "provider": "local",
            "is_active": True,
            "endpoints": ["generic_openai_chat"],
        })

    ``capabilities`` defaults to a text-in/text-out function-calling chat
    profile when absent — pass an explicit ``{input, output, features, ...}``
    dict to override. Idempotent per name (re-registering replaces).
    """
    name = str(model.get("name") or "").strip()
    if not name:
        raise ValueError("register_runtime_model: model dict must carry a non-empty 'name'")
    entry = dict(model)
    entry.setdefault("id", name)
    entry.setdefault("capabilities", dict(_DEFAULT_RUNTIME_CAPABILITIES))
    _runtime_models[name] = entry
    vcprint(f"[catalog] runtime model registered: {name}", color="green")


def unregister_runtime_model(id_or_name: str) -> bool:
    """Remove a runtime model by name or id. Returns True when removed."""
    key = str(id_or_name)
    if key in _runtime_models:
        del _runtime_models[key]
        vcprint(f"[catalog] runtime model unregistered: {key}", color="yellow")
        return True
    for name, entry in list(_runtime_models.items()):
        if str(entry.get("id")) == key:
            del _runtime_models[name]
            vcprint(f"[catalog] runtime model unregistered: {name}", color="yellow")
            return True
    return False


def get_runtime_model(id_or_name: str) -> CatalogModel | None:
    """Return the runtime model matching name or id, or None."""
    key = str(id_or_name)
    entry = _runtime_models.get(key)
    if entry is None:
        for candidate in _runtime_models.values():
            if str(candidate.get("id")) == key:
                entry = candidate
                break
    return CatalogModel(entry) if entry is not None else None


def list_runtime_models() -> list[CatalogModel]:
    """Every registered runtime model (registration order)."""
    return [CatalogModel(entry) for entry in _runtime_models.values()]


# ---------------------------------------------------------------------------
# Catalog-mode routing (wire-format resolution + synthetic profile)
# ---------------------------------------------------------------------------


def resolve_catalog_wire_format(model: CatalogModel) -> str:
    """Resolve the wire route for a catalog-served model (see module docs).

    Raises ``ValueError`` (loudly logged) when no known wire format can be
    determined — a client host must supply routable model data, never get a
    silent default.
    """
    from matrx_ai.catalog.manager import WIRE_FORMATS

    explicit = model.get("wire_format")
    if isinstance(explicit, str) and explicit:
        if explicit not in WIRE_FORMATS:
            raise ValueError(
                f"model '{model.name}' declares unknown wire_format {explicit!r} "
                f"(known: {sorted(WIRE_FORMATS)})"
            )
        return explicit

    endpoints = model.get("endpoints")
    if isinstance(endpoints, list | tuple):
        for candidate in endpoints:
            if isinstance(candidate, str) and candidate in WIRE_FORMATS:
                return candidate

    raise ValueError(
        f"Catalog model '{model.name}' carries no routable wire format: no "
        "'wire_format' key and no known 'endpoints' entry. Add wire_format "
        "(a UnifiedAIClient dispatch attr, e.g. 'openai_chat') to the model dict."
    )


# ── client-host fallback control rules (per chat wire) ──────────────────────
# A DB host compiles its controls from ai.api.rules <- ai.offering.override.
# A client host has neither, and PURE passthrough is wrong for the flipped
# chat translators: raw reasoning/thinking keys would leak onto providers that
# reject them, and Anthropic would be sent NO max_tokens (its SDK requires
# one). These mirror the DB api-level (conservative, family-agnostic) rules;
# per-model reasoning dialects need real offering rows — a client host that
# wants them supplies a DB-backed catalog.
_BASE_UNSUPPORTED_KEYS: tuple[str, ...] = (
    "clear_thinking",
    "thinking_level",
    "thinking_budget",
    "include_thoughts",
    "reasoning_effort",
    "reasoning_summary",
)
_THINKING_CONSUMES = [
    "thinking_budget",
    "thinking_level",
    "include_thoughts",
    "reasoning_summary",
    "clear_thinking",
]


def _openai_style_fallback(max_key: str, *, stop: bool, seed: bool) -> dict[str, Any]:
    rules: dict[str, Any] = {key: {"supported": False} for key in _BASE_UNSUPPORTED_KEYS}
    rules.update(
        {
            "temperature": {},
            "top_p": {},
            "top_k": {"supported": False},
            "max_output_tokens": {"provider_key": max_key},
            "stop_sequences": {"provider_key": "stop"} if stop else {"supported": False},
            "seed": {} if seed else {"supported": False},
        }
    )
    return rules


_CATALOG_FALLBACK_CHAT_RULES: dict[str, dict[str, Any]] = {
    "openai_chat": _openai_style_fallback("max_output_tokens", stop=False, seed=False),
    "groq_chat": _openai_style_fallback("max_completion_tokens", stop=True, seed=False),
    "cerebras_chat": _openai_style_fallback("max_completion_tokens", stop=True, seed=True),
    "xai_chat": _openai_style_fallback("max_tokens", stop=True, seed=False),
    "together_chat": _openai_style_fallback("max_tokens", stop=True, seed=False),
    "huggingface_chat": _openai_style_fallback("max_tokens", stop=True, seed=False),
    "generic_openai_chat": _openai_style_fallback("max_tokens", stop=True, seed=False),
    "google_chat": {
        **{key: {"supported": False} for key in _BASE_UNSUPPORTED_KEYS},
        "temperature": {},
        "top_p": {"supported": False},
        "top_k": {"supported": False},
        "seed": {"supported": False},
        "stop_sequences": {"supported": False},
        "max_output_tokens": {},
    },
    "anthropic_chat": {
        **{
            key: {"supported": False}
            for key in ("thinking_level", "thinking_budget", "include_thoughts",
                        "reasoning_summary", "clear_thinking")
        },
        "seed": {"supported": False},
        "stop_sequences": {"supported": False},
        "reasoning_effort": {
            "processor": "anthropic_thinking",
            "processor_config": {
                "mode": "budget",
                "order": 100,
                "consumes": list(_THINKING_CONSUMES),
                "default_max_tokens": 32768,
            },
        },
        "temperature": {
            "processor": "anthropic_temp_topp_exclusion",
            "processor_config": {"order": 200, "consumes": ["top_p", "top_k"]},
        },
        "max_output_tokens": {"provider_key": "max_tokens"},
    },
    "mock_chat": {
        "temperature": {},
        "top_p": {},
        "stop_sequences": {},
        "max_output_tokens": {},
    },
}


def _fallback_controls(wire_format: str) -> Any:
    from matrx_ai.catalog.controls import CompiledControlsMap
    from matrx_ai.catalog.models import ControlRule

    raw = _CATALOG_FALLBACK_CHAT_RULES.get(wire_format)
    if raw is None:
        return CompiledControlsMap(rules={})
    return CompiledControlsMap(
        rules={key: ControlRule.model_validate(rule) for key, rule in raw.items()}
    )


def _catalog_model_controls(model: CatalogModel, wire_format: str) -> Any:
    """Controls for a catalog-served model — DB-authored rules first.

    A DB-backed server exports each model's resolved control rules into the
    catalog payload (``AiCatalogManager.export_model_routing`` →
    ``control_rules`` on the model dict). When present they are authoritative:
    they are the SAME api ⊕ offering merge the server itself shapes params
    with, so a client host (matrx-local) can never drift from the DB — e.g.
    budget-vs-adaptive Anthropic thinking, which is a per-MODEL fact no
    per-wire fallback can know. Only a model dict without ``control_rules``
    (runtime/local models, stale caches) falls back to the conservative
    per-wire rules below — loudly, because on a modern catalog that means the
    payload is missing data the server exports.
    """
    from matrx_ai.catalog.controls import CompiledControlsMap
    from matrx_ai.catalog.models import ControlRule

    raw_rules = model.get("control_rules")
    if isinstance(raw_rules, dict) and raw_rules:
        try:
            return CompiledControlsMap(
                rules={
                    key: ControlRule.model_validate(rule)
                    for key, rule in raw_rules.items()
                }
            )
        except Exception as exc:  # noqa: BLE001 — a bad payload must not kill routing
            vcprint(
                f"[catalog] model '{model.name}' carries control_rules that failed "
                f"validation ({exc}); falling back to the per-wire "
                f"'{wire_format}' rules. The server payload and matrx-ai "
                "ControlRule schema have drifted — fix the exporter.",
                title="🚨 CATALOG CONTROL RULES INVALID",
                color="red",
            )
    return _fallback_controls(wire_format)


def build_catalog_call_profile(model: CatalogModel) -> Any:
    """Build a synthetic ``ResolvedCallProfile`` from a catalog model dict.

    Client hosts have no ai.endpoint / ai.api / ai.offering rows, so the
    profile is derived entirely from the model dict: fallback chat controls
    per wire (above; pure passthrough for non-chat wires), offering/endpoint/
    api ids stamped as ``catalog:*`` markers, pricing straight off the dict.
    The capability object comes from the same ``resolve_model_capabilities``
    seam the server path uses.
    """
    from matrx_ai.catalog.models import ResolvedCallProfile
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    wire_format = resolve_catalog_wire_format(model)
    from matrx_ai.catalog.resolve import client_attr_for_wire_format

    # vendor = the wire route's family token (openai_chat → openai);
    # extraction/realtime specials keep their full name as the vendor label.
    vendor = wire_format.rsplit("_", 1)[0] if "_" in wire_format else wire_format
    if wire_format in ("generic_openai_chat",):
        vendor = "generic_openai"

    name = str(model.name or "")
    provider_model_id = str(model.get("provider_model_id") or name)
    provider_name = str(model.get("provider") or vendor)
    tts = model.get("tts") if isinstance(model.get("tts"), dict) else {}
    voices = tts.get("voices", ())
    if isinstance(voices, str):
        voices = (voices,)

    return ResolvedCallProfile(
        model_id=str(model.id or name),
        model_name=name,
        provider_model_id=provider_model_id,
        offering_id=f"catalog:{name}",
        endpoint_id=f"catalog:{vendor}",
        api_id=f"catalog:{wire_format}",
        provider_name=provider_name,
        vendor=vendor,
        wire_format=wire_format,
        client_attr=client_attr_for_wire_format(wire_format),
        base_url=model.get("base_url"),
        auth_ref={},
        byok_secret_key=None,
        capabilities=resolve_model_capabilities(model),
        controls=_catalog_model_controls(model, wire_format),
        request_defaults={},
        pricing=model.get("pricing"),
        usage_basis=model.get("usage_basis"),
        token_billed=bool(model.get("token_billed", False)),
        model_is_deprecated=bool(model.get("is_deprecated", False)),
        model_is_primary=bool(model.get("is_primary", False)),
        offering_metadata={"tts": tts} if tts else {},
        tts_voice_ids=tuple(str(voice) for voice in voices),
        tts_default_voice_id=(
            str(tts["default_voice"]) if tts.get("default_voice") else None
        ),
    )


__all__ = [
    "MODEL_CATALOG_KEY",
    "MODEL_CATALOG_METHODS",
    "CatalogModel",
    "ModelCatalog",
    "build_catalog_call_profile",
    "get_model_catalog",
    "get_runtime_model",
    "list_runtime_models",
    "missing_catalog_methods",
    "register_runtime_model",
    "resolve_catalog_wire_format",
    "unregister_runtime_model",
]
