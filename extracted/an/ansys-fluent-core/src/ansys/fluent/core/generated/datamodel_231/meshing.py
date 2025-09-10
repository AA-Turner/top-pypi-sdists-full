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
        self.GlobalSettings = self.__class__.GlobalSettings(service, rules, path + [("GlobalSettings", "")])
        self.AddBoundaryLayers = self.__class__.AddBoundaryLayers(service, rules, "AddBoundaryLayers", path)
        self.AddBoundaryLayersForPartReplacement = self.__class__.AddBoundaryLayersForPartReplacement(service, rules, "AddBoundaryLayersForPartReplacement", path)
        self.AddBoundaryType = self.__class__.AddBoundaryType(service, rules, "AddBoundaryType", path)
        self.AddLocalSizingFTM = self.__class__.AddLocalSizingFTM(service, rules, "AddLocalSizingFTM", path)
        self.AddLocalSizingWTM = self.__class__.AddLocalSizingWTM(service, rules, "AddLocalSizingWTM", path)
        self.AddMultiZoneControls = self.__class__.AddMultiZoneControls(service, rules, "AddMultiZoneControls", path)
        self.AddShellBoundaryLayers = self.__class__.AddShellBoundaryLayers(service, rules, "AddShellBoundaryLayers", path)
        self.AddThickness = self.__class__.AddThickness(service, rules, "AddThickness", path)
        self.Capping = self.__class__.Capping(service, rules, "Capping", path)
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
        self.CreateOversetInterfaces = self.__class__.CreateOversetInterfaces(service, rules, "CreateOversetInterfaces", path)
        self.CreatePorousRegions = self.__class__.CreatePorousRegions(service, rules, "CreatePorousRegions", path)
        self.CreateRegions = self.__class__.CreateRegions(service, rules, "CreateRegions", path)
        self.DefineLeakageThreshold = self.__class__.DefineLeakageThreshold(service, rules, "DefineLeakageThreshold", path)
        self.DescribeGeometryAndFlow = self.__class__.DescribeGeometryAndFlow(service, rules, "DescribeGeometryAndFlow", path)
        self.DescribeOversetFeatures = self.__class__.DescribeOversetFeatures(service, rules, "DescribeOversetFeatures", path)
        self.ExtractEdges = self.__class__.ExtractEdges(service, rules, "ExtractEdges", path)
        self.ExtrudeVolumeMesh = self.__class__.ExtrudeVolumeMesh(service, rules, "ExtrudeVolumeMesh", path)
        self.GenerateInitialSurfaceMesh = self.__class__.GenerateInitialSurfaceMesh(service, rules, "GenerateInitialSurfaceMesh", path)
        self.GeneratePrisms = self.__class__.GeneratePrisms(service, rules, "GeneratePrisms", path)
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
        self.TransformVolumeMesh = self.__class__.TransformVolumeMesh(service, rules, "TransformVolumeMesh", path)
        self.UpdateBoundaries = self.__class__.UpdateBoundaries(service, rules, "UpdateBoundaries", path)
        self.UpdateRegionSettings = self.__class__.UpdateRegionSettings(service, rules, "UpdateRegionSettings", path)
        self.UpdateRegions = self.__class__.UpdateRegions(service, rules, "UpdateRegions", path)
        self.UpdateTheVolumeMesh = self.__class__.UpdateTheVolumeMesh(service, rules, "UpdateTheVolumeMesh", path)
        self.WrapMain = self.__class__.WrapMain(service, rules, "WrapMain", path)
        self.Write2dMesh = self.__class__.Write2dMesh(service, rules, "Write2dMesh", path)
        super().__init__(service, rules, path)

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
            self.EnablePrimeMeshing = self.__class__.EnablePrimeMeshing(service, rules, path + [("EnablePrimeMeshing", "")])
            self.InitialVersion = self.__class__.InitialVersion(service, rules, path + [("InitialVersion", "")])
            self.LengthUnit = self.__class__.LengthUnit(service, rules, path + [("LengthUnit", "")])
            self.NormalMode = self.__class__.NormalMode(service, rules, path + [("NormalMode", "")])
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

        class VolumeUnit(PyTextual):
            """
            Parameter VolumeUnit of value type str.
            """
            pass

    class AddBoundaryLayers(PyCommand):
        """
        Command AddBoundaryLayers.

        Parameters
        ----------
        AddChild : str
        ReadPrismControlFile : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        Rate : float
        FirstHeight : float
        FaceScope : dict[str, Any]
        RegionScope : list[str]
        BlLabelList : list[str]
        ZoneSelectionList : list[str]
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
                Argument AddChild.
                """

            class _ReadPrismControlFile(PyTextualCommandArgumentsSubItem):
                """
                Argument ReadPrismControlFile.
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

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Argument Rate.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstHeight.
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
                Argument RegionScope.
                """

            class _BlLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BlLabelList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
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
                    self.ModifyAtInvalidNormals = self._ModifyAtInvalidNormals(self, "ModifyAtInvalidNormals", service, rules, path)
                    self.AdditionalIgnoredLayers = self._AdditionalIgnoredLayers(self, "AdditionalIgnoredLayers", service, rules, path)
                    self.NumberOfSplitLayers = self._NumberOfSplitLayers(self, "NumberOfSplitLayers", service, rules, path)
                    self.Continuous = self._Continuous(self, "Continuous", service, rules, path)
                    self.ShowLocalPrismPreferences = self._ShowLocalPrismPreferences(self, "ShowLocalPrismPreferences", service, rules, path)
                    self.SplitPrism = self._SplitPrism(self, "SplitPrism", service, rules, path)
                    self.IgnoreBoundaryLayers = self._IgnoreBoundaryLayers(self, "IgnoreBoundaryLayers", service, rules, path)

                class _ModifyAtInvalidNormals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModifyAtInvalidNormals.
                    """

                class _AdditionalIgnoredLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AdditionalIgnoredLayers.
                    """

                class _NumberOfSplitLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfSplitLayers.
                    """

                class _Continuous(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Continuous.
                    """

                class _ShowLocalPrismPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowLocalPrismPreferences.
                    """

                class _SplitPrism(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SplitPrism.
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
        ReadPrismControlFile : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        Rate : float
        FirstHeight : float
        FaceScope : dict[str, Any]
        RegionScope : list[str]
        BlLabelList : list[str]
        ZoneSelectionList : list[str]
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
                Argument AddChild.
                """

            class _ReadPrismControlFile(PyTextualCommandArgumentsSubItem):
                """
                Argument ReadPrismControlFile.
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

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Argument Rate.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstHeight.
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
                Argument RegionScope.
                """

            class _BlLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BlLabelList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
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
                    self.ModifyAtInvalidNormals = self._ModifyAtInvalidNormals(self, "ModifyAtInvalidNormals", service, rules, path)
                    self.AdditionalIgnoredLayers = self._AdditionalIgnoredLayers(self, "AdditionalIgnoredLayers", service, rules, path)
                    self.NumberOfSplitLayers = self._NumberOfSplitLayers(self, "NumberOfSplitLayers", service, rules, path)
                    self.Continuous = self._Continuous(self, "Continuous", service, rules, path)
                    self.ShowLocalPrismPreferences = self._ShowLocalPrismPreferences(self, "ShowLocalPrismPreferences", service, rules, path)
                    self.SplitPrism = self._SplitPrism(self, "SplitPrism", service, rules, path)
                    self.IgnoreBoundaryLayers = self._IgnoreBoundaryLayers(self, "IgnoreBoundaryLayers", service, rules, path)

                class _ModifyAtInvalidNormals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModifyAtInvalidNormals.
                    """

                class _AdditionalIgnoredLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument AdditionalIgnoredLayers.
                    """

                class _NumberOfSplitLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfSplitLayers.
                    """

                class _Continuous(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Continuous.
                    """

                class _ShowLocalPrismPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowLocalPrismPreferences.
                    """

                class _SplitPrism(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SplitPrism.
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
        NewBoundaryType : str
        BoundaryFaceZoneList : list[str]
        Merge : str
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
                self.BoundaryFaceZoneList = self._BoundaryFaceZoneList(self, "BoundaryFaceZoneList", service, rules, path)
                self.Merge = self._Merge(self, "Merge", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _NewBoundaryLabelName(PyTextualCommandArgumentsSubItem):
                """
                Argument NewBoundaryLabelName.
                """

            class _NewBoundaryType(PyTextualCommandArgumentsSubItem):
                """
                Argument NewBoundaryType.
                """

            class _BoundaryFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument BoundaryFaceZoneList.
                """

            class _Merge(PyTextualCommandArgumentsSubItem):
                """
                Argument Merge.
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
        SelectionType : str
        ObjectSelectionList : list[str]
        LabelSelectionList : list[str]
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        EdgeSelectionList : list[str]
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
                Argument LocalSettingsName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeSelectionList.
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
                    self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                    self.InitialSizeControl = self._InitialSizeControl(self, "InitialSizeControl", service, rules, path)
                    self.WrapGrowthRate = self._WrapGrowthRate(self, "WrapGrowthRate", service, rules, path)
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

                class _SizingType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizingType.
                    """

                class _InitialSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument InitialSizeControl.
                    """

                class _WrapGrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapGrowthRate.
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
        BOIControlName : str
        BOIGrowthRate : float
        BOIExecution : str
        BOISize : float
        BOIMinSize : float
        BOIMaxSize : float
        BOICurvatureNormalAngle : float
        BOICellsPerGap : float
        BOIScopeTo : str
        IgnoreOrientation : str
        BOIZoneorLabel : str
        BOIFaceLabelList : list[str]
        BOIFaceZoneList : list[str]
        EdgeLabelList : list[str]
        TopologyList : list[str]
        BOIPatchingtoggle : bool
        DrawSizeControl : bool
        ZoneLocation : list[str]
        CompleteFaceZoneList : list[str]
        CompleteFaceLabelList : list[str]
        CompleteEdgeLabelList : list[str]
        CompleteTopologyList : list[str]

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
                self.BOISize = self._BOISize(self, "BOISize", service, rules, path)
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
                self.TopologyList = self._TopologyList(self, "TopologyList", service, rules, path)
                self.BOIPatchingtoggle = self._BOIPatchingtoggle(self, "BOIPatchingtoggle", service, rules, path)
                self.DrawSizeControl = self._DrawSizeControl(self, "DrawSizeControl", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.CompleteFaceZoneList = self._CompleteFaceZoneList(self, "CompleteFaceZoneList", service, rules, path)
                self.CompleteFaceLabelList = self._CompleteFaceLabelList(self, "CompleteFaceLabelList", service, rules, path)
                self.CompleteEdgeLabelList = self._CompleteEdgeLabelList(self, "CompleteEdgeLabelList", service, rules, path)
                self.CompleteTopologyList = self._CompleteTopologyList(self, "CompleteTopologyList", service, rules, path)

            class _AddChild(PyTextualCommandArgumentsSubItem):
                """
                Argument AddChild.
                """

            class _BOIControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument BOIControlName.
                """

            class _BOIGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOIGrowthRate.
                """

            class _BOIExecution(PyTextualCommandArgumentsSubItem):
                """
                Argument BOIExecution.
                """

            class _BOISize(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOISize.
                """

            class _BOIMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOIMinSize.
                """

            class _BOIMaxSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOIMaxSize.
                """

            class _BOICurvatureNormalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOICurvatureNormalAngle.
                """

            class _BOICellsPerGap(PyNumericalCommandArgumentsSubItem):
                """
                Argument BOICellsPerGap.
                """

            class _BOIScopeTo(PyTextualCommandArgumentsSubItem):
                """
                Argument BOIScopeTo.
                """

            class _IgnoreOrientation(PyTextualCommandArgumentsSubItem):
                """
                Argument IgnoreOrientation.
                """

            class _BOIZoneorLabel(PyTextualCommandArgumentsSubItem):
                """
                Argument BOIZoneorLabel.
                """

            class _BOIFaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BOIFaceLabelList.
                """

            class _BOIFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument BOIFaceZoneList.
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelList.
                """

            class _TopologyList(PyTextualCommandArgumentsSubItem):
                """
                Argument TopologyList.
                """

            class _BOIPatchingtoggle(PyParameterCommandArgumentsSubItem):
                """
                Argument BOIPatchingtoggle.
                """

            class _DrawSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Argument DrawSizeControl.
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
        MultiZName : str
        MeshMethod : str
        FillWith : str
        UseSweepSize : str
        MaxSweepSize : float
        RegionScope : list[str]
        SourceMethod : str
        ParallelSelection : bool
        LabelSourceList : list[str]
        ZoneSourceList : list[str]
        ZoneLocation : list[str]
        AssignSizeUsing : str
        Intervals : int
        Size : float
        SmallestHeight : float
        BiasMethod : str
        GrowthMethod : str
        GrowthRate : float
        BiasFactor : float
        EdgeLabelList : list[str]
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
                self.SourceMethod = self._SourceMethod(self, "SourceMethod", service, rules, path)
                self.ParallelSelection = self._ParallelSelection(self, "ParallelSelection", service, rules, path)
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
                self.EdgeLabelList = self._EdgeLabelList(self, "EdgeLabelList", service, rules, path)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)
                self.CompleteEdgeScope = self._CompleteEdgeScope(self, "CompleteEdgeScope", service, rules, path)

            class _ControlType(PyTextualCommandArgumentsSubItem):
                """
                Argument ControlType.
                """

            class _MultiZName(PyTextualCommandArgumentsSubItem):
                """
                Argument MultiZName.
                """

            class _MeshMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshMethod.
                """

            class _FillWith(PyTextualCommandArgumentsSubItem):
                """
                Argument FillWith.
                """

            class _UseSweepSize(PyTextualCommandArgumentsSubItem):
                """
                Argument UseSweepSize.
                """

            class _MaxSweepSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxSweepSize.
                """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionScope.
                """

            class _SourceMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument SourceMethod.
                """

            class _ParallelSelection(PyParameterCommandArgumentsSubItem):
                """
                Argument ParallelSelection.
                """

            class _LabelSourceList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSourceList.
                """

            class _ZoneSourceList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSourceList.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _AssignSizeUsing(PyTextualCommandArgumentsSubItem):
                """
                Argument AssignSizeUsing.
                """

            class _Intervals(PyNumericalCommandArgumentsSubItem):
                """
                Argument Intervals.
                """

            class _Size(PyNumericalCommandArgumentsSubItem):
                """
                Argument Size.
                """

            class _SmallestHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument SmallestHeight.
                """

            class _BiasMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument BiasMethod.
                """

            class _GrowthMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument GrowthMethod.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument GrowthRate.
                """

            class _BiasFactor(PyNumericalCommandArgumentsSubItem):
                """
                Argument BiasFactor.
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelList.
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

    class AddShellBoundaryLayers(PyCommand):
        """
        Command AddShellBoundaryLayers.

        Parameters
        ----------
        AddChild : str
        BLControlName : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        LastAspectRatio : float
        Rate : float
        FirstHeight : float
        FaceLabelList : list[str]
        EdgeLabelList : list[str]
        PrimeShellBLPreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _AddShellBoundaryLayersCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.AddChild = self._AddChild(self, "AddChild", service, rules, path)
                self.BLControlName = self._BLControlName(self, "BLControlName", service, rules, path)
                self.OffsetMethodType = self._OffsetMethodType(self, "OffsetMethodType", service, rules, path)
                self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                self.FirstAspectRatio = self._FirstAspectRatio(self, "FirstAspectRatio", service, rules, path)
                self.LastAspectRatio = self._LastAspectRatio(self, "LastAspectRatio", service, rules, path)
                self.Rate = self._Rate(self, "Rate", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.FaceLabelList = self._FaceLabelList(self, "FaceLabelList", service, rules, path)
                self.EdgeLabelList = self._EdgeLabelList(self, "EdgeLabelList", service, rules, path)
                self.PrimeShellBLPreferences = self._PrimeShellBLPreferences(self, "PrimeShellBLPreferences", service, rules, path)

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

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstHeight.
                """

            class _FaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceLabelList.
                """

            class _EdgeLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabelList.
                """

            class _PrimeShellBLPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument PrimeShellBLPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowPrimeShellBLPreferences = self._ShowPrimeShellBLPreferences(self, "ShowPrimeShellBLPreferences", service, rules, path)
                    self.SplitQuads = self._SplitQuads(self, "SplitQuads", service, rules, path)
                    self.MaxAspectRatio = self._MaxAspectRatio(self, "MaxAspectRatio", service, rules, path)
                    self.MinAspectRatio = self._MinAspectRatio(self, "MinAspectRatio", service, rules, path)
                    self.LocalRemesh = self._LocalRemesh(self, "LocalRemesh", service, rules, path)
                    self.MaxFaceSkew = self._MaxFaceSkew(self, "MaxFaceSkew", service, rules, path)
                    self.RefineStretchedQuads = self._RefineStretchedQuads(self, "RefineStretchedQuads", service, rules, path)
                    self.GapFactor = self._GapFactor(self, "GapFactor", service, rules, path)
                    self.MaxProjectionAngle = self._MaxProjectionAngle(self, "MaxProjectionAngle", service, rules, path)

                class _ShowPrimeShellBLPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowPrimeShellBLPreferences.
                    """

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

                class _LocalRemesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument LocalRemesh.
                    """

                class _MaxFaceSkew(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxFaceSkew.
                    """

                class _RefineStretchedQuads(PyTextualCommandArgumentsSubItem):
                    """
                    Argument RefineStretchedQuads.
                    """

                class _GapFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument GapFactor.
                    """

                class _MaxProjectionAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxProjectionAngle.
                    """

        def create_instance(self) -> _AddShellBoundaryLayersCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddShellBoundaryLayersCommandArguments(*args)

    class AddThickness(PyCommand):
        """
        Command AddThickness.

        Parameters
        ----------
        ZeroThicknessName : str
        SelectionType : str
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        ObjectSelectionList : list[str]
        LabelSelectionList : list[str]
        Distance : float

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
                Argument ZeroThicknessName.
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

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _Distance(PyNumericalCommandArgumentsSubItem):
                """
                Argument Distance.
                """

        def create_instance(self) -> _AddThicknessCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._AddThicknessCommandArguments(*args)

    class Capping(PyCommand):
        """
        Command Capping.

        Parameters
        ----------
        PatchName : str
        ZoneType : str
        PatchType : str
        SelectionType : str
        LabelSelectionList : list[str]
        ZoneSelectionList : list[str]
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
                Argument PatchName.
                """

            class _ZoneType(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneType.
                """

            class _PatchType(PyTextualCommandArgumentsSubItem):
                """
                Argument PatchType.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
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

    class ChooseMeshControlOptions(PyCommand):
        """
        Command ChooseMeshControlOptions.

        Parameters
        ----------
        ReadOrCreate : str
        SizeControlFileName : str
        WrapSizeControlFileName : str
        CreationMethod : str
        ViewOption : str
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
                Argument ReadOrCreate.
                """

            class _SizeControlFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument SizeControlFileName.
                """

            class _WrapSizeControlFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument WrapSizeControlFileName.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CreationMethod.
                """

            class _ViewOption(PyTextualCommandArgumentsSubItem):
                """
                Argument ViewOption.
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
                    self.WrapTargetBothOptions = self._WrapTargetBothOptions(self, "WrapTargetBothOptions", service, rules, path)
                    self.SolidFluidRaio = self._SolidFluidRaio(self, "SolidFluidRaio", service, rules, path)
                    self.BoundaryLayers = self._BoundaryLayers(self, "BoundaryLayers", service, rules, path)
                    self.EdgeProximityComputation = self._EdgeProximityComputation(self, "EdgeProximityComputation", service, rules, path)
                    self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                    self.ExistingSizeField = self._ExistingSizeField(self, "ExistingSizeField", service, rules, path)
                    self.WrapSizeFieldFileName = self._WrapSizeFieldFileName(self, "WrapSizeFieldFileName", service, rules, path)
                    self.TargeSizeFieldFileName = self._TargeSizeFieldFileName(self, "TargeSizeFieldFileName", service, rules, path)
                    self.WrapTargetRaio = self._WrapTargetRaio(self, "WrapTargetRaio", service, rules, path)

                class _WrapTargetSizeFieldRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WrapTargetSizeFieldRatio.
                    """

                class _WrapTargetBothOptions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument WrapTargetBothOptions.
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

                class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AdvancedOptions.
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
        AddPartReplacement : str
        AddLocalSizing : str
        AddBoundaryLayer : str
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
                Argument AddPartManagement.
                """

            class _AddPartReplacement(PyTextualCommandArgumentsSubItem):
                """
                Argument AddPartReplacement.
                """

            class _AddLocalSizing(PyTextualCommandArgumentsSubItem):
                """
                Argument AddLocalSizing.
                """

            class _AddBoundaryLayer(PyTextualCommandArgumentsSubItem):
                """
                Argument AddBoundaryLayer.
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
        BoundingBoxObject : dict[str, Any]
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]

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
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)

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
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Options = self._Options(self, "Options", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Options(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Options.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
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

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
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
        BoundingBoxObject : dict[str, Any]
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]
        VolumeFill : str

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
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)

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
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Options = self._Options(self, "Options", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Options(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Options.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
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

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Argument VolumeFill.
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
        BoundingBoxObject : dict[str, Any]
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]
        VolumeFill : str

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
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)

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
                    self.WakeGrowthFactor = self._WakeGrowthFactor(self, "WakeGrowthFactor", service, rules, path)
                    self.NumberOfLayers = self._NumberOfLayers(self, "NumberOfLayers", service, rules, path)
                    self.BoundaryLayerLevels = self._BoundaryLayerLevels(self, "BoundaryLayerLevels", service, rules, path)
                    self.FlowDirection = self._FlowDirection(self, "FlowDirection", service, rules, path)
                    self.MptMethodType = self._MptMethodType(self, "MptMethodType", service, rules, path)
                    self.EdgeSelectionList = self._EdgeSelectionList(self, "EdgeSelectionList", service, rules, path)
                    self.Rate = self._Rate(self, "Rate", service, rules, path)
                    self.X = self._X(self, "X", service, rules, path)
                    self.LastRatioPercentage = self._LastRatioPercentage(self, "LastRatioPercentage", service, rules, path)
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

                class _WakeGrowthFactor(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument WakeGrowthFactor.
                    """

                class _NumberOfLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfLayers.
                    """

                class _BoundaryLayerLevels(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument BoundaryLayerLevels.
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

                class _Rate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Rate.
                    """

                class _X(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument X.
                    """

                class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument LastRatioPercentage.
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
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Options = self._Options(self, "Options", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Options(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Options.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
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

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Argument VolumeFill.
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
        SelectionType : str
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        ObjectSelectionList : list[str]
        LabelSelectionList : list[str]
        GroundZoneSelectionList : list[str]
        Distance : float
        FeatureAngle : float
        PatchHole : bool
        FlipDirection : bool

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
                self.FeatureAngle = self._FeatureAngle(self, "FeatureAngle", service, rules, path)
                self.PatchHole = self._PatchHole(self, "PatchHole", service, rules, path)
                self.FlipDirection = self._FlipDirection(self, "FlipDirection", service, rules, path)

            class _ContactPatchName(PyTextualCommandArgumentsSubItem):
                """
                Argument ContactPatchName.
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

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _GroundZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument GroundZoneSelectionList.
                """

            class _Distance(PyNumericalCommandArgumentsSubItem):
                """
                Argument Distance.
                """

            class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument FeatureAngle.
                """

            class _PatchHole(PyParameterCommandArgumentsSubItem):
                """
                Argument PatchHole.
                """

            class _FlipDirection(PyParameterCommandArgumentsSubItem):
                """
                Argument FlipDirection.
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
        CreationMethod : str
        ExtractionMethod : str
        SelectionType : str
        ObjectSelectionList : list[str]
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
        ObjectSelectionSingle : list[str]
        ZoneSelectionSingle : list[str]
        LabelSelectionSingle : list[str]
        OriginalObjectName : str
        BoundingBoxObject : dict[str, Any]

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
                Argument ExternalBoundariesName.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CreationMethod.
                """

            class _ExtractionMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument ExtractionMethod.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
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

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionSingle.
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionSingle.
                """

            class _LabelSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionSingle.
                """

            class _OriginalObjectName(PyTextualCommandArgumentsSubItem):
                """
                Argument OriginalObjectName.
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
        SizingMethod : str
        GapSizeRatio : float
        GapSize : float
        SelectionType : str
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
        ObjectSelectionList : list[str]
        GapCoverBetweenZones : str
        GapCoverRefineFactor : float
        RefineWrapperBeforeProjection : str
        AdvancedOptions : bool
        MaxIslandFaceForGapCover : int
        GapCoverFeatureImprint : str

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
                self.RefineWrapperBeforeProjection = self._RefineWrapperBeforeProjection(self, "RefineWrapperBeforeProjection", service, rules, path)
                self.AdvancedOptions = self._AdvancedOptions(self, "AdvancedOptions", service, rules, path)
                self.MaxIslandFaceForGapCover = self._MaxIslandFaceForGapCover(self, "MaxIslandFaceForGapCover", service, rules, path)
                self.GapCoverFeatureImprint = self._GapCoverFeatureImprint(self, "GapCoverFeatureImprint", service, rules, path)

            class _GapCoverName(PyTextualCommandArgumentsSubItem):
                """
                Argument GapCoverName.
                """

            class _SizingMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument SizingMethod.
                """

            class _GapSizeRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument GapSizeRatio.
                """

            class _GapSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument GapSize.
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

            class _GapCoverBetweenZones(PyTextualCommandArgumentsSubItem):
                """
                Argument GapCoverBetweenZones.
                """

            class _GapCoverRefineFactor(PyNumericalCommandArgumentsSubItem):
                """
                Argument GapCoverRefineFactor.
                """

            class _RefineWrapperBeforeProjection(PyTextualCommandArgumentsSubItem):
                """
                Argument RefineWrapperBeforeProjection.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Argument AdvancedOptions.
                """

            class _MaxIslandFaceForGapCover(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxIslandFaceForGapCover.
                """

            class _GapCoverFeatureImprint(PyTextualCommandArgumentsSubItem):
                """
                Argument GapCoverFeatureImprint.
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
        BoundingBoxObject : dict[str, Any]
        OffsetObject : dict[str, Any]
        CylinderObject : dict[str, Any]
        VolumeFill : str

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
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)
                self.OffsetObject = self._OffsetObject(self, "OffsetObject", service, rules, path)
                self.CylinderObject = self._CylinderObject(self, "CylinderObject", service, rules, path)
                self.VolumeFill = self._VolumeFill(self, "VolumeFill", service, rules, path)

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
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Options = self._Options(self, "Options", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Options(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Options.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
                    """

                class _Node2(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node2.
                    """

                class _HeightFrontInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightFrontInc.
                    """

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
                    """

                class _Radius1(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius1.
                    """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Argument VolumeFill.
                """

        def create_instance(self) -> _CreateLocalRefinementRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateLocalRefinementRegionsCommandArguments(*args)

    class CreateOversetInterfaces(PyCommand):
        """
        Command CreateOversetInterfaces.

        Parameters
        ----------
        OversetInterfacesName : str
        ObjectSelectionList : list[str]

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
                Argument OversetInterfacesName.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
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
        PorousRegionName : str
        FileName : str
        Location : str
        CellSizeP1P2 : float
        CellSizeP1P3 : float
        CellSizeP1P4 : float
        BufferSizeRatio : float
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
                Argument InputMethod.
                """

            class _PorousRegionName(PyTextualCommandArgumentsSubItem):
                """
                Argument PorousRegionName.
                """

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Argument FileName.
                """

            class _Location(PyTextualCommandArgumentsSubItem):
                """
                Argument Location.
                """

            class _CellSizeP1P2(PyNumericalCommandArgumentsSubItem):
                """
                Argument CellSizeP1P2.
                """

            class _CellSizeP1P3(PyNumericalCommandArgumentsSubItem):
                """
                Argument CellSizeP1P3.
                """

            class _CellSizeP1P4(PyNumericalCommandArgumentsSubItem):
                """
                Argument CellSizeP1P4.
                """

            class _BufferSizeRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument BufferSizeRatio.
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
                    self.Thickness = self._Thickness(self, "Thickness", service, rules, path)
                    self.ZoneSelectionList = self._ZoneSelectionList(self, "ZoneSelectionList", service, rules, path)
                    self.SelectionType = self._SelectionType(self, "SelectionType", service, rules, path)
                    self.LabelSelectionList = self._LabelSelectionList(self, "LabelSelectionList", service, rules, path)
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

                class _Thickness(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Thickness.
                    """

                class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ZoneSelectionList.
                    """

                class _SelectionType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SelectionType.
                    """

                class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument LabelSelectionList.
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
        RetainDeadRegionName : str
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
                Argument NumberOfFlowVolumes.
                """

            class _RetainDeadRegionName(PyTextualCommandArgumentsSubItem):
                """
                Argument RetainDeadRegionName.
                """

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

        def create_instance(self) -> _CreateRegionsCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._CreateRegionsCommandArguments(*args)

    class DefineLeakageThreshold(PyCommand):
        """
        Command DefineLeakageThreshold.

        Parameters
        ----------
        AddChild : str
        LeakageName : str
        SelectionType : str
        DeadRegionsList : list[str]
        RegionSelectionSingle : list[str]
        DeadRegionsSize : float
        PlaneClippingValue : int
        PlaneDirection : str
        FlipDirection : bool

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
                Argument AddChild.
                """

            class _LeakageName(PyTextualCommandArgumentsSubItem):
                """
                Argument LeakageName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _DeadRegionsList(PyTextualCommandArgumentsSubItem):
                """
                Argument DeadRegionsList.
                """

            class _RegionSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionSelectionSingle.
                """

            class _DeadRegionsSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument DeadRegionsSize.
                """

            class _PlaneClippingValue(PyNumericalCommandArgumentsSubItem):
                """
                Argument PlaneClippingValue.
                """

            class _PlaneDirection(PyTextualCommandArgumentsSubItem):
                """
                Argument PlaneDirection.
                """

            class _FlipDirection(PyParameterCommandArgumentsSubItem):
                """
                Argument FlipDirection.
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
        GeometryOptions : bool
        AddEnclosure : str
        CloseCaps : str
        LocalRefinementRegions : str
        DescribeGeometryAndFlowOptions : dict[str, Any]

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

            class _FlowType(PyTextualCommandArgumentsSubItem):
                """
                Argument FlowType.
                """

            class _GeometryOptions(PyParameterCommandArgumentsSubItem):
                """
                Argument GeometryOptions.
                """

            class _AddEnclosure(PyTextualCommandArgumentsSubItem):
                """
                Argument AddEnclosure.
                """

            class _CloseCaps(PyTextualCommandArgumentsSubItem):
                """
                Argument CloseCaps.
                """

            class _LocalRefinementRegions(PyTextualCommandArgumentsSubItem):
                """
                Argument LocalRefinementRegions.
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

                class _EnableOverset(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EnableOverset.
                    """

                class _IdentifyRegions(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IdentifyRegions.
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
        CollarGrid : str
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
                Argument ComponentGrid.
                """

            class _CollarGrid(PyTextualCommandArgumentsSubItem):
                """
                Argument CollarGrid.
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
        ExtractMethodType : str
        SelectionType : str
        ObjectSelectionList : list[str]
        GeomObjectSelectionList : list[str]
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
        FeatureAngleLocal : int
        IndividualCollective : str
        SharpAngle : int
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
                Argument ExtractEdgesName.
                """

            class _ExtractMethodType(PyTextualCommandArgumentsSubItem):
                """
                Argument ExtractMethodType.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _GeomObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument GeomObjectSelectionList.
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

            class _FeatureAngleLocal(PyNumericalCommandArgumentsSubItem):
                """
                Argument FeatureAngleLocal.
                """

            class _IndividualCollective(PyTextualCommandArgumentsSubItem):
                """
                Argument IndividualCollective.
                """

            class _SharpAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument SharpAngle.
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
        Method : str
        ExternalBoundaryZoneList : list[str]
        TotalHeight : float
        FirstHeight : float
        NumberofLayers : int
        GrowthRate : float
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
                self.ExternalBoundaryZoneList = self._ExternalBoundaryZoneList(self, "ExternalBoundaryZoneList", service, rules, path)
                self.TotalHeight = self._TotalHeight(self, "TotalHeight", service, rules, path)
                self.FirstHeight = self._FirstHeight(self, "FirstHeight", service, rules, path)
                self.NumberofLayers = self._NumberofLayers(self, "NumberofLayers", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.VMExtrudePreferences = self._VMExtrudePreferences(self, "VMExtrudePreferences", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _MExControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument MExControlName.
                """

            class _Method(PyTextualCommandArgumentsSubItem):
                """
                Argument Method.
                """

            class _ExternalBoundaryZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ExternalBoundaryZoneList.
                """

            class _TotalHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument TotalHeight.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstHeight.
                """

            class _NumberofLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberofLayers.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument GrowthRate.
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
        MinSize : float
        MaxSize : float
        GrowthRate : float
        SizeFunctions : str
        CurvatureNormalAngle : float
        CellsPerGap : float
        PrimeMeshPreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _GenerateInitialSurfaceMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.MinSize = self._MinSize(self, "MinSize", service, rules, path)
                self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                self.SizeFunctions = self._SizeFunctions(self, "SizeFunctions", service, rules, path)
                self.CurvatureNormalAngle = self._CurvatureNormalAngle(self, "CurvatureNormalAngle", service, rules, path)
                self.CellsPerGap = self._CellsPerGap(self, "CellsPerGap", service, rules, path)
                self.PrimeMeshPreferences = self._PrimeMeshPreferences(self, "PrimeMeshPreferences", service, rules, path)

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

            class _PrimeMeshPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument PrimeMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.GenerateQuads = self._GenerateQuads(self, "GenerateQuads", service, rules, path)
                    self.ShowPrimeMeshPreferences = self._ShowPrimeMeshPreferences(self, "ShowPrimeMeshPreferences", service, rules, path)

                class _GenerateQuads(PyTextualCommandArgumentsSubItem):
                    """
                    Argument GenerateQuads.
                    """

                class _ShowPrimeMeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowPrimeMeshPreferences.
                    """

        def create_instance(self) -> _GenerateInitialSurfaceMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._GenerateInitialSurfaceMeshCommandArguments(*args)

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

    class GenerateTheMultiZoneMesh(PyCommand):
        """
        Command GenerateTheMultiZoneMesh.

        Parameters
        ----------
        OrthogonalQualityLimit : float
        RegionScope : list[str]
        NonConformal : str
        SizeFunctionScaleFactor : float
        CFDSurfaceMeshControls : dict[str, Any]
        CompleteRegionScope : list[str]

        Returns
        -------
        bool
        """
        class _GenerateTheMultiZoneMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.OrthogonalQualityLimit = self._OrthogonalQualityLimit(self, "OrthogonalQualityLimit", service, rules, path)
                self.RegionScope = self._RegionScope(self, "RegionScope", service, rules, path)
                self.NonConformal = self._NonConformal(self, "NonConformal", service, rules, path)
                self.SizeFunctionScaleFactor = self._SizeFunctionScaleFactor(self, "SizeFunctionScaleFactor", service, rules, path)
                self.CFDSurfaceMeshControls = self._CFDSurfaceMeshControls(self, "CFDSurfaceMeshControls", service, rules, path)
                self.CompleteRegionScope = self._CompleteRegionScope(self, "CompleteRegionScope", service, rules, path)

            class _OrthogonalQualityLimit(PyNumericalCommandArgumentsSubItem):
                """
                Argument OrthogonalQualityLimit.
                """

            class _RegionScope(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionScope.
                """

            class _NonConformal(PyTextualCommandArgumentsSubItem):
                """
                Argument NonConformal.
                """

            class _SizeFunctionScaleFactor(PyNumericalCommandArgumentsSubItem):
                """
                Argument SizeFunctionScaleFactor.
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
        SaveSurfaceMesh : bool
        AdvancedOptions : bool
        SaveIntermediateFiles : str
        IntermediateFileName : str
        SeparateSurface : str
        AutoPairing : str
        ParallelSerialOption : str
        NumberOfSessions : int
        MaxIslandFace : int
        SpikeRemovalAngle : float
        DihedralMinAngle : float
        ProjectOnGeometry : str
        AutoAssignZoneTypes : str
        AdvancedInnerWrap : str
        GapCoverZoneRecovery : str
        GlobalMin : float
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
                self.AutoPairing = self._AutoPairing(self, "AutoPairing", service, rules, path)
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
                Argument SurfaceQuality.
                """

            class _SaveSurfaceMesh(PyParameterCommandArgumentsSubItem):
                """
                Argument SaveSurfaceMesh.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Argument AdvancedOptions.
                """

            class _SaveIntermediateFiles(PyTextualCommandArgumentsSubItem):
                """
                Argument SaveIntermediateFiles.
                """

            class _IntermediateFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument IntermediateFileName.
                """

            class _SeparateSurface(PyTextualCommandArgumentsSubItem):
                """
                Argument SeparateSurface.
                """

            class _AutoPairing(PyTextualCommandArgumentsSubItem):
                """
                Argument AutoPairing.
                """

            class _ParallelSerialOption(PyTextualCommandArgumentsSubItem):
                """
                Argument ParallelSerialOption.
                """

            class _NumberOfSessions(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfSessions.
                """

            class _MaxIslandFace(PyNumericalCommandArgumentsSubItem):
                """
                Argument MaxIslandFace.
                """

            class _SpikeRemovalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument SpikeRemovalAngle.
                """

            class _DihedralMinAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument DihedralMinAngle.
                """

            class _ProjectOnGeometry(PyTextualCommandArgumentsSubItem):
                """
                Argument ProjectOnGeometry.
                """

            class _AutoAssignZoneTypes(PyTextualCommandArgumentsSubItem):
                """
                Argument AutoAssignZoneTypes.
                """

            class _AdvancedInnerWrap(PyTextualCommandArgumentsSubItem):
                """
                Argument AdvancedInnerWrap.
                """

            class _GapCoverZoneRecovery(PyTextualCommandArgumentsSubItem):
                """
                Argument GapCoverZoneRecovery.
                """

            class _GlobalMin(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalMin.
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
        SeparationAngle : float
        RemeshSelectionType : str
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
                Argument SeparationRequired.
                """

            class _SeparationAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument SeparationAngle.
                """

            class _RemeshSelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshSelectionType.
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
                    self.FoldFaceLimit = self._FoldFaceLimit(self, "FoldFaceLimit", service, rules, path)
                    self.SMQualityImprove = self._SMQualityImprove(self, "SMQualityImprove", service, rules, path)
                    self.SMSeparationAngle = self._SMSeparationAngle(self, "SMSeparationAngle", service, rules, path)
                    self.SMSeparation = self._SMSeparation(self, "SMSeparation", service, rules, path)
                    self.AutoMerge = self._AutoMerge(self, "AutoMerge", service, rules, path)
                    self.ShowSurfaceMeshPreferences = self._ShowSurfaceMeshPreferences(self, "ShowSurfaceMeshPreferences", service, rules, path)
                    self.SMRemoveStep = self._SMRemoveStep(self, "SMRemoveStep", service, rules, path)
                    self.SMStepWidth = self._SMStepWidth(self, "SMStepWidth", service, rules, path)
                    self.VolumeMeshMaxSize = self._VolumeMeshMaxSize(self, "VolumeMeshMaxSize", service, rules, path)
                    self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                    self.SMQualityMaxAngle = self._SMQualityMaxAngle(self, "SMQualityMaxAngle", service, rules, path)
                    self.SMQualityImproveLimit = self._SMQualityImproveLimit(self, "SMQualityImproveLimit", service, rules, path)
                    self.AutoSurfaceRemesh = self._AutoSurfaceRemesh(self, "AutoSurfaceRemesh", service, rules, path)
                    self.SelfIntersectCheck = self._SelfIntersectCheck(self, "SelfIntersectCheck", service, rules, path)
                    self.SetVolumeMeshMaxSize = self._SetVolumeMeshMaxSize(self, "SetVolumeMeshMaxSize", service, rules, path)

                class _SMQualityCollapseLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityCollapseLimit.
                    """

                class _FoldFaceLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FoldFaceLimit.
                    """

                class _SMQualityImprove(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMQualityImprove.
                    """

                class _SMSeparationAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMSeparationAngle.
                    """

                class _SMSeparation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SMSeparation.
                    """

                class _AutoMerge(PyParameterCommandArgumentsSubItem):
                    """
                    Argument AutoMerge.
                    """

                class _ShowSurfaceMeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSurfaceMeshPreferences.
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

                class _SMQualityImproveLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityImproveLimit.
                    """

                class _AutoSurfaceRemesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoSurfaceRemesh.
                    """

                class _SelfIntersectCheck(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SelfIntersectCheck.
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
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)
                    self.ExtractFeatures = self._ExtractFeatures(self, "ExtractFeatures", service, rules, path)
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

                class _ImportNamedSelections(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

                class _ExtractFeatures(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ExtractFeatures.
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
                    self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                    self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                    self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                    self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                    self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                    self.ConnectLabelWildcard = self._ConnectLabelWildcard(self, "ConnectLabelWildcard", service, rules, path)
                    self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                    self.RelativeShareTopologyTolerance = self._RelativeShareTopologyTolerance(self, "RelativeShareTopologyTolerance", service, rules, path)
                    self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                    self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)
                    self.Operation = self._Operation(self, "Operation", service, rules, path)

                class _STRenameInternals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument STRenameInternals.
                    """

                class _ModelIsPeriodic(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModelIsPeriodic.
                    """

                class _STToleranceIncrement(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument STToleranceIncrement.
                    """

                class _IntfLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IntfLabelList.
                    """

                class _PerLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PerLabelList.
                    """

                class _ShowShareTopologyPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowShareTopologyPreferences.
                    """

                class _FluidLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FluidLabelWildcard.
                    """

                class _ConnectLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ConnectLabelWildcard.
                    """

                class _ExecuteJoinIntersect(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExecuteJoinIntersect.
                    """

                class _RelativeShareTopologyTolerance(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RelativeShareTopologyTolerance.
                    """

                class _ShareTopologyAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShareTopologyAngle.
                    """

                class _NumberOfJoinTries(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfJoinTries.
                    """

                class _Operation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Operation.
                    """

            class _PreviewSizeToggle(PyParameterCommandArgumentsSubItem):
                """
                Argument PreviewSizeToggle.
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
        EnableParallel : bool
        SaveVolumeMesh : bool
        EditVolumeSettings : bool
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
        SpikeRemovalAngle : float
        DihedralMinAngle : float
        AvoidHangingNodes : str
        OctreePeelLayers : int
        FillWithSizeField : str
        OctreeBoundaryFaceSizeRatio : float
        GlobalBufferLayers : int
        TetPolyGrowthRate : float
        ConformalPrismSplit : str
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
                self.AvoidHangingNodes = self._AvoidHangingNodes(self, "AvoidHangingNodes", service, rules, path)
                self.OctreePeelLayers = self._OctreePeelLayers(self, "OctreePeelLayers", service, rules, path)
                self.FillWithSizeField = self._FillWithSizeField(self, "FillWithSizeField", service, rules, path)
                self.OctreeBoundaryFaceSizeRatio = self._OctreeBoundaryFaceSizeRatio(self, "OctreeBoundaryFaceSizeRatio", service, rules, path)
                self.GlobalBufferLayers = self._GlobalBufferLayers(self, "GlobalBufferLayers", service, rules, path)
                self.TetPolyGrowthRate = self._TetPolyGrowthRate(self, "TetPolyGrowthRate", service, rules, path)
                self.ConformalPrismSplit = self._ConformalPrismSplit(self, "ConformalPrismSplit", service, rules, path)
                self.ShowSubTasks = self._ShowSubTasks(self, "ShowSubTasks", service, rules, path)

            class _MeshQuality(PyNumericalCommandArgumentsSubItem):
                """
                Argument MeshQuality.
                """

            class _OrthogonalQuality(PyNumericalCommandArgumentsSubItem):
                """
                Argument OrthogonalQuality.
                """

            class _EnableParallel(PyParameterCommandArgumentsSubItem):
                """
                Argument EnableParallel.
                """

            class _SaveVolumeMesh(PyParameterCommandArgumentsSubItem):
                """
                Argument SaveVolumeMesh.
                """

            class _EditVolumeSettings(PyParameterCommandArgumentsSubItem):
                """
                Argument EditVolumeSettings.
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
                Argument AdvancedOptions.
                """

            class _SpikeRemovalAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument SpikeRemovalAngle.
                """

            class _DihedralMinAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument DihedralMinAngle.
                """

            class _AvoidHangingNodes(PyTextualCommandArgumentsSubItem):
                """
                Argument AvoidHangingNodes.
                """

            class _OctreePeelLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument OctreePeelLayers.
                """

            class _FillWithSizeField(PyTextualCommandArgumentsSubItem):
                """
                Argument FillWithSizeField.
                """

            class _OctreeBoundaryFaceSizeRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument OctreeBoundaryFaceSizeRatio.
                """

            class _GlobalBufferLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument GlobalBufferLayers.
                """

            class _TetPolyGrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument TetPolyGrowthRate.
                """

            class _ConformalPrismSplit(PyTextualCommandArgumentsSubItem):
                """
                Argument ConformalPrismSplit.
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
        VolumeFill : str
        MeshFluidRegions : bool
        MeshSolidRegions : bool
        SizingMethod : str
        VolumeFillControls : dict[str, Any]
        RegionBasedPreferences : bool
        ReMergeZones : str
        ParallelMeshing : bool
        VolumeMeshPreferences : dict[str, Any]
        PrismPreferences : dict[str, Any]
        InvokePrimsControl : str
        OffsetMethodType : str
        NumberOfLayers : int
        FirstAspectRatio : float
        TransitionRatio : float
        Rate : float
        FirstHeight : float
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

            class _Solver(PyTextualCommandArgumentsSubItem):
                """
                Argument Solver.
                """

            class _VolumeFill(PyTextualCommandArgumentsSubItem):
                """
                Argument VolumeFill.
                """

            class _MeshFluidRegions(PyParameterCommandArgumentsSubItem):
                """
                Argument MeshFluidRegions.
                """

            class _MeshSolidRegions(PyParameterCommandArgumentsSubItem):
                """
                Argument MeshSolidRegions.
                """

            class _SizingMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument SizingMethod.
                """

            class _VolumeFillControls(PySingletonCommandArgumentsSubItem):
                """
                Argument VolumeFillControls.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.HexMinCellLength = self._HexMinCellLength(self, "HexMinCellLength", service, rules, path)
                    self.TetPolyMaxCellLength = self._TetPolyMaxCellLength(self, "TetPolyMaxCellLength", service, rules, path)
                    self.PeelLayers = self._PeelLayers(self, "PeelLayers", service, rules, path)
                    self.Type = self._Type(self, "Type", service, rules, path)
                    self.CellSizing = self._CellSizing(self, "CellSizing", service, rules, path)
                    self.HexMaxCellLength = self._HexMaxCellLength(self, "HexMaxCellLength", service, rules, path)
                    self.GrowthRate = self._GrowthRate(self, "GrowthRate", service, rules, path)
                    self.BufferLayers = self._BufferLayers(self, "BufferLayers", service, rules, path)

                class _HexMinCellLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HexMinCellLength.
                    """

                class _TetPolyMaxCellLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument TetPolyMaxCellLength.
                    """

                class _PeelLayers(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PeelLayers.
                    """

                class _Type(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Type.
                    """

                class _CellSizing(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CellSizing.
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
                Argument ReMergeZones.
                """

            class _ParallelMeshing(PyParameterCommandArgumentsSubItem):
                """
                Argument ParallelMeshing.
                """

            class _VolumeMeshPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument VolumeMeshPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.ShowVolumeMeshPreferences = self._ShowVolumeMeshPreferences(self, "ShowVolumeMeshPreferences", service, rules, path)
                    self.WritePrismControlFile = self._WritePrismControlFile(self, "WritePrismControlFile", service, rules, path)
                    self.PrepareZoneNames = self._PrepareZoneNames(self, "PrepareZoneNames", service, rules, path)
                    self.CheckSelfProximity = self._CheckSelfProximity(self, "CheckSelfProximity", service, rules, path)
                    self.Avoid1_8Transition = self._Avoid1_8Transition(self, "Avoid1_8Transition", service, rules, path)
                    self.UseSizeField = self._UseSizeField(self, "UseSizeField", service, rules, path)
                    self.PolyFeatureAngle = self._PolyFeatureAngle(self, "PolyFeatureAngle", service, rules, path)
                    self.SolidGrowthRate = self._SolidGrowthRate(self, "SolidGrowthRate", service, rules, path)
                    self.MergeBodyLabels = self._MergeBodyLabels(self, "MergeBodyLabels", service, rules, path)
                    self.QualityWarningLimit = self._QualityWarningLimit(self, "QualityWarningLimit", service, rules, path)
                    self.PolyInSolids = self._PolyInSolids(self, "PolyInSolids", service, rules, path)

                class _ShowVolumeMeshPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowVolumeMeshPreferences.
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

                class _UseSizeField(PyTextualCommandArgumentsSubItem):
                    """
                    Argument UseSizeField.
                    """

                class _PolyFeatureAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PolyFeatureAngle.
                    """

                class _SolidGrowthRate(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SolidGrowthRate.
                    """

                class _MergeBodyLabels(PyTextualCommandArgumentsSubItem):
                    """
                    Argument MergeBodyLabels.
                    """

                class _QualityWarningLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument QualityWarningLimit.
                    """

                class _PolyInSolids(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PolyInSolids.
                    """

            class _PrismPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument PrismPreferences.
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

                class _PrismMinAspectRatio(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PrismMinAspectRatio.
                    """

                class _PrismAdjacentAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument PrismAdjacentAngle.
                    """

            class _InvokePrimsControl(PyTextualCommandArgumentsSubItem):
                """
                Argument InvokePrimsControl.
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

            class _Rate(PyNumericalCommandArgumentsSubItem):
                """
                Argument Rate.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstHeight.
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
        CappingRequired : str
        WallToInternal : str
        InvokeShareTopology : str
        NonConformal : str
        Multizone : str
        SetupInternals : list[str]
        SetupInternalTypes : list[str]
        OldZoneList : list[str]
        OldZoneTypeList : list[str]
        RegionList : list[str]
        EdgeLabels : list[str]
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
                self.EdgeLabels = self._EdgeLabels(self, "EdgeLabels", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)

            class _SetupType(PyTextualCommandArgumentsSubItem):
                """
                Argument SetupType.
                """

            class _CappingRequired(PyTextualCommandArgumentsSubItem):
                """
                Argument CappingRequired.
                """

            class _WallToInternal(PyTextualCommandArgumentsSubItem):
                """
                Argument WallToInternal.
                """

            class _InvokeShareTopology(PyTextualCommandArgumentsSubItem):
                """
                Argument InvokeShareTopology.
                """

            class _NonConformal(PyTextualCommandArgumentsSubItem):
                """
                Argument NonConformal.
                """

            class _Multizone(PyTextualCommandArgumentsSubItem):
                """
                Argument Multizone.
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

            class _EdgeLabels(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeLabels.
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
                    self.SIRemoveStep = self._SIRemoveStep(self, "SIRemoveStep", service, rules, path)
                    self.ShowSMImprovePreferences = self._ShowSMImprovePreferences(self, "ShowSMImprovePreferences", service, rules, path)
                    self.SIStepWidth = self._SIStepWidth(self, "SIStepWidth", service, rules, path)

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

                class _SIRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SIRemoveStep.
                    """

                class _ShowSMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _SIStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepWidth.
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
        CreationMethod : str
        SelectionType : str
        ObjectSelectionSingle : list[str]
        ZoneSelectionSingle : list[str]
        LabelSelectionSingle : list[str]
        ObjectSelectionList : list[str]
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
        DefeaturingSize : float
        OffsetHeight : float
        Pivot : dict[str, Any]
        Axis : dict[str, Any]
        Rotation : dict[str, Any]
        CylinderObject : dict[str, Any]
        BoundingBoxObject : dict[str, Any]

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
                self.BoundingBoxObject = self._BoundingBoxObject(self, "BoundingBoxObject", service, rules, path)

            class _MRFName(PyTextualCommandArgumentsSubItem):
                """
                Argument MRFName.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CreationMethod.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ObjectSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionSingle.
                """

            class _ZoneSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionSingle.
                """

            class _LabelSelectionSingle(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionSingle.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
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

            class _DefeaturingSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument DefeaturingSize.
                """

            class _OffsetHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument OffsetHeight.
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
                    self.HeightNode = self._HeightNode(self, "HeightNode", service, rules, path)
                    self.Radius2 = self._Radius2(self, "Radius2", service, rules, path)
                    self.Options = self._Options(self, "Options", service, rules, path)
                    self.HeightBackInc = self._HeightBackInc(self, "HeightBackInc", service, rules, path)
                    self.Node3 = self._Node3(self, "Node3", service, rules, path)
                    self.Node2 = self._Node2(self, "Node2", service, rules, path)
                    self.HeightFrontInc = self._HeightFrontInc(self, "HeightFrontInc", service, rules, path)
                    self.Radius1 = self._Radius1(self, "Radius1", service, rules, path)
                    self.Node1 = self._Node1(self, "Node1", service, rules, path)

                class _HeightNode(PyTextualCommandArgumentsSubItem):
                    """
                    Argument HeightNode.
                    """

                class _Radius2(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Radius2.
                    """

                class _Options(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Options.
                    """

                class _HeightBackInc(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument HeightBackInc.
                    """

                class _Node3(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node3.
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

                class _Node1(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Node1.
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
        SelectionType : str
        ObjectSelectionList : list[str]
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        AdvancedOptions : bool
        DeviationMinValue : float
        DeviationMaxValue : float
        Overlay : str
        IncludeGapCoverGeometry : str

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
                Argument DisplayGridName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Argument AdvancedOptions.
                """

            class _DeviationMinValue(PyNumericalCommandArgumentsSubItem):
                """
                Argument DeviationMinValue.
                """

            class _DeviationMaxValue(PyNumericalCommandArgumentsSubItem):
                """
                Argument DeviationMaxValue.
                """

            class _Overlay(PyTextualCommandArgumentsSubItem):
                """
                Argument Overlay.
                """

            class _IncludeGapCoverGeometry(PyTextualCommandArgumentsSubItem):
                """
                Argument IncludeGapCoverGeometry.
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
        ObjectSelectionList : list[str]
        EnableGridPriority : bool
        DonorPriorityMethod : str
        OverlapBoundaries : str
        CheckOversetInterfaceIntersection : str
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
                Argument NumberOfOrphans.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _EnableGridPriority(PyParameterCommandArgumentsSubItem):
                """
                Argument EnableGridPriority.
                """

            class _DonorPriorityMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument DonorPriorityMethod.
                """

            class _OverlapBoundaries(PyTextualCommandArgumentsSubItem):
                """
                Argument OverlapBoundaries.
                """

            class _CheckOversetInterfaceIntersection(PyTextualCommandArgumentsSubItem):
                """
                Argument CheckOversetInterfaceIntersection.
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
        MaterialPointsName : str
        MptMethodType : str
        NewRegionType : str
        LinkConstruction : str
        SelectionType : str
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        LabelSelectionList : list[str]
        ObjectSelectionList : list[str]
        GraphicalSelection : bool
        ShowCoordinates : bool
        X : float
        Y : float
        Z : float
        OffsetX : float
        OffsetY : float
        OffsetZ : float

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
                Argument AddChild.
                """

            class _MaterialPointsName(PyTextualCommandArgumentsSubItem):
                """
                Argument MaterialPointsName.
                """

            class _MptMethodType(PyTextualCommandArgumentsSubItem):
                """
                Argument MptMethodType.
                """

            class _NewRegionType(PyTextualCommandArgumentsSubItem):
                """
                Argument NewRegionType.
                """

            class _LinkConstruction(PyTextualCommandArgumentsSubItem):
                """
                Argument LinkConstruction.
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

            class _GraphicalSelection(PyParameterCommandArgumentsSubItem):
                """
                Argument GraphicalSelection.
                """

            class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                """
                Argument ShowCoordinates.
                """

            class _X(PyNumericalCommandArgumentsSubItem):
                """
                Argument X.
                """

            class _Y(PyNumericalCommandArgumentsSubItem):
                """
                Argument Y.
                """

            class _Z(PyNumericalCommandArgumentsSubItem):
                """
                Argument Z.
                """

            class _OffsetX(PyNumericalCommandArgumentsSubItem):
                """
                Argument OffsetX.
                """

            class _OffsetY(PyNumericalCommandArgumentsSubItem):
                """
                Argument OffsetY.
                """

            class _OffsetZ(PyNumericalCommandArgumentsSubItem):
                """
                Argument OffsetZ.
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
        LengthUnit : str
        Type : str
        GeometryFileName : str
        MeshFileName : str
        ImportedObjects : list[str]
        CadImportOptions : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImportBodyOfInfluenceGeometryCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.Type = self._Type(self, "Type", service, rules, path)
                self.GeometryFileName = self._GeometryFileName(self, "GeometryFileName", service, rules, path)
                self.MeshFileName = self._MeshFileName(self, "MeshFileName", service, rules, path)
                self.ImportedObjects = self._ImportedObjects(self, "ImportedObjects", service, rules, path)
                self.CadImportOptions = self._CadImportOptions(self, "CadImportOptions", service, rules, path)

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument LengthUnit.
                """

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Argument Type.
                """

            class _GeometryFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument GeometryFileName.
                """

            class _MeshFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshFileName.
                """

            class _ImportedObjects(PyTextualCommandArgumentsSubItem):
                """
                Argument ImportedObjects.
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
        LengthUnit : str
        MeshUnit : str
        ImportCadPreferences : dict[str, Any]
        FileName : str
        FileNames : str
        MeshFileName : str
        NumParts : float
        ImportType : str
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
                self.LengthUnit = self._LengthUnit(self, "LengthUnit", service, rules, path)
                self.MeshUnit = self._MeshUnit(self, "MeshUnit", service, rules, path)
                self.ImportCadPreferences = self._ImportCadPreferences(self, "ImportCadPreferences", service, rules, path)
                self.FileName = self._FileName(self, "FileName", service, rules, path)
                self.FileNames = self._FileNames(self, "FileNames", service, rules, path)
                self.MeshFileName = self._MeshFileName(self, "MeshFileName", service, rules, path)
                self.NumParts = self._NumParts(self, "NumParts", service, rules, path)
                self.ImportType = self._ImportType(self, "ImportType", service, rules, path)
                self.AppendMesh = self._AppendMesh(self, "AppendMesh", service, rules, path)
                self.Directory = self._Directory(self, "Directory", service, rules, path)
                self.Pattern = self._Pattern(self, "Pattern", service, rules, path)
                self.CadImportOptions = self._CadImportOptions(self, "CadImportOptions", service, rules, path)

            class _FileFormat(PyTextualCommandArgumentsSubItem):
                """
                Argument FileFormat.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument LengthUnit.
                """

            class _MeshUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshUnit.
                """

            class _ImportCadPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument ImportCadPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.EdgeLabel = self._EdgeLabel(self, "EdgeLabel", service, rules, path)
                    self.CISeparation = self._CISeparation(self, "CISeparation", service, rules, path)
                    self.CIRefaceting = self._CIRefaceting(self, "CIRefaceting", service, rules, path)
                    self.AutomaticObjectCreation = self._AutomaticObjectCreation(self, "AutomaticObjectCreation", service, rules, path)
                    self.ShowImportCadPreferences = self._ShowImportCadPreferences(self, "ShowImportCadPreferences", service, rules, path)
                    self.MaxFacetLength = self._MaxFacetLength(self, "MaxFacetLength", service, rules, path)
                    self.CISeparationAngle = self._CISeparationAngle(self, "CISeparationAngle", service, rules, path)
                    self.CITolerence = self._CITolerence(self, "CITolerence", service, rules, path)

                class _EdgeLabel(PyTextualCommandArgumentsSubItem):
                    """
                    Argument EdgeLabel.
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

                class _ShowImportCadPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowImportCadPreferences.
                    """

                class _MaxFacetLength(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxFacetLength.
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
                Argument FileName.
                """

            class _FileNames(PyTextualCommandArgumentsSubItem):
                """
                Argument FileNames.
                """

            class _MeshFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshFileName.
                """

            class _NumParts(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumParts.
                """

            class _ImportType(PyTextualCommandArgumentsSubItem):
                """
                Argument ImportType.
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
                    self.ImportCurvatureDataFromCAD = self._ImportCurvatureDataFromCAD(self, "ImportCurvatureDataFromCAD", service, rules, path)
                    self.ImportNamedSelections = self._ImportNamedSelections(self, "ImportNamedSelections", service, rules, path)
                    self.ExtractFeatures = self._ExtractFeatures(self, "ExtractFeatures", service, rules, path)
                    self.ImportPartNames = self._ImportPartNames(self, "ImportPartNames", service, rules, path)
                    self.UsePartOrBodyAsSuffix = self._UsePartOrBodyAsSuffix(self, "UsePartOrBodyAsSuffix", service, rules, path)

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

                class _ImportNamedSelections(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportNamedSelections.
                    """

                class _ExtractFeatures(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ExtractFeatures.
                    """

                class _ImportPartNames(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ImportPartNames.
                    """

                class _UsePartOrBodyAsSuffix(PyParameterCommandArgumentsSubItem):
                    """
                    Argument UsePartOrBodyAsSuffix.
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
        SQMinSize : float
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
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _FaceQualityLimit(PyNumericalCommandArgumentsSubItem):
                """
                Argument FaceQualityLimit.
                """

            class _SQMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument SQMinSize.
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
                    self.SIRemoveStep = self._SIRemoveStep(self, "SIRemoveStep", service, rules, path)
                    self.ShowSMImprovePreferences = self._ShowSMImprovePreferences(self, "ShowSMImprovePreferences", service, rules, path)
                    self.SIStepWidth = self._SIStepWidth(self, "SIStepWidth", service, rules, path)

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

                class _SIRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SIRemoveStep.
                    """

                class _ShowSMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _SIStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepWidth.
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
        CellQualityLimit : float
        VMImprovePreferences : dict[str, Any]

        Returns
        -------
        bool
        """
        class _ImproveVolumeMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.CellQualityLimit = self._CellQualityLimit(self, "CellQualityLimit", service, rules, path)
                self.VMImprovePreferences = self._VMImprovePreferences(self, "VMImprovePreferences", service, rules, path)

            class _CellQualityLimit(PyNumericalCommandArgumentsSubItem):
                """
                Argument CellQualityLimit.
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
        ObjectList : list[str]
        AutoPopulateVector : str
        PatternVector : dict[str, Any]
        Pitch : float
        NumberOfUnits : int
        CheckOverlappingFaces : str
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
                Argument ChildName.
                """

            class _ObjectList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectList.
                """

            class _AutoPopulateVector(PyTextualCommandArgumentsSubItem):
                """
                Argument AutoPopulateVector.
                """

            class _PatternVector(PySingletonCommandArgumentsSubItem):
                """
                Argument PatternVector.
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
                Argument Pitch.
                """

            class _NumberOfUnits(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumberOfUnits.
                """

            class _CheckOverlappingFaces(PyTextualCommandArgumentsSubItem):
                """
                Argument CheckOverlappingFaces.
                """

            class _BatteryModelingOptions(PySingletonCommandArgumentsSubItem):
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

                class _FirstNumber(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FirstNumber.
                    """

                class _NbCellsPerUnit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NbCellsPerUnit.
                    """

                class _CustomPatternString(PyTextualCommandArgumentsSubItem):
                    """
                    Argument CustomPatternString.
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
        CreateObjectPer : str
        NumParts : float
        2DRefaceting : dict[str, Any]

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
                self.CreateObjectPer = self._CreateObjectPer(self, "CreateObjectPer", service, rules, path)
                self.NumParts = self._NumParts(self, "NumParts", service, rules, path)
                self.TwoDRefaceting = self._TwoDRefaceting(self, "2DRefaceting", service, rules, path)

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

            class _CreateObjectPer(PyTextualCommandArgumentsSubItem):
                """
                Argument CreateObjectPer.
                """

            class _NumParts(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumParts.
                """

            class _TwoDRefaceting(PySingletonCommandArgumentsSubItem):
                """
                Argument 2DRefaceting.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Refacet = self._Refacet(self, "Refacet", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Deviation.
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NormalAngle.
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
        SelectionType : str
        ObjectSelectionList : list[str]
        LabelSelectionList : list[str]
        ZoneSelectionList : list[str]
        ZoneLocation : list[str]
        EdgeSelectionList : list[str]
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
                Argument LocalSettingsName.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
                """

            class _ObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSelectionList.
                """

            class _LabelSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelSelectionList.
                """

            class _ZoneSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneSelectionList.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _EdgeSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument EdgeSelectionList.
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
                    self.SizingType = self._SizingType(self, "SizingType", service, rules, path)
                    self.InitialSizeControl = self._InitialSizeControl(self, "InitialSizeControl", service, rules, path)
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

                class _SizingType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SizingType.
                    """

                class _InitialSizeControl(PyParameterCommandArgumentsSubItem):
                    """
                    Argument InitialSizeControl.
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
        ZoneFilter : str
        SizeFilter : str
        Area : float
        Volume : float
        EqualRange : float
        ZoneOrLabel : str
        LabelList : list[str]
        ManageFaceZoneList : list[str]
        ManageCellZoneList : list[str]
        BodyLabelList : list[str]
        Operation : str
        OperationName : str
        MZChildName : str
        AddPrefixName : str
        FaceMerge : str
        Angle : float
        ZoneList : list[str]
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
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Argument Type.
                """

            class _ZoneFilter(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneFilter.
                """

            class _SizeFilter(PyTextualCommandArgumentsSubItem):
                """
                Argument SizeFilter.
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
                Argument EqualRange.
                """

            class _ZoneOrLabel(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneOrLabel.
                """

            class _LabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelList.
                """

            class _ManageFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ManageFaceZoneList.
                """

            class _ManageCellZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ManageCellZoneList.
                """

            class _BodyLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument BodyLabelList.
                """

            class _Operation(PyTextualCommandArgumentsSubItem):
                """
                Argument Operation.
                """

            class _OperationName(PyTextualCommandArgumentsSubItem):
                """
                Argument OperationName.
                """

            class _MZChildName(PyTextualCommandArgumentsSubItem):
                """
                Argument MZChildName.
                """

            class _AddPrefixName(PyTextualCommandArgumentsSubItem):
                """
                Argument AddPrefixName.
                """

            class _FaceMerge(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceMerge.
                """

            class _Angle(PyNumericalCommandArgumentsSubItem):
                """
                Argument Angle.
                """

            class _ZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneList.
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
        RemeshControlName : str
        LocalSize : float
        FaceZoneOrLabel : str
        RemeshFaceZoneList : list[str]
        RemeshFaceLabelList : list[str]
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
                Argument RemeshExecution.
                """

            class _RemeshControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshControlName.
                """

            class _LocalSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument LocalSize.
                """

            class _FaceZoneOrLabel(PyTextualCommandArgumentsSubItem):
                """
                Argument FaceZoneOrLabel.
                """

            class _RemeshFaceZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshFaceZoneList.
                """

            class _RemeshFaceLabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshFaceLabelList.
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
        AppendFileName : str
        Append : bool
        LengthUnit : str
        CreateObjectPer : str
        FileLengthUnit : str
        FileLengthUnitAppend : str
        Route : str
        RouteAppend : str
        JtLOD : str
        JtLODAppend : str
        PartPerBody : bool
        PrefixParentName : bool
        RemoveEmptyParts : bool
        FeatureAngle : float
        OneZonePer : str
        Refaceting : dict[str, Any]
        IgnoreSolidNames : bool
        IgnoreSolidNamesAppend : bool
        Options : dict[str, Any]
        EdgeExtraction : str
        Context : int
        ObjectSetting : str

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

            class _FileLoaded(PyTextualCommandArgumentsSubItem):
                """
                Argument FileLoaded.
                """

            class _FMDFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument FMDFileName.
                """

            class _AppendFileName(PyTextualCommandArgumentsSubItem):
                """
                Argument AppendFileName.
                """

            class _Append(PyParameterCommandArgumentsSubItem):
                """
                Argument Append.
                """

            class _LengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument LengthUnit.
                """

            class _CreateObjectPer(PyTextualCommandArgumentsSubItem):
                """
                Argument CreateObjectPer.
                """

            class _FileLengthUnit(PyTextualCommandArgumentsSubItem):
                """
                Argument FileLengthUnit.
                """

            class _FileLengthUnitAppend(PyTextualCommandArgumentsSubItem):
                """
                Argument FileLengthUnitAppend.
                """

            class _Route(PyTextualCommandArgumentsSubItem):
                """
                Argument Route.
                """

            class _RouteAppend(PyTextualCommandArgumentsSubItem):
                """
                Argument RouteAppend.
                """

            class _JtLOD(PyTextualCommandArgumentsSubItem):
                """
                Argument JtLOD.
                """

            class _JtLODAppend(PyTextualCommandArgumentsSubItem):
                """
                Argument JtLODAppend.
                """

            class _PartPerBody(PyParameterCommandArgumentsSubItem):
                """
                Argument PartPerBody.
                """

            class _PrefixParentName(PyParameterCommandArgumentsSubItem):
                """
                Argument PrefixParentName.
                """

            class _RemoveEmptyParts(PyParameterCommandArgumentsSubItem):
                """
                Argument RemoveEmptyParts.
                """

            class _FeatureAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument FeatureAngle.
                """

            class _OneZonePer(PyTextualCommandArgumentsSubItem):
                """
                Argument OneZonePer.
                """

            class _Refaceting(PySingletonCommandArgumentsSubItem):
                """
                Argument Refaceting.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.MaxSize = self._MaxSize(self, "MaxSize", service, rules, path)
                    self.Deviation = self._Deviation(self, "Deviation", service, rules, path)
                    self.NormalAngle = self._NormalAngle(self, "NormalAngle", service, rules, path)
                    self.Refacet = self._Refacet(self, "Refacet", service, rules, path)

                class _MaxSize(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument MaxSize.
                    """

                class _Deviation(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument Deviation.
                    """

                class _NormalAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NormalAngle.
                    """

                class _Refacet(PyParameterCommandArgumentsSubItem):
                    """
                    Argument Refacet.
                    """

            class _IgnoreSolidNames(PyParameterCommandArgumentsSubItem):
                """
                Argument IgnoreSolidNames.
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
                Argument EdgeExtraction.
                """

            class _Context(PyNumericalCommandArgumentsSubItem):
                """
                Argument Context.
                """

            class _ObjectSetting(PyTextualCommandArgumentsSubItem):
                """
                Argument ObjectSetting.
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
        ManagementMethod : str
        CreationMethod : str
        OldObjectSelectionList : list[str]
        NewObjectSelectionList : list[str]
        AdvancedOptions : bool
        ScalingFactor : float
        MptMethodType : str
        GraphicalSelection : bool
        ShowCoordinates : bool
        X : float
        Y : float
        Z : float

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
                Argument PartReplacementName.
                """

            class _ManagementMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument ManagementMethod.
                """

            class _CreationMethod(PyTextualCommandArgumentsSubItem):
                """
                Argument CreationMethod.
                """

            class _OldObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument OldObjectSelectionList.
                """

            class _NewObjectSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument NewObjectSelectionList.
                """

            class _AdvancedOptions(PyParameterCommandArgumentsSubItem):
                """
                Argument AdvancedOptions.
                """

            class _ScalingFactor(PyNumericalCommandArgumentsSubItem):
                """
                Argument ScalingFactor.
                """

            class _MptMethodType(PyTextualCommandArgumentsSubItem):
                """
                Argument MptMethodType.
                """

            class _GraphicalSelection(PyParameterCommandArgumentsSubItem):
                """
                Argument GraphicalSelection.
                """

            class _ShowCoordinates(PyParameterCommandArgumentsSubItem):
                """
                Argument ShowCoordinates.
                """

            class _X(PyNumericalCommandArgumentsSubItem):
                """
                Argument X.
                """

            class _Y(PyNumericalCommandArgumentsSubItem):
                """
                Argument Y.
                """

            class _Z(PyNumericalCommandArgumentsSubItem):
                """
                Argument Z.
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

        Returns
        -------
        bool
        """
        class _RunCustomJournalCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.JournalString = self._JournalString(self, "JournalString", service, rules, path)

            class _JournalString(PyTextualCommandArgumentsSubItem):
                """
                Argument JournalString.
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
                Argument SeparateContactsOption.
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
        Method : str
        PeriodicityAngle : float
        LCSOrigin : dict[str, Any]
        LCSVector : dict[str, Any]
        TransShift : dict[str, Any]
        SelectionType : str
        ZoneList : list[str]
        LabelList : list[str]
        RemeshBoundariesOption : str
        ZoneLocation : list[str]
        ListAllLabelToggle : bool

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
                self.RemeshBoundariesOption = self._RemeshBoundariesOption(self, "RemeshBoundariesOption", service, rules, path)
                self.ZoneLocation = self._ZoneLocation(self, "ZoneLocation", service, rules, path)
                self.ListAllLabelToggle = self._ListAllLabelToggle(self, "ListAllLabelToggle", service, rules, path)

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Argument Type.
                """

            class _Method(PyTextualCommandArgumentsSubItem):
                """
                Argument Method.
                """

            class _PeriodicityAngle(PyNumericalCommandArgumentsSubItem):
                """
                Argument PeriodicityAngle.
                """

            class _LCSOrigin(PySingletonCommandArgumentsSubItem):
                """
                Argument LCSOrigin.
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
                Argument LCSVector.
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
                Argument SelectionType.
                """

            class _ZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneList.
                """

            class _LabelList(PyTextualCommandArgumentsSubItem):
                """
                Argument LabelList.
                """

            class _RemeshBoundariesOption(PyTextualCommandArgumentsSubItem):
                """
                Argument RemeshBoundariesOption.
                """

            class _ZoneLocation(PyTextualCommandArgumentsSubItem):
                """
                Argument ZoneLocation.
                """

            class _ListAllLabelToggle(PyParameterCommandArgumentsSubItem):
                """
                Argument ListAllLabelToggle.
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
        PrismsSettingsName : str
        AspectRatio : float
        GrowthRate : float
        OffsetMethodType : str
        LastRatioPercentage : float
        FirstHeight : float
        PrismLayers : int
        RegionSelectionList : list[str]

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
                Argument AddChild.
                """

            class _PrismsSettingsName(PyTextualCommandArgumentsSubItem):
                """
                Argument PrismsSettingsName.
                """

            class _AspectRatio(PyNumericalCommandArgumentsSubItem):
                """
                Argument AspectRatio.
                """

            class _GrowthRate(PyNumericalCommandArgumentsSubItem):
                """
                Argument GrowthRate.
                """

            class _OffsetMethodType(PyTextualCommandArgumentsSubItem):
                """
                Argument OffsetMethodType.
                """

            class _LastRatioPercentage(PyNumericalCommandArgumentsSubItem):
                """
                Argument LastRatioPercentage.
                """

            class _FirstHeight(PyNumericalCommandArgumentsSubItem):
                """
                Argument FirstHeight.
                """

            class _PrismLayers(PyNumericalCommandArgumentsSubItem):
                """
                Argument PrismLayers.
                """

            class _RegionSelectionList(PyTextualCommandArgumentsSubItem):
                """
                Argument RegionSelectionList.
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
        GapDistanceConnect : float
        STMinSize : float
        InterfaceSelect : str
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
                self.ShareTopologyPreferences = self._ShareTopologyPreferences(self, "ShareTopologyPreferences", service, rules, path)
                self.SMImprovePreferences = self._SMImprovePreferences(self, "SMImprovePreferences", service, rules, path)
                self.SurfaceMeshPreferences = self._SurfaceMeshPreferences(self, "SurfaceMeshPreferences", service, rules, path)

            class _GapDistance(PyNumericalCommandArgumentsSubItem):
                """
                Argument GapDistance.
                """

            class _GapDistanceConnect(PyNumericalCommandArgumentsSubItem):
                """
                Argument GapDistanceConnect.
                """

            class _STMinSize(PyNumericalCommandArgumentsSubItem):
                """
                Argument STMinSize.
                """

            class _InterfaceSelect(PyTextualCommandArgumentsSubItem):
                """
                Argument InterfaceSelect.
                """

            class _ShareTopologyPreferences(PySingletonCommandArgumentsSubItem):
                """
                Argument ShareTopologyPreferences.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.STRenameInternals = self._STRenameInternals(self, "STRenameInternals", service, rules, path)
                    self.ModelIsPeriodic = self._ModelIsPeriodic(self, "ModelIsPeriodic", service, rules, path)
                    self.STToleranceIncrement = self._STToleranceIncrement(self, "STToleranceIncrement", service, rules, path)
                    self.IntfLabelList = self._IntfLabelList(self, "IntfLabelList", service, rules, path)
                    self.PerLabelList = self._PerLabelList(self, "PerLabelList", service, rules, path)
                    self.NumberOfJoinTries = self._NumberOfJoinTries(self, "NumberOfJoinTries", service, rules, path)
                    self.ShowShareTopologyPreferences = self._ShowShareTopologyPreferences(self, "ShowShareTopologyPreferences", service, rules, path)
                    self.ConnectLabelWildcard = self._ConnectLabelWildcard(self, "ConnectLabelWildcard", service, rules, path)
                    self.ShareTopologyAngle = self._ShareTopologyAngle(self, "ShareTopologyAngle", service, rules, path)
                    self.RelativeShareTopologyTolerance = self._RelativeShareTopologyTolerance(self, "RelativeShareTopologyTolerance", service, rules, path)
                    self.FluidLabelWildcard = self._FluidLabelWildcard(self, "FluidLabelWildcard", service, rules, path)
                    self.ExecuteJoinIntersect = self._ExecuteJoinIntersect(self, "ExecuteJoinIntersect", service, rules, path)
                    self.Operation = self._Operation(self, "Operation", service, rules, path)

                class _STRenameInternals(PyTextualCommandArgumentsSubItem):
                    """
                    Argument STRenameInternals.
                    """

                class _ModelIsPeriodic(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ModelIsPeriodic.
                    """

                class _STToleranceIncrement(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument STToleranceIncrement.
                    """

                class _IntfLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument IntfLabelList.
                    """

                class _PerLabelList(PyTextualCommandArgumentsSubItem):
                    """
                    Argument PerLabelList.
                    """

                class _NumberOfJoinTries(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument NumberOfJoinTries.
                    """

                class _ShowShareTopologyPreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowShareTopologyPreferences.
                    """

                class _ConnectLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ConnectLabelWildcard.
                    """

                class _ShareTopologyAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument ShareTopologyAngle.
                    """

                class _RelativeShareTopologyTolerance(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument RelativeShareTopologyTolerance.
                    """

                class _FluidLabelWildcard(PyTextualCommandArgumentsSubItem):
                    """
                    Argument FluidLabelWildcard.
                    """

                class _ExecuteJoinIntersect(PyTextualCommandArgumentsSubItem):
                    """
                    Argument ExecuteJoinIntersect.
                    """

                class _Operation(PyTextualCommandArgumentsSubItem):
                    """
                    Argument Operation.
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
                    self.SIRemoveStep = self._SIRemoveStep(self, "SIRemoveStep", service, rules, path)
                    self.ShowSMImprovePreferences = self._ShowSMImprovePreferences(self, "ShowSMImprovePreferences", service, rules, path)
                    self.SIStepWidth = self._SIStepWidth(self, "SIStepWidth", service, rules, path)

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

                class _SIRemoveStep(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SIRemoveStep.
                    """

                class _ShowSMImprovePreferences(PyParameterCommandArgumentsSubItem):
                    """
                    Argument ShowSMImprovePreferences.
                    """

                class _SIStepWidth(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SIStepWidth.
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
                    self.FoldFaceLimit = self._FoldFaceLimit(self, "FoldFaceLimit", service, rules, path)
                    self.SMSeparationAngle = self._SMSeparationAngle(self, "SMSeparationAngle", service, rules, path)
                    self.SMSeparation = self._SMSeparation(self, "SMSeparation", service, rules, path)
                    self.SMRemoveStep = self._SMRemoveStep(self, "SMRemoveStep", service, rules, path)
                    self.SMStepWidth = self._SMStepWidth(self, "SMStepWidth", service, rules, path)
                    self.VolumeMeshMaxSize = self._VolumeMeshMaxSize(self, "VolumeMeshMaxSize", service, rules, path)
                    self.AutoAssignZoneTypes = self._AutoAssignZoneTypes(self, "AutoAssignZoneTypes", service, rules, path)
                    self.SMQualityMaxAngle = self._SMQualityMaxAngle(self, "SMQualityMaxAngle", service, rules, path)
                    self.SMQualityImproveLimit = self._SMQualityImproveLimit(self, "SMQualityImproveLimit", service, rules, path)
                    self.AutoSurfaceRemesh = self._AutoSurfaceRemesh(self, "AutoSurfaceRemesh", service, rules, path)
                    self.SelfIntersectCheck = self._SelfIntersectCheck(self, "SelfIntersectCheck", service, rules, path)
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

                class _FoldFaceLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument FoldFaceLimit.
                    """

                class _SMSeparationAngle(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMSeparationAngle.
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

                class _SMQualityImproveLimit(PyNumericalCommandArgumentsSubItem):
                    """
                    Argument SMQualityImproveLimit.
                    """

                class _AutoSurfaceRemesh(PyTextualCommandArgumentsSubItem):
                    """
                    Argument AutoSurfaceRemesh.
                    """

                class _SelfIntersectCheck(PyTextualCommandArgumentsSubItem):
                    """
                    Argument SelfIntersectCheck.
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
        InitialSizeControl : bool
        TargetSizeControl : bool
        SizeControlInterval : float
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
                Argument DrawSizeControl.
                """

            class _InitialSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Argument InitialSizeControl.
                """

            class _TargetSizeControl(PyParameterCommandArgumentsSubItem):
                """
                Argument TargetSizeControl.
                """

            class _SizeControlInterval(PyNumericalCommandArgumentsSubItem):
                """
                Argument SizeControlInterval.
                """

            class _SizeControlParameters(PySingletonCommandArgumentsSubItem):
                """
                Argument SizeControlParameters.
                """

                def __init__(self, parent, attr, service, rules, path):
                    super().__init__(parent, attr, service, rules, path)
                    self.NewLabelObjects = self._NewLabelObjects(self, "NewLabelObjects", service, rules, path)
                    self.NewLabelCells = self._NewLabelCells(self, "NewLabelCells", service, rules, path)
                    self.NewLabelType = self._NewLabelType(self, "NewLabelType", service, rules, path)
                    self.NewLabels = self._NewLabels(self, "NewLabels", service, rules, path)
                    self.NewLabelResolution = self._NewLabelResolution(self, "NewLabelResolution", service, rules, path)
                    self.NewLabelMax = self._NewLabelMax(self, "NewLabelMax", service, rules, path)
                    self.NewZoneType = self._NewZoneType(self, "NewZoneType", service, rules, path)
                    self.NewLabelCurvature = self._NewLabelCurvature(self, "NewLabelCurvature", service, rules, path)
                    self.NewLabelMin = self._NewLabelMin(self, "NewLabelMin", service, rules, path)

                class _NewLabelObjects(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelObjects.
                    """

                class _NewLabelCells(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelCells.
                    """

                class _NewLabelType(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelType.
                    """

                class _NewLabels(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabels.
                    """

                class _NewLabelResolution(PyTextualCommandArgumentsSubItem):
                    """
                    Argument NewLabelResolution.
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

    class TransformVolumeMesh(PyCommand):
        """
        Command TransformVolumeMesh.

        Parameters
        ----------
        MTControlName : str
        Type : str
        Method : str
        CellZoneList : list[str]
        LCSOrigin : dict[str, Any]
        LCSVector : dict[str, Any]
        TransShift : dict[str, Any]
        Angle : float
        Copy : str
        NumOfCopies : int
        Merge : str
        Rename : str

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
                self.CellZoneList = self._CellZoneList(self, "CellZoneList", service, rules, path)
                self.LCSOrigin = self._LCSOrigin(self, "LCSOrigin", service, rules, path)
                self.LCSVector = self._LCSVector(self, "LCSVector", service, rules, path)
                self.TransShift = self._TransShift(self, "TransShift", service, rules, path)
                self.Angle = self._Angle(self, "Angle", service, rules, path)
                self.Copy = self._Copy(self, "Copy", service, rules, path)
                self.NumOfCopies = self._NumOfCopies(self, "NumOfCopies", service, rules, path)
                self.Merge = self._Merge(self, "Merge", service, rules, path)
                self.Rename = self._Rename(self, "Rename", service, rules, path)

            class _MTControlName(PyTextualCommandArgumentsSubItem):
                """
                Argument MTControlName.
                """

            class _Type(PyTextualCommandArgumentsSubItem):
                """
                Argument Type.
                """

            class _Method(PyTextualCommandArgumentsSubItem):
                """
                Argument Method.
                """

            class _CellZoneList(PyTextualCommandArgumentsSubItem):
                """
                Argument CellZoneList.
                """

            class _LCSOrigin(PySingletonCommandArgumentsSubItem):
                """
                Argument LCSOrigin.
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
                Argument LCSVector.
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

            class _Angle(PyNumericalCommandArgumentsSubItem):
                """
                Argument Angle.
                """

            class _Copy(PyTextualCommandArgumentsSubItem):
                """
                Argument Copy.
                """

            class _NumOfCopies(PyNumericalCommandArgumentsSubItem):
                """
                Argument NumOfCopies.
                """

            class _Merge(PyTextualCommandArgumentsSubItem):
                """
                Argument Merge.
                """

            class _Rename(PyTextualCommandArgumentsSubItem):
                """
                Argument Rename.
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
        ZoneLocation : list[str]
        TopologyList : list[str]
        TopologyTypeList : list[str]
        OldTopologyList : list[str]
        OldTopologyTypeList : list[str]

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

            class _MeshObject(PyTextualCommandArgumentsSubItem):
                """
                Argument MeshObject.
                """

            class _SelectionType(PyTextualCommandArgumentsSubItem):
                """
                Argument SelectionType.
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
                Argument ListAllBoundariesToggle.
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
        FilterCategory : str
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
                Argument MainFluidRegion.
                """

            class _FilterCategory(PyTextualCommandArgumentsSubItem):
                """
                Argument FilterCategory.
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
                Argument EnableParallel.
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

        Returns
        -------
        bool
        """
        class _Write2dMeshCommandArguments(PyCommandArguments):
            def __init__(self, service, rules, command, path, id):
                super().__init__(service, rules, command, path, id)
                self.FileName = self._FileName(self, "FileName", service, rules, path)

            class _FileName(PyTextualCommandArgumentsSubItem):
                """
                Argument FileName.
                """

        def create_instance(self) -> _Write2dMeshCommandArguments:
            args = self._get_create_instance_args()
            if args is not None:
                return self._Write2dMeshCommandArguments(*args)

