from snowflake.core.sequence import Sequence


test_sequence_template = Sequence(
    name="to_be_set",
    start=2,
    increment=2,
    ordered=True,
    comment="Test sequence",
)

test_sequence_minimal_template = Sequence(
    name="to_be_set",
)
