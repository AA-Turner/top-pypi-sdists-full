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
        self.MoveCADComponentsToNewObject = self.__class__.MoveCADComponentsToNewObject(service, rules, "MoveCADComponentsToNewObject", path)
        self.MoveToNewSubobject = self.__class__.MoveToNewSubobject(service, rules, "MoveToNewSubobject", path)
        self.MoveToObject = self.__class__.MoveToObject(service, rules, "MoveToObject", path)
        self.RedoAllTransforms = self.__class__.RedoAllTransforms(service, rules, "RedoAllTransforms", path)
        self.ResetTemplate = self.__class__.ResetTemplate(service, rules, "ResetTemplate", path)
        self.SaveFmdFile = self.__class__.SaveFmdFile(service, rules, "SaveFmdFile", path)
        self.SaveTemplate = self.__class__.SaveTemplate(service, rules, "SaveTemplate", path)
        self.UndoAllTransforms = self.__class__.UndoAllTransforms(service, rules, "UndoAllTransforms", path)
        super().__init__(service, rules, path)

    class AssemblyNode(PyNamedObjectContainer):
        """
        .
        """
        class _AssemblyNode(PyMenu):
            """
            Singleton _AssemblyNode.
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
                Singleton Refaceting.
                """
                def __init__(self, service, rules, path):
                    self.Deviation = self.__class__.Deviation(service, rules, path + [("Deviation", "")])
                    self.MaxSize = self.__class__.MaxSize(service, rules, path + [("MaxSize", "")])
                    self.NormalAngle = self.__class__.NormalAngle(service, rules, path + [("NormalAngle", "")])
                    self.Refacet = self.__class__.Refacet(service, rules, path + [("Refacet", "")])
                    super().__init__(service, rules, path)

                class Deviation(PyNumerical):
                    """
                    Parameter Deviation of value type float.
                    """
                    pass

                class MaxSize(PyNumerical):
                    """
                    Parameter MaxSize of value type float.
                    """
                    pass

                class NormalAngle(PyNumerical):
                    """
                    Parameter NormalAngle of value type float.
                    """
                    pass

                class Refacet(PyParameter):
                    """
                    Parameter Refacet of value type bool.
                    """
                    pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class EdgeExtraction(PyTextual):
                """
                Parameter EdgeExtraction of value type str.
                """
                pass

            class FeatureAngle(PyNumerical):
                """
                Parameter FeatureAngle of value type float.
                """
                pass

            class IsChildrenSettingsChanged(PyParameter):
                """
                Parameter IsChildrenSettingsChanged of value type bool.
                """
                pass

            class KeyId(PyNumerical):
                """
                Parameter KeyId of value type int.
                """
                pass

            class MergeChildren(PyParameter):
                """
                Parameter MergeChildren of value type bool.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class OneZonePer(PyTextual):
                """
                Parameter OneZonePer of value type str.
                """
                pass

            class Parent(PyTextual):
                """
                Parameter Parent of value type str.
                """
                pass

            class PrefixObjectName(PyParameter):
                """
                Parameter PrefixObjectName of value type bool.
                """
                pass

            class RefacetOperation(PyTextual):
                """
                Parameter RefacetOperation of value type str.
                """
                pass

            class Transformations(PyTextual):
                """
                Parameter Transformations of value type list[str].
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class ChangeChildrenSettings(PyCommand):
                """
                Command ChangeChildrenSettings.


                Returns
                -------
                bool
                """
                class _ChangeChildrenSettingsArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ChangeChildrenSettingsArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ChangeChildrenSettingsArguments(*args)

            class Copy(PyCommand):
                """
                Command Copy.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _CopyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _CopyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CopyArguments(*args)

            class CreateChild(PyCommand):
                """
                Command CreateChild.

                Parameters
                ----------
                ChildName : str

                Returns
                -------
                bool
                """
                class _CreateChildArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.ChildName = self._ChildName(self, "ChildName", service, rules, path)

                    class _ChildName(PyArgumentsTextualSubItem):
                        """
                        Argument ChildName.
                        """

                def create_instance(self) -> _CreateChildArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateChildArguments(*args)

            class Move(PyCommand):
                """
                Command Move.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _MoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _MoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._MoveArguments(*args)

            class ReFacet(PyCommand):
                """
                Command ReFacet.

                Parameters
                ----------
                Deviation : float
                NormalAngle : float
                MaxSize : float

                Returns
                -------
                bool
                """
                class _ReFacetArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                        self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                        self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)

                    class _Deviation(PyArgumentsNumericalSubItem):
                        """
                        Argument Deviation.
                        """

                    class _NormalAngle(PyArgumentsNumericalSubItem):
                        """
                        Argument NormalAngle.
                        """

                    class _MaxSize(PyArgumentsNumericalSubItem):
                        """
                        Argument MaxSize.
                        """

                def create_instance(self) -> _ReFacetArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ReFacetArguments(*args)

            class ReFacetNow(PyCommand):
                """
                Command ReFacetNow.


                Returns
                -------
                bool
                """
                class _ReFacetNowArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ReFacetNowArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ReFacetNowArguments(*args)

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

        def __getitem__(self, key: str) -> _AssemblyNode:
            return super().__getitem__(key)

    class Mirror(PyNamedObjectContainer):
        """
        .
        """
        class _Mirror(PyMenu):
            """
            Singleton _Mirror.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class MirrorAbout(PyTextual):
                """
                Parameter MirrorAbout of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _Mirror:
            return super().__getitem__(key)

    class Node(PyNamedObjectContainer):
        """
        .
        """
        class _Node(PyMenu):
            """
            Singleton _Node.
            """
            def __init__(self, service, rules, path):
                self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
                self.Context = self.__class__.Context(service, rules, path + [("Context", "")])
                self.KeyId = self.__class__.KeyId(service, rules, path + [("KeyId", "")])
                self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
                self.ObjectSetting = self.__class__.ObjectSetting(service, rules, path + [("ObjectSetting", "")])
                self.Parent = self.__class__.Parent(service, rules, path + [("Parent", "")])
                self.RefacetOperation = self.__class__.RefacetOperation(service, rules, path + [("RefacetOperation", "")])
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
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class KeyId(PyNumerical):
                """
                Parameter KeyId of value type int.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class ObjectSetting(PyTextual):
                """
                Parameter ObjectSetting of value type str.
                """
                pass

            class Parent(PyTextual):
                """
                Parameter Parent of value type str.
                """
                pass

            class RefacetOperation(PyTextual):
                """
                Parameter RefacetOperation of value type str.
                """
                pass

            class Transformations(PyTextual):
                """
                Parameter Transformations of value type list[str].
                """
                pass

            class Updated(PyParameter):
                """
                Parameter Updated of value type bool.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Copy(PyCommand):
                """
                Command Copy.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _CopyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _CopyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CopyArguments(*args)

            class CreateChild(PyCommand):
                """
                Command CreateChild.

                Parameters
                ----------
                ChildName : str

                Returns
                -------
                bool
                """
                class _CreateChildArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.ChildName = self._ChildName(self, "ChildName", service, rules, path)

                    class _ChildName(PyArgumentsTextualSubItem):
                        """
                        Argument ChildName.
                        """

                def create_instance(self) -> _CreateChildArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._CreateChildArguments(*args)

            class Move(PyCommand):
                """
                Command Move.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _MoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _MoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._MoveArguments(*args)

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

            class WildcardCopy(PyCommand):
                """
                Command WildcardCopy.

                Parameters
                ----------
                Pattern : str

                Returns
                -------
                bool
                """
                class _WildcardCopyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Pattern = self._Pattern(self, "Pattern", service, rules, path)

                    class _Pattern(PyArgumentsTextualSubItem):
                        """
                        Argument Pattern.
                        """

                def create_instance(self) -> _WildcardCopyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._WildcardCopyArguments(*args)

        def __getitem__(self, key: str) -> _Node:
            return super().__getitem__(key)

    class ObjectSetting(PyNamedObjectContainer):
        """
        .
        """
        class _ObjectSetting(PyMenu):
            """
            Singleton _ObjectSetting.
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
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class EdgeExtraction(PyTextual):
                """
                Parameter EdgeExtraction of value type str.
                """
                pass

            class FeatureAngle(PyNumerical):
                """
                Parameter FeatureAngle of value type float.
                """
                pass

            class MergeChildren(PyParameter):
                """
                Parameter MergeChildren of value type bool.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class OneZonePer(PyTextual):
                """
                Parameter OneZonePer of value type str.
                """
                pass

            class PrefixObjectName(PyParameter):
                """
                Parameter PrefixObjectName of value type bool.
                """
                pass

            class UseDefaultSettings(PyParameter):
                """
                Parameter UseDefaultSettings of value type bool.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

        def __getitem__(self, key: str) -> _ObjectSetting:
            return super().__getitem__(key)

    class Refaceting(PyNamedObjectContainer):
        """
        .
        """
        class _Refaceting(PyMenu):
            """
            Singleton _Refaceting.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Deviation(PyNumerical):
                """
                Parameter Deviation of value type float.
                """
                pass

            class MaxSize(PyNumerical):
                """
                Parameter MaxSize of value type float.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class NormalAngle(PyNumerical):
                """
                Parameter NormalAngle of value type float.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Delete(PyCommand):
                """
                Command Delete.


                Returns
                -------
                bool
                """
                class _DeleteArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DeleteArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DeleteArguments(*args)

            class Edit(PyCommand):
                """
                Command Edit.


                Returns
                -------
                bool
                """
                class _EditArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _EditArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._EditArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

        def __getitem__(self, key: str) -> _Refaceting:
            return super().__getitem__(key)

    class Rotate(PyNamedObjectContainer):
        """
        .
        """
        class _Rotate(PyMenu):
            """
            Singleton _Rotate.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class RotateX(PyNumerical):
                """
                Parameter RotateX of value type float.
                """
                pass

            class RotateY(PyNumerical):
                """
                Parameter RotateY of value type float.
                """
                pass

            class RotateZ(PyNumerical):
                """
                Parameter RotateZ of value type float.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _Rotate:
            return super().__getitem__(key)

    class RotateAboutAxis(PyNamedObjectContainer):
        """
        .
        """
        class _RotateAboutAxis(PyMenu):
            """
            Singleton _RotateAboutAxis.
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
                Parameter Angle of value type float.
                """
                pass

            class Applied(PyParameter):
                """
                Parameter Applied of value type bool.
                """
                pass

            class AxisX(PyNumerical):
                """
                Parameter AxisX of value type float.
                """
                pass

            class AxisY(PyNumerical):
                """
                Parameter AxisY of value type float.
                """
                pass

            class AxisZ(PyNumerical):
                """
                Parameter AxisZ of value type float.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class PivotX(PyNumerical):
                """
                Parameter PivotX of value type float.
                """
                pass

            class PivotY(PyNumerical):
                """
                Parameter PivotY of value type float.
                """
                pass

            class PivotZ(PyNumerical):
                """
                Parameter PivotZ of value type float.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _RotateAboutAxis:
            return super().__getitem__(key)

    class Scaling(PyNamedObjectContainer):
        """
        .
        """
        class _Scaling(PyMenu):
            """
            Singleton _Scaling.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class ScaleX(PyNumerical):
                """
                Parameter ScaleX of value type float.
                """
                pass

            class ScaleY(PyNumerical):
                """
                Parameter ScaleY of value type float.
                """
                pass

            class ScaleZ(PyNumerical):
                """
                Parameter ScaleZ of value type float.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _Scaling:
            return super().__getitem__(key)

    class Transform(PyNamedObjectContainer):
        """
        .
        """
        class _Transform(PyMenu):
            """
            Singleton _Transform.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class RotateX(PyNumerical):
                """
                Parameter RotateX of value type float.
                """
                pass

            class RotateY(PyNumerical):
                """
                Parameter RotateY of value type float.
                """
                pass

            class RotateZ(PyNumerical):
                """
                Parameter RotateZ of value type float.
                """
                pass

            class TranslateX(PyNumerical):
                """
                Parameter TranslateX of value type float.
                """
                pass

            class TranslateY(PyNumerical):
                """
                Parameter TranslateY of value type float.
                """
                pass

            class TranslateZ(PyNumerical):
                """
                Parameter TranslateZ of value type float.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Delete(PyCommand):
                """
                Command Delete.

                Parameters
                ----------
                Path : str

                Returns
                -------
                bool
                """
                class _DeleteArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Path = self._Path(self, "Path", service, rules, path)

                    class _Path(PyArgumentsTextualSubItem):
                        """
                        Argument Path.
                        """

                def create_instance(self) -> _DeleteArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DeleteArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _Transform:
            return super().__getitem__(key)

    class TransformBase(PyNamedObjectContainer):
        """
        .
        """
        class _TransformBase(PyMenu):
            """
            Singleton _TransformBase.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _TransformBase:
            return super().__getitem__(key)

    class Translate(PyNamedObjectContainer):
        """
        .
        """
        class _Translate(PyMenu):
            """
            Singleton _Translate.
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
                Parameter Applied of value type bool.
                """
                pass

            class Children(PyTextual):
                """
                Parameter Children of value type list[str].
                """
                pass

            class Context(PyNumerical):
                """
                Parameter Context of value type int.
                """
                pass

            class Global(PyTextual):
                """
                Parameter Global of value type str.
                """
                pass

            class Name(PyTextual):
                """
                Parameter Name of value type str.
                """
                pass

            class TranslateX(PyNumerical):
                """
                Parameter TranslateX of value type float.
                """
                pass

            class TranslateY(PyNumerical):
                """
                Parameter TranslateY of value type float.
                """
                pass

            class TranslateZ(PyNumerical):
                """
                Parameter TranslateZ of value type float.
                """
                pass

            class Type(PyTextual):
                """
                Parameter Type of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

            class Add(PyCommand):
                """
                Command Add.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _AddArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _AddArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._AddArguments(*args)

            class Apply(PyCommand):
                """
                Command Apply.


                Returns
                -------
                bool
                """
                class _ApplyArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ApplyArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ApplyArguments(*args)

            class Remove(PyCommand):
                """
                Command Remove.

                Parameters
                ----------
                Paths : list[str]

                Returns
                -------
                bool
                """
                class _RemoveArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Paths = self._Paths(self, "Paths", service, rules, path)

                    class _Paths(PyArgumentsTextualSubItem):
                        """
                        Argument Paths.
                        """

                def create_instance(self) -> _RemoveArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._RemoveArguments(*args)

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

            class Undo(PyCommand):
                """
                Command Undo.


                Returns
                -------
                bool
                """
                class _UndoArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UndoArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UndoArguments(*args)

            class Update(PyCommand):
                """
                Command Update.


                Returns
                -------
                bool
                """
                class _UpdateArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _UpdateArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._UpdateArguments(*args)

        def __getitem__(self, key: str) -> _Translate:
            return super().__getitem__(key)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.CurrentContext = self.__class__.CurrentContext(service, rules, path + [("CurrentContext", "")])
            self.CurrentNode = self.__class__.CurrentNode(service, rules, path + [("CurrentNode", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            super().__init__(service, rules, path)

        class CurrentContext(PyNumerical):
            """
            Parameter CurrentContext of value type int.
            """
            pass

        class CurrentNode(PyTextual):
            """
            Parameter CurrentNode of value type str.
            """
            pass

        class LengthUnit(PyTextual):
            """
            Parameter LengthUnit of value type str.
            """
            pass

    class MeshingOperations(PyMenu):
        """
        Singleton MeshingOperations.
        """
        def __init__(self, service, rules, path):
            self.Children = self.__class__.Children(service, rules, path + [("Children", "")])
            self.Name = self.__class__.Name(service, rules, path + [("Name", "")])
            self.DeleteAllOperations = self.__class__.DeleteAllOperations(service, rules, "DeleteAllOperations", path)
            self.UpdateAllOperations = self.__class__.UpdateAllOperations(service, rules, "UpdateAllOperations", path)
            super().__init__(service, rules, path)

        class Children(PyTextual):
            """
            Parameter Children of value type list[str].
            """
            pass

        class Name(PyTextual):
            """
            Parameter Name of value type str.
            """
            pass

        class DeleteAllOperations(PyCommand):
            """
            Command DeleteAllOperations.


            Returns
            -------
            bool
            """
            class _DeleteAllOperationsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllOperationsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllOperationsArguments(*args)

        class UpdateAllOperations(PyCommand):
            """
            Command UpdateAllOperations.


            Returns
            -------
            bool
            """
            class _UpdateAllOperationsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateAllOperationsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateAllOperationsArguments(*args)

    class ObjectSettingOperations(PyMenu):
        """
        Singleton ObjectSettingOperations.
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
            Parameter Children of value type list[str].
            """
            pass

        class Name(PyTextual):
            """
            Parameter Name of value type str.
            """
            pass

        class CreateObjectSetting(PyCommand):
            """
            Command CreateObjectSetting.

            Parameters
            ----------
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _CreateObjectSettingArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _CreateObjectSettingArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateObjectSettingArguments(*args)

        class DeleteAllObjectSetting(PyCommand):
            """
            Command DeleteAllObjectSetting.


            Returns
            -------
            bool
            """
            class _DeleteAllObjectSettingArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllObjectSettingArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllObjectSettingArguments(*args)

        class DeleteObjectSetting(PyCommand):
            """
            Command DeleteObjectSetting.

            Parameters
            ----------
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _DeleteObjectSettingArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _DeleteObjectSettingArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteObjectSettingArguments(*args)

    class RefacetingOperations(PyMenu):
        """
        Singleton RefacetingOperations.
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
            Parameter Children of value type list[str].
            """
            pass

        class Name(PyTextual):
            """
            Parameter Name of value type str.
            """
            pass

        class CreateRefacet(PyCommand):
            """
            Command CreateRefacet.

            Parameters
            ----------
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _CreateRefacetArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _CreateRefacetArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateRefacetArguments(*args)

        class DeleteAllRefacets(PyCommand):
            """
            Command DeleteAllRefacets.


            Returns
            -------
            bool
            """
            class _DeleteAllRefacetsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllRefacetsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllRefacetsArguments(*args)

        class DeleteRefacet(PyCommand):
            """
            Command DeleteRefacet.

            Parameters
            ----------
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _DeleteRefacetArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _DeleteRefacetArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteRefacetArguments(*args)

        class UpdateAllRefacets(PyCommand):
            """
            Command UpdateAllRefacets.


            Returns
            -------
            bool
            """
            class _UpdateAllRefacetsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateAllRefacetsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateAllRefacetsArguments(*args)

    class TransformOperations(PyMenu):
        """
        Singleton TransformOperations.
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
            Parameter Children of value type list[str].
            """
            pass

        class Name(PyTextual):
            """
            Parameter Name of value type str.
            """
            pass

        class CreateTransform(PyCommand):
            """
            Command CreateTransform.

            Parameters
            ----------
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _CreateTransformArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _CreateTransformArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateTransformArguments(*args)

        class CreateTransformType(PyCommand):
            """
            Command CreateTransformType.

            Parameters
            ----------
            Type : str
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _CreateTransformTypeArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Type = self._Type(self, "Type", service, rules, path)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Type(PyArgumentsTextualSubItem):
                    """
                    Argument Type.
                    """

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _CreateTransformTypeArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CreateTransformTypeArguments(*args)

        class DeleteAllTransforms(PyCommand):
            """
            Command DeleteAllTransforms.


            Returns
            -------
            bool
            """
            class _DeleteAllTransformsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DeleteAllTransformsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteAllTransformsArguments(*args)

        class DeleteTransform(PyCommand):
            """
            Command DeleteTransform.

            Parameters
            ----------
            Paths : list[str]

            Returns
            -------
            bool
            """
            class _DeleteTransformArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Paths = self._Paths(self, "Paths", service, rules, path)

                class _Paths(PyArgumentsTextualSubItem):
                    """
                    Argument Paths.
                    """

            def create_instance(self) -> _DeleteTransformArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DeleteTransformArguments(*args)

        class UpdateAllTransforms(PyCommand):
            """
            Command UpdateAllTransforms.


            Returns
            -------
            bool
            """
            class _UpdateAllTransformsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateAllTransformsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateAllTransformsArguments(*args)

    class AppendFmdFiles(PyCommand):
        """
        Command AppendFmdFiles.

        Parameters
        ----------
        FilePath : list[str]
        AssemblyParentNode : int
        FileUnit : str
        Route : str
        JtLOD : str
        PartPerBody : bool
        PrefixParentName : bool
        RemoveEmptyParts : bool
        IgnoreSolidNamesAppend : bool
        Options : dict[str, Any]

        Returns
        -------
        bool
        """
        class _AppendFmdFilesArguments(PyArguments):
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

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

            class _AssemblyParentNode(PyArgumentsNumericalSubItem):
                """
                Argument AssemblyParentNode.
                """

            class _FileUnit(PyArgumentsTextualSubItem):
                """
                Argument FileUnit.
                """

            class _Route(PyArgumentsTextualSubItem):
                """
                Argument Route.
                """

            class _JtLOD(PyArgumentsTextualSubItem):
                """
                Argument JtLOD.
                """

            class _PartPerBody(PyArgumentsParameterSubItem):
                """
                Argument PartPerBody.
                """

            class _PrefixParentName(PyArgumentsParameterSubItem):
                """
                Argument PrefixParentName.
                """

            class _RemoveEmptyParts(PyArgumentsParameterSubItem):
                """
                Argument RemoveEmptyParts.
                """

            class _IgnoreSolidNamesAppend(PyArgumentsParameterSubItem):
                """
                Argument IgnoreSolidNamesAppend.
                """

            class _Options(PyArgumentsSingletonSubItem):
                """
                Argument Options.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyArgumentsParameterSubItem):
                    """
                    Argument Solid.
                    """

                class _Line(PyArgumentsParameterSubItem):
                    """
                    Argument Line.
                    """

                class _Surface(PyArgumentsParameterSubItem):
                    """
                    Argument Surface.
                    """

        def create_instance(self) -> _AppendFmdFilesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AppendFmdFilesArguments(*args)

    class ChangeFileLengthUnit(PyCommand):
        """
        Command ChangeFileLengthUnit.

        Parameters
        ----------
        LengthUnit : str

        Returns
        -------
        bool
        """
        class _ChangeFileLengthUnitArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Argument LengthUnit.
                """

        def create_instance(self) -> _ChangeFileLengthUnitArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChangeFileLengthUnitArguments(*args)

    class ChangeLengthUnit(PyCommand):
        """
        Command ChangeLengthUnit.

        Parameters
        ----------
        LengthUnit : str

        Returns
        -------
        bool
        """
        class _ChangeLengthUnitArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Argument LengthUnit.
                """

        def create_instance(self) -> _ChangeLengthUnitArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChangeLengthUnitArguments(*args)

    class CreateObjForEachPart(PyCommand):
        """
        Command CreateObjForEachPart.

        Parameters
        ----------
        Paths : list[str]

        Returns
        -------
        bool
        """
        class _CreateObjForEachPartArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyArgumentsTextualSubItem):
                """
                Argument Paths.
                """

        def create_instance(self) -> _CreateObjForEachPartArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateObjForEachPartArguments(*args)

    class CreateObjects(PyCommand):
        """
        Command CreateObjects.


        Returns
        -------
        bool
        """
        class _CreateObjectsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CreateObjectsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateObjectsArguments(*args)

    class Delete(PyCommand):
        """
        Command Delete.

        Parameters
        ----------
        Path : str

        Returns
        -------
        bool
        """
        class _DeleteArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Path = self._Path(self, "Path", service, rules, path)

            class _Path(PyArgumentsTextualSubItem):
                """
                Argument Path.
                """

        def create_instance(self) -> _DeleteArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DeleteArguments(*args)

    class DeletePaths(PyCommand):
        """
        Command DeletePaths.

        Parameters
        ----------
        Paths : list[str]

        Returns
        -------
        bool
        """
        class _DeletePathsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyArgumentsTextualSubItem):
                """
                Argument Paths.
                """

        def create_instance(self) -> _DeletePathsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DeletePathsArguments(*args)

    class InitializeTemplate(PyCommand):
        """
        Command InitializeTemplate.

        Parameters
        ----------
        templateType : str

        Returns
        -------
        bool
        """
        class _InitializeTemplateArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.templateType = self._templateType(self, "templateType", service, rules, path)

            class _templateType(PyArgumentsTextualSubItem):
                """
                Argument templateType.
                """

        def create_instance(self) -> _InitializeTemplateArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._InitializeTemplateArguments(*args)

    class InputFileChanged(PyCommand):
        """
        Command InputFileChanged.

        Parameters
        ----------
        FilePath : str
        PartPerBody : bool
        PrefixParentName : bool
        RemoveEmptyParts : bool
        IgnoreSolidNames : bool
        FileLengthUnit : str
        JtLOD : str
        Options : dict[str, Any]

        Returns
        -------
        bool
        """
        class _InputFileChangedArguments(PyArguments):
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

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

            class _PartPerBody(PyArgumentsParameterSubItem):
                """
                Argument PartPerBody.
                """

            class _PrefixParentName(PyArgumentsParameterSubItem):
                """
                Argument PrefixParentName.
                """

            class _RemoveEmptyParts(PyArgumentsParameterSubItem):
                """
                Argument RemoveEmptyParts.
                """

            class _IgnoreSolidNames(PyArgumentsParameterSubItem):
                """
                Argument IgnoreSolidNames.
                """

            class _FileLengthUnit(PyArgumentsTextualSubItem):
                """
                Argument FileLengthUnit.
                """

            class _JtLOD(PyArgumentsTextualSubItem):
                """
                Argument JtLOD.
                """

            class _Options(PyArgumentsSingletonSubItem):
                """
                Argument Options.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyArgumentsParameterSubItem):
                    """
                    Argument Solid.
                    """

                class _Line(PyArgumentsParameterSubItem):
                    """
                    Argument Line.
                    """

                class _Surface(PyArgumentsParameterSubItem):
                    """
                    Argument Surface.
                    """

        def create_instance(self) -> _InputFileChangedArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._InputFileChangedArguments(*args)

    class ListMeshingOperations(PyCommand):
        """
        Command ListMeshingOperations.

        Parameters
        ----------
        Path : str

        Returns
        -------
        bool
        """
        class _ListMeshingOperationsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Path = self._Path(self, "Path", service, rules, path)

            class _Path(PyArgumentsTextualSubItem):
                """
                Argument Path.
                """

        def create_instance(self) -> _ListMeshingOperationsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ListMeshingOperationsArguments(*args)

    class LoadFmdFile(PyCommand):
        """
        Command LoadFmdFile.

        Parameters
        ----------
        FilePath : str
        FileUnit : str
        Route : str
        JtLOD : str
        PartPerBody : bool
        PrefixParentName : bool
        RemoveEmptyParts : bool
        IgnoreSolidNames : bool
        Options : dict[str, Any]

        Returns
        -------
        bool
        """
        class _LoadFmdFileArguments(PyArguments):
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

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

            class _FileUnit(PyArgumentsTextualSubItem):
                """
                Argument FileUnit.
                """

            class _Route(PyArgumentsTextualSubItem):
                """
                Argument Route.
                """

            class _JtLOD(PyArgumentsTextualSubItem):
                """
                Argument JtLOD.
                """

            class _PartPerBody(PyArgumentsParameterSubItem):
                """
                Argument PartPerBody.
                """

            class _PrefixParentName(PyArgumentsParameterSubItem):
                """
                Argument PrefixParentName.
                """

            class _RemoveEmptyParts(PyArgumentsParameterSubItem):
                """
                Argument RemoveEmptyParts.
                """

            class _IgnoreSolidNames(PyArgumentsParameterSubItem):
                """
                Argument IgnoreSolidNames.
                """

            class _Options(PyArgumentsSingletonSubItem):
                """
                Argument Options.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyArgumentsParameterSubItem):
                    """
                    Argument Solid.
                    """

                class _Line(PyArgumentsParameterSubItem):
                    """
                    Argument Line.
                    """

                class _Surface(PyArgumentsParameterSubItem):
                    """
                    Argument Surface.
                    """

        def create_instance(self) -> _LoadFmdFileArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadFmdFileArguments(*args)

    class LoadTemplate(PyCommand):
        """
        Command LoadTemplate.

        Parameters
        ----------
        FilePath : str

        Returns
        -------
        bool
        """
        class _LoadTemplateArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

        def create_instance(self) -> _LoadTemplateArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadTemplateArguments(*args)

    class MoveCADComponentsToNewObject(PyCommand):
        """
        Command MoveCADComponentsToNewObject.

        Parameters
        ----------
        Paths : list[str]

        Returns
        -------
        bool
        """
        class _MoveCADComponentsToNewObjectArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyArgumentsTextualSubItem):
                """
                Argument Paths.
                """

        def create_instance(self) -> _MoveCADComponentsToNewObjectArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MoveCADComponentsToNewObjectArguments(*args)

    class MoveToNewSubobject(PyCommand):
        """
        Command MoveToNewSubobject.

        Parameters
        ----------
        Paths : list[str]

        Returns
        -------
        bool
        """
        class _MoveToNewSubobjectArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyArgumentsTextualSubItem):
                """
                Argument Paths.
                """

        def create_instance(self) -> _MoveToNewSubobjectArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MoveToNewSubobjectArguments(*args)

    class MoveToObject(PyCommand):
        """
        Command MoveToObject.

        Parameters
        ----------
        Paths : list[str]

        Returns
        -------
        bool
        """
        class _MoveToObjectArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Paths = self._Paths(self, "Paths", service, rules, path)

            class _Paths(PyArgumentsTextualSubItem):
                """
                Argument Paths.
                """

        def create_instance(self) -> _MoveToObjectArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MoveToObjectArguments(*args)

    class RedoAllTransforms(PyCommand):
        """
        Command RedoAllTransforms.


        Returns
        -------
        bool
        """
        class _RedoAllTransformsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _RedoAllTransformsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._RedoAllTransformsArguments(*args)

    class ResetTemplate(PyCommand):
        """
        Command ResetTemplate.


        Returns
        -------
        bool
        """
        class _ResetTemplateArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _ResetTemplateArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ResetTemplateArguments(*args)

    class SaveFmdFile(PyCommand):
        """
        Command SaveFmdFile.

        Parameters
        ----------
        FilePath : str

        Returns
        -------
        bool
        """
        class _SaveFmdFileArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

        def create_instance(self) -> _SaveFmdFileArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SaveFmdFileArguments(*args)

    class SaveTemplate(PyCommand):
        """
        Command SaveTemplate.

        Parameters
        ----------
        FilePath : str

        Returns
        -------
        bool
        """
        class _SaveTemplateArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FilePath = self._FilePath(self, "FilePath", service, rules, path)

            class _FilePath(PyArgumentsTextualSubItem):
                """
                Argument FilePath.
                """

        def create_instance(self) -> _SaveTemplateArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SaveTemplateArguments(*args)

    class UndoAllTransforms(PyCommand):
        """
        Command UndoAllTransforms.


        Returns
        -------
        bool
        """
        class _UndoAllTransformsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _UndoAllTransformsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UndoAllTransformsArguments(*args)

