######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.7);ob(v1)                                                    #
# Generated on 2025-09-23T01:34:30.688254                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.user_decorators.mutable_flow

from .....user_decorators.mutable_flow import MutableFlow as MutableFlow
from .....user_decorators.mutable_step import MutableStep as MutableStep
from .....user_decorators.user_flow_decorator import FlowMutator as FlowMutator

OBP_ASSUME_ROLE_ARN_ENV_VAR: str

class assume_role(metaflow.user_decorators.user_flow_decorator.FlowMutator, metaclass=metaflow.user_decorators.user_flow_decorator.FlowMutatorMeta):
    """
    Flow-level decorator for assuming AWS IAM roles.
    
    When applied to a flow, all steps in the flow will automatically use the specified IAM role-arn
    as their source principal.
    
    Usage:
    ------
    @assume_role(role_arn="arn:aws:iam::123456789012:role/my-iam-role")
    class MyFlow(FlowSpec):
        @step
        def start(self):
            import boto3
            client = boto3.client("dynamodb")  # Automatically uses the role in the flow decorator
            self.next(self.end)
    
        @step
        def end(self):
            from metaflow import get_aws_client
            client = get_aws_client("dynamodb")  # Automatically uses the role in the flow decorator
    """
    def init(self, *args, **kwargs):
        ...
    def pre_mutate(self, mutable_flow: metaflow.user_decorators.mutable_flow.MutableFlow):
        """
        This method is called by Metaflow to apply the decorator to the flow.
        It sets up environment variables that will be used by the AWS client
        to automatically assume the specified role.
        """
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

