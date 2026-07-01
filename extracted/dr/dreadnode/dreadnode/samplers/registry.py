"""Registry for sampler factories - enables JSON-based configuration for API exposure."""

import typing as t

from dreadnode.optimization.sampler import Sampler

# Registry of sampler factories by type name
SAMPLER_REGISTRY: dict[str, t.Callable[..., Sampler[t.Any]]] = {}


def register_sampler(
    name: str,
) -> t.Callable[[t.Callable[..., Sampler[t.Any]]], t.Callable[..., Sampler[t.Any]]]:
    """Decorator to register a sampler factory function.

    Args:
        name: The type name for this sampler (used in JSON config).

    Example:
        @register_sampler("temperature_search")
        def temperature_search(base_model: str, ...) -> GridSampler:
            ...
    """

    def decorator(fn: t.Callable[..., Sampler[t.Any]]) -> t.Callable[..., Sampler[t.Any]]:
        SAMPLER_REGISTRY[name] = fn
        return fn

    return decorator


def create_sampler(config: dict[str, t.Any]) -> Sampler[t.Any]:
    """Create a sampler from a configuration dict.

    This enables JSON-based sampler configuration for API endpoints.

    Args:
        config: Configuration dict with:
            - "type": The registered sampler type name
            - "params": Optional dict of parameters for the factory function

    Returns:
        Configured Sampler instance.

    Raises:
        ValueError: If the sampler type is not registered.

    Example:
        sampler = create_sampler({
            "type": "temperature_search",
            "params": {
                "base_model": "openai/gpt-4",
                "temperatures": [0.0, 0.5, 1.0]
            }
        })
    """
    sampler_type = config.get("type")
    if not sampler_type:
        raise ValueError("Sampler config must include 'type' field")

    if sampler_type not in SAMPLER_REGISTRY:
        available = ", ".join(sorted(SAMPLER_REGISTRY.keys())) or "(none)"
        raise ValueError(f"Unknown sampler type: {sampler_type}. Available: {available}")

    params = config.get("params", {})
    return SAMPLER_REGISTRY[sampler_type](**params)


def list_samplers() -> list[str]:
    """List all registered sampler type names."""
    return sorted(SAMPLER_REGISTRY.keys())
