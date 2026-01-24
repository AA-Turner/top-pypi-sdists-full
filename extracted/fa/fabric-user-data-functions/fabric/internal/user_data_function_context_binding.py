# flake8: noqa: I005
from typing import Any
from azure.functions.decorators.core import InputBinding
import azure
import json

from fabric.functions.udf_exception import UserDataFunctionInternalError
from fabric.functions.fabric_class import UserDataFunctionContext

class UserDataFunctionContextInput(InputBinding):
    @staticmethod
    def get_binding_name() -> str:
        return 'UserDataFunctionContext'
    
    def __init__(self,
                name: str,
                **kwargs):
        super().__init__(name)


# The input converter that automatically gets registered in the function app.
class UserDataFunctionContextConverter(azure.functions.meta.InConverter, binding='UserDataFunctionContext'):

    @classmethod
    def check_input_type_annotation(cls, pytype: type) -> bool:
        return pytype == UserDataFunctionContext

    @classmethod
    def decode(cls, data, *,
               trigger_metadata) -> Any:
        
        if data is not None and data.type == 'string' and data.value is not None: 
            body = json.loads(data.value) 
        else:
            raise UserDataFunctionInternalError(
                f'Unable to load data successfully for UserDataFunctionContext parameter.')
         
        body = json.loads(data.value) 

        return cls.parseType(body)
    
    @classmethod
    def parseType(self, body: json):

        return UserDataFunctionContext(
                invocationId=body['InvocationId'],
                executingUser=body['ExecutingUser'])    
