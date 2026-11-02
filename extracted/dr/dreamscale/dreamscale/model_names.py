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
    "fable": "claude-fable-5-1",
    "opus": "claude-opus-5-5",
    "argon": "gemini-4-argon",
}
_ALIASES = {
    **_LATEST,
    **{f"{family}-latest": model for family, model in _LATEST.items()},
    "claude-fable-5.1": "claude-fable-5-1",
    "fable-5.1": "claude-fable-5-1",
    "claude-opus-5.5": "claude-opus-5-5",
    "opus-5.5": "claude-opus-5-5",
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
    return _INTERNAL_NAMES.get(name, name)


def public_model(name: str) -> str:
    """The name users know a model by (unrenamed ids pass through)."""
    return PUBLIC_NAMES.get(name, name)
