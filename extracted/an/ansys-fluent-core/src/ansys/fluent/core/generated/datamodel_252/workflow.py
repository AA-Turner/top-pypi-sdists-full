#
# This is an auto-generated file.  DO NOT EDIT!
#
# pylint: disable=line-too-long

from ansys.fluent.core.services.datamodel_se import (
    PyMenu,
    PyParameter,
    PyTextual,
    PyNumerical,
    PyDictionary,
    PyNamedObjectContainer,
    PyCommand,
    PyQuery,
    PyArguments,
    PyArgumentsTextualSubItem,
    PyArgumentsNumericalSubItem,
    PyArgumentsDictionarySubItem,
    PyArgumentsParameterSubItem,
    PyArgumentsSingletonSubItem
)


class Root(PyMenu):
    """
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.TaskObject = self.__class__.TaskObject(service, rules, path + [("TaskObject", "")])
        self.Workflow = self.__class__.Workflow(service, rules, path + [("Workflow", "")])
        self.CreateCompositeTask = self.__class__.CreateCompositeTask(service, rules, "CreateCompositeTask", path)
        self.CreateNewWorkflow = self.__class__.CreateNewWorkflow(service, rules, "CreateNewWorkflow", path)
        self.DeleteTasks = self.__class__.DeleteTasks(service, rules, "DeleteTasks", path)
        self.InitializeWorkflow = self.__class__.InitializeWorkflow(service, rules, "InitializeWorkflow", path)
        self.InsertNewTask = self.__class__.InsertNewTask(service, rules, "InsertNewTask", path)
        self.LoadState = self.__class__.LoadState(service, rules, "LoadState", path)
        self.LoadWorkflow = self.__class__.LoadWorkflow(service, rules, "LoadWorkflow", path)
        self.ResetWorkflow = self.__class__.ResetWorkflow(service, rules, "ResetWorkflow", path)
        self.SaveWorkflow = self.__class__.SaveWorkflow(service, rules, "SaveWorkflow", path)
        super().__init__(service, rules, path)

    class TaskObject(PyNamedObjectContainer):
        """
        .
        """
        class _TaskObject(PyMenu):
            """
            Singleton _TaskObject.
            """
            def __init__(self, service, rules, path):
                self.Arguments = self.__class__.Arguments(service, rules, path + [("Arguments", "")])
                self.CheckPoint = self.__class__.CheckPoint(service, rules, path + [("CheckPoint", "")])
                self.CommandName = self.__class__.CommandName(service, rules, path + [("CommandName", "")])
                self.Errors = self.__class__.Errors(service, rules, path + [("Errors", "")])
                self.InactiveTaskList = self.__class__.InactiveTaskList(service, rules, path + [("InactiveTaskList", "")])
                self.ObjectPath = self.__class__.ObjectPath(service, rules, path + [("ObjectPath", "")])
                self.State = self.__class__.State(service, rules, path + [("State", "")])
                self.TaskList = self.__class__.TaskList(service, rules, path + [("TaskList", "")])
                self.TaskType = self.__class__.TaskType(service, rules, path + [("TaskType", "")])
                self.Warnings = self.__class__.Warnings(service, rules, path + [("Warnings", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.AddChildAndUpdate = self.__class__.AddChildAndUpdate(service, rules, "AddChildAndUpdate", path)
                self.AddChildToTask = self.__class__.AddChildToTask(service, rules, "AddChildToTask", path)
                self.DisplayModel = self.__class__.DisplayModel(service, rules, "DisplayModel", path)
                self.Execute = self.__class__.Execute(service, rules, "Execute", path)
                self.ExecuteUpstreamNonExecutedAndThisTask = self.__class__.ExecuteUpstreamNonExecutedAndThisTask(service, rules, "ExecuteUpstreamNonExecutedAndThisTask", path)
                self.ForceUptoDate = self.__class__.ForceUptoDate(service, rules, "ForceUptoDate", path)
                self.GetNextPossibleTasks = self.__class__.GetNextPossibleTasks(service, rules, "GetNextPossibleTasks", path)
                self.InsertCompositeChildTask = self.__class__.InsertCompositeChildTask(service, rules, "InsertCompositeChildTask", path)
                self.InsertCompoundChildTask = self.__class__.InsertCompoundChildTask(service, rules, "InsertCompoundChildTask", path)
                self.InsertNextTask = self.__class__.InsertNextTask(service, rules, "InsertNextTask", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Revert = self.__class__.Revert(service, rules, "Revert", path)
                self.SetAsCurrent = self.__class__.SetAsCurrent(service, rules, "SetAsCurrent", path)
                self.UpdateChildTasks = self.__class__.UpdateChildTasks(service, rules, "UpdateChildTasks", path)
                super().__init__(service, rules, path)

            class Arguments(PyDictionary):
                """
                Parameter Arguments of value type dict[str, Any].
                """
                pass

            class CheckPoint(PyTextual):
                """
                Parameter CheckPoint of value type str.
                """
                pass

            class CommandName(PyTextual):
                """
                Parameter CommandName of value type str.
                """
                pass

            class Errors(PyTextual):
                """
                Parameter Errors of value type list[str].
                """
                pass

            class InactiveTaskList(PyTextual):
                """
                Parameter InactiveTaskList of value type list[str].
                """
                pass

            class ObjectPath(PyTextual):
                """
                Parameter ObjectPath of value type str.
                """
                pass

            class State(PyTextual):
                """
                Parameter State of value type str.
                """
                pass

            class TaskList(PyTextual):
                """
                Parameter TaskList of value type list[str].
                """
                pass

            class TaskType(PyTextual):
                """
                Parameter TaskType of value type str.
                """
                pass

            class Warnings(PyTextual):
                """
                Parameter Warnings of value type list[str].
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class AddChildAndUpdate(PyCommand):
                """
                Command AddChildAndUpdate.

                Parameters
                ----------
                DeferUpdate : bool
                Force : bool

                Returns
                -------
                bool
                """
                class _AddChildAndUpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.DeferUpdate = self._DeferUpdate(self, "DeferUpdate", service, rules, path)
                        self.Force = self._Force(self, "Force", service, rules, path)

                    class _DeferUpdate(PyArgumentsParameterSubItem):
                        """
                        Argument DeferUpdate.
                        """

                    class _Force(PyArgumentsParameterSubItem):
                        """
                        Argument Force.
                        """

                def create_instance(self) -> _AddChildAndUpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddChildAndUpdateArguments(*args)

            class AddChildToTask(PyCommand):
                """
                Command AddChildToTask.


                Returns
                -------
                bool
                """
                class _AddChildToTaskArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _AddChildToTaskArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddChildToTaskArguments(*args)

            class DisplayModel(PyCommand):
                """
                Command DisplayModel.


                Returns
                -------
                bool
                """
                class _DisplayModelArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DisplayModelArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DisplayModelArguments(*args)

            class Execute(PyCommand):
                """
                Command Execute.

                Parameters
                ----------
                Force : bool

                Returns
                -------
                bool
                """
                class _ExecuteArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Force = self._Force(self, "Force", service, rules, path)

                    class _Force(PyArgumentsParameterSubItem):
                        """
                        Argument Force.
                        """

                def create_instance(self) -> _ExecuteArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ExecuteArguments(*args)

            class ExecuteUpstreamNonExecutedAndThisTask(PyCommand):
                """
                Command ExecuteUpstreamNonExecutedAndThisTask.


                Returns
                -------
                bool
                """
                class _ExecuteUpstreamNonExecutedAndThisTaskArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ExecuteUpstreamNonExecutedAndThisTaskArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ExecuteUpstreamNonExecutedAndThisTaskArguments(*args)

            class ForceUptoDate(PyCommand):
                """
                Command ForceUptoDate.

                Parameters
                ----------
                Force : bool

                Returns
                -------
                bool
                """
                class _ForceUptoDateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Force = self._Force(self, "Force", service, rules, path)

                    class _Force(PyArgumentsParameterSubItem):
                        """
                        Argument Force.
                        """

                def create_instance(self) -> _ForceUptoDateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ForceUptoDateArguments(*args)

            class GetNextPossibleTasks(PyCommand):
                """
                Command GetNextPossibleTasks.


                Returns
                -------
                bool
                """
                class _GetNextPossibleTasksArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _GetNextPossibleTasksArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._GetNextPossibleTasksArguments(*args)

            class InsertCompositeChildTask(PyCommand):
                """
                Command InsertCompositeChildTask.

                Parameters
                ----------
                CommandName : str

                Returns
                -------
                bool
                """
                class _InsertCompositeChildTaskArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.CommandName = self._CommandName(self, "CommandName", service, rules, path)

                    class _CommandName(PyArgumentsTextualSubItem):
                        """
                        Argument CommandName.
                        """

                def create_instance(self) -> _InsertCompositeChildTaskArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._InsertCompositeChildTaskArguments(*args)

            class InsertCompoundChildTask(PyCommand):
                """
                Command InsertCompoundChildTask.


                Returns
                -------
                bool
                """
                class _InsertCompoundChildTaskArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _InsertCompoundChildTaskArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._InsertCompoundChildTaskArguments(*args)

            class InsertNextTask(PyCommand):
                """
                Command InsertNextTask.

                Parameters
                ----------
                CommandName : str
                Select : bool

                Returns
                -------
                bool
                """
                class _InsertNextTaskArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.CommandName = self._CommandName(self, "CommandName", service, rules, path)
                        self.Select = self._Select(self, "Select", service, rules, path)

                    class _CommandName(PyArgumentsTextualSubItem):
                        """
                        Argument CommandName.
                        """

                    class _Select(PyArgumentsParameterSubItem):
                        """
                        Argument Select.
                        """

                def create_instance(self) -> _InsertNextTaskArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._InsertNextTaskArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str

                Returns
                -------
                bool
                """
                class _RenameArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyArgumentsTextualSubItem):
                        """
                        Argument NewName.
                        """

                def create_instance(self) -> _RenameArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameArguments(*args)

            class Revert(PyCommand):
                """
                Command Revert.


                Returns
                -------
                bool
                """
                class _RevertArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _RevertArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RevertArguments(*args)

            class SetAsCurrent(PyCommand):
                """
                Command SetAsCurrent.


                Returns
                -------
                bool
                """
                class _SetAsCurrentArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _SetAsCurrentArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._SetAsCurrentArguments(*args)

            class UpdateChildTasks(PyCommand):
                """
                Command UpdateChildTasks.

                Parameters
                ----------
                SetupTypeChanged : bool
                Arguments : dict[str, Any]

                Returns
                -------
                bool
                """
                class _UpdateChildTasksArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.SetupTypeChanged = self._SetupTypeChanged(self, "SetupTypeChanged", service, rules, path)
                        self.Arguments = self._Arguments(self, "Arguments", service, rules, path)

                    class _SetupTypeChanged(PyArgumentsParameterSubItem):
                        """
                        Argument SetupTypeChanged.
                        """

                    class _Arguments(PyArgumentsDictionarySubItem):
                        """
                        Argument Arguments.
                        """

                def create_instance(self) -> _UpdateChildTasksArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateChildTasksArguments(*args)

        def __getitem__(self, key: str) -> _TaskObject:
            return super().__getitem__(key)

    class Workflow(PyMenu):
        """
        Singleton Workflow.
        """
        def __init__(self, service, rules, path):
            self.CurrentTask = self.__class__.CurrentTask(service, rules, path + [("CurrentTask", "")])
            self.InactiveTaskList = self.__class__.InactiveTaskList(service, rules, path + [("InactiveTaskList", "")])
            self.TaskList = self.__class__.TaskList(service, rules, path + [("TaskList", "")])
            self.WorkflowType = self.__class__.WorkflowType(service, rules, path + [("WorkflowType", "")])
            super().__init__(service, rules, path)

        class CurrentTask(PyTextual):
            """
            Parameter CurrentTask of value type str.
            """
            pass

        class InactiveTaskList(PyTextual):
            """
            Parameter InactiveTaskList of value type list[str].
            """
            pass

        class TaskList(PyTextual):
            """
            Parameter TaskList of value type list[str].
            """
            pass

        class WorkflowType(PyTextual):
            """
            Parameter WorkflowType of value type str.
            """
            pass

    class CreateCompositeTask(PyCommand):
        """
        Command CreateCompositeTask.

        Parameters
        ----------
        ListOfTasks : list[str]

        Returns
        -------
        bool
        """
        class _CreateCompositeTaskArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ListOfTasks = self._ListOfTasks(self, "ListOfTasks", service, rules, path)

            class _ListOfTasks(PyArgumentsTextualSubItem):
                """
                Argument ListOfTasks.
                """

        def create_instance(self) -> _CreateCompositeTaskArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateCompositeTaskArguments(*args)

    class CreateNewWorkflow(PyCommand):
        """
        Command CreateNewWorkflow.


        Returns
        -------
        bool
        """
        class _CreateNewWorkflowArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CreateNewWorkflowArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateNewWorkflowArguments(*args)

    class DeleteTasks(PyCommand):
        """
        Command DeleteTasks.

        Parameters
        ----------
        ListOfTasks : list[str]

        Returns
        -------
        bool
        """
        class _DeleteTasksArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ListOfTasks = self._ListOfTasks(self, "ListOfTasks", service, rules, path)

            class _ListOfTasks(PyArgumentsTextualSubItem):
                """
                Argument ListOfTasks.
                """

        def create_instance(self) -> _DeleteTasksArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DeleteTasksArguments(*args)

    class InitializeWorkflow(PyCommand):
        """
        Command InitializeWorkflow.

        Parameters
        ----------
        WorkflowType : str

        Returns
        -------
        bool
        """
        class _InitializeWorkflowArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.WorkflowType = self._WorkflowType(self, "WorkflowType", service, rules, path)

            class _WorkflowType(PyArgumentsTextualSubItem):
                """
                Argument WorkflowType.
                """

        def create_instance(self) -> _InitializeWorkflowArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._InitializeWorkflowArguments(*args)

    class InsertNewTask(PyCommand):
        """
        Command InsertNewTask.

        Parameters
        ----------
        CommandName : str

        Returns
        -------
        bool
        """
        class _InsertNewTaskArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.CommandName = self._CommandName(self, "CommandName", service, rules, path)

            class _CommandName(PyArgumentsTextualSubItem):
                """
                Argument CommandName.
                """

        def create_instance(self) -> _InsertNewTaskArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._InsertNewTaskArguments(*args)

    class LoadState(PyCommand):
        """
        Command LoadState.

        Parameters
        ----------
        ListOfRoots : list[str]

        Returns
        -------
        bool
        """
        class _LoadStateArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ListOfRoots = self._ListOfRoots(self, "ListOfRoots", service, rules, path)

            class _ListOfRoots(PyArgumentsTextualSubItem):
                """
                Argument ListOfRoots.
                """

        def create_instance(self) -> _LoadStateArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadStateArguments(*args)

    class LoadWorkflow(PyCommand):
        """
        Command LoadWorkflow.

        Parameters
        ----------
        FilePath : str

        Returns
        -------
        bool
        """
        class _LoadWorkflowArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

        def create_instance(self) -> _LoadWorkflowArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadWorkflowArguments(*args)

    class ResetWorkflow(PyCommand):
        """
        Command ResetWorkflow.


        Returns
        -------
        bool
        """
        class _ResetWorkflowArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _ResetWorkflowArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ResetWorkflowArguments(*args)

    class SaveWorkflow(PyCommand):
        """
        Command SaveWorkflow.

        Parameters
        ----------
        FilePath : str

        Returns
        -------
        bool
        """
        class _SaveWorkflowArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

        def create_instance(self) -> _SaveWorkflowArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SaveWorkflowArguments(*args)

