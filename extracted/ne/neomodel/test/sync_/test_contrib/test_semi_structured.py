from test._async_compat import mark_sync_test

import pytest

from neomodel import (
    DeflateConflict,
    InflateConflict,
    IntegerProperty,
    StringProperty,
    db,
)
from neomodel.contrib import SemiStructuredNode


class UserProf(SemiStructuredNode):
    email = StringProperty(unique_index=True, required=True)
    age = IntegerProperty(index=True)


class Dummy(SemiStructuredNode):
    pass


@mark_sync_test
def test_to_save_to_model_with_required_only():
    u = UserProf(email="dummy@test.com")
    assert u.save()


@mark_sync_test
def test_save_to_model_with_extras():
    u = UserProf(email="jim@test.com", age=3, bar=99)
    u.foo = True
    assert u.save()
    u = UserProf.nodes.get(age=3)
    assert u.foo is True
    assert u.bar == 99


@mark_sync_test
def test_save_empty_model():
    dummy = Dummy()
    assert dummy.save()


@mark_sync_test
def test_inflate_conflict():
    class PersonForInflateTest(SemiStructuredNode):
        name = StringProperty()
        age = IntegerProperty()

        def hello(self):
            print("Hi my names " + self.name)

    # An ok model
    props = {"name": "Jim", "age": 8, "weight": 11}
    db.cypher_query("CREATE (n:PersonForInflateTest $props)", {"props": props})
    jim = PersonForInflateTest.nodes.get(name="Jim")
    assert jim.name == "Jim"
    assert jim.age == 8
    assert jim.weight == 11

    # A model that conflicts on `hello`
    props = {"name": "Tim", "age": 8, "hello": "goodbye"}
    db.cypher_query("CREATE (n:PersonForInflateTest $props)", {"props": props})
    with pytest.raises(InflateConflict):
        PersonForInflateTest.nodes.get(name="Tim")


@mark_sync_test
def test_save_with_injection_in_property_key():
    # A SemiStructuredNode lets arbitrary property keys through deflate. A key
    # crafted to break out of the SET clause must not be able to inject Cypher.
    malicious_key = "x` = 1 DETACH DELETE n //"
    u = UserProf(email="injection@test.com", age=42)
    setattr(u, malicious_key, "value")
    u.save()

    # The node must still exist (it was not DETACH DELETE-ed) and the malicious
    # key must have been stored verbatim as a property name.
    fetched = UserProf.nodes.get(email="injection@test.com")
    assert fetched.age == 42
    assert getattr(fetched, malicious_key) == "value"


@mark_sync_test
def test_deflate_conflict():
    class PersonForDeflateTest(SemiStructuredNode):
        name = StringProperty()
        age = IntegerProperty()

        def hello(self):
            print("Hi my names " + self.name)

    tim = PersonForDeflateTest(name="Tim", age=8, weight=11).save()
    tim.hello = "Hi"
    with pytest.raises(DeflateConflict):
        tim.save()
