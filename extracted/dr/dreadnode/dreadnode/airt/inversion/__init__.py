"""Model-inversion attacks against a black-box classifier predict API.

Given only query access, these attacks reconstruct a representative input for
each target class by maximizing the target's confidence for that class - recovering
what a class "looks like" to the model (Fredrikson et al. 2015, MI-Face). When
classes correspond to individuals, this is a concrete privacy leak.

Each algorithm lives in its own module for readability and easy extension; this
package re-exports the public factory functions and the shared types. Every attack
emits per-step traces of the intermediate reconstruction and the target's
confidence, so the full inversion trajectory is visible in the Traces tab.

Strategies:
- ``confidence_inversion`` - MI-Face-style Gaussian hill climbing (Fredrikson et al. 2015)
- ``nes_inversion`` - Natural Evolution Strategies ascent, query-efficient in higher dimensions
"""

from dreadnode.airt.inversion._base import (
    InversionResult,
    InversionStrategy,
    ModelInversionAttack,
)
from dreadnode.airt.inversion.confidence import confidence_inversion
from dreadnode.airt.inversion.nes_inversion import nes_inversion

__all__ = [
    "InversionResult",
    "InversionStrategy",
    "ModelInversionAttack",
    "confidence_inversion",
    "nes_inversion",
]
