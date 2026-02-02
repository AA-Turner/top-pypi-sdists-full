from ansys.fluent.core.generated.solver.settings_261 import root as settings_root_261
from ansys.fluent.core.generated.solver.settings_252 import root as settings_root_252
from ansys.fluent.core.generated.solver.settings_251 import root as settings_root_251
from ansys.fluent.core.generated.solver.settings_242 import root as settings_root_242
from ansys.fluent.core.generated.solver.settings_241 import root as settings_root_241
from ansys.fluent.core.generated.solver.settings_232 import root as settings_root_232
from ansys.fluent.core.generated.solver.settings_231 import root as settings_root_231
from ansys.fluent.core.generated.solver.settings_222 import root as settings_root_222


class Setup(
    type(settings_root_261.setup),
    type(settings_root_252.setup),
    type(settings_root_251.setup),
    type(settings_root_242.setup),
    type(settings_root_241.setup),
    type(settings_root_232.setup),
    type(settings_root_231.setup),
    type(settings_root_222.setup),
): ...

class General(
    type(settings_root_261.setup.general),
    type(settings_root_252.setup.general),
    type(settings_root_251.setup.general),
    type(settings_root_242.setup.general),
    type(settings_root_241.setup.general),
    type(settings_root_232.setup.general),
    type(settings_root_231.setup.general),
    type(settings_root_222.setup.general),
): ...

class Models(
    type(settings_root_261.setup.models),
    type(settings_root_252.setup.models),
    type(settings_root_251.setup.models),
    type(settings_root_242.setup.models),
    type(settings_root_241.setup.models),
    type(settings_root_232.setup.models),
    type(settings_root_231.setup.models),
    type(settings_root_222.setup.models),
): ...

class Multiphase(
    type(settings_root_261.setup.models.multiphase),
    type(settings_root_252.setup.models.multiphase),
    type(settings_root_251.setup.models.multiphase),
    type(settings_root_242.setup.models.multiphase),
    type(settings_root_241.setup.models.multiphase),
    type(settings_root_232.setup.models.multiphase),
    type(settings_root_231.setup.models.multiphase),
    type(settings_root_222.setup.models.multiphase),
): ...

class Energy(
    type(settings_root_261.setup.models.energy),
    type(settings_root_252.setup.models.energy),
    type(settings_root_251.setup.models.energy),
    type(settings_root_242.setup.models.energy),
    type(settings_root_241.setup.models.energy),
    type(settings_root_232.setup.models.energy),
    type(settings_root_231.setup.models.energy),
    type(settings_root_222.setup.models.energy),
): ...

class Viscous(
    type(settings_root_261.setup.models.viscous),
    type(settings_root_252.setup.models.viscous),
    type(settings_root_251.setup.models.viscous),
    type(settings_root_242.setup.models.viscous),
    type(settings_root_241.setup.models.viscous),
    type(settings_root_232.setup.models.viscous),
    type(settings_root_231.setup.models.viscous),
    type(settings_root_222.setup.models.viscous),
): ...

class Radiation(
    type(settings_root_261.setup.models.radiation),
    type(settings_root_252.setup.models.radiation),
    type(settings_root_251.setup.models.radiation),
    type(settings_root_242.setup.models.radiation),
    type(settings_root_241.setup.models.radiation),
    type(settings_root_232.setup.models.radiation),
): ...

class Species(
    type(settings_root_261.setup.models.species),
    type(settings_root_252.setup.models.species),
    type(settings_root_251.setup.models.species),
    type(settings_root_242.setup.models.species),
    type(settings_root_241.setup.models.species),
    type(settings_root_232.setup.models.species),
): ...

class DiscretePhase(
    type(settings_root_261.setup.models.discrete_phase),
    type(settings_root_252.setup.models.discrete_phase),
    type(settings_root_251.setup.models.discrete_phase),
    type(settings_root_242.setup.models.discrete_phase),
    type(settings_root_241.setup.models.discrete_phase),
    type(settings_root_232.setup.models.discrete_phase),
    type(settings_root_231.setup.models.discrete_phase),
): ...

class Injections(
    type(settings_root_261.setup.models.discrete_phase.injections),
    type(settings_root_252.setup.models.discrete_phase.injections),
    type(settings_root_251.setup.models.discrete_phase.injections),
    type(settings_root_242.setup.models.discrete_phase.injections),
    type(settings_root_241.setup.models.discrete_phase.injections),
    type(settings_root_232.setup.models.discrete_phase.injections),
    type(settings_root_231.setup.models.discrete_phase.injections),
): ...

class Injection(
    type(settings_root_261.setup.models.discrete_phase.injections.child_object_type),
    type(settings_root_252.setup.models.discrete_phase.injections.child_object_type),
    type(settings_root_251.setup.models.discrete_phase.injections.child_object_type),
    type(settings_root_242.setup.models.discrete_phase.injections.child_object_type),
    type(settings_root_241.setup.models.discrete_phase.injections.child_object_type),
    type(settings_root_232.setup.models.discrete_phase.injections.child_object_type),
    type(settings_root_231.setup.models.discrete_phase.injections.child_object_type),
): ...

class VirtualBladeModel(
    type(settings_root_261.setup.models.virtual_blade_model),
    type(settings_root_252.setup.models.virtual_blade_model),
    type(settings_root_251.setup.models.virtual_blade_model),
    type(settings_root_242.setup.models.virtual_blade_model),
    type(settings_root_241.setup.models.virtual_blade_model),
    type(settings_root_232.setup.models.virtual_blade_model),
    type(settings_root_231.setup.models.virtual_blade_model),
): ...

class Optics(
    type(settings_root_261.setup.models.optics),
    type(settings_root_252.setup.models.optics),
    type(settings_root_251.setup.models.optics),
    type(settings_root_242.setup.models.optics),
    type(settings_root_241.setup.models.optics),
    type(settings_root_232.setup.models.optics),
    type(settings_root_231.setup.models.optics),
): ...

class Structure(
    type(settings_root_261.setup.models.structure),
    type(settings_root_252.setup.models.structure),
    type(settings_root_251.setup.models.structure),
    type(settings_root_242.setup.models.structure),
    type(settings_root_241.setup.models.structure),
    type(settings_root_232.setup.models.structure),
): ...

class Ablation(
    type(settings_root_261.setup.models.ablation),
    type(settings_root_252.setup.models.ablation),
    type(settings_root_251.setup.models.ablation),
    type(settings_root_242.setup.models.ablation),
    type(settings_root_241.setup.models.ablation),
    type(settings_root_232.setup.models.ablation),
): ...

class EChemistry(
    type(settings_root_261.setup.models.echemistry),
    type(settings_root_252.setup.models.echemistry),
    type(settings_root_251.setup.models.echemistry),
    type(settings_root_242.setup.models.echemistry),
    type(settings_root_241.setup.models.echemistry),
): ...

class Battery(
    type(settings_root_261.setup.models.battery),
    type(settings_root_252.setup.models.battery),
    type(settings_root_251.setup.models.battery),
    type(settings_root_242.setup.models.battery),
    type(settings_root_241.setup.models.battery),
): ...

class SystemCoupling(
    type(settings_root_261.setup.models.system_coupling),
    type(settings_root_252.setup.models.system_coupling),
    type(settings_root_251.setup.models.system_coupling),
    type(settings_root_242.setup.models.system_coupling),
    type(settings_root_241.setup.models.system_coupling),
): ...

class Sofc(
    type(settings_root_261.setup.models.sofc),
    type(settings_root_252.setup.models.sofc),
    type(settings_root_251.setup.models.sofc),
    type(settings_root_242.setup.models.sofc),
    type(settings_root_241.setup.models.sofc),
): ...

class Pemfc(
    type(settings_root_261.setup.models.pemfc),
    type(settings_root_252.setup.models.pemfc),
    type(settings_root_251.setup.models.pemfc),
    type(settings_root_242.setup.models.pemfc),
): ...

class Materials(
    type(settings_root_261.setup.materials),
    type(settings_root_252.setup.materials),
    type(settings_root_251.setup.materials),
    type(settings_root_242.setup.materials),
    type(settings_root_241.setup.materials),
    type(settings_root_232.setup.materials),
    type(settings_root_231.setup.materials),
    type(settings_root_222.setup.materials),
): ...

class FluidMaterials(
    type(settings_root_261.setup.materials.fluid),
    type(settings_root_252.setup.materials.fluid),
    type(settings_root_251.setup.materials.fluid),
    type(settings_root_242.setup.materials.fluid),
    type(settings_root_241.setup.materials.fluid),
    type(settings_root_232.setup.materials.fluid),
    type(settings_root_231.setup.materials.fluid),
    type(settings_root_222.setup.materials.fluid),
): ...

class FluidMaterial(
    type(settings_root_261.setup.materials.fluid.child_object_type),
    type(settings_root_252.setup.materials.fluid.child_object_type),
    type(settings_root_251.setup.materials.fluid.child_object_type),
    type(settings_root_242.setup.materials.fluid.child_object_type),
    type(settings_root_241.setup.materials.fluid.child_object_type),
    type(settings_root_232.setup.materials.fluid.child_object_type),
    type(settings_root_231.setup.materials.fluid.child_object_type),
    type(settings_root_222.setup.materials.fluid.child_object_type),
): ...

class SolidMaterials(
    type(settings_root_261.setup.materials.solid),
    type(settings_root_252.setup.materials.solid),
    type(settings_root_251.setup.materials.solid),
    type(settings_root_242.setup.materials.solid),
    type(settings_root_241.setup.materials.solid),
    type(settings_root_232.setup.materials.solid),
    type(settings_root_231.setup.materials.solid),
    type(settings_root_222.setup.materials.solid),
): ...

class SolidMaterial(
    type(settings_root_261.setup.materials.solid.child_object_type),
    type(settings_root_252.setup.materials.solid.child_object_type),
    type(settings_root_251.setup.materials.solid.child_object_type),
    type(settings_root_242.setup.materials.solid.child_object_type),
    type(settings_root_241.setup.materials.solid.child_object_type),
    type(settings_root_232.setup.materials.solid.child_object_type),
    type(settings_root_231.setup.materials.solid.child_object_type),
    type(settings_root_222.setup.materials.solid.child_object_type),
): ...

class MixtureMaterials(
    type(settings_root_261.setup.materials.mixture),
    type(settings_root_252.setup.materials.mixture),
    type(settings_root_251.setup.materials.mixture),
    type(settings_root_242.setup.materials.mixture),
    type(settings_root_241.setup.materials.mixture),
    type(settings_root_232.setup.materials.mixture),
    type(settings_root_231.setup.materials.mixture),
    type(settings_root_222.setup.materials.mixture),
): ...

class MixtureMaterial(
    type(settings_root_261.setup.materials.mixture.child_object_type),
    type(settings_root_252.setup.materials.mixture.child_object_type),
    type(settings_root_251.setup.materials.mixture.child_object_type),
    type(settings_root_242.setup.materials.mixture.child_object_type),
    type(settings_root_241.setup.materials.mixture.child_object_type),
    type(settings_root_232.setup.materials.mixture.child_object_type),
    type(settings_root_231.setup.materials.mixture.child_object_type),
    type(settings_root_222.setup.materials.mixture.child_object_type),
): ...

class ParticleMixtureMaterials(
    type(settings_root_261.setup.materials.particle_mixture),
    type(settings_root_252.setup.materials.particle_mixture),
    type(settings_root_251.setup.materials.particle_mixture),
    type(settings_root_242.setup.materials.particle_mixture),
    type(settings_root_241.setup.materials.particle_mixture),
    type(settings_root_232.setup.materials.particle_mixture),
    type(settings_root_231.setup.materials.particle_mixture),
    type(settings_root_222.setup.materials.particle_mixture),
): ...

class ParticleMixtureMaterial(
    type(settings_root_261.setup.materials.particle_mixture.child_object_type),
    type(settings_root_252.setup.materials.particle_mixture.child_object_type),
    type(settings_root_251.setup.materials.particle_mixture.child_object_type),
    type(settings_root_242.setup.materials.particle_mixture.child_object_type),
    type(settings_root_241.setup.materials.particle_mixture.child_object_type),
    type(settings_root_232.setup.materials.particle_mixture.child_object_type),
    type(settings_root_231.setup.materials.particle_mixture.child_object_type),
    type(settings_root_222.setup.materials.particle_mixture.child_object_type),
): ...

class CellZoneConditions(
    type(settings_root_261.setup.cell_zone_conditions),
    type(settings_root_252.setup.cell_zone_conditions),
    type(settings_root_251.setup.cell_zone_conditions),
    type(settings_root_242.setup.cell_zone_conditions),
    type(settings_root_241.setup.cell_zone_conditions),
    type(settings_root_232.setup.cell_zone_conditions),
    type(settings_root_231.setup.cell_zone_conditions),
    type(settings_root_222.setup.cell_zone_conditions),
): ...

class CellZoneCondition(
    type(settings_root_261.setup.cell_zone_conditions.child_object_type),
    type(settings_root_252.setup.cell_zone_conditions.child_object_type),
    type(settings_root_251.setup.cell_zone_conditions.child_object_type),
    type(settings_root_242.setup.cell_zone_conditions.child_object_type),
    type(settings_root_241.setup.cell_zone_conditions.child_object_type),
    type(settings_root_232.setup.cell_zone_conditions.child_object_type),
    type(settings_root_231.setup.cell_zone_conditions.child_object_type),
): ...

class FluidCellZones(
    type(settings_root_261.setup.cell_zone_conditions.fluid),
    type(settings_root_252.setup.cell_zone_conditions.fluid),
    type(settings_root_251.setup.cell_zone_conditions.fluid),
    type(settings_root_242.setup.cell_zone_conditions.fluid),
    type(settings_root_241.setup.cell_zone_conditions.fluid),
    type(settings_root_232.setup.cell_zone_conditions.fluid),
    type(settings_root_231.setup.cell_zone_conditions.fluid),
    type(settings_root_222.setup.cell_zone_conditions.fluid),
): ...

class FluidCellZone(
    type(settings_root_261.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_252.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_251.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_242.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_241.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_232.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_231.setup.cell_zone_conditions.fluid.child_object_type),
    type(settings_root_222.setup.cell_zone_conditions.fluid.child_object_type),
): ...

class SolidCellZones(
    type(settings_root_261.setup.cell_zone_conditions.solid),
    type(settings_root_252.setup.cell_zone_conditions.solid),
    type(settings_root_251.setup.cell_zone_conditions.solid),
    type(settings_root_242.setup.cell_zone_conditions.solid),
    type(settings_root_241.setup.cell_zone_conditions.solid),
    type(settings_root_232.setup.cell_zone_conditions.solid),
    type(settings_root_231.setup.cell_zone_conditions.solid),
    type(settings_root_222.setup.cell_zone_conditions.solid),
): ...

class SolidCellZone(
    type(settings_root_261.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_252.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_251.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_242.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_241.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_232.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_231.setup.cell_zone_conditions.solid.child_object_type),
    type(settings_root_222.setup.cell_zone_conditions.solid.child_object_type),
): ...

class BoundaryConditions(
    type(settings_root_261.setup.boundary_conditions),
    type(settings_root_252.setup.boundary_conditions),
    type(settings_root_251.setup.boundary_conditions),
    type(settings_root_242.setup.boundary_conditions),
    type(settings_root_241.setup.boundary_conditions),
    type(settings_root_232.setup.boundary_conditions),
    type(settings_root_231.setup.boundary_conditions),
    type(settings_root_222.setup.boundary_conditions),
): ...

class BoundaryCondition(
    type(settings_root_261.setup.boundary_conditions.child_object_type),
    type(settings_root_252.setup.boundary_conditions.child_object_type),
    type(settings_root_251.setup.boundary_conditions.child_object_type),
    type(settings_root_242.setup.boundary_conditions.child_object_type),
    type(settings_root_241.setup.boundary_conditions.child_object_type),
    type(settings_root_232.setup.boundary_conditions.child_object_type),
    type(settings_root_231.setup.boundary_conditions.child_object_type),
): ...

class AxisBoundaries(
    type(settings_root_261.setup.boundary_conditions.axis),
    type(settings_root_252.setup.boundary_conditions.axis),
    type(settings_root_251.setup.boundary_conditions.axis),
    type(settings_root_242.setup.boundary_conditions.axis),
    type(settings_root_241.setup.boundary_conditions.axis),
    type(settings_root_232.setup.boundary_conditions.axis),
    type(settings_root_231.setup.boundary_conditions.axis),
    type(settings_root_222.setup.boundary_conditions.axis),
): ...

class AxisBoundary(
    type(settings_root_261.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_252.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_251.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_242.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_241.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_232.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_231.setup.boundary_conditions.axis.child_object_type),
    type(settings_root_222.setup.boundary_conditions.axis.child_object_type),
): ...

class DegassingBoundaries(
    type(settings_root_261.setup.boundary_conditions.degassing),
    type(settings_root_252.setup.boundary_conditions.degassing),
    type(settings_root_251.setup.boundary_conditions.degassing),
    type(settings_root_242.setup.boundary_conditions.degassing),
    type(settings_root_241.setup.boundary_conditions.degassing),
    type(settings_root_232.setup.boundary_conditions.degassing),
    type(settings_root_231.setup.boundary_conditions.degassing),
    type(settings_root_222.setup.boundary_conditions.degassing),
): ...

class DegassingBoundary(
    type(settings_root_261.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_252.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_251.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_242.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_241.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_232.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_231.setup.boundary_conditions.degassing.child_object_type),
    type(settings_root_222.setup.boundary_conditions.degassing.child_object_type),
): ...

class ExhaustFanBoundaries(
    type(settings_root_261.setup.boundary_conditions.exhaust_fan),
    type(settings_root_252.setup.boundary_conditions.exhaust_fan),
    type(settings_root_251.setup.boundary_conditions.exhaust_fan),
    type(settings_root_242.setup.boundary_conditions.exhaust_fan),
    type(settings_root_241.setup.boundary_conditions.exhaust_fan),
    type(settings_root_232.setup.boundary_conditions.exhaust_fan),
    type(settings_root_231.setup.boundary_conditions.exhaust_fan),
    type(settings_root_222.setup.boundary_conditions.exhaust_fan),
): ...

class ExhaustFanBoundary(
    type(settings_root_261.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_252.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_251.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_242.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_241.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_232.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_231.setup.boundary_conditions.exhaust_fan.child_object_type),
    type(settings_root_222.setup.boundary_conditions.exhaust_fan.child_object_type),
): ...

class FanBoundaries(
    type(settings_root_261.setup.boundary_conditions.fan),
    type(settings_root_252.setup.boundary_conditions.fan),
    type(settings_root_251.setup.boundary_conditions.fan),
    type(settings_root_242.setup.boundary_conditions.fan),
    type(settings_root_241.setup.boundary_conditions.fan),
    type(settings_root_232.setup.boundary_conditions.fan),
    type(settings_root_231.setup.boundary_conditions.fan),
    type(settings_root_222.setup.boundary_conditions.fan),
): ...

class FanBoundary(
    type(settings_root_261.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_252.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_251.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_242.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_241.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_232.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_231.setup.boundary_conditions.fan.child_object_type),
    type(settings_root_222.setup.boundary_conditions.fan.child_object_type),
): ...

class GeometryBoundaries(
    type(settings_root_261.setup.boundary_conditions.geometry),
    type(settings_root_252.setup.boundary_conditions.geometry),
    type(settings_root_251.setup.boundary_conditions.geometry),
    type(settings_root_242.setup.boundary_conditions.geometry),
    type(settings_root_241.setup.boundary_conditions.geometry),
    type(settings_root_232.setup.boundary_conditions.geometry),
    type(settings_root_231.setup.boundary_conditions.geometry),
    type(settings_root_222.setup.boundary_conditions.geometry),
): ...

class GeometryBoundary(
    type(settings_root_261.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_252.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_251.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_242.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_241.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_232.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_231.setup.boundary_conditions.geometry.child_object_type),
    type(settings_root_222.setup.boundary_conditions.geometry.child_object_type),
): ...

class InletVentBoundaries(
    type(settings_root_261.setup.boundary_conditions.inlet_vent),
    type(settings_root_252.setup.boundary_conditions.inlet_vent),
    type(settings_root_251.setup.boundary_conditions.inlet_vent),
    type(settings_root_242.setup.boundary_conditions.inlet_vent),
    type(settings_root_241.setup.boundary_conditions.inlet_vent),
    type(settings_root_232.setup.boundary_conditions.inlet_vent),
    type(settings_root_231.setup.boundary_conditions.inlet_vent),
    type(settings_root_222.setup.boundary_conditions.inlet_vent),
): ...

class InletVentBoundary(
    type(settings_root_261.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_252.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_251.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_242.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_241.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_232.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_231.setup.boundary_conditions.inlet_vent.child_object_type),
    type(settings_root_222.setup.boundary_conditions.inlet_vent.child_object_type),
): ...

class IntakeFanBoundaries(
    type(settings_root_261.setup.boundary_conditions.intake_fan),
    type(settings_root_252.setup.boundary_conditions.intake_fan),
    type(settings_root_251.setup.boundary_conditions.intake_fan),
    type(settings_root_242.setup.boundary_conditions.intake_fan),
    type(settings_root_241.setup.boundary_conditions.intake_fan),
    type(settings_root_232.setup.boundary_conditions.intake_fan),
    type(settings_root_231.setup.boundary_conditions.intake_fan),
    type(settings_root_222.setup.boundary_conditions.intake_fan),
): ...

class IntakeFanBoundary(
    type(settings_root_261.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_252.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_251.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_242.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_241.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_232.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_231.setup.boundary_conditions.intake_fan.child_object_type),
    type(settings_root_222.setup.boundary_conditions.intake_fan.child_object_type),
): ...

class InterfaceBoundaries(
    type(settings_root_261.setup.boundary_conditions.interface),
    type(settings_root_252.setup.boundary_conditions.interface),
    type(settings_root_251.setup.boundary_conditions.interface),
    type(settings_root_242.setup.boundary_conditions.interface),
    type(settings_root_241.setup.boundary_conditions.interface),
    type(settings_root_232.setup.boundary_conditions.interface),
    type(settings_root_231.setup.boundary_conditions.interface),
    type(settings_root_222.setup.boundary_conditions.interface),
): ...

class InterfaceBoundary(
    type(settings_root_261.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_252.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_251.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_242.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_241.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_232.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_231.setup.boundary_conditions.interface.child_object_type),
    type(settings_root_222.setup.boundary_conditions.interface.child_object_type),
): ...

class InteriorBoundaries(
    type(settings_root_261.setup.boundary_conditions.interior),
    type(settings_root_252.setup.boundary_conditions.interior),
    type(settings_root_251.setup.boundary_conditions.interior),
    type(settings_root_242.setup.boundary_conditions.interior),
    type(settings_root_241.setup.boundary_conditions.interior),
    type(settings_root_232.setup.boundary_conditions.interior),
    type(settings_root_231.setup.boundary_conditions.interior),
    type(settings_root_222.setup.boundary_conditions.interior),
): ...

class InteriorBoundary(
    type(settings_root_261.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_252.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_251.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_242.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_241.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_232.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_231.setup.boundary_conditions.interior.child_object_type),
    type(settings_root_222.setup.boundary_conditions.interior.child_object_type),
): ...

class MassFlowInlets(
    type(settings_root_261.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_252.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_251.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_242.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_241.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_232.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_231.setup.boundary_conditions.mass_flow_inlet),
    type(settings_root_222.setup.boundary_conditions.mass_flow_inlet),
): ...

class MassFlowInlet(
    type(settings_root_261.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.mass_flow_inlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.mass_flow_inlet.child_object_type),
): ...

class MassFlowOutlets(
    type(settings_root_261.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_252.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_251.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_242.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_241.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_232.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_231.setup.boundary_conditions.mass_flow_outlet),
    type(settings_root_222.setup.boundary_conditions.mass_flow_outlet),
): ...

class MassFlowOutlet(
    type(settings_root_261.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.mass_flow_outlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.mass_flow_outlet.child_object_type),
): ...

class NetworkBoundaries(
    type(settings_root_261.setup.boundary_conditions.network),
    type(settings_root_252.setup.boundary_conditions.network),
    type(settings_root_251.setup.boundary_conditions.network),
    type(settings_root_242.setup.boundary_conditions.network),
    type(settings_root_241.setup.boundary_conditions.network),
    type(settings_root_232.setup.boundary_conditions.network),
    type(settings_root_231.setup.boundary_conditions.network),
    type(settings_root_222.setup.boundary_conditions.network),
): ...

class NetworkBoundary(
    type(settings_root_261.setup.boundary_conditions.network.child_object_type),
    type(settings_root_252.setup.boundary_conditions.network.child_object_type),
    type(settings_root_251.setup.boundary_conditions.network.child_object_type),
    type(settings_root_242.setup.boundary_conditions.network.child_object_type),
    type(settings_root_241.setup.boundary_conditions.network.child_object_type),
    type(settings_root_232.setup.boundary_conditions.network.child_object_type),
    type(settings_root_231.setup.boundary_conditions.network.child_object_type),
    type(settings_root_222.setup.boundary_conditions.network.child_object_type),
): ...

class NetworkEndBoundaries(
    type(settings_root_261.setup.boundary_conditions.network_end),
    type(settings_root_252.setup.boundary_conditions.network_end),
    type(settings_root_251.setup.boundary_conditions.network_end),
    type(settings_root_242.setup.boundary_conditions.network_end),
    type(settings_root_241.setup.boundary_conditions.network_end),
    type(settings_root_232.setup.boundary_conditions.network_end),
    type(settings_root_231.setup.boundary_conditions.network_end),
    type(settings_root_222.setup.boundary_conditions.network_end),
): ...

class NetworkEndBoundary(
    type(settings_root_261.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_252.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_251.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_242.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_241.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_232.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_231.setup.boundary_conditions.network_end.child_object_type),
    type(settings_root_222.setup.boundary_conditions.network_end.child_object_type),
): ...

class OutflowBoundaries(
    type(settings_root_261.setup.boundary_conditions.outflow),
    type(settings_root_252.setup.boundary_conditions.outflow),
    type(settings_root_251.setup.boundary_conditions.outflow),
    type(settings_root_242.setup.boundary_conditions.outflow),
    type(settings_root_241.setup.boundary_conditions.outflow),
    type(settings_root_232.setup.boundary_conditions.outflow),
    type(settings_root_231.setup.boundary_conditions.outflow),
    type(settings_root_222.setup.boundary_conditions.outflow),
): ...

class OutflowBoundary(
    type(settings_root_261.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_252.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_251.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_242.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_241.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_232.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_231.setup.boundary_conditions.outflow.child_object_type),
    type(settings_root_222.setup.boundary_conditions.outflow.child_object_type),
): ...

class OutletVentBoundaries(
    type(settings_root_261.setup.boundary_conditions.outlet_vent),
    type(settings_root_252.setup.boundary_conditions.outlet_vent),
    type(settings_root_251.setup.boundary_conditions.outlet_vent),
    type(settings_root_242.setup.boundary_conditions.outlet_vent),
    type(settings_root_241.setup.boundary_conditions.outlet_vent),
    type(settings_root_232.setup.boundary_conditions.outlet_vent),
    type(settings_root_231.setup.boundary_conditions.outlet_vent),
    type(settings_root_222.setup.boundary_conditions.outlet_vent),
): ...

class OutletVentBoundary(
    type(settings_root_261.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_252.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_251.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_242.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_241.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_232.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_231.setup.boundary_conditions.outlet_vent.child_object_type),
    type(settings_root_222.setup.boundary_conditions.outlet_vent.child_object_type),
): ...

class OversetBoundaries(
    type(settings_root_261.setup.boundary_conditions.overset),
    type(settings_root_252.setup.boundary_conditions.overset),
    type(settings_root_251.setup.boundary_conditions.overset),
    type(settings_root_242.setup.boundary_conditions.overset),
    type(settings_root_241.setup.boundary_conditions.overset),
    type(settings_root_232.setup.boundary_conditions.overset),
    type(settings_root_231.setup.boundary_conditions.overset),
    type(settings_root_222.setup.boundary_conditions.overset),
): ...

class OversetBoundary(
    type(settings_root_261.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_252.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_251.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_242.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_241.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_232.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_231.setup.boundary_conditions.overset.child_object_type),
    type(settings_root_222.setup.boundary_conditions.overset.child_object_type),
): ...

class PeriodicBoundaries(
    type(settings_root_261.setup.boundary_conditions.periodic),
    type(settings_root_252.setup.boundary_conditions.periodic),
    type(settings_root_251.setup.boundary_conditions.periodic),
    type(settings_root_242.setup.boundary_conditions.periodic),
    type(settings_root_241.setup.boundary_conditions.periodic),
    type(settings_root_232.setup.boundary_conditions.periodic),
    type(settings_root_231.setup.boundary_conditions.periodic),
    type(settings_root_222.setup.boundary_conditions.periodic),
): ...

class PeriodicBoundary(
    type(settings_root_261.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_252.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_251.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_242.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_241.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_232.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_231.setup.boundary_conditions.periodic.child_object_type),
    type(settings_root_222.setup.boundary_conditions.periodic.child_object_type),
): ...

class PorousJumpBoundaries(
    type(settings_root_261.setup.boundary_conditions.porous_jump),
    type(settings_root_252.setup.boundary_conditions.porous_jump),
    type(settings_root_251.setup.boundary_conditions.porous_jump),
    type(settings_root_242.setup.boundary_conditions.porous_jump),
    type(settings_root_241.setup.boundary_conditions.porous_jump),
    type(settings_root_232.setup.boundary_conditions.porous_jump),
    type(settings_root_231.setup.boundary_conditions.porous_jump),
    type(settings_root_222.setup.boundary_conditions.porous_jump),
): ...

class PorousJumpBoundary(
    type(settings_root_261.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_252.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_251.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_242.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_241.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_232.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_231.setup.boundary_conditions.porous_jump.child_object_type),
    type(settings_root_222.setup.boundary_conditions.porous_jump.child_object_type),
): ...

class PressureFarFieldBoundaries(
    type(settings_root_261.setup.boundary_conditions.pressure_far_field),
    type(settings_root_252.setup.boundary_conditions.pressure_far_field),
    type(settings_root_251.setup.boundary_conditions.pressure_far_field),
    type(settings_root_242.setup.boundary_conditions.pressure_far_field),
    type(settings_root_241.setup.boundary_conditions.pressure_far_field),
    type(settings_root_232.setup.boundary_conditions.pressure_far_field),
    type(settings_root_231.setup.boundary_conditions.pressure_far_field),
    type(settings_root_222.setup.boundary_conditions.pressure_far_field),
): ...

class PressureFarFieldBoundary(
    type(settings_root_261.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_252.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_251.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_242.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_241.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_232.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_231.setup.boundary_conditions.pressure_far_field.child_object_type),
    type(settings_root_222.setup.boundary_conditions.pressure_far_field.child_object_type),
): ...

class PressureInlets(
    type(settings_root_261.setup.boundary_conditions.pressure_inlet),
    type(settings_root_252.setup.boundary_conditions.pressure_inlet),
    type(settings_root_251.setup.boundary_conditions.pressure_inlet),
    type(settings_root_242.setup.boundary_conditions.pressure_inlet),
    type(settings_root_241.setup.boundary_conditions.pressure_inlet),
    type(settings_root_232.setup.boundary_conditions.pressure_inlet),
    type(settings_root_231.setup.boundary_conditions.pressure_inlet),
    type(settings_root_222.setup.boundary_conditions.pressure_inlet),
): ...

class PressureInlet(
    type(settings_root_261.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.pressure_inlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.pressure_inlet.child_object_type),
): ...

class PressureOutlets(
    type(settings_root_261.setup.boundary_conditions.pressure_outlet),
    type(settings_root_252.setup.boundary_conditions.pressure_outlet),
    type(settings_root_251.setup.boundary_conditions.pressure_outlet),
    type(settings_root_242.setup.boundary_conditions.pressure_outlet),
    type(settings_root_241.setup.boundary_conditions.pressure_outlet),
    type(settings_root_232.setup.boundary_conditions.pressure_outlet),
    type(settings_root_231.setup.boundary_conditions.pressure_outlet),
    type(settings_root_222.setup.boundary_conditions.pressure_outlet),
): ...

class PressureOutlet(
    type(settings_root_261.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.pressure_outlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.pressure_outlet.child_object_type),
): ...

class RadiatorBoundaries(
    type(settings_root_261.setup.boundary_conditions.radiator),
    type(settings_root_252.setup.boundary_conditions.radiator),
    type(settings_root_251.setup.boundary_conditions.radiator),
    type(settings_root_242.setup.boundary_conditions.radiator),
    type(settings_root_241.setup.boundary_conditions.radiator),
    type(settings_root_232.setup.boundary_conditions.radiator),
    type(settings_root_231.setup.boundary_conditions.radiator),
    type(settings_root_222.setup.boundary_conditions.radiator),
): ...

class RadiatorBoundary(
    type(settings_root_261.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_252.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_251.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_242.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_241.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_232.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_231.setup.boundary_conditions.radiator.child_object_type),
    type(settings_root_222.setup.boundary_conditions.radiator.child_object_type),
): ...

class RansLesInterfaceBoundaries(
    type(settings_root_261.setup.boundary_conditions.rans_les_interface),
    type(settings_root_252.setup.boundary_conditions.rans_les_interface),
    type(settings_root_251.setup.boundary_conditions.rans_les_interface),
    type(settings_root_242.setup.boundary_conditions.rans_les_interface),
    type(settings_root_241.setup.boundary_conditions.rans_les_interface),
    type(settings_root_232.setup.boundary_conditions.rans_les_interface),
    type(settings_root_231.setup.boundary_conditions.rans_les_interface),
    type(settings_root_222.setup.boundary_conditions.rans_les_interface),
): ...

class RansLesInterfaceBoundary(
    type(settings_root_261.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_252.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_251.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_242.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_241.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_232.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_231.setup.boundary_conditions.rans_les_interface.child_object_type),
    type(settings_root_222.setup.boundary_conditions.rans_les_interface.child_object_type),
): ...

class RecirculationInlets(
    type(settings_root_261.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_252.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_251.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_242.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_241.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_232.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_231.setup.boundary_conditions.recirculation_inlet),
    type(settings_root_222.setup.boundary_conditions.recirculation_inlet),
): ...

class RecirculationInlet(
    type(settings_root_261.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.recirculation_inlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.recirculation_inlet.child_object_type),
): ...

class RecirculationOutlets(
    type(settings_root_261.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_252.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_251.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_242.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_241.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_232.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_231.setup.boundary_conditions.recirculation_outlet),
    type(settings_root_222.setup.boundary_conditions.recirculation_outlet),
): ...

class RecirculationOutlet(
    type(settings_root_261.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.recirculation_outlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.recirculation_outlet.child_object_type),
): ...

class ShadowBoundaries(
    type(settings_root_261.setup.boundary_conditions.shadow),
    type(settings_root_252.setup.boundary_conditions.shadow),
    type(settings_root_251.setup.boundary_conditions.shadow),
    type(settings_root_242.setup.boundary_conditions.shadow),
    type(settings_root_241.setup.boundary_conditions.shadow),
    type(settings_root_232.setup.boundary_conditions.shadow),
    type(settings_root_231.setup.boundary_conditions.shadow),
    type(settings_root_222.setup.boundary_conditions.shadow),
): ...

class ShadowBoundary(
    type(settings_root_261.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_252.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_251.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_242.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_241.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_232.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_231.setup.boundary_conditions.shadow.child_object_type),
    type(settings_root_222.setup.boundary_conditions.shadow.child_object_type),
): ...

class SymmetryBoundaries(
    type(settings_root_261.setup.boundary_conditions.symmetry),
    type(settings_root_252.setup.boundary_conditions.symmetry),
    type(settings_root_251.setup.boundary_conditions.symmetry),
    type(settings_root_242.setup.boundary_conditions.symmetry),
    type(settings_root_241.setup.boundary_conditions.symmetry),
    type(settings_root_232.setup.boundary_conditions.symmetry),
    type(settings_root_231.setup.boundary_conditions.symmetry),
    type(settings_root_222.setup.boundary_conditions.symmetry),
): ...

class SymmetryBoundary(
    type(settings_root_261.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_252.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_251.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_242.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_241.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_232.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_231.setup.boundary_conditions.symmetry.child_object_type),
    type(settings_root_222.setup.boundary_conditions.symmetry.child_object_type),
): ...

class VelocityInlets(
    type(settings_root_261.setup.boundary_conditions.velocity_inlet),
    type(settings_root_252.setup.boundary_conditions.velocity_inlet),
    type(settings_root_251.setup.boundary_conditions.velocity_inlet),
    type(settings_root_242.setup.boundary_conditions.velocity_inlet),
    type(settings_root_241.setup.boundary_conditions.velocity_inlet),
    type(settings_root_232.setup.boundary_conditions.velocity_inlet),
    type(settings_root_231.setup.boundary_conditions.velocity_inlet),
    type(settings_root_222.setup.boundary_conditions.velocity_inlet),
): ...

class VelocityInlet(
    type(settings_root_261.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_252.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_251.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_242.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_241.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_232.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_231.setup.boundary_conditions.velocity_inlet.child_object_type),
    type(settings_root_222.setup.boundary_conditions.velocity_inlet.child_object_type),
): ...

class WallBoundaries(
    type(settings_root_261.setup.boundary_conditions.wall),
    type(settings_root_252.setup.boundary_conditions.wall),
    type(settings_root_251.setup.boundary_conditions.wall),
    type(settings_root_242.setup.boundary_conditions.wall),
    type(settings_root_241.setup.boundary_conditions.wall),
    type(settings_root_232.setup.boundary_conditions.wall),
    type(settings_root_231.setup.boundary_conditions.wall),
    type(settings_root_222.setup.boundary_conditions.wall),
): ...

class WallBoundary(
    type(settings_root_261.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_252.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_251.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_242.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_241.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_232.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_231.setup.boundary_conditions.wall.child_object_type),
    type(settings_root_222.setup.boundary_conditions.wall.child_object_type),
): ...

class NonReflectingBoundary(
    type(settings_root_261.setup.boundary_conditions.non_reflecting_bc),
    type(settings_root_252.setup.boundary_conditions.non_reflecting_bc),
    type(settings_root_251.setup.boundary_conditions.non_reflecting_bc),
    type(settings_root_242.setup.boundary_conditions.non_reflecting_bc),
    type(settings_root_241.setup.boundary_conditions.non_reflecting_bc),
): ...

class PerforatedWallBoundary(
    type(settings_root_261.setup.boundary_conditions.perforated_wall),
    type(settings_root_252.setup.boundary_conditions.perforated_wall),
    type(settings_root_251.setup.boundary_conditions.perforated_wall),
    type(settings_root_242.setup.boundary_conditions.perforated_wall),
    type(settings_root_241.setup.boundary_conditions.perforated_wall),
): ...

class MeshInterfaces(
    type(settings_root_261.setup.mesh_interfaces),
    type(settings_root_252.setup.mesh_interfaces),
    type(settings_root_251.setup.mesh_interfaces),
    type(settings_root_242.setup.mesh_interfaces),
    type(settings_root_241.setup.mesh_interfaces),
    type(settings_root_232.setup.mesh_interfaces),
): ...

class DynamicMesh(
    type(settings_root_261.setup.dynamic_mesh),
    type(settings_root_252.setup.dynamic_mesh),
    type(settings_root_251.setup.dynamic_mesh),
): ...

class ReferenceValues(
    type(settings_root_261.setup.reference_values),
    type(settings_root_252.setup.reference_values),
    type(settings_root_251.setup.reference_values),
    type(settings_root_242.setup.reference_values),
    type(settings_root_241.setup.reference_values),
    type(settings_root_232.setup.reference_values),
    type(settings_root_231.setup.reference_values),
    type(settings_root_222.setup.reference_values),
): ...

class ReferenceFrames(
    type(settings_root_261.setup.reference_frames),
    type(settings_root_252.setup.reference_frames),
    type(settings_root_251.setup.reference_frames),
    type(settings_root_242.setup.reference_frames),
    type(settings_root_241.setup.reference_frames),
    type(settings_root_232.setup.reference_frames),
): ...

class ReferenceFrame(
    type(settings_root_261.setup.reference_frames.child_object_type),
    type(settings_root_252.setup.reference_frames.child_object_type),
    type(settings_root_251.setup.reference_frames.child_object_type),
    type(settings_root_242.setup.reference_frames.child_object_type),
    type(settings_root_241.setup.reference_frames.child_object_type),
    type(settings_root_232.setup.reference_frames.child_object_type),
): ...

class NamedExpressions(
    type(settings_root_261.setup.named_expressions),
    type(settings_root_252.setup.named_expressions),
    type(settings_root_251.setup.named_expressions),
    type(settings_root_242.setup.named_expressions),
    type(settings_root_241.setup.named_expressions),
    type(settings_root_232.setup.named_expressions),
): ...

class NamedExpression(
    type(settings_root_261.setup.named_expressions.child_object_type),
    type(settings_root_252.setup.named_expressions.child_object_type),
    type(settings_root_251.setup.named_expressions.child_object_type),
    type(settings_root_242.setup.named_expressions.child_object_type),
    type(settings_root_241.setup.named_expressions.child_object_type),
    type(settings_root_232.setup.named_expressions.child_object_type),
): ...

class Solution(
    type(settings_root_261.solution),
    type(settings_root_252.solution),
    type(settings_root_251.solution),
    type(settings_root_242.solution),
    type(settings_root_241.solution),
    type(settings_root_232.solution),
    type(settings_root_231.solution),
    type(settings_root_222.solution),
): ...

class Methods(
    type(settings_root_261.solution.methods),
    type(settings_root_252.solution.methods),
    type(settings_root_251.solution.methods),
    type(settings_root_242.solution.methods),
    type(settings_root_241.solution.methods),
    type(settings_root_232.solution.methods),
    type(settings_root_231.solution.methods),
    type(settings_root_222.solution.methods),
): ...

class Controls(
    type(settings_root_261.solution.controls),
    type(settings_root_252.solution.controls),
    type(settings_root_251.solution.controls),
    type(settings_root_242.solution.controls),
    type(settings_root_241.solution.controls),
    type(settings_root_232.solution.controls),
    type(settings_root_231.solution.controls),
    type(settings_root_222.solution.controls),
): ...

class ReportDefinitions(
    type(settings_root_261.solution.report_definitions),
    type(settings_root_252.solution.report_definitions),
    type(settings_root_251.solution.report_definitions),
    type(settings_root_242.solution.report_definitions),
    type(settings_root_241.solution.report_definitions),
    type(settings_root_232.solution.report_definitions),
    type(settings_root_231.solution.report_definitions),
    type(settings_root_222.solution.report_definitions),
): ...

class Monitor(
    type(settings_root_261.solution.monitor),
    type(settings_root_252.solution.monitor),
    type(settings_root_251.solution.monitor),
    type(settings_root_242.solution.monitor),
    type(settings_root_241.solution.monitor),
    type(settings_root_232.solution.monitor),
    type(settings_root_231.solution.monitor),
): ...

class Residual(
    type(settings_root_261.solution.monitor.residual),
    type(settings_root_252.solution.monitor.residual),
    type(settings_root_251.solution.monitor.residual),
    type(settings_root_242.solution.monitor.residual),
    type(settings_root_241.solution.monitor.residual),
): ...

class ReportFiles(
    type(settings_root_261.solution.monitor.report_files),
    type(settings_root_252.solution.monitor.report_files),
    type(settings_root_251.solution.monitor.report_files),
    type(settings_root_242.solution.monitor.report_files),
    type(settings_root_241.solution.monitor.report_files),
    type(settings_root_232.solution.monitor.report_files),
    type(settings_root_231.solution.monitor.report_files),
): ...

class ReportFile(
    type(settings_root_261.solution.monitor.report_files.child_object_type),
    type(settings_root_252.solution.monitor.report_files.child_object_type),
    type(settings_root_251.solution.monitor.report_files.child_object_type),
    type(settings_root_242.solution.monitor.report_files.child_object_type),
    type(settings_root_241.solution.monitor.report_files.child_object_type),
    type(settings_root_232.solution.monitor.report_files.child_object_type),
    type(settings_root_231.solution.monitor.report_files.child_object_type),
): ...

class ReportPlots(
    type(settings_root_261.solution.monitor.report_plots),
    type(settings_root_252.solution.monitor.report_plots),
    type(settings_root_251.solution.monitor.report_plots),
    type(settings_root_242.solution.monitor.report_plots),
    type(settings_root_241.solution.monitor.report_plots),
    type(settings_root_232.solution.monitor.report_plots),
    type(settings_root_231.solution.monitor.report_plots),
): ...

class ReportPlot(
    type(settings_root_261.solution.monitor.report_plots.child_object_type),
    type(settings_root_252.solution.monitor.report_plots.child_object_type),
    type(settings_root_251.solution.monitor.report_plots.child_object_type),
    type(settings_root_242.solution.monitor.report_plots.child_object_type),
    type(settings_root_241.solution.monitor.report_plots.child_object_type),
    type(settings_root_232.solution.monitor.report_plots.child_object_type),
    type(settings_root_231.solution.monitor.report_plots.child_object_type),
): ...

class ConvergenceConditions(
    type(settings_root_261.solution.monitor.convergence_conditions),
    type(settings_root_252.solution.monitor.convergence_conditions),
    type(settings_root_251.solution.monitor.convergence_conditions),
    type(settings_root_242.solution.monitor.convergence_conditions),
    type(settings_root_241.solution.monitor.convergence_conditions),
    type(settings_root_232.solution.monitor.convergence_conditions),
    type(settings_root_231.solution.monitor.convergence_conditions),
): ...

class CellRegisters(
    type(settings_root_261.solution.cell_registers),
    type(settings_root_252.solution.cell_registers),
    type(settings_root_251.solution.cell_registers),
    type(settings_root_242.solution.cell_registers),
    type(settings_root_241.solution.cell_registers),
    type(settings_root_232.solution.cell_registers),
    type(settings_root_231.solution.cell_registers),
): ...

class CellRegister(
    type(settings_root_261.solution.cell_registers.child_object_type),
    type(settings_root_252.solution.cell_registers.child_object_type),
    type(settings_root_251.solution.cell_registers.child_object_type),
    type(settings_root_242.solution.cell_registers.child_object_type),
    type(settings_root_241.solution.cell_registers.child_object_type),
    type(settings_root_232.solution.cell_registers.child_object_type),
    type(settings_root_231.solution.cell_registers.child_object_type),
): ...

class Initialization(
    type(settings_root_261.solution.initialization),
    type(settings_root_252.solution.initialization),
    type(settings_root_251.solution.initialization),
    type(settings_root_242.solution.initialization),
    type(settings_root_241.solution.initialization),
    type(settings_root_232.solution.initialization),
    type(settings_root_231.solution.initialization),
    type(settings_root_222.solution.initialization),
): ...

class CalculationActivity(
    type(settings_root_261.solution.calculation_activity),
    type(settings_root_252.solution.calculation_activity),
    type(settings_root_251.solution.calculation_activity),
    type(settings_root_242.solution.calculation_activity),
    type(settings_root_241.solution.calculation_activity),
    type(settings_root_232.solution.calculation_activity),
    type(settings_root_231.solution.calculation_activity),
): ...

class ExecuteCommands(
    type(settings_root_261.solution.calculation_activity.execute_commands),
    type(settings_root_252.solution.calculation_activity.execute_commands),
    type(settings_root_251.solution.calculation_activity.execute_commands),
    type(settings_root_242.solution.calculation_activity.execute_commands),
    type(settings_root_241.solution.calculation_activity.execute_commands),
    type(settings_root_232.solution.calculation_activity.execute_commands),
    type(settings_root_231.solution.calculation_activity.execute_commands),
): ...

class CaseModification(
    type(settings_root_261.solution.calculation_activity.case_modification),
    type(settings_root_252.solution.calculation_activity.case_modification),
    type(settings_root_251.solution.calculation_activity.case_modification),
    type(settings_root_242.solution.calculation_activity.case_modification),
    type(settings_root_241.solution.calculation_activity.case_modification),
): ...

class RunCalculation(
    type(settings_root_261.solution.run_calculation),
    type(settings_root_252.solution.run_calculation),
    type(settings_root_251.solution.run_calculation),
    type(settings_root_242.solution.run_calculation),
    type(settings_root_241.solution.run_calculation),
    type(settings_root_232.solution.run_calculation),
    type(settings_root_231.solution.run_calculation),
    type(settings_root_222.solution.run_calculation),
): ...

class Results(
    type(settings_root_261.results),
    type(settings_root_252.results),
    type(settings_root_251.results),
    type(settings_root_242.results),
    type(settings_root_241.results),
    type(settings_root_232.results),
    type(settings_root_231.results),
    type(settings_root_222.results),
): ...

class Surfaces(
    type(settings_root_261.results.surfaces),
    type(settings_root_252.results.surfaces),
    type(settings_root_251.results.surfaces),
    type(settings_root_242.results.surfaces),
    type(settings_root_241.results.surfaces),
    type(settings_root_232.results.surfaces),
    type(settings_root_231.results.surfaces),
    type(settings_root_222.results.surfaces),
): ...

class PointSurfaces(
    type(settings_root_261.results.surfaces.point_surface),
    type(settings_root_252.results.surfaces.point_surface),
    type(settings_root_251.results.surfaces.point_surface),
    type(settings_root_242.results.surfaces.point_surface),
    type(settings_root_241.results.surfaces.point_surface),
    type(settings_root_232.results.surfaces.point_surface),
): ...

class PointSurface(
    type(settings_root_261.results.surfaces.point_surface.child_object_type),
    type(settings_root_252.results.surfaces.point_surface.child_object_type),
    type(settings_root_251.results.surfaces.point_surface.child_object_type),
    type(settings_root_242.results.surfaces.point_surface.child_object_type),
    type(settings_root_241.results.surfaces.point_surface.child_object_type),
    type(settings_root_232.results.surfaces.point_surface.child_object_type),
): ...

class LineSurfaces(
    type(settings_root_261.results.surfaces.line_surface),
    type(settings_root_252.results.surfaces.line_surface),
    type(settings_root_251.results.surfaces.line_surface),
    type(settings_root_242.results.surfaces.line_surface),
    type(settings_root_241.results.surfaces.line_surface),
    type(settings_root_232.results.surfaces.line_surface),
): ...

class LineSurface(
    type(settings_root_261.results.surfaces.line_surface.child_object_type),
    type(settings_root_252.results.surfaces.line_surface.child_object_type),
    type(settings_root_251.results.surfaces.line_surface.child_object_type),
    type(settings_root_242.results.surfaces.line_surface.child_object_type),
    type(settings_root_241.results.surfaces.line_surface.child_object_type),
    type(settings_root_232.results.surfaces.line_surface.child_object_type),
): ...

class RakeSurfaces(
    type(settings_root_261.results.surfaces.rake_surface),
    type(settings_root_252.results.surfaces.rake_surface),
    type(settings_root_251.results.surfaces.rake_surface),
    type(settings_root_242.results.surfaces.rake_surface),
    type(settings_root_241.results.surfaces.rake_surface),
    type(settings_root_232.results.surfaces.rake_surface),
): ...

class RakeSurface(
    type(settings_root_261.results.surfaces.rake_surface.child_object_type),
    type(settings_root_252.results.surfaces.rake_surface.child_object_type),
    type(settings_root_251.results.surfaces.rake_surface.child_object_type),
    type(settings_root_242.results.surfaces.rake_surface.child_object_type),
    type(settings_root_241.results.surfaces.rake_surface.child_object_type),
    type(settings_root_232.results.surfaces.rake_surface.child_object_type),
): ...

class PlaneSurfaces(
    type(settings_root_261.results.surfaces.plane_surface),
    type(settings_root_252.results.surfaces.plane_surface),
    type(settings_root_251.results.surfaces.plane_surface),
    type(settings_root_242.results.surfaces.plane_surface),
    type(settings_root_241.results.surfaces.plane_surface),
    type(settings_root_232.results.surfaces.plane_surface),
    type(settings_root_231.results.surfaces.plane_surface),
    type(settings_root_222.results.surfaces.plane_surface),
): ...

class PlaneSurface(
    type(settings_root_261.results.surfaces.plane_surface.child_object_type),
    type(settings_root_252.results.surfaces.plane_surface.child_object_type),
    type(settings_root_251.results.surfaces.plane_surface.child_object_type),
    type(settings_root_242.results.surfaces.plane_surface.child_object_type),
    type(settings_root_241.results.surfaces.plane_surface.child_object_type),
    type(settings_root_232.results.surfaces.plane_surface.child_object_type),
    type(settings_root_231.results.surfaces.plane_surface.child_object_type),
    type(settings_root_222.results.surfaces.plane_surface.child_object_type),
): ...

class IsoSurfaces(
    type(settings_root_261.results.surfaces.iso_surface),
    type(settings_root_252.results.surfaces.iso_surface),
    type(settings_root_251.results.surfaces.iso_surface),
    type(settings_root_242.results.surfaces.iso_surface),
    type(settings_root_241.results.surfaces.iso_surface),
    type(settings_root_232.results.surfaces.iso_surface),
): ...

class IsoSurface(
    type(settings_root_261.results.surfaces.iso_surface.child_object_type),
    type(settings_root_252.results.surfaces.iso_surface.child_object_type),
    type(settings_root_251.results.surfaces.iso_surface.child_object_type),
    type(settings_root_242.results.surfaces.iso_surface.child_object_type),
    type(settings_root_241.results.surfaces.iso_surface.child_object_type),
    type(settings_root_232.results.surfaces.iso_surface.child_object_type),
): ...

class IsoClips(
    type(settings_root_261.results.surfaces.iso_clip),
    type(settings_root_252.results.surfaces.iso_clip),
    type(settings_root_251.results.surfaces.iso_clip),
    type(settings_root_242.results.surfaces.iso_clip),
    type(settings_root_241.results.surfaces.iso_clip),
): ...

class IsoClip(
    type(settings_root_261.results.surfaces.iso_clip.child_object_type),
    type(settings_root_252.results.surfaces.iso_clip.child_object_type),
    type(settings_root_251.results.surfaces.iso_clip.child_object_type),
    type(settings_root_242.results.surfaces.iso_clip.child_object_type),
    type(settings_root_241.results.surfaces.iso_clip.child_object_type),
): ...

class ZoneSurfaces(
    type(settings_root_261.results.surfaces.zone_surface),
    type(settings_root_252.results.surfaces.zone_surface),
    type(settings_root_251.results.surfaces.zone_surface),
    type(settings_root_242.results.surfaces.zone_surface),
    type(settings_root_241.results.surfaces.zone_surface),
): ...

class ZoneSurface(
    type(settings_root_261.results.surfaces.zone_surface.child_object_type),
    type(settings_root_252.results.surfaces.zone_surface.child_object_type),
    type(settings_root_251.results.surfaces.zone_surface.child_object_type),
    type(settings_root_242.results.surfaces.zone_surface.child_object_type),
    type(settings_root_241.results.surfaces.zone_surface.child_object_type),
): ...

class PartitionSurfaces(
    type(settings_root_261.results.surfaces.partition_surface),
    type(settings_root_252.results.surfaces.partition_surface),
    type(settings_root_251.results.surfaces.partition_surface),
    type(settings_root_242.results.surfaces.partition_surface),
    type(settings_root_241.results.surfaces.partition_surface),
): ...

class PartitionSurface(
    type(settings_root_261.results.surfaces.partition_surface.child_object_type),
    type(settings_root_252.results.surfaces.partition_surface.child_object_type),
    type(settings_root_251.results.surfaces.partition_surface.child_object_type),
    type(settings_root_242.results.surfaces.partition_surface.child_object_type),
    type(settings_root_241.results.surfaces.partition_surface.child_object_type),
): ...

class TransformSurfaces(
    type(settings_root_261.results.surfaces.transform_surface),
    type(settings_root_252.results.surfaces.transform_surface),
    type(settings_root_251.results.surfaces.transform_surface),
    type(settings_root_242.results.surfaces.transform_surface),
    type(settings_root_241.results.surfaces.transform_surface),
): ...

class TransformSurface(
    type(settings_root_261.results.surfaces.transform_surface.child_object_type),
    type(settings_root_252.results.surfaces.transform_surface.child_object_type),
    type(settings_root_251.results.surfaces.transform_surface.child_object_type),
    type(settings_root_242.results.surfaces.transform_surface.child_object_type),
    type(settings_root_241.results.surfaces.transform_surface.child_object_type),
): ...

class ImprintSurfaces(
    type(settings_root_261.results.surfaces.imprint_surface),
    type(settings_root_252.results.surfaces.imprint_surface),
    type(settings_root_251.results.surfaces.imprint_surface),
    type(settings_root_242.results.surfaces.imprint_surface),
    type(settings_root_241.results.surfaces.imprint_surface),
): ...

class ImprintSurface(
    type(settings_root_261.results.surfaces.imprint_surface.child_object_type),
    type(settings_root_252.results.surfaces.imprint_surface.child_object_type),
    type(settings_root_251.results.surfaces.imprint_surface.child_object_type),
    type(settings_root_242.results.surfaces.imprint_surface.child_object_type),
    type(settings_root_241.results.surfaces.imprint_surface.child_object_type),
): ...

class PlaneSlices(
    type(settings_root_261.results.surfaces.plane_slice),
    type(settings_root_252.results.surfaces.plane_slice),
    type(settings_root_251.results.surfaces.plane_slice),
    type(settings_root_242.results.surfaces.plane_slice),
    type(settings_root_241.results.surfaces.plane_slice),
): ...

class PlaneSlice(
    type(settings_root_261.results.surfaces.plane_slice.child_object_type),
    type(settings_root_252.results.surfaces.plane_slice.child_object_type),
    type(settings_root_251.results.surfaces.plane_slice.child_object_type),
    type(settings_root_242.results.surfaces.plane_slice.child_object_type),
    type(settings_root_241.results.surfaces.plane_slice.child_object_type),
): ...

class SphereSlices(
    type(settings_root_261.results.surfaces.sphere_slice),
    type(settings_root_252.results.surfaces.sphere_slice),
    type(settings_root_251.results.surfaces.sphere_slice),
    type(settings_root_242.results.surfaces.sphere_slice),
    type(settings_root_241.results.surfaces.sphere_slice),
): ...

class SphereSlice(
    type(settings_root_261.results.surfaces.sphere_slice.child_object_type),
    type(settings_root_252.results.surfaces.sphere_slice.child_object_type),
    type(settings_root_251.results.surfaces.sphere_slice.child_object_type),
    type(settings_root_242.results.surfaces.sphere_slice.child_object_type),
    type(settings_root_241.results.surfaces.sphere_slice.child_object_type),
): ...

class QuadricSurfaces(
    type(settings_root_261.results.surfaces.quadric_surface),
    type(settings_root_252.results.surfaces.quadric_surface),
    type(settings_root_251.results.surfaces.quadric_surface),
    type(settings_root_242.results.surfaces.quadric_surface),
    type(settings_root_241.results.surfaces.quadric_surface),
): ...

class QuadricSurface(
    type(settings_root_261.results.surfaces.quadric_surface.child_object_type),
    type(settings_root_252.results.surfaces.quadric_surface.child_object_type),
    type(settings_root_251.results.surfaces.quadric_surface.child_object_type),
    type(settings_root_242.results.surfaces.quadric_surface.child_object_type),
    type(settings_root_241.results.surfaces.quadric_surface.child_object_type),
): ...

class SurfaceCells(
    type(settings_root_261.results.surfaces.surface_cells),
    type(settings_root_252.results.surfaces.surface_cells),
    type(settings_root_251.results.surfaces.surface_cells),
    type(settings_root_242.results.surfaces.surface_cells),
    type(settings_root_241.results.surfaces.surface_cells),
): ...

class SurfaceCell(
    type(settings_root_261.results.surfaces.surface_cells.child_object_type),
    type(settings_root_252.results.surfaces.surface_cells.child_object_type),
    type(settings_root_251.results.surfaces.surface_cells.child_object_type),
    type(settings_root_242.results.surfaces.surface_cells.child_object_type),
    type(settings_root_241.results.surfaces.surface_cells.child_object_type),
): ...

class ExpressionVolumes(
    type(settings_root_261.results.surfaces.expression_volume),
    type(settings_root_252.results.surfaces.expression_volume),
    type(settings_root_251.results.surfaces.expression_volume),
): ...

class ExpressionVolume(
    type(settings_root_261.results.surfaces.expression_volume.child_object_type),
    type(settings_root_252.results.surfaces.expression_volume.child_object_type),
    type(settings_root_251.results.surfaces.expression_volume.child_object_type),
): ...

class GroupSurfaces(
    type(settings_root_261.results.surfaces.group_surface),
    type(settings_root_252.results.surfaces.group_surface),
    type(settings_root_251.results.surfaces.group_surface),
): ...

class GroupSurface(
    type(settings_root_261.results.surfaces.group_surface.child_object_type),
    type(settings_root_252.results.surfaces.group_surface.child_object_type),
    type(settings_root_251.results.surfaces.group_surface.child_object_type),
): ...

class Graphics(
    type(settings_root_261.results.graphics),
    type(settings_root_252.results.graphics),
    type(settings_root_251.results.graphics),
    type(settings_root_242.results.graphics),
    type(settings_root_241.results.graphics),
    type(settings_root_232.results.graphics),
    type(settings_root_231.results.graphics),
    type(settings_root_222.results.graphics),
): ...

class Meshes(
    type(settings_root_261.results.graphics.mesh),
    type(settings_root_252.results.graphics.mesh),
    type(settings_root_251.results.graphics.mesh),
    type(settings_root_242.results.graphics.mesh),
    type(settings_root_241.results.graphics.mesh),
    type(settings_root_232.results.graphics.mesh),
    type(settings_root_231.results.graphics.mesh),
    type(settings_root_222.results.graphics.mesh),
): ...

class Mesh(
    type(settings_root_261.results.graphics.mesh.child_object_type),
    type(settings_root_252.results.graphics.mesh.child_object_type),
    type(settings_root_251.results.graphics.mesh.child_object_type),
    type(settings_root_242.results.graphics.mesh.child_object_type),
    type(settings_root_241.results.graphics.mesh.child_object_type),
    type(settings_root_232.results.graphics.mesh.child_object_type),
    type(settings_root_231.results.graphics.mesh.child_object_type),
    type(settings_root_222.results.graphics.mesh.child_object_type),
): ...

class Contours(
    type(settings_root_261.results.graphics.contour),
    type(settings_root_252.results.graphics.contour),
    type(settings_root_251.results.graphics.contour),
    type(settings_root_242.results.graphics.contour),
    type(settings_root_241.results.graphics.contour),
    type(settings_root_232.results.graphics.contour),
    type(settings_root_231.results.graphics.contour),
    type(settings_root_222.results.graphics.contour),
): ...

class Contour(
    type(settings_root_261.results.graphics.contour.child_object_type),
    type(settings_root_252.results.graphics.contour.child_object_type),
    type(settings_root_251.results.graphics.contour.child_object_type),
    type(settings_root_242.results.graphics.contour.child_object_type),
    type(settings_root_241.results.graphics.contour.child_object_type),
    type(settings_root_232.results.graphics.contour.child_object_type),
    type(settings_root_231.results.graphics.contour.child_object_type),
    type(settings_root_222.results.graphics.contour.child_object_type),
): ...

class Vectors(
    type(settings_root_261.results.graphics.vector),
    type(settings_root_252.results.graphics.vector),
    type(settings_root_251.results.graphics.vector),
    type(settings_root_242.results.graphics.vector),
    type(settings_root_241.results.graphics.vector),
    type(settings_root_232.results.graphics.vector),
    type(settings_root_231.results.graphics.vector),
    type(settings_root_222.results.graphics.vector),
): ...

class Vector(
    type(settings_root_261.results.graphics.vector.child_object_type),
    type(settings_root_252.results.graphics.vector.child_object_type),
    type(settings_root_251.results.graphics.vector.child_object_type),
    type(settings_root_242.results.graphics.vector.child_object_type),
    type(settings_root_241.results.graphics.vector.child_object_type),
    type(settings_root_232.results.graphics.vector.child_object_type),
    type(settings_root_231.results.graphics.vector.child_object_type),
    type(settings_root_222.results.graphics.vector.child_object_type),
): ...

class Pathlines(
    type(settings_root_261.results.graphics.pathline),
    type(settings_root_252.results.graphics.pathline),
    type(settings_root_251.results.graphics.pathline),
    type(settings_root_242.results.graphics.pathline),
    type(settings_root_241.results.graphics.pathline),
    type(settings_root_232.results.graphics.pathline),
    type(settings_root_231.results.graphics.pathline),
): ...

class Pathline(
    type(settings_root_261.results.graphics.pathline.child_object_type),
    type(settings_root_252.results.graphics.pathline.child_object_type),
    type(settings_root_251.results.graphics.pathline.child_object_type),
    type(settings_root_242.results.graphics.pathline.child_object_type),
    type(settings_root_241.results.graphics.pathline.child_object_type),
    type(settings_root_232.results.graphics.pathline.child_object_type),
    type(settings_root_231.results.graphics.pathline.child_object_type),
): ...

class ParticleTracks(
    type(settings_root_261.results.graphics.particle_track),
    type(settings_root_252.results.graphics.particle_track),
    type(settings_root_251.results.graphics.particle_track),
    type(settings_root_242.results.graphics.particle_track),
    type(settings_root_241.results.graphics.particle_track),
    type(settings_root_232.results.graphics.particle_track),
    type(settings_root_231.results.graphics.particle_track),
): ...

class ParticleTrack(
    type(settings_root_261.results.graphics.particle_track.child_object_type),
    type(settings_root_252.results.graphics.particle_track.child_object_type),
    type(settings_root_251.results.graphics.particle_track.child_object_type),
    type(settings_root_242.results.graphics.particle_track.child_object_type),
    type(settings_root_241.results.graphics.particle_track.child_object_type),
    type(settings_root_232.results.graphics.particle_track.child_object_type),
    type(settings_root_231.results.graphics.particle_track.child_object_type),
): ...

class LICs(
    type(settings_root_261.results.graphics.lic),
    type(settings_root_252.results.graphics.lic),
    type(settings_root_251.results.graphics.lic),
    type(settings_root_242.results.graphics.lic),
    type(settings_root_241.results.graphics.lic),
    type(settings_root_232.results.graphics.lic),
    type(settings_root_231.results.graphics.lic),
    type(settings_root_222.results.graphics.lic),
): ...

class LIC(
    type(settings_root_261.results.graphics.lic.child_object_type),
    type(settings_root_252.results.graphics.lic.child_object_type),
    type(settings_root_251.results.graphics.lic.child_object_type),
    type(settings_root_242.results.graphics.lic.child_object_type),
    type(settings_root_241.results.graphics.lic.child_object_type),
    type(settings_root_232.results.graphics.lic.child_object_type),
    type(settings_root_231.results.graphics.lic.child_object_type),
    type(settings_root_222.results.graphics.lic.child_object_type),
): ...

class Plots(
    type(settings_root_261.results.plot),
    type(settings_root_252.results.plot),
    type(settings_root_251.results.plot),
    type(settings_root_242.results.plot),
    type(settings_root_241.results.plot),
    type(settings_root_232.results.plot),
    type(settings_root_231.results.plot),
): ...

class XYPlots(
    type(settings_root_261.results.plot.xy_plot),
    type(settings_root_252.results.plot.xy_plot),
    type(settings_root_251.results.plot.xy_plot),
    type(settings_root_242.results.plot.xy_plot),
    type(settings_root_241.results.plot.xy_plot),
    type(settings_root_232.results.plot.xy_plot),
    type(settings_root_231.results.plot.xy_plot),
): ...

class XYPlot(
    type(settings_root_261.results.plot.xy_plot.child_object_type),
    type(settings_root_252.results.plot.xy_plot.child_object_type),
    type(settings_root_251.results.plot.xy_plot.child_object_type),
    type(settings_root_242.results.plot.xy_plot.child_object_type),
    type(settings_root_241.results.plot.xy_plot.child_object_type),
    type(settings_root_232.results.plot.xy_plot.child_object_type),
    type(settings_root_231.results.plot.xy_plot.child_object_type),
): ...

class Histogram(
    type(settings_root_261.results.plot.histogram),
    type(settings_root_252.results.plot.histogram),
    type(settings_root_251.results.plot.histogram),
    type(settings_root_242.results.plot.histogram),
    type(settings_root_241.results.plot.histogram),
): ...

class CumulativePlots(
    type(settings_root_261.results.plot.cumulative_plot),
    type(settings_root_252.results.plot.cumulative_plot),
    type(settings_root_251.results.plot.cumulative_plot),
    type(settings_root_242.results.plot.cumulative_plot),
    type(settings_root_241.results.plot.cumulative_plot),
): ...

class CumulativePlot(
    type(settings_root_261.results.plot.cumulative_plot.child_object_type),
    type(settings_root_252.results.plot.cumulative_plot.child_object_type),
    type(settings_root_251.results.plot.cumulative_plot.child_object_type),
    type(settings_root_242.results.plot.cumulative_plot.child_object_type),
    type(settings_root_241.results.plot.cumulative_plot.child_object_type),
): ...

class ProfileData(
    type(settings_root_261.results.plot.profile_data),
    type(settings_root_252.results.plot.profile_data),
    type(settings_root_251.results.plot.profile_data),
    type(settings_root_242.results.plot.profile_data),
): ...

class InterpolatedData(
    type(settings_root_261.results.plot.interpolated_data),
    type(settings_root_252.results.plot.interpolated_data),
    type(settings_root_251.results.plot.interpolated_data),
    type(settings_root_242.results.plot.interpolated_data),
): ...

class Scenes(
    type(settings_root_261.results.scene),
    type(settings_root_252.results.scene),
    type(settings_root_251.results.scene),
    type(settings_root_242.results.scene),
    type(settings_root_241.results.scene),
    type(settings_root_232.results.scene),
    type(settings_root_231.results.scene),
): ...

class Scene(
    type(settings_root_261.results.scene.child_object_type),
    type(settings_root_252.results.scene.child_object_type),
    type(settings_root_251.results.scene.child_object_type),
    type(settings_root_242.results.scene.child_object_type),
    type(settings_root_241.results.scene.child_object_type),
    type(settings_root_232.results.scene.child_object_type),
    type(settings_root_231.results.scene.child_object_type),
): ...

class SceneAnimation(
    type(settings_root_261.results.animations.scene_animation),
    type(settings_root_252.results.animations.scene_animation),
    type(settings_root_251.results.animations.scene_animation),
    type(settings_root_242.results.animations.scene_animation),
    type(settings_root_241.results.animations.scene_animation),
): ...

class Report(
    type(settings_root_261.results.report),
    type(settings_root_252.results.report),
    type(settings_root_251.results.report),
    type(settings_root_242.results.report),
    type(settings_root_241.results.report),
    type(settings_root_232.results.report),
    type(settings_root_231.results.report),
): ...

class DiscretePhaseHistogram(
    type(settings_root_261.results.report.discrete_phase.histogram),
    type(settings_root_252.results.report.discrete_phase.histogram),
    type(settings_root_251.results.report.discrete_phase.histogram),
    type(settings_root_242.results.report.discrete_phase.histogram),
    type(settings_root_241.results.report.discrete_phase.histogram),
    type(settings_root_232.results.report.discrete_phase.histogram),
    type(settings_root_231.results.report.discrete_phase.histogram),
): ...

class Fluxes(
    type(settings_root_261.results.report.fluxes),
    type(settings_root_252.results.report.fluxes),
    type(settings_root_251.results.report.fluxes),
    type(settings_root_242.results.report.fluxes),
    type(settings_root_241.results.report.fluxes),
    type(settings_root_232.results.report.fluxes),
    type(settings_root_231.results.report.fluxes),
): ...

class SurfaceIntegrals(
    type(settings_root_261.results.report.surface_integrals),
    type(settings_root_252.results.report.surface_integrals),
    type(settings_root_251.results.report.surface_integrals),
    type(settings_root_242.results.report.surface_integrals),
    type(settings_root_241.results.report.surface_integrals),
    type(settings_root_232.results.report.surface_integrals),
    type(settings_root_231.results.report.surface_integrals),
): ...

class VolumeIntegrals(
    type(settings_root_261.results.report.volume_integrals),
    type(settings_root_252.results.report.volume_integrals),
    type(settings_root_251.results.report.volume_integrals),
    type(settings_root_242.results.report.volume_integrals),
    type(settings_root_241.results.report.volume_integrals),
    type(settings_root_232.results.report.volume_integrals),
    type(settings_root_231.results.report.volume_integrals),
): ...

class InputParameters(
    type(settings_root_261.parameters.input_parameters),
    type(settings_root_252.parameters.input_parameters),
    type(settings_root_251.parameters.input_parameters),
    type(settings_root_242.parameters.input_parameters),
    type(settings_root_241.parameters.input_parameters),
): ...

class OutputParameters(
    type(settings_root_261.parameters.output_parameters),
    type(settings_root_252.parameters.output_parameters),
    type(settings_root_251.parameters.output_parameters),
    type(settings_root_242.parameters.output_parameters),
    type(settings_root_241.parameters.output_parameters),
): ...

class CustomFieldFunctions(
    type(settings_root_261.results.custom_field_functions),
    type(settings_root_252.results.custom_field_functions),
    type(settings_root_251.results.custom_field_functions),
): ...

class CustomFieldFunction(
    type(settings_root_261.results.custom_field_functions.child_object_type),
    type(settings_root_252.results.custom_field_functions.child_object_type),
    type(settings_root_251.results.custom_field_functions.child_object_type),
): ...

class CustomVectors(
    type(settings_root_261.results.custom_vectors),
    type(settings_root_252.results.custom_vectors),
    type(settings_root_251.results.custom_vectors),
    type(settings_root_242.results.custom_vectors),
    type(settings_root_241.results.custom_vectors),
): ...

class CustomVector(
    type(settings_root_261.results.custom_vectors.child_object_type),
    type(settings_root_252.results.custom_vectors.child_object_type),
    type(settings_root_251.results.custom_vectors.child_object_type),
    type(settings_root_242.results.custom_vectors.child_object_type),
    type(settings_root_241.results.custom_vectors.child_object_type),
): ...

class SimulationReports(
    type(settings_root_261.results.report.simulation_reports),
    type(settings_root_252.results.report.simulation_reports),
    type(settings_root_251.results.report.simulation_reports),
    type(settings_root_242.results.report.simulation_reports),
    type(settings_root_241.results.report.simulation_reports),
    type(settings_root_232.results.report.simulation_reports),
    type(settings_root_231.results.report.simulation_reports),
): ...

class ParametricStudies(
    type(settings_root_261.parametric_studies),
    type(settings_root_252.parametric_studies),
    type(settings_root_251.parametric_studies),
    type(settings_root_242.parametric_studies),
    type(settings_root_241.parametric_studies),
    type(settings_root_232.parametric_studies),
    type(settings_root_231.parametric_studies),
    type(settings_root_222.parametric_studies),
): ...

class ParametricStudy(
    type(settings_root_261.parametric_studies.child_object_type),
    type(settings_root_252.parametric_studies.child_object_type),
    type(settings_root_251.parametric_studies.child_object_type),
    type(settings_root_242.parametric_studies.child_object_type),
    type(settings_root_241.parametric_studies.child_object_type),
    type(settings_root_232.parametric_studies.child_object_type),
    type(settings_root_231.parametric_studies.child_object_type),
    type(settings_root_222.parametric_studies.child_object_type),
): ...

class DesignPoints(
    type(settings_root_261.parametric_studies.design_points),
    type(settings_root_252.parametric_studies.design_points),
    type(settings_root_251.parametric_studies.design_points),
    type(settings_root_242.parametric_studies.design_points),
    type(settings_root_241.parametric_studies.design_points),
    type(settings_root_232.parametric_studies.design_points),
    type(settings_root_231.parametric_studies.design_points),
    type(settings_root_222.parametric_studies.design_points),
): ...

class DesignPoint(
    type(settings_root_261.parametric_studies.design_points.child_object_type),
    type(settings_root_252.parametric_studies.design_points.child_object_type),
    type(settings_root_251.parametric_studies.design_points.child_object_type),
    type(settings_root_242.parametric_studies.design_points.child_object_type),
    type(settings_root_241.parametric_studies.design_points.child_object_type),
    type(settings_root_232.parametric_studies.design_points.child_object_type),
    type(settings_root_231.parametric_studies.design_points.child_object_type),
    type(settings_root_222.parametric_studies.design_points.child_object_type),
): ...

class ReadCase(
    type(settings_root_261.file.read_case),
    type(settings_root_252.file.read_case),
    type(settings_root_251.file.read_case),
    type(settings_root_242.file.read_case),
    type(settings_root_241.file.read_case),
    type(settings_root_232.file.read_case),
    type(settings_root_231.file.read_case),
    type(settings_root_222.file.read_case),
): ...

class ReadData(
    type(settings_root_261.file.read_data),
    type(settings_root_252.file.read_data),
    type(settings_root_251.file.read_data),
    type(settings_root_242.file.read_data),
    type(settings_root_241.file.read_data),
    type(settings_root_232.file.read_data),
    type(settings_root_231.file.read_data),
    type(settings_root_222.file.read_data),
): ...

class ReadCaseData(
    type(settings_root_261.file.read_case_data),
    type(settings_root_252.file.read_case_data),
    type(settings_root_251.file.read_case_data),
    type(settings_root_242.file.read_case_data),
    type(settings_root_241.file.read_case_data),
    type(settings_root_232.file.read_case_data),
    type(settings_root_231.file.read_case_data),
    type(settings_root_222.file.read_case_data),
): ...

class WriteCase(
    type(settings_root_261.file.write_case),
    type(settings_root_252.file.write_case),
    type(settings_root_251.file.write_case),
    type(settings_root_242.file.write_case),
    type(settings_root_241.file.write_case),
): ...

class WriteData(
    type(settings_root_261.file.write_data),
    type(settings_root_252.file.write_data),
    type(settings_root_251.file.write_data),
    type(settings_root_242.file.write_data),
    type(settings_root_241.file.write_data),
): ...

class WriteCaseData(
    type(settings_root_261.file.write_case_data),
    type(settings_root_252.file.write_case_data),
    type(settings_root_251.file.write_case_data),
    type(settings_root_242.file.write_case_data),
    type(settings_root_241.file.write_case_data),
): ...

class Initialize(
    type(settings_root_261.solution.initialization.initialize),
    type(settings_root_252.solution.initialization.initialize),
    type(settings_root_251.solution.initialization.initialize),
    type(settings_root_242.solution.initialization.initialize),
    type(settings_root_241.solution.initialization.initialize),
    type(settings_root_232.solution.initialization.initialize),
    type(settings_root_231.solution.initialization.initialize),
    type(settings_root_222.solution.initialization.initialize),
): ...

class Calculate(
    type(settings_root_261.solution.run_calculation.calculate),
    type(settings_root_252.solution.run_calculation.calculate),
    type(settings_root_251.solution.run_calculation.calculate),
    type(settings_root_242.solution.run_calculation.calculate),
    type(settings_root_241.solution.run_calculation.calculate),
    type(settings_root_232.solution.run_calculation.calculate),
    type(settings_root_231.solution.run_calculation.calculate),
    type(settings_root_222.solution.run_calculation.calculate),
): ...

class Iterate(
    type(settings_root_261.solution.run_calculation.iterate),
    type(settings_root_252.solution.run_calculation.iterate),
    type(settings_root_251.solution.run_calculation.iterate),
    type(settings_root_242.solution.run_calculation.iterate),
    type(settings_root_241.solution.run_calculation.iterate),
    type(settings_root_232.solution.run_calculation.iterate),
    type(settings_root_231.solution.run_calculation.iterate),
    type(settings_root_222.solution.run_calculation.iterate),
): ...

class DualTimeIterate(
    type(settings_root_261.solution.run_calculation.dual_time_iterate),
    type(settings_root_252.solution.run_calculation.dual_time_iterate),
    type(settings_root_251.solution.run_calculation.dual_time_iterate),
    type(settings_root_242.solution.run_calculation.dual_time_iterate),
    type(settings_root_241.solution.run_calculation.dual_time_iterate),
    type(settings_root_232.solution.run_calculation.dual_time_iterate),
    type(settings_root_231.solution.run_calculation.dual_time_iterate),
    type(settings_root_222.solution.run_calculation.dual_time_iterate),
): ...

