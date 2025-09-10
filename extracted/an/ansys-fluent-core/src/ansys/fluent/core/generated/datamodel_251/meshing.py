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
    Singleton Root.
    """
    def __init__(self, service, rules, path):
        self.Diagnostics = self.__class__.Diagnostics(service, rules, path + [("Diagnostics", "")])
        self.File = self.__class__.File(service, rules, path + [("File", "")])
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.Graphics = self.__class__.Graphics(service, rules, path + [("Graphics", "")])
        self.Add2DBoundaryLayers = self.__class__.Add2DBoundaryLayers(service, rules, "Add2DBoundaryLayers", path)
        self.AddBoundaryLayers = self.__class__.AddBoundaryLayers(service, rules, "AddBoundaryLayers", path)
        self.AddBoundaryLayersForPartReplacement = self.__class__.AddBoundaryLayersForPartReplacement(service, rules, "AddBoundaryLayersForPartReplacement", path)
        self.AddBoundaryType = self.__class__.AddBoundaryType(service, rules, "AddBoundaryType", path)
        self.AddLocalSizingFTM = self.__class__.AddLocalSizingFTM(service, rules, "AddLocalSizingFTM", path)
        self.AddLocalSizingWTM = self.__class__.AddLocalSizingWTM(service, rules, "AddLocalSizingWTM", path)
        self.AddMultiZoneControls = self.__class__.AddMultiZoneControls(service, rules, "AddMultiZoneControls", path)
        self.AddShellBoundaryLayerControls = self.__class__.AddShellBoundaryLayerControls(service, rules, "AddShellBoundaryLayerControls", path)
        self.AddThickness = self.__class__.AddThickness(service, rules, "AddThickness", path)
        self.AddThinVolumeMeshControls = self.__class__.AddThinVolumeMeshControls(service, rules, "AddThinVolumeMeshControls", path)
        self.AddVirtualTopology = self.__class__.AddVirtualTopology(service, rules, "AddVirtualTopology", path)
        self.Capping = self.__class__.Capping(service, rules, "Capping", path)
        self.CheckMesh = self.__class__.CheckMesh(service, rules, "CheckMesh", path)
        self.CheckSurfaceQuality = self.__class__.CheckSurfaceQuality(service, rules, "CheckSurfaceQuality", path)
        self.CheckVolumeQuality = self.__class__.CheckVolumeQuality(service, rules, "CheckVolumeQuality", path)
        self.ChooseMeshControlOptions = self.__class__.ChooseMeshControlOptions(service, rules, "ChooseMeshControlOptions", path)
        self.ChoosePartReplacementOptions = self.__class__.ChoosePartReplacementOptions(service, rules, "ChoosePartReplacementOptions", path)
        self.CloseLeakage = self.__class__.CloseLeakage(service, rules, "CloseLeakage", path)
        self.ComplexMeshingRegions = self.__class__.ComplexMeshingRegions(service, rules, "ComplexMeshingRegions", path)
        self.ComputeSizeField = self.__class__.ComputeSizeField(service, rules, "ComputeSizeField", path)
        self.CreateBackgroundMesh = self.__class__.CreateBackgroundMesh(service, rules, "CreateBackgroundMesh", path)
        self.CreateCollarMesh = self.__class__.CreateCollarMesh(service, rules, "CreateCollarMesh", path)
        self.CreateComponentMesh = self.__class__.CreateComponentMesh(service, rules, "CreateComponentMesh", path)
        self.CreateContactPatch = self.__class__.CreateContactPatch(service, rules, "CreateContactPatch", path)
        self.CreateExternalFlowBoundaries = self.__class__.CreateExternalFlowBoundaries(service, rules, "CreateExternalFlowBoundaries", path)
        self.CreateGapCover = self.__class__.CreateGapCover(service, rules, "CreateGapCover", path)
        self.CreateLocalRefinementRegions = self.__class__.CreateLocalRefinementRegions(service, rules, "CreateLocalRefinementRegions", path)
        self.CreateMeshObjects = self.__class__.CreateMeshObjects(service, rules, "CreateMeshObjects", path)
        self.CreateOversetInterfaces = self.__class__.CreateOversetInterfaces(service, rules, "CreateOversetInterfaces", path)
        self.CreatePorousRegions = self.__class__.CreatePorousRegions(service, rules, "CreatePorousRegions", path)
        self.CreateRegions = self.__class__.CreateRegions(service, rules, "CreateRegions", path)
        self.DefineGlobalSizing = self.__class__.DefineGlobalSizing(service, rules, "DefineGlobalSizing", path)
        self.DefineLeakageThreshold = self.__class__.DefineLeakageThreshold(service, rules, "DefineLeakageThreshold", path)
        self.DescribeGeometryAndFlow = self.__class__.DescribeGeometryAndFlow(service, rules, "DescribeGeometryAndFlow", path)
        self.DescribeOversetFeatures = self.__class__.DescribeOversetFeatures(service, rules, "DescribeOversetFeatures", path)
        self.ExtractEdges = self.__class__.ExtractEdges(service, rules, "ExtractEdges", path)
        self.ExtrudeVolumeMesh = self.__class__.ExtrudeVolumeMesh(service, rules, "ExtrudeVolumeMesh", path)
        self.GenerateInitialSurfaceMesh = self.__class__.GenerateInitialSurfaceMesh(service, rules, "GenerateInitialSurfaceMesh", path)
        self.GenerateMapMesh = self.__class__.GenerateMapMesh(service, rules, "GenerateMapMesh", path)
        self.GeneratePrisms = self.__class__.GeneratePrisms(service, rules, "GeneratePrisms", path)
        self.GenerateShellBoundaryLayerMesh = self.__class__.GenerateShellBoundaryLayerMesh(service, rules, "GenerateShellBoundaryLayerMesh", path)
        self.GenerateTheMultiZoneMesh = self.__class__.GenerateTheMultiZoneMesh(service, rules, "GenerateTheMultiZoneMesh", path)
        self.GenerateTheSurfaceMeshFTM = self.__class__.GenerateTheSurfaceMeshFTM(service, rules, "GenerateTheSurfaceMeshFTM", path)
        self.GenerateTheSurfaceMeshWTM = self.__class__.GenerateTheSurfaceMeshWTM(service, rules, "GenerateTheSurfaceMeshWTM", path)
        self.GenerateTheVolumeMeshFTM = self.__class__.GenerateTheVolumeMeshFTM(service, rules, "GenerateTheVolumeMeshFTM", path)
        self.GenerateTheVolumeMeshWTM = self.__class__.GenerateTheVolumeMeshWTM(service, rules, "GenerateTheVolumeMeshWTM", path)
        self.GeometrySetup = self.__class__.GeometrySetup(service, rules, "GeometrySetup", path)
        self.IdentifyConstructionSurfaces = self.__class__.IdentifyConstructionSurfaces(service, rules, "IdentifyConstructionSurfaces", path)
        self.IdentifyDeviatedFaces = self.__class__.IdentifyDeviatedFaces(service, rules, "IdentifyDeviatedFaces", path)
        self.IdentifyOrphans = self.__class__.IdentifyOrphans(service, rules, "IdentifyOrphans", path)
        self.IdentifyRegions = self.__class__.IdentifyRegions(service, rules, "IdentifyRegions", path)
        self.ImportBodyOfInfluenceGeometry = self.__class__.ImportBodyOfInfluenceGeometry(service, rules, "ImportBodyOfInfluenceGeometry", path)
        self.ImportGeometry = self.__class__.ImportGeometry(service, rules, "ImportGeometry", path)
        self.ImproveSurfaceMesh = self.__class__.ImproveSurfaceMesh(service, rules, "ImproveSurfaceMesh", path)
        self.ImproveVolumeMesh = self.__class__.ImproveVolumeMesh(service, rules, "ImproveVolumeMesh", path)
        self.LinearMeshPattern = self.__class__.LinearMeshPattern(service, rules, "LinearMeshPattern", path)
        self.LoadCADGeometry = self.__class__.LoadCADGeometry(service, rules, "LoadCADGeometry", path)
        self.LocalScopedSizingForPartReplacement = self.__class__.LocalScopedSizingForPartReplacement(service, rules, "LocalScopedSizingForPartReplacement", path)
        self.ManageZones = self.__class__.ManageZones(service, rules, "ManageZones", path)
        self.MeshFluidDomain = self.__class__.MeshFluidDomain(service, rules, "MeshFluidDomain", path)
        self.ModifyMeshRefinement = self.__class__.ModifyMeshRefinement(service, rules, "ModifyMeshRefinement", path)
        self.PartManagement = self.__class__.PartManagement(service, rules, "PartManagement", path)
        self.PartReplacementSettings = self.__class__.PartReplacementSettings(service, rules, "PartReplacementSettings", path)
        self.RemeshSurface = self.__class__.RemeshSurface(service, rules, "RemeshSurface", path)
        self.RunCustomJournal = self.__class__.RunCustomJournal(service, rules, "RunCustomJournal", path)
        self.SeparateContacts = self.__class__.SeparateContacts(service, rules, "SeparateContacts", path)
        self.SetUpPeriodicBoundaries = self.__class__.SetUpPeriodicBoundaries(service, rules, "SetUpPeriodicBoundaries", path)
        self.SetupBoundaryLayers = self.__class__.SetupBoundaryLayers(service, rules, "SetupBoundaryLayers", path)
        self.ShareTopology = self.__class__.ShareTopology(service, rules, "ShareTopology", path)
        self.SizeControlsTable = self.__class__.SizeControlsTable(service, rules, "SizeControlsTable", path)
        self.SwitchToSolution = self.__class__.SwitchToSolution(service, rules, "SwitchToSolution", path)
        self.TransformVolumeMesh = self.__class__.TransformVolumeMesh(service, rules, "TransformVolumeMesh", path)
        self.UpdateBoundaries = self.__class__.UpdateBoundaries(service, rules, "UpdateBoundaries", path)
        self.UpdateRegionSettings = self.__class__.UpdateRegionSettings(service, rules, "UpdateRegionSettings", path)
        self.UpdateRegions = self.__class__.UpdateRegions(service, rules, "UpdateRegions", path)
        self.UpdateTheVolumeMesh = self.__class__.UpdateTheVolumeMesh(service, rules, "UpdateTheVolumeMesh", path)
        self.WrapMain = self.__class__.WrapMain(service, rules, "WrapMain", path)
        self.Write2dMesh = self.__class__.Write2dMesh(service, rules, "Write2dMesh", path)
        self.WriteSkinMesh = self.__class__.WriteSkinMesh(service, rules, "WriteSkinMesh", path)
        super().__init__(service, rules, path)

    class Diagnostics(PyMenu):
        """
        Singleton Diagnostics.
        """
        def __init__(self, service, rules, path):
            self.Close = self.__class__.Close(service, rules, "Close", path)
            self.Compute = self.__class__.Compute(service, rules, "Compute", path)
            self.DiagOptions = self.__class__.DiagOptions(service, rules, "DiagOptions", path)
            self.Draw = self.__class__.Draw(service, rules, "Draw", path)
            self.First = self.__class__.First(service, rules, "First", path)
            self.Histogram = self.__class__.Histogram(service, rules, "Histogram", path)
            self.Ignore = self.__class__.Ignore(service, rules, "Ignore", path)
            self.List = self.__class__.List(service, rules, "List", path)
            self.Mark = self.__class__.Mark(service, rules, "Mark", path)
            self.Next = self.__class__.Next(service, rules, "Next", path)
            self.Previous = self.__class__.Previous(service, rules, "Previous", path)
            self.Restore = self.__class__.Restore(service, rules, "Restore", path)
            self.Summary = self.__class__.Summary(service, rules, "Summary", path)
            self.Update = self.__class__.Update(service, rules, "Update", path)
            super().__init__(service, rules, path)

        class Close(PyCommand):
            """
            Command Close.


            Returns
            -------
            None
            """
            class _CloseCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _CloseCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CloseCommandArguments(*args)

        class Compute(PyCommand):
            """
            Command Compute.


            Returns
            -------
            None
            """
            class _ComputeCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _ComputeCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ComputeCommandArguments(*args)

        class DiagOptions(PyCommand):
            """
            Command DiagOptions.

            Parameters
            ----------
            Option : str
            Measure : str
            Average : float
            Minimum : float
            Maximum : float
            MarkRangeType : str
            MarkMin : float
            MarkMax : float
            Selected : str
            MarkedCount : int
            CurrentCount : int
            ExtentsUpdateBounds : bool
            ExtentsXMin : float
            ExtentsYMin : float
            ExtentsZMin : float
            ExtentsXMax : float
            ExtentsYMax : float
            ExtentsZMax : float

            Returns
            -------
            None
            """
            class _DiagOptionsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.Option = self._Option(self, "Option", service, rules, path)
                    self.Measure = self._Measure(self, "Measure", service, rules, path)
                    self.Average = self._Average(self, "Average", service, rules, path)
                    self.Minimum = self._Minimum(self, "Minimum", service, rules, path)
                    self.Maximum = self._Maximum(self, "Maximum", service, rules, path)
                    self.MarkRangeType = self._MarkRangeType(self, "MarkRangeType", service, rules, path)
                    self.MarkMin = self._MarkMin(self, "MarkMin", service, rules, path)
                    self.MarkMax = self._MarkMax(self, "MarkMax", service, rules, path)
                    self.Selected = self._Selected(self, "Selected", service, rules, path)
                    self.MarkedCount = self._MarkedCount(self, "MarkedCount", service, rules, path)
                    self.CurrentCount = self._CurrentCount(self, "CurrentCount", service, rules, path)
                    self.ExtentsUpdateBounds = self._ExtentsUpdateBounds(self, "ExtentsUpdateBounds", service, rules, path)
                    self.ExtentsXMin = self._ExtentsXMin(self, "ExtentsXMin", service, rules, path)
                    self.ExtentsYMin = self._ExtentsYMin(self, "ExtentsYMin", service, rules, path)
                    self.ExtentsZMin = self._ExtentsZMin(self, "ExtentsZMin", service, rules, path)
                    self.ExtentsXMax = self._ExtentsXMax(self, "ExtentsXMax", service, rules, path)
                    self.ExtentsYMax = self._ExtentsYMax(self, "ExtentsYMax", service, rules, path)
                    self.ExtentsZMax = self._ExtentsZMax(self, "ExtentsZMax", service, rules, path)

                class _Option(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Option.
                    """

                class _Measure(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Measure.
                    """

                class _Average(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Average.
                    """

                class _Minimum(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Minimum.
                    """

                class _Maximum(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Maximum.
                    """

                class _MarkRangeType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MarkRangeType.
                    """

                class _MarkMin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MarkMin.
                    """

                class _MarkMax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MarkMax.
                    """

                class _Selected(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Selected.
                    """

                class _MarkedCount(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MarkedCount.
                    """

                class _CurrentCount(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurrentCount.
                    """

                class _ExtentsUpdateBounds(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ExtentsUpdateBounds.
                    """

                class _ExtentsXMin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ExtentsXMin.
                    """

                class _ExtentsYMin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ExtentsYMin.
                    """

                class _ExtentsZMin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ExtentsZMin.
                    """

                class _ExtentsXMax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ExtentsXMax.
                    """

                class _ExtentsYMax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ExtentsYMax.
                    """

                class _ExtentsZMax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ExtentsZMax.
                    """

            def create_instance(self) -> _DiagOptionsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DiagOptionsCommandArguments(*args)

        class Draw(PyCommand):
            """
            Command Draw.


            Returns
            -------
            None
            """
            class _DrawCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DrawCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DrawCommandArguments(*args)

        class First(PyCommand):
            """
            Command First.


            Returns
            -------
            None
            """
            class _FirstCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _FirstCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._FirstCommandArguments(*args)

        class Histogram(PyCommand):
            """
            Command Histogram.


            Returns
            -------
            None
            """
            class _HistogramCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _HistogramCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._HistogramCommandArguments(*args)

        class Ignore(PyCommand):
            """
            Command Ignore.


            Returns
            -------
            None
            """
            class _IgnoreCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _IgnoreCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._IgnoreCommandArguments(*args)

        class List(PyCommand):
            """
            Command List.


            Returns
            -------
            None
            """
            class _ListCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _ListCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ListCommandArguments(*args)

        class Mark(PyCommand):
            """
            Command Mark.


            Returns
            -------
            None
            """
            class _MarkCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _MarkCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._MarkCommandArguments(*args)

        class Next(PyCommand):
            """
            Command Next.


            Returns
            -------
            None
            """
            class _NextCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _NextCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._NextCommandArguments(*args)

        class Previous(PyCommand):
            """
            Command Previous.


            Returns
            -------
            None
            """
            class _PreviousCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _PreviousCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._PreviousCommandArguments(*args)

        class Restore(PyCommand):
            """
            Command Restore.


            Returns
            -------
            None
            """
            class _RestoreCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _RestoreCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._RestoreCommandArguments(*args)

        class Summary(PyCommand):
            """
            Command Summary.


            Returns
            -------
            None
            """
            class _SummaryCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _SummaryCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._SummaryCommandArguments(*args)

        class Update(PyCommand):
            """
            Command Update.


            Returns
            -------
            None
            """
            class _UpdateCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateCommandArguments(*args)

    class File(PyMenu):
        """
        Singleton File.
        """
        def __init__(self, service, rules, path):
            self.ReadCase = self.__class__.ReadCase(service, rules, "ReadCase", path)
            self.ReadJournal = self.__class__.ReadJournal(service, rules, "ReadJournal", path)
            self.ReadMesh = self.__class__.ReadMesh(service, rules, "ReadMesh", path)
            self.StartJournal = self.__class__.StartJournal(service, rules, "StartJournal", path)
            self.StopJournal = self.__class__.StopJournal(service, rules, "StopJournal", path)
            self.WriteCase = self.__class__.WriteCase(service, rules, "WriteCase", path)
            self.WriteMesh = self.__class__.WriteMesh(service, rules, "WriteMesh", path)
            super().__init__(service, rules, path)

        class ReadCase(PyCommand):
            """
            Command ReadCase.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            None
            """
            class _ReadCaseCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadCaseCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadCaseCommandArguments(*args)

        class ReadJournal(PyCommand):
            """
            Command ReadJournal.

            Parameters
            ----------
            FileName : list[str]
            ChangeDirectory : bool

            Returns
            -------
            None
            """
            class _ReadJournalCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                    self.ChangeDirectory = self._ChangeDirectory(self, "ChangeDirectory", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

                class _ChangeDirectory(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ChangeDirectory.
                    """

            def create_instance(self) -> _ReadJournalCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadJournalCommandArguments(*args)

        class ReadMesh(PyCommand):
            """
            Command ReadMesh.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            None
            """
            class _ReadMeshCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadMeshCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadMeshCommandArguments(*args)

        class StartJournal(PyCommand):
            """
            Command StartJournal.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            None
            """
            class _StartJournalCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _StartJournalCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._StartJournalCommandArguments(*args)

        class StopJournal(PyCommand):
            """
            Command StopJournal.


            Returns
            -------
            None
            """
            class _StopJournalCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _StopJournalCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._StopJournalCommandArguments(*args)

        class WriteCase(PyCommand):
            """
            Command WriteCase.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            None
            """
            class _WriteCaseCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _WriteCaseCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteCaseCommandArguments(*args)

        class WriteMesh(PyCommand):
            """
            Command WriteMesh.

            Parameters
            ----------
            FileName : str

            Returns
            -------
            None
            """
            class _WriteMeshCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _WriteMeshCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteMeshCommandArguments(*args)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.FTMRegionData = self.__class__.FTMRegionData(service, rules, path + [("FTMRegionData", "")])
            self.AreaUnit = self.__class__.AreaUnit(service, rules, path + [("AreaUnit", "")])
            self.EnableCleanCAD = self.__class__.EnableCleanCAD(service, rules, path + [("EnableCleanCAD", "")])
            self.EnableComplexMeshing = self.__class__.EnableComplexMeshing(service, rules, path + [("EnableComplexMeshing", "")])
            self.EnableOversetMeshing = self.__class__.EnableOversetMeshing(service, rules, path + [("EnableOversetMeshing", "")])
            self.EnablePrime2dMeshing = self.__class__.EnablePrime2dMeshing(service, rules, path + [("EnablePrime2dMeshing", "")])
            self.EnablePrimeMeshing = self.__class__.EnablePrimeMeshing(service, rules, path + [("EnablePrimeMeshing", "")])
            self.InitialVersion = self.__class__.InitialVersion(service, rules, path + [("InitialVersion", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            self.NormalMode = self.__class__.NormalMode(service, rules, path + [("NormalMode", "")])
            self.UseAllowedValues = self.__class__.UseAllowedValues(service, rules, path + [("UseAllowedValues", "")])
            self.VolumeUnit = self.__class__.VolumeUnit(service, rules, path + [("VolumeUnit", "")])
            super().__init__(service, rules, path)

        class FTMRegionData(PyMenu):
            """
            Singleton FTMRegionData.
            """
            def __init__(self, service, rules, path):
                self.AllOversetNameList = self.__class__.AllOversetNameList(service, rules, path + [("AllOversetNameList", "")])
                self.AllOversetSizeList = self.__class__.AllOversetSizeList(service, rules, path + [("AllOversetSizeList", "")])
                self.AllOversetTypeList = self.__class__.AllOversetTypeList(service, rules, path + [("AllOversetTypeList", "")])
                self.AllOversetVolumeFillList = self.__class__.AllOversetVolumeFillList(service, rules, path + [("AllOversetVolumeFillList", "")])
                self.AllRegionFilterCategories = self.__class__.AllRegionFilterCategories(service, rules, path + [("AllRegionFilterCategories", "")])
                self.AllRegionLeakageSizeList = self.__class__.AllRegionLeakageSizeList(service, rules, path + [("AllRegionLeakageSizeList", "")])
                self.AllRegionLinkedConstructionSurfaceList = self.__class__.AllRegionLinkedConstructionSurfaceList(service, rules, path + [("AllRegionLinkedConstructionSurfaceList", "")])
                self.AllRegionMeshMethodList = self.__class__.AllRegionMeshMethodList(service, rules, path + [("AllRegionMeshMethodList", "")])
                self.AllRegionNameList = self.__class__.AllRegionNameList(service, rules, path + [("AllRegionNameList", "")])
                self.AllRegionOversetComponenList = self.__class__.AllRegionOversetComponenList(service, rules, path + [("AllRegionOversetComponenList", "")])
                self.AllRegionSizeList = self.__class__.AllRegionSizeList(service, rules, path + [("AllRegionSizeList", "")])
                self.AllRegionSourceList = self.__class__.AllRegionSourceList(service, rules, path + [("AllRegionSourceList", "")])
                self.AllRegionTypeList = self.__class__.AllRegionTypeList(service, rules, path + [("AllRegionTypeList", "")])
                self.AllRegionVolumeFillList = self.__class__.AllRegionVolumeFillList(service, rules, path + [("AllRegionVolumeFillList", "")])
                super().__init__(service, rules, path)

            class AllOversetNameList(PyTextual):
                """
                Parameter AllOversetNameList of value type list[str].
                """
                pass

            class AllOversetSizeList(PyTextual):
                """
                Parameter AllOversetSizeList of value type list[str].
                """
                pass

            class AllOversetTypeList(PyTextual):
                """
                Parameter AllOversetTypeList of value type list[str].
                """
                pass

            class AllOversetVolumeFillList(PyTextual):
                """
                Parameter AllOversetVolumeFillList of value type list[str].
                """
                pass

            class AllRegionFilterCategories(PyTextual):
                """
                Parameter AllRegionFilterCategories of value type list[str].
                """
                pass

            class AllRegionLeakageSizeList(PyTextual):
                """
                Parameter AllRegionLeakageSizeList of value type list[str].
                """
                pass

            class AllRegionLinkedConstructionSurfaceList(PyTextual):
                """
                Parameter AllRegionLinkedConstructionSurfaceList of value type list[str].
                """
                pass

            class AllRegionMeshMethodList(PyTextual):
                """
                Parameter AllRegionMeshMethodList of value type list[str].
                """
                pass

            class AllRegionNameList(PyTextual):
                """
                Parameter AllRegionNameList of value type list[str].
                """
                pass

            class AllRegionOversetComponenList(PyTextual):
                """
                Parameter AllRegionOversetComponenList of value type list[str].
                """
                pass

            class AllRegionSizeList(PyTextual):
                """
                Parameter AllRegionSizeList of value type list[str].
                """
                pass

            class AllRegionSourceList(PyTextual):
                """
                Parameter AllRegionSourceList of value type list[str].
                """
                pass

            class AllRegionTypeList(PyTextual):
                """
                Parameter AllRegionTypeList of value type list[str].
                """
                pass

            class AllRegionVolumeFillList(PyTextual):
                """
                Parameter AllRegionVolumeFillList of value type list[str].
                """
                pass

        class AreaUnit(PyTextual):
            """
            Parameter AreaUnit of value type str.
            """
            pass

        class EnableCleanCAD(PyParameter):
            """
            Parameter EnableCleanCAD of value type bool.
            """
            pass

        class EnableComplexMeshing(PyParameter):
            """
            Parameter EnableComplexMeshing of value type bool.
            """
            pass

        class EnableOversetMeshing(PyParameter):
            """
            Parameter EnableOversetMeshing of value type bool.
            """
            pass

        class EnablePrime2dMeshing(PyParameter):
            """
            Parameter EnablePrime2dMeshing of value type bool.
            """
            pass

        class EnablePrimeMeshing(PyParameter):
            """
            Parameter EnablePrimeMeshing of value type bool.
            """
            pass

        class InitialVersion(PyTextual):
            """
            Parameter InitialVersion of value type str.
            """
            pass

        class LengthUnit(PyTextual):
            """
            Parameter LengthUnit of value type str.
            """
            pass

        class NormalMode(PyParameter):
            """
            Parameter NormalMode of value type bool.
            """
            pass

        class UseAllowedValues(PyParameter):
            """
            Parameter UseAllowedValues of value type bool.
            """
            pass

        class VolumeUnit(PyTextual):
            """
            Parameter VolumeUnit of value type str.
            """
            pass

    class Graphics(PyMenu):
        """
        Singleton Graphics.
        """
        def __init__(self, service, rules, path):
            self.Bounds = self.__class__.Bounds(service, rules, path + [("Bounds", "")])
            self.ClippingPlane = self.__class__.ClippingPlane(service, rules, "ClippingPlane", path)
            self.GetClippingZoneIDs = self.__class__.GetClippingZoneIDs(service, rules, "GetClippingZoneIDs", path)
            self.GetVisibleDomainBounds = self.__class__.GetVisibleDomainBounds(service, rules, "GetVisibleDomainBounds", path)
            super().__init__(service, rules, path)

        class Bounds(PyMenu):
            """
            Singleton Bounds.
            """
            def __init__(self, service, rules, path):
                self.BoundX = self.__class__.BoundX(service, rules, path + [("BoundX", "")])
                self.BoundY = self.__class__.BoundY(service, rules, path + [("BoundY", "")])
                self.BoundZ = self.__class__.BoundZ(service, rules, path + [("BoundZ", "")])
                self.Delta3D = self.__class__.Delta3D(service, rules, path + [("Delta3D", "")])
                self.Selection = self.__class__.Selection(service, rules, path + [("Selection", "")])
                self.ResetBounds = self.__class__.ResetBounds(service, rules, "ResetBounds", path)
                self.SetBounds = self.__class__.SetBounds(service, rules, "SetBounds", path)
                super().__init__(service, rules, path)

            class BoundX(PyParameter):
                """
                Parameter BoundX of value type bool.
                """
                pass

            class BoundY(PyParameter):
                """
                Parameter BoundY of value type bool.
                """
                pass

            class BoundZ(PyParameter):
                """
                Parameter BoundZ of value type bool.
                """
                pass

            class Delta3D(PyNumerical):
                """
                Parameter Delta3D of value type float.
                """
                pass

            class Selection(PyTextual):
                """
                Parameter Selection of value type str.
                """
                pass

            class ResetBounds(PyCommand):
                """
                Command ResetBounds.


                Returns
                -------
                None
                """
                class _ResetBoundsCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ResetBoundsCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ResetBoundsCommandArguments(*args)

            class SetBounds(PyCommand):
                """
                Command SetBounds.


                Returns
                -------
                None
                """
                class _SetBoundsCommandArguments(PyCommandArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _SetBoundsCommandArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._SetBoundsCommandArguments(*args)

        class ClippingPlane(PyCommand):
            """
            Command ClippingPlane.

            Parameters
            ----------
            InsertClippingPlane : bool
            DrawCellLayer : bool
            FreezeCellLayer : bool
            FlipClippingPlane : bool
            PointCoordinates : list[float]
            PlaneNormal : list[float]
            SliderPosition : int
            CutDirection : str

            Returns
            -------
            None
            """
            class _ClippingPlaneCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.InsertClippingPlane = self._InsertClippingPlane(self, "InsertClippingPlane", service, rules, path)
                    self.DrawCellLayer = self._DrawCellLayer(self, "DrawCellLayer", service, rules, path)
                    self.FreezeCellLayer = self._FreezeCellLayer(self, "FreezeCellLayer", service, rules, path)
                    self.FlipClippingPlane = self._FlipClippingPlane(self, "FlipClippingPlane", service, rules, path)
                    self.PointCoordinates = self._PointCoordinates(self, "PointCoordinates", service, rules, path)
                    self.PlaneNormal = self._PlaneNormal(self, "PlaneNormal", service, rules, path)
                    self.SliderPosition = self._SliderPosition(self, "SliderPosition", service, rules, path)
                    self.CutDirection = self._CutDirection(self, "CutDirection", service, rules, path)

                class _InsertClippingPlane(PyParameterCommandArgumentsSubItem):
                    """
                    Argument InsertClippingPlane.
                    """

                class _DrawCellLayer(PyParameterCommandArgumentsSubItem):
                    """
                    Argument DrawCellLayer.
                    """

                class _FreezeCellLayer(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FreezeCellLayer.
                    """

                class _FlipClippingPlane(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FlipClippingPlane.
                    """

                class _PointCoordinates(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PointCoordinates.
                    """

                class _PlaneNormal(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PlaneNormal.
                    """

                class _SliderPosition(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SliderPosition.
                    """

                class _CutDirection(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CutDirection.
                    """

            def create_instance(self) -> _ClippingPlaneCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ClippingPlaneCommandArguments(*args)

        class GetClippingZoneIDs(PyCommand):
            """
            Command GetClippingZoneIDs.


            Returns
            -------
            None
            """
            class _GetClippingZoneIDsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _GetClippingZoneIDsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._GetClippingZoneIDsCommandArguments(*args)

        class GetVisibleDomainBounds(PyCommand):
            """
            Command GetVisibleDomainBounds.


            Returns
            -------
            None
            """
            class _GetVisibleDomainBoundsCommandArguments(PyCommandArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _GetVisibleDomainBoundsCommandArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._GetVisibleDomainBoundsCommandArguments(*args)

    class Add2DBoundaryLayers(PyCommand):
        """
        Command Add2DBoundaryLayers.

        Parameters
        ----------
        AddChild : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        LastAspectRatio : float
        Rate : float
        FirstLayerHeight : float
        MaxLayerHeight : float
        Addin : str
        FaceLabelList : list[str]
        GrowOn : str
        EdgeLabelList : list[str]
        EdgeZoneList : list[str]
        ShellBLAdvancedOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _Add2DBoundaryLayersCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.BLControlName = self._BLControlName(self, "BLControlName", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.FirstAspectRatio = self._FirstAspectRatio(self, "FirstAspectRatio", service, rules, path)
                self.TransitionRatio = self._TransitionRatio(self, "TransitionRatio", service, rules, path)
                self.LastAspectRatio = self._LastAspectRatio(self, "LastAspectRatio", service, rules, path)
                self.Rate = self._Rate(self, "Rate", service, rules, path)
                self.FirstLayerHeight = self._FirstLayerHeight(self, "FirstLayerHeight", service, rules, path)
                self.MaxLayerHeight = self._MaxLayerHeight(self, "MaxLayerHeight", service, rules, path)
                self.Addin = self._Addin(self, "Addin", service, rules, path)
                self.FaceLabelList = self._FaceLabelList(self, "FaceLabelList", service, rules, path)
                self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                self.EdgeLabelList = self._EdgeLabelList(self, "EdgeLabelList", service, rules, path)
                self.EdgeZoneList = self._EdgeZoneList(self, "EdgeZoneList", service, rules, path)
                self.ShellBLAdvancedOptions = self._ShellBLAdvancedOptions(self, "ShellBLAdvancedOptions", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Argument AddChild.
                """

            class _BLControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument BLControlName.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Argument OffsetMethodType.
                """

            class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfLayers.
                """

            class _FirstAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstAspectRatio.
                """

            class _TransitionRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument TransitionRatio.
                """

            class _LastAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument LastAspectRatio.
                """

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Argument Rate.
                """

            class _FirstLayerHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstLayerHeight.
                """

            class _MaxLayerHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _Addin(PyTextualCommandArgumentsSubItem):
                """
                Argument Addin.
                """

            class _FaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceLabelList.
                """

            class _GrowOn(PyTextualCommandArgumentsSubItem):
                """
                Argument GrowOn.
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelList.
                """

            class _EdgeZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeZoneList.
                """

            class _ShellBLAdvancedOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument ShellBLAdvancedOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ExposeSide = self._ExposeSide(self, "ExposeSide", service, rules, path)
                    self.ShowShellBLAdvancedOptions = self._ShowShellBLAdvancedOptions(self, "ShowShellBLAdvancedOptions", service, rules, path)
                    self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                    self.AdjacentAttachAngle = self._AdjacentAttachAngle(self, "AdjacentAttachAngle", service, rules, path)

                class _ExposeSide(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExposeSide.
                    """

                class _ShowShellBLAdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowShellBLAdvancedOptions.
                    """

                class _MaxAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxAspectRatio.
                    """

                class _MinAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinAspectRatio.
                    """

                class _LastRatioNumLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _GapFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GapFactor.
                    """

                class _AdjacentAttachAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AdjacentAttachAngle.
                    """

        def create_instance(self) -> _Add2DBoundaryLayersCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._Add2DBoundaryLayersCommandArguments(*args)

    class AddBoundaryLayers(PyCommand):
        """
        Command AddBoundaryLayers.

        Parameters
        ----------
        AddChild : str
            Determine whether (yes) or not (no) you want to specify one or more boundary layers for your simulation. If none are yet defined, you can choose yes, using prism control file and read in a prism control file that holds the boundary layer definition.
        ReadPrismControlFile : str
            Specify (or browse for) a .pzmcontrol file that contains the boundary (prism) layer specifications.
        BLControlName : str
            Specify a name for the boundary layer control or use the default value.
        OffsetMethodType : str
            Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
        NumberOfLayers : int
            Select the number of boundary layers to be generated.
        FirstAspectRatio : float
            Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
        TransitionRatio : float
            For the smooth transition offset method, specify the rate at which adjacent elements grow. For the last-ratio offset method, specify the factor by which the thickness of each subsequent boundary layer increases or decreases compared to the previous layer.
        Rate : float
            Specify the rate of growth for the boundary layer.
        FirstHeight : float
            Specify the height of the first layer of cells in the boundary layer.
        MaxLayerHeight : float
        FaceScope : dict[str, Any]
        RegionScope : list[str]
            Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        BlLabelList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LocalPrismPreferences : dict[str, Any]
        BLZoneList : list[str]
        BLRegionList : list[str]
        InvalidAdded : str
        CompleteRegionScope : list[str]
        CompleteBlLabelList : list[str]
        CompleteBLZoneList : list[str]
        CompleteBLRegionList : list[str]
        CompleteZoneSelectionList : list[str]
        CompleteLabelSelectionList : list[str]

        Returns
        -------
        bool
        """
        class _AddBoundaryLayersCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.ReadPrismControlFile = self._ReadPrismControlFile(self, "ReadPrismControlFile", service, rules, path)
                self.BLControlName = self._BLControlName(self, "BLControlName", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.FirstAspectRatio = self._FirstAspectRatio(self, "FirstAspectRatio", service, rules, path)
                self.TransitionRatio = self._TransitionRatio(self, "TransitionRatio", service, rules, path)
                self.Rate = self._Rate(self, "Rate", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.MaxLayerHeight = self._MaxLayerHeight(self, "MaxLayerHeight", service, rules, path)
                self.FaceScope = self._FaceScope(self, "FaceScope", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.BlLabelList = self._BlLabelList(self, "BlLabelList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LocalPrismPreferences = self._LocalPrismPreferences(self, "LocalPrismPreferences", service, rules, path)
                self.BLZoneList = self._BLZoneList(self, "BLZoneList", service, rules, path)
                self.BLRegionList = self._BLRegionList(self, "BLRegionList", service, rules, path)
                self.InvalidAdded = self._InvalidAdded(self, "InvalidAdded", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)
                self.CompleteBlLabelList = self._CompleteBlLabelList(self, "CompleteBlLabelList", service, rules, path)
                self.CompleteBLZoneList = self._CompleteBLZoneList(self, "CompleteBLZoneList", service, rules, path)
                self.CompleteBLRegionList = self._CompleteBLRegionList(self, "CompleteBLRegionList", service, rules, path)
                self.CompleteZoneSelectionList = self._CompleteZoneSelectionList(self, "CompleteZoneSelectionList", service, rules, path)
                self.CompleteLabelSelectionList = self._CompleteLabelSelectionList(self, "CompleteLabelSelectionList", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Determine whether (yes) or not (no) you want to specify one or more boundary layers for your simulation. If none are yet defined, you can choose yes, using prism control file and read in a prism control file that holds the boundary layer definition.
                """

            class _ReadPrismControlFile(PyTextualCommandArgumentsSubItem):
                """
                Specify (or browse for) a .pzmcontrol file that contains the boundary (prism) layer specifications.
                """

            class _BLControlName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the boundary layer control or use the default value.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
                """

            class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                """
                Select the number of boundary layers to be generated.
                """

            class _FirstAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
                """

            class _TransitionRatio(PyNumericalCommandArgumentsSubItem):
                """
                For the smooth transition offset method, specify the rate at which adjacent elements grow. For the last-ratio offset method, specify the factor by which the thickness of each subsequent boundary layer increases or decreases compared to the previous layer.
                """

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the rate of growth for the boundary layer.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _MaxLayerHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _FaceScope(PySingletonCommandArgumentsSubItem):
                """
                Argument FaceScope.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                    self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                    self.FaceScopeMeshObject = self._FaceScopeMeshObject(self, "FaceScopeMeshObject", service, rules, path)
                    self.RegionsType = self._RegionsType(self, "RegionsType", service, rules, path)

                class _TopologyList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument TopologyList.
                    """

                class _GrowOn(PyTextualCommandArgumentsSubItem):
                    """
                    Argument GrowOn.
                    """

                class _FaceScopeMeshObject(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FaceScopeMeshObject.
                    """

                class _RegionsType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RegionsType.
                    """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BlLabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LocalPrismPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument LocalPrismPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.LastRatio = self._LastRatio(self, "LastRatio", service, rules, path)
                    self.AdditionalIgnoredLayers = self._AdditionalIgnoredLayers(self, "AdditionalIgnoredLayers", service, rules, path)
                    self.SphereRadiusFactorAtInvalidNormals = self._SphereRadiusFactorAtInvalidNormals(self, "SphereRadiusFactorAtInvalidNormals", service, rules, path)
                    self.SmoothRingsAtInvalidNormals = self._SmoothRingsAtInvalidNormals(self, "SmoothRingsAtInvalidNormals", service, rules, path)
                    self.Continuous = self._Continuous(self, "Continuous", service, rules, path)
                    self.SplitPrism = self._SplitPrism(self, "SplitPrism", service, rules, path)
                    self.ModifyAtInvalidNormals = self._ModifyAtInvalidNormals(self, "ModifyAtInvalidNormals", service, rules, path)
                    self.InvalidNormalMethod = self._InvalidNormalMethod(self, "InvalidNormalMethod", service, rules, path)
                    self.NumberOfSplitLayers = self._NumberOfSplitLayers(self, "NumberOfSplitLayers", service, rules, path)
                    self.ShowLocalPrismPreferences = self._ShowLocalPrismPreferences(self, "ShowLocalPrismPreferences", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.AllowedTangencyAtInvalidNormals = self._AllowedTangencyAtInvalidNormals(self, "AllowedTangencyAtInvalidNormals", service, rules, path)
                    self.RemeshAtInvalidNormals = self._RemeshAtInvalidNormals(self, "RemeshAtInvalidNormals", service, rules, path)
                    self.IgnoreBoundaryLayers = self._IgnoreBoundaryLayers(self, "IgnoreBoundaryLayers", service, rules, path)

                class _LastRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatio.
                    """

                class _AdditionalIgnoredLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AdditionalIgnoredLayers.
                    """

                class _SphereRadiusFactorAtInvalidNormals(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SphereRadiusFactorAtInvalidNormals.
                    """

                class _SmoothRingsAtInvalidNormals(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SmoothRingsAtInvalidNormals.
                    """

                class _Continuous(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Continuous.
                    """

                class _SplitPrism(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SplitPrism.
                    """

                class _ModifyAtInvalidNormals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModifyAtInvalidNormals.
                    """

                class _InvalidNormalMethod(PyTextualCommandArgumentsSubItem):
                    """
                    Argument InvalidNormalMethod.
                    """

                class _NumberOfSplitLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfSplitLayers.
                    """

                class _ShowLocalPrismPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowLocalPrismPreferences.
                    """

                class _LastRatioNumLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _AllowedTangencyAtInvalidNormals(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AllowedTangencyAtInvalidNormals.
                    """

                class _RemeshAtInvalidNormals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshAtInvalidNormals.
                    """

                class _IgnoreBoundaryLayers(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IgnoreBoundaryLayers.
                    """

            class _BLZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument BLZoneList.
                """

            class _BLRegionList(PyTextualCommandArgumentsSubItem):
                """
                Argument BLRegionList.
                """

            class _InvalidAdded(PyTextualCommandArgumentsSubItem):
                """
                Argument InvalidAdded.
                """

            class _CompleteRegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteRegionScope.
                """

            class _CompleteBlLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteBlLabelList.
                """

            class _CompleteBLZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteBLZoneList.
                """

            class _CompleteBLRegionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteBLRegionList.
                """

            class _CompleteZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneSelectionList.
                """

            class _CompleteLabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

        def create_instance(self) -> _AddBoundaryLayersCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddBoundaryLayersCommandArguments(*args)

    class AddBoundaryLayersForPartReplacement(PyCommand):
        """
        Command AddBoundaryLayersForPartReplacement.

        Parameters
        ----------
        AddChild : str
            Determine whether or not you want to specify one or more boundary layers for your replacement part(s).
        ReadPrismControlFile : str
        BLControlName : str
            Specify a name for the boundary layer control or use the default value.
        OffsetMethodType : str
            Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
        NumberOfLayers : int
            Select the number of boundary layers to be generated.
        FirstAspectRatio : float
            Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
        TransitionRatio : float
            Specify the rate at which adjacent elements grow, for the smooth transition offset method.
        Rate : float
            Specify the rate of growth for the boundary layer.
        FirstHeight : float
            Specify the height of the first layer of cells in the boundary layer.
        MaxLayerHeight : float
        FaceScope : dict[str, Any]
        RegionScope : list[str]
            Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        BlLabelList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LocalPrismPreferences : dict[str, Any]
        BLZoneList : list[str]
        BLRegionList : list[str]
        CompleteRegionScope : list[str]
        CompleteBlLabelList : list[str]
        CompleteBLZoneList : list[str]
        CompleteBLRegionList : list[str]
        CompleteZoneSelectionList : list[str]
        CompleteLabelSelectionList : list[str]

        Returns
        -------
        bool
        """
        class _AddBoundaryLayersForPartReplacementCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.ReadPrismControlFile = self._ReadPrismControlFile(self, "ReadPrismControlFile", service, rules, path)
                self.BLControlName = self._BLControlName(self, "BLControlName", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.FirstAspectRatio = self._FirstAspectRatio(self, "FirstAspectRatio", service, rules, path)
                self.TransitionRatio = self._TransitionRatio(self, "TransitionRatio", service, rules, path)
                self.Rate = self._Rate(self, "Rate", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.MaxLayerHeight = self._MaxLayerHeight(self, "MaxLayerHeight", service, rules, path)
                self.FaceScope = self._FaceScope(self, "FaceScope", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.BlLabelList = self._BlLabelList(self, "BlLabelList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LocalPrismPreferences = self._LocalPrismPreferences(self, "LocalPrismPreferences", service, rules, path)
                self.BLZoneList = self._BLZoneList(self, "BLZoneList", service, rules, path)
                self.BLRegionList = self._BLRegionList(self, "BLRegionList", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)
                self.CompleteBlLabelList = self._CompleteBlLabelList(self, "CompleteBlLabelList", service, rules, path)
                self.CompleteBLZoneList = self._CompleteBLZoneList(self, "CompleteBLZoneList", service, rules, path)
                self.CompleteBLRegionList = self._CompleteBLRegionList(self, "CompleteBLRegionList", service, rules, path)
                self.CompleteZoneSelectionList = self._CompleteZoneSelectionList(self, "CompleteZoneSelectionList", service, rules, path)
                self.CompleteLabelSelectionList = self._CompleteLabelSelectionList(self, "CompleteLabelSelectionList", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to specify one or more boundary layers for your replacement part(s).
                """

            class _ReadPrismControlFile(PyTextualCommandArgumentsSubItem):
                """
                Argument ReadPrismControlFile.
                """

            class _BLControlName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the boundary layer control or use the default value.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
                """

            class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                """
                Select the number of boundary layers to be generated.
                """

            class _FirstAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
                """

            class _TransitionRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the rate at which adjacent elements grow, for the smooth transition offset method.
                """

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the rate of growth for the boundary layer.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _MaxLayerHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _FaceScope(PySingletonCommandArgumentsSubItem):
                """
                Argument FaceScope.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                    self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                    self.FaceScopeMeshObject = self._FaceScopeMeshObject(self, "FaceScopeMeshObject", service, rules, path)
                    self.RegionsType = self._RegionsType(self, "RegionsType", service, rules, path)

                class _TopologyList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument TopologyList.
                    """

                class _GrowOn(PyTextualCommandArgumentsSubItem):
                    """
                    Argument GrowOn.
                    """

                class _FaceScopeMeshObject(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FaceScopeMeshObject.
                    """

                class _RegionsType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RegionsType.
                    """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BlLabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LocalPrismPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument LocalPrismPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.LastRatio = self._LastRatio(self, "LastRatio", service, rules, path)
                    self.AdditionalIgnoredLayers = self._AdditionalIgnoredLayers(self, "AdditionalIgnoredLayers", service, rules, path)
                    self.SphereRadiusFactorAtInvalidNormals = self._SphereRadiusFactorAtInvalidNormals(self, "SphereRadiusFactorAtInvalidNormals", service, rules, path)
                    self.SmoothRingsAtInvalidNormals = self._SmoothRingsAtInvalidNormals(self, "SmoothRingsAtInvalidNormals", service, rules, path)
                    self.Continuous = self._Continuous(self, "Continuous", service, rules, path)
                    self.ModifyAtInvalidNormals = self._ModifyAtInvalidNormals(self, "ModifyAtInvalidNormals", service, rules, path)
                    self.SplitPrism = self._SplitPrism(self, "SplitPrism", service, rules, path)
                    self.InvalidNormalMethod = self._InvalidNormalMethod(self, "InvalidNormalMethod", service, rules, path)
                    self.ShowLocalPrismPreferences = self._ShowLocalPrismPreferences(self, "ShowLocalPrismPreferences", service, rules, path)
                    self.NumberOfSplitLayers = self._NumberOfSplitLayers(self, "NumberOfSplitLayers", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.AllowedTangencyAtInvalidNormals = self._AllowedTangencyAtInvalidNormals(self, "AllowedTangencyAtInvalidNormals", service, rules, path)
                    self.RemeshAtInvalidNormals = self._RemeshAtInvalidNormals(self, "RemeshAtInvalidNormals", service, rules, path)
                    self.IgnoreBoundaryLayers = self._IgnoreBoundaryLayers(self, "IgnoreBoundaryLayers", service, rules, path)

                class _LastRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatio.
                    """

                class _AdditionalIgnoredLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AdditionalIgnoredLayers.
                    """

                class _SphereRadiusFactorAtInvalidNormals(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SphereRadiusFactorAtInvalidNormals.
                    """

                class _SmoothRingsAtInvalidNormals(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SmoothRingsAtInvalidNormals.
                    """

                class _Continuous(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Continuous.
                    """

                class _ModifyAtInvalidNormals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModifyAtInvalidNormals.
                    """

                class _SplitPrism(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SplitPrism.
                    """

                class _InvalidNormalMethod(PyTextualCommandArgumentsSubItem):
                    """
                    Argument InvalidNormalMethod.
                    """

                class _ShowLocalPrismPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowLocalPrismPreferences.
                    """

                class _NumberOfSplitLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfSplitLayers.
                    """

                class _LastRatioNumLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _AllowedTangencyAtInvalidNormals(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AllowedTangencyAtInvalidNormals.
                    """

                class _RemeshAtInvalidNormals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshAtInvalidNormals.
                    """

                class _IgnoreBoundaryLayers(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IgnoreBoundaryLayers.
                    """

            class _BLZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument BLZoneList.
                """

            class _BLRegionList(PyTextualCommandArgumentsSubItem):
                """
                Argument BLRegionList.
                """

            class _CompleteRegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteRegionScope.
                """

            class _CompleteBlLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteBlLabelList.
                """

            class _CompleteBLZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteBLZoneList.
                """

            class _CompleteBLRegionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteBLRegionList.
                """

            class _CompleteZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneSelectionList.
                """

            class _CompleteLabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

        def create_instance(self) -> _AddBoundaryLayersForPartReplacementCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddBoundaryLayersForPartReplacementCommandArguments(*args)

    class AddBoundaryType(PyCommand):
        """
        Command AddBoundaryType.

        Parameters
        ----------
        MeshObject : str
        NewBoundaryLabelName : str
            Specify a name for the boundary type.
        NewBoundaryType : str
            Choose a boundary type from the available options.
        SelectionType : str
        BoundaryFaceZoneList : list[str]
            Enter a text string to filter out the list of zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        Merge : str
            Determine whether or not to merge the selected zones (set to yes by default).
        ZoneLocation : list[str]

        Returns
        -------
        bool
        """
        class _AddBoundaryTypeCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.NewBoundaryLabelName = self._NewBoundaryLabelName(self, "NewBoundaryLabelName", service, rules, path)
                self.NewBoundaryType = self._NewBoundaryType(self, "NewBoundaryType", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.BoundaryFaceZoneList = self._BoundaryFaceZoneList(self, "BoundaryFaceZoneList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.Merge = self._Merge(self, "Merge", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _NewBoundaryLabelName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the boundary type.
                """

            class _NewBoundaryType(PyTextualCommandArgumentsSubItem):
                """
                Choose a boundary type from the available options.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _BoundaryFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Enter a text string to filter out the list of zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _Merge(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not to merge the selected zones (set to yes by default).
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _AddBoundaryTypeCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddBoundaryTypeCommandArguments(*args)

    class AddLocalSizingFTM(PyCommand):
        """
        Command AddLocalSizingFTM.

        Parameters
        ----------
        LocalSettingsName : str
            Specify a name for the size control or use the default value.
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        EdgeSelectionList : list[str]
            Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LocalSizeControlParameters : dict[str, Any]
        ValueChanged : str
        CompleteZoneSelectionList : list[str]
        CompleteLabelSelectionList : list[str]
        CompleteObjectSelectionList : list[str]
        CompleteEdgeSelectionList : list[str]

        Returns
        -------
        bool
        """
        class _AddLocalSizingFTMCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LocalSettingsName = self._LocalSettingsName(self, "LocalSettingsName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                self.LocalSizeControlParameters = self._LocalSizeControlParameters(self, "LocalSizeControlParameters", service, rules, path)
                self.ValueChanged = self._ValueChanged(self, "ValueChanged", service, rules, path)
                self.CompleteZoneSelectionList = self._CompleteZoneSelectionList(self, "CompleteZoneSelectionList", service, rules, path)
                self.CompleteLabelSelectionList = self._CompleteLabelSelectionList(self, "CompleteLabelSelectionList", service, rules, path)
                self.CompleteObjectSelectionList = self._CompleteObjectSelectionList(self, "CompleteObjectSelectionList", service, rules, path)
                self.CompleteEdgeSelectionList = self._CompleteEdgeSelectionList(self, "CompleteEdgeSelectionList", service, rules, path)

            class _LocalSettingsName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the size control or use the default value.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LocalSizeControlParameters(PySingletonCommandArgumentsSubItem):
                """
                Argument LocalSizeControlParameters.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.IgnoreSelf = self._IgnoreSelf(self, "IgnoreSelf", service, rules, path)
                    self.WrapMin = self._WrapMin(self, "WrapMin", service, rules, path)
                    self.WrapCellsPerGap = self._WrapCellsPerGap(self, "WrapCellsPerGap", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.WrapMax = self._WrapMax(self, "WrapMax", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.InitialSizeControl = self._InitialSizeControl(self, "InitialSizeControl", service, rules, path)
                    self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                    self.WrapGrowthRate = self._WrapGrowthRate(self, "WrapGrowthRate", service, rules, path)
                    self.WrapCurvatureNormalAngle = self._WrapCurvatureNormalAngle(self, "WrapCurvatureNormalAngle", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.TargetSizeControl = self._TargetSizeControl(self, "TargetSizeControl", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _IgnoreSelf(PyParameterCommandArgumentsSubItem):
                    """
                    Argument IgnoreSelf.
                    """

                class _WrapMin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapMin.
                    """

                class _WrapCellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapCellsPerGap.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _WrapMax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapMax.
                    """

                class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AdvancedOptions.
                    """

                class _InitialSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument InitialSizeControl.
                    """

                class _SizingType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizingType.
                    """

                class _WrapGrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapGrowthRate.
                    """

                class _WrapCurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapCurvatureNormalAngle.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _TargetSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument TargetSizeControl.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

            class _ValueChanged(PyTextualCommandArgumentsSubItem):
                """
                Argument ValueChanged.
                """

            class _CompleteZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneSelectionList.
                """

            class _CompleteLabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

            class _CompleteObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteObjectSelectionList.
                """

            class _CompleteEdgeSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteEdgeSelectionList.
                """

        def create_instance(self) -> _AddLocalSizingFTMCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddLocalSizingFTMCommandArguments(*args)

    class AddLocalSizingWTM(PyCommand):
        """
        Command AddLocalSizingWTM.

        Parameters
        ----------
        AddChild : str
            Choose whether or not you want to add local size controls in order to create the surface mesh.
        BOIControlName : str
            Provide a name for this specific size control.
        BOIGrowthRate : float
            Specify the increase in element edge length with each succeeding layer of elements.
        BOIExecution : str
            Choose whether the size control is to be applied to a local edge size, a local face size, a local body size, a body of influence, a face of influence, curvature, or proximity.
        AssignSizeUsing : str
        BOISize : float
            Specify a value for the desired size of the local sizing (or body/face of influence) to be applied to the indicated label(s) or zone(s).
        NumberofLayers : int
        SmallestHeight : float
        GrowthPattern : str
        GrowthMethod : str
        BiasFactor : float
        BOIMinSize : float
            Specify the minimum size of the elements for the surface mesh.
        BOIMaxSize : float
            Specify the maximum size of the elements for the surface mesh.
        BOICurvatureNormalAngle : float
            Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
        BOICellsPerGap : float
            Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
        BOIScopeTo : str
            Set curvature or proximity based refinement. The edges option considers edge-to-edge proximity, while faces considers face-to-face proximity, and faces and edges considers both. The edge labels option considers edge sizing based on edge labels. Note that when you use the edges or the faces and edges options, you can only select face zones or face labels. Also, saving a size control file after using either of these two options will not be persistent.
        IgnoreOrientation : str
            Specify whether or not you need to apply additional refinement in and around thin areas (such as between plates), without over-refinement. This ignores face proximity within voids and will not allow you to refine in thin voids, but will allow refinement in gaps. This should be used in predominantly fluid regions with no thin solid regions.
        BOIZoneorLabel : str
            Choose how you want to select your surface (by label or by zone).
        BOIFaceLabelList : list[str]
            Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        BOIFaceZoneList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        EdgeLabelList : list[str]
        EdgeZoneList : list[str]
        TopologyList : list[str]
        ReverseEdgeZoneOrientation : bool
        ReverseEdgeZoneList : list[str]
        BOIPatchingtoggle : bool
            Enable this option to repair any openings that may still exist in the body of influence-based local sizing control.
        DrawSizeControl : bool
            Enable this field to display the size boxes in the graphics window.
        ZoneLocation : list[str]
        CompleteFaceZoneList : list[str]
        CompleteFaceLabelList : list[str]
        CompleteEdgeLabelList : list[str]
        CompleteTopologyList : list[str]
        PrimeSizeControlId : int

        Returns
        -------
        bool
        """
        class _AddLocalSizingWTMCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.BOIControlName = self._BOIControlName(self, "BOIControlName", service, rules, path)
                self.BOIGrowthRate = self._BOIGrowthRate(self, "BOIGrowthRate", service, rules, path)
                self.BOIExecution = self._BOIExecution(self, "BOIExecution", service, rules, path)
                self.AssignSizeUsing = self._AssignSizeUsing(self, "AssignSizeUsing", service, rules, path)
                self.BOISize = self._BOISize(self, "BOISize", service, rules, path)
                self.NumberofLayers = self._NumberofLayers(self, "NumberofLayers", service, rules, path)
                self.SmallestHeight = self._SmallestHeight(self, "SmallestHeight", service, rules, path)
                self.GrowthPattern = self._GrowthPattern(self, "GrowthPattern", service, rules, path)
                self.GrowthMethod = self._GrowthMethod(self, "GrowthMethod", service, rules, path)
                self.BiasFactor = self._BiasFactor(self, "BiasFactor", service, rules, path)
                self.BOIMinSize = self._BOIMinSize(self, "BOIMinSize", service, rules, path)
                self.BOIMaxSize = self._BOIMaxSize(self, "BOIMaxSize", service, rules, path)
                self.BOICurvatureNormalAngle = self._BOICurvatureNormalAngle(self, "BOICurvatureNormalAngle", service, rules, path)
                self.BOICellsPerGap = self._BOICellsPerGap(self, "BOICellsPerGap", service, rules, path)
                self.BOIScopeTo = self._BOIScopeTo(self, "BOIScopeTo", service, rules, path)
                self.IgnoreOrientation = self._IgnoreOrientation(self, "IgnoreOrientation", service, rules, path)
                self.BOIZoneorLabel = self._BOIZoneorLabel(self, "BOIZoneorLabel", service, rules, path)
                self.BOIFaceLabelList = self._BOIFaceLabelList(self, "BOIFaceLabelList", service, rules, path)
                self.BOIFaceZoneList = self._BOIFaceZoneList(self, "BOIFaceZoneList", service, rules, path)
                self.EdgeLabelList = self._EdgeLabelList(self, "EdgeLabelList", service, rules, path)
                self.EdgeZoneList = self._EdgeZoneList(self, "EdgeZoneList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.ReverseEdgeZoneOrientation = self._ReverseEdgeZoneOrientation(self, "ReverseEdgeZoneOrientation", service, rules, path)
                self.ReverseEdgeZoneList = self._ReverseEdgeZoneList(self, "ReverseEdgeZoneList", service, rules, path)
                self.BOIPatchingtoggle = self._BOIPatchingtoggle(self, "BOIPatchingtoggle", service, rules, path)
                self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.CompleteFaceZoneList = self._CompleteFaceZoneList(self, "CompleteFaceZoneList", service, rules, path)
                self.CompleteFaceLabelList = self._CompleteFaceLabelList(self, "CompleteFaceLabelList", service, rules, path)
                self.CompleteEdgeLabelList = self._CompleteEdgeLabelList(self, "CompleteEdgeLabelList", service, rules, path)
                self.CompleteTopologyList = self._CompleteTopologyList(self, "CompleteTopologyList", service, rules, path)
                self.PrimeSizeControlId = self._PrimeSizeControlId(self, "PrimeSizeControlId", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Choose whether or not you want to add local size controls in order to create the surface mesh.
                """

            class _BOIControlName(PyTextualCommandArgumentsSubItem):
                """
                Provide a name for this specific size control.
                """

            class _BOIGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the increase in element edge length with each succeeding layer of elements.
                """

            class _BOIExecution(PyTextualCommandArgumentsSubItem):
                """
                Choose whether the size control is to be applied to a local edge size, a local face size, a local body size, a body of influence, a face of influence, curvature, or proximity.
                """

            class _AssignSizeUsing(PyTextualCommandArgumentsSubItem):
                """
                Argument AssignSizeUsing.
                """

            class _BOISize(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the desired size of the local sizing (or body/face of influence) to be applied to the indicated label(s) or zone(s).
                """

            class _NumberofLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberofLayers.
                """

            class _SmallestHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument SmallestHeight.
                """

            class _GrowthPattern(PyTextualCommandArgumentsSubItem):
                """
                Argument GrowthPattern.
                """

            class _GrowthMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument GrowthMethod.
                """

            class _BiasFactor(PyNumericalCommandArgumentsSubItem):
                """
                Argument BiasFactor.
                """

            class _BOIMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify the minimum size of the elements for the surface mesh.
                """

            class _BOIMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum size of the elements for the surface mesh.
                """

            class _BOICurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
                """

            class _BOICellsPerGap(PyNumericalCommandArgumentsSubItem):
                """
                Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                """

            class _BOIScopeTo(PyTextualCommandArgumentsSubItem):
                """
                Set curvature or proximity based refinement. The edges option considers edge-to-edge proximity, while faces considers face-to-face proximity, and faces and edges considers both. The edge labels option considers edge sizing based on edge labels. Note that when you use the edges or the faces and edges options, you can only select face zones or face labels. Also, saving a size control file after using either of these two options will not be persistent.
                """

            class _IgnoreOrientation(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you need to apply additional refinement in and around thin areas (such as between plates), without over-refinement. This ignores face proximity within voids and will not allow you to refine in thin voids, but will allow refinement in gaps. This should be used in predominantly fluid regions with no thin solid regions.
                """

            class _BOIZoneorLabel(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to select your surface (by label or by zone).
                """

            class _BOIFaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BOIFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelList.
                """

            class _EdgeZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeZoneList.
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _ReverseEdgeZoneOrientation(PyParameterCommandArgumentsSubItem):
                """
                Argument ReverseEdgeZoneOrientation.
                """

            class _ReverseEdgeZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ReverseEdgeZoneList.
                """

            class _BOIPatchingtoggle(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to repair any openings that may still exist in the body of influence-based local sizing control.
                """

            class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Enable this field to display the size boxes in the graphics window.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _CompleteFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteFaceZoneList.
                """

            class _CompleteFaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteFaceLabelList.
                """

            class _CompleteEdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteEdgeLabelList.
                """

            class _CompleteTopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteTopologyList.
                """

            class _PrimeSizeControlId(PyNumericalCommandArgumentsSubItem):
                """
                Argument PrimeSizeControlId.
                """

        def create_instance(self) -> _AddLocalSizingWTMCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddLocalSizingWTMCommandArguments(*args)

    class AddMultiZoneControls(PyCommand):
        """
        Command AddMultiZoneControls.

        Parameters
        ----------
        ControlType : str
            Determine if you want to define the multi-zone control by selecting regions or edges.
        MultiZName : str
            Enter a name for the multi-zone mesh control, or use the default.
        MeshMethod : str
            Choose a multi-zone meshing technique: Standard or the Thin volume technique (for only a single layer)
        FillWith : str
            Choose a multi-zone meshing fill type: Hex-Pave, Hex-Map, Prism, or Mixed.
        UseSweepSize : str
            Determine whether or not a variable (no) or a fixed (yes) sweep size is to be applied to the multi-zone mesh control.
        MaxSweepSize : float
            Indicates the maximum value for the sweep size.
        RegionScope : list[str]
            Select the named region(s) from the list to which you would like to create the multi-zone control. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        SourceMethod : str
            Choose one or more face zones or labels from the list below. You can also provide the ability to select all source-target zones that are parallel to a global plane by choosing Zones parallel to XY plane, Zones parallel to XZ plane, or Zones parallel to YZ plane. For zones or labels. use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ParallelSelection : bool
            When your desired zones are aligned with the global x,y, or z plane, enable this checkbox to automatically select all parallel zones in  the selected region(s).
        ShowEdgeBiasing : str
            If edge labels are automatically created on all edges, preserving the face/edge topology, use this field to determine if you want to save time and preview any edge biasing, since when many edges are selected, there can be many nodes and biases that can take additional time. Choices include yes, selected to only preview the selected edge, yes, all to preview all edges, and no to not preview edge biasing.
        LabelSourceList : list[str]
            Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSourceList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        AssignSizeUsing : str
            For edge-based multizone controls, you can choose from Interval, Size, or Smallest Height. If double graded biasing is used and the Interval is set to an odd number (or the Size or Smallest Height results in an odd number Interval), the interval will automatically be increased by one.
        Intervals : int
            Specify the number of intervals for the edge-based multizone control. If double graded biasing is used and the Interval is set to an odd number (or the Size or Smallest Height results in an odd number Interval), the interval will automatically be increased by one.
        Size : float
            Specify the minimum size for the edge-based multizone control.
        SmallestHeight : float
            Specify a value for the smallest height for the edge-based multizone control.
        BiasMethod : str
            Select from a choice of patterns that you want to apply to your edge-based multizone control.
        GrowthMethod : str
            For edge-based multizone controls when using variable Growth Patterns, determine how you would like to determine the growth: either as a Growth Rate or as Bias Factor.
        GrowthRate : float
            Specify a value for the growth rate for the multizone, or use the default value.
        BiasFactor : float
            Specify a value for the bias factor for the multizone, or use the default value. The Bias Factor is the ratio of the largest to the smallest segment on the edge.
        EdgeLabelSelection : list[str]
        EdgeLabelList : list[str]
            Choose one or more edge labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CFDSurfaceMeshControls : dict[str, Any]
        CompleteRegionScope : list[str]
        CompleteEdgeScope : list[str]

        Returns
        -------
        bool
        """
        class _AddMultiZoneControlsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ControlType = self._ControlType(self, "ControlType", service, rules, path)
                self.MultiZName = self._MultiZName(self, "MultiZName", service, rules, path)
                self.MeshMethod = self._MeshMethod(self, "MeshMethod", service, rules, path)
                self.FillWith = self._FillWith(self, "FillWith", service, rules, path)
                self.UseSweepSize = self._UseSweepSize(self, "UseSweepSize", service, rules, path)
                self.MaxSweepSize = self._MaxSweepSize(self, "MaxSweepSize", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.SourceMethod = self._SourceMethod(self, "SourceMethod", service, rules, path)
                self.ParallelSelection = self._ParallelSelection(self, "ParallelSelection", service, rules, path)
                self.ShowEdgeBiasing = self._ShowEdgeBiasing(self, "ShowEdgeBiasing", service, rules, path)
                self.LabelSourceList = self._LabelSourceList(self, "LabelSourceList", service, rules, path)
                self.ZoneSourceList = self._ZoneSourceList(self, "ZoneSourceList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.AssignSizeUsing = self._AssignSizeUsing(self, "AssignSizeUsing", service, rules, path)
                self.Intervals = self._Intervals(self, "Intervals", service, rules, path)
                self.Size = self._Size(self, "Size", service, rules, path)
                self.SmallestHeight = self._SmallestHeight(self, "SmallestHeight", service, rules, path)
                self.BiasMethod = self._BiasMethod(self, "BiasMethod", service, rules, path)
                self.GrowthMethod = self._GrowthMethod(self, "GrowthMethod", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.BiasFactor = self._BiasFactor(self, "BiasFactor", service, rules, path)
                self.EdgeLabelSelection = self._EdgeLabelSelection(self, "EdgeLabelSelection", service, rules, path)
                self.EdgeLabelList = self._EdgeLabelList(self, "EdgeLabelList", service, rules, path)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)
                self.CompleteEdgeScope = self._CompleteEdgeScope(self, "CompleteEdgeScope", service, rules, path)

            class _ControlType(PyTextualCommandArgumentsSubItem):
                """
                Determine if you want to define the multi-zone control by selecting regions or edges.
                """

            class _MultiZName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the multi-zone mesh control, or use the default.
                """

            class _MeshMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose a multi-zone meshing technique: Standard or the Thin volume technique (for only a single layer)
                """

            class _FillWith(PyTextualCommandArgumentsSubItem):
                """
                Choose a multi-zone meshing fill type: Hex-Pave, Hex-Map, Prism, or Mixed.
                """

            class _UseSweepSize(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not a variable (no) or a fixed (yes) sweep size is to be applied to the multi-zone mesh control.
                """

            class _MaxSweepSize(PyNumericalCommandArgumentsSubItem):
                """
                Indicates the maximum value for the sweep size.
                """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Select the named region(s) from the list to which you would like to create the multi-zone control. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _SourceMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones or labels from the list below. You can also provide the ability to select all source-target zones that are parallel to a global plane by choosing Zones parallel to XY plane, Zones parallel to XZ plane, or Zones parallel to YZ plane. For zones or labels. use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ParallelSelection(PyParameterCommandArgumentsSubItem):
                """
                When your desired zones are aligned with the global x,y, or z plane, enable this checkbox to automatically select all parallel zones in  the selected region(s).
                """

            class _ShowEdgeBiasing(PyTextualCommandArgumentsSubItem):
                """
                If edge labels are automatically created on all edges, preserving the face/edge topology, use this field to determine if you want to save time and preview any edge biasing, since when many edges are selected, there can be many nodes and biases that can take additional time. Choices include yes, selected to only preview the selected edge, yes, all to preview all edges, and no to not preview edge biasing.
                """

            class _LabelSourceList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSourceList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _AssignSizeUsing(PyTextualCommandArgumentsSubItem):
                """
                For edge-based multizone controls, you can choose from Interval, Size, or Smallest Height. If double graded biasing is used and the Interval is set to an odd number (or the Size or Smallest Height results in an odd number Interval), the interval will automatically be increased by one.
                """

            class _Intervals(PyNumericalCommandArgumentsSubItem):
                """
                Specify the number of intervals for the edge-based multizone control. If double graded biasing is used and the Interval is set to an odd number (or the Size or Smallest Height results in an odd number Interval), the interval will automatically be increased by one.
                """

            class _Size(PyNumericalCommandArgumentsSubItem):
                """
                Specify the minimum size for the edge-based multizone control.
                """

            class _SmallestHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the smallest height for the edge-based multizone control.
                """

            class _BiasMethod(PyTextualCommandArgumentsSubItem):
                """
                Select from a choice of patterns that you want to apply to your edge-based multizone control.
                """

            class _GrowthMethod(PyTextualCommandArgumentsSubItem):
                """
                For edge-based multizone controls when using variable Growth Patterns, determine how you would like to determine the growth: either as a Growth Rate or as Bias Factor.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the growth rate for the multizone, or use the default value.
                """

            class _BiasFactor(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the bias factor for the multizone, or use the default value. The Bias Factor is the ratio of the largest to the smallest segment on the edge.
                """

            class _EdgeLabelSelection(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelSelection.
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more edge labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CFDSurfaceMeshControls(PySingletonCommandArgumentsSubItem):
                """
                Argument CFDSurfaceMeshControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SaveSizeFieldFile = self._SaveSizeFieldFile(self, "SaveSizeFieldFile", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.PreviewSizefield = self._PreviewSizefield(self, "PreviewSizefield", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.SaveSizeField = self._SaveSizeField(self, "SaveSizeField", service, rules, path)
                    self.UseSizeFiles = self._UseSizeFiles(self, "UseSizeFiles", service, rules, path)
                    self.AutoCreateScopedSizing = self._AutoCreateScopedSizing(self, "AutoCreateScopedSizing", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyParameterCommandArgumentsSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _CompleteRegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteRegionScope.
                """

            class _CompleteEdgeScope(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteEdgeScope.
                """

        def create_instance(self) -> _AddMultiZoneControlsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddMultiZoneControlsCommandArguments(*args)

    class AddShellBoundaryLayerControls(PyCommand):
        """
        Command AddShellBoundaryLayerControls.

        Parameters
        ----------
        AddChild : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        LastAspectRatio : float
        Rate : float
        FirstLayerHeight : float
        MaxLayerHeight : float
        GrowOn : str
        FaceLabelList : list[str]
        FaceZoneList : list[str]
        EdgeSelectionType : str
        EdgeLabelList : list[str]
        EdgeZoneList : list[str]
        ShellBLAdvancedOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _AddShellBoundaryLayerControlsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.BLControlName = self._BLControlName(self, "BLControlName", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.FirstAspectRatio = self._FirstAspectRatio(self, "FirstAspectRatio", service, rules, path)
                self.LastAspectRatio = self._LastAspectRatio(self, "LastAspectRatio", service, rules, path)
                self.Rate = self._Rate(self, "Rate", service, rules, path)
                self.FirstLayerHeight = self._FirstLayerHeight(self, "FirstLayerHeight", service, rules, path)
                self.MaxLayerHeight = self._MaxLayerHeight(self, "MaxLayerHeight", service, rules, path)
                self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                self.FaceLabelList = self._FaceLabelList(self, "FaceLabelList", service, rules, path)
                self.FaceZoneList = self._FaceZoneList(self, "FaceZoneList", service, rules, path)
                self.EdgeSelectionType = self._EdgeSelectionType(self, "EdgeSelectionType", service, rules, path)
                self.EdgeLabelList = self._EdgeLabelList(self, "EdgeLabelList", service, rules, path)
                self.EdgeZoneList = self._EdgeZoneList(self, "EdgeZoneList", service, rules, path)
                self.ShellBLAdvancedOptions = self._ShellBLAdvancedOptions(self, "ShellBLAdvancedOptions", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Argument AddChild.
                """

            class _BLControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument BLControlName.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Argument OffsetMethodType.
                """

            class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfLayers.
                """

            class _FirstAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstAspectRatio.
                """

            class _LastAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument LastAspectRatio.
                """

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Argument Rate.
                """

            class _FirstLayerHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstLayerHeight.
                """

            class _MaxLayerHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _GrowOn(PyTextualCommandArgumentsSubItem):
                """
                Argument GrowOn.
                """

            class _FaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceLabelList.
                """

            class _FaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceZoneList.
                """

            class _EdgeSelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeSelectionType.
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelList.
                """

            class _EdgeZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeZoneList.
                """

            class _ShellBLAdvancedOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument ShellBLAdvancedOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowShellBLAdvancedOptions = self._ShowShellBLAdvancedOptions(self, "ShowShellBLAdvancedOptions", service, rules, path)
                    self.ExposeSide = self._ExposeSide(self, "ExposeSide", service, rules, path)
                    self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                    self.AdjacentAttachAngle = self._AdjacentAttachAngle(self, "AdjacentAttachAngle", service, rules, path)

                class _ShowShellBLAdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowShellBLAdvancedOptions.
                    """

                class _ExposeSide(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExposeSide.
                    """

                class _MaxAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxAspectRatio.
                    """

                class _MinAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinAspectRatio.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _LastRatioNumLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _GapFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GapFactor.
                    """

                class _AdjacentAttachAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AdjacentAttachAngle.
                    """

        def create_instance(self) -> _AddShellBoundaryLayerControlsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddShellBoundaryLayerControlsCommandArguments(*args)

    class AddThickness(PyCommand):
        """
        Command AddThickness.

        Parameters
        ----------
        ZeroThicknessName : str
            Specify a name for the thickness control or use the default value.
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        Distance : float
            Specify a value that adds thickness to the selected object. Thickness is applied in the normal direction. Negative values are allowed to preview the opposite/flipped direction. The original face normal will be kept, but you can add thickness in either direction based on a positive or negative value.

        Returns
        -------
        bool
        """
        class _AddThicknessCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ZeroThicknessName = self._ZeroThicknessName(self, "ZeroThicknessName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.Distance = self._Distance(self, "Distance", service, rules, path)

            class _ZeroThicknessName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the thickness control or use the default value.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _Distance(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value that adds thickness to the selected object. Thickness is applied in the normal direction. Negative values are allowed to preview the opposite/flipped direction. The original face normal will be kept, but you can add thickness in either direction based on a positive or negative value.
                """

        def create_instance(self) -> _AddThicknessCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddThicknessCommandArguments(*args)

    class AddThinVolumeMeshControls(PyCommand):
        """
        Command AddThinVolumeMeshControls.

        Parameters
        ----------
        ThinMeshingName : str
            Enter a name for the thin volume mesh control, or use the default.
        AssignSizeUsing : str
            Specify the sizing of the mesh layers to be based on Intervals or based on the Size of the plates.
        Intervals : int
            Specifies the number of mesh layers to be created within the thin volume mesh.
        Size : float
            enter the Size of each thin mesh layer or use the default.
        GrowthRate : float
            Specify the Growth Rate which is the expansion rate of the extrusion for each thin volume mesh layer and is set to 1 by default. A growth rate of 1.2 for example will expand each layer of the extrusion by 20 percent of the previous length.
        RemeshOverlapping : bool
        DoubleBiasing : bool
            Enable the Doubling biasing option to invoke double biasing on edges of the thin volume mesh layers. Enabling double biasing will automatically set the Growth Rate to 1.3. When disabled, the thin volume mesh can only be graded from the Source to the Target.
        SideImprints : bool
            Specifies the mesher to project the outer nodes of the thin volume mesh onto adjacent boundary face zones and is enabled by default. This ensures that geometric details of the thin volume are accurately captured at the boundary.
        StackedPlates : bool
            For models consisting of stacked planar plates, you can enable the Stacked Plates option to select all source-target zones that are aligned with the global x-y-z plane.
        AutoControlCreation : bool
            enter the Size of each thin mesh layer or use the default.
        RegionScope : list[str]
            Specify the Region(s) where the thin volume meshing controls will be applied.
        SelectSourceBy : str
            Choose whether to select the source surfaces by label or by zone.
        ParallelSource : bool
            Enable this option if you have multiple source zones in parallel that you want to select for thin meshing.
        LabelSourceList : list[str]
            Select the label(s) to use as the source.
        ZoneSourceList : list[str]
            Select the zone(s) to use as the source.
        SelectTargetBy : str
            Choose whether to select the source surfaces by label or by zone.
        ParallelTarget : bool
            Enable this option if you have multiple target zones in parallel that you want to select for thin meshing,
        LabelTargetList : list[str]
            Select the label(s) to use as the target.
        ZoneTargetList : list[str]
            Select the zone(s) to use as the target.
        ThinVolRegs : list[str]
        CompleteRegionScope : list[str]
        CompleteLabelSourceList : list[str]
        CompleteZoneSourceList : list[str]
        CompleteLabelTargetList : list[str]
        CompleteZoneTargetList : list[str]
        ThinVolumePreferences : dict[str, Any]
        ZoneLocation : list[str]
        ZoneLocation2 : list[str]

        Returns
        -------
        bool
        """
        class _AddThinVolumeMeshControlsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ThinMeshingName = self._ThinMeshingName(self, "ThinMeshingName", service, rules, path)
                self.AssignSizeUsing = self._AssignSizeUsing(self, "AssignSizeUsing", service, rules, path)
                self.Intervals = self._Intervals(self, "Intervals", service, rules, path)
                self.Size = self._Size(self, "Size", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.RemeshOverlapping = self._RemeshOverlapping(self, "RemeshOverlapping", service, rules, path)
                self.DoubleBiasing = self._DoubleBiasing(self, "DoubleBiasing", service, rules, path)
                self.SideImprints = self._SideImprints(self, "SideImprints", service, rules, path)
                self.StackedPlates = self._StackedPlates(self, "StackedPlates", service, rules, path)
                self.AutoControlCreation = self._AutoControlCreation(self, "AutoControlCreation", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.SelectSourceBy = self._SelectSourceBy(self, "SelectSourceBy", service, rules, path)
                self.ParallelSource = self._ParallelSource(self, "ParallelSource", service, rules, path)
                self.LabelSourceList = self._LabelSourceList(self, "LabelSourceList", service, rules, path)
                self.ZoneSourceList = self._ZoneSourceList(self, "ZoneSourceList", service, rules, path)
                self.SelectTargetBy = self._SelectTargetBy(self, "SelectTargetBy", service, rules, path)
                self.ParallelTarget = self._ParallelTarget(self, "ParallelTarget", service, rules, path)
                self.LabelTargetList = self._LabelTargetList(self, "LabelTargetList", service, rules, path)
                self.ZoneTargetList = self._ZoneTargetList(self, "ZoneTargetList", service, rules, path)
                self.ThinVolRegs = self._ThinVolRegs(self, "ThinVolRegs", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)
                self.CompleteLabelSourceList = self._CompleteLabelSourceList(self, "CompleteLabelSourceList", service, rules, path)
                self.CompleteZoneSourceList = self._CompleteZoneSourceList(self, "CompleteZoneSourceList", service, rules, path)
                self.CompleteLabelTargetList = self._CompleteLabelTargetList(self, "CompleteLabelTargetList", service, rules, path)
                self.CompleteZoneTargetList = self._CompleteZoneTargetList(self, "CompleteZoneTargetList", service, rules, path)
                self.ThinVolumePreferences = self._ThinVolumePreferences(self, "ThinVolumePreferences", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ZoneLocation2 = self._ZoneLocation2(self, "ZoneLocation2", service, rules, path)

            class _ThinMeshingName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the thin volume mesh control, or use the default.
                """

            class _AssignSizeUsing(PyTextualCommandArgumentsSubItem):
                """
                Specify the sizing of the mesh layers to be based on Intervals or based on the Size of the plates.
                """

            class _Intervals(PyNumericalCommandArgumentsSubItem):
                """
                Specifies the number of mesh layers to be created within the thin volume mesh.
                """

            class _Size(PyNumericalCommandArgumentsSubItem):
                """
                enter the Size of each thin mesh layer or use the default.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the Growth Rate which is the expansion rate of the extrusion for each thin volume mesh layer and is set to 1 by default. A growth rate of 1.2 for example will expand each layer of the extrusion by 20 percent of the previous length.
                """

            class _RemeshOverlapping(PyParameterCommandArgumentsSubItem):
                """
                Argument RemeshOverlapping.
                """

            class _DoubleBiasing(PyParameterCommandArgumentsSubItem):
                """
                Enable the Doubling biasing option to invoke double biasing on edges of the thin volume mesh layers. Enabling double biasing will automatically set the Growth Rate to 1.3. When disabled, the thin volume mesh can only be graded from the Source to the Target.
                """

            class _SideImprints(PyParameterCommandArgumentsSubItem):
                """
                Specifies the mesher to project the outer nodes of the thin volume mesh onto adjacent boundary face zones and is enabled by default. This ensures that geometric details of the thin volume are accurately captured at the boundary.
                """

            class _StackedPlates(PyParameterCommandArgumentsSubItem):
                """
                For models consisting of stacked planar plates, you can enable the Stacked Plates option to select all source-target zones that are aligned with the global x-y-z plane.
                """

            class _AutoControlCreation(PyParameterCommandArgumentsSubItem):
                """
                enter the Size of each thin mesh layer or use the default.
                """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Specify the Region(s) where the thin volume meshing controls will be applied.
                """

            class _SelectSourceBy(PyTextualCommandArgumentsSubItem):
                """
                Choose whether to select the source surfaces by label or by zone.
                """

            class _ParallelSource(PyParameterCommandArgumentsSubItem):
                """
                Enable this option if you have multiple source zones in parallel that you want to select for thin meshing.
                """

            class _LabelSourceList(PyTextualCommandArgumentsSubItem):
                """
                Select the label(s) to use as the source.
                """

            class _ZoneSourceList(PyTextualCommandArgumentsSubItem):
                """
                Select the zone(s) to use as the source.
                """

            class _SelectTargetBy(PyTextualCommandArgumentsSubItem):
                """
                Choose whether to select the source surfaces by label or by zone.
                """

            class _ParallelTarget(PyParameterCommandArgumentsSubItem):
                """
                Enable this option if you have multiple target zones in parallel that you want to select for thin meshing,
                """

            class _LabelTargetList(PyTextualCommandArgumentsSubItem):
                """
                Select the label(s) to use as the target.
                """

            class _ZoneTargetList(PyTextualCommandArgumentsSubItem):
                """
                Select the zone(s) to use as the target.
                """

            class _ThinVolRegs(PyTextualCommandArgumentsSubItem):
                """
                Argument ThinVolRegs.
                """

            class _CompleteRegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteRegionScope.
                """

            class _CompleteLabelSourceList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelSourceList.
                """

            class _CompleteZoneSourceList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneSourceList.
                """

            class _CompleteLabelTargetList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelTargetList.
                """

            class _CompleteZoneTargetList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneTargetList.
                """

            class _ThinVolumePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument ThinVolumePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowThinVolumePreferences = self._ShowThinVolumePreferences(self, "ShowThinVolumePreferences", service, rules, path)
                    self.MaxGapSize = self._MaxGapSize(self, "MaxGapSize", service, rules, path)
                    self.IgnoreExtraSources = self._IgnoreExtraSources(self, "IgnoreExtraSources", service, rules, path)
                    self.StackedPlateTolerance = self._StackedPlateTolerance(self, "StackedPlateTolerance", service, rules, path)
                    self.IncludeAdjacent = self._IncludeAdjacent(self, "IncludeAdjacent", service, rules, path)

                class _ShowThinVolumePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowThinVolumePreferences.
                    """

                class _MaxGapSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxGapSize.
                    """

                class _IgnoreExtraSources(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IgnoreExtraSources.
                    """

                class _StackedPlateTolerance(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument StackedPlateTolerance.
                    """

                class _IncludeAdjacent(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IncludeAdjacent.
                    """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _ZoneLocation2(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation2.
                """

        def create_instance(self) -> _AddThinVolumeMeshControlsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddThinVolumeMeshControlsCommandArguments(*args)

    class AddVirtualTopology(PyCommand):
        """
        Command AddVirtualTopology.

        Parameters
        ----------
        AddChild : str
        ControlName : str
        SelectionType : str
        FaceLabelList : list[str]
        FaceZoneList : list[str]
        NewFaces : list[int]

        Returns
        -------
        bool
        """
        class _AddVirtualTopologyCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.ControlName = self._ControlName(self, "ControlName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.FaceLabelList = self._FaceLabelList(self, "FaceLabelList", service, rules, path)
                self.FaceZoneList = self._FaceZoneList(self, "FaceZoneList", service, rules, path)
                self.NewFaces = self._NewFaces(self, "NewFaces", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Argument AddChild.
                """

            class _ControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument ControlName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _FaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceLabelList.
                """

            class _FaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceZoneList.
                """

            class _NewFaces(PyNumericalCommandArgumentsSubItem):
                """
                Argument NewFaces.
                """

        def create_instance(self) -> _AddVirtualTopologyCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddVirtualTopologyCommandArguments(*args)

    class Capping(PyCommand):
        """
        Command Capping.

        Parameters
        ----------
        PatchName : str
            Enter a name for the capping surface.
        ZoneType : str
            Choose the type of zone to assign to the capping surface (velocity inlet, pressure outlet, etc.).
        PatchType : str
            Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
        SelectionType : str
            Choose how you want to select your surface (by label or by zone).
        LabelSelectionList : list[str]
            Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        CreatePatchPreferences : dict[str, Any]
        ObjectAssociation : str
        NewObjectName : str
        PatchObjectName : str
        CapLabels : list[str]
        ZoneLocation : list[str]
        CompleteZoneSelectionList : list[str]
        CompleteLabelSelectionList : list[str]
        CompleteTopologyList : list[str]

        Returns
        -------
        bool
        """
        class _CappingCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.PatchName = self._PatchName(self, "PatchName", service, rules, path)
                self.ZoneType = self._ZoneType(self, "ZoneType", service, rules, path)
                self.PatchType = self._PatchType(self, "PatchType", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.CreatePatchPreferences = self._CreatePatchPreferences(self, "CreatePatchPreferences", service, rules, path)
                self.ObjectAssociation = self._ObjectAssociation(self, "ObjectAssociation", service, rules, path)
                self.NewObjectName = self._NewObjectName(self, "NewObjectName", service, rules, path)
                self.PatchObjectName = self._PatchObjectName(self, "PatchObjectName", service, rules, path)
                self.CapLabels = self._CapLabels(self, "CapLabels", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.CompleteZoneSelectionList = self._CompleteZoneSelectionList(self, "CompleteZoneSelectionList", service, rules, path)
                self.CompleteLabelSelectionList = self._CompleteLabelSelectionList(self, "CompleteLabelSelectionList", service, rules, path)
                self.CompleteTopologyList = self._CompleteTopologyList(self, "CompleteTopologyList", service, rules, path)

            class _PatchName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the capping surface.
                """

            class _ZoneType(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of zone to assign to the capping surface (velocity inlet, pressure outlet, etc.).
                """

            class _PatchType(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to select your surface (by label or by zone).
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _CreatePatchPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument CreatePatchPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxCapLimit = self._MaxCapLimit(self, "MaxCapLimit", service, rules, path)
                    self.ShowCreatePatchPreferences = self._ShowCreatePatchPreferences(self, "ShowCreatePatchPreferences", service, rules, path)
                    self.CAPIntersectionCheck = self._CAPIntersectionCheck(self, "CAPIntersectionCheck", service, rules, path)

                class _MaxCapLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxCapLimit.
                    """

                class _ShowCreatePatchPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowCreatePatchPreferences.
                    """

                class _CAPIntersectionCheck(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CAPIntersectionCheck.
                    """

            class _ObjectAssociation(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectAssociation.
                """

            class _NewObjectName(PyTextualCommandArgumentsSubItem):
                """
                Argument NewObjectName.
                """

            class _PatchObjectName(PyTextualCommandArgumentsSubItem):
                """
                Argument PatchObjectName.
                """

            class _CapLabels(PyTextualCommandArgumentsSubItem):
                """
                Argument CapLabels.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _CompleteZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneSelectionList.
                """

            class _CompleteLabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

            class _CompleteTopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteTopologyList.
                """

        def create_instance(self) -> _CappingCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CappingCommandArguments(*args)

    class CheckMesh(PyCommand):
        """
        Command CheckMesh.


        Returns
        -------
        None
        """
        class _CheckMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CheckMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CheckMeshCommandArguments(*args)

    class CheckSurfaceQuality(PyCommand):
        """
        Command CheckSurfaceQuality.


        Returns
        -------
        None
        """
        class _CheckSurfaceQualityCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CheckSurfaceQualityCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CheckSurfaceQualityCommandArguments(*args)

    class CheckVolumeQuality(PyCommand):
        """
        Command CheckVolumeQuality.


        Returns
        -------
        None
        """
        class _CheckVolumeQualityCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CheckVolumeQualityCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CheckVolumeQualityCommandArguments(*args)

    class ChooseMeshControlOptions(PyCommand):
        """
        Command ChooseMeshControlOptions.

        Parameters
        ----------
        ReadOrCreate : str
            Determine whether you want to create new, or use existing mesh size controls or size fields.
        SizeControlFileName : str
            Browse to specify the location and the name of the size control file (.szcontrol) where your mesh controls are defined.
        WrapSizeControlFileName : str
        CreationMethod : str
            Determine whether you want to use default size controls or not. Default will populate your size controls with default settings, based on the number of objects in your model. The Custom option can be used to populate as many size controls as you need using your own customized settings.
        ViewOption : str
            Determine if you would like to use separate tasks or a table to view and work with your mesh controls.
        GlobalMin : float
        GlobalMax : float
        GlobalGrowthRate : float
        MeshControlOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ChooseMeshControlOptionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ReadOrCreate = self._ReadOrCreate(self, "ReadOrCreate", service, rules, path)
                self.SizeControlFileName = self._SizeControlFileName(self, "SizeControlFileName", service, rules, path)
                self.WrapSizeControlFileName = self._WrapSizeControlFileName(self, "WrapSizeControlFileName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.ViewOption = self._ViewOption(self, "ViewOption", service, rules, path)
                self.GlobalMin = self._GlobalMin(self, "GlobalMin", service, rules, path)
                self.GlobalMax = self._GlobalMax(self, "GlobalMax", service, rules, path)
                self.GlobalGrowthRate = self._GlobalGrowthRate(self, "GlobalGrowthRate", service, rules, path)
                self.MeshControlOptions = self._MeshControlOptions(self, "MeshControlOptions", service, rules, path)

            class _ReadOrCreate(PyTextualCommandArgumentsSubItem):
                """
                Determine whether you want to create new, or use existing mesh size controls or size fields.
                """

            class _SizeControlFileName(PyTextualCommandArgumentsSubItem):
                """
                Browse to specify the location and the name of the size control file (.szcontrol) where your mesh controls are defined.
                """

            class _WrapSizeControlFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument WrapSizeControlFileName.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Determine whether you want to use default size controls or not. Default will populate your size controls with default settings, based on the number of objects in your model. The Custom option can be used to populate as many size controls as you need using your own customized settings.
                """

            class _ViewOption(PyTextualCommandArgumentsSubItem):
                """
                Determine if you would like to use separate tasks or a table to view and work with your mesh controls.
                """

            class _GlobalMin(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalMin.
                """

            class _GlobalMax(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalMax.
                """

            class _GlobalGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalGrowthRate.
                """

            class _MeshControlOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument MeshControlOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.WrapTargetSizeFieldRatio = self._WrapTargetSizeFieldRatio(self, "WrapTargetSizeFieldRatio", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.SolidFluidRaio = self._SolidFluidRaio(self, "SolidFluidRaio", service, rules, path)
                    self.BoundaryLayers = self._BoundaryLayers(self, "BoundaryLayers", service, rules, path)
                    self.EdgeProximityComputation = self._EdgeProximityComputation(self, "EdgeProximityComputation", service, rules, path)
                    self.WrapTargetBothOptions = self._WrapTargetBothOptions(self, "WrapTargetBothOptions", service, rules, path)
                    self.ExistingSizeField = self._ExistingSizeField(self, "ExistingSizeField", service, rules, path)
                    self.WrapSizeFieldFileName = self._WrapSizeFieldFileName(self, "WrapSizeFieldFileName", service, rules, path)
                    self.TargeSizeFieldFileName = self._TargeSizeFieldFileName(self, "TargeSizeFieldFileName", service, rules, path)
                    self.WrapTargetRaio = self._WrapTargetRaio(self, "WrapTargetRaio", service, rules, path)

                class _WrapTargetSizeFieldRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapTargetSizeFieldRatio.
                    """

                class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AdvancedOptions.
                    """

                class _SolidFluidRaio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SolidFluidRaio.
                    """

                class _BoundaryLayers(PyTextualCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayers.
                    """

                class _EdgeProximityComputation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeProximityComputation.
                    """

                class _WrapTargetBothOptions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument WrapTargetBothOptions.
                    """

                class _ExistingSizeField(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExistingSizeField.
                    """

                class _WrapSizeFieldFileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument WrapSizeFieldFileName.
                    """

                class _TargeSizeFieldFileName(PyTextualCommandArgumentsSubItem):
                    """
                    Argument TargeSizeFieldFileName.
                    """

                class _WrapTargetRaio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapTargetRaio.
                    """

        def create_instance(self) -> _ChooseMeshControlOptionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChooseMeshControlOptionsCommandArguments(*args)

    class ChoosePartReplacementOptions(PyCommand):
        """
        Command ChoosePartReplacementOptions.

        Parameters
        ----------
        AddPartManagement : str
            Determine whether or not you will be appending new CAD parts to your original geometry. Answering Yes will add an Import CAD and Part Management task.
        AddPartReplacement : str
        AddLocalSizing : str
            Determine whether or not you will need to apply local sizing controls. Answering Yes will add an Add Local Sizing for Part Replacement task.
        AddBoundaryLayer : str
            Determine whether or not you will need to apply boundary layer (prism controls) to your replacement parts. Answering Yes will add an Add Boundary Layers for Part Replacement task.
        AddUpdateTheVolumeMesh : str

        Returns
        -------
        bool
        """
        class _ChoosePartReplacementOptionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddPartManagement = self._AddPartManagement(self, "AddPartManagement", service, rules, path)
                self.AddPartReplacement = self._AddPartReplacement(self, "AddPartReplacement", service, rules, path)
                self.AddLocalSizing = self._AddLocalSizing(self, "AddLocalSizing", service, rules, path)
                self.AddBoundaryLayer = self._AddBoundaryLayer(self, "AddBoundaryLayer", service, rules, path)
                self.AddUpdateTheVolumeMesh = self._AddUpdateTheVolumeMesh(self, "AddUpdateTheVolumeMesh", service, rules, path)

            class _AddPartManagement(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you will be appending new CAD parts to your original geometry. Answering Yes will add an Import CAD and Part Management task.
                """

            class _AddPartReplacement(PyTextualCommandArgumentsSubItem):
                """
                Argument AddPartReplacement.
                """

            class _AddLocalSizing(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you will need to apply local sizing controls. Answering Yes will add an Add Local Sizing for Part Replacement task.
                """

            class _AddBoundaryLayer(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you will need to apply boundary layer (prism controls) to your replacement parts. Answering Yes will add an Add Boundary Layers for Part Replacement task.
                """

            class _AddUpdateTheVolumeMesh(PyTextualCommandArgumentsSubItem):
                """
                Argument AddUpdateTheVolumeMesh.
                """

        def create_instance(self) -> _ChoosePartReplacementOptionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChoosePartReplacementOptionsCommandArguments(*args)

    class CloseLeakage(PyCommand):
        """
        Command CloseLeakage.

        Parameters
        ----------
        CloseLeakageOption : bool

        Returns
        -------
        bool
        """
        class _CloseLeakageCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.CloseLeakageOption = self._CloseLeakageOption(self, "CloseLeakageOption", service, rules, path)

            class _CloseLeakageOption(PyParameterCommandArgumentsSubItem):
                """
                Argument CloseLeakageOption.
                """

        def create_instance(self) -> _CloseLeakageCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CloseLeakageCommandArguments(*args)

    class ComplexMeshingRegions(PyCommand):
        """
        Command ComplexMeshingRegions.

        Parameters
        ----------
        ComplexMeshingRegionsOption : bool

        Returns
        -------
        bool
        """
        class _ComplexMeshingRegionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ComplexMeshingRegionsOption = self._ComplexMeshingRegionsOption(self, "ComplexMeshingRegionsOption", service, rules, path)

            class _ComplexMeshingRegionsOption(PyParameterCommandArgumentsSubItem):
                """
                Argument ComplexMeshingRegionsOption.
                """

        def create_instance(self) -> _ComplexMeshingRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ComplexMeshingRegionsCommandArguments(*args)

    class ComputeSizeField(PyCommand):
        """
        Command ComputeSizeField.

        Parameters
        ----------
        ComputeSizeFieldControl : str

        Returns
        -------
        bool
        """
        class _ComputeSizeFieldCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ComputeSizeFieldControl = self._ComputeSizeFieldControl(self, "ComputeSizeFieldControl", service, rules, path)

            class _ComputeSizeFieldControl(PyTextualCommandArgumentsSubItem):
                """
                Argument ComputeSizeFieldControl.
                """

        def create_instance(self) -> _ComputeSizeFieldCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ComputeSizeFieldCommandArguments(*args)

    class CreateBackgroundMesh(PyCommand):
        """
        Command CreateBackgroundMesh.

        Parameters
        ----------
        RefinementRegionsName : str
        CreationMethod : str
        BOIMaxSize : float
        BOISizeName : str
        SelectionType : str
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
        ObjectSelectionList : list[str]
        ZoneSelectionSingle : list[str]
        ObjectSelectionSingle : list[str]
        TopologyList : list[str]
        BoundingBoxObject : dict[str, Any]
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
        CylinderMethod : str
        CylinderLength : float

        Returns
        -------
        bool
        """
        class _CreateBackgroundMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RefinementRegionsName = self._RefinementRegionsName(self, "RefinementRegionsName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.BOIMaxSize = self._BOIMaxSize(self, "BOIMaxSize", service, rules, path)
                self.BOISizeName = self._BOISizeName(self, "BOISizeName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionSingle = self._ZoneSelectionSingle(self, "ZoneSelectionSingle", service, rules, path)
                self.ObjectSelectionSingle = self._ObjectSelectionSingle(self, "ObjectSelectionSingle", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)

            class _RefinementRegionsName(PyTextualCommandArgumentsSubItem):
                """
                Argument RefinementRegionsName.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CreationMethod.
                """

            class _BOIMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOIMaxSize.
                """

            class _BOISizeName(PyTextualCommandArgumentsSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionSingle.
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionSingle.
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PySingletonCommandArgumentsSubItem):
                """
                Argument BoundingBoxObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SizeRelativeLength = self._SizeRelativeLength(self, "SizeRelativeLength", service, rules, path)
                    self.XmaxRatio = self._XmaxRatio(self, "XmaxRatio", service, rules, path)
                    self.XminRatio = self._XminRatio(self, "XminRatio", service, rules, path)
                    self.YminRatio = self._YminRatio(self, "YminRatio", service, rules, path)
                    self.Zmin = self._Zmin(self, "Zmin", service, rules, path)
                    self.Zmax = self._Zmax(self, "Zmax", service, rules, path)
                    self.Ymax = self._Ymax(self, "Ymax", service, rules, path)
                    self.ZminRatio = self._ZminRatio(self, "ZminRatio", service, rules, path)
                    self.Ymin = self._Ymin(self, "Ymin", service, rules, path)
                    self.Xmin = self._Xmin(self, "Xmin", service, rules, path)
                    self.YmaxRatio = self._YmaxRatio(self, "YmaxRatio", service, rules, path)
                    self.ZmaxRatio = self._ZmaxRatio(self, "ZmaxRatio", service, rules, path)
                    self.Xmax = self._Xmax(self, "Xmax", service, rules, path)

                class _SizeRelativeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _XmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XmaxRatio.
                    """

                class _XminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _Xmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmax.
                    """

            class _OffsetObject(PySingletonCommandArgumentsSubItem):
                """
                Argument OffsetObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.WakeLevels = self._WakeLevels(self, "WakeLevels", service, rules, path)
                    self.ShowCoordinates = self._ShowCoordinates(self, "ShowCoordinates", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)
                    self.DefeaturingSize = self._DefeaturingSize(self, "DefeaturingSize", service, rules, path)
                    self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z.
                    """

                class _WakeLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y.
                    """

                class _DefeaturingSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _AspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _Rate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Rate.
                    """

                class _WakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _FlowDirection(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _BoundaryLayerLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FlipDirection(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerHeight.
                    """

                class _CrossWakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderObject(PySingletonCommandArgumentsSubItem):
                """
                Argument CylinderObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.HeightNode = self._HeightNode(self, "HeightNode", service, rules, path)
                    self.X_Offset = self._X_Offset(self, "X-Offset", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.X1 = self._X1(self, "X1", service, rules, path)
                    self.Y1 = self._Y1(self, "Y1", service, rules, path)
                    self.Z_Offset = self._Z_Offset(self, "Z-Offset", service, rules, path)
                    self.Z2 = self._Z2(self, "Z2", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Z1 = self._Z1(self, "Z1", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Y2 = self._Y2(self, "Y2", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _X_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
                    """

                class _Y_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _Node2(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node2.
                    """

                class _X2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X2.
                    """

                class _HeightFrontInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PySingletonCommandArgumentsSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Argument VolumeFill.
                """

            class _CylinderMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CylinderMethod.
                """

            class _CylinderLength(PyNumericalCommandArgumentsSubItem):
                """
                Argument CylinderLength.
                """

        def create_instance(self) -> _CreateBackgroundMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateBackgroundMeshCommandArguments(*args)

    class CreateCollarMesh(PyCommand):
        """
        Command CreateCollarMesh.

        Parameters
        ----------
        RefinementRegionsName : str
            Specify a name for the collar mesh or use the default name.
        CreationMethod : str
            Choose how you want to create the collar mesh: either by using intersecting objects, an edge-based collar, or an existing object.
        BOIMaxSize : float
            Specify the maximum size of the elements for the collar mesh.
        BOISizeName : str
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ZoneSelectionList : list[str]
            Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Select one or more labels that will make up the collar mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionSingle : list[str]
            Choose a single zone from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionSingle : list[str]
            Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        BoundingBoxObject : dict[str, Any]
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
            Specify the type of mesh cell to use to fill the collar mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
        CylinderMethod : str
        CylinderLength : float

        Returns
        -------
        bool
        """
        class _CreateCollarMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RefinementRegionsName = self._RefinementRegionsName(self, "RefinementRegionsName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.BOIMaxSize = self._BOIMaxSize(self, "BOIMaxSize", service, rules, path)
                self.BOISizeName = self._BOISizeName(self, "BOISizeName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionSingle = self._ZoneSelectionSingle(self, "ZoneSelectionSingle", service, rules, path)
                self.ObjectSelectionSingle = self._ObjectSelectionSingle(self, "ObjectSelectionSingle", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)

            class _RefinementRegionsName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the collar mesh or use the default name.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to create the collar mesh: either by using intersecting objects, an edge-based collar, or an existing object.
                """

            class _BOIMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum size of the elements for the collar mesh.
                """

            class _BOISizeName(PyTextualCommandArgumentsSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more labels that will make up the collar mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PySingletonCommandArgumentsSubItem):
                """
                Argument BoundingBoxObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SizeRelativeLength = self._SizeRelativeLength(self, "SizeRelativeLength", service, rules, path)
                    self.Xmax = self._Xmax(self, "Xmax", service, rules, path)
                    self.XminRatio = self._XminRatio(self, "XminRatio", service, rules, path)
                    self.YminRatio = self._YminRatio(self, "YminRatio", service, rules, path)
                    self.Zmin = self._Zmin(self, "Zmin", service, rules, path)
                    self.Zmax = self._Zmax(self, "Zmax", service, rules, path)
                    self.Ymax = self._Ymax(self, "Ymax", service, rules, path)
                    self.ZminRatio = self._ZminRatio(self, "ZminRatio", service, rules, path)
                    self.Ymin = self._Ymin(self, "Ymin", service, rules, path)
                    self.Xmin = self._Xmin(self, "Xmin", service, rules, path)
                    self.YmaxRatio = self._YmaxRatio(self, "YmaxRatio", service, rules, path)
                    self.ZmaxRatio = self._ZmaxRatio(self, "ZmaxRatio", service, rules, path)
                    self.XmaxRatio = self._XmaxRatio(self, "XmaxRatio", service, rules, path)

                class _SizeRelativeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _Xmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmax.
                    """

                class _XminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _XmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XmaxRatio.
                    """

            class _OffsetObject(PySingletonCommandArgumentsSubItem):
                """
                Argument OffsetObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.WakeLevels = self._WakeLevels(self, "WakeLevels", service, rules, path)
                    self.ShowCoordinates = self._ShowCoordinates(self, "ShowCoordinates", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)
                    self.DefeaturingSize = self._DefeaturingSize(self, "DefeaturingSize", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z.
                    """

                class _WakeLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y.
                    """

                class _DefeaturingSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _BoundaryLayerLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _WakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _Rate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Rate.
                    """

                class _FlowDirection(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _AspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FlipDirection(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerHeight.
                    """

                class _CrossWakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderObject(PySingletonCommandArgumentsSubItem):
                """
                Argument CylinderObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X_Offset = self._X_Offset(self, "X-Offset", service, rules, path)
                    self.HeightNode = self._HeightNode(self, "HeightNode", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.X1 = self._X1(self, "X1", service, rules, path)
                    self.Y1 = self._Y1(self, "Y1", service, rules, path)
                    self.Z_Offset = self._Z_Offset(self, "Z-Offset", service, rules, path)
                    self.Z2 = self._Z2(self, "Z2", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Z1 = self._Z1(self, "Z1", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Y2 = self._Y2(self, "Y2", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _X_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
                    """

                class _X2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X2.
                    """

                class _Y_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _Node2(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node2.
                    """

                class _HeightFrontInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PySingletonCommandArgumentsSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Specify the type of mesh cell to use to fill the collar mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
                """

            class _CylinderMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CylinderMethod.
                """

            class _CylinderLength(PyNumericalCommandArgumentsSubItem):
                """
                Argument CylinderLength.
                """

        def create_instance(self) -> _CreateCollarMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateCollarMeshCommandArguments(*args)

    class CreateComponentMesh(PyCommand):
        """
        Command CreateComponentMesh.

        Parameters
        ----------
        RefinementRegionsName : str
            Specify a name for the component mesh or use the default value.
        CreationMethod : str
            Choose how you want to create the component mesh: either by using an offset surface, creating a bounding box, using an existing portion of the geometry, or by growing a boundary layer.
        BOIMaxSize : float
            Specify the maximum size of the elements for the component mesh.
        BOISizeName : str
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ZoneSelectionList : list[str]
            Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Select one or more labels that will make up the component mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionSingle : list[str]
            Choose a single zone from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionSingle : list[str]
            Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        BoundingBoxObject : dict[str, Any]
            View the extents of the bounding box.
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
            Specify the type of mesh cell to use to fill the component mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
        CylinderMethod : str
        CylinderLength : float

        Returns
        -------
        bool
        """
        class _CreateComponentMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RefinementRegionsName = self._RefinementRegionsName(self, "RefinementRegionsName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.BOIMaxSize = self._BOIMaxSize(self, "BOIMaxSize", service, rules, path)
                self.BOISizeName = self._BOISizeName(self, "BOISizeName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionSingle = self._ZoneSelectionSingle(self, "ZoneSelectionSingle", service, rules, path)
                self.ObjectSelectionSingle = self._ObjectSelectionSingle(self, "ObjectSelectionSingle", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)

            class _RefinementRegionsName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the component mesh or use the default value.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to create the component mesh: either by using an offset surface, creating a bounding box, using an existing portion of the geometry, or by growing a boundary layer.
                """

            class _BOIMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum size of the elements for the component mesh.
                """

            class _BOISizeName(PyTextualCommandArgumentsSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more labels that will make up the component mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PySingletonCommandArgumentsSubItem):
                """
                View the extents of the bounding box.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SizeRelativeLength = self._SizeRelativeLength(self, "SizeRelativeLength", service, rules, path)
                    self.XmaxRatio = self._XmaxRatio(self, "XmaxRatio", service, rules, path)
                    self.XminRatio = self._XminRatio(self, "XminRatio", service, rules, path)
                    self.YminRatio = self._YminRatio(self, "YminRatio", service, rules, path)
                    self.Zmin = self._Zmin(self, "Zmin", service, rules, path)
                    self.Zmax = self._Zmax(self, "Zmax", service, rules, path)
                    self.Ymax = self._Ymax(self, "Ymax", service, rules, path)
                    self.ZminRatio = self._ZminRatio(self, "ZminRatio", service, rules, path)
                    self.Ymin = self._Ymin(self, "Ymin", service, rules, path)
                    self.Xmin = self._Xmin(self, "Xmin", service, rules, path)
                    self.YmaxRatio = self._YmaxRatio(self, "YmaxRatio", service, rules, path)
                    self.ZmaxRatio = self._ZmaxRatio(self, "ZmaxRatio", service, rules, path)
                    self.Xmax = self._Xmax(self, "Xmax", service, rules, path)

                class _SizeRelativeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _XmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XmaxRatio.
                    """

                class _XminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _Xmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmax.
                    """

            class _OffsetObject(PySingletonCommandArgumentsSubItem):
                """
                Argument OffsetObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.WakeLevels = self._WakeLevels(self, "WakeLevels", service, rules, path)
                    self.ShowCoordinates = self._ShowCoordinates(self, "ShowCoordinates", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)
                    self.DefeaturingSize = self._DefeaturingSize(self, "DefeaturingSize", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z.
                    """

                class _WakeLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y.
                    """

                class _DefeaturingSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _BoundaryLayerLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _AspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _Rate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Rate.
                    """

                class _FlowDirection(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _WakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FlipDirection(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerHeight.
                    """

                class _CrossWakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderObject(PySingletonCommandArgumentsSubItem):
                """
                Argument CylinderObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X_Offset = self._X_Offset(self, "X-Offset", service, rules, path)
                    self.HeightNode = self._HeightNode(self, "HeightNode", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.X1 = self._X1(self, "X1", service, rules, path)
                    self.Y1 = self._Y1(self, "Y1", service, rules, path)
                    self.Z_Offset = self._Z_Offset(self, "Z-Offset", service, rules, path)
                    self.Z1 = self._Z1(self, "Z1", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Z2 = self._Z2(self, "Z2", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Y2 = self._Y2(self, "Y2", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _X_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z1.
                    """

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

                class _Z2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z2.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
                    """

                class _Node2(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node2.
                    """

                class _X2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X2.
                    """

                class _Y_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _HeightFrontInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PySingletonCommandArgumentsSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Specify the type of mesh cell to use to fill the component mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
                """

            class _CylinderMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CylinderMethod.
                """

            class _CylinderLength(PyNumericalCommandArgumentsSubItem):
                """
                Argument CylinderLength.
                """

        def create_instance(self) -> _CreateComponentMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateComponentMeshCommandArguments(*args)

    class CreateContactPatch(PyCommand):
        """
        Command CreateContactPatch.

        Parameters
        ----------
        ContactPatchName : str
            Specify a name for the contact patch object, or retain the default name.
        SelectionType : str
            Choose how you want to make your selection (for instance, by object, zone, or label).
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        ObjectSelectionList : list[str]
            Choose an object from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LabelSelectionList : list[str]
            Select one or more labels that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        GroundZoneSelectionList : list[str]
            Choose one or more face zones from the list below that represent the contact target (for instance, the ground face zone in an enclosing bounding box for a tire-ground contact scenario).
        Distance : float
            Specify the distance of the contact patch geometry from the ground zone, or the thickness of the contact patch.
        ContactPatchDefeaturingSize : float
            Allows you to control the smoothness of the contact patch. With the default value of 0, no smoothing takes place. With a value greater than 0, the patch is defeatured to create a smooth patch. This will lead to better quality volume mesh at the contact, for instance, between the tire and the ground.
        FeatureAngle : float
            Specify a value for the angle used to extract feature edges on the contact patch object.
        PatchHole : bool
            Indicate whether you want the contact patch object to be filled or not.
        FlipDirection : bool
            Use this option to switch the direction/orientation of the contact patch.

        Returns
        -------
        bool
        """
        class _CreateContactPatchCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ContactPatchName = self._ContactPatchName(self, "ContactPatchName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.GroundZoneSelectionList = self._GroundZoneSelectionList(self, "GroundZoneSelectionList", service, rules, path)
                self.Distance = self._Distance(self, "Distance", service, rules, path)
                self.ContactPatchDefeaturingSize = self._ContactPatchDefeaturingSize(self, "ContactPatchDefeaturingSize", service, rules, path)
                self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                self.PatchHole = self._PatchHole(self, "PatchHole", service, rules, path)
                self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)

            class _ContactPatchName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the contact patch object, or retain the default name.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (for instance, by object, zone, or label).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose an object from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more labels that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GroundZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below that represent the contact target (for instance, the ground face zone in an enclosing bounding box for a tire-ground contact scenario).
                """

            class _Distance(PyNumericalCommandArgumentsSubItem):
                """
                Specify the distance of the contact patch geometry from the ground zone, or the thickness of the contact patch.
                """

            class _ContactPatchDefeaturingSize(PyNumericalCommandArgumentsSubItem):
                """
                Allows you to control the smoothness of the contact patch. With the default value of 0, no smoothing takes place. With a value greater than 0, the patch is defeatured to create a smooth patch. This will lead to better quality volume mesh at the contact, for instance, between the tire and the ground.
                """

            class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the angle used to extract feature edges on the contact patch object.
                """

            class _PatchHole(PyParameterCommandArgumentsSubItem):
                """
                Indicate whether you want the contact patch object to be filled or not.
                """

            class _FlipDirection(PyParameterCommandArgumentsSubItem):
                """
                Use this option to switch the direction/orientation of the contact patch.
                """

        def create_instance(self) -> _CreateContactPatchCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateContactPatchCommandArguments(*args)

    class CreateExternalFlowBoundaries(PyCommand):
        """
        Command CreateExternalFlowBoundaries.

        Parameters
        ----------
        ExternalBoundariesName : str
            Enter a name for the external flow boundary or use the default value.
        CreationMethod : str
            Choose how you want to create the external flow boundary: either by creating a new boundary using a bounding box, or use an existing portion of the geometry.
        ExtractionMethod : str
            Choose whether you would like to extract the external flow region either as a surface mesh object (a direct surface remesh of the object) a wrap, or an existing mesh (for overset components). The object setting is applied later when generating the surface mesh.
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionSingle : list[str]
            Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionSingle : list[str]
            Choose a single zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LabelSelectionSingle : list[str]
            Choose a single label from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        OriginalObjectName : str
        BoundingBoxObject : dict[str, Any]
            View the extents of the bounding box.

        Returns
        -------
        bool
        """
        class _CreateExternalFlowBoundariesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ExternalBoundariesName = self._ExternalBoundariesName(self, "ExternalBoundariesName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.ExtractionMethod = self._ExtractionMethod(self, "ExtractionMethod", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionSingle = self._ObjectSelectionSingle(self, "ObjectSelectionSingle", service, rules, path)
                self.ZoneSelectionSingle = self._ZoneSelectionSingle(self, "ZoneSelectionSingle", service, rules, path)
                self.LabelSelectionSingle = self._LabelSelectionSingle(self, "LabelSelectionSingle", service, rules, path)
                self.OriginalObjectName = self._OriginalObjectName(self, "OriginalObjectName", service, rules, path)
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)

            class _ExternalBoundariesName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the external flow boundary or use the default value.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to create the external flow boundary: either by creating a new boundary using a bounding box, or use an existing portion of the geometry.
                """

            class _ExtractionMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose whether you would like to extract the external flow region either as a surface mesh object (a direct surface remesh of the object) a wrap, or an existing mesh (for overset components). The object setting is applied later when generating the surface mesh.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single label from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _OriginalObjectName(PyTextualCommandArgumentsSubItem):
                """
                Argument OriginalObjectName.
                """

            class _BoundingBoxObject(PySingletonCommandArgumentsSubItem):
                """
                View the extents of the bounding box.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SizeRelativeLength = self._SizeRelativeLength(self, "SizeRelativeLength", service, rules, path)
                    self.XmaxRatio = self._XmaxRatio(self, "XmaxRatio", service, rules, path)
                    self.XminRatio = self._XminRatio(self, "XminRatio", service, rules, path)
                    self.YminRatio = self._YminRatio(self, "YminRatio", service, rules, path)
                    self.Zmin = self._Zmin(self, "Zmin", service, rules, path)
                    self.Zmax = self._Zmax(self, "Zmax", service, rules, path)
                    self.Ymax = self._Ymax(self, "Ymax", service, rules, path)
                    self.ZminRatio = self._ZminRatio(self, "ZminRatio", service, rules, path)
                    self.Ymin = self._Ymin(self, "Ymin", service, rules, path)
                    self.Xmin = self._Xmin(self, "Xmin", service, rules, path)
                    self.YmaxRatio = self._YmaxRatio(self, "YmaxRatio", service, rules, path)
                    self.ZmaxRatio = self._ZmaxRatio(self, "ZmaxRatio", service, rules, path)
                    self.Xmax = self._Xmax(self, "Xmax", service, rules, path)

                class _SizeRelativeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _XmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XmaxRatio.
                    """

                class _XminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _Xmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmax.
                    """

        def create_instance(self) -> _CreateExternalFlowBoundariesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateExternalFlowBoundariesCommandArguments(*args)

    class CreateGapCover(PyCommand):
        """
        Command CreateGapCover.

        Parameters
        ----------
        GapCoverName : str
            Specify a name for the gap cover object, or retain the default name.
        SizingMethod : str
            Determine the method for specifying the gap cover sizing controls. The Wrapper Based on Size Field option uses the size field control settings defined in the Choose Mesh Controls task. Using the Uniform Wrapper option requires you to provide a value for the Max Gap Size. If this task is located at a point in the workflow prior to the Choose Mesh Control Options task, then only the Uniform Wrapper option is available.
        GapSizeRatio : float
            Specify a value for the gap size factor that, when multiplied by the local initial size field, corresponds to the size of the gap that needs to be covered.
        GapSize : float
            A specified maximum width for the gap.
        SelectionType : str
            Choose how you want to make your selection (for instance, by object name, zone name, or label name).
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Select one or more labels that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionList : list[str]
            Choose an object from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        GapCoverBetweenZones : str
            Determine if you only want to cover gaps between boundary zones (Yes), or if you want to cover all gaps within and between boundary zones (No)
        GapCoverRefineFactor : float
            Allows you to control the resolution of the gap cover size based on a scaling of the Max Gap Size (or Max Gap Size Factor). It ranges from 0.0625 to 1 with a default value of 1.0). The higher the Resolution Factor, the more likely that some gaps may not be fully covered. Depending on the gap in question, lowering the Resolution Factor reduces the wrapper to sufficiently cover the gap in most cases.
        GapCoverRefineFactorAtGap : float
            Allows you to specify the level of refinement for the gap-cover (patch). Decreasing the value increases the refinement of the patch.
        RefineWrapperBeforeProjection : str
        AdvancedOptions : bool
            Display advanced options that you may want to apply to the task.
        MaxIslandFaceForGapCover : int
            Specify the maximum face count required for isolated areas (islands) to be created during surface mesh generation. Any islands that have a face count smaller than this value will be removed, and only larger islands will remain.
        GapCoverFeatureImprint : str
            Use this option to better define gap coverings. When this option is set to Yes, the gap covers are more accurate. Once the coarse wrap closes any gaps, this option also snaps the nodes of the wrapper onto all previously defined edge features to more closely cover the gaps. Setting this option to Yes, however, can be computationally expensive when modeling large vehicles (such as in aerospace), thus, the default is No.  Here, when set to No, wrapper faces at the corners are not on the geometry and are incorrectly marked as a gap. When set to Yes, only wrap faces at the gap are marked.

        Returns
        -------
        bool
        """
        class _CreateGapCoverCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GapCoverName = self._GapCoverName(self, "GapCoverName", service, rules, path)
                self.SizingMethod = self._SizingMethod(self, "SizingMethod", service, rules, path)
                self.GapSizeRatio = self._GapSizeRatio(self, "GapSizeRatio", service, rules, path)
                self.GapSize = self._GapSize(self, "GapSize", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.GapCoverBetweenZones = self._GapCoverBetweenZones(self, "GapCoverBetweenZones", service, rules, path)
                self.GapCoverRefineFactor = self._GapCoverRefineFactor(self, "GapCoverRefineFactor", service, rules, path)
                self.GapCoverRefineFactorAtGap = self._GapCoverRefineFactorAtGap(self, "GapCoverRefineFactorAtGap", service, rules, path)
                self.RefineWrapperBeforeProjection = self._RefineWrapperBeforeProjection(self, "RefineWrapperBeforeProjection", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.MaxIslandFaceForGapCover = self._MaxIslandFaceForGapCover(self, "MaxIslandFaceForGapCover", service, rules, path)
                self.GapCoverFeatureImprint = self._GapCoverFeatureImprint(self, "GapCoverFeatureImprint", service, rules, path)

            class _GapCoverName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the gap cover object, or retain the default name.
                """

            class _SizingMethod(PyTextualCommandArgumentsSubItem):
                """
                Determine the method for specifying the gap cover sizing controls. The Wrapper Based on Size Field option uses the size field control settings defined in the Choose Mesh Controls task. Using the Uniform Wrapper option requires you to provide a value for the Max Gap Size. If this task is located at a point in the workflow prior to the Choose Mesh Control Options task, then only the Uniform Wrapper option is available.
                """

            class _GapSizeRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the gap size factor that, when multiplied by the local initial size field, corresponds to the size of the gap that needs to be covered.
                """

            class _GapSize(PyNumericalCommandArgumentsSubItem):
                """
                A specified maximum width for the gap.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (for instance, by object name, zone name, or label name).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more labels that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose an object from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GapCoverBetweenZones(PyTextualCommandArgumentsSubItem):
                """
                Determine if you only want to cover gaps between boundary zones (Yes), or if you want to cover all gaps within and between boundary zones (No)
                """

            class _GapCoverRefineFactor(PyNumericalCommandArgumentsSubItem):
                """
                Allows you to control the resolution of the gap cover size based on a scaling of the Max Gap Size (or Max Gap Size Factor). It ranges from 0.0625 to 1 with a default value of 1.0). The higher the Resolution Factor, the more likely that some gaps may not be fully covered. Depending on the gap in question, lowering the Resolution Factor reduces the wrapper to sufficiently cover the gap in most cases.
                """

            class _GapCoverRefineFactorAtGap(PyNumericalCommandArgumentsSubItem):
                """
                Allows you to specify the level of refinement for the gap-cover (patch). Decreasing the value increases the refinement of the patch.
                """

            class _RefineWrapperBeforeProjection(PyTextualCommandArgumentsSubItem):
                """
                Argument RefineWrapperBeforeProjection.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _MaxIslandFaceForGapCover(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum face count required for isolated areas (islands) to be created during surface mesh generation. Any islands that have a face count smaller than this value will be removed, and only larger islands will remain.
                """

            class _GapCoverFeatureImprint(PyTextualCommandArgumentsSubItem):
                """
                Use this option to better define gap coverings. When this option is set to Yes, the gap covers are more accurate. Once the coarse wrap closes any gaps, this option also snaps the nodes of the wrapper onto all previously defined edge features to more closely cover the gaps. Setting this option to Yes, however, can be computationally expensive when modeling large vehicles (such as in aerospace), thus, the default is No.  Here, when set to No, wrapper faces at the corners are not on the geometry and are incorrectly marked as a gap. When set to Yes, only wrap faces at the gap are marked.
                """

        def create_instance(self) -> _CreateGapCoverCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateGapCoverCommandArguments(*args)

    class CreateLocalRefinementRegions(PyCommand):
        """
        Command CreateLocalRefinementRegions.

        Parameters
        ----------
        RefinementRegionsName : str
            Enter a name for the body of influence.
        CreationMethod : str
            Choose how you want to create the refinement region: by creating a bounding box, a cylindrical bounding region, or using an offset surface. You should select a closed body for the offset surface.
        BOIMaxSize : float
            Specify the cell size for the refinement region mesh.
        BOISizeName : str
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ZoneSelectionList : list[str]
            Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionSingle : list[str]
        ObjectSelectionSingle : list[str]
            Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        BoundingBoxObject : dict[str, Any]
            View the extents of the bounding box.
        OffsetObject : dict[str, Any]
            These fields contain parameters that define the characteristics of the refinements region (direction, thickness, levels, etc.)
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
        CylinderMethod : str
            Choose how the cylindrical refinement region will be defined. The Vector and Length option allows you to define the cylindrical refinement region based either on the location of selected object(s) or zone(s), or by coordinates. If you choose to select by object(s) or zone(s), the location of the cylindrical refinement region will be at the center point of the selected surface. The Two Positions option allows you to explicitly define the location and dimension of the cylindrical refinement region without having to select object(s) or zone(s).
        CylinderLength : float
            Specify the Length of the cylinder.

        Returns
        -------
        bool
        """
        class _CreateLocalRefinementRegionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RefinementRegionsName = self._RefinementRegionsName(self, "RefinementRegionsName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.BOIMaxSize = self._BOIMaxSize(self, "BOIMaxSize", service, rules, path)
                self.BOISizeName = self._BOISizeName(self, "BOISizeName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionSingle = self._ZoneSelectionSingle(self, "ZoneSelectionSingle", service, rules, path)
                self.ObjectSelectionSingle = self._ObjectSelectionSingle(self, "ObjectSelectionSingle", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)

            class _RefinementRegionsName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the body of influence.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to create the refinement region: by creating a bounding box, a cylindrical bounding region, or using an offset surface. You should select a closed body for the offset surface.
                """

            class _BOIMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify the cell size for the refinement region mesh.
                """

            class _BOISizeName(PyTextualCommandArgumentsSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionSingle.
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PySingletonCommandArgumentsSubItem):
                """
                View the extents of the bounding box.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SizeRelativeLength = self._SizeRelativeLength(self, "SizeRelativeLength", service, rules, path)
                    self.Xmax = self._Xmax(self, "Xmax", service, rules, path)
                    self.XminRatio = self._XminRatio(self, "XminRatio", service, rules, path)
                    self.YminRatio = self._YminRatio(self, "YminRatio", service, rules, path)
                    self.Zmin = self._Zmin(self, "Zmin", service, rules, path)
                    self.Zmax = self._Zmax(self, "Zmax", service, rules, path)
                    self.Ymax = self._Ymax(self, "Ymax", service, rules, path)
                    self.ZminRatio = self._ZminRatio(self, "ZminRatio", service, rules, path)
                    self.Ymin = self._Ymin(self, "Ymin", service, rules, path)
                    self.Xmin = self._Xmin(self, "Xmin", service, rules, path)
                    self.YmaxRatio = self._YmaxRatio(self, "YmaxRatio", service, rules, path)
                    self.ZmaxRatio = self._ZmaxRatio(self, "ZmaxRatio", service, rules, path)
                    self.XmaxRatio = self._XmaxRatio(self, "XmaxRatio", service, rules, path)

                class _SizeRelativeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _Xmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmax.
                    """

                class _XminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _XmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XmaxRatio.
                    """

            class _OffsetObject(PySingletonCommandArgumentsSubItem):
                """
                These fields contain parameters that define the characteristics of the refinements region (direction, thickness, levels, etc.)
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.WakeLevels = self._WakeLevels(self, "WakeLevels", service, rules, path)
                    self.ShowCoordinates = self._ShowCoordinates(self, "ShowCoordinates", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)
                    self.DefeaturingSize = self._DefeaturingSize(self, "DefeaturingSize", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z.
                    """

                class _WakeLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y.
                    """

                class _DefeaturingSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _BoundaryLayerLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _WakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _Rate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Rate.
                    """

                class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _FlowDirection(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _AspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _FlipDirection(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerHeight.
                    """

                class _CrossWakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderObject(PySingletonCommandArgumentsSubItem):
                """
                Argument CylinderObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.HeightNode = self._HeightNode(self, "HeightNode", service, rules, path)
                    self.X_Offset = self._X_Offset(self, "X-Offset", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.X1 = self._X1(self, "X1", service, rules, path)
                    self.Y1 = self._Y1(self, "Y1", service, rules, path)
                    self.Z_Offset = self._Z_Offset(self, "Z-Offset", service, rules, path)
                    self.Z2 = self._Z2(self, "Z2", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Z1 = self._Z1(self, "Z1", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Y2 = self._Y2(self, "Y2", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _X_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
                    """

                class _X2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X2.
                    """

                class _Node2(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node2.
                    """

                class _Y_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _HeightFrontInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PySingletonCommandArgumentsSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Argument VolumeFill.
                """

            class _CylinderMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose how the cylindrical refinement region will be defined. The Vector and Length option allows you to define the cylindrical refinement region based either on the location of selected object(s) or zone(s), or by coordinates. If you choose to select by object(s) or zone(s), the location of the cylindrical refinement region will be at the center point of the selected surface. The Two Positions option allows you to explicitly define the location and dimension of the cylindrical refinement region without having to select object(s) or zone(s).
                """

            class _CylinderLength(PyNumericalCommandArgumentsSubItem):
                """
                Specify the Length of the cylinder.
                """

        def create_instance(self) -> _CreateLocalRefinementRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateLocalRefinementRegionsCommandArguments(*args)

    class CreateMeshObjects(PyCommand):
        """
        Command CreateMeshObjects.

        Parameters
        ----------
        MergeZonesBasedOnLabels : bool
        CreateAFaceZonePerBody : bool

        Returns
        -------
        bool
        """
        class _CreateMeshObjectsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MergeZonesBasedOnLabels = self._MergeZonesBasedOnLabels(self, "MergeZonesBasedOnLabels", service, rules, path)
                self.CreateAFaceZonePerBody = self._CreateAFaceZonePerBody(self, "CreateAFaceZonePerBody", service, rules, path)

            class _MergeZonesBasedOnLabels(PyParameterCommandArgumentsSubItem):
                """
                Argument MergeZonesBasedOnLabels.
                """

            class _CreateAFaceZonePerBody(PyParameterCommandArgumentsSubItem):
                """
                Argument CreateAFaceZonePerBody.
                """

        def create_instance(self) -> _CreateMeshObjectsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateMeshObjectsCommandArguments(*args)

    class CreateOversetInterfaces(PyCommand):
        """
        Command CreateOversetInterfaces.

        Parameters
        ----------
        OversetInterfacesName : str
            Specify a name for the overset mesh interface or use the default value.
        ObjectSelectionList : list[str]
            Select one or more overset mesh objects that will make up the mesh interface. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...

        Returns
        -------
        bool
        """
        class _CreateOversetInterfacesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.OversetInterfacesName = self._OversetInterfacesName(self, "OversetInterfacesName", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)

            class _OversetInterfacesName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the overset mesh interface or use the default value.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more overset mesh objects that will make up the mesh interface. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _CreateOversetInterfacesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateOversetInterfacesCommandArguments(*args)

    class CreatePorousRegions(PyCommand):
        """
        Command CreatePorousRegions.

        Parameters
        ----------
        InputMethod : str
            Indicate whether you are creating the porous region using Direct coordinates, by using a Text file, or by specifying a Nonrectangular region.
        PorousRegionName : str
            Specify a name for the porous region or use the default value.
        WrapperSize : float
        FileName : str
            Specify the name and location of the text file containing the porous region definition.  More...
        Location : str
            Specify how you would like to determine the location of the porous region.
        CellSizeP1P2 : float
            Specify the size of the cells that lie between P1 and P2 of the porous region. P1 is the first point designated for the porous region; P2 is the second point of the porous region - created to the left of P1 in the same plane.
        CellSizeP1P3 : float
            Specify the size of the cells that lie between P1 and P3 of the porous region. P1 is the first point designated for the porous region; P3 is the third point of the porous region - created above P1 in the same plane.
        CellSizeP1P4 : float
            Specify the size of the cells that lie between P1 and P4 of the porous region. P1 is the first point designated for the porous region; P4 is the fourth point of the porous region - created in relation to P1 to essentially define a thickness for the porous region.
        BufferSizeRatio : float
            Specify a value for the buffer size ratio. The buffer is created as an extra layer. The thickness is equivalent to the product of the buffer size ratio and the core thickness. The core thickness is the distance between P1 and P4.
        P1 : list[float]
        P2 : list[float]
        P3 : list[float]
        P4 : list[float]
        NonRectangularParameters : dict[str, Any]

        Returns
        -------
        bool
        """
        class _CreatePorousRegionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.InputMethod = self._InputMethod(self, "InputMethod", service, rules, path)
                self.PorousRegionName = self._PorousRegionName(self, "PorousRegionName", service, rules, path)
                self.WrapperSize = self._WrapperSize(self, "WrapperSize", service, rules, path)
                self.FileName = self._FileName(self, "FileName", service, rules, path)
                self.Location = self._Location(self, "Location", service, rules, path)
                self.CellSizeP1P2 = self._CellSizeP1P2(self, "CellSizeP1P2", service, rules, path)
                self.CellSizeP1P3 = self._CellSizeP1P3(self, "CellSizeP1P3", service, rules, path)
                self.CellSizeP1P4 = self._CellSizeP1P4(self, "CellSizeP1P4", service, rules, path)
                self.BufferSizeRatio = self._BufferSizeRatio(self, "BufferSizeRatio", service, rules, path)
                self.P1 = self._P1(self, "P1", service, rules, path)
                self.P2 = self._P2(self, "P2", service, rules, path)
                self.P3 = self._P3(self, "P3", service, rules, path)
                self.P4 = self._P4(self, "P4", service, rules, path)
                self.NonRectangularParameters = self._NonRectangularParameters(self, "NonRectangularParameters", service, rules, path)

            class _InputMethod(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether you are creating the porous region using Direct coordinates, by using a Text file, or by specifying a Nonrectangular region.
                """

            class _PorousRegionName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the porous region or use the default value.
                """

            class _WrapperSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument WrapperSize.
                """

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Specify the name and location of the text file containing the porous region definition.  More...
                """

            class _Location(PyTextualCommandArgumentsSubItem):
                """
                Specify how you would like to determine the location of the porous region.
                """

            class _CellSizeP1P2(PyNumericalCommandArgumentsSubItem):
                """
                Specify the size of the cells that lie between P1 and P2 of the porous region. P1 is the first point designated for the porous region; P2 is the second point of the porous region - created to the left of P1 in the same plane.
                """

            class _CellSizeP1P3(PyNumericalCommandArgumentsSubItem):
                """
                Specify the size of the cells that lie between P1 and P3 of the porous region. P1 is the first point designated for the porous region; P3 is the third point of the porous region - created above P1 in the same plane.
                """

            class _CellSizeP1P4(PyNumericalCommandArgumentsSubItem):
                """
                Specify the size of the cells that lie between P1 and P4 of the porous region. P1 is the first point designated for the porous region; P4 is the fourth point of the porous region - created in relation to P1 to essentially define a thickness for the porous region.
                """

            class _BufferSizeRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the buffer size ratio. The buffer is created as an extra layer. The thickness is equivalent to the product of the buffer size ratio and the core thickness. The core thickness is the distance between P1 and P4.
                """

            class _P1(PyNumericalCommandArgumentsSubItem):
                """
                Argument P1.
                """

            class _P2(PyNumericalCommandArgumentsSubItem):
                """
                Argument P2.
                """

            class _P3(PyNumericalCommandArgumentsSubItem):
                """
                Argument P3.
                """

            class _P4(PyNumericalCommandArgumentsSubItem):
                """
                Argument P4.
                """

            class _NonRectangularParameters(PySingletonCommandArgumentsSubItem):
                """
                Argument NonRectangularParameters.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                    self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                    self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                    self.Thickness = self._Thickness(self, "Thickness", service, rules, path)
                    self.MeshSize = self._MeshSize(self, "MeshSize", service, rules, path)
                    self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                    self.BufferSize = self._BufferSize(self, "BufferSize", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.NonRectangularBufferSize = self._NonRectangularBufferSize(self, "NonRectangularBufferSize", service, rules, path)
                    self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)

                class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument LabelSelectionList.
                    """

                class _SelectionType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SelectionType.
                    """

                class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ZoneSelectionList.
                    """

                class _Thickness(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Thickness.
                    """

                class _MeshSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MeshSize.
                    """

                class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _BufferSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BufferSize.
                    """

                class _FlipDirection(PyParameterCommandArgumentsSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _NonRectangularBufferSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NonRectangularBufferSize.
                    """

                class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ObjectSelectionList.
                    """

        def create_instance(self) -> _CreatePorousRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreatePorousRegionsCommandArguments(*args)

    class CreateRegions(PyCommand):
        """
        Command CreateRegions.

        Parameters
        ----------
        NumberOfFlowVolumes : int
            Confirm the number of flow volumes required for the analysis. The system will detect additional regions if they exist, however, it will detect fluid regions only where they are connected to capping surfaces.
        RetainDeadRegionName : str
            If any dead regions are present, you can choose to determine how such regions are named. Voids or dead regions are usually named dead0, dead1, dead2, and so on, and can remain so when this prompt is set to no. When this prompt is set to yes, however, the dead region names will also be prefixed with the original dead region name (usually derived from an adjacent region), such as dead0-fluid:1, dead1-fluid:2, and so on.
        MeshObject : str

        Returns
        -------
        bool
        """
        class _CreateRegionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.NumberOfFlowVolumes = self._NumberOfFlowVolumes(self, "NumberOfFlowVolumes", service, rules, path)
                self.RetainDeadRegionName = self._RetainDeadRegionName(self, "RetainDeadRegionName", service, rules, path)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)

            class _NumberOfFlowVolumes(PyNumericalCommandArgumentsSubItem):
                """
                Confirm the number of flow volumes required for the analysis. The system will detect additional regions if they exist, however, it will detect fluid regions only where they are connected to capping surfaces.
                """

            class _RetainDeadRegionName(PyTextualCommandArgumentsSubItem):
                """
                If any dead regions are present, you can choose to determine how such regions are named. Voids or dead regions are usually named dead0, dead1, dead2, and so on, and can remain so when this prompt is set to no. When this prompt is set to yes, however, the dead region names will also be prefixed with the original dead region name (usually derived from an adjacent region), such as dead0-fluid:1, dead1-fluid:2, and so on.
                """

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

        def create_instance(self) -> _CreateRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateRegionsCommandArguments(*args)

    class DefineGlobalSizing(PyCommand):
        """
        Command DefineGlobalSizing.

        Parameters
        ----------
        MinSize : float
        MaxSize : float
        GrowthRate : float
        SizeFunctions : str
        CurvatureNormalAngle : float
        CellsPerGap : float
        ScopeProximityTo : str
        Mesher : str
        PrimeSizeControlIds : list[int]
        EnableMultiThreading : bool
        NumberOfMultiThreads : int

        Returns
        -------
        bool
        """
        class _DefineGlobalSizingCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                self.Mesher = self._Mesher(self, "Mesher", service, rules, path)
                self.PrimeSizeControlIds = self._PrimeSizeControlIds(self, "PrimeSizeControlIds", service, rules, path)
                self.EnableMultiThreading = self._EnableMultiThreading(self, "EnableMultiThreading", service, rules, path)
                self.NumberOfMultiThreads = self._NumberOfMultiThreads(self, "NumberOfMultiThreads", service, rules, path)

            class _MinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument MinSize.
                """

            class _MaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxSize.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument GrowthRate.
                """

            class _SizeFunctions(PyTextualCommandArgumentsSubItem):
                """
                Argument SizeFunctions.
                """

            class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument CurvatureNormalAngle.
                """

            class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                """
                Argument CellsPerGap.
                """

            class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                """
                Argument ScopeProximityTo.
                """

            class _Mesher(PyTextualCommandArgumentsSubItem):
                """
                Argument Mesher.
                """

            class _PrimeSizeControlIds(PyNumericalCommandArgumentsSubItem):
                """
                Argument PrimeSizeControlIds.
                """

            class _EnableMultiThreading(PyParameterCommandArgumentsSubItem):
                """
                Argument EnableMultiThreading.
                """

            class _NumberOfMultiThreads(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfMultiThreads.
                """

        def create_instance(self) -> _DefineGlobalSizingCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DefineGlobalSizingCommandArguments(*args)

    class DefineLeakageThreshold(PyCommand):
        """
        Command DefineLeakageThreshold.

        Parameters
        ----------
        AddChild : str
            Indicate whether or not you need to define a leakage threshold for one or more regions.
        LeakageName : str
            Specify a name for the leakage threshold or use the default value.
        SelectionType : str
            Choose how you want to make your selection (by object or by a previously identified region).
        DeadRegionsList : list[str]
            Choose one or more regions from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        RegionSelectionSingle : list[str]
            Choose a single region from the list of identified regions below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        DeadRegionsSize : float
            The leakage threshold size is based on multiples of two. For example, if leaks are detected at 8 but not at 16 (for example, 2*8), then the threshold size is 16, and any leakage smaller than 16 will be closed.
        PlaneClippingValue : int
            Use the slider to move the clipping plane along the axis of the selected X, Y, or Z direction.
        PlaneDirection : str
            Indicates the direction in which the clipping plane faces.
        FlipDirection : bool
            Change the orientation of the clipping plane, exposing the mesh on the opposite side.

        Returns
        -------
        bool
        """
        class _DefineLeakageThresholdCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.LeakageName = self._LeakageName(self, "LeakageName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.DeadRegionsList = self._DeadRegionsList(self, "DeadRegionsList", service, rules, path)
                self.RegionSelectionSingle = self._RegionSelectionSingle(self, "RegionSelectionSingle", service, rules, path)
                self.DeadRegionsSize = self._DeadRegionsSize(self, "DeadRegionsSize", service, rules, path)
                self.PlaneClippingValue = self._PlaneClippingValue(self, "PlaneClippingValue", service, rules, path)
                self.PlaneDirection = self._PlaneDirection(self, "PlaneDirection", service, rules, path)
                self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether or not you need to define a leakage threshold for one or more regions.
                """

            class _LeakageName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the leakage threshold or use the default value.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object or by a previously identified region).
                """

            class _DeadRegionsList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more regions from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _RegionSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single region from the list of identified regions below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _DeadRegionsSize(PyNumericalCommandArgumentsSubItem):
                """
                The leakage threshold size is based on multiples of two. For example, if leaks are detected at 8 but not at 16 (for example, 2\\*8), then the threshold size is 16, and any leakage smaller than 16 will be closed.
                """

            class _PlaneClippingValue(PyNumericalCommandArgumentsSubItem):
                """
                Use the slider to move the clipping plane along the axis of the selected X, Y, or Z direction.
                """

            class _PlaneDirection(PyTextualCommandArgumentsSubItem):
                """
                Indicates the direction in which the clipping plane faces.
                """

            class _FlipDirection(PyParameterCommandArgumentsSubItem):
                """
                Change the orientation of the clipping plane, exposing the mesh on the opposite side.
                """

        def create_instance(self) -> _DefineLeakageThresholdCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DefineLeakageThresholdCommandArguments(*args)

    class DescribeGeometryAndFlow(PyCommand):
        """
        Command DescribeGeometryAndFlow.

        Parameters
        ----------
        FlowType : str
            Specify the type of flow you want to simulate: external flow, internal flow, or both. The appropriate Standard Options (for example adding an enclosure, adding caps, etc.) will be selected for you, depending on your choice.
        GeometryOptions : bool
            Display standard geometry-based options that you may want to apply to the workflow.
        AddEnclosure : str
            Specify whether you are going to need to add an external flow boundary around your imported geometry. If so, this will add a Create External Flow Boundaries task to the workflow.
        CloseCaps : str
            Specify whether or not you will need to cover, or cap, and large holes in order to create an internal fluid flow region. If so, this will add an Enclose Fluid Regions (Capping) task to the workflow.
        LocalRefinementRegions : str
            Specify whether or not you will need to add local refinement in and around the imported geometry. If so, this will add a Create Local Refinement Regions task to the workflow.
        DescribeGeometryAndFlowOptions : dict[str, Any]
        AllTaskList : list[str]

        Returns
        -------
        bool
        """
        class _DescribeGeometryAndFlowCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FlowType = self._FlowType(self, "FlowType", service, rules, path)
                self.GeometryOptions = self._GeometryOptions(self, "GeometryOptions", service, rules, path)
                self.AddEnclosure = self._AddEnclosure(self, "AddEnclosure", service, rules, path)
                self.CloseCaps = self._CloseCaps(self, "CloseCaps", service, rules, path)
                self.LocalRefinementRegions = self._LocalRefinementRegions(self, "LocalRefinementRegions", service, rules, path)
                self.DescribeGeometryAndFlowOptions = self._DescribeGeometryAndFlowOptions(self, "DescribeGeometryAndFlowOptions", service, rules, path)
                self.AllTaskList = self._AllTaskList(self, "AllTaskList", service, rules, path)

            class _FlowType(PyTextualCommandArgumentsSubItem):
                """
                Specify the type of flow you want to simulate: external flow, internal flow, or both. The appropriate Standard Options (for example adding an enclosure, adding caps, etc.) will be selected for you, depending on your choice.
                """

            class _GeometryOptions(PyParameterCommandArgumentsSubItem):
                """
                Display standard geometry-based options that you may want to apply to the workflow.
                """

            class _AddEnclosure(PyTextualCommandArgumentsSubItem):
                """
                Specify whether you are going to need to add an external flow boundary around your imported geometry. If so, this will add a Create External Flow Boundaries task to the workflow.
                """

            class _CloseCaps(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you will need to cover, or cap, and large holes in order to create an internal fluid flow region. If so, this will add an Enclose Fluid Regions (Capping) task to the workflow.
                """

            class _LocalRefinementRegions(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you will need to add local refinement in and around the imported geometry. If so, this will add a Create Local Refinement Regions task to the workflow.
                """

            class _DescribeGeometryAndFlowOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument DescribeGeometryAndFlowOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.PorousRegions = self._PorousRegions(self, "PorousRegions", service, rules, path)
                    self.ZeroThickness = self._ZeroThickness(self, "ZeroThickness", service, rules, path)
                    self.CloseLeakges = self._CloseLeakges(self, "CloseLeakges", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.ExtractEdgeFeatures = self._ExtractEdgeFeatures(self, "ExtractEdgeFeatures", service, rules, path)
                    self.MovingObjects = self._MovingObjects(self, "MovingObjects", service, rules, path)
                    self.EnablePrimeWrapper = self._EnablePrimeWrapper(self, "EnablePrimeWrapper", service, rules, path)
                    self.EnableOverset = self._EnableOverset(self, "EnableOverset", service, rules, path)
                    self.IdentifyRegions = self._IdentifyRegions(self, "IdentifyRegions", service, rules, path)

                class _PorousRegions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PorousRegions.
                    """

                class _ZeroThickness(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ZeroThickness.
                    """

                class _CloseLeakges(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CloseLeakges.
                    """

                class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AdvancedOptions.
                    """

                class _ExtractEdgeFeatures(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExtractEdgeFeatures.
                    """

                class _MovingObjects(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MovingObjects.
                    """

                class _EnablePrimeWrapper(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EnablePrimeWrapper.
                    """

                class _EnableOverset(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EnableOverset.
                    """

                class _IdentifyRegions(PyTextualCommandArgumentsSubItem):
                    """
                    Identify specific regions in and around your imported geometry, such as a flow region surrounding a vehicle in an external flow simulation. In this task, you are positioning specific points in the domain where certain regions of interest can be identified and classified for later use in your simulation. More...
                    """

            class _AllTaskList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllTaskList.
                """

        def create_instance(self) -> _DescribeGeometryAndFlowCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DescribeGeometryAndFlowCommandArguments(*args)

    class DescribeOversetFeatures(PyCommand):
        """
        Command DescribeOversetFeatures.

        Parameters
        ----------
        AdvancedOptions : bool
        ComponentGrid : str
            Indicate whether you need to add an overset component mesh task to the workflow.
        CollarGrid : str
            Indicate whether you need to add an overset collar mesh task to the workflow
        BackgroundMesh : str
        OversetInterfaces : str

        Returns
        -------
        bool
        """
        class _DescribeOversetFeaturesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.ComponentGrid = self._ComponentGrid(self, "ComponentGrid", service, rules, path)
                self.CollarGrid = self._CollarGrid(self, "CollarGrid", service, rules, path)
                self.BackgroundMesh = self._BackgroundMesh(self, "BackgroundMesh", service, rules, path)
                self.OversetInterfaces = self._OversetInterfaces(self, "OversetInterfaces", service, rules, path)

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Argument AdvancedOptions.
                """

            class _ComponentGrid(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether you need to add an overset component mesh task to the workflow.
                """

            class _CollarGrid(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether you need to add an overset collar mesh task to the workflow
                """

            class _BackgroundMesh(PyTextualCommandArgumentsSubItem):
                """
                Argument BackgroundMesh.
                """

            class _OversetInterfaces(PyTextualCommandArgumentsSubItem):
                """
                Argument OversetInterfaces.
                """

        def create_instance(self) -> _DescribeOversetFeaturesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DescribeOversetFeaturesCommandArguments(*args)

    class ExtractEdges(PyCommand):
        """
        Command ExtractEdges.

        Parameters
        ----------
        ExtractEdgesName : str
            Specify a name for the edge feature extraction or use the default value.
        ExtractMethodType : str
            Choose how the edge features are to be extracted: either by feature angle, intersection loops, or by sharp angle.
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ObjectSelectionList : list[str]
            Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        GeomObjectSelectionList : list[str]
            Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Select one or more zones from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        FeatureAngleLocal : int
            Specify the minimum angle between the feature edges that should be preserved.
        IndividualCollective : str
            Choose face zone interactivity -  individual: considers intersection of face zones within the object(s) selected; collectively: consider intersection of faces only across selected objects.
        SharpAngle : int
            Use the slider to specify the sharp angle (in degrees) that will be used in the feature extraction.
        CompleteObjectSelectionList : list[str]
        CompleteGeomObjectSelectionList : list[str]
        NonExtractedObjects : list[str]

        Returns
        -------
        bool
        """
        class _ExtractEdgesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ExtractEdgesName = self._ExtractEdgesName(self, "ExtractEdgesName", service, rules, path)
                self.ExtractMethodType = self._ExtractMethodType(self, "ExtractMethodType", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.GeomObjectSelectionList = self._GeomObjectSelectionList(self, "GeomObjectSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.FeatureAngleLocal = self._FeatureAngleLocal(self, "FeatureAngleLocal", service, rules, path)
                self.IndividualCollective = self._IndividualCollective(self, "IndividualCollective", service, rules, path)
                self.SharpAngle = self._SharpAngle(self, "SharpAngle", service, rules, path)
                self.CompleteObjectSelectionList = self._CompleteObjectSelectionList(self, "CompleteObjectSelectionList", service, rules, path)
                self.CompleteGeomObjectSelectionList = self._CompleteGeomObjectSelectionList(self, "CompleteGeomObjectSelectionList", service, rules, path)
                self.NonExtractedObjects = self._NonExtractedObjects(self, "NonExtractedObjects", service, rules, path)

            class _ExtractEdgesName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the edge feature extraction or use the default value.
                """

            class _ExtractMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose how the edge features are to be extracted: either by feature angle, intersection loops, or by sharp angle.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GeomObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more zones from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _FeatureAngleLocal(PyNumericalCommandArgumentsSubItem):
                """
                Specify the minimum angle between the feature edges that should be preserved.
                """

            class _IndividualCollective(PyTextualCommandArgumentsSubItem):
                """
                Choose face zone interactivity -  individual: considers intersection of face zones within the object(s) selected; collectively: consider intersection of faces only across selected objects.
                """

            class _SharpAngle(PyNumericalCommandArgumentsSubItem):
                """
                Use the slider to specify the sharp angle (in degrees) that will be used in the feature extraction.
                """

            class _CompleteObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteObjectSelectionList.
                """

            class _CompleteGeomObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteGeomObjectSelectionList.
                """

            class _NonExtractedObjects(PyTextualCommandArgumentsSubItem):
                """
                Argument NonExtractedObjects.
                """

        def create_instance(self) -> _ExtractEdgesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ExtractEdgesCommandArguments(*args)

    class ExtrudeVolumeMesh(PyCommand):
        """
        Command ExtrudeVolumeMesh.

        Parameters
        ----------
        MExControlName : str
            Specify a name for the extrusion or use the default value.
        Method : str
            Choose whether you want the extrusion to be based on a specified Total Height value, or one based on a specified First Height value. The relationship between the two is illustrated by:
        SelectionType : str
        ExtendToPeriodicPair : bool
        ExtrudeNormalBased : bool
            Specify whether the volume extrusion is derived from normal-based faceting or direction-based faceting. When enabled (the default), the volume extrusion is derived on normal-based faceting, such that for each layer, the normal is calculated and smoothing occurs, and is suitable for non-planar surfaces. For planar surfaces, disable this option to use a direction-based approach where the direction is chosen based on the average normal of the entire surface, and is used to extrude all layers.
        ExternalBoundaryZoneList : list[str]
            Select one or more boundaries. All selected boundaries must share the same plane. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        TopologyList : list[str]
        TotalHeight : float
            Specify a value for the total height of the extrusion or use the default value.
        FirstHeight : float
            Specify a value for the height of the first layer of the extrusion or use the default value.
        NumberofLayers : int
            Specify the number of extrusion layers.
        GrowthRate : float
            Specify how the extrusion layers will grow. For example, a value of 1.2 indicates that each successive layer will grow by 20 percent of the previous layer. 
                            More...
        VMExtrudePreferences : dict[str, Any]
        ZoneLocation : list[str]

        Returns
        -------
        bool
        """
        class _ExtrudeVolumeMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MExControlName = self._MExControlName(self, "MExControlName", service, rules, path)
                self.Method = self._Method(self, "Method", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ExtendToPeriodicPair = self._ExtendToPeriodicPair(self, "ExtendToPeriodicPair", service, rules, path)
                self.ExtrudeNormalBased = self._ExtrudeNormalBased(self, "ExtrudeNormalBased", service, rules, path)
                self.ExternalBoundaryZoneList = self._ExternalBoundaryZoneList(self, "ExternalBoundaryZoneList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.TotalHeight = self._TotalHeight(self, "TotalHeight", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.NumberofLayers = self._NumberofLayers(self, "NumberofLayers", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.VMExtrudePreferences = self._VMExtrudePreferences(self, "VMExtrudePreferences", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _MExControlName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the extrusion or use the default value.
                """

            class _Method(PyTextualCommandArgumentsSubItem):
                """
                Choose whether you want the extrusion to be based on a specified Total Height value, or one based on a specified First Height value. The relationship between the two is illustrated by:
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ExtendToPeriodicPair(PyParameterCommandArgumentsSubItem):
                """
                Argument ExtendToPeriodicPair.
                """

            class _ExtrudeNormalBased(PyParameterCommandArgumentsSubItem):
                """
                Specify whether the volume extrusion is derived from normal-based faceting or direction-based faceting. When enabled (the default), the volume extrusion is derived on normal-based faceting, such that for each layer, the normal is calculated and smoothing occurs, and is suitable for non-planar surfaces. For planar surfaces, disable this option to use a direction-based approach where the direction is chosen based on the average normal of the entire surface, and is used to extrude all layers.
                """

            class _ExternalBoundaryZoneList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more boundaries. All selected boundaries must share the same plane. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _TotalHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the total height of the extrusion or use the default value.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the height of the first layer of the extrusion or use the default value.
                """

            class _NumberofLayers(PyNumericalCommandArgumentsSubItem):
                """
                Specify the number of extrusion layers.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Specify how the extrusion layers will grow. For example, a value of 1.2 indicates that each successive layer will grow by 20 percent of the previous layer. 
                                More...
                """

            class _VMExtrudePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument VMExtrudePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.BiasMethod = self._BiasMethod(self, "BiasMethod", service, rules, path)
                    self.MergeCellZones = self._MergeCellZones(self, "MergeCellZones", service, rules, path)
                    self.ShowVMExtrudePreferences = self._ShowVMExtrudePreferences(self, "ShowVMExtrudePreferences", service, rules, path)

                class _BiasMethod(PyTextualCommandArgumentsSubItem):
                    """
                    Argument BiasMethod.
                    """

                class _MergeCellZones(PyParameterCommandArgumentsSubItem):
                    """
                    Argument MergeCellZones.
                    """

                class _ShowVMExtrudePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowVMExtrudePreferences.
                    """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _ExtrudeVolumeMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ExtrudeVolumeMeshCommandArguments(*args)

    class GenerateInitialSurfaceMesh(PyCommand):
        """
        Command GenerateInitialSurfaceMesh.

        Parameters
        ----------
        GenerateQuads : bool
        ProjectOnGeometry : bool
        EnableMultiThreading : bool
        NumberOfMultiThreads : int
        Prism2DPreferences : dict[str, Any]
        Surface2DPreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _GenerateInitialSurfaceMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GenerateQuads = self._GenerateQuads(self, "GenerateQuads", service, rules, path)
                self.ProjectOnGeometry = self._ProjectOnGeometry(self, "ProjectOnGeometry", service, rules, path)
                self.EnableMultiThreading = self._EnableMultiThreading(self, "EnableMultiThreading", service, rules, path)
                self.NumberOfMultiThreads = self._NumberOfMultiThreads(self, "NumberOfMultiThreads", service, rules, path)
                self.Prism2DPreferences = self._Prism2DPreferences(self, "Prism2DPreferences", service, rules, path)
                self.Surface2DPreferences = self._Surface2DPreferences(self, "Surface2DPreferences", service, rules, path)

            class _GenerateQuads(PyParameterCommandArgumentsSubItem):
                """
                Argument GenerateQuads.
                """

            class _ProjectOnGeometry(PyParameterCommandArgumentsSubItem):
                """
                Argument ProjectOnGeometry.
                """

            class _EnableMultiThreading(PyParameterCommandArgumentsSubItem):
                """
                Argument EnableMultiThreading.
                """

            class _NumberOfMultiThreads(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfMultiThreads.
                """

            class _Prism2DPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument Prism2DPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SplitQuads = self._SplitQuads(self, "SplitQuads", service, rules, path)
                    self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.RemeshGrowthRate = self._RemeshGrowthRate(self, "RemeshGrowthRate", service, rules, path)
                    self.LocalRemesh = self._LocalRemesh(self, "LocalRemesh", service, rules, path)
                    self.MaxFaceSkew = self._MaxFaceSkew(self, "MaxFaceSkew", service, rules, path)
                    self.ShowPrism2DPreferences = self._ShowPrism2DPreferences(self, "ShowPrism2DPreferences", service, rules, path)
                    self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                    self.RefineStretchedQuads = self._RefineStretchedQuads(self, "RefineStretchedQuads", service, rules, path)
                    self.nOrthogonalLayers = self._nOrthogonalLayers(self, "nOrthogonalLayers", service, rules, path)

                class _SplitQuads(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SplitQuads.
                    """

                class _MaxAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxAspectRatio.
                    """

                class _MinAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinAspectRatio.
                    """

                class _RemeshGrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RemeshGrowthRate.
                    """

                class _LocalRemesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument LocalRemesh.
                    """

                class _MaxFaceSkew(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxFaceSkew.
                    """

                class _ShowPrism2DPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowPrism2DPreferences.
                    """

                class _GapFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GapFactor.
                    """

                class _RefineStretchedQuads(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RefineStretchedQuads.
                    """

                class _nOrthogonalLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument nOrthogonalLayers.
                    """

            class _Surface2DPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument Surface2DPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MergeFaceZonesBasedOnLabels = self._MergeFaceZonesBasedOnLabels(self, "MergeFaceZonesBasedOnLabels", service, rules, path)
                    self.MergeEdgeZonesBasedOnLabels = self._MergeEdgeZonesBasedOnLabels(self, "MergeEdgeZonesBasedOnLabels", service, rules, path)
                    self.ShowAdvancedOptions = self._ShowAdvancedOptions(self, "ShowAdvancedOptions", service, rules, path)

                class _MergeFaceZonesBasedOnLabels(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MergeFaceZonesBasedOnLabels.
                    """

                class _MergeEdgeZonesBasedOnLabels(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MergeEdgeZonesBasedOnLabels.
                    """

                class _ShowAdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowAdvancedOptions.
                    """

        def create_instance(self) -> _GenerateInitialSurfaceMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateInitialSurfaceMeshCommandArguments(*args)

    class GenerateMapMesh(PyCommand):
        """
        Command GenerateMapMesh.

        Parameters
        ----------
        AddChild : str
        ControlName : str
        SizingOption : str
        ConstantSize : float
        GrowthRate : float
        ShortSideDivisions : int
        SplitQuads : bool
        ProjectOnGeometry : bool
        SelectionType : str
        FaceLabelList : list[str]
        FaceZoneList : list[str]

        Returns
        -------
        bool
        """
        class _GenerateMapMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.ControlName = self._ControlName(self, "ControlName", service, rules, path)
                self.SizingOption = self._SizingOption(self, "SizingOption", service, rules, path)
                self.ConstantSize = self._ConstantSize(self, "ConstantSize", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.ShortSideDivisions = self._ShortSideDivisions(self, "ShortSideDivisions", service, rules, path)
                self.SplitQuads = self._SplitQuads(self, "SplitQuads", service, rules, path)
                self.ProjectOnGeometry = self._ProjectOnGeometry(self, "ProjectOnGeometry", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.FaceLabelList = self._FaceLabelList(self, "FaceLabelList", service, rules, path)
                self.FaceZoneList = self._FaceZoneList(self, "FaceZoneList", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Argument AddChild.
                """

            class _ControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument ControlName.
                """

            class _SizingOption(PyTextualCommandArgumentsSubItem):
                """
                Argument SizingOption.
                """

            class _ConstantSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument ConstantSize.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument GrowthRate.
                """

            class _ShortSideDivisions(PyNumericalCommandArgumentsSubItem):
                """
                Argument ShortSideDivisions.
                """

            class _SplitQuads(PyParameterCommandArgumentsSubItem):
                """
                Argument SplitQuads.
                """

            class _ProjectOnGeometry(PyParameterCommandArgumentsSubItem):
                """
                Argument ProjectOnGeometry.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _FaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceLabelList.
                """

            class _FaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceZoneList.
                """

        def create_instance(self) -> _GenerateMapMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateMapMeshCommandArguments(*args)

    class GeneratePrisms(PyCommand):
        """
        Command GeneratePrisms.

        Parameters
        ----------
        GeneratePrismsOption : bool

        Returns
        -------
        bool
        """
        class _GeneratePrismsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GeneratePrismsOption = self._GeneratePrismsOption(self, "GeneratePrismsOption", service, rules, path)

            class _GeneratePrismsOption(PyParameterCommandArgumentsSubItem):
                """
                Argument GeneratePrismsOption.
                """

        def create_instance(self) -> _GeneratePrismsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GeneratePrismsCommandArguments(*args)

    class GenerateShellBoundaryLayerMesh(PyCommand):
        """
        Command GenerateShellBoundaryLayerMesh.

        Parameters
        ----------
        GapFactor : float
        MaxAspectRatio : float
        MinAspectRatio : float
        LocalRemesh : str
        RemeshGrowthRate : float
        RefineStretchedQuads : str
        SplitQuads : str
        nOrthogonalLayers : int
        MaxFaceSkew : float

        Returns
        -------
        bool
        """
        class _GenerateShellBoundaryLayerMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                self.LocalRemesh = self._LocalRemesh(self, "LocalRemesh", service, rules, path)
                self.RemeshGrowthRate = self._RemeshGrowthRate(self, "RemeshGrowthRate", service, rules, path)
                self.RefineStretchedQuads = self._RefineStretchedQuads(self, "RefineStretchedQuads", service, rules, path)
                self.SplitQuads = self._SplitQuads(self, "SplitQuads", service, rules, path)
                self.nOrthogonalLayers = self._nOrthogonalLayers(self, "nOrthogonalLayers", service, rules, path)
                self.MaxFaceSkew = self._MaxFaceSkew(self, "MaxFaceSkew", service, rules, path)

            class _GapFactor(PyNumericalCommandArgumentsSubItem):
                """
                Argument GapFactor.
                """

            class _MaxAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxAspectRatio.
                """

            class _MinAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument MinAspectRatio.
                """

            class _LocalRemesh(PyTextualCommandArgumentsSubItem):
                """
                Argument LocalRemesh.
                """

            class _RemeshGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument RemeshGrowthRate.
                """

            class _RefineStretchedQuads(PyTextualCommandArgumentsSubItem):
                """
                Argument RefineStretchedQuads.
                """

            class _SplitQuads(PyTextualCommandArgumentsSubItem):
                """
                Argument SplitQuads.
                """

            class _nOrthogonalLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument nOrthogonalLayers.
                """

            class _MaxFaceSkew(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxFaceSkew.
                """

        def create_instance(self) -> _GenerateShellBoundaryLayerMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateShellBoundaryLayerMeshCommandArguments(*args)

    class GenerateTheMultiZoneMesh(PyCommand):
        """
        Command GenerateTheMultiZoneMesh.

        Parameters
        ----------
        OrthogonalQualityLimit : float
            This value sets the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit, and is recommended to be around 0.04.
        SelectionType : str
        RegionScope : list[str]
            Select the named region(s) from the list to which you would like to generate the multi-zone mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        NonConformal : str
            Optionally specify that multizone regions are non-conformally connected to other volumetric regions.  If you want to have a conformal mesh but, because of meshing constraints, that is not possible, then you can switch to non-conformal here and avoid doing so in the CAD model.
        SizeFunctionScaleFactor : float
            Enable the scaling of the multizone mesh. In some cases when the multizone region is too coarse when compared to the adjacent surface mesh, a connection is not possible. You can specify a size function scaling factor here to improve the sizing match between the multizone and the non-multizone regions and avoid any free faces. Typically, a value between 0.7 and 0.8 is recommended.
        MeshingStrategy : str
        ReMergeZones : str
        MergeBodyLabels : str
        CFDSurfaceMeshControls : dict[str, Any]
        BodyLabelList : list[str]
        CellZoneList : list[str]
        CompleteRegionScope : list[str]

        Returns
        -------
        bool
        """
        class _GenerateTheMultiZoneMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.OrthogonalQualityLimit = self._OrthogonalQualityLimit(self, "OrthogonalQualityLimit", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.NonConformal = self._NonConformal(self, "NonConformal", service, rules, path)
                self.SizeFunctionScaleFactor = self._SizeFunctionScaleFactor(self, "SizeFunctionScaleFactor", service, rules, path)
                self.MeshingStrategy = self._MeshingStrategy(self, "MeshingStrategy", service, rules, path)
                self.ReMergeZones = self._ReMergeZones(self, "ReMergeZones", service, rules, path)
                self.MergeBodyLabels = self._MergeBodyLabels(self, "MergeBodyLabels", service, rules, path)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.BodyLabelList = self._BodyLabelList(self, "BodyLabelList", service, rules, path)
                self.CellZoneList = self._CellZoneList(self, "CellZoneList", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)

            class _OrthogonalQualityLimit(PyNumericalCommandArgumentsSubItem):
                """
                This value sets the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit, and is recommended to be around 0.04.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Select the named region(s) from the list to which you would like to generate the multi-zone mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _NonConformal(PyTextualCommandArgumentsSubItem):
                """
                Optionally specify that multizone regions are non-conformally connected to other volumetric regions.  If you want to have a conformal mesh but, because of meshing constraints, that is not possible, then you can switch to non-conformal here and avoid doing so in the CAD model.
                """

            class _SizeFunctionScaleFactor(PyNumericalCommandArgumentsSubItem):
                """
                Enable the scaling of the multizone mesh. In some cases when the multizone region is too coarse when compared to the adjacent surface mesh, a connection is not possible. You can specify a size function scaling factor here to improve the sizing match between the multizone and the non-multizone regions and avoid any free faces. Typically, a value between 0.7 and 0.8 is recommended.
                """

            class _MeshingStrategy(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshingStrategy.
                """

            class _ReMergeZones(PyTextualCommandArgumentsSubItem):
                """
                Argument ReMergeZones.
                """

            class _MergeBodyLabels(PyTextualCommandArgumentsSubItem):
                """
                Argument MergeBodyLabels.
                """

            class _CFDSurfaceMeshControls(PySingletonCommandArgumentsSubItem):
                """
                Argument CFDSurfaceMeshControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SaveSizeFieldFile = self._SaveSizeFieldFile(self, "SaveSizeFieldFile", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.PreviewSizefield = self._PreviewSizefield(self, "PreviewSizefield", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.SaveSizeField = self._SaveSizeField(self, "SaveSizeField", service, rules, path)
                    self.UseSizeFiles = self._UseSizeFiles(self, "UseSizeFiles", service, rules, path)
                    self.AutoCreateScopedSizing = self._AutoCreateScopedSizing(self, "AutoCreateScopedSizing", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyParameterCommandArgumentsSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _BodyLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BodyLabelList.
                """

            class _CellZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument CellZoneList.
                """

            class _CompleteRegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteRegionScope.
                """

        def create_instance(self) -> _GenerateTheMultiZoneMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheMultiZoneMeshCommandArguments(*args)

    class GenerateTheSurfaceMeshFTM(PyCommand):
        """
        Command GenerateTheSurfaceMeshFTM.

        Parameters
        ----------
        SurfaceQuality : float
            This is the target maximum surface mesh quality. The recommended value is between 0.7 and 0.85.
        SaveSurfaceMesh : bool
            Select this option to save the surface mesh. Use advanced options to determine whether to save intermediate files or not, and to choose a specific directory to save the mesh.
        AdvancedOptions : bool
            Display advanced options that you may want to apply to the task.
        SaveIntermediateFiles : str
            Determine whether or not you want to save any intermediate files that are generated during volume meshing. Disabling this option may increase speed and efficiency.
        IntermediateFileName : str
            By default, files are saved in a temporary folder and later deleted once the session is ended. You can also save files in a specified folder. The prefix for the name of the files are taken from the FMD or STL file name.
        SeparateSurface : str
            Select Yes if you want to have the final surface mesh to be viewed as separated zones.
        UseSizeFieldForPrimeWrap : str
        AutoPairing : str
            Specify whether or not you want to separate contact pairs between fluids and solids.
        MergeWrapperAtSolidConacts : str
            Specify whether or not you want to allow contacts between solid and fluid regions to be merged into the surface mesh wrapper. When enabled, all bounding faces of a fluid region wrap that come into contact with solid regions will be merged into a single zone (using the prefix _contact). Each respective wrapped fluid region will have one _contact zone associated with it.
        ParallelSerialOption : str
            Specify whether or not you want to perform solid meshing using parallel sessions. Select Yes and indicate the Maximum Number of Sessions. The number of parallel sessions that are used will depend upon the number of solid objects that need to be meshed.
        NumberOfSessions : int
            Indicate the number of parallel sessions that are to be used, depending upon the number of solid objects that need to be meshed.
        MaxIslandFace : int
            Specify the maximum face count required for isolated areas (islands) to be created during surface mesh generation. Any islands that have a face count smaller than this value will be removed, and only larger islands will remain.
        SpikeRemovalAngle : float
            Specify a value for the minimum spike angle for the specified region. A spike angle of 250 degrees is recommended or use the default value. You should not exceed 260 degrees.
        DihedralMinAngle : float
            Specify a value for the minimum dihedral angle for the specified region. A dihedral angle of 30 degrees are recommended or use the default value. You should not exceed 30 degrees.
        ProjectOnGeometry : str
            Determine whether, after surface meshing, Fluent will project the mesh nodes back onto to the original CAD model.
        AutoAssignZoneTypes : str
            Choose whether or not to automatically assign boundary types to zones.
        AdvancedInnerWrap : str
            Choose whether or not to extend or expand the surface mesh into any interior pockets or cavities.
        GapCoverZoneRecovery : str
            Determine whether or not to keep or remove the zones representing the cap covers. When set to Yes, the zones representing the gap covers are retained, whereas when set to No (the default), the zones for the gap covers are removed.
        GlobalMin : float
            Specify a global minimum value for the surface mesh. The default minimum value is calculated based on available target and wrap size controls and bodies of influence. 
                            More...
        ShowSubTasks : str

        Returns
        -------
        bool
        """
        class _GenerateTheSurfaceMeshFTMCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.SurfaceQuality = self._SurfaceQuality(self, "SurfaceQuality", service, rules, path)
                self.SaveSurfaceMesh = self._SaveSurfaceMesh(self, "SaveSurfaceMesh", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.SaveIntermediateFiles = self._SaveIntermediateFiles(self, "SaveIntermediateFiles", service, rules, path)
                self.IntermediateFileName = self._IntermediateFileName(self, "IntermediateFileName", service, rules, path)
                self.SeparateSurface = self._SeparateSurface(self, "SeparateSurface", service, rules, path)
                self.UseSizeFieldForPrimeWrap = self._UseSizeFieldForPrimeWrap(self, "UseSizeFieldForPrimeWrap", service, rules, path)
                self.AutoPairing = self._AutoPairing(self, "AutoPairing", service, rules, path)
                self.MergeWrapperAtSolidConacts = self._MergeWrapperAtSolidConacts(self, "MergeWrapperAtSolidConacts", service, rules, path)
                self.ParallelSerialOption = self._ParallelSerialOption(self, "ParallelSerialOption", service, rules, path)
                self.NumberOfSessions = self._NumberOfSessions(self, "NumberOfSessions", service, rules, path)
                self.MaxIslandFace = self._MaxIslandFace(self, "MaxIslandFace", service, rules, path)
                self.SpikeRemovalAngle = self._SpikeRemovalAngle(self, "SpikeRemovalAngle", service, rules, path)
                self.DihedralMinAngle = self._DihedralMinAngle(self, "DihedralMinAngle", service, rules, path)
                self.ProjectOnGeometry = self._ProjectOnGeometry(self, "ProjectOnGeometry", service, rules, path)
                self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                self.AdvancedInnerWrap = self._AdvancedInnerWrap(self, "AdvancedInnerWrap", service, rules, path)
                self.GapCoverZoneRecovery = self._GapCoverZoneRecovery(self, "GapCoverZoneRecovery", service, rules, path)
                self.GlobalMin = self._GlobalMin(self, "GlobalMin", service, rules, path)
                self.ShowSubTasks = self._ShowSubTasks(self, "ShowSubTasks", service, rules, path)

            class _SurfaceQuality(PyNumericalCommandArgumentsSubItem):
                """
                This is the target maximum surface mesh quality. The recommended value is between 0.7 and 0.85.
                """

            class _SaveSurfaceMesh(PyParameterCommandArgumentsSubItem):
                """
                Select this option to save the surface mesh. Use advanced options to determine whether to save intermediate files or not, and to choose a specific directory to save the mesh.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _SaveIntermediateFiles(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to save any intermediate files that are generated during volume meshing. Disabling this option may increase speed and efficiency.
                """

            class _IntermediateFileName(PyTextualCommandArgumentsSubItem):
                """
                By default, files are saved in a temporary folder and later deleted once the session is ended. You can also save files in a specified folder. The prefix for the name of the files are taken from the FMD or STL file name.
                """

            class _SeparateSurface(PyTextualCommandArgumentsSubItem):
                """
                Select Yes if you want to have the final surface mesh to be viewed as separated zones.
                """

            class _UseSizeFieldForPrimeWrap(PyTextualCommandArgumentsSubItem):
                """
                Argument UseSizeFieldForPrimeWrap.
                """

            class _AutoPairing(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you want to separate contact pairs between fluids and solids.
                """

            class _MergeWrapperAtSolidConacts(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you want to allow contacts between solid and fluid regions to be merged into the surface mesh wrapper. When enabled, all bounding faces of a fluid region wrap that come into contact with solid regions will be merged into a single zone (using the prefix _contact). Each respective wrapped fluid region will have one _contact zone associated with it.
                """

            class _ParallelSerialOption(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you want to perform solid meshing using parallel sessions. Select Yes and indicate the Maximum Number of Sessions. The number of parallel sessions that are used will depend upon the number of solid objects that need to be meshed.
                """

            class _NumberOfSessions(PyNumericalCommandArgumentsSubItem):
                """
                Indicate the number of parallel sessions that are to be used, depending upon the number of solid objects that need to be meshed.
                """

            class _MaxIslandFace(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum face count required for isolated areas (islands) to be created during surface mesh generation. Any islands that have a face count smaller than this value will be removed, and only larger islands will remain.
                """

            class _SpikeRemovalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the minimum spike angle for the specified region. A spike angle of 250 degrees is recommended or use the default value. You should not exceed 260 degrees.
                """

            class _DihedralMinAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the minimum dihedral angle for the specified region. A dihedral angle of 30 degrees are recommended or use the default value. You should not exceed 30 degrees.
                """

            class _ProjectOnGeometry(PyTextualCommandArgumentsSubItem):
                """
                Determine whether, after surface meshing, Fluent will project the mesh nodes back onto to the original CAD model.
                """

            class _AutoAssignZoneTypes(PyTextualCommandArgumentsSubItem):
                """
                Choose whether or not to automatically assign boundary types to zones.
                """

            class _AdvancedInnerWrap(PyTextualCommandArgumentsSubItem):
                """
                Choose whether or not to extend or expand the surface mesh into any interior pockets or cavities.
                """

            class _GapCoverZoneRecovery(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not to keep or remove the zones representing the cap covers. When set to Yes, the zones representing the gap covers are retained, whereas when set to No (the default), the zones for the gap covers are removed.
                """

            class _GlobalMin(PyNumericalCommandArgumentsSubItem):
                """
                Specify a global minimum value for the surface mesh. The default minimum value is calculated based on available target and wrap size controls and bodies of influence. 
                                More...
                """

            class _ShowSubTasks(PyTextualCommandArgumentsSubItem):
                """
                Argument ShowSubTasks.
                """

        def create_instance(self) -> _GenerateTheSurfaceMeshFTMCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheSurfaceMeshFTMCommandArguments(*args)

    class GenerateTheSurfaceMeshWTM(PyCommand):
        """
        Command GenerateTheSurfaceMeshWTM.

        Parameters
        ----------
        CFDSurfaceMeshControls : dict[str, Any]
        SeparationRequired : str
            Choose whether or not to separate face zones. By default, this is set to No. If you choose to separate zones, specify a Separation Angle. You should separate zones when using Multizone meshing. Separation is needed in case named selections for inlets, outlets, capping, local boundary layers, etc. have not been defined within the CAD model in advance. You should only select Yes if you need to separate faces for capping, boundary conditions, or inflation on specific faces.
        SeparationAngle : float
            Specify a desired angle for determining separation. Assigning a smaller separation angle will produce more zones.
        RemeshSelectionType : str
            Choose how you want to select your surface(s) to remesh (by label or by zone).
        RemeshZoneList : list[str]
        RemeshLabelList : list[str]
        SurfaceMeshPreferences : dict[str, Any]
        ImportType : str
        AppendMesh : bool
        CadFacetingFileName : str
        Directory : str
        Pattern : str
        LengthUnit : str
        TesselationMethod : str
        OriginalZones : list[str]
        ExecuteShareTopology : str
        CADFacetingControls : dict[str, Any]
        CadImportOptions : dict[str, Any]
        ShareTopologyPreferences : dict[str, Any]
        PreviewSizeToggle : bool
            For an imported surface mesh, use this field to visualize those boundaries that already have assigned local sizing controls (and any selected boundaries if applicable).

        Returns
        -------
        bool
        """
        class _GenerateTheSurfaceMeshWTMCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.SeparationRequired = self._SeparationRequired(self, "SeparationRequired", service, rules, path)
                self.SeparationAngle = self._SeparationAngle(self, "SeparationAngle", service, rules, path)
                self.RemeshSelectionType = self._RemeshSelectionType(self, "RemeshSelectionType", service, rules, path)
                self.RemeshZoneList = self._RemeshZoneList(self, "RemeshZoneList", service, rules, path)
                self.RemeshLabelList = self._RemeshLabelList(self, "RemeshLabelList", service, rules, path)
                self.SurfaceMeshPreferences = self._SurfaceMeshPreferences(self, "SurfaceMeshPreferences", service, rules, path)
                self.ImportType = self._ImportType(self, "ImportType", service, rules, path)
                self.AppendMesh = self._AppendMesh(self, "AppendMesh", service, rules, path)
                self.CadFacetingFileName = self._CadFacetingFileName(self, "CadFacetingFileName", service, rules, path)
                self.Directory = self._Directory(self, "Directory", service, rules, path)
                self.Pattern = self._Pattern(self, "Pattern", service, rules, path)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.TesselationMethod = self._TesselationMethod(self, "TesselationMethod", service, rules, path)
                self.OriginalZones = self._OriginalZones(self, "OriginalZones", service, rules, path)
                self.ExecuteShareTopology = self._ExecuteShareTopology(self, "ExecuteShareTopology", service, rules, path)
                self.CADFacetingControls = self._CADFacetingControls(self, "CADFacetingControls", service, rules, path)
                self.CadImportOptions = self._CadImportOptions(self, "CadImportOptions", service, rules, path)
                self.ShareTopologyPreferences = self._ShareTopologyPreferences(self, "ShareTopologyPreferences", service, rules, path)
                self.PreviewSizeToggle = self._PreviewSizeToggle(self, "PreviewSizeToggle", service, rules, path)

            class _CFDSurfaceMeshControls(PySingletonCommandArgumentsSubItem):
                """
                Argument CFDSurfaceMeshControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SaveSizeFieldFile = self._SaveSizeFieldFile(self, "SaveSizeFieldFile", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.PreviewSizefield = self._PreviewSizefield(self, "PreviewSizefield", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.SaveSizeField = self._SaveSizeField(self, "SaveSizeField", service, rules, path)
                    self.UseSizeFiles = self._UseSizeFiles(self, "UseSizeFiles", service, rules, path)
                    self.AutoCreateScopedSizing = self._AutoCreateScopedSizing(self, "AutoCreateScopedSizing", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyParameterCommandArgumentsSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _SeparationRequired(PyTextualCommandArgumentsSubItem):
                """
                Choose whether or not to separate face zones. By default, this is set to No. If you choose to separate zones, specify a Separation Angle. You should separate zones when using Multizone meshing. Separation is needed in case named selections for inlets, outlets, capping, local boundary layers, etc. have not been defined within the CAD model in advance. You should only select Yes if you need to separate faces for capping, boundary conditions, or inflation on specific faces.
                """

            class _SeparationAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify a desired angle for determining separation. Assigning a smaller separation angle will produce more zones.
                """

            class _RemeshSelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to select your surface(s) to remesh (by label or by zone).
                """

            class _RemeshZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshZoneList.
                """

            class _RemeshLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshLabelList.
                """

            class _SurfaceMeshPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument SurfaceMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SMQualityCollapseLimit = self._SMQualityCollapseLimit(self, "SMQualityCollapseLimit", service, rules, path)
                    self.AutoMerge = self._AutoMerge(self, "AutoMerge", service, rules, path)
                    self.SMQualityImprove = self._SMQualityImprove(self, "SMQualityImprove", service, rules, path)
                    self.SMSeparationAngle = self._SMSeparationAngle(self, "SMSeparationAngle", service, rules, path)
                    self.FoldFaceLimit = self._FoldFaceLimit(self, "FoldFaceLimit", service, rules, path)
                    self.ShowSurfaceMeshPreferences = self._ShowSurfaceMeshPreferences(self, "ShowSurfaceMeshPreferences", service, rules, path)
                    self.TVMAutoControlCreation = self._TVMAutoControlCreation(self, "TVMAutoControlCreation", service, rules, path)
                    self.SMSeparation = self._SMSeparation(self, "SMSeparation", service, rules, path)
                    self.SMRemoveStep = self._SMRemoveStep(self, "SMRemoveStep", service, rules, path)
                    self.SMStepWidth = self._SMStepWidth(self, "SMStepWidth", service, rules, path)
                    self.VolumeMeshMaxSize = self._VolumeMeshMaxSize(self, "VolumeMeshMaxSize", service, rules, path)
                    self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                    self.SMQualityMaxAngle = self._SMQualityMaxAngle(self, "SMQualityMaxAngle", service, rules, path)
                    self.SelfIntersectCheck = self._SelfIntersectCheck(self, "SelfIntersectCheck", service, rules, path)
                    self.AutoSurfaceRemesh = self._AutoSurfaceRemesh(self, "AutoSurfaceRemesh", service, rules, path)
                    self.SMQualityImproveLimit = self._SMQualityImproveLimit(self, "SMQualityImproveLimit", service, rules, path)
                    self.SetVolumeMeshMaxSize = self._SetVolumeMeshMaxSize(self, "SetVolumeMeshMaxSize", service, rules, path)

                class _SMQualityCollapseLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityCollapseLimit.
                    """

                class _AutoMerge(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoMerge.
                    """

                class _SMQualityImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMQualityImprove.
                    """

                class _SMSeparationAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMSeparationAngle.
                    """

                class _FoldFaceLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FoldFaceLimit.
                    """

                class _ShowSurfaceMeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSurfaceMeshPreferences.
                    """

                class _TVMAutoControlCreation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument TVMAutoControlCreation.
                    """

                class _SMSeparation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMSeparation.
                    """

                class _SMRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMRemoveStep.
                    """

                class _SMStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMStepWidth.
                    """

                class _VolumeMeshMaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VolumeMeshMaxSize.
                    """

                class _AutoAssignZoneTypes(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoAssignZoneTypes.
                    """

                class _SMQualityMaxAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityMaxAngle.
                    """

                class _SelfIntersectCheck(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SelfIntersectCheck.
                    """

                class _AutoSurfaceRemesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoSurfaceRemesh.
                    """

                class _SMQualityImproveLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityImproveLimit.
                    """

                class _SetVolumeMeshMaxSize(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SetVolumeMeshMaxSize.
                    """

            class _ImportType(PyTextualCommandArgumentsSubItem):
                """
                Argument ImportType.
                """

            class _AppendMesh(PyParameterCommandArgumentsSubItem):
                """
                Argument AppendMesh.
                """

            class _CadFacetingFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument CadFacetingFileName.
                """

            class _Directory(PyTextualCommandArgumentsSubItem):
                """
                Argument Directory.
                """

            class _Pattern(PyTextualCommandArgumentsSubItem):
                """
                Argument Pattern.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument LengthUnit.
                """

            class _TesselationMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument TesselationMethod.
                """

            class _OriginalZones(PyTextualCommandArgumentsSubItem):
                """
                Argument OriginalZones.
                """

            class _ExecuteShareTopology(PyTextualCommandArgumentsSubItem):
                """
                Argument ExecuteShareTopology.
                """

            class _CADFacetingControls(PySingletonCommandArgumentsSubItem):
                """
                Argument CADFacetingControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.RefineFaceting = self._RefineFaceting(self, "RefineFaceting", service, rules, path)
                    self.Tolerance = self._Tolerance(self, "Tolerance", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _RefineFaceting(PyParameterCommandArgumentsSubItem):
                    """
                    Argument RefineFaceting.
                    """

                class _Tolerance(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Tolerance.
                    """

            class _CadImportOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument CadImportOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SavePMDBIntermediateFile = self._SavePMDBIntermediateFile(self, "SavePMDBIntermediateFile", service, rules, path)
                    self.OneObjectPer = self._OneObjectPer(self, "OneObjectPer", service, rules, path)
                    self.OpenAllCadInSubdirectories = self._OpenAllCadInSubdirectories(self, "OpenAllCadInSubdirectories", service, rules, path)
                    self.CreateCADAssemblies = self._CreateCADAssemblies(self, "CreateCADAssemblies", service, rules, path)
                    self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                    self.OneZonePer = self._OneZonePer(self, "OneZonePer", service, rules, path)
                    self.UsePartOrBodyAsSuffix = self._UsePartOrBodyAsSuffix(self, "UsePartOrBodyAsSuffix", service, rules, path)
                    self.ExtractFeatures = self._ExtractFeatures(self, "ExtractFeatures", service, rules, path)
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)
                    self.ImportPartNames = self._ImportPartNames(self, "ImportPartNames", service, rules, path)
                    self.ImportCurvatureDataFromCAD = self._ImportCurvatureDataFromCAD(self, "ImportCurvatureDataFromCAD", service, rules, path)

                class _SavePMDBIntermediateFile(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SavePMDBIntermediateFile.
                    """

                class _OneObjectPer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OneObjectPer.
                    """

                class _OpenAllCadInSubdirectories(PyParameterCommandArgumentsSubItem):
                    """
                    Argument OpenAllCadInSubdirectories.
                    """

                class _CreateCADAssemblies(PyParameterCommandArgumentsSubItem):
                    """
                    Argument CreateCADAssemblies.
                    """

                class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _OneZonePer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OneZonePer.
                    """

                class _UsePartOrBodyAsSuffix(PyParameterCommandArgumentsSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
                    """

                class _ExtractFeatures(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _ImportNamedSelections(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

                class _ImportPartNames(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _ImportCurvatureDataFromCAD(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportCurvatureDataFromCAD.
                    """

            class _ShareTopologyPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument ShareTopologyPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.STRenameInternals = self._STRenameInternals(self, "STRenameInternals", service, rules, path)
                    self.ModelIsPeriodic = self._ModelIsPeriodic(self, "ModelIsPeriodic", service, rules, path)
                    self.ConnectLabelWildcard = self._ConnectLabelWildcard(self, "ConnectLabelWildcard", service, rules, path)
                    self.AllowDefeaturing = self._AllowDefeaturing(self, "AllowDefeaturing", service, rules, path)
                    self.RelativeShareTopologyTolerance = self._RelativeShareTopologyTolerance(self, "RelativeShareTopologyTolerance", service, rules, path)
                    self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                    self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                    self.Operation = self._Operation(self, "Operation", service, rules, path)
                    self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                    self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                    self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                    self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                    self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)

                class _STRenameInternals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument STRenameInternals.
                    """

                class _ModelIsPeriodic(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModelIsPeriodic.
                    """

                class _ConnectLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ConnectLabelWildcard.
                    """

                class _AllowDefeaturing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _RelativeShareTopologyTolerance(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RelativeShareTopologyTolerance.
                    """

                class _ShareTopologyAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShareTopologyAngle.
                    """

                class _ExecuteJoinIntersect(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExecuteJoinIntersect.
                    """

                class _Operation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Operation.
                    """

                class _FluidLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FluidLabelWildcard.
                    """

                class _STToleranceIncrement(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument STToleranceIncrement.
                    """

                class _ShowShareTopologyPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowShareTopologyPreferences.
                    """

                class _PerLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PerLabelList.
                    """

                class _IntfLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IntfLabelList.
                    """

                class _AdvancedImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _NumberOfJoinTries(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfJoinTries.
                    """

            class _PreviewSizeToggle(PyParameterCommandArgumentsSubItem):
                """
                For an imported surface mesh, use this field to visualize those boundaries that already have assigned local sizing controls (and any selected boundaries if applicable).
                """

        def create_instance(self) -> _GenerateTheSurfaceMeshWTMCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheSurfaceMeshWTMCommandArguments(*args)

    class GenerateTheVolumeMeshFTM(PyCommand):
        """
        Command GenerateTheVolumeMeshFTM.

        Parameters
        ----------
        MeshQuality : float
        OrthogonalQuality : float
            This value sets the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit, and is recommended to be around 0.04.
        EnableParallel : bool
            Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.
        SaveVolumeMesh : bool
            Select this option to save the volume mesh.
        EditVolumeSettings : bool
            Enable this option to review and/or edit the fill settings for your volume region(s).
        RegionNameList : list[str]
        RegionVolumeFillList : list[str]
        RegionSizeList : list[str]
        OldRegionNameList : list[str]
        OldRegionVolumeFillList : list[str]
        OldRegionSizeList : list[str]
        AllRegionNameList : list[str]
        AllRegionVolumeFillList : list[str]
        AllRegionSizeList : list[str]
        AdvancedOptions : bool
            Display advanced options that you may want to apply to the task.
        SpikeRemovalAngle : float
        DihedralMinAngle : float
        QualityMethod : str
            Choose from different types of mesh quality controls (aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows) and Enhanced Orthogonal. For more information, see  More... .
        AvoidHangingNodes : str
            Specify whether or not you want to avoid any potential 1:8 cell transition in the hexcore or polyhexcore region of the volume mesh, replacing any abrupt change in the cell size with tetrahedral or polyhedral cells.
        OctreePeelLayers : int
            Specify the number of octree layers to be removed between the boundary and the core. The resulting cavity will be filled with tet cells for hexcore meshes and with poly cells for polyhexcore meshes.
        FillWithSizeField : str
            Determine whether or not you want to use size fields when generating the volume mesh. Generating the volume mesh using size fields can require additional memory as you increase the number of processing cores. This is because the size field is replicated for each core as the size field is not properly distributed. When using size fields, you are limited by the size of the machine. When not using size fields, however, you require less memory and you can use a higher number of cores with limited RAM, leading to a faster mesh generation.
        OctreeBoundaryFaceSizeRatio : float
            Specify the ratio between the octree face size and the boundary face size. The default is 2.5 such that the octree mesh near the boundary is 2.5 times larger than the boundary mesh.
        GlobalBufferLayers : int
            Specify the number of buffer layers for the octree volume mesh. If size controls have not been defined previously, then the default is 2, otherwise the default is calculated based on the maximum growth size.
        TetPolyGrowthRate : float
            Specify the maximum growth rate for tet and poly cells. By default, this corresponds to a growth rate of 1.2.
        ConformalPrismSplit : str
            Since neighboring zones with different numbers of layers will lead to conformal prism layers between them, use this field to determine whether you want to split the boundary layer cells conformally or not. When this option is set to Yes, the prism sides of the two zones will share nodes. This option is only available when stair-stepping is invoked. Note that adjacent regions should have an even ratio of prism layers when using this option.
        TetPrismStairstepExposedQuads : str
            This option can be used when generating a tetrahedral mesh with prism cells and is set to No by default. Selecting Yes for this option will enable stair-stepping for exposed quadrilateral faces (exposed quads) on prism cells. Stair-stepping will prevent pyramids from being created on these exposed quads, which generally would lead to poor quality in the exposed quad location.
        PrismNormalSmoothRelaxationFactor : float
            Specify the smoothness factor for normal prism layers. Increasing this value will generate more prism layers especially near sharp corners. Note that this option is only available when Enable Parallel Meshing for Fluids is turned on and when Stairstep is selected for the Post Improvement Method in the Add Boundary Layers task.
        ShowSubTasks : str

        Returns
        -------
        bool
        """
        class _GenerateTheVolumeMeshFTMCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshQuality = self._MeshQuality(self, "MeshQuality", service, rules, path)
                self.OrthogonalQuality = self._OrthogonalQuality(self, "OrthogonalQuality", service, rules, path)
                self.EnableParallel = self._EnableParallel(self, "EnableParallel", service, rules, path)
                self.SaveVolumeMesh = self._SaveVolumeMesh(self, "SaveVolumeMesh", service, rules, path)
                self.EditVolumeSettings = self._EditVolumeSettings(self, "EditVolumeSettings", service, rules, path)
                self.RegionNameList = self._RegionNameList(self, "RegionNameList", service, rules, path)
                self.RegionVolumeFillList = self._RegionVolumeFillList(self, "RegionVolumeFillList", service, rules, path)
                self.RegionSizeList = self._RegionSizeList(self, "RegionSizeList", service, rules, path)
                self.OldRegionNameList = self._OldRegionNameList(self, "OldRegionNameList", service, rules, path)
                self.OldRegionVolumeFillList = self._OldRegionVolumeFillList(self, "OldRegionVolumeFillList", service, rules, path)
                self.OldRegionSizeList = self._OldRegionSizeList(self, "OldRegionSizeList", service, rules, path)
                self.AllRegionNameList = self._AllRegionNameList(self, "AllRegionNameList", service, rules, path)
                self.AllRegionVolumeFillList = self._AllRegionVolumeFillList(self, "AllRegionVolumeFillList", service, rules, path)
                self.AllRegionSizeList = self._AllRegionSizeList(self, "AllRegionSizeList", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.SpikeRemovalAngle = self._SpikeRemovalAngle(self, "SpikeRemovalAngle", service, rules, path)
                self.DihedralMinAngle = self._DihedralMinAngle(self, "DihedralMinAngle", service, rules, path)
                self.QualityMethod = self._QualityMethod(self, "QualityMethod", service, rules, path)
                self.AvoidHangingNodes = self._AvoidHangingNodes(self, "AvoidHangingNodes", service, rules, path)
                self.OctreePeelLayers = self._OctreePeelLayers(self, "OctreePeelLayers", service, rules, path)
                self.FillWithSizeField = self._FillWithSizeField(self, "FillWithSizeField", service, rules, path)
                self.OctreeBoundaryFaceSizeRatio = self._OctreeBoundaryFaceSizeRatio(self, "OctreeBoundaryFaceSizeRatio", service, rules, path)
                self.GlobalBufferLayers = self._GlobalBufferLayers(self, "GlobalBufferLayers", service, rules, path)
                self.TetPolyGrowthRate = self._TetPolyGrowthRate(self, "TetPolyGrowthRate", service, rules, path)
                self.ConformalPrismSplit = self._ConformalPrismSplit(self, "ConformalPrismSplit", service, rules, path)
                self.TetPrismStairstepExposedQuads = self._TetPrismStairstepExposedQuads(self, "TetPrismStairstepExposedQuads", service, rules, path)
                self.PrismNormalSmoothRelaxationFactor = self._PrismNormalSmoothRelaxationFactor(self, "PrismNormalSmoothRelaxationFactor", service, rules, path)
                self.ShowSubTasks = self._ShowSubTasks(self, "ShowSubTasks", service, rules, path)

            class _MeshQuality(PyNumericalCommandArgumentsSubItem):
                """
                Argument MeshQuality.
                """

            class _OrthogonalQuality(PyNumericalCommandArgumentsSubItem):
                """
                This value sets the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit, and is recommended to be around 0.04.
                """

            class _EnableParallel(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.
                """

            class _SaveVolumeMesh(PyParameterCommandArgumentsSubItem):
                """
                Select this option to save the volume mesh.
                """

            class _EditVolumeSettings(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to review and/or edit the fill settings for your volume region(s).
                """

            class _RegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionVolumeFillList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionVolumeFillList.
                """

            class _RegionSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionSizeList.
                """

            class _OldRegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionVolumeFillList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionVolumeFillList.
                """

            class _OldRegionSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionSizeList.
                """

            class _AllRegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionNameList.
                """

            class _AllRegionVolumeFillList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionVolumeFillList.
                """

            class _AllRegionSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionSizeList.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _SpikeRemovalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument SpikeRemovalAngle.
                """

            class _DihedralMinAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument DihedralMinAngle.
                """

            class _QualityMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose from different types of mesh quality controls (aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows) and Enhanced Orthogonal. For more information, see  More... .
                """

            class _AvoidHangingNodes(PyTextualCommandArgumentsSubItem):
                """
                Specify whether or not you want to avoid any potential 1:8 cell transition in the hexcore or polyhexcore region of the volume mesh, replacing any abrupt change in the cell size with tetrahedral or polyhedral cells.
                """

            class _OctreePeelLayers(PyNumericalCommandArgumentsSubItem):
                """
                Specify the number of octree layers to be removed between the boundary and the core. The resulting cavity will be filled with tet cells for hexcore meshes and with poly cells for polyhexcore meshes.
                """

            class _FillWithSizeField(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to use size fields when generating the volume mesh. Generating the volume mesh using size fields can require additional memory as you increase the number of processing cores. This is because the size field is replicated for each core as the size field is not properly distributed. When using size fields, you are limited by the size of the machine. When not using size fields, however, you require less memory and you can use a higher number of cores with limited RAM, leading to a faster mesh generation.
                """

            class _OctreeBoundaryFaceSizeRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the ratio between the octree face size and the boundary face size. The default is 2.5 such that the octree mesh near the boundary is 2.5 times larger than the boundary mesh.
                """

            class _GlobalBufferLayers(PyNumericalCommandArgumentsSubItem):
                """
                Specify the number of buffer layers for the octree volume mesh. If size controls have not been defined previously, then the default is 2, otherwise the default is calculated based on the maximum growth size.
                """

            class _TetPolyGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum growth rate for tet and poly cells. By default, this corresponds to a growth rate of 1.2.
                """

            class _ConformalPrismSplit(PyTextualCommandArgumentsSubItem):
                """
                Since neighboring zones with different numbers of layers will lead to conformal prism layers between them, use this field to determine whether you want to split the boundary layer cells conformally or not. When this option is set to Yes, the prism sides of the two zones will share nodes. This option is only available when stair-stepping is invoked. Note that adjacent regions should have an even ratio of prism layers when using this option.
                """

            class _TetPrismStairstepExposedQuads(PyTextualCommandArgumentsSubItem):
                """
                This option can be used when generating a tetrahedral mesh with prism cells and is set to No by default. Selecting Yes for this option will enable stair-stepping for exposed quadrilateral faces (exposed quads) on prism cells. Stair-stepping will prevent pyramids from being created on these exposed quads, which generally would lead to poor quality in the exposed quad location.
                """

            class _PrismNormalSmoothRelaxationFactor(PyNumericalCommandArgumentsSubItem):
                """
                Specify the smoothness factor for normal prism layers. Increasing this value will generate more prism layers especially near sharp corners. Note that this option is only available when Enable Parallel Meshing for Fluids is turned on and when Stairstep is selected for the Post Improvement Method in the Add Boundary Layers task.
                """

            class _ShowSubTasks(PyTextualCommandArgumentsSubItem):
                """
                Argument ShowSubTasks.
                """

        def create_instance(self) -> _GenerateTheVolumeMeshFTMCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheVolumeMeshFTMCommandArguments(*args)

    class GenerateTheVolumeMeshWTM(PyCommand):
        """
        Command GenerateTheVolumeMeshWTM.

        Parameters
        ----------
        Solver : str
            Specify the target solver for which you want to generate the volume mesh (Fluent or CFX).
        VolumeFill : str
            Specify the type of cell to be used in the volumetric mesh: polyhedra (default), poly-hexcore, hexcore, or tetrahedral.
        MeshFluidRegions : bool
            Choose whether to mesh the fluid regions in addition to the solid regions. This is enabled by default, and can be enabled along with the Mesh Solid Regions option, however, both options cannot be turned off at the same time.
        MeshSolidRegions : bool
            Choose whether to mesh the solid regions in addition to the fluid regions. This is enabled by default, and can be enabled along with the Mesh Fluid Regions option, however, both options cannot be turned off at the same time.
        SizingMethod : str
            Choose how the cell sizing controls (such as growth rate and the maximum cell length) will be evaluated: either globally or on a region-by-region basis.
        VolumeFillControls : dict[str, Any]
        RegionBasedPreferences : bool
        ReMergeZones : str
            After separating zones during surface meshing, here, choose to re-merge the zones prior to creating the volume mesh.
        ParallelMeshing : bool
            Allows you to employ parallel settings for quicker and more efficient volume meshing. Disable this option if you are interested in only generating the volume mesh in serial mode.
        VolumeMeshPreferences : dict[str, Any]
        PrismPreferences : dict[str, Any]
            Display global settings for your boundary layers. Note that these settings are not applied for Multizone boundary layers
        GlobalThinVolumePreferences : dict[str, Any]
        InvokePrimsControl : str
        OffsetMethodType : str
            Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
        NumberOfLayers : int
            Select the number of boundary layers to be generated.
        FirstAspectRatio : float
            Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
        TransitionRatio : float
            Specify the rate at which adjacent elements grow, for the smooth transition offset method.
        Rate : float
            Specify the rate of growth for the boundary layer.
        FirstHeight : float
            Specify the height of the first layer of cells in the boundary layer.
        MeshObject : str
        MeshDeadRegions : bool
        BodyLabelList : list[str]
        PrismLayers : bool
        QuadTetTransition : str
        MergeCellZones : bool
        FaceScope : dict[str, Any]
        RegionTetNameList : list[str]
        RegionTetMaxCellLengthList : list[str]
        RegionTetGrowthRateList : list[str]
        RegionHexNameList : list[str]
        RegionHexMaxCellLengthList : list[str]
        OldRegionTetMaxCellLengthList : list[str]
        OldRegionTetGrowthRateList : list[str]
        OldRegionHexMaxCellLengthList : list[str]
        CFDSurfaceMeshControls : dict[str, Any]
        ShowSolidFluidMeshed : bool

        Returns
        -------
        bool
        """
        class _GenerateTheVolumeMeshWTMCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Solver = self._Solver(self, "Solver", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.MeshFluidRegions = self._MeshFluidRegions(self, "MeshFluidRegions", service, rules, path)
                self.MeshSolidRegions = self._MeshSolidRegions(self, "MeshSolidRegions", service, rules, path)
                self.SizingMethod = self._SizingMethod(self, "SizingMethod", service, rules, path)
                self.VolumeFillControls = self._VolumeFillControls(self, "VolumeFillControls", service, rules, path)
                self.RegionBasedPreferences = self._RegionBasedPreferences(self, "RegionBasedPreferences", service, rules, path)
                self.ReMergeZones = self._ReMergeZones(self, "ReMergeZones", service, rules, path)
                self.ParallelMeshing = self._ParallelMeshing(self, "ParallelMeshing", service, rules, path)
                self.VolumeMeshPreferences = self._VolumeMeshPreferences(self, "VolumeMeshPreferences", service, rules, path)
                self.PrismPreferences = self._PrismPreferences(self, "PrismPreferences", service, rules, path)
                self.GlobalThinVolumePreferences = self._GlobalThinVolumePreferences(self, "GlobalThinVolumePreferences", service, rules, path)
                self.InvokePrimsControl = self._InvokePrimsControl(self, "InvokePrimsControl", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.FirstAspectRatio = self._FirstAspectRatio(self, "FirstAspectRatio", service, rules, path)
                self.TransitionRatio = self._TransitionRatio(self, "TransitionRatio", service, rules, path)
                self.Rate = self._Rate(self, "Rate", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.MeshDeadRegions = self._MeshDeadRegions(self, "MeshDeadRegions", service, rules, path)
                self.BodyLabelList = self._BodyLabelList(self, "BodyLabelList", service, rules, path)
                self.PrismLayers = self._PrismLayers(self, "PrismLayers", service, rules, path)
                self.QuadTetTransition = self._QuadTetTransition(self, "QuadTetTransition", service, rules, path)
                self.MergeCellZones = self._MergeCellZones(self, "MergeCellZones", service, rules, path)
                self.FaceScope = self._FaceScope(self, "FaceScope", service, rules, path)
                self.RegionTetNameList = self._RegionTetNameList(self, "RegionTetNameList", service, rules, path)
                self.RegionTetMaxCellLengthList = self._RegionTetMaxCellLengthList(self, "RegionTetMaxCellLengthList", service, rules, path)
                self.RegionTetGrowthRateList = self._RegionTetGrowthRateList(self, "RegionTetGrowthRateList", service, rules, path)
                self.RegionHexNameList = self._RegionHexNameList(self, "RegionHexNameList", service, rules, path)
                self.RegionHexMaxCellLengthList = self._RegionHexMaxCellLengthList(self, "RegionHexMaxCellLengthList", service, rules, path)
                self.OldRegionTetMaxCellLengthList = self._OldRegionTetMaxCellLengthList(self, "OldRegionTetMaxCellLengthList", service, rules, path)
                self.OldRegionTetGrowthRateList = self._OldRegionTetGrowthRateList(self, "OldRegionTetGrowthRateList", service, rules, path)
                self.OldRegionHexMaxCellLengthList = self._OldRegionHexMaxCellLengthList(self, "OldRegionHexMaxCellLengthList", service, rules, path)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.ShowSolidFluidMeshed = self._ShowSolidFluidMeshed(self, "ShowSolidFluidMeshed", service, rules, path)

            class _Solver(PyTextualCommandArgumentsSubItem):
                """
                Specify the target solver for which you want to generate the volume mesh (Fluent or CFX).
                """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Specify the type of cell to be used in the volumetric mesh: polyhedra (default), poly-hexcore, hexcore, or tetrahedral.
                """

            class _MeshFluidRegions(PyParameterCommandArgumentsSubItem):
                """
                Choose whether to mesh the fluid regions in addition to the solid regions. This is enabled by default, and can be enabled along with the Mesh Solid Regions option, however, both options cannot be turned off at the same time.
                """

            class _MeshSolidRegions(PyParameterCommandArgumentsSubItem):
                """
                Choose whether to mesh the solid regions in addition to the fluid regions. This is enabled by default, and can be enabled along with the Mesh Fluid Regions option, however, both options cannot be turned off at the same time.
                """

            class _SizingMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose how the cell sizing controls (such as growth rate and the maximum cell length) will be evaluated: either globally or on a region-by-region basis.
                """

            class _VolumeFillControls(PySingletonCommandArgumentsSubItem):
                """
                Argument VolumeFillControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.PeelLayers = self._PeelLayers(self, "PeelLayers", service, rules, path)
                    self.TetPolyMaxCellLength = self._TetPolyMaxCellLength(self, "TetPolyMaxCellLength", service, rules, path)
                    self.HexMinCellLength = self._HexMinCellLength(self, "HexMinCellLength", service, rules, path)
                    self.Type = self._Type(self, "Type", service, rules, path)
                    self.CellSizing = self._CellSizing(self, "CellSizing", service, rules, path)
                    self.HexMaxSize = self._HexMaxSize(self, "HexMaxSize", service, rules, path)
                    self.HexMaxCellLength = self._HexMaxCellLength(self, "HexMaxCellLength", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.BufferLayers = self._BufferLayers(self, "BufferLayers", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _PeelLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PeelLayers.
                    """

                class _TetPolyMaxCellLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument TetPolyMaxCellLength.
                    """

                class _HexMinCellLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HexMinCellLength.
                    """

                class _Type(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Type.
                    """

                class _CellSizing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CellSizing.
                    """

                class _HexMaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HexMaxSize.
                    """

                class _HexMaxCellLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HexMaxCellLength.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _BufferLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BufferLayers.
                    """

            class _RegionBasedPreferences(PyParameterCommandArgumentsSubItem):
                """
                Argument RegionBasedPreferences.
                """

            class _ReMergeZones(PyTextualCommandArgumentsSubItem):
                """
                After separating zones during surface meshing, here, choose to re-merge the zones prior to creating the volume mesh.
                """

            class _ParallelMeshing(PyParameterCommandArgumentsSubItem):
                """
                Allows you to employ parallel settings for quicker and more efficient volume meshing. Disable this option if you are interested in only generating the volume mesh in serial mode.
                """

            class _VolumeMeshPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument VolumeMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.UseSizeField = self._UseSizeField(self, "UseSizeField", service, rules, path)
                    self.PolyFeatureAngle = self._PolyFeatureAngle(self, "PolyFeatureAngle", service, rules, path)
                    self.MinPolySize = self._MinPolySize(self, "MinPolySize", service, rules, path)
                    self.UseSizeFieldInSolids = self._UseSizeFieldInSolids(self, "UseSizeFieldInSolids", service, rules, path)
                    self.MergeBodyLabels = self._MergeBodyLabels(self, "MergeBodyLabels", service, rules, path)
                    self.QualityMethod = self._QualityMethod(self, "QualityMethod", service, rules, path)
                    self.PolyInSolids = self._PolyInSolids(self, "PolyInSolids", service, rules, path)
                    self.MinEdgeLength = self._MinEdgeLength(self, "MinEdgeLength", service, rules, path)
                    self.AddMultipleQualityMethods = self._AddMultipleQualityMethods(self, "AddMultipleQualityMethods", service, rules, path)
                    self.MaxCellSizeChange = self._MaxCellSizeChange(self, "MaxCellSizeChange", service, rules, path)
                    self.WritePrismControlFile = self._WritePrismControlFile(self, "WritePrismControlFile", service, rules, path)
                    self.PrepareZoneNames = self._PrepareZoneNames(self, "PrepareZoneNames", service, rules, path)
                    self.CheckSelfProximity = self._CheckSelfProximity(self, "CheckSelfProximity", service, rules, path)
                    self.Avoid1_8Transition = self._Avoid1_8Transition(self, "Avoid1_8Transition", service, rules, path)
                    self.MinFaceArea = self._MinFaceArea(self, "MinFaceArea", service, rules, path)
                    self.ShowVolumeMeshPreferences = self._ShowVolumeMeshPreferences(self, "ShowVolumeMeshPreferences", service, rules, path)
                    self.SolidGrowthRate = self._SolidGrowthRate(self, "SolidGrowthRate", service, rules, path)
                    self.QualityWarningLimit = self._QualityWarningLimit(self, "QualityWarningLimit", service, rules, path)

                class _UseSizeField(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeField.
                    """

                class _PolyFeatureAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PolyFeatureAngle.
                    """

                class _MinPolySize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinPolySize.
                    """

                class _UseSizeFieldInSolids(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeFieldInSolids.
                    """

                class _MergeBodyLabels(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MergeBodyLabels.
                    """

                class _QualityMethod(PyTextualCommandArgumentsSubItem):
                    """
                    Argument QualityMethod.
                    """

                class _PolyInSolids(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PolyInSolids.
                    """

                class _MinEdgeLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinEdgeLength.
                    """

                class _AddMultipleQualityMethods(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AddMultipleQualityMethods.
                    """

                class _MaxCellSizeChange(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxCellSizeChange.
                    """

                class _WritePrismControlFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument WritePrismControlFile.
                    """

                class _PrepareZoneNames(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PrepareZoneNames.
                    """

                class _CheckSelfProximity(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CheckSelfProximity.
                    """

                class _Avoid1_8Transition(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Avoid1_8Transition.
                    """

                class _MinFaceArea(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinFaceArea.
                    """

                class _ShowVolumeMeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowVolumeMeshPreferences.
                    """

                class _SolidGrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SolidGrowthRate.
                    """

                class _QualityWarningLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument QualityWarningLimit.
                    """

            class _PrismPreferences(PySingletonCommandArgumentsSubItem):
                """
                Display global settings for your boundary layers. Note that these settings are not applied for Multizone boundary layers
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.PrismKeepFirstLayer = self._PrismKeepFirstLayer(self, "PrismKeepFirstLayer", service, rules, path)
                    self.PrismMaxAspectRatio = self._PrismMaxAspectRatio(self, "PrismMaxAspectRatio", service, rules, path)
                    self.PrismStairStepOptions = self._PrismStairStepOptions(self, "PrismStairStepOptions", service, rules, path)
                    self.PrismGapFactor = self._PrismGapFactor(self, "PrismGapFactor", service, rules, path)
                    self.IgnoreInflation = self._IgnoreInflation(self, "IgnoreInflation", service, rules, path)
                    self.MergeBoundaryLayers = self._MergeBoundaryLayers(self, "MergeBoundaryLayers", service, rules, path)
                    self.ShowPrismPreferences = self._ShowPrismPreferences(self, "ShowPrismPreferences", service, rules, path)
                    self.NormalSmoothRelaxationFactor = self._NormalSmoothRelaxationFactor(self, "NormalSmoothRelaxationFactor", service, rules, path)
                    self.StairstepExposedQuads = self._StairstepExposedQuads(self, "StairstepExposedQuads", service, rules, path)
                    self.PrismMinAspectRatio = self._PrismMinAspectRatio(self, "PrismMinAspectRatio", service, rules, path)
                    self.PrismAdjacentAngle = self._PrismAdjacentAngle(self, "PrismAdjacentAngle", service, rules, path)

                class _PrismKeepFirstLayer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PrismKeepFirstLayer.
                    """

                class _PrismMaxAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PrismMaxAspectRatio.
                    """

                class _PrismStairStepOptions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PrismStairStepOptions.
                    """

                class _PrismGapFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PrismGapFactor.
                    """

                class _IgnoreInflation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IgnoreInflation.
                    """

                class _MergeBoundaryLayers(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MergeBoundaryLayers.
                    """

                class _ShowPrismPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowPrismPreferences.
                    """

                class _NormalSmoothRelaxationFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NormalSmoothRelaxationFactor.
                    """

                class _StairstepExposedQuads(PyTextualCommandArgumentsSubItem):
                    """
                    Argument StairstepExposedQuads.
                    """

                class _PrismMinAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PrismMinAspectRatio.
                    """

                class _PrismAdjacentAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PrismAdjacentAngle.
                    """

            class _GlobalThinVolumePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument GlobalThinVolumePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowGlobalThinVolumePreferences = self._ShowGlobalThinVolumePreferences(self, "ShowGlobalThinVolumePreferences", service, rules, path)
                    self.AutoOrderControls = self._AutoOrderControls(self, "AutoOrderControls", service, rules, path)
                    self.StairStep = self._StairStep(self, "StairStep", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)

                class _ShowGlobalThinVolumePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowGlobalThinVolumePreferences.
                    """

                class _AutoOrderControls(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoOrderControls.
                    """

                class _StairStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument StairStep.
                    """

                class _MinAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinAspectRatio.
                    """

            class _InvokePrimsControl(PyTextualCommandArgumentsSubItem):
                """
                Argument InvokePrimsControl.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
                """

            class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                """
                Select the number of boundary layers to be generated.
                """

            class _FirstAspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
                """

            class _TransitionRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the rate at which adjacent elements grow, for the smooth transition offset method.
                """

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the rate of growth for the boundary layer.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _MeshDeadRegions(PyParameterCommandArgumentsSubItem):
                """
                Argument MeshDeadRegions.
                """

            class _BodyLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BodyLabelList.
                """

            class _PrismLayers(PyParameterCommandArgumentsSubItem):
                """
                Argument PrismLayers.
                """

            class _QuadTetTransition(PyTextualCommandArgumentsSubItem):
                """
                Argument QuadTetTransition.
                """

            class _MergeCellZones(PyParameterCommandArgumentsSubItem):
                """
                Argument MergeCellZones.
                """

            class _FaceScope(PySingletonCommandArgumentsSubItem):
                """
                Argument FaceScope.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                    self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                    self.FaceScopeMeshObject = self._FaceScopeMeshObject(self, "FaceScopeMeshObject", service, rules, path)
                    self.RegionsType = self._RegionsType(self, "RegionsType", service, rules, path)

                class _TopologyList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument TopologyList.
                    """

                class _GrowOn(PyTextualCommandArgumentsSubItem):
                    """
                    Argument GrowOn.
                    """

                class _FaceScopeMeshObject(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FaceScopeMeshObject.
                    """

                class _RegionsType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RegionsType.
                    """

            class _RegionTetNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionTetNameList.
                """

            class _RegionTetMaxCellLengthList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionTetMaxCellLengthList.
                """

            class _RegionTetGrowthRateList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionTetGrowthRateList.
                """

            class _RegionHexNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionHexNameList.
                """

            class _RegionHexMaxCellLengthList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionHexMaxCellLengthList.
                """

            class _OldRegionTetMaxCellLengthList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionTetMaxCellLengthList.
                """

            class _OldRegionTetGrowthRateList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionTetGrowthRateList.
                """

            class _OldRegionHexMaxCellLengthList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionHexMaxCellLengthList.
                """

            class _CFDSurfaceMeshControls(PySingletonCommandArgumentsSubItem):
                """
                Argument CFDSurfaceMeshControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SaveSizeFieldFile = self._SaveSizeFieldFile(self, "SaveSizeFieldFile", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.PreviewSizefield = self._PreviewSizefield(self, "PreviewSizefield", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.SaveSizeField = self._SaveSizeField(self, "SaveSizeField", service, rules, path)
                    self.UseSizeFiles = self._UseSizeFiles(self, "UseSizeFiles", service, rules, path)
                    self.AutoCreateScopedSizing = self._AutoCreateScopedSizing(self, "AutoCreateScopedSizing", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyParameterCommandArgumentsSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _ShowSolidFluidMeshed(PyParameterCommandArgumentsSubItem):
                """
                Argument ShowSolidFluidMeshed.
                """

        def create_instance(self) -> _GenerateTheVolumeMeshWTMCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheVolumeMeshWTMCommandArguments(*args)

    class GeometrySetup(PyCommand):
        """
        Command GeometrySetup.

        Parameters
        ----------
        SetupType : str
            Choose whether your geometry represents only a solid body, only a fluid body, or both a solid and fluid body.
        CappingRequired : str
            Choose whether or not you are going to perform any capping operations, thereby enclosing a fluid region.
        WallToInternal : str
            Choose whether or not to change interior fluid-fluid boundaries from type "wall" to "internal". Only internal boundaries bounded by two fluid regions are converted into internal zone types. If new fluid regions are assigned, this task is executed after the Update Regions task. Internal boundaries that are designated as "baffles" are retained as walls.
        InvokeShareTopology : str
            For CAD assemblies with multiple parts, choose whether or not to identify and close any problematic gaps and whether to join and/or intersect problematic faces. This will add an Apply Share Topology task to your workflow. Note that in situations where you want to use overlapping non-conformal interfaces, you must use the non-conformal option. In all other situations, such as when you have totally disconnected bodies (that is, with no overlap), you should instead elect to choose the Share Topology option even if there is nothing to share.
        NonConformal : str
            Determine whether or not you want to create non-conformal meshes between the objects in your geometry. Note that in situations where you want to use overlapping non-conformal interfaces, you must use the non-conformal option. In all other situations, such as when you have totally disconnected bodies (that is, with no overlap), you should instead elect to choose the Share Topology option even if there is nothing to share.
        Multizone : str
            Determine whether or not you want to perform multi-zone meshing on your geometry. Selecting Yes will add an Add Multizone Controls task and a Generate Multizone Mesh task to your workflow.
        SetupInternals : list[str]
        SetupInternalTypes : list[str]
        OldZoneList : list[str]
        OldZoneTypeList : list[str]
        RegionList : list[str]
        EdgeZoneList : list[str]
        EdgeLabels : list[str]
        Duplicates : bool
        SMImprovePreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _GeometrySetupCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.SetupType = self._SetupType(self, "SetupType", service, rules, path)
                self.CappingRequired = self._CappingRequired(self, "CappingRequired", service, rules, path)
                self.WallToInternal = self._WallToInternal(self, "WallToInternal", service, rules, path)
                self.InvokeShareTopology = self._InvokeShareTopology(self, "InvokeShareTopology", service, rules, path)
                self.NonConformal = self._NonConformal(self, "NonConformal", service, rules, path)
                self.Multizone = self._Multizone(self, "Multizone", service, rules, path)
                self.SetupInternals = self._SetupInternals(self, "SetupInternals", service, rules, path)
                self.SetupInternalTypes = self._SetupInternalTypes(self, "SetupInternalTypes", service, rules, path)
                self.OldZoneList = self._OldZoneList(self, "OldZoneList", service, rules, path)
                self.OldZoneTypeList = self._OldZoneTypeList(self, "OldZoneTypeList", service, rules, path)
                self.RegionList = self._RegionList(self, "RegionList", service, rules, path)
                self.EdgeZoneList = self._EdgeZoneList(self, "EdgeZoneList", service, rules, path)
                self.EdgeLabels = self._EdgeLabels(self, "EdgeLabels", service, rules, path)
                self.Duplicates = self._Duplicates(self, "Duplicates", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)

            class _SetupType(PyTextualCommandArgumentsSubItem):
                """
                Choose whether your geometry represents only a solid body, only a fluid body, or both a solid and fluid body.
                """

            class _CappingRequired(PyTextualCommandArgumentsSubItem):
                """
                Choose whether or not you are going to perform any capping operations, thereby enclosing a fluid region.
                """

            class _WallToInternal(PyTextualCommandArgumentsSubItem):
                """
                Choose whether or not to change interior fluid-fluid boundaries from type "wall" to "internal". Only internal boundaries bounded by two fluid regions are converted into internal zone types. If new fluid regions are assigned, this task is executed after the Update Regions task. Internal boundaries that are designated as "baffles" are retained as walls.
                """

            class _InvokeShareTopology(PyTextualCommandArgumentsSubItem):
                """
                For CAD assemblies with multiple parts, choose whether or not to identify and close any problematic gaps and whether to join and/or intersect problematic faces. This will add an Apply Share Topology task to your workflow. Note that in situations where you want to use overlapping non-conformal interfaces, you must use the non-conformal option. In all other situations, such as when you have totally disconnected bodies (that is, with no overlap), you should instead elect to choose the Share Topology option even if there is nothing to share.
                """

            class _NonConformal(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to create non-conformal meshes between the objects in your geometry. Note that in situations where you want to use overlapping non-conformal interfaces, you must use the non-conformal option. In all other situations, such as when you have totally disconnected bodies (that is, with no overlap), you should instead elect to choose the Share Topology option even if there is nothing to share.
                """

            class _Multizone(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to perform multi-zone meshing on your geometry. Selecting Yes will add an Add Multizone Controls task and a Generate Multizone Mesh task to your workflow.
                """

            class _SetupInternals(PyTextualCommandArgumentsSubItem):
                """
                Argument SetupInternals.
                """

            class _SetupInternalTypes(PyTextualCommandArgumentsSubItem):
                """
                Argument SetupInternalTypes.
                """

            class _OldZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldZoneList.
                """

            class _OldZoneTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldZoneTypeList.
                """

            class _RegionList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionList.
                """

            class _EdgeZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeZoneList.
                """

            class _EdgeLabels(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabels.
                """

            class _Duplicates(PyParameterCommandArgumentsSubItem):
                """
                Argument Duplicates.
                """

            class _SMImprovePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument SMImprovePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SIStepQualityLimit = self._SIStepQualityLimit(self, "SIStepQualityLimit", service, rules, path)
                    self.SIQualityCollapseLimit = self._SIQualityCollapseLimit(self, "SIQualityCollapseLimit", service, rules, path)
                    self.SIQualityIterations = self._SIQualityIterations(self, "SIQualityIterations", service, rules, path)
                    self.SIQualityMaxAngle = self._SIQualityMaxAngle(self, "SIQualityMaxAngle", service, rules, path)
                    self.AllowDefeaturing = self._AllowDefeaturing(self, "AllowDefeaturing", service, rules, path)
                    self.ShowSMImprovePreferences = self._ShowSMImprovePreferences(self, "ShowSMImprovePreferences", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.SIStepWidth = self._SIStepWidth(self, "SIStepWidth", service, rules, path)
                    self.SIRemoveStep = self._SIRemoveStep(self, "SIRemoveStep", service, rules, path)

                class _SIStepQualityLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepQualityLimit.
                    """

                class _SIQualityCollapseLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityCollapseLimit.
                    """

                class _SIQualityIterations(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityIterations.
                    """

                class _SIQualityMaxAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityMaxAngle.
                    """

                class _AllowDefeaturing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _ShowSMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _AdvancedImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _SIStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepWidth.
                    """

                class _SIRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SIRemoveStep.
                    """

        def create_instance(self) -> _GeometrySetupCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GeometrySetupCommandArguments(*args)

    class IdentifyConstructionSurfaces(PyCommand):
        """
        Command IdentifyConstructionSurfaces.

        Parameters
        ----------
        MRFName : str
            Specify a name for the construction surface or use the default value.
        CreationMethod : str
            Choose whether to create the construction surface using an Existing object or zone, a bounding Box, or by using an Offset Surface.
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ObjectSelectionSingle : list[str]
            Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionSingle : list[str]
            Choose a single zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LabelSelectionSingle : list[str]
            Choose a single label from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        DefeaturingSize : float
            Specify a value that is used to obtain a rough shape of the selected object(s). The larger the value, the more approximate the shape.
        OffsetHeight : float
            Specify the height of the offset construction surface. This is how far from the selected object(s) the rough shape is offset.
        Pivot : dict[str, Any]
        Axis : dict[str, Any]
        Rotation : dict[str, Any]
        CylinderObject : dict[str, Any]
        CylinderMethod : str
        BoundingBoxObject : dict[str, Any]
            View the extents of the bounding box.

        Returns
        -------
        bool
        """
        class _IdentifyConstructionSurfacesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MRFName = self._MRFName(self, "MRFName", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ObjectSelectionSingle = self._ObjectSelectionSingle(self, "ObjectSelectionSingle", service, rules, path)
                self.ZoneSelectionSingle = self._ZoneSelectionSingle(self, "ZoneSelectionSingle", service, rules, path)
                self.LabelSelectionSingle = self._LabelSelectionSingle(self, "LabelSelectionSingle", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.DefeaturingSize = self._DefeaturingSize(self, "DefeaturingSize", service, rules, path)
                self.OffsetHeight = self._OffsetHeight(self, "OffsetHeight", service, rules, path)
                self.Pivot = self._Pivot(self, "Pivot", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.Rotation = self._Rotation(self, "Rotation", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)

            class _MRFName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the construction surface or use the default value.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose whether to create the construction surface using an Existing object or zone, a bounding Box, or by using an Offset Surface.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Choose a single label from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _DefeaturingSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value that is used to obtain a rough shape of the selected object(s). The larger the value, the more approximate the shape.
                """

            class _OffsetHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify the height of the offset construction surface. This is how far from the selected object(s) the rough shape is offset.
                """

            class _Pivot(PySingletonCommandArgumentsSubItem):
                """
                Argument Pivot.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _Z(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z.
                    """

                class _Y(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y.
                    """

            class _Axis(PySingletonCommandArgumentsSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _Rotation(PySingletonCommandArgumentsSubItem):
                """
                Argument Rotation.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _X_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _CylinderObject(PySingletonCommandArgumentsSubItem):
                """
                Argument CylinderObject.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X_Offset = self._X_Offset(self, "X-Offset", service, rules, path)
                    self.HeightNode = self._HeightNode(self, "HeightNode", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.X1 = self._X1(self, "X1", service, rules, path)
                    self.Y1 = self._Y1(self, "Y1", service, rules, path)
                    self.Z_Offset = self._Z_Offset(self, "Z-Offset", service, rules, path)
                    self.Z2 = self._Z2(self, "Z2", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Z1 = self._Z1(self, "Z1", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Y2 = self._Y2(self, "Y2", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _X_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
                    """

                class _Y_Offset(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _X2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X2.
                    """

                class _Node2(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node2.
                    """

                class _HeightFrontInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius1.
                    """

            class _CylinderMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CylinderMethod.
                """

            class _BoundingBoxObject(PySingletonCommandArgumentsSubItem):
                """
                View the extents of the bounding box.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SizeRelativeLength = self._SizeRelativeLength(self, "SizeRelativeLength", service, rules, path)
                    self.Xmax = self._Xmax(self, "Xmax", service, rules, path)
                    self.XminRatio = self._XminRatio(self, "XminRatio", service, rules, path)
                    self.YminRatio = self._YminRatio(self, "YminRatio", service, rules, path)
                    self.Zmin = self._Zmin(self, "Zmin", service, rules, path)
                    self.Zmax = self._Zmax(self, "Zmax", service, rules, path)
                    self.Ymax = self._Ymax(self, "Ymax", service, rules, path)
                    self.ZminRatio = self._ZminRatio(self, "ZminRatio", service, rules, path)
                    self.Ymin = self._Ymin(self, "Ymin", service, rules, path)
                    self.Xmin = self._Xmin(self, "Xmin", service, rules, path)
                    self.YmaxRatio = self._YmaxRatio(self, "YmaxRatio", service, rules, path)
                    self.ZmaxRatio = self._ZmaxRatio(self, "ZmaxRatio", service, rules, path)
                    self.XmaxRatio = self._XmaxRatio(self, "XmaxRatio", service, rules, path)

                class _SizeRelativeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _Xmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmax.
                    """

                class _XminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _XmaxRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument XmaxRatio.
                    """

        def create_instance(self) -> _IdentifyConstructionSurfacesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyConstructionSurfacesCommandArguments(*args)

    class IdentifyDeviatedFaces(PyCommand):
        """
        Command IdentifyDeviatedFaces.

        Parameters
        ----------
        DisplayGridName : str
            Enter a name for the identified deviated faces.
        SelectionType : str
            Specify whether the identification of deviated faces is to be applied to an indicated object or zone.
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        AdvancedOptions : bool
            Enable this option to automatically calculate the minimum and maximum deviation for the selected object(s) or zone(s).
        DeviationMinValue : float
            When Auto Compute is disabled, specify a minimum value for the deviation.
        DeviationMaxValue : float
            When Auto Compute is disabled, specify a maximum value for the deviation.
        Overlay : str
            Determine how you want the deviated faces to be displayed (either with the mesh or with the geometry).
        IncludeGapCoverGeometry : str
            Determine if you want to include any gap covers in the check for deviated faces. If so, the default minimum and maximum deviation range is automatically calculated.

        Returns
        -------
        bool
        """
        class _IdentifyDeviatedFacesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.DisplayGridName = self._DisplayGridName(self, "DisplayGridName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.DeviationMinValue = self._DeviationMinValue(self, "DeviationMinValue", service, rules, path)
                self.DeviationMaxValue = self._DeviationMaxValue(self, "DeviationMaxValue", service, rules, path)
                self.Overlay = self._Overlay(self, "Overlay", service, rules, path)
                self.IncludeGapCoverGeometry = self._IncludeGapCoverGeometry(self, "IncludeGapCoverGeometry", service, rules, path)

            class _DisplayGridName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the identified deviated faces.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Specify whether the identification of deviated faces is to be applied to an indicated object or zone.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to automatically calculate the minimum and maximum deviation for the selected object(s) or zone(s).
                """

            class _DeviationMinValue(PyNumericalCommandArgumentsSubItem):
                """
                When Auto Compute is disabled, specify a minimum value for the deviation.
                """

            class _DeviationMaxValue(PyNumericalCommandArgumentsSubItem):
                """
                When Auto Compute is disabled, specify a maximum value for the deviation.
                """

            class _Overlay(PyTextualCommandArgumentsSubItem):
                """
                Determine how you want the deviated faces to be displayed (either with the mesh or with the geometry).
                """

            class _IncludeGapCoverGeometry(PyTextualCommandArgumentsSubItem):
                """
                Determine if you want to include any gap covers in the check for deviated faces. If so, the default minimum and maximum deviation range is automatically calculated.
                """

        def create_instance(self) -> _IdentifyDeviatedFacesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyDeviatedFacesCommandArguments(*args)

    class IdentifyOrphans(PyCommand):
        """
        Command IdentifyOrphans.

        Parameters
        ----------
        NumberOfOrphans : str
            Specify the allowable number of orphans to accept in your mesh.
        ObjectSelectionList : list[str]
            Select one or more mesh objects that you would like to identify any potential orphan faces. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        EnableGridPriority : bool
            Controls the ability to prioritize your overset grids (meshes). The priorities of the overset mesh are then carried over into the solver.
        DonorPriorityMethod : str
            Determines the location of the overset mesh. Choose how the mesh donor cells are prioritized - either based on the cell size (proportional to the inverse of the cell volume) or based on the boundary distance (proportional to the inverse of the distance to the closest boundary).
        OverlapBoundaries : str
            Determine if you need to account for any overlapping boundaries that may be present in your overset mesh (due to overlapping geometry and boundaries or those sometimes generated by collar meshes). You can improve the overset performance by setting this option to no.
        CheckOversetInterfaceIntersection : str
            Enabled by default, Fluent checks for any overset interface intersections while identifying orphans. Disable this option to skip the intersection check and increase the speed of identifying orphans.
        RegionNameList : list[str]
        RegionSizeList : list[str]
        OldRegionNameList : list[str]
        OldRegionSizeList : list[str]

        Returns
        -------
        bool
        """
        class _IdentifyOrphansCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.NumberOfOrphans = self._NumberOfOrphans(self, "NumberOfOrphans", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.EnableGridPriority = self._EnableGridPriority(self, "EnableGridPriority", service, rules, path)
                self.DonorPriorityMethod = self._DonorPriorityMethod(self, "DonorPriorityMethod", service, rules, path)
                self.OverlapBoundaries = self._OverlapBoundaries(self, "OverlapBoundaries", service, rules, path)
                self.CheckOversetInterfaceIntersection = self._CheckOversetInterfaceIntersection(self, "CheckOversetInterfaceIntersection", service, rules, path)
                self.RegionNameList = self._RegionNameList(self, "RegionNameList", service, rules, path)
                self.RegionSizeList = self._RegionSizeList(self, "RegionSizeList", service, rules, path)
                self.OldRegionNameList = self._OldRegionNameList(self, "OldRegionNameList", service, rules, path)
                self.OldRegionSizeList = self._OldRegionSizeList(self, "OldRegionSizeList", service, rules, path)

            class _NumberOfOrphans(PyTextualCommandArgumentsSubItem):
                """
                Specify the allowable number of orphans to accept in your mesh.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more mesh objects that you would like to identify any potential orphan faces. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _EnableGridPriority(PyParameterCommandArgumentsSubItem):
                """
                Controls the ability to prioritize your overset grids (meshes). The priorities of the overset mesh are then carried over into the solver.
                """

            class _DonorPriorityMethod(PyTextualCommandArgumentsSubItem):
                """
                Determines the location of the overset mesh. Choose how the mesh donor cells are prioritized - either based on the cell size (proportional to the inverse of the cell volume) or based on the boundary distance (proportional to the inverse of the distance to the closest boundary).
                """

            class _OverlapBoundaries(PyTextualCommandArgumentsSubItem):
                """
                Determine if you need to account for any overlapping boundaries that may be present in your overset mesh (due to overlapping geometry and boundaries or those sometimes generated by collar meshes). You can improve the overset performance by setting this option to no.
                """

            class _CheckOversetInterfaceIntersection(PyTextualCommandArgumentsSubItem):
                """
                Enabled by default, Fluent checks for any overset interface intersections while identifying orphans. Disable this option to skip the intersection check and increase the speed of identifying orphans.
                """

            class _RegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionSizeList.
                """

            class _OldRegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionSizeList.
                """

        def create_instance(self) -> _IdentifyOrphansCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyOrphansCommandArguments(*args)

    class IdentifyRegions(PyCommand):
        """
        Command IdentifyRegions.

        Parameters
        ----------
        AddChild : str
            Determine whether or not you want to specify any fluid or void regions using this task.
        MaterialPointsName : str
            Specify a name for the region that you want to identify or use the default value.
        MptMethodType : str
            Choose how you want to identify the region: using a distinct numerical input of X, Y, and Z coordinates, using the centroid of the selected object, or by using an offset distance relative to the centroid of selected object/zone.
        NewRegionType : str
            Specify the type of region as being fluid, solid, or a void.
        LinkConstruction : str
            Keep the default value of no for most cases involving a singular fluid region. If you mean to identify an additional fluid region, choose yes to indicate that the current fluid region is either inside or adjacent to a construction surface(s), in order to properly mesh this fluid region accordingly (that is, using a surface mesh).
        SelectionType : str
            Choose how you want to make your selection (by object, label, or zone name).
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ObjectSelectionList : list[str]
            Choose one or more objects (or voids) from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        GraphicalSelection : bool
            Enable this option and select a point in the graphics window to be the center of the region.
        ShowCoordinates : bool
            Enable this option when providing numerical inputs for the region location, and you want to view the exact coordinates.
        X : float
            The x-coordinate of the center of the region.
        Y : float
            The y-coordinate of the center of the region.
        Z : float
            The z-coordinate of the center of the region.
        OffsetX : float
            The x-coordinate of the offset distance relative to the centroid of the selected object/zone.
        OffsetY : float
            The y-coordinate of the offset distance relative to the centroid of the selected object/zone.
        OffsetZ : float
            The z-coordinate of the offset distance relative to the centroid of the selected object/zone.

        Returns
        -------
        bool
        """
        class _IdentifyRegionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.MaterialPointsName = self._MaterialPointsName(self, "MaterialPointsName", service, rules, path)
                self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                self.NewRegionType = self._NewRegionType(self, "NewRegionType", service, rules, path)
                self.LinkConstruction = self._LinkConstruction(self, "LinkConstruction", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.GraphicalSelection = self._GraphicalSelection(self, "GraphicalSelection", service, rules, path)
                self.ShowCoordinates = self._ShowCoordinates(self, "ShowCoordinates", service, rules, path)
                self.X = self._X(self, "X", service, rules, path)
                self.Y = self._Y(self, "Y", service, rules, path)
                self.Z = self._Z(self, "Z", service, rules, path)
                self.OffsetX = self._OffsetX(self, "OffsetX", service, rules, path)
                self.OffsetY = self._OffsetY(self, "OffsetY", service, rules, path)
                self.OffsetZ = self._OffsetZ(self, "OffsetZ", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to specify any fluid or void regions using this task.
                """

            class _MaterialPointsName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the region that you want to identify or use the default value.
                """

            class _MptMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to identify the region: using a distinct numerical input of X, Y, and Z coordinates, using the centroid of the selected object, or by using an offset distance relative to the centroid of selected object/zone.
                """

            class _NewRegionType(PyTextualCommandArgumentsSubItem):
                """
                Specify the type of region as being fluid, solid, or a void.
                """

            class _LinkConstruction(PyTextualCommandArgumentsSubItem):
                """
                Keep the default value of no for most cases involving a singular fluid region. If you mean to identify an additional fluid region, choose yes to indicate that the current fluid region is either inside or adjacent to a construction surface(s), in order to properly mesh this fluid region accordingly (that is, using a surface mesh).
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects (or voids) from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GraphicalSelection(PyParameterCommandArgumentsSubItem):
                """
                Enable this option and select a point in the graphics window to be the center of the region.
                """

            class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                """
                Enable this option when providing numerical inputs for the region location, and you want to view the exact coordinates.
                """

            class _X(PyNumericalCommandArgumentsSubItem):
                """
                The x-coordinate of the center of the region.
                """

            class _Y(PyNumericalCommandArgumentsSubItem):
                """
                The y-coordinate of the center of the region.
                """

            class _Z(PyNumericalCommandArgumentsSubItem):
                """
                The z-coordinate of the center of the region.
                """

            class _OffsetX(PyNumericalCommandArgumentsSubItem):
                """
                The x-coordinate of the offset distance relative to the centroid of the selected object/zone.
                """

            class _OffsetY(PyNumericalCommandArgumentsSubItem):
                """
                The y-coordinate of the offset distance relative to the centroid of the selected object/zone.
                """

            class _OffsetZ(PyNumericalCommandArgumentsSubItem):
                """
                The z-coordinate of the offset distance relative to the centroid of the selected object/zone.
                """

        def create_instance(self) -> _IdentifyRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyRegionsCommandArguments(*args)

    class ImportBodyOfInfluenceGeometry(PyCommand):
        """
        Command ImportBodyOfInfluenceGeometry.

        Parameters
        ----------
        Type : str
            Specify whether you are importing CAD geometry file(s) or whether you are specifying surface or volume mesh file(s) to represent bodies of influence for your simulation. The units for length will be the same as those specified in the Import Geometry task.
        GeometryFileName : str
            Select CAD file(s) to import into your simulation as a body of influence. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: *.CATpart, *.prt, *.x_t, *.sat, *.step, and *.iges files)
        MeshFileName : str
            Select surface or volume mesh file(s) to import into your simulation as a body of influence. Supported file types are: *.msh, *.msh.gz, and *.msh.h5 files).
        ImportedObjects : list[str]
        LengthUnit : str
        CadImportOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImportBodyOfInfluenceGeometryCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Type = self._Type(self, "Type", service, rules, path)
                self.GeometryFileName = self._GeometryFileName(self, "GeometryFileName", service, rules, path)
                self.MeshFileName = self._MeshFileName(self, "MeshFileName", service, rules, path)
                self.ImportedObjects = self._ImportedObjects(self, "ImportedObjects", service, rules, path)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.CadImportOptions = self._CadImportOptions(self, "CadImportOptions", service, rules, path)

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Specify whether you are importing CAD geometry file(s) or whether you are specifying surface or volume mesh file(s) to represent bodies of influence for your simulation. The units for length will be the same as those specified in the Import Geometry task.
                """

            class _GeometryFileName(PyTextualCommandArgumentsSubItem):
                """
                Select CAD file(s) to import into your simulation as a body of influence. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files)
                """

            class _MeshFileName(PyTextualCommandArgumentsSubItem):
                """
                Select surface or volume mesh file(s) to import into your simulation as a body of influence. Supported file types are: \\*.msh, \\*.msh.gz, and \\*.msh.h5 files).
                """

            class _ImportedObjects(PyTextualCommandArgumentsSubItem):
                """
                Argument ImportedObjects.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument LengthUnit.
                """

            class _CadImportOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument CadImportOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SavePMDBIntermediateFile = self._SavePMDBIntermediateFile(self, "SavePMDBIntermediateFile", service, rules, path)
                    self.OneObjectPer = self._OneObjectPer(self, "OneObjectPer", service, rules, path)
                    self.OpenAllCadInSubdirectories = self._OpenAllCadInSubdirectories(self, "OpenAllCadInSubdirectories", service, rules, path)
                    self.CreateCADAssemblies = self._CreateCADAssemblies(self, "CreateCADAssemblies", service, rules, path)
                    self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                    self.OneZonePer = self._OneZonePer(self, "OneZonePer", service, rules, path)
                    self.ImportCurvatureDataFromCAD = self._ImportCurvatureDataFromCAD(self, "ImportCurvatureDataFromCAD", service, rules, path)
                    self.ExtractFeatures = self._ExtractFeatures(self, "ExtractFeatures", service, rules, path)
                    self.UsePartOrBodyAsSuffix = self._UsePartOrBodyAsSuffix(self, "UsePartOrBodyAsSuffix", service, rules, path)
                    self.ImportPartNames = self._ImportPartNames(self, "ImportPartNames", service, rules, path)
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)

                class _SavePMDBIntermediateFile(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SavePMDBIntermediateFile.
                    """

                class _OneObjectPer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OneObjectPer.
                    """

                class _OpenAllCadInSubdirectories(PyParameterCommandArgumentsSubItem):
                    """
                    Argument OpenAllCadInSubdirectories.
                    """

                class _CreateCADAssemblies(PyParameterCommandArgumentsSubItem):
                    """
                    Argument CreateCADAssemblies.
                    """

                class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _OneZonePer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OneZonePer.
                    """

                class _ImportCurvatureDataFromCAD(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportCurvatureDataFromCAD.
                    """

                class _ExtractFeatures(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _UsePartOrBodyAsSuffix(PyParameterCommandArgumentsSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
                    """

                class _ImportPartNames(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _ImportNamedSelections(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

        def create_instance(self) -> _ImportBodyOfInfluenceGeometryCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImportBodyOfInfluenceGeometryCommandArguments(*args)

    class ImportGeometry(PyCommand):
        """
        Command ImportGeometry.

        Parameters
        ----------
        FileFormat : str
            Indicate whether the imported geometry is a CAD File or a Mesh (either a surface or volume mesh).
        ImportType : str
            When the File Format is set to CAD, use the Import Type field to import a Single File (the default), or Multiple Files. When importing multiple files, the Select File dialog allows you to make multiple selections, as long as the files are in the same directory and are of the same CAD format.
        LengthUnit : str
            Select a suitable working unit for the meshing operation, with a min size of the order of 1. The model will be automatically scaled to meters when switching to the solver. It is recommended to select units so that the minimum size is between approximately 0.1 - 10. If the minimum size falls outside of this range, then you should change the units.
        MeshUnit : str
            Specify the units in which the surface or volume mesh was created in.
        UseBodyLabels : str
            Specify that you want to use any composite body labels that are defined in your imported CAD geometry by choosing Yes. If the imported CAD file does not contain any body labels, then this will automatically be set to No.
        ImportCadPreferences : dict[str, Any]
        FileName : str
            Select a CAD file to import into your simulation. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: *.CATpart, *.prt, *.x_t, *.sat, *.step, and *.iges files).
        FileNames : str
            Select multiple CAD files to import into your simulation. When importing multiple files, use the browse button (...) to open the Select File dialog that allows you to make multiple selections, as long as the files are in the same directory and are of the same CAD format. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: *.CATpart, *.prt, *.x_t, *.sat, *.step, and *.iges files).
        MeshFileName : str
        NumParts : float
        AppendMesh : bool
        Directory : str
        Pattern : str
        CadImportOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImportGeometryCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileFormat = self._FileFormat(self, "FileFormat", service, rules, path)
                self.ImportType = self._ImportType(self, "ImportType", service, rules, path)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.MeshUnit = self._MeshUnit(self, "MeshUnit", service, rules, path)
                self.UseBodyLabels = self._UseBodyLabels(self, "UseBodyLabels", service, rules, path)
                self.ImportCadPreferences = self._ImportCadPreferences(self, "ImportCadPreferences", service, rules, path)
                self.FileName = self._FileName(self, "FileName", service, rules, path)
                self.FileNames = self._FileNames(self, "FileNames", service, rules, path)
                self.MeshFileName = self._MeshFileName(self, "MeshFileName", service, rules, path)
                self.NumParts = self._NumParts(self, "NumParts", service, rules, path)
                self.AppendMesh = self._AppendMesh(self, "AppendMesh", service, rules, path)
                self.Directory = self._Directory(self, "Directory", service, rules, path)
                self.Pattern = self._Pattern(self, "Pattern", service, rules, path)
                self.CadImportOptions = self._CadImportOptions(self, "CadImportOptions", service, rules, path)

            class _FileFormat(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether the imported geometry is a CAD File or a Mesh (either a surface or volume mesh).
                """

            class _ImportType(PyTextualCommandArgumentsSubItem):
                """
                When the File Format is set to CAD, use the Import Type field to import a Single File (the default), or Multiple Files. When importing multiple files, the Select File dialog allows you to make multiple selections, as long as the files are in the same directory and are of the same CAD format.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Select a suitable working unit for the meshing operation, with a min size of the order of 1. The model will be automatically scaled to meters when switching to the solver. It is recommended to select units so that the minimum size is between approximately 0.1 - 10. If the minimum size falls outside of this range, then you should change the units.
                """

            class _MeshUnit(PyTextualCommandArgumentsSubItem):
                """
                Specify the units in which the surface or volume mesh was created in.
                """

            class _UseBodyLabels(PyTextualCommandArgumentsSubItem):
                """
                Specify that you want to use any composite body labels that are defined in your imported CAD geometry by choosing Yes. If the imported CAD file does not contain any body labels, then this will automatically be set to No.
                """

            class _ImportCadPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument ImportCadPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.EdgeLabel = self._EdgeLabel(self, "EdgeLabel", service, rules, path)
                    self.FacetedBodies = self._FacetedBodies(self, "FacetedBodies", service, rules, path)
                    self.CISeparation = self._CISeparation(self, "CISeparation", service, rules, path)
                    self.CIRefaceting = self._CIRefaceting(self, "CIRefaceting", service, rules, path)
                    self.AutomaticObjectCreation = self._AutomaticObjectCreation(self, "AutomaticObjectCreation", service, rules, path)
                    self.MaxFacetLength = self._MaxFacetLength(self, "MaxFacetLength", service, rules, path)
                    self.ShowImportCadPreferences = self._ShowImportCadPreferences(self, "ShowImportCadPreferences", service, rules, path)
                    self.MergeNodes = self._MergeNodes(self, "MergeNodes", service, rules, path)
                    self.CISeparationAngle = self._CISeparationAngle(self, "CISeparationAngle", service, rules, path)
                    self.CITolerence = self._CITolerence(self, "CITolerence", service, rules, path)

                class _EdgeLabel(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeLabel.
                    """

                class _FacetedBodies(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FacetedBodies.
                    """

                class _CISeparation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CISeparation.
                    """

                class _CIRefaceting(PyParameterCommandArgumentsSubItem):
                    """
                    Argument CIRefaceting.
                    """

                class _AutomaticObjectCreation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutomaticObjectCreation.
                    """

                class _MaxFacetLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxFacetLength.
                    """

                class _ShowImportCadPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowImportCadPreferences.
                    """

                class _MergeNodes(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MergeNodes.
                    """

                class _CISeparationAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CISeparationAngle.
                    """

                class _CITolerence(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CITolerence.
                    """

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Select a CAD file to import into your simulation. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files).
                """

            class _FileNames(PyTextualCommandArgumentsSubItem):
                """
                Select multiple CAD files to import into your simulation. When importing multiple files, use the browse button (...) to open the Select File dialog that allows you to make multiple selections, as long as the files are in the same directory and are of the same CAD format. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files).
                """

            class _MeshFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshFileName.
                """

            class _NumParts(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumParts.
                """

            class _AppendMesh(PyParameterCommandArgumentsSubItem):
                """
                Argument AppendMesh.
                """

            class _Directory(PyTextualCommandArgumentsSubItem):
                """
                Argument Directory.
                """

            class _Pattern(PyTextualCommandArgumentsSubItem):
                """
                Argument Pattern.
                """

            class _CadImportOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument CadImportOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SavePMDBIntermediateFile = self._SavePMDBIntermediateFile(self, "SavePMDBIntermediateFile", service, rules, path)
                    self.OneObjectPer = self._OneObjectPer(self, "OneObjectPer", service, rules, path)
                    self.OpenAllCadInSubdirectories = self._OpenAllCadInSubdirectories(self, "OpenAllCadInSubdirectories", service, rules, path)
                    self.CreateCADAssemblies = self._CreateCADAssemblies(self, "CreateCADAssemblies", service, rules, path)
                    self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                    self.OneZonePer = self._OneZonePer(self, "OneZonePer", service, rules, path)
                    self.UsePartOrBodyAsSuffix = self._UsePartOrBodyAsSuffix(self, "UsePartOrBodyAsSuffix", service, rules, path)
                    self.ExtractFeatures = self._ExtractFeatures(self, "ExtractFeatures", service, rules, path)
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)
                    self.ImportPartNames = self._ImportPartNames(self, "ImportPartNames", service, rules, path)
                    self.ImportCurvatureDataFromCAD = self._ImportCurvatureDataFromCAD(self, "ImportCurvatureDataFromCAD", service, rules, path)

                class _SavePMDBIntermediateFile(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SavePMDBIntermediateFile.
                    """

                class _OneObjectPer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OneObjectPer.
                    """

                class _OpenAllCadInSubdirectories(PyParameterCommandArgumentsSubItem):
                    """
                    Argument OpenAllCadInSubdirectories.
                    """

                class _CreateCADAssemblies(PyParameterCommandArgumentsSubItem):
                    """
                    Argument CreateCADAssemblies.
                    """

                class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _OneZonePer(PyTextualCommandArgumentsSubItem):
                    """
                    Argument OneZonePer.
                    """

                class _UsePartOrBodyAsSuffix(PyParameterCommandArgumentsSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
                    """

                class _ExtractFeatures(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _ImportNamedSelections(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

                class _ImportPartNames(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _ImportCurvatureDataFromCAD(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportCurvatureDataFromCAD.
                    """

        def create_instance(self) -> _ImportGeometryCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImportGeometryCommandArguments(*args)

    class ImproveSurfaceMesh(PyCommand):
        """
        Command ImproveSurfaceMesh.

        Parameters
        ----------
        MeshObject : str
        FaceQualityLimit : float
            Use the specified value to improve the surface mesh. Note that this control can aggressively change your surface mesh when applied.
        SQMinSize : float
        ScopeImproveTo : str
        SMImprovePreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImproveSurfaceMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.FaceQualityLimit = self._FaceQualityLimit(self, "FaceQualityLimit", service, rules, path)
                self.SQMinSize = self._SQMinSize(self, "SQMinSize", service, rules, path)
                self.ScopeImproveTo = self._ScopeImproveTo(self, "ScopeImproveTo", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _FaceQualityLimit(PyNumericalCommandArgumentsSubItem):
                """
                Use the specified value to improve the surface mesh. Note that this control can aggressively change your surface mesh when applied.
                """

            class _SQMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument SQMinSize.
                """

            class _ScopeImproveTo(PyTextualCommandArgumentsSubItem):
                """
                Argument ScopeImproveTo.
                """

            class _SMImprovePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument SMImprovePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SIStepQualityLimit = self._SIStepQualityLimit(self, "SIStepQualityLimit", service, rules, path)
                    self.SIQualityCollapseLimit = self._SIQualityCollapseLimit(self, "SIQualityCollapseLimit", service, rules, path)
                    self.SIQualityIterations = self._SIQualityIterations(self, "SIQualityIterations", service, rules, path)
                    self.SIQualityMaxAngle = self._SIQualityMaxAngle(self, "SIQualityMaxAngle", service, rules, path)
                    self.AllowDefeaturing = self._AllowDefeaturing(self, "AllowDefeaturing", service, rules, path)
                    self.ShowSMImprovePreferences = self._ShowSMImprovePreferences(self, "ShowSMImprovePreferences", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.SIStepWidth = self._SIStepWidth(self, "SIStepWidth", service, rules, path)
                    self.SIRemoveStep = self._SIRemoveStep(self, "SIRemoveStep", service, rules, path)

                class _SIStepQualityLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepQualityLimit.
                    """

                class _SIQualityCollapseLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityCollapseLimit.
                    """

                class _SIQualityIterations(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityIterations.
                    """

                class _SIQualityMaxAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityMaxAngle.
                    """

                class _AllowDefeaturing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _ShowSMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _AdvancedImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _SIStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepWidth.
                    """

                class _SIRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SIRemoveStep.
                    """

        def create_instance(self) -> _ImproveSurfaceMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImproveSurfaceMeshCommandArguments(*args)

    class ImproveVolumeMesh(PyCommand):
        """
        Command ImproveVolumeMesh.

        Parameters
        ----------
        QualityMethod : str
            Choose from several different types of mesh quality controls (skewness, aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows), Enhanced Orthogonal, and Skewness. For more information, see  More... .
        CellQualityLimit : float
            Use the specified value to improve the volume mesh. Note that this control can aggressively change your volume mesh when applied.
        AddMultipleQualityMethods : str
            Use this option to specify quality criteria for multiple quality methods.
        QualityMethodList : list[str]
        QualityCriteriaList : list[str]
        OldQualityMethodList : list[str]
        OldQualityCriteriaList : list[str]
        VMImprovePreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImproveVolumeMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.QualityMethod = self._QualityMethod(self, "QualityMethod", service, rules, path)
                self.CellQualityLimit = self._CellQualityLimit(self, "CellQualityLimit", service, rules, path)
                self.AddMultipleQualityMethods = self._AddMultipleQualityMethods(self, "AddMultipleQualityMethods", service, rules, path)
                self.QualityMethodList = self._QualityMethodList(self, "QualityMethodList", service, rules, path)
                self.QualityCriteriaList = self._QualityCriteriaList(self, "QualityCriteriaList", service, rules, path)
                self.OldQualityMethodList = self._OldQualityMethodList(self, "OldQualityMethodList", service, rules, path)
                self.OldQualityCriteriaList = self._OldQualityCriteriaList(self, "OldQualityCriteriaList", service, rules, path)
                self.VMImprovePreferences = self._VMImprovePreferences(self, "VMImprovePreferences", service, rules, path)

            class _QualityMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose from several different types of mesh quality controls (skewness, aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows), Enhanced Orthogonal, and Skewness. For more information, see  More... .
                """

            class _CellQualityLimit(PyNumericalCommandArgumentsSubItem):
                """
                Use the specified value to improve the volume mesh. Note that this control can aggressively change your volume mesh when applied.
                """

            class _AddMultipleQualityMethods(PyTextualCommandArgumentsSubItem):
                """
                Use this option to specify quality criteria for multiple quality methods.
                """

            class _QualityMethodList(PyTextualCommandArgumentsSubItem):
                """
                Argument QualityMethodList.
                """

            class _QualityCriteriaList(PyTextualCommandArgumentsSubItem):
                """
                Argument QualityCriteriaList.
                """

            class _OldQualityMethodList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldQualityMethodList.
                """

            class _OldQualityCriteriaList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldQualityCriteriaList.
                """

            class _VMImprovePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument VMImprovePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.VIgnoreFeature = self._VIgnoreFeature(self, "VIgnoreFeature", service, rules, path)
                    self.ShowVMImprovePreferences = self._ShowVMImprovePreferences(self, "ShowVMImprovePreferences", service, rules, path)
                    self.VIQualityIterations = self._VIQualityIterations(self, "VIQualityIterations", service, rules, path)
                    self.VIQualityMinAngle = self._VIQualityMinAngle(self, "VIQualityMinAngle", service, rules, path)

                class _VIgnoreFeature(PyTextualCommandArgumentsSubItem):
                    """
                    Argument VIgnoreFeature.
                    """

                class _ShowVMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowVMImprovePreferences.
                    """

                class _VIQualityIterations(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VIQualityIterations.
                    """

                class _VIQualityMinAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VIQualityMinAngle.
                    """

        def create_instance(self) -> _ImproveVolumeMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImproveVolumeMeshCommandArguments(*args)

    class LinearMeshPattern(PyCommand):
        """
        Command LinearMeshPattern.

        Parameters
        ----------
        ChildName : str
            Specify a name for the mesh pattern or use the default value.
        ObjectList : list[str]
            Select one or more parts from the list below that you want to use for creating the mesh pattern. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        AutoPopulateVector : str
            Indicate whether or not you want Fluent to approximate both the axes orientation and the pitch value, or whether you want to estimate the Pitch Only (default). This estimation only takes place once, either when the object is selected, or when the option is changed.
        PatternVector : dict[str, Any]
            Specify a name for the mesh pattern or use the default value.
        Pitch : float
            Specify a value for the pitch, or displacement factor, or use the default value.
        NumberOfUnits : int
            Indicate the overall number of units that the pattern will use.
        CheckOverlappingFaces : str
            Graphically highlights the mesh pattern units so that you can visualize them and make sure they are properly aligned. Misaligned units can cause a failure in the share topology of the battery cells.
        BatteryModelingOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _LinearMeshPatternCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ChildName = self._ChildName(self, "ChildName", service, rules, path)
                self.ObjectList = self._ObjectList(self, "ObjectList", service, rules, path)
                self.AutoPopulateVector = self._AutoPopulateVector(self, "AutoPopulateVector", service, rules, path)
                self.PatternVector = self._PatternVector(self, "PatternVector", service, rules, path)
                self.Pitch = self._Pitch(self, "Pitch", service, rules, path)
                self.NumberOfUnits = self._NumberOfUnits(self, "NumberOfUnits", service, rules, path)
                self.CheckOverlappingFaces = self._CheckOverlappingFaces(self, "CheckOverlappingFaces", service, rules, path)
                self.BatteryModelingOptions = self._BatteryModelingOptions(self, "BatteryModelingOptions", service, rules, path)

            class _ChildName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the mesh pattern or use the default value.
                """

            class _ObjectList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more parts from the list below that you want to use for creating the mesh pattern. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _AutoPopulateVector(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether or not you want Fluent to approximate both the axes orientation and the pitch value, or whether you want to estimate the Pitch Only (default). This estimation only takes place once, either when the object is selected, or when the option is changed.
                """

            class _PatternVector(PySingletonCommandArgumentsSubItem):
                """
                Specify a name for the mesh pattern or use the default value.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _Z(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Z.
                    """

                class _Y(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Y.
                    """

            class _Pitch(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the pitch, or displacement factor, or use the default value.
                """

            class _NumberOfUnits(PyNumericalCommandArgumentsSubItem):
                """
                Indicate the overall number of units that the pattern will use.
                """

            class _CheckOverlappingFaces(PyTextualCommandArgumentsSubItem):
                """
                Graphically highlights the mesh pattern units so that you can visualize them and make sure they are properly aligned. Misaligned units can cause a failure in the share topology of the battery cells.
                """

            class _BatteryModelingOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument BatteryModelingOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.FirstNumber = self._FirstNumber(self, "FirstNumber", service, rules, path)
                    self.CustomPatternString = self._CustomPatternString(self, "CustomPatternString", service, rules, path)
                    self.NbCellsPerUnit = self._NbCellsPerUnit(self, "NbCellsPerUnit", service, rules, path)
                    self.InvokeBatteryModelingOptions = self._InvokeBatteryModelingOptions(self, "InvokeBatteryModelingOptions", service, rules, path)
                    self.UseCustomPattern = self._UseCustomPattern(self, "UseCustomPattern", service, rules, path)

                class _FirstNumber(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FirstNumber.
                    """

                class _CustomPatternString(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CustomPatternString.
                    """

                class _NbCellsPerUnit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NbCellsPerUnit.
                    """

                class _InvokeBatteryModelingOptions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument InvokeBatteryModelingOptions.
                    """

                class _UseCustomPattern(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseCustomPattern.
                    """

        def create_instance(self) -> _LinearMeshPatternCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LinearMeshPatternCommandArguments(*args)

    class LoadCADGeometry(PyCommand):
        """
        Command LoadCADGeometry.

        Parameters
        ----------
        FileName : str
        LengthUnit : str
        Route : str
        UsePrimeGeometryKernel : bool
        FacetingTolerance : float
        CreateObjectPer : str
        NumParts : float
        Refaceting : dict[str, Any]

        Returns
        -------
        bool
        """
        class _LoadCADGeometryCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileName = self._FileName(self, "FileName", service, rules, path)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.Route = self._Route(self, "Route", service, rules, path)
                self.UsePrimeGeometryKernel = self._UsePrimeGeometryKernel(self, "UsePrimeGeometryKernel", service, rules, path)
                self.FacetingTolerance = self._FacetingTolerance(self, "FacetingTolerance", service, rules, path)
                self.CreateObjectPer = self._CreateObjectPer(self, "CreateObjectPer", service, rules, path)
                self.NumParts = self._NumParts(self, "NumParts", service, rules, path)
                self.Refaceting = self._Refaceting(self, "Refaceting", service, rules, path)

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Argument FileName.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument LengthUnit.
                """

            class _Route(PyTextualCommandArgumentsSubItem):
                """
                Argument Route.
                """

            class _UsePrimeGeometryKernel(PyParameterCommandArgumentsSubItem):
                """
                Argument UsePrimeGeometryKernel.
                """

            class _FacetingTolerance(PyNumericalCommandArgumentsSubItem):
                """
                Argument FacetingTolerance.
                """

            class _CreateObjectPer(PyTextualCommandArgumentsSubItem):
                """
                Argument CreateObjectPer.
                """

            class _NumParts(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumParts.
                """

            class _Refaceting(PySingletonCommandArgumentsSubItem):
                """
                Argument Refaceting.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.FacetMaxEdgeLength = self._FacetMaxEdgeLength(self, "FacetMaxEdgeLength", service, rules, path)
                    self.FacetResolution = self._FacetResolution(self, "FacetResolution", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                    self.MaxEdgeLengthFactor = self._MaxEdgeLengthFactor(self, "MaxEdgeLengthFactor", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.MaxEdgeLength = self._MaxEdgeLength(self, "MaxEdgeLength", service, rules, path)
                    self.CustomNormalAngle = self._CustomNormalAngle(self, "CustomNormalAngle", service, rules, path)
                    self.CustomDeviation = self._CustomDeviation(self, "CustomDeviation", service, rules, path)
                    self.Refacet = self._Refacet(self, "Refacet", service, rules, path)

                class _FacetMaxEdgeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FacetMaxEdgeLength.
                    """

                class _FacetResolution(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FacetResolution.
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Deviation.
                    """

                class _MaxEdgeLengthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxEdgeLengthFactor.
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NormalAngle.
                    """

                class _MaxEdgeLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxEdgeLength.
                    """

                class _CustomNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CustomNormalAngle.
                    """

                class _CustomDeviation(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CustomDeviation.
                    """

                class _Refacet(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Refacet.
                    """

        def create_instance(self) -> _LoadCADGeometryCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadCADGeometryCommandArguments(*args)

    class LocalScopedSizingForPartReplacement(PyCommand):
        """
        Command LocalScopedSizingForPartReplacement.

        Parameters
        ----------
        LocalSettingsName : str
            Specify a name for the size control or use the default value.
        SelectionType : str
            Choose how you want to make your selection (by object or by zone).
        ObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LabelSelectionList : list[str]
        ZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]
        EdgeSelectionList : list[str]
            Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LocalSizeControlParameters : dict[str, Any]
        ValueChanged : str
        CompleteZoneSelectionList : list[str]
        CompleteLabelSelectionList : list[str]
        CompleteObjectSelectionList : list[str]
        CompleteEdgeSelectionList : list[str]

        Returns
        -------
        bool
        """
        class _LocalScopedSizingForPartReplacementCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LocalSettingsName = self._LocalSettingsName(self, "LocalSettingsName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                self.LocalSizeControlParameters = self._LocalSizeControlParameters(self, "LocalSizeControlParameters", service, rules, path)
                self.ValueChanged = self._ValueChanged(self, "ValueChanged", service, rules, path)
                self.CompleteZoneSelectionList = self._CompleteZoneSelectionList(self, "CompleteZoneSelectionList", service, rules, path)
                self.CompleteLabelSelectionList = self._CompleteLabelSelectionList(self, "CompleteLabelSelectionList", service, rules, path)
                self.CompleteObjectSelectionList = self._CompleteObjectSelectionList(self, "CompleteObjectSelectionList", service, rules, path)
                self.CompleteEdgeSelectionList = self._CompleteEdgeSelectionList(self, "CompleteEdgeSelectionList", service, rules, path)

            class _LocalSettingsName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the size control or use the default value.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by object or by zone).
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LocalSizeControlParameters(PySingletonCommandArgumentsSubItem):
                """
                Argument LocalSizeControlParameters.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.IgnoreSelf = self._IgnoreSelf(self, "IgnoreSelf", service, rules, path)
                    self.WrapMin = self._WrapMin(self, "WrapMin", service, rules, path)
                    self.WrapCellsPerGap = self._WrapCellsPerGap(self, "WrapCellsPerGap", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.WrapMax = self._WrapMax(self, "WrapMax", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.WrapGrowthRate = self._WrapGrowthRate(self, "WrapGrowthRate", service, rules, path)
                    self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                    self.InitialSizeControl = self._InitialSizeControl(self, "InitialSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.WrapCurvatureNormalAngle = self._WrapCurvatureNormalAngle(self, "WrapCurvatureNormalAngle", service, rules, path)
                    self.TargetSizeControl = self._TargetSizeControl(self, "TargetSizeControl", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _IgnoreSelf(PyParameterCommandArgumentsSubItem):
                    """
                    Argument IgnoreSelf.
                    """

                class _WrapMin(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapMin.
                    """

                class _WrapCellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapCellsPerGap.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _WrapMax(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapMax.
                    """

                class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AdvancedOptions.
                    """

                class _WrapGrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapGrowthRate.
                    """

                class _SizingType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizingType.
                    """

                class _InitialSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument InitialSizeControl.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _WrapCurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapCurvatureNormalAngle.
                    """

                class _TargetSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument TargetSizeControl.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

            class _ValueChanged(PyTextualCommandArgumentsSubItem):
                """
                Argument ValueChanged.
                """

            class _CompleteZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneSelectionList.
                """

            class _CompleteLabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

            class _CompleteObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteObjectSelectionList.
                """

            class _CompleteEdgeSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteEdgeSelectionList.
                """

        def create_instance(self) -> _LocalScopedSizingForPartReplacementCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LocalScopedSizingForPartReplacementCommandArguments(*args)

    class ManageZones(PyCommand):
        """
        Command ManageZones.

        Parameters
        ----------
        Type : str
            Indicate whether you are going to operate on Cell Zones or Face Zones. If your imported CAD geometry contains bodies with multiple body labels, you can also choose Body Labels.
        ZoneFilter : str
            Choose the type of zone. For cell zones, choose from Fluid, Solid, or All. For face zones, choose from Internal, Fluid-Fluid, Solid-Fluid, Fluid-Solid, External-Solid, External-Fluid, or External.
        SizeFilter : str
            Indicate how you would like to filter the list of zones: All, Less than, More than, or Equal to the indicated value for the Volume (cell zone) or Area (face zone).
        Area : float
        Volume : float
        EqualRange : float
            Specify a percentage range to maintain equivalency for the cell zone volume value or the face zone area value.
        ZoneOrLabel : str
            Choose how you want to make your selection (by label or zone name).
        LabelList : list[str]
            Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ManageFaceZoneList : list[str]
            Choose from the list of face zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ManageCellZoneList : list[str]
            Choose from the list of cell zones, or enter a text string to filter out the list of cell zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        BodyLabelList : list[str]
        Operation : str
            Indicate the operation you wish to perform on the zones. When the task is located prior volume meshing: Separate Zones, Split Cylinders, Split normal to X, Split normal to Y, Split normal to Z, or Extract Edges. When the task is located after volume meshing: Change prefix, Rename, Merge, or Separate Zones. If your imported CAD geometry contains bodies with multiple body labels, you can also choose Merge cells within each body label
        OperationName : str
            The text string to be applied to this zone operation.
        MZChildName : str
            Specify a name for the managed zone control or use the default value.
        AddPrefixName : str
            The text string to be applied to this zone operation.
        FaceMerge : str
            Indicate whether or not you want to merge faces as part of the zone operation.
        Angle : float
            Specify a value for the separation angle for determining separation. Assigning a smaller separation angle will produce more zones.
        ZoneList : list[str]
        CompleteZoneList : list[str]
        CompleteLabelList : list[str]
        ZoneLocation : list[str]

        Returns
        -------
        bool
        """
        class _ManageZonesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Type = self._Type(self, "Type", service, rules, path)
                self.ZoneFilter = self._ZoneFilter(self, "ZoneFilter", service, rules, path)
                self.SizeFilter = self._SizeFilter(self, "SizeFilter", service, rules, path)
                self.Area = self._Area(self, "Area", service, rules, path)
                self.Volume = self._Volume(self, "Volume", service, rules, path)
                self.EqualRange = self._EqualRange(self, "EqualRange", service, rules, path)
                self.ZoneOrLabel = self._ZoneOrLabel(self, "ZoneOrLabel", service, rules, path)
                self.LabelList = self._LabelList(self, "LabelList", service, rules, path)
                self.ManageFaceZoneList = self._ManageFaceZoneList(self, "ManageFaceZoneList", service, rules, path)
                self.ManageCellZoneList = self._ManageCellZoneList(self, "ManageCellZoneList", service, rules, path)
                self.BodyLabelList = self._BodyLabelList(self, "BodyLabelList", service, rules, path)
                self.Operation = self._Operation(self, "Operation", service, rules, path)
                self.OperationName = self._OperationName(self, "OperationName", service, rules, path)
                self.MZChildName = self._MZChildName(self, "MZChildName", service, rules, path)
                self.AddPrefixName = self._AddPrefixName(self, "AddPrefixName", service, rules, path)
                self.FaceMerge = self._FaceMerge(self, "FaceMerge", service, rules, path)
                self.Angle = self._Angle(self, "Angle", service, rules, path)
                self.ZoneList = self._ZoneList(self, "ZoneList", service, rules, path)
                self.CompleteZoneList = self._CompleteZoneList(self, "CompleteZoneList", service, rules, path)
                self.CompleteLabelList = self._CompleteLabelList(self, "CompleteLabelList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether you are going to operate on Cell Zones or Face Zones. If your imported CAD geometry contains bodies with multiple body labels, you can also choose Body Labels.
                """

            class _ZoneFilter(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of zone. For cell zones, choose from Fluid, Solid, or All. For face zones, choose from Internal, Fluid-Fluid, Solid-Fluid, Fluid-Solid, External-Solid, External-Fluid, or External.
                """

            class _SizeFilter(PyTextualCommandArgumentsSubItem):
                """
                Indicate how you would like to filter the list of zones: All, Less than, More than, or Equal to the indicated value for the Volume (cell zone) or Area (face zone).
                """

            class _Area(PyNumericalCommandArgumentsSubItem):
                """
                Argument Area.
                """

            class _Volume(PyNumericalCommandArgumentsSubItem):
                """
                Argument Volume.
                """

            class _EqualRange(PyNumericalCommandArgumentsSubItem):
                """
                Specify a percentage range to maintain equivalency for the cell zone volume value or the face zone area value.
                """

            class _ZoneOrLabel(PyTextualCommandArgumentsSubItem):
                """
                Choose how you want to make your selection (by label or zone name).
                """

            class _LabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ManageFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of face zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ManageCellZoneList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of cell zones, or enter a text string to filter out the list of cell zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BodyLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BodyLabelList.
                """

            class _Operation(PyTextualCommandArgumentsSubItem):
                """
                Indicate the operation you wish to perform on the zones. When the task is located prior volume meshing: Separate Zones, Split Cylinders, Split normal to X, Split normal to Y, Split normal to Z, or Extract Edges. When the task is located after volume meshing: Change prefix, Rename, Merge, or Separate Zones. If your imported CAD geometry contains bodies with multiple body labels, you can also choose Merge cells within each body label
                """

            class _OperationName(PyTextualCommandArgumentsSubItem):
                """
                The text string to be applied to this zone operation.
                """

            class _MZChildName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the managed zone control or use the default value.
                """

            class _AddPrefixName(PyTextualCommandArgumentsSubItem):
                """
                The text string to be applied to this zone operation.
                """

            class _FaceMerge(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether or not you want to merge faces as part of the zone operation.
                """

            class _Angle(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the separation angle for determining separation. Assigning a smaller separation angle will produce more zones.
                """

            class _ZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneList.
                """

            class _CompleteZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteZoneList.
                """

            class _CompleteLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument CompleteLabelList.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _ManageZonesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ManageZonesCommandArguments(*args)

    class MeshFluidDomain(PyCommand):
        """
        Command MeshFluidDomain.

        Parameters
        ----------
        MeshFluidDomainOption : bool

        Returns
        -------
        bool
        """
        class _MeshFluidDomainCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshFluidDomainOption = self._MeshFluidDomainOption(self, "MeshFluidDomainOption", service, rules, path)

            class _MeshFluidDomainOption(PyParameterCommandArgumentsSubItem):
                """
                Argument MeshFluidDomainOption.
                """

        def create_instance(self) -> _MeshFluidDomainCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MeshFluidDomainCommandArguments(*args)

    class ModifyMeshRefinement(PyCommand):
        """
        Command ModifyMeshRefinement.

        Parameters
        ----------
        MeshObject : str
        RemeshExecution : str
            Specify whether to just add the current size control to the workflow, or to add the size control and perform a remeshing operation immediately thereafter.
        RemeshControlName : str
            Provide a name for this specific size control.
        LocalSize : float
            Specify a value for the local sizing parameter to be applied to the indicated zone.
        FaceZoneOrLabel : str
            Specify whether the size control is to be applied to an indicated zone or a label.
        RemeshFaceZoneList : list[str]
            Choose from the list of zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        RemeshFaceLabelList : list[str]
            Choose from the list of zone labels, or enter a text string to filter out the list of face zone labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        SizingType : str
        LocalMinSize : float
        LocalMaxSize : float
        RemeshGrowthRate : float
        RemeshCurvatureNormalAngle : float
        RemeshCellsPerGap : float
        CFDSurfaceMeshControls : dict[str, Any]
        RemeshPreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ModifyMeshRefinementCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.RemeshExecution = self._RemeshExecution(self, "RemeshExecution", service, rules, path)
                self.RemeshControlName = self._RemeshControlName(self, "RemeshControlName", service, rules, path)
                self.LocalSize = self._LocalSize(self, "LocalSize", service, rules, path)
                self.FaceZoneOrLabel = self._FaceZoneOrLabel(self, "FaceZoneOrLabel", service, rules, path)
                self.RemeshFaceZoneList = self._RemeshFaceZoneList(self, "RemeshFaceZoneList", service, rules, path)
                self.RemeshFaceLabelList = self._RemeshFaceLabelList(self, "RemeshFaceLabelList", service, rules, path)
                self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                self.LocalMinSize = self._LocalMinSize(self, "LocalMinSize", service, rules, path)
                self.LocalMaxSize = self._LocalMaxSize(self, "LocalMaxSize", service, rules, path)
                self.RemeshGrowthRate = self._RemeshGrowthRate(self, "RemeshGrowthRate", service, rules, path)
                self.RemeshCurvatureNormalAngle = self._RemeshCurvatureNormalAngle(self, "RemeshCurvatureNormalAngle", service, rules, path)
                self.RemeshCellsPerGap = self._RemeshCellsPerGap(self, "RemeshCellsPerGap", service, rules, path)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.RemeshPreferences = self._RemeshPreferences(self, "RemeshPreferences", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _RemeshExecution(PyTextualCommandArgumentsSubItem):
                """
                Specify whether to just add the current size control to the workflow, or to add the size control and perform a remeshing operation immediately thereafter.
                """

            class _RemeshControlName(PyTextualCommandArgumentsSubItem):
                """
                Provide a name for this specific size control.
                """

            class _LocalSize(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the local sizing parameter to be applied to the indicated zone.
                """

            class _FaceZoneOrLabel(PyTextualCommandArgumentsSubItem):
                """
                Specify whether the size control is to be applied to an indicated zone or a label.
                """

            class _RemeshFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _RemeshFaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of zone labels, or enter a text string to filter out the list of face zone labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _SizingType(PyTextualCommandArgumentsSubItem):
                """
                Argument SizingType.
                """

            class _LocalMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument LocalMinSize.
                """

            class _LocalMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument LocalMaxSize.
                """

            class _RemeshGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument RemeshGrowthRate.
                """

            class _RemeshCurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument RemeshCurvatureNormalAngle.
                """

            class _RemeshCellsPerGap(PyNumericalCommandArgumentsSubItem):
                """
                Argument RemeshCellsPerGap.
                """

            class _CFDSurfaceMeshControls(PySingletonCommandArgumentsSubItem):
                """
                Argument CFDSurfaceMeshControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SaveSizeFieldFile = self._SaveSizeFieldFile(self, "SaveSizeFieldFile", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.ScopeProximityTo = self._ScopeProximityTo(self, "ScopeProximityTo", service, rules, path)
                    self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                    self.PreviewSizefield = self._PreviewSizefield(self, "PreviewSizefield", service, rules, path)
                    self.SaveSizeField = self._SaveSizeField(self, "SaveSizeField", service, rules, path)
                    self.UseSizeFiles = self._UseSizeFiles(self, "UseSizeFiles", service, rules, path)
                    self.AutoCreateScopedSizing = self._AutoCreateScopedSizing(self, "AutoCreateScopedSizing", service, rules, path)
                    self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                    self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _CurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _PreviewSizefield(PyParameterCommandArgumentsSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _SaveSizeField(PyParameterCommandArgumentsSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SizeFieldFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _RemeshPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument RemeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.RMCornerAngle = self._RMCornerAngle(self, "RMCornerAngle", service, rules, path)
                    self.RMFeatureMinAngle = self._RMFeatureMinAngle(self, "RMFeatureMinAngle", service, rules, path)
                    self.RMFeatureMaxAngle = self._RMFeatureMaxAngle(self, "RMFeatureMaxAngle", service, rules, path)
                    self.ShowRemeshPreferences = self._ShowRemeshPreferences(self, "ShowRemeshPreferences", service, rules, path)

                class _RMCornerAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RMCornerAngle.
                    """

                class _RMFeatureMinAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RMFeatureMinAngle.
                    """

                class _RMFeatureMaxAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RMFeatureMaxAngle.
                    """

                class _ShowRemeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowRemeshPreferences.
                    """

        def create_instance(self) -> _ModifyMeshRefinementCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ModifyMeshRefinementCommandArguments(*args)

    class PartManagement(PyCommand):
        """
        Command PartManagement.

        Parameters
        ----------
        FileLoaded : str
        FMDFileName : str
            Select a CAD file to import into your simulation. Standard Ansys file types, among others, are supported, including .scdoc, .dsco, .agdb, .fmd, .fmdb, .fmd, .pmdb, .tgf, and .msh. To quickly import multiple CAD files, you can use basic wildcard expression patterns such as the * or ? wildcards. More...
        AppendFileName : str
            Enable this option and browse/select another CAD file to append to your original geometry. Specify additional CAD files in the Append File field, and use the Append button to load additional CAD files into the tree, after the original CAD objects. To quickly append multiple CAD files, you can use basic wildcard expression patterns such as the * or ? wildcards.
        Append : bool
            Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
        LengthUnit : str
            Select a suitable unit for display in the graphics window.
        CreateObjectPer : str
            Choose whether to create meshing objects by part, or by selectively customizing the portions of the imported CAD geometry to mesh. If you select by part, then meshing objects are automatically created for you once you import the geometry. Refaceting options are available as well for all meshing objects.
        FileLengthUnit : str
            Specify the units of length used by this .stl file before loading the CAD file.
        FileLengthUnitAppend : str
            Specify the units of length used by this .stl file before appending the CAD file.
        Route : str
            Provides the recommended route in order to import and load the specified CAD file into this task. The default settings are recommended in most cases.  More...
        RouteAppend : str
            Provides the recommended route in order to import and append the specified CAD file into this task. The default settings are recommended in most cases.  More...
        JtLOD : str
            Specify the level of detail that you want to include for this .jt file before loading the CAD file.
        JtLODAppend : str
            Specify the level of detail that you want to include for this .jt file before appending the CAD file.
        PartPerBody : bool
            Enable this option to make all bodies available as individual parts in the CAD Model tree once the CAD file is loaded into the task.
        PrefixParentName : bool
            This applies the name of the component (or assembly) as a prefix to the individual part names when the geometry is loaded into the task.
        RemoveEmptyParts : bool
            Enabled by default, this option lets you import your CAD geometry while removing any empty components.
        FeatureAngle : float
            Specify the angle at which features will be extracted from the CAD model on import. The smaller the angle, the more features will be captured, thereby taking more time for processing. An angle of 40 degrees is a typical value.
        OneZonePer : str
            Specify whether to create your meshing zones based on an object, part, body or face. For instance, choosing the face option would create a separate zone for every topological face.
        Refaceting : dict[str, Any]
        IgnoreSolidNames : bool
            Enable this option to import your CAD geometry while ignoring the names assigned to solids. Note that binary STL files contain a single solid and may have an associated solid name, whereas ASCII STL files contain one or more solids and each can have a  solid name. This option allows to control whether or not to use the name contained in the STL file for naming mesh objects and components.
        IgnoreSolidNamesAppend : bool
        Options : dict[str, Any]
        EdgeExtraction : str
            Choose how edges will be extracted from the CAD geometry. Setting this option to auto will extract edges from the CAD geometry when the number of meshing objects is less than 10,000. If this limit is exceeded, then no edges are extracted. When this option is set to yes, then edges are extracted regardless of the number of meshing objects. No edges are extracted when this option is set to no.
        Context : int
        ObjectSetting : str
        RefacetOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _PartManagementCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileLoaded = self._FileLoaded(self, "FileLoaded", service, rules, path)
                self.FMDFileName = self._FMDFileName(self, "FMDFileName", service, rules, path)
                self.AppendFileName = self._AppendFileName(self, "AppendFileName", service, rules, path)
                self.Append = self._Append(self, "Append", service, rules, path)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.CreateObjectPer = self._CreateObjectPer(self, "CreateObjectPer", service, rules, path)
                self.FileLengthUnit = self._FileLengthUnit(self, "FileLengthUnit", service, rules, path)
                self.FileLengthUnitAppend = self._FileLengthUnitAppend(self, "FileLengthUnitAppend", service, rules, path)
                self.Route = self._Route(self, "Route", service, rules, path)
                self.RouteAppend = self._RouteAppend(self, "RouteAppend", service, rules, path)
                self.JtLOD = self._JtLOD(self, "JtLOD", service, rules, path)
                self.JtLODAppend = self._JtLODAppend(self, "JtLODAppend", service, rules, path)
                self.PartPerBody = self._PartPerBody(self, "PartPerBody", service, rules, path)
                self.PrefixParentName = self._PrefixParentName(self, "PrefixParentName", service, rules, path)
                self.RemoveEmptyParts = self._RemoveEmptyParts(self, "RemoveEmptyParts", service, rules, path)
                self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                self.OneZonePer = self._OneZonePer(self, "OneZonePer", service, rules, path)
                self.Refaceting = self._Refaceting(self, "Refaceting", service, rules, path)
                self.IgnoreSolidNames = self._IgnoreSolidNames(self, "IgnoreSolidNames", service, rules, path)
                self.IgnoreSolidNamesAppend = self._IgnoreSolidNamesAppend(self, "IgnoreSolidNamesAppend", service, rules, path)
                self.Options = self._Options(self, "Options", service, rules, path)
                self.EdgeExtraction = self._EdgeExtraction(self, "EdgeExtraction", service, rules, path)
                self.Context = self._Context(self, "Context", service, rules, path)
                self.ObjectSetting = self._ObjectSetting(self, "ObjectSetting", service, rules, path)
                self.RefacetOptions = self._RefacetOptions(self, "RefacetOptions", service, rules, path)

            class _FileLoaded(PyTextualCommandArgumentsSubItem):
                """
                Argument FileLoaded.
                """

            class _FMDFileName(PyTextualCommandArgumentsSubItem):
                """
                Select a CAD file to import into your simulation. Standard Ansys file types, among others, are supported, including .scdoc, .dsco, .agdb, .fmd, .fmdb, .fmd, .pmdb, .tgf, and .msh. To quickly import multiple CAD files, you can use basic wildcard expression patterns such as the \\* or ? wildcards. More...
                """

            class _AppendFileName(PyTextualCommandArgumentsSubItem):
                """
                Enable this option and browse/select another CAD file to append to your original geometry. Specify additional CAD files in the Append File field, and use the Append button to load additional CAD files into the tree, after the original CAD objects. To quickly append multiple CAD files, you can use basic wildcard expression patterns such as the \\* or ? wildcards.
                """

            class _Append(PyParameterCommandArgumentsSubItem):
                """
                Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Select a suitable unit for display in the graphics window.
                """

            class _CreateObjectPer(PyTextualCommandArgumentsSubItem):
                """
                Choose whether to create meshing objects by part, or by selectively customizing the portions of the imported CAD geometry to mesh. If you select by part, then meshing objects are automatically created for you once you import the geometry. Refaceting options are available as well for all meshing objects.
                """

            class _FileLengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Specify the units of length used by this .stl file before loading the CAD file.
                """

            class _FileLengthUnitAppend(PyTextualCommandArgumentsSubItem):
                """
                Specify the units of length used by this .stl file before appending the CAD file.
                """

            class _Route(PyTextualCommandArgumentsSubItem):
                """
                Provides the recommended route in order to import and load the specified CAD file into this task. The default settings are recommended in most cases.  More...
                """

            class _RouteAppend(PyTextualCommandArgumentsSubItem):
                """
                Provides the recommended route in order to import and append the specified CAD file into this task. The default settings are recommended in most cases.  More...
                """

            class _JtLOD(PyTextualCommandArgumentsSubItem):
                """
                Specify the level of detail that you want to include for this .jt file before loading the CAD file.
                """

            class _JtLODAppend(PyTextualCommandArgumentsSubItem):
                """
                Specify the level of detail that you want to include for this .jt file before appending the CAD file.
                """

            class _PartPerBody(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to make all bodies available as individual parts in the CAD Model tree once the CAD file is loaded into the task.
                """

            class _PrefixParentName(PyParameterCommandArgumentsSubItem):
                """
                This applies the name of the component (or assembly) as a prefix to the individual part names when the geometry is loaded into the task.
                """

            class _RemoveEmptyParts(PyParameterCommandArgumentsSubItem):
                """
                Enabled by default, this option lets you import your CAD geometry while removing any empty components.
                """

            class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify the angle at which features will be extracted from the CAD model on import. The smaller the angle, the more features will be captured, thereby taking more time for processing. An angle of 40 degrees is a typical value.
                """

            class _OneZonePer(PyTextualCommandArgumentsSubItem):
                """
                Specify whether to create your meshing zones based on an object, part, body or face. For instance, choosing the face option would create a separate zone for every topological face.
                """

            class _Refaceting(PySingletonCommandArgumentsSubItem):
                """
                Argument Refaceting.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.FacetMaxEdgeLength = self._FacetMaxEdgeLength(self, "FacetMaxEdgeLength", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                    self.Refacet = self._Refacet(self, "Refacet", service, rules, path)
                    self.MaxEdgeLengthFactor = self._MaxEdgeLengthFactor(self, "MaxEdgeLengthFactor", service, rules, path)

                class _FacetMaxEdgeLength(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FacetMaxEdgeLength.
                    """

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NormalAngle.
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Deviation.
                    """

                class _Refacet(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Refacet.
                    """

                class _MaxEdgeLengthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxEdgeLengthFactor.
                    """

            class _IgnoreSolidNames(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to import your CAD geometry while ignoring the names assigned to solids. Note that binary STL files contain a single solid and may have an associated solid name, whereas ASCII STL files contain one or more solids and each can have a  solid name. This option allows to control whether or not to use the name contained in the STL file for naming mesh objects and components.
                """

            class _IgnoreSolidNamesAppend(PyParameterCommandArgumentsSubItem):
                """
                Argument IgnoreSolidNamesAppend.
                """

            class _Options(PySingletonCommandArgumentsSubItem):
                """
                Argument Options.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Solid = self._Solid(self, "Solid", service, rules, path)
                    self.Line = self._Line(self, "Line", service, rules, path)
                    self.Surface = self._Surface(self, "Surface", service, rules, path)

                class _Solid(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Solid.
                    """

                class _Line(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Line.
                    """

                class _Surface(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Surface.
                    """

            class _EdgeExtraction(PyTextualCommandArgumentsSubItem):
                """
                Choose how edges will be extracted from the CAD geometry. Setting this option to auto will extract edges from the CAD geometry when the number of meshing objects is less than 10,000. If this limit is exceeded, then no edges are extracted. When this option is set to yes, then edges are extracted regardless of the number of meshing objects. No edges are extracted when this option is set to no.
                """

            class _Context(PyNumericalCommandArgumentsSubItem):
                """
                Argument Context.
                """

            class _ObjectSetting(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSetting.
                """

            class _RefacetOptions(PySingletonCommandArgumentsSubItem):
                """
                Argument RefacetOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.RefacetDuringLoad = self._RefacetDuringLoad(self, "RefacetDuringLoad", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _RefacetDuringLoad(PyParameterCommandArgumentsSubItem):
                    """
                    Argument RefacetDuringLoad.
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NormalAngle.
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Deviation.
                    """

        def create_instance(self) -> _PartManagementCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._PartManagementCommandArguments(*args)

    class PartReplacementSettings(PyCommand):
        """
        Command PartReplacementSettings.

        Parameters
        ----------
        PartReplacementName : str
            Enter a name for the part replacement object, or keep the default value.
        ManagementMethod : str
            Choose whether the part replacement operation will be an Addition, Replacement, or Removal of a part.
        CreationMethod : str
            Choose the approach for handling meshing for the part replacement task: Surface Mesh Based or Volume Mesh Based. The volume mesh based approach defines a separate region for the area of interest surrounding the part replacement. Volume meshing is performed only in this region and thus is much faster than generating the volume mesh in the entire domain.  The surface mesh approach requires the remeshing of all volume regions.
        OldObjectSelectionList : list[str]
            For part replacement or removal, use this list to pick the original object(s) that you wish to replace or remove. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []).
        NewObjectSelectionList : list[str]
            For part replacement or addition, use this list to pick the new object(s) that you wish to replace or add. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []).
        AdvancedOptions : bool
            Display advanced options that you may want to apply to the task.
        ScalingFactor : float
            Specify a factor to change the size of the bounding box surrounding the selected object(s) for part replacement.
        MptMethodType : str
            Choose how you are going to determine the location of the region around the replacement part - by using numerical inputs directly, or by using the region around the selected object(s).
        GraphicalSelection : bool
            Use this option to have the numerical inputs be automatically filled out based on the centroid of the object(s) selected in the graphics window.
        ShowCoordinates : bool
            Use this option to see the exact coordinate values of the current location point.
        X : float
            Indicates the x-coordinate of the current point location.
        Y : float
            Indicates the y-coordinate of the current point location.
        Z : float
            Indicates the z-coordinate of the current point location.

        Returns
        -------
        bool
        """
        class _PartReplacementSettingsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.PartReplacementName = self._PartReplacementName(self, "PartReplacementName", service, rules, path)
                self.ManagementMethod = self._ManagementMethod(self, "ManagementMethod", service, rules, path)
                self.CreationMethod = self._CreationMethod(self, "CreationMethod", service, rules, path)
                self.OldObjectSelectionList = self._OldObjectSelectionList(self, "OldObjectSelectionList", service, rules, path)
                self.NewObjectSelectionList = self._NewObjectSelectionList(self, "NewObjectSelectionList", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.ScalingFactor = self._ScalingFactor(self, "ScalingFactor", service, rules, path)
                self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                self.GraphicalSelection = self._GraphicalSelection(self, "GraphicalSelection", service, rules, path)
                self.ShowCoordinates = self._ShowCoordinates(self, "ShowCoordinates", service, rules, path)
                self.X = self._X(self, "X", service, rules, path)
                self.Y = self._Y(self, "Y", service, rules, path)
                self.Z = self._Z(self, "Z", service, rules, path)

            class _PartReplacementName(PyTextualCommandArgumentsSubItem):
                """
                Enter a name for the part replacement object, or keep the default value.
                """

            class _ManagementMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose whether the part replacement operation will be an Addition, Replacement, or Removal of a part.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Choose the approach for handling meshing for the part replacement task: Surface Mesh Based or Volume Mesh Based. The volume mesh based approach defines a separate region for the area of interest surrounding the part replacement. Volume meshing is performed only in this region and thus is much faster than generating the volume mesh in the entire domain.  The surface mesh approach requires the remeshing of all volume regions.
                """

            class _OldObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                For part replacement or removal, use this list to pick the original object(s) that you wish to replace or remove. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).
                """

            class _NewObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                For part replacement or addition, use this list to pick the new object(s) that you wish to replace or add. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _ScalingFactor(PyNumericalCommandArgumentsSubItem):
                """
                Specify a factor to change the size of the bounding box surrounding the selected object(s) for part replacement.
                """

            class _MptMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose how you are going to determine the location of the region around the replacement part - by using numerical inputs directly, or by using the region around the selected object(s).
                """

            class _GraphicalSelection(PyParameterCommandArgumentsSubItem):
                """
                Use this option to have the numerical inputs be automatically filled out based on the centroid of the object(s) selected in the graphics window.
                """

            class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                """
                Use this option to see the exact coordinate values of the current location point.
                """

            class _X(PyNumericalCommandArgumentsSubItem):
                """
                Indicates the x-coordinate of the current point location.
                """

            class _Y(PyNumericalCommandArgumentsSubItem):
                """
                Indicates the y-coordinate of the current point location.
                """

            class _Z(PyNumericalCommandArgumentsSubItem):
                """
                Indicates the z-coordinate of the current point location.
                """

        def create_instance(self) -> _PartReplacementSettingsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._PartReplacementSettingsCommandArguments(*args)

    class RemeshSurface(PyCommand):
        """
        Command RemeshSurface.

        Parameters
        ----------
        RemeshSurfaceOption : bool

        Returns
        -------
        bool
        """
        class _RemeshSurfaceCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RemeshSurfaceOption = self._RemeshSurfaceOption(self, "RemeshSurfaceOption", service, rules, path)

            class _RemeshSurfaceOption(PyParameterCommandArgumentsSubItem):
                """
                Argument RemeshSurfaceOption.
                """

        def create_instance(self) -> _RemeshSurfaceCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._RemeshSurfaceCommandArguments(*args)

    class RunCustomJournal(PyCommand):
        """
        Command RunCustomJournal.

        Parameters
        ----------
        JournalString : str
            Enter one or more journal commands.
        PythonJournal : bool
        PrimeJournal : bool

        Returns
        -------
        bool
        """
        class _RunCustomJournalCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.JournalString = self._JournalString(self, "JournalString", service, rules, path)
                self.PythonJournal = self._PythonJournal(self, "PythonJournal", service, rules, path)
                self.PrimeJournal = self._PrimeJournal(self, "PrimeJournal", service, rules, path)

            class _JournalString(PyTextualCommandArgumentsSubItem):
                """
                Enter one or more journal commands.
                """

            class _PythonJournal(PyParameterCommandArgumentsSubItem):
                """
                Argument PythonJournal.
                """

            class _PrimeJournal(PyParameterCommandArgumentsSubItem):
                """
                Argument PrimeJournal.
                """

        def create_instance(self) -> _RunCustomJournalCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._RunCustomJournalCommandArguments(*args)

    class SeparateContacts(PyCommand):
        """
        Command SeparateContacts.

        Parameters
        ----------
        SeparateContactsOption : bool
            Use this option to enable or disable the ability to separate any existing contacts between surfaces.

        Returns
        -------
        bool
        """
        class _SeparateContactsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.SeparateContactsOption = self._SeparateContactsOption(self, "SeparateContactsOption", service, rules, path)

            class _SeparateContactsOption(PyParameterCommandArgumentsSubItem):
                """
                Use this option to enable or disable the ability to separate any existing contacts between surfaces.
                """

        def create_instance(self) -> _SeparateContactsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SeparateContactsCommandArguments(*args)

    class SetUpPeriodicBoundaries(PyCommand):
        """
        Command SetUpPeriodicBoundaries.

        Parameters
        ----------
        MeshObject : str
        Type : str
            Choose the type of periodicity: rotational or translational.
        Method : str
            Choose the method for how you are going to define the periodic boundary. Automatic requires you to select two zones or labels. Manual requires only one zone or label.
        PeriodicityAngle : float
            Specify the angle at which periodicity occurs.
        LCSOrigin : dict[str, Any]
            The X, Y, and Z components of the origin point for the periodic boundary.
        LCSVector : dict[str, Any]
            The X, Y, and Z components of the vector for the periodic boundary.
        TransShift : dict[str, Any]
        SelectionType : str
            Specify whether the periodic boundary is to be applied to an indicated zone or a label.
        ZoneList : list[str]
            Choose from the list of zones, or enter a text string to filter out the list of face zones. Provide text and/or regular expressions in filtering the list (for example, using *, ?, and []).  More...
        LabelList : list[str]
            Choose from the list of zone labels, or enter a text string to filter out the list of face zone labels. Provide text and/or regular expressions in filtering the list (for example, using *, ?, and []).  More...
        TopologyList : list[str]
        RemeshBoundariesOption : str
            Enable this option to remesh boundaries when there is an asymmetric mesh on the periodic faces.
        ZoneLocation : list[str]
        ListAllLabelToggle : bool
            View more labels in the table, such as those for fluid-fluid internal boundaries, in addition to external boundaries.
        AutoMultiplePeriodic : str
        MultipleOption : str

        Returns
        -------
        bool
        """
        class _SetUpPeriodicBoundariesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.Type = self._Type(self, "Type", service, rules, path)
                self.Method = self._Method(self, "Method", service, rules, path)
                self.PeriodicityAngle = self._PeriodicityAngle(self, "PeriodicityAngle", service, rules, path)
                self.LCSOrigin = self._LCSOrigin(self, "LCSOrigin", service, rules, path)
                self.LCSVector = self._LCSVector(self, "LCSVector", service, rules, path)
                self.TransShift = self._TransShift(self, "TransShift", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneList = self._ZoneList(self, "ZoneList", service, rules, path)
                self.LabelList = self._LabelList(self, "LabelList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.RemeshBoundariesOption = self._RemeshBoundariesOption(self, "RemeshBoundariesOption", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ListAllLabelToggle = self._ListAllLabelToggle(self, "ListAllLabelToggle", service, rules, path)
                self.AutoMultiplePeriodic = self._AutoMultiplePeriodic(self, "AutoMultiplePeriodic", service, rules, path)
                self.MultipleOption = self._MultipleOption(self, "MultipleOption", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Choose the type of periodicity: rotational or translational.
                """

            class _Method(PyTextualCommandArgumentsSubItem):
                """
                Choose the method for how you are going to define the periodic boundary. Automatic requires you to select two zones or labels. Manual requires only one zone or label.
                """

            class _PeriodicityAngle(PyNumericalCommandArgumentsSubItem):
                """
                Specify the angle at which periodicity occurs.
                """

            class _LCSOrigin(PySingletonCommandArgumentsSubItem):
                """
                The X, Y, and Z components of the origin point for the periodic boundary.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.OriginY = self._OriginY(self, "OriginY", service, rules, path)
                    self.OriginZ = self._OriginZ(self, "OriginZ", service, rules, path)
                    self.OriginX = self._OriginX(self, "OriginX", service, rules, path)

                class _OriginY(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument OriginY.
                    """

                class _OriginZ(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument OriginZ.
                    """

                class _OriginX(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument OriginX.
                    """

            class _LCSVector(PySingletonCommandArgumentsSubItem):
                """
                The X, Y, and Z components of the vector for the periodic boundary.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.VectorX = self._VectorX(self, "VectorX", service, rules, path)
                    self.VectorZ = self._VectorZ(self, "VectorZ", service, rules, path)
                    self.VectorY = self._VectorY(self, "VectorY", service, rules, path)

                class _VectorX(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VectorX.
                    """

                class _VectorZ(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VectorZ.
                    """

                class _VectorY(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VectorY.
                    """

            class _TransShift(PySingletonCommandArgumentsSubItem):
                """
                Argument TransShift.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShiftY = self._ShiftY(self, "ShiftY", service, rules, path)
                    self.ShiftZ = self._ShiftZ(self, "ShiftZ", service, rules, path)
                    self.ShiftX = self._ShiftX(self, "ShiftX", service, rules, path)

                class _ShiftY(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShiftY.
                    """

                class _ShiftZ(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShiftZ.
                    """

                class _ShiftX(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShiftX.
                    """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Specify whether the periodic boundary is to be applied to an indicated zone or a label.
                """

            class _ZoneList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of zones, or enter a text string to filter out the list of face zones. Provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).  More...
                """

            class _LabelList(PyTextualCommandArgumentsSubItem):
                """
                Choose from the list of zone labels, or enter a text string to filter out the list of face zone labels. Provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).  More...
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _RemeshBoundariesOption(PyTextualCommandArgumentsSubItem):
                """
                Enable this option to remesh boundaries when there is an asymmetric mesh on the periodic faces.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _ListAllLabelToggle(PyParameterCommandArgumentsSubItem):
                """
                View more labels in the table, such as those for fluid-fluid internal boundaries, in addition to external boundaries.
                """

            class _AutoMultiplePeriodic(PyTextualCommandArgumentsSubItem):
                """
                Argument AutoMultiplePeriodic.
                """

            class _MultipleOption(PyTextualCommandArgumentsSubItem):
                """
                Argument MultipleOption.
                """

        def create_instance(self) -> _SetUpPeriodicBoundariesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SetUpPeriodicBoundariesCommandArguments(*args)

    class SetupBoundaryLayers(PyCommand):
        """
        Command SetupBoundaryLayers.

        Parameters
        ----------
        AddChild : str
            Determine whether or not you want to better capture flow in and around the boundary layer of your fluid regions.
        PrismsSettingsName : str
            Specify a name for the boundary layer control or use the default value.
        AspectRatio : float
            Specify the ratio of the prism base length to the prism layer height.
        GrowthRate : float
            Specify the rate of growth of the boundary layer.
        OffsetMethodType : str
            Choose the method that will be used to create the boundary layer, or prism, controls.
        LastRatioPercentage : float
            Specify the offset height of the last layer as a percentage of the local base mesh size.
        FirstHeight : float
            Specify the height of the first layer of cells in the boundary layer.
        PrismLayers : int
            Specify the number of cell layers you require along the boundary.
        RegionSelectionList : list[str]
            Choose one or more regions from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...

        Returns
        -------
        bool
        """
        class _SetupBoundaryLayersCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.PrismsSettingsName = self._PrismsSettingsName(self, "PrismsSettingsName", service, rules, path)
                self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.PrismLayers = self._PrismLayers(self, "PrismLayers", service, rules, path)
                self.RegionSelectionList = self._RegionSelectionList(self, "RegionSelectionList", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Determine whether or not you want to better capture flow in and around the boundary layer of your fluid regions.
                """

            class _PrismsSettingsName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the boundary layer control or use the default value.
                """

            class _AspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Specify the ratio of the prism base length to the prism layer height.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Specify the rate of growth of the boundary layer.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Choose the method that will be used to create the boundary layer, or prism, controls.
                """

            class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                """
                Specify the offset height of the last layer as a percentage of the local base mesh size.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _PrismLayers(PyNumericalCommandArgumentsSubItem):
                """
                Specify the number of cell layers you require along the boundary.
                """

            class _RegionSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Choose one or more regions from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _SetupBoundaryLayersCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SetupBoundaryLayersCommandArguments(*args)

    class ShareTopology(PyCommand):
        """
        Command ShareTopology.

        Parameters
        ----------
        GapDistance : float
            Specify the maximum distance under which gaps will be removed. Use the Show Marked Gaps button to display such gaps.
        GapDistanceConnect : float
            Specify the maximum distance under which gaps will be removed (the default value of 0 is recommended). Use the Show Marked Gaps button to display such gaps.
        STMinSize : float
        InterfaceSelect : str
            Choose whether to have the interface labels selected manually (Manual), automatically (Automatic), or when force share connect topology is utilized in the  geometry (Automatic - Using Connect Topology).
        EdgeLabels : list[str]
        ShareTopologyPreferences : dict[str, Any]
        SMImprovePreferences : dict[str, Any]
        SurfaceMeshPreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ShareTopologyCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GapDistance = self._GapDistance(self, "GapDistance", service, rules, path)
                self.GapDistanceConnect = self._GapDistanceConnect(self, "GapDistanceConnect", service, rules, path)
                self.STMinSize = self._STMinSize(self, "STMinSize", service, rules, path)
                self.InterfaceSelect = self._InterfaceSelect(self, "InterfaceSelect", service, rules, path)
                self.EdgeLabels = self._EdgeLabels(self, "EdgeLabels", service, rules, path)
                self.ShareTopologyPreferences = self._ShareTopologyPreferences(self, "ShareTopologyPreferences", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)
                self.SurfaceMeshPreferences = self._SurfaceMeshPreferences(self, "SurfaceMeshPreferences", service, rules, path)

            class _GapDistance(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum distance under which gaps will be removed. Use the Show Marked Gaps button to display such gaps.
                """

            class _GapDistanceConnect(PyNumericalCommandArgumentsSubItem):
                """
                Specify the maximum distance under which gaps will be removed (the default value of 0 is recommended). Use the Show Marked Gaps button to display such gaps.
                """

            class _STMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument STMinSize.
                """

            class _InterfaceSelect(PyTextualCommandArgumentsSubItem):
                """
                Choose whether to have the interface labels selected manually (Manual), automatically (Automatic), or when force share connect topology is utilized in the  geometry (Automatic - Using Connect Topology).
                """

            class _EdgeLabels(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabels.
                """

            class _ShareTopologyPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument ShareTopologyPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.STRenameInternals = self._STRenameInternals(self, "STRenameInternals", service, rules, path)
                    self.ModelIsPeriodic = self._ModelIsPeriodic(self, "ModelIsPeriodic", service, rules, path)
                    self.ConnectLabelWildcard = self._ConnectLabelWildcard(self, "ConnectLabelWildcard", service, rules, path)
                    self.AllowDefeaturing = self._AllowDefeaturing(self, "AllowDefeaturing", service, rules, path)
                    self.RelativeShareTopologyTolerance = self._RelativeShareTopologyTolerance(self, "RelativeShareTopologyTolerance", service, rules, path)
                    self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                    self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                    self.Operation = self._Operation(self, "Operation", service, rules, path)
                    self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                    self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                    self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                    self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                    self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)

                class _STRenameInternals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument STRenameInternals.
                    """

                class _ModelIsPeriodic(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModelIsPeriodic.
                    """

                class _ConnectLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ConnectLabelWildcard.
                    """

                class _AllowDefeaturing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _RelativeShareTopologyTolerance(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RelativeShareTopologyTolerance.
                    """

                class _ShareTopologyAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShareTopologyAngle.
                    """

                class _ExecuteJoinIntersect(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExecuteJoinIntersect.
                    """

                class _Operation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Operation.
                    """

                class _FluidLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FluidLabelWildcard.
                    """

                class _STToleranceIncrement(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument STToleranceIncrement.
                    """

                class _ShowShareTopologyPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowShareTopologyPreferences.
                    """

                class _PerLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PerLabelList.
                    """

                class _IntfLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IntfLabelList.
                    """

                class _AdvancedImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _NumberOfJoinTries(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfJoinTries.
                    """

            class _SMImprovePreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument SMImprovePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SIStepQualityLimit = self._SIStepQualityLimit(self, "SIStepQualityLimit", service, rules, path)
                    self.SIQualityCollapseLimit = self._SIQualityCollapseLimit(self, "SIQualityCollapseLimit", service, rules, path)
                    self.SIQualityIterations = self._SIQualityIterations(self, "SIQualityIterations", service, rules, path)
                    self.SIQualityMaxAngle = self._SIQualityMaxAngle(self, "SIQualityMaxAngle", service, rules, path)
                    self.AllowDefeaturing = self._AllowDefeaturing(self, "AllowDefeaturing", service, rules, path)
                    self.ShowSMImprovePreferences = self._ShowSMImprovePreferences(self, "ShowSMImprovePreferences", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.SIStepWidth = self._SIStepWidth(self, "SIStepWidth", service, rules, path)
                    self.SIRemoveStep = self._SIRemoveStep(self, "SIRemoveStep", service, rules, path)

                class _SIStepQualityLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepQualityLimit.
                    """

                class _SIQualityCollapseLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityCollapseLimit.
                    """

                class _SIQualityIterations(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityIterations.
                    """

                class _SIQualityMaxAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIQualityMaxAngle.
                    """

                class _AllowDefeaturing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _ShowSMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _AdvancedImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _SIStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepWidth.
                    """

                class _SIRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SIRemoveStep.
                    """

            class _SurfaceMeshPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument SurfaceMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SMQualityCollapseLimit = self._SMQualityCollapseLimit(self, "SMQualityCollapseLimit", service, rules, path)
                    self.AutoMerge = self._AutoMerge(self, "AutoMerge", service, rules, path)
                    self.SMQualityImprove = self._SMQualityImprove(self, "SMQualityImprove", service, rules, path)
                    self.ShowSurfaceMeshPreferences = self._ShowSurfaceMeshPreferences(self, "ShowSurfaceMeshPreferences", service, rules, path)
                    self.SMSeparation = self._SMSeparation(self, "SMSeparation", service, rules, path)
                    self.FoldFaceLimit = self._FoldFaceLimit(self, "FoldFaceLimit", service, rules, path)
                    self.TVMAutoControlCreation = self._TVMAutoControlCreation(self, "TVMAutoControlCreation", service, rules, path)
                    self.SMSeparationAngle = self._SMSeparationAngle(self, "SMSeparationAngle", service, rules, path)
                    self.SMRemoveStep = self._SMRemoveStep(self, "SMRemoveStep", service, rules, path)
                    self.SMStepWidth = self._SMStepWidth(self, "SMStepWidth", service, rules, path)
                    self.SMQualityMaxAngle = self._SMQualityMaxAngle(self, "SMQualityMaxAngle", service, rules, path)
                    self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                    self.VolumeMeshMaxSize = self._VolumeMeshMaxSize(self, "VolumeMeshMaxSize", service, rules, path)
                    self.SelfIntersectCheck = self._SelfIntersectCheck(self, "SelfIntersectCheck", service, rules, path)
                    self.AutoSurfaceRemesh = self._AutoSurfaceRemesh(self, "AutoSurfaceRemesh", service, rules, path)
                    self.SMQualityImproveLimit = self._SMQualityImproveLimit(self, "SMQualityImproveLimit", service, rules, path)
                    self.SetVolumeMeshMaxSize = self._SetVolumeMeshMaxSize(self, "SetVolumeMeshMaxSize", service, rules, path)

                class _SMQualityCollapseLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityCollapseLimit.
                    """

                class _AutoMerge(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoMerge.
                    """

                class _SMQualityImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMQualityImprove.
                    """

                class _ShowSurfaceMeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSurfaceMeshPreferences.
                    """

                class _SMSeparation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMSeparation.
                    """

                class _FoldFaceLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FoldFaceLimit.
                    """

                class _TVMAutoControlCreation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument TVMAutoControlCreation.
                    """

                class _SMSeparationAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMSeparationAngle.
                    """

                class _SMRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMRemoveStep.
                    """

                class _SMStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMStepWidth.
                    """

                class _SMQualityMaxAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityMaxAngle.
                    """

                class _AutoAssignZoneTypes(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoAssignZoneTypes.
                    """

                class _VolumeMeshMaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VolumeMeshMaxSize.
                    """

                class _SelfIntersectCheck(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SelfIntersectCheck.
                    """

                class _AutoSurfaceRemesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoSurfaceRemesh.
                    """

                class _SMQualityImproveLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityImproveLimit.
                    """

                class _SetVolumeMeshMaxSize(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SetVolumeMeshMaxSize.
                    """

        def create_instance(self) -> _ShareTopologyCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ShareTopologyCommandArguments(*args)

    class SizeControlsTable(PyCommand):
        """
        Command SizeControlsTable.

        Parameters
        ----------
        GlobalMin : float
        GlobalMax : float
        TargetGrowthRate : float
        DrawSizeControl : bool
            Enable this field to display the size boxes in the graphics window.
        InitialSizeControl : bool
            Enable this field to display the initial size control in the graphics window.
        TargetSizeControl : bool
            Enable this field to display the target size control in the graphics window.
        SizeControlInterval : float
            Specify the amount of size control boxes to display.
        SizeControlParameters : dict[str, Any]

        Returns
        -------
        bool
        """
        class _SizeControlsTableCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GlobalMin = self._GlobalMin(self, "GlobalMin", service, rules, path)
                self.GlobalMax = self._GlobalMax(self, "GlobalMax", service, rules, path)
                self.TargetGrowthRate = self._TargetGrowthRate(self, "TargetGrowthRate", service, rules, path)
                self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                self.InitialSizeControl = self._InitialSizeControl(self, "InitialSizeControl", service, rules, path)
                self.TargetSizeControl = self._TargetSizeControl(self, "TargetSizeControl", service, rules, path)
                self.SizeControlInterval = self._SizeControlInterval(self, "SizeControlInterval", service, rules, path)
                self.SizeControlParameters = self._SizeControlParameters(self, "SizeControlParameters", service, rules, path)

            class _GlobalMin(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalMin.
                """

            class _GlobalMax(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalMax.
                """

            class _TargetGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument TargetGrowthRate.
                """

            class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Enable this field to display the size boxes in the graphics window.
                """

            class _InitialSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Enable this field to display the initial size control in the graphics window.
                """

            class _TargetSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Enable this field to display the target size control in the graphics window.
                """

            class _SizeControlInterval(PyNumericalCommandArgumentsSubItem):
                """
                Specify the amount of size control boxes to display.
                """

            class _SizeControlParameters(PySingletonCommandArgumentsSubItem):
                """
                Argument SizeControlParameters.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.NewLabelObjects = self._NewLabelObjects(self, "NewLabelObjects", service, rules, path)
                    self.NewLabelResolution = self._NewLabelResolution(self, "NewLabelResolution", service, rules, path)
                    self.NewLabelType = self._NewLabelType(self, "NewLabelType", service, rules, path)
                    self.NewLabelCells = self._NewLabelCells(self, "NewLabelCells", service, rules, path)
                    self.NewLabels = self._NewLabels(self, "NewLabels", service, rules, path)
                    self.NewLabelMax = self._NewLabelMax(self, "NewLabelMax", service, rules, path)
                    self.NewZoneType = self._NewZoneType(self, "NewZoneType", service, rules, path)
                    self.NewLabelCurvature = self._NewLabelCurvature(self, "NewLabelCurvature", service, rules, path)
                    self.NewLabelMin = self._NewLabelMin(self, "NewLabelMin", service, rules, path)

                class _NewLabelObjects(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelObjects.
                    """

                class _NewLabelResolution(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelResolution.
                    """

                class _NewLabelType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelType.
                    """

                class _NewLabelCells(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelCells.
                    """

                class _NewLabels(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabels.
                    """

                class _NewLabelMax(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelMax.
                    """

                class _NewZoneType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewZoneType.
                    """

                class _NewLabelCurvature(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelCurvature.
                    """

                class _NewLabelMin(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelMin.
                    """

        def create_instance(self) -> _SizeControlsTableCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SizeControlsTableCommandArguments(*args)

    class SwitchToSolution(PyCommand):
        """
        Command SwitchToSolution.


        Returns
        -------
        None
        """
        class _SwitchToSolutionCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _SwitchToSolutionCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SwitchToSolutionCommandArguments(*args)

    class TransformVolumeMesh(PyCommand):
        """
        Command TransformVolumeMesh.

        Parameters
        ----------
        MTControlName : str
            Specify a name for the transformation or use the default value.
        Type : str
            Indicate the type of transformation: translational or rotational
        Method : str
            By default, the Manual method is utilized, however, when periodics are detected, then Automatic - use existing periodics is the default.
        SelectionType : str
        TopoBodyList : list[str]
        CellZoneList : list[str]
            Select one or more objects from the list to which you will apply the transformation. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        LCSOrigin : dict[str, Any]
            Specify the coordinates of the rotational origin.
        LCSVector : dict[str, Any]
            Specify the coordinates of the rotational vector.
        TransShift : dict[str, Any]
            Specify the coordinates of the translational shift.
        Angle : float
            Specify a value for the angle of rotation for this transformation.
        Copy : str
            Indicate whether or not to make a copy of the volume mesh and apply the transformation to the copy.
        NumOfCopies : int
            Specify the number of copies that you want to make for this transformation.
        Merge : str
            Indicate whether or not you want to merge cell and face zones prior to transforming the volume mesh, in order to avoid duplication.
        Rename : str
            Indicate whether or not you want to rename cell and face zones prior to transforming the volume mesh.
        MergeBoundaries : list[str]

        Returns
        -------
        bool
        """
        class _TransformVolumeMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MTControlName = self._MTControlName(self, "MTControlName", service, rules, path)
                self.Type = self._Type(self, "Type", service, rules, path)
                self.Method = self._Method(self, "Method", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.TopoBodyList = self._TopoBodyList(self, "TopoBodyList", service, rules, path)
                self.CellZoneList = self._CellZoneList(self, "CellZoneList", service, rules, path)
                self.LCSOrigin = self._LCSOrigin(self, "LCSOrigin", service, rules, path)
                self.LCSVector = self._LCSVector(self, "LCSVector", service, rules, path)
                self.TransShift = self._TransShift(self, "TransShift", service, rules, path)
                self.Angle = self._Angle(self, "Angle", service, rules, path)
                self.Copy = self._Copy(self, "Copy", service, rules, path)
                self.NumOfCopies = self._NumOfCopies(self, "NumOfCopies", service, rules, path)
                self.Merge = self._Merge(self, "Merge", service, rules, path)
                self.Rename = self._Rename(self, "Rename", service, rules, path)
                self.MergeBoundaries = self._MergeBoundaries(self, "MergeBoundaries", service, rules, path)

            class _MTControlName(PyTextualCommandArgumentsSubItem):
                """
                Specify a name for the transformation or use the default value.
                """

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Indicate the type of transformation: translational or rotational
                """

            class _Method(PyTextualCommandArgumentsSubItem):
                """
                By default, the Manual method is utilized, however, when periodics are detected, then Automatic - use existing periodics is the default.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _TopoBodyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopoBodyList.
                """

            class _CellZoneList(PyTextualCommandArgumentsSubItem):
                """
                Select one or more objects from the list to which you will apply the transformation. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LCSOrigin(PySingletonCommandArgumentsSubItem):
                """
                Specify the coordinates of the rotational origin.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.OriginY = self._OriginY(self, "OriginY", service, rules, path)
                    self.OriginZ = self._OriginZ(self, "OriginZ", service, rules, path)
                    self.OriginX = self._OriginX(self, "OriginX", service, rules, path)

                class _OriginY(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument OriginY.
                    """

                class _OriginZ(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument OriginZ.
                    """

                class _OriginX(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument OriginX.
                    """

            class _LCSVector(PySingletonCommandArgumentsSubItem):
                """
                Specify the coordinates of the rotational vector.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.VectorX = self._VectorX(self, "VectorX", service, rules, path)
                    self.VectorZ = self._VectorZ(self, "VectorZ", service, rules, path)
                    self.VectorY = self._VectorY(self, "VectorY", service, rules, path)

                class _VectorX(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VectorX.
                    """

                class _VectorZ(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VectorZ.
                    """

                class _VectorY(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument VectorY.
                    """

            class _TransShift(PySingletonCommandArgumentsSubItem):
                """
                Specify the coordinates of the translational shift.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShiftY = self._ShiftY(self, "ShiftY", service, rules, path)
                    self.ShiftZ = self._ShiftZ(self, "ShiftZ", service, rules, path)
                    self.ShiftX = self._ShiftX(self, "ShiftX", service, rules, path)

                class _ShiftY(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShiftY.
                    """

                class _ShiftZ(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShiftZ.
                    """

                class _ShiftX(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShiftX.
                    """

            class _Angle(PyNumericalCommandArgumentsSubItem):
                """
                Specify a value for the angle of rotation for this transformation.
                """

            class _Copy(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether or not to make a copy of the volume mesh and apply the transformation to the copy.
                """

            class _NumOfCopies(PyNumericalCommandArgumentsSubItem):
                """
                Specify the number of copies that you want to make for this transformation.
                """

            class _Merge(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether or not you want to merge cell and face zones prior to transforming the volume mesh, in order to avoid duplication.
                """

            class _Rename(PyTextualCommandArgumentsSubItem):
                """
                Indicate whether or not you want to rename cell and face zones prior to transforming the volume mesh.
                """

            class _MergeBoundaries(PyTextualCommandArgumentsSubItem):
                """
                Argument MergeBoundaries.
                """

        def create_instance(self) -> _TransformVolumeMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TransformVolumeMeshCommandArguments(*args)

    class UpdateBoundaries(PyCommand):
        """
        Command UpdateBoundaries.

        Parameters
        ----------
        MeshObject : str
        SelectionType : str
            Choose how boundaries are displayed in the table.
        BoundaryLabelList : list[str]
        BoundaryLabelTypeList : list[str]
        BoundaryZoneList : list[str]
        BoundaryZoneTypeList : list[str]
        OldBoundaryLabelList : list[str]
        OldBoundaryLabelTypeList : list[str]
        OldBoundaryZoneList : list[str]
        OldBoundaryZoneTypeList : list[str]
        OldLabelZoneList : list[str]
        ListAllBoundariesToggle : bool
            View more boundaries in the table, such as fluid-fluid internal boundaries, in addition to external boundaries.
        ZoneLocation : list[str]
        TopologyList : list[str]
        TopologyTypeList : list[str]
        OldTopologyList : list[str]
        OldTopologyTypeList : list[str]
        BoundaryCurrentList : list[str]
        BoundaryCurrentTypeList : list[str]
        BoundaryAllowedTypeList : list[str]

        Returns
        -------
        bool
        """
        class _UpdateBoundariesCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.BoundaryLabelList = self._BoundaryLabelList(self, "BoundaryLabelList", service, rules, path)
                self.BoundaryLabelTypeList = self._BoundaryLabelTypeList(self, "BoundaryLabelTypeList", service, rules, path)
                self.BoundaryZoneList = self._BoundaryZoneList(self, "BoundaryZoneList", service, rules, path)
                self.BoundaryZoneTypeList = self._BoundaryZoneTypeList(self, "BoundaryZoneTypeList", service, rules, path)
                self.OldBoundaryLabelList = self._OldBoundaryLabelList(self, "OldBoundaryLabelList", service, rules, path)
                self.OldBoundaryLabelTypeList = self._OldBoundaryLabelTypeList(self, "OldBoundaryLabelTypeList", service, rules, path)
                self.OldBoundaryZoneList = self._OldBoundaryZoneList(self, "OldBoundaryZoneList", service, rules, path)
                self.OldBoundaryZoneTypeList = self._OldBoundaryZoneTypeList(self, "OldBoundaryZoneTypeList", service, rules, path)
                self.OldLabelZoneList = self._OldLabelZoneList(self, "OldLabelZoneList", service, rules, path)
                self.ListAllBoundariesToggle = self._ListAllBoundariesToggle(self, "ListAllBoundariesToggle", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.TopologyTypeList = self._TopologyTypeList(self, "TopologyTypeList", service, rules, path)
                self.OldTopologyList = self._OldTopologyList(self, "OldTopologyList", service, rules, path)
                self.OldTopologyTypeList = self._OldTopologyTypeList(self, "OldTopologyTypeList", service, rules, path)
                self.BoundaryCurrentList = self._BoundaryCurrentList(self, "BoundaryCurrentList", service, rules, path)
                self.BoundaryCurrentTypeList = self._BoundaryCurrentTypeList(self, "BoundaryCurrentTypeList", service, rules, path)
                self.BoundaryAllowedTypeList = self._BoundaryAllowedTypeList(self, "BoundaryAllowedTypeList", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Choose how boundaries are displayed in the table.
                """

            class _BoundaryLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryLabelList.
                """

            class _BoundaryLabelTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryLabelTypeList.
                """

            class _BoundaryZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryZoneList.
                """

            class _BoundaryZoneTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryZoneTypeList.
                """

            class _OldBoundaryLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldBoundaryLabelList.
                """

            class _OldBoundaryLabelTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldBoundaryLabelTypeList.
                """

            class _OldBoundaryZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldBoundaryZoneList.
                """

            class _OldBoundaryZoneTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldBoundaryZoneTypeList.
                """

            class _OldLabelZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldLabelZoneList.
                """

            class _ListAllBoundariesToggle(PyParameterCommandArgumentsSubItem):
                """
                View more boundaries in the table, such as fluid-fluid internal boundaries, in addition to external boundaries.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _TopologyTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyTypeList.
                """

            class _OldTopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldTopologyList.
                """

            class _OldTopologyTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldTopologyTypeList.
                """

            class _BoundaryCurrentList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryCurrentList.
                """

            class _BoundaryCurrentTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryCurrentTypeList.
                """

            class _BoundaryAllowedTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryAllowedTypeList.
                """

        def create_instance(self) -> _UpdateBoundariesCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateBoundariesCommandArguments(*args)

    class UpdateRegionSettings(PyCommand):
        """
        Command UpdateRegionSettings.

        Parameters
        ----------
        MainFluidRegion : str
            Identify the main fluid region for your simulation.
        FilterCategory : str
            Select how your regions will be displayed in the table. You can choose to view all regions, or specifically identified regions, or only object-based regions.
        RegionNameList : list[str]
        RegionMeshMethodList : list[str]
        RegionTypeList : list[str]
        RegionVolumeFillList : list[str]
        RegionLeakageSizeList : list[str]
        RegionOversetComponenList : list[str]
        OldRegionNameList : list[str]
        OldRegionMeshMethodList : list[str]
        OldRegionTypeList : list[str]
        OldRegionVolumeFillList : list[str]
        OldRegionLeakageSizeList : list[str]
        OldRegionOversetComponenList : list[str]
        AllRegionNameList : list[str]
        AllRegionMeshMethodList : list[str]
        AllRegionTypeList : list[str]
        AllRegionVolumeFillList : list[str]
        AllRegionLeakageSizeList : list[str]
        AllRegionOversetComponenList : list[str]
        AllRegionLinkedConstructionSurfaceList : list[str]
        AllRegionSourceList : list[str]
        AllRegionFilterCategories : list[str]

        Returns
        -------
        bool
        """
        class _UpdateRegionSettingsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MainFluidRegion = self._MainFluidRegion(self, "MainFluidRegion", service, rules, path)
                self.FilterCategory = self._FilterCategory(self, "FilterCategory", service, rules, path)
                self.RegionNameList = self._RegionNameList(self, "RegionNameList", service, rules, path)
                self.RegionMeshMethodList = self._RegionMeshMethodList(self, "RegionMeshMethodList", service, rules, path)
                self.RegionTypeList = self._RegionTypeList(self, "RegionTypeList", service, rules, path)
                self.RegionVolumeFillList = self._RegionVolumeFillList(self, "RegionVolumeFillList", service, rules, path)
                self.RegionLeakageSizeList = self._RegionLeakageSizeList(self, "RegionLeakageSizeList", service, rules, path)
                self.RegionOversetComponenList = self._RegionOversetComponenList(self, "RegionOversetComponenList", service, rules, path)
                self.OldRegionNameList = self._OldRegionNameList(self, "OldRegionNameList", service, rules, path)
                self.OldRegionMeshMethodList = self._OldRegionMeshMethodList(self, "OldRegionMeshMethodList", service, rules, path)
                self.OldRegionTypeList = self._OldRegionTypeList(self, "OldRegionTypeList", service, rules, path)
                self.OldRegionVolumeFillList = self._OldRegionVolumeFillList(self, "OldRegionVolumeFillList", service, rules, path)
                self.OldRegionLeakageSizeList = self._OldRegionLeakageSizeList(self, "OldRegionLeakageSizeList", service, rules, path)
                self.OldRegionOversetComponenList = self._OldRegionOversetComponenList(self, "OldRegionOversetComponenList", service, rules, path)
                self.AllRegionNameList = self._AllRegionNameList(self, "AllRegionNameList", service, rules, path)
                self.AllRegionMeshMethodList = self._AllRegionMeshMethodList(self, "AllRegionMeshMethodList", service, rules, path)
                self.AllRegionTypeList = self._AllRegionTypeList(self, "AllRegionTypeList", service, rules, path)
                self.AllRegionVolumeFillList = self._AllRegionVolumeFillList(self, "AllRegionVolumeFillList", service, rules, path)
                self.AllRegionLeakageSizeList = self._AllRegionLeakageSizeList(self, "AllRegionLeakageSizeList", service, rules, path)
                self.AllRegionOversetComponenList = self._AllRegionOversetComponenList(self, "AllRegionOversetComponenList", service, rules, path)
                self.AllRegionLinkedConstructionSurfaceList = self._AllRegionLinkedConstructionSurfaceList(self, "AllRegionLinkedConstructionSurfaceList", service, rules, path)
                self.AllRegionSourceList = self._AllRegionSourceList(self, "AllRegionSourceList", service, rules, path)
                self.AllRegionFilterCategories = self._AllRegionFilterCategories(self, "AllRegionFilterCategories", service, rules, path)

            class _MainFluidRegion(PyTextualCommandArgumentsSubItem):
                """
                Identify the main fluid region for your simulation.
                """

            class _FilterCategory(PyTextualCommandArgumentsSubItem):
                """
                Select how your regions will be displayed in the table. You can choose to view all regions, or specifically identified regions, or only object-based regions.
                """

            class _RegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionMeshMethodList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionMeshMethodList.
                """

            class _RegionTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionTypeList.
                """

            class _RegionVolumeFillList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionVolumeFillList.
                """

            class _RegionLeakageSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionLeakageSizeList.
                """

            class _RegionOversetComponenList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionOversetComponenList.
                """

            class _OldRegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionMeshMethodList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionMeshMethodList.
                """

            class _OldRegionTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionTypeList.
                """

            class _OldRegionVolumeFillList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionVolumeFillList.
                """

            class _OldRegionLeakageSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionLeakageSizeList.
                """

            class _OldRegionOversetComponenList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionOversetComponenList.
                """

            class _AllRegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionNameList.
                """

            class _AllRegionMeshMethodList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionMeshMethodList.
                """

            class _AllRegionTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionTypeList.
                """

            class _AllRegionVolumeFillList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionVolumeFillList.
                """

            class _AllRegionLeakageSizeList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionLeakageSizeList.
                """

            class _AllRegionOversetComponenList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionOversetComponenList.
                """

            class _AllRegionLinkedConstructionSurfaceList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionLinkedConstructionSurfaceList.
                """

            class _AllRegionSourceList(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionSourceList.
                """

            class _AllRegionFilterCategories(PyTextualCommandArgumentsSubItem):
                """
                Argument AllRegionFilterCategories.
                """

        def create_instance(self) -> _UpdateRegionSettingsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateRegionSettingsCommandArguments(*args)

    class UpdateRegions(PyCommand):
        """
        Command UpdateRegions.

        Parameters
        ----------
        MeshObject : str
        RegionNameList : list[str]
        RegionTypeList : list[str]
        OldRegionNameList : list[str]
        OldRegionTypeList : list[str]
        RegionInternals : list[str]
        RegionInternalTypes : list[str]
        RegionCurrentList : list[str]
        RegionCurrentTypeList : list[str]
        NumberOfListedRegions : int

        Returns
        -------
        bool
        """
        class _UpdateRegionsCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.RegionNameList = self._RegionNameList(self, "RegionNameList", service, rules, path)
                self.RegionTypeList = self._RegionTypeList(self, "RegionTypeList", service, rules, path)
                self.OldRegionNameList = self._OldRegionNameList(self, "OldRegionNameList", service, rules, path)
                self.OldRegionTypeList = self._OldRegionTypeList(self, "OldRegionTypeList", service, rules, path)
                self.RegionInternals = self._RegionInternals(self, "RegionInternals", service, rules, path)
                self.RegionInternalTypes = self._RegionInternalTypes(self, "RegionInternalTypes", service, rules, path)
                self.RegionCurrentList = self._RegionCurrentList(self, "RegionCurrentList", service, rules, path)
                self.RegionCurrentTypeList = self._RegionCurrentTypeList(self, "RegionCurrentTypeList", service, rules, path)
                self.NumberOfListedRegions = self._NumberOfListedRegions(self, "NumberOfListedRegions", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _RegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionTypeList.
                """

            class _OldRegionNameList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldRegionTypeList.
                """

            class _RegionInternals(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionInternals.
                """

            class _RegionInternalTypes(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionInternalTypes.
                """

            class _RegionCurrentList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionCurrentList.
                """

            class _RegionCurrentTypeList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionCurrentTypeList.
                """

            class _NumberOfListedRegions(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfListedRegions.
                """

        def create_instance(self) -> _UpdateRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateRegionsCommandArguments(*args)

    class UpdateTheVolumeMesh(PyCommand):
        """
        Command UpdateTheVolumeMesh.

        Parameters
        ----------
        EnableParallel : bool
            Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.

        Returns
        -------
        bool
        """
        class _UpdateTheVolumeMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.EnableParallel = self._EnableParallel(self, "EnableParallel", service, rules, path)

            class _EnableParallel(PyParameterCommandArgumentsSubItem):
                """
                Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.
                """

        def create_instance(self) -> _UpdateTheVolumeMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateTheVolumeMeshCommandArguments(*args)

    class WrapMain(PyCommand):
        """
        Command WrapMain.

        Parameters
        ----------
        WrapRegionsName : str

        Returns
        -------
        bool
        """
        class _WrapMainCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.WrapRegionsName = self._WrapRegionsName(self, "WrapRegionsName", service, rules, path)

            class _WrapRegionsName(PyTextualCommandArgumentsSubItem):
                """
                Argument WrapRegionsName.
                """

        def create_instance(self) -> _WrapMainCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._WrapMainCommandArguments(*args)

    class Write2dMesh(PyCommand):
        """
        Command Write2dMesh.

        Parameters
        ----------
        FileName : str
        SkipExport : bool

        Returns
        -------
        bool
        """
        class _Write2dMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileName = self._FileName(self, "FileName", service, rules, path)
                self.SkipExport = self._SkipExport(self, "SkipExport", service, rules, path)

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Argument FileName.
                """

            class _SkipExport(PyParameterCommandArgumentsSubItem):
                """
                Argument SkipExport.
                """

        def create_instance(self) -> _Write2dMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._Write2dMeshCommandArguments(*args)

    class WriteSkinMesh(PyCommand):
        """
        Command WriteSkinMesh.

        Parameters
        ----------
        FileName : str

        Returns
        -------
        bool
        """
        class _WriteSkinMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileName = self._FileName(self, "FileName", service, rules, path)

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Argument FileName.
                """

        def create_instance(self) -> _WriteSkinMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._WriteSkinMeshCommandArguments(*args)

