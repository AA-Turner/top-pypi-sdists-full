######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.19.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-02-19T20:41:45.629026                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.mutable_flow
    import metaflow.user_decorators.user_flow_decorator

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
    
    You can also filter which steps should use the role:
    @assume_role(role_arn="arn:aws:iam::123456789012:role/my-iam-role", steps=["start", "process"])
    class MyFlow(FlowSpec):
        @step
        def start(self):
            # user code in this step will use the assumed role
            pass
    
        @step
        def process(self):
            # user code in this step will use the assumed role
            pass
    
        @step
        def end(self):
            # user code in this step will NOT use the assumed role
            pass
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

