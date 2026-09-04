######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.2+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T00:14:52.323742                                                            #
######################################################################################################

from __future__ import annotations



class ModelAccessDenied(ValueError, metaclass=type):
    """
    Raised when a model is denied by ModelAccessPolicy.
    """
    def __init__(self, model_name, reason):
        ...
    ...

