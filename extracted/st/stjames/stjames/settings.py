import logging
from typing import Any, Self, TypeVar

from pydantic import PositiveFloat, computed_field, field_validator, model_validator

from .base import Base, LowercaseStrEnum, UniqueList
from .basis_set import BasisSet
from .compute_settings import ComputeSettings
from .correction import Correction
from .engine import Engine
from .engine_compatibility import ENGINE_METHODS, ENGINE_SOLVENT_MODELS, METHOD_ENGINES, get_supported_corrections
from .excited_state_settings import ExcitedStateSettingsUnion
from .method import CORRECTABLE_NNP_METHODS, DFT_FUNCTIONALS, METHODS_WITH_CORRECTION, PREPACKAGED_METHODS, RANGE_SEPARATED_FUNCTIONALS, Method
from .mode import Mode
from .opt_settings import OptimizationSettings
from .pbc_dft_settings import PBCDFTSettings
from .scf_settings import SCFSettings
from .solvent import SolventModel, SolventSettings
from .task import Task
from .thermochem_settings import ThermochemistrySettings

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class OmegaTuning(LowercaseStrEnum):
    """Options for omega (range-separation parameter) tuning"""

    KOOPMANS = "koopmans"  # Baer et al. doi.org/10.1146/annurev.physchem.012809.103321
    GENERALIZED_KOOPMANS = "generalized_koopmans"  # Stein et al. doi.org/10.1103/PhysRevLett.105.266802
    HALF = "half"  # Cut the default omega in half


class Settings(Base):
    """
    Settings for (base) computational chemistry calculations.

    :param mode: calculation mode (affects thresholds for optimizations, etc.)
    :param tasks: tasks to perform (deprecated, specify in workflows or calculations instead)
    :param method: computational method
    :param basis_set: basis set to use (autopopulated for 3c methods)
    :param engine: computational engine to use (auto-selected if None)
    :param corrections: list of corrections to apply (e.g. D3BJ, D4)
    :param solvent_settings: solvent model settings (if any)
    :param omega: range-separation parameter (Bohr⁻¹) or method to tune it (optional)
    :param excited_state_settings: settings for excited-state calculations (if any)
    :param pbc_dft_settings: settings specific to DFT calculations on periodic systems
    :param scf_settings: SCF settings
    :param opt_settings: geometry optimization settings
    :param thermochem_settings: thermochemistry settings
    :param compute_settings: hardware settings
    """

    mode: Mode = Mode.AUTO

    # DEPRECATED - specify tasks only in BasicCalculationWorkflow or Calculation now
    tasks: UniqueList[Task] = [Task.ENERGY, Task.CHARGE, Task.DIPOLE]

    method: Method = Method.HARTREE_FOCK
    basis_set: BasisSet | None = None
    engine: Engine = None  # ty: ignore[invalid-assignment]
    corrections: UniqueList[Correction] = []
    solvent_settings: SolventSettings | None = None
    omega: OmegaTuning | PositiveFloat | None = None

    excited_state_settings: ExcitedStateSettingsUnion | None = None

    pbc_dft_settings: PBCDFTSettings | None = None
    # scf/opt settings will be set automatically based on mode, but can be overridden manually
    scf_settings: SCFSettings = SCFSettings()
    opt_settings: OptimizationSettings = OptimizationSettings()
    thermochem_settings: ThermochemistrySettings = ThermochemistrySettings()
    compute_settings: ComputeSettings = ComputeSettings()

    @model_validator(mode="before")
    @classmethod
    def _force_cosmors_recipe(cls, data: Any) -> Any:
        """Force the fixed COSMO-RS recipe.

        The COSMO-RS parameters were fit to surfaces from a specific level of theory
        (BP86/def2-TZVPD), so requesting the 'cosmors' solvent model pins the method and
        basis set regardless of what was supplied -- any other recipe silently
        reparametrizes the inputs. The engine defaults to GPU4PySCF, but an explicit PySCF
        request is honored; any other engine is overridden. Overriding a conflicting request
        is logged at WARNING.
        """
        if not isinstance(data, dict):
            return data
        solvent_settings = data.get("solvent_settings")
        if isinstance(solvent_settings, dict):
            model = solvent_settings.get("model")
        else:
            model = getattr(solvent_settings, "model", None)
        if model not in (SolventModel.COSMORS, SolventModel.COSMORS.value):
            return data

        forced_method, forced_basis = Method.BP86, "def2-TZVPD"
        allowed_engines = (Engine.PYSCF, Engine.PYSCF.value, Engine.GPU4PYSCF, Engine.GPU4PYSCF.value)

        requested_method = data.get("method")
        requested_basis = data.get("basis_set")
        requested_basis_name = requested_basis.get("name") if isinstance(requested_basis, dict) else getattr(requested_basis, "name", requested_basis)
        requested_engine = data.get("engine")
        resolved_engine = Engine.PYSCF if requested_engine in (Engine.PYSCF, Engine.PYSCF.value) else Engine.GPU4PYSCF

        requested = f"{requested_method or '?'} / {requested_basis_name or '?'} / {requested_engine or '?'}"
        forced = f"{forced_method.value} / {forced_basis} / {resolved_engine.value}"

        if (
            requested_method not in (None, forced_method, forced_method.value)
            or (requested_basis_name is not None and str(requested_basis_name).lower() != forced_basis.lower())
            or requested_engine not in (None, *allowed_engines)
        ):
            logger.warning("COSMO-RS overrides the requested recipe (%s) with %s.", requested, forced)

        data["method"] = forced_method
        data["basis_set"] = forced_basis
        data["engine"] = resolved_engine
        return data

    @model_validator(mode="after")
    def set_defaults(self) -> Self:
        """Set the calculation engine and any dependent defaults."""
        if not self.engine:
            engine = self.method.default_engine(is_periodic=self.pbc_dft_settings is not None)
            # Fall back to PySCF if the auto-selected engine has a solvent allowlist that excludes the requested model
            if self.solvent_settings and engine in ENGINE_SOLVENT_MODELS and self.solvent_settings.model not in ENGINE_SOLVENT_MODELS[engine]:
                engine = Engine.PYSCF
            self.engine = engine
        if self.engine == Engine.QUANTUM_ESPRESSO and self.pbc_dft_settings is None:
            self.pbc_dft_settings = PBCDFTSettings()
        return self

    @computed_field
    @property
    def level_of_theory(self) -> str:
        corrections = list(filter(lambda x: x not in (None, ""), self.corrections))

        if self.method in CORRECTABLE_NNP_METHODS:
            method = self.method.value if not corrections else f"{self.method.value}-{'-'.join(c.value for c in corrections)}"
        elif self.method in PREPACKAGED_METHODS or self.basis_set is None:
            method = self.method.value
        elif self.method in METHODS_WITH_CORRECTION or not corrections:
            method = f"{self.method.value}/{self.basis_set.name.lower()}"
        else:
            method = f"{self.method.value}-{'-'.join(c.value for c in corrections)}/{self.basis_set.name.lower()}"

        if self.solvent_settings is not None:
            method += f"/{self.solvent_settings.model.value}({self.solvent_settings.solvent.value})"

        return method

    @field_validator("mode")
    @classmethod
    def set_mode_auto(cls, mode: Mode) -> Mode:
        """Set the mode to RAPID if AUTO is selected."""
        if mode == Mode.AUTO:
            return Mode.RAPID

        return mode

    @model_validator(mode="after")
    def validate_and_build(self) -> Self:
        if self.mode == Mode.AUTO:
            self.mode = Mode.RAPID

        self.opt_settings = _assign_opt_settings_by_mode(self.mode, self.opt_settings)

        if self.method not in ENGINE_METHODS.get(self.engine, frozenset()):
            valid_engines = ", ".join(sorted(e.value for e in METHOD_ENGINES.get(self.method, [])))
            msg = f"'{self.method.value}' is not supported by engine '{self.engine.value}'. Supported engines: {valid_engines or 'none'}"
            raise ValueError(msg)

        allowed_corrections = get_supported_corrections(self.method, self.engine)
        if invalid_corrections := sorted(set(self.corrections) - allowed_corrections):
            invalid_str = ", ".join(c.value for c in invalid_corrections)
            allowed_str = ", ".join(sorted(c.value for c in allowed_corrections)) or "none"
            raise ValueError(f"{self.method.value}/{self.engine.value} does not support correction(s): {invalid_str}. Supported: {allowed_str}")

        if self.omega is not None and self.method not in RANGE_SEPARATED_FUNCTIONALS:
            functionals = "\n    ".join(RANGE_SEPARATED_FUNCTIONALS)
            raise ValueError(f"Omega tuning may only be specified for range-separated DFT functionals:\n    {functionals}.")

        if self.excited_state_settings:
            if self.engine not in {Engine.PYSCF, Engine.GPU4PYSCF}:
                raise ValueError("Excited-state calculations are only supported with the PySCF and GPU4PySCF engines.")

            if self.method not in DFT_FUNCTIONALS:
                functionals = "\n    ".join(DFT_FUNCTIONALS)
                raise ValueError(f"Excited-state calculations may only be performed with DFT:\n    {functionals}.")

        if self.solvent_settings and (supported := ENGINE_SOLVENT_MODELS.get(self.engine)) and self.solvent_settings.model not in supported:
            allowed = ", ".join(sorted(m.value for m in supported))
            raise ValueError(f"{self.engine.value} does not support the {self.solvent_settings.model.value.upper()} solvent model. Supported: {allowed}")

        return self

    def model_post_init(self, __context: Any, /) -> None:
        # figure out `optimize_ts`
        if Task.OPTIMIZE_TS in self.tasks:
            self.tasks.pop(self.tasks.index(Task.OPTIMIZE_TS))
            self.tasks.append(Task.OPTIMIZE)
            self.opt_settings.transition_state = True

        # composite methods have their own basis sets, so overwrite user stuff
        if self.method == Method.HF3C:
            self.basis_set = BasisSet(name="minix")
        elif self.method == Method.B973C:
            self.basis_set = BasisSet(name="def2-mTZVP")
        elif self.method == Method.R2SCAN3C:
            self.basis_set = BasisSet(name="def2-mTZVPP")
        elif self.method == Method.WB97X3C:
            self.basis_set = BasisSet(name="vDZP")

    @field_validator("basis_set", mode="before")
    @classmethod
    def parse_basis_set(cls, v: Any) -> BasisSet | dict[str, Any] | None:
        """Turn a string into a BasisSet object. (This is a little crude.)"""
        if isinstance(v, BasisSet):
            return None if v.name is None else v
        elif isinstance(v, dict):
            return None if v.get("name") is None else v
        elif isinstance(v, str):
            if len(v):
                return BasisSet(name=v)
            # "" is basically None, let's be real here...
            return None
        elif v is None:
            return None
        else:
            raise ValueError(f"invalid value {v} for basis_set")

    @field_validator("corrections", mode="before")
    @classmethod
    def remove_empty_string(cls, v: list[_T]) -> list[_T]:
        """Remove empty string values."""
        return [c for c in v if c] if v is not None else v


def _assign_opt_settings_by_mode(mode: Mode, opt_settings: OptimizationSettings) -> OptimizationSettings:
    """
    Assign optimization settings based on the mode.

    Constraints lead to a lot of noise, so we need to loosen the thresholds.

    cf. DLFIND manual, and https://www.cup.uni-muenchen.de/ch/compchem/geom/basic.html
    and the discussion at https://geometric.readthedocs.io/en/latest/how-it-works.html
    in periodic systems, "normal" is 0.05 eV/Å ~= 2e-3 Hartree/Å, and "careful" is 0.01 ~= 4e-4

    Note: thresholds here are in units of Hartree/Å, not Hartree/Bohr as listed in many places.
    """
    opt_settings.energy_threshold = 1e-6
    match mode:
        case Mode.RECKLESS:
            opt_settings.energy_threshold = 2e-5
            opt_settings.max_gradient_threshold = 7e-3
            opt_settings.rms_gradient_threshold = 6e-3
        case Mode.RAPID:
            opt_settings.energy_threshold = 5e-5
            opt_settings.max_gradient_threshold = 5e-3
            opt_settings.rms_gradient_threshold = 3.5e-3
        case Mode.CAREFUL:
            opt_settings.max_gradient_threshold = 9e-4
            opt_settings.rms_gradient_threshold = 6e-4
        case Mode.METICULOUS:
            opt_settings.max_gradient_threshold = 3e-5
            opt_settings.rms_gradient_threshold = 2e-5
        case Mode.DEBUG:
            opt_settings.max_gradient_threshold = 4e-6
            opt_settings.rms_gradient_threshold = 2e-6
        case _:
            raise ValueError(f"Unknown mode {mode.value}!")

    return opt_settings
