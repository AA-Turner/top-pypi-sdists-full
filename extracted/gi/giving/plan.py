_current = count(1)


class ObservablePlan:
    def __init__(self, *, parent=None, id=None, create_base=None):
        self.id = id
        self.create_base = create_base
        self.parent = parent
        self.operations = {}
        self.pipes = []
        self.subscribes = []

    def pipe(self, *args, **kwargs):
        id = next(_current)
        child = ObservablePlan(parent=self, id=id)
        self.operations[id] = (child, "pipe", args, kwargs)
        return child

    def subscribe(self, *args, **kwargs):
        self.operations[next(_current)] = (None, "subscribe", args, kwargs)

    def _instantiate(self, base, child_path=None):
        def _do(entry, child_path):
            (child, method, args, kwargs) = entry
            p = getattr(base, method)(*args, **kwargs)
            if child is not None:
                return child._instantiate(p, child_path)

        if child_path:
            child_id, *rest = child_path
            return _do(self.operations[child_id], rest)
        else:
            for id, entry in self.operations.items():
                _do(entry, None)
            return base

    def instantiate(self, child_path=()):
        if self.create_base is not None:
            base = self.create_base()
            return self._instantiate(base, child_path)
        else:
            return self.parent.instantiate((self.child_id, *child_path))

    def __enter__(self):
        if self.create_base is not None:
            base = self.create_base()
            return self.instantiate(base)
        else:
            return self.parent.instantiate()

    def __exit__(self, exc_type, exc, tb):
        pass


from contextlib import contextmanager
from itertools import count

from .api import given
from .gvn import ExtendedInterface

_current = count(1)


class ObservablePlan(ExtendedInterface):
    def __init__(self, *, parent=None, id=None, is_root=False):
        self.id = id
        self.is_root = is_root
        self.parent = parent
        self.operations = {}
        self.pipes = []
        self.subscribes = []
        self.instantiated = None

    ##################
    # Special piping #
    ##################

    def pipe(self, *args, **kwargs):
        id = next(_current)
        child = ObservablePlan(parent=self, id=id)
        self.operations[id] = (child, "pipe", args, kwargs)
        return child

    @contextmanager
    def values(self):
        with self as gv:
            results = gv.accum()
            yield results

    def subscribe(self, *args, **kwargs):
        self.operations[next(_current)] = (None, "subscribe", args, kwargs)

    def _instantiate(self, base, child_path=None):
        def _do(entry, child_path):
            (child, method, args, kwargs) = entry
            p = getattr(base, method)(*args, **kwargs)
            if child is not None:
                return child._instantiate(p, child_path)

        if child_path:
            child_id, *rest = child_path
            return _do(self.operations[child_id], rest)
        else:
            for id, entry in self.operations.items():
                _do(entry, None)
            return base

    def instantiate(self, child_path=()):
        if self.is_root:
            base = given()
            return base, self._instantiate(base.__enter__(), child_path)
        else:
            return self.parent.instantiate((self.id, *child_path))

    def run(self, fn, *args):
        base, _ = self.instantiate()
        fn(*args)
        base.__exit__(None, None, None)

    def __enter__(self):
        assert self.instantiated is None
        self.instantiated = self.instantiate()
        return self.instantiated[1]

        # if self.create_base is not None:
        #     base = self.create_base()
        #     self.instantiated = self._instantiate(base)
        # else:
        #     self.instantiated = self.parent.instantiate((self.id,))
        # return self.instantiated

    def __exit__(self, exc_type, exc, tb):
        self.instantiated[0].__exit__(exc_type, exc, tb)
        self.instantiated = None


def plan():
    return ObservablePlan(is_root=True)


from giving import give
from giving.plan import plan

from .test_operators import things


def test_plan_simple():
    pln = plan()

    with pln as gv:
        results = gv["?a"].accum()
        things(1, 2, 3)

    assert results == [1, 2, 3]


def test_plan_values():
    pln = plan()["?a"]

    with pln.values() as results:
        things(1, 2, 3)

    assert results == [1, 2, 3]

    with pln.values() as results:
        things(4, 5, 6)

    assert results == [4, 5, 6]


def test_plan_min():
    pln = plan()["?a"].min()

    with pln.values() as results:
        things(1, -2, 3)

    assert results == [-2]


def test_subplans():
    results = []

    def do():
        give(a=1)
        give(b="x")
        give(a=2)
        give(a=3)
        give(b="y")

    pln = plan()
    plna = pln["?a"]
    plnb = pln["?b"]
    plna.map(lambda a: a * a).subscribe(results.append)
    plnb.subscribe(results.append)

    pln.run(do)
    assert results == [1, "x", 4, 9, "y"]

    results.clear()
    plna.run(do)
    assert results == [1, 4, 9]

    results.clear()
    plnb.run(do)
    assert results == ["x", "y"]
