"""
This module contains functions for serializing and deserializing lmfit objects.
"""

from typing import TYPE_CHECKING

from bec_lib.utils.import_utils import lazy_import_from

if TYPE_CHECKING:  # pragma: no cover
    from lmfit import Parameter, Parameters
else:
    Parameter, Parameters = lazy_import_from("lmfit", ("Parameter", "Parameters"))


def serialize_param_object(param: Parameter) -> dict:
    """
    Serialize lmfit.Parameter object to JSON-serializable dictionary.

    Args:
        param (Parameter): Parameter object

    Returns:
        dict: Dictionary representation of the parameter
    """
    obj = {
        "name": param.name,
        "value": param.value,
        "vary": param.vary,
        "min": param.min,
        "max": param.max,
        "expr": param.expr,
        "brute_step": param.brute_step,
    }
    return obj


def serialize_lmfit_params(params: Parameters) -> dict:
    """
    Serialize lmfit.Parameters object to JSON-serializable dictionary.

    Args:
        params (Parameters): Parameters object containing lmfit.Parameter objects

    Returns:
        dict: Dictionary representation of the parameters
    """
    if not params:
        return {}
    if isinstance(params, Parameters):
        return {k: serialize_param_object(v) for k, v in params.items()}
    if isinstance(params, list):
        return {v.name: serialize_param_object(v) for v in params}


def deserialize_param_object(obj: dict) -> Parameter:
    """
    Deserialize dictionary representation of lmfit.Parameter object.

    Args:
        obj (dict): Dictionary representation of the parameters

    Returns:
        Parameter: Parameter object
    """
    param = Parameters()
    for k, v in obj.items():
        v.pop("name")
        param.add(k, **v)
    return param
