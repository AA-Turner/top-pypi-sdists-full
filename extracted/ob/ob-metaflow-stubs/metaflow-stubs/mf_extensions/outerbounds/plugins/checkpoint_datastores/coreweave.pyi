######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.1.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-07-15T20:32:21.490363                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.mutable_flow
    import metaflow.user_decorators.user_flow_decorator

from .....user_decorators.user_flow_decorator import FlowMutator as FlowMutator
from .....user_decorators.mutable_flow import MutableFlow as MutableFlow
from .....user_decorators.mutable_step import MutableStep as MutableStep

class coreweave_checkpoints(metaflow.user_decorators.user_flow_decorator.FlowMutator, metaclass=metaflow.user_decorators.user_flow_decorator.FlowMutatorMeta):
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
    
    @coreweave_checkpoints(secrets=[], bucket_path="s3://my-coreweave-bucket/foo")
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
    def init(self, *args, **kwargs):
        ...
    def pre_mutate(self, mutable_flow: metaflow.user_decorators.mutable_flow.MutableFlow):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

