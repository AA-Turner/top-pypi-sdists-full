"""Typed failures raised before an AI provider call can be routed."""


class CatalogRoutingError(ValueError):
    """The model catalog cannot deterministically route the requested call."""


__all__ = ["CatalogRoutingError"]
