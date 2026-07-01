from ._core import Dimensionless, Log
from ._iso80000 import ACTIVITY_OF_SOLUTE

ACTIVITY_HPLUS = ACTIVITY_OF_SOLUTE["H+"]
ACTIVITY_AMINUS = ACTIVITY_OF_SOLUTE["A-"]
ACTIVITY_HA = ACTIVITY_OF_SOLUTE["HA"]
PH = (-1 * Log(ACTIVITY_HPLUS, base=10)).alias("pH")
KA = Dimensionless("Ka")
"""Acid dissociation constant, a measure of the strength of an acid in solution."""
PKA = (-1 * Log(KA, base=10)).alias("pKa")
