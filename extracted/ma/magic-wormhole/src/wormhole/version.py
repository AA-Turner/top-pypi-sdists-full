# this exists because hatch doesn't understand versioneer, except as
# the "code" thing .. but we have extra code in __init__.py which
# would require potentially all of our dependencies to be available at
# "install" time.
#
# so _just_ the version code is here so "hatch" can import
# "src/wormhole/version.py" and be happy.

from wormhole import _version
__version__ = _version.get_versions()['version']
