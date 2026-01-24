##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from .basic_circuits import *
from .random import *

# Core test fixtures
core_tests = [
    "ghz",
    "unroll",
    "measure_x_as_subroutine",
] + random_fixtures

noop_tests = ["bernstein_vazirani_with_delay", "ghz_with_delay"]
