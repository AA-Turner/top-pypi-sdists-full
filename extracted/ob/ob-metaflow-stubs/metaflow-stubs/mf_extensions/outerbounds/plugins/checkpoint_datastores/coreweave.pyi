######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.880586                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_configs.config_decorators

from .....user_configs.config_decorators import MutableFlow as MutableFlow
from .....user_configs.config_decorators import MutableStep as MutableStep
from .....user_configs.config_decorators import CustomFlowDecorator as CustomFlowDecorator

class coreweave_checkpoints(metaflow.user_configs.config_decorators.CustomFlowDecorator, metaclass=type):
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
    def evaluate(self, mutable_flow: metaflow.user_configs.config_decorators.MutableFlow):
        ...
    ...

