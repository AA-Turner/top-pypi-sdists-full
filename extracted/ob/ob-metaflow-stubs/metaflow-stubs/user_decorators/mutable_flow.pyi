######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.34.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-08-13T18:38:42.581920                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing
    import metaflow.user_configs.config_parameters
    import functools
    import metaflow.parameters
    import metaflow.flowspec
    import metaflow.user_decorators.mutable_step
    import metaflow.decorators
    import metaflow.user_decorators.user_flow_decorator

from ..exception import MetaflowException as MetaflowException
from ..user_configs.config_parameters import ConfigValue as ConfigValue

TYPE_CHECKING: bool

class MutableFlow(object, metaclass=type):
    def __init__(self, flow_spec: "metaflow.flowspec.FlowSpec", pre_mutate: bool = False, statically_defined: bool = False, inserted_by: typing.Union[str, None] = None):
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
            A tuple containing the decorator name, its fully qualified name,
            a list of positional arguments, and a dictionary of keyword arguments.
        """
        ...
    def has_decorator(self, name: str) -> bool:
        """
        Check whether this flow has at least one decorator with the given name.
        
        Parameters
        ----------
        name : str
            The decorator name (short) or fully qualified name (contains a period).
        """
        ...
    def get_decorator_specs(self, name: str) -> typing.List[typing.Tuple[str, str, typing.List[typing.Any], typing.Dict[str, typing.Any]]]:
        """
        Return all spec tuples matching the given name.
        
        Parameters
        ----------
        name : str
            The decorator name (short) or fully qualified name (contains a period).
        
        Returns
        -------
        List[Tuple[str, str, List[Any], Dict[str, Any]]]
            A list of (short_name, fq_name, args, kwargs) tuples. Empty list if
            no decorators match.
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
        
        If you want to access a particular configuration value, you can use the getattr
        method or simply <MutableFlow>.step_name.
        
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
        
        If you want to access a particular parameter, you can use the getattr method or
        simply <MutableFlow>.step_name.
        
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
        
        If you want to access a particular step, you can use the getattr method or simply
        <MutableFlow>.step_name.
        
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
    def add_decorator(self, deco_type: typing.Union[functools.partial, "metaflow.user_decorators.user_flow_decorator.FlowMutator", str], deco_args: typing.Union[typing.List[typing.Any], None] = None, deco_kwargs: typing.Union[typing.Dict[str, typing.Any], None] = None, duplicates: int = 1) -> typing.Union["metaflow.decorators.FlowDecorator", "metaflow.user_decorators.user_flow_decorator.FlowMutator", None]:
        """
        Add a Metaflow flow-decorator or a FlowMutator to a flow. You can only add
        decorators in the `pre_mutate` method.
        
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
        
        You can also add a FlowMutator class. The new FlowMutator will have its
        ``external_init()`` called immediately and its ``pre_mutate`` will be called after
        all previously existing FlowMutators have called pre-mutate.
        
        Parameters
        ----------
        deco_type : Union[partial, FlowMutator, str]
            The decorator class to add to this flow. Can be a FlowDecorator partial,
            a FlowMutator subclass, or a string decorator specification.
        deco_args : List[Any], optional, default None
            Positional arguments to pass to the decorator.
        deco_kwargs : Dict[str, Any], optional, default None
            Keyword arguments to pass to the decorator.
        duplicates : int, default MutableFlow.IGNORE
            Instruction on how to handle duplicates. It can be one of:
            - `MutableFlow.IGNORE`: Ignore the decorator if it already exists.
            - `MutableFlow.ERROR`: Raise an error if the decorator already exists.
            - `MutableFlow.OVERRIDE`: Remove the existing decorator and add this one.
        
        Returns
        -------
        Optional[Union[FlowDecorator, FlowMutator]]
            The decorator that was added or None if none was added due to duplicate handling.
        """
        ...
    def remove_decorator(self, deco_name: str, deco_args: typing.Union[typing.List[typing.Any], None] = None, deco_kwargs: typing.Union[typing.Dict[str, typing.Any], None] = None) -> bool:
        """
        Remove a flow-level decorator. To remove a decorator, you can pass the decorator
        specification (obtained from `decorator_specs` for example).
        Note that if multiple decorators share the same decorator specification
        (very rare), they will all be removed.
        
        FlowMutators cannot be removed because they are processed during iteration.
        Attempting to remove a FlowMutator will raise an error.
        
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

