# flake8: noqa: I003
from functools import wraps
import logging
from azure.functions import HttpRequest
import inspect
from typing import Callable, TypeVar

from fabric.functions.udf_exception import UserDataFunctionInvalidInputError, UserDataFunctionMissingInputError
from fabric.internal.arrow import arrow_request
from fabric.internal.converters.basic_datatype_converter import BasicDatatypeConverter
from .function_parameter_keywords import REQ_PARAMETER
import json
import asyncio
from fabric.internal.providers import ProviderMetadata, ProviderFactory

T = TypeVar('T')

def create_missing_input_error(param: inspect.Parameter):
    annotation_name = getattr(param.annotation, '__name__', None)
    properties = {'parameter_value': "Parameter not found in request"}
    if annotation_name:
        properties['parameter_type'] = annotation_name
    return UserDataFunctionMissingInputError(properties=properties)

def add_parameters(func: Callable[..., T], 
                   udfParams: list[inspect.Parameter], 
                   fabricItemParams: list[inspect.Parameter]):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # get request from kwargs
        req : HttpRequest = None
        if REQ_PARAMETER in kwargs:
            req = kwargs[REQ_PARAMETER]
        # find parameters in request and add to kwargs
        content_type = req.headers.get('Content-Type')
        if content_type == None or 'application/json' in content_type:
            body = req.get_json()
            for param in udfParams:
                if param.name in body:
                    #kwargs[param.name] = body[param.name]
                    val = body[param.name]
                    kwargs[param.name] = BasicDatatypeConverter.tryconvert(param.annotation.__name__, val)
        elif 'multipart/form-data' in content_type:
            
            # file can be parameters or a octet stream for arrow upload
            for file in req.files:
                
                if file == "parameters":
                    # parse udf parameters
                    json_part = req.files[file]
                    json_data = json.loads(json_part.stream._file.read())
                    for param in udfParams:
                        if param.name in json_data:
                            val = json_data[param.name]
                            kwargs[param.name] = BasicDatatypeConverter.tryconvert(param.annotation.__name__, val)
                        elif param.default != inspect.Parameter.empty:
                            kwargs[param.name] = param.default
                        else:
                            kwargs[param.name] = create_missing_input_error(param)
                else:
                    # ensure parameter exists
                    param = next((item for item in udfParams if item.name == file), None)
                    if param is None:
                        continue
                    # parse as arrow to pandas
                    # file = name of part = name of parameter
                    try:
                        arrow_part = req.files[file].read()
                        ar_request = arrow_request(arrow_part)
                        pandas_df = ar_request.to_pandas()
                        kwargs[file] = pandas_df
                    except Exception as e:
                        kwargs[arg.name] = UserDataFunctionInvalidInputError(properties={'parameter_type': param.annotation.__name__, 'parameter_value': "Unable to parse"})
                continue
            
        for arg in udfParams:
            if arg.name not in kwargs:
                if arg.default != inspect.Parameter.empty:
                    kwargs[arg.name] = arg.default
                else:
                    kwargs[arg.name] = create_missing_input_error(arg)

        for arg in fabricItemParams:
            # Get Provider if it exists for annotation type
            provider = ProviderFactory().get_provider(arg.annotation)
            
            if provider:
                item_args = ProviderMetadata().get_kwargs(func.__name__, arg.name)
                # Create item from provider and use that instead of FabricItem
                kwargs[arg.name] = provider.create(item=kwargs[arg.name], **item_args)

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs) 
        else: 
            return func(*args, **kwargs) 
    return wrapper