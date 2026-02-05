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
        self.AxisymmetricSweep = self.__class__.AxisymmetricSweep(service, rules, "AxisymmetricSweep", path)
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
        self.CreateGroup = self.__class__.CreateGroup(service, rules, "CreateGroup", path)
        self.CreateLeakShield = self.__class__.CreateLeakShield(service, rules, "CreateLeakShield", path)
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
            class _CloseArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _CloseArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._CloseArguments(*args)

        class Compute(PyCommand):
            """
            Command Compute.


            Returns
            -------
            None
            """
            class _ComputeArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _ComputeArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ComputeArguments(*args)

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
            class _DiagOptionsArguments(PyArguments):
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

                class _Option(PyArgumentsTextualSubItem):
                    """
                    Argument Option.
                    """

                class _Measure(PyArgumentsTextualSubItem):
                    """
                    Argument Measure.
                    """

                class _Average(PyArgumentsNumericalSubItem):
                    """
                    Argument Average.
                    """

                class _Minimum(PyArgumentsNumericalSubItem):
                    """
                    Argument Minimum.
                    """

                class _Maximum(PyArgumentsNumericalSubItem):
                    """
                    Argument Maximum.
                    """

                class _MarkRangeType(PyArgumentsTextualSubItem):
                    """
                    Argument MarkRangeType.
                    """

                class _MarkMin(PyArgumentsNumericalSubItem):
                    """
                    Argument MarkMin.
                    """

                class _MarkMax(PyArgumentsNumericalSubItem):
                    """
                    Argument MarkMax.
                    """

                class _Selected(PyArgumentsTextualSubItem):
                    """
                    Argument Selected.
                    """

                class _MarkedCount(PyArgumentsNumericalSubItem):
                    """
                    Argument MarkedCount.
                    """

                class _CurrentCount(PyArgumentsNumericalSubItem):
                    """
                    Argument CurrentCount.
                    """

                class _ExtentsUpdateBounds(PyArgumentsParameterSubItem):
                    """
                    Argument ExtentsUpdateBounds.
                    """

                class _ExtentsXMin(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtentsXMin.
                    """

                class _ExtentsYMin(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtentsYMin.
                    """

                class _ExtentsZMin(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtentsZMin.
                    """

                class _ExtentsXMax(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtentsXMax.
                    """

                class _ExtentsYMax(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtentsYMax.
                    """

                class _ExtentsZMax(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtentsZMax.
                    """

            def create_instance(self) -> _DiagOptionsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DiagOptionsArguments(*args)

        class Draw(PyCommand):
            """
            Command Draw.


            Returns
            -------
            None
            """
            class _DrawArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _DrawArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DrawArguments(*args)

        class First(PyCommand):
            """
            Command First.


            Returns
            -------
            None
            """
            class _FirstArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _FirstArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._FirstArguments(*args)

        class Histogram(PyCommand):
            """
            Command Histogram.


            Returns
            -------
            None
            """
            class _HistogramArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _HistogramArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._HistogramArguments(*args)

        class Ignore(PyCommand):
            """
            Command Ignore.


            Returns
            -------
            None
            """
            class _IgnoreArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _IgnoreArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._IgnoreArguments(*args)

        class List(PyCommand):
            """
            Command List.


            Returns
            -------
            None
            """
            class _ListArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _ListArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ListArguments(*args)

        class Mark(PyCommand):
            """
            Command Mark.


            Returns
            -------
            None
            """
            class _MarkArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _MarkArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._MarkArguments(*args)

        class Next(PyCommand):
            """
            Command Next.


            Returns
            -------
            None
            """
            class _NextArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _NextArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._NextArguments(*args)

        class Previous(PyCommand):
            """
            Command Previous.


            Returns
            -------
            None
            """
            class _PreviousArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _PreviousArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._PreviousArguments(*args)

        class Restore(PyCommand):
            """
            Command Restore.


            Returns
            -------
            None
            """
            class _RestoreArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _RestoreArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._RestoreArguments(*args)

        class Summary(PyCommand):
            """
            Command Summary.


            Returns
            -------
            None
            """
            class _SummaryArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _SummaryArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._SummaryArguments(*args)

        class Update(PyCommand):
            """
            Command Update.


            Returns
            -------
            None
            """
            class _UpdateArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _UpdateArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._UpdateArguments(*args)

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
            class _ReadCaseArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadCaseArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadCaseArguments(*args)

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
            class _ReadJournalArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)
                    self.ChangeDirectory = self._ChangeDirectory(self, "ChangeDirectory", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

                class _ChangeDirectory(PyArgumentsParameterSubItem):
                    """
                    Argument ChangeDirectory.
                    """

            def create_instance(self) -> _ReadJournalArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadJournalArguments(*args)

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
            class _ReadMeshArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _ReadMeshArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ReadMeshArguments(*args)

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
            class _StartJournalArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _StartJournalArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._StartJournalArguments(*args)

        class StopJournal(PyCommand):
            """
            Command StopJournal.


            Returns
            -------
            None
            """
            class _StopJournalArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _StopJournalArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._StopJournalArguments(*args)

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
            class _WriteCaseArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _WriteCaseArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteCaseArguments(*args)

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
            class _WriteMeshArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.FileName = self._FileName(self, "FileName", service, rules, path)

                class _FileName(PyArgumentsTextualSubItem):
                    """
                    Argument FileName.
                    """

            def create_instance(self) -> _WriteMeshArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._WriteMeshArguments(*args)

    class GlobalSettings(PyMenu):
        """
        Singleton GlobalSettings.
        """
        def __init__(self, service, rules, path):
            self.FTMRegionData = self.__class__.FTMRegionData(service, rules, path + [("FTMRegionData", "")])
            self.AreaUnit = self.__class__.AreaUnit(service, rules, path + [("AreaUnit", "")])
            self.CurrentTask = self.__class__.CurrentTask(service, rules, path + [("CurrentTask", "")])
            self.EnableCleanCAD = self.__class__.EnableCleanCAD(service, rules, path + [("EnableCleanCAD", "")])
            self.EnableComplexMeshing = self.__class__.EnableComplexMeshing(service, rules, path + [("EnableComplexMeshing", "")])
            self.EnableOversetMeshing = self.__class__.EnableOversetMeshing(service, rules, path + [("EnableOversetMeshing", "")])
            self.EnablePrime2dMeshing = self.__class__.EnablePrime2dMeshing(service, rules, path + [("EnablePrime2dMeshing", "")])
            self.EnablePrimeMeshing = self.__class__.EnablePrimeMeshing(service, rules, path + [("EnablePrimeMeshing", "")])
            self.InitialVersion = self.__class__.InitialVersion(service, rules, path + [("InitialVersion", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            self.NormalMode = self.__class__.NormalMode(service, rules, path + [("NormalMode", "")])
            self.OldSize = self.__class__.OldSize(service, rules, path + [("OldSize", "")])
            self.UTLEnabled = self.__class__.UTLEnabled(service, rules, path + [("UTLEnabled", "")])
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

        class CurrentTask(PyTextual):
            """
            Parameter CurrentTask of value type str.
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

        class OldSize(PyNumerical):
            """
            Parameter OldSize of value type float.
            """
            pass

        class UTLEnabled(PyParameter):
            """
            Parameter UTLEnabled of value type bool.
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
            self.Regions = self.__class__.Regions(service, rules, path + [("Regions", "")])
            self.ClippingPlane = self.__class__.ClippingPlane(service, rules, "ClippingPlane", path)
            self.DrawThinVolumeRegions = self.__class__.DrawThinVolumeRegions(service, rules, "DrawThinVolumeRegions", path)
            self.GetClippingZoneIDs = self.__class__.GetClippingZoneIDs(service, rules, "GetClippingZoneIDs", path)
            self.GetVisibleDomainBounds = self.__class__.GetVisibleDomainBounds(service, rules, "GetVisibleDomainBounds", path)
            self.MarkGaps = self.__class__.MarkGaps(service, rules, "MarkGaps", path)
            super().__init__(service, rules, path)

        class Bounds(PyMenu):
            """
            Singleton Bounds.
            """
            def __init__(self, service, rules, path):
                self.BoundX = self.__class__.BoundX(service, rules, path + [("BoundX", "")])
                self.BoundY = self.__class__.BoundY(service, rules, path + [("BoundY", "")])
                self.BoundZ = self.__class__.BoundZ(service, rules, path + [("BoundZ", "")])
                self.DeltaValue = self.__class__.DeltaValue(service, rules, path + [("DeltaValue", "")])
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

            class DeltaValue(PyNumerical):
                """
                Parameter DeltaValue of value type float.
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
                class _ResetBoundsArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _ResetBoundsArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._ResetBoundsArguments(*args)

            class SetBounds(PyCommand):
                """
                Command SetBounds.

                Parameters
                ----------
                Value : float

                Returns
                -------
                None
                """
                class _SetBoundsArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)
                        self.Value = self._Value(self, "Value", service, rules, path)

                    class _Value(PyArgumentsNumericalSubItem):
                        """
                        Argument Value.
                        """

                def create_instance(self) -> _SetBoundsArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._SetBoundsArguments(*args)

        class Regions(PyMenu):
            """
            Singleton Regions.
            """
            def __init__(self, service, rules, path):
                self.DrawAll = self.__class__.DrawAll(service, rules, "DrawAll", path)
                self.DrawDead = self.__class__.DrawDead(service, rules, "DrawDead", path)
                self.DrawFluid = self.__class__.DrawFluid(service, rules, "DrawFluid", path)
                self.DrawSolid = self.__class__.DrawSolid(service, rules, "DrawSolid", path)
                super().__init__(service, rules, path)

            class DrawAll(PyCommand):
                """
                Command DrawAll.


                Returns
                -------
                None
                """
                class _DrawAllArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DrawAllArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DrawAllArguments(*args)

            class DrawDead(PyCommand):
                """
                Command DrawDead.


                Returns
                -------
                None
                """
                class _DrawDeadArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DrawDeadArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DrawDeadArguments(*args)

            class DrawFluid(PyCommand):
                """
                Command DrawFluid.


                Returns
                -------
                None
                """
                class _DrawFluidArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DrawFluidArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DrawFluidArguments(*args)

            class DrawSolid(PyCommand):
                """
                Command DrawSolid.


                Returns
                -------
                None
                """
                class _DrawSolidArguments(PyArguments):
                    def __init__(self, service, rules, command, path, id):
                        super().__init__(service, rules, command, path, id)

                def create_instance(self) -> _DrawSolidArguments:
                    args = self._get_create_instance_args()
                    if args is not None:
                        return self._DrawSolidArguments(*args)

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
            class _ClippingPlaneArguments(PyArguments):
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

                class _InsertClippingPlane(PyArgumentsParameterSubItem):
                    """
                    Argument InsertClippingPlane.
                    """

                class _DrawCellLayer(PyArgumentsParameterSubItem):
                    """
                    Argument DrawCellLayer.
                    """

                class _FreezeCellLayer(PyArgumentsParameterSubItem):
                    """
                    Argument FreezeCellLayer.
                    """

                class _FlipClippingPlane(PyArgumentsParameterSubItem):
                    """
                    Argument FlipClippingPlane.
                    """

                class _PointCoordinates(PyArgumentsNumericalSubItem):
                    """
                    Argument PointCoordinates.
                    """

                class _PlaneNormal(PyArgumentsNumericalSubItem):
                    """
                    Argument PlaneNormal.
                    """

                class _SliderPosition(PyArgumentsNumericalSubItem):
                    """
                    Argument SliderPosition.
                    """

                class _CutDirection(PyArgumentsTextualSubItem):
                    """
                    Argument CutDirection.
                    """

            def create_instance(self) -> _ClippingPlaneArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._ClippingPlaneArguments(*args)

        class DrawThinVolumeRegions(PyCommand):
            """
            Command DrawThinVolumeRegions.

            Parameters
            ----------
            TaskInstanceName : str

            Returns
            -------
            None
            """
            class _DrawThinVolumeRegionsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.TaskInstanceName = self._TaskInstanceName(self, "TaskInstanceName", service, rules, path)

                class _TaskInstanceName(PyArgumentsTextualSubItem):
                    """
                    Argument TaskInstanceName.
                    """

            def create_instance(self) -> _DrawThinVolumeRegionsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._DrawThinVolumeRegionsArguments(*args)

        class GetClippingZoneIDs(PyCommand):
            """
            Command GetClippingZoneIDs.


            Returns
            -------
            None
            """
            class _GetClippingZoneIDsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _GetClippingZoneIDsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._GetClippingZoneIDsArguments(*args)

        class GetVisibleDomainBounds(PyCommand):
            """
            Command GetVisibleDomainBounds.


            Returns
            -------
            None
            """
            class _GetVisibleDomainBoundsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)

            def create_instance(self) -> _GetVisibleDomainBoundsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._GetVisibleDomainBoundsArguments(*args)

        class MarkGaps(PyCommand):
            """
            Command MarkGaps.

            Parameters
            ----------
            GapDistance : float
            GapDistanceConnect : float
            STMinSize : float
            ShareTopologyPreferences : dict[str, Any]

            Returns
            -------
            None
            """
            class _MarkGapsArguments(PyArguments):
                def __init__(self, service, rules, command, path, id):
                    super().__init__(service, rules, command, path, id)
                    self.GapDistance = self._GapDistance(self, "GapDistance", service, rules, path)
                    self.GapDistanceConnect = self._GapDistanceConnect(self, "GapDistanceConnect", service, rules, path)
                    self.STMinSize = self._STMinSize(self, "STMinSize", service, rules, path)
                    self.ShareTopologyPreferences = self._ShareTopologyPreferences(self, "ShareTopologyPreferences", service, rules, path)

                class _GapDistance(PyArgumentsNumericalSubItem):
                    """
                    Argument GapDistance.
                    """

                class _GapDistanceConnect(PyArgumentsNumericalSubItem):
                    """
                    Argument GapDistanceConnect.
                    """

                class _STMinSize(PyArgumentsNumericalSubItem):
                    """
                    Argument STMinSize.
                    """

                class _ShareTopologyPreferences(PyArgumentsSingletonSubItem):
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
                        self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                        self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                        self.Operation = self._Operation(self, "Operation", service, rules, path)
                        self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                        self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                        self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                        self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                        self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                        self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                        self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)

                    class _STRenameInternals(PyArgumentsTextualSubItem):
                        """
                        Choose whether or not to apply body names from the imported geometry and use them in naming internal boundaries.  For instance, the internal face between two regions solid and body would be renamed to solid-body.
                        """

                    class _ModelIsPeriodic(PyArgumentsTextualSubItem):
                        """
                        Choose whether or not you need to set up periodic boundaries. If you select yes, then choose your periodic boundaries from the list of available boundaries.
                        """

                    class _ConnectLabelWildcard(PyArgumentsTextualSubItem):
                        """
                        Enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                        """

                    class _AllowDefeaturing(PyArgumentsTextualSubItem):
                        """
                        Argument AllowDefeaturing.
                        """

                    class _RelativeShareTopologyTolerance(PyArgumentsNumericalSubItem):
                        """
                        Specify the relative tolerance for joining or intersecting face pairs, or the relative tolerance for connecting edge and face pairs.
                        """

                    class _FluidLabelWildcard(PyArgumentsTextualSubItem):
                        """
                        Argument FluidLabelWildcard.
                        """

                    class _ExecuteJoinIntersect(PyArgumentsTextualSubItem):
                        """
                        Choose whether the system will only join faces, only intersect faces, or do both.
                        """

                    class _Operation(PyArgumentsTextualSubItem):
                        """
                        Choose whether to apply share topology using the Join-Intersect method where you join and/or intersect the problematic faces, or using the Interface Connect method where you connect edges of overlapping face pairs. Note that imprinting of overlapping faces in SCDM/Discovery is highly recommended for the Interface Connect method.
                        """

                    class _ShareTopologyAngle(PyArgumentsNumericalSubItem):
                        """
                        Specify the threshold angle for joining face pairs.
                        """

                    class _STToleranceIncrement(PyArgumentsNumericalSubItem):
                        """
                        Specify the increment by which the tolerance changes for each attempt to join face pairs.
                        """

                    class _ShowShareTopologyPreferences(PyArgumentsParameterSubItem):
                        """
                        Display advanced options that you may want to apply to the task.
                        """

                    class _PerLabelList(PyArgumentsTextualSubItem):
                        """
                        Argument PerLabelList.
                        """

                    class _IntfLabelList(PyArgumentsTextualSubItem):
                        """
                        Enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                        """

                    class _AdvancedImprove(PyArgumentsTextualSubItem):
                        """
                        Argument AdvancedImprove.
                        """

                    class _NumberOfJoinTries(PyArgumentsNumericalSubItem):
                        """
                        Specify the number of attempts that will be made to join face pairs under the given criteria.
                        """

            def create_instance(self) -> _MarkGapsArguments:
                args = self._get_create_instance_args()
                if args is not None:
                    return self._MarkGapsArguments(*args)

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
        class _Add2DBoundaryLayersArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Argument AddChild.
                """

            class _BLControlName(PyArgumentsTextualSubItem):
                """
                Argument BLControlName.
                """

            class _OffsetMethodType(PyArgumentsTextualSubItem):
                """
                Argument OffsetMethodType.
                """

            class _NumberOfLayers(PyArgumentsNumericalSubItem):
                """
                Argument NumberOfLayers.
                """

            class _FirstAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument FirstAspectRatio.
                """

            class _TransitionRatio(PyArgumentsNumericalSubItem):
                """
                Argument TransitionRatio.
                """

            class _LastAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument LastAspectRatio.
                """

            class _Rate(PyArgumentsNumericalSubItem):
                """
                Argument Rate.
                """

            class _FirstLayerHeight(PyArgumentsNumericalSubItem):
                """
                Argument FirstLayerHeight.
                """

            class _MaxLayerHeight(PyArgumentsNumericalSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _Addin(PyArgumentsTextualSubItem):
                """
                Argument Addin.
                """

            class _FaceLabelList(PyArgumentsTextualSubItem):
                """
                Argument FaceLabelList.
                """

            class _GrowOn(PyArgumentsTextualSubItem):
                """
                Argument GrowOn.
                """

            class _EdgeLabelList(PyArgumentsTextualSubItem):
                """
                Argument EdgeLabelList.
                """

            class _EdgeZoneList(PyArgumentsTextualSubItem):
                """
                Argument EdgeZoneList.
                """

            class _ShellBLAdvancedOptions(PyArgumentsSingletonSubItem):
                """
                Argument ShellBLAdvancedOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowShellBLAdvancedOptions = self._ShowShellBLAdvancedOptions(self, "ShowShellBLAdvancedOptions", service, rules, path)
                    self.ExposeSide = self._ExposeSide(self, "ExposeSide", service, rules, path)
                    self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                    self.AdjacentAttachAngle = self._AdjacentAttachAngle(self, "AdjacentAttachAngle", service, rules, path)

                class _ShowShellBLAdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Argument ShowShellBLAdvancedOptions.
                    """

                class _ExposeSide(PyArgumentsTextualSubItem):
                    """
                    Argument ExposeSide.
                    """

                class _MaxAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxAspectRatio.
                    """

                class _MinAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument MinAspectRatio.
                    """

                class _LastRatioNumLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _GapFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument GapFactor.
                    """

                class _AdjacentAttachAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument AdjacentAttachAngle.
                    """

        def create_instance(self) -> _Add2DBoundaryLayersArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._Add2DBoundaryLayersArguments(*args)

    class AddBoundaryLayers(PyCommand):
        """
        Determine whether or not boundary layers will be added to various portions of the model. Once a boundary layer is defined, global boundary layer settings are determined in the Create Volume Mesh task.
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
            Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteBlLabelList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteBLZoneList : list[str]
        CompleteBLRegionList : list[str]
        CompleteZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteLabelSelectionList : list[str]

        Returns
        -------
        bool
        """
        class _AddBoundaryLayersArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Determine whether (yes) or not (no) you want to specify one or more boundary layers for your simulation. If none are yet defined, you can choose yes, using prism control file and read in a prism control file that holds the boundary layer definition.
                """

            class _ReadPrismControlFile(PyArgumentsTextualSubItem):
                """
                Specify (or browse for) a .pzmcontrol file that contains the boundary (prism) layer specifications.
                """

            class _BLControlName(PyArgumentsTextualSubItem):
                """
                Specify a name for the boundary layer control or use the default value.
                """

            class _OffsetMethodType(PyArgumentsTextualSubItem):
                """
                Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
                """

            class _NumberOfLayers(PyArgumentsNumericalSubItem):
                """
                Select the number of boundary layers to be generated.
                """

            class _FirstAspectRatio(PyArgumentsNumericalSubItem):
                """
                Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
                """

            class _TransitionRatio(PyArgumentsNumericalSubItem):
                """
                For the smooth transition offset method, specify the rate at which adjacent elements grow. For the last-ratio offset method, specify the factor by which the thickness of each subsequent boundary layer increases or decreases compared to the previous layer.
                """

            class _Rate(PyArgumentsNumericalSubItem):
                """
                Specify the rate of growth for the boundary layer.
                """

            class _FirstHeight(PyArgumentsNumericalSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _MaxLayerHeight(PyArgumentsNumericalSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _FaceScope(PyArgumentsSingletonSubItem):
                """
                Argument FaceScope.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                    self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                    self.FaceScopeMeshObject = self._FaceScopeMeshObject(self, "FaceScopeMeshObject", service, rules, path)
                    self.RegionsType = self._RegionsType(self, "RegionsType", service, rules, path)

                class _TopologyList(PyArgumentsTextualSubItem):
                    """
                    Argument TopologyList.
                    """

                class _GrowOn(PyArgumentsTextualSubItem):
                    """
                    Specify where you would like to develop the boundary layers: either along only walls, all zones, along solid-fluid interfaces, or specifically selected zones or labels.
                    """

                class _FaceScopeMeshObject(PyArgumentsTextualSubItem):
                    """
                    Argument FaceScopeMeshObject.
                    """

                class _RegionsType(PyArgumentsTextualSubItem):
                    """
                    Specify what regions you would like to add the boundary layers: solid regions, fluid regions, or specifically named regions.
                    """

            class _RegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BlLabelList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LocalPrismPreferences(PyArgumentsSingletonSubItem):
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
                    self.ShowLocalPrismPreferences = self._ShowLocalPrismPreferences(self, "ShowLocalPrismPreferences", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.NumberOfSplitLayers = self._NumberOfSplitLayers(self, "NumberOfSplitLayers", service, rules, path)
                    self.AllowedTangencyAtInvalidNormals = self._AllowedTangencyAtInvalidNormals(self, "AllowedTangencyAtInvalidNormals", service, rules, path)
                    self.RemeshAtInvalidNormals = self._RemeshAtInvalidNormals(self, "RemeshAtInvalidNormals", service, rules, path)
                    self.IgnoreBoundaryLayers = self._IgnoreBoundaryLayers(self, "IgnoreBoundaryLayers", service, rules, path)

                class _LastRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatio.
                    """

                class _AdditionalIgnoredLayers(PyArgumentsNumericalSubItem):
                    """
                    Indicate the number of buffer layers that can be placed around ignored boundary layer faces, extending the ignored regions around sharp angles. Increasing the value increases the number of faces for which the boundary layer will be ignored at acute angles.
                    """

                class _SphereRadiusFactorAtInvalidNormals(PyArgumentsNumericalSubItem):
                    """
                    This factor is used to determine the size of the spheres created at the invalid normal location. The spheres have a radius of one half of the average mesh edge length adjacent to the invalid location. The default factor of 0.8 ensures a sphere size that is slightly smaller than that.
                    """

                class _SmoothRingsAtInvalidNormals(PyArgumentsNumericalSubItem):
                    """
                    Argument SmoothRingsAtInvalidNormals.
                    """

                class _Continuous(PyArgumentsTextualSubItem):
                    """
                    Specify how you would like to improve the generated boundary layer: as a continuous or stair-stepped boundary layer in the specified area(s).
                    """

                class _SplitPrism(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to add split prisms to each layer along the boundary. Not available when the Offset Method Type is set to last-ratio.
                    """

                class _ModifyAtInvalidNormals(PyArgumentsTextualSubItem):
                    """
                    Specify whether to automatically change the surface mesh where invalid normal faces are detected. To grow the boundary layer mesh in the proper direction (away from the boundary), normal vectors (valid) are required at the boundary face nodes of the surface mesh. More...
                    """

                class _InvalidNormalMethod(PyArgumentsTextualSubItem):
                    """
                    Argument InvalidNormalMethod.
                    """

                class _ShowLocalPrismPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to this task.
                    """

                class _LastRatioNumLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _NumberOfSplitLayers(PyArgumentsNumericalSubItem):
                    """
                    Indicate the number of split prism layers you wish to apply to each layer that you specified for the boundary layer definition.
                    """

                class _AllowedTangencyAtInvalidNormals(PyArgumentsNumericalSubItem):
                    """
                    Controls the tangency of the invalid normal faces. An invalid normal location with all 90 degree angles has a tangency of 1. So, faces are still treated as an invalid normal even if the angle deviates slightly from 90 degrees (resulting in a tangency of 0.98).
                    """

                class _RemeshAtInvalidNormals(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not to remesh around the area of the invalid normal(s). When enabled, a local (non-size function-based) remeshing procedure is performed to obtain similar sizes around the sphere with a reasonable transition to the surrounding mesh.
                    """

                class _IgnoreBoundaryLayers(PyArgumentsTextualSubItem):
                    """
                    Specify whether to automatically ignore boundary layers where there is an acute angle. Note that if there are sharp angles adjacent to other regions with boundary layers, some boundary layer removal may occur in those adjacent regions.
                    """

            class _BLZoneList(PyArgumentsTextualSubItem):
                """
                Argument BLZoneList.
                """

            class _BLRegionList(PyArgumentsTextualSubItem):
                """
                Argument BLRegionList.
                """

            class _InvalidAdded(PyArgumentsTextualSubItem):
                """
                Argument InvalidAdded.
                """

            class _CompleteRegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteBlLabelList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteBLZoneList(PyArgumentsTextualSubItem):
                """
                Argument CompleteBLZoneList.
                """

            class _CompleteBLRegionList(PyArgumentsTextualSubItem):
                """
                Argument CompleteBLRegionList.
                """

            class _CompleteZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteLabelSelectionList(PyArgumentsTextualSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

        def create_instance(self) -> _AddBoundaryLayersArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddBoundaryLayersArguments(*args)

    class AddBoundaryLayersForPartReplacement(PyCommand):
        """
        Determine whether or not boundary layers will be added to your replacement parts for this model.
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
        CompleteRegionScope : list[str]
            Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteBlLabelList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteBLZoneList : list[str]
        CompleteBLRegionList : list[str]
        CompleteZoneSelectionList : list[str]
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteLabelSelectionList : list[str]

        Returns
        -------
        bool
        """
        class _AddBoundaryLayersForPartReplacementArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Determine whether (yes) or not (no) you want to specify one or more boundary layers for your simulation. If none are yet defined, you can choose yes, using prism control file and read in a prism control file that holds the boundary layer definition.
                """

            class _ReadPrismControlFile(PyArgumentsTextualSubItem):
                """
                Specify (or browse for) a .pzmcontrol file that contains the boundary (prism) layer specifications.
                """

            class _BLControlName(PyArgumentsTextualSubItem):
                """
                Specify a name for the boundary layer control or use the default value.
                """

            class _OffsetMethodType(PyArgumentsTextualSubItem):
                """
                Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
                """

            class _NumberOfLayers(PyArgumentsNumericalSubItem):
                """
                Select the number of boundary layers to be generated.
                """

            class _FirstAspectRatio(PyArgumentsNumericalSubItem):
                """
                Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
                """

            class _TransitionRatio(PyArgumentsNumericalSubItem):
                """
                For the smooth transition offset method, specify the rate at which adjacent elements grow. For the last-ratio offset method, specify the factor by which the thickness of each subsequent boundary layer increases or decreases compared to the previous layer.
                """

            class _Rate(PyArgumentsNumericalSubItem):
                """
                Specify the rate of growth for the boundary layer.
                """

            class _FirstHeight(PyArgumentsNumericalSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _MaxLayerHeight(PyArgumentsNumericalSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _FaceScope(PyArgumentsSingletonSubItem):
                """
                Argument FaceScope.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                    self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                    self.FaceScopeMeshObject = self._FaceScopeMeshObject(self, "FaceScopeMeshObject", service, rules, path)
                    self.RegionsType = self._RegionsType(self, "RegionsType", service, rules, path)

                class _TopologyList(PyArgumentsTextualSubItem):
                    """
                    Argument TopologyList.
                    """

                class _GrowOn(PyArgumentsTextualSubItem):
                    """
                    Specify where you would like to develop the boundary layers: either along only walls, all zones, along solid-fluid interfaces, or specifically selected zones or labels.
                    """

                class _FaceScopeMeshObject(PyArgumentsTextualSubItem):
                    """
                    Argument FaceScopeMeshObject.
                    """

                class _RegionsType(PyArgumentsTextualSubItem):
                    """
                    Specify what regions you would like to add the boundary layers: solid regions, fluid regions, or specifically named regions.
                    """

            class _RegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BlLabelList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LocalPrismPreferences(PyArgumentsSingletonSubItem):
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
                    self.NumberOfSplitLayers = self._NumberOfSplitLayers(self, "NumberOfSplitLayers", service, rules, path)
                    self.ShowLocalPrismPreferences = self._ShowLocalPrismPreferences(self, "ShowLocalPrismPreferences", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.AllowedTangencyAtInvalidNormals = self._AllowedTangencyAtInvalidNormals(self, "AllowedTangencyAtInvalidNormals", service, rules, path)
                    self.RemeshAtInvalidNormals = self._RemeshAtInvalidNormals(self, "RemeshAtInvalidNormals", service, rules, path)
                    self.IgnoreBoundaryLayers = self._IgnoreBoundaryLayers(self, "IgnoreBoundaryLayers", service, rules, path)

                class _LastRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatio.
                    """

                class _AdditionalIgnoredLayers(PyArgumentsNumericalSubItem):
                    """
                    Indicate the number of buffer layers that can be placed around ignored boundary layer faces, extending the ignored regions around sharp angles. Increasing the value increases the number of faces for which the boundary layer will be ignored at acute angles.
                    """

                class _SphereRadiusFactorAtInvalidNormals(PyArgumentsNumericalSubItem):
                    """
                    This factor is used to determine the size of the spheres created at the invalid normal location. The spheres have a radius of one half of the average mesh edge length adjacent to the invalid location. The default factor of 0.8 ensures a sphere size that is slightly smaller than that.
                    """

                class _SmoothRingsAtInvalidNormals(PyArgumentsNumericalSubItem):
                    """
                    Argument SmoothRingsAtInvalidNormals.
                    """

                class _Continuous(PyArgumentsTextualSubItem):
                    """
                    Specify how you would like to improve the generated boundary layer: as a continuous or stair-stepped boundary layer in the specified area(s).
                    """

                class _ModifyAtInvalidNormals(PyArgumentsTextualSubItem):
                    """
                    Specify whether to automatically change the surface mesh where invalid normal faces are detected. To grow the boundary layer mesh in the proper direction (away from the boundary), normal vectors (valid) are required at the boundary face nodes of the surface mesh. More...
                    """

                class _SplitPrism(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to add split prisms to each layer along the boundary. Not available when the Offset Method Type is set to last-ratio.
                    """

                class _InvalidNormalMethod(PyArgumentsTextualSubItem):
                    """
                    Argument InvalidNormalMethod.
                    """

                class _NumberOfSplitLayers(PyArgumentsNumericalSubItem):
                    """
                    Indicate the number of split prism layers you wish to apply to each layer that you specified for the boundary layer definition.
                    """

                class _ShowLocalPrismPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to this task.
                    """

                class _LastRatioNumLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _AllowedTangencyAtInvalidNormals(PyArgumentsNumericalSubItem):
                    """
                    Controls the tangency of the invalid normal faces. An invalid normal location with all 90 degree angles has a tangency of 1. So, faces are still treated as an invalid normal even if the angle deviates slightly from 90 degrees (resulting in a tangency of 0.98).
                    """

                class _RemeshAtInvalidNormals(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not to remesh around the area of the invalid normal(s). When enabled, a local (non-size function-based) remeshing procedure is performed to obtain similar sizes around the sphere with a reasonable transition to the surrounding mesh.
                    """

                class _IgnoreBoundaryLayers(PyArgumentsTextualSubItem):
                    """
                    Specify whether to automatically ignore boundary layers where there is an acute angle. Note that if there are sharp angles adjacent to other regions with boundary layers, some boundary layer removal may occur in those adjacent regions.
                    """

            class _BLZoneList(PyArgumentsTextualSubItem):
                """
                Argument BLZoneList.
                """

            class _BLRegionList(PyArgumentsTextualSubItem):
                """
                Argument BLRegionList.
                """

            class _CompleteRegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to add a boundary layer. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteBlLabelList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteBLZoneList(PyArgumentsTextualSubItem):
                """
                Argument CompleteBLZoneList.
                """

            class _CompleteBLRegionList(PyArgumentsTextualSubItem):
                """
                Argument CompleteBLRegionList.
                """

            class _CompleteZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteLabelSelectionList(PyArgumentsTextualSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

        def create_instance(self) -> _AddBoundaryLayersForPartReplacementArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddBoundaryLayersForPartReplacementArguments(*args)

    class AddBoundaryType(PyCommand):
        """
        Create additional boundaries for your simulation. Provide a name, and assign a boundary type to one or more selected zones in your geometry.  More...
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
        class _AddBoundaryTypeArguments(PyArguments):
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

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _NewBoundaryLabelName(PyArgumentsTextualSubItem):
                """
                Specify a name for the boundary type.
                """

            class _NewBoundaryType(PyArgumentsTextualSubItem):
                """
                Choose a boundary type from the available options.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _BoundaryFaceZoneList(PyArgumentsTextualSubItem):
                """
                Enter a text string to filter out the list of zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _Merge(PyArgumentsTextualSubItem):
                """
                Determine whether or not to merge the selected zones (set to yes by default).
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _AddBoundaryTypeArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddBoundaryTypeArguments(*args)

    class AddLocalSizingFTM(PyCommand):
        """
        Create individual sizing controls for your mesh. For every size control that you create, it is added to the workflow as a subtask. More...
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
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteLabelSelectionList : list[str]
            Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteEdgeSelectionList : list[str]
            Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...

        Returns
        -------
        bool
        """
        class _AddLocalSizingFTMArguments(PyArguments):
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

            class _LocalSettingsName(PyArgumentsTextualSubItem):
                """
                Specify a name for the size control or use the default value.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _EdgeSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LocalSizeControlParameters(PyArgumentsSingletonSubItem):
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
                    self.InitialSizeControl = self._InitialSizeControl(self, "InitialSizeControl", service, rules, path)
                    self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.WrapCurvatureNormalAngle = self._WrapCurvatureNormalAngle(self, "WrapCurvatureNormalAngle", service, rules, path)
                    self.TargetSizeControl = self._TargetSizeControl(self, "TargetSizeControl", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum size of the elements for the surface mesh.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Set proximity based refinement. The edges option considers edge-to-edge proximity, while faces considers face-to-face proximity, and faces and edges considers both. Note that when you use the faces and edges option, you can only select objects.
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
                    """

                class _IgnoreSelf(PyArgumentsParameterSubItem):
                    """
                    Select this option to ignore the proximity computation between facets within a face zone, and avoid over-refinement.
                    """

                class _WrapMin(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the minimum wrapping size for the size control. It will wrap with this minimum size and later coarsen through remeshing to the given target size. One of the advantages of the wrapper is that it can automatically de-feature unnecessary small details. The wrap size is used to wrap the geometry and target size is used to remesh. Feature capturing highly depends on the value of the wrap size. The default wrap size is 1/1.5 times smaller than the target size, and you can change the value.
                    """

                class _WrapCellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum size of the elements for the surface mesh.
                    """

                class _WrapMax(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the maximum wrapping size for the size control. It will wrap with this maximum size and later coarsen through remeshing to the given target size.
                    """

                class _AdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Display advanced wrap-specific options that are also applied to the task. See this description  for more information about wrap (and target) mesh size controls.
                    """

                class _WrapGrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the increase in element edge length with each succeeding layer of elements.
                    """

                class _InitialSizeControl(PyArgumentsParameterSubItem):
                    """
                    Enable this field to display the initial size control in the graphics window.
                    """

                class _SizingType(PyArgumentsTextualSubItem):
                    """
                    Choose the type of sizing control (curvature, proximity, soft, or boi).
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                    """

                class _WrapCurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
                    """

                class _TargetSizeControl(PyArgumentsParameterSubItem):
                    """
                    Enable this field to display the target size control in the graphics window.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the increase in element edge length with each succeeding layer of elements.
                    """

            class _ValueChanged(PyArgumentsTextualSubItem):
                """
                Argument ValueChanged.
                """

            class _CompleteZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteLabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteEdgeSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _AddLocalSizingFTMArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddLocalSizingFTMArguments(*args)

    class AddLocalSizingWTM(PyCommand):
        """
        Apply local sizing controls. Use this task to gain better control over the mesh size distribution, and define specific mesh size controls that operate on specific, localized, portions of the geometry and mesh. Using this task, you can add as many localized size controls to the workflow as you need, depending on the requirements and details of your geometry.  More...
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
        class _AddLocalSizingWTMArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Choose whether or not you want to add local size controls in order to create the surface mesh.
                """

            class _BOIControlName(PyArgumentsTextualSubItem):
                """
                Provide a name for this specific size control.
                """

            class _BOIGrowthRate(PyArgumentsNumericalSubItem):
                """
                Specify the increase in element edge length with each succeeding layer of elements.
                """

            class _BOIExecution(PyArgumentsTextualSubItem):
                """
                Choose whether the size control is to be applied to a local edge size, a local face size, a local body size, a body of influence, a face of influence, curvature, or proximity.
                """

            class _AssignSizeUsing(PyArgumentsTextualSubItem):
                """
                Argument AssignSizeUsing.
                """

            class _BOISize(PyArgumentsNumericalSubItem):
                """
                Specify a value for the desired size of the local sizing (or body/face of influence) to be applied to the indicated label(s) or zone(s).
                """

            class _NumberofLayers(PyArgumentsNumericalSubItem):
                """
                Argument NumberofLayers.
                """

            class _SmallestHeight(PyArgumentsNumericalSubItem):
                """
                Argument SmallestHeight.
                """

            class _GrowthPattern(PyArgumentsTextualSubItem):
                """
                Argument GrowthPattern.
                """

            class _GrowthMethod(PyArgumentsTextualSubItem):
                """
                Argument GrowthMethod.
                """

            class _BiasFactor(PyArgumentsNumericalSubItem):
                """
                Argument BiasFactor.
                """

            class _BOIMinSize(PyArgumentsNumericalSubItem):
                """
                Specify the minimum size of the elements for the surface mesh.
                """

            class _BOIMaxSize(PyArgumentsNumericalSubItem):
                """
                Specify the maximum size of the elements for the surface mesh.
                """

            class _BOICurvatureNormalAngle(PyArgumentsNumericalSubItem):
                """
                Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
                """

            class _BOICellsPerGap(PyArgumentsNumericalSubItem):
                """
                Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                """

            class _BOIScopeTo(PyArgumentsTextualSubItem):
                """
                Set curvature or proximity based refinement. The edges option considers edge-to-edge proximity, while faces considers face-to-face proximity, and faces and edges considers both. The edge labels option considers edge sizing based on edge labels. Note that when you use the edges or the faces and edges options, you can only select face zones or face labels. Also, saving a size control file after using either of these two options will not be persistent.
                """

            class _IgnoreOrientation(PyArgumentsTextualSubItem):
                """
                Specify whether or not you need to apply additional refinement in and around thin areas (such as between plates), without over-refinement. This ignores face proximity within voids and will not allow you to refine in thin voids, but will allow refinement in gaps. This should be used in predominantly fluid regions with no thin solid regions.
                """

            class _BOIZoneorLabel(PyArgumentsTextualSubItem):
                """
                Choose how you want to select your surface (by label or by zone).
                """

            class _BOIFaceLabelList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BOIFaceZoneList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _EdgeLabelList(PyArgumentsTextualSubItem):
                """
                Argument EdgeLabelList.
                """

            class _EdgeZoneList(PyArgumentsTextualSubItem):
                """
                Argument EdgeZoneList.
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _ReverseEdgeZoneOrientation(PyArgumentsParameterSubItem):
                """
                Argument ReverseEdgeZoneOrientation.
                """

            class _ReverseEdgeZoneList(PyArgumentsTextualSubItem):
                """
                Argument ReverseEdgeZoneList.
                """

            class _BOIPatchingtoggle(PyArgumentsParameterSubItem):
                """
                Enable this option to repair any openings that may still exist in the body of influence-based local sizing control.
                """

            class _DrawSizeControl(PyArgumentsParameterSubItem):
                """
                Enable this field to display the size boxes in the graphics window.
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _CompleteFaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument CompleteFaceZoneList.
                """

            class _CompleteFaceLabelList(PyArgumentsTextualSubItem):
                """
                Argument CompleteFaceLabelList.
                """

            class _CompleteEdgeLabelList(PyArgumentsTextualSubItem):
                """
                Argument CompleteEdgeLabelList.
                """

            class _CompleteTopologyList(PyArgumentsTextualSubItem):
                """
                Argument CompleteTopologyList.
                """

            class _PrimeSizeControlId(PyArgumentsNumericalSubItem):
                """
                Argument PrimeSizeControlId.
                """

        def create_instance(self) -> _AddLocalSizingWTMArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddLocalSizingWTMArguments(*args)

    class AddMultiZoneControls(PyCommand):
        """
        Use this task to add multi-zone mesh controls for the selected regions.  More...
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
            Specify the minimum size for the edge-based multizone control.
        MaxSweepSize : float
            Indicates the maximum value for the sweep size.
        RegionScope : list[str]
            Select the named region(s) from the list to which you would like to create the multi-zone control. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        SourceMethod : str
            Choose one or more face zones or labels from the list below. You can also provide the ability to select all source-target zones that are parallel to a global plane by choosing Zones parallel to XY plane, Zones parallel to XZ plane, or Zones parallel to YZ plane. For zones or labels. use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ParallelSelection : bool
            When your desired zones are aligned with the global x,y, or z plane, enable this checkbox to automatically select all parallel zones in  the selected region(s).
        ShowEdgeBiasing : str
            If edge labels are automatically created on all edges, preserving the face/edge topology, use this field to determine if you want to save time and preview any edge biasing, since when many edges are selected, there can be many nodes and biases that can take additional time. Choices include yes, selected to only preview the selected edge, yes, all to preview all edges, and no to not preview edge biasing.
        TopoSourceList : list[str]
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
            Select the named region(s) from the list to which you would like to create the multi-zone control. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteEdgeScope : list[str]

        Returns
        -------
        bool
        """
        class _AddMultiZoneControlsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ControlType = self._ControlType(self, "ControlType", service, rules, path)
                self.MultiZName = self._MultiZName(self, "MultiZName", service, rules, path)
                self.MeshMethod = self._MeshMethod(self, "MeshMethod", service, rules, path)
                self.FillWith = self._FillWith(self, "FillWith", service, rules, path)
                self.UseSweepSize = self._UseSweepSize(self, "UseSweepSize", service, rules, path)
                self.MaxSweepSize = self._MaxSweepSize(self, "MaxSweepSize", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.SourceMethod = self._SourceMethod(self, "SourceMethod", service, rules, path)
                self.ParallelSelection = self._ParallelSelection(self, "ParallelSelection", service, rules, path)
                self.ShowEdgeBiasing = self._ShowEdgeBiasing(self, "ShowEdgeBiasing", service, rules, path)
                self.TopoSourceList = self._TopoSourceList(self, "TopoSourceList", service, rules, path)
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

            class _ControlType(PyArgumentsTextualSubItem):
                """
                Determine if you want to define the multi-zone control by selecting regions or edges.
                """

            class _MultiZName(PyArgumentsTextualSubItem):
                """
                Enter a name for the multi-zone mesh control, or use the default.
                """

            class _MeshMethod(PyArgumentsTextualSubItem):
                """
                Choose a multi-zone meshing technique: Standard or the Thin volume technique (for only a single layer)
                """

            class _FillWith(PyArgumentsTextualSubItem):
                """
                Choose a multi-zone meshing fill type: Hex-Pave, Hex-Map, Prism, or Mixed.
                """

            class _UseSweepSize(PyArgumentsTextualSubItem):
                """
                Specify the minimum size for the edge-based multizone control.
                """

            class _MaxSweepSize(PyArgumentsNumericalSubItem):
                """
                Indicates the maximum value for the sweep size.
                """

            class _RegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to create the multi-zone control. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _SourceMethod(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones or labels from the list below. You can also provide the ability to select all source-target zones that are parallel to a global plane by choosing Zones parallel to XY plane, Zones parallel to XZ plane, or Zones parallel to YZ plane. For zones or labels. use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ParallelSelection(PyArgumentsParameterSubItem):
                """
                When your desired zones are aligned with the global x,y, or z plane, enable this checkbox to automatically select all parallel zones in  the selected region(s).
                """

            class _ShowEdgeBiasing(PyArgumentsTextualSubItem):
                """
                If edge labels are automatically created on all edges, preserving the face/edge topology, use this field to determine if you want to save time and preview any edge biasing, since when many edges are selected, there can be many nodes and biases that can take additional time. Choices include yes, selected to only preview the selected edge, yes, all to preview all edges, and no to not preview edge biasing.
                """

            class _TopoSourceList(PyArgumentsTextualSubItem):
                """
                Argument TopoSourceList.
                """

            class _LabelSourceList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSourceList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _AssignSizeUsing(PyArgumentsTextualSubItem):
                """
                For edge-based multizone controls, you can choose from Interval, Size, or Smallest Height. If double graded biasing is used and the Interval is set to an odd number (or the Size or Smallest Height results in an odd number Interval), the interval will automatically be increased by one.
                """

            class _Intervals(PyArgumentsNumericalSubItem):
                """
                Specify the number of intervals for the edge-based multizone control. If double graded biasing is used and the Interval is set to an odd number (or the Size or Smallest Height results in an odd number Interval), the interval will automatically be increased by one.
                """

            class _Size(PyArgumentsNumericalSubItem):
                """
                Specify the minimum size for the edge-based multizone control.
                """

            class _SmallestHeight(PyArgumentsNumericalSubItem):
                """
                Specify a value for the smallest height for the edge-based multizone control.
                """

            class _BiasMethod(PyArgumentsTextualSubItem):
                """
                Select from a choice of patterns that you want to apply to your edge-based multizone control.
                """

            class _GrowthMethod(PyArgumentsTextualSubItem):
                """
                For edge-based multizone controls when using variable Growth Patterns, determine how you would like to determine the growth: either as a Growth Rate or as Bias Factor.
                """

            class _GrowthRate(PyArgumentsNumericalSubItem):
                """
                Specify a value for the growth rate for the multizone, or use the default value.
                """

            class _BiasFactor(PyArgumentsNumericalSubItem):
                """
                Specify a value for the bias factor for the multizone, or use the default value. The Bias Factor is the ratio of the largest to the smallest segment on the edge.
                """

            class _EdgeLabelSelection(PyArgumentsTextualSubItem):
                """
                Argument EdgeLabelSelection.
                """

            class _EdgeLabelList(PyArgumentsTextualSubItem):
                """
                Choose one or more edge labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CFDSurfaceMeshControls(PyArgumentsSingletonSubItem):
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
                    self.SurfaceMeshMethod = self._SurfaceMeshMethod(self, "SurfaceMeshMethod", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum size for the edge-based multizone control.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyArgumentsParameterSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyArgumentsParameterSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyArgumentsTextualSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyArgumentsParameterSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum size for the edge-based multizone control.
                    """

                class _SizeFunctions(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SurfaceMeshMethod(PyArgumentsTextualSubItem):
                    """
                    Choose a multi-zone meshing technique: Standard or the Thin volume technique (for only a single layer)
                    """

                class _SizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyArgumentsParameterSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyArgumentsTextualSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the growth rate for the multizone, or use the default value.
                    """

                class _ObjectBasedControls(PyArgumentsTextualSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _CompleteRegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to create the multi-zone control. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteEdgeScope(PyArgumentsTextualSubItem):
                """
                Argument CompleteEdgeScope.
                """

        def create_instance(self) -> _AddMultiZoneControlsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddMultiZoneControlsArguments(*args)

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
        class _AddShellBoundaryLayerControlsArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Argument AddChild.
                """

            class _BLControlName(PyArgumentsTextualSubItem):
                """
                Argument BLControlName.
                """

            class _OffsetMethodType(PyArgumentsTextualSubItem):
                """
                Argument OffsetMethodType.
                """

            class _NumberOfLayers(PyArgumentsNumericalSubItem):
                """
                Argument NumberOfLayers.
                """

            class _FirstAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument FirstAspectRatio.
                """

            class _LastAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument LastAspectRatio.
                """

            class _Rate(PyArgumentsNumericalSubItem):
                """
                Argument Rate.
                """

            class _FirstLayerHeight(PyArgumentsNumericalSubItem):
                """
                Argument FirstLayerHeight.
                """

            class _MaxLayerHeight(PyArgumentsNumericalSubItem):
                """
                Argument MaxLayerHeight.
                """

            class _GrowOn(PyArgumentsTextualSubItem):
                """
                Argument GrowOn.
                """

            class _FaceLabelList(PyArgumentsTextualSubItem):
                """
                Argument FaceLabelList.
                """

            class _FaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument FaceZoneList.
                """

            class _EdgeSelectionType(PyArgumentsTextualSubItem):
                """
                Argument EdgeSelectionType.
                """

            class _EdgeLabelList(PyArgumentsTextualSubItem):
                """
                Argument EdgeLabelList.
                """

            class _EdgeZoneList(PyArgumentsTextualSubItem):
                """
                Argument EdgeZoneList.
                """

            class _ShellBLAdvancedOptions(PyArgumentsSingletonSubItem):
                """
                Argument ShellBLAdvancedOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowShellBLAdvancedOptions = self._ShowShellBLAdvancedOptions(self, "ShowShellBLAdvancedOptions", service, rules, path)
                    self.ExposeSide = self._ExposeSide(self, "ExposeSide", service, rules, path)
                    self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.LastRatioNumLayers = self._LastRatioNumLayers(self, "LastRatioNumLayers", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                    self.AdjacentAttachAngle = self._AdjacentAttachAngle(self, "AdjacentAttachAngle", service, rules, path)

                class _ShowShellBLAdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Argument ShowShellBLAdvancedOptions.
                    """

                class _ExposeSide(PyArgumentsTextualSubItem):
                    """
                    Argument ExposeSide.
                    """

                class _MaxAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxAspectRatio.
                    """

                class _MinAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument MinAspectRatio.
                    """

                class _LastRatioNumLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioNumLayers.
                    """

                class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _GapFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument GapFactor.
                    """

                class _AdjacentAttachAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument AdjacentAttachAngle.
                    """

        def create_instance(self) -> _AddShellBoundaryLayerControlsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddShellBoundaryLayerControlsArguments(*args)

    class AddThickness(PyCommand):
        """
        Add thickness to any zero-thickness portions of your geometry (such as baffles or interior walls) where those portions of the geometry are relevant to your simulation. Not all portions of the geometry require a thickness, however, a more refined surface mesh can be generated if all important and relevant aspects of the geometry have a certain thickness. More...
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
        class _AddThicknessArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ZeroThicknessName = self._ZeroThicknessName(self, "ZeroThicknessName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
                self.Distance = self._Distance(self, "Distance", service, rules, path)

            class _ZeroThicknessName(PyArgumentsTextualSubItem):
                """
                Specify a name for the thickness control or use the default value.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _Distance(PyArgumentsNumericalSubItem):
                """
                Specify a value that adds thickness to the selected object. Thickness is applied in the normal direction. Negative values are allowed to preview the opposite/flipped direction. The original face normal will be kept, but you can add thickness in either direction based on a positive or negative value.
                """

        def create_instance(self) -> _AddThicknessArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddThicknessArguments(*args)

    class AddThinVolumeMeshControls(PyCommand):
        """
        Use this task to add thin volume meshing controls for the selected regions.
        Parameters
        ----------
        ThinMeshingName : str
            Enter a name for the thin volume mesh control, or use the default.
        AssignSizeUsing : str
            Specify the sizing of the mesh layers to be based on Intervals or based on the Size of the plates.
        Intervals : int
            Specifies the minimum number of mesh layers to be created within the thin volume mesh.
        MaxNumberOfIntervals : int
            Specifies the minimum number of mesh layers to be created within the thin volume mesh.
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
        Objects : list[str]
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
        TopoSourceList : list[str]
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
            Specify the Region(s) where the thin volume meshing controls will be applied.
        CompleteLabelSourceList : list[str]
            Select the label(s) to use as the source.
        CompleteZoneSourceList : list[str]
            Select the zone(s) to use as the source.
        CompleteTopoSourceList : list[str]
        CompleteLabelTargetList : list[str]
            Select the label(s) to use as the target.
        CompleteZoneTargetList : list[str]
            Select the zone(s) to use as the target.
        ThinVolumePreferences : dict[str, Any]
        ZoneLocation : list[str]
        ZoneLocation2 : list[str]

        Returns
        -------
        bool
        """
        class _AddThinVolumeMeshControlsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ThinMeshingName = self._ThinMeshingName(self, "ThinMeshingName", service, rules, path)
                self.AssignSizeUsing = self._AssignSizeUsing(self, "AssignSizeUsing", service, rules, path)
                self.Intervals = self._Intervals(self, "Intervals", service, rules, path)
                self.MaxNumberOfIntervals = self._MaxNumberOfIntervals(self, "MaxNumberOfIntervals", service, rules, path)
                self.Size = self._Size(self, "Size", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.RemeshOverlapping = self._RemeshOverlapping(self, "RemeshOverlapping", service, rules, path)
                self.DoubleBiasing = self._DoubleBiasing(self, "DoubleBiasing", service, rules, path)
                self.SideImprints = self._SideImprints(self, "SideImprints", service, rules, path)
                self.StackedPlates = self._StackedPlates(self, "StackedPlates", service, rules, path)
                self.AutoControlCreation = self._AutoControlCreation(self, "AutoControlCreation", service, rules, path)
                self.Objects = self._Objects(self, "Objects", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.SelectSourceBy = self._SelectSourceBy(self, "SelectSourceBy", service, rules, path)
                self.ParallelSource = self._ParallelSource(self, "ParallelSource", service, rules, path)
                self.LabelSourceList = self._LabelSourceList(self, "LabelSourceList", service, rules, path)
                self.ZoneSourceList = self._ZoneSourceList(self, "ZoneSourceList", service, rules, path)
                self.TopoSourceList = self._TopoSourceList(self, "TopoSourceList", service, rules, path)
                self.SelectTargetBy = self._SelectTargetBy(self, "SelectTargetBy", service, rules, path)
                self.ParallelTarget = self._ParallelTarget(self, "ParallelTarget", service, rules, path)
                self.LabelTargetList = self._LabelTargetList(self, "LabelTargetList", service, rules, path)
                self.ZoneTargetList = self._ZoneTargetList(self, "ZoneTargetList", service, rules, path)
                self.ThinVolRegs = self._ThinVolRegs(self, "ThinVolRegs", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)
                self.CompleteLabelSourceList = self._CompleteLabelSourceList(self, "CompleteLabelSourceList", service, rules, path)
                self.CompleteZoneSourceList = self._CompleteZoneSourceList(self, "CompleteZoneSourceList", service, rules, path)
                self.CompleteTopoSourceList = self._CompleteTopoSourceList(self, "CompleteTopoSourceList", service, rules, path)
                self.CompleteLabelTargetList = self._CompleteLabelTargetList(self, "CompleteLabelTargetList", service, rules, path)
                self.CompleteZoneTargetList = self._CompleteZoneTargetList(self, "CompleteZoneTargetList", service, rules, path)
                self.ThinVolumePreferences = self._ThinVolumePreferences(self, "ThinVolumePreferences", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ZoneLocation2 = self._ZoneLocation2(self, "ZoneLocation2", service, rules, path)

            class _ThinMeshingName(PyArgumentsTextualSubItem):
                """
                Enter a name for the thin volume mesh control, or use the default.
                """

            class _AssignSizeUsing(PyArgumentsTextualSubItem):
                """
                Specify the sizing of the mesh layers to be based on Intervals or based on the Size of the plates.
                """

            class _Intervals(PyArgumentsNumericalSubItem):
                """
                Specifies the minimum number of mesh layers to be created within the thin volume mesh.
                """

            class _MaxNumberOfIntervals(PyArgumentsNumericalSubItem):
                """
                Specifies the minimum number of mesh layers to be created within the thin volume mesh.
                """

            class _Size(PyArgumentsNumericalSubItem):
                """
                enter the Size of each thin mesh layer or use the default.
                """

            class _GrowthRate(PyArgumentsNumericalSubItem):
                """
                Specify the Growth Rate which is the expansion rate of the extrusion for each thin volume mesh layer and is set to 1 by default. A growth rate of 1.2 for example will expand each layer of the extrusion by 20 percent of the previous length.
                """

            class _RemeshOverlapping(PyArgumentsParameterSubItem):
                """
                Argument RemeshOverlapping.
                """

            class _DoubleBiasing(PyArgumentsParameterSubItem):
                """
                Enable the Doubling biasing option to invoke double biasing on edges of the thin volume mesh layers. Enabling double biasing will automatically set the Growth Rate to 1.3. When disabled, the thin volume mesh can only be graded from the Source to the Target.
                """

            class _SideImprints(PyArgumentsParameterSubItem):
                """
                Specifies the mesher to project the outer nodes of the thin volume mesh onto adjacent boundary face zones and is enabled by default. This ensures that geometric details of the thin volume are accurately captured at the boundary.
                """

            class _StackedPlates(PyArgumentsParameterSubItem):
                """
                For models consisting of stacked planar plates, you can enable the Stacked Plates option to select all source-target zones that are aligned with the global x-y-z plane.
                """

            class _AutoControlCreation(PyArgumentsParameterSubItem):
                """
                enter the Size of each thin mesh layer or use the default.
                """

            class _Objects(PyArgumentsTextualSubItem):
                """
                Argument Objects.
                """

            class _RegionScope(PyArgumentsTextualSubItem):
                """
                Specify the Region(s) where the thin volume meshing controls will be applied.
                """

            class _SelectSourceBy(PyArgumentsTextualSubItem):
                """
                Choose whether to select the source surfaces by label or by zone.
                """

            class _ParallelSource(PyArgumentsParameterSubItem):
                """
                Enable this option if you have multiple source zones in parallel that you want to select for thin meshing.
                """

            class _LabelSourceList(PyArgumentsTextualSubItem):
                """
                Select the label(s) to use as the source.
                """

            class _ZoneSourceList(PyArgumentsTextualSubItem):
                """
                Select the zone(s) to use as the source.
                """

            class _TopoSourceList(PyArgumentsTextualSubItem):
                """
                Argument TopoSourceList.
                """

            class _SelectTargetBy(PyArgumentsTextualSubItem):
                """
                Choose whether to select the source surfaces by label or by zone.
                """

            class _ParallelTarget(PyArgumentsParameterSubItem):
                """
                Enable this option if you have multiple target zones in parallel that you want to select for thin meshing,
                """

            class _LabelTargetList(PyArgumentsTextualSubItem):
                """
                Select the label(s) to use as the target.
                """

            class _ZoneTargetList(PyArgumentsTextualSubItem):
                """
                Select the zone(s) to use as the target.
                """

            class _ThinVolRegs(PyArgumentsTextualSubItem):
                """
                Argument ThinVolRegs.
                """

            class _CompleteRegionScope(PyArgumentsTextualSubItem):
                """
                Specify the Region(s) where the thin volume meshing controls will be applied.
                """

            class _CompleteLabelSourceList(PyArgumentsTextualSubItem):
                """
                Select the label(s) to use as the source.
                """

            class _CompleteZoneSourceList(PyArgumentsTextualSubItem):
                """
                Select the zone(s) to use as the source.
                """

            class _CompleteTopoSourceList(PyArgumentsTextualSubItem):
                """
                Argument CompleteTopoSourceList.
                """

            class _CompleteLabelTargetList(PyArgumentsTextualSubItem):
                """
                Select the label(s) to use as the target.
                """

            class _CompleteZoneTargetList(PyArgumentsTextualSubItem):
                """
                Select the zone(s) to use as the target.
                """

            class _ThinVolumePreferences(PyArgumentsSingletonSubItem):
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

                class _ShowThinVolumePreferences(PyArgumentsParameterSubItem):
                    """
                    Advanced settings for thin volume meshing controls.
                    """

                class _MaxGapSize(PyArgumentsNumericalSubItem):
                    """
                    The maximum gap distance between thin mesh layers. This size is computed automatically and should not be changed for most cases.
                    """

                class _IgnoreExtraSources(PyArgumentsTextualSubItem):
                    """
                    Choose to have Standard or Aggressive unstructured fill. This option applies unstructured meshing in complex regions of the thin volume mesh.
                    """

                class _StackedPlateTolerance(PyArgumentsNumericalSubItem):
                    """
                    Specifies the tolerance to include adjacent source faces.
                    """

                class _IncludeAdjacent(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not adjacent stacked plate(s) are included in the thin mesh. This option is set to Yes by default.
                    """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _ZoneLocation2(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation2.
                """

        def create_instance(self) -> _AddThinVolumeMeshControlsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddThinVolumeMeshControlsArguments(*args)

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
        class _AddVirtualTopologyArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.ControlName = self._ControlName(self, "ControlName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.FaceLabelList = self._FaceLabelList(self, "FaceLabelList", service, rules, path)
                self.FaceZoneList = self._FaceZoneList(self, "FaceZoneList", service, rules, path)
                self.NewFaces = self._NewFaces(self, "NewFaces", service, rules, path)

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Argument AddChild.
                """

            class _ControlName(PyArgumentsTextualSubItem):
                """
                Argument ControlName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _FaceLabelList(PyArgumentsTextualSubItem):
                """
                Argument FaceLabelList.
                """

            class _FaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument FaceZoneList.
                """

            class _NewFaces(PyArgumentsNumericalSubItem):
                """
                Argument NewFaces.
                """

        def create_instance(self) -> _AddVirtualTopologyArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddVirtualTopologyArguments(*args)

    class AxisymmetricSweep(PyCommand):
        """
        Command AxisymmetricSweep.

        Parameters
        ----------
        AxisSweepControlName : str
        SelectionType : str
        SweepBoundaryZoneList : list[str]
        TopologyList : list[str]
        AxisOrigin : dict[str, Any]
        AxisDirection : dict[str, Any]
        RevolutionAngleDeg : float
        NumberOfLayers : int
        ZoneLocation : list[str]

        Returns
        -------
        bool
        """
        class _AxisymmetricSweepArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AxisSweepControlName = self._AxisSweepControlName(self, "AxisSweepControlName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.SweepBoundaryZoneList = self._SweepBoundaryZoneList(self, "SweepBoundaryZoneList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.AxisOrigin = self._AxisOrigin(self, "AxisOrigin", service, rules, path)
                self.AxisDirection = self._AxisDirection(self, "AxisDirection", service, rules, path)
                self.RevolutionAngleDeg = self._RevolutionAngleDeg(self, "RevolutionAngleDeg", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _AxisSweepControlName(PyArgumentsTextualSubItem):
                """
                Argument AxisSweepControlName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _SweepBoundaryZoneList(PyArgumentsTextualSubItem):
                """
                Argument SweepBoundaryZoneList.
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _AxisOrigin(PyArgumentsSingletonSubItem):
                """
                Argument AxisOrigin.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Argument X.
                    """

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Argument Z.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Argument Y.
                    """

            class _AxisDirection(PyArgumentsSingletonSubItem):
                """
                Argument AxisDirection.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Argument X.
                    """

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Argument Z.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Argument Y.
                    """

            class _RevolutionAngleDeg(PyArgumentsNumericalSubItem):
                """
                Argument RevolutionAngleDeg.
                """

            class _NumberOfLayers(PyArgumentsNumericalSubItem):
                """
                Argument NumberOfLayers.
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _AxisymmetricSweepArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AxisymmetricSweepArguments(*args)

    class Capping(PyCommand):
        """
        For solid model geometries where you want to extract a flow volume, use this task to enclose, or cap, any openings in your geometry in order to later calculate your fluid region(s). Assign a name for the capping surface, and designate the type of opening (inlet, outlet, etc.) and assign one or more zones or labels to the capping surface. Create as many caps as required to cover all openings. Choose any advanced options that you want to take effect upon updating the task.  More...
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
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteLabelSelectionList : list[str]
            Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteTopologyList : list[str]

        Returns
        -------
        bool
        """
        class _CappingArguments(PyArguments):
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

            class _PatchName(PyArgumentsTextualSubItem):
                """
                Enter a name for the capping surface.
                """

            class _ZoneType(PyArgumentsTextualSubItem):
                """
                Choose the type of zone to assign to the capping surface (velocity inlet, pressure outlet, etc.).
                """

            class _PatchType(PyArgumentsTextualSubItem):
                """
                Choose the type of capping surface: a regular, simple opening with one or more faces:  or an annular opening where the fluid is within two concentric cylinders:
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to select your surface (by label or by zone).
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _CreatePatchPreferences(PyArgumentsSingletonSubItem):
                """
                Argument CreatePatchPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxCapLimit = self._MaxCapLimit(self, "MaxCapLimit", service, rules, path)
                    self.ShowCreatePatchPreferences = self._ShowCreatePatchPreferences(self, "ShowCreatePatchPreferences", service, rules, path)
                    self.CAPIntersectionCheck = self._CAPIntersectionCheck(self, "CAPIntersectionCheck", service, rules, path)

                class _MaxCapLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify the upper limit for the number of edges that can be present on the capping surface.
                    """

                class _ShowCreatePatchPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _CAPIntersectionCheck(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not the system will detect if the capping surface intersects with any other face in the model. If an intersected face is found, it is automatically deleted. To increase the efficiency of the capping task, this option should be set to "no".
                    """

            class _ObjectAssociation(PyArgumentsTextualSubItem):
                """
                Argument ObjectAssociation.
                """

            class _NewObjectName(PyArgumentsTextualSubItem):
                """
                Argument NewObjectName.
                """

            class _PatchObjectName(PyArgumentsTextualSubItem):
                """
                Argument PatchObjectName.
                """

            class _CapLabels(PyArgumentsTextualSubItem):
                """
                Argument CapLabels.
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _CompleteZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteLabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zone labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteTopologyList(PyArgumentsTextualSubItem):
                """
                Argument CompleteTopologyList.
                """

        def create_instance(self) -> _CappingArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CappingArguments(*args)

    class CheckMesh(PyCommand):
        """
        Command CheckMesh.


        Returns
        -------
        None
        """
        class _CheckMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CheckMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CheckMeshArguments(*args)

    class CheckSurfaceQuality(PyCommand):
        """
        Command CheckSurfaceQuality.


        Returns
        -------
        None
        """
        class _CheckSurfaceQualityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CheckSurfaceQualityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CheckSurfaceQualityArguments(*args)

    class CheckVolumeQuality(PyCommand):
        """
        Command CheckVolumeQuality.


        Returns
        -------
        None
        """
        class _CheckVolumeQualityArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _CheckVolumeQualityArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CheckVolumeQualityArguments(*args)

    class ChooseMeshControlOptions(PyCommand):
        """
        Pick and choose various means of generating and refining the mesh in your simulation. Determine how you want to create and manage and view your size controls in the workflow. More...
        Parameters
        ----------
        ReadOrCreate : str
            Determine whether you want to create new, or use existing mesh size controls or size fields.
        SizeControlFileName : str
            Browse to specify the location and the name of the size control file (.szcontrol) where your mesh controls are defined.
        WrapSizeControlFileName : str
            Browse to specify the location and the name of the size control file (.szcontrol) where your mesh controls are defined.
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
        class _ChooseMeshControlOptionsArguments(PyArguments):
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

            class _ReadOrCreate(PyArgumentsTextualSubItem):
                """
                Determine whether you want to create new, or use existing mesh size controls or size fields.
                """

            class _SizeControlFileName(PyArgumentsTextualSubItem):
                """
                Browse to specify the location and the name of the size control file (.szcontrol) where your mesh controls are defined.
                """

            class _WrapSizeControlFileName(PyArgumentsTextualSubItem):
                """
                Browse to specify the location and the name of the size control file (.szcontrol) where your mesh controls are defined.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Determine whether you want to use default size controls or not. Default will populate your size controls with default settings, based on the number of objects in your model. The Custom option can be used to populate as many size controls as you need using your own customized settings.
                """

            class _ViewOption(PyArgumentsTextualSubItem):
                """
                Determine if you would like to use separate tasks or a table to view and work with your mesh controls.
                """

            class _GlobalMin(PyArgumentsNumericalSubItem):
                """
                Argument GlobalMin.
                """

            class _GlobalMax(PyArgumentsNumericalSubItem):
                """
                Argument GlobalMax.
                """

            class _GlobalGrowthRate(PyArgumentsNumericalSubItem):
                """
                Argument GlobalGrowthRate.
                """

            class _MeshControlOptions(PyArgumentsSingletonSubItem):
                """
                Argument MeshControlOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TargeSizeFieldFileName = self._TargeSizeFieldFileName(self, "TargeSizeFieldFileName", service, rules, path)
                    self.WrapTargetSizeFieldRatio = self._WrapTargetSizeFieldRatio(self, "WrapTargetSizeFieldRatio", service, rules, path)
                    self.WrapTargetBothOptions = self._WrapTargetBothOptions(self, "WrapTargetBothOptions", service, rules, path)
                    self.SolidFluidRaio = self._SolidFluidRaio(self, "SolidFluidRaio", service, rules, path)
                    self.BoundaryLayers = self._BoundaryLayers(self, "BoundaryLayers", service, rules, path)
                    self.EdgeProximityComputation = self._EdgeProximityComputation(self, "EdgeProximityComputation", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.ExistingSizeField = self._ExistingSizeField(self, "ExistingSizeField", service, rules, path)
                    self.TargetSizeFieldFileName = self._TargetSizeFieldFileName(self, "TargetSizeFieldFileName", service, rules, path)
                    self.SolidFluidRatio = self._SolidFluidRatio(self, "SolidFluidRatio", service, rules, path)
                    self.WrapSizeFieldFileName = self._WrapSizeFieldFileName(self, "WrapSizeFieldFileName", service, rules, path)
                    self.WrapTargetRatio = self._WrapTargetRatio(self, "WrapTargetRatio", service, rules, path)
                    self.WrapTargetRaio = self._WrapTargetRaio(self, "WrapTargetRaio", service, rules, path)

                class _TargeSizeFieldFileName(PyArgumentsTextualSubItem):
                    """
                    Indicate the name and location of the target size field file (\\*.sf).
                    """

                class _WrapTargetSizeFieldRatio(PyArgumentsNumericalSubItem):
                    """
                    The ratio of the initial wrap size field and the local target size field.
                    """

                class _WrapTargetBothOptions(PyArgumentsTextualSubItem):
                    """
                    Determine how the size controls are calculated in the Add Local Sizing task: using Both Wrap and Target values, by Target Only (the default), or by Wrap Only. For complex models, computational expense can be lowered by choosing one of the other options. If either Wrap Only or Target Only is selected, then the other values are determined using the Wrap/Target Size Ratio value.
                    """

                class _SolidFluidRaio(PyArgumentsNumericalSubItem):
                    """
                    The ratio of the actual size of the solid and the actual size of the fluid.
                    """

                class _BoundaryLayers(PyArgumentsTextualSubItem):
                    """
                    Argument BoundaryLayers.
                    """

                class _EdgeProximityComputation(PyArgumentsTextualSubItem):
                    """
                    For geometries having a very large number of small feature edges, select Yes to speed up the calculation and reduce memory requirements when using a proximity size function.
                    """

                class _AdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _ExistingSizeField(PyArgumentsTextualSubItem):
                    """
                    Determine which existing size field files will be used: Both Wrap and Target (the default), Target Only, or Wrap Only. For complex models, computational expense can be lowered by choosing one of the other options. If either Wrap Only or Target Only is selected, then the other values are determined using the Wrap/Target Size Ratio value.
                    """

                class _TargetSizeFieldFileName(PyArgumentsTextualSubItem):
                    """
                    Argument TargetSizeFieldFileName.
                    """

                class _SolidFluidRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument SolidFluidRatio.
                    """

                class _WrapSizeFieldFileName(PyArgumentsTextualSubItem):
                    """
                    Indicate the name and location of the wrap size field file (\\*.sf).
                    """

                class _WrapTargetRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument WrapTargetRatio.
                    """

                class _WrapTargetRaio(PyArgumentsNumericalSubItem):
                    """
                    This is the ratio of the wrap size and the target size controls. For example, if this ratio is 0.67 and the initial minimum target size is 1 and initial maximum target size is 16, then the initial minimum wrap size will be 0.67 and the initial maximum wrap size will be 10.72 . This value does not affect BOI or soft size controls, since, in such cases, the Wrap/Target Size Control Ratio is set to 1.
                    """

        def create_instance(self) -> _ChooseMeshControlOptionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChooseMeshControlOptionsArguments(*args)

    class ChoosePartReplacementOptions(PyCommand):
        """
        After creating a volume mesh, use this task to append, add, remove, or replace portions of your original geometry with other CAD parts. By applying localized surface mesh or volume mesh based analyses, you can use this task to quickly update the volume mesh to easily see how geometry changes impact the volume mesh.
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
            Use this task to remove the existing volume mesh and to update the volume mesh with your new part replacement changes.

        Returns
        -------
        bool
        """
        class _ChoosePartReplacementOptionsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddPartManagement = self._AddPartManagement(self, "AddPartManagement", service, rules, path)
                self.AddPartReplacement = self._AddPartReplacement(self, "AddPartReplacement", service, rules, path)
                self.AddLocalSizing = self._AddLocalSizing(self, "AddLocalSizing", service, rules, path)
                self.AddBoundaryLayer = self._AddBoundaryLayer(self, "AddBoundaryLayer", service, rules, path)
                self.AddUpdateTheVolumeMesh = self._AddUpdateTheVolumeMesh(self, "AddUpdateTheVolumeMesh", service, rules, path)

            class _AddPartManagement(PyArgumentsTextualSubItem):
                """
                Determine whether or not you will be appending new CAD parts to your original geometry. Answering Yes will add an Import CAD and Part Management task.
                """

            class _AddPartReplacement(PyArgumentsTextualSubItem):
                """
                Argument AddPartReplacement.
                """

            class _AddLocalSizing(PyArgumentsTextualSubItem):
                """
                Determine whether or not you will need to apply local sizing controls. Answering Yes will add an Add Local Sizing for Part Replacement task.
                """

            class _AddBoundaryLayer(PyArgumentsTextualSubItem):
                """
                Determine whether or not you will need to apply boundary layer (prism controls) to your replacement parts. Answering Yes will add an Add Boundary Layers for Part Replacement task.
                """

            class _AddUpdateTheVolumeMesh(PyArgumentsTextualSubItem):
                """
                Use this task to remove the existing volume mesh and to update the volume mesh with your new part replacement changes.
                """

        def create_instance(self) -> _ChoosePartReplacementOptionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ChoosePartReplacementOptionsArguments(*args)

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
        class _CloseLeakageArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.CloseLeakageOption = self._CloseLeakageOption(self, "CloseLeakageOption", service, rules, path)

            class _CloseLeakageOption(PyArgumentsParameterSubItem):
                """
                Argument CloseLeakageOption.
                """

        def create_instance(self) -> _CloseLeakageArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CloseLeakageArguments(*args)

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
        class _ComplexMeshingRegionsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ComplexMeshingRegionsOption = self._ComplexMeshingRegionsOption(self, "ComplexMeshingRegionsOption", service, rules, path)

            class _ComplexMeshingRegionsOption(PyArgumentsParameterSubItem):
                """
                Argument ComplexMeshingRegionsOption.
                """

        def create_instance(self) -> _ComplexMeshingRegionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ComplexMeshingRegionsArguments(*args)

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
        class _ComputeSizeFieldArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.ComputeSizeFieldControl = self._ComputeSizeFieldControl(self, "ComputeSizeFieldControl", service, rules, path)

            class _ComputeSizeFieldControl(PyArgumentsTextualSubItem):
                """
                Argument ComputeSizeFieldControl.
                """

        def create_instance(self) -> _ComputeSizeFieldArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ComputeSizeFieldArguments(*args)

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
        CylinderMethod : str
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
        CylinderLength : float
        GeometryToolsProperties : dict[str, Any]

        Returns
        -------
        bool
        """
        class _CreateBackgroundMeshArguments(PyArguments):
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
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)
                self.GeometryToolsProperties = self._GeometryToolsProperties(self, "GeometryToolsProperties", service, rules, path)

            class _RefinementRegionsName(PyArgumentsTextualSubItem):
                """
                Argument RefinementRegionsName.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Argument CreationMethod.
                """

            class _BOIMaxSize(PyArgumentsNumericalSubItem):
                """
                Argument BOIMaxSize.
                """

            class _BOISizeName(PyArgumentsTextualSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Argument ZoneSelectionList.
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _ZoneSelectionSingle(PyArgumentsTextualSubItem):
                """
                Argument ZoneSelectionSingle.
                """

            class _ObjectSelectionSingle(PyArgumentsTextualSubItem):
                """
                Argument ObjectSelectionSingle.
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PyArgumentsSingletonSubItem):
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

                class _SizeRelativeLength(PyArgumentsTextualSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _Xmax(PyArgumentsNumericalSubItem):
                    """
                    Argument Xmax.
                    """

                class _XminRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyArgumentsNumericalSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyArgumentsNumericalSubItem):
                    """
                    Argument Zmax.
                    """

                class _Ymax(PyArgumentsNumericalSubItem):
                    """
                    Argument Ymax.
                    """

                class _ZminRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyArgumentsNumericalSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyArgumentsNumericalSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _XmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument XmaxRatio.
                    """

            class _OffsetObject(PyArgumentsSingletonSubItem):
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
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Argument Z.
                    """

                class _WakeLevels(PyArgumentsNumericalSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyArgumentsParameterSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Argument Y.
                    """

                class _DefeaturingSize(PyArgumentsNumericalSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _AspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _WakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _NumberOfLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _Rate(PyArgumentsNumericalSubItem):
                    """
                    Argument Rate.
                    """

                class _FlowDirection(PyArgumentsTextualSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyArgumentsTextualSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyArgumentsTextualSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _BoundaryLayerLevels(PyArgumentsNumericalSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Argument X.
                    """

                class _FlipDirection(PyArgumentsParameterSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _OffsetMethodType(PyArgumentsTextualSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FirstHeight(PyArgumentsNumericalSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyArgumentsNumericalSubItem):
                    """
                    Argument BoundaryLayerHeight.
                    """

                class _CrossWakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderMethod(PyArgumentsTextualSubItem):
                """
                Argument CylinderMethod.
                """

            class _CylinderObject(PyArgumentsSingletonSubItem):
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
                    self.Z1 = self._Z1(self, "Z1", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Z2 = self._Z2(self, "Z2", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Y2 = self._Y2(self, "Y2", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyArgumentsTextualSubItem):
                    """
                    Argument HeightNode.
                    """

                class _X_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightBackInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyArgumentsNumericalSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyArgumentsNumericalSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z1(PyArgumentsNumericalSubItem):
                    """
                    Argument Z1.
                    """

                class _Node1(PyArgumentsTextualSubItem):
                    """
                    Argument Node1.
                    """

                class _Z2(PyArgumentsNumericalSubItem):
                    """
                    Argument Z2.
                    """

                class _Radius2(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyArgumentsNumericalSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyArgumentsTextualSubItem):
                    """
                    Argument Node3.
                    """

                class _Node2(PyArgumentsTextualSubItem):
                    """
                    Argument Node2.
                    """

                class _Y_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _X2(PyArgumentsNumericalSubItem):
                    """
                    Argument X2.
                    """

                class _HeightFrontInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PyArgumentsSingletonSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyArgumentsTextualSubItem):
                """
                Argument VolumeFill.
                """

            class _CylinderLength(PyArgumentsNumericalSubItem):
                """
                Argument CylinderLength.
                """

            class _GeometryToolsProperties(PyArgumentsSingletonSubItem):
                """
                Argument GeometryToolsProperties.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.CylinderZ2 = self._CylinderZ2(self, "CylinderZ2", service, rules, path)
                    self.CylinderX2 = self._CylinderX2(self, "CylinderX2", service, rules, path)
                    self.BoxYLength = self._BoxYLength(self, "BoxYLength", service, rules, path)
                    self.CylinderX1 = self._CylinderX1(self, "CylinderX1", service, rules, path)
                    self.BoxXLength = self._BoxXLength(self, "BoxXLength", service, rules, path)
                    self.CylinderY1 = self._CylinderY1(self, "CylinderY1", service, rules, path)
                    self.BoxZLength = self._BoxZLength(self, "BoxZLength", service, rules, path)
                    self.BoxCenterY = self._BoxCenterY(self, "BoxCenterY", service, rules, path)
                    self.CylinderZ1 = self._CylinderZ1(self, "CylinderZ1", service, rules, path)
                    self.CylinderRadius1 = self._CylinderRadius1(self, "CylinderRadius1", service, rules, path)
                    self.BoxCenterX = self._BoxCenterX(self, "BoxCenterX", service, rules, path)
                    self.CylinderRadius2 = self._CylinderRadius2(self, "CylinderRadius2", service, rules, path)
                    self.BoxCenterZ = self._BoxCenterZ(self, "BoxCenterZ", service, rules, path)
                    self.CylinderY2 = self._CylinderY2(self, "CylinderY2", service, rules, path)

                class _CylinderZ2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderZ2.
                    """

                class _CylinderX2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderX2.
                    """

                class _BoxYLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxYLength.
                    """

                class _CylinderX1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderX1.
                    """

                class _BoxXLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxXLength.
                    """

                class _CylinderY1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderY1.
                    """

                class _BoxZLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxZLength.
                    """

                class _BoxCenterY(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxCenterY.
                    """

                class _CylinderZ1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderZ1.
                    """

                class _CylinderRadius1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderRadius1.
                    """

                class _BoxCenterX(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxCenterX.
                    """

                class _CylinderRadius2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderRadius2.
                    """

                class _BoxCenterZ(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxCenterZ.
                    """

                class _CylinderY2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderY2.
                    """

        def create_instance(self) -> _CreateBackgroundMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateBackgroundMeshArguments(*args)

    class CreateCollarMesh(PyCommand):
        """
        Use this task to create an overset collar mesh. You can use various techniques, such as using intersecting objects, using an edge-based approach, or using an existing object. 
                        More...
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
        CylinderMethod : str
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
            Specify the type of mesh cell to use to fill the collar mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
        CylinderLength : float
        GeometryToolsProperties : dict[str, Any]

        Returns
        -------
        bool
        """
        class _CreateCollarMeshArguments(PyArguments):
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
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)
                self.GeometryToolsProperties = self._GeometryToolsProperties(self, "GeometryToolsProperties", service, rules, path)

            class _RefinementRegionsName(PyArgumentsTextualSubItem):
                """
                Specify a name for the collar mesh or use the default name.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Choose how you want to create the collar mesh: either by using intersecting objects, an edge-based collar, or an existing object.
                """

            class _BOIMaxSize(PyArgumentsNumericalSubItem):
                """
                Specify the maximum size of the elements for the collar mesh.
                """

            class _BOISizeName(PyArgumentsTextualSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more labels that will make up the collar mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PyArgumentsSingletonSubItem):
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

                class _SizeRelativeLength(PyArgumentsTextualSubItem):
                    """
                    Argument SizeRelativeLength.
                    """

                class _XmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument XmaxRatio.
                    """

                class _XminRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument XminRatio.
                    """

                class _YminRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument YminRatio.
                    """

                class _Zmin(PyArgumentsNumericalSubItem):
                    """
                    Argument Zmin.
                    """

                class _Zmax(PyArgumentsNumericalSubItem):
                    """
                    Specify the x-coordinate of the offset collar mesh.
                    """

                class _Ymax(PyArgumentsNumericalSubItem):
                    """
                    Specify the x-coordinate of the offset collar mesh.
                    """

                class _ZminRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument ZminRatio.
                    """

                class _Ymin(PyArgumentsNumericalSubItem):
                    """
                    Argument Ymin.
                    """

                class _Xmin(PyArgumentsNumericalSubItem):
                    """
                    Argument Xmin.
                    """

                class _YmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument YmaxRatio.
                    """

                class _ZmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument ZmaxRatio.
                    """

                class _Xmax(PyArgumentsNumericalSubItem):
                    """
                    Specify the x-coordinate of the offset collar mesh.
                    """

            class _OffsetObject(PyArgumentsSingletonSubItem):
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
                    self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Specify the z-coordinate of the offset collar mesh.
                    """

                class _WakeLevels(PyArgumentsNumericalSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyArgumentsParameterSubItem):
                    """
                    Display the X, Y, and Z coordinate fields
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Specify the y-coordinate of the offset collar mesh.
                    """

                class _DefeaturingSize(PyArgumentsNumericalSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _BoundaryLayerLevels(PyArgumentsNumericalSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _WakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _NumberOfLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _AspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _FlowDirection(PyArgumentsTextualSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyArgumentsTextualSubItem):
                    """
                    Choose how you want to assign the location of the offset collar mesh. You can choose Automatic to have the system determine the best place for the collar mesh based on the intersected bodies or zones, or you can choose to use distinct Numerical Inputs.
                    """

                class _EdgeSelectionList(PyArgumentsTextualSubItem):
                    """
                    Choose a single edge zone from the list below for your edge-based collar mesh. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _Rate(PyArgumentsNumericalSubItem):
                    """
                    Argument Rate.
                    """

                class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Specify the x-coordinate of the offset collar mesh.
                    """

                class _FlipDirection(PyArgumentsParameterSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _OffsetMethodType(PyArgumentsTextualSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FirstHeight(PyArgumentsNumericalSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyArgumentsNumericalSubItem):
                    """
                    Specify the total height of the boundary layer for this refinement region (this is flow in the vicinity).
                    """

                class _CrossWakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderMethod(PyArgumentsTextualSubItem):
                """
                Argument CylinderMethod.
                """

            class _CylinderObject(PyArgumentsSingletonSubItem):
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
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyArgumentsTextualSubItem):
                    """
                    Argument HeightNode.
                    """

                class _X_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightBackInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyArgumentsNumericalSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyArgumentsNumericalSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyArgumentsNumericalSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyArgumentsTextualSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyArgumentsNumericalSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyArgumentsNumericalSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyArgumentsTextualSubItem):
                    """
                    Argument Node3.
                    """

                class _Node2(PyArgumentsTextualSubItem):
                    """
                    Argument Node2.
                    """

                class _X2(PyArgumentsNumericalSubItem):
                    """
                    Argument X2.
                    """

                class _Y_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _HeightFrontInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PyArgumentsSingletonSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyArgumentsTextualSubItem):
                """
                Specify the type of mesh cell to use to fill the collar mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
                """

            class _CylinderLength(PyArgumentsNumericalSubItem):
                """
                Argument CylinderLength.
                """

            class _GeometryToolsProperties(PyArgumentsSingletonSubItem):
                """
                Argument GeometryToolsProperties.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.CylinderZ2 = self._CylinderZ2(self, "CylinderZ2", service, rules, path)
                    self.CylinderX2 = self._CylinderX2(self, "CylinderX2", service, rules, path)
                    self.BoxYLength = self._BoxYLength(self, "BoxYLength", service, rules, path)
                    self.CylinderX1 = self._CylinderX1(self, "CylinderX1", service, rules, path)
                    self.BoxZLength = self._BoxZLength(self, "BoxZLength", service, rules, path)
                    self.CylinderY1 = self._CylinderY1(self, "CylinderY1", service, rules, path)
                    self.BoxXLength = self._BoxXLength(self, "BoxXLength", service, rules, path)
                    self.BoxCenterY = self._BoxCenterY(self, "BoxCenterY", service, rules, path)
                    self.CylinderZ1 = self._CylinderZ1(self, "CylinderZ1", service, rules, path)
                    self.CylinderRadius1 = self._CylinderRadius1(self, "CylinderRadius1", service, rules, path)
                    self.BoxCenterX = self._BoxCenterX(self, "BoxCenterX", service, rules, path)
                    self.CylinderRadius2 = self._CylinderRadius2(self, "CylinderRadius2", service, rules, path)
                    self.BoxCenterZ = self._BoxCenterZ(self, "BoxCenterZ", service, rules, path)
                    self.CylinderY2 = self._CylinderY2(self, "CylinderY2", service, rules, path)

                class _CylinderZ2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderZ2.
                    """

                class _CylinderX2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderX2.
                    """

                class _BoxYLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxYLength.
                    """

                class _CylinderX1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderX1.
                    """

                class _BoxZLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxZLength.
                    """

                class _CylinderY1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderY1.
                    """

                class _BoxXLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxXLength.
                    """

                class _BoxCenterY(PyArgumentsNumericalSubItem):
                    """
                    Specify the y-coordinate of the offset collar mesh.
                    """

                class _CylinderZ1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderZ1.
                    """

                class _CylinderRadius1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderRadius1.
                    """

                class _BoxCenterX(PyArgumentsNumericalSubItem):
                    """
                    Specify the x-coordinate of the offset collar mesh.
                    """

                class _CylinderRadius2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderRadius2.
                    """

                class _BoxCenterZ(PyArgumentsNumericalSubItem):
                    """
                    Specify the z-coordinate of the offset collar mesh.
                    """

                class _CylinderY2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderY2.
                    """

        def create_instance(self) -> _CreateCollarMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateCollarMeshArguments(*args)

    class CreateComponentMesh(PyCommand):
        """
        Use this task to create an overset component mesh. You can use various techniques, such as using an offset surface, a bounding box, or an existing object. 
                        More...
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
        CylinderMethod : str
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
            Specify the type of mesh cell to use to fill the component mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
        CylinderLength : float
        GeometryToolsProperties : dict[str, Any]

        Returns
        -------
        bool
        """
        class _CreateComponentMeshArguments(PyArguments):
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
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)
                self.GeometryToolsProperties = self._GeometryToolsProperties(self, "GeometryToolsProperties", service, rules, path)

            class _RefinementRegionsName(PyArgumentsTextualSubItem):
                """
                Specify a name for the component mesh or use the default value.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Choose how you want to create the component mesh: either by using an offset surface, creating a bounding box, using an existing portion of the geometry, or by growing a boundary layer.
                """

            class _BOIMaxSize(PyArgumentsNumericalSubItem):
                """
                Specify the maximum size of the elements for the component mesh.
                """

            class _BOISizeName(PyArgumentsTextualSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more labels that will make up the component mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PyArgumentsSingletonSubItem):
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

                class _SizeRelativeLength(PyArgumentsTextualSubItem):
                    """
                    Determine if you would like to specify the bounding box for the component mesh as a ratio of the geometry length, or by specifying a specific location for the minimum and maximum coordinates.
                    """

                class _Xmax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value.
                    """

                class _XminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

                class _YminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _Zmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value.
                    """

                class _Zmax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value.
                    """

                class _Ymax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value.
                    """

                class _ZminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _Ymin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value.
                    """

                class _Xmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value.
                    """

                class _YmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _ZmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _XmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

            class _OffsetObject(PyArgumentsSingletonSubItem):
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
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Argument Z.
                    """

                class _WakeLevels(PyArgumentsNumericalSubItem):
                    """
                    Argument WakeLevels.
                    """

                class _ShowCoordinates(PyArgumentsParameterSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Argument Y.
                    """

                class _DefeaturingSize(PyArgumentsNumericalSubItem):
                    """
                    Argument DefeaturingSize.
                    """

                class _AspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Specify the ratio of the prism base length to the prism layer height.
                    """

                class _WakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _NumberOfLayers(PyArgumentsNumericalSubItem):
                    """
                    Select the number of boundary layers to be generated.
                    """

                class _Rate(PyArgumentsNumericalSubItem):
                    """
                    Specify the rate of growth of the boundary layer.
                    """

                class _FlowDirection(PyArgumentsTextualSubItem):
                    """
                    Argument FlowDirection.
                    """

                class _MptMethodType(PyArgumentsTextualSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyArgumentsTextualSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _BoundaryLayerLevels(PyArgumentsNumericalSubItem):
                    """
                    Argument BoundaryLayerLevels.
                    """

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Argument X.
                    """

                class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                    """
                    Specify the offset height of the last layer as a percentage of the local base mesh size.
                    """

                class _OffsetMethodType(PyArgumentsTextualSubItem):
                    """
                    Choose the method that will be used to create the boundary layer, or prism, controls.
                    """

                class _FlipDirection(PyArgumentsParameterSubItem):
                    """
                    Argument FlipDirection.
                    """

                class _FirstHeight(PyArgumentsNumericalSubItem):
                    """
                    Specify the height of the first layer of cells in the boundary layer.
                    """

                class _BoundaryLayerHeight(PyArgumentsNumericalSubItem):
                    """
                    Specify the total height of the boundary layer for this refinement region (this is flow in the vicinity).
                    """

                class _CrossWakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument CrossWakeGrowthFactor.
                    """

            class _CylinderMethod(PyArgumentsTextualSubItem):
                """
                Argument CylinderMethod.
                """

            class _CylinderObject(PyArgumentsSingletonSubItem):
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
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyArgumentsTextualSubItem):
                    """
                    Argument HeightNode.
                    """

                class _X_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightBackInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyArgumentsNumericalSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyArgumentsNumericalSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyArgumentsNumericalSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyArgumentsTextualSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyArgumentsNumericalSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyArgumentsNumericalSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyArgumentsTextualSubItem):
                    """
                    Argument Node3.
                    """

                class _Node2(PyArgumentsTextualSubItem):
                    """
                    Argument Node2.
                    """

                class _X2(PyArgumentsNumericalSubItem):
                    """
                    Argument X2.
                    """

                class _Y_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _HeightFrontInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius1.
                    """

            class _Axis(PyArgumentsSingletonSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _VolumeFill(PyArgumentsTextualSubItem):
                """
                Specify the type of mesh cell to use to fill the component mesh. Available options are tetrahedral, hexcore, poly, or poly-hexcore. .
                """

            class _CylinderLength(PyArgumentsNumericalSubItem):
                """
                Argument CylinderLength.
                """

            class _GeometryToolsProperties(PyArgumentsSingletonSubItem):
                """
                Argument GeometryToolsProperties.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.CylinderZ2 = self._CylinderZ2(self, "CylinderZ2", service, rules, path)
                    self.BoxYLength = self._BoxYLength(self, "BoxYLength", service, rules, path)
                    self.CylinderX2 = self._CylinderX2(self, "CylinderX2", service, rules, path)
                    self.CylinderX1 = self._CylinderX1(self, "CylinderX1", service, rules, path)
                    self.BoxXLength = self._BoxXLength(self, "BoxXLength", service, rules, path)
                    self.CylinderY1 = self._CylinderY1(self, "CylinderY1", service, rules, path)
                    self.BoxZLength = self._BoxZLength(self, "BoxZLength", service, rules, path)
                    self.BoxCenterY = self._BoxCenterY(self, "BoxCenterY", service, rules, path)
                    self.CylinderZ1 = self._CylinderZ1(self, "CylinderZ1", service, rules, path)
                    self.CylinderRadius1 = self._CylinderRadius1(self, "CylinderRadius1", service, rules, path)
                    self.BoxCenterX = self._BoxCenterX(self, "BoxCenterX", service, rules, path)
                    self.BoxCenterZ = self._BoxCenterZ(self, "BoxCenterZ", service, rules, path)
                    self.CylinderRadius2 = self._CylinderRadius2(self, "CylinderRadius2", service, rules, path)
                    self.CylinderY2 = self._CylinderY2(self, "CylinderY2", service, rules, path)

                class _CylinderZ2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderZ2.
                    """

                class _BoxYLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxYLength.
                    """

                class _CylinderX2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderX2.
                    """

                class _CylinderX1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderX1.
                    """

                class _BoxXLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxXLength.
                    """

                class _CylinderY1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderY1.
                    """

                class _BoxZLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxZLength.
                    """

                class _BoxCenterY(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxCenterY.
                    """

                class _CylinderZ1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderZ1.
                    """

                class _CylinderRadius1(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderRadius1.
                    """

                class _BoxCenterX(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxCenterX.
                    """

                class _BoxCenterZ(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxCenterZ.
                    """

                class _CylinderRadius2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderRadius2.
                    """

                class _CylinderY2(PyArgumentsNumericalSubItem):
                    """
                    Argument CylinderY2.
                    """

        def create_instance(self) -> _CreateComponentMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateComponentMeshArguments(*args)

    class CreateContactPatch(PyCommand):
        """
        This task will create patches in and around any problematic, sharp-angle contact areas (such as between a tire and the road surface) in order to avoid such areas during the meshing process. More...
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
        class _CreateContactPatchArguments(PyArguments):
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

            class _ContactPatchName(PyArgumentsTextualSubItem):
                """
                Specify a name for the contact patch object, or retain the default name.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (for instance, by object, zone, or label).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose an object from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more labels that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GroundZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below that represent the contact target (for instance, the ground face zone in an enclosing bounding box for a tire-ground contact scenario).
                """

            class _Distance(PyArgumentsNumericalSubItem):
                """
                Specify the distance of the contact patch geometry from the ground zone, or the thickness of the contact patch.
                """

            class _ContactPatchDefeaturingSize(PyArgumentsNumericalSubItem):
                """
                Allows you to control the smoothness of the contact patch. With the default value of 0, no smoothing takes place. With a value greater than 0, the patch is defeatured to create a smooth patch. This will lead to better quality volume mesh at the contact, for instance, between the tire and the ground.
                """

            class _FeatureAngle(PyArgumentsNumericalSubItem):
                """
                Specify a value for the angle used to extract feature edges on the contact patch object.
                """

            class _PatchHole(PyArgumentsParameterSubItem):
                """
                Indicate whether you want the contact patch object to be filled or not.
                """

            class _FlipDirection(PyArgumentsParameterSubItem):
                """
                Use this option to switch the direction/orientation of the contact patch.
                """

        def create_instance(self) -> _CreateContactPatchArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateContactPatchArguments(*args)

    class CreateExternalFlowBoundaries(PyCommand):
        """
        Create an enclosure, or a bounding box, around the geometry, or use a pre-existing object from the CAD model to represent the enclosure. This enclosure will represent the external flow region, whose bounds can be specified as a ratio of geometry size, or as specific minimum and maximum coordinates. More...
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
        class _CreateExternalFlowBoundariesArguments(PyArguments):
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

            class _ExternalBoundariesName(PyArgumentsTextualSubItem):
                """
                Enter a name for the external flow boundary or use the default value.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Choose how you want to create the external flow boundary: either by creating a new boundary using a bounding box, or use an existing portion of the geometry.
                """

            class _ExtractionMethod(PyArgumentsTextualSubItem):
                """
                Choose whether you would like to extract the external flow region either as a surface mesh object (a direct surface remesh of the object) a wrap, or an existing mesh (for overset components). The object setting is applied later when generating the surface mesh.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single label from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _OriginalObjectName(PyArgumentsTextualSubItem):
                """
                Argument OriginalObjectName.
                """

            class _BoundingBoxObject(PyArgumentsSingletonSubItem):
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

                class _SizeRelativeLength(PyArgumentsTextualSubItem):
                    """
                    Determine if you would like to specify the bounding box as a ratio of the geometry length, or by specifying a specific location for the minimum and maximum coordinates.
                    """

                class _Xmax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value.
                    """

                class _XminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

                class _YminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _Zmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value.
                    """

                class _Zmax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value.
                    """

                class _Ymax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value.
                    """

                class _ZminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _Ymin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value.
                    """

                class _Xmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value.
                    """

                class _YmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _ZmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _XmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

        def create_instance(self) -> _CreateExternalFlowBoundariesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateExternalFlowBoundariesArguments(*args)

    class CreateGapCover(PyCommand):
        """
        This task will cover any gaps within a selected object. Recommended with geometries containing noticeable gaps and openings that need to be covered prior to surface meshing. More...
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
        class _CreateGapCoverArguments(PyArguments):
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

            class _GapCoverName(PyArgumentsTextualSubItem):
                """
                Specify a name for the gap cover object, or retain the default name.
                """

            class _SizingMethod(PyArgumentsTextualSubItem):
                """
                Determine the method for specifying the gap cover sizing controls. The Wrapper Based on Size Field option uses the size field control settings defined in the Choose Mesh Controls task. Using the Uniform Wrapper option requires you to provide a value for the Max Gap Size. If this task is located at a point in the workflow prior to the Choose Mesh Control Options task, then only the Uniform Wrapper option is available.
                """

            class _GapSizeRatio(PyArgumentsNumericalSubItem):
                """
                Specify a value for the gap size factor that, when multiplied by the local initial size field, corresponds to the size of the gap that needs to be covered.
                """

            class _GapSize(PyArgumentsNumericalSubItem):
                """
                A specified maximum width for the gap.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (for instance, by object name, zone name, or label name).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more labels that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose an object from the list below that represent the contact source. Use the Filter Text field to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GapCoverBetweenZones(PyArgumentsTextualSubItem):
                """
                Determine if you only want to cover gaps between boundary zones (Yes), or if you want to cover all gaps within and between boundary zones (No)
                """

            class _GapCoverRefineFactor(PyArgumentsNumericalSubItem):
                """
                Allows you to control the resolution of the gap cover size based on a scaling of the Max Gap Size (or Max Gap Size Factor). It ranges from 0.0625 to 1 with a default value of 1.0). The higher the Resolution Factor, the more likely that some gaps may not be fully covered. Depending on the gap in question, lowering the Resolution Factor reduces the wrapper to sufficiently cover the gap in most cases.
                """

            class _GapCoverRefineFactorAtGap(PyArgumentsNumericalSubItem):
                """
                Allows you to specify the level of refinement for the gap-cover (patch). Decreasing the value increases the refinement of the patch.
                """

            class _RefineWrapperBeforeProjection(PyArgumentsTextualSubItem):
                """
                Argument RefineWrapperBeforeProjection.
                """

            class _AdvancedOptions(PyArgumentsParameterSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _MaxIslandFaceForGapCover(PyArgumentsNumericalSubItem):
                """
                Specify the maximum face count required for isolated areas (islands) to be created during surface mesh generation. Any islands that have a face count smaller than this value will be removed, and only larger islands will remain.
                """

            class _GapCoverFeatureImprint(PyArgumentsTextualSubItem):
                """
                Use this option to better define gap coverings. When this option is set to Yes, the gap covers are more accurate. Once the coarse wrap closes any gaps, this option also snaps the nodes of the wrapper onto all previously defined edge features to more closely cover the gaps. Setting this option to Yes, however, can be computationally expensive when modeling large vehicles (such as in aerospace), thus, the default is No.  Here, when set to No, wrapper faces at the corners are not on the geometry and are incorrectly marked as a gap. When set to Yes, only wrap faces at the gap are marked.
                """

        def create_instance(self) -> _CreateGapCoverArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateGapCoverArguments(*args)

    class CreateGroup(PyCommand):
        """
        Command CreateGroup.

        Parameters
        ----------
        NewGroupName : str
        SelectionType : str
        TopologyList : list[str]

        Returns
        -------
        bool
        """
        class _CreateGroupArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.NewGroupName = self._NewGroupName(self, "NewGroupName", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)

            class _NewGroupName(PyArgumentsTextualSubItem):
                """
                Argument NewGroupName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

        def create_instance(self) -> _CreateGroupArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateGroupArguments(*args)

    class CreateLeakShield(PyCommand):
        """
        Command CreateLeakShield.

        Parameters
        ----------
        LeakShieldName : str
        UseSizeField : str
        SizeFieldFileName : str
        MaxHoleSize : float
        MinHoleSize : float
        SpecifyObj : bool
        SpecifyLive : bool
        SpecifyDead : bool
        ObjectSelectionList : list[str]
        LiveMptSelectionList : list[str]
        DeadRegionsList : list[str]
        PatchAtLive : str
        PromptForCleanup : str
        MergePatches : str

        Returns
        -------
        bool
        """
        class _CreateLeakShieldArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LeakShieldName = self._LeakShieldName(self, "LeakShieldName", service, rules, path)
                self.UseSizeField = self._UseSizeField(self, "UseSizeField", service, rules, path)
                self.SizeFieldFileName = self._SizeFieldFileName(self, "SizeFieldFileName", service, rules, path)
                self.MaxHoleSize = self._MaxHoleSize(self, "MaxHoleSize", service, rules, path)
                self.MinHoleSize = self._MinHoleSize(self, "MinHoleSize", service, rules, path)
                self.SpecifyObj = self._SpecifyObj(self, "SpecifyObj", service, rules, path)
                self.SpecifyLive = self._SpecifyLive(self, "SpecifyLive", service, rules, path)
                self.SpecifyDead = self._SpecifyDead(self, "SpecifyDead", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)
                self.LiveMptSelectionList = self._LiveMptSelectionList(self, "LiveMptSelectionList", service, rules, path)
                self.DeadRegionsList = self._DeadRegionsList(self, "DeadRegionsList", service, rules, path)
                self.PatchAtLive = self._PatchAtLive(self, "PatchAtLive", service, rules, path)
                self.PromptForCleanup = self._PromptForCleanup(self, "PromptForCleanup", service, rules, path)
                self.MergePatches = self._MergePatches(self, "MergePatches", service, rules, path)

            class _LeakShieldName(PyArgumentsTextualSubItem):
                """
                Argument LeakShieldName.
                """

            class _UseSizeField(PyArgumentsTextualSubItem):
                """
                Argument UseSizeField.
                """

            class _SizeFieldFileName(PyArgumentsTextualSubItem):
                """
                Argument SizeFieldFileName.
                """

            class _MaxHoleSize(PyArgumentsNumericalSubItem):
                """
                Argument MaxHoleSize.
                """

            class _MinHoleSize(PyArgumentsNumericalSubItem):
                """
                Argument MinHoleSize.
                """

            class _SpecifyObj(PyArgumentsParameterSubItem):
                """
                Argument SpecifyObj.
                """

            class _SpecifyLive(PyArgumentsParameterSubItem):
                """
                Argument SpecifyLive.
                """

            class _SpecifyDead(PyArgumentsParameterSubItem):
                """
                Argument SpecifyDead.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _LiveMptSelectionList(PyArgumentsTextualSubItem):
                """
                Argument LiveMptSelectionList.
                """

            class _DeadRegionsList(PyArgumentsTextualSubItem):
                """
                Argument DeadRegionsList.
                """

            class _PatchAtLive(PyArgumentsTextualSubItem):
                """
                Argument PatchAtLive.
                """

            class _PromptForCleanup(PyArgumentsTextualSubItem):
                """
                Argument PromptForCleanup.
                """

            class _MergePatches(PyArgumentsTextualSubItem):
                """
                Argument MergePatches.
                """

        def create_instance(self) -> _CreateLeakShieldArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateLeakShieldArguments(*args)

    class CreateLocalRefinementRegions(PyCommand):
        """
        Define a more refined region, or body of influence (BOI) when simulating flow within or around your geometry. You can manually create a body of influence using a bounding box or by using an offset surface. This body surrounds the relevant aspects of your geometry, such as the wake region behind a vehicle. More...
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
        CylinderMethod : str
            Choose how the cylindrical refinement region will be defined. The Vector and Length option allows you to define the cylindrical refinement region based either on the location of selected object(s) or zone(s), or by coordinates. If you choose to select by object(s) or zone(s), the location of the cylindrical refinement region will be at the center point of the selected surface. The Two Positions option allows you to explicitly define the location and dimension of the cylindrical refinement region without having to select object(s) or zone(s).
        CylinderObject : dict[str, Any]
        Axis : dict[str, Any]
        VolumeFill : str
        CylinderLength : float
            Specify the Length of the cylinder.
        GeometryToolsProperties : dict[str, Any]

        Returns
        -------
        bool
        """
        class _CreateLocalRefinementRegionsArguments(PyArguments):
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
                self.CylinderMethod = self._CylinderMethod(self, "CylinderMethod", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.Axis = self._Axis(self, "Axis", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)
                self.CylinderLength = self._CylinderLength(self, "CylinderLength", service, rules, path)
                self.GeometryToolsProperties = self._GeometryToolsProperties(self, "GeometryToolsProperties", service, rules, path)

            class _RefinementRegionsName(PyArgumentsTextualSubItem):
                """
                Enter a name for the body of influence.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Choose how you want to create the refinement region: by creating a bounding box, a cylindrical bounding region, or using an offset surface. You should select a closed body for the offset surface.
                """

            class _BOIMaxSize(PyArgumentsNumericalSubItem):
                """
                Specify the cell size for the refinement region mesh.
                """

            class _BOISizeName(PyArgumentsTextualSubItem):
                """
                Argument BOISizeName.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyArgumentsTextualSubItem):
                """
                Argument ZoneSelectionSingle.
                """

            class _ObjectSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _BoundingBoxObject(PyArgumentsSingletonSubItem):
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

                class _SizeRelativeLength(PyArgumentsTextualSubItem):
                    """
                    Determine if you would like to specify the bounding box for the refinement region as a ratio of the geometry length, or by specifying a specific location for the minimum and maximum coordinates.
                    """

                class _Xmax(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _XminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

                class _YminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _Zmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value.
                    """

                class _Zmax(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _Ymax(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _ZminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _Ymin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value.
                    """

                class _Xmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value.
                    """

                class _YmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _ZmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _XmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

            class _OffsetObject(PyArgumentsSingletonSubItem):
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
                    self.AspectRatio = self._AspectRatio(self, "AspectRatio", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)
                    self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                    self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                    self.BoundaryLayerHeight = self._BoundaryLayerHeight(self, "BoundaryLayerHeight", service, rules, path)
                    self.CrossWakeGrowthFactor = self._CrossWakeGrowthFactor(self, "CrossWakeGrowthFactor", service, rules, path)

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _WakeLevels(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of refinement layers that will appear in the wake.
                    """

                class _ShowCoordinates(PyArgumentsParameterSubItem):
                    """
                    Argument ShowCoordinates.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _DefeaturingSize(PyArgumentsNumericalSubItem):
                    """
                    Specify a value that is used to obtain a rough shape of the selected object(s). The larger the value, the more approximate the shape.
                    """

                class _AspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument AspectRatio.
                    """

                class _NumberOfLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _Rate(PyArgumentsNumericalSubItem):
                    """
                    Argument Rate.
                    """

                class _BoundaryLayerLevels(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of boundary layers that are to be captured in the refinement region.
                    """

                class _FlowDirection(PyArgumentsTextualSubItem):
                    """
                    Specify the direction that the flow through this refinement region.
                    """

                class _MptMethodType(PyArgumentsTextualSubItem):
                    """
                    Argument MptMethodType.
                    """

                class _EdgeSelectionList(PyArgumentsTextualSubItem):
                    """
                    Argument EdgeSelectionList.
                    """

                class _WakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Specify the factor by which the refinement region expands in the wake of the flow direction.
                    """

                class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                    """
                    Argument LastRatioPercentage.
                    """

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _FlipDirection(PyArgumentsParameterSubItem):
                    """
                    Reverses the orientation of the refinement region.
                    """

                class _OffsetMethodType(PyArgumentsTextualSubItem):
                    """
                    Argument OffsetMethodType.
                    """

                class _FirstHeight(PyArgumentsNumericalSubItem):
                    """
                    Argument FirstHeight.
                    """

                class _BoundaryLayerHeight(PyArgumentsNumericalSubItem):
                    """
                    Specify the total height of the boundary layer for this refinement region (this is flow in the vicinity).
                    """

                class _CrossWakeGrowthFactor(PyArgumentsNumericalSubItem):
                    """
                    Specify the factor by which the refinement region expands in the rest of the directions.
                    """

            class _CylinderMethod(PyArgumentsTextualSubItem):
                """
                Choose how the cylindrical refinement region will be defined. The Vector and Length option allows you to define the cylindrical refinement region based either on the location of selected object(s) or zone(s), or by coordinates. If you choose to select by object(s) or zone(s), the location of the cylindrical refinement region will be at the center point of the selected surface. The Two Positions option allows you to explicitly define the location and dimension of the cylindrical refinement region without having to select object(s) or zone(s).
                """

            class _CylinderObject(PyArgumentsSingletonSubItem):
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
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.X2 = self._X2(self, "X2", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _X_Offset(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate for the offset of the initial position of the cylinder.
                    """

                class _HeightNode(PyArgumentsTextualSubItem):
                    """
                    Argument HeightNode.
                    """

                class _HeightBackInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the first position of the cylinder.
                    """

                class _Y1(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the first position of the cylinder.
                    """

                class _Z_Offset(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate for the offset of the initial position of the cylinder.
                    """

                class _Z1(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the first position of the cylinder.
                    """

                class _Node1(PyArgumentsTextualSubItem):
                    """
                    Argument Node1.
                    """

                class _Z2(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the second position of the cylinder.
                    """

                class _Radius2(PyArgumentsNumericalSubItem):
                    """
                    Specify the radius of the cylinder at the second position.
                    """

                class _Y2(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the second position of the cylinder.
                    """

                class _Node3(PyArgumentsTextualSubItem):
                    """
                    Argument Node3.
                    """

                class _Y_Offset(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate for the offset of the initial position of the cylinder.
                    """

                class _X2(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the second position of the cylinder.
                    """

                class _Node2(PyArgumentsTextualSubItem):
                    """
                    Argument Node2.
                    """

                class _HeightFrontInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyArgumentsNumericalSubItem):
                    """
                    Specify the radius of the cylinder at the initial position.
                    """

            class _Axis(PyArgumentsSingletonSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-component of the cylindrical vector.
                    """

                class _X_Comp(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-component of the cylindrical vector.
                    """

                class _Y_Comp(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-component of the cylindrical vector.
                    """

            class _VolumeFill(PyArgumentsTextualSubItem):
                """
                Argument VolumeFill.
                """

            class _CylinderLength(PyArgumentsNumericalSubItem):
                """
                Specify the Length of the cylinder.
                """

            class _GeometryToolsProperties(PyArgumentsSingletonSubItem):
                """
                Argument GeometryToolsProperties.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.CylinderZ2 = self._CylinderZ2(self, "CylinderZ2", service, rules, path)
                    self.BoxYLength = self._BoxYLength(self, "BoxYLength", service, rules, path)
                    self.CylinderX2 = self._CylinderX2(self, "CylinderX2", service, rules, path)
                    self.CylinderX1 = self._CylinderX1(self, "CylinderX1", service, rules, path)
                    self.BoxZLength = self._BoxZLength(self, "BoxZLength", service, rules, path)
                    self.CylinderY1 = self._CylinderY1(self, "CylinderY1", service, rules, path)
                    self.BoxXLength = self._BoxXLength(self, "BoxXLength", service, rules, path)
                    self.BoxCenterY = self._BoxCenterY(self, "BoxCenterY", service, rules, path)
                    self.CylinderZ1 = self._CylinderZ1(self, "CylinderZ1", service, rules, path)
                    self.CylinderRadius1 = self._CylinderRadius1(self, "CylinderRadius1", service, rules, path)
                    self.BoxCenterX = self._BoxCenterX(self, "BoxCenterX", service, rules, path)
                    self.BoxCenterZ = self._BoxCenterZ(self, "BoxCenterZ", service, rules, path)
                    self.CylinderRadius2 = self._CylinderRadius2(self, "CylinderRadius2", service, rules, path)
                    self.CylinderY2 = self._CylinderY2(self, "CylinderY2", service, rules, path)

                class _CylinderZ2(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the second position of the cylinder.
                    """

                class _BoxYLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxYLength.
                    """

                class _CylinderX2(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the second position of the cylinder.
                    """

                class _CylinderX1(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the first position of the cylinder.
                    """

                class _BoxZLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxZLength.
                    """

                class _CylinderY1(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the first position of the cylinder.
                    """

                class _BoxXLength(PyArgumentsNumericalSubItem):
                    """
                    Argument BoxXLength.
                    """

                class _BoxCenterY(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _CylinderZ1(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the first position of the cylinder.
                    """

                class _CylinderRadius1(PyArgumentsNumericalSubItem):
                    """
                    Specify the radius of the cylinder at the initial position.
                    """

                class _BoxCenterX(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _BoxCenterZ(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate for the initial position of the cylindrical refinement region.
                    """

                class _CylinderRadius2(PyArgumentsNumericalSubItem):
                    """
                    Specify the radius of the cylinder at the second position.
                    """

                class _CylinderY2(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the second position of the cylinder.
                    """

        def create_instance(self) -> _CreateLocalRefinementRegionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateLocalRefinementRegionsArguments(*args)

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
        class _CreateMeshObjectsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MergeZonesBasedOnLabels = self._MergeZonesBasedOnLabels(self, "MergeZonesBasedOnLabels", service, rules, path)
                self.CreateAFaceZonePerBody = self._CreateAFaceZonePerBody(self, "CreateAFaceZonePerBody", service, rules, path)

            class _MergeZonesBasedOnLabels(PyArgumentsParameterSubItem):
                """
                Argument MergeZonesBasedOnLabels.
                """

            class _CreateAFaceZonePerBody(PyArgumentsParameterSubItem):
                """
                Argument CreateAFaceZonePerBody.
                """

        def create_instance(self) -> _CreateMeshObjectsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateMeshObjectsArguments(*args)

    class CreateOversetInterfaces(PyCommand):
        """
        Use this task to create a mesh interface between two or more overset mesh objects.  More...
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
        class _CreateOversetInterfacesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.OversetInterfacesName = self._OversetInterfacesName(self, "OversetInterfacesName", service, rules, path)
                self.ObjectSelectionList = self._ObjectSelectionList(self, "ObjectSelectionList", service, rules, path)

            class _OversetInterfacesName(PyArgumentsTextualSubItem):
                """
                Specify a name for the overset mesh interface or use the default value.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more overset mesh objects that will make up the mesh interface. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _CreateOversetInterfacesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateOversetInterfacesArguments(*args)

    class CreatePorousRegions(PyCommand):
        """
        Identify porous regions in your imported geometry so that you can simulate flow through porous media. More...
        Parameters
        ----------
        InputMethod : str
            Indicate whether you are creating the porous region using Direct coordinates, by using a Text file, or by specifying a Nonrectangular region.
        PorousRegionName : str
            Specify a name for the porous region or use the default value.
        WrapperSizeFactor : float
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
        class _CreatePorousRegionsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.InputMethod = self._InputMethod(self, "InputMethod", service, rules, path)
                self.PorousRegionName = self._PorousRegionName(self, "PorousRegionName", service, rules, path)
                self.WrapperSizeFactor = self._WrapperSizeFactor(self, "WrapperSizeFactor", service, rules, path)
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

            class _InputMethod(PyArgumentsTextualSubItem):
                """
                Indicate whether you are creating the porous region using Direct coordinates, by using a Text file, or by specifying a Nonrectangular region.
                """

            class _PorousRegionName(PyArgumentsTextualSubItem):
                """
                Specify a name for the porous region or use the default value.
                """

            class _WrapperSizeFactor(PyArgumentsNumericalSubItem):
                """
                Argument WrapperSizeFactor.
                """

            class _FileName(PyArgumentsTextualSubItem):
                """
                Specify the name and location of the text file containing the porous region definition.  More...
                """

            class _Location(PyArgumentsTextualSubItem):
                """
                Specify how you would like to determine the location of the porous region.
                """

            class _CellSizeP1P2(PyArgumentsNumericalSubItem):
                """
                Specify the size of the cells that lie between P1 and P2 of the porous region. P1 is the first point designated for the porous region; P2 is the second point of the porous region - created to the left of P1 in the same plane.
                """

            class _CellSizeP1P3(PyArgumentsNumericalSubItem):
                """
                Specify the size of the cells that lie between P1 and P3 of the porous region. P1 is the first point designated for the porous region; P3 is the third point of the porous region - created above P1 in the same plane.
                """

            class _CellSizeP1P4(PyArgumentsNumericalSubItem):
                """
                Specify the size of the cells that lie between P1 and P4 of the porous region. P1 is the first point designated for the porous region; P4 is the fourth point of the porous region - created in relation to P1 to essentially define a thickness for the porous region.
                """

            class _BufferSizeRatio(PyArgumentsNumericalSubItem):
                """
                Specify a value for the buffer size ratio. The buffer is created as an extra layer. The thickness is equivalent to the product of the buffer size ratio and the core thickness. The core thickness is the distance between P1 and P4.
                """

            class _P1(PyArgumentsNumericalSubItem):
                """
                Argument P1.
                """

            class _P2(PyArgumentsNumericalSubItem):
                """
                Argument P2.
                """

            class _P3(PyArgumentsNumericalSubItem):
                """
                Argument P3.
                """

            class _P4(PyArgumentsNumericalSubItem):
                """
                Argument P4.
                """

            class _NonRectangularParameters(PyArgumentsSingletonSubItem):
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

                class _NumberOfLayers(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of layers, or divisions, along the thickness of the porous region.
                    """

                class _LabelSelectionList(PyArgumentsTextualSubItem):
                    """
                    Select a single label that will correspond to the porous region. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _SelectionType(PyArgumentsTextualSubItem):
                    """
                    Choose how you want to make your selection (by object, zone, or label).
                    """

                class _ZoneSelectionList(PyArgumentsTextualSubItem):
                    """
                    Choose a single face zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _Thickness(PyArgumentsNumericalSubItem):
                    """
                    Specify the thickness (or the total height) of the porous region.
                    """

                class _MeshSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the cell size for the porous region mesh.
                    """

                class _FeatureAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the angle at which features will be extracted for the porous region.
                    """

                class _BufferSize(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the buffer size. The buffer is created as an extra layer. The thickness is equivalent to the product of the buffer size ratio and the core thickness. The core thickness is the distance between P1 and P4.
                    """

                class _FlipDirection(PyArgumentsParameterSubItem):
                    """
                    Reverses the orientation of the porous region.
                    """

                class _NonRectangularBufferSize(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the buffer size. The buffer is created as an extra layer. The thickness is equivalent to the product of the buffer size ratio and the core thickness. The core thickness is the distance between P1 and P4.
                    """

                class _ObjectSelectionList(PyArgumentsTextualSubItem):
                    """
                    Choose a single object (or void) from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

        def create_instance(self) -> _CreatePorousRegionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreatePorousRegionsArguments(*args)

    class CreateRegions(PyCommand):
        """
        Confirm that Fluent has correctly estimated the number of fluid regions. Fluent will detect additional regions if they exist, however, it will detect fluid regions only where they are connected to capping surfaces. Your geometry may include a solid region only, or it may contain a fluid region within a solid region.  More...
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
        class _CreateRegionsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.NumberOfFlowVolumes = self._NumberOfFlowVolumes(self, "NumberOfFlowVolumes", service, rules, path)
                self.RetainDeadRegionName = self._RetainDeadRegionName(self, "RetainDeadRegionName", service, rules, path)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)

            class _NumberOfFlowVolumes(PyArgumentsNumericalSubItem):
                """
                Confirm the number of flow volumes required for the analysis. The system will detect additional regions if they exist, however, it will detect fluid regions only where they are connected to capping surfaces.
                """

            class _RetainDeadRegionName(PyArgumentsTextualSubItem):
                """
                If any dead regions are present, you can choose to determine how such regions are named. Voids or dead regions are usually named dead0, dead1, dead2, and so on, and can remain so when this prompt is set to no. When this prompt is set to yes, however, the dead region names will also be prefixed with the original dead region name (usually derived from an adjacent region), such as dead0-fluid:1, dead1-fluid:2, and so on.
                """

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

        def create_instance(self) -> _CreateRegionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateRegionsArguments(*args)

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
        ReverseEdgeZoneOrientationforPersistent : list[int]
        EnableMultiThreading : bool
        NumberOfMultiThreads : int

        Returns
        -------
        bool
        """
        class _DefineGlobalSizingArguments(PyArguments):
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
                self.ReverseEdgeZoneOrientationforPersistent = self._ReverseEdgeZoneOrientationforPersistent(self, "ReverseEdgeZoneOrientationforPersistent", service, rules, path)
                self.EnableMultiThreading = self._EnableMultiThreading(self, "EnableMultiThreading", service, rules, path)
                self.NumberOfMultiThreads = self._NumberOfMultiThreads(self, "NumberOfMultiThreads", service, rules, path)

            class _MinSize(PyArgumentsNumericalSubItem):
                """
                Argument MinSize.
                """

            class _MaxSize(PyArgumentsNumericalSubItem):
                """
                Argument MaxSize.
                """

            class _GrowthRate(PyArgumentsNumericalSubItem):
                """
                Argument GrowthRate.
                """

            class _SizeFunctions(PyArgumentsTextualSubItem):
                """
                Argument SizeFunctions.
                """

            class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                """
                Argument CurvatureNormalAngle.
                """

            class _CellsPerGap(PyArgumentsNumericalSubItem):
                """
                Argument CellsPerGap.
                """

            class _ScopeProximityTo(PyArgumentsTextualSubItem):
                """
                Argument ScopeProximityTo.
                """

            class _Mesher(PyArgumentsTextualSubItem):
                """
                Argument Mesher.
                """

            class _PrimeSizeControlIds(PyArgumentsNumericalSubItem):
                """
                Argument PrimeSizeControlIds.
                """

            class _ReverseEdgeZoneOrientationforPersistent(PyArgumentsNumericalSubItem):
                """
                Argument ReverseEdgeZoneOrientationforPersistent.
                """

            class _EnableMultiThreading(PyArgumentsParameterSubItem):
                """
                Argument EnableMultiThreading.
                """

            class _NumberOfMultiThreads(PyArgumentsNumericalSubItem):
                """
                Argument NumberOfMultiThreads.
                """

        def create_instance(self) -> _DefineGlobalSizingArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DefineGlobalSizingArguments(*args)

    class DefineLeakageThreshold(PyCommand):
        """
        Define leakage threshold size to fix any potential leakages that may occur due to any missing, misaligned parts, or small imperfections from the imported geometry. These holes may be larger than any of your initial local size controls, resulting in leaks that need to be closed. Use the Preview Leakages button and associated controls repeatedly to identify holes that need to be closed. Leakages can be closed to a void region or inside an object. More...
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
        class _DefineLeakageThresholdArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Indicate whether or not you need to define a leakage threshold for one or more regions.
                """

            class _LeakageName(PyArgumentsTextualSubItem):
                """
                Specify a name for the leakage threshold or use the default value.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object or by a previously identified region).
                """

            class _DeadRegionsList(PyArgumentsTextualSubItem):
                """
                Choose one or more regions from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _RegionSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single region from the list of identified regions below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _DeadRegionsSize(PyArgumentsNumericalSubItem):
                """
                The leakage threshold size is based on multiples of two. For example, if leaks are detected at 8 but not at 16 (for example, 2\\*8), then the threshold size is 16, and any leakage smaller than 16 will be closed.
                """

            class _PlaneClippingValue(PyArgumentsNumericalSubItem):
                """
                Use the slider to move the clipping plane along the axis of the selected X, Y, or Z direction.
                """

            class _PlaneDirection(PyArgumentsTextualSubItem):
                """
                Indicates the direction in which the clipping plane faces.
                """

            class _FlipDirection(PyArgumentsParameterSubItem):
                """
                Change the orientation of the clipping plane, exposing the mesh on the opposite side.
                """

        def create_instance(self) -> _DefineLeakageThresholdArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DefineLeakageThresholdArguments(*args)

    class DescribeGeometryAndFlow(PyCommand):
        """
        Specify the type of geometry you have and the type of flow you are trying to simulate. You can determine whether the flow is an external flow around an object, or whether it is an internal flow inside an object. For external flows, you can choose to add an enclosure. For internal flows, you can choose to cover large openings to extract the flow region, or rely on automatically detecting and closing any leaks to the outer domain. In either case, you are also able to add refinement regions in and around your geometry. More...
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
        class _DescribeGeometryAndFlowArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FlowType = self._FlowType(self, "FlowType", service, rules, path)
                self.GeometryOptions = self._GeometryOptions(self, "GeometryOptions", service, rules, path)
                self.AddEnclosure = self._AddEnclosure(self, "AddEnclosure", service, rules, path)
                self.CloseCaps = self._CloseCaps(self, "CloseCaps", service, rules, path)
                self.LocalRefinementRegions = self._LocalRefinementRegions(self, "LocalRefinementRegions", service, rules, path)
                self.DescribeGeometryAndFlowOptions = self._DescribeGeometryAndFlowOptions(self, "DescribeGeometryAndFlowOptions", service, rules, path)
                self.AllTaskList = self._AllTaskList(self, "AllTaskList", service, rules, path)

            class _FlowType(PyArgumentsTextualSubItem):
                """
                Specify the type of flow you want to simulate: external flow, internal flow, or both. The appropriate Standard Options (for example adding an enclosure, adding caps, etc.) will be selected for you, depending on your choice.
                """

            class _GeometryOptions(PyArgumentsParameterSubItem):
                """
                Display standard geometry-based options that you may want to apply to the workflow.
                """

            class _AddEnclosure(PyArgumentsTextualSubItem):
                """
                Specify whether you are going to need to add an external flow boundary around your imported geometry. If so, this will add a Create External Flow Boundaries task to the workflow.
                """

            class _CloseCaps(PyArgumentsTextualSubItem):
                """
                Specify whether or not you will need to cover, or cap, and large holes in order to create an internal fluid flow region. If so, this will add an Enclose Fluid Regions (Capping) task to the workflow.
                """

            class _LocalRefinementRegions(PyArgumentsTextualSubItem):
                """
                Specify whether or not you will need to add local refinement in and around the imported geometry. If so, this will add a Create Local Refinement Regions task to the workflow.
                """

            class _DescribeGeometryAndFlowOptions(PyArgumentsSingletonSubItem):
                """
                Argument DescribeGeometryAndFlowOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.PorousRegions = self._PorousRegions(self, "PorousRegions", service, rules, path)
                    self.CloseLeakages = self._CloseLeakages(self, "CloseLeakages", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.CloseLeakges = self._CloseLeakges(self, "CloseLeakges", service, rules, path)
                    self.ZeroThickness = self._ZeroThickness(self, "ZeroThickness", service, rules, path)
                    self.ExtractEdgeFeatures = self._ExtractEdgeFeatures(self, "ExtractEdgeFeatures", service, rules, path)
                    self.MovingObjects = self._MovingObjects(self, "MovingObjects", service, rules, path)
                    self.EnablePrimeWrapper = self._EnablePrimeWrapper(self, "EnablePrimeWrapper", service, rules, path)
                    self.EnableOverset = self._EnableOverset(self, "EnableOverset", service, rules, path)
                    self.IdentifyRegions = self._IdentifyRegions(self, "IdentifyRegions", service, rules, path)

                class _PorousRegions(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you will have any porous regions in your geometry. If so, then a Create Porous Regions task will be added to the workflow. A simple primitive rectangle will be placed over complex and detailed geometry of a porous region (for example, fins and tubes of a heat exchanger).  With buffer layer:
                    """

                class _CloseLeakages(PyArgumentsTextualSubItem):
                    """
                    Argument CloseLeakages.
                    """

                class _AdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the workflow.
                    """

                class _CloseLeakges(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not your geometry contains any problems (such as gaps or overlapping/intersecting surfaces) that may create leakages that need to be closed. If so, then a Define Leakage Threshold task is added to the workflow.
                    """

                class _ZeroThickness(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you will need to account for any portions of your geometry with zero-thickness, and apply thickness to them for a more refined surface mesh. If so, then an Add Thickness task will be added to the workflow.
                    """

                class _ExtractEdgeFeatures(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you will need to extract additional edge features from your imported geometry. These edge features will be captured. If so, then an Extract Edge Features task will be added to the workflow.
                    """

                class _MovingObjects(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you will need to create or identify any specialized construction surfaces within your geometry or flow that need to be identified (such as capping surfaces or cylindrical surfaces to be used for moving reference frames, etc.). If so, then an Identify Construction Surfaces task will be added to the workflow. More...
                    """

                class _EnablePrimeWrapper(PyArgumentsTextualSubItem):
                    """
                    Argument EnablePrimeWrapper.
                    """

                class _EnableOverset(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you will need to create any overlapping or overset meshes. Such types of meshes can provide better mesh resolution in and around complicated, intersected portions of your geometry.
                    """

                class _IdentifyRegions(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you need to specifically identify and analyze particular regions. If so, then an Identify Regions task is added to the workflow.
                    """

            class _AllTaskList(PyArgumentsTextualSubItem):
                """
                Argument AllTaskList.
                """

        def create_instance(self) -> _DescribeGeometryAndFlowArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DescribeGeometryAndFlowArguments(*args)

    class DescribeOversetFeatures(PyCommand):
        """
        Use this task to determine if specific overset features are required for your workflow. Depending on your simulation requirements, you may or may not need to add an overset collar mesh and/or an overset component mesh to your overall workflow tasks.
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
        class _DescribeOversetFeaturesArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.ComponentGrid = self._ComponentGrid(self, "ComponentGrid", service, rules, path)
                self.CollarGrid = self._CollarGrid(self, "CollarGrid", service, rules, path)
                self.BackgroundMesh = self._BackgroundMesh(self, "BackgroundMesh", service, rules, path)
                self.OversetInterfaces = self._OversetInterfaces(self, "OversetInterfaces", service, rules, path)

            class _AdvancedOptions(PyArgumentsParameterSubItem):
                """
                Argument AdvancedOptions.
                """

            class _ComponentGrid(PyArgumentsTextualSubItem):
                """
                Indicate whether you need to add an overset component mesh task to the workflow.
                """

            class _CollarGrid(PyArgumentsTextualSubItem):
                """
                Indicate whether you need to add an overset collar mesh task to the workflow
                """

            class _BackgroundMesh(PyArgumentsTextualSubItem):
                """
                Argument BackgroundMesh.
                """

            class _OversetInterfaces(PyArgumentsTextualSubItem):
                """
                Argument OversetInterfaces.
                """

        def create_instance(self) -> _DescribeOversetFeaturesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._DescribeOversetFeaturesArguments(*args)

    class ExtractEdges(PyCommand):
        """
        Fidelity of the geometry can be improved by extracting feature edges. There are three types of feature edges that can be extracted: edges based on an angle; edges based on a sharp-angle; and edges based on intersections. More...
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
            Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteGeomObjectSelectionList : list[str]
            Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        NonExtractedObjects : list[str]

        Returns
        -------
        bool
        """
        class _ExtractEdgesArguments(PyArguments):
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

            class _ExtractEdgesName(PyArgumentsTextualSubItem):
                """
                Specify a name for the edge feature extraction or use the default value.
                """

            class _ExtractMethodType(PyArgumentsTextualSubItem):
                """
                Choose how the edge features are to be extracted: either by feature angle, intersection loops, or by sharp angle.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GeomObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more zones from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _FeatureAngleLocal(PyArgumentsNumericalSubItem):
                """
                Specify the minimum angle between the feature edges that should be preserved.
                """

            class _IndividualCollective(PyArgumentsTextualSubItem):
                """
                Choose face zone interactivity -  individual: considers intersection of face zones within the object(s) selected; collectively: consider intersection of faces only across selected objects.
                """

            class _SharpAngle(PyArgumentsNumericalSubItem):
                """
                Use the slider to specify the sharp angle (in degrees) that will be used in the feature extraction.
                """

            class _CompleteObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteGeomObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more geometry objects from the list below to apply the edge feature extraction to. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _NonExtractedObjects(PyArgumentsTextualSubItem):
                """
                Argument NonExtractedObjects.
                """

        def create_instance(self) -> _ExtractEdgesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ExtractEdgesArguments(*args)

    class ExtrudeVolumeMesh(PyCommand):
        """
        Use this task to extend all or parts of your volume mesh beyond the original domain. 
                       
                        More...
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
        ReverseDirection : bool
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
        class _ExtrudeVolumeMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MExControlName = self._MExControlName(self, "MExControlName", service, rules, path)
                self.Method = self._Method(self, "Method", service, rules, path)
                self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                self.ExtendToPeriodicPair = self._ExtendToPeriodicPair(self, "ExtendToPeriodicPair", service, rules, path)
                self.ExtrudeNormalBased = self._ExtrudeNormalBased(self, "ExtrudeNormalBased", service, rules, path)
                self.ExternalBoundaryZoneList = self._ExternalBoundaryZoneList(self, "ExternalBoundaryZoneList", service, rules, path)
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.ReverseDirection = self._ReverseDirection(self, "ReverseDirection", service, rules, path)
                self.TotalHeight = self._TotalHeight(self, "TotalHeight", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.NumberofLayers = self._NumberofLayers(self, "NumberofLayers", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.VMExtrudePreferences = self._VMExtrudePreferences(self, "VMExtrudePreferences", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _MExControlName(PyArgumentsTextualSubItem):
                """
                Specify a name for the extrusion or use the default value.
                """

            class _Method(PyArgumentsTextualSubItem):
                """
                Choose whether you want the extrusion to be based on a specified Total Height value, or one based on a specified First Height value. The relationship between the two is illustrated by:
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _ExtendToPeriodicPair(PyArgumentsParameterSubItem):
                """
                Argument ExtendToPeriodicPair.
                """

            class _ExtrudeNormalBased(PyArgumentsParameterSubItem):
                """
                Specify whether the volume extrusion is derived from normal-based faceting or direction-based faceting. When enabled (the default), the volume extrusion is derived on normal-based faceting, such that for each layer, the normal is calculated and smoothing occurs, and is suitable for non-planar surfaces. For planar surfaces, disable this option to use a direction-based approach where the direction is chosen based on the average normal of the entire surface, and is used to extrude all layers.
                """

            class _ExternalBoundaryZoneList(PyArgumentsTextualSubItem):
                """
                Select one or more boundaries. All selected boundaries must share the same plane. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _ReverseDirection(PyArgumentsParameterSubItem):
                """
                Argument ReverseDirection.
                """

            class _TotalHeight(PyArgumentsNumericalSubItem):
                """
                Specify a value for the total height of the extrusion or use the default value.
                """

            class _FirstHeight(PyArgumentsNumericalSubItem):
                """
                Specify a value for the height of the first layer of the extrusion or use the default value.
                """

            class _NumberofLayers(PyArgumentsNumericalSubItem):
                """
                Specify the number of extrusion layers.
                """

            class _GrowthRate(PyArgumentsNumericalSubItem):
                """
                Specify how the extrusion layers will grow. For example, a value of 1.2 indicates that each successive layer will grow by 20 percent of the previous layer. 
                                More...
                """

            class _VMExtrudePreferences(PyArgumentsSingletonSubItem):
                """
                Argument VMExtrudePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxLayerHeight = self._MaxLayerHeight(self, "MaxLayerHeight", service, rules, path)
                    self.MidSpanLength = self._MidSpanLength(self, "MidSpanLength", service, rules, path)
                    self.BiasMethod = self._BiasMethod(self, "BiasMethod", service, rules, path)
                    self.BiasMethodControl = self._BiasMethodControl(self, "BiasMethodControl", service, rules, path)
                    self.MergeCellZones = self._MergeCellZones(self, "MergeCellZones", service, rules, path)
                    self.ShowVMExtrudePreferences = self._ShowVMExtrudePreferences(self, "ShowVMExtrudePreferences", service, rules, path)

                class _MaxLayerHeight(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxLayerHeight.
                    """

                class _MidSpanLength(PyArgumentsNumericalSubItem):
                    """
                    Argument MidSpanLength.
                    """

                class _BiasMethod(PyArgumentsTextualSubItem):
                    """
                    Select from a choice of patterns that you want to apply to your volume mesh extrusion.
                    """

                class _BiasMethodControl(PyArgumentsTextualSubItem):
                    """
                    Argument BiasMethodControl.
                    """

                class _MergeCellZones(PyArgumentsParameterSubItem):
                    """
                    Indicate whether or not you want to merge the extruded layers with any adjacent regions.
                    """

                class _ShowVMExtrudePreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _ExtrudeVolumeMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ExtrudeVolumeMeshArguments(*args)

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
        class _GenerateInitialSurfaceMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GenerateQuads = self._GenerateQuads(self, "GenerateQuads", service, rules, path)
                self.ProjectOnGeometry = self._ProjectOnGeometry(self, "ProjectOnGeometry", service, rules, path)
                self.EnableMultiThreading = self._EnableMultiThreading(self, "EnableMultiThreading", service, rules, path)
                self.NumberOfMultiThreads = self._NumberOfMultiThreads(self, "NumberOfMultiThreads", service, rules, path)
                self.Prism2DPreferences = self._Prism2DPreferences(self, "Prism2DPreferences", service, rules, path)
                self.Surface2DPreferences = self._Surface2DPreferences(self, "Surface2DPreferences", service, rules, path)

            class _GenerateQuads(PyArgumentsParameterSubItem):
                """
                Argument GenerateQuads.
                """

            class _ProjectOnGeometry(PyArgumentsParameterSubItem):
                """
                Argument ProjectOnGeometry.
                """

            class _EnableMultiThreading(PyArgumentsParameterSubItem):
                """
                Argument EnableMultiThreading.
                """

            class _NumberOfMultiThreads(PyArgumentsNumericalSubItem):
                """
                Argument NumberOfMultiThreads.
                """

            class _Prism2DPreferences(PyArgumentsSingletonSubItem):
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

                class _SplitQuads(PyArgumentsTextualSubItem):
                    """
                    Argument SplitQuads.
                    """

                class _MaxAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxAspectRatio.
                    """

                class _MinAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Argument MinAspectRatio.
                    """

                class _RemeshGrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Argument RemeshGrowthRate.
                    """

                class _LocalRemesh(PyArgumentsTextualSubItem):
                    """
                    Argument LocalRemesh.
                    """

                class _MaxFaceSkew(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxFaceSkew.
                    """

                class _ShowPrism2DPreferences(PyArgumentsParameterSubItem):
                    """
                    Argument ShowPrism2DPreferences.
                    """

                class _GapFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument GapFactor.
                    """

                class _RefineStretchedQuads(PyArgumentsTextualSubItem):
                    """
                    Argument RefineStretchedQuads.
                    """

                class _nOrthogonalLayers(PyArgumentsNumericalSubItem):
                    """
                    Argument nOrthogonalLayers.
                    """

            class _Surface2DPreferences(PyArgumentsSingletonSubItem):
                """
                Argument Surface2DPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MergeFaceZonesBasedOnLabels = self._MergeFaceZonesBasedOnLabels(self, "MergeFaceZonesBasedOnLabels", service, rules, path)
                    self.MergeEdgeZonesBasedOnLabels = self._MergeEdgeZonesBasedOnLabels(self, "MergeEdgeZonesBasedOnLabels", service, rules, path)
                    self.ShowAdvancedOptions = self._ShowAdvancedOptions(self, "ShowAdvancedOptions", service, rules, path)

                class _MergeFaceZonesBasedOnLabels(PyArgumentsTextualSubItem):
                    """
                    Argument MergeFaceZonesBasedOnLabels.
                    """

                class _MergeEdgeZonesBasedOnLabels(PyArgumentsTextualSubItem):
                    """
                    Argument MergeEdgeZonesBasedOnLabels.
                    """

                class _ShowAdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Argument ShowAdvancedOptions.
                    """

        def create_instance(self) -> _GenerateInitialSurfaceMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateInitialSurfaceMeshArguments(*args)

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
        class _GenerateMapMeshArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Argument AddChild.
                """

            class _ControlName(PyArgumentsTextualSubItem):
                """
                Argument ControlName.
                """

            class _SizingOption(PyArgumentsTextualSubItem):
                """
                Argument SizingOption.
                """

            class _ConstantSize(PyArgumentsNumericalSubItem):
                """
                Argument ConstantSize.
                """

            class _GrowthRate(PyArgumentsNumericalSubItem):
                """
                Argument GrowthRate.
                """

            class _ShortSideDivisions(PyArgumentsNumericalSubItem):
                """
                Argument ShortSideDivisions.
                """

            class _SplitQuads(PyArgumentsParameterSubItem):
                """
                Argument SplitQuads.
                """

            class _ProjectOnGeometry(PyArgumentsParameterSubItem):
                """
                Argument ProjectOnGeometry.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _FaceLabelList(PyArgumentsTextualSubItem):
                """
                Argument FaceLabelList.
                """

            class _FaceZoneList(PyArgumentsTextualSubItem):
                """
                Argument FaceZoneList.
                """

        def create_instance(self) -> _GenerateMapMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateMapMeshArguments(*args)

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
        class _GeneratePrismsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.GeneratePrismsOption = self._GeneratePrismsOption(self, "GeneratePrismsOption", service, rules, path)

            class _GeneratePrismsOption(PyArgumentsParameterSubItem):
                """
                Argument GeneratePrismsOption.
                """

        def create_instance(self) -> _GeneratePrismsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GeneratePrismsArguments(*args)

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
        class _GenerateShellBoundaryLayerMeshArguments(PyArguments):
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

            class _GapFactor(PyArgumentsNumericalSubItem):
                """
                Argument GapFactor.
                """

            class _MaxAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument MaxAspectRatio.
                """

            class _MinAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument MinAspectRatio.
                """

            class _LocalRemesh(PyArgumentsTextualSubItem):
                """
                Argument LocalRemesh.
                """

            class _RemeshGrowthRate(PyArgumentsNumericalSubItem):
                """
                Argument RemeshGrowthRate.
                """

            class _RefineStretchedQuads(PyArgumentsTextualSubItem):
                """
                Argument RefineStretchedQuads.
                """

            class _SplitQuads(PyArgumentsTextualSubItem):
                """
                Argument SplitQuads.
                """

            class _nOrthogonalLayers(PyArgumentsNumericalSubItem):
                """
                Argument nOrthogonalLayers.
                """

            class _MaxFaceSkew(PyArgumentsNumericalSubItem):
                """
                Argument MaxFaceSkew.
                """

        def create_instance(self) -> _GenerateShellBoundaryLayerMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateShellBoundaryLayerMeshArguments(*args)

    class GenerateTheMultiZoneMesh(PyCommand):
        """
        Use this task to create a multi-zone mesh for the designated region(s).  More...
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
            Select the named region(s) from the list to which you would like to generate the multi-zone mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...

        Returns
        -------
        bool
        """
        class _GenerateTheMultiZoneMeshArguments(PyArguments):
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

            class _OrthogonalQualityLimit(PyArgumentsNumericalSubItem):
                """
                This value sets the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit, and is recommended to be around 0.04.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Argument SelectionType.
                """

            class _RegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to generate the multi-zone mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _NonConformal(PyArgumentsTextualSubItem):
                """
                Optionally specify that multizone regions are non-conformally connected to other volumetric regions.  If you want to have a conformal mesh but, because of meshing constraints, that is not possible, then you can switch to non-conformal here and avoid doing so in the CAD model.
                """

            class _SizeFunctionScaleFactor(PyArgumentsNumericalSubItem):
                """
                Enable the scaling of the multizone mesh. In some cases when the multizone region is too coarse when compared to the adjacent surface mesh, a connection is not possible. You can specify a size function scaling factor here to improve the sizing match between the multizone and the non-multizone regions and avoid any free faces. Typically, a value between 0.7 and 0.8 is recommended.
                """

            class _MeshingStrategy(PyArgumentsTextualSubItem):
                """
                Argument MeshingStrategy.
                """

            class _ReMergeZones(PyArgumentsTextualSubItem):
                """
                Argument ReMergeZones.
                """

            class _MergeBodyLabels(PyArgumentsTextualSubItem):
                """
                Argument MergeBodyLabels.
                """

            class _CFDSurfaceMeshControls(PyArgumentsSingletonSubItem):
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
                    self.SurfaceMeshMethod = self._SurfaceMeshMethod(self, "SurfaceMeshMethod", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _PreviewSizefield(PyArgumentsParameterSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _SaveSizeField(PyArgumentsParameterSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyArgumentsTextualSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyArgumentsParameterSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SurfaceMeshMethod(PyArgumentsTextualSubItem):
                    """
                    Argument SurfaceMeshMethod.
                    """

                class _SizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyArgumentsParameterSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyArgumentsTextualSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyArgumentsTextualSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _BodyLabelList(PyArgumentsTextualSubItem):
                """
                Argument BodyLabelList.
                """

            class _CellZoneList(PyArgumentsTextualSubItem):
                """
                Argument CellZoneList.
                """

            class _CompleteRegionScope(PyArgumentsTextualSubItem):
                """
                Select the named region(s) from the list to which you would like to generate the multi-zone mesh. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _GenerateTheMultiZoneMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheMultiZoneMeshArguments(*args)

    class GenerateTheSurfaceMeshFTM(PyCommand):
        """
        This task will close all the leakages to objects and void regions and then generate only the surface mesh. More...
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
        LeakShield : str
        AutoRegionBetweenPorous : str
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
        class _GenerateTheSurfaceMeshFTMArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.SurfaceQuality = self._SurfaceQuality(self, "SurfaceQuality", service, rules, path)
                self.SaveSurfaceMesh = self._SaveSurfaceMesh(self, "SaveSurfaceMesh", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.SaveIntermediateFiles = self._SaveIntermediateFiles(self, "SaveIntermediateFiles", service, rules, path)
                self.IntermediateFileName = self._IntermediateFileName(self, "IntermediateFileName", service, rules, path)
                self.SeparateSurface = self._SeparateSurface(self, "SeparateSurface", service, rules, path)
                self.UseSizeFieldForPrimeWrap = self._UseSizeFieldForPrimeWrap(self, "UseSizeFieldForPrimeWrap", service, rules, path)
                self.LeakShield = self._LeakShield(self, "LeakShield", service, rules, path)
                self.AutoRegionBetweenPorous = self._AutoRegionBetweenPorous(self, "AutoRegionBetweenPorous", service, rules, path)
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

            class _SurfaceQuality(PyArgumentsNumericalSubItem):
                """
                This is the target maximum surface mesh quality. The recommended value is between 0.7 and 0.85.
                """

            class _SaveSurfaceMesh(PyArgumentsParameterSubItem):
                """
                Select this option to save the surface mesh. Use advanced options to determine whether to save intermediate files or not, and to choose a specific directory to save the mesh.
                """

            class _AdvancedOptions(PyArgumentsParameterSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _SaveIntermediateFiles(PyArgumentsTextualSubItem):
                """
                Determine whether or not you want to save any intermediate files that are generated during volume meshing. Disabling this option may increase speed and efficiency.
                """

            class _IntermediateFileName(PyArgumentsTextualSubItem):
                """
                By default, files are saved in a temporary folder and later deleted once the session is ended. You can also save files in a specified folder. The prefix for the name of the files are taken from the FMD or STL file name.
                """

            class _SeparateSurface(PyArgumentsTextualSubItem):
                """
                Select Yes if you want to have the final surface mesh to be viewed as separated zones.
                """

            class _UseSizeFieldForPrimeWrap(PyArgumentsTextualSubItem):
                """
                Argument UseSizeFieldForPrimeWrap.
                """

            class _LeakShield(PyArgumentsTextualSubItem):
                """
                Argument LeakShield.
                """

            class _AutoRegionBetweenPorous(PyArgumentsTextualSubItem):
                """
                Argument AutoRegionBetweenPorous.
                """

            class _AutoPairing(PyArgumentsTextualSubItem):
                """
                Specify whether or not you want to separate contact pairs between fluids and solids.
                """

            class _MergeWrapperAtSolidConacts(PyArgumentsTextualSubItem):
                """
                Specify whether or not you want to allow contacts between solid and fluid regions to be merged into the surface mesh wrapper. When enabled, all bounding faces of a fluid region wrap that come into contact with solid regions will be merged into a single zone (using the prefix _contact). Each respective wrapped fluid region will have one _contact zone associated with it.
                """

            class _ParallelSerialOption(PyArgumentsTextualSubItem):
                """
                Specify whether or not you want to perform solid meshing using parallel sessions. Select Yes and indicate the Maximum Number of Sessions. The number of parallel sessions that are used will depend upon the number of solid objects that need to be meshed.
                """

            class _NumberOfSessions(PyArgumentsNumericalSubItem):
                """
                Indicate the number of parallel sessions that are to be used, depending upon the number of solid objects that need to be meshed.
                """

            class _MaxIslandFace(PyArgumentsNumericalSubItem):
                """
                Specify the maximum face count required for isolated areas (islands) to be created during surface mesh generation. Any islands that have a face count smaller than this value will be removed, and only larger islands will remain.
                """

            class _SpikeRemovalAngle(PyArgumentsNumericalSubItem):
                """
                Specify a value for the minimum spike angle for the specified region. A spike angle of 250 degrees is recommended or use the default value. You should not exceed 260 degrees.
                """

            class _DihedralMinAngle(PyArgumentsNumericalSubItem):
                """
                Specify a value for the minimum dihedral angle for the specified region. A dihedral angle of 30 degrees are recommended or use the default value. You should not exceed 30 degrees.
                """

            class _ProjectOnGeometry(PyArgumentsTextualSubItem):
                """
                Determine whether, after surface meshing, Fluent will project the mesh nodes back onto to the original CAD model.
                """

            class _AutoAssignZoneTypes(PyArgumentsTextualSubItem):
                """
                Choose whether or not to automatically assign boundary types to zones.
                """

            class _AdvancedInnerWrap(PyArgumentsTextualSubItem):
                """
                Choose whether or not to extend or expand the surface mesh into any interior pockets or cavities.
                """

            class _GapCoverZoneRecovery(PyArgumentsTextualSubItem):
                """
                Determine whether or not to keep or remove the zones representing the cap covers. When set to Yes, the zones representing the gap covers are retained, whereas when set to No (the default), the zones for the gap covers are removed.
                """

            class _GlobalMin(PyArgumentsNumericalSubItem):
                """
                Specify a global minimum value for the surface mesh. The default minimum value is calculated based on available target and wrap size controls and bodies of influence. 
                                More...
                """

            class _ShowSubTasks(PyArgumentsTextualSubItem):
                """
                Argument ShowSubTasks.
                """

        def create_instance(self) -> _GenerateTheSurfaceMeshFTMArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheSurfaceMeshFTMArguments(*args)

    class GenerateTheSurfaceMeshWTM(PyCommand):
        """
        Generate a mesh over the surface of the imported CAD geometry, or remesh an imported surface mesh, or use pre-existing size field or size control files. Surface meshes are used to define the computational region or volume for the CFD analysis. Specify and adjust various properties of the computational surface mesh and preview them in the graphics window until you are satisfied that the surface mesh completely and accurately captures the topology of the imported CAD geometry. No gaps or slivers should be present, and you should refine the surface mesh in key areas to ensure that you can capture important physical behavior in your CFD analysis. Choose any advanced options that you want to take effect upon updating the task.  More...
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
            For imported CAD assemblies with multiple parts, use this task to identify and close any problematic gaps and choose whether to join and/or intersect the problematic faces.   More...
        CADFacetingControls : dict[str, Any]
        CadImportOptions : dict[str, Any]
        ShareTopologyPreferences : dict[str, Any]
        PreviewSizeToggle : bool
            For an imported surface mesh, use this field to visualize those boundaries that already have assigned local sizing controls (and any selected boundaries if applicable).

        Returns
        -------
        bool
        """
        class _GenerateTheSurfaceMeshWTMArguments(PyArguments):
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

            class _CFDSurfaceMeshControls(PyArgumentsSingletonSubItem):
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
                    self.SurfaceMeshMethod = self._SurfaceMeshMethod(self, "SurfaceMeshMethod", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Specify a size field file that contains the size function definitions based on specified parameters.
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum size of the elements for the surface mesh.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Set proximity based refinement. Edges considers edge-to-edge proximity, while Faces considers face-to-face proximity, and Faces and Edges considers both.  More...
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.  More...
                    """

                class _PreviewSizefield(PyArgumentsParameterSubItem):
                    """
                    Enable this option to visualize the size field in the graphics window.
                    """

                class _SaveSizeField(PyArgumentsParameterSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you want to use your own size field file and/or your own size control file when generating the surface mesh.
                    """

                class _AutoCreateScopedSizing(PyArgumentsParameterSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum size of the elements for the surface mesh. A minimum size between approximately 0.1 - 10 is recommended.
                    """

                class _SizeFunctions(PyArgumentsTextualSubItem):
                    """
                    Choose the type of size function that you want to apply to the surface mesh: based on curvature, proximity, or both.
                    """

                class _SurfaceMeshMethod(PyArgumentsTextualSubItem):
                    """
                    Argument SurfaceMeshMethod.
                    """

                class _SizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Specify a size field file that contains the size function definitions based on specified parameters.
                    """

                class _DrawSizeControl(PyArgumentsParameterSubItem):
                    """
                    Enable this field to display the size boxes in the graphics window.
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                    """

                class _SizeControlFile(PyArgumentsTextualSubItem):
                    """
                    Specify a size controls file (\\*.szcontrol) that contains the scoped sizing control definitions. The control name and type, and the scope of the control will be included in the size control file along with global size parameters.
                    """

                class _RemeshImportedMesh(PyArgumentsTextualSubItem):
                    """
                    For an imported surface mesh, determine which surfaces you wish to remesh in this task. Choices depend upon if any local sizing has been added or not.  More...
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the increase in element edge length with each succeeding layer of elements.
                    """

                class _ObjectBasedControls(PyArgumentsTextualSubItem):
                    """
                    Choose if you would like to ignore any small artificial gaps that may exist between two objects/bodies; especially applicable to assemblies that typically have duplicate faces and edges in between each body.
                    """

            class _SeparationRequired(PyArgumentsTextualSubItem):
                """
                Choose whether or not to separate face zones. By default, this is set to No. If you choose to separate zones, specify a Separation Angle. You should separate zones when using Multizone meshing. Separation is needed in case named selections for inlets, outlets, capping, local boundary layers, etc. have not been defined within the CAD model in advance. You should only select Yes if you need to separate faces for capping, boundary conditions, or inflation on specific faces.
                """

            class _SeparationAngle(PyArgumentsNumericalSubItem):
                """
                Specify a desired angle for determining separation. Assigning a smaller separation angle will produce more zones.
                """

            class _RemeshSelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to select your surface(s) to remesh (by label or by zone).
                """

            class _RemeshZoneList(PyArgumentsTextualSubItem):
                """
                Argument RemeshZoneList.
                """

            class _RemeshLabelList(PyArgumentsTextualSubItem):
                """
                Argument RemeshLabelList.
                """

            class _SurfaceMeshPreferences(PyArgumentsSingletonSubItem):
                """
                Argument SurfaceMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SMQualityCollapseLimit = self._SMQualityCollapseLimit(self, "SMQualityCollapseLimit", service, rules, path)
                    self.FoldFaceLimit = self._FoldFaceLimit(self, "FoldFaceLimit", service, rules, path)
                    self.SMSeparation = self._SMSeparation(self, "SMSeparation", service, rules, path)
                    self.ShowSurfaceMeshPreferences = self._ShowSurfaceMeshPreferences(self, "ShowSurfaceMeshPreferences", service, rules, path)
                    self.AutoMerge = self._AutoMerge(self, "AutoMerge", service, rules, path)
                    self.SMSeparationAngle = self._SMSeparationAngle(self, "SMSeparationAngle", service, rules, path)
                    self.TVMAutoControlCreation = self._TVMAutoControlCreation(self, "TVMAutoControlCreation", service, rules, path)
                    self.SMQualityImprove = self._SMQualityImprove(self, "SMQualityImprove", service, rules, path)
                    self.SMRemoveStep = self._SMRemoveStep(self, "SMRemoveStep", service, rules, path)
                    self.SMStepWidth = self._SMStepWidth(self, "SMStepWidth", service, rules, path)
                    self.SMQualityMaxAngle = self._SMQualityMaxAngle(self, "SMQualityMaxAngle", service, rules, path)
                    self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                    self.VolumeMeshMaxSize = self._VolumeMeshMaxSize(self, "VolumeMeshMaxSize", service, rules, path)
                    self.SelfIntersectCheck = self._SelfIntersectCheck(self, "SelfIntersectCheck", service, rules, path)
                    self.AutoSurfaceRemesh = self._AutoSurfaceRemesh(self, "AutoSurfaceRemesh", service, rules, path)
                    self.SMQualityImproveLimit = self._SMQualityImproveLimit(self, "SMQualityImproveLimit", service, rules, path)
                    self.SetVolumeMeshMaxSize = self._SetVolumeMeshMaxSize(self, "SetVolumeMeshMaxSize", service, rules, path)

                class _SMQualityCollapseLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify the limiting skewness value for cell collapse to improve the mesh. If any remaining triangles are above this limit, these triangles will be aggressively removed using a fixed maximum angle of 120 degrees.
                    """

                class _FoldFaceLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify the value limiting when folded faces are smoothed or resolved. Folded faces are resolved while under this limit. Set this value to 0 if the number of free nodes (due to a zero-thickness wall such as a baffle for instance) falls below 10.
                    """

                class _SMSeparation(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to separate zones. This is required to select faces for capping. If Named Selections have already been defined at these locations, then separation is not needed. Performance may be improved if this is disabled.
                    """

                class _ShowSurfaceMeshPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _AutoMerge(PyArgumentsParameterSubItem):
                    """
                    Argument AutoMerge.
                    """

                class _SMSeparationAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify a desired angle for determining separation. Assigning a smaller separation angle will produce more zones.
                    """

                class _TVMAutoControlCreation(PyArgumentsTextualSubItem):
                    """
                    If your geometry contains small edges, you can choose to extract these edge features when generating the surface mesh by selecting yes. Note that selecting yes , will always extract small edge features regardless of your selection for the Auto Remesh to Remove Clustering? option.
                    """

                class _SMQualityImprove(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to apply quality measures during surface mesh generation. You should disable this option when using Multizone meshing of very thin structures, relative to the minimum size.
                    """

                class _SMRemoveStep(PyArgumentsTextualSubItem):
                    """
                    Indicate if there are any small imperfections (ledge or step artifacts from the original CAD geometry) that can be removed as part of this task. If you select yes, then you must specify a Max Step Width.
                    """

                class _SMStepWidth(PyArgumentsNumericalSubItem):
                    """
                    Specify the width of the step that you wish to remove.
                    """

                class _SMQualityMaxAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum angle between the normals of adjacent faces. This quality measure is useful in locating sharp corners in complicated geometries. The angle value ranges from 0 to 180 degrees. Four consecutive attempts are made to improve the quality, each using a larger adjacent angle, until this maximum value.
                    """

                class _AutoAssignZoneTypes(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to automatically assign boundary types to zones.
                    """

                class _VolumeMeshMaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum size of the elements for the surface mesh.
                    """

                class _SelfIntersectCheck(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to check for self-intersecting faces. Performance may be improved if this is disabled.
                    """

                class _AutoSurfaceRemesh(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to automatically remesh in order to remove excessive clustering of nodes. By default (auto), this is done if local sizing has been assigned or Share Topology is invoked, but skipped if not. Performance may be improved if this is disabled. In addition, you can choose to use the much faster refaceting technique as an alternative to automatic remeshing. When importing the mesh, remeshing is only performed if this option is set to yes and then all faces are remeshed; and the refaceting option is not available because the initial mesh cannot be refaceted.
                    """

                class _SMQualityImproveLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify a limiting value for skewness to improve the quality of the surface mesh. Quality improvement is attempted on those triangles where the skewness is above this limit.
                    """

                class _SetVolumeMeshMaxSize(PyArgumentsTextualSubItem):
                    """
                    Specify the maximum size of the elements for the surface mesh.
                    """

            class _ImportType(PyArgumentsTextualSubItem):
                """
                Argument ImportType.
                """

            class _AppendMesh(PyArgumentsParameterSubItem):
                """
                Argument AppendMesh.
                """

            class _CadFacetingFileName(PyArgumentsTextualSubItem):
                """
                Argument CadFacetingFileName.
                """

            class _Directory(PyArgumentsTextualSubItem):
                """
                Argument Directory.
                """

            class _Pattern(PyArgumentsTextualSubItem):
                """
                Argument Pattern.
                """

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Argument LengthUnit.
                """

            class _TesselationMethod(PyArgumentsTextualSubItem):
                """
                Argument TesselationMethod.
                """

            class _OriginalZones(PyArgumentsTextualSubItem):
                """
                Argument OriginalZones.
                """

            class _ExecuteShareTopology(PyArgumentsTextualSubItem):
                """
                For imported CAD assemblies with multiple parts, use this task to identify and close any problematic gaps and choose whether to join and/or intersect the problematic faces.   More...
                """

            class _CADFacetingControls(PyArgumentsSingletonSubItem):
                """
                Argument CADFacetingControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.RefineFaceting = self._RefineFaceting(self, "RefineFaceting", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.Tolerance = self._Tolerance(self, "Tolerance", service, rules, path)

                class _RefineFaceting(PyArgumentsParameterSubItem):
                    """
                    Argument RefineFaceting.
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum size of the elements for the surface mesh.
                    """

                class _Tolerance(PyArgumentsNumericalSubItem):
                    """
                    Argument Tolerance.
                    """

            class _CadImportOptions(PyArgumentsSingletonSubItem):
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
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)
                    self.ImportPartNames = self._ImportPartNames(self, "ImportPartNames", service, rules, path)
                    self.UsePartOrBodyAsSuffix = self._UsePartOrBodyAsSuffix(self, "UsePartOrBodyAsSuffix", service, rules, path)

                class _SavePMDBIntermediateFile(PyArgumentsParameterSubItem):
                    """
                    Argument SavePMDBIntermediateFile.
                    """

                class _OneObjectPer(PyArgumentsTextualSubItem):
                    """
                    Argument OneObjectPer.
                    """

                class _OpenAllCadInSubdirectories(PyArgumentsParameterSubItem):
                    """
                    Argument OpenAllCadInSubdirectories.
                    """

                class _CreateCADAssemblies(PyArgumentsParameterSubItem):
                    """
                    Argument CreateCADAssemblies.
                    """

                class _FeatureAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _OneZonePer(PyArgumentsTextualSubItem):
                    """
                    Argument OneZonePer.
                    """

                class _ImportCurvatureDataFromCAD(PyArgumentsParameterSubItem):
                    """
                    Argument ImportCurvatureDataFromCAD.
                    """

                class _ExtractFeatures(PyArgumentsParameterSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _ImportNamedSelections(PyArgumentsParameterSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

                class _ImportPartNames(PyArgumentsParameterSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _UsePartOrBodyAsSuffix(PyArgumentsParameterSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
                    """

            class _ShareTopologyPreferences(PyArgumentsSingletonSubItem):
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
                    self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                    self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                    self.Operation = self._Operation(self, "Operation", service, rules, path)
                    self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                    self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                    self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                    self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                    self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)

                class _STRenameInternals(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to apply body names from the imported geometry and use them in naming internal boundaries.  For instance, the internal face between two regions solid and body would be renamed to solid-body.
                    """

                class _ModelIsPeriodic(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not you need to set up periodic boundaries. If you select yes, then choose your periodic boundaries from the list of available boundaries.
                    """

                class _ConnectLabelWildcard(PyArgumentsTextualSubItem):
                    """
                    Enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _AllowDefeaturing(PyArgumentsTextualSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _RelativeShareTopologyTolerance(PyArgumentsNumericalSubItem):
                    """
                    Specify the relative tolerance for joining or intersecting face pairs, or the relative tolerance for connecting edge and face pairs.
                    """

                class _FluidLabelWildcard(PyArgumentsTextualSubItem):
                    """
                    Argument FluidLabelWildcard.
                    """

                class _ExecuteJoinIntersect(PyArgumentsTextualSubItem):
                    """
                    Choose whether the system will only join faces, only intersect faces, or do both.
                    """

                class _Operation(PyArgumentsTextualSubItem):
                    """
                    Choose whether to apply share topology using the Join-Intersect method where you join and/or intersect the problematic faces, or using the Interface Connect method where you connect edges of overlapping face pairs. Note that imprinting of overlapping faces in SCDM/Discovery is highly recommended for the Interface Connect method.
                    """

                class _ShareTopologyAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the threshold angle for joining face pairs.
                    """

                class _STToleranceIncrement(PyArgumentsNumericalSubItem):
                    """
                    Specify the increment by which the tolerance changes for each attempt to join face pairs.
                    """

                class _ShowShareTopologyPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _PerLabelList(PyArgumentsTextualSubItem):
                    """
                    Argument PerLabelList.
                    """

                class _IntfLabelList(PyArgumentsTextualSubItem):
                    """
                    Enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _AdvancedImprove(PyArgumentsTextualSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _NumberOfJoinTries(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of attempts that will be made to join face pairs under the given criteria.
                    """

            class _PreviewSizeToggle(PyArgumentsParameterSubItem):
                """
                For an imported surface mesh, use this field to visualize those boundaries that already have assigned local sizing controls (and any selected boundaries if applicable).
                """

        def create_instance(self) -> _GenerateTheSurfaceMeshWTMArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheSurfaceMeshWTMArguments(*args)

    class GenerateTheVolumeMeshFTM(PyCommand):
        """
        This task will generate the volume mesh for all the fluid regions. It will generate the cell type based on the selection from the Volume Fill setting in the Update Region Settings  task. Boundary layer prisms will also be generated if assigned for the fluid region. Use the Edit Volume Fill Setting option to view previous settings and edit them accordingly prior to creating the volume mesh.
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
        ThinVolumeMeshingMaxAspectRatio : float
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
        class _GenerateTheVolumeMeshFTMArguments(PyArguments):
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
                self.ThinVolumeMeshingMaxAspectRatio = self._ThinVolumeMeshingMaxAspectRatio(self, "ThinVolumeMeshingMaxAspectRatio", service, rules, path)
                self.ConformalPrismSplit = self._ConformalPrismSplit(self, "ConformalPrismSplit", service, rules, path)
                self.TetPrismStairstepExposedQuads = self._TetPrismStairstepExposedQuads(self, "TetPrismStairstepExposedQuads", service, rules, path)
                self.PrismNormalSmoothRelaxationFactor = self._PrismNormalSmoothRelaxationFactor(self, "PrismNormalSmoothRelaxationFactor", service, rules, path)
                self.ShowSubTasks = self._ShowSubTasks(self, "ShowSubTasks", service, rules, path)

            class _MeshQuality(PyArgumentsNumericalSubItem):
                """
                Argument MeshQuality.
                """

            class _OrthogonalQuality(PyArgumentsNumericalSubItem):
                """
                This value sets the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit, and is recommended to be around 0.04.
                """

            class _EnableParallel(PyArgumentsParameterSubItem):
                """
                Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.
                """

            class _SaveVolumeMesh(PyArgumentsParameterSubItem):
                """
                Select this option to save the volume mesh.
                """

            class _EditVolumeSettings(PyArgumentsParameterSubItem):
                """
                Enable this option to review and/or edit the fill settings for your volume region(s).
                """

            class _RegionNameList(PyArgumentsTextualSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionVolumeFillList(PyArgumentsTextualSubItem):
                """
                Argument RegionVolumeFillList.
                """

            class _RegionSizeList(PyArgumentsTextualSubItem):
                """
                Argument RegionSizeList.
                """

            class _OldRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionVolumeFillList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionVolumeFillList.
                """

            class _OldRegionSizeList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionSizeList.
                """

            class _AllRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionNameList.
                """

            class _AllRegionVolumeFillList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionVolumeFillList.
                """

            class _AllRegionSizeList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionSizeList.
                """

            class _AdvancedOptions(PyArgumentsParameterSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _SpikeRemovalAngle(PyArgumentsNumericalSubItem):
                """
                Argument SpikeRemovalAngle.
                """

            class _DihedralMinAngle(PyArgumentsNumericalSubItem):
                """
                Argument DihedralMinAngle.
                """

            class _QualityMethod(PyArgumentsTextualSubItem):
                """
                Choose from different types of mesh quality controls (aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows) and Enhanced Orthogonal. For more information, see  More... .
                """

            class _AvoidHangingNodes(PyArgumentsTextualSubItem):
                """
                Specify whether or not you want to avoid any potential 1:8 cell transition in the hexcore or polyhexcore region of the volume mesh, replacing any abrupt change in the cell size with tetrahedral or polyhedral cells.
                """

            class _OctreePeelLayers(PyArgumentsNumericalSubItem):
                """
                Specify the number of octree layers to be removed between the boundary and the core. The resulting cavity will be filled with tet cells for hexcore meshes and with poly cells for polyhexcore meshes.
                """

            class _FillWithSizeField(PyArgumentsTextualSubItem):
                """
                Determine whether or not you want to use size fields when generating the volume mesh. Generating the volume mesh using size fields can require additional memory as you increase the number of processing cores. This is because the size field is replicated for each core as the size field is not properly distributed. When using size fields, you are limited by the size of the machine. When not using size fields, however, you require less memory and you can use a higher number of cores with limited RAM, leading to a faster mesh generation.
                """

            class _OctreeBoundaryFaceSizeRatio(PyArgumentsNumericalSubItem):
                """
                Specify the ratio between the octree face size and the boundary face size. The default is 2.5 such that the octree mesh near the boundary is 2.5 times larger than the boundary mesh.
                """

            class _GlobalBufferLayers(PyArgumentsNumericalSubItem):
                """
                Specify the number of buffer layers for the octree volume mesh. If size controls have not been defined previously, then the default is 2, otherwise the default is calculated based on the maximum growth size.
                """

            class _TetPolyGrowthRate(PyArgumentsNumericalSubItem):
                """
                Specify the maximum growth rate for tet and poly cells. By default, this corresponds to a growth rate of 1.2.
                """

            class _ThinVolumeMeshingMaxAspectRatio(PyArgumentsNumericalSubItem):
                """
                Argument ThinVolumeMeshingMaxAspectRatio.
                """

            class _ConformalPrismSplit(PyArgumentsTextualSubItem):
                """
                Since neighboring zones with different numbers of layers will lead to conformal prism layers between them, use this field to determine whether you want to split the boundary layer cells conformally or not. When this option is set to Yes, the prism sides of the two zones will share nodes. This option is only available when stair-stepping is invoked. Note that adjacent regions should have an even ratio of prism layers when using this option.
                """

            class _TetPrismStairstepExposedQuads(PyArgumentsTextualSubItem):
                """
                This option can be used when generating a tetrahedral mesh with prism cells and is set to No by default. Selecting Yes for this option will enable stair-stepping for exposed quadrilateral faces (exposed quads) on prism cells. Stair-stepping will prevent pyramids from being created on these exposed quads, which generally would lead to poor quality in the exposed quad location.
                """

            class _PrismNormalSmoothRelaxationFactor(PyArgumentsNumericalSubItem):
                """
                Specify the smoothness factor for normal prism layers. Increasing this value will generate more prism layers especially near sharp corners. Note that this option is only available when Enable Parallel Meshing for Fluids is turned on and when Stairstep is selected for the Post Improvement Method in the Add Boundary Layers task.
                """

            class _ShowSubTasks(PyArgumentsTextualSubItem):
                """
                Argument ShowSubTasks.
                """

        def create_instance(self) -> _GenerateTheVolumeMeshFTMArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheVolumeMeshFTMArguments(*args)

    class GenerateTheVolumeMeshWTM(PyCommand):
        """
        Generate a computational mesh for the entire volume within your geometry. As needed, specify and adjust various global properties of the boundary layer and the volume itself to ensure a comprehensive mesh for the entire flow volume. In many cases, the default values will be sufficient.  More...
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
        class _GenerateTheVolumeMeshWTMArguments(PyArguments):
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

            class _Solver(PyArgumentsTextualSubItem):
                """
                Specify the target solver for which you want to generate the volume mesh (Fluent or CFX).
                """

            class _VolumeFill(PyArgumentsTextualSubItem):
                """
                Specify the type of cell to be used in the volumetric mesh: polyhedra (default), poly-hexcore, hexcore, or tetrahedral.
                """

            class _MeshFluidRegions(PyArgumentsParameterSubItem):
                """
                Choose whether to mesh the fluid regions in addition to the solid regions. This is enabled by default, and can be enabled along with the Mesh Solid Regions option, however, both options cannot be turned off at the same time.
                """

            class _MeshSolidRegions(PyArgumentsParameterSubItem):
                """
                Choose whether to mesh the solid regions in addition to the fluid regions. This is enabled by default, and can be enabled along with the Mesh Fluid Regions option, however, both options cannot be turned off at the same time.
                """

            class _SizingMethod(PyArgumentsTextualSubItem):
                """
                Choose how the cell sizing controls (such as growth rate and the maximum cell length) will be evaluated: either globally or on a region-by-region basis.
                """

            class _VolumeFillControls(PyArgumentsSingletonSubItem):
                """
                Argument VolumeFillControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.HexMinCellLength = self._HexMinCellLength(self, "HexMinCellLength", service, rules, path)
                    self.TetPolyMaxCellLength = self._TetPolyMaxCellLength(self, "TetPolyMaxCellLength", service, rules, path)
                    self.PeelLayers = self._PeelLayers(self, "PeelLayers", service, rules, path)
                    self.Type = self._Type(self, "Type", service, rules, path)
                    self.CellSizing = self._CellSizing(self, "CellSizing", service, rules, path)
                    self.HexMaxSize = self._HexMaxSize(self, "HexMaxSize", service, rules, path)
                    self.HexMaxCellLength = self._HexMaxCellLength(self, "HexMaxCellLength", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.BufferLayers = self._BufferLayers(self, "BufferLayers", service, rules, path)

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxSize.
                    """

                class _HexMinCellLength(PyArgumentsNumericalSubItem):
                    """
                    The minimum cell length for the hexcore or  poly-hexcore volume fill types.
                    """

                class _TetPolyMaxCellLength(PyArgumentsNumericalSubItem):
                    """
                    The maximum cell length for either the tetrahedron, polyhedron, or poly-hexcore volume fill types.
                    """

                class _PeelLayers(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of layers that control the gap between the hexahedra core and the geometry.  This distance is assumed to be the height of an ideal tetrahedral cell on the boundary face.
                    """

                class _Type(PyArgumentsTextualSubItem):
                    """
                    Argument Type.
                    """

                class _CellSizing(PyArgumentsTextualSubItem):
                    """
                    Argument CellSizing.
                    """

                class _HexMaxSize(PyArgumentsNumericalSubItem):
                    """
                    Argument HexMaxSize.
                    """

                class _HexMaxCellLength(PyArgumentsNumericalSubItem):
                    """
                    The maximum cell length for the hexahedron volume fill type.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the rate of growth for a tetrahedron or polyhedron mesh.
                    """

                class _BufferLayers(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of additional layers required to cover the rapid transition between finer cells in the boundary mesh and the coarser cells in the initial Cartesian mesh.
                    """

            class _RegionBasedPreferences(PyArgumentsParameterSubItem):
                """
                Argument RegionBasedPreferences.
                """

            class _ReMergeZones(PyArgumentsTextualSubItem):
                """
                After separating zones during surface meshing, here, choose to re-merge the zones prior to creating the volume mesh.
                """

            class _ParallelMeshing(PyArgumentsParameterSubItem):
                """
                Allows you to employ parallel settings for quicker and more efficient volume meshing. Disable this option if you are interested in only generating the volume mesh in serial mode.
                """

            class _VolumeMeshPreferences(PyArgumentsSingletonSubItem):
                """
                Argument VolumeMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MergeBodyLabels = self._MergeBodyLabels(self, "MergeBodyLabels", service, rules, path)
                    self.PolyFeatureAngle = self._PolyFeatureAngle(self, "PolyFeatureAngle", service, rules, path)
                    self.MinPolySize = self._MinPolySize(self, "MinPolySize", service, rules, path)
                    self.QualityMethod = self._QualityMethod(self, "QualityMethod", service, rules, path)
                    self.UseSizeFieldInSolids = self._UseSizeFieldInSolids(self, "UseSizeFieldInSolids", service, rules, path)
                    self.UseSizeField = self._UseSizeField(self, "UseSizeField", service, rules, path)
                    self.ShowVolumeMeshPreferences = self._ShowVolumeMeshPreferences(self, "ShowVolumeMeshPreferences", service, rules, path)
                    self.TetInSolids = self._TetInSolids(self, "TetInSolids", service, rules, path)
                    self.AddMultipleQualityMethods = self._AddMultipleQualityMethods(self, "AddMultipleQualityMethods", service, rules, path)
                    self.MaxCellSizeChange = self._MaxCellSizeChange(self, "MaxCellSizeChange", service, rules, path)
                    self.WritePrismControlFile = self._WritePrismControlFile(self, "WritePrismControlFile", service, rules, path)
                    self.MinFaceArea = self._MinFaceArea(self, "MinFaceArea", service, rules, path)
                    self.CheckSelfProximity = self._CheckSelfProximity(self, "CheckSelfProximity", service, rules, path)
                    self.Avoid1_8Transition = self._Avoid1_8Transition(self, "Avoid1_8Transition", service, rules, path)
                    self.PrepareZoneNames = self._PrepareZoneNames(self, "PrepareZoneNames", service, rules, path)
                    self.MinEdgeLength = self._MinEdgeLength(self, "MinEdgeLength", service, rules, path)
                    self.SolidGrowthRate = self._SolidGrowthRate(self, "SolidGrowthRate", service, rules, path)
                    self.PolyInSolids = self._PolyInSolids(self, "PolyInSolids", service, rules, path)
                    self.QualityWarningLimit = self._QualityWarningLimit(self, "QualityWarningLimit", service, rules, path)

                class _MergeBodyLabels(PyArgumentsTextualSubItem):
                    """
                    Determine whether or not you would like to merge bodies that contain multiple body labels when generating the volume mesh (the default is yes)
                    """

                class _PolyFeatureAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the angle to preserve features when using a polyhedral-based mesh.
                    """

                class _MinPolySize(PyArgumentsNumericalSubItem):
                    """
                    Argument MinPolySize.
                    """

                class _QualityMethod(PyArgumentsTextualSubItem):
                    """
                    Choose from several different types of mesh quality controls (skewness, aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows), Enhanced Orthogonal, and Skewness. For more information, see  More... .
                    """

                class _UseSizeFieldInSolids(PyArgumentsTextualSubItem):
                    """
                    This option is available when both the Use Size Field? and Fill Polyhedra in Solids? options are enabled for the poly-hexcore fill method. By default this option is set to no, which specifies growth-rate-based sizing for polyhedra regions during poly-hexcore generation. Selecting yes for this option specifies the sizing for polyhedra regions to be size-field based and is recommended when BOI(s) or body sizing have been defined that include the polyhedra region.
                    """

                class _UseSizeField(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not to use size fields as part of generating the volume mesh. By default, this is set to yes when a BOI or body sizing has been defined in the Add Local Sizing task, however, for large cases, it can be turned off for the hexcore and poly-hexcore volume fill methods.
                    """

                class _ShowVolumeMeshPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _TetInSolids(PyArgumentsTextualSubItem):
                    """
                    Argument TetInSolids.
                    """

                class _AddMultipleQualityMethods(PyArgumentsTextualSubItem):
                    """
                    Argument AddMultipleQualityMethods.
                    """

                class _MaxCellSizeChange(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxCellSizeChange.
                    """

                class _WritePrismControlFile(PyArgumentsTextualSubItem):
                    """
                    Indicate whether or not you want to save a .pzmcontrol file to your working folder that will contain the boundary (prism) layer specifications.
                    """

                class _MinFaceArea(PyArgumentsNumericalSubItem):
                    """
                    Argument MinFaceArea.
                    """

                class _CheckSelfProximity(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not you would like to check for proximity issues (such as overlapping surfaces, very small gaps between surfaces, very sharp angles, etc.). Problematic areas will be highlighted in the graphics window if this option is set to yes.
                    """

                class _Avoid1_8Transition(PyArgumentsTextualSubItem):
                    """
                    Indicate whether or not you want to avoid any potential 1:8 cell transition in the hexcore region of the volume mesh, replacing any abrupt change in the cell size with polyhedral cells to improve solver performance in such transitional areas.
                    """

                class _PrepareZoneNames(PyArgumentsTextualSubItem):
                    """
                    Indicate whether or not you want to persistently rename volume mesh components. This will make zone names equivalent to region names, and will make cell and face zone names unique.  Using this field is highly recommended for any parametric study. Persistent renaming only works if all body names are unique.
                    """

                class _MinEdgeLength(PyArgumentsNumericalSubItem):
                    """
                    Argument MinEdgeLength.
                    """

                class _SolidGrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the rate of growth for a tetrahedron or polyhedron mesh.
                    """

                class _PolyInSolids(PyArgumentsTextualSubItem):
                    """
                    Indicate whether or not to fill only polyhedra cells in all solid regions during volume meshing using the poly-hexcore volume fill method.  The default value is no. Setting this to yes may improve meshing efficiency.
                    """

                class _QualityWarningLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify the threshold for when mesh quality improvements are automatically invoked that employ the orthogonal quality limit.
                    """

            class _PrismPreferences(PyArgumentsSingletonSubItem):
                """
                Display global settings for your boundary layers. Note that these settings are not applied for Multizone boundary layers
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.PrismKeepFirstLayer = self._PrismKeepFirstLayer(self, "PrismKeepFirstLayer", service, rules, path)
                    self.PrismMaxAspectRatio = self._PrismMaxAspectRatio(self, "PrismMaxAspectRatio", service, rules, path)
                    self.StairStepIcemQualityLimit = self._StairStepIcemQualityLimit(self, "StairStepIcemQualityLimit", service, rules, path)
                    self.PrismStairStepOptions = self._PrismStairStepOptions(self, "PrismStairStepOptions", service, rules, path)
                    self.PrismGapFactor = self._PrismGapFactor(self, "PrismGapFactor", service, rules, path)
                    self.IgnoreInflation = self._IgnoreInflation(self, "IgnoreInflation", service, rules, path)
                    self.MergeBoundaryLayers = self._MergeBoundaryLayers(self, "MergeBoundaryLayers", service, rules, path)
                    self.ShowPrismPreferences = self._ShowPrismPreferences(self, "ShowPrismPreferences", service, rules, path)
                    self.NormalSmoothRelaxationFactor = self._NormalSmoothRelaxationFactor(self, "NormalSmoothRelaxationFactor", service, rules, path)
                    self.PrismMinAspectRatio = self._PrismMinAspectRatio(self, "PrismMinAspectRatio", service, rules, path)
                    self.StairstepExposedQuads = self._StairstepExposedQuads(self, "StairstepExposedQuads", service, rules, path)
                    self.PrismAdjacentAngle = self._PrismAdjacentAngle(self, "PrismAdjacentAngle", service, rules, path)

                class _PrismKeepFirstLayer(PyArgumentsTextualSubItem):
                    """
                    Specify whether to retain the initial boundary layer height.
                    """

                class _PrismMaxAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum aspect ratio for the boundary layer when proximity compression is applied.
                    """

                class _StairStepIcemQualityLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument StairStepIcemQualityLimit.
                    """

                class _PrismStairStepOptions(PyArgumentsTextualSubItem):
                    """
                    Use this option to reduce the stair-stepping at certain locations based on quality or proximity criteria. By default, Yes allows you to retain the default stair-step handling, otherwise you can also choose No, Exclude proximity check, No, Exclude quality check, or No, Exclude both checks.
                    """

                class _PrismGapFactor(PyArgumentsNumericalSubItem):
                    """
                    Specify the relative gap-size (based on local mesh size) between two boundary layer caps. If this limit is exceeded, the boundary layer will automatically be compressed.
                    """

                class _IgnoreInflation(PyArgumentsTextualSubItem):
                    """
                    Specify whether to automatically ignore boundary layers where there is an acute angle.
                    """

                class _MergeBoundaryLayers(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not you want to have the boundary layer mesh merged into the bulk mesh.
                    """

                class _ShowPrismPreferences(PyArgumentsParameterSubItem):
                    """
                    Display global settings for your boundary layers. Note that these settings are not applied for Multizone boundary layers
                    """

                class _NormalSmoothRelaxationFactor(PyArgumentsNumericalSubItem):
                    """
                    Specify the smoothness factor for normal prism layers. Increasing this value will generate more prism layers especially near sharp corners.
                    """

                class _PrismMinAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Controls the minimum aspect ratio for cells at the boundary of the thin volume mesh regions. By default, this option is set to 0.3, other than for Stacked Plates, where it is set to 0.1. For flat parallel plates (not including stacked plates), it is recommended to use a value of 0.1 to produce a high quality thin volume mesh.
                    """

                class _StairstepExposedQuads(PyArgumentsTextualSubItem):
                    """
                    This option can be used when generating a tetrahedral mesh with prism cells and is set to No by default. Selecting Yes for this option will enable stair-stepping for exposed quadrilateral faces (exposed quads) on prism cells. Stair-stepping will prevent pyramids from being created on these exposed quads, which generally would lead to poor quality in the exposed quad location.
                    """

                class _PrismAdjacentAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the angle for which the boundary layer would imprint on an adjacent boundary.
                    """

            class _GlobalThinVolumePreferences(PyArgumentsSingletonSubItem):
                """
                Argument GlobalThinVolumePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowGlobalThinVolumePreferences = self._ShowGlobalThinVolumePreferences(self, "ShowGlobalThinVolumePreferences", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.StairStep = self._StairStep(self, "StairStep", service, rules, path)
                    self.AutoOrderControls = self._AutoOrderControls(self, "AutoOrderControls", service, rules, path)

                class _ShowGlobalThinVolumePreferences(PyArgumentsParameterSubItem):
                    """
                    Display global settings for thin volume meshing.
                    """

                class _MinAspectRatio(PyArgumentsNumericalSubItem):
                    """
                    Controls the minimum aspect ratio for cells at the boundary of the thin volume mesh regions. By default, this option is set to 0.3, other than for Stacked Plates, where it is set to 0.1. For flat parallel plates (not including stacked plates), it is recommended to use a value of 0.1 to produce a high quality thin volume mesh.
                    """

                class _StairStep(PyArgumentsTextualSubItem):
                    """
                    Use this option to invoke stair-stepping at thin volume mesh regions.
                    """

                class _AutoOrderControls(PyArgumentsTextualSubItem):
                    """
                    When set to yes, will automatically swap source and target faces in order to increase the success rate of the thin volume mesh generation. This option is set to yes by default for conventional thin volume meshing and is set to no when Stacked Plates is enabled.
                    """

            class _InvokePrimsControl(PyArgumentsTextualSubItem):
                """
                Argument InvokePrimsControl.
                """

            class _OffsetMethodType(PyArgumentsTextualSubItem):
                """
                Choose the type of offset to determine how the mesh cells closest to the boundary are generated.  More...
                """

            class _NumberOfLayers(PyArgumentsNumericalSubItem):
                """
                Select the number of boundary layers to be generated.
                """

            class _FirstAspectRatio(PyArgumentsNumericalSubItem):
                """
                Specify the aspect ratio of the first layer of prism cells that are extruded from the base boundary zone.
                """

            class _TransitionRatio(PyArgumentsNumericalSubItem):
                """
                Specify the rate at which adjacent elements grow, for the smooth transition offset method.
                """

            class _Rate(PyArgumentsNumericalSubItem):
                """
                Specify the rate of growth for the boundary layer.
                """

            class _FirstHeight(PyArgumentsNumericalSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _MeshDeadRegions(PyArgumentsParameterSubItem):
                """
                Argument MeshDeadRegions.
                """

            class _BodyLabelList(PyArgumentsTextualSubItem):
                """
                Argument BodyLabelList.
                """

            class _PrismLayers(PyArgumentsParameterSubItem):
                """
                Argument PrismLayers.
                """

            class _QuadTetTransition(PyArgumentsTextualSubItem):
                """
                Argument QuadTetTransition.
                """

            class _MergeCellZones(PyArgumentsParameterSubItem):
                """
                Argument MergeCellZones.
                """

            class _FaceScope(PyArgumentsSingletonSubItem):
                """
                Argument FaceScope.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                    self.GrowOn = self._GrowOn(self, "GrowOn", service, rules, path)
                    self.FaceScopeMeshObject = self._FaceScopeMeshObject(self, "FaceScopeMeshObject", service, rules, path)
                    self.RegionsType = self._RegionsType(self, "RegionsType", service, rules, path)

                class _TopologyList(PyArgumentsTextualSubItem):
                    """
                    Argument TopologyList.
                    """

                class _GrowOn(PyArgumentsTextualSubItem):
                    """
                    Argument GrowOn.
                    """

                class _FaceScopeMeshObject(PyArgumentsTextualSubItem):
                    """
                    Argument FaceScopeMeshObject.
                    """

                class _RegionsType(PyArgumentsTextualSubItem):
                    """
                    Argument RegionsType.
                    """

            class _RegionTetNameList(PyArgumentsTextualSubItem):
                """
                Argument RegionTetNameList.
                """

            class _RegionTetMaxCellLengthList(PyArgumentsTextualSubItem):
                """
                Argument RegionTetMaxCellLengthList.
                """

            class _RegionTetGrowthRateList(PyArgumentsTextualSubItem):
                """
                Argument RegionTetGrowthRateList.
                """

            class _RegionHexNameList(PyArgumentsTextualSubItem):
                """
                Argument RegionHexNameList.
                """

            class _RegionHexMaxCellLengthList(PyArgumentsTextualSubItem):
                """
                Argument RegionHexMaxCellLengthList.
                """

            class _OldRegionTetMaxCellLengthList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionTetMaxCellLengthList.
                """

            class _OldRegionTetGrowthRateList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionTetGrowthRateList.
                """

            class _OldRegionHexMaxCellLengthList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionHexMaxCellLengthList.
                """

            class _CFDSurfaceMeshControls(PyArgumentsSingletonSubItem):
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
                    self.SurfaceMeshMethod = self._SurfaceMeshMethod(self, "SurfaceMeshMethod", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyArgumentsParameterSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyArgumentsParameterSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyArgumentsTextualSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyArgumentsParameterSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SurfaceMeshMethod(PyArgumentsTextualSubItem):
                    """
                    Argument SurfaceMeshMethod.
                    """

                class _SizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyArgumentsParameterSubItem):
                    """
                    Argument DrawSizeControl.
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyArgumentsTextualSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the rate of growth for a tetrahedron or polyhedron mesh.
                    """

                class _ObjectBasedControls(PyArgumentsTextualSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _ShowSolidFluidMeshed(PyArgumentsParameterSubItem):
                """
                Argument ShowSolidFluidMeshed.
                """

        def create_instance(self) -> _GenerateTheVolumeMeshWTMArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateTheVolumeMeshWTMArguments(*args)

    class GeometrySetup(PyCommand):
        """
        Specify the type of geometry you are importing: whether it is a solid model a fluid model, or both. The workflow changes based on your selection. Additionally, for fluid volume extraction, you need to indicate whether or not any openings need to be closed.  More...
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
        FluidRegions : list[str]
        SMImprovePreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _GeometrySetupArguments(PyArguments):
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
                self.FluidRegions = self._FluidRegions(self, "FluidRegions", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)

            class _SetupType(PyArgumentsTextualSubItem):
                """
                Choose whether your geometry represents only a solid body, only a fluid body, or both a solid and fluid body.
                """

            class _CappingRequired(PyArgumentsTextualSubItem):
                """
                Choose whether or not you are going to perform any capping operations, thereby enclosing a fluid region.
                """

            class _WallToInternal(PyArgumentsTextualSubItem):
                """
                Choose whether or not to change interior fluid-fluid boundaries from type "wall" to "internal". Only internal boundaries bounded by two fluid regions are converted into internal zone types. If new fluid regions are assigned, this task is executed after the Update Regions task. Internal boundaries that are designated as "baffles" are retained as walls.
                """

            class _InvokeShareTopology(PyArgumentsTextualSubItem):
                """
                For CAD assemblies with multiple parts, choose whether or not to identify and close any problematic gaps and whether to join and/or intersect problematic faces. This will add an Apply Share Topology task to your workflow. Note that in situations where you want to use overlapping non-conformal interfaces, you must use the non-conformal option. In all other situations, such as when you have totally disconnected bodies (that is, with no overlap), you should instead elect to choose the Share Topology option even if there is nothing to share.
                """

            class _NonConformal(PyArgumentsTextualSubItem):
                """
                Determine whether or not you want to create non-conformal meshes between the objects in your geometry. Note that in situations where you want to use overlapping non-conformal interfaces, you must use the non-conformal option. In all other situations, such as when you have totally disconnected bodies (that is, with no overlap), you should instead elect to choose the Share Topology option even if there is nothing to share.
                """

            class _Multizone(PyArgumentsTextualSubItem):
                """
                Determine whether or not you want to perform multi-zone meshing on your geometry. Selecting Yes will add an Add Multizone Controls task and a Generate Multizone Mesh task to your workflow.
                """

            class _SetupInternals(PyArgumentsTextualSubItem):
                """
                Argument SetupInternals.
                """

            class _SetupInternalTypes(PyArgumentsTextualSubItem):
                """
                Argument SetupInternalTypes.
                """

            class _OldZoneList(PyArgumentsTextualSubItem):
                """
                Argument OldZoneList.
                """

            class _OldZoneTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldZoneTypeList.
                """

            class _RegionList(PyArgumentsTextualSubItem):
                """
                Argument RegionList.
                """

            class _EdgeZoneList(PyArgumentsTextualSubItem):
                """
                Argument EdgeZoneList.
                """

            class _EdgeLabels(PyArgumentsTextualSubItem):
                """
                Argument EdgeLabels.
                """

            class _Duplicates(PyArgumentsParameterSubItem):
                """
                Argument Duplicates.
                """

            class _FluidRegions(PyArgumentsTextualSubItem):
                """
                Argument FluidRegions.
                """

            class _SMImprovePreferences(PyArgumentsSingletonSubItem):
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

                class _SIStepQualityLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument SIStepQualityLimit.
                    """

                class _SIQualityCollapseLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument SIQualityCollapseLimit.
                    """

                class _SIQualityIterations(PyArgumentsNumericalSubItem):
                    """
                    Argument SIQualityIterations.
                    """

                class _SIQualityMaxAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument SIQualityMaxAngle.
                    """

                class _AllowDefeaturing(PyArgumentsTextualSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _ShowSMImprovePreferences(PyArgumentsParameterSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _AdvancedImprove(PyArgumentsTextualSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _SIStepWidth(PyArgumentsNumericalSubItem):
                    """
                    Argument SIStepWidth.
                    """

                class _SIRemoveStep(PyArgumentsTextualSubItem):
                    """
                    Argument SIRemoveStep.
                    """

        def create_instance(self) -> _GeometrySetupArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GeometrySetupArguments(*args)

    class IdentifyConstructionSurfaces(PyCommand):
        """
        Identify specific portions of your imported geometry that may exist as some form of construction surface, such as capping surface(s), or cylindrical surface(s) (for identifying moving reference frames, for example). You need to identify such objects within your geometry as being construction surfaces so that Fluent can mange those objects accordingly during the meshing process. More...
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
        class _IdentifyConstructionSurfacesArguments(PyArguments):
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

            class _MRFName(PyArgumentsTextualSubItem):
                """
                Specify a name for the construction surface or use the default value.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Choose whether to create the construction surface using an Existing object or zone, a bounding Box, or by using an Offset Surface.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ObjectSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single object from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single zone from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionSingle(PyArgumentsTextualSubItem):
                """
                Choose a single label from the list below. Use the Filter Text field to provide text and/or regular expressions in filtering the list. The matching list item(s) are automatically displayed in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _DefeaturingSize(PyArgumentsNumericalSubItem):
                """
                Specify a value that is used to obtain a rough shape of the selected object(s). The larger the value, the more approximate the shape.
                """

            class _OffsetHeight(PyArgumentsNumericalSubItem):
                """
                Specify the height of the offset construction surface. This is how far from the selected object(s) the rough shape is offset.
                """

            class _Pivot(PyArgumentsSingletonSubItem):
                """
                Argument Pivot.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Argument X.
                    """

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Argument Z.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Argument Y.
                    """

            class _Axis(PyArgumentsSingletonSubItem):
                """
                Argument Axis.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.Z_Comp = self._Z_Comp(self, "Z-Comp", service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _Z_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Comp.
                    """

                class _X_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _Rotation(PyArgumentsSingletonSubItem):
                """
                Argument Rotation.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X_Comp = self._X_Comp(self, "X-Comp", service, rules, path)
                    self.Y_Comp = self._Y_Comp(self, "Y-Comp", service, rules, path)

                class _X_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Comp.
                    """

                class _Y_Comp(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Comp.
                    """

            class _CylinderObject(PyArgumentsSingletonSubItem):
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
                    self.Y_Offset = self._Y_Offset(self, "Y-Offset", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyArgumentsTextualSubItem):
                    """
                    Argument HeightNode.
                    """

                class _X_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument X-Offset.
                    """

                class _HeightBackInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _X1(PyArgumentsNumericalSubItem):
                    """
                    Argument X1.
                    """

                class _Y1(PyArgumentsNumericalSubItem):
                    """
                    Argument Y1.
                    """

                class _Z_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Z-Offset.
                    """

                class _Z2(PyArgumentsNumericalSubItem):
                    """
                    Argument Z2.
                    """

                class _Node1(PyArgumentsTextualSubItem):
                    """
                    Argument Node1.
                    """

                class _Z1(PyArgumentsNumericalSubItem):
                    """
                    Argument Z1.
                    """

                class _Radius2(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius2.
                    """

                class _Y2(PyArgumentsNumericalSubItem):
                    """
                    Argument Y2.
                    """

                class _Node3(PyArgumentsTextualSubItem):
                    """
                    Argument Node3.
                    """

                class _X2(PyArgumentsNumericalSubItem):
                    """
                    Argument X2.
                    """

                class _Y_Offset(PyArgumentsNumericalSubItem):
                    """
                    Argument Y-Offset.
                    """

                class _Node2(PyArgumentsTextualSubItem):
                    """
                    Argument Node2.
                    """

                class _HeightFrontInc(PyArgumentsNumericalSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Radius1(PyArgumentsNumericalSubItem):
                    """
                    Argument Radius1.
                    """

            class _CylinderMethod(PyArgumentsTextualSubItem):
                """
                Argument CylinderMethod.
                """

            class _BoundingBoxObject(PyArgumentsSingletonSubItem):
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

                class _SizeRelativeLength(PyArgumentsTextualSubItem):
                    """
                    Determine if you would like to specify the bounding box for the construction surface as a ratio of the geometry length, or by specifying a specific location for the minimum and maximum coordinates.
                    """

                class _XmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

                class _XminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value. The value is the ratio relative to the geometry size in the X direction.
                    """

                class _YminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _Zmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value.
                    """

                class _Zmax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value.
                    """

                class _Ymax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value.
                    """

                class _ZminRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _Ymin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the Y direction by the specified value.
                    """

                class _Xmin(PyArgumentsNumericalSubItem):
                    """
                    Extends the minimum size of the bounding box in the X direction by the specified value.
                    """

                class _YmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Y direction by the specified value. The value is the ratio relative to the geometry size in the Y direction.
                    """

                class _ZmaxRatio(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the Z direction by the specified value. The value is the ratio relative to the geometry size in the Z direction.
                    """

                class _Xmax(PyArgumentsNumericalSubItem):
                    """
                    Extends the maximum size of the bounding box in the X direction by the specified value.
                    """

        def create_instance(self) -> _IdentifyConstructionSurfacesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyConstructionSurfacesArguments(*args)

    class IdentifyDeviatedFaces(PyCommand):
        """
        Use this task to identify how the wrapped surface mesh differs from the original geometry. This task can be useful for identifying deviations in the surface mesh in, for example, geometries with sharp angles.
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
        class _IdentifyDeviatedFacesArguments(PyArguments):
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

            class _DisplayGridName(PyArgumentsTextualSubItem):
                """
                Enter a name for the identified deviated faces.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Specify whether the identification of deviated faces is to be applied to an indicated object or zone.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _AdvancedOptions(PyArgumentsParameterSubItem):
                """
                Enable this option to automatically calculate the minimum and maximum deviation for the selected object(s) or zone(s).
                """

            class _DeviationMinValue(PyArgumentsNumericalSubItem):
                """
                When Auto Compute is disabled, specify a minimum value for the deviation.
                """

            class _DeviationMaxValue(PyArgumentsNumericalSubItem):
                """
                When Auto Compute is disabled, specify a maximum value for the deviation.
                """

            class _Overlay(PyArgumentsTextualSubItem):
                """
                Determine how you want the deviated faces to be displayed (either with the mesh or with the geometry).
                """

            class _IncludeGapCoverGeometry(PyArgumentsTextualSubItem):
                """
                Determine if you want to include any gap covers in the check for deviated faces. If so, the default minimum and maximum deviation range is automatically calculated.
                """

        def create_instance(self) -> _IdentifyDeviatedFacesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyDeviatedFacesArguments(*args)

    class IdentifyOrphans(PyCommand):
        """
        Use this task to isolate and locate any orphan cells in your mesh. 
                        More...
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
        class _IdentifyOrphansArguments(PyArguments):
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

            class _NumberOfOrphans(PyArgumentsTextualSubItem):
                """
                Specify the allowable number of orphans to accept in your mesh.
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Select one or more mesh objects that you would like to identify any potential orphan faces. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _EnableGridPriority(PyArgumentsParameterSubItem):
                """
                Controls the ability to prioritize your overset grids (meshes). The priorities of the overset mesh are then carried over into the solver.
                """

            class _DonorPriorityMethod(PyArgumentsTextualSubItem):
                """
                Determines the location of the overset mesh. Choose how the mesh donor cells are prioritized - either based on the cell size (proportional to the inverse of the cell volume) or based on the boundary distance (proportional to the inverse of the distance to the closest boundary).
                """

            class _OverlapBoundaries(PyArgumentsTextualSubItem):
                """
                Determine if you need to account for any overlapping boundaries that may be present in your overset mesh (due to overlapping geometry and boundaries or those sometimes generated by collar meshes). You can improve the overset performance by setting this option to no.
                """

            class _CheckOversetInterfaceIntersection(PyArgumentsTextualSubItem):
                """
                Enabled by default, Fluent checks for any overset interface intersections while identifying orphans. Disable this option to skip the intersection check and increase the speed of identifying orphans.
                """

            class _RegionNameList(PyArgumentsTextualSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionSizeList(PyArgumentsTextualSubItem):
                """
                Argument RegionSizeList.
                """

            class _OldRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionSizeList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionSizeList.
                """

        def create_instance(self) -> _IdentifyOrphansArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyOrphansArguments(*args)

    class IdentifyRegions(PyCommand):
        """
        Identify specific regions in and around your imported geometry, such as a flow region surrounding a vehicle in an external flow simulation. In this task, you are positioning specific points in the domain where certain regions of interest can be identified and classified for later use in your simulation. More...
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
        class _IdentifyRegionsArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Determine whether or not you want to specify any fluid or void regions using this task.
                """

            class _MaterialPointsName(PyArgumentsTextualSubItem):
                """
                Specify a name for the region that you want to identify or use the default value.
                """

            class _MptMethodType(PyArgumentsTextualSubItem):
                """
                Choose how you want to identify the region: using a distinct numerical input of X, Y, and Z coordinates, using the centroid of the selected object, or by using an offset distance relative to the centroid of selected object/zone.
                """

            class _NewRegionType(PyArgumentsTextualSubItem):
                """
                Specify the type of region as being fluid, solid, or a void.
                """

            class _LinkConstruction(PyArgumentsTextualSubItem):
                """
                Keep the default value of no for most cases involving a singular fluid region. If you mean to identify an additional fluid region, choose yes to indicate that the current fluid region is either inside or adjacent to a construction surface(s), in order to properly mesh this fluid region accordingly (that is, using a surface mesh).
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object, label, or zone name).
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more labels from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects (or voids) from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _GraphicalSelection(PyArgumentsParameterSubItem):
                """
                Enable this option and select a point in the graphics window to be the center of the region.
                """

            class _ShowCoordinates(PyArgumentsParameterSubItem):
                """
                Enable this option when providing numerical inputs for the region location, and you want to view the exact coordinates.
                """

            class _X(PyArgumentsNumericalSubItem):
                """
                The x-coordinate of the center of the region.
                """

            class _Y(PyArgumentsNumericalSubItem):
                """
                The y-coordinate of the center of the region.
                """

            class _Z(PyArgumentsNumericalSubItem):
                """
                The z-coordinate of the center of the region.
                """

            class _OffsetX(PyArgumentsNumericalSubItem):
                """
                The x-coordinate of the offset distance relative to the centroid of the selected object/zone.
                """

            class _OffsetY(PyArgumentsNumericalSubItem):
                """
                The y-coordinate of the offset distance relative to the centroid of the selected object/zone.
                """

            class _OffsetZ(PyArgumentsNumericalSubItem):
                """
                The z-coordinate of the offset distance relative to the centroid of the selected object/zone.
                """

        def create_instance(self) -> _IdentifyRegionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._IdentifyRegionsArguments(*args)

    class ImportBodyOfInfluenceGeometry(PyCommand):
        """
        Specify the geometry or mesh file(s) that represent the bodies of influence you wish to import into the workflow. Choose from either a CAD file or a surface or volume mesh. For CAD geometries, choose the appropriate units in which the geometry was created. Browse, or specify the file name(s) and location for the CAD geometry or mesh that you are going to import. It is recommended to select units so that the minimum size is between approximately 0.1 and 10.  More...
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
        class _ImportBodyOfInfluenceGeometryArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.Type = self._Type(self, "Type", service, rules, path)
                self.GeometryFileName = self._GeometryFileName(self, "GeometryFileName", service, rules, path)
                self.MeshFileName = self._MeshFileName(self, "MeshFileName", service, rules, path)
                self.ImportedObjects = self._ImportedObjects(self, "ImportedObjects", service, rules, path)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.CadImportOptions = self._CadImportOptions(self, "CadImportOptions", service, rules, path)

            class _Type(PyArgumentsTextualSubItem):
                """
                Specify whether you are importing CAD geometry file(s) or whether you are specifying surface or volume mesh file(s) to represent bodies of influence for your simulation. The units for length will be the same as those specified in the Import Geometry task.
                """

            class _GeometryFileName(PyArgumentsTextualSubItem):
                """
                Select CAD file(s) to import into your simulation as a body of influence. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files)
                """

            class _MeshFileName(PyArgumentsTextualSubItem):
                """
                Select surface or volume mesh file(s) to import into your simulation as a body of influence. Supported file types are: \\*.msh, \\*.msh.gz, and \\*.msh.h5 files).
                """

            class _ImportedObjects(PyArgumentsTextualSubItem):
                """
                Argument ImportedObjects.
                """

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Argument LengthUnit.
                """

            class _CadImportOptions(PyArgumentsSingletonSubItem):
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

                class _SavePMDBIntermediateFile(PyArgumentsParameterSubItem):
                    """
                    Argument SavePMDBIntermediateFile.
                    """

                class _OneObjectPer(PyArgumentsTextualSubItem):
                    """
                    Argument OneObjectPer.
                    """

                class _OpenAllCadInSubdirectories(PyArgumentsParameterSubItem):
                    """
                    Argument OpenAllCadInSubdirectories.
                    """

                class _CreateCADAssemblies(PyArgumentsParameterSubItem):
                    """
                    Argument CreateCADAssemblies.
                    """

                class _FeatureAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _OneZonePer(PyArgumentsTextualSubItem):
                    """
                    Argument OneZonePer.
                    """

                class _ImportCurvatureDataFromCAD(PyArgumentsParameterSubItem):
                    """
                    Argument ImportCurvatureDataFromCAD.
                    """

                class _ExtractFeatures(PyArgumentsParameterSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _UsePartOrBodyAsSuffix(PyArgumentsParameterSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
                    """

                class _ImportPartNames(PyArgumentsParameterSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _ImportNamedSelections(PyArgumentsParameterSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

        def create_instance(self) -> _ImportBodyOfInfluenceGeometryArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImportBodyOfInfluenceGeometryArguments(*args)

    class ImportGeometry(PyCommand):
        """
        Specify the CAD geometry that you want to work with. Choose from either a CAD file or a surface or volume mesh. Choose the appropriate units in which the geometry or mesh was created. Choose any advanced options (such as faceting controls) that you want to take effect upon import. Browse, or specify the file name and location for the CAD geometry that you are going to import. It is recommended to select units so that the minimum size is between approximately 0.1 and 10.  More...
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
            Select a CAD file to import into your simulation. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: *.CATpart, *.prt, *.x_t, *.sat, *.step, and *.iges files).
        NumParts : float
        AppendMesh : bool
        Directory : str
        Pattern : str
        CadImportOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImportGeometryArguments(PyArguments):
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

            class _FileFormat(PyArgumentsTextualSubItem):
                """
                Indicate whether the imported geometry is a CAD File or a Mesh (either a surface or volume mesh).
                """

            class _ImportType(PyArgumentsTextualSubItem):
                """
                When the File Format is set to CAD, use the Import Type field to import a Single File (the default), or Multiple Files. When importing multiple files, the Select File dialog allows you to make multiple selections, as long as the files are in the same directory and are of the same CAD format.
                """

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Select a suitable working unit for the meshing operation, with a min size of the order of 1. The model will be automatically scaled to meters when switching to the solver. It is recommended to select units so that the minimum size is between approximately 0.1 - 10. If the minimum size falls outside of this range, then you should change the units.
                """

            class _MeshUnit(PyArgumentsTextualSubItem):
                """
                Specify the units in which the surface or volume mesh was created in.
                """

            class _UseBodyLabels(PyArgumentsTextualSubItem):
                """
                Specify that you want to use any composite body labels that are defined in your imported CAD geometry by choosing Yes. If the imported CAD file does not contain any body labels, then this will automatically be set to No.
                """

            class _ImportCadPreferences(PyArgumentsSingletonSubItem):
                """
                Argument ImportCadPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ExtractAngle = self._ExtractAngle(self, "ExtractAngle", service, rules, path)
                    self.FacetedBodies = self._FacetedBodies(self, "FacetedBodies", service, rules, path)
                    self.CISeparation = self._CISeparation(self, "CISeparation", service, rules, path)
                    self.EdgeLabel = self._EdgeLabel(self, "EdgeLabel", service, rules, path)
                    self.CIRefaceting = self._CIRefaceting(self, "CIRefaceting", service, rules, path)
                    self.AutomaticObjectCreation = self._AutomaticObjectCreation(self, "AutomaticObjectCreation", service, rules, path)
                    self.MaxFacetLength = self._MaxFacetLength(self, "MaxFacetLength", service, rules, path)
                    self.ShowImportCadPreferences = self._ShowImportCadPreferences(self, "ShowImportCadPreferences", service, rules, path)
                    self.MergeNodes = self._MergeNodes(self, "MergeNodes", service, rules, path)
                    self.CISeparationAngle = self._CISeparationAngle(self, "CISeparationAngle", service, rules, path)
                    self.CITolerence = self._CITolerence(self, "CITolerence", service, rules, path)

                class _ExtractAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument ExtractAngle.
                    """

                class _FacetedBodies(PyArgumentsTextualSubItem):
                    """
                    When performing faceting and wrapping operations in your CAD tool lead to non-CAD geometries, set this option to yes to be able to use such geometries in the workflow. To ensure a relatively good quality surface mesh, you should shrink wrap any faceted bodies. In addition, each shrink-wrapped faceted body should be defined in its own unique component within the CAD environment.
                    """

                class _CISeparation(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not you are going to separate zones upon import based on a region, a region and a specified separation angle, a face, or neither. This is required to select faces for local sizing. If Named Selections have already been defined at these locations, then separation is not needed.
                    """

                class _EdgeLabel(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not the imported CAD geometry already includes specific edges with assigned names (named selections). These named edges can be available later in the workflow when you are adding local size controls.
                    """

                class _CIRefaceting(PyArgumentsParameterSubItem):
                    """
                    Enable this option to be able to set the Tolerance and the Max Facet Length custom faceting options for the imported geometry.
                    """

                class _AutomaticObjectCreation(PyArgumentsTextualSubItem):
                    """
                    Determine whether or not mesh objects and labels are automatically created upon import, potentially and dramatically increasing the mesh import speed for very large cases. By default, this is set to yes however, if it is set to no, then no labels are created and a single mesh object is created employing all zones.
                    """

                class _MaxFacetLength(PyArgumentsNumericalSubItem):
                    """
                    Enables you to specify a maximum facet size for the imported model to avoid very large facets during the file import. Depending on the CAD geometry, this may yield more accuracy.
                    """

                class _ShowImportCadPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _MergeNodes(PyArgumentsTextualSubItem):
                    """
                    Argument MergeNodes.
                    """

                class _CISeparationAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the angle at which features will be extracted from the CAD model on import. Assigning a smaller separation angle will produce more zones.
                    """

                class _CITolerence(PyArgumentsNumericalSubItem):
                    """
                    Specify the level of facet refinement during import. A value approximately 1/10 of the intended minimum size is recommended. Using a value of 0 results in the coarsest possible faceting.
                    """

            class _FileName(PyArgumentsTextualSubItem):
                """
                Select a CAD file to import into your simulation. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files).
                """

            class _FileNames(PyArgumentsTextualSubItem):
                """
                Select multiple CAD files to import into your simulation. When importing multiple files, use the browse button (...) to open the Select File dialog that allows you to make multiple selections, as long as the files are in the same directory and are of the same CAD format. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files).
                """

            class _MeshFileName(PyArgumentsTextualSubItem):
                """
                Select a CAD file to import into your simulation. Supported file types are SpaceClaim (.scdoc) and Workbench (.agdb) files and also .pmdb files. Other supported formats include: \\*.CATpart, \\*.prt, \\*.x_t, \\*.sat, \\*.step, and \\*.iges files).
                """

            class _NumParts(PyArgumentsNumericalSubItem):
                """
                Argument NumParts.
                """

            class _AppendMesh(PyArgumentsParameterSubItem):
                """
                Argument AppendMesh.
                """

            class _Directory(PyArgumentsTextualSubItem):
                """
                Argument Directory.
                """

            class _Pattern(PyArgumentsTextualSubItem):
                """
                Argument Pattern.
                """

            class _CadImportOptions(PyArgumentsSingletonSubItem):
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
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)
                    self.ExtractFeatures = self._ExtractFeatures(self, "ExtractFeatures", service, rules, path)
                    self.ImportPartNames = self._ImportPartNames(self, "ImportPartNames", service, rules, path)
                    self.UsePartOrBodyAsSuffix = self._UsePartOrBodyAsSuffix(self, "UsePartOrBodyAsSuffix", service, rules, path)

                class _SavePMDBIntermediateFile(PyArgumentsParameterSubItem):
                    """
                    Argument SavePMDBIntermediateFile.
                    """

                class _OneObjectPer(PyArgumentsTextualSubItem):
                    """
                    Argument OneObjectPer.
                    """

                class _OpenAllCadInSubdirectories(PyArgumentsParameterSubItem):
                    """
                    Argument OpenAllCadInSubdirectories.
                    """

                class _CreateCADAssemblies(PyArgumentsParameterSubItem):
                    """
                    Argument CreateCADAssemblies.
                    """

                class _FeatureAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument FeatureAngle.
                    """

                class _OneZonePer(PyArgumentsTextualSubItem):
                    """
                    Argument OneZonePer.
                    """

                class _ImportCurvatureDataFromCAD(PyArgumentsParameterSubItem):
                    """
                    Argument ImportCurvatureDataFromCAD.
                    """

                class _ImportNamedSelections(PyArgumentsParameterSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

                class _ExtractFeatures(PyArgumentsParameterSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _ImportPartNames(PyArgumentsParameterSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _UsePartOrBodyAsSuffix(PyArgumentsParameterSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
                    """

        def create_instance(self) -> _ImportGeometryArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImportGeometryArguments(*args)

    class ImproveSurfaceMesh(PyCommand):
        """
        Perform immediate improvements to the quality of the existing surface mesh by adjusting various parameters such as the face quality limit, as well as maximum angle and face skewness.  More...
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
        class _ImproveSurfaceMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshObject = self._MeshObject(self, "MeshObject", service, rules, path)
                self.FaceQualityLimit = self._FaceQualityLimit(self, "FaceQualityLimit", service, rules, path)
                self.SQMinSize = self._SQMinSize(self, "SQMinSize", service, rules, path)
                self.ScopeImproveTo = self._ScopeImproveTo(self, "ScopeImproveTo", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _FaceQualityLimit(PyArgumentsNumericalSubItem):
                """
                Use the specified value to improve the surface mesh. Note that this control can aggressively change your surface mesh when applied.
                """

            class _SQMinSize(PyArgumentsNumericalSubItem):
                """
                Argument SQMinSize.
                """

            class _ScopeImproveTo(PyArgumentsTextualSubItem):
                """
                Argument ScopeImproveTo.
                """

            class _SMImprovePreferences(PyArgumentsSingletonSubItem):
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

                class _SIStepQualityLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify the limiting skewness quality for the step(s) to be removed.
                    """

                class _SIQualityCollapseLimit(PyArgumentsNumericalSubItem):
                    """
                    Specify the limiting skewness value for cell collapse to improve the mesh. The default value changes automatically when you change the Face Quality Limit.
                    """

                class _SIQualityIterations(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of iterations that will be performed to improve the mesh.
                    """

                class _SIQualityMaxAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum angle between the normals of adjacent faces during mesh improvement. This quality measure is useful in locating sharp corners in complicated geometries. The angle value ranges from 0-180 degrees.
                    """

                class _AllowDefeaturing(PyArgumentsTextualSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _ShowSMImprovePreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _AdvancedImprove(PyArgumentsTextualSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _SIStepWidth(PyArgumentsNumericalSubItem):
                    """
                    Specify the width of the step that you wish to remove.
                    """

                class _SIRemoveStep(PyArgumentsTextualSubItem):
                    """
                    Indicate if there are any small imperfections (ledge or step artifacts from the original CAD geometry) that can be removed as part of this task. If you select yes, then you must specify a Max Step Width and the Step Skewness Quality Limit.
                    """

        def create_instance(self) -> _ImproveSurfaceMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImproveSurfaceMeshArguments(*args)

    class ImproveVolumeMesh(PyCommand):
        """
        Perform immediate improvements to the quality of the existing volume mesh by adjusting various parameters such as the cell quality limit, as well as minimum angle and the ability to ignore problematic features.  More...
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
        class _ImproveVolumeMeshArguments(PyArguments):
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

            class _QualityMethod(PyArgumentsTextualSubItem):
                """
                Choose from several different types of mesh quality controls (skewness, aspect ratio, change in size, and so on). Choices include Orthogonal (the default for the workflows), Enhanced Orthogonal, and Skewness. For more information, see  More... .
                """

            class _CellQualityLimit(PyArgumentsNumericalSubItem):
                """
                Use the specified value to improve the volume mesh. Note that this control can aggressively change your volume mesh when applied.
                """

            class _AddMultipleQualityMethods(PyArgumentsTextualSubItem):
                """
                Use this option to specify quality criteria for multiple quality methods.
                """

            class _QualityMethodList(PyArgumentsTextualSubItem):
                """
                Argument QualityMethodList.
                """

            class _QualityCriteriaList(PyArgumentsTextualSubItem):
                """
                Argument QualityCriteriaList.
                """

            class _OldQualityMethodList(PyArgumentsTextualSubItem):
                """
                Argument OldQualityMethodList.
                """

            class _OldQualityCriteriaList(PyArgumentsTextualSubItem):
                """
                Argument OldQualityCriteriaList.
                """

            class _VMImprovePreferences(PyArgumentsSingletonSubItem):
                """
                Argument VMImprovePreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.VIgnoreFeature = self._VIgnoreFeature(self, "VIgnoreFeature", service, rules, path)
                    self.ShowVMImprovePreferences = self._ShowVMImprovePreferences(self, "ShowVMImprovePreferences", service, rules, path)
                    self.VIQualityIterations = self._VIQualityIterations(self, "VIQualityIterations", service, rules, path)
                    self.VIQualityMinAngle = self._VIQualityMinAngle(self, "VIQualityMinAngle", service, rules, path)

                class _VIgnoreFeature(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to ignore geometric features that are related to any remaining problematic cells in the volume mesh.
                    """

                class _ShowVMImprovePreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _VIQualityIterations(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of iterations that will be performed to improve the mesh.
                    """

                class _VIQualityMinAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum angle between the normals of adjacent faces during mesh improvement. This quality measure is useful in locating sharp corners in complicated geometries. The angle value ranges from 0 to 180 degrees.
                    """

        def create_instance(self) -> _ImproveVolumeMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ImproveVolumeMeshArguments(*args)

    class LinearMeshPattern(PyCommand):
        """
        Create linear patterns of objects based on one or more CAD parts, greatly simplifying meshing for CAD geometries that require multiple, linearly spaced parts such as in modeling batteries.   More...
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
        class _LinearMeshPatternArguments(PyArguments):
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

            class _ChildName(PyArgumentsTextualSubItem):
                """
                Specify a name for the mesh pattern or use the default value.
                """

            class _ObjectList(PyArgumentsTextualSubItem):
                """
                Select one or more parts from the list below that you want to use for creating the mesh pattern. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _AutoPopulateVector(PyArgumentsTextualSubItem):
                """
                Indicate whether or not you want Fluent to approximate both the axes orientation and the pitch value, or whether you want to estimate the Pitch Only (default). This estimation only takes place once, either when the object is selected, or when the option is changed.
                """

            class _PatternVector(PyArgumentsSingletonSubItem):
                """
                Specify a name for the mesh pattern or use the default value.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.Z = self._Z(self, "Z", service, rules, path)
                    self.Y = self._Y(self, "Y", service, rules, path)

                class _X(PyArgumentsNumericalSubItem):
                    """
                    Specify the X component of the axis orientation/direction.
                    """

                class _Z(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z component of the axis orientation/direction.
                    """

                class _Y(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y component of the axis orientation/direction.
                    """

            class _Pitch(PyArgumentsNumericalSubItem):
                """
                Specify a value for the pitch, or displacement factor, or use the default value.
                """

            class _NumberOfUnits(PyArgumentsNumericalSubItem):
                """
                Indicate the overall number of units that the pattern will use.
                """

            class _CheckOverlappingFaces(PyArgumentsTextualSubItem):
                """
                Graphically highlights the mesh pattern units so that you can visualize them and make sure they are properly aligned. Misaligned units can cause a failure in the share topology of the battery cells.
                """

            class _BatteryModelingOptions(PyArgumentsSingletonSubItem):
                """
                Argument BatteryModelingOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.FirstNumber = self._FirstNumber(self, "FirstNumber", service, rules, path)
                    self.NbCellsPerUnit = self._NbCellsPerUnit(self, "NbCellsPerUnit", service, rules, path)
                    self.CustomPatternString = self._CustomPatternString(self, "CustomPatternString", service, rules, path)
                    self.InvokeBatteryModelingOptions = self._InvokeBatteryModelingOptions(self, "InvokeBatteryModelingOptions", service, rules, path)
                    self.UseCustomPattern = self._UseCustomPattern(self, "UseCustomPattern", service, rules, path)

                class _FirstNumber(PyArgumentsNumericalSubItem):
                    """
                    Specify the numerical value that will be appended to the name of the first unit associated with the meshing pattern object. This value also dictates the labeling for mesh objects associated with this mesh pattern.  More...
                    """

                class _NbCellsPerUnit(PyArgumentsNumericalSubItem):
                    """
                    Specify the numerical value that will be appended to the name of the first unit associated with the meshing pattern object. This value also dictates the labeling for mesh objects associated with this mesh pattern.   More...
                    """

                class _CustomPatternString(PyArgumentsTextualSubItem):
                    """
                    Argument CustomPatternString.
                    """

                class _InvokeBatteryModelingOptions(PyArgumentsTextualSubItem):
                    """
                    Specify whether or not you are interested in creating a pattern based on custom numbering/labeling and setting dual unit labeling options (often useful in battery modeling).   More...
                    """

                class _UseCustomPattern(PyArgumentsTextualSubItem):
                    """
                    Indicate whether or not you want to create a customized pattern based on your own specifications. Enter the pattern specification in the field below.  More...
                    """

        def create_instance(self) -> _LinearMeshPatternArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LinearMeshPatternArguments(*args)

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
        class _LoadCADGeometryArguments(PyArguments):
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

            class _FileName(PyArgumentsTextualSubItem):
                """
                Argument FileName.
                """

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Argument LengthUnit.
                """

            class _Route(PyArgumentsTextualSubItem):
                """
                Argument Route.
                """

            class _UsePrimeGeometryKernel(PyArgumentsParameterSubItem):
                """
                Argument UsePrimeGeometryKernel.
                """

            class _FacetingTolerance(PyArgumentsNumericalSubItem):
                """
                Argument FacetingTolerance.
                """

            class _CreateObjectPer(PyArgumentsTextualSubItem):
                """
                Argument CreateObjectPer.
                """

            class _NumParts(PyArgumentsNumericalSubItem):
                """
                Argument NumParts.
                """

            class _Refaceting(PyArgumentsSingletonSubItem):
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

                class _FacetMaxEdgeLength(PyArgumentsTextualSubItem):
                    """
                    Argument FacetMaxEdgeLength.
                    """

                class _FacetResolution(PyArgumentsTextualSubItem):
                    """
                    Argument FacetResolution.
                    """

                class _Deviation(PyArgumentsNumericalSubItem):
                    """
                    Argument Deviation.
                    """

                class _MaxEdgeLengthFactor(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxEdgeLengthFactor.
                    """

                class _NormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument NormalAngle.
                    """

                class _MaxEdgeLength(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxEdgeLength.
                    """

                class _CustomNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument CustomNormalAngle.
                    """

                class _CustomDeviation(PyArgumentsNumericalSubItem):
                    """
                    Argument CustomDeviation.
                    """

                class _Refacet(PyArgumentsParameterSubItem):
                    """
                    Argument Refacet.
                    """

        def create_instance(self) -> _LoadCADGeometryArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LoadCADGeometryArguments(*args)

    class LocalScopedSizingForPartReplacement(PyCommand):
        """
        Create individual sizing controls for your mesh. For every size control that you create, it is added to the workflow as a subtask. More...
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
            Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteLabelSelectionList : list[str]
        CompleteObjectSelectionList : list[str]
            Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        CompleteEdgeSelectionList : list[str]
            Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...

        Returns
        -------
        bool
        """
        class _LocalScopedSizingForPartReplacementArguments(PyArguments):
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

            class _LocalSettingsName(PyArgumentsTextualSubItem):
                """
                Specify a name for the size control or use the default value.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by object or by zone).
                """

            class _ObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LabelSelectionList(PyArgumentsTextualSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _EdgeSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LocalSizeControlParameters(PyArgumentsSingletonSubItem):
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
                    self.WrapGrowthRate = self._WrapGrowthRate(self, "WrapGrowthRate", service, rules, path)
                    self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.WrapCurvatureNormalAngle = self._WrapCurvatureNormalAngle(self, "WrapCurvatureNormalAngle", service, rules, path)
                    self.TargetSizeControl = self._TargetSizeControl(self, "TargetSizeControl", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum size of the elements for the surface mesh.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Set proximity based refinement. The edges option considers edge-to-edge proximity, while faces considers face-to-face proximity, and faces and edges considers both. Note that when you use the faces and edges option, you can only select objects.
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
                    """

                class _IgnoreSelf(PyArgumentsParameterSubItem):
                    """
                    Select this option to ignore the proximity computation between facets within a face zone, and avoid over-refinement.
                    """

                class _WrapMin(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the minimum wrapping size for the size control. It will wrap with this minimum size and later coarsen through remeshing to the given target size. One of the advantages of the wrapper is that it can automatically de-feature unnecessary small details. The wrap size is used to wrap the geometry and target size is used to remesh. Feature capturing highly depends on the value of the wrap size. The default wrap size is 1/1.5 times smaller than the target size, and you can change the value.
                    """

                class _WrapCellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum size of the elements for the surface mesh.
                    """

                class _WrapMax(PyArgumentsNumericalSubItem):
                    """
                    Specify a value for the maximum wrapping size for the size control. It will wrap with this maximum size and later coarsen through remeshing to the given target size.
                    """

                class _AdvancedOptions(PyArgumentsParameterSubItem):
                    """
                    Display advanced wrap-specific options that are also applied to the task. See this description  for more information about wrap (and target) mesh size controls.
                    """

                class _InitialSizeControl(PyArgumentsParameterSubItem):
                    """
                    Enable this field to display the initial size control in the graphics window.
                    """

                class _WrapGrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the increase in element edge length with each succeeding layer of elements.
                    """

                class _SizingType(PyArgumentsTextualSubItem):
                    """
                    Choose the type of sizing control (curvature, proximity, soft, or boi).
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum number of layers of elements to be generated in the gaps. The number of cells per gap can be a real value, with a minimum value of 0.01.
                    """

                class _WrapCurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum allowable angle (from 0 to 180 degrees) that one element edge is allowed to span given a particular geometry curvature. You can use this field to limit the number of elements that are generated along a curve or surface if the minimum size is too small for that particular curve.
                    """

                class _TargetSizeControl(PyArgumentsParameterSubItem):
                    """
                    Enable this field to display the target size control in the graphics window.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Specify the increase in element edge length with each succeeding layer of elements.
                    """

            class _ValueChanged(PyArgumentsTextualSubItem):
                """
                Argument ValueChanged.
                """

            class _CompleteZoneSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more face zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteLabelSelectionList(PyArgumentsTextualSubItem):
                """
                Argument CompleteLabelSelectionList.
                """

            class _CompleteObjectSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more objects from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _CompleteEdgeSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more edge zones from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _LocalScopedSizingForPartReplacementArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._LocalScopedSizingForPartReplacementArguments(*args)

    class ManageZones(PyCommand):
        """
        Use this task to perform common operations on cell zones or face zones, Prior to generating the volume mesh, you can perform operations such as separating zones, splitting cylindrical regions, or extracting edges. After generating your volume mesh, you can perform operations such as renaming, changing prefixes, and merging zones. Especially useful for complex models with numerous zones.  More...
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
        TopologyList : list[str]
        ManageFaceZoneList : list[str]
            Choose from the list of face zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ManageCellZoneList : list[str]
            Choose from the list of cell zones, or enter a text string to filter out the list of cell zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        BodyLabelList : list[str]
            Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
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
            Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using *, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or * in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
        ZoneLocation : list[str]

        Returns
        -------
        bool
        """
        class _ManageZonesArguments(PyArguments):
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
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
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

            class _Type(PyArgumentsTextualSubItem):
                """
                Indicate whether you are going to operate on Cell Zones or Face Zones. If your imported CAD geometry contains bodies with multiple body labels, you can also choose Body Labels.
                """

            class _ZoneFilter(PyArgumentsTextualSubItem):
                """
                Choose the type of zone. For cell zones, choose from Fluid, Solid, or All. For face zones, choose from Internal, Fluid-Fluid, Solid-Fluid, Fluid-Solid, External-Solid, External-Fluid, or External.
                """

            class _SizeFilter(PyArgumentsTextualSubItem):
                """
                Indicate how you would like to filter the list of zones: All, Less than, More than, or Equal to the indicated value for the Volume (cell zone) or Area (face zone).
                """

            class _Area(PyArgumentsNumericalSubItem):
                """
                Argument Area.
                """

            class _Volume(PyArgumentsNumericalSubItem):
                """
                Argument Volume.
                """

            class _EqualRange(PyArgumentsNumericalSubItem):
                """
                Specify a percentage range to maintain equivalency for the cell zone volume value or the face zone area value.
                """

            class _ZoneOrLabel(PyArgumentsTextualSubItem):
                """
                Choose how you want to make your selection (by label or zone name).
                """

            class _LabelList(PyArgumentsTextualSubItem):
                """
                Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _ManageFaceZoneList(PyArgumentsTextualSubItem):
                """
                Choose from the list of face zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ManageCellZoneList(PyArgumentsTextualSubItem):
                """
                Choose from the list of cell zones, or enter a text string to filter out the list of cell zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _BodyLabelList(PyArgumentsTextualSubItem):
                """
                Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _Operation(PyArgumentsTextualSubItem):
                """
                Indicate the operation you wish to perform on the zones. When the task is located prior volume meshing: Separate Zones, Split Cylinders, Split normal to X, Split normal to Y, Split normal to Z, or Extract Edges. When the task is located after volume meshing: Change prefix, Rename, Merge, or Separate Zones. If your imported CAD geometry contains bodies with multiple body labels, you can also choose Merge cells within each body label
                """

            class _OperationName(PyArgumentsTextualSubItem):
                """
                The text string to be applied to this zone operation.
                """

            class _MZChildName(PyArgumentsTextualSubItem):
                """
                Specify a name for the managed zone control or use the default value.
                """

            class _AddPrefixName(PyArgumentsTextualSubItem):
                """
                The text string to be applied to this zone operation.
                """

            class _FaceMerge(PyArgumentsTextualSubItem):
                """
                Indicate whether or not you want to merge faces as part of the zone operation.
                """

            class _Angle(PyArgumentsNumericalSubItem):
                """
                Specify a value for the separation angle for determining separation. Assigning a smaller separation angle will produce more zones.
                """

            class _ZoneList(PyArgumentsTextualSubItem):
                """
                Argument ZoneList.
                """

            class _CompleteZoneList(PyArgumentsTextualSubItem):
                """
                Argument CompleteZoneList.
                """

            class _CompleteLabelList(PyArgumentsTextualSubItem):
                """
                Choose from the list of labels, or enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

        def create_instance(self) -> _ManageZonesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ManageZonesArguments(*args)

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
        class _MeshFluidDomainArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MeshFluidDomainOption = self._MeshFluidDomainOption(self, "MeshFluidDomainOption", service, rules, path)

            class _MeshFluidDomainOption(PyArgumentsParameterSubItem):
                """
                Argument MeshFluidDomainOption.
                """

        def create_instance(self) -> _MeshFluidDomainArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._MeshFluidDomainArguments(*args)

    class ModifyMeshRefinement(PyCommand):
        """
        Perform individual modifications to the surface mesh by creating mesh refinement objects and sequences. Assign a name, a remeshing sequence if desired, along with local sizing parameters. Create as many refinement controls as needed in order to modify the surface mesh to your needs. Choose any advanced options that you want to take effect upon updating the task.  More...
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
        class _ModifyMeshRefinementArguments(PyArguments):
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

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _RemeshExecution(PyArgumentsTextualSubItem):
                """
                Specify whether to just add the current size control to the workflow, or to add the size control and perform a remeshing operation immediately thereafter.
                """

            class _RemeshControlName(PyArgumentsTextualSubItem):
                """
                Provide a name for this specific size control.
                """

            class _LocalSize(PyArgumentsNumericalSubItem):
                """
                Specify a value for the local sizing parameter to be applied to the indicated zone.
                """

            class _FaceZoneOrLabel(PyArgumentsTextualSubItem):
                """
                Specify whether the size control is to be applied to an indicated zone or a label.
                """

            class _RemeshFaceZoneList(PyArgumentsTextualSubItem):
                """
                Choose from the list of zones, or enter a text string to filter out the list of face zones. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _RemeshFaceLabelList(PyArgumentsTextualSubItem):
                """
                Choose from the list of zone labels, or enter a text string to filter out the list of face zone labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _SizingType(PyArgumentsTextualSubItem):
                """
                Argument SizingType.
                """

            class _LocalMinSize(PyArgumentsNumericalSubItem):
                """
                Argument LocalMinSize.
                """

            class _LocalMaxSize(PyArgumentsNumericalSubItem):
                """
                Argument LocalMaxSize.
                """

            class _RemeshGrowthRate(PyArgumentsNumericalSubItem):
                """
                Argument RemeshGrowthRate.
                """

            class _RemeshCurvatureNormalAngle(PyArgumentsNumericalSubItem):
                """
                Argument RemeshCurvatureNormalAngle.
                """

            class _RemeshCellsPerGap(PyArgumentsNumericalSubItem):
                """
                Argument RemeshCellsPerGap.
                """

            class _CFDSurfaceMeshControls(PyArgumentsSingletonSubItem):
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
                    self.SurfaceMeshMethod = self._SurfaceMeshMethod(self, "SurfaceMeshMethod", service, rules, path)
                    self.SizeFieldFile = self._SizeFieldFile(self, "SizeFieldFile", service, rules, path)
                    self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                    self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                    self.SizeControlFile = self._SizeControlFile(self, "SizeControlFile", service, rules, path)
                    self.RemeshImportedMesh = self._RemeshImportedMesh(self, "RemeshImportedMesh", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.ObjectBasedControls = self._ObjectBasedControls(self, "ObjectBasedControls", service, rules, path)

                class _SaveSizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SaveSizeFieldFile.
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MaxSize.
                    """

                class _ScopeProximityTo(PyArgumentsTextualSubItem):
                    """
                    Argument ScopeProximityTo.
                    """

                class _PreviewSizefield(PyArgumentsParameterSubItem):
                    """
                    Argument PreviewSizefield.
                    """

                class _CurvatureNormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument CurvatureNormalAngle.
                    """

                class _SaveSizeField(PyArgumentsParameterSubItem):
                    """
                    Argument SaveSizeField.
                    """

                class _UseSizeFiles(PyArgumentsTextualSubItem):
                    """
                    Argument UseSizeFiles.
                    """

                class _AutoCreateScopedSizing(PyArgumentsParameterSubItem):
                    """
                    Argument AutoCreateScopedSizing.
                    """

                class _MinSize(PyArgumentsNumericalSubItem):
                    """
                    Argument MinSize.
                    """

                class _SizeFunctions(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFunctions.
                    """

                class _SurfaceMeshMethod(PyArgumentsTextualSubItem):
                    """
                    Argument SurfaceMeshMethod.
                    """

                class _SizeFieldFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeFieldFile.
                    """

                class _DrawSizeControl(PyArgumentsParameterSubItem):
                    """
                    Enable this field to display the size boxes in the graphics window.
                    """

                class _CellsPerGap(PyArgumentsNumericalSubItem):
                    """
                    Argument CellsPerGap.
                    """

                class _SizeControlFile(PyArgumentsTextualSubItem):
                    """
                    Argument SizeControlFile.
                    """

                class _RemeshImportedMesh(PyArgumentsTextualSubItem):
                    """
                    Argument RemeshImportedMesh.
                    """

                class _GrowthRate(PyArgumentsNumericalSubItem):
                    """
                    Argument GrowthRate.
                    """

                class _ObjectBasedControls(PyArgumentsTextualSubItem):
                    """
                    Argument ObjectBasedControls.
                    """

            class _RemeshPreferences(PyArgumentsSingletonSubItem):
                """
                Argument RemeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.RMCornerAngle = self._RMCornerAngle(self, "RMCornerAngle", service, rules, path)
                    self.RMFeatureMinAngle = self._RMFeatureMinAngle(self, "RMFeatureMinAngle", service, rules, path)
                    self.RMFeatureMaxAngle = self._RMFeatureMaxAngle(self, "RMFeatureMaxAngle", service, rules, path)
                    self.ShowRemeshPreferences = self._ShowRemeshPreferences(self, "ShowRemeshPreferences", service, rules, path)

                class _RMCornerAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the corner angle for remeshing.
                    """

                class _RMFeatureMinAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the minimum angle for which features will be preserved upon remeshing.
                    """

                class _RMFeatureMaxAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the maximum angle for which features will be preserved upon remeshing.
                    """

                class _ShowRemeshPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

        def create_instance(self) -> _ModifyMeshRefinementArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ModifyMeshRefinementArguments(*args)

    class PartManagement(PyCommand):
        """
        Import a CAD geometry (.fmd or .stl), then determine how you want to create your meshing objects: by Part (simple, a mesh object will be created for each of the CAD part), or by Custom where you customize the import process (for complicated, multiple part assemblies, etc.). For a customized approach, you can pick and choose the portions of the CAD model that you want to add to your simulation, and adjust any meshing-related settings for individual objects, before converting them into meshing objects. You can further simplify your CAD model and combine parts and assemblies into a single object. To capture features more effectively, you can increase or decrease the faceting resolution, thereby controlling the surface mesh granularity and therefore influencing the simulation time. More...
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
            Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
        Route : str
            Provides the recommended route in order to import and load the specified CAD file into this task. The default settings are recommended in most cases.  More...
        RouteAppend : str
            Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
        JtLOD : str
            Specify the level of detail that you want to include for this .jt file before loading the CAD file.
        JtLODAppend : str
            Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
        PartPerBody : bool
            Enable this option to make all bodies available as individual parts in the CAD Model tree once the CAD file is loaded into the task.
        PrefixParentName : bool
            This applies the name of the component (or assembly) as a prefix to the individual part names when the geometry is loaded into the task.
        RemoveEmptyParts : bool
            Enabled by default, this option lets you import your CAD geometry while removing any empty components.
        FeatureAngle : float
            Specify a rotational angle (in degrees) of transformation.
        OneZonePer : str
            Specify whether to create your meshing zones based on an object, part, body or face. For instance, choosing the face option would create a separate zone for every topological face.
        Refaceting : dict[str, Any]
        IgnoreSolidNames : bool
            Enable this option to import your CAD geometry while ignoring the names assigned to solids. Note that binary STL files contain a single solid and may have an associated solid name, whereas ASCII STL files contain one or more solids and each can have a  solid name. This option allows to control whether or not to use the name contained in the STL file for naming mesh objects and components.
        IgnoreSolidNamesAppend : bool
            Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
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
        class _PartManagementArguments(PyArguments):
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

            class _FileLoaded(PyArgumentsTextualSubItem):
                """
                Argument FileLoaded.
                """

            class _FMDFileName(PyArgumentsTextualSubItem):
                """
                Select a CAD file to import into your simulation. Standard Ansys file types, among others, are supported, including .scdoc, .dsco, .agdb, .fmd, .fmdb, .fmd, .pmdb, .tgf, and .msh. To quickly import multiple CAD files, you can use basic wildcard expression patterns such as the \\* or ? wildcards. More...
                """

            class _AppendFileName(PyArgumentsTextualSubItem):
                """
                Enable this option and browse/select another CAD file to append to your original geometry. Specify additional CAD files in the Append File field, and use the Append button to load additional CAD files into the tree, after the original CAD objects. To quickly append multiple CAD files, you can use basic wildcard expression patterns such as the \\* or ? wildcards.
                """

            class _Append(PyArgumentsParameterSubItem):
                """
                Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
                """

            class _LengthUnit(PyArgumentsTextualSubItem):
                """
                Select a suitable unit for display in the graphics window.
                """

            class _CreateObjectPer(PyArgumentsTextualSubItem):
                """
                Choose whether to create meshing objects by part, or by selectively customizing the portions of the imported CAD geometry to mesh. If you select by part, then meshing objects are automatically created for you once you import the geometry. Refaceting options are available as well for all meshing objects.
                """

            class _FileLengthUnit(PyArgumentsTextualSubItem):
                """
                Specify the units of length used by this .stl file before loading the CAD file.
                """

            class _FileLengthUnitAppend(PyArgumentsTextualSubItem):
                """
                Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
                """

            class _Route(PyArgumentsTextualSubItem):
                """
                Provides the recommended route in order to import and load the specified CAD file into this task. The default settings are recommended in most cases.  More...
                """

            class _RouteAppend(PyArgumentsTextualSubItem):
                """
                Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
                """

            class _JtLOD(PyArgumentsTextualSubItem):
                """
                Specify the level of detail that you want to include for this .jt file before loading the CAD file.
                """

            class _JtLODAppend(PyArgumentsTextualSubItem):
                """
                Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
                """

            class _PartPerBody(PyArgumentsParameterSubItem):
                """
                Enable this option to make all bodies available as individual parts in the CAD Model tree once the CAD file is loaded into the task.
                """

            class _PrefixParentName(PyArgumentsParameterSubItem):
                """
                This applies the name of the component (or assembly) as a prefix to the individual part names when the geometry is loaded into the task.
                """

            class _RemoveEmptyParts(PyArgumentsParameterSubItem):
                """
                Enabled by default, this option lets you import your CAD geometry while removing any empty components.
                """

            class _FeatureAngle(PyArgumentsNumericalSubItem):
                """
                Specify a rotational angle (in degrees) of transformation.
                """

            class _OneZonePer(PyArgumentsTextualSubItem):
                """
                Specify whether to create your meshing zones based on an object, part, body or face. For instance, choosing the face option would create a separate zone for every topological face.
                """

            class _Refaceting(PyArgumentsSingletonSubItem):
                """
                Argument Refaceting.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.FacetMaxEdgeLength = self._FacetMaxEdgeLength(self, "FacetMaxEdgeLength", service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Refacet = self._Refacet(self, "Refacet", service, rules, path)
                    self.MaxEdgeLengthFactor = self._MaxEdgeLengthFactor(self, "MaxEdgeLengthFactor", service, rules, path)

                class _FacetMaxEdgeLength(PyArgumentsTextualSubItem):
                    """
                    Controls the edge size of facets, ensuring that no facet edge exceeds the specified length. The max edge length size (Max Size) can either be specified directly by selecting Absolute or specified as a factor (Max Edge Length Factor) relative to the bounding box of the geometry by selecting Relative (Bounding Box).
                    """

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify a maximum element size for the imported model to avoid very large facets during the file import.
                    """

                class _Deviation(PyArgumentsNumericalSubItem):
                    """
                    Specify the distance between facet edges and the geometry edges. Decreasing this value will result in more facets along curved edges.
                    """

                class _NormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify a rotational angle (in degrees) of transformation.
                    """

                class _Refacet(PyArgumentsParameterSubItem):
                    """
                    Select this option when you want to change faceting of the selected object. Refaceting will refacet the original CAD geometry. Only the faceted CAD geometry is used during the meshing process. The refaceting settings control how far the facet edges are from the model and the size of the facets.  More...
                    """

                class _MaxEdgeLengthFactor(PyArgumentsNumericalSubItem):
                    """
                    Specifies the maximum size of the facets relative to the bounding box of the geometry.
                    """

            class _IgnoreSolidNames(PyArgumentsParameterSubItem):
                """
                Enable this option to import your CAD geometry while ignoring the names assigned to solids. Note that binary STL files contain a single solid and may have an associated solid name, whereas ASCII STL files contain one or more solids and each can have a  solid name. This option allows to control whether or not to use the name contained in the STL file for naming mesh objects and components.
                """

            class _IgnoreSolidNamesAppend(PyArgumentsParameterSubItem):
                """
                Enable this field and browse and select additional CAD files. Use the Append button to add the additional CAD components to the bottom of the CAD Model tree upon loading.
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
                    Enable this option to import solid bodies along with your CAD geometry.
                    """

                class _Line(PyArgumentsParameterSubItem):
                    """
                    Enable this option to import line bodies along with your CAD geometry.
                    """

                class _Surface(PyArgumentsParameterSubItem):
                    """
                    Enable this option to import surface bodies along with your CAD geometry.
                    """

            class _EdgeExtraction(PyArgumentsTextualSubItem):
                """
                Choose how edges will be extracted from the CAD geometry. Setting this option to auto will extract edges from the CAD geometry when the number of meshing objects is less than 10,000. If this limit is exceeded, then no edges are extracted. When this option is set to yes, then edges are extracted regardless of the number of meshing objects. No edges are extracted when this option is set to no.
                """

            class _Context(PyArgumentsNumericalSubItem):
                """
                Argument Context.
                """

            class _ObjectSetting(PyArgumentsTextualSubItem):
                """
                Argument ObjectSetting.
                """

            class _RefacetOptions(PyArgumentsSingletonSubItem):
                """
                Argument RefacetOptions.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.RefacetDuringLoad = self._RefacetDuringLoad(self, "RefacetDuringLoad", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)

                class _MaxSize(PyArgumentsNumericalSubItem):
                    """
                    Specify a maximum element size for the imported model to avoid very large facets during the file import.
                    """

                class _RefacetDuringLoad(PyArgumentsParameterSubItem):
                    """
                    This option is available when DSCO is selected for the Import Route. When enabled, this option will refacet the geometry as it is converted to a .fmd file. This option eliminates the need for any refaceting operation after the geometry is loaded, which can be expensive.
                    """

                class _NormalAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify a rotational angle (in degrees) of transformation.
                    """

                class _Deviation(PyArgumentsNumericalSubItem):
                    """
                    Specify the distance between facet edges and the geometry edges. Decreasing this value will result in more facets along curved edges.
                    """

        def create_instance(self) -> _PartManagementArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._PartManagementArguments(*args)

    class PartReplacementSettings(PyCommand):
        """
        Use this task to define particular details for the part replacement operation where you can choose to add, remove, or replace one or more portions of your original imported geometry.
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
        class _PartReplacementSettingsArguments(PyArguments):
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

            class _PartReplacementName(PyArgumentsTextualSubItem):
                """
                Enter a name for the part replacement object, or keep the default value.
                """

            class _ManagementMethod(PyArgumentsTextualSubItem):
                """
                Choose whether the part replacement operation will be an Addition, Replacement, or Removal of a part.
                """

            class _CreationMethod(PyArgumentsTextualSubItem):
                """
                Choose the approach for handling meshing for the part replacement task: Surface Mesh Based or Volume Mesh Based. The volume mesh based approach defines a separate region for the area of interest surrounding the part replacement. Volume meshing is performed only in this region and thus is much faster than generating the volume mesh in the entire domain.  The surface mesh approach requires the remeshing of all volume regions.
                """

            class _OldObjectSelectionList(PyArgumentsTextualSubItem):
                """
                For part replacement or removal, use this list to pick the original object(s) that you wish to replace or remove. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).
                """

            class _NewObjectSelectionList(PyArgumentsTextualSubItem):
                """
                For part replacement or addition, use this list to pick the new object(s) that you wish to replace or add. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).
                """

            class _AdvancedOptions(PyArgumentsParameterSubItem):
                """
                Display advanced options that you may want to apply to the task.
                """

            class _ScalingFactor(PyArgumentsNumericalSubItem):
                """
                Specify a factor to change the size of the bounding box surrounding the selected object(s) for part replacement.
                """

            class _MptMethodType(PyArgumentsTextualSubItem):
                """
                Choose how you are going to determine the location of the region around the replacement part - by using numerical inputs directly, or by using the region around the selected object(s).
                """

            class _GraphicalSelection(PyArgumentsParameterSubItem):
                """
                Use this option to have the numerical inputs be automatically filled out based on the centroid of the object(s) selected in the graphics window.
                """

            class _ShowCoordinates(PyArgumentsParameterSubItem):
                """
                Use this option to see the exact coordinate values of the current location point.
                """

            class _X(PyArgumentsNumericalSubItem):
                """
                Indicates the x-coordinate of the current point location.
                """

            class _Y(PyArgumentsNumericalSubItem):
                """
                Indicates the y-coordinate of the current point location.
                """

            class _Z(PyArgumentsNumericalSubItem):
                """
                Indicates the z-coordinate of the current point location.
                """

        def create_instance(self) -> _PartReplacementSettingsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._PartReplacementSettingsArguments(*args)

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
        class _RemeshSurfaceArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.RemeshSurfaceOption = self._RemeshSurfaceOption(self, "RemeshSurfaceOption", service, rules, path)

            class _RemeshSurfaceOption(PyArgumentsParameterSubItem):
                """
                Argument RemeshSurfaceOption.
                """

        def create_instance(self) -> _RemeshSurfaceArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._RemeshSurfaceArguments(*args)

    class RunCustomJournal(PyCommand):
        """
        Customize your workflow using journaling commands. Use a text editor to copy portions of any of your own journal files, and paste them into this task to perform additional meshing refinements.  More...
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
        class _RunCustomJournalArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.JournalString = self._JournalString(self, "JournalString", service, rules, path)
                self.PythonJournal = self._PythonJournal(self, "PythonJournal", service, rules, path)
                self.PrimeJournal = self._PrimeJournal(self, "PrimeJournal", service, rules, path)

            class _JournalString(PyArgumentsTextualSubItem):
                """
                Enter one or more journal commands.
                """

            class _PythonJournal(PyArgumentsParameterSubItem):
                """
                Argument PythonJournal.
                """

            class _PrimeJournal(PyArgumentsParameterSubItem):
                """
                Argument PrimeJournal.
                """

        def create_instance(self) -> _RunCustomJournalArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._RunCustomJournalArguments(*args)

    class SeparateContacts(PyCommand):
        """
        Enable or disable the ability to separate any existing contacts between surfaces.
        Parameters
        ----------
        SeparateContactsOption : bool
            Use this option to enable or disable the ability to separate any existing contacts between surfaces.

        Returns
        -------
        bool
        """
        class _SeparateContactsArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.SeparateContactsOption = self._SeparateContactsOption(self, "SeparateContactsOption", service, rules, path)

            class _SeparateContactsOption(PyArgumentsParameterSubItem):
                """
                Use this option to enable or disable the ability to separate any existing contacts between surfaces.
                """

        def create_instance(self) -> _SeparateContactsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SeparateContactsArguments(*args)

    class SetUpPeriodicBoundaries(PyCommand):
        """
        Define boundaries suited for rotational periodicity. The task will remesh a single periodic face to exactly match its reference side, as well as create the corresponding periodic and shadow boundary types for use in the Fluent solver.   More...
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
        class _SetUpPeriodicBoundariesArguments(PyArguments):
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

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _Type(PyArgumentsTextualSubItem):
                """
                Choose the type of periodicity: rotational or translational.
                """

            class _Method(PyArgumentsTextualSubItem):
                """
                Choose the method for how you are going to define the periodic boundary. Automatic requires you to select two zones or labels. Manual requires only one zone or label.
                """

            class _PeriodicityAngle(PyArgumentsNumericalSubItem):
                """
                Specify the angle at which periodicity occurs.
                """

            class _LCSOrigin(PyArgumentsSingletonSubItem):
                """
                The X, Y, and Z components of the origin point for the periodic boundary.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.OriginY = self._OriginY(self, "OriginY", service, rules, path)
                    self.OriginZ = self._OriginZ(self, "OriginZ", service, rules, path)
                    self.OriginX = self._OriginX(self, "OriginX", service, rules, path)

                class _OriginY(PyArgumentsNumericalSubItem):
                    """
                    The Y component of the origin point for the periodic boundary.
                    """

                class _OriginZ(PyArgumentsNumericalSubItem):
                    """
                    The Z component of the origin point for the periodic boundary.
                    """

                class _OriginX(PyArgumentsNumericalSubItem):
                    """
                    The X component of the origin point for the periodic boundary.
                    """

            class _LCSVector(PyArgumentsSingletonSubItem):
                """
                The X, Y, and Z components of the vector for the periodic boundary.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.VectorX = self._VectorX(self, "VectorX", service, rules, path)
                    self.VectorZ = self._VectorZ(self, "VectorZ", service, rules, path)
                    self.VectorY = self._VectorY(self, "VectorY", service, rules, path)

                class _VectorX(PyArgumentsNumericalSubItem):
                    """
                    The X component of the vector for the periodic boundary.
                    """

                class _VectorZ(PyArgumentsNumericalSubItem):
                    """
                    The Z component of the vector for the periodic boundary.
                    """

                class _VectorY(PyArgumentsNumericalSubItem):
                    """
                    The Y component of the vector for the periodic boundary.
                    """

            class _TransShift(PyArgumentsSingletonSubItem):
                """
                Argument TransShift.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShiftY = self._ShiftY(self, "ShiftY", service, rules, path)
                    self.ShiftZ = self._ShiftZ(self, "ShiftZ", service, rules, path)
                    self.ShiftX = self._ShiftX(self, "ShiftX", service, rules, path)

                class _ShiftY(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the translational shift.
                    """

                class _ShiftZ(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the translational shift.
                    """

                class _ShiftX(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the translational shift.
                    """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Specify whether the periodic boundary is to be applied to an indicated zone or a label.
                """

            class _ZoneList(PyArgumentsTextualSubItem):
                """
                Choose from the list of zones, or enter a text string to filter out the list of face zones. Provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).  More...
                """

            class _LabelList(PyArgumentsTextualSubItem):
                """
                Choose from the list of zone labels, or enter a text string to filter out the list of face zone labels. Provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []).  More...
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _RemeshBoundariesOption(PyArgumentsTextualSubItem):
                """
                Enable this option to remesh boundaries when there is an asymmetric mesh on the periodic faces.
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _ListAllLabelToggle(PyArgumentsParameterSubItem):
                """
                View more labels in the table, such as those for fluid-fluid internal boundaries, in addition to external boundaries.
                """

            class _AutoMultiplePeriodic(PyArgumentsTextualSubItem):
                """
                Argument AutoMultiplePeriodic.
                """

            class _MultipleOption(PyArgumentsTextualSubItem):
                """
                Argument MultipleOption.
                """

        def create_instance(self) -> _SetUpPeriodicBoundariesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SetUpPeriodicBoundariesArguments(*args)

    class SetupBoundaryLayers(PyCommand):
        """
        Improve how the boundary layer flow along the walls of the geometry is captured using specialized boundary layer elements within the volume mesh (also called prisms or inflation layers). You can use this task to assign different fluid regions to have their own boundary layer controls. For more layers (greater than 3), consider adding 1 layer and performing anisotropic adaption in the solver. More...
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
        class _SetupBoundaryLayersArguments(PyArguments):
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

            class _AddChild(PyArgumentsTextualSubItem):
                """
                Determine whether or not you want to better capture flow in and around the boundary layer of your fluid regions.
                """

            class _PrismsSettingsName(PyArgumentsTextualSubItem):
                """
                Specify a name for the boundary layer control or use the default value.
                """

            class _AspectRatio(PyArgumentsNumericalSubItem):
                """
                Specify the ratio of the prism base length to the prism layer height.
                """

            class _GrowthRate(PyArgumentsNumericalSubItem):
                """
                Specify the rate of growth of the boundary layer.
                """

            class _OffsetMethodType(PyArgumentsTextualSubItem):
                """
                Choose the method that will be used to create the boundary layer, or prism, controls.
                """

            class _LastRatioPercentage(PyArgumentsNumericalSubItem):
                """
                Specify the offset height of the last layer as a percentage of the local base mesh size.
                """

            class _FirstHeight(PyArgumentsNumericalSubItem):
                """
                Specify the height of the first layer of cells in the boundary layer.
                """

            class _PrismLayers(PyArgumentsNumericalSubItem):
                """
                Specify the number of cell layers you require along the boundary.
                """

            class _RegionSelectionList(PyArgumentsTextualSubItem):
                """
                Choose one or more regions from the list below. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

        def create_instance(self) -> _SetupBoundaryLayersArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SetupBoundaryLayersArguments(*args)

    class ShareTopology(PyCommand):
        """
        For imported CAD assemblies with multiple parts, use this task to identify and close any problematic gaps and choose whether to join and/or intersect the problematic faces.   More...
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
        class _ShareTopologyArguments(PyArguments):
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

            class _GapDistance(PyArgumentsNumericalSubItem):
                """
                Specify the maximum distance under which gaps will be removed. Use the Show Marked Gaps button to display such gaps.
                """

            class _GapDistanceConnect(PyArgumentsNumericalSubItem):
                """
                Specify the maximum distance under which gaps will be removed (the default value of 0 is recommended). Use the Show Marked Gaps button to display such gaps.
                """

            class _STMinSize(PyArgumentsNumericalSubItem):
                """
                Argument STMinSize.
                """

            class _InterfaceSelect(PyArgumentsTextualSubItem):
                """
                Choose whether to have the interface labels selected manually (Manual), automatically (Automatic), or when force share connect topology is utilized in the  geometry (Automatic - Using Connect Topology).
                """

            class _EdgeLabels(PyArgumentsTextualSubItem):
                """
                Argument EdgeLabels.
                """

            class _ShareTopologyPreferences(PyArgumentsSingletonSubItem):
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
                    self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                    self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                    self.Operation = self._Operation(self, "Operation", service, rules, path)
                    self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                    self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                    self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                    self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                    self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                    self.AdvancedImprove = self._AdvancedImprove(self, "AdvancedImprove", service, rules, path)
                    self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)

                class _STRenameInternals(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not to apply body names from the imported geometry and use them in naming internal boundaries.  For instance, the internal face between two regions solid and body would be renamed to solid-body.
                    """

                class _ModelIsPeriodic(PyArgumentsTextualSubItem):
                    """
                    Choose whether or not you need to set up periodic boundaries. If you select yes, then choose your periodic boundaries from the list of available boundaries.
                    """

                class _ConnectLabelWildcard(PyArgumentsTextualSubItem):
                    """
                    Enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _AllowDefeaturing(PyArgumentsTextualSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _RelativeShareTopologyTolerance(PyArgumentsNumericalSubItem):
                    """
                    Specify the relative tolerance for joining or intersecting face pairs, or the relative tolerance for connecting edge and face pairs.
                    """

                class _FluidLabelWildcard(PyArgumentsTextualSubItem):
                    """
                    Argument FluidLabelWildcard.
                    """

                class _ExecuteJoinIntersect(PyArgumentsTextualSubItem):
                    """
                    Choose whether the system will only join faces, only intersect faces, or do both.
                    """

                class _Operation(PyArgumentsTextualSubItem):
                    """
                    Choose whether to apply share topology using the Join-Intersect method where you join and/or intersect the problematic faces, or using the Interface Connect method where you connect edges of overlapping face pairs. Note that imprinting of overlapping faces in SCDM/Discovery is highly recommended for the Interface Connect method.
                    """

                class _ShareTopologyAngle(PyArgumentsNumericalSubItem):
                    """
                    Specify the threshold angle for joining face pairs.
                    """

                class _STToleranceIncrement(PyArgumentsNumericalSubItem):
                    """
                    Specify the increment by which the tolerance changes for each attempt to join face pairs.
                    """

                class _ShowShareTopologyPreferences(PyArgumentsParameterSubItem):
                    """
                    Display advanced options that you may want to apply to the task.
                    """

                class _PerLabelList(PyArgumentsTextualSubItem):
                    """
                    Argument PerLabelList.
                    """

                class _IntfLabelList(PyArgumentsTextualSubItem):
                    """
                    Enter a text string to filter out the list of labels. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                    """

                class _AdvancedImprove(PyArgumentsTextualSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _NumberOfJoinTries(PyArgumentsNumericalSubItem):
                    """
                    Specify the number of attempts that will be made to join face pairs under the given criteria.
                    """

            class _SMImprovePreferences(PyArgumentsSingletonSubItem):
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

                class _SIStepQualityLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument SIStepQualityLimit.
                    """

                class _SIQualityCollapseLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument SIQualityCollapseLimit.
                    """

                class _SIQualityIterations(PyArgumentsNumericalSubItem):
                    """
                    Argument SIQualityIterations.
                    """

                class _SIQualityMaxAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument SIQualityMaxAngle.
                    """

                class _AllowDefeaturing(PyArgumentsTextualSubItem):
                    """
                    Argument AllowDefeaturing.
                    """

                class _ShowSMImprovePreferences(PyArgumentsParameterSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _AdvancedImprove(PyArgumentsTextualSubItem):
                    """
                    Argument AdvancedImprove.
                    """

                class _SIStepWidth(PyArgumentsNumericalSubItem):
                    """
                    Argument SIStepWidth.
                    """

                class _SIRemoveStep(PyArgumentsTextualSubItem):
                    """
                    Argument SIRemoveStep.
                    """

            class _SurfaceMeshPreferences(PyArgumentsSingletonSubItem):
                """
                Argument SurfaceMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.SMQualityCollapseLimit = self._SMQualityCollapseLimit(self, "SMQualityCollapseLimit", service, rules, path)
                    self.FoldFaceLimit = self._FoldFaceLimit(self, "FoldFaceLimit", service, rules, path)
                    self.SMSeparation = self._SMSeparation(self, "SMSeparation", service, rules, path)
                    self.SMSeparationAngle = self._SMSeparationAngle(self, "SMSeparationAngle", service, rules, path)
                    self.AutoMerge = self._AutoMerge(self, "AutoMerge", service, rules, path)
                    self.ShowSurfaceMeshPreferences = self._ShowSurfaceMeshPreferences(self, "ShowSurfaceMeshPreferences", service, rules, path)
                    self.TVMAutoControlCreation = self._TVMAutoControlCreation(self, "TVMAutoControlCreation", service, rules, path)
                    self.SMQualityImprove = self._SMQualityImprove(self, "SMQualityImprove", service, rules, path)
                    self.SMRemoveStep = self._SMRemoveStep(self, "SMRemoveStep", service, rules, path)
                    self.SMStepWidth = self._SMStepWidth(self, "SMStepWidth", service, rules, path)
                    self.VolumeMeshMaxSize = self._VolumeMeshMaxSize(self, "VolumeMeshMaxSize", service, rules, path)
                    self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                    self.SMQualityMaxAngle = self._SMQualityMaxAngle(self, "SMQualityMaxAngle", service, rules, path)
                    self.SelfIntersectCheck = self._SelfIntersectCheck(self, "SelfIntersectCheck", service, rules, path)
                    self.AutoSurfaceRemesh = self._AutoSurfaceRemesh(self, "AutoSurfaceRemesh", service, rules, path)
                    self.SMQualityImproveLimit = self._SMQualityImproveLimit(self, "SMQualityImproveLimit", service, rules, path)
                    self.SetVolumeMeshMaxSize = self._SetVolumeMeshMaxSize(self, "SetVolumeMeshMaxSize", service, rules, path)

                class _SMQualityCollapseLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument SMQualityCollapseLimit.
                    """

                class _FoldFaceLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument FoldFaceLimit.
                    """

                class _SMSeparation(PyArgumentsTextualSubItem):
                    """
                    Argument SMSeparation.
                    """

                class _SMSeparationAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument SMSeparationAngle.
                    """

                class _AutoMerge(PyArgumentsParameterSubItem):
                    """
                    Argument AutoMerge.
                    """

                class _ShowSurfaceMeshPreferences(PyArgumentsParameterSubItem):
                    """
                    Argument ShowSurfaceMeshPreferences.
                    """

                class _TVMAutoControlCreation(PyArgumentsTextualSubItem):
                    """
                    Argument TVMAutoControlCreation.
                    """

                class _SMQualityImprove(PyArgumentsTextualSubItem):
                    """
                    Argument SMQualityImprove.
                    """

                class _SMRemoveStep(PyArgumentsTextualSubItem):
                    """
                    Argument SMRemoveStep.
                    """

                class _SMStepWidth(PyArgumentsNumericalSubItem):
                    """
                    Argument SMStepWidth.
                    """

                class _VolumeMeshMaxSize(PyArgumentsNumericalSubItem):
                    """
                    Argument VolumeMeshMaxSize.
                    """

                class _AutoAssignZoneTypes(PyArgumentsTextualSubItem):
                    """
                    Argument AutoAssignZoneTypes.
                    """

                class _SMQualityMaxAngle(PyArgumentsNumericalSubItem):
                    """
                    Argument SMQualityMaxAngle.
                    """

                class _SelfIntersectCheck(PyArgumentsTextualSubItem):
                    """
                    Argument SelfIntersectCheck.
                    """

                class _AutoSurfaceRemesh(PyArgumentsTextualSubItem):
                    """
                    Argument AutoSurfaceRemesh.
                    """

                class _SMQualityImproveLimit(PyArgumentsNumericalSubItem):
                    """
                    Argument SMQualityImproveLimit.
                    """

                class _SetVolumeMeshMaxSize(PyArgumentsTextualSubItem):
                    """
                    Argument SetVolumeMeshMaxSize.
                    """

        def create_instance(self) -> _ShareTopologyArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._ShareTopologyArguments(*args)

    class SizeControlsTable(PyCommand):
        """
        Review the mesh control settings, such as the Minimum Size, the Maximum Size, and the Growth Rate, as well as a table of common settings.
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
        class _SizeControlsTableArguments(PyArguments):
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

            class _GlobalMin(PyArgumentsNumericalSubItem):
                """
                Argument GlobalMin.
                """

            class _GlobalMax(PyArgumentsNumericalSubItem):
                """
                Argument GlobalMax.
                """

            class _TargetGrowthRate(PyArgumentsNumericalSubItem):
                """
                Argument TargetGrowthRate.
                """

            class _DrawSizeControl(PyArgumentsParameterSubItem):
                """
                Enable this field to display the size boxes in the graphics window.
                """

            class _InitialSizeControl(PyArgumentsParameterSubItem):
                """
                Enable this field to display the initial size control in the graphics window.
                """

            class _TargetSizeControl(PyArgumentsParameterSubItem):
                """
                Enable this field to display the target size control in the graphics window.
                """

            class _SizeControlInterval(PyArgumentsNumericalSubItem):
                """
                Specify the amount of size control boxes to display.
                """

            class _SizeControlParameters(PyArgumentsSingletonSubItem):
                """
                Argument SizeControlParameters.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.NewLabelObjects = self._NewLabelObjects(self, "NewLabelObjects", service, rules, path)
                    self.NewLabelResolution = self._NewLabelResolution(self, "NewLabelResolution", service, rules, path)
                    self.NewLabelType = self._NewLabelType(self, "NewLabelType", service, rules, path)
                    self.NewLabels = self._NewLabels(self, "NewLabels", service, rules, path)
                    self.NewLabelCells = self._NewLabelCells(self, "NewLabelCells", service, rules, path)
                    self.NewLabelMax = self._NewLabelMax(self, "NewLabelMax", service, rules, path)
                    self.NewZoneType = self._NewZoneType(self, "NewZoneType", service, rules, path)
                    self.NewLabelCurvature = self._NewLabelCurvature(self, "NewLabelCurvature", service, rules, path)
                    self.NewLabelMin = self._NewLabelMin(self, "NewLabelMin", service, rules, path)

                class _NewLabelObjects(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelObjects.
                    """

                class _NewLabelResolution(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelResolution.
                    """

                class _NewLabelType(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelType.
                    """

                class _NewLabels(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabels.
                    """

                class _NewLabelCells(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelCells.
                    """

                class _NewLabelMax(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelMax.
                    """

                class _NewZoneType(PyArgumentsTextualSubItem):
                    """
                    Argument NewZoneType.
                    """

                class _NewLabelCurvature(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelCurvature.
                    """

                class _NewLabelMin(PyArgumentsTextualSubItem):
                    """
                    Argument NewLabelMin.
                    """

        def create_instance(self) -> _SizeControlsTableArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SizeControlsTableArguments(*args)

    class SwitchToSolution(PyCommand):
        """
        Command SwitchToSolution.


        Returns
        -------
        None
        """
        class _SwitchToSolutionArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)

        def create_instance(self) -> _SwitchToSolutionArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._SwitchToSolutionArguments(*args)

    class TransformVolumeMesh(PyCommand):
        """
        Use this task to create and apply either a translational or a rotational transformation to the volume mesh (or to one or more copies of the volume mesh). 
                       
                        More...
        Parameters
        ----------
        MTControlName : str
            Specify a name for the transformation or use the default value.
        Type : str
            Indicate the type of transformation: translational or rotational
        Method : str
            By default, the Manual method is utilized, however, when periodics are detected, then Automatic - use existing periodics is the default.
        SelectionType : str
            Indicate the type of transformation: translational or rotational
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
        class _TransformVolumeMeshArguments(PyArguments):
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

            class _MTControlName(PyArgumentsTextualSubItem):
                """
                Specify a name for the transformation or use the default value.
                """

            class _Type(PyArgumentsTextualSubItem):
                """
                Indicate the type of transformation: translational or rotational
                """

            class _Method(PyArgumentsTextualSubItem):
                """
                By default, the Manual method is utilized, however, when periodics are detected, then Automatic - use existing periodics is the default.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Indicate the type of transformation: translational or rotational
                """

            class _TopoBodyList(PyArgumentsTextualSubItem):
                """
                Argument TopoBodyList.
                """

            class _CellZoneList(PyArgumentsTextualSubItem):
                """
                Select one or more objects from the list to which you will apply the transformation. Use the Filter Text drop-down to provide text and/or regular expressions in filtering the list (for example, using \\*, ?, and []). Choose Use Wildcard to provide wildcard expressions in filtering the list. When you use either ? or \\* in your expression, the matching list item(s) are automatically selected in the list. Use ^, |, and & in your expression to indicate boolean operations for NOT, OR, and AND, respectively.  More...
                """

            class _LCSOrigin(PyArgumentsSingletonSubItem):
                """
                Specify the coordinates of the rotational origin.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.OriginY = self._OriginY(self, "OriginY", service, rules, path)
                    self.OriginZ = self._OriginZ(self, "OriginZ", service, rules, path)
                    self.OriginX = self._OriginX(self, "OriginX", service, rules, path)

                class _OriginY(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the rotational origin.
                    """

                class _OriginZ(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the rotational origin.
                    """

                class _OriginX(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the rotational origin.
                    """

            class _LCSVector(PyArgumentsSingletonSubItem):
                """
                Specify the coordinates of the rotational vector.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.VectorX = self._VectorX(self, "VectorX", service, rules, path)
                    self.VectorZ = self._VectorZ(self, "VectorZ", service, rules, path)
                    self.VectorY = self._VectorY(self, "VectorY", service, rules, path)

                class _VectorX(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the rotational vector.
                    """

                class _VectorZ(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the rotational vector.
                    """

                class _VectorY(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the rotational vector.
                    """

            class _TransShift(PyArgumentsSingletonSubItem):
                """
                Specify the coordinates of the translational shift.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShiftY = self._ShiftY(self, "ShiftY", service, rules, path)
                    self.ShiftZ = self._ShiftZ(self, "ShiftZ", service, rules, path)
                    self.ShiftX = self._ShiftX(self, "ShiftX", service, rules, path)

                class _ShiftY(PyArgumentsNumericalSubItem):
                    """
                    Specify the Y-coordinate of the translational shift.
                    """

                class _ShiftZ(PyArgumentsNumericalSubItem):
                    """
                    Specify the Z-coordinate of the translational shift.
                    """

                class _ShiftX(PyArgumentsNumericalSubItem):
                    """
                    Specify the X-coordinate of the translational shift.
                    """

            class _Angle(PyArgumentsNumericalSubItem):
                """
                Specify a value for the angle of rotation for this transformation.
                """

            class _Copy(PyArgumentsTextualSubItem):
                """
                Indicate whether or not to make a copy of the volume mesh and apply the transformation to the copy.
                """

            class _NumOfCopies(PyArgumentsNumericalSubItem):
                """
                Specify the number of copies that you want to make for this transformation.
                """

            class _Merge(PyArgumentsTextualSubItem):
                """
                Indicate whether or not you want to merge cell and face zones prior to transforming the volume mesh, in order to avoid duplication.
                """

            class _Rename(PyArgumentsTextualSubItem):
                """
                Indicate whether or not you want to rename cell and face zones prior to transforming the volume mesh.
                """

            class _MergeBoundaries(PyArgumentsTextualSubItem):
                """
                Argument MergeBoundaries.
                """

        def create_instance(self) -> _TransformVolumeMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._TransformVolumeMeshArguments(*args)

    class UpdateBoundaries(PyCommand):
        """
        Use the table to review a summary of all of your defined boundaries, and their assigned types, and make revisions as needed. Rename a boundary by double-clicking its name in the list and providing another name. Reassign the type for a specific boundary by clicking the type designation and using the drop-down menu that appears.  More...
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
        TopologyBodyList : list[str]
        BoundaryCurrentList : list[str]
        BoundaryCurrentTypeList : list[str]
        BoundaryAllowedTypeList : list[str]

        Returns
        -------
        bool
        """
        class _UpdateBoundariesArguments(PyArguments):
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
                self.TopologyBodyList = self._TopologyBodyList(self, "TopologyBodyList", service, rules, path)
                self.BoundaryCurrentList = self._BoundaryCurrentList(self, "BoundaryCurrentList", service, rules, path)
                self.BoundaryCurrentTypeList = self._BoundaryCurrentTypeList(self, "BoundaryCurrentTypeList", service, rules, path)
                self.BoundaryAllowedTypeList = self._BoundaryAllowedTypeList(self, "BoundaryAllowedTypeList", service, rules, path)

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _SelectionType(PyArgumentsTextualSubItem):
                """
                Choose how boundaries are displayed in the table.
                """

            class _BoundaryLabelList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryLabelList.
                """

            class _BoundaryLabelTypeList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryLabelTypeList.
                """

            class _BoundaryZoneList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryZoneList.
                """

            class _BoundaryZoneTypeList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryZoneTypeList.
                """

            class _OldBoundaryLabelList(PyArgumentsTextualSubItem):
                """
                Argument OldBoundaryLabelList.
                """

            class _OldBoundaryLabelTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldBoundaryLabelTypeList.
                """

            class _OldBoundaryZoneList(PyArgumentsTextualSubItem):
                """
                Argument OldBoundaryZoneList.
                """

            class _OldBoundaryZoneTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldBoundaryZoneTypeList.
                """

            class _OldLabelZoneList(PyArgumentsTextualSubItem):
                """
                Argument OldLabelZoneList.
                """

            class _ListAllBoundariesToggle(PyArgumentsParameterSubItem):
                """
                View more boundaries in the table, such as fluid-fluid internal boundaries, in addition to external boundaries.
                """

            class _ZoneLocation(PyArgumentsTextualSubItem):
                """
                Argument ZoneLocation.
                """

            class _TopologyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyList.
                """

            class _TopologyTypeList(PyArgumentsTextualSubItem):
                """
                Argument TopologyTypeList.
                """

            class _OldTopologyList(PyArgumentsTextualSubItem):
                """
                Argument OldTopologyList.
                """

            class _OldTopologyTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldTopologyTypeList.
                """

            class _TopologyBodyList(PyArgumentsTextualSubItem):
                """
                Argument TopologyBodyList.
                """

            class _BoundaryCurrentList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryCurrentList.
                """

            class _BoundaryCurrentTypeList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryCurrentTypeList.
                """

            class _BoundaryAllowedTypeList(PyArgumentsTextualSubItem):
                """
                Argument BoundaryAllowedTypeList.
                """

        def create_instance(self) -> _UpdateBoundariesArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateBoundariesArguments(*args)

    class UpdateRegionSettings(PyCommand):
        """
        Review the settings assigned to the regions in your simulation. Use the table to reassign their extraction techniques, region types, volume meshing cell types, or leakage size settings. More...
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
        class _UpdateRegionSettingsArguments(PyArguments):
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

            class _MainFluidRegion(PyArgumentsTextualSubItem):
                """
                Identify the main fluid region for your simulation.
                """

            class _FilterCategory(PyArgumentsTextualSubItem):
                """
                Select how your regions will be displayed in the table. You can choose to view all regions, or specifically identified regions, or only object-based regions.
                """

            class _RegionNameList(PyArgumentsTextualSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionMeshMethodList(PyArgumentsTextualSubItem):
                """
                Argument RegionMeshMethodList.
                """

            class _RegionTypeList(PyArgumentsTextualSubItem):
                """
                Argument RegionTypeList.
                """

            class _RegionVolumeFillList(PyArgumentsTextualSubItem):
                """
                Argument RegionVolumeFillList.
                """

            class _RegionLeakageSizeList(PyArgumentsTextualSubItem):
                """
                Argument RegionLeakageSizeList.
                """

            class _RegionOversetComponenList(PyArgumentsTextualSubItem):
                """
                Argument RegionOversetComponenList.
                """

            class _OldRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionMeshMethodList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionMeshMethodList.
                """

            class _OldRegionTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionTypeList.
                """

            class _OldRegionVolumeFillList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionVolumeFillList.
                """

            class _OldRegionLeakageSizeList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionLeakageSizeList.
                """

            class _OldRegionOversetComponenList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionOversetComponenList.
                """

            class _AllRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionNameList.
                """

            class _AllRegionMeshMethodList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionMeshMethodList.
                """

            class _AllRegionTypeList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionTypeList.
                """

            class _AllRegionVolumeFillList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionVolumeFillList.
                """

            class _AllRegionLeakageSizeList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionLeakageSizeList.
                """

            class _AllRegionOversetComponenList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionOversetComponenList.
                """

            class _AllRegionLinkedConstructionSurfaceList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionLinkedConstructionSurfaceList.
                """

            class _AllRegionSourceList(PyArgumentsTextualSubItem):
                """
                Argument AllRegionSourceList.
                """

            class _AllRegionFilterCategories(PyArgumentsTextualSubItem):
                """
                Argument AllRegionFilterCategories.
                """

        def create_instance(self) -> _UpdateRegionSettingsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateRegionSettingsArguments(*args)

    class UpdateRegions(PyCommand):
        """
        Use the table to review a summary of all of your defined regions, and their assigned types, and make revisions as needed. Rename a region by double-clicking its name in the list and providing another name. Reassign the type for a specific region by clicking the type designation and using the drop-down menu that appears. Dead regions are the same as a void or a pocket in the domain, and are not transferred to the Fluent solver.  More...
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
        class _UpdateRegionsArguments(PyArguments):
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

            class _MeshObject(PyArgumentsTextualSubItem):
                """
                Argument MeshObject.
                """

            class _RegionNameList(PyArgumentsTextualSubItem):
                """
                Argument RegionNameList.
                """

            class _RegionTypeList(PyArgumentsTextualSubItem):
                """
                Argument RegionTypeList.
                """

            class _OldRegionNameList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionNameList.
                """

            class _OldRegionTypeList(PyArgumentsTextualSubItem):
                """
                Argument OldRegionTypeList.
                """

            class _RegionInternals(PyArgumentsTextualSubItem):
                """
                Argument RegionInternals.
                """

            class _RegionInternalTypes(PyArgumentsTextualSubItem):
                """
                Argument RegionInternalTypes.
                """

            class _RegionCurrentList(PyArgumentsTextualSubItem):
                """
                Argument RegionCurrentList.
                """

            class _RegionCurrentTypeList(PyArgumentsTextualSubItem):
                """
                Argument RegionCurrentTypeList.
                """

            class _NumberOfListedRegions(PyArgumentsNumericalSubItem):
                """
                Argument NumberOfListedRegions.
                """

        def create_instance(self) -> _UpdateRegionsArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateRegionsArguments(*args)

    class UpdateTheVolumeMesh(PyCommand):
        """
        Use this task to remove the existing volume mesh and to update the volume mesh with your new part replacement changes.
        Parameters
        ----------
        EnableParallel : bool
            Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.

        Returns
        -------
        bool
        """
        class _UpdateTheVolumeMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.EnableParallel = self._EnableParallel(self, "EnableParallel", service, rules, path)

            class _EnableParallel(PyArgumentsParameterSubItem):
                """
                Enable this option to perform parallel volume and continuous boundary layer (prism) meshing for fluid region(s). Applicable for poly, hexcore and poly-hexcore volume fill types.
                """

        def create_instance(self) -> _UpdateTheVolumeMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._UpdateTheVolumeMeshArguments(*args)

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
        class _WrapMainArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.WrapRegionsName = self._WrapRegionsName(self, "WrapRegionsName", service, rules, path)

            class _WrapRegionsName(PyArgumentsTextualSubItem):
                """
                Argument WrapRegionsName.
                """

        def create_instance(self) -> _WrapMainArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._WrapMainArguments(*args)

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
        class _Write2dMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileName = self._FileName(self, "FileName", service, rules, path)
                self.SkipExport = self._SkipExport(self, "SkipExport", service, rules, path)

            class _FileName(PyArgumentsTextualSubItem):
                """
                Argument FileName.
                """

            class _SkipExport(PyArgumentsParameterSubItem):
                """
                Argument SkipExport.
                """

        def create_instance(self) -> _Write2dMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._Write2dMeshArguments(*args)

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
        class _WriteSkinMeshArguments(PyArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileName = self._FileName(self, "FileName", service, rules, path)

            class _FileName(PyArgumentsTextualSubItem):
                """
                Argument FileName.
                """

        def create_instance(self) -> _WriteSkinMeshArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._WriteSkinMeshArguments(*args)

