from pkgutil import extend_path

# Extend __path__ to support namespace package discovery in editable installs.
#
# The `mistralai.workflows.plugins` subpackage is a PEP 420 implicit namespace package,
# allowing external packages to contribute plugins by creating:
#
#   their-package-on-pypi/mistralai.workflows/plugins/their_plugin/__init__.py
#
# PEP 420 namespaces work correctly for regular (non-editable) installs.
# However, editable installs may fail to properly merge namespace contributions.
#
# We solve this by explicitly calling extend_path(), which iterates through
# all entries in sys.path, checks if each contains a `mistralai.workflows/plugins`
# directory, and adds any it finds to __path__.
#
# Note that there are two mechanisms for editable installs, and our fix
# only works for the first:
#
# 1. Static .pth files that add directories to sys.path:
#    - uv build backend
#    - setuptools with src layout (default) or with editable_mode=compat
#    - hatchling
#    - flit (via pip install -e or flit install --pth-file)
#    - pdm-backend with editable-backend="path" (default)
#    - poetry-core
#
# 2. Import hooks via sys.meta_path (these do NOT work with extend_path):
#    - setuptools with flat layout (installs a custom finder)
#    - pdm-backend with editable-backend="editables"
#
# For case (2), there is no clean solution at the import level. The import
# hook intercepts imports before sys.path is searched, and extend_path()
# cannot discover paths that aren't in sys.path.
#
# In practice, most modern build backends default to static .pth files,
# so this workaround covers the majority of use cases.
#
# See also:
# - https://github.com/pypa/pip/issues/7265
# - PEP 420 (implicit namespace packages)
# - PEP 660 (editable installs)
__path__ = extend_path(__path__, __name__)

from .exports import *  # noqa: F403
from .exports import __all__ as __all__
