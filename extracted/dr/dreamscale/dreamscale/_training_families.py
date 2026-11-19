"""Training descriptors supplied with this client installation."""

from dreamscale_core.training_families import REGISTRY as public

try:
    from dreamscale_serving.training_descriptors import REGISTRY as families
except ModuleNotFoundError as error:
    if error.name not in {"dreamscale_serving", "dreamscale_serving.training_descriptors"}:
        raise
    families = public
