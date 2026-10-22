"""Redox potential workflow."""

from typing import Annotated, Any, Self

from pydantic import AfterValidator, field_validator, model_validator

from ..base import round_optional_float
from ..engine_compatibility import supports_open_shell
from ..method import FORCE_FIELD_METHODS, Method
from ..mode import Mode
from ..solvent import Solvent
from ..types import UUID
from .multistage_opt import MultiStageOptMixin, mso_settings_from_mode
from .workflow import MoleculeWorkflow

PRESET_REDOX_MODES = frozenset({Mode.RECKLESS, Mode.RAPID, Mode.CAREFUL, Mode.METICULOUS})
VALID_REDOX_MODES = PRESET_REDOX_MODES | {Mode.MANUAL}

# Force fields have no electronic structure, and GFN-FF and GFN0-xTB give inaccurate redox energies
_UNRELIABLE_REDOX_METHODS = FORCE_FIELD_METHODS | {Method.GFN_FF, Method.GFN0_XTB}


class RedoxPotentialWorkflow(MoleculeWorkflow, MultiStageOptMixin):
    """Workflow for computing redox potentials of molecules.

    Uses MultiStageOptSettings to compute single-point energies in acetonitrile.

    Inherited

    Attributes:
        initial_molecule: Molecule of interest
        mode: optional preset from `PRESET_REDOX_MODES` used only to build
            `multistage_opt_settings`; `Mode.MANUAL` when settings are supplied without one
        multistage_opt_settings: settings for optimization and singlepoint; auto-built from
            `mode` (with acetonitrile on the singlepoint) when not supplied

    Overridden:

        solvent: solvent to use for optimization

        reduction: calculate the reduction half-reaction when true
        oxidation: calculate the oxidation half-reaction when true
        neutral_molecule: UUID of the calculation for the neutral molecule
        anion_molecule: UUID of the calculation for the anion molecule
        cation_molecule: UUID of the calculation for the cation molecule
        reduction_potential: final potential in V
        oxidation_potential: final potential in V

    Legacy:

        redox_type: one of "reduction" or "oxidation"
        redox_potential: corresponding potential in V
    """

    solvent: Solvent = Solvent.ACETONITRILE

    reduction: bool = True
    oxidation: bool = True

    # legacy values - remove in future release!
    redox_type: str | None = None
    redox_potential: float | None = None

    # UUIDs
    neutral_molecule: UUID | None = None
    anion_molecule: UUID | None = None
    cation_molecule: UUID | None = None

    reduction_potential: Annotated[float | None, AfterValidator(round_optional_float(6))] = None
    oxidation_potential: Annotated[float | None, AfterValidator(round_optional_float(6))] = None

    @field_validator("solvent", mode="before")
    @classmethod
    def only_mecn_please(cls, val: Solvent | None) -> Solvent:
        """Only MeCN please!

        Args:
            val: solvent setting to validate
        """
        if val != Solvent.ACETONITRILE:
            raise ValueError("Only acetonitrile permitted!")

        return val

    @model_validator(mode="before")
    @classmethod
    def populate_mso_from_mode(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Resolve an automatic mode, and build MSO settings with acetonitrile from a preset mode when not supplied.

        An omitted, null, or automatic mode becomes `Mode.MANUAL` with settings and `Mode.RAPID` without.
        """
        has_msos = values.get("multistage_opt_settings") is not None
        mode = Mode(values.get("mode") or Mode.AUTO)
        if mode == Mode.AUTO:
            mode = Mode.MANUAL if has_msos else Mode.RAPID
        values["mode"] = mode

        if not has_msos and mode in PRESET_REDOX_MODES:
            values["multistage_opt_settings"] = mso_settings_from_mode(mode, solvent=Solvent.ACETONITRILE)

        return values

    @model_validator(mode="after")
    def validate_mode(self) -> "RedoxPotentialWorkflow":
        """Restrict mode to those supported by the redox potential workflow."""
        if self.mode not in VALID_REDOX_MODES:
            allowed = ", ".join(m.name for m in VALID_REDOX_MODES)
            raise ValueError(f"RedoxPotentialWorkflow only supports modes: {{{allowed}}}, got {self.mode.name}")

        return self

    @model_validator(mode="after")
    def validate_multistage_opt_settings(self) -> Self:
        """Check that the MSO settings can compute an acetonitrile redox potential.

        The energy-defining stage is the singlepoint, or the last optimization when there is
        no singlepoint.

        Raises:
            ValueError: no optimization stage, a stage cannot model open-shell species, a stage is
                solvated in anything but acetonitrile, or the energy-defining stage is unsolvated
                or uses a method without meaningful ionization energies or electron affinities
        """
        msos = self.multistage_opt_settings
        if not msos.optimization_settings:
            raise ValueError("Redox potentials require at least one optimization stage.")

        stages = [*msos.optimization_settings, *([msos.singlepoint_settings] if msos.singlepoint_settings else [])]

        # Adding or removing one electron flips the spin parity, so the neutral or the ion is open-shell
        if closed_shell := sorted({s.level_of_theory for s in stages if not supports_open_shell(s.method, s.engine)}):
            raise ValueError(f"Redox potentials require open-shell species, which {', '.join(closed_shell)} cannot model.")

        if any(s.solvent_settings is not None and s.solvent_settings.solvent != Solvent.ACETONITRILE for s in stages):
            raise ValueError("Only acetonitrile permitted!")

        energy_stage = msos.singlepoint_settings or msos.optimization_settings[-1]
        if energy_stage.solvent_settings is None:
            raise ValueError(f"Energy-defining stage {energy_stage.level_of_theory} must be solvated in acetonitrile.")
        if energy_stage.method in _UNRELIABLE_REDOX_METHODS:
            raise ValueError(f"Energy-defining stage {energy_stage.level_of_theory} does not give meaningful redox energies.")

        return self

    def model_post_init(self, __context: Any, /) -> None:
        """Keep back-compatible with old schema, then validate the half-reaction request."""
        if self.redox_type == "oxidation":
            self.oxidation = True
            self.reduction = False
            if self.oxidation_potential is None:
                self.oxidation_potential = self.redox_potential
        elif self.redox_type == "reduction":
            self.oxidation = False
            self.reduction = True
            if self.reduction_potential is None:
                self.reduction_potential = self.redox_potential

        if not self.reduction and not self.oxidation:
            raise ValueError("Neither reduction nor oxidation requested; no work to do.")
