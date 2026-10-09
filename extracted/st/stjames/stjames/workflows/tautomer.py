"""Tautomer prediction workflow."""

from typing import Annotated, Literal

from pydantic import AfterValidator

from ..base import Base, round_float, round_optional_float
from ..conformers import ConformerGenSettingsUnion, OpenConfSettings
from ..method import Method
from ..mode import Mode
from ..settings import Settings
from ..solvent import Solvent, SolventModel, SolventSettings
from ..task import Task
from .multistage_opt import MultiStageOptSettings
from .workflow import DBCalculation, MoleculeWorkflow


class Tautomer(Base):
    """A tautomer.

    Attributes:
        energy: energy of the tautomer
        weight: statistical weight of the tautomer
        predicted_relative_energy: relative energy of the tautomer
        structures: UUIDs of the structures
        smiles: SMILES associated w/ the tautomer
    """

    energy: Annotated[float, AfterValidator(round_float(6))]
    weight: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    predicted_relative_energy: Annotated[float | None, AfterValidator(round_optional_float(6))] = None

    structures: list[DBCalculation] = []
    smiles: str | None = None


class TautomerWorkflow(MoleculeWorkflow):
    """A workflow to calculate tautomers.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (deprecated)

        conf_gen_settings: conformer-search settings, defaults to old "careful"
        multistage_opt_settings: optimization settings
        screening_window: maximum relative energy to include in initial screen, in kcal/mol
        final_correction: use COSMO-RS for final corrections when true

        tautomers: resulting Tautomers
    """

    conf_gen_settings: ConformerGenSettingsUnion = OpenConfSettings(
        max_confs=20,
    )

    multistage_opt_settings: MultiStageOptSettings = MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.AIMNET2_WB97MD3, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(
            method=Method.AIMNET2_WB97MD3, tasks=[Task.ENERGY], solvent_settings=SolventSettings(solvent=Solvent.WATER, model=SolventModel.CPCMX)
        ),
    )

    screening_window: Annotated[float, AfterValidator(round_float(3))] = 10.0
    final_correction: Literal["COSMO_RS"] | None = None

    mode: Mode = Mode.CAREFUL  # deprecated
    tautomers: list[Tautomer] = []
