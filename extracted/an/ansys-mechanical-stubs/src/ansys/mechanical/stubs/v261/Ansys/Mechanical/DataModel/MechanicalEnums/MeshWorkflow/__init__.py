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

    AddPrescribedPoints = 96
    AddPrescribedPointsFromFile = 97
    AdvancedTessellationDiagnostics = 153
    AdvancedTopologyDiagnostics = 174
    UserNamesAdvancedTopologyDiagnostics = 175
    AspectRatioValidation = 197
    ZoneMaterialAssignment = 14
    ZoneThicknessAssignment = 15
    AutoBlock = 183
    AutoBlockAutoPlanarCut = 185
    AutoBlockExistingLoopsCut = 187
    AutoBlockManualPlanarCut = 186
    AutoBlockUserNames = 184
    AutoQuadConversion = 164
    AutoQuadHoleAndFeatureTreatment = 160
    AutoQuadMeshing = 163
    AutoQuadTopologyDefeature = 162
    AutoQuadTopologyRepair = 161
    AutoRepair = 137
    Checkpoint = 3
    HoleClosing = 135
    ShortEdgeCollapse = 132
    Connect = 121
    ConnectMultiTolerances = 122
    CuboidalEnclosure = 10
    PartEnclosure = 7
    HemisphereEnclosure = 9
    IrregularShapeConvexEnclosure = 11
    IrregularShapeHemiConvexEnclosure = 12
    SphericalEnclosure = 8
    CustomNamesEnclosure = 13
    TopologyCreation = 19
    SingleZoneCreation = 35
    Custom = 1
    Delete = 6
    InteriorVertexDeletion = 139
    TopologyDeletion = 20
    ZonePropertiesDeletion = 17
    FilletDetection = 203
    CylindricalScalingMorphing = 42
    FilletMorphing = 47
    FlexPCBMorphing = 48
    FlexPCBMorphingBendDefinition = 49
    FlexPCBMorphingBendDefinitionEdgeBased = 51
    FlexPCBMorphingBendDefinitionPointBased = 50
    OffsetMorphing = 46
    RotationMorphing = 45
    SphericalScalingMorphing = 43
    TranslationMorphing = 44
    ConstantSizeEdgeMesher = 65
    EdgeBiasingEdgeMesher = 67
    SizeFieldEdgeMesher = 66
    Extrusion = 27
    ScalingExtrusion = 28
    CustomNamesExtrusion = 29
    UserNamesFailedTopology = 177
    AnnularHoleFilling = 32
    HoleFilling = 31
    Fuse = 123
    FuseMultiTolerances = 124
    GrainsGeneration = 38
    GrainsGenerationCylinder = 41
    GrainsGenerationEllipsoid = 40
    GrainsGenerationHex = 159
    GrainsGenerationSphere = 39
    ImageGeneration = 205
    ImageGenerationOrbitCamera = 207
    ImageGenerationPointCamera = 206
    HoleDetection = 143
    IGASolverFileExport = 166
    IGASplineConversion = 165
    CADImport = 114
    CADOptionsDomainCreation = 120
    CADOptionsDiscovery = 119
    CADOptionsParasolid = 116
    CADOptionsSTL = 115
    CADOptionsStride = 117
    CADOptionsWorkbench = 118
    ImproveSurfaceMeshSecondOrderConversion = 89
    ImproveSurfaceMeshProjectionOnGeometry = 91
    ResolveIntersections = 92
    ImproveSurfaceMeshQuadsToTrianglesSplitting = 90
    ImproveVolumeMeshAutoNodeMove = 93
    ImproveVolumeMeshSecondOrderConversion = 94
    Interactive = 126
    JacobianRatioCornerNodesValidation = 199
    JacobianRatioGaussPointsValidation = 200
    JacobianRatioMAPDLValidation = 198
    LabelAdditionByExpression = 156
    LabelAdditionByProximity = 155
    LabelAdditionByScope = 154
    LabelRemovalByScope = 157
    LeakPrevention = 103
    HintMorphing = 57
    PlaneProjectionMorphing = 58
    SourceTargetMorphing = 56
    MaterialPoint = 104
    FaceMerging = 128
    MergeNodes = 144
    MergeOverlappingFaces = 125
    PartsMerging = 127
    VolumesMerging = 34
    MeshCheckValidation = 202
    MeshReplication = 95
    EditMeshMergeFaces = 182
    EditMeshSeparateFaces = 181
    MeshValidation = 194
    LoadRecording = 62
    AdvancedScopeMorphing = 59
    PlaybackMorphing = 64
    RecordingMorphing = 61
    SaveMorphing = 63
    AdvancedSolverMorphing = 60
    EdgeBiasingMultiZoneMesher = 85
    InflationMultiZoneMesher = 84
    MappedMeshingMultiZoneMesher = 86
    MatchControlMultiZoneMesher = 87
    TopologyProtectionMultiZoneMesher = 88
    ConstantSizeMultiZoneSurfaceMesher = 80
    SizeFieldMultiZoneSurfaceMesher = 81
    ConstantSizeMultiZoneVolumeMesher = 82
    SizeFieldMultiZoneVolumeMesher = 83
    UserNamesNewTopology = 176
    NumberOfDivisionsOnEdges = 111
    PartialDefeature = 130
    HolePatching = 33
    FacePinching = 134
    TopologyProtection = 136
    PyPrimeMeshScript = 106
    PythonScript = 105
    PythonVariable = 107
    MeshImport = 4
    SharpAngleFaceRemoval = 133
    ThinFaceRemoval = 131
    RenameZone = 36
    EdgesOfFacesRepair = 140
    ResolveSurfaceOverlaps = 141
    ResolveSurfaceOverlaps_MultiTolerances = 142
    RevertSurfaceOrientation = 37
    Revolve = 30
    SALEControlPoints = 148
    SALETrim = 173
    SetSOLSH190 = 18
    Setup = 2
    ZonePropertySetting = 16
    SkewnessValidation = 196
    CheckSlicedLayers = 191
    MeshLayerCreation = 178
    DeleteTrappedSlices = 190
    ImproveSlicedPart = 188
    PostSlicePart = 189
    SolderBallCreation = 179
    UserNamesSolderBall = 180
    SolidIGAGeometryImport = 167
    SolidIGAPhysicalSpaceMapping = 172
    SolidIGASolverFileImport = 169
    SolidIGASplineCreation = 168
    SolidIGATetMeshCreation = 170
    SolidIGATetMeshRefinement = 171
    StackableBodiesDetection = 145
    UserNamesStackableBodiesDetection = 146
    StackerVolumeFlattening = 108
    UserNamesStackerVolumeFlattening = 109
    StackerVolumeMeshing = 110
    StackerDiagnostics = 147
    EdgeSuppression = 129
    InteriorEdgeSuppression = 138
    SurfaceDiagnostics = 149
    UserNamesSurfaceDiagnostics = 150
    QuadMeshAdvancedOptions = 71
    ConstantSizeSurfaceMesh = 68
    QuadBoundaryLayer = 72
    SizeFieldSurfaceMesher = 69
    WrapSpecificSurfaceMesh = 70
    TetCollapseValidation = 201
    TopologyDiagnostics = 151
    UserNamesTopologyDiagnostics = 152
    TopologyValidation = 195
    TransformAligning = 55
    TransformRotation = 53
    TransformSphericalScaling = 54
    TransformTranslation = 52
    TubeSplitting = 158
    Undefined = 0
    Verticalize = 112
    VerticalizeAdvanced = 113
    VolumeExtraction = 73
    ConstantSizeVolumeMesh = 76
    GeometricVolumeMesher = 74
    HexDominant = 79
    PrismsAdvanced = 78
    PrismsGeneration = 77
    SizeFieldVolumeMesher = 75
    AutoNodeMove = 193
    ImproveTetrahedrons = 192
    VolumeSplittingAdvanced = 209
    VolumeSplittingBlend = 212
    VolumeSplittingLoop = 211
    VolumeSplittingPlane = 210
    VolumeSplittingUserNames = 208
    VolumetricSizeFieldBOI = 26
    VolumetricSizeFieldCurvature = 24
    VolumetricSizeFieldLoad = 22
    VolumetricSizeFieldMaxSize = 23
    VolumetricSizeFieldProximity = 25
    UserNamesVolumetricSizeField = 21
    WeldCreation = 204
    ConstantFidelityWrapper = 100
    ConstantSizeWrap = 98
    GeometryFidelity = 99
    SizeFieldWrap = 101
    CustomNamesWrap = 102
    MeshExport = 5

class CuboidCenterDefinitionType(Enum):
    """
    This enum specifies the type of cuboid center modality being configured. Based on the type of cuboid center modality, different rules are applied which define the applicable list of modality data to be used for creating a cuboidal enclosure.
    """

    Centered = 1
    Undefined = 0
    UserDefined = 2

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
    Unspecified = 0

class DefeatureToleranceDefineBy(Enum):
    """
    This enum is referenced in MultiZone mesher controls. It specifies how the MultiZone Defeature Tolerance is defined.
    """

    ProgramControlled = 1
    UserDefined = 2

class EdgeBiasingDefineBy(Enum):
    """
    This enum specifies how the edge sizing is defined when applying Edge Biasing.
    """

    NumberOfDivisions = 2
    ElementSize = 1
    Unspecified = 0

class EdgeBiasingType(Enum):
    """
    This enum specifies the MultiZone Edge Biasing type to apply.
    """

    EndToStart = 5
    InwardGrowth = 2
    OutwardGrowth = 3
    StartToEnd = 4
    Unspecified = 0
    Uniform = 1

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

class MeshEntityType(Enum):

    Edge = 2
    Face = 3
    Node = 1
    Unspecified = 0
    Volume = 4

class MeshFlowControl(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the mesh flow control being configured.
    """

    Global = 2
    None_ = 1
    Undefined = 0

class MorphingBiasingType(Enum):
    """
    This enum specifies the biasing type to apply for the morphing operation.
    """

    Disabled = 1
    PreserveFixed = 2
    PreserveFixedAndMovable = 4
    PreserveMovable = 3
    Unspecified = 0

class MorphingSolverType(Enum):
    """
    This enum specifies the interpolator to use for a morphing operation.
    """

    Fast = 1
    Linear = 2
    Smooth = 3
    Unspecified = 0

class OperationType(Enum):
    """
    This enum is referenced in the “Step” tree node and reflects the type of operation being configured. Based on the type of an operation different rules are applied which define the applicable list of controls and outcomes which can be added.
    """

    AddPrescribedPoints = 36
    AutoBlock = 75
    AutoQuadConvertToAllQuad = 63
    AutoQuadDefeature = 61
    AutoQuadMesher = 62
    AutoQuadRepair = 60
    AutoQuadTreatHolesAndFeatures = 59
    AutoRepairTopology = 51
    Checkpoint = 2
    Connect = 45
    CreateEnclosure = 7
    AddLabels = 56
    CreateSolderBall = 73
    CreateTopology = 9
    CreateVolumetricSizeField = 11
    CreateWelds = 84
    CreateZones = 17
    Custom = 1
    DecomposeTopology = 58
    Delete = 6
    DeleteTopology = 10
    DetectFillets = 83
    DetectHoles = 52
    DetectStackableBodies = 41
    CreateEdgeMesh = 27
    ExtractVolumes = 29
    Extrude = 12
    FillHoles = 14
    Fuse = 46
    GenerateGrains = 20
    GenerateImages = 85
    IGAConvertToSpline = 64
    IGAExportSolverFile = 65
    ImportCAD = 44
    ImproveSurfaceMesh = 33
    ImproveVolumeMesh = 34
    Interactive = 48
    LoadRecording = 24
    ManageZoneProperties = 8
    Match = 23
    MergeNodes = 53
    MergeOverlappingFaces = 47
    MergeParts = 49
    MergeVolumes = 16
    ReplicateMesh = 35
    EditMesh = 74
    ModelDiagnostics = 55
    ModifySurfaceOrientations = 19
    ModifyZones = 18
    Morph = 21
    MorphPlayback = 26
    MultiZoneSurfaceMesher = 31
    MultiZoneVolumeMesher = 32
    PatchHoles = 15
    Python = 38
    ImportMesh = 4
    RemoveLabels = 57
    RepairTopology = 50
    Revolve = 13
    SALEGenerateMesh = 54
    SaveRecording = 25
    SetupEnvironment = 3
    SlicerCheckSlicedLayers = 79
    SlicerCreateMeshLayers = 72
    SlicerDeleteTrappedSlices = 78
    SlicerImproveSlicedPart = 76
    SlicerPostSlicePart = 77
    SolidIGACreateSplines = 67
    SolidIGACreateTetMesh = 69
    SolidIGAImportGeometry = 66
    SolidIGAImportSolverFile = 68
    SolidIGAMapToPhysicalSpace = 71
    SolidIGARefineTetMesh = 70
    SplitVolumes = 86
    StackerFlattenVolume = 39
    StackerDiagnostics = 42
    StackerMeshVolume = 40
    CreateSurfaceMesh = 28
    Transform = 22
    Undefined = 0
    ValidateMesh = 82
    Verticalize = 43
    CreateVolumeMesh = 30
    VolumeMeshToolAutoNodeMove = 81
    VolumeMeshToolImproveTetrahedrons = 80
    Wrap = 37
    ExportMesh = 5

class OutcomeType(Enum):
    """
    This enum is referenced in the “Outcome” tree node and reflects the type of outcome being configured. Based on the type of an outcome different rules are applied which define the applicable list of outcome data to be used.
    """

    AdvancedTessellationDiagnostics = 10
    AdvancedTopologyDiagnostics = 36
    Checkpoint = 3
    CSVProcessingInfo = 29
    Custom = 1
    EdgeZoneScope = 18
    EnclosureExternalScope = 14
    EnclosureInternalScope = 13
    EnclosureScope = 12
    ExtrusionEndScope = 16
    ExtrusionStartScope = 15
    FaceZoneScope = 19
    FailedTopology = 38
    FailureInfo = 11
    InternalVolumeZoneScope = 21
    MergeNodes = 30
    MultiZoneSurfaceMesherDiagnostics = 46
    MultiZoneVolumeMesherDiagnostics = 45
    NewTopology = 37
    NonStackableBodies = 25
    NonStackableEdges = 27
    NonStackableFaces = 26
    Performance = 2
    PreviewMorph = 39
    PreviewResolveSurfaceOverlaps = 41
    PreviewSplitVolumes = 42
    PreviewSurfaceMesher = 40
    PythonTraceback = 17
    QualityMetrics = 7
    Recording = 6
    Scope = 4
    SizeFieldName = 5
    SolderBallBottomPad = 44
    SolderBallTopPad = 43
    StackerBaseEdge = 23
    StackerBaseFace = 22
    StackerDiagnostics = 31
    StackerSeedFace = 24
    SurfaceDiagnostics = 8
    TopologyCountChange = 35
    TopologyDiagnostics = 9
    TubeSplittingCaps = 34
    TubeSplittingFaces = 32
    TubeSplittingVolumes = 33
    Undefined = 0
    ValidateMeshAspectRatioWarning = 50
    ValidateMeshError = 47
    ValidateMeshJacobianRatioCornerNodesWarning = 52
    ValidateMeshJacobianRatioGaussPointsWarning = 53
    ValidateMeshJacobianRatioMAPDLWarning = 51
    ValidateMeshSkewnessWarning = 49
    ValidateMeshTetCollapseWarning = 54
    ValidateMeshWarning = 48
    VolumeZoneScope = 20
    WarningInfo = 28

class ProximityType(Enum):

    Closest = 1
    Radius = 2
    Unspecified = 0

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

class SemistructuredPatternType(Enum):
    """
    This enum is referenced in MultiZone mesher Mapped Meshing controls. It specifies the Semistructured Pattern Type used to generate the mapped mesh.
    """

    Circle = 2
    HalfCircle = 3
    QuarterCircle = 4
    Transition = 1
    Unspecified = 0

class SettingsType(Enum):
    """
    A SettingsType allows the user to add the additional specific Settings type entries to the Steps. The additional entries can be set by the user to automatically define the attributes of different operation Controls.
    """

    Acoustic = 2
    Attachment = 3
    Custom = 1
    Global = 5
    MeshValidation = 7
    Slicer = 6
    Stacker = 4
    Undefined = 0

class SolderBallShapeType(Enum):
    """
    This enum specifies the shape of the created solder ball.
    """

    Sphere = 1
    Torus = 2
    Unspecified = 0

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

class SurfaceScopeModalityType(Enum):
    """
    This enum specifies how the morphable area is automatically computed for a morphing operation.
    """

    Distance = 2
    Rings = 1
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
    Slicer = 15
    SolidIGA = 14
    Stacker = 11
    Undefined = 0

class WrapperRegionType(Enum):
    """
    This enum is referenced in the 'Control' tree node and reflects the type of wrapper region being configured.
    """

    External = 2
    LargestInternal = 3
    MaterialPoint = 1
    Undefined = 0

