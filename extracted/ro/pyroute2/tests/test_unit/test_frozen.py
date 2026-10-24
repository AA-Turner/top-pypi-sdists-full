import importlib.util
from collections import OrderedDict
from pathlib import Path


SCRIPT = Path(__file__).parents[2] / 'pyroute2-frozen.py'
SPEC = importlib.util.spec_from_file_location('pyroute2_frozen', SCRIPT)
frozen_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(frozen_module)


class FakeObject(dict):
    def __init__(self, number):
        super().__init__(number=number, value='initial')
        self.key = OrderedDict((('number', number),))
        self.state = 'system'
        self.commits = 0
        self.rollbacks = 0
        self.snapshots = 0

    def snapshot(self):
        self.snapshots += 1
        return dict(self)

    def set(self, **values):
        self.update(values)
        return self

    def commit(self):
        self.commits += 1
        return self

    def rollback(self, snapshot):
        self.rollbacks += 1
        self.clear()
        self.update(snapshot)
        self.state = 'system'
        return self


class FakeView:
    def __init__(self):
        self.objects = []

    def getmany(self, selector):
        for obj in self.objects:
            if all(obj.get(key) == value for key, value in selector.items()):
                yield obj

    def __getitem__(self, record):
        return record


class FakeNDB:
    def __init__(self):
        self.interfaces = FakeView()


def test_nonexistent_objects_are_discovered_later():
    ndb = FakeNDB()
    frozen = frozen_module.Frozen(ndb, {'interfaces': [{'value': 'initial'}]})

    frozen.reconcile()
    assert frozen.objects == {}

    ndb.interfaces.objects.append(FakeObject(1))
    frozen.reconcile()
    assert len(frozen.objects) == 1


def test_partial_selector_snapshots_all_matches():
    ndb = FakeNDB()
    ndb.interfaces.objects.extend((FakeObject(1), FakeObject(2)))
    frozen = frozen_module.Frozen(ndb, {'interfaces': [{'value': 'initial'}]})

    frozen.reconcile()
    assert len(frozen.objects) == 2


def test_changed_object_is_restored():
    ndb = FakeNDB()
    obj = FakeObject(1)
    ndb.interfaces.objects.append(obj)
    frozen = frozen_module.Frozen(ndb, {'interfaces': [{'number': 1}]})
    frozen.reconcile()

    obj['value'] = 'changed'
    frozen.reconcile()

    assert obj['value'] == 'initial'
    assert obj.commits == 1


def test_disappeared_object_is_rolled_back():
    ndb = FakeNDB()
    obj = FakeObject(1)
    ndb.interfaces.objects.append(obj)
    frozen = frozen_module.Frozen(ndb, {'interfaces': [{'number': 1}]})
    frozen.reconcile()

    obj.state = 'invalid'
    frozen.reconcile()

    assert obj.state == 'system'
    assert obj.rollbacks == 1
    assert obj.snapshots == 2
