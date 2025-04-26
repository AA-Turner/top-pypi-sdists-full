"""
Exported interface, when nbtoolbelt is imported as library

Copyright (c) 2017-2020 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.

.. data:: __version__

   Version number, as string

.. data:: version_info

   Version as tuple

.. data:: package_name

   Name of the ``nbtoolbelt`` package

.. data:: CELL_STATISTICS

   Tuple with the keys used in the dictionary returned by ``nb_cell_stats()``
"""

from ._version import __version__, package_name
from .counting import CELL_STATISTICS, nb_metadata, nb_other_metadata, nb_extra_fields, nb_cell_stats
from .printing import print_dict, print_set
from .running import run_nb

__all__ = [
    "__version__", "package_name",
    "CELL_STATISTICS",
    "nb_metadata", "nb_other_metadata", "nb_extra_fields", "nb_cell_stats",  # from counting
    "print_dict", "print_set",  # from printing
    "run_nb",  # from running
    ]
