######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.7.5+obcheckpoint(0.2.7);ob(v1)                                                    #
# Generated on 2025-09-23T01:34:30.701066                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorator.mutable_flow
    import functools
    import metaflow.decorators
    import metaflow.flowspec
    import typing
    import metaflow.user_decorators.user_step_decorator

from ..exception import MetaflowException as MetaflowException
from .user_step_decorator import StepMutator as StepMutator
from .user_step_decorator import UserStepDecoratorBase as UserStepDecoratorBase

TYPE_CHECKING: bool

class MutableStep(object, metaclass=type):
    def __init__(self, flow_spec: "metaflow.flowspec.FlowSpec", step: typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None]], pre_mutate: bool = False, statically_defined: bool = False, inserted_by: typing.Optional[str] = None):
        ...
    @property
    def flow(self) -> "metaflow.user_decorator.mutable_flow.MutableFlow":
        """
        The flow that contains this step
        
        Returns
        -------
        MutableFlow
            The flow that contains this step
        """
        ...
    @property
    def decorator_specs(self) -> typing.Generator[typing.Tuple[str, str, typing.List[typing.Any], typing.Dict[str, typing.Any]], None, None]:
        """
        Iterate over all the decorator specifications of this step. Note that the same
        type of decorator may be present multiple times and no order is guaranteed.
        
        The returned tuple contains:
        - The decorator's name (shortest possible)
        - The decorator's fully qualified name (in the case of Metaflow decorators, this
          will indicate which extension the decorator comes from)
        - A list of positional arguments
        - A dictionary of keyword arguments
        
        You can use the resulting tuple to remove a decorator for example
        
        Yields
        ------
        str, str, List[Any], Dict[str, Any]
            A tuple containing the decorator name, it's fully qualified name,
            a list of positional arguments, and a dictionary of keyword arguments.
        """
        ...
    def add_decorator(self, deco_type: typing.Union[functools.partial, metaflow.user_decorators.user_step_decorator.UserStepDecoratorBase, str], deco_args: typing.Optional[typing.List[typing.Any]] = None, deco_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None, duplicates: int = 1):
        """
        Add a Metaflow step-decorator or a user step-decorator to a step.
        
        You can either add the decorator itself or its decorator specification for it
        (the same you would get back from decorator_specs). You can also mix and match
        but you cannot provide arguments both through the string and the
        deco_args/deco_kwargs.
        
        As an example:
        ```
        from metaflow import environment
        ...
        my_step.add_decorator(environment, deco_kwargs={"vars": {"foo": 42})}
        ```
        
        is equivalent to:
        ```
        my_step.add_decorator('environment:vars={"foo": 42}')
        ```
        
        is equivalent to:
        ```
        my_step.add_decorator('environment', deco_kwargs={"vars":{"foo": 42}})
        ```
        
        but this is not allowed:
        ```
        my_step.add_decorator('environment:vars={"bar" 43}', deco_kwargs={"vars":{"foo": 42}})
        ```
        
        Note in the case where you specify a
        string for the decorator, there is no need to import the decorator.
        
        The string syntax is useful to, for example, allow decorators to be stored as
        strings in a configuration file.
        
        You can only add StepMutators in the pre_mutate stage.
        
        In terms of precedence for decorators:
          - if a decorator can be applied multiple times (like `@card`) all decorators
            added are kept.
          - if `duplicates` is set to `MutableStep.IGNORE`, then the decorator
            being added is ignored (in other words, the existing decorator has precedence).
          - if `duplicates` is set to `MutableStep.OVERRIDE`, then the *existing*
            decorator is removed and this newly added one replaces it (in other
            words, the newly added decorator has precedence).
          - if `duplicates` is set to `MutableStep.ERROR`, then an error is raised but only
            if the newly added decorator is *static* (ie: defined directly in the code).
            If not, it is ignored.
        
        Parameters
        ----------
        deco_type : Union[partial, UserStepDecoratorBase, str]
            The decorator class to add to this step.
        deco_args : List[Any], optional, default None
            Positional arguments to pass to the decorator.
        deco_kwargs : Dict[str, Any], optional, default None
            Keyword arguments to pass to the decorator.
        duplicates : int, default MutableStep.IGNORE
            Instruction on how to handle duplicates. It can be one of:
            - `MutableStep.IGNORE`: Ignore the decorator if it already exists.
            - `MutableStep.ERROR`: Raise an error if the decorator already exists.
            - `MutableStep.OVERRIDE`: Remove the existing decorator and add this one.
        """
        ...
    def remove_decorator(self, deco_name: str, deco_args: typing.Optional[typing.List[typing.Any]] = None, deco_kwargs: typing.Optional[typing.Dict[str, typing.Any]] = None) -> bool:
        """
        Remove a step-level decorator. To remove a decorator, you can pass the decorator
        specification (obtained from `decorator_specs` for example).
        Note that if multiple decorators share the same decorator specification
        (very rare), they will all be removed.
        
        You can only remove StepMutators in the `pre_mutate` method.
        
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
    ...

