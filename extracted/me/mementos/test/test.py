from mementos import *
import sys
import pytest


def test_one():
    class Thing(with_metaclass(MementoMetaclass, object)):

        def __init__(self, name):
            self.name = name


    t1 = Thing("one")
    t2 = Thing("one")
    assert t1 is t2

    o1 = Thing("lovely")
    o2 = Thing(name="lovely")
    assert o1 is not o2   # because the call signature is different

    class OtherThing(with_metaclass(MementoMetaclass, object)):

        def __init__(self, name):
            self.name = name
            self.color = None
            self.weight = None

        def set(self, color=None, weight=None):
            self.color = color or self.color
            self.weight = weight or self.weight
            return self

    ot1 = OtherThing("one").set(color='blue')
    ot2 = OtherThing("one").set(weight='light')
    assert ot1 is ot2
    assert ot1.color == ot2.color == 'blue'
    assert ot1.weight == ot2.weight == 'light'


def test_simplified():
    class Thing(mementos):

        def __init__(self, name):
            self.name = name


    t1 = Thing("one")
    t2 = Thing("one")
    assert t1 is t2

    o1 = Thing("lovely")
    o2 = Thing(name="lovely")
    assert o1 is not o2   # because the call signature is different

    class OtherThing(with_metaclass(MementoMetaclass, object)):

        def __init__(self, name):
            self.name = name
            self.color = None
            self.weight = None

        def set(self, color=None, weight=None):
            self.color = color or self.color
            self.weight = weight or self.weight
            return self

    ot1 = OtherThing("one").set(color='blue')
    ot2 = OtherThing("one").set(weight='light')
    assert ot1 is ot2
    assert ot1.color == ot2.color == 'blue'
    assert ot1.weight == ot2.weight == 'light'


def test_tuple_subclass():

    class Fribble(object):
        def fribble(self):
            return 100

    class Frabble(object):
        def frabble(self):
            return 333

    class Complex(with_metaclass(MementoMetaclass, (Fribble, Frabble))):

        def __init__(self, name):
            self.name = name

    c = Complex('Joe')
    assert c.name == 'Joe'
    assert c.fribble() == 100
    assert c.frabble() -- 333

    c2 = Complex('Joe')
    assert c2 is c


def test_inline_with_metaclass():

    # Make sure you can do the metaclass specification directly.

    class Thing23(MementoMetaclass("NewBase", (object,), {})):

        def __init__(self, name):
            self.name = name


    t1 = Thing23("one")
    t2 = Thing23("one")
    assert t1 is t2

    o1 = Thing23("lovely")
    o2 = Thing23(name="lovely")
    assert o1 is not o2   # because the call signature is different


def test_id_metaclass():

    # Test the metaclass that uses the id of the first arg
    # but really as much a test of memento_factory, since IdMementoMetaclass not
    # part of base module

    IdMementoMetaclass = memento_factory("IdMementoMetaclass",
                                         lambda cls, args, kwargs: (cls, id(args[0])) )

    class IdTrack(with_metaclass(IdMementoMetaclass, object)):
        def __init__(self, name, *args):
            self.name = name
            self.args = args

    id1 = IdTrack("joe")
    id2 = IdTrack("joe")
    assert id1 is id2

    id3 = IdTrack("joe", 1, 4)
    assert id3 is id2

    id4 = IdTrack("Joe", 1, 4)
    id5 = IdTrack("Joe")
    assert id4 is id5
    assert id4 is not id3
    assert id5 is not id3


def test_id_metaclass_primitive():

    # Test the metaclass that uses the id of the first arg
    # but really as much a test of memento_factory, since IdMementoMetaclass not
    # part of base module

    IdMementoPrimitive = memento_factory("IdMementoMetaclass",
                                         lambda cls, args, kwargs: id(args[0]) )

    class IdTrackPrim(with_metaclass(IdMementoPrimitive, object)):
        def __init__(self, name, *args):
            self.name = name
            self.args = args

    id1 = IdTrackPrim("joe")
    id2 = IdTrackPrim("joe")
    assert id1 is id2

    id3 = IdTrackPrim("joe", 1, 4)
    assert id3 is id2

    id4 = IdTrackPrim("Joe", 1, 4)
    id5 = IdTrackPrim("Joe")
    assert id4 is id5
    assert id4 is not id3
    assert id5 is not id3


def test_metaclass_factory():

    mymeta = memento_factory("mymeta", lambda cls, args, kwargs: (cls, kwargs['b']))

    class BTrack(with_metaclass(mymeta, object)):
        def __init__(self, name, **kwargs):
            assert 'b' in kwargs
            self.name = name
            self.b = kwargs['b']

    b1 = BTrack('andy', b=1)
    b2 = BTrack('dave', b=1)
    assert b1 is b2
    assert b1.name == 'andy'  # because b1 got there first, defined object such that b=1

    b3 = BTrack('andy', b=2)
    assert b3 is not b1
    assert b3 is not b2
    assert b3.name == 'andy'


@pytest.mark.skipif("sys.version_info < (2,7)")
def test_hasher_signatures():
    # use inspect.getcallargs to make signatures that dont vary

    # alternate way of constructing hash key - seems more generally applicable

    from inspect import getcallargs
    from collections import Mapping, Iterable

    def hasher(c):
        """
        Return a hash for a collection, even if it's putatively unhashable (i.e.
        contains any dicts or lists). Does this by traversing the collection and
        accumulating the hash of its subvalues, then hashing a hashable
        collection of those sub-hashes. Works for basic types like strings,
        lists, dicts, and collections of same. Does not try to manage complex
        objects, unless they are already hashable. Works by hashing the current
        values; if the collection (or any sub-collection) is mutable and
        changes, the subsequent hasher() calls on the same object will return
        different values. Also, all collections of a given type (dict and OrderedDict,
        say, or list, tuple, and set) are collapsed to the same hash result.
        Whether this weaker, type-collapsing, value-oriented hash function
        suits your purposes will depend on the purposes.

        For canonicalizing call fingerprints for memoizing object creation, it
        works well, because such instantiation-time memoizing rarely needs to
        involve complex objects, and instantiation arguments are typically of
        simple-ish types (often literals), and they tend to crisply define the
        object's core 'identity'.

        If you need a slightly stronger version that differentiates dict from
        OrderedDict, say, you could create a variant that adds type(c) to the
        constructed tuple before returning the tuple hash.
        """
        try:
            return hash(c)
        except TypeError:
            if isinstance(c, Mapping):
                subhash = []
                for k in sorted(c.keys()):
                    subhash.append(hash(k))
                    subhash.append(hasher(c[k]))
                return hash(tuple(subhash))
            elif isinstance(c, Iterable):
                return hash(tuple(hasher(item) for item in c))
            else:
                raise TypeError('cant figure out ' + repr(c))

    def call_fingerprint(cls, args, kwargs):
        """
        Given a complex __init__ call with varied positional, keyward, variable,
        and variable keyword arguments, canonicalize the argument values and
        return a suitable hash key. NB this is suitable for cases where it is
        primarily the use of default values and keyword specification of args
        that might otherwise be given positionally that causes key signatures to
        vary, and in which the primary args (ie, not * or ** values) are simple
        scalars.
        """
        return hasher(getcallargs(cls.__init__, None, *args, **kwargs))

    Perfect2 = memento_factory("Perfect", call_fingerprint)

    class PerfectCall(with_metaclass(Perfect2, object)):
        def __init__(self, name, a=1, b=2, c=3, *args, **kwargs):
            self.vector = (name, a, b, c)

    p1 = PerfectCall('amy')
    p2 = PerfectCall('amy', b=2)
    p3 = PerfectCall('amy', c=3)
    p4 = PerfectCall('amy', c=3, a=1)
    p5 = PerfectCall(c=3, a=1, b=2, name='amy')
    assert p1 is p2
    assert p2 is p3
    assert p3 is p4
    assert p4 is p5

    p6 = PerfectCall('amy', b=33)
    assert p1 is not p6

    p7 = PerfectCall(**{'name': 'amy', 'b': 33})
    assert p6 is p7

    p8  = PerfectCall("bill", woot='more!', nixnax=3304)
    p9  = PerfectCall(**dict(woot='more!', nixnax=3304, name='bill'))
    p10 = PerfectCall(**dict([('nixnax', 3304), ('woot', 'more!'), ('name', 'bill')]))
    assert p8 is p9 is p10
