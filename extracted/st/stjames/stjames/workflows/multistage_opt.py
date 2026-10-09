"""Multi-stage optimization workflow."""

import logging
import re
from typing import Sequence

import more_itertools as mit
from pydantic import BaseModel, Field

from stjames.basis_set import BasisSet

from ..constraint import Constraint
from ..correction import Correction
from ..method import XTB_METHODS, Method
from ..mode import Mode
from ..opt_settings import OptimizationSettings
from ..settings import Settings
from ..solvent import Solvent, SolventModel, SolventSettings
from ..task import Task
from ..types import UUID
from .workflow import MoleculeWorkflow

logger = logging.getLogger(__name__)


class MultiStageOptSettings(BaseModel):
    """Settings for multi-stage optimizations.

    Attributes:
        optimization_settings: list of opt settings to apply successively
        singlepoint_settings: final single point settings
        frequencies: calculate frequencies on the last optimization step when true

    Examples:
    >>> s1 = Settings(method=Method.GFN2_XTB)
    >>> s2 = Settings(method=Method.R2SCAN3C, solvent_settings=SolventSettings(solvent=Solvent.HEXANE, model=SolventModel.CPCM))
    >>> msos = MultiStageOptSettings(optimization_settings=[s1], singlepoint_settings=s2)
    >>> msos.level_of_theory
    'r2scan_3c/cpcm(hexane)//gfn2_xtb'
    """

    optimization_settings: Sequence[Settings] = ()
    singlepoint_settings: Settings | None = None
    frequencies: bool = False

    def __str__(self) -> str:
        """Return the workflow representation as text."""
        return repr(self)

    def __repr__(self) -> str:
        """String representation of the settings."""
        return f"<{type(self).__name__} {self.level_of_theory}>"

    @property
    def level_of_theory(self) -> str:
        """Returns the level of theory for the workflow."""
        methods = [self.singlepoint_settings] if self.singlepoint_settings else []
        methods += reversed(self.optimization_settings)

        return "//".join(m.level_of_theory for m in methods)


class MultiStageOptWorkflow(MoleculeWorkflow, MultiStageOptSettings):
    """MoleculeWorkflow for multi-stage optimizations.

    Inherited

    Attributes:
        initial_molecule: Molecule of interest
        optimization_settings: list of opt settings to apply successively
        singlepoint_settings: final single point settings
        frequencies: calculate frequencies on the last optimization step when true

    Populated while running

        calculations: list of calculation UUIDs

    Examples:
    >>> from stjames.molecule import Atom, Molecule
    >>> He = Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=2, position=[0, 0, 0])])
    >>> s1 = Settings(method=Method.GFN0_XTB)
    >>> s2 = Settings(method=Method.R2SCAN3C, solvent_settings=SolventSettings(solvent=Solvent.WATER, model=SolventModel.CPCM))
    >>> msow = MultiStageOptWorkflow(initial_molecule=He, optimization_settings=[s1], singlepoint_settings=s2)
    >>> msow.level_of_theory
    'r2scan_3c/cpcm(water)//gfn0_xtb'
    """

    # Populated while running the workflow
    calculations: list[UUID | None] = Field(default_factory=list)

    def __repr__(self) -> str:
        """Represent MultiStageOptWorkflow with its calculation settings."""
        return f"<{type(self).__name__} {self.level_of_theory}>"


class MultiStageOptMixin(BaseModel):
    """Mixin for workflows that use MultiStageOptSettings.

    Attributes:
        multistage_opt_settings: settings for multistage optimization
    """

    multistage_opt_settings: MultiStageOptSettings


def mso_settings_from_method_string(
    methods: str,
    constraints: list[Constraint] | None = None,
    transition_state: bool = False,
    frequencies: bool = False,
) -> MultiStageOptSettings:
    """Helper function to construct multi-stage opt settings objects from a method string.

    Args:
        methods: method string with optimization stages and possible leading single-point stage
        constraints: geometric constraints to apply
        transition_state: optimize a transition state when true
        frequencies: calculate vibrational frequencies when true

    Examples:
    >>> mso_settings_from_method_string("r2SCAN-3c/CPCM(Water)//B3LYP-D3/6-31G(d)/CPCM(Water)//GFN2-xTB/ALPB(Water)//GFN0-xTB").level_of_theory
    'r2scan_3c/cpcm(water)//b3lyp-d3/6-31g(d)/cpcm(water)//gfn2_xtb/alpb(water)//gfn0_xtb'
    """
    solvent_models = "|".join(model.name for model in SolventModel)

    pattern = rf"""
        (?P<method>[^/()]+)                                 # Method + optional corrections
        (?:/(?P<basis_set>(?!{solvent_models})[^/]+?))?     # Optional basis_set, not starting with solvent model name
        (?:/(?P<solvent_model>{solvent_models})             # Optional solvent model
            \((?P<solvent>[^()]+)\))?                       # Solvent name in parentheses
        (?:\/\/|$)                                          # End or separator
"""
    constraints = constraints or []
    opt_settings = OptimizationSettings(constraints=constraints, transition_state=transition_state)
    OPT = [Task.OPTIMIZE if not transition_state else Task.OPTIMIZE_TS]

    valid_corrections = {c.name.lower() for c in Correction}  # Python3.11 hack

    def process(match: re.Match[str]) -> Settings:
        data = match.groupdict()

        method, corrections = mit.partition(lambda x: x.lower() in valid_corrections, data["method"].split("-"))
        solvent_settings = SolventSettings(solvent=Solvent(data["solvent"]), model=SolventModel(data["solvent_model"])) if data["solvent"] else None

        return Settings(
            method=Method("-".join(method)),
            basis_set=BasisSet(name=data["basis_set"]) if data["basis_set"] else None,
            tasks=OPT,
            solvent_settings=solvent_settings,
            opt_settings=opt_settings,
            corrections=[Correction(c) for c in corrections],
        )

    optimization_settings = [process(match) for match in re.finditer(pattern, methods, re.VERBOSE | re.IGNORECASE)]
    if len(optimization_settings) > 1:
        sp_settings = optimization_settings.pop(0)
        sp_settings.tasks = [Task.ENERGY]
    else:
        sp_settings = None

    optimization_settings = optimization_settings[::-1]
    if frequencies:
        optimization_settings[-1].tasks.append(Task.FREQUENCIES)

    return MultiStageOptSettings(
        optimization_settings=optimization_settings,
        singlepoint_settings=sp_settings,
        frequencies=frequencies,
    )


_MSO_FROM_MODE_VALID = frozenset({Mode.RECKLESS, Mode.RAPID, Mode.CAREFUL, Mode.METICULOUS})


def mso_settings_from_mode(
    mode: Mode,
    solvent: Solvent | None = None,
    xtb_preopt: bool = False,
    frequencies: bool = False,
) -> MultiStageOptSettings:
    """Build multi-stage opt settings for a standard accuracy mode.

    Optimizations run gas-phase; solvent (if given) attaches only to the singlepoint.

    Args:
        mode: one of RECKLESS, RAPID, CAREFUL, METICULOUS
        solvent: solvent for the singlepoint
        xtb_preopt: prepend an xTB pre-optimization (RAPID/CAREFUL/METICULOUS)
        frequencies: run frequencies on the last optimization

    Returns:
        settings with optimization and singlepoint stages assigned

    Examples:
    >>> mso_settings_from_mode(Mode.RAPID).level_of_theory
    'r2scan_3c//gfn2_xtb'
    >>> mso_settings_from_mode(Mode.CAREFUL, solvent=Solvent.WATER).level_of_theory
    'wb97x_3c/cpcm(water)//r2scan_3c'
    """
    if mode not in _MSO_FROM_MODE_VALID:
        raise NotImplementedError(f"Cannot build MSO settings from {mode=}")

    opt_settings = OptimizationSettings()
    OPT = [Task.OPTIMIZE]

    def opt(method: Method, basis_set: BasisSet | None = None, freq: bool = False) -> Settings:
        return Settings(
            method=method,
            basis_set=basis_set,
            tasks=OPT + [Task.FREQUENCIES] * freq,
            opt_settings=opt_settings,
        )

    def sp(method: Method, basis_set: BasisSet | None = None, solvent: Solvent | None = None) -> Settings:
        model = SolventModel.CPCMX if method in XTB_METHODS else SolventModel.CPCM
        return Settings(
            method=method,
            basis_set=basis_set,
            tasks=[Task.ENERGY],
            solvent_settings=SolventSettings(solvent=solvent, model=model) if solvent else None,
        )

    gfn0_pre = [opt(Method.GFN0_XTB)] if xtb_preopt else []
    gfn2_pre = [opt(Method.GFN2_XTB)] if xtb_preopt else []

    match mode:
        case Mode.RECKLESS:
            optimization_settings = [opt(Method.GFN_FF, freq=frequencies)]
            singlepoint_settings = sp(Method.GFN2_XTB, solvent=solvent)
        case Mode.RAPID:
            optimization_settings = [*gfn0_pre, opt(Method.GFN2_XTB, freq=frequencies)]
            singlepoint_settings = sp(Method.R2SCAN3C, solvent=solvent)
        case Mode.CAREFUL:
            optimization_settings = [*gfn2_pre, opt(Method.R2SCAN3C, freq=frequencies)]
            singlepoint_settings = sp(Method.WB97X3C, solvent=solvent)
        case Mode.METICULOUS:
            optimization_settings = [
                *gfn2_pre,
                opt(Method.R2SCAN3C),
                opt(Method.WB97X3C, freq=frequencies),
            ]
            singlepoint_settings = sp(Method.WB97MD3BJ, BasisSet(name="def2-TZVPPD"), solvent=solvent)
        case _:
            raise NotImplementedError(f"Cannot build MSO settings from {mode=}")

    return MultiStageOptSettings(
        optimization_settings=optimization_settings,
        singlepoint_settings=singlepoint_settings,
        frequencies=frequencies,
    )


def build_mso_settings(
    sp_method: Method,
    sp_basis_set: BasisSet | None,
    opt_methods: list[Method],
    opt_basis_sets: list[BasisSet | None],
    solvent: Solvent | None = None,
    use_solvent_for_opt: bool = False,
    constraints: list[Constraint] | None = None,
    transition_state: bool = False,
    frequencies: bool = False,
) -> MultiStageOptSettings:
    """Build settings for a multi-stage optimization.

    Args:
        sp_method: method for the final single-point calculation
        sp_basis_set: basis set for the final single-point calculation
        opt_methods: methods for the optimization stages
        opt_basis_sets: basis sets for the optimization stages
        solvent: solvent to use
        use_solvent_for_opt: conduct optimizations with solvent when true
        constraints: constraints for optimization
        transition_state: indicates that this is a transition state
        frequencies: calculate frequencies when true

    Returns:
        Settings for the optimization and final single-point calculation
    """
    if constraints is None:
        constraints = []

    opt_settings = OptimizationSettings(constraints=constraints, transition_state=transition_state)

    OPT = [Task.OPTIMIZE if not transition_state else Task.OPTIMIZE_TS]

    def opt(method: Method, basis_set: BasisSet | None = None, solvent: Solvent | None = None, freq: bool = False) -> Settings:
        """Generates optimization settings."""
        model = SolventModel.ALPB if method in XTB_METHODS else SolventModel.CPCM

        return Settings(
            method=method,
            basis_set=basis_set,
            tasks=OPT + [Task.FREQUENCIES] * freq,
            solvent_settings=SolventSettings(solvent=solvent, model=model) if (solvent and use_solvent_for_opt) else None,
            opt_settings=opt_settings,
        )

    def sp(method: Method, basis_set: BasisSet | None = None, solvent: Solvent | None = None) -> Settings:
        """Generate singlepoint settings."""
        model = SolventModel.CPCMX if method in XTB_METHODS else SolventModel.CPCM

        return Settings(
            method=method,
            basis_set=basis_set,
            tasks=[Task.ENERGY],
            solvent_settings=SolventSettings(solvent=solvent, model=model) if solvent else None,
        )

    return MultiStageOptSettings(
        optimization_settings=[
            opt(method=method, basis_set=basis_set, solvent=solvent, freq=frequencies) for method, basis_set in zip(opt_methods, opt_basis_sets, strict=True)
        ],
        singlepoint_settings=sp(method=sp_method, basis_set=sp_basis_set, solvent=solvent),
        frequencies=frequencies,
    )


def multi_stage_opt_settings_from_workflow(msow: MultiStageOptWorkflow) -> MultiStageOptSettings:
    """Extract multi-stage optimization settings from a workflow.

    Args:
        msow: workflow containing the settings

    Returns:
        Settings for the workflow's optimization and single-point stages

    Examples:
    >>> from stjames.molecule import Atom, Molecule
    >>> He = Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=2, position=[0, 0, 0])])
    >>> s1 = Settings(method=Method.GFN2_XTB)
    >>> s2 = Settings(method=Method.R2SCAN3C, solvent_settings=SolventSettings(solvent=Solvent.WATER, model=SolventModel.CPCM))
    >>> msow = MultiStageOptWorkflow(initial_molecule=He, optimization_settings=[s1], singlepoint_settings=s2)
    >>> msos = multi_stage_opt_settings_from_workflow(msow)
    >>> msos.level_of_theory
    'r2scan_3c/cpcm(water)//gfn2_xtb'
    """
    data = {k: getattr(msow, k) for k in MultiStageOptSettings.model_fields}
    return MultiStageOptSettings.model_construct(**data)
