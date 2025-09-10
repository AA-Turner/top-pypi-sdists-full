######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.3.2+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-09T09:20:35.509255                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.flowspec
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.user_decorators.mutable_flow
    import metaflow.decorators

from ..exception import MetaflowException as MetaflowException
from ..user_configs.config_parameters import resolve_delayed_evaluator as resolve_delayed_evaluator
from ..user_configs.config_parameters import unpack_delayed_evaluator as unpack_delayed_evaluator
from .common import ClassPath_Trie as ClassPath_Trie

TYPE_CHECKING: bool

class FlowMutatorMeta(type, metaclass=type):
    @staticmethod
    def __new__(mcs, name, bases, namespace):
        ...
    @classmethod
    def all_decorators(mcs) -> typing.Dict[str, "FlowMutatorMeta"]:
        ...
    def __str__(cls):
        ...
    @classmethod
    def get_decorator_by_name(mcs, decorator_name: str) -> typing.Union["FlowDecoratorMeta", "metaflow.decorators.Decorator", None]:
        """
        Get a decorator by its name.
        
        Parameters
        ----------
        decorator_name: str
            The name of the decorator to retrieve.
        
        Returns
        -------
        Optional[FlowDecoratorMeta]
            The decorator class if found, None otherwise.
        """
        ...
    @classmethod
    def get_decorator_name(mcs, decorator_type: type) -> typing.Optional[str]:
        """
        Get the minimally unique classpath name for a decorator type.
        
        Parameters
        ----------
        decorator_type: type
            The type of the decorator to retrieve the name for.
        
        Returns
        -------
        Optional[str]
            The minimally unique classpath name if found, None otherwise.
        """
        ...
    ...

class FlowMutator(object, metaclass=FlowMutatorMeta):
    """
    Derive from this class to implement a flow mutator.
    
    A flow mutator allows you to introspect a flow and its included steps. You can
    then add parameters, configurations and decorators to the flow as well as modify
    any of its steps.
    use values available through configurations to determine how to mutate the flow.
    
    There are two main methods provided:
      - pre_mutate: called as early as possible right after configuration values are read.
      - mutate: called right after all the command line is parsed but before any
        Metaflow decorators are applied.
    
    The `mutate` method does not allow you to modify the flow itself but you can still
    modify the steps.
    """
    def __init__(self, *args, **kwargs):
        ...
    def __mro_entries__(self, bases):
        ...
    def __call__(self, flow_spec: typing.Optional["metaflow.flowspec.FlowSpecMeta"] = None) -> "metaflow.flowspec.FlowSpecMeta":
        ...
    def __str__(self):
        ...
    def init(self, *args, **kwargs):
        """
        Implement this method if you wish for your FlowMutator to take in arguments.
        
        Your flow-mutator can then look like:
        
        @MyMutator(arg1, arg2)
        class MyFlow(FlowSpec):
            pass
        
        It is an error to use your mutator with arguments but not implement this method.
        """
        ...
    def external_init(self):
        ...
    def pre_mutate(self, mutable_flow: "metaflow.user_decorators.mutable_flow.MutableFlow"):
        """
        Method called right after all configuration values are read.
        
        Parameters
        ----------
        mutable_flow : metaflow.user_decorators.mutable_flow.MutableFlow
            A representation of this flow
        """
        ...
    def mutate(self, mutable_flow: "metaflow.user_decorators.mutable_flow.MutableFlow"):
        """
        Method called right before the first Metaflow step decorator is applied. This
        means that the command line, including all `--with` options has been parsed.
        
        Given how late this function is called, there are a few restrictions on what
        you can do; the following methods on MutableFlow are not allowed and calling
        them will result in an error:
          - add_parameter/remove_parameter
          - add_decorator/remove_decorator
        
        To call these methods, use the `pre_mutate` method instead.
        
        Parameters
        ----------
        mutable_flow : metaflow.user_decorators.mutable_flow.MutableFlow
            A representation of this flow
        """
        ...
    ...

