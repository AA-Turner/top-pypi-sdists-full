from contextlib import suppress
from importlib import import_module
from inspect import getmembers
from typing import Any, Iterable

from django.conf import settings
from rest_framework.request import Request


class ConfigRegistry:
    """
    A class that is able to discover all functions that are wrapped in the `@register_config` decorator. This registry
    should never be used from the outside and its sole purpose is to gather all functions, so they are returned
    in the APIView of this module.
    """

    def __init__(self, *args, **kwargs):
        self.config_members = []
        self._load_configs()

    def _load_configs(self):
        for app in settings.INSTALLED_APPS:
            with suppress(ModuleNotFoundError):
                module = import_module(f"{app}.configs")
                for member in getmembers(module, lambda member: hasattr(member, "_is_config")):
                    self.config_members.append(member[1])

    def get_configs(self, request: Request) -> Iterable[tuple[str, Any]]:
        for member in self.config_members:
            if res := member(request=request):
                yield res

    def get_config_dict(self, request: Request) -> dict[str, Any]:
        return dict(self.get_configs(request))


config_registry = ConfigRegistry()
