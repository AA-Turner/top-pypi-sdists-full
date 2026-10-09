"""Define self-consistent field convergence settings."""

from .base import Base, LowercaseStrEnum


class UseSOSCF(LowercaseStrEnum):
    """Select when to use second-order SCF convergence."""

    ALWAYS = "always"
    UPON_FAILURE = "upon_failure"
    NEVER = "never"


class SCFSettings(Base):
    """Settings for SCF convergence.

    Attributes:
        max_iters: maximum number of SCF iterations to permit
        soscf: use SOSCF (second-order SCF) when true.
    """

    max_iters: int = 250
    soscf: UseSOSCF = UseSOSCF.UPON_FAILURE
