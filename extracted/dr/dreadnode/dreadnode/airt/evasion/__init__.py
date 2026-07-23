"""Model-evasion (adversarial-example) attacks against a black-box predict API.

Each algorithm lives in its own module for readability and easy extension; this
package re-exports the public factory functions and the shared types. Numeric
strategies (boundary / hopskipjump / simba / square / zoo) perturb feature
vectors under an L2/Linf budget; text strategies (text / deepwordbug / textfooler
/ pwws / bae / textbugger) perturb tokens under a token-fraction budget. Every
attack emits per-step traces of the intermediate candidate and the target's
verdict, so the full adversarial trajectory is visible in the Traces tab.
"""

from dreadnode.airt.evasion._base import (
    DistanceNorm,
    EvasionResult,
    EvasionStrategy,
    ModelEvasionAttack,
)
from dreadnode.airt.evasion.bae import bae_evasion
from dreadnode.airt.evasion.boundary import boundary_evasion
from dreadnode.airt.evasion.deepwordbug import deepwordbug_evasion
from dreadnode.airt.evasion.hopskipjump import hopskipjump_evasion
from dreadnode.airt.evasion.pwws import pwws_evasion
from dreadnode.airt.evasion.simba import simba_evasion
from dreadnode.airt.evasion.square import square_evasion
from dreadnode.airt.evasion.text import text_evasion
from dreadnode.airt.evasion.textbugger import textbugger_evasion
from dreadnode.airt.evasion.textfooler import textfooler_evasion
from dreadnode.airt.evasion.zoo import zoo_evasion

__all__ = [
    "DistanceNorm",
    "EvasionResult",
    "EvasionStrategy",
    "ModelEvasionAttack",
    "bae_evasion",
    "boundary_evasion",
    "deepwordbug_evasion",
    "hopskipjump_evasion",
    "pwws_evasion",
    "simba_evasion",
    "square_evasion",
    "text_evasion",
    "textbugger_evasion",
    "textfooler_evasion",
    "zoo_evasion",
]
