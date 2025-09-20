######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.6);ob(v1)                                                    #
# Generated on 2025-09-19T21:56:58.734044                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.secrets
    import abc

from . import SecretsProvider as SecretsProvider

class InlineSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Intended to be used for testing purposes only.
        """
        ...
    ...

