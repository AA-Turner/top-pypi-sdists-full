from .functions import OpaqueKey
from .model import Entry, Locator, Resource, Stream, wrap
from .scope import StaticScope
from .search import resolvedscopeornone
from .util import NoSuchPathException, selectentrypoints
from foyndation import dotpy, Forkable, rmsuffix
from io import StringIO
from parabject import Parabject, register
from pathlib import Path
import errno, logging, os, sys

log = logging.getLogger(__name__)

def _processmainfunction(mainfunction):
    module = mainfunction.__module__
    if '__main__' == module:
        p = Path(sys.argv[0])
        name = p.name
        if name in {'__init__.py', '__main__.py'}:
            stem = p.parent.name
        else:
            assert (stem := rmsuffix(name, dotpy)) is not None
        assert '-' not in stem
        appname = stem.replace('_', '-')
    else:
        attr = mainfunction.__qualname__
        # FIXME: Requires metadata e.g. egg-info in projects that have not been installed:
        appname, = (ep.name for ep in selectentrypoints('console_scripts') if ep.module == module and ep.attr == attr)
    return module, appname

def _wrappathorstream(pathorstream):
    return (Stream if getattr(pathorstream, 'readable', lambda: False)() else Locator)(pathorstream)

class ConfigCtrl(Forkable):
    'High level scope API.'

    if 'HOME' in os.environ:
        settingsopenable = Locator(Path.home() / '.settings.arid')

    @property
    def node(self):
        return register(self, Config)

    @property
    def r(self):
        'Get config object for reading, i.e. missing scopes will error.'
        return register(self, RConfig)

    @property
    def w(self):
        'Get config object for writing, i.e. missing scopes will be created.'
        return register(self, WConfig)

    def __init__(self, basescope = None, prefix = None):
        self.basescope = StaticScope.createchild() if basescope is None else basescope
        self.prefix = [] if prefix is None else prefix

    def loadappconfig(self, mainfunction, moduleresource, encoding = 'ascii', settingsoptional = False):
        'Using app name as prefix load config from the given resource, apply user settings, and return config object for app. Context module for loading resource and the app name are deduced from `mainfunction`, or these can be provided as a tuple. Set `settingsoptional` to suppress the usual error if ~/.settings.arid does not exist.'
        try:
            module_name, appname = mainfunction
        except TypeError:
            module_name, appname = _processmainfunction(mainfunction)
        appconfig = self._loadappconfig(appname, Resource(module_name, moduleresource, encoding))
        try:
            self.loadsettings()
        except (IOError, OSError) as e:
            if not (settingsoptional and errno.ENOENT == e.errno):
                raise
            log.info("No such file: %s", e)
        return appconfig

    def _loadappconfig(self, appname, resource):
        resource.source(self.basescope.getorcreatesubscope([*self.prefix, appname]), Entry([]))
        return getattr(self.node, appname)

    def load(self, pathorstream):
        'Execute config from the given path or stream.'
        _wrappathorstream(pathorstream).source(self.scope, Entry([]))

    def loadsettings(self):
        self.settingsopenable.source(self.scope, Entry([]))

    def execute(self, text):
        'Execute given config text.'
        self.load(StringIO(text))

    @property
    def scope(self):
        s = resolvedscopeornone(self.basescope, self.prefix)
        assert s is not None
        return s

    def __iter__(self): # TODO: Add API to get keys without resolving values.
        'Yield keys and values.'
        for k, o in self.resolve().resolveditems():
            try:
                yield k, o.scalar
            except AttributeError:
                yield k, self.addname(k).node

    def processtemplate(self, frompathorstream, topathorstream):
        'Evaluate expression from path/stream and write result to path/stream.'
        obj = _wrappathorstream(frompathorstream).processtemplate(self.resolve())
        if getattr(topathorstream, 'writable', lambda: False)():
            topathorstream.write(obj.textvalue if hasattr(topathorstream, 'encoding') else obj.binaryvalue)
        else:
            obj.writeout(topathorstream)

    def childctrl(self):
        return self._of(self.scope.createchild())

    def addname(self, name):
        return self._of(self.basescope, [*self.prefix, name])

    def resolve(self):
        return self.basescope.resolved(*self.prefix)

    def prefixrepr(self):
        return '.'.join(w if w.isidentifier() else repr(w) for w in self.prefix)

class Config(Parabject):

    def __getattr__(self, name):
        query = (-self).addname(name)
        try:
            obj = query.resolve() # TODO LATER: Guidance for how lazy non-scalars should be in this situation.
        except NoSuchPathException:
            raise AttributeError(query.prefixrepr())
        try:
            return obj.scalar
        except AttributeError:
            return query.node

    def __iter__(self):
        for _, o in -self:
            yield o

    def __setattr__(self, name, value):
        (-self).scope[name,] = wrap(value)

class RConfig(Parabject):

    def __getattr__(self, name):
        query = (-self).addname(name)
        try:
            obj = query.resolve()
        except NoSuchPathException:
            raise AttributeError(query.prefixrepr())
        try:
            return obj.scalar
        except AttributeError:
            return query.r

    def __iter__(self):
        'Yield values only. Iterate over `-self` for keys and values.'
        for _, o in (-self).resolve().resolveditems(): # TODO: Investigate how iteration should work.
            yield o.scalar

class WConfig(Parabject):

    def __getattr__(self, name):
        return (-self).addname(name).w

    def __setattr__(self, name, value):
        query = (-self).addname(name)
        query.basescope[tuple(query.prefix)] = wrap(value)

    def __iadd__(self, value):
        query = (-self).addname(OpaqueKey())
        query.basescope[tuple(query.prefix)] = wrap(value)
        return self

    def __neg__(self):
        query = super().__neg__()
        query.basescope.getorcreatesubscope(query.prefix) # TODO: Too eager.
        return query
