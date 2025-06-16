import abc
from typing import TYPE_CHECKING

from .contexts import APIContext, YAMLContext

if TYPE_CHECKING:
    import papi  # noqa


class PapiObject(metaclass=abc.ABCMeta):
    papi: "papi.Papi"

    def to_api(self, api_context: APIContext):
        raise NotImplementedError(f"{self} must implement to_api")

    def to_yaml(self, yaml_context: YAMLContext):
        raise NotImplementedError(f"{self} must implement to_yaml")
