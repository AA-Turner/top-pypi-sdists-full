"""MeshWorkflow module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


class ControlDataDefinedByType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of the definition for the control data of the specific control.
    """

    BySettings = 1
    ByOutcome = 1
    ByValue = 0

class MaterialPointDefineByType(Enum):
    """
    This enum is referenced in Material Point controls. It specifies how the material point location is defined.
    """

    Location = 1
    CoordinateSystem = 2
    GeometrySelection = 3

class CheckpointDefinitionType(Enum):
    """
    To select the MeshWorkflow Process Entity Type.
    """

    Disabled = 1
    Enabled = 2
    Undefined = 0
    UserDefined = 3

class ControlType(Enum):
    """
    To select the mesh workflow control type.
    """

    AddPrescribedPoints = 86
    AddPrescribedPointsFromFile = 87
    AdvancedTessellationDiagnostics = 142
    AdvancedTopologyDiagnostics = 162
    UserNamesAdvancedTopologyDiagnostics = 163
    ZoneMaterialAssignment = 14
    ZoneThicknessAssignment = 15
    AutoBlock = 171
    AutoBlockAutoPlanarCut = 173
    AutoBlockExistingLoopsCut = 175
    AutoBlockManualPlanarCut = 174
    AutoBlockUserNames = 172
    AutoQuadConversion = 152
    AutoQuadHoleAndFeatureTreatment = 148
    AutoQuadMeshing = 151
    AutoQuadTopologyDefeature = 150
    AutoQuadTopologyRepair = 149
    AutoRepair = 127
    Checkpoint = 3
    HoleClosing = 125
    ShortEdgeCollapse = 122
    Connect = 111
    ConnectMultiTolerances = 112
    CuboidalEnclosure = 10
    PartEnclosure = 7
    HemisphereEnclosure = 9
    IrregularShapeConvexEnclosure = 11
    IrregularShapeHemiConvexEnclosure = 12
    SphericalEnclosure = 8
    CustomNamesEnclosure = 13
    TopologyCreation = 19
    SingleZoneCreation = 32
    Custom = 1
    Delete = 6
    InteriorNodeDeletion = 129
    TopologyDeletion = 20
    ZonePropertiesDeletion = 17
    CylindricalScalingDirectMorphing = 39
    FlexPCBMorphing = 44
    FlexPCBMorphingBendDefinition = 45
    FlexPCBMorphingBendDefinitionEdgeBased = 47
    FlexPCBMorphingBendDefinitionPointBased = 46
    OffsetMorphing = 43
    RotationMorphing = 42
    SphericalScalingMorphing = 40
    TranslationMorphing = 41
    ConstantSizeEdgeMesher = 56
    EdgeBiasingEdgeMesher = 58
    SizeFieldEdgeMesher = 57
    Extrusion = 27
    CustomNamesExtrusion = 28
    UserNamesFailedTopology = 165
    HoleFilling = 29
    Fuse = 113
    FuseMultiTolerances = 114
    GrainsGeneration = 35
    GrainsGenerationCylinder = 38
    GrainsGenerationEllipsoid = 37
    GrainsGenerationHex = 147
    GrainsGenerationSphere = 36
    HoleDetection = 132
    IGASolverFileExport = 154
    IGASplineConversion = 153
    CADImport = 104
    CADOptionsDomainCreation = 110
    CADOptionsDiscovery = 109
    CADOptionsParasolid = 106
    CADOptionsSTL = 105
    CADOptionsStride = 107
    CADOptionsWorkbench = 108
    ImproveSurfaceMeshSecondOrderConversion = 79
    ImproveSurfaceMeshProjectionOnGeometry = 81
    ResolveIntersections = 82
    ImproveSurfaceMeshQuadsToTrianglesSplitting = 80
    ImproveVolumeMeshAutoNodeMove = 83
    ImproveVolumeMeshSecondOrderConversion = 84
    Interactive = 116
    LabelCreationByExpression = 145
    LabelCreationByProximity = 144
    LabelCreationByScope = 143
    LeakPrevention = 93
    HintMorphing = 49
    SourceTargetMorphing = 48
    MaterialPoint = 94
    FaceMerging = 118
    MergeNodes = 133
    MergeOverlappingFaces = 115
    PartsMerging = 117
    VolumesMerging = 31
    MeshReplication = 85
    EditMeshMergeFaces = 170
    EditMeshSeparateFaces = 169
    LoadRecording = 53
    AdvancedScopeMorphing = 50
    PlaybackMorphing = 55
    RecordingMorphing = 52
    SaveMorphing = 54
    AdvancedSolverMorphing = 51
    EdgeBiasingMultiZoneMesher = 75
    InflationMultiZoneMesher = 74
    MappedMeshingMultiZoneMesher = 76
    MatchControlMultiZoneMesher = 77
    TopologyProtectionMultiZoneMesher = 78
    ConstantSizeMultiZoneSurfaceMesher = 70
    SizeFieldMultiZoneSurfaceMesher = 71
    ConstantSizeMultiZoneVolumeMesher = 72
    SizeFieldMultiZoneVolumeMesher = 73
    UserNamesNewTopology = 164
    NumberOfDivisionsOnEdges = 101
    PartialDefeature = 120
    HolePatching = 30
    FacePinching = 124
    TopologyProtection = 126
    PyPrimeMeshScript = 96
    PythonScript = 95
    PythonVariable = 97
    MeshImport = 4
    SharpAngleFaceRemoval = 123
    ThinFaceRemoval = 121
    RenameZone = 33
    TopoEdgesOfTopoFacesRepair = 130
    ResolveSurfaceOverlaps = 131
    RevertSurfaceOrientation = 34
    SALEControlPoints = 137
    SALETrim = 161
    SetSOLSH190 = 18
    Setup = 2
    ZonePropertySetting = 16
    MeshLayerCreation = 166
    SolderBallCreation = 167
    UserNamesSolderBall = 168
    SolidIGAGeometryImport = 155
    SolidIGAPhysicalSpaceMapping = 160
    SolidIGASolverFileImport = 157
    SolidIGASplineCreation = 156
    SolidIGATetMeshCreation = 158
    SolidIGATetMeshRefinement = 159
    StackableBodiesDetection = 134
    UserNamesStackableBodiesDetection = 135
    StackerVolumeFlattening = 98
    UserNamesStackerVolumeFlattening = 99
    StackerVolumeMeshing = 100
    StackerDiagnostics = 136
    EdgeSuppression = 119
    InteriorEdgeSuppression = 128
    SurfaceDiagnostics = 138
    UserNamesSurfaceDiagnostics = 139
    QuadMeshAdvancedOptions = 62
    ConstantSizeSurfaceMesh = 59
    QuadBoundaryLayer = 63
    SizeFieldSurfaceMesher = 60
    WrapSpecificSurfaceMesh = 61
    TopologyDiagnostics = 140
    UserNamesTopologyDiagnostics = 141
    TubeSplitting = 146
    Undefined = 0
    Verticalize = 102
    VerticalizeAdvanced = 103
    ConstantSizeVolumeMesh = 66
    GeometricVolumeMesher = 64
    HexDominant = 69
    PrismsAdvanced = 68
    PrismsGeneration = 67
    SizeFieldVolumeMesher = 65
    VolumetricSizeFieldBOI = 26
    VolumetricSizeFieldCurvature = 24
    VolumetricSizeFieldLoad = 22
    VolumetricSizeFieldMaxSize = 23
    VolumetricSizeFieldProximity = 25
    UserNamesVolumetricSizeField = 21
    ConstantFidelityWrapper = 90
    ConstantSizeWrap = 88
    GeometryFidelity = 89
    SizeFieldWrap = 91
    CustomNamesWrap = 92
    MeshExport = 5

class DataTransferType(Enum):
    """
    This enum is referenced in the "Output" tree node and defines how the generated Mesh Workflow data should be transferred back into Mechanical geometry part(s) together with the associated mesh.
    """

    ByTopology = 1
    ByZones = 2
    ProgramControlled = 0

class DecompositionType(Enum):
    """
    This enum is referenced in MultiZone mesher controls. It specifies the decomposition type used to generate the MultiZone mesh.
    """

    Aggressive = 3
    AllFree = 1
    AxisSweep = 6
    CartSweep = 5
    ProgramControlled = 7
    Standard = 2
    ThinSweep = 4

class DefeatureToleranceDefineBy(Enum):
    """
    This enum is referenced in MultiZone mesher controls. It specifies how the MultiZone Defeature Tolerance is defined.
    """

    ProgramControlled = 1
    UserDefined = 2

class FreeFaceMeshType(Enum):
    """
    This enum is referenced in MultiZone mesher controls. It specifies the element type for the MultiZone free face mesh.
    """

    AllQuads = 4
    AllTris = 3
    OneTri = 1
    SomeTris = 2

class FreeVolumeMeshType(Enum):
    """
    This enum is referenced in MultiZone mesher controls. It specifies how free blocks are treated by the MultiZone meshing algorithm.
    """

    NotAllowed = 1
    TetraPyramid = 2

class HemisphereCenterDefinitionType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of hemisphere center modality being configured. Based on the type of an hemisphere center modality different rules are applied which define the applicable list of modality data to be used for creating a hemispherical enclosure.
    """

    Centered = 1
    Undefined = 0
    UserDefined = 2

class HemisphereOrientationDefinitionType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of hemisphere orientation modality being configured.
    """

    NegativeX = 4
    NegativeY = 5
    NegativeZ = 6
    PositiveX = 1
    PositiveY = 2
    PositiveZ = 3
    Undefined = 0

class MaterialPointType(Enum):
    """
    To select the MeshWorkflow Surface Scope Modality Type.
    """

    Exclude = 2
    Include = 1
    Undefined = 0

class MergeNodesToleranceType(Enum):
    """
    This enum specifies the merge nodes tolerance type to be used when executing Merge Nodes operation.
    """

    Absolute = 1
    Relative = 2

class MeshFlowControl(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the mesh flow control being configured.
    """

    Global = 2
    None_ = 1
    Undefined = 0

class OperationType(Enum):
    """
    This enum is referenced in the “Step” tree node and reflects the type of operation being configured. Based on the type of an operation different rules are applied which define the applicable list of controls and outcomes which can be added.
    """

    AddPrescribedPoints = 33
    AutoBlock = 71
    AutoQuadConvertToAllQuad = 59
    AutoQuadDefeature = 57
    AutoQuadMesher = 58
    AutoQuadRepair = 56
    AutoQuadTreatHolesAndFeatures = 55
    AutoRepairTopology = 48
    Checkpoint = 2
    Connect = 42
    CreateEnclosure = 7
    CreateLabels = 53
    CreateSolderBall = 69
    CreateTopology = 9
    CreateVolumetricSizeField = 11
    CreateZones = 16
    Custom = 1
    DecomposeTopology = 54
    Delete = 6
    DeleteTopology = 10
    DetectHoles = 49
    DetectStackableBodies = 38
    CreateEdgeMesh = 25
    Extrude = 12
    FillHoles = 13
    Fuse = 43
    GenerateGrains = 19
    IGAConvertToSpline = 60
    IGAExportSolverFile = 61
    ImportCAD = 41
    ImproveSurfaceMesh = 30
    ImproveVolumeMesh = 31
    Interactive = 45
    LoadRecording = 22
    ManageZoneProperties = 8
    Match = 21
    MergeNodes = 50
    MergeOverlappingFaces = 44
    MergeParts = 46
    MergeVolumes = 15
    ReplicateMesh = 32
    EditMesh = 70
    ModelDiagnostics = 52
    ModifySurfaceOrientations = 18
    ModifyZones = 17
    Morph = 20
    MorphPlayback = 24
    MultiZoneSurfaceMesher = 28
    MultiZoneVolumeMesher = 29
    PatchHoles = 14
    Python = 35
    ImportMesh = 4
    RepairTopology = 47
    SALEGenerateMesh = 51
    SaveRecording = 23
    SetupEnvironment = 3
    SlicerCreateMeshLayers = 68
    SolidIGACreateSplines = 63
    SolidIGACreateTetMesh = 65
    SolidIGAImportGeometry = 62
    SolidIGAImportSolverFile = 64
    SolidIGAMapToPhysicalSpace = 67
    SolidIGARefineTetMesh = 66
    StackerFlattenVolume = 36
    StackerDiagnostics = 39
    StackerMeshVolume = 37
    CreateSurfaceMesh = 26
    Undefined = 0
    Verticalize = 40
    CreateVolumeMesh = 27
    Wrap = 34
    ExportMesh = 5

class OutcomeType(Enum):
    """
    This enum is referenced in the “Outcome” tree node and reflects the type of outcome being configured. Based on the type of an outcome different rules are applied which define the applicable list of outcome data to be used.
    """

    AdvancedTessellationDiagnostics = 10
    AdvancedTopologyDiagnostics = 34
    Checkpoint = 3
    CSVProcessingInfo = 27
    Custom = 1
    EdgeZoneScope = 18
    EnclosureExternalScope = 14
    EnclosureInternalScope = 13
    EnclosureScope = 12
    ExtrusionEndScope = 16
    ExtrusionStartScope = 15
    FaceZoneScope = 19
    FailedTopology = 36
    FailureInfo = 11
    InternalVolumeZoneScope = 21
    MergeNodes = 28
    MultiZoneSurfaceMesherDiagnostics = 42
    MultiZoneVolumeMesherDiagnostics = 41
    NewTopology = 35
    NonStackableBodies = 25
    Performance = 2
    PreviewMorph = 37
    PreviewSurfaceMesher = 38
    PythonTraceback = 17
    QualityMetrics = 7
    Recording = 6
    Scope = 4
    SizeFieldName = 5
    SolderBallBottomCap = 40
    SolderBallTopCap = 39
    StackerBaseEdge = 23
    StackerBaseFace = 22
    StackerDiagnostics = 29
    StackerSeedFace = 24
    SurfaceDiagnostics = 8
    TopologyCountChange = 33
    TopologyDiagnostics = 9
    TubeSplittingCaps = 32
    TubeSplittingFaces = 30
    TubeSplittingVolumes = 31
    Undefined = 0
    VolumeZoneScope = 20
    WarningInfo = 26

class ScopeDefinedByType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects how a scope is being defined. Based on the type of a scope definition different rules are applied which define the applicable list of scope definitions to be used.
    """

    Outcome = 1
    Value = 0

class ScopeType(Enum):
    """
    To select the MeshWorkflow Process Entity Type.
    """

    ElementSet = 5
    Label = 2
    MaterialPoint = 4
    Part = 1
    Undefined = 0
    Zone = 3

class SettingsType(Enum):
    """
    A SettingsType allows the user to add the additional specific Settings type entries to the Steps. The additional entries can be set by the user to automatically define the attributes of different operation Controls.
    """

    Acoustic = 2
    Attachment = 3
    Custom = 1
    Global = 5
    Stacker = 4
    Undefined = 0

class SphereCenterDefinitionType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of sphere center modality being configured. Based on the type of an sphere center modality different rules are applied which define the applicable list of modality data to be used for creating a spherical enclosure.
    """

    Centered = 2
    Minimal = 1
    Undefined = 0
    UserDefined = 3

class SurfaceMeshType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of surface mesh being configured.
    """

    Quadrilaterals = 2
    Triangles = 1
    Undefined = 0

class TriangleCountReductionMode(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the mode of triangle count reduction during surface meshing.
    """

    Aggressive = 3
    Conservative = 2
    None_ = 1
    Undefined = 0

class VolumeMeshType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of volume mesh being configured.
    """

    HexCore = 3
    Polyhedral = 2
    Tetrahedral = 1
    Undefined = 0

class WorkflowType(Enum):
    """
    This enum is referenced in the “Steps” tree node and reflects the type of workflow being configured. Based on the type of workflow different rules are applied which define the applicable order and type of operations which can be added.
    """

    AllQuadSurfaceIGA = 13
    BEMAcoustics = 9
    Custom = 1
    DirectMorphing = 2
    FEMAcousticsExternal = 4
    FEMAcousticsFSI = 6
    FEMAcousticsFSISingleBody = 7
    FEMAcousticsFSISingleBodyCutPlane = 8
    FEMAcousticsInternal = 5
    MatchMorphing = 3
    MicrostructureMeshing = 10
    SALE = 12
    SolidIGA = 14
    Stacker = 11
    Undefined = 0

class WrapperRegionType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of wrapper region being configured.
    """

    External = 2
    MaterialPoint = 1
    Undefined = 0

