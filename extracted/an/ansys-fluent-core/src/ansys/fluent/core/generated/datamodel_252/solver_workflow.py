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
        Use this task to associate each cell zone from the imported mesh file(s) with the corresponding row.
        Parameters
        ----------
        AMChildName : str
        AMSelectComponentScope : str
        UseWireframe : bool
            Toggle the display of the model in wireframe.
        RenameCellZones : str
            Determines how your zones names appear once this task is complete, depending on your preferences. When set to Yes, using row names, this field will change the associated cell (or face) zone name according to the corresponding Name. When set to Yes, using row numbers, this field will change the associated cell (or face) zone name according to the corresponding Row number. You can also choose No to keep the zone names as they are.
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
                Toggle the display of the model in wireframe.
                """

            class _RenameCellZones(PyArgumentsTextualSubItem):
                """
                Determines how your zones names appear once this task is complete, depending on your preferences. When set to Yes, using row names, this field will change the associated cell (or face) zone name according to the corresponding Name. When set to Yes, using row numbers, this field will change the associated cell (or face) zone name according to the corresponding Row number. You can also choose No to keep the zone names as they are.
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
        This task gathers physical information about the turbomachine such as the machine type (axial compressor or turbine, radial compressor or turbine), the number of blade rows in the machine, and the number of blades in each row, and whether or not there is a tip gap. You must also specify the rotating and stationary blade rows.  More...
        Parameters
        ----------
        ComponentType : str
            Specify the type of machine component: either an Axial Turbine, Axial Compressor, a Radial Turbine, or a Radial Compressor.
        ComponentName : str
            Specify a name for the component, or use the default value.
        NumRows : int
            Specify the number of rows for the component. For each row, use the table to provide a Name, a Type (stationary or rotating), the Number of Blades, and whether or not there is a tip gap present (spacing between the blade and the hub/shroud).
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
                Specify the type of machine component: either an Axial Turbine, Axial Compressor, a Radial Turbine, or a Radial Compressor.
                """

            class _ComponentName(PyArgumentsTextualSubItem):
                """
                Specify a name for the component, or use the default value.
                """

            class _NumRows(PyArgumentsNumericalSubItem):
                """
                Specify the number of rows for the component. For each row, use the table to provide a Name, a Type (stationary or rotating), the Number of Blades, and whether or not there is a tip gap present (spacing between the blade and the hub/shroud).
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
        Use this task to specify which rows are included in the CFD analysis. You must define a single contiguous set of rows. Indicate whether or not to include or exclude the row. The analysis scope can include all the rows defined in the Component Description task or a portion of it. Review the information in the table, and make any changes as needed.  More...
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
        Use this task to formally create the CFD model. For each blade row, specify the number of modeled passages (or sectors) per row. Make sure to first specify the Axis of Rotation. Use the graphics window to visually verify and ensure the CFD model is constructed properly.
        Parameters
        ----------
        CFDMChildName : str
        CFDMSelectMeshAssociation : str
        AxisOfRotation : str
            Specify the rotational axis for the generated CFD turbomachine geometry.
        DelayCFDModelCreation : bool
        RestrictToFactors : bool
            Choose whether or not to restrict the number of model blade sectors to a factor of the number of blades.
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
                Specify the rotational axis for the generated CFD turbomachine geometry.
                """

            class _DelayCFDModelCreation(PyArgumentsParameterSubItem):
                """
                Argument DelayCFDModelCreation.
                """

            class _RestrictToFactors(PyArgumentsParameterSubItem):
                """
                Choose whether or not to restrict the number of model blade sectors to a factor of the number of blades.
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
        Use this task to supply the mesh for the row you wish to include in the CFD model. You can import a single mesh file that includes all of the rows/passages/blades, or import multiple mesh files that represent each passage/blade.
        Parameters
        ----------
        AddChild : str
        MeshFilePath : str
            Specify the name and location of a single mesh file that includes all the zones, or import multiple mesh files that represent each zone. Standard Ansys mesh file types are supported, including .msh, .msh.h5, .def, .cgns, and .gtm.
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
                Specify the name and location of a single mesh file that includes all the zones, or import multiple mesh files that represent each zone. Standard Ansys mesh file types are supported, including .msh, .msh.h5, .def, .cgns, and .gtm.
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
        Use this task to ensure that, for each cell zone, the face zones correspond to the correct passage region. Use the table to check the associations, or make changes as needed.
        Parameters
        ----------
        MRChildName : str
        MRSelectCellZone : str
            Select a cell zone for which you wish to review associations.
        UseWireframe : bool
            In order to more easily visualize highlighted items, use this option to display the 3D wireframe representation of the CFD model in the graphics window.
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
                Select a cell zone for which you wish to review associations.
                """

            class _UseWireframe(PyArgumentsParameterSubItem):
                """
                In order to more easily visualize highlighted items, use this option to display the 3D wireframe representation of the CFD model in the graphics window.
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
        In this task, determine whether or not you want this task to create contour plots of the iso-surfaces you defined as part of the Define Turbo Surfaces task. In addition, once complete, the workflow will have Fluent automatically create performance parameters such as flow rate, pressure-ratio, efficiency, and so on.
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
        Use this task to specify the turbo-related physics for the machine, such as the rotational speed, operating pressure, and the working fluid.
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
                    Provide a value for the density of air, or use the default value.
                    """

                class _EFM(PyArgumentsTextualSubItem):
                    """
                    Displays the current existing fluid assigned to the CFD model. Use the Create/Edit... button to create your own material, or edit other existing materials.
                    """

                class _Energy(PyArgumentsParameterSubItem):
                    """
                    Indicates whether or not temperature conditions are to be considered.
                    """

                class _CEBtn(PyArgumentsParameterSubItem):
                    """
                    Argument CEBtn.
                    """

                class _WF(PyArgumentsTextualSubItem):
                    """
                    Choose one of the following materials as the working fluid for the CFD model.
                    """

                class _OpP(PyArgumentsNumericalSubItem):
                    """
                    Specify the operating pressure, or keep the default value.
                    """

                class _Vrpm(PyArgumentsNumericalSubItem):
                    """
                    Specify the rotation speed, or keep the default value.
                    """

        def create_instance(self) -> _TWF_TurboPhysicsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TWF_TurboPhysicsArguments(*args)

    class TWF_TurboRegionsZones(PyCommand):
        """
        Use this task to specify the main path inflow and outflow operating conditions. By default, zones are merged to simplify boundary condition input and based on the target turbo model requirements.
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
        Use this task to create turbo surfaces at span-wise locations that will be used in solution post processing. By default, the locations will be at 0.25, 0.5, and 0.75.
        Parameters
        ----------
        NumIsoSurfaces : int
            Specify the number of turbo iso-surfaces you want to create, or keep the default value of 3.
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
                Specify the number of turbo iso-surfaces you want to create, or keep the default value of 3.
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
        Use this task so that Ansys Fluent can compute the turbo coordinates the machine main path inflow and outflow, the hub and shroud, and the side boundaries should be associated.
        Parameters
        ----------
        TopologyName : str
            Provide a name for the turbo topology, or use the default name.
        AddChild : str
        UseWireframe : bool
            In order to more easily visualize highlighted items, use this option to display the 3D wireframe representation of the turbo topology model in the graphics window.
        SkipTurboTopology : bool
            Use this task so that Ansys Fluent can compute the turbo coordinates the machine main path inflow and outflow, the hub and shroud, and the side boundaries should be associated.
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
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.UseWireframe = self._UseWireframe(self, "UseWireframe", service, rules, path)
                self.SkipTurboTopology = self._SkipTurboTopology(self, "SkipTurboTopology", service, rules, path)
                self.DefaultTopologyNameList = self._DefaultTopologyNameList(self, "DefaultTopologyNameList", service, rules, path)
                self.DefaultTopologyZoneList = self._DefaultTopologyZoneList(self, "DefaultTopologyZoneList", service, rules, path)
                self.TopologyNameList = self._TopologyNameList(self, "TopologyNameList", service, rules, path)
                self.OldTopologyZoneList = self._OldTopologyZoneList(self, "OldTopologyZoneList", service, rules, path)
                self.NewTopologyZoneList = self._NewTopologyZoneList(self, "NewTopologyZoneList", service, rules, path)

            class _TopologyName(PyArgumentsTextualSubItem):
                """
                Provide a name for the turbo topology, or use the default name.
                """

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Argument AddChild.
                """

            class _UseWireframe(PyArgumentsParameterSubItem):
                """
                In order to more easily visualize highlighted items, use this option to display the 3D wireframe representation of the turbo topology model in the graphics window.
                """

            class _SkipTurboTopology(PyArgumentsParameterSubItem):
                """
                Use this task so that Ansys Fluent can compute the turbo coordinates the machine main path inflow and outflow, the hub and shroud, and the side boundaries should be associated.
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

