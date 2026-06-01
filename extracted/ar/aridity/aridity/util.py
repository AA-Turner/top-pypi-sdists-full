from contextlib import contextmanager
from importlib.metadata import entry_points

class NoSuchPathException(Exception): pass

class UnparseNoSuchPathException(NoSuchPathException):

    @property
    def path(self):
        return self.args[-1]

    def __str__(self):
        return ' '.join(self.path)

class TreeNoSuchPathException(NoSuchPathException):

    def __str__(self):
        path, causes = self.args # XXX: Also collect (and show) where in the tree the causes happened?
        causestrtocount = {}
        for causestr in map(str, causes):
            try:
                causestrtocount[causestr] += 1
            except KeyError:
                causestrtocount[causestr] = 1
        lines = [' '.join(path)]
        for causestr, count in causestrtocount.items():
            causelines = causestr.splitlines()
            lines.append(f"{count}x {causelines[0]}")
            for l in causelines[1:]:
                lines.append(f"    {l}")
        return '\n'.join(lines)

class CycleException(UnparseNoSuchPathException): pass

class UnsupportedEntryException(Exception): pass

def selectentrypoints(group):
    obj = entry_points()
    try:
        select = obj.select
    except AttributeError:
        return obj[group]
    return select(group = group)

def popattr(obj, name):
    val = getattr(obj, name)
    delattr(obj, name)
    return val

class Burial:

    name = 'burial'

    @classmethod
    def value(cls, e):
        return getattr(e, cls.name, 0)

    @classmethod
    @contextmanager
    def bumping(cls, exctype):
        try:
            yield
        except exctype as e:
            setattr(e, cls.name, cls.value(e) + 1)
            raise
