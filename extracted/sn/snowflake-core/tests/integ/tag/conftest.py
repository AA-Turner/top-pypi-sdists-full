from snowflake.core.tag import Tag


test_tag_template = Tag(
    name="to_be_set",
    allowed_values=["value1", "value2", "value3"],
    comment="Test tag",
    # propagate and on_conflict are settable only on ENTERPRISE level accounts
)

test_tag_minimal_template = Tag(
    name="to_be_set",
)
