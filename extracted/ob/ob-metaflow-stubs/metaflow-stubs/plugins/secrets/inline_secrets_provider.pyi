######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-04-03T19:36:22.643738                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import abc
    import metaflow.plugins.secrets

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

