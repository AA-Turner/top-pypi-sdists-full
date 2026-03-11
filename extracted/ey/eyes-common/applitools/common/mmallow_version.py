from __future__ import absolute_import, division, print_function


class LooseVersion(object):
    """Minimal replacement for deprecated distutils.version.LooseVersion"""

    def __init__(self, version):
        # type: (str) -> None
        self.version = tuple(int(c) for c in version.split("."))
