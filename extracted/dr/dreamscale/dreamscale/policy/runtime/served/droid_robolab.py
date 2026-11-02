"""RoboLab DROID policy releases: the served contract is the catalog's; a model with a
placement rule of its own (``client.placement_name``) runs on AWS or Modal, from us-west-2."""

from __future__ import annotations

from dreamscale_transport import catalog

from dreamscale.policy.runtime.contract import catalog_check


def check(model, resolved_config, **served):
    return catalog_check(model, catalog.entry(model).client.refusal_name, resolved_config,
                         **served)


def placement(model, provider, region):
    from dreamscale.region_probe import _US_WEST_OK

    name = catalog.entry(model).client.placement_name
    if name is None:
        return False
    if provider not in (None, "aws", "modal"):
        raise ValueError(f"{name} supports provider='aws' or provider='modal'")
    if region not in _US_WEST_OK:
        raise ValueError(f"{name} is served from us-west-2")
    return True
