"""Partial-charge methods used by molecular-simulation workflows."""

from .base import LowercaseStrEnum


class ChargeMethod(LowercaseStrEnum):
    """Method for computing partial charges for force-field simulations."""

    AMBER_AM1BCC = "amber_am1bcc"
    NAGL = "nagl"
    RESP = "resp"
