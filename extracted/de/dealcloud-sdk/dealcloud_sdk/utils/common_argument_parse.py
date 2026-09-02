def parse_output_argument(output: str):
    if output not in ["list", "pandas"]:
        raise AttributeError('output must be one of "list" or "pandas".')


def parse_lookup_column_argument(lookup_column: str, use_dealcloud_ids: bool):
    if not use_dealcloud_ids and not lookup_column:
        raise AttributeError(
            "if not using dealcloud ids for update, a lookup column must be defined."
        )
