######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.864897                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import functools
    import metaflow.parameters
    import metaflow.decorators
    import metaflow.flowspec
    import metaflow.user_configs.config_parameters
    import metaflow.user_configs.config_decorators
    import typing

from ..exception import MetaflowException as MetaflowException
from .config_parameters import ConfigValue as ConfigValue
from .config_parameters import resolve_delayed_evaluator as resolve_delayed_evaluator

TYPE_CHECKING: bool

class MutableStep(object, metaclass=type):
    """
    A MutableStep is a wrapper passed to the `CustomStepDecorator`'s `evaluate` method
    to allow the decorator to interact with the step and providing easy methods to
    modify the behavior of the step.
    """
    def __init__(self, flow_spec: "metaflow.flowspec.FlowSpec", step: typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None]]):
        ...
    @property
    def flow(self) -> MutableFlow:
        """
        The flow that contains this step
        
        Returns
        -------
        MutableFlow
            The flow that contains this step
        """
        ...
    @property
    def decorators(self) -> typing.Generator["metaflow.decorators.StepDecorator", None, None]:
        """
        Iterate over all the decorators of this step. Note that the same type of decorator
        may be present multiple times and no order is guaranteed.
        
        Yields
        ------
        metaflow.decorators.StepDecorator
            A decorator of the step
        """
        ...
    def add_decorator(self, deco_type: functools.partial, **kwargs):
        """
        Add a Metaflow decorator to a step.
        
        Parameters
        ----------
        deco_type : partial
            The decorator class to add to this step
        """
        ...
    def remove_decorator(self, deco_name: str, all: bool = True, **kwargs) -> bool:
        """
        Remove one or more Metaflow decorators from a step.
        
        Some decorators can be applied multiple times to a step. This method allows you
        to choose which decorator to remove or just remove all of them or one of them.
        
        Parameters
        ----------
        deco_name : str
            Name of the decorator to remove
        all : bool, default True
            If True, remove all instances of the decorator that match the filters
            passed using kwargs (or all the instances of the decorator if no filters are
            passed). If False, removes only the first found instance of the decorator.
        
        Returns
        -------
        bool
            Returns True if at least one decorator was removed.
        """
        ...
    ...

class MutableFlow(object, metaclass=type):
    def __init__(self, flow_spec: "metaflow.flowspec.FlowSpec"):
        ...
    @property
    def decorators(self) -> typing.Generator["metaflow.decorators.FlowDecorator", None, None]:
        """
        Iterate over all the decorators of this flow. Note that the same type of decorator
        may be present multiple times and no order is guaranteed.
        
        Yields
        ------
        metaflow.decorators.FlowDecorator
            A decorator of the flow
        """
        ...
    @property
    def configs(self) -> typing.Generator[typing.Tuple[str, metaflow.user_configs.config_parameters.ConfigValue], None, None]:
        """
        Iterate over all user configurations in this flow
        
        Use this to parameterize your flow based on configuration. As an example, the
        `evaluate` method of your `CustomFlowDecorator` can use this to add an
        environment decorator.
        ```
        class MyDecorator(CustomFlowDecorator):
            def evaluate(flow: MutableFlow):
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
    def parameters(self) -> typing.Generator[typing.Tuple[str, typing.Any], None, None]:
        ...
    @property
    def steps(self) -> typing.Generator[typing.Tuple[str, metaflow.user_configs.config_decorators.MutableStep], None, None]:
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
        ...
    def remove_parameter(self, parameter_name: str) -> bool:
        """
        Remove a parameter from the flow.
        
        The name given should match the name of the parameter (can be different
        from the name of the parameter in the flow. You can not remove config parameters.
        
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
    def add_decorator(self, deco_type: functools.partial, **kwargs):
        """
        Add a Metaflow decorator to a flow.
        
        Parameters
        ----------
        deco_type : partial
            The decorator class to add to this flow
        """
        ...
    def remove_decorator(self, deco_name: str, all: bool = True, **kwargs) -> bool:
        """
        Remove one or more Metaflow decorators from a flow.
        
        Some decorators can be applied multiple times to a flow. This method allows you
        to choose which decorator to remove or just remove all of them or one of them.
        
        Parameters
        ----------
        deco_name : str
            Name of the decorator to remove
        all : bool, default True
            If True, remove all instances of the decorator that match the filters
            passed using kwargs (or all the instances of the decorator if no filters are
            passed). If False, removes only the first found instance of the decorator.
        
        Returns
        -------
        bool
            Returns True if at least one decorator was removed.
        """
        ...
    def __getattr__(self, name):
        ...
    ...

class CustomFlowDecorator(object, metaclass=type):
    def __init__(self, *args, **kwargs):
        ...
    def __call__(self, flow_spec: typing.Optional["metaflow.flowspec.FlowSpecMeta"] = None) -> "metaflow.flowspec.FlowSpecMeta":
        ...
    def init(self, *args, **kwargs):
        """
        This method is intended to be optionally overridden if you need to
        have an initializer.
        """
        ...
    def evaluate(self, mutable_flow: MutableFlow):
        """
        Implement this method to act on the flow and modify it as needed.
        
        Parameters
        ----------
        mutable_flow : MutableFlow
            Flow
        
        Raises
        ------
        NotImplementedError
            _description_
        """
        ...
    ...

class CustomStepDecorator(object, metaclass=type):
    def __init__(self, *args, **kwargs):
        ...
    def __get__(self, instance, owner):
        ...
    def __call__(self, step: typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None], None] = None) -> typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None]]:
        ...
    def init(self, *args, **kwargs):
        """
        This method is intended to be optionally overridden if you need to
        have an initializer.
        """
        ...
    def evaluate(self, mutable_step: MutableStep):
        ...
    ...

