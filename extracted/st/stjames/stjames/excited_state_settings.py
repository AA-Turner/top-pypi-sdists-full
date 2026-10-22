"""Define excited state calculation settings."""

from abc import ABC
from typing import Annotated, Literal, Self

from pydantic import BaseModel, Field, PositiveInt, model_validator


class ExcitedStateSettings(BaseModel, ABC):
    """Settings for excited state calculations."""


class TDDFTSettings(ExcitedStateSettings):
    """Settings for TDDFT calculations.

    Attributes:
        tda: use Tamm-Dancoff approximation
        num_excitations: positive number of excitations to calculate
        target_root: positive root to target (for gradient/optimization); must not exceed `num_excitations` when set
        settings_type: excited-state settings discriminator, fixed to `tddft_settings`
    """

    tda: bool = True
    num_excitations: PositiveInt = 5
    target_root: PositiveInt | None = None

    settings_type: Literal["tddft_settings"] = "tddft_settings"

    @model_validator(mode="after")
    def validate_setup(self) -> Self:
        """Check that the target root is among requested excitations.

        Returns:
            validated settings

        Raises:
            ValueError: target root exceeds the excitation count
        """
        if self.target_root and (self.target_root > self.num_excitations):
            raise ValueError("target_root cannot be greater than num_excitations.")

        return self


ExcitedStateSettingsUnion = Annotated[TDDFTSettings, Field(discriminator="settings_type")]
