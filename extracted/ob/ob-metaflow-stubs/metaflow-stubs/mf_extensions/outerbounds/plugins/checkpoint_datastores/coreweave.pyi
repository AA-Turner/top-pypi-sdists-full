######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.3.2+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-09T09:20:35.524848                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.mutable_flow
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.mf_extensions.outerbounds.plugins.checkpoint_datastores.external_chckpt

from .....user_decorators.user_flow_decorator import FlowMutator as FlowMutator
from .....user_decorators.mutable_flow import MutableFlow as MutableFlow
from .....user_decorators.mutable_step import MutableStep as MutableStep

class coreweave_checkpoints(metaflow.mf_extensions.outerbounds.plugins.checkpoint_datastores.external_chckpt._ExternalCheckpointFlowDeco, metaclass=metaflow.user_decorators.user_flow_decorator.FlowMutatorMeta):
    """
    This decorator is used for setting the coreweave object store as the artifact store for checkpoints/models created by the flow.
    
    Parameters
    ----------
    secrets: list
        A list of secrets to be added to the step. These secrets should contain any secrets that are required globally and the secret
        for the coreweave object store. The secret should contain the following keys:
        - COREWEAVE_ACCESS_KEY
        - COREWEAVE_SECRET_KEY
    
    bucket_path: str
        The path to the bucket to store the checkpoints/models.
    
    Usage
    -----
    ```python
    from metaflow import checkpoint, step, FlowSpec, coreweave_checkpoints
    
    @coreweave_checkpoints(secrets=[], bucket_path=None)
    class MyFlow(FlowSpec):
        @checkpoint
        @step
        def start(self):
            # Saves the checkpoint in the coreweave object store
            current.checkpoint.save("./foo.txt")
    
        @step
        def end(self):
            pass
    ```
    """
    def __init__(self, *args, **kwargs):
        ...
    def init(self, *args, **kwargs):
        ...
    def pre_mutate(self, mutable_flow: metaflow.user_decorators.mutable_flow.MutableFlow):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

