"""logP prediction workflow."""

from typing import Annotated

from pydantic import AfterValidator

from ..base import LowercaseStrEnum, round_float
from .workflow import SMILESWorkflow


class LogPMethod(LowercaseStrEnum):
    """
    Method used for logP prediction.

    CHEMPROP_SANGSTER2026: chemprop v2 D-MPNN trained on experimental logP (octanol/water
        partition coefficient) from the Sangster dataset
    CRIPPEN: RDKit implementation of the Wildman-Crippen atom-contribution model
    COSMORS: COSMO-RS activity coefficients
    """

    CHEMPROP_SANGSTER2026 = "chemprop_sangster2026"
    CRIPPEN = "crippen"
    COSMORS = "cosmors"


class LogPWorkflow(SMILESWorkflow):
    """logP prediction workflow.

    Inherited:
    :param initial_smiles: SMILES string of the molecule

    Inputs:
    :param logp_method: model used for logP prediction

    Results:
    :param logp: predicted logP value
    """

    logp_method: LogPMethod = LogPMethod.CHEMPROP_SANGSTER2026

    logp: Annotated[float, AfterValidator(round_float(3))] | None = None
