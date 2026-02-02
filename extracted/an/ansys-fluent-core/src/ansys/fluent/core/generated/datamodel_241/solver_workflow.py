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
        self.CellZone = self.__class__.CellZone(service, rules, path + [("CellZone", "")])
        self.FaceZone = self.__class__.FaceZone(service, rules, path + [("FaceZone", "")])
        self.Zone = self.__class__.Zone(service, rules, path + [("Zone", "")])
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.ZoneList = self.__class__.ZoneList(service, rules, path + [("ZoneList", "")])
        self.JournalCommand = self.__class__.JournalCommand(service, rules, "JournalCommand", path)
        self.TWF_AssociateMesh = self.__class__.TWF_AssociateMesh(service, rules, "TWF_AssociateMesh", path)
        self.TWF_BasicMachineDescription = self.__class__.TWF_BasicMachineDescription(service, rules, "TWF_BasicMachineDescription", path)
        self.TWF_BladeRowAnalysisScope = self.__class__.TWF_BladeRowAnalysisScope(service, rules, "TWF_BladeRowAnalysisScope", path)
        self.TWF_CompleteWorkflowSetup = self.__class__.TWF_CompleteWorkflowSetup(service, rules, "TWF_CompleteWorkflowSetup", path)
        self.TWF_CreateCFDModel = self.__class__.TWF_CreateCFDModel(service, rules, "TWF_CreateCFDModel", path)
        self.TWF_ImportMesh = self.__class__.TWF_ImportMesh(service, rules, "TWF_ImportMesh", path)
        self.TWF_MapRegionInfo = self.__class__.TWF_MapRegionInfo(service, rules, "TWF_MapRegionInfo", path)
        self.TWF_ReportDefMonitors = self.__class__.TWF_ReportDefMonitors(service, rules, "TWF_ReportDefMonitors", path)
        self.TWF_TurboPhysics = self.__class__.TWF_TurboPhysics(service, rules, "TWF_TurboPhysics", path)
        self.TWF_TurboRegionsZones = self.__class__.TWF_TurboRegionsZones(service, rules, "TWF_TurboRegionsZones", path)
        self.TWF_TurboSurfaces = self.__class__.TWF_TurboSurfaces(service, rules, "TWF_TurboSurfaces", path)
        self.TWF_TurboTopology = self.__class__.TWF_TurboTopology(service, rules, "TWF_TurboTopology", path)
        super().__init__(service, rules, path)

    class CellZone(PyNamedObjectContainer):
        """
        .
        """
        class _CellZone(PyMenu):
            """
            Singleton _CellZone.
            """
            def __init__(self, service, rules, path):
                self.ChildZones = self.__class__.ChildZones(service, rules, path + [("ChildZones", "")])
                self.ConnectedFaces = self.__class__.ConnectedFaces(service, rules, path + [("ConnectedFaces", "")])
                self.NameInMesh = self.__class__.NameInMesh(service, rules, path + [("NameInMesh", "")])
                self.ParentZone = self.__class__.ParentZone(service, rules, path + [("ParentZone", "")])
                self.UnambiguousName = self.__class__.UnambiguousName(service, rules, path + [("UnambiguousName", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class ChildZones(PyTextual):
                """
                Parameter ChildZones of value type list[str].
                """
                pass

            class ConnectedFaces(PyTextual):
                """
                Parameter ConnectedFaces of value type list[str].
                """
                pass

            class NameInMesh(PyTextual):
                """
                Parameter NameInMesh of value type str.
                """
                pass

            class ParentZone(PyTextual):
                """
                Parameter ParentZone of value type str.
                """
                pass

            class UnambiguousName(PyTextual):
                """
                Parameter UnambiguousName of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _CellZone:
            return super().__getitem__(key)

    class FaceZone(PyNamedObjectContainer):
        """
        .
        """
        class _FaceZone(PyMenu):
            """
            Singleton _FaceZone.
            """
            def __init__(self, service, rules, path):
                self.ChildZones = self.__class__.ChildZones(service, rules, path + [("ChildZones", "")])
                self.NameInMesh = self.__class__.NameInMesh(service, rules, path + [("NameInMesh", "")])
                self.ParentZone = self.__class__.ParentZone(service, rules, path + [("ParentZone", "")])
                self.UnambiguousName = self.__class__.UnambiguousName(service, rules, path + [("UnambiguousName", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class ChildZones(PyTextual):
                """
                Parameter ChildZones of value type list[str].
                """
                pass

            class NameInMesh(PyTextual):
                """
                Parameter NameInMesh of value type str.
                """
                pass

            class ParentZone(PyTextual):
                """
                Parameter ParentZone of value type str.
                """
                pass

            class UnambiguousName(PyTextual):
                """
                Parameter UnambiguousName of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _FaceZone:
            return super().__getitem__(key)

    class Zone(PyNamedObjectContainer):
        """
        .
        """
        class _Zone(PyMenu):
            """
            Singleton _Zone.
            """
            def __init__(self, service, rules, path):
                self.ChildZones = self.__class__.ChildZones(service, rules, path + [("ChildZones", "")])
                self.NameInMesh = self.__class__.NameInMesh(service, rules, path + [("NameInMesh", "")])
                self.ParentZone = self.__class__.ParentZone(service, rules, path + [("ParentZone", "")])
                self.UnambiguousName = self.__class__.UnambiguousName(service, rules, path + [("UnambiguousName", "")])
                self._name_ = self.__class__._name_(service, rules, path + [("_name_", "")])
                super().__init__(service, rules, path)

            class ChildZones(PyTextual):
                """
                Parameter ChildZones of value type list[str].
                """
                pass

            class NameInMesh(PyTextual):
                """
                Parameter NameInMesh of value type str.
                """
                pass

            class ParentZone(PyTextual):
                """
                Parameter ParentZone of value type str.
                """
                pass

            class UnambiguousName(PyTextual):
                """
                Parameter UnambiguousName of value type str.
                """
                pass

            class _name_(PyTextual):
                """
                Parameter _name_ of value type str.
                """
                pass

        def __getitem__(self, key: str) -> _Zone:
            return super().__getitem__(key)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.EnableTurboMeshing = self.__class__.EnableTurboMeshing(service, rules, path + [("EnableTurboMeshing", "")])
            super().__init__(service, rules, path)

        class EnableTurboMeshing(PyParameter):
            """
            Parameter EnableTurboMeshing of value type bool.
            """
            pass

    class ZoneList(PyMenu):
        """
        Singleton ZoneList.
        """
        def __init__(self, service, rules, path):
            self.CellZones = self.__class__.CellZones(service, rules, path + [("CellZones", "")])
            self.FaceZones = self.__class__.FaceZones(service, rules, path + [("FaceZones", "")])
            super().__init__(service, rules, path)

        class CellZones(PyTextual):
            """
            Parameter CellZones of value type list[str].
            """
            pass

        class FaceZones(PyTextual):
            """
            Parameter FaceZones of value type list[str].
            """
            pass

    class JournalCommand(PyCommand):
        """
        Command JournalCommand.

        Parameters
        ----------
        JournalString : str
        PythonJournal : bool

        Returns
        -------
        bool
        """
        class _JournalCommandArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.JournalString = self._JournalString(self, "JournalString", service, rules, path)
                self.PythonJournal = self._PythonJournal(self, "PythonJournal", service, rules, path)

            class _JournalString(PyArgumentsTextualSubItem):
                """
                Argument JournalString.
                """

            class _PythonJournal(PyArgumentsParameterSubItem):
                """
                Argument PythonJournal.
                """

        def create_instance(self) -> _JournalCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._JournalCommandArguments(*args)

    class TWF_AssociateMesh(PyCommand):
        """
        Command TWF_AssociateMesh.

        Parameters
        ----------
        AMChildName : str
        AMSelectComponentScope : str
        UseWireframe : bool
        RenameCellZones : str
        DefaultAMRowNumList : list[str]
        DefaultAMCellZonesList : list[str]
        AMRowNumList : list[str]
        OldAMCellZonesList : list[str]
        NewAMCellZonesList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_AssociateMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AMChildName = self._AMChildName(self, "AMChildName", service, rules, path)
                self.AMSelectComponentScope = self._AMSelectComponentScope(self, "AMSelectComponentScope", service, rules, path)
                self.UseWireframe = self._UseWireframe(self, "UseWireframe", service, rules, path)
                self.RenameCellZones = self._RenameCellZones(self, "RenameCellZones", service, rules, path)
                self.DefaultAMRowNumList = self._DefaultAMRowNumList(self, "DefaultAMRowNumList", service, rules, path)
                self.DefaultAMCellZonesList = self._DefaultAMCellZonesList(self, "DefaultAMCellZonesList", service, rules, path)
                self.AMRowNumList = self._AMRowNumList(self, "AMRowNumList", service, rules, path)
                self.OldAMCellZonesList = self._OldAMCellZonesList(self, "OldAMCellZonesList", service, rules, path)
                self.NewAMCellZonesList = self._NewAMCellZonesList(self, "NewAMCellZonesList", service, rules, path)

            class _AMChildName(PyArgumentsTextualSubItem):
                """
                Argument AMChildName.
                """

            class _AMSelectComponentScope(PyArgumentsTextualSubItem):
                """
                Argument AMSelectComponentScope.
                """

            class _UseWireframe(PyArgumentsParameterSubItem):
                """
                Argument UseWireframe.
                """

            class _RenameCellZones(PyArgumentsTextualSubItem):
                """
                Argument RenameCellZones.
                """

            class _DefaultAMRowNumList(PyArgumentsTextualSubItem):
                """
                Argument DefaultAMRowNumList.
                """

            class _DefaultAMCellZonesList(PyArgumentsTextualSubItem):
                """
                Argument DefaultAMCellZonesList.
                """

            class _AMRowNumList(PyArgumentsTextualSubItem):
                """
                Argument AMRowNumList.
                """

            class _OldAMCellZonesList(PyArgumentsTextualSubItem):
                """
                Argument OldAMCellZonesList.
                """

            class _NewAMCellZonesList(PyArgumentsTextualSubItem):
                """
                Argument NewAMCellZonesList.
                """

        def create_instance(self) -> _TWF_AssociateMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_AssociateMeshArguments(*args)

    class TWF_BasicMachineDescription(PyCommand):
        """
        Command TWF_BasicMachineDescription.

        Parameters
        ----------
        ComponentType : str
        ComponentName : str
        NumRows : int
        RowNumList : list[str]
        OldRowNameList : list[str]
        NewRowNameList : list[str]
        OldRowTypeList : list[str]
        NewRowTypeList : list[str]
        OldNumOfBladesList : list[str]
        NewNumOfBladesList : list[str]
        OldEnableTipGapList : list[str]
        NewEnableTipGapList : list[str]
        CombustorType : str

        Returns
        -------
        bool
        """
        class _TWF_BasicMachineDescriptionArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ComponentType = self._ComponentType(self, "ComponentType", service, rules, path)
                self.ComponentName = self._ComponentName(self, "ComponentName", service, rules, path)
                self.NumRows = self._NumRows(self, "NumRows", service, rules, path)
                self.RowNumList = self._RowNumList(self, "RowNumList", service, rules, path)
                self.OldRowNameList = self._OldRowNameList(self, "OldRowNameList", service, rules, path)
                self.NewRowNameList = self._NewRowNameList(self, "NewRowNameList", service, rules, path)
                self.OldRowTypeList = self._OldRowTypeList(self, "OldRowTypeList", service, rules, path)
                self.NewRowTypeList = self._NewRowTypeList(self, "NewRowTypeList", service, rules, path)
                self.OldNumOfBladesList = self._OldNumOfBladesList(self, "OldNumOfBladesList", service, rules, path)
                self.NewNumOfBladesList = self._NewNumOfBladesList(self, "NewNumOfBladesList", service, rules, path)
                self.OldEnableTipGapList = self._OldEnableTipGapList(self, "OldEnableTipGapList", service, rules, path)
                self.NewEnableTipGapList = self._NewEnableTipGapList(self, "NewEnableTipGapList", service, rules, path)
                self.CombustorType = self._CombustorType(self, "CombustorType", service, rules, path)

            class _ComponentType(PyArgumentsTextualSubItem):
                """
                Argument ComponentType.
                """

            class _ComponentName(PyArgumentsTextualSubItem):
                """
                Argument ComponentName.
                """

            class _NumRows(PyArgumentsNumericalSubItem):
                """
                Argument NumRows.
                """

            class _RowNumList(PyArgumentsTextualSubItem):
                """
                Argument RowNumList.
                """

            class _OldRowNameList(PyArgumentsTextualSubItem):
                """
                Argument OldRowNameList.
                """

            class _NewRowNameList(PyArgumentsTextualSubItem):
                """
                Argument NewRowNameList.
                """

            class _OldRowTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldRowTypeList.
                """

            class _NewRowTypeList(PyArgumentsTextualSubItem):
                """
                Argument NewRowTypeList.
                """

            class _OldNumOfBladesList(PyArgumentsTextualSubItem):
                """
                Argument OldNumOfBladesList.
                """

            class _NewNumOfBladesList(PyArgumentsTextualSubItem):
                """
                Argument NewNumOfBladesList.
                """

            class _OldEnableTipGapList(PyArgumentsTextualSubItem):
                """
                Argument OldEnableTipGapList.
                """

            class _NewEnableTipGapList(PyArgumentsTextualSubItem):
                """
                Argument NewEnableTipGapList.
                """

            class _CombustorType(PyArgumentsTextualSubItem):
                """
                Argument CombustorType.
                """

        def create_instance(self) -> _TWF_BasicMachineDescriptionArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_BasicMachineDescriptionArguments(*args)

    class TWF_BladeRowAnalysisScope(PyCommand):
        """
        Command TWF_BladeRowAnalysisScope.

        Parameters
        ----------
        ASChildName : str
        ASSelectComponent : str
        ASRowNumList : list[str]
        OldASIncludeRowList : list[str]
        NewASIncludeRowList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_BladeRowAnalysisScopeArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ASChildName = self._ASChildName(self, "ASChildName", service, rules, path)
                self.ASSelectComponent = self._ASSelectComponent(self, "ASSelectComponent", service, rules, path)
                self.ASRowNumList = self._ASRowNumList(self, "ASRowNumList", service, rules, path)
                self.OldASIncludeRowList = self._OldASIncludeRowList(self, "OldASIncludeRowList", service, rules, path)
                self.NewASIncludeRowList = self._NewASIncludeRowList(self, "NewASIncludeRowList", service, rules, path)

            class _ASChildName(PyArgumentsTextualSubItem):
                """
                Argument ASChildName.
                """

            class _ASSelectComponent(PyArgumentsTextualSubItem):
                """
                Argument ASSelectComponent.
                """

            class _ASRowNumList(PyArgumentsTextualSubItem):
                """
                Argument ASRowNumList.
                """

            class _OldASIncludeRowList(PyArgumentsTextualSubItem):
                """
                Argument OldASIncludeRowList.
                """

            class _NewASIncludeRowList(PyArgumentsTextualSubItem):
                """
                Argument NewASIncludeRowList.
                """

        def create_instance(self) -> _TWF_BladeRowAnalysisScopeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_BladeRowAnalysisScopeArguments(*args)

    class TWF_CompleteWorkflowSetup(PyCommand):
        """
        Command TWF_CompleteWorkflowSetup.


        Returns
        -------
        bool
        """
        class _TWF_CompleteWorkflowSetupArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _TWF_CompleteWorkflowSetupArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_CompleteWorkflowSetupArguments(*args)

    class TWF_CreateCFDModel(PyCommand):
        """
        Command TWF_CreateCFDModel.

        Parameters
        ----------
        CFDMChildName : str
        CFDMSelectMeshAssociation : str
        AxisOfRotation : str
        DelayCFDModelCreation : bool
        RestrictToFactors : bool
        EstimateNumBlades : bool
        CFDMRowNumList : list[str]
        OldCFDMNumOfBladesList : list[str]
        NewCFDMNumOfBladesList : list[str]
        OldCFDMModelBladesList : list[str]
        NewCFDMModelBladesList : list[str]
        OldCFDMAngleOffset : list[str]
        NewCFDMAngleOffset : list[str]
        OldCFDMBladesPerSectorList : list[str]
        NewCFDMBladesPerSectorList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_CreateCFDModelArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.CFDMChildName = self._CFDMChildName(self, "CFDMChildName", service, rules, path)
                self.CFDMSelectMeshAssociation = self._CFDMSelectMeshAssociation(self, "CFDMSelectMeshAssociation", service, rules, path)
                self.AxisOfRotation = self._AxisOfRotation(self, "AxisOfRotation", service, rules, path)
                self.DelayCFDModelCreation = self._DelayCFDModelCreation(self, "DelayCFDModelCreation", service, rules, path)
                self.RestrictToFactors = self._RestrictToFactors(self, "RestrictToFactors", service, rules, path)
                self.EstimateNumBlades = self._EstimateNumBlades(self, "EstimateNumBlades", service, rules, path)
                self.CFDMRowNumList = self._CFDMRowNumList(self, "CFDMRowNumList", service, rules, path)
                self.OldCFDMNumOfBladesList = self._OldCFDMNumOfBladesList(self, "OldCFDMNumOfBladesList", service, rules, path)
                self.NewCFDMNumOfBladesList = self._NewCFDMNumOfBladesList(self, "NewCFDMNumOfBladesList", service, rules, path)
                self.OldCFDMModelBladesList = self._OldCFDMModelBladesList(self, "OldCFDMModelBladesList", service, rules, path)
                self.NewCFDMModelBladesList = self._NewCFDMModelBladesList(self, "NewCFDMModelBladesList", service, rules, path)
                self.OldCFDMAngleOffset = self._OldCFDMAngleOffset(self, "OldCFDMAngleOffset", service, rules, path)
                self.NewCFDMAngleOffset = self._NewCFDMAngleOffset(self, "NewCFDMAngleOffset", service, rules, path)
                self.OldCFDMBladesPerSectorList = self._OldCFDMBladesPerSectorList(self, "OldCFDMBladesPerSectorList", service, rules, path)
                self.NewCFDMBladesPerSectorList = self._NewCFDMBladesPerSectorList(self, "NewCFDMBladesPerSectorList", service, rules, path)

            class _CFDMChildName(PyArgumentsTextualSubItem):
                """
                Argument CFDMChildName.
                """

            class _CFDMSelectMeshAssociation(PyArgumentsTextualSubItem):
                """
                Argument CFDMSelectMeshAssociation.
                """

            class _AxisOfRotation(PyArgumentsTextualSubItem):
                """
                Argument AxisOfRotation.
                """

            class _DelayCFDModelCreation(PyArgumentsParameterSubItem):
                """
                Argument DelayCFDModelCreation.
                """

            class _RestrictToFactors(PyArgumentsParameterSubItem):
                """
                Argument RestrictToFactors.
                """

            class _EstimateNumBlades(PyArgumentsParameterSubItem):
                """
                Argument EstimateNumBlades.
                """

            class _CFDMRowNumList(PyArgumentsTextualSubItem):
                """
                Argument CFDMRowNumList.
                """

            class _OldCFDMNumOfBladesList(PyArgumentsTextualSubItem):
                """
                Argument OldCFDMNumOfBladesList.
                """

            class _NewCFDMNumOfBladesList(PyArgumentsTextualSubItem):
                """
                Argument NewCFDMNumOfBladesList.
                """

            class _OldCFDMModelBladesList(PyArgumentsTextualSubItem):
                """
                Argument OldCFDMModelBladesList.
                """

            class _NewCFDMModelBladesList(PyArgumentsTextualSubItem):
                """
                Argument NewCFDMModelBladesList.
                """

            class _OldCFDMAngleOffset(PyArgumentsTextualSubItem):
                """
                Argument OldCFDMAngleOffset.
                """

            class _NewCFDMAngleOffset(PyArgumentsTextualSubItem):
                """
                Argument NewCFDMAngleOffset.
                """

            class _OldCFDMBladesPerSectorList(PyArgumentsTextualSubItem):
                """
                Argument OldCFDMBladesPerSectorList.
                """

            class _NewCFDMBladesPerSectorList(PyArgumentsTextualSubItem):
                """
                Argument NewCFDMBladesPerSectorList.
                """

        def create_instance(self) -> _TWF_CreateCFDModelArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_CreateCFDModelArguments(*args)

    class TWF_ImportMesh(PyCommand):
        """
        Command TWF_ImportMesh.

        Parameters
        ----------
        AddChild : str
        MeshFilePath : str
        MeshFilePath_old : str
        MeshName : str
        CellZoneNames : list[str]
        ListItemLevels : list[str]
        ListItemTitles : list[str]
        ListOfCellZones : str
        CellZones : list[str]

        Returns
        -------
        bool
        """
        class _TWF_ImportMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.MeshFilePath = self._MeshFilePath(self, "MeshFilePath", service, rules, path)
                self.MeshFilePath_old = self._MeshFilePath_old(self, "MeshFilePath_old", service, rules, path)
                self.MeshName = self._MeshName(self, "MeshName", service, rules, path)
                self.CellZoneNames = self._CellZoneNames(self, "CellZoneNames", service, rules, path)
                self.ListItemLevels = self._ListItemLevels(self, "ListItemLevels", service, rules, path)
                self.ListItemTitles = self._ListItemTitles(self, "ListItemTitles", service, rules, path)
                self.ListOfCellZones = self._ListOfCellZones(self, "ListOfCellZones", service, rules, path)
                self.CellZones = self._CellZones(self, "CellZones", service, rules, path)

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Argument AddChild.
                """

            class _MeshFilePath(PyArgumentsTextualSubItem):
                """
                Argument MeshFilePath.
                """

            class _MeshFilePath_old(PyArgumentsTextualSubItem):
                """
                Argument MeshFilePath_old.
                """

            class _MeshName(PyArgumentsTextualSubItem):
                """
                Argument MeshName.
                """

            class _CellZoneNames(PyArgumentsTextualSubItem):
                """
                Argument CellZoneNames.
                """

            class _ListItemLevels(PyArgumentsTextualSubItem):
                """
                Argument ListItemLevels.
                """

            class _ListItemTitles(PyArgumentsTextualSubItem):
                """
                Argument ListItemTitles.
                """

            class _ListOfCellZones(PyArgumentsTextualSubItem):
                """
                Argument ListOfCellZones.
                """

            class _CellZones(PyArgumentsTextualSubItem):
                """
                Argument CellZones.
                """

        def create_instance(self) -> _TWF_ImportMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_ImportMeshArguments(*args)

    class TWF_MapRegionInfo(PyCommand):
        """
        Command TWF_MapRegionInfo.

        Parameters
        ----------
        MRChildName : str
        MRSelectCellZone : str
        UseWireframe : bool
        DefaultMRRegionNameList : list[str]
        DefaultMRFaceZoneList : list[str]
        MRRegionNameList : list[str]
        OldMRFaceZoneList : list[str]
        NewMRFaceZoneList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_MapRegionInfoArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MRChildName = self._MRChildName(self, "MRChildName", service, rules, path)
                self.MRSelectCellZone = self._MRSelectCellZone(self, "MRSelectCellZone", service, rules, path)
                self.UseWireframe = self._UseWireframe(self, "UseWireframe", service, rules, path)
                self.DefaultMRRegionNameList = self._DefaultMRRegionNameList(self, "DefaultMRRegionNameList", service, rules, path)
                self.DefaultMRFaceZoneList = self._DefaultMRFaceZoneList(self, "DefaultMRFaceZoneList", service, rules, path)
                self.MRRegionNameList = self._MRRegionNameList(self, "MRRegionNameList", service, rules, path)
                self.OldMRFaceZoneList = self._OldMRFaceZoneList(self, "OldMRFaceZoneList", service, rules, path)
                self.NewMRFaceZoneList = self._NewMRFaceZoneList(self, "NewMRFaceZoneList", service, rules, path)

            class _MRChildName(PyArgumentsTextualSubItem):
                """
                Argument MRChildName.
                """

            class _MRSelectCellZone(PyArgumentsTextualSubItem):
                """
                Argument MRSelectCellZone.
                """

            class _UseWireframe(PyArgumentsParameterSubItem):
                """
                Argument UseWireframe.
                """

            class _DefaultMRRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument DefaultMRRegionNameList.
                """

            class _DefaultMRFaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument DefaultMRFaceZoneList.
                """

            class _MRRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument MRRegionNameList.
                """

            class _OldMRFaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument OldMRFaceZoneList.
                """

            class _NewMRFaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument NewMRFaceZoneList.
                """

        def create_instance(self) -> _TWF_MapRegionInfoArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_MapRegionInfoArguments(*args)

    class TWF_ReportDefMonitors(PyCommand):
        """
        Command TWF_ReportDefMonitors.

        Parameters
        ----------
        RDIsoSurfaceNumList : list[str]
        OldCreateContourList : list[str]
        NewCreateContourList : list[str]
        TurboContoursList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_ReportDefMonitorsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RDIsoSurfaceNumList = self._RDIsoSurfaceNumList(self, "RDIsoSurfaceNumList", service, rules, path)
                self.OldCreateContourList = self._OldCreateContourList(self, "OldCreateContourList", service, rules, path)
                self.NewCreateContourList = self._NewCreateContourList(self, "NewCreateContourList", service, rules, path)
                self.TurboContoursList = self._TurboContoursList(self, "TurboContoursList", service, rules, path)

            class _RDIsoSurfaceNumList(PyArgumentsTextualSubItem):
                """
                Argument RDIsoSurfaceNumList.
                """

            class _OldCreateContourList(PyArgumentsTextualSubItem):
                """
                Argument OldCreateContourList.
                """

            class _NewCreateContourList(PyArgumentsTextualSubItem):
                """
                Argument NewCreateContourList.
                """

            class _TurboContoursList(PyArgumentsTextualSubItem):
                """
                Argument TurboContoursList.
                """

        def create_instance(self) -> _TWF_ReportDefMonitorsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_ReportDefMonitorsArguments(*args)

    class TWF_TurboPhysics(PyCommand):
        """
        Command TWF_TurboPhysics.

        Parameters
        ----------
        States : dict[str, Any]

        Returns
        -------
        bool
        """
        class _TWF_TurboPhysicsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.States = self._States(self, "States", service, rules, path)

            class _States(PyArgumentsSingletonSubItem):
                """
                Argument States.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Density = self._Density(self, "Density", service, rules, path)
                    self.EFM = self._EFM(self, "EFM", service, rules, path)
                    self.Energy = self._Energy(self, "Energy", service, rules, path)
                    self.CEBtn = self._CEBtn(self, "CEBtn", service, rules, path)
                    self.WF = self._WF(self, "WF", service, rules, path)
                    self.OpP = self._OpP(self, "OpP", service, rules, path)
                    self.Vrpm = self._Vrpm(self, "Vrpm", service, rules, path)

                class _Density(PyArgumentsNumericalSubItem):
                    """
                    Argument Density.
                    """

                class _EFM(PyArgumentsTextualSubItem):
                    """
                    Argument EFM.
                    """

                class _Energy(PyArgumentsParameterSubItem):
                    """
                    Argument Energy.
                    """

                class _CEBtn(PyArgumentsParameterSubItem):
                    """
                    Argument CEBtn.
                    """

                class _WF(PyArgumentsTextualSubItem):
                    """
                    Argument WF.
                    """

                class _OpP(PyArgumentsNumericalSubItem):
                    """
                    Argument OpP.
                    """

                class _Vrpm(PyArgumentsNumericalSubItem):
                    """
                    Argument Vrpm.
                    """

        def create_instance(self) -> _TWF_TurboPhysicsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_TurboPhysicsArguments(*args)

    class TWF_TurboRegionsZones(PyCommand):
        """
        Command TWF_TurboRegionsZones.

        Parameters
        ----------
        States : dict[str, Any]

        Returns
        -------
        bool
        """
        class _TWF_TurboRegionsZonesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.States = self._States(self, "States", service, rules, path)

            class _States(PyArgumentsSingletonSubItem):
                """
                Argument States.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.UseUndo = self._UseUndo(self, "UseUndo", service, rules, path)
                    self.UndoOperationsLog = self._UndoOperationsLog(self, "UndoOperationsLog", service, rules, path)

                class _UseUndo(PyArgumentsParameterSubItem):
                    """
                    Argument UseUndo.
                    """

                class _UndoOperationsLog(PyArgumentsTextualSubItem):
                    """
                    Argument UndoOperationsLog.
                    """

        def create_instance(self) -> _TWF_TurboRegionsZonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_TurboRegionsZonesArguments(*args)

    class TWF_TurboSurfaces(PyCommand):
        """
        Command TWF_TurboSurfaces.

        Parameters
        ----------
        NumIsoSurfaces : int
        IsoSurfaceNumList : list[str]
        OldIsoSurfaceNameList : list[str]
        NewIsoSurfaceNameList : list[str]
        OldIsoSurfaceValueList : list[str]
        NewIsoSurfaceValueList : list[str]
        SurfacesList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_TurboSurfacesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.NumIsoSurfaces = self._NumIsoSurfaces(self, "NumIsoSurfaces", service, rules, path)
                self.IsoSurfaceNumList = self._IsoSurfaceNumList(self, "IsoSurfaceNumList", service, rules, path)
                self.OldIsoSurfaceNameList = self._OldIsoSurfaceNameList(self, "OldIsoSurfaceNameList", service, rules, path)
                self.NewIsoSurfaceNameList = self._NewIsoSurfaceNameList(self, "NewIsoSurfaceNameList", service, rules, path)
                self.OldIsoSurfaceValueList = self._OldIsoSurfaceValueList(self, "OldIsoSurfaceValueList", service, rules, path)
                self.NewIsoSurfaceValueList = self._NewIsoSurfaceValueList(self, "NewIsoSurfaceValueList", service, rules, path)
                self.SurfacesList = self._SurfacesList(self, "SurfacesList", service, rules, path)

            class _NumIsoSurfaces(PyArgumentsNumericalSubItem):
                """
                Argument NumIsoSurfaces.
                """

            class _IsoSurfaceNumList(PyArgumentsTextualSubItem):
                """
                Argument IsoSurfaceNumList.
                """

            class _OldIsoSurfaceNameList(PyArgumentsTextualSubItem):
                """
                Argument OldIsoSurfaceNameList.
                """

            class _NewIsoSurfaceNameList(PyArgumentsTextualSubItem):
                """
                Argument NewIsoSurfaceNameList.
                """

            class _OldIsoSurfaceValueList(PyArgumentsTextualSubItem):
                """
                Argument OldIsoSurfaceValueList.
                """

            class _NewIsoSurfaceValueList(PyArgumentsTextualSubItem):
                """
                Argument NewIsoSurfaceValueList.
                """

            class _SurfacesList(PyArgumentsTextualSubItem):
                """
                Argument SurfacesList.
                """

        def create_instance(self) -> _TWF_TurboSurfacesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_TurboSurfacesArguments(*args)

    class TWF_TurboTopology(PyCommand):
        """
        Command TWF_TurboTopology.

        Parameters
        ----------
        TopologyName : str
        UseWireframe : bool
        DefaultTopologyNameList : list[str]
        DefaultTopologyZoneList : list[str]
        TopologyNameList : list[str]
        OldTopologyZoneList : list[str]
        NewTopologyZoneList : list[str]

        Returns
        -------
        bool
        """
        class _TWF_TurboTopologyArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.TopologyName = self._TopologyName(self, "TopologyName", service, rules, path)
                self.UseWireframe = self._UseWireframe(self, "UseWireframe", service, rules, path)
                self.DefaultTopologyNameList = self._DefaultTopologyNameList(self, "DefaultTopologyNameList", service, rules, path)
                self.DefaultTopologyZoneList = self._DefaultTopologyZoneList(self, "DefaultTopologyZoneList", service, rules, path)
                self.TopologyNameList = self._TopologyNameList(self, "TopologyNameList", service, rules, path)
                self.OldTopologyZoneList = self._OldTopologyZoneList(self, "OldTopologyZoneList", service, rules, path)
                self.NewTopologyZoneList = self._NewTopologyZoneList(self, "NewTopologyZoneList", service, rules, path)

            class _TopologyName(PyArgumentsTextualSubItem):
                """
                Argument TopologyName.
                """

            class _UseWireframe(PyArgumentsParameterSubItem):
                """
                Argument UseWireframe.
                """

            class _DefaultTopologyNameList(PyArgumentsTextualSubItem):
                """
                Argument DefaultTopologyNameList.
                """

            class _DefaultTopologyZoneList(PyArgumentsTextualSubItem):
                """
                Argument DefaultTopologyZoneList.
                """

            class _TopologyNameList(PyArgumentsTextualSubItem):
                """
                Argument TopologyNameList.
                """

            class _OldTopologyZoneList(PyArgumentsTextualSubItem):
                """
                Argument OldTopologyZoneList.
                """

            class _NewTopologyZoneList(PyArgumentsTextualSubItem):
                """
                Argument NewTopologyZoneList.
                """

        def create_instance(self) -> _TWF_TurboTopologyArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_TurboTopologyArguments(*args)

