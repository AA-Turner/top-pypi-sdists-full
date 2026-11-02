"""Each catalog wire's checks of how its sessions are served, in the SDK (DSL-353,
docs/plans/2026-10-30-family-registries.md §6.11).

A module here is named for the catalog wire (``CatalogModel.wire``) whose sessions it checks,
and is optional: a wire with none takes the served contract as the server resolves it. A module
may define:

- ``check(model, resolved_config, *, execution_horizon, action_hz_override,
  chunk_size_override, control_hz)``: refuse a served contract that isn't the model's, or an
  override it doesn't take; returns the chunk override the session keeps.
- ``base(model, resolved_config, own)``: the contract the session builds on (``own()``: the
  model's own, ``runtime_contract_for_model``).
- ``own_contract(model)``: refuse a model whose contract only its server knows.
- ``control_hz(model, requested)``: the command rate a caller may ask for.
- ``placement(model, provider, region)``: refuse a provider or region the model isn't served
  on; True when that settles it (region_probe.validate_provider_selection), False to go on to
  the catalog's provider and region lists.
- ``sim_task(model, benchmark, suite)``: refuse a simulator task the model wasn't trained on.

The runtime contract (``policy.runtime.contract``) asks a model's wire module and never names a
model; ``catalog_check`` is the check most wires make, from the model's catalog contract.
"""

from __future__ import annotations

import importlib
import pkgutil
from functools import cache
from types import ModuleType

from dreamscale_transport import catalog


@cache
def _modules() -> dict[str, ModuleType]:
    """Every wire module here, by wire (loaded when first asked: they import the runtime)."""
    return {
        info.name: importlib.import_module(f"{__name__}.{info.name}")
        for info in pkgutil.iter_modules(__path__)
    }


def wires() -> tuple[str, ...]:
    """The wires this SDK checks served contracts for."""
    return tuple(sorted(_modules()))


def module(model: str | None) -> ModuleType | None:
    """The served-contract checks of a model's wire (its catalog entry's), else None."""
    wire = catalog.wire(model) if model else None
    return _modules().get(wire) if wire is not None else None


def hook(model: str | None, name: str):
    """A model's wire module's ``name`` hook, else None."""
    found = module(model)
    return getattr(found, name, None) if found is not None else None
