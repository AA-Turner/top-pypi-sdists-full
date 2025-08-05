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
    PyCommandArguments,
    PyTextualCommandArgumentsSubItem,
    PyNumericalCommandArgumentsSubItem,
    PyDictionaryCommandArgumentsSubItem,
    PyParameterCommandArgumentsSubItem,
    PySingletonCommandArgumentsSubItem
)


class Root(PyMenu):
    """
    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
    """
    def __init__(self, service, rules, path):
        self.AssemblyNode = self.__class__.AssemblyNode(service, rules, path + [("AssemblyNode", "")])
        self.Mirror = self.__class__.Mirror(service, rules, path + [("Mirror", "")])
        self.Node = self.__class__.Node(service, rules, path + [("Node", "")])
        self.ObjectSetting = self.__class__.ObjectSetting(service, rules, path + [("ObjectSetting", "")])
        self.Refaceting = self.__class__.Refaceting(service, rules, path + [("Refaceting", "")])
        self.Rotate = self.__class__.Rotate(service, rules, path + [("Rotate", "")])
        self.RotateAboutAxis = self.__class__.RotateAboutAxis(service, rules, path + [("RotateAboutAxis", "")])
        self.Scaling = self.__class__.Scaling(service, rules, path + [("Scaling", "")])
        self.Transform = self.__class__.Transform(service, rules, path + [("Transform", "")])
        self.TransformBase = self.__class__.TransformBase(service, rules, path + [("TransformBase", "")])
        self.Translate = self.__class__.Translate(service, rules, path + [("Translate", "")])
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.MeshingOperations = self.__class__.MeshingOperations(service, rules, path + [("MeshingOperations", "")])
        self.ObjectSettingOperations = self.__class__.ObjectSettingOperations(service, rules, path + [("ObjectSettingOperations", "")])
        self.RefacetingOperations = self.__class__.RefacetingOperations(service, rules, path + [("RefacetingOperations", "")])
        self.TransformOperations = self.__class__.TransformOperations(service, rules, path + [("TransformOperations", "")])
        self.AppendFmdFiles = self.__class__.AppendFmdFiles(service, rules, "AppendFmdFiles", path)
        self.ChangeFileLengthUnit = self.__class__.ChangeFileLengthUnit(service, rules, "ChangeFileLengthUnit", path)
        self.ChangeLengthUnit = self.__class__.ChangeLengthUnit(service, rules, "ChangeLengthUnit", path)
        self.CreateObjForEachPart = self.__class__.CreateObjForEachPart(service, rules, "CreateObjForEachPart", path)
        self.CreateObjects = self.__class__.CreateObjects(service, rules, "CreateObjects", path)
        self.Delete = self.__class__.Delete(service, rules, "Delete", path)
        self.DeletePaths = self.__class__.DeletePaths(service, rules, "DeletePaths", path)
        self.InitializeTemplate = self.__class__.InitializeTemplate(service, rules, "InitializeTemplate", path)
        self.InputFileChanged = self.__class__.InputFileChanged(service, rules, "InputFileChanged", path)
        self.ListMeshingOperations = self.__class__.ListMeshingOperations(service, rules, "ListMeshingOperations", path)
        self.LoadFmdFile = self.__class__.LoadFmdFile(service, rules, "LoadFmdFile", path)
        self.LoadTemplate = self.__class__.LoadTemplate(service, rules, "LoadTemplate", path)
        self.MarkObjectsOutofDate = self.__class__.MarkObjectsOutofDate(service, rules, "MarkObjectsOutofDate", path)
        self.MoveCADComponentsToNewObject = self.__class__.MoveCADComponentsToNewObject(service, rules, "MoveCADComponentsToNewObject", path)
        self.MoveToNewSubobject = self.__class__.MoveToNewSubobject(service, rules, "MoveToNewSubobject", path)
        self.MoveToObject = self.__class__.MoveToObject(service, rules, "MoveToObject", path)
        self.RedoAllTransforms = self.__class__.RedoAllTransforms(service, rules, "RedoAllTransforms", path)
        self.ResetTemplate = self.__class__.ResetTemplate(service, rules, "ResetTemplate", path)
        self.SaveFmdFile = self.__class__.SaveFmdFile(service, rules, "SaveFmdFile", path)
        self.SaveTemplate = self.__class__.SaveTemplate(service, rules, "SaveTemplate", path)
        self.SuppressNodeObjects = self.__class__.SuppressNodeObjects(service, rules, "SuppressNodeObjects", path)
        self.UndoAllTransforms = self.__class__.UndoAllTransforms(service, rules, "UndoAllTransforms", path)
        super().__init__(service, rules, path)

    class AssemblyNode(PyNamedObjectContainer):
        """
        .
        """
        class _AssemblyNode(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Refaceting = self.__class__.Refaceting(service, rules, path + [("Refaceting", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.EdgeExtraction = self.__class__.EdgeExtraction(service, rules, path + [("EdgeExtraction", "")])
                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                self.IsChildrenSettingsChanged = self.__class__.IsChildrenSettingsChanged(service, rules, path + [("IsChildrenSettingsChanged", "")])
                self.KeyId = self.__class__.KeyId(service, rules, path + [("KeyId", "")])
                self.MergeChildren = self.__class__.MergeChildren(service, rules, path + [("MergeChildren", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.OneZonePer = self.__class__.OneZonePer(service, rules, path + [("OneZonePer", "")])
                self.Parent = self.__class__.Parent(service, rules, path + [("Parent", "")])
                self.PrefixObjectName = self.__class__.PrefixObjectName(service, rules, path + [("PrefixObjectName", "")])
                self.RefacetOperation = self.__class__.RefacetOperation(service, rules, path + [("RefacetOperation", "")])
                self.Transformations = self.__class__.Transformations(service, rules, path + [("Transformations", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.ChangeChildrenSettings = self.__class__.ChangeChildrenSettings(service, rules, "ChangeChildrenSettings", path)
                self.Copy = self.__class__.Copy(service, rules, "Copy", path)
                self.CreateChild = self.__class__.CreateChild(service, rules, "CreateChild", path)
                self.Move = self.__class__.Move(service, rules, "Move", path)
                self.ReFacet = self.__class__.ReFacet(service, rules, "ReFacet", path)
                self.ReFacetNow = self.__class__.ReFacetNow(service, rules, "ReFacetNow", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                super().__init__(service, rules, path)

            class Refaceting(PyMenu):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                def __init__(self, service, rules, path):
                    self.Deviation = self.__class__.Deviation(service, rules, path + [("Deviation", "")])
                    self.MaxSize = self.__class__.MaxSize(service, rules, path + [("MaxSize", "")])
                    self.NormalAngle = self.__class__.NormalAngle(service, rules, path + [("NormalAngle", "")])
                    self.Refacet = self.__class__.Refacet(service, rules, path + [("Refacet", "")])
                    super().__init__(service, rules, path)

                class Deviation(PyNumerical):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """
                    pass

                class MaxSize(PyNumerical):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """
                    pass

                class NormalAngle(PyNumerical):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """
                    pass

                class Refacet(PyParameter):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """
                    pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class EdgeExtraction(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class FeatureAngle(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class IsChildrenSettingsChanged(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class KeyId(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class MergeChildren(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class OneZonePer(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Parent(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class PrefixObjectName(PyParameter):
                """
                Enter a name for the capping surface.
                """
                pass

            class RefacetOperation(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Transformations(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class ChangeChildrenSettings(PyCommand):
                """
                Command ChangeChildrenSettings.


                Returns
                -------
                bool
                """
                class _ChangeChildrenSettingsCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ChangeChildrenSettingsCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ChangeChildrenSettingsCommandArguments(*args)

            class Copy(PyCommand):
                """
                Command Copy.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _CopyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _CopyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CopyCommandArguments(*args)

            class CreateChild(PyCommand):
                """
                Command CreateChild.

                Parameters
                ----------
                ChildName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _CreateChildCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.ChildName = self._ChildName(self, "ChildName", service, rules, path)

                    class _ChildName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _CreateChildCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateChildCommandArguments(*args)

            class Move(PyCommand):
                """
                Command Move.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _MoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _MoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._MoveCommandArguments(*args)

            class ReFacet(PyCommand):
                """
                Command ReFacet.

                Parameters
                ----------
                Deviation : float
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                NormalAngle : float
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                MaxSize : float
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _ReFacetCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                        self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                        self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)

                    class _Deviation(PyNumericalCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                    class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                    class _MaxSize(PyNumericalCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _ReFacetCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ReFacetCommandArguments(*args)

            class ReFacetNow(PyCommand):
                """
                Command ReFacetNow.


                Returns
                -------
                bool
                """
                class _ReFacetNowCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ReFacetNowCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ReFacetNowCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

        def __getitem__(self, key: str) -> _AssemblyNode:
            return super().__getitem__(key)

    class Mirror(PyNamedObjectContainer):
        """
        .
        """
        class _Mirror(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.MirrorAbout = self.__class__.MirrorAbout(service, rules, path + [("MirrorAbout", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class MirrorAbout(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _Mirror:
            return super().__getitem__(key)

    class Node(PyNamedObjectContainer):
        """
        .
        """
        class _Node(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.KeyId = self.__class__.KeyId(service, rules, path + [("KeyId", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.ObjectSetting = self.__class__.ObjectSetting(service, rules, path + [("ObjectSetting", "")])
                self.Parent = self.__class__.Parent(service, rules, path + [("Parent", "")])
                self.RefacetOperation = self.__class__.RefacetOperation(service, rules, path + [("RefacetOperation", "")])
                self.Suppress = self.__class__.Suppress(service, rules, path + [("Suppress", "")])
                self.Transformations = self.__class__.Transformations(service, rules, path + [("Transformations", "")])
                self.Updated = self.__class__.Updated(service, rules, path + [("Updated", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Copy = self.__class__.Copy(service, rules, "Copy", path)
                self.CreateChild = self.__class__.CreateChild(service, rules, "CreateChild", path)
                self.Move = self.__class__.Move(service, rules, "Move", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.WildcardCopy = self.__class__.WildcardCopy(service, rules, "WildcardCopy", path)
                super().__init__(service, rules, path)

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class KeyId(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class ObjectSetting(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Parent(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class RefacetOperation(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Suppress(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Transformations(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Updated(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Copy(PyCommand):
                """
                Command Copy.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _CopyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _CopyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CopyCommandArguments(*args)

            class CreateChild(PyCommand):
                """
                Command CreateChild.

                Parameters
                ----------
                ChildName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _CreateChildCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.ChildName = self._ChildName(self, "ChildName", service, rules, path)

                    class _ChildName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _CreateChildCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateChildCommandArguments(*args)

            class Move(PyCommand):
                """
                Command Move.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _MoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _MoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._MoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class WildcardCopy(PyCommand):
                """
                Command WildcardCopy.

                Parameters
                ----------
                Pattern : str
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _WildcardCopyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Pattern = self._Pattern(self, "Pattern", service, rules, path)

                    class _Pattern(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _WildcardCopyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._WildcardCopyCommandArguments(*args)

        def __getitem__(self, key: str) -> _Node:
            return super().__getitem__(key)

    class ObjectSetting(PyNamedObjectContainer):
        """
        .
        """
        class _ObjectSetting(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.EdgeExtraction = self.__class__.EdgeExtraction(service, rules, path + [("EdgeExtraction", "")])
                self.FeatureAngle = self.__class__.FeatureAngle(service, rules, path + [("FeatureAngle", "")])
                self.MergeChildren = self.__class__.MergeChildren(service, rules, path + [("MergeChildren", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.OneZonePer = self.__class__.OneZonePer(service, rules, path + [("OneZonePer", "")])
                self.PrefixObjectName = self.__class__.PrefixObjectName(service, rules, path + [("PrefixObjectName", "")])
                self.UseDefaultSettings = self.__class__.UseDefaultSettings(service, rules, path + [("UseDefaultSettings", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                super().__init__(service, rules, path)

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class EdgeExtraction(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class FeatureAngle(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class MergeChildren(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class OneZonePer(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class PrefixObjectName(PyParameter):
                """
                Enter a name for the capping surface.
                """
                pass

            class UseDefaultSettings(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

        def __getitem__(self, key: str) -> _ObjectSetting:
            return super().__getitem__(key)

    class Refaceting(PyNamedObjectContainer):
        """
        .
        """
        class _Refaceting(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Deviation = self.__class__.Deviation(service, rules, path + [("Deviation", "")])
                self.MaxSize = self.__class__.MaxSize(service, rules, path + [("MaxSize", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.NormalAngle = self.__class__.NormalAngle(service, rules, path + [("NormalAngle", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                self.Edit = self.__class__.Edit(service, rules, "Edit", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Deviation(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class MaxSize(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class NormalAngle(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Delete(PyCommand):
                """
                Command Delete.


                Returns
                -------
                bool
                """
                class _DeleteCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DeleteCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DeleteCommandArguments(*args)

            class Edit(PyCommand):
                """
                Command Edit.


                Returns
                -------
                bool
                """
                class _EditCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _EditCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._EditCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

        def __getitem__(self, key: str) -> _Refaceting:
            return super().__getitem__(key)

    class Rotate(PyNamedObjectContainer):
        """
        .
        """
        class _Rotate(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.RotateX = self.__class__.RotateX(service, rules, path + [("RotateX", "")])
                self.RotateY = self.__class__.RotateY(service, rules, path + [("RotateY", "")])
                self.RotateZ = self.__class__.RotateZ(service, rules, path + [("RotateZ", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class RotateX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class RotateY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class RotateZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _Rotate:
            return super().__getitem__(key)

    class RotateAboutAxis(PyNamedObjectContainer):
        """
        .
        """
        class _RotateAboutAxis(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Angle = self.__class__.Angle(service, rules, path + [("Angle", "")])
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.AxisX = self.__class__.AxisX(service, rules, path + [("AxisX", "")])
                self.AxisY = self.__class__.AxisY(service, rules, path + [("AxisY", "")])
                self.AxisZ = self.__class__.AxisZ(service, rules, path + [("AxisZ", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.PivotX = self.__class__.PivotX(service, rules, path + [("PivotX", "")])
                self.PivotY = self.__class__.PivotY(service, rules, path + [("PivotY", "")])
                self.PivotZ = self.__class__.PivotZ(service, rules, path + [("PivotZ", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Angle(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class AxisX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class AxisY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class AxisZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class PivotX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class PivotY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class PivotZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _RotateAboutAxis:
            return super().__getitem__(key)

    class Scaling(PyNamedObjectContainer):
        """
        .
        """
        class _Scaling(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.ScaleX = self.__class__.ScaleX(service, rules, path + [("ScaleX", "")])
                self.ScaleY = self.__class__.ScaleY(service, rules, path + [("ScaleY", "")])
                self.ScaleZ = self.__class__.ScaleZ(service, rules, path + [("ScaleZ", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class ScaleX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class ScaleY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class ScaleZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _Scaling:
            return super().__getitem__(key)

    class Transform(PyNamedObjectContainer):
        """
        .
        """
        class _Transform(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.RotateX = self.__class__.RotateX(service, rules, path + [("RotateX", "")])
                self.RotateY = self.__class__.RotateY(service, rules, path + [("RotateY", "")])
                self.RotateZ = self.__class__.RotateZ(service, rules, path + [("RotateZ", "")])
                self.TranslateX = self.__class__.TranslateX(service, rules, path + [("TranslateX", "")])
                self.TranslateY = self.__class__.TranslateY(service, rules, path + [("TranslateY", "")])
                self.TranslateZ = self.__class__.TranslateZ(service, rules, path + [("TranslateZ", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Delete = self.__class__.Delete(service, rules, "Delete", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class RotateX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class RotateY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class RotateZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class TranslateX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class TranslateY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class TranslateZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Delete(PyCommand):
                """
                Command Delete.

                Parameters
                ----------
                Path : str
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _DeleteCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Path = self._Path(self, "Path", service, rules, path)

                    class _Path(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _DeleteCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DeleteCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _Transform:
            return super().__getitem__(key)

    class TransformBase(PyNamedObjectContainer):
        """
        .
        """
        class _TransformBase(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _TransformBase:
            return super().__getitem__(key)

    class Translate(PyNamedObjectContainer):
        """
        .
        """
        class _Translate(PyMenu):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            def __init__(self, service, rules, path):
                self.Applied = self.__class__.Applied(service, rules, path + [("Applied", "")])
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.Global = self.__class__.Global(service, rules, path + [("Global", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.TranslateX = self.__class__.TranslateX(service, rules, path + [("TranslateX", "")])
                self.TranslateY = self.__class__.TranslateY(service, rules, path + [("TranslateY", "")])
                self.TranslateZ = self.__class__.TranslateZ(service, rules, path + [("TranslateZ", "")])
                self.Type = self.__class__.Type(service, rules, path + [("Type", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                self.Add = self.__class__.Add(service, rules, "Add", path)
                self.Apply = self.__class__.Apply(service, rules, "Apply", path)
                self.Remove = self.__class__.Remove(service, rules, "Remove", path)
                self.Rename = self.__class__.Rename(service, rules, "Rename", path)
                self.Undo = self.__class__.Undo(service, rules, "Undo", path)
                self.Update = self.__class__.Update(service, rules, "Update", path)
                super().__init__(service, rules, path)

            class Applied(PyParameter):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Children(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Context(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Global(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Name(PyTextual):
                """
                Enter a name for the capping surface.
                """
                pass

            class TranslateX(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class TranslateY(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class TranslateZ(PyNumerical):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Type(PyTextual):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """
                pass

            class _name_(PyTextual):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _AddCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _AddCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddCommandArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyCommandArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

                Returns
                -------
                bool
                """
                class _RemoveCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyTextualCommandArgumentsSubItem):
                        """
                        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                        """

                def create_instance(self) -> _RemoveCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveCommandArguments(*args)

            class Rename(PyCommand):
                """
                Command Rename.

                Parameters
                ----------
                NewName : str
                    Enter a name for the capping surface.

                Returns
                -------
                bool
                """
                class _RenameCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.NewName = self._NewName(self, "NewName", service, rules, path)

                    class _NewName(PyTextualCommandArgumentsSubItem):
                        """
                        Enter a name for the capping surface.
                        """

                def create_instance(self) -> _RenameCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RenameCommandArguments(*args)

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoCommandArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateCommandArguments(*args)

        def __getitem__(self, key: str) -> _Translate:
            return super().__getitem__(key)

    class GlobalSettings(PyMenu):
        """
        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        """
        def __init__(self, service, rules, path):
            self.CurrentContext = self.__class__.CurrentContext(service, rules, path + [("CurrentContext", "")])
            self.CurrentNode = self.__class__.CurrentNode(service, rules, path + [("CurrentNode", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            super().__init__(service, rules, path)

        class CurrentContext(PyNumerical):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

        class CurrentNode(PyTextual):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

        class LengthUnit(PyTextual):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

    class MeshingOperations(PyMenu):
        """
        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.DeleteAllOperations = self.__class__.DeleteAllOperations(service, rules, "DeleteAllOperations", path)
            self.UpdateAllOperations = self.__class__.UpdateAllOperations(service, rules, "UpdateAllOperations", path)
            super().__init__(service, rules, path)

        class Children(PyTextual):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

        class Name(PyTextual):
            """
            Enter a name for the capping surface.
            """
            pass

        class DeleteAllOperations(PyCommand):
            """
            Command DeleteAllOperations.


            Returns
            -------
            bool
            """
            class _DeleteAllOperationsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllOperationsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllOperationsCommandArguments(*args)

        class UpdateAllOperations(PyCommand):
            """
            Command UpdateAllOperations.


            Returns
            -------
            bool
            """
            class _UpdateAllOperationsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateAllOperationsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateAllOperationsCommandArguments(*args)

    class ObjectSettingOperations(PyMenu):
        """
        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.CreateObjectSetting = self.__class__.CreateObjectSetting(service, rules, "CreateObjectSetting", path)
            self.DeleteAllObjectSetting = self.__class__.DeleteAllObjectSetting(service, rules, "DeleteAllObjectSetting", path)
            self.DeleteObjectSetting = self.__class__.DeleteObjectSetting(service, rules, "DeleteObjectSetting", path)
            super().__init__(service, rules, path)

        class Children(PyTextual):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

        class Name(PyTextual):
            """
            Enter a name for the capping surface.
            """
            pass

        class CreateObjectSetting(PyCommand):
            """
            Command CreateObjectSetting.

            Parameters
            ----------
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _CreateObjectSettingCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _CreateObjectSettingCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateObjectSettingCommandArguments(*args)

        class DeleteAllObjectSetting(PyCommand):
            """
            Command DeleteAllObjectSetting.


            Returns
            -------
            bool
            """
            class _DeleteAllObjectSettingCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllObjectSettingCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllObjectSettingCommandArguments(*args)

        class DeleteObjectSetting(PyCommand):
            """
            Command DeleteObjectSetting.

            Parameters
            ----------
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _DeleteObjectSettingCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _DeleteObjectSettingCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteObjectSettingCommandArguments(*args)

    class RefacetingOperations(PyMenu):
        """
        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.CreateRefacet = self.__class__.CreateRefacet(service, rules, "CreateRefacet", path)
            self.DeleteAllRefacets = self.__class__.DeleteAllRefacets(service, rules, "DeleteAllRefacets", path)
            self.DeleteRefacet = self.__class__.DeleteRefacet(service, rules, "DeleteRefacet", path)
            self.UpdateAllRefacets = self.__class__.UpdateAllRefacets(service, rules, "UpdateAllRefacets", path)
            super().__init__(service, rules, path)

        class Children(PyTextual):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

        class Name(PyTextual):
            """
            Enter a name for the capping surface.
            """
            pass

        class CreateRefacet(PyCommand):
            """
            Command CreateRefacet.

            Parameters
            ----------
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _CreateRefacetCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _CreateRefacetCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateRefacetCommandArguments(*args)

        class DeleteAllRefacets(PyCommand):
            """
            Command DeleteAllRefacets.


            Returns
            -------
            bool
            """
            class _DeleteAllRefacetsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllRefacetsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllRefacetsCommandArguments(*args)

        class DeleteRefacet(PyCommand):
            """
            Command DeleteRefacet.

            Parameters
            ----------
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _DeleteRefacetCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _DeleteRefacetCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteRefacetCommandArguments(*args)

        class UpdateAllRefacets(PyCommand):
            """
            Command UpdateAllRefacets.


            Returns
            -------
            bool
            """
            class _UpdateAllRefacetsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateAllRefacetsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateAllRefacetsCommandArguments(*args)

    class TransformOperations(PyMenu):
        """
        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.CreateTransform = self.__class__.CreateTransform(service, rules, "CreateTransform", path)
            self.CreateTransformType = self.__class__.CreateTransformType(service, rules, "CreateTransformType", path)
            self.DeleteAllTransforms = self.__class__.DeleteAllTransforms(service, rules, "DeleteAllTransforms", path)
            self.DeleteTransform = self.__class__.DeleteTransform(service, rules, "DeleteTransform", path)
            self.UpdateAllTransforms = self.__class__.UpdateAllTransforms(service, rules, "UpdateAllTransforms", path)
            super().__init__(service, rules, path)

        class Children(PyTextual):
            """
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
            """
            pass

        class Name(PyTextual):
            """
            Enter a name for the capping surface.
            """
            pass

        class CreateTransform(PyCommand):
            """
            Command CreateTransform.

            Parameters
            ----------
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _CreateTransformCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _CreateTransformCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateTransformCommandArguments(*args)

        class CreateTransformType(PyCommand):
            """
            Command CreateTransformType.

            Parameters
            ----------
            Type : str
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _CreateTransformTypeCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Type = self._Type(self, "Type", service, rules, path)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Type(PyTextualCommandArgumentsSubItem):
                    """
                    Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                    """

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _CreateTransformTypeCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateTransformTypeCommandArguments(*args)

        class DeleteAllTransforms(PyCommand):
            """
            Command DeleteAllTransforms.


            Returns
            -------
            bool
            """
            class _DeleteAllTransformsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllTransformsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllTransformsCommandArguments(*args)

        class DeleteTransform(PyCommand):
            """
            Command DeleteTransform.

            Parameters
            ----------
            Paths : list[str]
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

            Returns
            -------
            bool
            """
            class _DeleteTransformCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyTextualCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            def create_instance(self) -> _DeleteTransformCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteTransformCommandArguments(*args)

        class UpdateAllTransforms(PyCommand):
            """
            Command UpdateAllTransforms.


            Returns
            -------
            bool
            """
            class _UpdateAllTransformsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateAllTransformsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateAllTransformsCommandArguments(*args)

    class AppendFmdFiles(PyCommand):
        """
        Command AppendFmdFiles.

        Parameters
        ----------
        FilePath : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        AssemblyParentNode : int
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        FileUnit : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        Route : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        JtLOD : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        PartPerBody : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        PrefixParentName : bool
            Enter a name for the capping surface.
        RemoveEmptyParts : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        IgnoreSolidNamesAppend : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        Options : dict[str, Any]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        RefacetOptions : dict[str, Any]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _AppendFmdFilesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)
                self.AssemblyParentNode = self._AssemblyParentNode(self, "AssemblyParentNode", service, rules, path)
                self.FileUnit = self._FileUnit(self, "FileUnit", service, rules, path)
                self.Route = self._Route(self, "Route", service, rules, path)
                self.JtLOD = self._JtLOD(self, "JtLOD", service, rules, path)
                self.PartPerBody = self._PartPerBody(self, "PartPerBody", service, rules, path)
                self.PrefixParentName = self._PrefixParentName(self, "PrefixParentName", service, rules, path)
                self.RemoveEmptyParts = self._RemoveEmptyParts(self, "RemoveEmptyParts", service, rules, path)
                self.IgnoreSolidNamesAppend = self._IgnoreSolidNamesAppend(self, "IgnoreSolidNamesAppend", service, rules, path)
                self.Options = self._Options(self, "Options", service, rules, path)
                self.RefacetOptions = self._RefacetOptions(self, "RefacetOptions", service, rules, path)

            class _FilePath(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _AssemblyParentNode(PyNumericalCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _FileUnit(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _Route(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _JtLOD(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _PartPerBody(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _PrefixParentName(PyParameterCommandArgumentsSubItem):
                """
                Enter a name for the capping surface.
                """

            class _RemoveEmptyParts(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _IgnoreSolidNamesAppend(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _Options(PySingletonCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Line(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Surface(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            class _RefacetOptions(PySingletonCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.RefacetDuringLoad = self._RefacetDuringLoad(self, "RefacetDuringLoad", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _RefacetDuringLoad(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

        def create_instance(self) -> _AppendFmdFilesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AppendFmdFilesCommandArguments(*args)

    class ChangeFileLengthUnit(PyCommand):
        """
        Command ChangeFileLengthUnit.

        Parameters
        ----------
        LengthUnit : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _ChangeFileLengthUnitCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _ChangeFileLengthUnitCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChangeFileLengthUnitCommandArguments(*args)

    class ChangeLengthUnit(PyCommand):
        """
        Command ChangeLengthUnit.

        Parameters
        ----------
        LengthUnit : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _ChangeLengthUnitCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _ChangeLengthUnitCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChangeLengthUnitCommandArguments(*args)

    class CreateObjForEachPart(PyCommand):
        """
        Command CreateObjForEachPart.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _CreateObjForEachPartCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _CreateObjForEachPartCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateObjForEachPartCommandArguments(*args)

    class CreateObjects(PyCommand):
        """
        Command CreateObjects.


        Returns
        -------
        bool
        """
        class _CreateObjectsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CreateObjectsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateObjectsCommandArguments(*args)

    class Delete(PyCommand):
        """
        Command Delete.

        Parameters
        ----------
        Path : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _DeleteCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Path = self._Path(self, "Path", service, rules, path)

            class _Path(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _DeleteCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DeleteCommandArguments(*args)

    class DeletePaths(PyCommand):
        """
        Command DeletePaths.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _DeletePathsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _DeletePathsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DeletePathsCommandArguments(*args)

    class InitializeTemplate(PyCommand):
        """
        Command InitializeTemplate.

        Parameters
        ----------
        templateType : str
            Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:

        Returns
        -------
        bool
        """
        class _InitializeTemplateCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.templateType = self._templateType(self, "templateType", service, rules, path)

            class _templateType(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """

        def create_instance(self) -> _InitializeTemplateCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._InitializeTemplateCommandArguments(*args)

    class InputFileChanged(PyCommand):
        """
        Command InputFileChanged.

        Parameters
        ----------
        FilePath : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        PartPerBody : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        PrefixParentName : bool
            Enter a name for the capping surface.
        RemoveEmptyParts : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        IgnoreSolidNames : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        FileLengthUnit : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        JtLOD : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        Options : dict[str, Any]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        RefacetOptions : dict[str, Any]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _InputFileChangedCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)
                self.PartPerBody = self._PartPerBody(self, "PartPerBody", service, rules, path)
                self.PrefixParentName = self._PrefixParentName(self, "PrefixParentName", service, rules, path)
                self.RemoveEmptyParts = self._RemoveEmptyParts(self, "RemoveEmptyParts", service, rules, path)
                self.IgnoreSolidNames = self._IgnoreSolidNames(self, "IgnoreSolidNames", service, rules, path)
                self.FileLengthUnit = self._FileLengthUnit(self, "FileLengthUnit", service, rules, path)
                self.JtLOD = self._JtLOD(self, "JtLOD", service, rules, path)
                self.Options = self._Options(self, "Options", service, rules, path)
                self.RefacetOptions = self._RefacetOptions(self, "RefacetOptions", service, rules, path)

            class _FilePath(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _PartPerBody(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _PrefixParentName(PyParameterCommandArgumentsSubItem):
                """
                Enter a name for the capping surface.
                """

            class _RemoveEmptyParts(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _IgnoreSolidNames(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _FileLengthUnit(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _JtLOD(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _Options(PySingletonCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Line(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Surface(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            class _RefacetOptions(PySingletonCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.RefacetDuringLoad = self._RefacetDuringLoad(self, "RefacetDuringLoad", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _RefacetDuringLoad(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

        def create_instance(self) -> _InputFileChangedCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._InputFileChangedCommandArguments(*args)

    class ListMeshingOperations(PyCommand):
        """
        Command ListMeshingOperations.

        Parameters
        ----------
        Path : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _ListMeshingOperationsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Path = self._Path(self, "Path", service, rules, path)

            class _Path(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _ListMeshingOperationsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ListMeshingOperationsCommandArguments(*args)

    class LoadFmdFile(PyCommand):
        """
        Command LoadFmdFile.

        Parameters
        ----------
        FilePath : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        FileUnit : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        Route : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        JtLOD : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        PartPerBody : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        PrefixParentName : bool
            Enter a name for the capping surface.
        RemoveEmptyParts : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        IgnoreSolidNames : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        Options : dict[str, Any]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        RefacetOptions : dict[str, Any]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _LoadFmdFileCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)
                self.FileUnit = self._FileUnit(self, "FileUnit", service, rules, path)
                self.Route = self._Route(self, "Route", service, rules, path)
                self.JtLOD = self._JtLOD(self, "JtLOD", service, rules, path)
                self.PartPerBody = self._PartPerBody(self, "PartPerBody", service, rules, path)
                self.PrefixParentName = self._PrefixParentName(self, "PrefixParentName", service, rules, path)
                self.RemoveEmptyParts = self._RemoveEmptyParts(self, "RemoveEmptyParts", service, rules, path)
                self.IgnoreSolidNames = self._IgnoreSolidNames(self, "IgnoreSolidNames", service, rules, path)
                self.Options = self._Options(self, "Options", service, rules, path)
                self.RefacetOptions = self._RefacetOptions(self, "RefacetOptions", service, rules, path)

            class _FilePath(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _FileUnit(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _Route(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _JtLOD(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _PartPerBody(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _PrefixParentName(PyParameterCommandArgumentsSubItem):
                """
                Enter a name for the capping surface.
                """

            class _RemoveEmptyParts(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _IgnoreSolidNames(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _Options(PySingletonCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Line(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Surface(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

            class _RefacetOptions(PySingletonCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.RefacetDuringLoad = self._RefacetDuringLoad(self, "RefacetDuringLoad", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _RefacetDuringLoad(PyParameterCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                    """

        def create_instance(self) -> _LoadFmdFileCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadFmdFileCommandArguments(*args)

    class LoadTemplate(PyCommand):
        """
        Command LoadTemplate.

        Parameters
        ----------
        FilePath : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _LoadTemplateCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _LoadTemplateCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadTemplateCommandArguments(*args)

    class MarkObjectsOutofDate(PyCommand):
        """
        Command MarkObjectsOutofDate.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _MarkObjectsOutofDateCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _MarkObjectsOutofDateCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MarkObjectsOutofDateCommandArguments(*args)

    class MoveCADComponentsToNewObject(PyCommand):
        """
        Command MoveCADComponentsToNewObject.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _MoveCADComponentsToNewObjectCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _MoveCADComponentsToNewObjectCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MoveCADComponentsToNewObjectCommandArguments(*args)

    class MoveToNewSubobject(PyCommand):
        """
        Command MoveToNewSubobject.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _MoveToNewSubobjectCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _MoveToNewSubobjectCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MoveToNewSubobjectCommandArguments(*args)

    class MoveToObject(PyCommand):
        """
        Command MoveToObject.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _MoveToObjectCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _MoveToObjectCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MoveToObjectCommandArguments(*args)

    class RedoAllTransforms(PyCommand):
        """
        Command RedoAllTransforms.


        Returns
        -------
        bool
        """
        class _RedoAllTransformsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _RedoAllTransformsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._RedoAllTransformsCommandArguments(*args)

    class ResetTemplate(PyCommand):
        """
        Command ResetTemplate.


        Returns
        -------
        bool
        """
        class _ResetTemplateCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _ResetTemplateCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ResetTemplateCommandArguments(*args)

    class SaveFmdFile(PyCommand):
        """
        Command SaveFmdFile.

        Parameters
        ----------
        FilePath : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _SaveFmdFileCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _SaveFmdFileCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SaveFmdFileCommandArguments(*args)

    class SaveTemplate(PyCommand):
        """
        Command SaveTemplate.

        Parameters
        ----------
        FilePath : str
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _SaveTemplateCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _SaveTemplateCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SaveTemplateCommandArguments(*args)

    class SuppressNodeObjects(PyCommand):
        """
        Command SuppressNodeObjects.

        Parameters
        ----------
        Paths : list[str]
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
        Suppress : bool
            This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...

        Returns
        -------
        bool
        """
        class _SuppressNodeObjectsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)
                self.Suppress = self._Suppress(self, "Suppress", service, rules, path)

            class _Paths(PyTextualCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

            class _Suppress(PyParameterCommandArgumentsSubItem):
                """
                This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
                """

        def create_instance(self) -> _SuppressNodeObjectsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SuppressNodeObjectsCommandArguments(*args)

    class UndoAllTransforms(PyCommand):
        """
        Command UndoAllTransforms.


        Returns
        -------
        bool
        """
        class _UndoAllTransformsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _UndoAllTransformsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UndoAllTransformsCommandArguments(*args)

