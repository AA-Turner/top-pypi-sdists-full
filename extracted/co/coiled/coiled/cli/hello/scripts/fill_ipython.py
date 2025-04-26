import pathlib
import sys

import IPython

import coiled
from coiled.utils import error_info_for_tracking

# Prepopulate first cell with code example
ip = IPython.get_ipython()
script = pathlib.Path(sys.argv[1]).resolve()
code = script.read_text()
ip.set_next_input(code)


# Log exceptions that happen in IPython
name = script.name.split(".")[0].replace("_", "-")


def exception_handler(self, etype, evalue, tb, tb_offset=None):
    coiled.add_interaction(f"cli-hello:example-{name}-error", success=False, **error_info_for_tracking(evalue))
    self.showtraceback((etype, evalue, tb), tb_offset=tb_offset)  # standard IPython error printing


ip.set_custom_exc((Exception,), exception_handler)
