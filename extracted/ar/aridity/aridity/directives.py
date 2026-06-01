from .model import Stream
from .search import resolvedscopeornone
from .util import Burial
from itertools import chain
import logging, os, sys, unicodedata

log = logging.getLogger(__name__)

def acceptdirectivename(word):
    return word and unicodedata.category(word[0])[0] in 'PS'

def prime(d):
    def pd(prefix, suffix, scope):
        if not prefix.directives:
            return d(prefix, suffix, scope)
    return pd

def colon(prefix, suffix, scope):
    'Ignore rest of logical line.'
    return prefix

@prime
def _redirect(prefix, suffix, scope):
    scope['stdout',] = Stream(suffix.tophrase().resolve(scope).openable(scope).open(True))

@prime
def _write(prefix, suffix, scope):
    scope.resolved('stdout').flush(suffix.tophrase().resolve(scope).textvalue)

@prime
def source(prefix, suffix, scope):
    'Include path or resource at prefix.'
    # XXX: Use full algo to get phrasescope?
    def rootscopes():
        for s in chain.from_iterable(phrasescope.scopedepths()):
            if [staticscope] == s.parents: # XXX: Slow?
                yield s
    staticscope = scope.staticscope()
    phrasescope = scope
    wordresolvables = prefix.words()
    k = 0
    n = len(wordresolvables)
    for i, r in enumerate(wordresolvables):
        wordobj = r.resolve(scope)
        if staticscope.rootscopekey is wordobj.scalar:
            scope, = rootscopes()
            phrasescope = scope
            k = i + 1
            continue
        s = resolvedscopeornone(phrasescope, [wordobj.totext().textvalue])
        if s is None:
            break
        phrasescope = s
    with Burial.bumping(FileNotFoundError):
        openable = suffix.tophrase().resolve(phrasescope).openable(phrasescope)
    openable.source(scope, prefix.subentry(k, n))

@prime
def sourceifexists(prefix, suffix, scope):
    'Like `.` but allow the resource to be absent.'
    try:
        source(prefix, suffix, scope)
    except FileNotFoundError as e:
        if Burial.value(e):
            raise
        log.debug("Ignore absence: %s", e)

@prime
def _cd(prefix, suffix, scope):
    scope['cwd',] = suffix.tophrase().resolve(scope).openable(scope)

@prime
def _test(prefix, suffix, scope):
    sys.stderr.write(str(suffix.tophrase().resolve(scope)))
    sys.stderr.write(os.linesep)

@prime
def equals(prefix, suffix, scope):
    'Assign expression to path.'
    scope[prefix.topath(scope)] = suffix.tophrase()

@prime
def colonequals(prefix, suffix, scope):
    'Evaluate expression and assign result to path.'
    path = prefix.topath(scope)
    scope[path] = suffix.tophrase().resolve(scope.getorcreatesubscope(path[:-1]))

@prime
def plusequals(prefix, suffix, scope):
    'Assign expression to prefix plus an opaque key, i.e. add to list.'
    from .functions import OpaqueKey
    scope[prefix.topath(scope) + (OpaqueKey(),)] = suffix.tophrase()

@prime
def commaequals(prefix, suffix, scope):
    'Split expression on whitespace and make a list out of the parts.'
    from .functions import OpaqueKey
    basepath = prefix.topath(scope)
    scope.getorcreatesubscope(basepath)
    for r in suffix.words():
        scope[basepath + (OpaqueKey(),)] = r

@prime
def _cat(prefix, suffix, scope):
    scope = scope.getorcreatesubscope(prefix.topath(scope))
    scope.resolved('stdout').flush(suffix.tophrase().resolve(scope).openable(scope).processtemplate(scope).textvalue)

def coredirectives():
    yield ':', colon
    yield '!redirect', _redirect
    yield '!write', _write
    yield '.', source
    yield '.?', sourceifexists
    yield '!cd', _cd
    yield '!test', _test
    yield '=', equals
    yield ':=', colonequals
    yield '+=', plusequals
    yield ',=', commaequals
    yield '<', _cat
