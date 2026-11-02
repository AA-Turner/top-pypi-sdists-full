# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.propagators import SplatPropagator


class StarletteSafePathPropagator(SplatPropagator):
    """
    The purpose of this propagator is to SPLAT safe tags to the first element of the returned list from
    StaticFiles.lookup_path -> (full_path, os.stat(full_path))
    """

    def __init__(self, node, preshift, target):
        super(SplatPropagator, self).__init__(node, preshift, target)

        if isinstance(self.target, (tuple, list)):
            # First returned value of the list is the safely calculated path
            self.target = self.target[0]
