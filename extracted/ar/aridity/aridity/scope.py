from .directives import acceptdirectivename, coredirectives, prime
from .functions import corefunctions, getimpl, OpaqueKey
from .model import Directive, Function, Hole, Resolvable, Scalar, star, Stream, Text
from .resolve import AnchorResolveContext
from .search import Query
from .stacks import IndentStack, SimpleStack, ThreadLocalResolvable
from .util import NoSuchPathException, UnsupportedEntryException
from foyndation import singleton, solo
from itertools import chain
import os, sys, threading

class NotAPathException(Exception): pass

class NotAResolvableException(Exception): pass

class Resolvables:

    def _proto(self):
        def allparents():
            scopes = [self.scope]
            while scopes:
                nextscopes = []
                for s in scopes:
                    for p in s.parents:
                        yield s, p
                        nextscopes.append(p)
                scopes = nextscopes
        revpath = []
        for s, parent in allparents():
            try:
                protoc = parent.resolvables.d[Star.protokey]
            except KeyError:
                pass
            else:
                try:
                    for component in reversed(revpath):
                        protoc = protoc.resolvables.d[component]
                except KeyError:
                    break
                return protoc.resolvables.d
            try:
                keyobj = s.label
            except AttributeError:
                break
            revpath.append(keyobj.scalar)
        return {}

    def __init__(self, scope):
        self.d = {}
        self.scope = scope

    def put(self, key, resolvable):
        self.d[key] = resolvable

    def getornone(self, key):
        try:
            return self.d[key]
        except KeyError:
            pass
        obj = self._proto().get(key)
        # FIXME LATER: Reads should be thread-safe, only create child if we're about to put something in it.
        return self.scope._putchild(key) if hasattr(obj, 'resolvables') else obj

    def items(self):
        for k, v in self.d.items():
            if Star.protokey != k:
                yield k, v
        for k, v in self._proto().items():
            if Star.protokey != k and k not in self.d:
                yield k, v

# XXX: Isn't this Resolved rather than Resolvable?
class Scope(Resolvable):

    nametypes = {str, type(None), OpaqueKey} # XXX: Is None still used by anything?

    def __init__(self, parents):
        self.resolvables = Resolvables(self)
        self.threadlocals = threading.local()
        self.parents = parents

    def __setitem__(self, path, resolvable):
        # TODO: Interpret non-tuple path as singleton.
        if not (tuple == type(path) and {type(name) for name in path} <= self.nametypes):
            raise NotAPathException(path)
        if not isinstance(resolvable, Resolvable):
            raise NotAResolvableException(resolvable)
        self.getorcreatesubscope(path[:-1]).resolvables.put(path[-1], resolvable)

    def getorcreatesubscope(self, path):
        for name in path:
            that = self.resolvables.getornone(name)
            if that is None:
                that = self._putchild(name)
            self = that
        return self

    def _putchild(self, key):
        child = self.createchild()
        # XXX: Deduce label to allow same Scope in multiple trees?
        child.label = Text(key) # TODO: Not necessarily str.
        self.resolvables.put(key, child)
        return child

    def duplicate(self):
        s = solo(self.parents).createchild()
        for k, v in self.resolvables.items():
            try:
                d = v.duplicate
            except AttributeError:
                pass
            else:
                v = d()
                v.label = Text(k)
            s.resolvables.put(k, v)
        return s

    def getresolvecontext(self):
        return AnchorResolveContext(self)

    def resolved(self, *path):
        'Follow the given path to get an expression, evaluate it (resolving any paths it requires, recursively), and return the resulting model object.'
        # TODO LATER: API to filter out results unsuitable for context.
        for s in chain.from_iterable(self.scopedepths()):
            obj = getimpl(s.getresolvecontext(), Text(''))
            try:
                g = obj.functionvalue
                break
            except AttributeError:
                pass
        return g(self.getresolvecontext(), *map(Text, path))

    def resolvableornone(self, key):
        return self.resolvables.getornone(key)

    def scopedepths(self):
        scopes = [self]
        while scopes:
            nextscopes = []
            for s in scopes:
                nextscopes.extend(s.parents)
            yield scopes
            scopes = nextscopes

    def unravel(self, listmode = 0):
        def g():
            args = [2] if 2 == listmode else []
            for k, o in self.resolveditems():
                yield k, o.unravel(*args)
        return [v for _, v in g()] if listmode else dict(g())

    def staticscope(self):
        for s in chain.from_iterable(self.scopedepths()):
            pass
        return s

    def execute(self, entry):
        directives = []
        for i, wordobj in enumerate(entry.words()):
            try:
                word = wordobj.textvalue
            except AttributeError:
                continue
            if not acceptdirectivename(word):
                continue
            try:
                resolvable = Query([], [word]).search(self).resolvable
            except NoSuchPathException:
                continue
            try:
                d = resolvable.directivevalue
            except AttributeError:
                continue
            directives.append((d, i))
        if not directives:
            raise UnsupportedEntryException(f"Expected at least one directive: {entry}")
        while directives:
            d, i = directives[-1]
            prefix = entry.subentry(0, i)
            prefix.directives = directives[:-1]
            e = d(prefix, entry.subentry(i + 1, entry.size()), self)
            if e is None:
                directives = prefix.directives
            else:
                entry = e
                directives = e.directives

    def __str__(self):
        def g():
            s = self
            while True:
                yield "{}{}".format(type(s).__name__, ''.join(f"{eol}\t{w} = {r!r}" for w, r in s.resolvables.items()))
                if not s.parents:
                    break
                s, = s.parents # FIXME: Support multiple parents.
        eol = '\n'
        return eol.join(g())

    def resolveditems(self):
        for k, r in self.resolvables.items():
            for t in r.resolvemulti(k, self):
                yield t

    def createchild(self):
        return Scope([self])

    def resolve(self, scope):
        return self

def _slashfunction(scope, *resolvables):
    path = None
    for r in reversed(resolvables):
        component = r.resolve(scope).textvalue
        path = component if path is None else os.path.join(component, path)
        if os.path.isabs(path):
            break
    return Text(os.path.join() if path is None else path)

class Slash(Text, Function):
    'As text, the platform slash. As function, join args using that slash, starting with the last absolute path (or using all args if all relative).'

    def __init__(self):
        Text.__init__(self, os.sep)
        Function.__init__(self, _slashfunction)

class Star(Function, Directive):

    protokey = object()

    def __init__(self):
        Function.__init__(self, star)
        Directive.__init__(self, prime(self._star))

    def _star(self, prefix, suffix, scope):
        scope.getorcreatesubscope(prefix.topath(scope) + (self.protokey,)).execute(suffix)

@singleton
class StaticScope(Scope):

    rootscopekey = OpaqueKey()
    stacktypes = dict(here = SimpleStack, indent = IndentStack)

    def __init__(self):
        super().__init__(())
        for word, d in coredirectives():
            self[word,] = Directive(d)
        for name, f in corefunctions():
            self[name,] = Function(f)
        self['~',] = Text(os.path.expanduser('~'))
        self['LF',] = Text('\n')
        self['EOL',] = Text(os.linesep)
        self['stdout',] = Stream(sys.stdout)
        self['/',] = Slash()
        self['*',] = Star()
        self['None',] = Scalar(None)
        self['eolhole',] = Hole(Text(''), '\n')
        self['^',] = Scalar(self.rootscopekey)
        for name in self.stacktypes:
            self[name,] = ThreadLocalResolvable(self.threadlocals, name)

    def __getattr__(self, name):
        threadlocals = self.threadlocals
        try:
            return getattr(threadlocals, name)
        except AttributeError:
            stack = self.stacktypes[name](name)
            setattr(threadlocals, name, stack)
            return stack

class ScalarScope(Scope):

    def __init__(self, parents, scalarobj):
        super().__init__(parents)
        self.scalarobj = scalarobj

    def __getattr__(self, name):
        return getattr(self.scalarobj, name)
