"""Intrinsic reaction coordinate (IRC) workflow."""

from pydantic import Field, PositiveFloat, field_validator

from ..settings import Settings
from ..types import UUID
from .workflow import MoleculeWorkflow


class IRCWorkflow(MoleculeWorkflow):
    """Workflow for Intrinsic Reaction Coordinate (IRC) calculations.

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow (not used)

        settings: Settings for running the IRC
        preopt: optimize the geometry before starting the IRC when true
        max_irc_steps: maximum number of steps for the IRC
        step_size: step size for the IRC (Å√amu)
        optimize_endpoints: optimize the endpoints once the IRC completes when true

        starting_TS: optimized TS before the IRC (==initial_molecule if preopt=False)
        irc_forward: forward calculation(s), either a single Calculation UUID or a list of them
        irc_backward: reverse calculation(s), either a single Calculation UUID or a list of them
        step_sizes_forward: actual step sizes taken along the forward direction (Å√amu)
        step_sizes_backward: actual step sizes taken along the backward direction (Å√amu)
        endpoint_opt_forward: optimization of forward endpoint (if optimize_endpoints=True)
        endpoint_opt_backward: optimization of backward endpoint (if optimize_endpoints=True)
    """

    settings: Settings

    preopt: bool = False
    max_irc_steps: int = 30
    step_size: PositiveFloat = 0.05
    optimize_endpoints: bool = False

    starting_TS: UUID | None = None

    irc_forward: UUID | list[UUID] = Field(default_factory=list)
    irc_backward: UUID | list[UUID] = Field(default_factory=list)

    step_sizes_forward: list[PositiveFloat] = Field(default_factory=list)
    step_sizes_backward: list[PositiveFloat] = Field(default_factory=list)

    endpoint_opt_forward: UUID | None = None
    endpoint_opt_backward: UUID | None = None

    def __str__(self) -> str:
        """Return the workflow representation as text."""
        return repr(self)

    def __repr__(self) -> str:
        """String representation of the workflow."""
        return f"<{type(self).__name__} {self.level_of_theory}>"

    @property
    def level_of_theory(self) -> str:
        """Level of theory for the workflow."""
        return self.settings.level_of_theory

    @field_validator("step_size", mode="after")
    @classmethod
    def validate_step_size(cls, step_size: float) -> PositiveFloat:
        """Validate the step size.

        Args:
            step_size: integration step size
        """
        if step_size < 1e-3 or step_size > 0.5:
            raise ValueError(f"Step size must be between 0.001 and 0.5 Å, got: {step_size}")

        return step_size

    @field_validator("settings", mode="after")
    @classmethod
    def validate_settings(cls, settings: Settings) -> Settings:
        """Validate the calculation settings.

        Args:
            settings: settings for the IRC calculation
        """
        if opt_settings := settings.opt_settings:
            if opt_settings.constraints:
                raise ValueError("IRCWorkflow does not support constraints")
            if opt_settings.optimize_cell:
                raise NotImplementedError("IRCWorkflow only supports fixed cell during optimization")

        return settings
