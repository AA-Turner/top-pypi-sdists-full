import importlib.machinery
import logging
import sys
import types
import urllib.parse
import urllib.request


log = logging.getLogger(__name__)


class HeadRequest(urllib.request.Request):
    def get_method(self):
        return 'HEAD'


class URLLoader(str):
    def load_module(self, fullname):
        url = self + fullname + '.py'
        resp = urllib.request.urlopen(url)
        co = compile(resp.read(), fullname, 'exec')
        module = sys.modules.setdefault(fullname, types.ModuleType(fullname))
        module.__file__ = url
        module.__loader__ = self
        exec(co, module.__dict__)
        return sys.modules[fullname]


class URLImporter(str):
    """
    Simple Importer that imports from the network
    """

    # interface.Provides(python_importer)

    def find_spec(self, fullname, path, target=None):
        if not self.endswith('/'):
            return

        req = HeadRequest(self + fullname + '.py')
        try:
            urllib.request.urlopen(req)
            log.debug("Found at %s", self)
            return importlib.machinery.ModuleSpec(fullname, loader=URLLoader(self))
        except Exception:
            pass

    def find_module(self, fullname, path=None):
        log.debug("Finding %s in %s", fullname, self)
        if not self.endswith('/'):
            return
        req = HeadRequest(self + fullname + '.py')
        try:
            urllib.request.urlopen(req)
            log.debug("Found at %s", self)
            return URLLoader(self)
        except Exception:
            pass

    @classmethod
    def install(cls):
        sys.path_hooks.append(cls.handles)

    @classmethod
    def remove(cls):
        sys.path_hooks.remove(cls.handles)

    @classmethod
    def handles(cls, path):
        path_p = urllib.parse.urlparse(path)
        if path_p.scheme in ('http', 'https'):
            return cls(path)
        raise ImportError(path)
