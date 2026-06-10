######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.33                                                                                #
# Generated on 2026-06-09T19:39:31.659266                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.plugins.argo.exit_hooks


class JsonSerializable(object, metaclass=type):
    def to_json(self):
        ...
    def __str__(self):
        ...
    ...

class Hook(object, metaclass=type):
    """
    Abstraction for Argo Workflows exit hooks.
    A hook consists of a Template, and one or more LifecycleHooks that trigger the template
    """
    def __annotate_func__(format):
        ...
    ...

class HttpExitHook(Hook, metaclass=type):
    def __init__(self, name: str, url: str, method: str = 'GET', headers: typing.Union[typing.Dict, None] = None, body: typing.Union[str, None] = None, on_success: bool = False, on_error: bool = False):
        ...
    ...

class ExitHookHack(Hook, metaclass=type):
    def __init__(self, url, headers = None, body = None):
        ...
    ...

class ContainerHook(Hook, metaclass=type):
    def __init__(self, name: str, container: typing.Dict, service_account_name: str = None, on_success: bool = False, on_error: bool = False):
        ...
    ...

