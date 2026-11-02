"""MeshWorkflow module."""
from __future__ import annotations
from enum import Enum
import typing
if typing.TYPE_CHECKING:
    import Ansys


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

class ControlDataDefinedByType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of the definition for the control data of the specific control.
    """

    ByOutcome = 1
    ByValue = 0

class ControlType(Enum):
    """
    To select the mesh workflow control type.
    """

    AddPrescribedPoints = 75
    AddPrescribedPointsFromFile = 76
    AdvancedTopologyDiagnostics = 136
    UserNamesAdvancedTopologyDiagnostics = 137
    ZoneMaterialAssignment = 13
    ZoneThicknessAssignment = 14
    AutoQuadConversion = 132
    AutoQuadHoleAndFeatureTreatment = 128
    AutoQuadMeshing = 131
    AutoQuadTopologyDefeature = 130
    AutoQuadTopologyRepair = 129
    AutoRepair = 110
    Checkpoint = 3
    HoleClosing = 108
    ShortEdgeCollapse = 105
    Connect = 96
    PartEnclosure = 7
    HemisphereEnclosure = 9
    IrregularShapeConvexEnclosure = 10
    IrregularShapeHemiConvexEnclosure = 11
    SphericalEnclosure = 8
    CustomNamesEnclosure = 12
    TopologyCreation = 18
    SingleZoneCreation = 31
    Custom = 1
    Delete = 6
    InteriorNodeDeletion = 112
    TopologyDeletion = 19
    ZonePropertiesDeletion = 16
    CylindricalScalingDirectMorphing = 38
    OffsetMorphing = 42
    RotationMorphing = 41
    SphericalScalingMorphing = 39
    TranslationMorphing = 40
    Extrusion = 26
    CustomNamesExtrusion = 27
    UserNamesFailedTopology = 139
    HoleFilling = 28
    Fuse = 97
    GrainsGeneration = 34
    GrainsGenerationCylinder = 37
    GrainsGenerationEllipsoid = 36
    GrainsGenerationHex = 127
    GrainsGenerationSphere = 35
    HoleDetection = 114
    IGASolverFileExport = 134
    IGASplineConversion = 133
    ImportCAD = 92
    CADOptionsDomainCreation = 95
    CADOptionsParasolid = 94
    CADOptionsSTL = 93
    ImproveSurfaceMeshSecondOrderConversion = 69
    ResolveIntersections = 71
    ImproveSurfaceMeshQuadsToTrianglesSplitting = 70
    ImproveVolumeMeshAutoNodeMove = 72
    ImproveVolumeMeshSecondOrderConversion = 73
    Interactive = 99
    LabelCreationByExpression = 125
    LabelCreationByProximity = 124
    LabelCreationByScope = 123
    LeakPrevention = 82
    HintMorphing = 44
    SourceTargetMorphing = 43
    MaterialPoint = 83
    FaceMerging = 101
    MergeNodes = 115
    MergeOverlappingFaces = 98
    PartsMerging = 100
    VolumesMerging = 30
    MeshCopy = 74
    LoadRecording = 48
    AdvancedScopeMorphing = 45
    PlaybackMorphing = 50
    RecordingMorphing = 47
    SaveMorphing = 49
    AdvancedSolverMorphing = 46
    EdgeBiasingMultiZoneMesher = 67
    InflationMultiZoneMesher = 66
    MappedMeshingMultiZoneMesher = 68
    ConstantSizeMultiZoneSurfaceMesher = 62
    SizeFieldMultiZoneSurfaceMesher = 63
    ConstantSizeMultiZoneVolumeMesher = 64
    SizeFieldMultiZoneVolumeMesher = 65
    UserNamesNewTopology = 138
    NumberOfDivisionsOnEdges = 89
    PartialDefeature = 103
    HolePatching = 29
    FacePinching = 107
    TopologyProtection = 109
    PyPrimeMeshScript = 85
    PythonScript = 84
    PythonVariable = 86
    MeshImport = 4
    SharpAngleFaceRemoval = 106
    ThinFaceRemoval = 104
    RenameZone = 32
    TopoEdgesOfTopoFacesRepair = 113
    RevertSurfaceOrientation = 33
    SALEControlPoints = 118
    SALETrim = 135
    SetSOLSH190 = 17
    Setup = 2
    ZonePropertySetting = 15
    StackableBodiesDetection = 116
    StackerCreateBaseFace = 87
    StackerStackBaseFace = 88
    StackerDiagnostics = 117
    EdgeSuppression = 102
    InteriorEdgeSuppression = 111
    SurfaceDiagnostics = 119
    UserNamesSurfaceDiagnostics = 120
    AdvancedSurfaceMesher = 54
    ConstantSizeSurfaceMesh = 51
    QuadBoundaryLayer = 55
    SizeFieldSurfaceMesher = 52
    WrapSpecificSurfaceMesh = 53
    TopologyDiagnostics = 121
    UserNamesTopologyDiagnostics = 122
    TubeSplitting = 126
    Undefined = 0
    Verticalize = 90
    VerticalizeAdvanced = 91
    ConstantSizeVolumeMesh = 58
    GeometricVolumeMesher = 56
    HexDominant = 61
    PrismsAdvanced = 60
    PrismsGeneration = 59
    SizeFieldVolumeMesher = 57
    VolumetricSizeFieldBOI = 25
    VolumetricSizeFieldCurvature = 23
    VolumetricSizeFieldLoad = 21
    VolumetricSizeFieldMaxSize = 22
    VolumetricSizeFieldProximity = 24
    UserNamesVolumetricSizeField = 20
    ConstantFidelityWrapper = 79
    ConstantSizeWrap = 77
    GeometryFidelity = 78
    SizeFieldWrap = 80
    CustomNamesWrap = 81
    MeshExport = 5

class DataTransferType(Enum):
    """
    This enum is referenced in the "Output" tree node and defines how the generated Mesh Workflow data should be transferred back into Mechanical geometry part(s) together with the associated mesh.
    """

    ByTopology = 1
    ByZones = 2
    ProgramControlled = 0

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

class OperationType(Enum):
    """
    This enum is referenced in the “Step” tree node and reflects the type of operation being configured. Based on the type of an operation different rules are applied which define the applicable list of controls and outcomes which can be added.
    """

    AddPrescribedPoints = 32
    AutoQuadConvertToAllQuad = 58
    AutoQuadDefeature = 56
    AutoQuadMesher = 57
    AutoQuadRepair = 55
    AutoQuadTreatHolesAndFeatures = 54
    AutoRepairTopology = 47
    Checkpoint = 2
    Connect = 41
    CreateEnclosure = 7
    CreateLabels = 52
    CreateTopology = 9
    CreateVolumetricSizeField = 11
    CreateZones = 16
    Custom = 1
    DecomposeTopology = 53
    Delete = 6
    DeleteTopology = 10
    DetectHoles = 48
    DetectStackableBodies = 37
    Extrude = 12
    FillHoles = 13
    Fuse = 42
    GenerateGrains = 19
    IGAConvertToSpline = 59
    IGAExportSolverFile = 60
    ImportCAD = 40
    ImproveSurfaceMesh = 29
    ImproveVolumeMesh = 30
    Interactive = 44
    LoadRecording = 22
    ManageZoneProperties = 8
    Match = 21
    MergeNodes = 49
    MergeOverlappingFaces = 43
    MergeParts = 45
    MergeVolumes = 15
    MeshCopy = 31
    ModelDiagnostics = 51
    ModifySurfaceOrientations = 18
    ModifyZones = 17
    Morph = 20
    MorphPlayback = 24
    MultiZoneSurfaceMesher = 27
    MultiZoneVolumeMesher = 28
    PatchHoles = 14
    Python = 34
    ImportMesh = 4
    RepairTopology = 46
    SALEGenerateMesh = 50
    SaveRecording = 23
    SetupEnvironment = 3
    StackerCreateBaseFace = 35
    StackerDiagnostics = 38
    StackerStackBaseFace = 36
    CreateSurfaceMesh = 25
    Undefined = 0
    Verticalize = 39
    CreateVolumeMesh = 26
    Wrap = 33
    ExportMesh = 5

class OutcomeType(Enum):
    """
    This enum is referenced in the “Outcome” tree node and reflects the type of outcome being configured. Based on the type of an outcome different rules are applied which define the applicable list of outcome data to be used.
    """

    AdvancedTopologyDiagnostics = 30
    Checkpoint = 3
    CSVProcessing = 23
    Custom = 1
    EdgeZoneScope = 17
    EnclosureExternalScope = 13
    EnclosureInternalScope = 12
    EnclosureScope = 11
    ExtrusionEndScope = 15
    ExtrusionStartScope = 14
    FaceZoneScope = 18
    FailedTopology = 32
    FailureInfo = 10
    InternalVolumeZoneScope = 20
    MergeNodes = 24
    NewTopology = 31
    Performance = 2
    PythonTraceback = 16
    QualityMetrics = 7
    Recording = 6
    Scope = 4
    SizeFieldName = 5
    StackerBaseFace = 21
    StackerDiagnostics = 25
    SurfaceDiagnostics = 8
    TopologyCountChange = 29
    TopologyDiagnostics = 9
    TubeSplittingCaps = 28
    TubeSplittingFaces = 26
    TubeSplittingVolumes = 27
    Undefined = 0
    VolumeZoneScope = 19

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
    Stacker = 11
    Undefined = 0

class WrapperRegionType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of wrapper region being configured.
    """

    External = 2
    MaterialPoint = 1
    Undefined = 0

