from .keyring import gpg
from .model import Boolean, Hole, Indeterminate, Number, Resource, Text, wrap
from .util import NoSuchPathException
from foyndation import dotpy
from importlib import import_module
from itertools import chain
import json, re, shlex

xmlentities = {c: f"&{w};" for c, w in [['"', 'quot'], ["'", 'apos']]}
tomlbasicbadchars = re.compile("[{}]+".format(re.escape(r'\"' + ''.join(chr(x) for x in chain(range(0x08 + 1), range(0x0A, 0x1F + 1), [0x7F])))))
zeroormoredots = re.compile('[.]*')

def _tomlquote(text):
    def repl(m):
        return ''.join(fr"\u{ord(c):04X}" for c in m.group())
    return f'"{tomlbasicbadchars.sub(repl, text)}"'

class OpaqueKey:

    @classmethod
    def isopaque(cls, key):
        return all(cls.isopaque(k) for k in key) if isinstance(key, tuple) else isinstance(key, cls)

def screenstr(scope, resolvable):
    'GNU Screen string literal.'
    return Text('"{}"'.format(re.sub(r'[\\\n"]', r'\\\g<0>', resolvable.resolve(scope).textvalue)))

def scstr(scope, resolvable):
    'SuperCollider string literal.'
    return Text('"{}"'.format(re.sub(r'[\\\n"]', r'\\\g<0>', resolvable.resolve(scope).textvalue)))

def hclstr(scope, resolvable):
    'HashiCorp configuration language string literal.'
    return Text('"{}"'.format(re.sub(r'[\\\n"]', r'\\\g<0>', resolvable.resolve(scope).textvalue)))

def groovystr(scope, resolvable):
    'Groovy string literal.'
    return Text("'{}'".format(re.sub(r"[\\\n']", r'\\\g<0>', resolvable.resolve(scope).textvalue)))

def pystr(scope, resolvable):
    'Python literal.'
    return Text(repr(resolvable.resolve(scope).scalar))

def shstr(scope, resolvable):
    'Shell string literal.'
    return Text(shlex.quote(resolvable.resolve(scope).textvalue))

def jsonquote(scope, resolvable):
    'JSON literal, also suitable for YAML.'
    return Text(json.dumps(resolvable.resolve(scope).scalar))

def xmlattr(scope, resolvable):
    'XML attribute literal (including quotes).'
    from xml.sax.saxutils import quoteattr
    return Text(quoteattr(resolvable.resolve(scope).textvalue)) # TODO: Support booleans.

def xmltext(scope, resolvable):
    'XML content, suggest assigning this to & with xmlattr assigned to " as is convention.'
    from xml.sax.saxutils import escape
    return Text(escape(resolvable.resolve(scope).textvalue, xmlentities))

def tomlquote(scope, resolvable):
    'TOML string literal.'
    return Text(_tomlquote(resolvable.resolve(scope).textvalue))

def urlquote(scope, resolvable):
    'Percent-encode all reserved characters.'
    from urllib.parse import quote
    return Text(quote(resolvable.resolve(scope).textvalue, safe = ''))

def map_(scope, objsresolvable, *args):
    '''If given 1 arg, evaluate it against every scope in `objsresolvable` and return that list.
    If given 2 args, the first is a variable name to which each scope is temporarily assigned.
    If given 3 args, the first two are variable names for scope key and scope respectively.'''
    from .scope import ScalarScope, Scope
    objs = objsresolvable.resolve(scope)
    parents = objs, scope
    if 1 == len(args):
        def context(k, v):
            try:
                resolvables = v.resolvables
            except AttributeError:
                s = ScalarScope(parents, v)
            else:
                s = Scope(parents)
                s.label = Text(k)
                for i in resolvables.items():
                    s.resolvables.put(*i)
            return s
        resolvable, = args
    elif 2 == len(args):
        def context(k, v):
            s = Scope(parents)
            s[vname,] = v
            return s
        vname, resolvable = args
        vname = vname.resolve(scope).textvalue
    else:
        def context(k, v):
            s = Scope(parents)
            s[kname,] = Text(k)
            s[vname,] = v
            return s
        kname, vname, resolvable = args
        kname = kname.resolve(scope).textvalue
        vname = vname.resolve(scope).textvalue
    result = Scope([])
    for k, v in objs.resolveditems():
        result.resolvables.put(k, resolvable.resolve(context(k, v)))
    return result

def map1(scope, contextresolvable, resultresolvable):
    'Like map, treating the given resolvable as the sole element in a collection and returning the resulting sole element instead of a collection.'
    from .scope import ScalarScope, Scope
    context = contextresolvable.resolve(scope)
    # FIXME: In scalar context case we need to propagate its resolve context.
    return resultresolvable.resolve(Scope([context, scope]) if hasattr(context, 'resolvables') else ScalarScope([scope], context))

def _flat(scope, listsresolvable):
    from .scope import Scope
    s = Scope([])
    for lk, l in listsresolvable.resolve(scope).resolveditems():
        for ok, obj in l.resolveditems():
            s.resolvables.put((lk, ok), obj)
    return s

def _label(scope):
    return scope.label

def join(scope, partsresolvable, sepresolvable = None):
    'Concatenate the given list, using optional separator. Frequently used with `map`.'
    return Join(scope, partsresolvable).execute(sepresolvable)

def str_(scope, resolvable):
    'Coerce to string.'
    return resolvable.resolve(scope).totext()

def list_(scope, *resolvables):
    'Create a list.'
    v = scope.createchild()
    for r in resolvables:
        v[OpaqueKey(),] = r
    return v

def _fork(scope):
    return scope.createchild()

def try_(scope, *resolvables):
    'Attempt to evaluate each resolvable, returning the first that succeeds.'
    for r in resolvables[:-1]:
        try:
            return r.resolve(scope)
        except NoSuchPathException:
            pass # XXX: Log it at a fine level?
    return resolvables[-1].resolve(scope)

def _mul(scope, *resolvables):
    x = 1
    for r in resolvables:
        x *= r.resolve(scope).scalar
    return Number(x)

def _div(scope, r, *resolvables):
    x = r.resolve(scope).scalar
    for r in resolvables:
        x /= r.resolve(scope).scalar
    return Number(x)

def _repr(scope, resolvable):
    return Text(repr(resolvable.resolve(scope).unravel()))

def hereslash(scope, *resolvables):
    'Join the given path components with the directory of the current resource.'
    return scope.resolved('here').slash((r.resolve(scope).textvalue for r in resolvables), False)

def readfile(scope, resolvable):
    'Include the content of the given path.'
    with resolvable.resolve(scope).openable(scope).open(False) as f:
        return Text(f.read())

def processtemplate(scope, resolvable):
    'Evaluate the content of the given path as an expression.'
    return resolvable.resolve(scope).openable(scope).processtemplate(scope)

def _lower(scope, resolvable):
    return Text(resolvable.resolve(scope).textvalue.lower())

def pyref(scope, moduleresolvable, qualnameresolvable): # FIXME: Allow load from __init__.py in current dir.
    'Python object in given module with given qualified name. Module may be relative to current resource, in which case assignment with `:=` is normally necessary. Typically used to import functions.'
    def moduleobj():
        moduleref = moduleresolvable.resolve(scope).textvalue
        leadingdots = len(zeroormoredots.match(moduleref).group())
        if not leadingdots:
            return import_module(moduleref)
        words = moduleref[leadingdots:].split('.')
        openable = scope.resolved('here').slash(['..'] * (leadingdots - 1) + words[:-1] + [words[-1] + dotpy], False)
        openablemodule = openable.modulenameornone()
        if openablemodule is not None:
            return import_module(openablemodule)
        class M:
            def __getattr__(self, name):
                return g[name]
        g = {} # XXX: Set __name__ so it can do its own relative imports?
        with openable.open(False) as f:
            exec(f.read(), g)
        return M()
    pyobj = moduleobj()
    for name in qualnameresolvable.resolve(scope).textvalue.split('.'):
        pyobj = getattr(pyobj, name)
    return wrap(pyobj)

def pyres(scope, packageresolvable, nameresolvable, encoding = Text('ascii')):
    'Python resource for inclusion with `.` directive.'
    return Resource(packageresolvable.resolve(scope).textvalue, nameresolvable.resolve(scope).textvalue, encoding.resolve(scope).textvalue)

def _not(scope, resolvable):
    return Boolean(not resolvable.resolve(scope).truth())

def _indentmorelines(scope, resolvable):
    indent = scope.resolved('indent').textvalue
    lines = resolvable.resolve(scope).textvalue.splitlines(True)
    return Text(''.join(chain(lines[:1], (indent + line for line in lines[1:]))))

def _hole(scope, resolvable):
    return Hole(Text(''), resolvable.resolve(scope).textvalue)

class Join:

    def __init__(self, scope, partsresolvable):
        self.i = (o for _, o in partsresolvable.resolve(scope).resolveditems())
        self.scope = scope

    def _load(self):
        try:
            self.obj = next(self.i)
            return True
        except StopIteration:
            pass

    def execute(self, sepresolvable):
        resobj = Indeterminate
        if self._load():
            resobj = resobj.plus(self.obj)
            if self._load():
                sepobj = Indeterminate if sepresolvable is None else sepresolvable.resolve(self.scope)
                while True:
                    resobj = resobj.plus(sepobj).plus(self.obj)
                    if not self._load():
                        break
        return resobj

def getimpl(scope, *resolvables):
    return scope.resolved(*(r.resolve(scope).textvalue for r in resolvables))

def corefunctions():
    yield 'gpg', gpg
    yield 'screenstr', screenstr
    yield 'scstr', scstr
    yield 'hclstr', hclstr
    yield 'groovystr', groovystr
    yield 'pystr', pystr
    yield 'shstr', shstr
    yield 'jsonquote', jsonquote
    yield 'xmlattr', xmlattr
    yield 'xmltext', xmltext
    yield 'tomlquote', tomlquote
    yield 'urlquote', urlquote
    yield 'map', map_
    yield 'map1', map1
    yield 'flat', _flat
    yield 'label', _label
    yield 'join', join
    yield 'str', str_
    yield 'list', list_
    yield 'fork', _fork
    yield 'try', try_
    yield 'mul', _mul
    yield 'div', _div
    yield 'repr', _repr
    yield './', hereslash
    yield 'readfile', readfile
    yield 'processtemplate', processtemplate
    yield 'lower', _lower
    yield 'pyref', pyref
    yield 'pyres', pyres
    yield '\N{NOT SIGN}', _not
    yield 'indentmorelines', _indentmorelines
    yield 'hole', _hole
    yield '', getimpl # TODO: Refer to the other one.
    yield 'get', getimpl
