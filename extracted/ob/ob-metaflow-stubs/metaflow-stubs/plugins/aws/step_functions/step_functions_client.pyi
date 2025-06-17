######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.028304                                                            #
######################################################################################################

from __future__ import annotations



AWS_SANDBOX_ENABLED: bool

AWS_SANDBOX_REGION: None

SFN_EXECUTION_LOG_GROUP_ARN: None

class StepFunctionsClient(object, metaclass=type):
    def __init__(self):
        ...
    def search(self, name):
        ...
    def push(self, name, definition, role_arn, log_execution_history):
        ...
    def get(self, name):
        ...
    def trigger(self, state_machine_arn, input):
        ...
    def list_executions(self, state_machine_arn, states):
        ...
    def terminate_execution(self, execution_arn):
        ...
    def get_state_machine_arn(self, name):
        ...
    def delete(self, name):
        ...
    ...

