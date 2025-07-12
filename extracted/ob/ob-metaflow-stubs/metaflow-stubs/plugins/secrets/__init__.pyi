######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.547845                                                            #
######################################################################################################

from __future__ import annotations

import typing
import abc
if typing.TYPE_CHECKING:
    import abc

from . import utils as utils
from . import secrets_spec as secrets_spec
from . import secrets_func as secrets_func
from .secrets_func import get_secret as get_secret
from . import secrets_decorator as secrets_decorator
from . import inline_secrets_provider as inline_secrets_provider

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

