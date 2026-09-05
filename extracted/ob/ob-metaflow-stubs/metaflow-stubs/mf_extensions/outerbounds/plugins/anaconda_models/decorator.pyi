######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.3+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T19:03:46.029002                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.user_step_decorator

from .....user_decorators.user_step_decorator import user_step_decorator as user_step_decorator
from .....user_decorators.user_step_decorator import StepMutator as StepMutator
from .exceptions import ModelAccessDenied as ModelAccessDenied

class anaconda_models(metaflow.user_decorators.user_step_decorator.StepMutator, metaclass=metaflow.user_decorators.user_step_decorator.UserStepDecoratorMeta):
    """
    Pull Anaconda catalog models inside a Metaflow step.
    
    Injects ``@card`` and exposes ``self.anaconda_models`` with a
    ``.model(...)`` method. Authentication is handled via OBP platform
    environment variables (OBP_API_SERVER, OBP_PERIMETER, METAFLOW_SERVICE_HEADERS).
    
    Parameters
    ----------
    temp_dir_root : str, optional
        Root directory for downloaded model files.
        Defaults to a new temp directory per step execution.
    """
    def init(self, temp_dir_root = None):
        ...
    def mutate(self, mutable_step):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

