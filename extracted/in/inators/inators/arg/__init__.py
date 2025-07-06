# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

"""
Helper functions to ensure uniform command-line arguments across tools.
"""

from .add_argument import add_argument
from .log_level_argument import add_log_level_argument, process_log_level_argument
from .sys_path_argument import add_sys_path_argument, process_sys_path_argument
from .sys_recursion_limit_argument import add_sys_recursion_limit_argument, process_sys_recursion_limit_argument
from .version_argument import add_version_argument
