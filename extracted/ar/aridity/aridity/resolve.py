from .search import Query
from .util import CycleException, NoSuchPathException, TreeNoSuchPathException
from foyndation import Forkable

class BaseResolveContext:

    @property
    def label(self):
        return self.resolved().label

    @property
    def parents(self):
        return self.resolved().parents

    @property
    def resolvables(self):
        return self.resolved().resolvables

    def createchild(self):
        return self.resolved().createchild()

    def getresolvecontext(self):
        return self

    def resolvableornone(self, key):
        return self.resolved().resolvableornone(key)

    def staticscope(self):
        return self.resolved().staticscope()

class AnchorResolveContext(BaseResolveContext):

    def __init__(self, anchorscope):
        self.anchorscope = anchorscope

    def resolved(self, *path):
        hit = Query([], path).search(self.anchorscope)
        return hit.resolvable.resolve(ResolveContext(self.anchorscope, path, [hit.address]))

class ResolveContext(BaseResolveContext, Forkable):

    def __init__(self, anchorscope, exprpath, addresses):
        self.anchorscope = anchorscope
        self.scopepath = exprpath[:-1]
        self.exprpath = exprpath
        self.addresses = addresses

    def resolved(self, *path):
        try:
            hit = Query(self.scopepath, path).search(self.anchorscope)
            if hit.address in self.addresses: # XXX: Could it be valid to resolve the same address recursively with 2 different contexts?
                raise CycleException(path)
            return hit.resolvable.resolve(self._of(self.anchorscope, [*self.scopepath, *path], [*self.addresses, hit.address]))
        except NoSuchPathException as e:
            raise TreeNoSuchPathException(self.exprpath, [e])
