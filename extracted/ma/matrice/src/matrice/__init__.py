"""Module providing __init__ functionality."""

import multiprocessing

from matrice_common.utils import dependencies_check

# Skip dependency installation in mp-children (spawned/forked workers
# re-import this module and rerunning pip would corrupt site-packages).
# Cross-process serialization between sibling main interpreters is handled
# inside `dependencies_check` itself.
if multiprocessing.parent_process() is None:
    dependencies_check(["requests", "Pillow"])
