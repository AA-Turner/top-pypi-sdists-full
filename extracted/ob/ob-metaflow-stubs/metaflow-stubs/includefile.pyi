######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.868674                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow._vendor.click.types
    import metaflow.parameters
    import typing

from ._vendor import click as click
from .exception import MetaflowException as MetaflowException
from .parameters import DelayedEvaluationParameter as DelayedEvaluationParameter
from .parameters import DeployTimeField as DeployTimeField
from .parameters import Parameter as Parameter
from .parameters import ParameterContext as ParameterContext
from .user_configs.config_parameters import ConfigValue as ConfigValue

DATACLIENTS: list

class IncludedFile(object, metaclass=type):
    def __init__(self, descriptor: typing.Dict[str, typing.Any]):
        ...
    @property
    def descriptor(self):
        ...
    @property
    def size(self):
        ...
    def decode(self, name, var_type = 'Artifact'):
        ...
    ...

class FilePathClass(metaflow._vendor.click.types.ParamType, metaclass=type):
    def __init__(self, is_text, encoding):
        ...
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class IncludeFile(metaflow.parameters.Parameter, metaclass=type):
    """
    Includes a local file as a parameter for the flow.
    
    `IncludeFile` behaves like `Parameter` except that it reads its value from a file instead of
    the command line. The user provides a path to a file on the command line. The file contents
    are saved as a read-only artifact which is available in all steps of the flow.
    
    Parameters
    ----------
    name : str
        User-visible parameter name.
    default : Union[str, Callable[ParameterContext, str]]
        Default path to a local file. A function
        implies that the parameter corresponds to a *deploy-time parameter*.
    is_text : bool, optional, default None
        Convert the file contents to a string using the provided `encoding`.
        If False, the artifact is stored in `bytes`. A value of None is equivalent to
        True.
    encoding : str, optional, default None
        Use this encoding to decode the file contexts if `is_text=True`. A value of None
        is equivalent to "utf-8".
    required : bool, optional, default None
        Require that the user specified a value for the parameter.
        `required=True` implies that the `default` is not used. A value of None is
        equivalent to False
    help : str, optional
        Help text to show in `run --help`.
    show_default : bool, default True
        If True, show the default value in the help text. A value of None is equivalent
        to True.
    """
    def __init__(self, name: str, required: typing.Optional[bool] = None, is_text: typing.Optional[bool] = None, encoding: typing.Optional[str] = None, help: typing.Optional[str] = None, **kwargs: typing.Dict[str, str]):
        ...
    def init(self, ignore_errors = False):
        ...
    def load_parameter(self, v):
        ...
    ...

class UploaderV1(object, metaclass=type):
    @classmethod
    def encode_url(cls, url_type, url, **kwargs):
        ...
    @classmethod
    def store(cls, flow_name, path, is_text, encoding, handler, echo):
        ...
    @classmethod
    def size(cls, descriptor):
        ...
    @classmethod
    def load(cls, descriptor):
        ...
    ...

class UploaderV2(object, metaclass=type):
    @classmethod
    def encode_url(cls, url_type, url, **kwargs):
        ...
    @classmethod
    def store(cls, flow_name, path, is_text, encoding, handler, echo):
        ...
    @classmethod
    def size(cls, descriptor):
        ...
    @classmethod
    def load(cls, descriptor):
        ...
    ...

UPLOADERS: dict

class CURRENT_UPLOADER(object, metaclass=type):
    @classmethod
    def encode_url(cls, url_type, url, **kwargs):
        ...
    @classmethod
    def store(cls, flow_name, path, is_text, encoding, handler, echo):
        ...
    @classmethod
    def size(cls, descriptor):
        ...
    @classmethod
    def load(cls, descriptor):
        ...
    ...

