import importlib
from importlib import abc
import sys
import os
import functools
import pathlib

def patchonimport(module_name=None):
    def decorator(target_function):
        sys.meta_path.insert(0, ImportModulePatch({module_name: target_function}))

        def wrapper(*args, **kwargs):
            target_function(*args, **kwargs)

        return wrapper

    return decorator


class ImportModulePatch(abc.MetaPathFinder, abc.Loader):
    def __init__(self, patch_modules):
        # type: (Dict[str, Callable[[Module], None]]) -> None
        self._patch_modules = patch_modules
        self._in_create_module = False

    def find_module(self, fullname, path=None):
        spec = self.find_spec(fullname, path)
        if spec is None:
            return None
        return spec

    def create_module(self, spec):
        try:
            self._in_create_module = True

            from importlib.util import find_spec, module_from_spec
            real_spec = importlib.util.find_spec(spec.name)

            real_module = module_from_spec(real_spec)
            real_spec.loader.exec_module(real_module)

            self._in_create_module = False
            return real_module
        except:
            return None

    def exec_module(self, module):
        try:
            _ = sys.modules.pop(module.__name__)
        except KeyError:
            print("module %s is not in sys.modules", module.__name__)
        sys.modules[module.__name__] = module
        globals()[module.__name__] = module
        self._patch_modules[module.__name__](module)

    def find_spec(self, fullname, path=None, target=None):
        if fullname not in self._patch_modules:
            return None
        if self._in_create_module:
            return None
        spec = importlib.machinery.ModuleSpec(fullname, self)
        return spec


class PatchesForRay(object):
    @staticmethod
    @patchonimport(module_name='botocore')
    def loader_patch(real_module):
        os.environ['AWS_DATA_PATH'] = str(pathlib.Path(__file__).parent)

# Importing base kernel after the patch so that botocore is patched on import
from ..glue_kernel_base.BaseKernel import BaseKernel


class GlueKernel(BaseKernel):
    implementation = "Python Glue Session"
    implementation_version = "1.0"
    language = "no-op"
    language_version = "0.1"
    language_info = {
        "name": "Python_Glue_Session",
        "mimetype": "text/x-python",
        "codemirror_mode": {"name": "python", "version": 3},
        "pygments_lexer": "python3",
        "file_extension": ".py",
    }
    session_language = "python"

    def __init__(self, **kwargs):
        self.request_origin = "GluePySparkKernel"
        super(GlueKernel, self).__init__(**kwargs)


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=GlueKernel)
