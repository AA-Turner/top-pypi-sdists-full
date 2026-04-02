import casefy


def check_type_to_ref(check_type: str) -> str:
    """
    Convert a check type like MLTableTimeZeroStatic to a reference string like ml_table_time
    """

    # Strip off the static identifier
    if check_type.endswith("Static"):
        check_type = check_type[:-6]

    return casefy.snakecase(check_type, keep_together=["ML"])
