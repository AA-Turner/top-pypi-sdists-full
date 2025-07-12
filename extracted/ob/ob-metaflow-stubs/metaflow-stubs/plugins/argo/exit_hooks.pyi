######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.655621                                                            #
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
    def __init__(self, template: _Template, lifecycle_hooks: typing.List["_LifecycleHook"]):
        ...
    ...

class HttpExitHook(Hook, metaclass=type):
    def __init__(self, name, url, method = 'GET', headers = None, body = None, on_success = False, on_error = False):
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

