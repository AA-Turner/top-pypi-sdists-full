# This file helps PyLance/VS Code and mypy resolve imports for our PEP 420 namespace mistralai.workflows/plugins.
# By re-exporting from the core package, this approach works with both PyRight (VS Code) and mypy (CI).
# See: https://github.com/microsoft/pylance-release/issues/7618
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from mistralai.workflows.exports import *  # noqa: F403
from mistralai.workflows.exports import __all__ as __all__
