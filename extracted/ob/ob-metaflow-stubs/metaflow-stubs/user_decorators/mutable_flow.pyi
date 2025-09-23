######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.7);ob(v1)                                                    #
# Generated on 2025-09-23T01:34:30.700043                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import functools
    import metaflow.flowspec
    import metaflow.user_configs.config_parameters
    import metaflow.user_decorators.mutable_step
    import typing
    import metaflow.parameters

from ..exception import MetaflowException as MetaflowException
from ..user_configs.config_parameters import ConfigValue as ConfigValue

TYPE_CHECKING: bool

class MutableFlow(object, metaclass=type):
    def __init__(self, flow_spec: "metaflow.flowspec.FlowSpec", pre_mutate: bool = False, statically_defined: bool = False, inserted_by: typing.Optional[str] = None):
        ...
    @property
    def decorator_specs(self) -> typing.Generator[typing.Tuple[str, str, typing.List[typing.Any], typing.Dict[str, typing.Any]], None, None]:
        """
        Iterate over all the decorator specifications of this flow. Note that the same
        type of decorator may be present multiple times and no order is guaranteed.
        
        The returned tuple contains:
        - The decorator's name (shortest possible)
        - The decorator's fully qualified name (in the case of Metaflow decorators, this
          will indicate which extension the decorator comes from)
        - A list of positional arguments
        - A dictionary of keyword arguments
        
        You can use the decorator specification to remove a decorator from the flow
        for example.
        
        Yields
        ------
        str, str, List[Any], Dict[str, Any]
            A tuple containing the decorator name, it's fully qualified name,
            a list of positional arguments, and a dictionary of keyword arguments.
        """
        ...
    @property
    def configs(self) -> typing.Generator[typing.Tuple[str, metaflow.user_configs.config_parameters.ConfigValue], None, None]:
        """
        Iterate over all user configurations in this flow
        
        Use this to parameterize your flow based on configuration. As an example, the
        `pre_mutate`/`mutate` methods can add decorators to steps in the flow that
        depend on values in the configuration.
        
        ```
        class MyDecorator(FlowMutator):
            def mutate(flow: MutableFlow):
                val = next(flow.configs)[1].steps.start.cpu
                flow.start.add_decorator(environment, vars={'mycpu': val})
                return flow
        
        @MyDecorator()
        class TestFlow(FlowSpec):
            config = Config('myconfig.json')
        
            @step
            def start(self):
                pass
        ```
        can be used to add an environment decorator to the `start` step.
        
        Yields
        ------
        Tuple[str, ConfigValue]
            Iterates over the configurations of the flow
        """
        ...
    @property
    def parameters(self) -> typing.Generator[typing.Tuple[str, "metaflow.parameters.Parameter"], None, None]:
        """
        Iterate over all the parameters in this flow.
        
        Yields
        ------
        Tuple[str, Parameter]
            Name of the parameter and parameter in the flow
        """
        ...
    @property
    def steps(self) -> typing.Generator[typing.Tuple[str, "metaflow.user_decorators.mutable_step.MutableStep"], None, None]:
        """
        Iterate over all the steps in this flow. The order of the steps
        returned is not guaranteed.
        
        Yields
        ------
        Tuple[str, MutableStep]
            A tuple with the step name and the step proxy
        """
        ...
    def add_parameter(self, name: str, value: "metaflow.parameters.Parameter", overwrite: bool = False):
        """
        Add a parameter to the flow. You can only add parameters in the `pre_mutate`
        method.
        
        Parameters
        ----------
        name : str
            Name of the parameter
        value : Parameter
            Parameter to add to the flow
        overwrite : bool, default False
            If True, overwrite the parameter if it already exists
        """
        ...
    def remove_parameter(self, parameter_name: str) -> bool:
        """
        Remove a parameter from the flow.
        
        The name given should match the name of the parameter (can be different
        from the name of the parameter in the flow. You can not remove config parameters.
        You can only remove parameters in the `pre_mutate` method.
        
        Parameters
        ----------
        parameter_name : str
            Name of the parameter
        
        Returns
        -------
        bool
            Returns True if the parameter was removed
        """
        ...
    def add_decorator(self, deco_type: typing.Union[functools.partial, str], deco_args: typing.Optional[typing.List[typing.Any]] = None, deco_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None, duplicates: int = 1):
        """
        Add a Metaflow flow-decorator to a flow. You can only add decorators in the
        `pre_mutate` method.
        
        You can either add the decorator itself or its decorator specification for it
        (the same you would get back from decorator_specs). You can also mix and match
        but you cannot provide arguments both through the string and the
        deco_args/deco_kwargs.
        
        As an example:
        ```
        from metaflow import project
        
        ...
        my_flow.add_decorator(project, deco_kwargs={"name":"my_project"})
        ```
        
        is equivalent to:
        ```
        my_flow.add_decorator("project:name=my_project")
        ```
        
        Note in the later case, there is no need to import the flow decorator.
        
        The latter syntax is useful to, for example, allow decorators to be stored as
        strings in a configuration file.
        
        In terms of precedence for decorators:
          - if a decorator can be applied multiple times all decorators
            added are kept (this is rare for flow-decorators).
          - if `duplicates` is set to `MutableFlow.IGNORE`, then the decorator
            being added is ignored (in other words, the existing decorator has precedence).
          - if `duplicates` is set to `MutableFlow.OVERRIDE`, then the *existing*
            decorator is removed and this newly added one replaces it (in other
            words, the newly added decorator has precedence).
          - if `duplicates` is set to `MutableFlow.ERROR`, then an error is raised but only
            if the newly added decorator is *static* (ie: defined directly in the code).
            If not, it is ignored.
        
        Parameters
        ----------
        deco_type : Union[partial, str]
            The decorator class to add to this flow. If using a string, you cannot specify
            additional arguments as all argument will be parsed from the decorator
            specification.
        deco_args : List[Any], optional, default None
            Positional arguments to pass to the decorator.
        deco_kwargs : Dict[str, Any], optional, default None
            Keyword arguments to pass to the decorator.
        duplicates : int, default MutableFlow.IGNORE
            Instruction on how to handle duplicates. It can be one of:
            - `MutableFlow.IGNORE`: Ignore the decorator if it already exists.
            - `MutableFlow.ERROR`: Raise an error if the decorator already exists.
            - `MutableFlow.OVERRIDE`: Remove the existing decorator and add this one.
        """
        ...
    def remove_decorator(self, deco_name: str, deco_args: typing.Optional[typing.List[typing.Any]] = None, deco_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None) -> bool:
        """
        Remove a flow-level decorator. To remove a decorator, you can pass the decorator
        specification (obtained from `decorator_specs` for example).
        Note that if multiple decorators share the same decorator specification
        (very rare), they will all be removed.
        
        You can only remove decorators in the `pre_mutate` method.
        
        Parameters
        ----------
        deco_name : str
            Decorator specification of the decorator to remove. If nothing else is
            specified, all decorators matching that name will be removed.
        deco_args : List[Any], optional, default None
            Positional arguments to match the decorator specification.
        deco_kwargs : Dict[str, Any], optional, default None
            Keyword arguments to match the decorator specification.
        
        Returns
        -------
        bool
            Returns True if a decorator was removed.
        """
        ...
    def __getattr__(self, name):
        ...
    ...

