# flake8: noqa : I005, I900, I001, I003

from fabric.internal.openapi_spec_generator import create_pydantic_model
from pydantic import BaseModel
import copy
import inspect


def get_multipart_content(
    func_name: str, udf_params: list[inspect.Parameter]
) -> tuple[dict, dict, BaseModel]:
    # If udfParams contains a parameter of type pandas.DataFrame, then the request is expected to be a multipart/form-data request
    # where the parameters are in the 'parameters' part and the files are in the 'files' part
    udf_params_copy = copy.deepcopy(udf_params)
    has_pandas_df = False
    df_params = list(
        filter(
            lambda param: param.annotation.__name__ == "DataFrame"
            or param.annotation.__name__ == "Series",
            udf_params_copy,
        )
    )
    arrow_params = {}
    if len(df_params) > 0:
        has_pandas_df = True
        for param in df_params:
            # Remove the parameter from the list of parameters
            udf_params_copy.remove(param)
            # Add the parameter to the arrow_params dictionary
            arrow_params[param.name] = {
                "type": "string",
                "format": "binary",
                "description": f"The Arrow file for the parameter '{param.name}'",
            }

    if len(arrow_params) > 0:
        req_param_model_name = f"{func_name.capitalize()}MultipartRequestModel"
        req_param_model = create_pydantic_model(
            f"{req_param_model_name}", udf_params_copy
        )
    else:
        req_param_model = {}
    # If the function has a pandas.DataFrame parameter, then the request is expected to be a multipart/form-data request
    # where the parameters are in the 'parameters' part and the files are in the 'files' part
    if has_pandas_df:
        req = {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "required": ["parameters", *arrow_params.keys()],
                    "properties": {
                        "parameters": {
                            "$ref": f"#/components/schemas/{req_param_model.__name__}"
                        },
                        **arrow_params,
                    },
                },
                "encoding": {
                    "parameters": {"contentType": "application/json"},
                    **{
                        param: {"contentType": "application/octet-stream"}
                        for param in arrow_params.keys()
                    },
                },
            }
        }
        res = {
            "application/octet-stream": {
                "schema": {"type": "string", "format": "binary"}
            }
        }
        return req, res, req_param_model
    else:
        return {}, {}, None
