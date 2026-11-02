"""
Shared gateway glue: the catalogue lookup, the `Model` row, and the response envelope.

WHY this lives in `_core` rather than in any one endpoint: `chat()` and `decide()` both resolve a
model string against the catalogue and pull the same shell fields off a response. Duplicating either
across the surfaces is how they drift. (act's
`Policy` resolves its own model once at `connect()` and does not come through here.)

`Model` is the catalogue row every surface receives from `models()`; it is defined here, in the
shared layer, because it is not specific to chat or decide.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Model:
    """One entry of `models()`: everything on the platform a user can start from, told apart by `kind`.

    kind="model"    — a model the platform serves itself, called with a key (GET /v1/models): `endpoint` is "chat"
                      or "decide", the rest of the row (pricing, supported_parameters, ...) is in `raw`.
    kind="template" — a starting point for `seq init <name>` (GET /v1/templates): `template_kind` is "policy",
                      "benchmark" or "adapter", `stable` / `beta` the version each channel points at, `usage` the
                      command; it has no endpoint.

    A robot policy has no entry: it runs as its own deployment, and what it reads and returns is its own, not a
    catalogue row.
    """

    id: str
    endpoint: str
    architecture: str
    raw: dict[str, Any] = field(default_factory=dict)
    kind: str = "model"
    template_kind: str | None = None
    stable: str | None = None
    beta: str | None = None
    usage: str | None = None

    @property
    def short_id(self) -> str:
        """`gpt-6-luna` rather than `accounts/sequences/models/gpt-6-luna` (a template's id is its name already)."""
        return self.id.rsplit("/", 1)[-1]

    @property
    def pricing(self) -> list[dict[str, Any]]:
        """What this model costs, spelled as the console's Models page and the bill spell it: one {"amount", "unit"} a
        line - [{"amount": "$10.5", "unit": "M in"}, {"amount": "$52.5", "unit": "M out"}] - or [] for a template or
        a model not priced yet."""
        quote = self.raw.get("pricing") or {}
        rows = (quote.get("display") or {}).get("rows") or []
        return [dict(r) for r in rows if isinstance(r, dict) and r.get("amount")] if quote.get("priceable") else []

    @property
    def supported_parameters(self) -> list[str] | None:
        """The request parameters a chat model takes, by their usual names (`reasoning` among them when it
        thinks); [] for a decision model, None for a template or when the platform has not read them yet."""
        return self.raw.get("supported_parameters")





_CATALOGUE: dict[tuple[str | None, str | None], dict[str, Model]] = {}


def _catalogue(api_key: str | None, base_url: str | None) -> dict[str, Model]:
    """The catalogue as a {short_id or full id -> Model} map, fetched once per deployment."""
    key = (api_key, base_url)
    cat = _CATALOGUE.get(key)
    if cat is None:



        from .. import models as _list_models

        by_id: dict[str, Model] = {}


        for m in _list_models(kind="model", api_key=api_key, base_url=base_url):
            by_id[m.short_id] = m
            by_id[m.id] = m
        _CATALOGUE[key] = cat = by_id
    return cat


def _resolve(model: Model | str, api_key: str | None, base_url: str | None, endpoint: str) -> Model:
    """A Model passed through untouched, or a string looked up in the catalogue.

    A name the catalogue does not list goes to the gateway as written: only it can say whether the name was retired
    on purpose (410 `Gone`, with what replaced it) or never existed (404 `NotFound`), and that answer is the same
    exception whichever call meets it."""
    if isinstance(model, Model):
        return model
    hit = _catalogue(api_key, base_url).get(model)
    if hit is None:
        return Model(id=model, endpoint=endpoint, architecture="")
    return hit


def _envelope(r: dict[str, Any], model_id: str) -> dict[str, Any]:
    """The shell fields every one-shot response carries, pulled defensively. Shared by chat and
    decide so the surfaces cannot disagree on how a response is unwrapped."""
    return {
        "id": r.get("id", ""),
        "model": r.get("model", model_id),
        "usage": r.get("usage") or {},
        "perf": r.get("perf") or {},
        "warnings": r.get("warnings") or [],
    }
