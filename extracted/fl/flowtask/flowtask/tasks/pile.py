"""
TaskPîle.
"""
from numbers import Number
from typing import Any
from collections.abc import Callable
from functools import partial
import networkx as nx
from navconfig.logging import logging
from ..components import getComponent, GroupComponent
from ..exceptions import TaskDefinition, ComponentError

logging.getLogger("matplotlib").setLevel(logging.CRITICAL)
logging.getLogger("PIL").setLevel(logging.CRITICAL)


class Step:
    """Step.

    Step is the basic component of a Task.
    """

    def __init__(
        self, step_name: str, step_id: int, params: dict, program: str = None
    ) -> None:
        try:
            self._component = getComponent(step_name, program=program)
        except Exception as e:
            logging.exception(e, stack_info=False)
            raise ComponentError(
                f"Step Error: Unable to load Component {step_name}: {e}"
            ) from e
        self.step_id = f"{step_name}_{step_id}"
        self.step_name = step_name
        self.params = params
        self.job: Callable = None
        self.depends: list = params.get('depends', [])
        self.branch: dict = params.get("branch", {})

    def get_depends(self, previous) -> Any:
        if not self.depends:
            return previous
        else:
            return self.depends

    def __str__(self) -> str:
        return f"<{self.step_id}>: {self.params!r}"

    def __repr__(self) -> str:
        return f"<{self.step_id}>: {self.params!r}"

    @property
    def name(self):
        return self.step_id

    @property
    def component(self):
        return self._component


class GroupStep(Step):
    def __init__(
        self, step_name: str, step_id: int, params: dict, program: str = None
    ) -> None:
        try:
            self._component = GroupComponent
        except Exception as e:
            logging.exception(e, stack_info=False)
            raise ComponentError(
                f"Step Error: Unable to load Group Component {step_name}: {e}"
            ) from e
        self.step_idx = step_id
        self.step_id = f"{step_name}_{step_id}"
        self.step_name = step_name
        self.params = params
        self.job: Callable = None
        self.depends: list = []
        self._steps: list = []
        try:
            self.depends = params["depends"]
        except KeyError:
            pass

    def add_step(self, step) -> None:
        self._steps.append(step)

    @property
    def component(self):
        return partial(self._component, component_list=self._steps)

    @property
    def steps(self):
        return self._steps


class TaskPile:
    """
    TaskPile is responsible for parsing a task definition (in JSON/YAML/TOML format)
    and converting it into a sequence of components, constructing a dependency graph
    for orderly execution.

    This class manages the following:

    - Parsing a task, which consists of multiple steps, each step representing a component
      that performs a specific action (e.g., data transformation, database query).
    - Creating a directed acyclic graph (DAG) to represent the dependencies between the
      components, ensuring that each component is executed in the correct order.
    - Handling grouping of components, where a group can contain multiple steps, providing
      a way to organize related tasks.
    - Verifying the task's structure to ensure that it forms a valid DAG, raising an error
      if any circular dependencies are detected.

    Attributes:
    ----------
    task : dict
        The task definition containing details of all steps.
    program : str, optional
        The name of the program associated with the task, used to define context.
    _size : int
        The total number of steps in the task.
    _graph : networkx.DiGraph
        A directed graph representing the dependencies between task steps.
    _task : list
        A list storing components of the task in the order of execution.
    _groups : dict
        A dictionary to manage groups of steps, allowing for easier organization and reuse.

    Methods:
    -------
    build():
        Compiles the task steps into a sequence of components and creates the dependency graph.
    """

    def __init__(self, task: dict, program: str = None):
        self._size: int = 0
        self._n = 0
        self.task: dict = task
        self._task: list = []  # List of Steps components
        self.__name__ = self.task["name"]
        self._program: str = program
        self._groups: dict = {}
        try:
            self._steps: list = task["steps"]
        except KeyError as e:
            raise TaskDefinition("Task Error: This task has no Steps.") from e
        self._step = None
        self._graph = nx.DiGraph(task=self.__name__)  # creates an empty Graph
        self.build()

    def _build_group(self, group: GroupStep, group_name: str, counter: int, params: dict):
        """Builds the group of steps.

        """
        # Iterate through self._steps to find all steps with the matching "Group" name
        new_count = 1
        for j, inner_step in enumerate(self._steps):
            if j in self._added_to_group:
                continue  # Skip if this step is already added to another group
            for step_name, step_params in inner_step.items():
                if step_params.get("Group") == group_name:
                    # create the step:
                    sp = Step(
                        step_name,
                        f"{counter}_{new_count}",
                        step_params,
                        program=self._program
                    )
                    # add the step to the group:
                    group.add_step(sp)
                    # Mark this step as processed
                    self._added_to_group.add(j)
                    new_count += 1
        # When group is filled, added to the task:
        if not group.steps:  # Check if no steps were added to the group
            raise ValueError(
                f"Task Error: Group '{group_name}' was defined but has no matching steps."
            )
        self._groups[group_name] = group
        s = {"task_id": f"{group_name}_{counter}", "step": group}
        self._graph.add_node(group.name, attrs=params)
        self._task.append(s)

    def build(self):
        counter = 1
        # Set to keep track of steps already processed in a group
        self._added_to_group = set()
        next_component = None

        for i, step in enumerate(self._steps):
            for step_name, params in step.items():
                # Skip if this step has already been added to a group
                if i in self._added_to_group:
                    continue

                # Handle branching if the previous component provided a branch
                if next_component and step_name != next_component:
                    continue

                # Reset branching after processing the step
                next_component = None

                # Check if this step is a Parent Group:
                if "to_group" in params:
                    # Create the Group:
                    group_name = params["to_group"]

                    # Step 1: Add the parent component (like PandasIterator) to the task
                    try:
                        cp = Step(step_name, counter, params, program=self._program)
                        s = {"task_id": f"{step_name}_{counter}", "step": cp}
                        self._graph.add_node(cp.name, attrs=params)
                        self._task.append(s)
                        counter += 1
                    except Exception as e:
                        raise ComponentError(
                            f"Task Error: Error loading Component: {e}"
                        ) from e

                    # Step 2: Check if Group Task already exists
                    if group_name in self._groups:  # already exists:
                        raise ValueError(
                            f"Task Error: Group '{group_name}' defined in step '{step_name}' already exists."
                        )
                    # Step 3: Creating the Group
                    gs = GroupStep(
                        group_name, counter, params={}, program=self._program
                    )
                    # Step 4: Build the Group
                    self._build_group(gs, group_name, counter, params)
                    # Move to the next step after processing the group
                    counter += 1
                    continue
                try:
                    cp = Step(
                        step_name,
                        counter,
                        params,
                        program=self._program
                    )
                    s = {"task_id": f"{step_name}_{counter}", "step": cp}
                except Exception as e:
                    raise ComponentError(
                        f"Task Error: Error loading Component: {e}"
                    ) from e
                counter += 1
                prev = None
                try:
                    prev = self._task[-1]
                except IndexError:
                    pass
                self._graph.add_node(cp.name, attrs=params)
                self._task.append(s)
                # calculate dependencies:
                depends = cp.get_depends(prev)
                if isinstance(depends, dict):
                    self._graph.add_edge(depends["task_id"], cp.name)
                elif isinstance(depends, list):
                    # TODO: making calculation of edges.
                    pass
        # size of the Pile of Components
        self._size = len(self._task)
        # check if Task is a DAG:
        if nx.is_directed_acyclic_graph(self._graph) is False:
            raise TaskDefinition(
                "Task Error: This task is not an Acyclic Graph."
            )

    def __len__(self):
        return len(self._steps)

    def __del__(self):
        del self._steps

    # Iterators:
    def __iter__(self):
        self._n = 0
        self._step = self._task[0]["step"]
        return self

    def __next__(self):
        if self._n < self._size:
            try:
                result = self._task[self._n]["step"]
            except IndexError as e:
                raise StopIteration from e
            self._step = result
            self._n += 1
            return self
        else:
            self._step = None
            raise StopIteration

    # Get properties of the Step
    @property
    def name(self):
        return self._step.name

    @property
    def component(self):
        return self._step.component

    @property
    def step(self):
        return self._step.step_name

    def params(self):
        return self._step.params

    ## Component Properties
    def getStepByID(self, task_id):
        return self._task[task_id]

    def delStep(self, task_id):
        del self._task[task_id]

    def delStepByName(self, name):
        for i, obj in enumerate(self._task):
            if obj.get("task_id") == name:
                del self._task[i]
                break

    def getStep(self, name):
        obj = next((item for item in self._task if item["task_id"] == name), None)
        if obj:
            self._step = obj
            return self

    def getStepByName(self, name):
        idx = next(
            (i for i, item in enumerate(self._task) if item["task_id"] == name), None
        )
        if idx != -1:
            self._step = self._task[idx]["step"]
            return [self, idx]

    def goto(self, name: str) -> bool:
        """
        Jump to a specific component by task_id or step_name index.
        To maintain DAG constraints, only forward jumps are permitted.
        """
        # Search by task_id first, then fallback to step_name
        idx = next(
            (i for i, item in enumerate(self._task) if item["task_id"] == name), None
        )
        if idx is None:
            # Fallback to searching by step_name alone
            idx = next(
                (i for i, item in enumerate(self._task) if item["step"].step_name == name), None
            )

        if idx is not None:
            # We enforce forward jumping
            if idx >= self._n:
                self._n = idx
                if self._n < len(self._task):
                    self._step = self._task[idx]["step"]
                return True
            else:
                from ..exceptions import TaskError
                raise TaskError(
                    f"Flowtask DAG Rule Violation: Cannot jump backwards to Component '{name}'"
                )
        else:
            from ..exceptions import TaskError
            raise TaskError(
                f"TaskPile Error: Target Component '{name}' for Goto/OnError not found in DAG"
            )

    def nextStep(self, name):
        idx = next(
            (i for i, item in enumerate(self._task) if item["task_id"] == name), None
        )
        if idx != -1:
            i = idx + 1
            self._step = self._task[i]["step"]
            return [self, i]

    def popStep(self, name, n: int = 1):
        idx = next(
            (i for i, item in enumerate(self._task) if item["task_id"] == name), None
        )
        if idx is not None and idx + (1 + n) < len(self._task):
            i = idx + (1 + n)
            removed_element = self._task.pop(i)
            return [removed_element["step"], i]
        return None

    def setStep(self, step):
        self._step.job = step

    def getDepends(self, previous=None):
        depends = self._step.depends
        if not depends:
            return previous
        else:
            if isinstance(depends, Number):
                try:
                    obj = self._task[depends]
                    return obj["job"]
                except (KeyError, IndexError):
                    task = self._step["task"]
                    logging.error(
                        f"Task Error: invalid Step index {depends} on task name {task}"
                    )
                    return None
            elif isinstance(depends, list):
                # list of depends
                obj = []
                for d in depends:
                    o = next(
                        (item for item in self._task if item["task_id"] == d), None
                    )
                    if o:
                        component = o["step"]
                        obj.append(component.job)
                return obj
            else:
                # is a string, this is the task id
                obj = next(
                    (item for item in self._task if item["task_id"] == depends), None
                )
                if obj:
                    component = obj["step"]
                    return component.job

    def plot_task(self, filename: str = None):
        import matplotlib.pyplot as plt  # lazy: only needed for visualization
        plt.figure(figsize=(24, 16))

        # Use the spring layout with modified parameters for better distribution
        pos = nx.spring_layout(
            self._graph,
            k=1.2,
            iterations=100
        )

        first_node = self._task[0]["task_id"]

        # Draw the first node (starting point) with special attributes
        nx.draw_networkx_nodes(
            self._graph,
            pos,
            nodelist=[first_node],
            node_color='blue',
            node_size=1200,  # Increase the size of the first node
            edgecolors='black',
            linewidths=2
        )

        # Draw the rest of the nodes (other steps)
        other_nodes = [n for n in self._graph.nodes() if n != first_node]
        nx.draw_networkx_nodes(
            self._graph,
            pos,
            nodelist=other_nodes,
            node_color='lightblue',
            node_size=800,
            edgecolors='black',
            linewidths=1.5
        )

        # Draw the edges between the nodes with improved thickness and arrow size
        nx.draw_networkx_edges(
            self._graph,
            pos,
            edgelist=self._graph.edges(),
            width=2,  # Make the edges thicker
            arrowstyle='-|>',  # Change arrow style
            arrowsize=25,  # Increase the size of arrows
            edge_color='gray'
        )

        # Draw labels for the nodes
        nx.draw_networkx_labels(
            self._graph,
            pos,
            labels={n: n for n in self._graph.nodes()},
            font_size=12,  # Slightly increase font size
            font_color='black'
        )

        # Add title for the task graph
        plt.title(
            f"Task Workflow: {self.__name__}",
            fontsize=18
        )

        # Save the graph to a file
        if not filename:
            filename = f"task_{self.__name__}.png"
        plt.savefig(filename, format="PNG", dpi=300)
        plt.clf()

    @staticmethod
    def from_task_pile(
        task_pile: list,
        name: str = "Generated TaskPile",
        program: str = None
    ) -> "TaskPile":
        """
        Creates a TaskPile instance from a pre-defined task_pile list.

        Args:
            task_pile (list): A list of dictionaries, each representing a task with `task_id` and `step`.
            name (str): Name for the generated task pile. Defaults to "Generated TaskPile".
            program (str): Optional program context for the task pile.

        Returns:
            TaskPile: An instance of the TaskPile class.
        """
        task = {
            "name": name,
            "steps": [
                {step["step"]: {"task_id": step["task_id"]}}
                for step in task_pile
            ]
        }
        return TaskPile(task, program=program)
