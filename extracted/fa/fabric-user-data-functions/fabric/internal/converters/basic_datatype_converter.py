# flake8: noqa: I005

import datetime
from typing import Any, Optional
import builtins
import json
from fabric.internal.lib_helpers import module_factory
from fabric.functions.udf_exception import UserDataFunctionInvalidInputError

class BasicDatatypeConverter:

    @staticmethod
    def try_convert_type(value: object, pytype: type) -> object:
        if isinstance(value, str):
            # this is the case if the tuple is passed as a string e.g., '[1,2,3]'
            value_as_json = json.loads(value)
            return pytype(value_as_json)
        return pytype(value)
    
    @staticmethod
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

    @staticmethod
    def try_convert_dataframe(value: object):
        pd = module_factory().load_module('pandas')
        return pd.DataFrame.from_dict(value, orient='columns')

    @staticmethod
    def try_convert_series(value: object):
        pd = module_factory().load_module('pandas')
        return pd.Series(value)

    special_types = {
        "dict": lambda x : BasicDatatypeConverter.try_convert_type(x, dict),
        "list": lambda x : BasicDatatypeConverter.try_convert_type(x, list),
        "set": lambda x : BasicDatatypeConverter.try_convert_type(x, set),
        "tuple": lambda x : BasicDatatypeConverter.try_convert_type(x, tuple),
        "bool": lambda x : BasicDatatypeConverter.try_convert_bool(x),
    }

    @staticmethod
    def check_input_type_annotation(pytype: type) -> bool:
        return True
      
    @staticmethod
    def tryconvert(property_type: str, property_value: str):
        try:
            if property_type == 'datetime':
                # datetime is not a builtin type, so we need to handle it separately
                return datetime.datetime.fromisoformat(property_value)
            elif property_type == "DataFrame":
                # if the value is a string, we need to convert it to a list first
                if isinstance(property_value, str):
                    property_value = json.loads(property_value)
                return BasicDatatypeConverter.try_convert_dataframe(property_value)
            elif property_type == 'Series':
                if isinstance(property_value, str):
                    # if the value is a string, we need to convert it to a list first
                    
                    property_value = json.loads(property_value)
                return BasicDatatypeConverter.try_convert_series(property_value)

            prop_type = get_type(property_type)
            prop_type_name = getattr(prop_type, '__name__', None)
            if prop_type_name in BasicDatatypeConverter.special_types:
                constructor = BasicDatatypeConverter.special_types[prop_type_name]
                return constructor(property_value)
            else:
                return prop_type(property_value)
            
        except (ValueError, TypeError, json.JSONDecodeError): 
            # We can get ValueError, JSONDecodeError, and TypeError due to the special_types that have json.loads
            # Since we can't catch this exception and return it in the formatted output, we will return it as the value of the parameter and then check the parameter types for it
            # We add the parameter name later on in fabric_app.py
            return UserDataFunctionInvalidInputError(properties={'parameter_type': property_type, 'parameter_value': property_value})
        
def get_type(type_name): 
      try: 
          return getattr(builtins, type_name) 
      except AttributeError: 
          return None 