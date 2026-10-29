"""Configure enhanced molecular dynamics sampling."""

from itertools import pairwise
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, model_validator


class REST2Settings(BaseModel):
    """Configure replica exchange with solute tempering (REST2).

    Protein chains and parameterized small molecules form the tempered solute.
    Water and free ions remain unscaled. All replicas use the workflow's physical
    thermostat temperature; effective temperatures determine Hamiltonian scaling.
    User restraints remain identical across states.

    Default ladder contains eight states from 300 to 450 K with exchanges every
    1 ps. Workflows at other physical temperatures require a matching ladder.

    Outputs contain only the unscaled (λ=1) state trajectory from each independent
    ensemble. This follows the state through exchanges, so consecutive frames can
    come from different replicas. Tempered-state trajectories are not included.

    Attributes:
        type: enhanced sampling method discriminator
        effective_temperatures: strictly increasing replica temperature ladder,
            starting at the workflow temperature, in K
        exchange_interval_ps: interval between replica exchange attempts, in ps
    """

    model_config = ConfigDict(allow_inf_nan=False)

    type: Literal["rest2"] = "rest2"
    effective_temperatures: Annotated[list[PositiveFloat], Field(min_length=2)] = [300, 320, 340, 360, 380, 400, 425, 450]
    exchange_interval_ps: PositiveFloat = 1

    @model_validator(mode="after")
    def validate_temperature_ladder(self) -> Self:
        """Require strictly increasing effective temperatures."""
        if any(lower >= upper for lower, upper in pairwise(self.effective_temperatures)):
            raise ValueError("effective_temperatures must be strictly increasing")
        return self
