"""Example of use of the AvoidChanges as an objective to minimize modifications
of a sequence."""

import numpy

from dnachisel import AllowPrimer, DnaOptimizationProblem


def test_AllowPrimer():
    numpy.random.seed(123)
    primers = ["ATTGCGCCAAACT", "TAATCCACCCTAAT", "ATTCACACTTCAA"]
    problem = DnaOptimizationProblem(
        sequence=40 * "A",
        constraints=[
            AllowPrimer(
                tmin=50,
                tmax=60,
                max_homology_length=7,
                location=(10, 30),
                avoid_heterodim_with=primers,
            )
        ],
        logger=None,
    )
    problem.resolve_constraints()
    assert problem.all_constraints_pass()
