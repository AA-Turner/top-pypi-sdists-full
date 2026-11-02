"""Quality: grading, measured verdicts, review, benchmarks and evictions.
"""


def grade_fixture(probe, payload, *, library=None):
    from .fixtures import grade
    return grade(probe, payload, library=library)
