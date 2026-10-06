"""Significance of a change: the tests every comparing module shares."""
from .stats import (MIN_CONFIDENCE, bias_and_sigma, ftest_confidence,  # noqa: F401
                    is_significant, ks_from_counts, moments_from_sums,
                    sample_std, sigma_confidence, ttest_confidence)

# the test on the cycles
from .stats import cycle_bootstrap_confidence, cycle_bootstrap_many, cycle_changes, cycle_confidence  # noqa: F401
