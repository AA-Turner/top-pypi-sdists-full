######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.859689                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow._vendor.click.types
    import metaflow.parameters
    import typing

from ._vendor import click as click
from .exception import ParameterFieldFailed as ParameterFieldFailed
from .exception import ParameterFieldTypeMismatch as ParameterFieldTypeMismatch
from .exception import MetaflowException as MetaflowException

TYPE_CHECKING: bool

class ParameterContext(tuple, metaclass=type):
    """
    ParameterContext(flow_name, user_name, parameter_name, logger, ds_type, configs)
    """
    @staticmethod
    def __new__(_cls, flow_name: str, user_name: str, parameter_name: str, logger: typing.Callable[..., None], ds_type: str, configs: typing.Optional["ConfigValue"]):
        """
        Create new instance of ParameterContext(flow_name, user_name, parameter_name, logger, ds_type, configs)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    def __init__(self, flow_name: str, user_name: str, parameter_name: str, logger: typing.Callable[..., None], ds_type: str, configs: typing.Optional["ConfigValue"]):
        ...
    ...

def flow_context(flow_cls):
    """
    Context manager to set the current flow for the thread. This is used
    to extract the parameters from the FlowSpec that is being used to create
    the CLI.
    """
    ...

context_proto: None

def replace_flow_context(flow_cls):
    """
    Replace the current flow context with a new flow class. This is used
    when we change the current flow class after having run user configuration functions
    """
    ...

class JSONTypeClass(metaflow._vendor.click.types.ParamType, metaclass=type):
    def convert(self, value, param, ctx):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

class DeployTimeField(object, metaclass=type):
    """
    This a wrapper object for a user-defined function that is called
    at deploy time to populate fields in a Parameter. The wrapper
    is needed to make Click show the actual value returned by the
    function instead of a function pointer in its help text. Also, this
    object curries the context argument for the function, and pretty
    prints any exceptions that occur during evaluation.
    """
    def __init__(self, parameter_name, parameter_type, field, fun, return_str = True, print_representation = None):
        ...
    def __call__(self, deploy_time = False):
        ...
    @property
    def description(self):
        ...
    def __str__(self):
        ...
    def __repr__(self):
        ...
    ...

def deploy_time_eval(value):
    ...

def set_parameter_context(flow_name, echo, datastore, configs):
    ...

class DelayedEvaluationParameter(object, metaclass=type):
    """
    This is a very simple wrapper to allow parameter "conversion" to be delayed until
    the `_set_constants` function in FlowSpec. Typically, parameters are converted
    by click when the command line option is processed. For some parameters, like
    IncludeFile, this is too early as it would mean we would trigger the upload
    of the file too early. If a parameter converts to a DelayedEvaluationParameter
    object through the usual click mechanisms, `_set_constants` knows to invoke the
    __call__ method on that DelayedEvaluationParameter; in that case, the __call__
    method is invoked without any parameter. The return_str parameter will be used
    by schedulers when they need to convert DelayedEvaluationParameters to a
    string to store them
    """
    def __init__(self, name, field, fun):
        ...
    def __call__(self, return_str = False):
        ...
    ...

class Parameter(object, metaclass=type):
    """
    Defines a parameter for a flow.
    
    Parameters must be instantiated as class variables in flow classes, e.g.
    ```
    class MyFlow(FlowSpec):
        param = Parameter('myparam')
    ```
    in this case, the parameter is specified on the command line as
    ```
    python myflow.py run --myparam=5
    ```
    and its value is accessible through a read-only artifact like this:
    ```
    print(self.param == 5)
    ```
    Note that the user-visible parameter name, `myparam` above, can be
    different from the artifact name, `param` above.
    
    The parameter value is converted to a Python type based on the `type`
    argument or to match the type of `default`, if it is set.
    
    Parameters
    ----------
    name : str
        User-visible parameter name.
    default : Union[str, float, int, bool, Dict[str, Any],
                Callable[
                    [ParameterContext], Union[str, float, int, bool, Dict[str, Any]]
                ],
            ], optional, default None
        Default value for the parameter. Use a special `JSONType` class to
        indicate that the value must be a valid JSON object. A function
        implies that the parameter corresponds to a *deploy-time parameter*.
        The type of the default value is used as the parameter `type`.
    type : Type, default None
        If `default` is not specified, define the parameter type. Specify
        one of `str`, `float`, `int`, `bool`, or `JSONType`. If None, defaults
        to the type of `default` or `str` if none specified.
    help : str, optional, default None
        Help text to show in `run --help`.
    required : bool, optional, default None
        Require that the user specifies a value for the parameter. Note that if
        a default is provide, the required flag is ignored.
        A value of None is equivalent to False.
    show_default : bool, optional, default None
        If True, show the default value in the help text. A value of None is equivalent
        to True.
    """
    def __init__(self, name: str, default: typing.Union[str, float, int, bool, typing.Dict[str, typing.Any], typing.Callable[[metaflow.parameters.ParameterContext], typing.Union[str, float, int, bool, typing.Dict[str, typing.Any]]], None] = None, type: typing.Union[typing.Type[str], typing.Type[float], typing.Type[int], typing.Type[bool], metaflow.parameters.JSONTypeClass, None] = None, help: typing.Optional[str] = None, required: typing.Optional[bool] = None, show_default: typing.Optional[bool] = None, **kwargs: typing.Dict[str, typing.Any]):
        ...
    def init(self, ignore_errors = False):
        ...
    def __repr__(self):
        ...
    def __str__(self):
        ...
    def option_kwargs(self, deploy_mode):
        ...
    def load_parameter(self, v):
        ...
    @property
    def is_string_type(self):
        ...
    def __getitem__(self, x):
        ...
    ...

def add_custom_parameters(deploy_mode = False):
    ...

JSONType: JSONTypeClass

