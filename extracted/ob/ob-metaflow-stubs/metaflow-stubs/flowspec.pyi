######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.861582                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow.datastore.inputs
    import metaflow.flowspec
    import metaflow.unbounded_foreach
    import typing

from . import parameters as parameters
from .parameters import DelayedEvaluationParameter as DelayedEvaluationParameter
from .parameters import Parameter as Parameter
from .exception import MetaflowException as MetaflowException
from .exception import MissingInMergeArtifactsException as MissingInMergeArtifactsException
from .exception import MetaflowInternalError as MetaflowInternalError
from .exception import UnhandledInMergeArtifactsException as UnhandledInMergeArtifactsException
from .user_configs.config_parameters import ConfigValue as ConfigValue
from .user_configs.config_decorators import CustomFlowDecorator as CustomFlowDecorator
from .user_configs.config_decorators import CustomStepDecorator as CustomStepDecorator
from .user_configs.config_decorators import MutableFlow as MutableFlow
from .user_configs.config_decorators import MutableStep as MutableStep

TYPE_CHECKING: bool

INCLUDE_FOREACH_STACK: bool

MAXIMUM_FOREACH_VALUE_CHARS: int

INTERNAL_ARTIFACTS_SET: set

class InvalidNextException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class ParallelUBF(metaflow.unbounded_foreach.UnboundedForeachInput, metaclass=type):
    """
    Unbounded-for-each placeholder for supporting parallel (multi-node) steps.
    """
    def __init__(self, num_parallel):
        ...
    def __getitem__(self, item):
        ...
    ...

class FlowSpecMeta(type, metaclass=type):
    def __init__(cls, name, bases, attrs):
        ...
    ...

class FlowSpec(object, metaclass=FlowSpecMeta):
    """
    Main class from which all Flows should inherit.
    
    Attributes
    ----------
    index
    input
    """
    def __init__(self, use_cli = True):
        """
        Construct a FlowSpec
        
        Parameters
        ----------
        use_cli : bool, default True
            Set to True if the flow is invoked from __main__ or the command line
        """
        ...
    @property
    def script_name(self) -> str:
        """
        [Legacy function - do not use. Use `current` instead]
        
        Returns the name of the script containing the flow
        
        Returns
        -------
        str
            A string containing the name of the script
        """
        ...
    def __iter__(self):
        """
        [Legacy function - do not use]
        
        Iterate over all steps in the Flow
        
        Returns
        -------
        Iterator[graph.DAGNode]
            Iterator over the steps in the flow
        """
        ...
    def __getattr__(self, name: str):
        ...
    def cmd(self, cmdline, input = {}, output = []):
        """
        [Legacy function - do not use]
        """
        ...
    @property
    def index(self) -> typing.Optional[int]:
        """
        The index of this foreach branch.
        
        In a foreach step, multiple instances of this step (tasks) will be executed,
        one for each element in the foreach. This property returns the zero based index
        of the current task. If this is not a foreach step, this returns None.
        
        If you need to know the indices of the parent tasks in a nested foreach, use
        `FlowSpec.foreach_stack`.
        
        Returns
        -------
        int, optional
            Index of the task in a foreach step.
        """
        ...
    @property
    def input(self) -> typing.Optional[typing.Any]:
        """
        The value of the foreach artifact in this foreach branch.
        
        In a foreach step, multiple instances of this step (tasks) will be executed,
        one for each element in the foreach. This property returns the element passed
        to the current task. If this is not a foreach step, this returns None.
        
        If you need to know the values of the parent tasks in a nested foreach, use
        `FlowSpec.foreach_stack`.
        
        Returns
        -------
        object, optional
            Input passed to the foreach task.
        """
        ...
    def foreach_stack(self) -> typing.Optional[typing.List[typing.Tuple[int, int, typing.Any]]]:
        """
        Returns the current stack of foreach indexes and values for the current step.
        
        Use this information to understand what data is being processed in the current
        foreach branch. For example, considering the following code:
        ```
        @step
        def root(self):
            self.split_1 = ['a', 'b', 'c']
            self.next(self.nest_1, foreach='split_1')
        
        @step
        def nest_1(self):
            self.split_2 = ['d', 'e', 'f', 'g']
            self.next(self.nest_2, foreach='split_2'):
        
        @step
        def nest_2(self):
            foo = self.foreach_stack()
        ```
        
        `foo` will take the following values in the various tasks for nest_2:
        ```
            [(0, 3, 'a'), (0, 4, 'd')]
            [(0, 3, 'a'), (1, 4, 'e')]
            ...
            [(0, 3, 'a'), (3, 4, 'g')]
            [(1, 3, 'b'), (0, 4, 'd')]
            ...
        ```
        where each tuple corresponds to:
        
        - The index of the task for that level of the loop.
        - The number of splits for that level of the loop.
        - The value for that level of the loop.
        
        Note that the last tuple returned in a task corresponds to:
        
        - 1st element: value returned by `self.index`.
        - 3rd element: value returned by `self.input`.
        
        Returns
        -------
        List[Tuple[int, int, Any]]
            An array describing the current stack of foreach steps.
        """
        ...
    def merge_artifacts(self, inputs: metaflow.datastore.inputs.Inputs, exclude: typing.Optional[typing.List[str]] = None, include: typing.Optional[typing.List[str]] = None):
        """
        Helper function for merging artifacts in a join step.
        
        This function takes all the artifacts coming from the branches of a
        join point and assigns them to self in the calling step. Only artifacts
        not set in the current step are considered. If, for a given artifact, different
        values are present on the incoming edges, an error will be thrown and the artifacts
        that conflict will be reported.
        
        As a few examples, in the simple graph: A splitting into B and C and joining in D:
        ```
        A:
          self.x = 5
          self.y = 6
        B:
          self.b_var = 1
          self.x = from_b
        C:
          self.x = from_c
        
        D:
          merge_artifacts(inputs)
        ```
        In D, the following artifacts are set:
          - `y` (value: 6), `b_var` (value: 1)
          - if `from_b` and `from_c` are the same, `x` will be accessible and have value `from_b`
          - if `from_b` and `from_c` are different, an error will be thrown. To prevent this error,
            you need to manually set `self.x` in D to a merged value (for example the max) prior to
            calling `merge_artifacts`.
        
        Parameters
        ----------
        inputs : Inputs
            Incoming steps to the join point.
        exclude : List[str], optional, default None
            If specified, do not consider merging artifacts with a name in `exclude`.
            Cannot specify if `include` is also specified.
        include : List[str], optional, default None
            If specified, only merge artifacts specified. Cannot specify if `exclude` is
            also specified.
        
        Raises
        ------
        MetaflowException
            This exception is thrown if this is not called in a join step.
        UnhandledInMergeArtifactsException
            This exception is thrown in case of unresolved conflicts.
        MissingInMergeArtifactsException
            This exception is thrown in case an artifact specified in `include` cannot
            be found.
        """
        ...
    def next(self, *dsts: typing.Callable[..., None], **kwargs):
        """
        Indicates the next step to execute after this step has completed.
        
        This statement should appear as the last statement of each step, except
        the end step.
        
        There are several valid formats to specify the next step:
        
        - Straight-line connection: `self.next(self.next_step)` where `next_step` is a method in
          the current class decorated with the `@step` decorator.
        
        - Static fan-out connection: `self.next(self.step1, self.step2, ...)` where `stepX` are
          methods in the current class decorated with the `@step` decorator.
        
        - Foreach branch:
          ```
          self.next(self.foreach_step, foreach='foreach_iterator')
          ```
          In this situation, `foreach_step` is a method in the current class decorated with the
          `@step` decorator and `foreach_iterator` is a variable name in the current class that
          evaluates to an iterator. A task will be launched for each value in the iterator and
          each task will execute the code specified by the step `foreach_step`.
        
        Parameters
        ----------
        dsts : Callable[..., None]
            One or more methods annotated with `@step`.
        
        Raises
        ------
        InvalidNextException
            Raised if the format of the arguments does not match one of the ones given above.
        """
        ...
    def __str__(self):
        ...
    def __getstate__(self):
        ...
    ...

