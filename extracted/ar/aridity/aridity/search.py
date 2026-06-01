from .util import popattr, UnparseNoSuchPathException
from collections import namedtuple
from foyndation import inf
from itertools import islice
import heapq

def resolvedscopeornone(s, path):
    for name in path:
        r = s.resolvableornone(name)
        if r is None:
            return
        s = r.resolve(s)
        if not hasattr(s, 'resolvableornone'):
            return
    return s

class Address(namedtuple('BaseAddress', 'scope key')): pass

class Hit(namedtuple('BaseHit', 'depths address resolvable')):

    def naiveresolve(self):
        return self.resolvable if self.address is None else self.resolvable.resolve(self.address.scope) # XXX: Wise?

    def iterornone(self, word, inprefix):
        contextscope = self.naiveresolve()
        if hasattr(contextscope, 'resolvableornone'):
            return Iterator(self.depths, contextscope, word, inprefix)

    def shortcut(self, zerocount):
        return all(not d for d in islice(self.depths, len(self.depths) - zerocount, None))

class Iterable:

    def __iter__(self):
        return self.popiterator()

class Iterator(Iterable):

    def __init__(self, depths, contextscope, word, inprefix):
        def g():
            for depth, scopes in enumerate(contextscope.scopedepths()):
                for scope in scopes:
                    resolvable = scope.resolvableornone(word)
                    if resolvable is not None:
                        yield Hit(depths + [depth], Address(scope, word), resolvable)
            if inprefix:
                yield Hit(depths + [inf], None, contextscope)
        self.iterator = g()

    def next(self):
        return next(self.iterator)

    def popiterator(self):
        return popattr(self, 'iterator')

class Merge(Iterable):

    def __init__(self):
        self.iterables = []

    def add(self, iterable):
        self.iterables.append(iterable)

    def popiterator(self):
        return heapq.merge(*popattr(self, 'iterables'))

def _lt(*depthspair):
    for d1, d2 in zip(*map(reversed, depthspair)):
        if d1 < d2:
            return True
        if d1 > d2:
            break

class Query:

    def __init__(self, prefix, path):
        self.prefixlen = len(prefix)
        self.path = [*prefix, *path]

    def _search(self, scope):
        merges = [[Hit([], None, scope)], *(Merge() for _ in self.path)]
        size = len(self.path)
        for cursor, merge in enumerate(merges):
            zerocount = size - cursor
            yield None, zerocount
            for hit in merge:
                for x in range(cursor, size):
                    i = hit.iterornone(self.path[x], x < self.prefixlen)
                    if i is None:
                        break
                    try:
                        hit = i.next()
                    except StopIteration:
                        break
                    merges[1 + x].add(i)
                else:
                    yield hit, zerocount

    def findall(self, scope):
        for hit, _ in self._search(scope):
            if hit is not None:
                yield hit

    def search(self, scope):
        besthit = None
        for hit, zc in self._search(scope):
            if hit is None:
                if besthit is not None and besthit.shortcut(zc):
                    return besthit
            else:
                if hit.shortcut(zc):
                    return hit
                if besthit is None or _lt(hit.depths, besthit.depths):
                    besthit = hit
        raise UnparseNoSuchPathException(scope, self.path[:self.prefixlen], self.path[self.prefixlen:])
