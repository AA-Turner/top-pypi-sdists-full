######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.32.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-06-03T22:23:58.304868                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import typing
    import metaflow.decorators
    import metaflow.user_decorators.user_flow_decorator
    import metaflow.user_decorators.mutable_flow
    import metaflow.flowspec

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
    def get_decorator_name(mcs, decorator_type: type) -> typing.Union[str, None]:
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
    def __call__(self, flow_spec: typing.Union["metaflow.flowspec.FlowSpecMeta", None] = None) -> "metaflow.flowspec.FlowSpecMeta":
        ...
    def __str__(self):
        ...
    @classmethod
    def extract_args_kwargs_from_decorator_spec(cls, deco_spec: str) -> typing.Tuple[typing.List[typing.Any], typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def parse_decorator_spec(cls, deco_spec: str) -> "FlowMutator":
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
    def add_to_package(self):
        """
        Called to add custom files needed by this flow mutator. This hook will be
        called in the `MetaflowPackage` class where metaflow compiles the code package
        tarball. This hook can return one of two things (the first is for backwards
        compatibility -- generally use the second when you implement your mutator):
          - a generator yielding a tuple of `(file_path, arcname)` to add files to
            the code package. `file_path` is the path to the file on the local filesystem
            and `arcname` is the path relative to the packaged code.
          - a generator yielding a tuple of `(content, arcname, type)` where:
            - type is one of
            ContentType.{USER_CONTENT, CODE_CONTENT, MODULE_CONTENT, OTHER_CONTENT}
            - for USER_CONTENT:
              - the file will be included relative to the directory containing the
                user's flow file.
              - content: path to the file to include
              - arcname: path relative to the directory containing the user's flow file
            - for CODE_CONTENT:
              - the file will be included relative to the code directory in the package.
                This will be the directory containing `metaflow`.
              - content: path to the file to include
              - arcname: path relative to the code directory in the package
            - for MODULE_CONTENT:
              - the module will be added to the code package as a python module. It will
                be accessible as usual (import <module_name>)
              - content: name of the module
              - arcname: None (ignored)
            - for OTHER_CONTENT:
              - the file will be included relative to any other configuration/metadata
                files for the flow
              - content: path to the file to include
              - arcname: path relative to the config directory in the package
        """
        ...
    ...

