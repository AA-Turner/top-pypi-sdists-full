######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.31                                                                                #
# Generated on 2026-06-01T01:50:49.527003                                                            #
######################################################################################################

from __future__ import annotations

import typing
import metaflow
if typing.TYPE_CHECKING:
    import metaflow.flowspec
    import metaflow.user_decorators.mutable_step
    import typing
    import metaflow.user_decorators.user_step_decorator
    import metaflow.decorators
    import metaflow.datastore.inputs

from ..exception import MetaflowException as MetaflowException
from ..user_configs.config_parameters import resolve_delayed_evaluator as resolve_delayed_evaluator
from ..user_configs.config_parameters import unpack_delayed_evaluator as unpack_delayed_evaluator
from .common import ClassPath_Trie as ClassPath_Trie

TYPE_CHECKING: bool

USER_SKIP_STEP: dict

class UserStepDecoratorMeta(type, metaclass=type):
    @staticmethod
    def __new__(mcs, name, bases, namespace, **_kwargs):
        ...
    def __str__(cls):
        ...
    @classmethod
    def all_decorators(mcs) -> typing.Dict[str, "UserStepDecoratorMeta"]:
        """
        Get all registered decorators using the minimally unique classpath name
        
        Returns
        -------
        Dict[str, UserStepDecoratorBase]
            A dictionary mapping decorator names to their classes.
        """
        ...
    @classmethod
    def get_decorator_by_name(mcs, decorator_name: str) -> typing.Union["UserStepDecoratorBase", "metaflow.decorators.Decorator", None]:
        """
        Get a decorator by its name.
        
        Parameters
        ----------
        decorator_name: str
            The name of the decorator to retrieve.
        
        Returns
        -------
        Optional[UserStepDecoratorBase]
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

class UserStepDecoratorBase(object, metaclass=UserStepDecoratorMeta):
    def __init__(self, *args, **kwargs):
        ...
    def __get__(self, instance, owner):
        ...
    def __call__(self, step: typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None], None] = None, **kwargs) -> typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None]]:
        ...
    def add_or_raise(self, step: typing.Union[typing.Callable[["metaflow.decorators.FlowSpecDerived"], None], typing.Callable[["metaflow.decorators.FlowSpecDerived", typing.Any], None]], statically_defined: bool, duplicates: int, inserted_by: typing.Union[str, None] = None):
        """
        Register this decorator on *step*.
        
        Returns
        -------
        Optional[UserStepDecoratorBase]
            ``self`` if the decorator was registered, ``None`` if a duplicate
            already existed and the *duplicates* policy suppressed the
            addition (IGNORE, or ERROR on a non-statically-defined step).
        """
        ...
    def __str__(self):
        ...
    @classmethod
    def extract_args_kwargs_from_decorator_spec(cls, deco_spec: str) -> typing.Tuple[typing.List[typing.Any], typing.Dict[str, typing.Any]]:
        ...
    @classmethod
    def parse_decorator_spec(cls, deco_spec: str) -> typing.Union["UserStepDecoratorBase", None]:
        ...
    def make_decorator_spec(self):
        ...
    def get_args_kwargs(self) -> typing.Tuple[typing.List[typing.Any], typing.Dict[str, typing.Any]]:
        """
        Get the arguments and keyword arguments of the decorator.
        
        Returns
        -------
        Tuple[List[Any], Dict[str, Any]]
            A tuple containing a list of arguments and a dictionary of keyword arguments.
        """
        ...
    def init(self, *args, **kwargs):
        ...
    def external_init(self):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

class UserStepDecorator(UserStepDecoratorBase, metaclass=UserStepDecoratorMeta):
    def init(self, *args, **kwargs):
        """
        Implement this method if your UserStepDecorator takes arguments. It replaces the
        __init__ method in traditional Python classes.
        
        
        As an example:
        ```
        class MyDecorator(UserStepDecorator):
            def init(self, *args, **kwargs):
                self.arg1 = kwargs.get("arg1", None)
                self.arg2 = kwargs.get("arg2", None)
                # Do something with the arguments
        ```
        
        can then be used as
        ```
        @MyDecorator(arg1=42, arg2=conf_expr("config.my_arg2"))
        @step
        def start(self):
            pass
        ```
        """
        ...
    def pre_step(self, step_name: str, flow: "metaflow.flowspec.FlowSpec", inputs: typing.Union["metaflow.datastore.inputs.Inputs", None] = None) -> typing.Union[typing.Callable[["metaflow.flowspec.FlowSpec", typing.Union[typing.Any, None]], typing.Any], None]:
        """
        Implement this method to perform any action prior to the execution of a step.
        
        It should return either None to execute anything wrapped by this step decorator
        as usual or a callable that will be called instead.
        
        Parameters
        ----------
        step_name: str
            The name of the step being decorated.
        flow: FlowSpec
            The flow object to which the step belongs.
        inputs: Optional[List[FlowSpec]]
            The inputs to the step being decorated. This is only provided for join steps
            and is None for all other steps.
        
        Returns
        -------
        Optional[Callable[FlowSpec, Optional[Any]]]
            An optional function to use instead of the wrapped step. Note that the function
            returned should match the signature of the step being wrapped (join steps
            take an additional "inputs" argument).
        """
        ...
    def post_step(self, step_name: str, flow: "metaflow.flowspec.FlowSpec", exception: typing.Union[Exception, None] = None) -> typing.Union[Exception, None, typing.Tuple[typing.Union[Exception, None], typing.Union[typing.Dict[str, typing.Any], None]]]:
        """
        Implement this method to perform any action after the execution of a step.
        
        If the step (or any code being wrapped by this decorator) raises an exception,
        it will be passed here and can either be caught (in which case the step will
        be considered as successful) or re-raised (in which case the entire step
        will be considered a failure unless another decorator catches the execption).
        
        Note that this method executes *before* artifacts are stored in the datastore
        so it is able to modify, add or remove artifacts from `flow`.
        
        Parameters
        ----------
        step_name: str
            The name of the step being decorated.
        flow: FlowSpec
            The flow object to which the step belongs.
        exception: Optional[Exception]
            The exception raised during the step execution, if any.
        
        Returns
        -------
        Optional[Union[Optional[Exception], Tuple[Optional[Exception], Optional[Dict[str, Any]]]]]
            An exception (if None, the step is considered successful)
            OR
            A tuple containing:
              - An exception to be raised (if None, the step is considered successful).
              - A dictionary with values to pass to `self.next()`. If an empty dictionary
                is returned, the default arguments to `self.next()` for this step will be
                used. Return None if you do not want to call `self.next()` at all
                (this is typically the case as the step will call it itself).
        Note that returning None will gobble the exception.
        """
        ...
    @property
    def skip_step(self) -> typing.Union[bool, typing.Dict[str, typing.Any]]:
        """
        Returns whether or not the step (or rather anything wrapped by this decorator)
        should be skipped
        
        Returns
        -------
        Union[bool, Dict[str, Any]]
            False if the step should not be skipped. True if it should be skipped and
            a dictionary if it should be skipped and the values passed in used as
            the arguments to the self.next call.
        """
        ...
    @skip_step.setter
    def skip_step(self, value: typing.Union[bool, typing.Dict[str, typing.Any]]):
        """
        Set the skip_step property. You can set it to:
          - True to skip the step
          - False to not skip the step (default)
          - A dictionary with the keys valid in the `self.next` call.
        
        Parameters
        ----------
        value: Union[bool, Dict[str, Any]]
            True/False or a dictionary with the keys valid in the `self.next` call.
        """
        ...
    ...

def user_step_decorator(*args, **kwargs):
    """
    Use this decorator to transform a generator function into a user step decorator.
    
    As an example:
    
    ```
    @user_step_decorator
    def timing(step_name, flow, inputs, attributes):
        start_time = time.time()
        yield
        end_time = time.time()
        flow.artifact_total_time = end_time - start_time
        print(f"Step {step_name} took {flow.artifact_total_time} seconds")
    ```
    which can then be used as:
    
    ```
    @timing
    @step
    def start(self):
        print("Hello, world!")
    ```
    
    Your generator should:
      - take 3 or 4 arguments: step_name, flow, inputs, and attributes (optional)
        - step_name: the name of the step
        - flow: the flow object
        - inputs: the inputs to the step
        - attributes: the kwargs passed in when initializing the decorator. In the
          example above, something like `@timing(arg1="foo", arg2=42)` would make
          `attributes = {"arg1": "foo", "arg2": 42}`. If you choose to pass arguments
          to the decorator when you apply it to the step, your function *must* take
          4 arguments (step_name, flow, inputs, attributes).
      - yield at most once -- if you do not yield, the step will not execute.
      - yield:
          - None
          - a callable that will replace whatever is being wrapped (it
            should have the same parameters as the wrapped function, namely, it should
            be a
            Callable[[FlowSpec, Inputs], Optional[Union[Dict[str, Any], bool]]]).
            Note that the return type is a bit different -- you can return:
              - None or False: no special behavior, your callable called `self.next()` as
                usual.
              - A dictionary containing parameters for `self.next()`.
              - True to instruct Metaflow to call the `self.next()` statement that
                would have been called normally by the step function you replaced.
          - a dictionary to skip the step. An empty dictionary is equivalent
            to just skipping the step. A full dictionary will pass the arguments
            to the `self.next()` call -- this allows you to modify the behavior
            of `self.next` (for example, changing the `foreach` values. We provide
            USER_SKIP_STEP as a special value that is equivalent to {}.
    
    
    You are able to catch exceptions thrown by the yield statement (ie: coming from the
    wrapped code). Catching and not re-raising the exception will make the step
    successful.
    
    Note that you are able to modify the step's artifact after the yield.
    
    For more complex use cases, you can use the `UserStepDecorator` class directly which
    allows more control.
    """
    ...

class StepMutator(UserStepDecoratorBase, metaclass=UserStepDecoratorMeta):
    """
    Derive from this class to implement a step mutator.
    
    A step mutator allows you to introspect a step and add decorators to it. You can
    use values available through configurations to determine how to mutate the step.
    
    There are two main methods provided:
      - pre_mutate: called as early as possible right after configuration values are read.
      - mutate: called right after all the command line is parsed but before any
        Metaflow decorators are applied.
    """
    def init(self, *args, **kwargs):
        """
        Implement this method if you wish for your StepMutator to take in arguments.
        
        Your step-mutator can then look like:
        
        @MyMutator(arg1, arg2)
        @step
        def my_step(self):
            pass
        
        It is an error to use your mutator with arguments but not implement this method.
        """
        ...
    def pre_mutate(self, mutable_step: "metaflow.user_decorators.mutable_step.MutableStep"):
        """
        Method called right after all configuration values are read.
        
        Parameters
        ----------
        mutable_step : metaflow.user_decorators.mutable_step.MutableStep
            A representation of this step
        """
        ...
    def mutate(self, mutable_step: "metaflow.user_decorators.mutable_step.MutableStep"):
        """
        Method called right before the first Metaflow decorator is applied. This
        means that the command line, including all `--with` options has been parsed.
        
        Parameters
        ----------
        mutable_step : metaflow.user_decorators.mutable_step.MutableStep
            A representation of this step
        """
        ...
    def add_to_package(self):
        """
        Called to add custom files needed by this step mutator. This hook will be
        called in the `MetaflowPackage` class where metaflow compiles the code package
        tarball. This hook can return one of two things (the first is for backwards
        compatibility -- move to the second):
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

