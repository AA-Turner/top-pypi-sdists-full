######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39.1+obcheckpoint(0.2.14);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-10-05T21:11:54.613857                                                            #
######################################################################################################

from __future__ import annotations



class ModelAccessDenied(ValueError, metaclass=type):
    """
    Raised when a model is denied by ModelAccessPolicy.
    """
    def __init__(self, model_name, reason):
        ...
    ...

