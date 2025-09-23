######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.7);ob(v1)                                                    #
# Generated on 2025-09-23T01:34:30.686770                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.checkpoint_datastores.external_chckpt
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.user_decorators.mutable_flow

from .....user_decorators.mutable_flow import MutableFlow as MutableFlow

NEBIUS_ENDPOINT_URL: str

class nebius_checkpoints(metaflow.mf_extensions.outerbounds.plugins.checkpoint_datastores.external_chckpt._ExternalCheckpointFlowDeco, metaclass=metaflow.user_decorators.user_flow_decorator.FlowMutatorMeta):
    """
    This decorator is used for setting the nebius's S3 compatible object store as the artifact store for
    checkpoints/models created by the flow.
    
    Parameters
    ----------
    secrets: list
        A list of secrets to be added to the step. These secrets should contain any secrets that are required globally and the secret
        for the nebius object store. The secret should contain the following keys:
        - NEBIUS_ACCESS_KEY
        - NEBIUS_SECRET_KEY
    
    bucket_path: str
        The path to the bucket to store the checkpoints/models.
    
    endpoint_url: str
        The endpoint url for the nebius object store. Defaults to `https://storage.eu-north1.nebius.cloud:443`
    
    Usage
    -----
    ```python
    from metaflow import checkpoint, step, FlowSpec, nebius_checkpoints
    
    @nebius_checkpoints(secrets=[], bucket_path=None)
    class MyFlow(FlowSpec):
        @checkpoint
        @step
        def start(self):
            # Saves the checkpoint in the nebius object store
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

