# flake8: noqa: I005
import datetime
from typing import Any, Optional
from azure.functions.decorators.core import DataType, InputBinding
import azure
import json
import builtins

from fabric.functions.udf_exception import UserDataFunctionInternalError, UserDataFunctionInvalidInputError, UserDataFunctionMissingInputError

class UdfPropertyInput(InputBinding):
    @staticmethod
    def get_binding_name() -> str:
        return 'UdfProperty'
    
    def __init__(self,
                name: str,
                parameterName: str,
                typeName: Optional[str] = None,
                data_type: Optional[DataType] = DataType.STRING,
                **kwargs):
        super().__init__(name, data_type)


# The input converter that automatically gets registered in the function app.
class UdfPropertyConverter(azure.functions.meta.InConverter, binding='UdfProperty'):
    
    def try_convert_type(value: object, pytype: type) -> object:
        if isinstance(value, str):
            # this is the case if the tuple is passed as a string e.g., '[1,2,3]'
            value_as_json = json.loads(value)
            return pytype(value_as_json)
        return pytype(value)
    
    def try_convert_bool(value: object) -> bool:
        if value == None:
            return False
        elif isinstance(value, str):
            if value.lower() == 'false' or value == '' or value == '0' or value == '0.0': # Everything but False / false should return True
                return False
            elif value.lower() == 'true' or value == '1' or value == '1.0':
                return True
        elif value == 0 or value == False:
            return False
        elif value == 1 or value == True:
            return True

        raise ValueError("Input is not a valid boolean value")

    special_types = {
        "dict": lambda x : UdfPropertyConverter.try_convert_type(x, dict),
        "list": lambda x : UdfPropertyConverter.try_convert_type(x, list),
        "set": lambda x : UdfPropertyConverter.try_convert_type(x, set),
        "tuple": lambda x : UdfPropertyConverter.try_convert_type(x, tuple),
        "bool": lambda x : UdfPropertyConverter.try_convert_bool(x),
    }

    @classmethod
    def check_input_type_annotation(cls, pytype: type) -> bool:
        return True



    @classmethod
    def decode(cls, data, *,
               trigger_metadata) -> Any:
        if data is not None and data.type == 'string' and data.value is not None:
            body = json.loads(data.value)
            error = body.get('ErrorMessage', None)
            if error:
                if error == "Parameter does not exist in binding data":
                    return UserDataFunctionMissingInputError()
                
                return UserDataFunctionInternalError(
                    f"Unable to load data successfully for parameter. This could be because the invocation isn't valid JSON.", {'reason': error})
        else:
            return UserDataFunctionInternalError(
                'Unable to load data successfully for udf property')
        return tryconvert(body['PropertyType'], body['PropertyJsonValue'])

def get_type(type_name): 
      try: 
          return getattr(builtins, type_name) 
      except AttributeError: 
          return None 

def tryconvert(property_type: str, property_json_value: str):
    if not property_json_value:  # This can happen if/when the value is empty, so we should return None
        return None
    value_as_json = json.loads(property_json_value)
    if value_as_json == None:
        return None
    
    if property_type == 'datetime': # datetime is not a built in, so we must handle it separately
        return datetime.datetime.fromisoformat(value_as_json)

    if property_type == 'UdfString': # locate can't find custom classes within its
        # own module unless their names are qualified with module name, so let's 
        # just make the only custom type we are allowing in a conditional here
        return value_as_json

    # Built ins go here
    prop_type = get_type(property_type)
    prop_type_name = getattr(prop_type, '__name__', None)
    try:
        if prop_type_name in UdfPropertyConverter.special_types:
            constructor = UdfPropertyConverter.special_types[prop_type_name]
            return constructor(value_as_json)
        return prop_type(value_as_json)
    except (ValueError, TypeError, json.JSONDecodeError): 
        # We can get ValueError, JSONDecodeError, and TypeError due to the special_types that have json.loads
        # Since we can't catch this exception and return it in the formatted output, we will return it as the value of the parameter and then check the parameter types for it
        # We add the parameter name later on in fabric_app.py
        return UserDataFunctionInvalidInputError(properties={'parameter_type': property_type, 'parameter_value': value_as_json})
