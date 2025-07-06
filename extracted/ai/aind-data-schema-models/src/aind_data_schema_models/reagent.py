"""Enums for reagents used in imaging experiments"""

from enum import Enum


class StainType(str, Enum):
    """Stain types for probes describing what is being labeled"""

    CYTOSKELETON = "Cytoskeleton"
    FILL = "Fill"
    RNA = "RNA"
    PROTEIN = "Protein"
    NUCLEAR = "Nuclear"
    VASCULATURE = "Vasculature"


class FluorophoreType(str, Enum):
    """Fluorophores types"""

    ALEXA = "Alexa Fluor"
    ATTO = "Atto"
    CF = "CF"
    CYANINE = "Cyanine"
    DYLIGHT = "DyLight"
