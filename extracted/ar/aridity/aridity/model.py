from .util import Burial
from contextlib import contextmanager
from foyndation import dotpy, Forkable, rmsuffix, singleton, solo
from importlib import import_module
from importlib.resources import files
from io import TextIOWrapper
from itertools import chain
from parabject import dereference, UnknownParabjectException
from pathlib import PurePath
import numbers, os, re

class Struct:

    def __eq__(self, that):
        if type(self) != type(that):
            return False
        if self.__dict__.keys() != that.__dict__.keys():
            return False
        for k, v in self.__dict__.items():
            if v != that.__dict__[k]:
                return False
        return True

    def __repr__(self):
        t = type(self)
        init = t.__init__.__code__
        args = ', '.join(repr(getattr(self, name)) for name in init.co_varnames[1:init.co_argcount])
        return f"{t.__name__}({args})"

class Resolvable(Struct):

    def resolve(self, scope):
        'Evaluate this expression against the given scope.'
        raise NotImplementedError

    def resolvemulti(self, j, scope):
        yield j, self.resolve(scope)

class Resolved(Resolvable):

    def resolve(self, scope):
        return self

nullmonitor = lambda text: None

class NegBuffer:

    def __init__(self):
        self.text = ''

    def insert(self, text):
        self.text = text + self.text

    def annihilate(self, obj):
        if not self.text:
            return obj
        text = obj.textvalue
        if not text:
            return obj
        k = min(len(self.text), len(text))
        assert self.text[:k] == text[:k]
        self.text = self.text[k:]
        return Text(text[k:])

    def propagate(self, obj):
        return Hole(obj, self.text) if self.text else obj

class Concat(Resolvable): # TODO: Ban in path components.

    ignorable = False

    @classmethod
    def smartpa(cls, s, l, t):
        return cls.unlesssingleton(t.asList())

    @classmethod
    def unlesssingleton(cls, v):
        return v[0] if 1 == len(v) else cls(v, nullmonitor)

    def __init__(self, parts, monitor):
        self.parts = parts
        self.monitor = monitor

    def resolve(self, scope):
        result = Indeterminate
        negbuffer = NegBuffer()
        for part in self.parts:
            obj = part.resolve(scope)
            try:
                negtext = obj.holevalue
            except AttributeError:
                negtext = ''
            else:
                obj = obj.prefix
            obj = negbuffer.annihilate(obj)
            result = result.plus(obj)
            try:
                text = obj.textvalue
            except AttributeError:
                pass
            else:
                self.monitor(text)
            negbuffer.insert(negtext)
        return negbuffer.propagate(result)

class BaseSimpleValue(Resolved):

    @classmethod
    def pa(cls, s, l, t):
        value, = t
        return cls(value)

    def unravel(self, listmode = None):
        return self.scalar

class Blank(BaseSimpleValue):

    ignorable = True
    boundary = False

    def __init__(self, textvalue):
        self.textvalue = textvalue

    def plus(self, that):
        return Text(self.textvalue + that.textvalue)

@singleton
class Boundary:

    ignorable = True
    boundary = True

class BaseScalar(BaseSimpleValue):

    ignorable = False

    def __hash__(self):
        return hash(self.scalar)

    def augment(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def __getattr__(self, name):
        raise self.attrerror(name)

    def attrerror(self, name):
        return AttributeError(f"{self} does not have: {name}")

class Scalar(BaseScalar):

    def __init__(self, scalar):
        self.scalar = scalar

class Text(BaseScalar, Forkable):

    @classmethod
    def joinpa(cls, s, l, t):
        return cls(''.join(t))

    @property
    def scalar(self):
        return self.textvalue

    @property
    def binaryvalue(self):
        if self.textvalue:
            raise self.attrerror('binaryvalue')
        return b''

    def __init__(self, textvalue):
        self.textvalue = textvalue

    def totext(self):
        return self

    def writeout(self, path):
        with open(path, 'w') as f:
            f.write(self.textvalue)

    def slash(self, words, rstrip):
        return self._of(os.path.join(os.path.dirname(self.textvalue) if rstrip else self.textvalue, *words))

    def openable(self, scope):
        if os.path.isabs(self.textvalue):
            return Locator(self.textvalue)
        o = scope.resolved('cwd').slash([self.textvalue], False)
        try:
            s = o.textvalue
        except AttributeError:
            return o
        return Locator(s)

    def plus(self, that):
        return self._of(self.textvalue + that.textvalue)

@singleton
class Indeterminate(BaseSimpleValue): # XXX: Base class needed?

    binaryvalue = b''
    textvalue = ''

    def plus(self, that):
        return that

    def totext(self):
        return Text('')

class ResidualHoleException(Exception): pass

class Hole(BaseScalar):

    @property
    def scalar(self):
        raise ResidualHoleException

    def __init__(self, prefix, holevalue):
        self.prefix = prefix
        self.holevalue = holevalue

class Openable:

    def openable(self, scope):
        return self

    @contextmanager
    def pushopen(self, scope):
        with scope.staticscope().here.push(self.slash([], True)), self.open(False) as f:
            yield f

    def source(self, scope, prefix):
        with self.pushopen(scope) as f, Burial.bumping(FileNotFoundError):
            Stream(f).source(scope, prefix)

    def processtemplate(self, scope):
        with self.pushopen(scope) as f:
            return Stream(f).processtemplate(scope)

class Locator(Resolved, Openable, Forkable):

    @property
    def scalar(self):
        return self.pathvalue

    def __init__(self, pathvalue):
        self.pathvalue = pathvalue

    def open(self, write):
        return open(self.pathvalue, 'w' if write else 'r')

    def slash(self, words, rstrip):
        return self._of(os.path.join(os.path.dirname(self.pathvalue) if rstrip else self.pathvalue, *words))

    def modulenameornone(self):
        pass

class Resource(Resolved, Openable, Forkable):

    def __init__(self, package_or_requirement, resource_name, encoding = 'ascii'):
        self.package_or_requirement = package_or_requirement
        self.resource_name = resource_name
        self.encoding = encoding

    def _packagename(self):
        m = import_module(self.package_or_requirement)
        package = m.__spec__.parent
        return (self.package_or_requirement if hasattr(m, '__path__') else self.package_or_requirement[:self.package_or_requirement.rindex('.')]) if package is None else package

    def _resource_words(self):
        return [] if self.resource_name is None else self.resource_name.split('/')

    @contextmanager
    def open(self, write):
        assert not write
        package = self._packagename()
        path = files(package)
        for name in self._resource_words():
            path /= name
        with path.open('rb') as f, TextIOWrapper(f, self.encoding) as g:
            yield g

    def slash(self, words, rstrip):
        v = list(chain(self._resource_words()[:-1 if rstrip else None], words))
        return self._of(self.package_or_requirement, '/'.join(v) if v else None, self.encoding)

    def modulenameornone(self):
        if (stem := rmsuffix(self.resource_name, dotpy)) is not None:
            return f"{self._packagename()}.{stem.replace('/', '.')}"

class Binary(BaseScalar, Forkable):

    @property
    def scalar(self):
        return self.binaryvalue

    def __init__(self, binaryvalue):
        self.binaryvalue = binaryvalue

    def writeout(self, path):
        with open(path, 'wb') as f:
            f.write(self.binaryvalue)

    def plus(self, that):
        return self._of(self.binaryvalue + that.binaryvalue)

class Number(BaseScalar):

    @property
    def scalar(self):
        return self.numbervalue

    def __init__(self, numbervalue):
        self.numbervalue = numbervalue

    def totext(self):
        try:
            text = self.textvalue
        except AttributeError:
            text = str(self.numbervalue) # TODO: Test this.
        return Text(text)

    def plus(self, that):
        return Text(self.textvalue + that.textvalue)

class Boolean(BaseScalar):

    @property
    def scalar(self):
        return self.booleanvalue

    def __init__(self, booleanvalue):
        self.booleanvalue = booleanvalue

    def truth(self):
        return self.booleanvalue

def star(scope, resolvable):
    raise Exception('Spread not implemented in this context.')

class Call(Resolvable):

    ignorable = False

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def _functionvalue(self, scope):
        return scope.resolved(self.name).functionvalue

    def resolve(self, scope):
        return self._functionvalue(scope)(scope.getresolvecontext(), *self.args)

    def resolvemulti(self, j, scope):
        f = self._functionvalue(scope.getresolvecontext())
        if star != f:
            yield j, f(scope, *self.args)
        else:
            for k, o in solo(self.args).resolve(scope).resolveditems(): # XXX: Support multiple args?
                yield (j, k), o

class Directive(Resolved):

    @property
    def scalar(self):
        return self.directivevalue

    def __init__(self, directivevalue):
        self.directivevalue = directivevalue

class Function(Resolved):

    @property
    def scalar(self):
        return self.functionvalue

    def __init__(self, functionvalue):
        self.functionvalue = functionvalue

    def unravel(self):
        return self.functionvalue

class Stream(Resolved):

    @property
    def scalar(self):
        return self.streamvalue

    def __init__(self, streamvalue):
        self.streamvalue = streamvalue

    def flush(self, text):
        self.streamvalue.write(text)
        self.streamvalue.flush()

    def source(self, scope, prefix):
        from .repl import CommandReader
        CommandReader(self.streamvalue, prefix).pipeto(scope)

    def processtemplate(self, scope):
        from .grammar import Parser
        with scope.staticscope().indent.push() as monitor:
            return Parser(monitor).readtemplate(self.streamvalue.read()).resolve(scope)

class Entry(Struct, Forkable):

    def __init__(self, resolvables):
        self.resolvables = resolvables

    def size(self):
        return sum(1 for r in self.resolvables if not r.ignorable)

    def words(self):
        return [r for r in self.resolvables if not r.ignorable]

    def topath(self, scope):
        return tuple(r.resolve(scope).totext().textvalue for r in self.resolvables if not r.ignorable)

    def subentry(self, i, j):
        v = list(self.resolvables)
        def trim(end):
            while v and v[end].ignorable:
                del v[end]
        n = self.size()
        while j < n:
            trim(-1)
            del v[-1]
            j += 1
        while i:
            trim(0)
            del v[0]
            i -= 1
        for end in 0, -1:
            trim(end)
        return Entry(v)

    def tophrase(self):
        return Concat.unlesssingleton(self.resolvables)

    def indent(self):
        indent = []
        for r in self.resolvables:
            if not r.ignorable or r.boundary:
                break
            indent.append(r.textvalue)
        return ''.join(indent)

    def plus(self, that):
        return self._of([*self.resolvables, *that.resolvables])

class MalformedEntryException(Exception): pass

class Suffix:

    def __init__(self, entry):
        self.indent = entry.indent()
        self.entry = entry

    def closing(self, contextindent):
        if any(x != y for x, y in zip(self.indent, contextindent)):
            raise MalformedEntryException(self.entry)
        return len(self.indent) <= len(contextindent)

def wrap(value):
    'Attempt to wrap the given value in a model object of the most specific type.'
    try:
        ctrl = dereference(value)
    except UnknownParabjectException:
        pass
    else:
        return ctrl.scope
    for b in map(bool, range(2)):
        if value is b:
            return Boolean(value)
    if isinstance(value, numbers.Number):
        return Number(value)
    if callable(value):
        return Function(value)
    if hasattr(value, 'encode'):
        return Text(value)
    return Scalar(value) # XXX: Interpret mappings and sequences?

quotablebysquare = re.compile('[$()]+')

def quote(obj): # TODO: Duplicates some wrap logic.
    for b in map(bool, range(2)):
        if obj is b:
            return str(b).lower()
    if isinstance(obj, PurePath):
        obj = str(obj)
    try:
        return f"""$.({quotablebysquare.sub(lambda m: f"$'[{m.group()}]", obj)})"""
    except TypeError:
        return obj
