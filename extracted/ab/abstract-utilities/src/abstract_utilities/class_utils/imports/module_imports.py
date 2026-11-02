# Canonical class / caller helpers live in the stdlib-only core (abstract_essentials).
# The caller helpers are frame-walk based (no inspect.stack()), so lazily loaded
# dependencies are not forced to import.
from abstract_essentials import (
    SingletonMeta,
    prune_inputs,
    run_pruned_func,
)
from abstract_essentials.caller_utils import (
    _stack_files,
    get_initial_caller,
    get_initial_caller_path,
    get_initial_caller_dir,
    get_caller,
    get_caller_path,
    get_caller_dir,
    get_original_caller_dir,
)
