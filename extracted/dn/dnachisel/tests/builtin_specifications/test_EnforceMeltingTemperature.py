from dnachisel import DnaOptimizationProblem
from dnachisel.builtin_specifications import (
    EnforceMeltingTemperature,
)


def test_enforce_melting_temperature():
    """Test by creating a new primer."""
    # Test issue #89
    problem = DnaOptimizationProblem(
        sequence="ATTTGAGACCCGACGTTAGA",
        objectives=[
            EnforceMeltingTemperature(mini=20, maxi=86, location=None, boost=1.0)
        ],
    )
    problem.resolve_constraints()
    problem.optimize()
