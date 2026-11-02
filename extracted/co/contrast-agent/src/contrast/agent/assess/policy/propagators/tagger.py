# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from . import BasePropagator


class Tagger(BasePropagator):
    """
    Propagation action that only applies tags/untags

    This is different from KEEP, which also copies tags from the source(s) to the target.
    """

    def propagate(self):
        return
