######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.17.1.0+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-21T23:31:59.905535                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
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
    def __init__(self, template: _Template, lifecycle_hooks: typing.List["_LifecycleHook"]):
        ...
    ...

class HttpExitHook(Hook, metaclass=type):
    def __init__(self, name: str, url: str, method: str = 'GET', headers: typing.Optional[typing.Dict] = None, body: typing.Optional[str] = None, on_success: bool = False, on_error: bool = False):
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

