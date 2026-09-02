import sys
from ..conf import PLUGINS_DIR
from .importer import PluginImporter


### add plugins directory to sys.path
sys.path.insert(0, str(PLUGINS_DIR))

### Components Loader.
components_dir = PLUGINS_DIR.joinpath("components")
package_name = "flowtask.plugins.components"
try:
    sys.meta_path.append(PluginImporter(package_name, str(components_dir)))
except ImportError as exc:
    print(exc)

### Models Loader.
models_dir = PLUGINS_DIR.joinpath("models")
package_name = "flowtask.plugins.models"
try:
    sys.meta_path.append(PluginImporter(package_name, str(models_dir)))
except ImportError as exc:
    print('Model Error: ', exc)
