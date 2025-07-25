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
    "NonReflectingBoundaries",
    "NonReflectingBoundary",
    "PerforatedWallBoundaries",
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
    "ReadData",
    "ReadCaseData",
    "WriteCase",
    "WriteData",
    "WriteCaseData",
    "Initialize",
    "Calculate",
    "Iterate",
    "DualTimeIterate",
]

class Setup(_SingletonSetting):
    """Setup setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class General(_SingletonSetting):
    """General setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Models(_SingletonSetting):
    """Models setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Multiphase(_SingletonSetting):
    """Multiphase setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Energy(_SingletonSetting):
    """Energy setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Viscous(_SingletonSetting):
    """Viscous setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Radiation(_SingletonSetting):
    """Radiation setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Species(_SingletonSetting):
    """Species setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DiscretePhase(_SingletonSetting):
    """DiscretePhase setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Injections(_SingletonSetting):
    """Injections setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Injection(_CreatableNamedObjectSetting):
    """Injection setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class VirtualBladeModel(_SingletonSetting):
    """VirtualBladeModel setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Optics(_SingletonSetting):
    """Optics setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Structure(_SingletonSetting):
    """Structure setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Ablation(_SingletonSetting):
    """Ablation setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class EChemistry(_SingletonSetting):
    """EChemistry setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Battery(_SingletonSetting):
    """Battery setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SystemCoupling(_SingletonSetting):
    """SystemCoupling setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Sofc(_SingletonSetting):
    """Sofc setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Pemfc(_SingletonSetting):
    """Pemfc setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Materials(_SingletonSetting):
    """Materials setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FluidMaterials(_SingletonSetting):
    """FluidMaterials setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FluidMaterial(_CreatableNamedObjectSetting):
    """FluidMaterial setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SolidMaterials(_SingletonSetting):
    """SolidMaterials setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SolidMaterial(_CreatableNamedObjectSetting):
    """SolidMaterial setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class MixtureMaterials(_SingletonSetting):
    """MixtureMaterials setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MixtureMaterial(_CreatableNamedObjectSetting):
    """MixtureMaterial setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ParticleMixtureMaterials(_SingletonSetting):
    """ParticleMixtureMaterials setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParticleMixtureMaterial(_CreatableNamedObjectSetting):
    """ParticleMixtureMaterial setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class CellZoneConditions(_SingletonSetting):
    """CellZoneConditions setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CellZoneCondition(_NonCreatableNamedObjectSetting):
    """CellZoneCondition setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None):
        super().__init__(settings_source=settings_source, name=name)

class FluidCellZones(_SingletonSetting):
    """FluidCellZones setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FluidCellZone(_CreatableNamedObjectSetting):
    """FluidCellZone setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SolidCellZones(_SingletonSetting):
    """SolidCellZones setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SolidCellZone(_CreatableNamedObjectSetting):
    """SolidCellZone setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class BoundaryConditions(_SingletonSetting):
    """BoundaryConditions setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class BoundaryCondition(_NonCreatableNamedObjectSetting):
    """BoundaryCondition setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None):
        super().__init__(settings_source=settings_source, name=name)

class AxisBoundaries(_SingletonSetting):
    """AxisBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class AxisBoundary(_CreatableNamedObjectSetting):
    """AxisBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class DegassingBoundaries(_SingletonSetting):
    """DegassingBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DegassingBoundary(_CreatableNamedObjectSetting):
    """DegassingBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ExhaustFanBoundaries(_SingletonSetting):
    """ExhaustFanBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ExhaustFanBoundary(_CreatableNamedObjectSetting):
    """ExhaustFanBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class FanBoundaries(_SingletonSetting):
    """FanBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class FanBoundary(_CreatableNamedObjectSetting):
    """FanBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class GeometryBoundaries(_SingletonSetting):
    """GeometryBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class GeometryBoundary(_CreatableNamedObjectSetting):
    """GeometryBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class InletVentBoundaries(_SingletonSetting):
    """InletVentBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InletVentBoundary(_CreatableNamedObjectSetting):
    """InletVentBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class IntakeFanBoundaries(_SingletonSetting):
    """IntakeFanBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class IntakeFanBoundary(_CreatableNamedObjectSetting):
    """IntakeFanBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class InterfaceBoundaries(_SingletonSetting):
    """InterfaceBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InterfaceBoundary(_CreatableNamedObjectSetting):
    """InterfaceBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class InteriorBoundaries(_SingletonSetting):
    """InteriorBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InteriorBoundary(_CreatableNamedObjectSetting):
    """InteriorBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class MassFlowInlets(_SingletonSetting):
    """MassFlowInlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MassFlowInlet(_CreatableNamedObjectSetting):
    """MassFlowInlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class MassFlowOutlets(_SingletonSetting):
    """MassFlowOutlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class MassFlowOutlet(_CreatableNamedObjectSetting):
    """MassFlowOutlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NetworkBoundaries(_SingletonSetting):
    """NetworkBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NetworkBoundary(_CreatableNamedObjectSetting):
    """NetworkBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NetworkEndBoundaries(_SingletonSetting):
    """NetworkEndBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NetworkEndBoundary(_CreatableNamedObjectSetting):
    """NetworkEndBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class OutflowBoundaries(_SingletonSetting):
    """OutflowBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OutflowBoundary(_CreatableNamedObjectSetting):
    """OutflowBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class OutletVentBoundaries(_SingletonSetting):
    """OutletVentBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OutletVentBoundary(_CreatableNamedObjectSetting):
    """OutletVentBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class OversetBoundaries(_SingletonSetting):
    """OversetBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OversetBoundary(_CreatableNamedObjectSetting):
    """OversetBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PeriodicBoundaries(_SingletonSetting):
    """PeriodicBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PeriodicBoundary(_CreatableNamedObjectSetting):
    """PeriodicBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PorousJumpBoundaries(_SingletonSetting):
    """PorousJumpBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PorousJumpBoundary(_CreatableNamedObjectSetting):
    """PorousJumpBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PressureFarFieldBoundaries(_SingletonSetting):
    """PressureFarFieldBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PressureFarFieldBoundary(_CreatableNamedObjectSetting):
    """PressureFarFieldBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PressureInlets(_SingletonSetting):
    """PressureInlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PressureInlet(_CreatableNamedObjectSetting):
    """PressureInlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PressureOutlets(_SingletonSetting):
    """PressureOutlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PressureOutlet(_CreatableNamedObjectSetting):
    """PressureOutlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RadiatorBoundaries(_SingletonSetting):
    """RadiatorBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RadiatorBoundary(_CreatableNamedObjectSetting):
    """RadiatorBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RansLesInterfaceBoundaries(_SingletonSetting):
    """RansLesInterfaceBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RansLesInterfaceBoundary(_CreatableNamedObjectSetting):
    """RansLesInterfaceBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RecirculationInlets(_SingletonSetting):
    """RecirculationInlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RecirculationInlet(_CreatableNamedObjectSetting):
    """RecirculationInlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RecirculationOutlets(_SingletonSetting):
    """RecirculationOutlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RecirculationOutlet(_CreatableNamedObjectSetting):
    """RecirculationOutlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ShadowBoundaries(_SingletonSetting):
    """ShadowBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ShadowBoundary(_CreatableNamedObjectSetting):
    """ShadowBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SymmetryBoundaries(_SingletonSetting):
    """SymmetryBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SymmetryBoundary(_CreatableNamedObjectSetting):
    """SymmetryBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class VelocityInlets(_SingletonSetting):
    """VelocityInlets setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class VelocityInlet(_CreatableNamedObjectSetting):
    """VelocityInlet setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class WallBoundaries(_SingletonSetting):
    """WallBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class WallBoundary(_CreatableNamedObjectSetting):
    """WallBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NonReflectingBoundaries(_SingletonSetting):
    """NonReflectingBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NonReflectingBoundary(_NonCreatableNamedObjectSetting):
    """NonReflectingBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None):
        super().__init__(settings_source=settings_source, name=name)

class PerforatedWallBoundaries(_SingletonSetting):
    """PerforatedWallBoundaries setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PerforatedWallBoundary(_NonCreatableNamedObjectSetting):
    """PerforatedWallBoundary setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None):
        super().__init__(settings_source=settings_source, name=name)

class MeshInterfaces(_SingletonSetting):
    """MeshInterfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DynamicMesh(_SingletonSetting):
    """DynamicMesh setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReferenceValues(_SingletonSetting):
    """ReferenceValues setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReferenceFrames(_SingletonSetting):
    """ReferenceFrames setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReferenceFrame(_CreatableNamedObjectSetting):
    """ReferenceFrame setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class NamedExpressions(_SingletonSetting):
    """NamedExpressions setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class NamedExpression(_CreatableNamedObjectSetting):
    """NamedExpression setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Solution(_SingletonSetting):
    """Solution setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Methods(_SingletonSetting):
    """Methods setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Controls(_SingletonSetting):
    """Controls setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportDefinitions(_SingletonSetting):
    """ReportDefinitions setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Monitor(_SingletonSetting):
    """Monitor setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Residual(_SingletonSetting):
    """Residual setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportFiles(_SingletonSetting):
    """ReportFiles setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportFile(_CreatableNamedObjectSetting):
    """ReportFile setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ReportPlots(_SingletonSetting):
    """ReportPlots setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ReportPlot(_CreatableNamedObjectSetting):
    """ReportPlot setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ConvergenceConditions(_SingletonSetting):
    """ConvergenceConditions setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CellRegisters(_SingletonSetting):
    """CellRegisters setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CellRegister(_CreatableNamedObjectSetting):
    """CellRegister setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Initialization(_SingletonSetting):
    """Initialization setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CalculationActivity(_SingletonSetting):
    """CalculationActivity setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ExecuteCommands(_SingletonSetting):
    """ExecuteCommands setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CaseModification(_SingletonSetting):
    """CaseModification setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RunCalculation(_SingletonSetting):
    """RunCalculation setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Results(_SingletonSetting):
    """Results setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Surfaces(_SingletonSetting):
    """Surfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PointSurfaces(_SingletonSetting):
    """PointSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PointSurface(_CreatableNamedObjectSetting):
    """PointSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class LineSurfaces(_SingletonSetting):
    """LineSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class LineSurface(_CreatableNamedObjectSetting):
    """LineSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class RakeSurfaces(_SingletonSetting):
    """RakeSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class RakeSurface(_CreatableNamedObjectSetting):
    """RakeSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PlaneSurfaces(_SingletonSetting):
    """PlaneSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PlaneSurface(_CreatableNamedObjectSetting):
    """PlaneSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class IsoSurfaces(_SingletonSetting):
    """IsoSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class IsoSurface(_CreatableNamedObjectSetting):
    """IsoSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class IsoClips(_SingletonSetting):
    """IsoClips setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class IsoClip(_CreatableNamedObjectSetting):
    """IsoClip setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ZoneSurfaces(_SingletonSetting):
    """ZoneSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ZoneSurface(_CreatableNamedObjectSetting):
    """ZoneSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PartitionSurfaces(_SingletonSetting):
    """PartitionSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PartitionSurface(_CreatableNamedObjectSetting):
    """PartitionSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class TransformSurfaces(_SingletonSetting):
    """TransformSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class TransformSurface(_CreatableNamedObjectSetting):
    """TransformSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ImprintSurfaces(_SingletonSetting):
    """ImprintSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ImprintSurface(_CreatableNamedObjectSetting):
    """ImprintSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class PlaneSlices(_SingletonSetting):
    """PlaneSlices setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class PlaneSlice(_CreatableNamedObjectSetting):
    """PlaneSlice setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SphereSlices(_SingletonSetting):
    """SphereSlices setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SphereSlice(_CreatableNamedObjectSetting):
    """SphereSlice setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class QuadricSurfaces(_SingletonSetting):
    """QuadricSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class QuadricSurface(_CreatableNamedObjectSetting):
    """QuadricSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SurfaceCells(_SingletonSetting):
    """SurfaceCells setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SurfaceCell(_CreatableNamedObjectSetting):
    """SurfaceCell setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ExpressionVolumes(_SingletonSetting):
    """ExpressionVolumes setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ExpressionVolume(_CreatableNamedObjectSetting):
    """ExpressionVolume setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class GroupSurfaces(_SingletonSetting):
    """GroupSurfaces setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class GroupSurface(_CreatableNamedObjectSetting):
    """GroupSurface setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Graphics(_SingletonSetting):
    """Graphics setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Meshes(_SingletonSetting):
    """Meshes setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Mesh(_CreatableNamedObjectSetting):
    """Mesh setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Contours(_SingletonSetting):
    """Contours setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Contour(_CreatableNamedObjectSetting):
    """Contour setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Vectors(_SingletonSetting):
    """Vectors setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Vector(_CreatableNamedObjectSetting):
    """Vector setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Pathlines(_SingletonSetting):
    """Pathlines setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Pathline(_CreatableNamedObjectSetting):
    """Pathline setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ParticleTracks(_SingletonSetting):
    """ParticleTracks setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParticleTrack(_CreatableNamedObjectSetting):
    """ParticleTrack setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class LICs(_SingletonSetting):
    """LICs setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class LIC(_CreatableNamedObjectSetting):
    """LIC setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Plots(_SingletonSetting):
    """Plots setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class XYPlots(_SingletonSetting):
    """XYPlots setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class XYPlot(_CreatableNamedObjectSetting):
    """XYPlot setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class Histogram(_SingletonSetting):
    """Histogram setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CumulativePlots(_SingletonSetting):
    """CumulativePlots setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CumulativePlot(_CreatableNamedObjectSetting):
    """CumulativePlot setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class ProfileData(_SingletonSetting):
    """ProfileData setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InterpolatedData(_SingletonSetting):
    """InterpolatedData setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Scenes(_SingletonSetting):
    """Scenes setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Scene(_CreatableNamedObjectSetting):
    """Scene setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SceneAnimation(_SingletonSetting):
    """SceneAnimation setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Report(_SingletonSetting):
    """Report setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class DiscretePhaseHistogram(_SingletonSetting):
    """DiscretePhaseHistogram setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class Fluxes(_SingletonSetting):
    """Fluxes setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class SurfaceIntegrals(_SingletonSetting):
    """SurfaceIntegrals setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class VolumeIntegrals(_SingletonSetting):
    """VolumeIntegrals setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class InputParameters(_SingletonSetting):
    """InputParameters setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class OutputParameters(_SingletonSetting):
    """OutputParameters setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CustomFieldFunctions(_SingletonSetting):
    """CustomFieldFunctions setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CustomFieldFunction(_CreatableNamedObjectSetting):
    """CustomFieldFunction setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class CustomVectors(_SingletonSetting):
    """CustomVectors setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class CustomVector(_CreatableNamedObjectSetting):
    """CustomVector setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class SimulationReports(_SingletonSetting):
    """SimulationReports setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParametricStudies(_SingletonSetting):
    """ParametricStudies setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source)

class ParametricStudy(_CreatableNamedObjectSetting):
    """ParametricStudy setting."""

    def __init__(self, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name)

class DesignPoints(_SingletonSetting):
    """DesignPoints setting."""

    def __init__(self, parametric_studies: str, settings_source: SettingsBase | Solver | None = None):
        super().__init__(settings_source=settings_source, parametric_studies=parametric_studies)

class DesignPoint(_CreatableNamedObjectSetting):
    """DesignPoint setting."""

    def __init__(self, parametric_studies: str, settings_source: SettingsBase | Solver | None = None, name: str = None, new_instance_name: str = None):
        super().__init__(settings_source=settings_source, name=name, new_instance_name=new_instance_name, parametric_studies=parametric_studies)

class ReadCase(_CommandSetting):
    """ReadCase command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class ReadData(_CommandSetting):
    """ReadData command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class ReadCaseData(_CommandSetting):
    """ReadCaseData command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class WriteCase(_CommandSetting):
    """WriteCase command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class WriteData(_CommandSetting):
    """WriteData command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class WriteCaseData(_CommandSetting):
    """WriteCaseData command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class Initialize(_CommandSetting):
    """Initialize command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class Calculate(_CommandSetting):
    """Calculate command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class Iterate(_CommandSetting):
    """Iterate command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

class DualTimeIterate(_CommandSetting):
    """DualTimeIterate command."""

    def __new__(cls, settings_source: SettingsBase | Solver | None = None, **kwargs):
       instance = super().__new__(cls)
       instance.__init__(settings_source=settings_source, **kwargs)
       return instance(**kwargs)

