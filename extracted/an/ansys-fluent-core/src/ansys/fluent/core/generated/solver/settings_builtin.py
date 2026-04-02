"""Solver settings."""

from ansys.fluent.core.solver.settings_builtin_bases import _SingletonSetting, _CreatableNamedObjectSetting, _NonCreatableNamedObjectSetting, _CommandSetting, Solver
from ansys.fluent.core.solver.flobject import SettingsBase


__all__ = [
    "Setup",
    "General",
    "Models",
    "Multiphase",
    "Energy",
    "Viscous",
    "Radiation",
    "Species",
    "DiscretePhase",
    "Injections",
    "Injection",
    "VirtualBladeModel",
    "Optics",
    "Structure",
    "Ablation",
    "EChemistry",
    "Battery",
    "SystemCoupling",
    "Sofc",
    "Pemfc",
    "Materials",
    "FluidMaterials",
    "FluidMaterial",
    "SolidMaterials",
    "SolidMaterial",
    "MixtureMaterials",
    "MixtureMaterial",
    "ParticleMixtureMaterials",
    "ParticleMixtureMaterial",
    "CellZoneConditions",
    "CellZoneCondition",
    "FluidCellZones",
    "FluidCellZone",
    "SolidCellZones",
    "SolidCellZone",
    "BoundaryConditions",
    "BoundaryCondition",
    "AxisBoundaries",
    "AxisBoundary",
    "DegassingBoundaries",
    "DegassingBoundary",
    "ExhaustFanBoundaries",
    "ExhaustFanBoundary",
    "FanBoundaries",
    "FanBoundary",
    "GeometryBoundaries",
    "GeometryBoundary",
    "InletVentBoundaries",
    "InletVentBoundary",
    "IntakeFanBoundaries",
    "IntakeFanBoundary",
    "InterfaceBoundaries",
    "InterfaceBoundary",
    "InteriorBoundaries",
    "InteriorBoundary",
    "MassFlowInlets",
    "MassFlowInlet",
    "MassFlowOutlets",
    "MassFlowOutlet",
    "NetworkBoundaries",
    "NetworkBoundary",
    "NetworkEndBoundaries",
    "NetworkEndBoundary",
    "OutflowBoundaries",
    "OutflowBoundary",
    "OutletVentBoundaries",
    "OutletVentBoundary",
    "OversetBoundaries",
    "OversetBoundary",
    "PeriodicBoundaries",
    "PeriodicBoundary",
    "PorousJumpBoundaries",
    "PorousJumpBoundary",
    "PressureFarFieldBoundaries",
    "PressureFarFieldBoundary",
    "PressureInlets",
    "PressureInlet",
    "PressureOutlets",
    "PressureOutlet",
    "RadiatorBoundaries",
    "RadiatorBoundary",
    "RansLesInterfaceBoundaries",
    "RansLesInterfaceBoundary",
    "RecirculationInlets",
    "RecirculationInlet",
    "RecirculationOutlets",
    "RecirculationOutlet",
    "ShadowBoundaries",
    "ShadowBoundary",
    "SymmetryBoundaries",
    "SymmetryBoundary",
    "VelocityInlets",
    "VelocityInlet",
    "WallBoundaries",
    "WallBoundary",
    "NonReflectingBoundary",
    "PerforatedWallBoundary",
    "MeshInterfaces",
    "DynamicMesh",
    "ReferenceValues",
    "ReferenceFrames",
    "ReferenceFrame",
    "NamedExpressions",
    "NamedExpression",
    "Solution",
    "Methods",
    "Controls",
    "ReportDefinitions",
    "Monitor",
    "Residual",
    "ReportFiles",
    "ReportFile",
    "ReportPlots",
    "ReportPlot",
    "ConvergenceConditions",
    "CellRegisters",
    "CellRegister",
    "Initialization",
    "CalculationActivity",
    "ExecuteCommands",
    "CaseModification",
    "RunCalculation",
    "Results",
    "Surfaces",
    "PointSurfaces",
    "PointSurface",
    "LineSurfaces",
    "LineSurface",
    "RakeSurfaces",
    "RakeSurface",
    "PlaneSurfaces",
    "PlaneSurface",
    "IsoSurfaces",
    "IsoSurface",
    "IsoClips",
    "IsoClip",
    "ZoneSurfaces",
    "ZoneSurface",
    "PartitionSurfaces",
    "PartitionSurface",
    "TransformSurfaces",
    "TransformSurface",
    "ImprintSurfaces",
    "ImprintSurface",
    "PlaneSlices",
    "PlaneSlice",
    "SphereSlices",
    "SphereSlice",
    "QuadricSurfaces",
    "QuadricSurface",
    "SurfaceCells",
    "SurfaceCell",
    "ExpressionVolumes",
    "ExpressionVolume",
    "GroupSurfaces",
    "GroupSurface",
    "Graphics",
    "Meshes",
    "Mesh",
    "Contours",
    "Contour",
    "Vectors",
    "Vector",
    "Pathlines",
    "Pathline",
    "ParticleTracks",
    "ParticleTrack",
    "LICs",
    "LIC",
    "Plots",
    "XYPlots",
    "XYPlot",
    "Histogram",
    "CumulativePlots",
    "CumulativePlot",
    "ProfileData",
    "InterpolatedData",
    "Scenes",
    "Scene",
    "SceneAnimation",
    "Report",
    "DiscretePhaseHistogram",
    "Fluxes",
    "SurfaceIntegrals",
    "VolumeIntegrals",
    "InputParameters",
    "OutputParameters",
    "CustomFieldFunctions",
    "CustomFieldFunction",
    "CustomVectors",
    "CustomVector",
    "SimulationReports",
    "ParametricStudies",
    "ParametricStudy",
    "DesignPoints",
    "DesignPoint",
    "ReadCase",
    "read_case",
    "ReadData",
    "read_data",
    "ReadCaseData",
    "read_case_data",
    "WriteCase",
    "write_case",
    "WriteData",
    "write_data",
    "WriteCaseData",
    "write_case_data",
    "Initialize",
    "initialize",
    "Calculate",
    "calculate",
    "Iterate",
    "iterate",
    "DualTimeIterate",
    "dual_time_iterate",
]

class Setup(_SingletonSetting):
    """Setup setting."""

    _db_name = "Setup"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class General(_SingletonSetting):
    """General setting."""

    _db_name = "General"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Models(_SingletonSetting):
    """Models setting."""

    _db_name = "Models"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Multiphase(_SingletonSetting):
    """Multiphase setting."""

    _db_name = "Multiphase"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Energy(_SingletonSetting):
    """Energy setting."""

    _db_name = "Energy"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Viscous(_SingletonSetting):
    """Viscous setting."""

    _db_name = "Viscous"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Radiation(_SingletonSetting):
    """Radiation setting."""

    _db_name = "Radiation"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Species(_SingletonSetting):
    """Species setting."""

    _db_name = "Species"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DiscretePhase(_SingletonSetting):
    """DiscretePhase setting."""

    _db_name = "DiscretePhase"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Injections(_SingletonSetting):
    """Injections setting."""

    _db_name = "Injections"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Injection(_CreatableNamedObjectSetting):
    """Injection setting."""

    _db_name = "Injection"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class VirtualBladeModel(_SingletonSetting):
    """VirtualBladeModel setting."""

    _db_name = "VirtualBladeModel"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Optics(_SingletonSetting):
    """Optics setting."""

    _db_name = "Optics"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Structure(_SingletonSetting):
    """Structure setting."""

    _db_name = "Structure"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Ablation(_SingletonSetting):
    """Ablation setting."""

    _db_name = "Ablation"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class EChemistry(_SingletonSetting):
    """EChemistry setting."""

    _db_name = "EChemistry"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Battery(_SingletonSetting):
    """Battery setting."""

    _db_name = "Battery"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SystemCoupling(_SingletonSetting):
    """SystemCoupling setting."""

    _db_name = "SystemCoupling"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Sofc(_SingletonSetting):
    """Sofc setting."""

    _db_name = "Sofc"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Pemfc(_SingletonSetting):
    """Pemfc setting."""

    _db_name = "Pemfc"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Materials(_SingletonSetting):
    """Materials setting."""

    _db_name = "Materials"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FluidMaterials(_SingletonSetting):
    """FluidMaterials setting."""

    _db_name = "FluidMaterials"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FluidMaterial(_CreatableNamedObjectSetting):
    """FluidMaterial setting."""

    _db_name = "FluidMaterial"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SolidMaterials(_SingletonSetting):
    """SolidMaterials setting."""

    _db_name = "SolidMaterials"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SolidMaterial(_CreatableNamedObjectSetting):
    """SolidMaterial setting."""

    _db_name = "SolidMaterial"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class MixtureMaterials(_SingletonSetting):
    """MixtureMaterials setting."""

    _db_name = "MixtureMaterials"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MixtureMaterial(_CreatableNamedObjectSetting):
    """MixtureMaterial setting."""

    _db_name = "MixtureMaterial"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ParticleMixtureMaterials(_SingletonSetting):
    """ParticleMixtureMaterials setting."""

    _db_name = "ParticleMixtureMaterials"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParticleMixtureMaterial(_CreatableNamedObjectSetting):
    """ParticleMixtureMaterial setting."""

    _db_name = "ParticleMixtureMaterial"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class CellZoneConditions(_SingletonSetting):
    """CellZoneConditions setting."""

    _db_name = "CellZoneConditions"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CellZoneCondition(_NonCreatableNamedObjectSetting):
    """CellZoneCondition setting."""

    _db_name = "CellZoneCondition"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None):
        super().__init__(settings_source=settings_source, name=name)

class FluidCellZones(_SingletonSetting):
    """FluidCellZones setting."""

    _db_name = "FluidCellZones"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FluidCellZone(_CreatableNamedObjectSetting):
    """FluidCellZone setting."""

    _db_name = "FluidCellZone"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SolidCellZones(_SingletonSetting):
    """SolidCellZones setting."""

    _db_name = "SolidCellZones"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SolidCellZone(_CreatableNamedObjectSetting):
    """SolidCellZone setting."""

    _db_name = "SolidCellZone"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class BoundaryConditions(_SingletonSetting):
    """BoundaryConditions setting."""

    _db_name = "BoundaryConditions"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class BoundaryCondition(_NonCreatableNamedObjectSetting):
    """BoundaryCondition setting."""

    _db_name = "BoundaryCondition"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None):
        super().__init__(settings_source=settings_source, name=name)

class AxisBoundaries(_SingletonSetting):
    """AxisBoundaries setting."""

    _db_name = "AxisBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class AxisBoundary(_CreatableNamedObjectSetting):
    """AxisBoundary setting."""

    _db_name = "AxisBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class DegassingBoundaries(_SingletonSetting):
    """DegassingBoundaries setting."""

    _db_name = "DegassingBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DegassingBoundary(_CreatableNamedObjectSetting):
    """DegassingBoundary setting."""

    _db_name = "DegassingBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ExhaustFanBoundaries(_SingletonSetting):
    """ExhaustFanBoundaries setting."""

    _db_name = "ExhaustFanBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ExhaustFanBoundary(_CreatableNamedObjectSetting):
    """ExhaustFanBoundary setting."""

    _db_name = "ExhaustFanBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class FanBoundaries(_SingletonSetting):
    """FanBoundaries setting."""

    _db_name = "FanBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FanBoundary(_CreatableNamedObjectSetting):
    """FanBoundary setting."""

    _db_name = "FanBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class GeometryBoundaries(_SingletonSetting):
    """GeometryBoundaries setting."""

    _db_name = "GeometryBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class GeometryBoundary(_CreatableNamedObjectSetting):
    """GeometryBoundary setting."""

    _db_name = "GeometryBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class InletVentBoundaries(_SingletonSetting):
    """InletVentBoundaries setting."""

    _db_name = "InletVentBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InletVentBoundary(_CreatableNamedObjectSetting):
    """InletVentBoundary setting."""

    _db_name = "InletVentBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class IntakeFanBoundaries(_SingletonSetting):
    """IntakeFanBoundaries setting."""

    _db_name = "IntakeFanBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class IntakeFanBoundary(_CreatableNamedObjectSetting):
    """IntakeFanBoundary setting."""

    _db_name = "IntakeFanBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class InterfaceBoundaries(_SingletonSetting):
    """InterfaceBoundaries setting."""

    _db_name = "InterfaceBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InterfaceBoundary(_CreatableNamedObjectSetting):
    """InterfaceBoundary setting."""

    _db_name = "InterfaceBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class InteriorBoundaries(_SingletonSetting):
    """InteriorBoundaries setting."""

    _db_name = "InteriorBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InteriorBoundary(_CreatableNamedObjectSetting):
    """InteriorBoundary setting."""

    _db_name = "InteriorBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class MassFlowInlets(_SingletonSetting):
    """MassFlowInlets setting."""

    _db_name = "MassFlowInlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MassFlowInlet(_CreatableNamedObjectSetting):
    """MassFlowInlet setting."""

    _db_name = "MassFlowInlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class MassFlowOutlets(_SingletonSetting):
    """MassFlowOutlets setting."""

    _db_name = "MassFlowOutlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MassFlowOutlet(_CreatableNamedObjectSetting):
    """MassFlowOutlet setting."""

    _db_name = "MassFlowOutlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NetworkBoundaries(_SingletonSetting):
    """NetworkBoundaries setting."""

    _db_name = "NetworkBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NetworkBoundary(_CreatableNamedObjectSetting):
    """NetworkBoundary setting."""

    _db_name = "NetworkBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NetworkEndBoundaries(_SingletonSetting):
    """NetworkEndBoundaries setting."""

    _db_name = "NetworkEndBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NetworkEndBoundary(_CreatableNamedObjectSetting):
    """NetworkEndBoundary setting."""

    _db_name = "NetworkEndBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class OutflowBoundaries(_SingletonSetting):
    """OutflowBoundaries setting."""

    _db_name = "OutflowBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OutflowBoundary(_CreatableNamedObjectSetting):
    """OutflowBoundary setting."""

    _db_name = "OutflowBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class OutletVentBoundaries(_SingletonSetting):
    """OutletVentBoundaries setting."""

    _db_name = "OutletVentBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OutletVentBoundary(_CreatableNamedObjectSetting):
    """OutletVentBoundary setting."""

    _db_name = "OutletVentBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class OversetBoundaries(_SingletonSetting):
    """OversetBoundaries setting."""

    _db_name = "OversetBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OversetBoundary(_CreatableNamedObjectSetting):
    """OversetBoundary setting."""

    _db_name = "OversetBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PeriodicBoundaries(_SingletonSetting):
    """PeriodicBoundaries setting."""

    _db_name = "PeriodicBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PeriodicBoundary(_CreatableNamedObjectSetting):
    """PeriodicBoundary setting."""

    _db_name = "PeriodicBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PorousJumpBoundaries(_SingletonSetting):
    """PorousJumpBoundaries setting."""

    _db_name = "PorousJumpBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PorousJumpBoundary(_CreatableNamedObjectSetting):
    """PorousJumpBoundary setting."""

    _db_name = "PorousJumpBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PressureFarFieldBoundaries(_SingletonSetting):
    """PressureFarFieldBoundaries setting."""

    _db_name = "PressureFarFieldBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PressureFarFieldBoundary(_CreatableNamedObjectSetting):
    """PressureFarFieldBoundary setting."""

    _db_name = "PressureFarFieldBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PressureInlets(_SingletonSetting):
    """PressureInlets setting."""

    _db_name = "PressureInlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PressureInlet(_CreatableNamedObjectSetting):
    """PressureInlet setting."""

    _db_name = "PressureInlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PressureOutlets(_SingletonSetting):
    """PressureOutlets setting."""

    _db_name = "PressureOutlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PressureOutlet(_CreatableNamedObjectSetting):
    """PressureOutlet setting."""

    _db_name = "PressureOutlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RadiatorBoundaries(_SingletonSetting):
    """RadiatorBoundaries setting."""

    _db_name = "RadiatorBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RadiatorBoundary(_CreatableNamedObjectSetting):
    """RadiatorBoundary setting."""

    _db_name = "RadiatorBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RansLesInterfaceBoundaries(_SingletonSetting):
    """RansLesInterfaceBoundaries setting."""

    _db_name = "RansLesInterfaceBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RansLesInterfaceBoundary(_CreatableNamedObjectSetting):
    """RansLesInterfaceBoundary setting."""

    _db_name = "RansLesInterfaceBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RecirculationInlets(_SingletonSetting):
    """RecirculationInlets setting."""

    _db_name = "RecirculationInlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RecirculationInlet(_CreatableNamedObjectSetting):
    """RecirculationInlet setting."""

    _db_name = "RecirculationInlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RecirculationOutlets(_SingletonSetting):
    """RecirculationOutlets setting."""

    _db_name = "RecirculationOutlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RecirculationOutlet(_CreatableNamedObjectSetting):
    """RecirculationOutlet setting."""

    _db_name = "RecirculationOutlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ShadowBoundaries(_SingletonSetting):
    """ShadowBoundaries setting."""

    _db_name = "ShadowBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ShadowBoundary(_CreatableNamedObjectSetting):
    """ShadowBoundary setting."""

    _db_name = "ShadowBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SymmetryBoundaries(_SingletonSetting):
    """SymmetryBoundaries setting."""

    _db_name = "SymmetryBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SymmetryBoundary(_CreatableNamedObjectSetting):
    """SymmetryBoundary setting."""

    _db_name = "SymmetryBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class VelocityInlets(_SingletonSetting):
    """VelocityInlets setting."""

    _db_name = "VelocityInlets"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class VelocityInlet(_CreatableNamedObjectSetting):
    """VelocityInlet setting."""

    _db_name = "VelocityInlet"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class WallBoundaries(_SingletonSetting):
    """WallBoundaries setting."""

    _db_name = "WallBoundaries"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class WallBoundary(_CreatableNamedObjectSetting):
    """WallBoundary setting."""

    _db_name = "WallBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NonReflectingBoundary(_SingletonSetting):
    """NonReflectingBoundary setting."""

    _db_name = "NonReflectingBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PerforatedWallBoundary(_SingletonSetting):
    """PerforatedWallBoundary setting."""

    _db_name = "PerforatedWallBoundary"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MeshInterfaces(_SingletonSetting):
    """MeshInterfaces setting."""

    _db_name = "MeshInterfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DynamicMesh(_SingletonSetting):
    """DynamicMesh setting."""

    _db_name = "DynamicMesh"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReferenceValues(_SingletonSetting):
    """ReferenceValues setting."""

    _db_name = "ReferenceValues"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReferenceFrames(_SingletonSetting):
    """ReferenceFrames setting."""

    _db_name = "ReferenceFrames"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReferenceFrame(_CreatableNamedObjectSetting):
    """ReferenceFrame setting."""

    _db_name = "ReferenceFrame"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NamedExpressions(_SingletonSetting):
    """NamedExpressions setting."""

    _db_name = "NamedExpressions"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NamedExpression(_CreatableNamedObjectSetting):
    """NamedExpression setting."""

    _db_name = "NamedExpression"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Solution(_SingletonSetting):
    """Solution setting."""

    _db_name = "Solution"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Methods(_SingletonSetting):
    """Methods setting."""

    _db_name = "Methods"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Controls(_SingletonSetting):
    """Controls setting."""

    _db_name = "Controls"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportDefinitions(_SingletonSetting):
    """ReportDefinitions setting."""

    _db_name = "ReportDefinitions"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Monitor(_SingletonSetting):
    """Monitor setting."""

    _db_name = "Monitor"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Residual(_SingletonSetting):
    """Residual setting."""

    _db_name = "Residual"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportFiles(_SingletonSetting):
    """ReportFiles setting."""

    _db_name = "ReportFiles"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportFile(_CreatableNamedObjectSetting):
    """ReportFile setting."""

    _db_name = "ReportFile"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ReportPlots(_SingletonSetting):
    """ReportPlots setting."""

    _db_name = "ReportPlots"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportPlot(_CreatableNamedObjectSetting):
    """ReportPlot setting."""

    _db_name = "ReportPlot"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ConvergenceConditions(_SingletonSetting):
    """ConvergenceConditions setting."""

    _db_name = "ConvergenceConditions"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CellRegisters(_SingletonSetting):
    """CellRegisters setting."""

    _db_name = "CellRegisters"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CellRegister(_CreatableNamedObjectSetting):
    """CellRegister setting."""

    _db_name = "CellRegister"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Initialization(_SingletonSetting):
    """Initialization setting."""

    _db_name = "Initialization"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CalculationActivity(_SingletonSetting):
    """CalculationActivity setting."""

    _db_name = "CalculationActivity"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ExecuteCommands(_SingletonSetting):
    """ExecuteCommands setting."""

    _db_name = "ExecuteCommands"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CaseModification(_SingletonSetting):
    """CaseModification setting."""

    _db_name = "CaseModification"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RunCalculation(_SingletonSetting):
    """RunCalculation setting."""

    _db_name = "RunCalculation"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Results(_SingletonSetting):
    """Results setting."""

    _db_name = "Results"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Surfaces(_SingletonSetting):
    """Surfaces setting."""

    _db_name = "Surfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PointSurfaces(_SingletonSetting):
    """PointSurfaces setting."""

    _db_name = "PointSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PointSurface(_CreatableNamedObjectSetting):
    """PointSurface setting."""

    _db_name = "PointSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class LineSurfaces(_SingletonSetting):
    """LineSurfaces setting."""

    _db_name = "LineSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class LineSurface(_CreatableNamedObjectSetting):
    """LineSurface setting."""

    _db_name = "LineSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RakeSurfaces(_SingletonSetting):
    """RakeSurfaces setting."""

    _db_name = "RakeSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RakeSurface(_CreatableNamedObjectSetting):
    """RakeSurface setting."""

    _db_name = "RakeSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PlaneSurfaces(_SingletonSetting):
    """PlaneSurfaces setting."""

    _db_name = "PlaneSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PlaneSurface(_CreatableNamedObjectSetting):
    """PlaneSurface setting."""

    _db_name = "PlaneSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class IsoSurfaces(_SingletonSetting):
    """IsoSurfaces setting."""

    _db_name = "IsoSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class IsoSurface(_CreatableNamedObjectSetting):
    """IsoSurface setting."""

    _db_name = "IsoSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class IsoClips(_SingletonSetting):
    """IsoClips setting."""

    _db_name = "IsoClips"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class IsoClip(_CreatableNamedObjectSetting):
    """IsoClip setting."""

    _db_name = "IsoClip"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ZoneSurfaces(_SingletonSetting):
    """ZoneSurfaces setting."""

    _db_name = "ZoneSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ZoneSurface(_CreatableNamedObjectSetting):
    """ZoneSurface setting."""

    _db_name = "ZoneSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PartitionSurfaces(_SingletonSetting):
    """PartitionSurfaces setting."""

    _db_name = "PartitionSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PartitionSurface(_CreatableNamedObjectSetting):
    """PartitionSurface setting."""

    _db_name = "PartitionSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class TransformSurfaces(_SingletonSetting):
    """TransformSurfaces setting."""

    _db_name = "TransformSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class TransformSurface(_CreatableNamedObjectSetting):
    """TransformSurface setting."""

    _db_name = "TransformSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ImprintSurfaces(_SingletonSetting):
    """ImprintSurfaces setting."""

    _db_name = "ImprintSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ImprintSurface(_CreatableNamedObjectSetting):
    """ImprintSurface setting."""

    _db_name = "ImprintSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PlaneSlices(_SingletonSetting):
    """PlaneSlices setting."""

    _db_name = "PlaneSlices"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PlaneSlice(_CreatableNamedObjectSetting):
    """PlaneSlice setting."""

    _db_name = "PlaneSlice"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SphereSlices(_SingletonSetting):
    """SphereSlices setting."""

    _db_name = "SphereSlices"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SphereSlice(_CreatableNamedObjectSetting):
    """SphereSlice setting."""

    _db_name = "SphereSlice"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class QuadricSurfaces(_SingletonSetting):
    """QuadricSurfaces setting."""

    _db_name = "QuadricSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class QuadricSurface(_CreatableNamedObjectSetting):
    """QuadricSurface setting."""

    _db_name = "QuadricSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SurfaceCells(_SingletonSetting):
    """SurfaceCells setting."""

    _db_name = "SurfaceCells"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SurfaceCell(_CreatableNamedObjectSetting):
    """SurfaceCell setting."""

    _db_name = "SurfaceCell"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ExpressionVolumes(_SingletonSetting):
    """ExpressionVolumes setting."""

    _db_name = "ExpressionVolumes"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ExpressionVolume(_CreatableNamedObjectSetting):
    """ExpressionVolume setting."""

    _db_name = "ExpressionVolume"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class GroupSurfaces(_SingletonSetting):
    """GroupSurfaces setting."""

    _db_name = "GroupSurfaces"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class GroupSurface(_CreatableNamedObjectSetting):
    """GroupSurface setting."""

    _db_name = "GroupSurface"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Graphics(_SingletonSetting):
    """Graphics setting."""

    _db_name = "Graphics"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Meshes(_SingletonSetting):
    """Meshes setting."""

    _db_name = "Meshes"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Mesh(_CreatableNamedObjectSetting):
    """Mesh setting."""

    _db_name = "Mesh"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Contours(_SingletonSetting):
    """Contours setting."""

    _db_name = "Contours"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Contour(_CreatableNamedObjectSetting):
    """Contour setting."""

    _db_name = "Contour"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Vectors(_SingletonSetting):
    """Vectors setting."""

    _db_name = "Vectors"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Vector(_CreatableNamedObjectSetting):
    """Vector setting."""

    _db_name = "Vector"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Pathlines(_SingletonSetting):
    """Pathlines setting."""

    _db_name = "Pathlines"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Pathline(_CreatableNamedObjectSetting):
    """Pathline setting."""

    _db_name = "Pathline"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ParticleTracks(_SingletonSetting):
    """ParticleTracks setting."""

    _db_name = "ParticleTracks"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParticleTrack(_CreatableNamedObjectSetting):
    """ParticleTrack setting."""

    _db_name = "ParticleTrack"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class LICs(_SingletonSetting):
    """LICs setting."""

    _db_name = "LICs"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class LIC(_CreatableNamedObjectSetting):
    """LIC setting."""

    _db_name = "LIC"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Plots(_SingletonSetting):
    """Plots setting."""

    _db_name = "Plots"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class XYPlots(_SingletonSetting):
    """XYPlots setting."""

    _db_name = "XYPlots"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class XYPlot(_CreatableNamedObjectSetting):
    """XYPlot setting."""

    _db_name = "XYPlot"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Histogram(_SingletonSetting):
    """Histogram setting."""

    _db_name = "Histogram"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CumulativePlots(_SingletonSetting):
    """CumulativePlots setting."""

    _db_name = "CumulativePlots"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CumulativePlot(_CreatableNamedObjectSetting):
    """CumulativePlot setting."""

    _db_name = "CumulativePlot"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ProfileData(_SingletonSetting):
    """ProfileData setting."""

    _db_name = "ProfileData"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InterpolatedData(_SingletonSetting):
    """InterpolatedData setting."""

    _db_name = "InterpolatedData"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Scenes(_SingletonSetting):
    """Scenes setting."""

    _db_name = "Scenes"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Scene(_CreatableNamedObjectSetting):
    """Scene setting."""

    _db_name = "Scene"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SceneAnimation(_SingletonSetting):
    """SceneAnimation setting."""

    _db_name = "SceneAnimation"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Report(_SingletonSetting):
    """Report setting."""

    _db_name = "Report"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DiscretePhaseHistogram(_SingletonSetting):
    """DiscretePhaseHistogram setting."""

    _db_name = "DiscretePhaseHistogram"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Fluxes(_SingletonSetting):
    """Fluxes setting."""

    _db_name = "Fluxes"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SurfaceIntegrals(_SingletonSetting):
    """SurfaceIntegrals setting."""

    _db_name = "SurfaceIntegrals"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class VolumeIntegrals(_SingletonSetting):
    """VolumeIntegrals setting."""

    _db_name = "VolumeIntegrals"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InputParameters(_SingletonSetting):
    """InputParameters setting."""

    _db_name = "InputParameters"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OutputParameters(_SingletonSetting):
    """OutputParameters setting."""

    _db_name = "OutputParameters"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CustomFieldFunctions(_SingletonSetting):
    """CustomFieldFunctions setting."""

    _db_name = "CustomFieldFunctions"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CustomFieldFunction(_CreatableNamedObjectSetting):
    """CustomFieldFunction setting."""

    _db_name = "CustomFieldFunction"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class CustomVectors(_SingletonSetting):
    """CustomVectors setting."""

    _db_name = "CustomVectors"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CustomVector(_CreatableNamedObjectSetting):
    """CustomVector setting."""

    _db_name = "CustomVector"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SimulationReports(_SingletonSetting):
    """SimulationReports setting."""

    _db_name = "SimulationReports"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParametricStudies(_SingletonSetting):
    """ParametricStudies setting."""

    _db_name = "ParametricStudies"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParametricStudy(_CreatableNamedObjectSetting):
    """ParametricStudy setting."""

    _db_name = "ParametricStudy"

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class DesignPoints(_SingletonSetting):
    """DesignPoints setting."""

    _db_name = "DesignPoints"

    def __init__(self, parametric_studies: str, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source, parametric_studies=parametric_studies)

class DesignPoint(_CreatableNamedObjectSetting):
    """DesignPoint setting."""

    _db_name = "DesignPoint"

    def __init__(self, parametric_studies: str, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name, parametric_studies=parametric_studies)

class ReadCase(_CommandSetting):
    """ReadCase command object."""

    _db_name = "ReadCase"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class read_case(_CommandSetting):
    """read_case command."""

    _db_name = "ReadCase"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class ReadData(_CommandSetting):
    """ReadData command object."""

    _db_name = "ReadData"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class read_data(_CommandSetting):
    """read_data command."""

    _db_name = "ReadData"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class ReadCaseData(_CommandSetting):
    """ReadCaseData command object."""

    _db_name = "ReadCaseData"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class read_case_data(_CommandSetting):
    """read_case_data command."""

    _db_name = "ReadCaseData"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class WriteCase(_CommandSetting):
    """WriteCase command object."""

    _db_name = "WriteCase"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class write_case(_CommandSetting):
    """write_case command."""

    _db_name = "WriteCase"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class WriteData(_CommandSetting):
    """WriteData command object."""

    _db_name = "WriteData"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class write_data(_CommandSetting):
    """write_data command."""

    _db_name = "WriteData"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class WriteCaseData(_CommandSetting):
    """WriteCaseData command object."""

    _db_name = "WriteCaseData"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class write_case_data(_CommandSetting):
    """write_case_data command."""

    _db_name = "WriteCaseData"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class Initialize(_CommandSetting):
    """Initialize command object."""

    _db_name = "Initialize"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class initialize(_CommandSetting):
    """initialize command."""

    _db_name = "Initialize"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class Calculate(_CommandSetting):
    """Calculate command object."""

    _db_name = "Calculate"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class calculate(_CommandSetting):
    """calculate command."""

    _db_name = "Calculate"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class Iterate(_CommandSetting):
    """Iterate command object."""

    _db_name = "Iterate"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class iterate(_CommandSetting):
    """iterate command."""

    _db_name = "Iterate"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class DualTimeIterate(_CommandSetting):
    """DualTimeIterate command object."""

    _db_name = "DualTimeIterate"

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class dual_time_iterate(_CommandSetting):
    """dual_time_iterate command."""

    _db_name = "DualTimeIterate"

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

