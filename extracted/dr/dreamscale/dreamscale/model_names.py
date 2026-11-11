"""User-facing model names.

LLM names resolve before dispatch and session admission (``resolve_llm_model``).

Policy models can also be known to users by a public name (``pi0.5-bimanualyam``) while
the platform keys them by an internal id (``pi05-yam``): the catalog's
``model_variants.public_id``, mirrored in ``PUBLIC_NAMES``. The control plane accepts
either name. The SDK keys its per-model contracts on the internal id it shares with the
transport and the workers, so names convert at the edges: ``internal_model`` where a
name comes in (``connect``, ``--model``, control-plane responses) and ``public_model``
where one goes out to a person (printed output, errors).
"""

# Latest means the latest qualified model in this SDK release. Persist and send
# the concrete provider ID so an existing session never changes models.
_LATEST = {
    "astra": "gpt-6-astra",
    "sol": "gpt-6.1-sol",
    "terra": "gpt-6.1-terra",
    "luna": "gpt-6-luna",
    "fable": "claude-fable-5-2",
    "opus": "claude-opus-5-5",
    "sonnet": "claude-sonnet-5-5",
    "haiku": "claude-haiku-5-5",
    "argon": "gemini-4-argon",
    "carbon": "gemini-4-carbon",
}
_ALIASES = {
    **_LATEST,
    **{f"{family}-latest": model for family, model in _LATEST.items()},
    "claude-fable-5.1": "claude-fable-5-1",
    "fable-5.1": "claude-fable-5-1",
    "claude-fable-5.2": "claude-fable-5-2",
    "fable-5.2": "claude-fable-5-2",
    "claude-opus-5.5": "claude-opus-5-5",
    "opus-5.5": "claude-opus-5-5",
    "claude-sonnet-5.5": "claude-sonnet-5-5",
    "sonnet-5.5": "claude-sonnet-5-5",
    "claude-haiku-5.5": "claude-haiku-5-5",
    "haiku-5.5": "claude-haiku-5-5",
}


def resolve_llm_model(model: str) -> str:
    """Resolve known aliases; preserve policy IDs and unknown names for validation."""
    return _ALIASES.get(model, model)


def _public_names() -> dict[str, str]:
    """Internal id -> public name: each deployment base's and catalog model's that differs
    (dreamscale_transport.families and .catalog; CI checks them against
    model_variants.public_id)."""
    from dreamscale_transport import catalog, families

    return {
        **{family.deploy.base: family.deploy.public_id for family in families.FAMILIES
           if family.deploy is not None and family.deploy.public_id != family.deploy.base},
        **{entry.id: entry.public_id for entry in catalog.CATALOG if entry.public_id},
    }


PUBLIC_NAMES: dict[str, str] = _public_names()
_INTERNAL_NAMES = {public: internal for internal, public in PUBLIC_NAMES.items()}


# One name for what people run, <account>/<model>: ``dreamscale/<model>`` is the system
# catalog (dreamscale/pi0.5-bimanualyam), ``<account>/<slug>`` an organization's deployment
# (northstar-robotics/pi0.5-towel-fold). A bare name is a catalog model, or your own
# deployment of that slug.
CATALOG = "dreamscale"


def is_account_ref(name: str | None) -> bool:
    """``<account>/<slug>`` with an account other than the catalog: a deployment."""
    account, slash, rest = (name or "").partition("/")
    return bool(slash and account and rest) and account != CATALOG


def internal_model(name: str) -> str:
    """The internal id a model name refers to, by either name, with or without the catalog's
    account (an internal id passes through)."""
    name = name.removeprefix(CATALOG + "/")
    if name in _INTERNAL_NAMES:
        return _INTERNAL_NAMES[name]
    return next((internal for internal, listed in _LISTED_NAMES.items() if listed == name), name)


def public_model(name: str) -> str:
    """The name users know a model by (unrenamed ids pass through)."""
    return PUBLIC_NAMES.get(name) or _LISTED_NAMES.get(name, name)


# Names only the control plane knows: a catalog model whose user-facing name lives in Neon's
# model_variants.public_id alone (not in this package), listed with its internal id to the
# organizations that can run it. Filled by ``resolve_model``.
_LISTED_NAMES: dict[str, str] = {}


def _shipped_ids() -> frozenset[str]:
    from dreamscale_transport import catalog, families

    return frozenset({entry.id for entry in catalog.CATALOG} | {
        family.deploy.base for family in families.FAMILIES if family.deploy is not None})


def resolve_model(name: str, *, list_models=None) -> str:
    """``internal_model``, and for a name this SDK doesn't ship, the internal id the control
    plane lists it under for this organization (GET /v1/models ``internal_id``). A name it
    lists under no other id, and any lookup failure, pass through for the usual refusal."""
    internal = internal_model(name)
    if not _unshipped(name, internal):
        return internal
    try:
        rows = (list_models or _list_models)()
    except Exception:  # noqa: BLE001 - offline or signed out: the caller refuses the name
        return internal
    return _listed_id(internal, rows)


async def aresolve_model(name: str, *, api_key: str | None = None, list_models=None) -> str:
    """``resolve_model`` from a running event loop (``aconnect``)."""
    internal = internal_model(name)
    if not _unshipped(name, internal):
        return internal
    try:
        rows = await (list_models or (lambda: _alist_models(api_key)))()
    except Exception:  # noqa: BLE001 - offline or signed out: the caller refuses the name
        return internal
    return _listed_id(internal, rows)


def _unshipped(name: str, internal: str) -> bool:
    return not (internal != name.removeprefix(CATALOG + "/") or is_account_ref(name)
                or internal in _shipped_ids())


def _listed_id(internal: str, rows) -> str:
    for row in rows:
        listed = row.get("internal_id")
        if row.get("id") == internal and isinstance(listed, str) and listed:
            _LISTED_NAMES[listed] = internal
            return listed
    return internal


def _list_models() -> list[dict]:
    import asyncio

    return asyncio.run(_alist_models(None))


async def _alist_models(api_key: str | None) -> list[dict]:
    from dreamscale.config import load_config
    from dreamscale.control import ControlPlaneClient

    config = load_config()
    api_key = api_key or config.api_key
    if not api_key:
        return []
    client = ControlPlaneClient(config.control_plane_url, api_key)
    try:
        return await client.list_models()
    finally:
        await client.close()
