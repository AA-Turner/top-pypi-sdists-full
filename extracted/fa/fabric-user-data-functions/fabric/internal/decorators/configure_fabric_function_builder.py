# flake8: noqa: I003
import inspect
from typing import Any, Callable, List, Optional, Type
from azure.functions import HttpRequest, HttpResponse, FunctionApp, Context
from fabric.functions.fabric_class import (
    FabricLakehouseClient,
    FabricSqlConnection,
    UserDataFunctionContext,
    FabricVariablesClient,
)
from fabric.functions.fabric_item import FabricItem
from fabric.internal.decorators.constants import SpecConstants
from fabric.internal.utils.spec_utils import get_multipart_content
from fabric.internal.openapi_spec_generator import (
    create_pydantic_model,
    FunctionMetadata
)
from fabric.internal.utils.docstring_parser import extract_summary_description
from .ensure_formatted_returntype import ensure_formatted_returntype
from .add_timeout import add_timeout
from .remove_unused_binding_params import remove_unused_binding_params
from .add_parameters import add_parameters
from .log_error import log_error
from fabric.internal.fabric_lakehouse_files_client import FabricLakehouseFilesClient
from pydantic import BaseModel
from fabric.internal.providers.provider_factory import ProviderFactory

from .function_parameter_keywords import (
    REQ_PARAMETER,
    CONTEXT_PARAMETER,
    UNUSED_FABRIC_CONTEXT_PARAMETER,
)


def configure_fabric_function_builder(
    udf: FunctionApp, wrap, functions_metadata: List[FunctionMetadata]
) -> Callable[..., Any]:
    def decorator(func):
        sig = inspect.signature(func)

        # Update function parameters to include a request object for validation
        params = []
        params.append(inspect.Parameter(REQ_PARAMETER, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=HttpRequest))
        params.append(inspect.Parameter(UNUSED_FABRIC_CONTEXT_PARAMETER, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=UserDataFunctionContext))
        params.append(inspect.Parameter(CONTEXT_PARAMETER, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Context))

        # Udf params to be parsed from the request
        udfParams = []
        fabricItemParams = []
        for param in sig.parameters.values():
            # Ensure bindings are still there
            if _is_typeof_fabricitem_input(
                param.annotation
            ) or _is_typeof_userdatafunctioncontext_input(param.annotation):
                param = inspect.Parameter(
                        param.name,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=param.annotation,
                    )
                fabricItemParams.append(param)
                params.append(param)
            # Separate out basic parameters to parse later
            if param.name != REQ_PARAMETER and param.name != CONTEXT_PARAMETER:
                udfParams.append(
                    inspect.Parameter(
                        param.name,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        annotation=_get_cleaned_type_and_wrap_str(param),
                        default=param.default,
                    )
                )
        sig = sig.replace(parameters=tuple(params)).replace(return_annotation=str)
        func.__signature__ = sig
        annotations = {}
        # Update annotations to ensure it uses the cleaned type
        for param in params:
            annotations[param.name] = param.annotation
        # Update return annotation of func to be HttpResponse
        # We should catch if they don't have a return type during metadata generation, but good to double check here
        if "return" in func.__annotations__:
            annotations["old_return"] = func.__annotations__["return"]

        annotations["return"] = HttpResponse
        func.__annotations__ = annotations

        # Add wrapper for function to handle ensure all return values are parsed to HttpResponse
        user_func = log_error(func)
        user_func = remove_unused_binding_params(user_func)
        user_func = add_timeout(user_func)
        user_func = ensure_formatted_returntype(user_func)

        # Add parameters to the function
        user_func = add_parameters(user_func, udfParams, fabricItemParams)
        fb = udf._validate_type(user_func)
        udf._function_builders.append(fb)

        _build_spec(user_func, udfParams, functions_metadata, func.__annotations__)

        return wrap(fb, user_func)

    return decorator


def _is_typeof_fabricitem_input(obj):
    # Check to see if parameter is anything we might return from a fabric binding
    return (
        obj == FabricSqlConnection
        or obj == FabricLakehouseFilesClient
        or obj == FabricLakehouseClient
        or obj == FabricItem
        or obj in ProviderFactory().get_types()
        or obj == FabricVariablesClient
    )


def _is_typeof_userdatafunctioncontext_input(obj):
    # Check to see if parameter is anything we might return from a fabric binding
    return obj == UserDataFunctionContext


def _get_cleaned_type_and_wrap_str(param):
    if hasattr(param.annotation, "__origin__"):
        return param.annotation.__origin__
    else:
        return param.annotation
    
def _build_spec(
    user_func: Callable[..., Any],
    udfParams: List[inspect.Parameter],
    functions_metadata: List[FunctionMetadata],
    func_annotations: dict,
) -> None:
    # Remove FabricSqlConnection, FabricLakehouseClient, UserDataFunctionContext from the parameters
    # or anything in the provider factory
    
    input_params: List[inspect.Parameter] = [
        param for param in udfParams if param.annotation not in [
            FabricSqlConnection, 
            FabricLakehouseClient, 
            UserDataFunctionContext,
            FabricItem,
            FabricVariablesClient,
            *ProviderFactory().get_types(),
        ]
    ]


    # Create a pydantic model from udfParams
    req_param_model_name: str = f"{user_func.__name__.capitalize()}RequestModel"
    req_param_model: Type[BaseModel] = create_pydantic_model(f"{req_param_model_name}", input_params)
    # Create a pydantic model from the return type
    res_param_model_name: str = f"{user_func.__name__.capitalize()}ResponseModel"
    old_return_annotation: Optional[Type] = func_annotations.get("old_return", None)
    
    # Create full response model with all fields
    res_param_model: Type[BaseModel] = create_pydantic_model(
        f"{res_param_model_name}",
        [
            inspect.Parameter(
                "functionName",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            ),
            inspect.Parameter(
                "invocationId",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            ),
            inspect.Parameter(
                "status",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=str,
            ),
            inspect.Parameter(
                "output",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=old_return_annotation,
            ),
            inspect.Parameter(
                "errors",
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=List[str],
                default=[],
            )
        ],
    )

    if user_func.__name__ not in [SpecConstants.SPEC_FUNCTION_NAME_JSON, SpecConstants.SPEC_FUNCTION_NAME_YAML]:
        summary: str
        desc: str
        summary, desc = extract_summary_description(user_func.__doc__)
        multipart_req: dict
        binary_res: dict
        multipart_req_model: Optional[Type[BaseModel]] = None
        multipart_req, binary_res, multipart_req_model = get_multipart_content(user_func.__name__, udfParams)
        func_metadata: FunctionMetadata = FunctionMetadata(user_func.__name__)
        func_metadata.add_path(
            f"/{user_func.__name__}/invoke",
            {
                "post": {
                    "summary": f"{summary}",
                    "description": f"{desc}",
                    "operationId": f"{user_func.__name__}",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": f"#/components/schemas/{req_param_model.__name__}"
                                }
                            },
                            **multipart_req
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": f"#/components/schemas/{res_param_model.__name__}"
                                    }
                                },
                                **binary_res
                            },
                        },
                        "400": {
                            "description": "Bad Request - Invalid input, missing input, or user thrown error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Unauthorized",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        },
                        "403": {
                            "description": "Forbidden",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        },
                        "408": {
                            "description": "Request Timeout - Execution time exceeded timeout limit",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        },
                        "409": {
                            "description": "Conflict",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        },
                        "413": {
                            "description": "Response Too Large - Response exceeds the maximum size limit",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        },
                        "500": {
                            "description": "Internal Server Error - System exception or programming error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                    }
                                }
                            }
                        }
                    },
                }
            },
        )
        func_metadata.add_component(req_param_model_name, req_param_model)
        func_metadata.add_component(res_param_model_name, res_param_model)
        
        if multipart_req_model:
            func_metadata.add_component(multipart_req_model.__name__, multipart_req_model)

        functions_metadata.append(func_metadata)