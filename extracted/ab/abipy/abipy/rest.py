#!/usr/bin/env python

from pymatgen.core import Structure as pmg_Structure
from abipy.core import Structure
s = pmg_Structure.from_id("mp-149")
print(s)

s = Structure.from_mpid("mp-149")
print(s)
