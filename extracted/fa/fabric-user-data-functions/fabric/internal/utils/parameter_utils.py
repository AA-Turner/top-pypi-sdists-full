"""
Utility functions for handling UDF parameters and input validation.
"""

import inspect

from ...functions import udf_exception
from ..converters.basic_datatype_converter import BasicDatatypeConverter


def check_args_for_exceptions(args: tuple, kwargs: dict) -> list:
    """Check arguments and keyword arguments for exception objects.

    Args:
        args: Positional arguments to check
        kwargs: Keyword arguments to check

    Returns:
        List of UserDataFunctionError exceptions found in the arguments
    """
    exceptions = []
    for arg in args:
        if issubclass(type(arg), udf_exception.UserDataFunctionError):
            exceptions.append(arg)
    for key, value in kwargs.items():
        if issubclass(type(value), udf_exception.UserDataFunctionError):
            value.properties['parameter_name'] = key
            exceptions.append(value)

    return exceptions


def create_missing_input_error(param: inspect.Parameter):
    """
    Create a missing input error for a parameter.

    Args:
        param: The parameter that is missing from the request

    Returns:
        UserDataFunctionMissingInputError: Error object with parameter details
    """
    annotation_name = getattr(param.annotation, '__name__', None)
    properties = {
        'parameter_value': "Parameter not found in request",
        'parameter_name': param.name
    }
    if annotation_name:
        properties['parameter_type'] = annotation_name
    return udf_exception.UserDataFunctionMissingInputError(properties=properties)


def apply_fabric_item_providers(
    fabric_item_params: list,
    kwargs: dict,
    func_name: str,
    req,
    provider_factory,
    provider_metadata
) -> None:
    """Apply fabric item providers to parameters.

    Args:
        fabric_item_params: List of fabric item parameters to process
        kwargs: Keyword arguments dict to update with provider-created items
        func_name: Name of the function (for provider metadata)
        req: The HTTP request, which providers read request-scoped data from
        provider_factory: ProviderFactory instance to get providers
        provider_metadata: ProviderMetadata instance to get kwargs
    """
    for arg in fabric_item_params:
        provider = provider_factory.get_provider(arg.annotation)

        if provider:
            item_args = provider_metadata.get_kwargs(func_name, arg.name)
            item = kwargs.get(arg.name, None)
            kwargs[arg.name] = provider.create(item=item, req=req, **item_args)


def parse_scalar_parameters(body: dict, udf_params: list, kwargs: dict) -> None:
    """Parse scalar parameters from request body into kwargs.

    This function extracts parameters from a dictionary body, converts them to the appropriate types,
    and validates that all required parameters are present.

    Args:
        body: Dictionary containing parameter values from request
        udf_params: List of parameter definitions (inspect.Parameter objects)
        kwargs: Dictionary to populate with parsed parameters
    """
    # Parse parameters from body
    for param in udf_params:
        if param.name in body:
            val = body[param.name]
            annotation_name = getattr(param.annotation, "__name__", None)
            kwargs[param.name] = BasicDatatypeConverter.tryconvert(annotation_name, val)

    # Validate missing parameters
    for arg in udf_params:
        if arg.name not in kwargs:
            if arg.default != inspect.Parameter.empty:
                kwargs[arg.name] = arg.default
            else:
                kwargs[arg.name] = create_missing_input_error(arg)
