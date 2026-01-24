#!/usr/bin/env python

#--- !WARNING
s = """
---
src_file: mpi_setup.F90
src_line: 692
message: |
    The number of KPT processors, npkpt, should be a multiple of nkpt*nsppol.
    However, npkpt=2 and nkpt*nsppol=97
...
"""

from ruamel.yaml import YAML

yaml = YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
doc = yaml.load(s)

print(doc)
