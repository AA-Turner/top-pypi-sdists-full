"""Model-extraction attacks against a black-box classifier predict API.

Each algorithm lives in its own module for readability and easy extension; this
package re-exports the public factory functions and the shared types. Every attack
runs a query campaign, trains a surrogate that replicates the target's decision
boundary, and reports how faithfully the surrogate reproduces the target (fidelity /
agreement) for the queries spent. Each attack emits per-step traces of the
intermediate query batches and the round's surrogate fidelity, so the full
extraction trajectory is visible in the Traces tab.

Methods (PR1 ships the ones that need no shadow models):
- ``equation_solving_extraction`` - Tramer et al., USENIX'16 (exact for linear models)
- ``jacobian_extraction`` - Papernot et al., arXiv 1602.02697
- ``copycat_extraction`` - Correia-Silva et al., arXiv 1806.05476
- ``knockoff_extraction`` - Orekondy et al., arXiv 1812.02766
- ``activethief_extraction`` - Pal et al. 2020
- ``distillation_extraction`` - knowledge-distillation baseline
"""

from dreadnode.airt.extraction._base import (
    ExtractionEngine,
    ExtractionResult,
    ExtractionStrategy,
    ModelExtractionAttack,
    QueryPool,
    SurrogateName,
    kl_divergence,
    per_class_fidelity,
    predictions_to_labels,
    predictions_to_proba,
    soft_fidelity,
    top1_fidelity,
)
from dreadnode.airt.extraction._base import (
    _Surrogate as _Surrogate,
)
from dreadnode.airt.extraction.activethief import activethief_extraction
from dreadnode.airt.extraction.copycat import copycat_extraction
from dreadnode.airt.extraction.distillation import distillation_extraction
from dreadnode.airt.extraction.equation_solving import equation_solving_extraction
from dreadnode.airt.extraction.jacobian import jacobian_extraction
from dreadnode.airt.extraction.knockoff import knockoff_extraction

__all__ = [
    "ExtractionEngine",
    "ExtractionResult",
    "ExtractionStrategy",
    "ModelExtractionAttack",
    "QueryPool",
    "SurrogateName",
    "activethief_extraction",
    "copycat_extraction",
    "distillation_extraction",
    "equation_solving_extraction",
    "jacobian_extraction",
    "kl_divergence",
    "knockoff_extraction",
    "per_class_fidelity",
    "predictions_to_labels",
    "predictions_to_proba",
    "soft_fidelity",
    "top1_fidelity",
]
