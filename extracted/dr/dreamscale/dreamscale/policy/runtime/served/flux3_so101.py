"""A policy release whose served contract is the catalog's, every predicted action
executable, named in refusals by its catalog refusal name."""

from __future__ import annotations

from dreamscale_transport import catalog

from dreamscale.policy.runtime.contract import catalog_check


def check(model, resolved_config, **served):
    return catalog_check(model, catalog.entry(model).client.refusal_name, resolved_config,
                         **served)
