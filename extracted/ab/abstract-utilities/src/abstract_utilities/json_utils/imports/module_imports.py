from ...compare_utils import get_closest_match_from_list
from ...imports import make_list

# Canonical JSON / key helpers live in the stdlib-only core (abstract_essentials).
# This is the only place json_utils imports them from.
from abstract_essentials import (
    get_keys,
    make_key_map,
    find_keys,
    safe_json_dumps,
    try_json_loads,
    safe_json_loads,
    clean_invalid_newlines,
    read_malformed_json,
    get_value_from_path,
    find_paths_to_key,
    get_any_value,
    flatten_json,
    dump_if_json,
    validate_file_path,
    get_file_path,
    get_only_kwargs,
    get_desired_key_values,
    makeParams,
)
