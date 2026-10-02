from typing import Annotated

from pydantic import AfterValidator

from ..base import round_float, round_optional_float
from ..conformers import ConformerClusteringSettings, ConformerGenSettingsUnion, OpenConfSettings
from ..method import Method
from ..opt_settings import OptimizationSettings
from ..settings import Settings
from ..solvent import Solvent, SolventModel, SolventSettings
from ..task import Task
from ..types import UUID
from .multistage_opt import MultiStageOptSettings
from .workflow import MoleculeWorkflow


class StrainWorkflow(MoleculeWorkflow):
    """
    Workflow for calculating the strain of a given molecular geometry.

    Inherited:
    :param initial_molecule: Molecule of interest
    :param mode: Mode for workflow (currently unused)

    New:
    :param conf_gen_settings: conformer-search settings
    :param multistage_opt_settings: optimization settings
    :param harmonic_constraint_spring_constant: spring constant for constraints, in kcal/mol/Å
    :param constrain_hydrogens: whether or not to constrain hydrogens

    Results:
    :param conformers: list of conformer UUIDs
    :param constrained_optimization: UUID of optimized strained structure
    :param strain: actual strain, in kcal/mol
    """

    conf_gen_settings: ConformerGenSettingsUnion | None = OpenConfSettings()

    conformer_clustering_settings: ConformerClusteringSettings | None = ConformerClusteringSettings()

    multistage_opt_settings: MultiStageOptSettings = MultiStageOptSettings(
        optimization_settings=[
            Settings(
                method=Method.GFN2_XTB,
                solvent_settings=SolventSettings(
                    solvent=Solvent.WATER,
                    model=SolventModel.ALPB,
                ),
                tasks=[Task.OPTIMIZE],
                opt_settings=OptimizationSettings.loose(),
            )
        ],
        singlepoint_settings=Settings(
            method=Method.G_XTB,
            tasks=[Task.ENERGY],
            solvent_settings=SolventSettings(solvent=Solvent.WATER, model=SolventModel.CPCMX),
        ),
    )

    harmonic_constraint_spring_constant: Annotated[float, AfterValidator(round_float(3))] = 5.0
    constrain_hydrogens: bool = False

    constrained_optimization: UUID | None = None
    conformers: list[UUID | None] = []
    strain: Annotated[float | None, AfterValidator(round_optional_float(3))] = None
