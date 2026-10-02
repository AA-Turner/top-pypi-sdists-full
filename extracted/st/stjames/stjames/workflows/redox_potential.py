"""Redox potential workflow."""

from typing import Annotated, Any

from pydantic import AfterValidator, field_validator, model_validator

from ..base import round_optional_float
from ..mode import Mode
from ..solvent import Solvent
from ..types import UUID
from .multistage_opt import MultiStageOptMixin, mso_settings_from_mode
from .workflow import MoleculeWorkflow

VALID_REDOX_MODES = frozenset({Mode.RECKLESS, Mode.RAPID, Mode.CAREFUL, Mode.METICULOUS})


class RedoxPotentialWorkflow(MoleculeWorkflow, MultiStageOptMixin):
    """
    Workflow for computing redox potentials of molecules.

    Uses MultiStageOptSettings to compute single-point energies in acetonitrile.

    Inherited
    :param initial_molecule: Molecule of interest
    :param mode: Mode for workflow
    :param multistage_opt_settings: settings for optimization and singlepoint; auto-built from
        `mode` (with acetonitrile on the singlepoint) when not supplied

    Overridden:
    :param solvent: solvent to use for optimization

    New:
    :param reduction: whether or not to calculate the reduction half-reaction
    :param oxidation: whether or not to calculate the oxidation half-reaction
    :param neutral_molecule: UUID of the calculation for the neutral molecule
    :param anion_molecule: UUID of the calculation for the anion molecule
    :param cation_molecule: UUID of the calculation for the cation molecule
    :param reduction_potential: final potential in V
    :param oxidation_potential: final potential in V

    Legacy:
    :param redox_type: one of "reduction" or "oxidation"
    :param redox_potential: corresponding potential in V
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
        """Only MeCN please!"""
        if val != Solvent.ACETONITRILE:
            raise ValueError("Only acetonitrile permitted!")

        return val

    @model_validator(mode="before")
    @classmethod
    def populate_mso_from_mode(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Auto-build MSO settings from mode + acetonitrile when not supplied."""
        if "multistage_opt_settings" in values:
            return values

        raw_mode = values.get("mode", Mode.AUTO)
        if isinstance(raw_mode, Mode):
            mode = raw_mode
        else:
            try:
                mode = Mode(raw_mode)
            except ValueError:
                return values
        if mode == Mode.AUTO:
            mode = Mode.RAPID
        values["mode"] = mode

        if mode in VALID_REDOX_MODES:
            values["multistage_opt_settings"] = mso_settings_from_mode(mode, solvent=Solvent.ACETONITRILE)

        return values

    @model_validator(mode="after")
    def validate_mode(self) -> "RedoxPotentialWorkflow":
        """Restrict mode to those supported by the redox potential workflow."""
        if self.mode not in VALID_REDOX_MODES:
            allowed = ", ".join(m.name for m in VALID_REDOX_MODES)
            raise ValueError(f"RedoxPotentialWorkflow only supports modes: {{{allowed}}}, got {self.mode.name}")

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
