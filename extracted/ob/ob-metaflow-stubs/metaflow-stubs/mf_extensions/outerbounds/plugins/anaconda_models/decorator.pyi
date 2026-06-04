######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.32.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-03T22:23:58.325942                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.user_step_decorator

from .....user_decorators.user_step_decorator import user_step_decorator as user_step_decorator
from .....user_decorators.user_step_decorator import StepMutator as StepMutator

class anaconda_models(metaflow.user_decorators.user_step_decorator.StepMutator, metaclass=metaflow.user_decorators.user_step_decorator.UserStepDecoratorMeta):
    """
    Pull Anaconda catalog models inside a Metaflow step.
    
    Injects ``@card`` and ``@secrets`` for the API key and exposes
    ``self.anaconda_models`` with a ``.model(...)`` method.
    
    Parameters
    ----------
    integration_name : str
        Metaflow secret source for the Anaconda API key
        (e.g. "outerbounds.ac-models-keys").
    temp_dir_root : str, optional
        Root directory for downloaded model files.
        Defaults to a new temp directory per step execution.
    """
    def init(self, integration_name, temp_dir_root = None):
        ...
    def mutate(self, mutable_step):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

